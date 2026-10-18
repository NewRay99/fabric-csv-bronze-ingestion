# Read-only native DAX acceptance; never save, refresh or modify the live model.
param([Parameter(Mandatory)][int]$Port)
$ErrorActionPreference = 'Stop'
$taskProject = Join-Path $PSScriptRoot '../reports/WIP/SM WMPP v16 updated WIP'
$taskSdk = Join-Path $env:TEMP 'mission-control-tmdl-sdk'
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'sdk/lib/net8.0/Microsoft.AnalysisServices.Tabular.dll')
$taskModel = [Microsoft.AnalysisServices.Tabular.TmdlSerializer]::DeserializeDatabaseFromFolder((Join-Path $taskProject 'SM_WMPP_v16.SemanticModel/definition'))
$taskExpression = $taskModel.Model.Tables['_Story Measures'].Measures['Detail location matches offer'].Expression
[pscustomobject]@{native_tmdl='passed';tables=$taskModel.Model.Tables.Count;relationships=$taskModel.Model.Relationships.Count;roles=$taskModel.Model.Roles.Count} | ConvertTo-Json -Compress
$taskServer = [Microsoft.AnalysisServices.Tabular.Server]::new()
$taskServer.Connect("localhost:$Port")
try {
    $taskCatalog = $taskServer.Databases[0].ID
    foreach($taskTableName in @('fact_offer','Referral Map Points','fact_referral')) {
        if(@($taskServer.Databases[0].Model.Tables[$taskTableName].Partitions | Where-Object {$_.Mode.ToString() -ne 'Import'}).Count){throw 'Verification requires cached Import data.'}
    }
} finally {$taskServer.Disconnect()}
Add-Type -Path (Join-Path $taskSdk 'adomd/lib/net8.0/Microsoft.AnalysisServices.Runtime.Core.dll')
Add-Type -Path (Join-Path $taskSdk 'adomd/lib/net8.0/Microsoft.AnalysisServices.Runtime.Windows.dll')
Add-Type -Path (Join-Path $taskSdk 'adomd/lib/net8.0/Microsoft.AnalysisServices.AdomdClient.dll')
$taskConnection=[Microsoft.AnalysisServices.AdomdClient.AdomdConnection]::new("Data Source=localhost:$Port;Initial Catalog=$taskCatalog")
$taskConnection.Open()
try {
    $taskCommand=$taskConnection.CreateCommand()
    $taskCommand.CommandTimeout=30
    $taskCases=@'
VAR __candidateRefs = FILTER(SUMMARIZE('fact_offer', 'fact_offer'[referral_id], "__offers", COUNTROWS('fact_offer')), [__offers] >= 2 && NOT ISBLANK('fact_offer'[referral_id]))
VAR __ref = SELECTCOLUMNS(TOPN(1, __candidateRefs, 'fact_offer'[referral_id], ASC), "r", 'fact_offer'[referral_id])
VAR __refFilter = TREATAS(__ref, 'fact_referral'[referral_id])
VAR __twoOffers = CALCULATETABLE(TOPN(2, VALUES('fact_offer'[offer_id]), 'fact_offer'[offer_id], ASC), __refFilter)
VAR __oneOffer = TOPN(1, __twoOffers, 'fact_offer'[offer_id], ASC)
VAR __noSelection = CALCULATETABLE(SUMMARIZECOLUMNS('Referral Map Points'[Point ID], 'Referral Map Points'[Offer], 'Referral Map Points'[Location type], "__visible", '_Story Measures'[Detail location matches offer]), __refFilter)
VAR __one = CALCULATETABLE(SUMMARIZECOLUMNS('Referral Map Points'[Point ID], 'Referral Map Points'[Offer], 'Referral Map Points'[Location type], "__visible", '_Story Measures'[Detail location matches offer]), __refFilter, TREATAS(__oneOffer, 'fact_offer'[offer_id]))
VAR __two = CALCULATETABLE(SUMMARIZECOLUMNS('Referral Map Points'[Point ID], 'Referral Map Points'[Offer], 'Referral Map Points'[Location type], "__visible", '_Story Measures'[Detail location matches offer]), __refFilter, TREATAS(__twoOffers, 'fact_offer'[offer_id]))
VAR __missing = CALCULATETABLE(SUMMARIZECOLUMNS('Referral Map Points'[Point ID], "__visible", '_Story Measures'[Detail location matches offer]), __refFilter, TREATAS({"__nonexistent_offer__"}, 'fact_offer'[offer_id]))
VAR __noReferral = SUMMARIZECOLUMNS('Referral Map Points'[Point ID], "__visible", '_Story Measures'[Detail location matches offer])
VAR __expectedAll = CALCULATE(COUNTROWS('Referral Map Points'), __refFilter)
VAR __expectedOne = CALCULATE(COUNTROWS('Referral Map Points'), __refFilter, TREATAS(__oneOffer, 'Referral Map Points'[Offer]))
VAR __expectedTwo = CALCULATE(COUNTROWS('Referral Map Points'), __refFilter, TREATAS(__twoOffers, 'Referral Map Points'[Offer]))
EVALUATE ROW(
 "all_referral_locations", __expectedAll,
 "cleared_selection_locations", COALESCE(COUNTROWS(__noSelection), 0),
 "expected_one_offer", __expectedOne,
 "one_offer_locations", COALESCE(COUNTROWS(__one), 0),
 "expected_two_offers", __expectedTwo,
 "two_offer_locations", COALESCE(COUNTROWS(__two), 0),
 "assigned_provider_rows_when_offer_selected", COALESCE(COUNTROWS(FILTER(__one, 'Referral Map Points'[Location type] <> "Offer home")), 0),
 "unrelated_offer_rows", COALESCE(COUNTROWS(FILTER(__one, NOT ('Referral Map Points'[Offer] IN __oneOffer))), 0),
 "unmatched_offer_locations", COALESCE(COUNTROWS(__missing), 0),
 "without_referral_locations", COALESCE(COUNTROWS(__noReferral), 0)
)
'@
    $taskCommand.CommandText="DEFINE MEASURE '_Story Measures'[Detail location matches offer] = `n"+$taskExpression+"`n"+$taskCases
    $taskReader=$taskCommand.ExecuteReader()
    try {
        if(-not $taskReader.Read()){throw 'No behaviour result.'}
        $taskResult=[ordered]@{}
        for($taskI=0;$taskI -lt $taskReader.FieldCount;$taskI++){$taskResult[$taskReader.GetName($taskI)]=$taskReader.GetValue($taskI)}
    } finally {$taskReader.Close()}
    $taskResult | ConvertTo-Json -Compress
    foreach($taskPair in @(@('[all_referral_locations]','[cleared_selection_locations]'),@('[expected_one_offer]','[one_offer_locations]'),@('[expected_two_offers]','[two_offer_locations]'))) {
        if([int]$taskResult[$taskPair[0]] -ne [int]$taskResult[$taskPair[1]]){throw 'Location count mismatch.'}
    }
    foreach($taskKey in @('[assigned_provider_rows_when_offer_selected]','[unrelated_offer_rows]','[unmatched_offer_locations]','[without_referral_locations]')) {
        if([int]$taskResult[$taskKey] -ne 0){throw "Unexpected locations: $taskKey"}
    }
    if([int]$taskResult['[one_offer_locations]'] -lt 1 -or [int]$taskResult['[two_offer_locations]'] -lt 2){throw 'Insufficient positive selection coverage.'}
    'PASS: single/multiple selection, cleared, no-match and no-referral cases. No live write or refresh.'
} finally {$taskConnection.Close()}
