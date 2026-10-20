# Validate this WIP project's PBIR files against Microsoft's public schemas.
param([switch]$CompatibilityOnly,[string]$ProjectRoot,[switch]$SkipUnpublishedVisualSchema)
$ErrorActionPreference = 'Stop'
$taskRoot = if ($ProjectRoot) {$ProjectRoot} else {Join-Path (Split-Path $PSScriptRoot -Parent) 'reports/WIP/SM WMPP Mission Control v16'}
$taskReport = Join-Path $taskRoot 'SM WMPP Mission Control.Report/definition'
$taskDatabase = Join-Path $taskRoot 'SM WMPP Mission Control.SemanticModel/definition/database.tmdl'
$taskDatabaseText = Get-Content -LiteralPath $taskDatabase -Raw
if ($taskDatabaseText -notmatch 'compatibilityLevel:\s*(\d+)') { throw 'Database compatibility level is missing.' }
$taskSavedLevel = [int]$Matches[1]
if ($taskSavedLevel -lt 1606) { throw "Saved compatibility level $taskSavedLevel would downgrade the observed Desktop model at level 1606 during reload." }
Write-Output "PASS: compatibility level $taskSavedLevel supports reload against the observed Desktop model at level 1606."
if ($CompatibilityOnly) { exit 0 }
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
        foreach ($key in @($node.get_Keys())) { Convert-References $node[$key] $source }
    } elseif ($node -is [System.Collections.IList]) {
        foreach ($child in $node) { Convert-References $child $source }
    }
}
$files = @(Get-ChildItem -LiteralPath $taskReport -Filter '*.json' -Recurse -File)
$documents = [System.Collections.Generic.List[object]]::new()
$items = [System.Collections.Generic.List[object]]::new()
$validatedFiles = [System.Collections.Generic.List[object]]::new()
$unpublishedFiles = [System.Collections.Generic.List[object]]::new()
foreach ($file in $files) {
    $document = Get-Content -LiteralPath $file.FullName -Raw | ConvertFrom-Json -AsHashtable
    if ($SkipUnpublishedVisualSchema -and $document['$schema'] -in @(
        'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json',
        'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainerMobileState/2.8.0/schema.json')) {
        # These versions are emitted by the observed Desktop build but Microsoft's
        # public registry returns HTTP 404. Do not downgrade or rewrite it.
        $unpublishedFiles.Add($file.FullName)
        continue
    }
    $name = Add-Schema $document['$schema']
    $documents.Add($document)
    $items.Add(@{'$ref' = '#/definitions/' + $name})
    $validatedFiles.Add($file)
}
$schema = @{'$schema' = 'http://json-schema.org/draft-07/schema#'; type = 'array'; items = $items.ToArray(); definitions = $script:definitions}
$schemaJson = ConvertTo-Json -InputObject $schema -Depth 100 -Compress
$dataJson = ConvertTo-Json -InputObject $documents.ToArray() -Depth 100 -Compress
$valid = Test-Json -Json $dataJson -Schema $schemaJson -ErrorAction SilentlyContinue
if ($valid) {
    Write-Output "PASS: $($validatedFiles.Count) PBIR files against $($script:definitions.Count) Microsoft schemas."
    if ($unpublishedFiles.Count) {
        Write-Output "LIMITATION: $($unpublishedFiles.Count) native visual/mobile files parsed as JSON; their public schemas are unavailable. Native verification remains required."
    }
    [ordered]@{Status=if ($unpublishedFiles.Count) {'PASS_WITH_UNPUBLISHED_SCHEMA'} else {'PASS'};ValidatedFiles=$validatedFiles.Count;MicrosoftSchemas=$script:definitions.Count;UnpublishedSchemaFiles=$unpublishedFiles.ToArray()} |
        ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $taskRoot 'PBIR schema validation.json') -Encoding utf8
    exit 0
}
$failures = 0
foreach ($index in 0..($validatedFiles.Count - 1)) {
    $single = @{'$schema' = 'http://json-schema.org/draft-07/schema#'; '$ref' = $items[$index]['$ref']; definitions = $script:definitions}
    $validationErrors = @()
    $valid = Test-Json -Json (ConvertTo-Json $documents[$index] -Depth 100 -Compress) -Schema (ConvertTo-Json $single -Depth 100 -Compress) -ErrorAction SilentlyContinue -ErrorVariable validationErrors
    if (-not $valid) {
        $failures++
        Write-Output $validatedFiles[$index].FullName
        Write-Output ($validationErrors | Select-Object -First 8 | Out-String)
    }
}
Write-Output "FAIL: $failures files."
exit 1
