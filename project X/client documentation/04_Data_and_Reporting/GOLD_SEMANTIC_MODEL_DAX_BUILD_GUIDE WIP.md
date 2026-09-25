# Gold semantic model DAX build guide

## ETL category and location contract — 25 September 2026

The active ETL now separates proposed offer category from actual home category,
adds referral framework and spot bridges, and renames `fact_offer.home_id` to
`provider_home_id`. Generalised referral locations and approximate offer distances
include explicit default/review/missing-data flags. See the
[implementation and deployment guide](CATEGORY_AND_LOCATION_ETL_IMPLEMENTATION.md).

**What's outstanding:** deploy/verify the notebooks in Fabric, load approved
city/postcode coordinates, approve location parsing/default rules, and rebind
downstream keys/category relationships. Use bridges for multi-category membership;
do not treat a null single-category key as no membership without checking its
count. Distances are approximate straight-line city-to-postcode distances, not
child addresses or travel distances. Client semantic/report projects were not
edited or tested for this ETL change. Retained historical months require a
separately approved rebuild to populate the new snapshot fields.

## End-goal KPI pages and snapshot window — 23 September 2026

The report under `reports/current/RPT WMPP v16` now includes **Board Dashboard**,
**Provider & Placement Supply**, **Target & Urgency Performance** and
**Referral Snapshots**, alongside its existing pages. The snapshot graph and
detail table have a single-select **Last 6 months / Last 12 months** control
(default 12), ending at the displayed latest available snapshot month.

The local model adds six disconnected axis/control tables and 18 supporting
measures in `_Design Measures`; existing canonical measures are preserved.
See [end-goal implementation and KPI mapping](WMPP_END_GOAL_DESIGN_IMPLEMENTATION.md)
for exact definitions and verification results.

**What's outstanding:** Desktop refresh/rendering and live KPI reconciliation;
governed region, escalation, review and shortlist evidence for labelled gaps;
business agreement on cohort and prior-month comparison semantics; and, as
the final task after user review/check-in, deployment of the new model fields
to the client semantic model followed by client-bound report validation.
Use `definition-local.pbir` for repository review in the meantime.

## Repository v16 report and model completion — 23 September 2026

The supplied v16 bundle, original 117-row KPI workbook, Word KPI/visual guide,
target dashboard images and repository client documentation have now been
reconciled. The implementation candidate is
`reports/current/SM WMPP v16 updated`; the styled report is
`reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report`.

Completed repository work:

- 49 legacy measure aliases with a canonical replacement and two empty
  placeholder measures were removed, reducing `_Measures` from 309 to 258;
- all report/DAX references were rebound before measure removal;
- `KPI Selector` was de-duplicated to 74 canonical entries and an eight-entry
  `Dashboard Metric Selector` field parameter was added;
- the styled report now has Provider Single View, Referral Single View and a
  referral-ID drillthrough detail page covering offers, provider responses and
  IPA detail;
- provider and referral searches use fields actually present in Gold; person
  search is `initials | person_id` because full child/person name is absent;
- the client live connection remains in `definition.pbir`, with a separate
  `definition-local.pbir` for the reconciled repository model; and
- static validation passes for JSON, model/report fields, measures, page
  bindings, Gold reconciliation, RLS structure and the Mission Control model.

The source KPI disposition is 101 implemented/covered, four explicitly
labelled proxies and 12 blocked by missing governed source evidence. See
[WMPP v16 KPI and report reconciliation](WMPP_V16_KPI_AND_REPORT_RECONCILIATION.md)
for the exact KPI groups, report changes and validation boundary.

### What's outstanding

1. Refresh the current Gold build in Fabric and validate representative DAX
   results, relationship cardinality and the dynamic RLS matrix with real data.
2. Obtain business approval for the four proxy KPIs (KPI-107, KPI-110,
   KPI-113 and KPI-117), or replace them when source-perfect facts exist.
3. Supply governed source fields/history for KPI-95, KPI-96, KPI-98,
   KPI-102, KPI-103, KPI-105, KPI-106, KPI-108, KPI-109, KPI-111, KPI-112 and
   KPI-115 before implementing them.
4. Decide whether `initials | person_id` is sufficient for person search. A
   full-name field must be deliberately promoted to Gold and protected by the
   approved governance/RLS design; it must not be inferred or copied from an
   unapproved layer.
5. Open `definition-local.pbir` in Power BI Desktop, refresh, test the dynamic
   metric selectors, provider/referral searches and referral drillthrough, and
   complete layout/accessibility review.
6. **Final task, only after the user has reviewed and checked in the completed
   repository work:** open the preserved client-bound `definition.pbir` in the
   client environment, repair its workspace credential/binding if necessary,
   complete a full refresh and confirm the report and semantic model open
   without errors before publishing.

## Client-site v16 reconciliation — 20 September 2026

`reports/current/MWPP Repo 20092026.zip` is the current client-site baseline
for this guide. The reviewed PBIP is `SM_WMPP_v16`. This section supersedes
the v15 deployment-status wording below; the v15 section remains as migration
history.

### What is present

| Check | Client-site v16 result | Assessment |
| --- | ---: | --- |
| Semantic tables | 117 | 29 business/model tables plus 87 automatic local-date tables and one date template. |
| Measures | 274 | All 195 concrete measures defined in this guide are present by name. |
| Storage | 115 Import, 2 DirectQuery | `gold referral_journey_flow` and `gold rpt_kpi_referral_board_summary` are DirectQuery; the rest, including automatic date tables, are Import. |
| RLS roles | 0 | R55 and the requested UserGroup partial-RLS pattern are not implemented. |
| Mission Control tables/measures | 0 | Correctly remains a separate subject/model; see the Mission Control guide. |

Name coverage does not mean the client model is ready for acceptance. Static
inspection of the semantic and report definitions found the following changes
still required.

### Repository implementation candidate

`reports/current/SM WMPP v16 updated` is now a version-controlled candidate
built from that ZIP by `tools/reconcile_semantic_model_v16.py`. The candidate
repairs all statically detectable report bindings, uses the maintained measure
source, moves stock MoM logic to the snapshot month role, removes the
fact-to-fact and bidirectional business paths, connects placement type,
disables/removes automatic date tables, normalises storage to Import, adds the
provider KPI evidence layer, and adds deny-by-default dynamic detail RLS plus
an identifier-free global summary.

This is a repository implementation, not proof of deployment or acceptance.
Run the updated `00_setup_cfg.py`, `04_gold_model.py` and
`05_gold_dimensions.py`, populate approved security mappings, refresh the
model, open it in Power BI Desktop, test DAX results and execute the RLS test
matrix before replacing the client-site version.

### Required model updates

