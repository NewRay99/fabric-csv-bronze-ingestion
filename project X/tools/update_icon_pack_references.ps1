$ErrorActionPreference = 'Stop'
$projectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$packRoot = Join-Path $projectRoot 'assets\brand-pack\icons'
$reportRoot = Join-Path $projectRoot 'reports'
$manifest = Get-Content -LiteralPath (Join-Path $packRoot 'ICON_MIGRATION_20260930.json') -Raw | ConvertFrom-Json
$mapping = @{}
foreach ($item in $manifest.files) { $mapping[$item.source] = $item.destination }
$metadata = @(Get-ChildItem -LiteralPath $reportRoot -Recurse -File | Where-Object {
    $_.FullName -notmatch '\\(_review|retired|archive|archives)\\' -and $_.Name -in @('REPORT_ANNOTATIONS.md','Lucide-provenance.json','ICON_CATALOG.json')
})
$utf8 = [Text.UTF8Encoding]::new($false)
foreach ($f in $metadata) {
    $raw = [IO.File]::ReadAllText($f.FullName)
    if ($f.Name -eq 'REPORT_ANNOTATIONS.md') {
        $updated = $raw.Replace('`lucide-*.svg` files in this project root are upstream originals. `lc-*-ink.svg` / `lc-*-light.svg` are report variants with only the stroke colour changed.', 'The upstream `lucide-*.svg` originals now live in `project X/assets/brand-pack/icons/lucide-originals`; `lc-*-ink.svg` / `lc-*-light.svg` variants are in `icons/report-variants` in that shared pack. See its migration manifest for exact version mappings.')
    } elseif ($f.Name -eq 'Lucide-provenance.json') {
        $updated = $raw.Replace('Originals and license are beside this file.', 'Originals and variants are now in project X/assets/brand-pack/icons; the delivery license remains beside this file. See ICON_MIGRATION_20260930.json for exact paths and hashes.')
    } else {
        $doc = $raw | ConvertFrom-Json -AsHashtable
        foreach ($icon in $doc.icons) {
            $old = [IO.Path]::GetFullPath((Join-Path $f.DirectoryName $icon.file))
            if ($mapping.ContainsKey($old)) { $icon.file = [IO.Path]::GetRelativePath($f.DirectoryName,$mapping[$old]).Replace('\','/') }
            if (!(Test-Path -LiteralPath (Join-Path $f.DirectoryName $icon.file))) { throw 'Unresolved icon catalogue reference.' }
        }
        $updated = $doc | ConvertTo-Json -Depth 30
    }
    if ($updated -ne $raw) {
        $backup = Join-Path $manifest.backup $f.FullName.Substring($projectRoot.Length+1)
        New-Item -ItemType Directory -Path (Split-Path $backup -Parent) -Force | Out-Null
        if (!(Test-Path -LiteralPath $backup)) { Copy-Item -LiteralPath $f.FullName -Destination $backup }
        [IO.File]::WriteAllText($f.FullName,$updated,$utf8)
    }
}
$catalogues = @($metadata | Where-Object Name -eq 'ICON_CATALOG.json')
if ($catalogues.Count) {
    $catalogue = Get-Content -LiteralPath $catalogues[0].FullName -Raw | ConvertFrom-Json -AsHashtable
    foreach ($icon in $catalogue.icons) {
        $absolute = [IO.Path]::GetFullPath((Join-Path $catalogues[0].DirectoryName $icon.file))
        $icon.file = [IO.Path]::GetRelativePath((Join-Path $packRoot 'category-icons'),$absolute).Replace('\','/')
    }
    $catalogue | ConvertTo-Json -Depth 30 | Set-Content -LiteralPath (Join-Path $packRoot 'category-icons\ICON_CATALOG.json') -Encoding utf8
    Copy-Item -LiteralPath (Join-Path $packRoot 'LUCIDE_LICENSE.txt') -Destination (Join-Path $packRoot 'category-icons\LUCIDE_LICENSE.txt')
}
foreach ($item in $manifest.files) {
    if ((Get-FileHash -LiteralPath $item.destination).Hash -ne $item.sha256) { throw 'Pack hash mismatch.' }
    if ($item.action -eq 'move loose asset') {
        if (Test-Path -LiteralPath $item.source) { throw 'Loose source still present.' }
    } elseif ((Get-FileHash -LiteralPath $item.source).Hash -ne $item.sha256) { throw 'Embedded resource changed.' }
}
$icons = @(Get-ChildItem -LiteralPath $packRoot -Recurse -File -Filter '*.svg')
foreach ($icon in $icons) {
    [xml]$svg = [IO.File]::ReadAllText($icon.FullName)
    if ($svg.DocumentElement.LocalName -ne 'svg') { throw 'Invalid SVG root.' }
}
Write-Output ('Verified '+$manifest.files.Count+' source mappings; '+$icons.Count+' SVGs in the shared pack; embedded copies unchanged.')
