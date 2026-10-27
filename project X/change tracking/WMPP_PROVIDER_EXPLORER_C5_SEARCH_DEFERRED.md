# WMPP Provider Explorer C5 search deferred implementation

Status: Deferred at the user's request on 25 October 2026. This is a saved proposal, not an implemented workbook feature. Implement only when the user is ready and authorises the change again.

The proposed change makes cell C5 on Provider Explorer select one provider across PivotTables connected to a shared provider-name slicer. Use the latest client workbook containing the PivotTables the user has built, rather than an earlier layout-only copy.

## Scope and behaviour

- Search runs when the user commits an edit in C5, for example by pressing Enter. It is not a per-keystroke search.
- Match the full provider name first, ignoring case and outer spaces. Otherwise accept a partial name only when it matches one provider.
- Set the shared slicer's selection to that one provider, and replace C5 with its full name.
- Blank, unmatched or ambiguous searches leave the existing provider selection unchanged. Clearing C5 must not select every provider.
- Keep the existing row-visibility measures and greater-than-zero filters.
- Do not call Refresh All from the event. Applying the slicer can still cause connected queries to run; this proposal does not resolve existing query-performance problems.
- Do not change the published semantic model, credentials, permissions or row-level security.

## Before implementation

1. Obtain and back up the latest working client workbook. Confirm the original connected PivotTable refreshes under the client's authorised WMPP account.
2. Confirm the client permits this VBA macro. If policy blocks it, obtain IT review or approval rather than weakening macro security.
3. Save a separate Excel Macro-Enabled Workbook copy with the .xlsm extension. Do not replace the working .xlsx backup.
4. Use one shared provider-name slicer based on dim_provider[provider_name]. In Slicer > Report Connections, connect every applicable Explorer PivotTable, including the selected-provider count. Resolve any missing PivotTable connection first.
5. Avoid independent manual provider-name filters on individual PivotTables, which can intersect with the shared selector. Retain row-visibility filters and other intentional report filters.
6. Keep C5 outside PivotTable output and editable if the sheet is protected. Protection and refresh behaviour require testing for this Power BI/OLAP connection.

The proposed code has not been run against the client workbook or its live Power BI connection. Multiple separate active slicer caches for the provider-name hierarchy cause it to stop rather than silently filter only part of the workbook.

## Add the worksheet event when authorised

1. Press Alt+F11, then Ctrl+R to display the VBA project list.
2. In the correct workbook, expand Microsoft Excel Objects.
3. Double-click the worksheet entry ending in (Provider Explorer).
4. Paste the code below into its blank code window, not ThisWorkbook or a standard Module. If code already exists, merge it carefully. Do not replace existing procedures or create a second Worksheet_Change procedure.

