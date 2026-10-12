# Read-only DAX projection workload profiler. This is NOT a Performance Analyzer
# recording: it does not measure display, visual scheduling, totals or bookmarks.
# Unsupported projection/filter shapes are reported, never silently discarded.
# Slicer interactions and field-parameter expansion require captured Desktop DAX.
# -Define must include dependent measures too: query-local leaf substitutions do
# not automatically rebind already-stored parent measure expressions in Desktop.
param(
    [Parameter(Mandatory)][int]$Port,
    [string]$Project = 'project X/reports/WIP/SM WMPP v16 updated WIP',
    [int]$Runs = 1,
    [int]$TimeoutSeconds = 15,
    [string]$PagePattern = '*',
    [string]$VisualPattern = '*',
    [string]$ProviderName,
    [string]$Define = ''
)
$ErrorActionPreference = 'Stop'
$taskBin = 'C:\Program Files\WindowsApps\Microsoft.MicrosoftPowerBIDesktop_2.158.1304.0_x64__8wekyb3d8bbwe\bin'
$null = [Reflection.Assembly]::Load([IO.File]::ReadAllBytes((Join-Path $taskBin 'Microsoft.PowerBI.AdomdClient.dll')))
$taskRoot = (Resolve-Path -LiteralPath $Project).Path
$taskReport = Join-Path $taskRoot 'SM_WMPP_v16.Report/definition'
$taskConnection = [Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port")
function Field($Node, $Sources = @{}) {
    if ($Node.Column -or $Node.Measure) {
        $item = if ($Node.Column) { $Node.Column } else { $Node.Measure }
        $entity = $item.Expression.SourceRef.Entity
        if (-not $entity) { $entity = $Sources[$item.Expression.SourceRef.Source] }
        if (-not $entity) { throw 'Unresolved source' }
        return "'" + $entity.Replace("'", "''") + "'[" + $item.Property.Replace(']', ']]') + ']'
    }
    if ($Node.Aggregation) {
        $functions = @{0='SUM';1='AVERAGE';2='COUNT';3='MIN';4='MAX';5='DISTINCTCOUNT';6='COUNTA';7='MEDIAN'}
        $function = $functions[[int]$Node.Aggregation.Function]
        if (-not $function) { throw "Unsupported aggregation $($Node.Aggregation.Function)" }
        return $function + '(' + (Field $Node.Aggregation.Expression $Sources) + ')'
    }
    if ($Node.Literal) {
        $value = $Node.Literal.Value
        if ($value -match "^'(.*)'$") { return '"' + $Matches[1].Replace("''", "'").Replace('"', '""') + '"' }
        if ($value -eq 'null') { return 'BLANK()' }
        if ($value -eq 'true') { return 'TRUE()' }
        if ($value -eq 'false') { return 'FALSE()' }
        if ($value -match '^(-?[\d.]+)[LD]?$') { return $Matches[1] }
        if ($value -match "^datetime'(.*)'$") {
            $date = [datetime]::Parse($Matches[1], [cultureinfo]::InvariantCulture)
            return "(DATE($($date.Year),$($date.Month),$($date.Day))+TIME($($date.Hour),$($date.Minute),$($date.Second)))"
        }
        throw "Unsupported literal type"
    }
    throw ('Unsupported expression: ' + ($Node.PSObject.Properties.Name -join ','))
}
function Predicate($Node, $Sources) {
    if ($Node.Comparison) {
        $ops = @{0='=';1='>';2='>=';3='<';4='<=';5='<>'}
        $op = $ops[[int]$Node.Comparison.ComparisonKind]
        if (-not $op) { throw 'Unsupported comparison' }
        return '(' + (Field $Node.Comparison.Left $Sources) + $op + (Field $Node.Comparison.Right $Sources) + ')'
    }
    if ($Node.In) {
        $fields = @($Node.In.Expressions | ForEach-Object { Field $_ $Sources })
        $values = @($Node.In.Values | ForEach-Object {
            $tuple = @($_ | ForEach-Object { Field $_ $Sources }) -join ','
            if ($fields.Count -gt 1) { '(' + $tuple + ')' } else { $tuple }
        })
        return 'CONTAINSROW({' + ($values -join ',') + '},' + ($fields -join ',') + ')'
    }
    if ($Node.Not) { return 'NOT(' + (Predicate $Node.Not.Expression $Sources) + ')' }
    throw 'Unsupported filter condition'
}
function FilterPlan($Filters) {
    $tables = @(); $gates = @(); $gateFields = @()
    foreach ($filter in @($Filters | Where-Object { $_.filter })) {
        $sources = @{}; foreach ($source in $filter.filter.From) { $sources[$source.Name] = $source.Entity }
        $predicates = @($filter.filter.Where | ForEach-Object { Predicate $_.Condition $sources })
        $predicate = $predicates -join ' && '
        if ($filter.field.Measure) {
            $field = Field $filter.field
            $gates += $predicate; $gateFields += $field
        } elseif ($filter.field.Column) {
            $tables += 'FILTER(ALL(' + (Field $filter.field) + '),' + $predicate + ')'
        } else { throw 'Unsupported filtered field' }
    }
    return @{Tables=$tables;Gates=$gates;GateFields=$gateFields}
}
function ExecuteWorkload($Dax) {
    $command = $taskConnection.CreateCommand(); $command.CommandText = $Dax; $command.CommandTimeout = $TimeoutSeconds
    $watch = [diagnostics.stopwatch]::StartNew(); $reader = $command.ExecuteReader(); $rows = 0
    $payload = [System.Collections.Generic.List[object]]::new()
    try {
        while ($reader.Read()) {
            $values = @(); for ($i=0; $i -lt $reader.FieldCount; $i++) {
                $value = $reader.GetValue($i)
                $values += if ($value -is [DBNull]) { $null } elseif ($value -is [datetime]) { $value.ToString('O') } else { $value }
            }
            $payload.Add($values)
            $rows++
        }
    } finally { $reader.Close(); $watch.Stop(); $command.Dispose() }
    # Result payloads (identifiers/messages) never leave the local process.
    $hashes = @($payload | ForEach-Object {
        $serialized = ConvertTo-Json -InputObject $_ -Compress -Depth 3
        [Convert]::ToHexString([security.cryptography.SHA256]::HashData([text.encoding]::UTF8.GetBytes($serialized)))
    })
    $digest = [Convert]::ToHexString([security.cryptography.SHA256]::HashData([text.encoding]::UTF8.GetBytes((@($hashes | Sort-Object) -join ''))))
    return @{Ms=[math]::Round($watch.Elapsed.TotalMilliseconds,2);Rows=$rows;Digest=$digest}
}
try {
    $taskConnection.Open()
    $catalogCommand = $taskConnection.CreateCommand(); $catalogCommand.CommandText = 'SELECT [CATALOG_NAME] FROM $SYSTEM.DBSCHEMA_CATALOGS'
    $catalogReader = $catalogCommand.ExecuteReader(); if (-not $catalogReader.Read()) { throw 'No loaded model' }
    $catalog = $catalogReader.GetString(0); $catalogReader.Close(); $taskConnection.ChangeDatabase($catalog)
    $report = Get-Content -LiteralPath (Join-Path $taskReport 'report.json') -Raw | ConvertFrom-Json
    foreach ($pageDir in Get-ChildItem -LiteralPath (Join-Path $taskReport 'pages') -Directory) {
        $page = Get-Content -LiteralPath (Join-Path $pageDir.FullName 'page.json') -Raw | ConvertFrom-Json
        if ($page.displayName -notlike $PagePattern) { continue }
        $dataVisuals = 0
        foreach ($visualFile in Get-ChildItem -LiteralPath (Join-Path $pageDir.FullName 'visuals') -Filter visual.json -Recurse -File) {
            $visual = Get-Content -LiteralPath $visualFile.FullName -Raw | ConvertFrom-Json
            if (-not $visual.visual.query -or $visual.name -notlike $VisualPattern) { continue }
            $dataVisuals++
            $result = [ordered]@{Page=$page.displayName;Visual=$visual.name;Type=$visual.visual.visualType;Status='';Fields=@();Times=@();Rows=$null;Digest=$null;Detail=$null}
            try {
                $projections = @($visual.visual.query.queryState.PSObject.Properties.Value.projections)
                $result.Fields = @($projections.queryRef)
                $columns = @(); $values = @(); $valueIndex = 0
                foreach ($projection in $projections) {
                    $field = Field $projection.field
                    if ($projection.field.Column) { $columns += $field } else { $values += '"v' + $valueIndex + '",' + $field; $valueIndex++ }
                }
                $columns = @($columns | Select-Object -Unique)
                $plan = FilterPlan (@($report.filterConfig.filters)+@($page.filterConfig.filters)+@($visual.filterConfig.filters))
                $tables = @($plan.Tables)
                if ($ProviderName -and $page.displayName -like 'Provider*') { $tables += 'TREATAS({"' + $ProviderName.Replace('"','""') + '"},''dim_provider''[provider_name])' }
                $gateNames = @()
                foreach ($gateField in @($plan.GateFields | Select-Object -Unique)) {
                    $alias = '__gate' + $gateNames.Count
                    $values += '"' + $alias + '",' + $gateField
                    $gateNames += $alias
                }
                $gates = $plan.Gates -join ' && '
                for ($i=0; $i -lt $plan.GateFields.Count; $i++) { $gates = $gates.Replace($plan.GateFields[$i], '[' + $gateNames[$i] + ']') }
                if ($columns.Count -eq 0) {
                    $core = 'ROW(' + ($values -join ',') + ')'
                    if ($tables.Count) { $core = 'CALCULATETABLE(' + $core + ',' + ($tables -join ',') + ')' }
                } else {
                    $core = 'SUMMARIZECOLUMNS(' + ((@($columns)+@($tables)+@($values)) -join ',') + ')'
                }
                if ($gates) { $core = 'FILTER(' + $core + ',' + $gates + ')' }
                $sort = @($columns | ForEach-Object { $_ + ',ASC' })
                if ($sort.Count) { $core = 'TOPN(501,' + $core + ',' + ($sort -join ',') + ')' }
                $dax = $Define + "`nEVALUATE " + $core
                $measurements = @(); for ($run=0; $run -lt $Runs; $run++) { $measurements += ExecuteWorkload $dax }
                $result.Status = 'measured'; $result.Times = @($measurements.Ms); $result.Rows=$measurements[-1].Rows; $result.Digest=$measurements[-1].Digest
                if (@($measurements.Digest | Select-Object -Unique).Count -ne 1) { $result.Detail = 'Non-identical repeated results' }
            } catch { $result.Status='error-or-unsupported'; $result.Detail=$_.Exception.Message }
            [pscustomobject]$result | ConvertTo-Json -Compress -Depth 8
        }
        if (-not $dataVisuals) { [pscustomobject]@{Page=$page.displayName;Status='no-data-visuals'} | ConvertTo-Json -Compress }
    }
} finally { $taskConnection.Close() }
