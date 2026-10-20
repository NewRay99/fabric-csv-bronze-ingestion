# Read-only validation. Bundle Microsoft's public schemas once in memory to avoid
# hundreds of repeated CDN requests and parallel validator registry collisions.
$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$manifest = Get-Content -LiteralPath (Join-Path $root 'reports/templates/WMPP_Common_Theme.manifest.json') -Raw | ConvertFrom-Json -AsHashtable
$script:schemaNames = @{}
$script:definitions = @{}

function Add-Schema([string]$url) {
    $url = $url.Replace('https://developer.microsoft.com/json-schemas/', 'https://raw.githubusercontent.com/microsoft/json-schemas/main/')
    if ($script:schemaNames.ContainsKey($url)) { return $script:schemaNames[$url] }
    $name = 'schema' + $script:schemaNames.Count
    $script:schemaNames[$url] = $name
    $node = (Invoke-WebRequest -Uri $url).Content | ConvertFrom-Json -AsHashtable
    $script:definitions[$name] = $node
    Convert-References $node $url
    return $name
}

function Convert-References($node, [string]$source) {
    if ($node -is [System.Collections.IDictionary]) {
        if ($node.Contains('$id')) { $node.Remove('$id') }
        if ($node.Contains('$ref')) {
            $target = [uri]::new([uri]$source, [string]$node['$ref'])
            $name = Add-Schema $target.GetLeftPart([System.UriPartial]::Path)
            $node['$ref'] = '#/definitions/' + $name + $target.Fragment.TrimStart('#')
        }
        # Some schemas themselves have a property named Keys; use the method.
        foreach ($key in @($node.get_Keys())) { Convert-References $node[$key] $source }
    } elseif ($node -is [System.Collections.IList]) {
        foreach ($child in $node) { Convert-References $child $source }
    }
}

$files = @('reports/templates/WMPP_Common_Theme.json')
$files += @($manifest.reports | ForEach-Object {
    Get-ChildItem -LiteralPath (Join-Path $root "$_/definition") -File -Filter '*.json' -Recurse |
        ForEach-Object { [IO.Path]::GetRelativePath($root, $_.FullName).Replace('\','/') }
})
$documents = [System.Collections.Generic.List[object]]::new()
$items = [System.Collections.Generic.List[object]]::new()
foreach ($path in $files) {
    $document = Get-Content -LiteralPath (Join-Path $root $path) -Raw | ConvertFrom-Json -AsHashtable
    $name = Add-Schema $document['$schema']
    $documents.Add($document)
    $items.Add(@{'$ref' = '#/definitions/' + $name})
}
$schema = @{'$schema' = 'http://json-schema.org/draft-07/schema#'; type = 'array'; items = $items.ToArray(); definitions = $script:definitions}
$schemaJson = ConvertTo-Json -InputObject $schema -Depth 100 -Compress
$unconverted = @([regex]::Matches($schemaJson, '"\$ref":"(#[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Where-Object { $_ -notmatch '^#/definitions/schema\d+' } | Sort-Object -Unique)
if ($unconverted.Count) { throw "Unconverted references: $($unconverted -join ', ')" }
$dataJson = ConvertTo-Json -InputObject $documents.ToArray() -Depth 100 -Compress
$null = [System.Text.Json.JsonDocument]::Parse($dataJson)
$null = [System.Text.Json.JsonDocument]::Parse($schemaJson)
$validationErrors = @()
$valid = Test-Json -Json $dataJson -Schema $schemaJson -ErrorAction SilentlyContinue -ErrorVariable validationErrors
if ($valid) {
    Write-Output "PASS: $($files.Count) final report/theme/visual files against $($script:definitions.Count) bundled Microsoft schemas."
    exit 0
}
# Test-Json emits failed oneOf alternatives even for valid siblings when the
# overall batch fails. Bisect the batch; do not treat every diagnostic as a file
# failure. This also reuses the in-memory schema bundle without network requests.
$indices = [System.Collections.Generic.List[int]]::new()
$queue = [System.Collections.Generic.Queue[object]]::new()
$queue.Enqueue(@(0..($files.Count - 1)))
while ($queue.Count) {
    $chunk = @($queue.Dequeue())
    $chunkSchema = @{'$schema' = 'http://json-schema.org/draft-07/schema#'; type = 'array';
        items = @($chunk | ForEach-Object { $items[$_] }); definitions = $script:definitions}
    $chunkData = @($chunk | ForEach-Object { $documents[$_] })
    $chunkValid = Test-Json -Json (ConvertTo-Json -InputObject $chunkData -Depth 100 -Compress) -Schema (ConvertTo-Json -InputObject $chunkSchema -Depth 100 -Compress) -ErrorAction SilentlyContinue
    if ($chunkValid) { continue }
    if ($chunk.Count -eq 1) { $indices.Add($chunk[0]); continue }
    $mid = [int][Math]::Floor($chunk.Count / 2)
    $queue.Enqueue(@($chunk[0..($mid - 1)]))
    $queue.Enqueue(@($chunk[$mid..($chunk.Count - 1)]))
}
Write-Output "Schema failures: $($indices.Count) of $($files.Count) files."
foreach ($index in $indices) { Write-Output $files[$index] }
exit 1