| Priority | Update | Evidence in client-site v16 | Required action |
| --- | --- | --- | --- |
| P0 | Repair report bindings | 73 report field-reference occurrences point to nine fields that are absent from the semantic model. | Rebind or add governed compatibility aliases before publishing; use the mapping below. |
| P0 | Replace state-based Month-on-Month logic | Every legacy card stack shifts `dim_date[date]`, whose active relationship is referral creation date. This compares creation cohorts, not what was open/closed/under-offer at each month. | Source stock/state cards from `fact_referral_snapshot`; retain event facts only for flow measures. Follow [Snapshot Month-on-Month KPI guide](SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md). |
| P0 | Remove the active fact-to-fact snapshot path | `fact_referral_snapshot[referral_id]` and `fact_referral[referral_id]` are active and bidirectional while the snapshot-date relationship is inactive. | Remove or deactivate the fact-to-fact relationship. Relate both facts directly to conformed dimensions and give snapshots an active month/date role. |
| P0 | Implement and test RLS | There is no `roles/` definition, no UPN-to-authority/UserGroup mapping and no RLS-ready authority or UserGroup key in the current semantic model. `fact_referral[region]` is populated as `NULL` by the reviewed Gold notebook. | Implement the Gold security keys, mapping tables, role and partial-aggregate design in [RLS and partial aggregate access guide](RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md). |
| P1 | Restore a single-direction star | Four relationships use `bothDirections`: referral-to-provider assignment, provider-home-to-offer, provider-assignment-to-reject-reason, and current-referral-to-snapshot. | Make business relationships dimension-to-fact and single-direction. Allow a bidirectional security filter only on the one approved security bridge, if that design is selected and tested. |
| P1 | Connect placement type | `dim_placement_type` is imported but has no relationship to either referral fact. | Relate `dim_placement_type[placement_type]` to current and snapshot placement-type keys after uniqueness and value coverage checks. |
| P1 | Remove automatic date tables | `__PBI_TimeIntelligenceEnabled = 1` has generated 87 `LocalDateTable_*` objects plus a date template. | Disable Auto date/time, remove generated date metadata and use controlled date/month dimensions only. |
| P1 | Reconcile three guide/client expression drifts | Client v16 scopes `Offers in Draft` to under-offer referrals, implements `Referrals Not Yet Closed (Created in Period)` from two status values instead of `is_open`, and returns zero for an empty Offer Receipt Rate denominator. | Use the guide definitions for the unscoped/canonical measures. Keep separately named scoped measures when required by a visual; return blank for an undefined rate unless the business explicitly approves zero. |
| P1 | Remove the unapproved provider-contact proxy | Client v16 contains the legacy `Provider Contact Referral` family using `first_action_date`; that field is not proven to mean provider contact. | Remove, hide or rename it as a first-action KPI until a governed provider-contact event exists. |
| P2 | Decide the composite-model contract | Two Gold reporting objects are DirectQuery while the remainder is Import. | Either document and performance-test the composite model, or align those objects to the chosen storage mode. Do not leave the storage split accidental. |
| P2 | Add governed provider scoring | No score facts, score version, required-document rules, feedback rating or home-to-framework-category bridge are present. | Follow [Provider scoring implementation guide](PROVIDER_SCORING_IMPLEMENTATION_GUIDE.md); do not calculate an overall score until the documented blockers are resolved. |

### Broken binding repair map

The count below is the number of static references in report JSON, not the
number of visible visuals. Hidden or scrapbook pages still need repair or
removal because they remain part of the PBIP.

| Missing report field | References | Repair |
| --- | ---: | --- |
| `Referral Closure Reason Summary_old[Closed Referral Reason Bucket]` | 23 | Replace with a governed referral-closure-reason dimension. As an interim display only, use `fact_referral[referral_closure_reason]`; do not substitute provider decline reasons. |
| `dim_referral[placement_type]` | 4 | Rebind to `dim_placement_type[placement_type]` after adding its fact relationships. |
| `_Measures[Active Awaiting Offers (Engaged)]` | 2 | Rebind to `Active Awaiting Offers With Engagement`, or retain a compatibility alias. |
| `_Measures[Active Awaiting Offers (No Engagement)]` | 1 | Rebind to `Active Awaiting Offers Without Engagement`, or retain a compatibility alias. |
| `_Measures[Offers in Draft (Under Offer Referrals)]` | 3 | Rebind to `Draft Offers on Referrals Under Offer`. |
| `_Measures[Open Referral]` | 3 | Rebind current-state uses to `Open Referrals`; use `Open Referrals at Snapshot` for as-of cards. |
| `_Measures[Open Referral Previous Month]` | 34 | Do not restore the creation-date alias as the final fix. Rebind historical stock cards to the snapshot previous-month measure. |
| `_Measures[Spot Offers (Under Offer Referrals)]` | 1 | Rebind to `Spot Offers on Referrals Under Offer`. |
| `_Measures[Successful Offers (Under Offer Referrals)]` | 2 | Rebind to `Successful Offers on Referrals Under Offer`. |

After repair, run a static binding check across every report JSON file and then
open the PBIP in Power BI Desktop. Static inspection cannot prove DAX results,
relationship cardinality against refreshed data, or RLS behaviour.

## Implemented Gold migration — 15 September 2026

The extracted v15 project now uses the active Gold layer for business data. The current implementation and remaining acceptance work are recorded in [Gold report implementation and requirements](GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md). The earlier [coverage audit](GOLD_MEASURE_REQUIREMENT_COVERAGE_AUDIT.md) is the **pre-migration baseline**, not the current defect list.

All 195 concrete guide measures remain available. Formulas below now match the implemented report where requirements required a correction. The report uses semantic `fact_ipa` over physical `gold.fact_ipa`, and imports `dim_person[gender_clean]` directly from Gold. Deploy the updated `04_gold_model.py` and refresh Gold before refreshing this report: the IPA-grain signature fields are new. File validation is complete; Fabric refresh, DAX results and business acceptance are still required.

## Purpose

Use this guide to build the replacement Power BI semantic model over the
active notebook-created Gold database. It was reconciled against:

- `SM WMPP v15.zip` — legacy business-report measures;
- `SM WMPP Mission Control.zip` — operational monitoring report; and
- [Mission Control semantic model DAX build guide](MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md)
  — monitoring-only measures.

The Mission Control measures remain a separate monitoring model because they
use `monitoring.cfg_*` tables, not referral Gold facts. The v15 measures must
be recreated only from the active Gold tables listed below; do not retain a
legacy table in the new semantic model just to preserve a measure name.

## Gold-only KPI contract

Every published referral KPI must reference a field in an active Gold fact,
dimension or bridge table imported into the semantic model. `bronze.*`,
`silver.*`, retired facts and legacy model tables are lineage evidence only and
must never appear in a published DAX expression. A source marked as available
in Bronze or Silver is therefore **not** KPI-ready until the required field is
deliberately promoted into Gold. The source-coverage worksheet in
`configuration/Dashboard Legend.xlsx` records this distinction in its **KPI
DAX eligibility** column.

## Import and relationship instructions

Import `fact_referral`, `fact_referral_snapshot`, `fact_offer`, `fact_ipa`,
`fact_referral_provider`, and the active `dim_*` / `bridge_*` tables
(including `dim_person` and `dim_offer_status`). Their
columns are lower-case `snake_case`.

Create these active relationships:

