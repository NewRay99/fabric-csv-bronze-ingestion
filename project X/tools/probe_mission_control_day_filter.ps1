param([int]$Port = 54939, [switch]$Assert, [switch]$UseLoadedModel, [string]$ProjectRoot)
$ErrorActionPreference = 'Stop'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
$taskDatabase = $taskServer.Databases[0]
$taskModel = $taskDatabase.Model
[pscustomobject]@{
    Database = $taskDatabase.ID
    Calendar = $taskModel.Tables['Load Calendar'].Partitions[0].State.ToString()
    Relationship = @($taskModel.Relationships | Where-Object { $_.ToTable.Name -eq 'Load Calendar' } | ForEach-Object {
        [pscustomobject]@{ Active = $_.IsActive; From = $_.FromColumn.Name; To = $_.ToColumn.Name; Direction = $_.CrossFilteringBehavior.ToString() }
    })
} | ConvertTo-Json -Depth 4
$taskCatalog = $taskDatabase.ID
$taskServer.Disconnect()
$taskAdomd = Join-Path $taskSdk 'adomd/lib/net8.0'
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
function Query($Name, $Dax) {
    $taskCommand = $taskConnection.CreateCommand()
    $taskCommand.CommandText = $Dax
    $taskReader = $taskCommand.ExecuteReader()
    $taskRows = @()
    while ($taskReader.Read()) {
        $taskRow = [ordered]@{}
        for ($i = 0; $i -lt $taskReader.FieldCount; $i++) {
            $taskValue = $taskReader.GetValue($i)
            $taskRow[$taskReader.GetName($i)] = if ($taskValue -is [DBNull]) { $null } else { $taskValue }
        }
        $taskRows += ,([pscustomobject]$taskRow)
    }
    $taskReader.Close()
    [pscustomobject]@{ Name = $Name; Rows = $taskRows } | ConvertTo-Json -Depth 6 | Write-Host
    return $taskRows
}
$taskRoot = if ($ProjectRoot) {$ProjectRoot} else {Join-Path (Split-Path $PSScriptRoot -Parent) 'reports/WIP/SM WMPP Mission Control v16'}
$taskPage = Join-Path $taskRoot 'SM WMPP Mission Control.Report/definition/pages/803165f7d2f5aaccd8ac'
$taskSource = Get-Content -LiteralPath (Join-Path $taskRoot 'SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl') -Raw
$taskDefinition = ''
if (-not $UseLoadedModel -and $taskSource -match "(?ms)^\tmeasure 'Day Explorer Job Visible' =\s*\r?\n(.*?)(?=^\t\tformatString:)") {
    $taskDefinition = "DEFINE MEASURE '_MissionControl_Measures'[Day Explorer Job Visible] = " + $Matches[1].Trim() + "`n"
}
$taskCases = @(
    @{ Name='Three jobs'; Dates='DATE(2026,10,1)'; ExpectedSingle=$true },
    @{ Name='Two jobs'; Dates='DATE(2026,10,6)'; ExpectedSingle=$true },
    @{ Name='One job'; Dates='DATE(2026,10,7)'; ExpectedSingle=$true },
    @{ Name='No loads'; Dates='DATE(2026,10,8)'; ExpectedSingle=$true },
    @{ Name='Latest default'; Dates=$null; ExpectedSingle=$false; ExpectedLatest=$true },
    @{ Name='Multiple days'; Dates='DATE(2026,10,6),DATE(2026,10,7)'; ExpectedSingle=$false }
)
$taskFailures = @()
try {
    $null = Query 'Calendar health' @'
EVALUATE ROW("Dates",COUNTROWS('Load Calendar'),"First",MIN('Load Calendar'[Date]),"Last",MAX('Load Calendar'[Date]),"Jobs",COUNTROWS(rpt_job_run_summary),"JobDates",DISTINCTCOUNT(rpt_job_run_summary[Run Date]))
'@
    foreach ($taskVisualId in @('3b28a42eb9ca129a560e','fe821948e1b3b2425852')) {
        $taskVisual = Get-Content -LiteralPath (Join-Path $taskPage "visuals/$taskVisualId/visual.json") -Raw | ConvertFrom-Json
        $taskIsGantt = $taskVisual.visual.visualType -like 'deneb*'
        $taskLabel = if ($taskIsGantt) {'Day Gantt'} else {'Register'}
        $taskProjections = @($taskVisual.visual.query.queryState.PSObject.Properties.Value.projections)
        $taskColumns = @($taskProjections | Where-Object {$_.field.Column} | ForEach-Object {
            $taskColumn = $_.field.Column
            "'" + $taskColumn.Expression.SourceRef.Entity.Replace("'","''") + "'[" + $taskColumn.Property.Replace(']',']]') + ']'
        })
        $taskMeasures = @($taskProjections | Where-Object {$_.field.Measure} | ForEach-Object {
            '"' + $_.nativeQueryRef.Replace('"','""') + '",[' + $_.field.Measure.Property.Replace(']',']]') + ']'
        })
        $taskGate = @($taskVisual.filterConfig.filters | Where-Object {$_.field.Measure.Property -eq 'Day Explorer Job Visible'}).Count -gt 0
        if ($taskGate -and -not @($taskProjections | Where-Object {$_.field.Measure.Property -eq 'Day Explorer Job Visible'}).Count) {
            $taskMeasures += '"Day Explorer Job Visible",[Day Explorer Job Visible]'
        }
        if ($taskIsGantt -and $taskGate) {
            $taskSpec = $taskVisual.visual.objects.vega[0].properties.jsonSpec.expr.Literal.Value
            if (-not $taskSpec.Contains("datum[''Day Explorer Job Visible''] == 1")) { throw 'Day Gantt is missing its datum filter.' }
        }
        foreach ($taskCase in $taskCases) {
            $taskDateFilter = if ($taskCase.Dates) { "TREATAS({" + $taskCase.Dates + "},'Load Calendar'[Date])" } else { $null }
            $taskArguments = @($taskColumns)
            if ($taskDateFilter) { $taskArguments += $taskDateFilter }
            $taskArguments += $taskMeasures
            $taskPredicate = if ($taskGate) { '[Day Explorer Job Visible] = 1' } elseif ($taskIsGantt) { '[Single calendar day] = 1' } else { 'TRUE()' }
            $taskExpected = if ($taskCase.ExpectedLatest) { 'COALESCE(COUNTROWS(TOPN(1,FILTER(rpt_job_run_summary,NOT ISBLANK(rpt_job_run_summary[started_at])),rpt_job_run_summary[started_at],DESC,rpt_job_run_summary[job_run_id],DESC)),0)' } elseif (-not $taskCase.ExpectedSingle) { '0' } else { "COALESCE(CALCULATE(COUNTROWS(rpt_job_run_summary),$taskDateFilter),0)" }
            $taskWrong = if ($taskCase.Dates) { "NOT(INT(rpt_job_run_summary[started_at]) IN {" + $taskCase.Dates + '})' } elseif ($taskCase.ExpectedLatest) { 'NOT(rpt_job_run_summary[job_run_id] IN SELECTCOLUMNS(TOPN(1,FILTER(ALL(rpt_job_run_summary),NOT ISBLANK(rpt_job_run_summary[started_at])),rpt_job_run_summary[started_at],DESC,rpt_job_run_summary[job_run_id],DESC),"Id",rpt_job_run_summary[job_run_id]))' } else { 'TRUE()' }
            $taskDax = $taskDefinition + @"
EVALUATE
VAR JobRows=SUMMARIZECOLUMNS($($taskArguments -join ','))
VAR VisibleRows=FILTER(JobRows,$taskPredicate && NOT ISBLANK(rpt_job_run_summary[started_at]))
RETURN ROW("VisibleJobs",COALESCE(COUNTROWS(VisibleRows),0),"ExpectedJobs",$taskExpected,"WrongDayJobs",COALESCE(COUNTROWS(FILTER(VisibleRows,$taskWrong)),0))
"@
            $taskResult = Query "$taskLabel / $($taskCase.Name)" $taskDax
            if ($taskResult[0].'[VisibleJobs]' -ne $taskResult[0].'[ExpectedJobs]' -or $taskResult[0].'[WrongDayJobs]' -gt 0) {
                $taskFailures += "$taskLabel / $($taskCase.Name)"
            }
        }
    }
    if ($taskFailures.Count) {
        Write-Output "FAIL: $($taskFailures -join '; ')"
        if ($Assert) { throw 'Day explorer includes jobs outside its selected day, or omits matching jobs.' }
    } else { Write-Output 'PASS: latest default and historical filtering in both Day explorer views, including empty and multiple-date selections.' }
} finally { $taskConnection.Close() }
