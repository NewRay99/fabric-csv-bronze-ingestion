param([Parameter(Mandatory)][int]$ProcessId,[Parameter(Mandatory)][string]$ProjectRoot,[Parameter(Mandatory)][string]$Destination)
$ErrorActionPreference='Stop'
$taskManifest=Get-Content -LiteralPath (Join-Path $ProjectRoot 'Mission Control mobile layout revision.json') -Raw | ConvertFrom-Json
$taskResults=@()
foreach ($taskPage in $taskManifest.pages) {
    $taskOutput=Join-Path $Destination ('phone-native-'+$taskPage.id+'.png')
    $taskArgs=@{args=@{pageId=$taskPage.id;scale=1}} | ConvertTo-Json -Depth 3 -Compress
    $taskResponse=$null
    for ($taskAttempt=0; $taskAttempt -lt 3; $taskAttempt++) {
        $taskResponse=(& node (Join-Path $env:TEMP 'mission-control-bridge.cjs') $ProcessId 'report.snapshot.capture/v1' $taskArgs $taskOutput | Out-String) | ConvertFrom-Json
        if ($taskResponse.result) {break}
        if (-not $taskResponse.error.data.retryable) {break}
        Start-Sleep -Milliseconds 1200
    }
    if ($taskResponse.result) {
        # The initial capture switches pages before card queries always finish.
        # Take the delivered frame after those cached queries can settle.
        Start-Sleep -Milliseconds 1500
        $taskSettled=(& node (Join-Path $env:TEMP 'mission-control-bridge.cjs') $ProcessId 'report.snapshot.capture/v1' $taskArgs $taskOutput | Out-String) | ConvertFrom-Json
        if ($taskSettled.result) {$taskResponse=$taskSettled}
    }
    $taskResults += [pscustomobject]@{Page=$taskPage.name;PageId=$taskPage.id;Success=[bool]$taskResponse.result;Path=$taskOutput;Error=$taskResponse.error}
    Write-Output ('Captured: '+$taskPage.name+' / '+[bool]$taskResponse.result)
}
$taskResults | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $ProjectRoot 'Mission Control native phone previews.json') -Encoding utf8
if (@($taskResults | Where-Object {-not $_.Success}).Count) {throw 'Some phone previews did not complete.'}
