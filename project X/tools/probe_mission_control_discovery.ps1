# Read-only checks of the actual register projections and loaded measures.
# Import-only guard prevents this verification from contacting the data source.
param([Parameter(Mandatory)][int]$Port,
      [Parameter(Mandatory)][string]$ProjectRoot,
      [string]$OutputFile,[switch]$UseSourceMeasures)
$ErrorActionPreference = 'Stop'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
$taskDatabase = $taskServer.Databases[0]
$taskModel = $taskDatabase.Model
$taskModes = @($taskModel.Tables | ForEach-Object {$_.Partitions} | ForEach-Object {$_.Mode.ToString()} | Sort-Object -Unique)
if (@($taskModes | Where-Object {$_ -ne 'Import'}).Count) {throw 'This probe requires a fully imported model; no source queries will be issued.'}
$taskCatalog = $taskDatabase.ID
$taskModelCounts = @{Tables=$taskModel.Tables.Count; Measures=@($taskModel.Tables | ForEach-Object {$_.Measures}).Count; StorageModes=$taskModes}
$taskServer.Disconnect()
$taskAdomd = Join-Path $taskSdk 'adomd/lib/net8.0'
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
$taskActivityPath=Join-Path $ProjectRoot 'Change and discovery calendar revision.json'
$taskActivity=if (Test-Path -LiteralPath $taskActivityPath) {Get-Content -LiteralPath $taskActivityPath -Raw | ConvertFrom-Json} else {$null}
$taskDefinitions=''
if ($UseSourceMeasures) {
    if (-not $taskActivity) {throw 'Source measure overrides require the activity revision manifest.'}
    $taskSourceDatabase=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $ProjectRoot 'SM WMPP Mission Control.SemanticModel/definition'))
    $taskLines=@('DEFINE')
    foreach ($taskMeasureName in $taskActivity.writtenMeasures) {
        $taskExpression=$taskSourceDatabase.Model.Tables['_MissionControl_Measures'].Measures[$taskMeasureName].Expression
        $taskLines+="MEASURE '_MissionControl_Measures'["+$taskMeasureName.Replace(']',']]')+"] = "+$taskExpression
    }
    $taskDefinitions=($taskLines -join "`n")+"`n"
}
function Invoke-LocalQuery([string]$Dax) {
    $taskCommand = $taskConnection.CreateCommand()
    $taskCommand.CommandText = $taskDefinitions+$Dax
    $taskCommand.CommandTimeout = 60
    $taskReader = $taskCommand.ExecuteReader()
    $taskRows = [System.Collections.Generic.List[object]]::new()
    try {
        while ($taskReader.Read()) {
            $taskRow = [ordered]@{}
            for ($taskIndex=0; $taskIndex -lt $taskReader.FieldCount; $taskIndex++) {
                $taskValue=$taskReader.GetValue($taskIndex)
                $taskRow[$taskReader.GetName($taskIndex).Trim('[',']')] = if ($taskValue -is [DBNull]) {$null} else {$taskValue}
            }
            $taskRows.Add([pscustomobject]$taskRow)
        }
    } finally {$taskReader.Close()}
    return $taskRows.ToArray()
}
function DaxColumn([string]$Table,[string]$Column) {return "'"+$Table.Replace("'","''")+"'["+$Column.Replace(']',']]')+']'}
function DaxMeasure([string]$Measure) {return '['+$Measure.Replace(']',']]')+']'}
$taskTargets = [ordered]@{
    cfg_data_domain='profiled_at'; cfg_location_coordinate=$null
    cfg_schema_drift_event='detected_at'; rpt_job_schema_drift='last_detected_at'
    cfg_schema_drift_definition='definition_loaded_at'; cfg_schema_definition_candidate=$null
    cfg_bronze_schema_live='captured_at'; cfg_schema_contract_column='contract_loaded_at'
    rpt_job_data_quality='checked_at'; cfg_rejected_row='rejected_at'; cfg_referential_exception='detected_at'
    cfg_table_load_metric='recorded_at'; cfg_silver_export_load='started_at'; cfg_silver_load_control='started_at'
    rpt_job_layer_lineage='observed_at'; rpt_job_step_summary='started_at'; cfg_gold_lineage_mapping=$null
}
$taskPages = Join-Path $ProjectRoot 'SM WMPP Mission Control.Report/definition/pages'
$taskRegisters = @{}
foreach ($taskVisualPath in Get-ChildItem -LiteralPath $taskPages -Recurse -Filter 'visual.json' -File) {
    $taskVisual = Get-Content -LiteralPath $taskVisualPath.FullName -Raw | ConvertFrom-Json
    $taskProjections = @($taskVisual.visual.query.queryState.Values.projections)
    if (-not $taskProjections.Count -or -not $taskProjections[0].field.Column) {continue}
    $taskTable = $taskProjections[0].field.Column.Expression.SourceRef.Entity
    if (-not $taskTargets.Contains($taskTable)) {continue}
    $taskGate = 'Discovery '+$taskTable+' Visible'
    if (@($taskVisual.filterConfig.filters | Where-Object {$_.field.Measure.Property -eq $taskGate}).Count) {
        $taskRegisters[$taskTable]=$taskProjections
    }
}
$taskChecks=[System.Collections.Generic.List[object]]::new()
try {
    $taskHistory = Invoke-LocalQuery @'
EVALUATE
VAR LatestDate=MAX('Discovery Job Runs'[Run Date])
VAR EarlierDate=MAXX(FILTER(ALL('Discovery Job Runs'),'Discovery Job Runs'[Run Date]<LatestDate),'Discovery Job Runs'[Run Date])
VAR EmptyDate=MINX(FILTER(ALL('Load Calendar'),NOT('Load Calendar'[Date] IN VALUES('Discovery Job Runs'[Run Date]))),'Load Calendar'[Date])
VAR LatestJob=TOPN(1,FILTER(ALL('Discovery Job Runs'),NOT ISBLANK('Discovery Job Runs'[job_run_id])),'Discovery Job Runs'[started_at],DESC,'Discovery Job Runs'[job_run_id],DESC)
RETURN ROW("LatestDate",LatestDate,"EarlierDate",EarlierDate,"EmptyDate",EmptyDate,"LatestJob",MAXX(LatestJob,'Discovery Job Runs'[job_run_id]),"Jobs",COUNTROWS('Discovery Job Runs'),"DistinctJobIds",DISTINCTCOUNT('Discovery Job Runs'[job_run_id]))
'@
    foreach ($taskTable in $taskTargets.Keys) {
        if (-not $taskRegisters.ContainsKey($taskTable)) {throw "Missing scoped register for $taskTable"}
        $taskProjections=$taskRegisters[$taskTable]
        $taskColumns=@($taskProjections | ForEach-Object {DaxColumn $_.field.Column.Expression.SourceRef.Entity $_.field.Column.Property})
        $taskFieldNames=@($taskProjections | ForEach-Object {$_.field.Column.Property})
        $taskKey=if ('run_id' -in $taskFieldNames) {'run_id'} elseif ('job_run_id' -in $taskFieldNames) {'job_run_id'} else {$null}
        $taskTimestamp=$taskTargets[$taskTable]
        $taskBase="'$taskTable'"
        $taskLatestVariables=''
        $taskDefaultPredicate='TRUE()'
        if ($taskTimestamp) {
            $taskTimeCol=DaxColumn $taskTable $taskTimestamp
            $taskLatestVariables="VAR LatestTime=MAXX(ALL($taskBase),$taskTimeCol)`n"
            if ($taskKey) {
                $taskKeyCol=DaxColumn $taskTable $taskKey
                $taskLatestVariables += @"
VAR Batches=SUMMARIZE(ALL($taskBase),$taskKeyCol,"BatchTime",MAX($taskTimeCol))
VAR LatestBatch=TOPN(1,FILTER(Batches,NOT ISBLANK([BatchTime])),[BatchTime],DESC,$taskKeyCol,DESC)
VAR LatestKey=MAXX(LatestBatch,$taskKeyCol)
"@
                $taskDefaultPredicate="IF(ISBLANK(LatestKey),$taskTimeCol=LatestTime,$taskKeyCol=LatestKey)"
            } else {$taskDefaultPredicate="$taskTimeCol=LatestTime"}
        }
        $taskAliases=@()
        for ($taskIndex=0; $taskIndex -lt $taskColumns.Count; $taskIndex++) {
            $taskAliases+='"c'+$taskIndex+'",'+$taskColumns[$taskIndex]
        }
        $taskCases=@('Latest default','Latest loaded day','Earlier loaded day','Empty day','Single job')
        $taskOwnDate=$null
        if ($taskTimestamp) {
            $taskOwnTime=(Invoke-LocalQuery ("EVALUATE ROW(`"OwnTime`",MAX("+(DaxColumn $taskTable $taskTimestamp)+'))'))[0].OwnTime
            if ($taskOwnTime) {$taskOwnDate=[datetime]$taskOwnTime; $taskCases+='Own discovery day'}
        }
        foreach ($taskCase in $taskCases) {
            $taskFilter=$null
            $taskHistoricalPredicate=$null
            if ($taskCase -eq 'Single job') {
                $taskFilter='TREATAS({SelectedJob},''Discovery Job Runs''[job_run_id])'
                $taskHistoricalPredicate=(DaxColumn $taskTable 'job_run_id')+'=SelectedJob'
            } elseif ($taskCase -ne 'Latest default') {
                $taskDateProperty=switch ($taskCase) {'Latest loaded day' {'LatestDate'} 'Earlier loaded day' {'EarlierDate'} 'Empty day' {'EmptyDate'}}
                $taskDate=if ($taskCase -eq 'Own discovery day') {$taskOwnDate} else {[datetime]$taskHistory[0].$taskDateProperty}
                $taskDateLiteral="DATE($($taskDate.Year),$($taskDate.Month),$($taskDate.Day))"
                $taskFilter="TREATAS({$taskDateLiteral},'Load Calendar'[Date])"
                $taskHistoricalPredicate=(DaxColumn $taskTable 'job_run_id')+" IN SELECTCOLUMNS(FILTER(ALL('Discovery Job Runs'),'Discovery Job Runs'[Run Date]=$taskDateLiteral),`"JobKey`",'Discovery Job Runs'[job_run_id])"
                if ($taskActivity -and $taskTimestamp) {
                    $taskDateExpression=$taskActivity.recordDateExpressions.$taskTable
                    $taskDateFields=@($taskActivity.recordDates.$taskTable)
                    if ($taskDateExpression) {$taskDateExpressions=@($taskDateExpression)} else {$taskDateExpressions=@($taskDateFields | ForEach-Object {DaxColumn $taskTable $_})}
                    $taskHistoricalPredicate='('+(@($taskDateExpressions | ForEach-Object {"(NOT ISBLANK($_) && INT($_)=$taskDateLiteral)"}) -join ' || ')+')'
                }
            }
            # Job-linked evidence follows the selected jobs; unlinked snapshots
            # keep their current scope. This also prevents stale latest fallback
            # when a selected day has no retained records.
            $taskCanFilterHistory=if ($taskActivity -and $taskCase -ne 'Single job') {[bool]$taskTimestamp} else {'job_run_id' -in $taskFieldNames -and [bool]$taskTimestamp}
            $taskPredicate=if ($taskHistoricalPredicate -and $taskCanFilterHistory) {$taskHistoricalPredicate} else {$taskDefaultPredicate}
            $taskVisualArgs=@($taskColumns)
            if ($taskFilter) {$taskVisualArgs+=$taskFilter}
            $taskVisibleMeasure=DaxMeasure ('Discovery '+$taskTable+' Visible')
            $taskRowsMeasure=DaxMeasure ('Discovery '+$taskTable+' Rows')
            $taskVisualArgs+='"__Visible__",'+$taskVisibleMeasure
            $taskActualRows=if ($taskFilter) {"CALCULATE($taskRowsMeasure,$taskFilter)"} else {$taskRowsMeasure}
            $taskActualTime=if (-not $taskTimestamp) {'BLANK()'} elseif ($taskFilter) {"CALCULATE($(DaxMeasure ('Discovery '+$taskTable+' Selected time')),$taskFilter)"} else {DaxMeasure ('Discovery '+$taskTable+' Selected time')}
            $taskExpectedTime=if ($taskTimestamp) {"MAXX(ExpectedFact,$taskTimeCol)"} else {'BLANK()'}
            $taskDax=@"
EVALUATE
VAR SelectedJob="$($taskHistory[0].LatestJob.Replace('"','""'))"
$taskLatestVariables
VAR ExpectedFact=FILTER(ALL($taskBase),$taskPredicate)
VAR ExpectedVisual=SELECTCOLUMNS(SUMMARIZE(ExpectedFact,$($taskColumns -join ',')),$($taskAliases -join ','))
VAR ActualVisual=SUMMARIZECOLUMNS($($taskVisualArgs -join ','))
VAR VisibleVisual=SELECTCOLUMNS(FILTER(ActualVisual,[__Visible__]=1),$($taskAliases -join ','))
RETURN ROW("ActualRows",$taskActualRows,"ExpectedRows",COALESCE(COUNTROWS(ExpectedFact),0),"VisibleRows",COALESCE(COUNTROWS(VisibleVisual),0),"ExpectedVisibleRows",COALESCE(COUNTROWS(ExpectedVisual),0),"WrongRows",COALESCE(COUNTROWS(EXCEPT(VisibleVisual,ExpectedVisual)),0),"MissingRows",COALESCE(COUNTROWS(EXCEPT(ExpectedVisual,VisibleVisual)),0),"ActualTime",$taskActualTime,"ExpectedTime",$taskExpectedTime)
"@
            $taskResult=(Invoke-LocalQuery $taskDax)[0]
            $taskPass=$taskResult.ActualRows -eq $taskResult.ExpectedRows -and $taskResult.VisibleRows -eq $taskResult.ExpectedVisibleRows -and $taskResult.WrongRows -eq 0 -and $taskResult.MissingRows -eq 0 -and $taskResult.ActualTime -eq $taskResult.ExpectedTime
            $taskChecks.Add([pscustomobject]@{Table=$taskTable;Case=$taskCase;ActualRows=$taskResult.ActualRows;ExpectedRows=$taskResult.ExpectedRows;VisibleRows=$taskResult.VisibleRows;WrongRows=$taskResult.WrongRows;MissingRows=$taskResult.MissingRows;ActualTime=$taskResult.ActualTime;ExpectedTime=$taskResult.ExpectedTime;Pass=$taskPass})
        }
        Write-Host "Checked $taskTable"
    }
    $taskFailures=@($taskChecks | Where-Object {-not $_.Pass})
    $taskOutput=[ordered]@{Status=if ($taskFailures.Count) {'FAIL'} else {'PASS'};ProjectRoot=$ProjectRoot;Model=$taskModelCounts;History=$taskHistory[0];SourceMeasureOverrides=$UseSourceMeasures.IsPresent;Checks=$taskChecks.ToArray();FailedChecks=$taskFailures.Count;Scope='Actual loaded Import data and saved register projections; no source refresh or UI clicks.'}
    $taskJson=ConvertTo-Json -InputObject $taskOutput -Depth 8
    if ($OutputFile) {Set-Content -LiteralPath $OutputFile -Value $taskJson -Encoding utf8}
    if ($taskFailures.Count) {$taskFailures | ConvertTo-Json -Depth 6; throw 'Latest or historical discovery scope returned missing, stale or unrelated records.'}
    Write-Output "PASS: $($taskChecks.Count) checks across $($taskTargets.Count) registers."
} finally {$taskConnection.Close()}
