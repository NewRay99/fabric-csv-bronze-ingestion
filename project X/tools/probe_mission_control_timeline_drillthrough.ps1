# Read-only regression checks against the loaded Desktop model. Libraries come
# from Microsoft's public AnalysisServices and AdomdClient NuGet packages.
param([int]$Port = 54939)
$ErrorActionPreference = 'Stop'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
$taskCatalog = $taskServer.Databases[0].ID
$taskServer.Disconnect()
$taskAdomd = Join-Path $taskSdk 'adomd/lib/net8.0'
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
$taskRoot = Join-Path (Split-Path $PSScriptRoot -Parent) 'reports/WIP/SM WMPP Mission Control v16/SM WMPP Mission Control.Report/definition/pages'
$taskPage = Join-Path $taskRoot 'ed27e90d06816c7c1eee'
$taskBinding = (Get-Content -LiteralPath (Join-Path $taskPage 'page.json') -Raw | ConvertFrom-Json).pageBinding
# Desktop omits default values when saving. Microsoft's page schema defaults
# an absent acceptsFilterContext to Default (flow the current filters).
$taskAcceptsContext = if ($taskBinding.acceptsFilterContext) {$taskBinding.acceptsFilterContext} else {'Default'}
if ($taskBinding.type -ne 'Drillthrough' -or $taskAcceptsContext -ne 'Default' -or
    $taskBinding.parameters[0].fieldExpr.Column.Expression.SourceRef.Entity -ne 'Load Calendar' -or
    $taskBinding.parameters[0].fieldExpr.Column.Property -ne 'Date') { throw 'Drillthrough does not pass calendar Date and current filters.' }
$taskCases = @(
    @{ Name='Default latest load'; Filters=@(); Latest=$true },
    @{ Name='Older day outside 14 days'; Filters=@("TREATAS({DATE(2026,8,24)},'Load Calendar'[Date])") },
    @{ Name='Recent day'; Filters=@("TREATAS({DATE(2026,10,1)},'Load Calendar'[Date])") },
    @{ Name='No loads'; Filters=@("TREATAS({DATE(2026,10,8)},'Load Calendar'[Date])") },
    @{ Name='Day and pipeline'; Filters=@("TREATAS({DATE(2026,8,24)},'Load Calendar'[Date])", "TREATAS({`"90_run_live_pipeline`"},rpt_job_run_summary[pipeline_name])") },
    @{ Name='No matching pipeline'; Filters=@("TREATAS({DATE(2026,8,24)},'Load Calendar'[Date])", "TREATAS({`"no-such-pipeline`"},rpt_job_run_summary[pipeline_name])") }
)
$taskChecks = @()
try {
    foreach ($taskVisualId in @('8137eed10da16ee6c04a','32a158a22eb7ccd12103','1eba88b43b2625ccf766')) {
        $taskVisual = Get-Content -LiteralPath (Join-Path $taskPage "visuals/$taskVisualId/visual.json") -Raw | ConvertFrom-Json
        $taskProjections = @($taskVisual.visual.query.queryState.PSObject.Properties.Value.projections)
        $taskColumns = @($taskProjections | Where-Object {$_.field.Column} | ForEach-Object {
            $taskColumn = $_.field.Column
            "'" + $taskColumn.Expression.SourceRef.Entity.Replace("'","''") + "'[" + $taskColumn.Property.Replace(']',']]') + ']'
        })
        $taskTable = if ($taskVisualId -eq '32a158a22eb7ccd12103') {'rpt_job_step_timing'} else {'rpt_job_run_summary'}
        $taskMeasures = @($taskProjections | Where-Object {$_.field.Measure} | ForEach-Object {
            '"' + $_.nativeQueryRef.Replace('"','""') + '",[' + $_.field.Measure.Property.Replace(']',']]') + ']'
        })
        $taskGate = if ($taskTable -eq 'rpt_job_step_timing') {'Timeline Step Visible'} else {'Timeline Job Visible'}
        if (-not @($taskVisual.filterConfig.filters | Where-Object {$_.field.Measure.Property -eq $taskGate}).Count) { throw "$taskVisualId has no context row filter." }
        if (-not @($taskProjections | Where-Object {$_.field.Measure.Property -eq $taskGate}).Count) { $taskMeasures += '"' + $taskGate + '",[' + $taskGate + ']' }
        foreach ($taskCase in $taskCases) {
            $taskContext = if ($taskCase.ContainsKey('Context')) {$taskCase.Context} else {$taskCase.Filters}
            $taskArgs = @($taskColumns) + @($taskContext) + @($taskMeasures)
            $taskExpectedFilters = @($taskCase.Filters)
            if ($taskCase.Latest) {
                $taskExpectedFilters += 'TREATAS(SELECTCOLUMNS(LatestJob,"JobKey",rpt_job_run_summary[job_run_id]),rpt_job_run_summary[job_run_id])'
            }
            $taskExpectedArguments = @("FILTER($taskTable,NOT ISBLANK($taskTable[started_at]))") + $taskExpectedFilters
            $taskDax = @"
EVALUATE
VAR LatestJob=TOPN(1,FILTER(ALL(rpt_job_run_summary),NOT ISBLANK(rpt_job_run_summary[started_at])),rpt_job_run_summary[started_at],DESC,rpt_job_run_summary[job_run_id],DESC)
VAR ExpectedRows=CALCULATETABLE($($taskExpectedArguments -join ','))
VAR ExpectedIds=SELECTCOLUMNS(ExpectedRows,"JobKey",$taskTable[job_run_id])
VAR VisualRows=SUMMARIZECOLUMNS($($taskArgs -join ','))
VAR VisibleRows=FILTER(VisualRows,[$taskGate]=1 && NOT ISBLANK($taskTable[started_at]))
RETURN ROW("Visible",COALESCE(COUNTROWS(VisibleRows),0),"Expected",COALESCE(COUNTROWS(ExpectedRows),0),"WrongJobs",COALESCE(COUNTROWS(FILTER(VisibleRows,NOT($taskTable[job_run_id] IN ExpectedIds))),0))
"@
            $taskCommand = $taskConnection.CreateCommand()
            $taskCommand.CommandText = $taskDax
            $taskReader = $taskCommand.ExecuteReader()
            $null = $taskReader.Read()
            $taskVisible = $taskReader.GetValue(0)
            $taskExpected = $taskReader.GetValue(1)
            $taskWrong = $taskReader.GetValue(2)
            $taskReader.Close()
            $taskCheck = [pscustomobject]@{Visual=$taskVisualId;Case=$taskCase.Name;Visible=$taskVisible;Expected=$taskExpected;WrongJobs=$taskWrong;Pass=($taskVisible -eq $taskExpected -and $taskWrong -eq 0)}
            $taskChecks += $taskCheck
        }
    }
    $taskChecks | ConvertTo-Json -Depth 4
    if (@($taskChecks | Where-Object {-not $_.Pass}).Count) { throw 'Drillthrough date/pipeline context produced missing or unrelated rows.' }
    Write-Output "PASS: $($taskChecks.Count) live-model checks, including the latest load default and historical date/pipeline drillthrough."
} finally { $taskConnection.Close() }
