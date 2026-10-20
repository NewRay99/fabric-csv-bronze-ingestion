param([Parameter(Mandatory)][int]$Port,
      [Parameter(Mandatory)][string]$ProjectRoot,
      [Parameter(Mandatory)][string]$OutputDirectory)
$ErrorActionPreference = 'Stop'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskSource = [Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $ProjectRoot 'SM WMPP Mission Control.SemanticModel/definition'))
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
try {
    $taskDatabase = $taskServer.Databases[0]
    if (-not $taskDatabase.Model.Tables.ContainsName('cfg_table_load_metric')) {throw 'This is not the Mission Control model.'}
    if (@($taskDatabase.Model.Tables | ForEach-Object {$_.Partitions} | Where-Object {$_.Mode.ToString() -ne 'Import'}).Count) {throw 'Only imported cached data may be queried.'}
    $taskCatalog = $taskDatabase.ID
} finally {$taskServer.Disconnect()}
$taskAdomd = Join-Path $taskSdk 'adomd/lib/net8.0'
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
function Read-CachedDax([string]$Query) {
    $command = $taskConnection.CreateCommand()
    $command.CommandText = $Query
    $command.CommandTimeout = 45
    $reader = $command.ExecuteReader()
    $rows = [System.Collections.Generic.List[object]]::new()
    try {
        while ($reader.Read()) {
            $row = [ordered]@{}
            for ($i=0; $i -lt $reader.FieldCount; $i++) {
                $value = $reader.GetValue($i)
                $row[$reader.GetName($i).Trim('[',']')] = if ($value -is [DBNull]) {$null} else {$value}
            }
            $rows.Add([pscustomobject]$row)
        }
    } finally {$reader.Close()}
    return $rows.ToArray()
}
try {
    $taskRaw = @(Read-CachedDax @'
EVALUATE SELECTCOLUMNS(cfg_table_load_metric,
"Run",cfg_table_load_metric[run_id],"At",cfg_table_load_metric[recorded_at],
"Layer",cfg_table_load_metric[layer],"Kind",cfg_table_load_metric[source_kind],
"Source",cfg_table_load_metric[source_object],"Target",cfg_table_load_metric[target_object],
"Read",cfg_table_load_metric[rows_read],"Written",cfg_table_load_metric[rows_written])
'@)
    $taskDefinitions = [System.Collections.Generic.List[string]]::new()
    $taskDefinitions.Add('DEFINE')
    foreach ($label in @('Read','Written')) {
        foreach ($suffix in @('Previous','Delta','Delta %','Sparkline')) {
            $name = "Load Rows $label $suffix"
            $expression = $taskSource.Model.Tables['_MissionControl_Measures'].Measures[$name].Expression
            $taskDefinitions.Add("MEASURE '_MissionControl_Measures'[$name] = $expression")
        }
    }
    $taskQuery = ($taskDefinitions -join "`n") + @'

EVALUATE
VAR SampleLoads=TOPN(50,cfg_table_load_metric,cfg_table_load_metric[recorded_at],DESC,cfg_table_load_metric[run_id],DESC)
VAR Checked=ADDCOLUMNS(SampleLoads,
"PriorRead",[Load Rows Read Previous],"DeltaRead",[Load Rows Read Delta],"PercentRead",[Load Rows Read Delta %],
"PriorWritten",[Load Rows Written Previous],"DeltaWritten",[Load Rows Written Delta],
"ReadSparkline",[Load Rows Read Sparkline],"WrittenSparkline",[Load Rows Written Sparkline])
RETURN SELECTCOLUMNS(Checked,
"Run",cfg_table_load_metric[run_id],"At",cfg_table_load_metric[recorded_at],
"Layer",cfg_table_load_metric[layer],"Kind",cfg_table_load_metric[source_kind],
"Source",cfg_table_load_metric[source_object],"Target",cfg_table_load_metric[target_object],
"Read",cfg_table_load_metric[rows_read],"Written",cfg_table_load_metric[rows_written],
"PriorRead",[PriorRead],"DeltaRead",[DeltaRead],"PercentRead",[PercentRead],
"PriorWritten",[PriorWritten],"DeltaWritten",[DeltaWritten],
"ReadSparkline",[ReadSparkline],"WrittenSparkline",[WrittenSparkline])
'@
    $taskChecked = @(Read-CachedDax $taskQuery)
    # Additional fixture covers zero baselines, same-run archive loads, and grain isolation.
    $fixtureDefinitions = [System.Collections.Generic.List[string]]::new()
    $fixtureDefinitions.Add(@'
DEFINE TABLE 'Load History Fixture' = DATATABLE(
"run_id",STRING,"recorded_at",DATETIME,"layer",STRING,"source_kind",STRING,
"source_object",STRING,"target_object",STRING,"rows_read",INTEGER,"rows_written",INTEGER,
{{"r1",dt"2026-10-01","SILVER","LATEST","bronze.a","silver.a",0,0},
 {"r2",dt"2026-10-02","SILVER","LATEST","bronze.a","silver.a",10,9},
 {"r2",dt"2026-10-03","SILVER","LATEST","bronze.a","silver.a",15,14},
 {"r3",dt"2026-10-04","SILVER","LATEST","bronze.a","silver.a",0,0},
 {"archive",dt"2026-10-02","SILVER","ARCHIVE","bronze.a","silver.a",999,999},
 {"other",dt"2026-10-02","SILVER","LATEST","bronze.b","silver.b",888,888}})
'@)
    foreach ($label in @('Read','Written')) {
        foreach ($suffix in @('Previous','Delta','Delta %','Sparkline')) {
            $name = "Load Rows $label $suffix"
            $expression = $taskSource.Model.Tables['_MissionControl_Measures'].Measures[$name].Expression.Replace('cfg_table_load_metric', "'Load History Fixture'")
            $fixtureDefinitions.Add("MEASURE '_MissionControl_Measures'[$name] = $expression")
        }
    }
    $fixtureQuery = ($fixtureDefinitions -join "`n") + @'

EVALUATE SELECTCOLUMNS(ADDCOLUMNS('Load History Fixture',
"Prior",[Load Rows Read Previous],"Difference",[Load Rows Read Delta],"Percent",[Load Rows Read Delta %]),
"At",'Load History Fixture'[recorded_at],"Kind",'Load History Fixture'[source_kind],
"Target",'Load History Fixture'[target_object],"Prior",[Prior],"Delta",[Difference],"Percent",[Percent])
'@
    $fixtureChecked = @(Read-CachedDax $fixtureQuery)
    $sameRun = @($fixtureChecked | Where-Object {$_.At -eq [datetime]'2026-10-03' -and $_.Target -eq 'silver.a'})
    if ($sameRun[0].Prior -ne 10 -or $sameRun[0].Delta -ne 5) {throw 'Same-run retained loads must participate in the comparison.'}
    $zeroBaseline = @($fixtureChecked | Where-Object {$_.At -eq [datetime]'2026-10-02' -and $_.Kind -eq 'LATEST' -and $_.Target -eq 'silver.a'})
    if ($zeroBaseline[0].Delta -ne 10 -or $null -ne $zeroBaseline[0].Percent) {throw 'Incorrect zero-baseline handling.'}
    if (@($fixtureChecked | Where-Object {($_.Kind -eq 'ARCHIVE' -or $_.Target -eq 'silver.b') -and $null -ne $_.Prior}).Count) {throw 'Load-history grains were mixed.'}
    # Query-scoped definitions exercise the future domain schema without modifying
    # cached data or adding columns to the user's open model.
    $domainDefinitions = [System.Collections.Generic.List[string]]::new()
    $domainDefinitions.Add('DEFINE')
    $domainDefinitions.Add('TABLE ''Domain History View'' = DATATABLE("Mode",STRING,{{"Latest version"},{"All retained versions"}})')
    $domainDefinitions.Add('COLUMN cfg_data_domain[change_type] = "BASELINE"')
    $domainDefinitions.Add('COLUMN cfg_data_domain[profile_status] = "PROFILED"')
    foreach ($name in @('Discovery cfg_data_domain Rows','Discovery cfg_data_domain Scope count',
                        'Discovery cfg_data_domain Distinct objects','Discovery cfg_data_domain Discovery batches',
                        'Domain values Added','Domain values Removed','Domain value changes',
                        'Discovery cfg_data_domain Context','Discovery domains calendar changes')) {
        $expression = $taskSource.Model.Tables['_MissionControl_Measures'].Measures[$name].Expression
        $domainDefinitions.Add("MEASURE '_MissionControl_Measures'[$name] = $expression")
    }
    $domainQuery = ($domainDefinitions -join "`n") + @'

EVALUATE UNION(ROW("Mode","Latest","Retained",[Discovery cfg_data_domain Rows],
"ProfiledColumns",[Discovery cfg_data_domain Scope count],
"Added",[Domain values Added],"Removed",[Domain values Removed],
"Context",[Discovery cfg_data_domain Context],"Changes",[Domain value changes]),
CALCULATETABLE(ROW("Mode","All versions","Retained",[Discovery cfg_data_domain Rows],
"ProfiledColumns",[Discovery cfg_data_domain Scope count],
"Added",[Domain values Added],"Removed",[Domain values Removed],
"Context",[Discovery cfg_data_domain Context],"Changes",[Domain value changes]),
TREATAS({"All retained versions"},'Domain History View'[Mode])),
CALCULATETABLE(ROW("Mode","Empty day","Retained",[Discovery cfg_data_domain Rows],
"ProfiledColumns",[Discovery cfg_data_domain Scope count],
"Added",[Domain values Added],"Removed",[Domain values Removed],
"Context",[Discovery cfg_data_domain Context],"Changes",[Domain value changes]),
TREATAS({DATE(2099,1,1)},'Load Calendar'[Date])))
'@
    $domainChecked = @(Read-CachedDax $domainQuery)
    if ($domainChecked[0].Added -gt 0 -or $domainChecked[0].Removed -gt 0) {throw 'A legacy baseline must not imply additions or removals.'}
    $domainEmpty = @($domainChecked | Where-Object {$_.Mode -eq 'Empty day'})
    if ($domainEmpty.Count -ne 1 -or $domainEmpty[0].Retained -ne 0) {throw 'An empty history day must show zero rows.'}
    $domainAll = @($domainChecked | Where-Object {$_.Mode -eq 'All versions'})
    if ($domainAll[0].Context -ne 'All retained discovery versions') {throw 'The all-versions selector did not reach the measures.'}
    $taskPriorCount = 0
    $taskSvgCount = 0
    New-Item -ItemType Directory -Path $OutputDirectory -Force | Out-Null
    foreach ($row in $taskChecked) {
        $prior = @($taskRaw | Where-Object {
            $_.Layer -eq $row.Layer -and $_.Kind -eq $row.Kind -and $_.Source -eq $row.Source -and $_.Target -eq $row.Target -and
            ($_.At -lt $row.At -or ($_.At -eq $row.At -and $_.Run -lt $row.Run))
        } | Sort-Object @{Expression='At';Descending=$true},@{Expression='Run';Descending=$true} | Select-Object -First 1)
        if ($prior.Count) {$taskPriorCount++}
        foreach ($label in @('Read','Written')) {
            $expected = if ($prior.Count) {$prior[0].$label} else {$null}
            if ($row."Prior$label" -ne $expected) {throw "Incorrect prior $label count for $($row.Target)."}
            $delta = if ($null -ne $expected -and $null -ne $row.$label) {$row.$label - $expected} else {$null}
            if ($row."Delta$label" -ne $delta) {throw "Incorrect $label delta for $($row.Target)."}
            if ($row."${label}Sparkline") {
                $svg = [uri]::UnescapeDataString($row."${label}Sparkline".Substring('data:image/svg+xml;utf8,'.Length))
                $xml = [xml]$svg
                $points = @($xml.svg.polyline.points -split ' ')
                if ($points.Count -gt 12 -or $points.Count -lt 1 -or $svg -match 'NaN|Infinity') {throw 'Invalid sparkline geometry.'}
                if ($taskSvgCount -eq 0) {$svg | Set-Content -LiteralPath (Join-Path $OutputDirectory 'load-history-sparkline.svg') -Encoding utf8}
                $taskSvgCount++
            }
        }
        $percent = if ($null -ne $row.PriorRead -and $row.PriorRead -ne 0) {$row.DeltaRead / $row.PriorRead} else {$null}
        if ($null -eq $percent) {
            if ($null -ne $row.PercentRead) {throw 'A missing or zero baseline must have a blank percentage.'}
        } elseif ([Math]::Abs($row.PercentRead - $percent) -gt 0.00000001) {throw 'Incorrect read percentage.'}
    }
    $result = [ordered]@{Status='PASS';CachedHistoryRows=$taskRaw.Count;CheckedLoadRows=$taskChecked.Count;
        RowsWithPriorLoad=$taskPriorCount;ValidSparklines=$taskSvgCount;
        DomainFormulaChecks=$domainChecked;LoadBoundaryFixtureRows=$fixtureChecked.Count;
        SourceRefresh='None';ModelChanges='None'}
    $result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $OutputDirectory 'load-history-validation.json') -Encoding utf8
    $result | ConvertTo-Json
} finally {$taskConnection.Close()}
