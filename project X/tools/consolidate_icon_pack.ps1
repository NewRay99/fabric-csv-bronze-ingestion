param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$packRoot = Join-Path $projectRoot 'assets\brand-pack\icons'
$reportRoot = Join-Path $projectRoot 'reports'
$manifestPath = Join-Path $packRoot 'ICON_MIGRATION_20260930.json'
if ($Apply -and (Test-Path -LiteralPath $manifestPath)) { throw 'Migration already applied; inspect the existing manifest first.' }
$existing = @(Get-ChildItem -LiteralPath $packRoot -Recurse -File -Filter '*.svg')
$sources = @(Get-ChildItem -LiteralPath $reportRoot -Recurse -File -Filter '*.svg' | Where-Object {
    $_.FullName -notmatch '\\(_review|retired|archive|archives)\\' -and $_.Name -notmatch '^(Frame|wmpp-reference-)'
} | Sort-Object FullName)
$known = @{}
foreach ($f in $existing) { $known[$f.FullName] = (Get-FileHash -LiteralPath $f.FullName).Hash }
$plan = @()
foreach ($f in $sources) {
    $hash = (Get-FileHash -LiteralPath $f.FullName).Hash
    $matches = @($known.Keys | Where-Object { [IO.Path]::GetFileName($_) -eq $f.Name -and $known[$_] -eq $hash } | Sort-Object)
    if ($matches.Count) { $dest = $matches[0] }
    else {
        $group = if ($f.Name -like 'wmpp-category-*') {'category-icons'} elseif ($f.Name -like 'wmpp-journey-*') {'journey'} elseif ($f.Name -like 'wmpp-bubble-*') {'navigation-bubbles'} elseif ($f.Name -like 'lc-*') {'report-variants'} elseif ($f.Name -like 'lucide-*' -and $f.FullName -notmatch '\\StaticResources\\') {'lucide-originals'} else {'report-resources'}
        $dest = Join-Path (Join-Path $packRoot $group) $f.Name
        if ($known.ContainsKey($dest) -and $known[$dest] -ne $hash) { $dest = Join-Path (Join-Path $packRoot ('variants\'+$hash.ToLower())) $f.Name }
        $known[$dest] = $hash
    }
    $embedded = $f.FullName -match '\\StaticResources\\'
    $plan += [pscustomobject]@{source=$f.FullName;destination=$dest;sha256=$hash;action=$(if($embedded){'retain embedded; catalogue copy'}else{'move loose asset'})}
}
$plan | Group-Object action | Select-Object Count,Name | Format-Table -AutoSize
Write-Output ('Unique destination files: '+@($plan.destination | Sort-Object -Unique).Count)
if (!$Apply) { return }
$backupRoot = Join-Path (Split-Path $projectRoot -Parent) ('outputs\icon-pack-migration-'+(Get-Date -Format 'yyyyMMdd-HHmmss'))
New-Item -ItemType Directory -Path $backupRoot | Out-Null
foreach ($item in $plan) {
    $source = [IO.Path]::GetFullPath($item.source)
    $dest = [IO.Path]::GetFullPath($item.destination)
    if (!$source.StartsWith($reportRoot+'\',[StringComparison]::OrdinalIgnoreCase) -or !$dest.StartsWith($packRoot+'\',[StringComparison]::OrdinalIgnoreCase)) { throw 'Path outside migration scope.' }
    if ((Get-FileHash -LiteralPath $source).Hash -ne $item.sha256) { throw 'Source changed since planning.' }
    if (!(Test-Path -LiteralPath $dest)) {
        New-Item -ItemType Directory -Path (Split-Path $dest -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $dest
    }
    if ((Get-FileHash -LiteralPath $dest).Hash -ne $item.sha256) { throw 'Destination content mismatch.' }
    if ($item.action -eq 'move loose asset') {
        $backup = Join-Path $backupRoot $source.Substring($projectRoot.Length+1)
        New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force | Out-Null
        Copy-Item -LiteralPath $source -Destination $backup
        if ((Get-FileHash -LiteralPath $backup).Hash -ne $item.sha256) { throw 'Backup content mismatch.' }
        Remove-Item -LiteralPath $source
    }
}
$manifest = [ordered]@{date='2026-09-30';backup=$backupRoot;scope='Loose report SVG icons moved; embedded resources retained; mockups, review backups and retired reports excluded';files=$plan}
$manifest | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $manifestPath -Encoding utf8
Write-Output ('Verified migration manifest: '+$manifestPath)
