# One-time, recoverable consolidation. Does not change the semantic model,
# local model cache, connection, PBIP launcher or report logical identity.
$ErrorActionPreference = 'Stop'
$root = [IO.Path]::GetFullPath((Split-Path $PSScriptRoot -Parent))
$source = Join-Path $root 'reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report'
$activeProject = Join-Path $root 'reports/current/SM WMPP v16 updated'
$destination = Join-Path $activeProject 'SM_WMPP_v16.Report'
$retired = Join-Path $root 'reports/current/SM WMPP v16'
$archive = Join-Path $root 'reports/retired/2026-09-23-local-report-consolidation'
$stage = Join-Path $activeProject '.report-consolidation-staging'
$model = Join-Path $activeProject 'SM_WMPP_v16.SemanticModel'

foreach ($path in @($source, $destination, $retired, $archive, $stage, $model)) {
    $resolved = [IO.Path]::GetFullPath($path)
    if (!$resolved.StartsWith($root + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Path outside intended project: $resolved"
    }
}
foreach ($path in @($source, $destination, $retired, $model)) {
    if (!(Test-Path -LiteralPath $path -PathType Container)) { throw "Expected folder missing: $path" }
}
if ((Test-Path -LiteralPath $archive) -or (Test-Path -LiteralPath $stage)) {
    throw 'Archive/staging already exists. Inspect it; do not repeat this one-time operation blindly.'
}
$binding = Get-Content -LiteralPath (Join-Path $destination 'definition.pbir') -Raw | ConvertFrom-Json
if ($binding.datasetReference.byPath.path -ne '../SM_WMPP_v16.SemanticModel' -or $binding.datasetReference.byConnection) {
    throw 'Destination is not bound to the expected local model.'
}
$unexpected = @(Get-ChildItem -LiteralPath $destination -Force | Where-Object { $_.Name -notin @('definition','StaticResources','.platform','definition.pbir','.pbi') })
if ($unexpected.Count) { throw 'Unexpected destination content; review before replacement.' }
$sourcePages = Get-Content -LiteralPath (Join-Path $source 'definition/pages/pages.json') -Raw | ConvertFrom-Json
if ($sourcePages.pageOrder.Count -ne 16) { throw 'Source page count changed; review before consolidation.' }
$modelHashes = @{}
Get-ChildItem -LiteralPath $model -File -Recurse -Force | ForEach-Object {
    $modelHashes[[IO.Path]::GetRelativePath($model, $_.FullName)] = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
}

$null = New-Item -ItemType Directory -Path $stage
foreach ($name in @('definition', 'StaticResources')) {
    Copy-Item -LiteralPath (Join-Path $source $name) -Destination (Join-Path $stage $name) -Recurse
}
# Preserve local identity/connection and any existing local report state.
foreach ($name in @('.platform', 'definition.pbir', '.pbi')) {
    $path = Join-Path $destination $name
    if (Test-Path -LiteralPath $path) { Copy-Item -LiteralPath $path -Destination (Join-Path $stage $name) -Recurse -Force }
}
foreach ($name in @('definition', 'StaticResources')) {
    Get-ChildItem -LiteralPath (Join-Path $source $name) -File -Recurse -Force | ForEach-Object {
        $relative = [IO.Path]::GetRelativePath($source, $_.FullName)
        if ((Get-FileHash -LiteralPath $_.FullName).Hash -ne (Get-FileHash -LiteralPath (Join-Path $stage $relative)).Hash) {
            throw "Staged file mismatch: $relative"
        }
    }
}
$null = New-Item -ItemType Directory -Path $archive
Copy-Item -LiteralPath (Join-Path $root 'reports/templates/WMPP_Common_Theme.manifest.json') -Destination (Join-Path $archive 'WMPP_Common_Theme.manifest.before.json')
# Exact absolute targets were checked above. Move instead of deleting, so both
# the retired model and the previous attached report remain recoverable.
Move-Item -LiteralPath $destination -Destination (Join-Path $archive 'SM_WMPP_v16.Report-before-dashboard-copy')
Move-Item -LiteralPath $stage -Destination $destination
Move-Item -LiteralPath $retired -Destination (Join-Path $archive 'SM WMPP v16')

foreach ($relative in $modelHashes.Keys) {
    if ((Get-FileHash -LiteralPath (Join-Path $model $relative)).Hash -ne $modelHashes[$relative]) {
        throw "Semantic model changed unexpectedly: $relative"
    }
}
$receipt = @{
    date = '2026-09-23'; source = [IO.Path]::GetRelativePath($root, $source)
    destination = [IO.Path]::GetRelativePath($root, $destination)
    retiredArchive = [IO.Path]::GetRelativePath($root, (Join-Path $archive 'SM WMPP v16'))
    previousReport = [IO.Path]::GetRelativePath($root, (Join-Path $archive 'SM_WMPP_v16.Report-before-dashboard-copy'))
    pageCount = $sourcePages.pageOrder.Count; modelFileHashes = $modelHashes
    localBindingPreserved = $true; clientSourceUnchanged = $true
}
$receipt | ConvertTo-Json -Depth 20 | Set-Content -LiteralPath (Join-Path $archive 'consolidation-receipt.json') -Encoding utf8
Write-Output "Copied all 16 dashboard pages and resources into: $destination"
Write-Output "Preserved $($modelHashes.Count) model files and the local connection."
Write-Output "Retired project and previous attached report are recoverable in: $archive"