```vb
Option Explicit

Private Sub Worksheet_Change(ByVal Target As Range)

    Dim candidate As SlicerCache
    Dim providerCache As SlicerCache
    Dim item As SlicerItem
    Dim selectedItem As SlicerItem
    Dim exactMatches As Collection
    Dim partialMatches As Collection
    Dim matches As Collection
    Dim searchText As String
    Dim cacheCount As Long
    Dim eventsWereOn As Boolean

    eventsWereOn = Application.EnableEvents
    On Error GoTo SearchFailed

    'Only respond to a single-cell edit in C5.
    If Intersect(Target, Me.Range("C5")) Is Nothing Then Exit Sub
    If Target.CountLarge <> 1 Then Exit Sub
    If IsError(Target.Value2) Then Exit Sub

    searchText = Trim$(CStr(Me.Range("C5").Value2))

    'A blank search must not select every provider.
    If Len(searchText) = 0 Then Exit Sub

    Application.EnableEvents = False

    'Find the Power BI provider-name slicer cache.
    For Each candidate In Me.Parent.SlicerCaches
        If candidate.OLAP Then
            If StrComp(candidate.SourceName, _
                       "[dim_provider].[provider_name]", _
                       vbTextCompare) = 0 Then

                If candidate.Slicers.Count > 0 Then
                    cacheCount = cacheCount + 1
                    Set providerCache = candidate
                End If
            End If
        End If
    Next candidate

    If cacheCount = 0 Then
        Err.Raise vbObjectError + 1001, "Provider search", _
            "No provider-name slicer was found. Create a slicer " & _
            "using dim_provider[provider_name] first."
    End If

    If cacheCount > 1 Then
        Err.Raise vbObjectError + 1002, "Provider search", _
            "More than one provider slicer cache was found. " & _
            "The search needs one shared provider selector."
    End If

    Set exactMatches = New Collection
    Set partialMatches = New Collection

    For Each item In _
        providerCache.SlicerCacheLevels(1).SlicerItems

        If StrComp(Trim$(item.Caption), searchText, _
                   vbTextCompare) = 0 Then
            exactMatches.Add item
        End If

        If InStr(1, item.Caption, searchText, _
                 vbTextCompare) > 0 Then
            partialMatches.Add item
        End If
    Next item

    'Prefer an exact name over partial matches.
    If exactMatches.Count > 0 Then
        Set matches = exactMatches
    Else
        Set matches = partialMatches
    End If

    Select Case matches.Count

        Case 0
            MsgBox "No matching provider was found." & vbCrLf & _
                   "The provider selection has not changed.", _
                   vbInformation, "Provider search"

        Case 1
            Set selectedItem = matches.Item(1)

            'Apply the existing Power BI member identifier.
            providerCache.VisibleSlicerItemsList = _
                Array(selectedItem.Name)

            'Display the complete selected name as text.
            Me.Range("C5").NumberFormat = "@"
            Me.Range("C5").Value2 = selectedItem.Caption

        Case Else
            MsgBox CStr(matches.Count) & _
                   " providers match that search." & vbCrLf & _
                   "Enter more of the name, or the full name." & _
                   vbCrLf & _
                   "The provider selection has not changed.", _
                   vbInformation, "Provider search"

    End Select

CleanExit:
    Application.EnableEvents = eventsWereOn
    Exit Sub

SearchFailed:
    MsgBox "Provider search could not complete:" & vbCrLf & _
           Err.Description & vbCrLf & vbCrLf & _
           "Check the provider slicer's current selection " & _
           "before using the results.", _
           vbExclamation, "Provider search"
    Resume CleanExit

End Sub
```

## Client validation before release

1. In the VBA editor, select Debug > Compile VBAProject. Resolve any compilation error before proceeding.
2. Return to Excel with Alt+Q and save the .xlsm copy.
3. Enter a known provider's full name in C5 and press Enter. Confirm the slicer selects it, C5 displays its full name, and every connected Explorer PivotTable responds.
4. Repeat with a unique partial name and a different provider. Compare representative messages, offers and counts against Power BI under the same filters.
5. Test a blank search, a name with no match, and a partial name with several matches. Confirm each leaves the selected provider unchanged and does not query every provider.
6. Check for independent filters that leave old provider criteria on individual PivotTables.
7. Save, close and reopen. Verify normal macro approval, Power BI authentication and worksheet protection behaviour on the client workstation.
8. Confirm an error restores Application.EnableEvents and check the slicer's actual selection before using results after a failed search.

## Microsoft references

- [Save your workbook](https://support.microsoft.com/en-us/excel/save-your-workbook)
- [Shared slicer connections](https://support.microsoft.com/en-us/excel/get-started/use-slicers-to-filter-data)
- [Worksheet.Change event](https://learn.microsoft.com/en-us/office/vba/api/excel.worksheet.change)
- [OLAP slicer filter list](https://learn.microsoft.com/en-us/office/vba/api/excel.slicercache.visiblesliceritemslist)
- [Macro security settings](https://support.microsoft.com/en-us/excel/change-macro-security-settings-in-excel)