| From | To | Cardinality / direction | Status |
| --- | --- | --- | --- |
| `fact_referral[referral_id]` | `fact_offer[referral_id]` | One-to-many, single direction | Active |
| `fact_referral[referral_id]` | `fact_ipa[referral_id]` | One-to-many, single direction | Active |
| `fact_referral[referral_id]` | `fact_referral_provider[referral_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `fact_offer[provider_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `fact_referral_provider[provider_id]` | One-to-many, single direction | Active |
| `dim_provider_home[provider_home_id]` | `fact_offer[home_id]` | One-to-many, single direction | Active |
| `dim_provider[provider_id]` | `dim_provider_home[provider_id]` | One-to-many, single direction | Inactive: avoids a second provider-to-offer path; home/QA measures transfer provider IDs explicitly |
| `dim_provider[provider_id]` | `bridge_provider_framework[provider_id]` | One-to-many, single direction | Active |
| `dim_provider_home[provider_home_id]` | `dim_provider_submission_document[home_id]` | One-to-many, single direction | Active |
| `dim_person[person_id]` | `fact_referral[person_id]` | One-to-many, single direction | Active |
| `dim_person[person_id]` | `fact_referral_snapshot[person_id]` | One-to-many, single direction | Active |
| `dim_placement_type[placement_type]` | `fact_referral[placement_type_required]` | One-to-many, single direction | Active after value-coverage validation |
| `dim_placement_type[placement_type]` | `fact_referral_snapshot[placement_type_required]` | One-to-many, single direction | Active after value-coverage validation |
| `dim_snapshot_month[month_start]` | `fact_referral_snapshot[snapshot_month_start]` | One-to-many, single direction | Active; required for monthly as-of reporting |
| `dim_offer_status[offer_status]` | `fact_offer[offer_status]` | One-to-many, single direction | Active |

Use `dim_date[date]` for event dates such as referral creation. Use a governed
monthly role (`dim_snapshot_month`) for state-at-snapshot reporting. Add
`snapshot_month_start` to Gold as the first day of the calendar month so that
irregular physical snapshot dates (for example a live snapshot on the 20th and
a prior month-end snapshot on the 31st) still compare like-for-like months.

Do **not** relate `fact_referral` directly to `fact_referral_snapshot`. The
client-site v16 fact-to-fact relationship is bidirectional and lets the active
referral-creation date path constrain snapshot rows to creation cohorts. Relate
each fact to the conformed person, placement type and other approved dimensions
instead. Keep other event-date relationships inactive or implement explicit
role-playing date dimensions. Do not create an active
`fact_offer[offer_id]` to `fact_ipa[accepted_offer_id]` relationship when it
creates an ambiguous route; use `USERELATIONSHIP` in a specific conversion
measure instead.

## Copy-ready DAX

Create the measures below in a dedicated `_measures` table. They refer only to
the new Gold model.

```DAX
Total Referrals =
DISTINCTCOUNT ( 'fact_referral'[referral_id] )

Open Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Closed Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = FALSE () )

Referrals With an Offer =
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )

Referrals Awaiting Offer =
CALCULATE ( [Total Referrals], 'fact_referral'[is_awaiting_offer] = TRUE () )

Referrals Without Provider Assignment =
CALCULATE ( [Total Referrals], 'fact_referral'[is_not_seen_by_providers] = TRUE () )

Open Overdue Referrals =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open_overdue] = TRUE () )

Referrals Placed by Required Date =
CALCULATE ( [Total Referrals], 'fact_referral'[placed_by_required_date] = TRUE () )

Placement Target Hit Rate =
DIVIDE (
    [Referrals Placed by Required Date],
    CALCULATE (
        [Total Referrals],
        FILTER (
            'fact_referral',
            NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
                && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
        )
    )
)

Median Days to First Action =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_action] ) ),
    'fact_referral'[days_to_first_action]
)

Median Days to First Offer =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_offer] ) ),
    'fact_referral'[days_to_first_offer]
)

Median Days to IPA =
MEDIANX (
    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_ipa] ) ),
    'fact_referral'[days_to_ipa]
)

Open Referrals Stalled 7+ Days =
CALCULATE (
    [Total Referrals],
    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[days_without_activity] >= 7 )
)
```

```DAX
Offers Submitted =
DISTINCTCOUNT ( 'fact_offer'[offer_id] )

Accepted Offers =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( 'fact_offer'[offer_status] ) IN { "accepted", "approved", "selected", "offer_successful" }
    )
)

Offers with a Decision =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_decision_date] ) )
)

Offer Acceptance Rate =
DIVIDE ( [Accepted Offers], [Offers with a Decision] )

Average Offers per Referral =
DIVIDE ( [Offers Submitted], [Referrals With an Offer] )

Offers in Draft =
CALCULATE ( [Offers Submitted], LOWER ( 'fact_offer'[offer_status] ) = "draft" )

Draft Offers Stalled 7+ Days =
CALCULATE (
	[Offers Submitted],
	FILTER (
		'fact_offer',
		LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
			&& 'fact_offer'[days_since_offer_activity] >= 7
	)
)

IPAs Created =
DISTINCTCOUNT ( 'fact_ipa'[ipa_id] )

Active IPAs =
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = FALSE () )

Estimated Active Weekly Cost =
CALCULATE (
    SUM ( 'fact_ipa'[estimated_weekly_cost] ),
    'fact_ipa'[is_placement_closed] = FALSE ()
)

Average Estimated Weekly Cost — Confirmed Referrals =
AVERAGEX (
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
            && NOT ISBLANK ( 'fact_referral'[estimated_weekly_cost] )
    ),
    'fact_referral'[estimated_weekly_cost]
)

Provider Assignments =
DISTINCTCOUNT ( 'fact_referral_provider'[referral_provider_id] )

Provider Declines =
CALCULATE ( [Provider Assignments], 'fact_referral_provider'[is_declined] = TRUE () )

Provider Decline Rate =
DIVIDE ( [Provider Declines], [Provider Assignments] )
```

```DAX
Snapshot Referrals =
DISTINCTCOUNT ( 'fact_referral_snapshot'[referral_id] )

Open Referrals at Snapshot =
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open] = TRUE () )

Closed Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    FILTER (
        'fact_referral_snapshot',
        NOT ISBLANK ( 'fact_referral_snapshot'[referral_closed_date] )
            && 'fact_referral_snapshot'[referral_closed_date] < 'fact_referral_snapshot'[snapshot_date] + 1
    )
)

Referrals with IPA at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    FILTER (
        'fact_referral_snapshot',
        NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
            && 'fact_referral_snapshot'[ipa_issued_date] < 'fact_referral_snapshot'[snapshot_date] + 1
    )
)

Open Overdue Referrals at Snapshot =
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open_overdue] = TRUE () )

Open On-Track Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    'fact_referral_snapshot'[required_placement_date_outcome] = "Open on track"
)

Open Referral Rate at Snapshot =
DIVIDE ( [Open Referrals at Snapshot], [Snapshot Referrals] )

Placement Rate at Snapshot =
DIVIDE ( [Referrals with IPA at Snapshot], [Snapshot Referrals] )
```

### Gender referral measures (KPI-04–07)

`gold.dim_person` (GLD-006/GLD-007) supplies `gender_clean` at person grain,
and `fact_referral[person_id]` links each referral to its recorded person.
The active `dim_person[person_id]` → `fact_referral[person_id]` relationship
makes these measures possible; they replace the legacy `dim_referral[Gender
Clean]` breakdown.

```DAX
Female Referrals =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Female" )

Male Referrals =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Male" )

Other Gender Referrals =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Other" )

Total Gendered Referrals =
CALCULATE ( [Total Referrals], KEEPFILTERS ( FILTER ( 'dim_person', NOT ISBLANK ( 'dim_person'[gender_clean] ) && 'dim_person'[gender_clean] <> "Unknown" ) ) )
```

## Additional legacy KPI ports

The following measures complete the **supported** portion of the historical
KPI library. They use active Gold fields only. Measures with similar historic
names can be renamed in the semantic model after the totals have been
reconciled.

### Referral, provider engagement and planning

```DAX
Referrals Created This Month =
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of ) ) )

Referrals Created Previous Month =
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referral Volume Month on Month =
[Total Referrals] - [Referrals Created Previous Month]

Referral Volume Month on Month % =
DIVIDE ( [Referral Volume Month on Month], [Referrals Created Previous Month] )

Referrals Created This Financial Year =
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
VAR year_start = DATE ( YEAR ( as_of ) - IF ( MONTH ( as_of ) < 4, 1, 0 ), 4, 1 )
RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], year_start, as_of ) ) )

Referrals Currently Active =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Referrals Under Offer =
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[is_open] = TRUE () ), KEEPFILTERS ( 'fact_referral'[current_status] = "UNDER_OFFER" ) )

Closed or Cancelled Referrals =
CALCULATE (
    [Total Referrals],
    FILTER (
        'fact_referral',
        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
            IN { "closed", "cancelled", "withdrawn", "completed" }
    )
)

Active Referrals With Provider Engagement =
VAR engaged_referral_ids =
	CALCULATETABLE (
		VALUES ( 'fact_referral_provider'[referral_id] ),
		'fact_referral_provider'[is_engaged] = TRUE ()
	)
RETURN
	CALCULATE (
		[Total Referrals],
		'fact_referral'[is_open] = TRUE (),
		TREATAS ( engaged_referral_ids, 'fact_referral'[referral_id] )
	)

Active Referral Engagement Rate =
DIVIDE ( [Active Referrals With Provider Engagement], [Referrals Currently Active] )

Active Awaiting Offers With Engagement =
VAR engaged_referral_ids =
	CALCULATETABLE (
		VALUES ( 'fact_referral_provider'[referral_id] ),
		'fact_referral_provider'[is_engaged] = TRUE ()
	)
RETURN
	CALCULATE (
		[Total Referrals],
		'fact_referral'[is_open] = TRUE (),
'fact_referral'[is_awaiting_offer] = TRUE (),
		TREATAS ( engaged_referral_ids, 'fact_referral'[referral_id] )
	)

Active Awaiting Offers Without Engagement =
VAR awaiting_referral_ids =
	CALCULATETABLE (
		VALUES ( 'fact_referral'[referral_id] ),
		'fact_referral'[is_awaiting_offer] = TRUE ()
	)
VAR engaged_referral_ids =
	CALCULATETABLE (
		VALUES ( 'fact_referral_provider'[referral_id] ),
		'fact_referral_provider'[is_engaged] = TRUE ()
	)
RETURN
	CALCULATE (
		[Total Referrals],
		TREATAS (
			EXCEPT ( awaiting_referral_ids, engaged_referral_ids ),
			'fact_referral'[referral_id]
		)
	)

Emergency Referrals =
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ), KEEPFILTERS ( 'fact_referral'[is_emergency_placement] = TRUE () ) )

Planned Referrals =
CALCULATE (
    [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ),
    KEEPFILTERS ( FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[referral_created_date] ) && NOT ISBLANK ( 'fact_referral'[required_placement_date] ) && 'fact_referral'[is_emergency_placement] = FALSE () ) )
)

Emergency Placement Rate =
DIVIDE ( [Emergency Referrals], [Total Referrals] )

Referrals With Multiple Provider Assignments =
CALCULATE ( [Total Referrals], 'fact_referral'[provider_assignment_count] > 1 )
```

Use `fact_referral[referral_closure_reason]`,
`fact_referral[placement_type_required]`, `fact_referral[priority]` and
`fact_referral[complexity_band]` directly as visual dimensions with the
appropriate referral count measure. This ports the legacy closed-reason and
placement-type visual logic without creating redundant measures.

### Offer, spot/framework and draft/pending-offer portfolio

```DAX
Non-Draft Offers =
CALCULATE (
    [Offers Submitted],
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_status] ) && LOWER ( 'fact_offer'[offer_status] ) <> "draft" ) )
)

Pending Offers =
CALCULATE (
    [Offers Submitted],
    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } ) )
)

Unsuccessful Offers =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
            IN { "declined", "rejected", "withdrawn", "offer_unsuccessful", "offer_withdrawn" }
    )
)

Offers With Recorded Rejection Reason =
CALCULATE (
    [Offers Submitted],
    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[rejection_reason] ) )
)

Providers Who Made Offers =
CALCULATE (
    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
    FILTER (
        'fact_offer',
        NOT (
            LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
                IN { "draft", "withdrawn", "offer_withdrawn" }
        )
    ))

Average Offers per Provider =
DIVIDE ( [Non-Draft Offers], [Providers Who Made Offers] )

Average Offers per Referral Under Offer =
DIVIDE (
    CALCULATE (
        [Non-Draft Offers],
        FILTER (
            'fact_referral',
            'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
        )
    ),
    [Referrals Under Offer]
)

Offers on Referrals Under Offer =
CALCULATE (
    [Non-Draft Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Spot Offers =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home'[is_spot] = TRUE () )

Non-Spot Offers =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home'[is_spot] = FALSE () )

Spot Offer Rate =
DIVIDE ( [Spot Offers], [Non-Draft Offers] )

Draft Offers With No Activity Since Creation =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_no_activity] = TRUE () )

Draft Offers With Activity Since Creation =
CALCULATE (
    [Offers in Draft],
    KEEPFILTERS ( 'fact_offer'[is_draft_no_activity] = FALSE () ),
    KEEPFILTERS ( 'fact_offer'[is_draft_missing_dates] = FALSE () )
)

Draft Offers Missing Dates =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_missing_dates] = TRUE () )

Draft Offers Stalled 14+ Days =
CALCULATE (
	[Offers Submitted],
	FILTER (
		'fact_offer',
		LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
			&& 'fact_offer'[days_since_offer_activity] >= 14
	)
)

Average Days in Draft =
AVERAGEX (
	FILTER (
		'fact_offer',
		LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
			&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
	),
	'fact_offer'[offer_age_days]
)

Oldest Draft Age Days =
MAXX (
	FILTER (
		'fact_offer',
		LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
			&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
	),
	'fact_offer'[offer_age_days]
)

Draft Offers With No Activity % =
DIVIDE ( [Draft Offers With No Activity Since Creation], [Offers in Draft] )

Pending Offers 0-7 Days =
CALCULATE (
    [Pending Offers],
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 0 && 'fact_offer'[offer_age_days] <= 7 ) )
)

Pending Offers 8-14 Days =
CALCULATE (
    [Pending Offers],
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 8 && 'fact_offer'[offer_age_days] <= 14 ) )
)

Pending Offers 15-29 Days =
CALCULATE (
    [Pending Offers],
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 15 && 'fact_offer'[offer_age_days] <= 29 ) )
)

Pending Offers 30+ Days =
CALCULATE (
    [Pending Offers],
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 30 ) )
)

Providers With Pending Offers 30+ Days =
CALCULATE (
    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } && 'fact_offer'[offer_age_days] >= 30 ) )
)

Latest Offer Source Export =
MAX ( 'fact_offer'[source_export_date] )
```

Use `fact_offer[offer_status]`, `fact_offer[offer_type]`,
`fact_offer[rejection_reason]`, and `dim_provider[provider_name]` as visual
dimensions for the historic offer-status, decline-reason and provider ranking
tables.

### Provider register, framework, QA and documentation

```DAX
Provider Homes Registered =
IF ( ISFILTERED ( 'dim_provider' ),
    CALCULATE ( DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] ), KEEPFILTERS ( TREATAS ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider_home'[provider_id] ) ) ),
    DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] )
)

Providers Registered =
DISTINCTCOUNT(dim_provider[provider_id])

Providers - Fostering =
VAR framework_providers = CALCULATETABLE ( VALUES ( 'bridge_provider_framework'[provider_id] ), FILTER ( 'dim_framework', LOWER ( 'dim_framework'[placement_type] ) IN { "fostering", "plcm-fost" } ) )
VAR home_providers = CALCULATETABLE ( VALUES ( 'dim_provider_home'[provider_id] ), FILTER ( 'dim_provider_home', LOWER ( 'dim_provider_home'[service_type] ) IN { "fostering", "plcm-fost" } ) )
RETURN CALCULATE ( [Providers Registered], KEEPFILTERS ( TREATAS ( DISTINCT ( UNION ( framework_providers, home_providers ) ), 'dim_provider'[provider_id] ) ) )

Providers - Residential =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
    'dim_provider_home'[service_type] = "Residential"
)

Providers - Supported Accommodation =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
    'dim_provider_home'[service_type] = "Supported Accommodation"
)

Residential Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Residential" )

Supported Accommodation Homes =
CALCULATE (
    [Provider Homes Registered],
    'dim_provider_home'[service_type] = "Supported Accommodation"
)

Fostering Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Fostering" )

Framework Providers =
DISTINCTCOUNT(bridge_provider_framework[provider_id])

Non-Framework Providers =
COUNTROWS (
    EXCEPT (
        VALUES ( 'dim_provider'[provider_id] ),
        VALUES ( 'bridge_provider_framework'[provider_id] )
    )
)

Providers With QA Flags =
CALCULATE ( [Providers Registered], KEEPFILTERS ( 'dim_provider'[qa_flag] = TRUE () ) )

QA Flagged Homes =
VAR flagged_providers = CALCULATETABLE ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider'[qa_flag] = TRUE () )
VAR selected_providers = VALUES ( 'dim_provider'[provider_id] )
RETURN
    CALCULATE (
        [Provider Homes Registered],
        KEEPFILTERS ( TREATAS ( selected_providers, 'dim_provider_home'[provider_id] ) ),
        KEEPFILTERS ( FILTER ( 'dim_provider_home', 'dim_provider_home'[qa_flag] = TRUE () || 'dim_provider_home'[provider_id] IN flagged_providers ) )
    )

Providers Pending Onboarding =
CALCULATE (
    [Providers Registered],
    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "pending" )
)

Providers Approved =
CALCULATE (
    [Providers Registered],
    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "approved" )
)

Provider Onboarding Success Rate =
DIVIDE ( [Providers Approved], [Providers Registered] )

Provider Submission Documents =
DISTINCTCOUNT ( 'dim_provider_submission_document'[document_id] )

Documents Expiring Next 30 Days =
CALCULATE (
    [Provider Submission Documents],
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] >= TODAY ()
            && 'dim_provider_submission_document'[expiry_date] <= TODAY () + 30
    )
)

Documents Expired =
CALCULATE (
    [Provider Submission Documents],
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
    )
)

Provider Homes With Expired Documents =
CALCULATE (
    DISTINCTCOUNT ( 'dim_provider_submission_document'[home_id] ),
    FILTER (
        'dim_provider_submission_document',
        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
    )
)
```

### IPA, cost and referral-lifecycle measures

Create an inactive `dim_date[date]` to `fact_ipa[ipa_issued_date]`
relationship and use `USERELATIONSHIP` (or make it active only on an IPA
report page) for the issued-date time-intelligence measures below.

```DAX
IPAs Issued This Month =
VAR as_of = MAX ( 'fact_ipa'[as_of_date] )
RETURN IF ( NOT ISBLANK ( as_of ),
    CALCULATE ( [IPAs Created],
        CROSSFILTER ( 'dim_date'[date], 'fact_referral'[referral_created_date], NONE ),
        USERELATIONSHIP ( 'dim_date'[date], 'fact_ipa'[ipa_issued_date] ),
        DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of )
    )
)

Closed IPAs =
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = TRUE () )

Average Active IPA Weekly Cost =
DIVIDE ( [Estimated Active Weekly Cost], [Active IPAs] )

Total IPA Weekly Cost =
SUM ( 'fact_ipa'[estimated_weekly_cost] )

Accepted Offers With IPA =
VAR linked_offers = VALUES ( 'fact_ipa'[accepted_offer_id] )
RETURN CALCULATE ( [Accepted Offers], KEEPFILTERS ( TREATAS ( linked_offers, 'fact_offer'[offer_id] ) ) )

Offers Awaiting IPA Creation =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_awaiting_ipa_creation] = TRUE () )

Accepted Offer to IPA Conversion % =
DIVIDE ( [IPAs Created], [Accepted Offers] )

Offers Still to Progress to IPA % =
IF ( NOT ISBLANK ( [Accepted Offer to IPA Conversion %] ), 1 - [Accepted Offer to IPA Conversion %] )

Referrals With Fully Signed IPA =
CALCULATE ( DISTINCTCOUNT ( 'fact_ipa'[referral_id] ), KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )

IPA Signature Completion Rate =
DIVIDE ( [IPA Completed], [IPAs Created] )

Referral Lifecycle Events =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[event_id] )

Referrals With Lifecycle Activity =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[referral_id] )

Average Lifecycle Events per Referral =
DIVIDE ( [Referral Lifecycle Events], [Referrals With Lifecycle Activity] )

Provider Messages Sent =
CALCULATE (
    [Referral Lifecycle Events],
    'fact_referral_lifecycle_event'[event_type] = "ProviderMessageSent"
)

Gold Model Last Refreshed =
MAX ( 'fact_referral'[gold_modelled_at] )
```

`Accepted Offers With IPA` transfers the current IPA offer IDs to the offer fact and counts accepted offers. The separate `IPAs Created` measure counts individual IPAs. `Offers Awaiting IPA Creation` uses the Gold offer flag. These measures deliberately retain their different grains.

## Legacy v15 reconciliation

| Historic KPI groups now portable | Use the measures above / visual dimensions |
| --- | --- |
| KPI-01–10, 19–24, 29–39, 87–90 | Referral, gender (via `dim_person[gender_clean]`), offer, provider-engagement, time, closure reason, status, assignment overlap and export measures. |
| KPI-11–18, 25–28, 53–72 | Provider activity, offer portfolio, spot/non-spot, draft and pending age measures. |
| KPI-40–52, 97, 99–101, 104, 116–117 | Provider/home register, framework coverage, QA flags, document expiry and onboarding measures. |
| KPI-73–76, 79, 83–84, 107, 110 and 113 | IPA volume/cost, accepted-offer conversion, provider-message volume proxy and lifecycle-activity measures. |
| KPI-114 | IPA-level signature counts and completion rate now use the new Gold signature fields. |
| KPI-115 | Durable referral-update history remains unavailable; lifecycle events are a separate activity measure. |
| KPI-91–94 | Emergency/planned referral measures using created and required-placement dates. |

| Do not recreate yet | Missing active-Gold field or grain |
| --- | --- |
| KPI-95–96 | `fact_referral[region]` is not populated; provider geography is not a safe referral-region substitute. |
| KPI-98 | Only one provider/home QA flag is published, not the historic flag-type breakdown. |
| KPI-102–103 | The current document fact has no documented expected-document set or blocking outcome, so compliance cannot be calculated. |
| KPI-105–106 | No referral-level decline-reason or framework-change history fact. Use offer rejection reasons only. |
| KPI-108–109 and KPI-111–112 | No payment, invoice, detailed provider-message or message-status facts. `Provider Messages Sent` is supported as a lifecycle-event proxy only. |
| KPI-115 | No durable referral update timestamp; lifecycle events provide the supported activity measure. |
| Child support needs and referral categories | No active Gold dimension/fact at the required analysis grain. |

For any unsupported item, add the missing Gold fact/dimension first; do not
point DAX at Bronze, Silver, or a legacy imported table as a workaround.

## Deployment checklist

1. Run `04_gold_model.ipynb`, which publishes snake-case fact fields, retires
   `fact_placement`, and creates `fact_ipa`.
2. Run `05_gold_dimensions.ipynb`, which publishes snake-case dimension and
   bridge fields.
3. Refresh the Lakehouse semantic model and remove old imported tables.
4. Create the active relationships, then add the DAX above.
5. Reconcile totals by `referral_id`, `offer_id`, `ipa_id`, and
   `referral_provider_id` before rebuilding visual pages.

## Legacy v15 full-library port

This section reconciles **all 153 measures** extracted from the legacy
`SM WMPP v15.zip` semantic model (`_Measures` table, TMDL) against the Gold
build guide. Disposition:

| Disposition | Count | Meaning |
| --- | ---: | --- |
| Already covered (identical or alias) | 62 | Served by a measure in the sections above (rev 3: includes the 4 gender measures now supported via `dim_person[gender_clean]`, GLD-006/GLD-007) |
| Newly ported in this revision | 68 | Copy-ready Gold DAX below (rev 4: +6 IPA-signature measures now on offer-grain Gold flags `fact_offer[is_ipa_completed]` / `[is_ipa_pending]` / `[is_awaiting_ipa_creation]`, GLD-013) |
| Retired report-construct helpers | 15 | Not recreated; reasons listed below |
| Blocked by missing Gold source fields | 8 | Added to the do-not-recreate list |
| **Total legacy v15 measures** | **153** | |

Every ported measure references active Gold tables only. No `bronze.*`,
`silver.*`, `fact_placement`, `fact_referral_offer`, `dim_referral`,
or `LocalDateTable` reference survives the port. (`dim_offer_status` is now
an active Gold table per GLD-008, rebuilt from Gold `fact_offer` status
codes.)

### Month-on-month measures — state versus flow decision

The client-site v16 model gives each legacy KPI card a previous-month
companion, an absolute variance, a month-on-month percentage, and arrow/colour
indicator measures. However, every stack uses the active `dim_date[date]` to
`fact_referral[referral_created_date]` relationship. For open, closed,
awaiting-offer, under-offer and engagement cards, that answers the wrong
historical question: it compares the **current status of referrals created in
each month**, rather than the status of all referrals **as it stood in each
month**.

Use this rule:

| KPI type | Examples | Historical source |
| --- | --- | --- |
| Stock/state at a point in time | Open, closed, awaiting offer, under offer, open overdue, offer count held by the under-offer population, placement/IPA state | `fact_referral_snapshot`, filtered by the governed snapshot month |
| Flow/event during a period | Referrals created, offers submitted, IPAs issued, closures occurring during the month | The event-grain fact and its event-date relationship |
| Cohort outcome | Share of referrals created in a month that later received an offer | `fact_referral` by creation month, with a clearly labelled maturation/as-of rule |

The approved snapshot pattern, required Gold fields, DAX and validation tests
are in [Snapshot Month-on-Month KPI guide](SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md).
In particular, add historical engagement evidence to the snapshot before
moving `Active Referral Engagement Rate`; the current snapshot has
`provider_assignment_count` but not the current provider-level `is_engaged`
state.

The creation-date stacks below are retained only as a **legacy binding
inventory**. They are valid for a measure that is explicitly a creation cohort
or event flow. Do not use them for state-at-month cards. Repair the missing
`Open Referral Previous Month` report bindings by moving those visuals to the
snapshot family, not by reinstating the old creation-date calculation as the
final solution.

For an approved event/cohort stack, the generic pattern remains:

```DAX
<Base> Previous Month = CALCULATE ( [<Base>], DATEADD ( 'dim_date'[date], -1, MONTH ) )
<Base> Variance = [<Base>] - [<Base> Previous Month]
<Base> MoM % = DIVIDE ( [<Base> Variance], [<Base> Previous Month] )
<Base> Variance Indicator = IF ( [<Base> Variance] > 0, "▲", IF ( [<Base> Variance] < 0, "▼", "–" ) )
<Base> Variance Indicator Color = IF ( [<Base> Variance] > 0, "green", IF ( [<Base> Variance] < 0, "red", "grey" ) )
```

Copy-ready stacks for every legacy KPI card:

```DAX
-- Legacy card: Total Referrals
Total Referrals Previous Month =
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Total Referrals Variance =
[Total Referrals] - [Total Referrals Previous Month]

Total Referrals MoM % =
DIVIDE ( [Total Referrals Variance], [Total Referrals Previous Month] )

Total Referrals Variance Indicator =
IF ( [Total Referrals Variance] > 0, "▲", IF ( [Total Referrals Variance] < 0, "▼", "–" ) )

Total Referrals Variance Indicator Color =
IF ( [Total Referrals Variance] > 0, "green", IF ( [Total Referrals Variance] < 0, "red", "grey" ) )

Open Referrals Previous Month =
CALCULATE ( [Open Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Open Referrals Variance =
[Open Referrals] - [Open Referrals Previous Month]

Open Referrals MoM % =
DIVIDE ( [Open Referrals Variance], [Open Referrals Previous Month] )

Open Referrals Variance Indicator =
IF ( [Open Referrals Variance] > 0, "▲", IF ( [Open Referrals Variance] < 0, "▼", "–" ) )

Open Referrals Variance Indicator Color =
IF ( [Open Referrals Variance] > 0, "green", IF ( [Open Referrals Variance] < 0, "red", "grey" ) )

Closed Referrals Previous Month =
CALCULATE ( [Closed Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Closed Referrals Variance =
[Closed Referrals] - [Closed Referrals Previous Month]

Closed Referrals MoM % =
DIVIDE ( [Closed Referrals Variance], [Closed Referrals Previous Month] )

Closed Referrals Variance Indicator =
IF ( [Closed Referrals Variance] > 0, "▲", IF ( [Closed Referrals Variance] < 0, "▼", "–" ) )

Closed Referrals Variance Indicator Color =
IF ( [Closed Referrals Variance] > 0, "green", IF ( [Closed Referrals Variance] < 0, "red", "grey" ) )

Referrals With an Offer Previous Month =
CALCULATE ( [Referrals With an Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals With an Offer Variance =
[Referrals With an Offer] - [Referrals With an Offer Previous Month]

Referrals With an Offer MoM % =
DIVIDE ( [Referrals With an Offer Variance], [Referrals With an Offer Previous Month] )

Referrals With an Offer Variance Indicator =
IF ( [Referrals With an Offer Variance] > 0, "▲", IF ( [Referrals With an Offer Variance] < 0, "▼", "–" ) )

Referrals With an Offer Variance Indicator Color =
IF ( [Referrals With an Offer Variance] > 0, "green", IF ( [Referrals With an Offer Variance] < 0, "red", "grey" ) )

Referrals Awaiting Offer Previous Month =
CALCULATE ( [Referrals Awaiting Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Awaiting Offer Variance =
[Referrals Awaiting Offer] - [Referrals Awaiting Offer Previous Month]

Referrals Awaiting Offer MoM % =
DIVIDE ( [Referrals Awaiting Offer Variance], [Referrals Awaiting Offer Previous Month] )

Referrals Awaiting Offer Variance Indicator =
IF ( [Referrals Awaiting Offer Variance] > 0, "▲", IF ( [Referrals Awaiting Offer Variance] < 0, "▼", "–" ) )

Referrals Awaiting Offer Variance Indicator Color =
IF ( [Referrals Awaiting Offer Variance] > 0, "green", IF ( [Referrals Awaiting Offer Variance] < 0, "red", "grey" ) )

Referrals Under Offer Previous Month =
CALCULATE ( [Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Under Offer Variance =
[Referrals Under Offer] - [Referrals Under Offer Previous Month]

Referrals Under Offer MoM % =
DIVIDE ( [Referrals Under Offer Variance], [Referrals Under Offer Previous Month] )

Referrals Under Offer Variance Indicator =
IF ( [Referrals Under Offer Variance] > 0, "▲", IF ( [Referrals Under Offer Variance] < 0, "▼", "–" ) )

Referrals Under Offer Variance Indicator Color =
IF ( [Referrals Under Offer Variance] > 0, "green", IF ( [Referrals Under Offer Variance] < 0, "red", "grey" ) )

Referrals Currently Active Previous Month =
CALCULATE ( [Referrals Currently Active], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Referrals Currently Active Variance =
[Referrals Currently Active] - [Referrals Currently Active Previous Month]

Referrals Currently Active MoM % =
DIVIDE ( [Referrals Currently Active Variance], [Referrals Currently Active Previous Month] )

Referrals Currently Active Variance Indicator =
IF ( [Referrals Currently Active Variance] > 0, "▲", IF ( [Referrals Currently Active Variance] < 0, "▼", "–" ) )

Referrals Currently Active Variance Indicator Color =
IF ( [Referrals Currently Active Variance] > 0, "green", IF ( [Referrals Currently Active Variance] < 0, "red", "grey" ) )

Closed or Cancelled Referrals Previous Month =
CALCULATE ( [Closed or Cancelled Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Closed or Cancelled Referrals Variance =
[Closed or Cancelled Referrals] - [Closed or Cancelled Referrals Previous Month]

Closed or Cancelled Referrals MoM % =
DIVIDE ( [Closed or Cancelled Referrals Variance], [Closed or Cancelled Referrals Previous Month] )

Closed or Cancelled Referrals Variance Indicator =
IF ( [Closed or Cancelled Referrals Variance] > 0, "▲", IF ( [Closed or Cancelled Referrals Variance] < 0, "▼", "–" ) )

Closed or Cancelled Referrals Variance Indicator Color =
IF ( [Closed or Cancelled Referrals Variance] > 0, "green", IF ( [Closed or Cancelled Referrals Variance] < 0, "red", "grey" ) )

Active Referral Engagement Rate Previous Month =
CALCULATE ( [Active Referral Engagement Rate], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Active Referral Engagement Rate Variance =
[Active Referral Engagement Rate] - [Active Referral Engagement Rate Previous Month]

Active Referral Engagement Rate MoM % =
DIVIDE ( [Active Referral Engagement Rate Variance], [Active Referral Engagement Rate Previous Month] )

Active Referral Engagement Rate Variance Indicator =
IF ( [Active Referral Engagement Rate Variance] > 0, "▲", IF ( [Active Referral Engagement Rate Variance] < 0, "▼", "–" ) )

Active Referral Engagement Rate Variance Indicator Color =
IF ( [Active Referral Engagement Rate Variance] > 0, "green", IF ( [Active Referral Engagement Rate Variance] < 0, "red", "grey" ) )

Offers on Referrals Under Offer Previous Month =
CALCULATE ( [Offers on Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Offers on Referrals Under Offer Variance =
[Offers on Referrals Under Offer] - [Offers on Referrals Under Offer Previous Month]

Offers on Referrals Under Offer MoM % =
DIVIDE ( [Offers on Referrals Under Offer Variance], [Offers on Referrals Under Offer Previous Month] )

Offers on Referrals Under Offer Variance Indicator =
IF ( [Offers on Referrals Under Offer Variance] > 0, "▲", IF ( [Offers on Referrals Under Offer Variance] < 0, "▼", "–" ) )

Offers on Referrals Under Offer Variance Indicator Color =
IF ( [Offers on Referrals Under Offer Variance] > 0, "green", IF ( [Offers on Referrals Under Offer Variance] < 0, "red", "grey" ) )

Offer Receipt Rate (Created in Period) Previous Month =
CALCULATE ( [Offer Receipt Rate (Created in Period)], DATEADD ( 'dim_date'[date], -1, MONTH ) )

Offer Receipt Rate (Created in Period) Variance =
[Offer Receipt Rate (Created in Period)] - [Offer Receipt Rate (Created in Period) Previous Month]

Offer Receipt Rate (Created in Period) MoM % =
DIVIDE ( [Offer Receipt Rate (Created in Period) Variance], [Offer Receipt Rate (Created in Period) Previous Month] )

Offer Receipt Rate (Created in Period) Variance Indicator =
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "▲", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "▼", "–" ) )

Offer Receipt Rate (Created in Period) Variance Indicator Color =
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "green", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "red", "grey" ) )
```

> The legacy `Provider Contact Referral` card family (6 measures) is
> **not** ported: there is no `contact_made` field anywhere in the
> active Gold layer. See the blocked list below.


### Created-in-period measures

These replace the legacy `USERELATIONSHIP(dim_date[Date],
dim_referral[referral_date_only])` pattern; the Gold active relationship
already filters on `referral_created_date`.

```DAX
Referrals Not Yet Closed (Created in Period) =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )

Referrals With Offers (Created in Period) =
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )

Offer Receipt Rate (Created in Period) =
DIVIDE ( [Referrals With Offers (Created in Period)], [Total Referrals] )
```

> `Offer Receipt Rate (Created in Period)` ports the legacy measure named
> `Total Referrals That Received Offers`, which despite its name returns a
> ratio, not a count.

### Under-offer referral offer portfolio

The legacy model scoped offer measures to referrals in `UNDER_OFFER` status
through a chain of `CALCULATETABLE`/`TREATAS` helper measures. In Gold the
active `fact_referral` to `fact_offer` relationship makes this a single
cross-table filter, matching the existing `Offers on Referrals Under Offer`
pattern.

```DAX
Draft Offers on Referrals Under Offer =
CALCULATE (
    [Offers in Draft],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Pending Offers on Referrals Under Offer =
CALCULATE (
    [Pending Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Successful Offers on Referrals Under Offer =
CALCULATE (
    [Accepted Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Unsuccessful Offers on Referrals Under Offer =
CALCULATE (
    [Unsuccessful Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Spot Offers on Referrals Under Offer =
CALCULATE (
    [Spot Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Framework Offers on Referrals Under Offer =
CALCULATE (
    [Non-Spot Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Providers With Offers on Referrals Under Offer =
CALCULATE (
    [Providers Who Made Offers],
    FILTER (
        'fact_referral',
        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
    )
)

Average Offers per Provider - Under Offer =
DIVIDE (
    [Offers on Referrals Under Offer],
    [Providers With Offers on Referrals Under Offer]
)

Draft Offers With No Activity - Under Offer Referrals =
CALCULATE (
	[Draft Offers With No Activity Since Creation],
	FILTER (
		'fact_referral',
		'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
	)
)

Draft Offers Stalled 14+ Days - Under Offer Referrals =
CALCULATE (
	[Draft Offers Stalled 14+ Days],
	FILTER (
		'fact_referral',
		'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
	)
)
```

> Legacy `Draft Offer Count (Under Offer Referrals)` and `Offers per Provider
> (Under Offer Referrals)` are exact duplicates of `Draft Offers on Referrals
> Under Offer` and `Offers on Referrals Under Offer`; they are not recreated
> as separate measures.

### IPA signature funnel

The legacy funnel (`IPA Created`, `IPA Completed`, `IPAs Pending Completion`,
`IPA Created to Completion %`, `Successful Offers to IPA Completed %`) read
`fact_ipa[signed_by_provider]` and `fact_ipa[signed_by_local_authority]`.
Gold now also exposes `signed_by_provider`, `signed_by_local_authority`, `is_ipa_completed` and `is_ipa_pending` on `fact_ipa`. The report counts individual IPAs for the original signature requirements. Pending excludes closed IPAs. The existing offer flags remain available for offer-row helpers; an offer with several IPAs can have both a completed and a pending IPA.

`Referrals With IPA` counts distinct referral IDs in the IPA fact. `IPA Signature Completion Rate` uses completed IPAs divided by all IPAs; it is no longer a referral-grain proxy.

```DAX
IPA Completed =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )

IPAs Pending Completion =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_pending] = TRUE () ) )

IPA Created to Completion % =
DIVIDE ( [IPA Completed], [IPAs Created] )

Successful Offers to IPA Completed % =
DIVIDE ( [IPA Completed], [Accepted Offers] )

Referrals With IPA =
DISTINCTCOUNT ( 'fact_ipa'[referral_id] )

Referrals With IPA Pending Signature =
CALCULATE ( DISTINCTCOUNT ( 'fact_ipa'[referral_id] ), KEEPFILTERS ( 'fact_ipa'[is_ipa_pending] = TRUE () ) )

IPA Signature Pending Rate =
DIVIDE ( [IPAs Pending Completion], [IPAs Created] )
```

### Snapshot target measures

`fact_referral_snapshot` carries every `fact_referral` column including
`placed_by_required_date`, so the legacy target-at-snapshot pair ports
directly. Legacy `Referrals with Placement at Snapshot` is a name alias of
the existing `Referrals with IPA at Snapshot`.

```DAX
Referrals Placed by Target at Snapshot =
CALCULATE (
    [Snapshot Referrals],
    'fact_referral_snapshot'[placed_by_required_date] = TRUE ()
)

Target Hit Rate at Snapshot =
DIVIDE (
    [Referrals Placed by Target at Snapshot],
    CALCULATE (
        [Snapshot Referrals],
        FILTER (
            'fact_referral_snapshot',
            NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
                && NOT ISBLANK ( 'fact_referral_snapshot'[required_placement_date] )
        )
    )
)
```

### Row-level visual helpers

Legacy per-row Yes/No flags used on the IPA funnel and provider registry
pages. These evaluate in a single-row visual context (`SELECTEDVALUE`); they
are not aggregation measures.

```DAX
Is Non Framework Provider =
IF ( CALCULATE ( COUNTROWS ( 'bridge_provider_framework' ) ) = 0, 1, 0 )

IPA Exists =
IF (
    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ) ) > 0, "Yes", "No" ),
    IF ( [IPAs Created] > 0, "Yes", "No" )
)

Is Awaiting IPA Creation =
IF ( COALESCE ( SELECTEDVALUE ( 'fact_offer'[is_awaiting_ipa_creation] ), FALSE () ), 1, 0 )

Is IPA Completed =
IF (
    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_completed] = TRUE () ) > 0, 1, 0 ),
    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_completed], FALSE () ), 1, 0 )
)

Is IPA Pending =
IF (
    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_pending] = TRUE () ) > 0, 1, 0 ),
    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_pending], FALSE () ), 1, 0 )
)
```


### Legacy-to-Gold alias map

These legacy measures are already satisfied by an existing Gold measure
under a different name; rename visuals at reconciliation time, do not
recreate.

| Legacy v15 measure | Gold measure |
| --- | --- |
| Open Referral | Open Referrals |
| Referrals This Month | Referrals Created This Month |
| Referrals This FY | Referrals Created This Financial Year |
| Referrals With Offers / Referrals With One or More Offers | Referrals With an Offer |
| Active Referrals Awaiting Offers | Referrals Awaiting Offer |
| Active Referrals Under Offer | Referrals Under Offer |
| Referrals Cancelled/Closed | Closed or Cancelled Referrals |
| Closed Referrals (by Reason) | Closed Referrals + `fact_referral[referral_closure_reason]` visual dimension |
| Active Awaiting Offers (Engaged) | Active Referrals With Provider Engagement |
| Active Awaiting Offers (No Engagement) | Active Awaiting Offers Without Engagement |
| Offer Count / Total Offers Made Historically / (NEW)Total Offers Made / Latest Offer Status Count | Offers Submitted (Gold `fact_offer` holds the latest state per offer) |
| Placement Type Totals (Visual) | Total Referrals + `fact_referral[placement_type_required]` visual dimension |
| Offers At Risk (8-14 Days) | Pending Offers 8-14 Days |
| Offers Outside Timeframe (15-30 Days) | Pending Offers 15–30 Days (original inclusive boundary; overlaps 30+ on day 30) |
| Critical Offers (30+ Days) | Pending Offers 30+ Days |
| Provider with Offers over 30+ Days | Providers With Pending Offers 30+ Days |
| Draft No Activity 7+ Days | Draft Offers Stalled 7+ Days |
| Drafts With No Activity 14+ Days | Draft Offers Stalled 14+ Days |
| Draft Offers Updated After Creation | Draft Offers With Activity Since Creation |
| Draft With No Activity Since Creation (%) | Draft Offers With No Activity % |
| Latest Export per Offer | Latest Offer Source Export |
| Dashboard Last Refreshed: | Gold Model Last Refreshed |
| Average Active Weekly Cost | Average Active IPA Weekly Cost |
| Overlap Referrals | Referrals With Multiple Provider Assignments |
| Fostering Providers | Providers - Fostering |
| NON Framework Providers | Non-Framework Providers |
| Total Offers Made (Active Referrals Under Offer) | Offers on Referrals Under Offer |
| Avg Offers per Referral Under Offer | Average Offers per Referral Under Offer |
| IPA Created (successful offers with IPA) | Accepted Offers With IPA |
| IPAs Created | IPAs Created (identical name) |
| Offers Still to Progress to IPA | Offers Awaiting IPA Creation |
| Referrals with Placement at Snapshot | Referrals with IPA at Snapshot |
| IPA Completed / IPA Created to Completion % / Successful Offers to IPA Completed % | Offer-grain measures: IPA Completed, IPA Created to Completion %, Successful Offers to IPA Completed % (GLD-013) |

### Retired report-construct helpers

These legacy measures exist only to drive v15 report navigation or SCD
latest-export logic. They are deliberately **not** recreated in the Gold
model.

| Legacy v15 measure | Why retired |
| --- | --- |
| Accepted Offers Base / Accepted Offers (Scoped Table) / Offer IDs (Under Offer Referrals) | Internal `CALCULATETABLE` helpers; the Gold relationship graph and `TREATAS` patterns make them unnecessary |
| KPI Tooltip Style 1 | Reads the `ref_KPI` functional-spec metadata table, which is not a Gold object; re-import `ref_KPI` as a static table if the tooltip page is rebuilt |
| Directory Summary Count / Fostering Chart Count | Depend on the `Directory Summary Axis` and `rpt_provider_fostering` report-view tables; rebuild with field parameters over `dim_provider_home[service_type]` |
| Pending Offers by Age Bucket | Depended on the disconnected `Draft Age Band Table`; the four pending-age measures cover the same bands |
| Latest Export per Offer / Latest Offer Status Count | Gold `fact_offer` is already deduplicated to the latest state per offer |
| Dashboard Last Refreshed: | Superseded by Gold Model Last Refreshed (`gold_modelled_at`) |

### Additional blocked legacy measures

These rows extend the do-not-recreate list above; they must not be pointed
at Bronze, Silver or legacy tables.

| Do not recreate yet | Missing active-Gold field or grain |
| --- | --- |
| Provider Contact Referral card family (6 measures: base, Previous Month, Variance, MoM %, Indicator, Indicator Color) | No provider-contact flag (legacy `dim_referral[contact_made]`) anywhere in the active Gold referral fact. `is_not_seen_by_providers` is an offer-visibility flag, not a safe substitute. |
| Is In Accepted KPI | Row-level accepted-KPI visual state from the legacy report layout; use the IPA/offer-context `Is IPA Completed` / `Is IPA Pending` and offer-only `Is Awaiting IPA Creation` helpers and the `Accepted Offers` measure instead. |

The legacy Female / Male / Other / Total Gendered Referrals measures are no
longer blocked: `dim_person[gender_clean]` and `fact_referral[person_id]`
(GLD-006/GLD-007) support them. Use the copy-ready definitions in the
"Gender referral measures (KPI-04–07)" section.

## Shared report theme — 2026-09-23

Implemented a common Power BI report theme at
`project X/reports/templates/WMPP_Common_Theme.json`, with maintenance instructions
in that folder's `README.md`. The dashboard colours, typography and supported
visual styling are consolidated into 97 reusable presets and applied to all five
current report projects, including the reports paired with the WMPP semantic
models and Mission Control. This is report formatting only: DAX, models,
connections, filters, referral/provider drill-through and the 6/12-month snapshot
window remain unchanged. Source ZIPs and client-deliverables were not modified.

Outstanding: Power BI Desktop visual acceptance of the common theme/presets,
especially table/matrix styling, button states and text contrast. Static checks
do not establish rendered appearance or live-data access. Client-environment
connection and deployment remain the final workstatement, after user check-in
and acceptance of the other completed work.

The theme QA also identified one pre-existing PBIR schema exception on the
`Requirements Complete` card (`0aef383ced90ab2d5c70`, page
`b95eb4c0b53cd8c60710`) in RPT WMPP v16. It also fails in the original ZIP and
with the pre-theme formatting restored in memory. Investigate/re-save it in
Desktop; no field, filter or data-connection change was made by this theme task.

## Local project consolidation — 2026-09-23

Use `project X/reports/current/SM WMPP v16 updated/SM_WMPP_v16.pbip` as the
latest local WMPP project. Its 45-table semantic model is newer than the
retired nested `SM WMPP v16` model (37 tables). All 16 dashboard pages / 255
visuals, bookmarks and resources have been copied from RPT WMPP v16 into the
active model's attached report. The local `byPath` connection, report identity
and all 53 model files are preserved. Static field, snapshot and drill-through
checks pass; the theme manifest now targets four active reports.

The older `project X/reports/current/SM WMPP v16` folder was removed from
`current` by moving it intact to
`project X/reports/retired/2026-09-23-local-report-consolidation/SM WMPP v16`.
The previous attached report and migration audit are backed up alongside it.
No permanent deletion was performed; source ZIPs and the client-connected RPT
project remain intact.

Outstanding: open the active PBIP in Desktop and accept report rendering. The
existing Requirements Complete card schema exception is inherited by the local
copy and still needs investigation. Local linkage does not supply an offline
data cache; refreshing client-backed partitions still needs client access.
Client reconnection/deployment remains last, after user check-in and acceptance.

## Reference-style correction — 2026-09-23

The rejected boxed dashboard layout has been replaced on Board Dashboard,
Provider & Placement Supply and Target & Urgency Performance: single KPI strip
with icons, borderless headings, compact 3 × 2 panels and chart/table switches.
Both report copies have 16 pages / 315 visuals. All 53 model files are unchanged;
no illustrative sample values or unapproved KPI comparisons were introduced.
See `WMPP_REFERENCE_DESIGN_REVIEW.md` for precise changes and recovery locations.

Outstanding: **final design sign-off is blocked on actual Power BI rendering**.
The current session has no accessible Desktop renderer. Obtain Fit-to-page
screenshots of the three pages and complete the visual/interaction acceptance
pass; schema and static layout checks do not meet that acceptance requirement.
