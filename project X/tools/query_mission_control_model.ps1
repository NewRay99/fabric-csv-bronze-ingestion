param([Parameter(Mandatory)][int]$Port,
      [Parameter(Mandatory)][string]$QueryFile,
      [string]$OutputFile,[string]$ProjectRoot,[switch]$UseSourceMeasures,[switch]$Quiet)
$ErrorActionPreference = 'Stop'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
$taskCatalog = $taskServer.Databases[0].ID
$taskDefinitions=''
if ($UseSourceMeasures) {
    if (-not $ProjectRoot) {throw 'ProjectRoot is required for source measure overrides.'}
    if (@($taskServer.Databases[0].Model.Tables | ForEach-Object {$_.Partitions} | Where-Object {$_.Mode.ToString() -ne 'Import'}).Count) {throw 'Source overrides require imported cached data.'}
    $taskSourceDatabase=[Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $ProjectRoot 'SM WMPP Mission Control.SemanticModel/definition'))
    $taskManifest=Get-Content -LiteralPath (Join-Path $ProjectRoot 'Change and discovery calendar revision.json') -Raw | ConvertFrom-Json
    $taskLines=@('DEFINE')
    foreach ($taskName in $taskManifest.writtenMeasures) {
        $taskLines+="MEASURE '_MissionControl_Measures'["+$taskName.Replace(']',']]')+"] = "+$taskSourceDatabase.Model.Tables['_MissionControl_Measures'].Measures[$taskName].Expression
    }
    $taskDefinitions=($taskLines -join "`n")+"`n"
}
$taskServer.Disconnect()
$taskAdomd = Join-Path $taskSdk 'adomd/lib/net8.0'
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskAdomd 'Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
try {
    $taskCommand = $taskConnection.CreateCommand()
    $taskCommand.CommandText = $taskDefinitions+(Get-Content -LiteralPath $QueryFile -Raw)
    $taskCommand.CommandTimeout = 60
    $taskReader = $taskCommand.ExecuteReader()
    $taskRows = [System.Collections.Generic.List[object]]::new()
    while ($taskReader.Read()) {
        $taskRow = [ordered]@{}
        for ($i = 0; $i -lt $taskReader.FieldCount; $i++) {
            $taskValue = $taskReader.GetValue($i)
            $taskRow[$taskReader.GetName($i)] = if ($taskValue -is [DBNull]) {$null} else {$taskValue}
        }
        $taskRows.Add([pscustomobject]$taskRow)
    }
    $taskReader.Close()
    $taskJson = ConvertTo-Json -InputObject $taskRows.ToArray() -Depth 8
    if ($OutputFile) { Set-Content -LiteralPath $OutputFile -Value $taskJson -Encoding utf8 }
    if ($Quiet) {Write-Output "Read $($taskRows.Count) cached result rows."} else {$taskJson}
} finally { $taskConnection.Close() }
