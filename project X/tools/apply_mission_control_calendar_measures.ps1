# Apply only the prepared measures using the public TOM API. No table query,
# storage mode, partition, relationship or refresh operation is changed.
param([Parameter(Mandatory)][int]$Port,[Parameter(Mandatory)][string]$ProjectRoot,[string]$OutputFile,[string]$ManifestFile='Change and discovery calendar revision.json')
$ErrorActionPreference='Stop'
$taskSdk=Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskSource=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $ProjectRoot 'SM WMPP Mission Control.SemanticModel/definition'))
$taskManifest=Get-Content -LiteralPath (Join-Path $ProjectRoot $ManifestFile) -Raw | ConvertFrom-Json
$taskServer=[Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
try {
    $taskModel=$taskServer.Databases[0].Model
    if (@($taskModel.Tables | ForEach-Object {$_.Partitions} | Where-Object {$_.Mode.ToString() -ne 'Import'}).Count) {throw 'This deployment requires the observed fully imported model.'}
    if (@(Compare-Object @($taskSource.Model.Tables | ForEach-Object {$_.Name} | Sort-Object) @($taskModel.Tables | ForEach-Object {$_.Name} | Sort-Object)).Count) {throw 'The open model does not match the prepared project.'}
    $taskBefore=@($taskModel.Tables | ForEach-Object {
        $taskTableName=$_.Name
        $_.Partitions | ForEach-Object {[pscustomobject]@{Table=$taskTableName;Partition=$_.Name;Mode=$_.Mode.ToString();State=$_.State.ToString();RefreshedTime=$_.RefreshedTime}}
    })
    $taskTarget=$taskModel.Tables['_MissionControl_Measures']
    foreach ($taskName in $taskManifest.writtenMeasures) {
        $taskDefinition=$taskSource.Model.Tables['_MissionControl_Measures'].Measures[$taskName]
        if (-not $taskDefinition) {throw "Prepared measure missing: $taskName"}
        $taskMeasure=$taskTarget.Measures.Find($taskName)
        if (-not $taskMeasure) {
            $taskMeasure=[Microsoft.AnalysisServices.Tabular.Measure]::new()
            $taskMeasure.Name=$taskName
            $taskTarget.Measures.Add($taskMeasure)
        }
        $taskMeasure.Expression=$taskDefinition.Expression
        $taskMeasure.FormatString=$taskDefinition.FormatString
        $taskMeasure.DisplayFolder=$taskDefinition.DisplayFolder
        $taskMeasure.LineageTag=$taskDefinition.LineageTag
    }
    $taskModel.SaveChanges()
    # Read partition metadata again from the server, not the client-side objects
    # that were populated before the measure-only commit.
    $taskServer.Disconnect()
    $taskServer.Connect("localhost:$Port")
    $taskModel=$taskServer.Databases[0].Model
    $taskAfter=@($taskModel.Tables | ForEach-Object {
        $taskTableName=$_.Name
        $_.Partitions | ForEach-Object {[pscustomobject]@{Table=$taskTableName;Partition=$_.Name;Mode=$_.Mode.ToString();State=$_.State.ToString();RefreshedTime=$_.RefreshedTime}}
    })
    $taskBeforeJson=ConvertTo-Json -InputObject $taskBefore -Depth 5 -Compress
    $taskAfterJson=ConvertTo-Json -InputObject $taskAfter -Depth 5 -Compress
    if ($taskBeforeJson -ne $taskAfterJson) {throw 'Partition metadata changed unexpectedly; inspect the deployment before continuing.'}
    $taskResult=[ordered]@{Status='PASS';UpdatedMeasures=$taskManifest.writtenMeasures.Count;ModelTables=$taskModel.Tables.Count;ModelMeasures=@($taskModel.Tables | ForEach-Object {$_.Measures}).Count;StorageModesPreserved=$true;PartitionStatesAndRefreshTimesPreserved=$true;SourceRefresh='None';Partitions=$taskAfter}
    if ($OutputFile) {$taskResult | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $OutputFile -Encoding utf8}
    Write-Output "PASS: applied $($taskManifest.writtenMeasures.Count) measures; cached partitions and refresh times preserved."
} finally {$taskServer.Disconnect()}
