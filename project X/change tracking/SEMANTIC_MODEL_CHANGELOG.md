# Semantic-Model Changelog — report v00 to v01

## 17 October 2026 — New catalogue entries in KPI Definition

Appended `GOLD-KPI-110`–`GOLD-KPI-144` to **KPI Definition rows 119–153** using the existing A:I fields. The sheet now contains 152 records: the unchanged 117 legacy records plus 35 later catalogue entries. Stable Gold identifiers are retained. These are existing WIP measures newly included in this import sheet; no calculation was implemented by this workbook change. The overlapping 144-entry Gold catalogue is unchanged, and 152 is a workbook record count, not an accepted KPI scope baseline. All additions are dated 30 September 2026 based on first catalogue appearance (`70b71eb`). This extends LEGEND-001; no TMDL/PBIR, model measure, relationship or embedded reference table changed. Model synchronisation remains a separate controlled action.

## 17 October 2026 — KPI Date Added metadata

Appended the user-requested `Date Added` field as KPI Definition column I. All 117 original KPI rows first appear in the repository on 26 August 2026 (`b372181`); this is a first-recorded date, not business creation or approval. Original A:H column names/order, KPI values and v1 remain unchanged. Dates are native Excel dates (`dd mmm yyyy`). This is a workbook-only metadata extension to LEGEND-001; no semantic-model table, partition, relationship, measure or reference data changed.

## 17 October 2026 — Legend v1 compatibility and verified coverage

**LEGEND-001 — workbook compatibility repaired; model update pending.** Restored exact v1 workbook schemas and retained 80 RIDs/117 legacy KPI rows. Added separate evidence for 144 catalogue entries, current Python/Spark SQL and exact DAX, and proposed Mission Control requirement contributions. Verified source baseline `0a65e962ff3ab9681ed87d9a0a54df610774b736`; no TMDL, PBIR, relationship, role or measure modification. Embedded ref tables still require separate controlled synchronisation and refresh/UAT. See [calculation evidence](../client%20documentation/04_Data_and_Reporting/KPI_CALCULATION_TRACEABILITY.md).

## 15 October 2026 — Shared report version parameter (RPT-001)

Added a required Power Query text parameter `ReportVersion`, initially `0.16`.
A local one-row import table, `Report Settings`, reads the trimmed parameter;
its hidden string column feeds the visible `Report Version Label` measure.
The measure ignores filters on this disconnected settings table and returns
`Version: ` plus the parameter value. No duplicate hardcoded version fallback
is stored in DAX. Blank parameters raise a refresh error rather than silently
publishing a missing or stale version. Existing data sources, measures,
relationships and roles are unchanged.

All 14 existing version footers retain their text-box type, IDs, geometry,
alignment and theme. Only their static run payload changes to the native
dynamic-value reference and matching shared-measure expression. No new footers
or phone placements are added; existing mobile layouts remain unchanged.

To update: reopen saved WIP, Home > Transform data > Manage Parameters,
select ReportVersion, edit Current Value, then Close & Apply. Refresh the local
Report Settings query if prompted. Publish the updated report/model for online
users. This is a query parameter, not an interactive report slicer.

Validation: six new portable version tests plus 23 mobile tests pass; all 14
visuals pass the published compatible visual contract while retaining their
actual saved schema references. Native TMDL parsing passes: 72 tables, 491
measures, two expressions, unchanged 54 relationships and two roles. All
unlisted report/model/assets and all phone files are byte-preserved. Native
refresh, label rendering and published Viewer acceptance remain unverified.
No live-model write, refresh, publication, ZIP or alternate-project changes.
Backup: `reports/_review/report-version-parameter-before-20261015`.

## 12 October 2026 — Native phone layouts and mobile drawer (MOB-001)

Added separate native Power BI phone layouts in the saved WIP for 31 report,
drillthrough, extract and guide pages. Five tooltip/superseded/scratch pages are
unchanged. Existing desktop visuals and page definitions are preserved byte for
byte; no semantic-model file, measure, relationship, role or connection changed.
The prior performance tuning and provider-home five-provider limit are preserved.

Phone layouts use a 323-point canvas, full-width charts/maps/tables, readable
mobile-only font settings, 44-point-or-larger action targets, vertical explorer
and detail milestones, and compact KPI arrangements. Wide tables retain their
columns and horizontal panning; this is not a table-grain or query rewrite.
Long selection messages wrap at a smaller font; milestone dates are not styled
as large numeric KPIs. Existing chart/table, drillthrough, back and guide actions
remain available. Native filter drawers reuse existing fields and groups with
separate mobile-only close controls and display-only open/close bookmarks.

Added a hamburger-style opener and a display-only navigation drawer on each
phone page. Default/selected rows stay neutral; orange is used on hover, with
the existing charcoal/warm-white/orange palette. Twelve report destinations are
available; the restricted registry extract is not added to the menu and its
existing hidden-page setting is unchanged. Seventy-four navigation bookmarks
and 18 filter-panel bookmarks are scoped and display-only, without resetting
data filters. Power BI uses
show/hide bookmarks, not a smooth sliding animation. New mobile chrome is parked
outside the desktop canvas, rather than over existing desktop visuals.

Validation: all mobile/new-visual/bookmark files pass their exact public schemas;
the saved layout checker finds no default-visible overlaps and confirms all
original report/model hashes. Menu links and touch sizes are checked. Native
Power BI/phone rendering and published Viewer/RLS acceptance remain pending.
No refresh or publication was performed. Reopen the WIP PBIP and inspect
View > Mobile layout before publishing; portrait phone layouts are consumed
in the Power BI mobile app, not the ordinary report browser view.

Delivery manifest and verification report are in the WIP root. Reusable builder
and checker: `project X/tools/plan_wmpp_mobile_layout.py`. Report-definition backup:
`project X/reports/_review/mobile-before-20261012/definition` (excluded from Git).

## 12 October 2026 — Provider Explorer home-table selection cap (PERF-003)

Limited only Provider Explorer's `Provider homes — including homes with no offers`
table to one through five matching providers. Six new measures count the whole
page selection with `ALLSELECTED()`, preserve the existing provider-eligibility
rules, and guard the row-visibility filter plus all three projected offer measures.
With more than five providers, the table returns no rows and its existing title
shows the user-requested `Please select 1 or fewer providers`. The cap remains
five even though the requested warning recommends one. No-match selections are
empty with the normal title. No overlay visual was added.

Native checks of the exact saved expressions pass for one, five, six, unrestricted
and unmatched selections: visible home counts are respectively 7, 18, 0, 0 and 0.
Full-projection comparisons for one and five providers have zero extra/missing
rows and unchanged values. Six-provider and unrestricted full queries return
zero rows in approximately 79 and 125 ms; these are reconstructed native query
workloads, not Performance Analyzer rendering or page-load timings. Durable
read-only regression query: `provider-homes-cap-acceptance.dax` in the WIP root.

Native TMDL parsing passes (71 tables, 490 measures, 54 relationships); the edited
visual passes its exact published 2.7.0 schema. All existing measure expressions,
including the prior 34 performance improvements, are preserved. All other
report/model definition files have unchanged hashes. Table geometry, columns,
display labels, formatting and other visuals are unchanged; only its measure
bindings, visibility filter and title expression changed.

Reopen the saved WIP PBIP to load the changes, reconciling any unsaved Desktop
edits first. No running-model write, refresh, publication, permission, relationship,
connection, ETL, client-deliverable, ZIP or alternate-project change. Desktop
rendering and Viewer/RLS acceptance remain pending.

## 12 October 2026 — Reapplied tuning to replacement WIP (PERF-002)

Reapplied the verified provider-eligibility optimisation to the user-corrected
`project X/reports/WIP/SM WMPP v16 updated WIP` project: 26 measures in
`_Explorer KPI Measures`, eight in `_Report Journey Measures`. All 34 original
expressions were present and the saved definitions matched the open model.
Only the eligibility block was changed; no old report or entire model was copied.
Offer-status/stage restrictions continue to use the original visibility check;
home filtering and all downstream fact calculations are preserved.

Native before/after projection-workload medians: provider directory 2,156.70 to
84.76 ms; provider KPI list 569.26 to 348.47 ms; detail KPI list 567.77 to 269.23 ms;
Page 2 home table 5,472.28 to 1,710.72 ms. Returned-row digests are identical. All
34 base measures match originals for every provider row and totals in 17 filter
scenarios. Saved-file verification confirms exactly the intended 34 expression
changes, unchanged measure metadata and successful TMDL parsing (71 tables,
484 measures, 54 relationships).

Hashes of all report files and other model definitions are identical before/after.
No layout, theme, bookmark, relationship, role, connection, partition, linked-list,
ETL, client-deliverable, ZIP or alternate-project change. The initially supplied
`SM WMPP v16 updated` project was inspected read-only before the path correction.

Reopen the saved PBIP to activate the tuning, preserving any unsaved Desktop edits
before saving over the updated files. No live model write or refresh was performed.
Timings are native reconstructed query workloads, not Performance Analyzer visual
rendering/page-load timings. This run rechecked four hotspots, not the previous
full report inventory; details are in the corrected WIP `PERFORMANCE_REVIEW.json`.

## 11 October 2026 — Native query performance optimisation (PERF-002)

Optimised provider eligibility in 34 saved-WIP measures: 26 in
`_Explorer KPI Measures`, eight in `_Report Journey Measures`. With no offer-status
restriction and stage selection resolving to -1, use current nonblank provider
IDs, intersected with visible home-provider IDs when the home dimension is
directly filtered. Restricted status/stage contexts retain the original
`CALCULATE([Explorer provider row visible])` check. Existing fact calculations,
KEEPFILTERS, signatures, lineage tags, relationships and RLS definitions remain
unchanged. No columns, tables or measures added/removed.

All 36 report pages were inventoried and 283 of 310 reconstructed data workloads
timed against the native Desktop import model. This is not a Performance Analyzer
recording: display/Other timings, generated Desktop queries, slicer/bookmark and
drillthrough contexts are not captured. Twenty-seven workloads remain unmeasured
because of unsupported field parameters/shapes or projection-workload timeouts;
these are coverage gaps, not diagnosed report defects.

Native A/B warm medians, with the same affected dependency chain rebound in both
variants and identical result digests: Provider Explorer directory 2,134.84 to
83.94 ms; provider KPI list 567.45 to 342.30 ms; Provider Detail KPI list 578.66 to
271.18 ms; Page 2 provider-home offer table 5,431.31 to 1,727.20 ms. All exact
saved measures match originals at provider-row and total level in 17 scenarios,
with zero mismatches. Native TMDL parses: 71 tables, 484 measures, 54 relationships.
The complete report-definition JSON hash is unchanged, preserving every layout,
theme, binding, filter, bookmark and navigation setting.

No running-model writes, refresh, publication, permissions, source, ETL,
client-deliverable or ZIP changes. Reopen the saved WIP PBIP to load the changes;
do not overwrite them by saving the old Desktop session without reconciling
unsaved edits. Remaining Performance Analyzer and Viewer/RLS checks are detailed
in the WIP `PERFORMANCE_REVIEW.json`. Reusable read-only projection profiler:
`project X/tools/profile_wmpp_wip.ps1`.

## 11 October 2026 — Source Reference ID on linked provider referrals (SEM-002)

Added a string `Source Reference ID` column to the saved WIP's calculated
`Linked Provider Referrals` table. The existing referral/provider union and UUID
keys remain unchanged; `ADDCOLUMNS` resolves each referral's `person_id` from
`fact_referral`, then reads the actual renamed `dim_person[Source Reference ID]`
field. Missing person/reference values remain blank rather than dropping rows.
This is a display identifier, not a unique referral key or relationship key.

Added the column first in Provider Explorer's supplementary table with a
150-pixel column width. Existing projections, including the user's removed
provider-ID projection, are preserved as found. All 124 visual positions,
sizes and stacking orders remain identical to the user's current layout.
Cancellation/activity filters, measures, KPI, relationships, roles, imports,
other pages, ETL, client deliverables and ZIPs are unchanged.

The exact saved calculated-table expression executed read-only in the native
Power BI engine: 106,267 pairs before/after, zero extra/missing pairs, zero
reference mismatches against the referral/person relationship, and all current
pairs populated. The saved table parses with four calculated-table columns;
the reference has string type. Existing pair/count/card/detail acceptance checks
still pass (Hayshousing: 128 pairs / 56 linked providers). Report JSON passes
published visual 2.12.0 schema compatibility validation, with the original
Desktop-saved 2.13.0 declaration retained in the actual file.

No running-model write or refresh was performed. Reopen the saved PBIP and
refresh to recalculate/populate the new table column; persisted-column rendering
and Viewer/RLS acceptance remain pending. No external location lookup is needed.

## 11 October 2026 — Exclude cancelled linked referrals/responses (SEM-002)

User identified cancelled referrals as the source of the over-broad linked list
and requested exclusions for `fact_referral.current_status = CANCELLED` or
`fact_referral_provider.provider_response_status = Cancelled`. Updated only
`Linked provider row visible` in the saved WIP. Status comparisons ignore case
and surrounding spaces. Cancelled referral IDs are excluded outright; a current
cancelled provider response excludes that exact referral/provider pair on both
the searched and comparison sides. Thus a cancelled searched-provider link
cannot seed the shared-referral list, even if it has offers/messages. Other
providers on an otherwise eligible referral are not excluded merely because a
different provider cancelled its response. Blank/unknown statuses remain allowed.

The table, distinct linked-provider card and existing count/status/message
measures all inherit this shared visibility rule. Assignment-only links remain
excluded. No visual, geometry, relationship, role, connection, ETL, other-page,
client-deliverable or ZIP change; all lineage tags are retained.

Native acceptance went from FAIL (700 actual pairs versus 128 expected;
572 cancelled pairs visible) to PASS. Hayshousing now reconciles to 128 pairs,
56 distinct linked providers, 102 offers, 128 assignments and 244 messages, with
no extra/missing pairs or cancelled-row leaks. Two searched providers yield
9 pairs / 9 linked providers; unmatched/cleared searches remain empty. All text
columns reconcile and the complete model passes the native TMDL parser. The
current dataset has no mixed cancelled/non-cancelled responses on a pair and
no cancelled activity pairs on non-cancelled referrals, so those isolated data
cases cannot be demonstrated against this snapshot. The independent oracle in
`linked-provider-acceptance.dax` now asserts both cancellation exclusions.

Checks used read-only query-local overrides of saved expressions; no running
model write, refresh, publication or permission change. Reopen the PBIP to load
the change. On-screen rendering and Viewer/RLS acceptance remain pending.

## 11 October 2026 — Linked-provider activity detail columns (SEM-002)

The user requested the columns in their pasted linked-provider instructions.
Offer and message counts were already present, so their existing measures and
lineage were retained. Added three measures to `Linked Provider Referrals`:
`Linked offer statuses`, `Linked response statuses`, and `Linked latest message`.
The first two list distinct statuses for exact visible referral/provider pairs.
The preview shows the latest message timestamp and up to 150 text characters,
matched through assignment IDs; timestamp ties use message ID descending. It
is blank for multi-pair aggregates. Unknown/absent records have explicit labels.

Provider Explorer's supplementary table now displays the three added measures,
alongside its UUID keys, provider name, assignment/offer/message counts. Totals
and value wrapping are off; only new text-column widths are capped. All 124
visual positions/sizes/stacking orders and the page dimensions are unchanged.
No change to provider-search eligibility, activity-only linkage, the linked
provider KPI, relationships, RLS, source connections, ETL, other pages, client
deliverables or ZIPs. The pasted conditional offer-status eligibility example
was not applied: this batch adds the requested columns only.

Saved formulas passed native query-local reconciliation for all 700 visible
Hayshousing pairs and 56 pairs with two searched providers: zero offer-status,
response-status or latest-message mismatches against independent fact-key
lookups. Empty/cleared searches yield no text payload, and multi-pair previews
are blank. Existing count/card acceptance checks still pass (103 linked
providers for Hayshousing). The complete model passes the native TMDL parser;
the changed visual passes published 2.12.0 schema compatibility validation with
its Desktop-saved 2.13.0 source declaration preserved. The additional read-only
recheck is `linked-provider-details-acceptance.dax` in the WIP root; it reports
counts/verdicts, never message text. Rendering and Viewer/RLS acceptance remain
pending after reopening the saved PBIP. No running-model write or refresh.

## 11 October 2026 — Approved activity-only linked providers and KPI (SEM-002)

Applies only to `reports/WIP/SM WMPP v16 updated WIP`. Following the user's
approval, this supersedes the assignment-inclusive linked-provider scope in the
repair below. A shared referral now qualifies only when the searched provider
and the other provider each have an offer or recorded message on that referral.
Offers include drafts; messages can be from either sender. Assignment-only
links on either side are excluded. Canonical `dim_provider` search and the
existing linked-table partition, keys, lineage and visibility filter are retained.

Added `Linked Provider Referrals[Linked providers in selection]` and a Provider
Explorer card titled **Linked providers**. It counts each other qualifying
provider once across shared referrals, excludes all searched providers, and
returns zero without a provider search. The card responds to the provider search
but is not narrowed by clicking one row in the linked table. Existing linked
offer/assignment/message measures automatically inherit the narrowed pair scope.

Native read-only DAX reconciliation passed for the saved Hayshousing search
(700 shared referral/provider pairs; 103 distinct other providers), two selected
providers (56 pairs; 42 distinct providers), an unmatched search, and no-search
visibility/card behaviour. Exact offer/assignment/message totals also reconcile.
The entire saved model passed Power BI's native TMDL parser. The three changed
report JSON documents pass the published page 2.1.0 / visual 2.12.0 schemas using
an in-memory schema-label substitution only: Desktop's existing visual 2.13.0
declaration is retained because that schema is not yet published.

All 123 existing visual positions/sizes and the page dimensions are unchanged;
the new card has no bounding-box overlap, including with hidden visuals. No
relationship, role, source connection, client-deliverable or ZIP change. Saved
formulas were tested as query-local overrides, not written to Desktop's running
model. Reopen the PBIP to load them; visual rendering and Viewer/RLS acceptance
remain pending. See SEM-002 and `linked-provider-acceptance.dax` in the WIP root.

## 11 October 2026 — Saved-WIP linked provider referrals repair (SEM-002)

Applies only to `reports/WIP/SM WMPP v16 updated WIP`. Provider Explorer keeps
its canonical `dim_provider[provider_name]` search. Linked-row visibility now
supports provider-only and referral/provider grouping, applies the selected
provider IDs directly to assignment/offer facts, excludes the searched
providers, and is blank without a provider search. Assignment-only links remain
included, as originally requested.

Added distinct linked assignment/message counts and updated the existing linked
offer count to use exact visible referral/provider pairs, including correct
aggregate scope. The supplementary table displays those counts instead of the
debugging visibility flag. Existing lineage tags and all visual geometry,
relationships, source connections, bookmarks and RLS roles are preserved.

Saved expressions passed native read-only DAX reconciliation for the saved
provider search and cleared-search visibility; the complete model passed native
TMDL parsing. Desktop closed before multi-provider/unmatched-search checks.
Rendering and Viewer/RLS acceptance are pending after reopen. See SEM-002 in
`ETL_ISSUE_LOG.md` and the WIP root's `linked-provider-acceptance.dax`.

## 7 October 2026 — Separate saved-WIP identifier update (GLD-024)

This additive change applies to `reports/WIP/SM WMPP v16 updated WIP`, not the
immutable v00/v01 ZIP comparison below. Nine new direct Gold import columns:
`dim_person.source_reference_id`, and reference/count/multiple-referral flag/
sequence on both `fact_referral` and `fact_referral_snapshot`. Existing source
connections, lineage tags and UUID-key relationships remain unchanged.

Thirteen tables now display Source reference, Referral sequence and Multiple
referrals instead of referral UUID. Six identifier searches and the person
search/selection labels use the source reference. Referral Detail uses matching canonical
`fact_referral.source_reference_id` and `fact_referral.order_dupe` fields as
compound drillthrough filters; UUID still supplies the actual internal key.
No business measure was added/rekeyed, and no RLS/export/layout/bookmark change.

Root ETL and saved files are implemented; run Gold 04/05 before model refresh.
Native Power BI row-selection/drillthrough/rendering checks remain pending.
All 32 touched files are backed up under
`reports/WIP/_review/source-reference-identifiers-20261007-734c16`.
See [field semantics and acceptance steps](../client%20documentation/04_Data_and_Reporting/GOLD_REFERRAL_JOURNEY_STATUS.md#source-person-reference-and-multiple-referrals-7-october-2026).

## WMPP Power BI Baseline Reconciliation

| Field | Value |
|---|---|
| **Document Reference** | WMPP-DE-CHG-001 |
| **Version** | 1.0 |
| **Date** | 23 July 2026 |
| **Prepared For** | West Midlands Placement Portal (WMPP) Programme |
| **Status** | Draft for Client Validation |
| **Classification** | Commercial in Confidence |

---

## 1. Purpose and Decision Summary

This document records the verified semantic-model changes between the archived `report v00.zip` and `report v01.zip` Power BI projects. It reconciles those changes with the draft [Statement of Work](06_Statement_of_Work.md) and the legacy [Measures Comparison Checklist](../measures_comparison_checklist.md).

The archive comparison establishes that:

- v00 declares **90 measures**, all as `EXTERNALMEASURE(...)` references to the remote model `DirectQuery to AS - NEW WMPP PILOT DASHBOARD (V13)`.
- v01 retains all **90 measure names**, replaces the external references with local DAX definitions, and adds **5 measures**, giving **95 measures** in total.
- No measure is removed or renamed between the two archives.
- Relationships reduce from **54 to 48**: six date-table relationships are removed; three existing one-to-one relationships are recreated with reversed endpoints; nineteen date relationships change to `datePartOnly`; two relationships become bidirectional; and one export-date relationship becomes inactive.
- The Statement of Work still uses a commercial baseline of **90 migrated + 27 new = 117 KPIs**. If v01 is the accepted migration baseline and the 27 gap measures remain additional, the arithmetic becomes **95 + 27 = 122 KPIs**. This is a scope decision, not an editorial correction, and must be resolved through the Statement of Work change-control process before contractual counts are amended.

**Recommended control position:** preserve all 95 v01 measures as the technical parity baseline, keep the 27 gap measures separate unless the client explicitly confirms an overlap, and raise a formal count-baseline decision under Statement of Work Section 10.

---

## 2. Authoritative Sources and Method

### 2.1 Source controls

| Version | Source archive | Semantic-model path inside archive | SHA-256 | Archive members | Table TMDL files |
|---|---|---|---|---:|---:|
| v00 | `project X/report v00.zip` | `Report/WMPP PILOT DASHBOARD (V13.1).SemanticModel/definition/` | `fb0089ac6d16561e34e1140fe830fa93e3a978e91fc6ad1197b068e9dff157b8` | 381 | 50 |
| v01 | `project X/report v01.zip` | `semantic_model __/SM_WMPP.SemanticModel/definition/` | `db3d5df1151e03cf4e07fa682d28b0af3cc194e158630443c3c9568c93dff4be` | 546 | 79 |

Both archived models use compatibility level 1600. The comparison was performed directly against the ZIP members, not against the mutable extracted working tree. Later repository enhancements, including the separately documented `Closed_Date` calculated columns, are therefore outside this v00-to-v01 delta.

### 2.2 Comparison method

1. Parsed every `measure` declaration across `definition/tables/*.tmdl` in both archives.
2. Matched measures by exact name and compared their source expressions and metadata.
3. Parsed every declaration in `definition/relationships.tmdl`.
4. Matched relationships first by directed `fromColumn`/`toColumn` endpoints and then by undirected endpoint pair to identify direction reversals.
5. Normalised omitted TMDL defaults when comparing relationship semantics:
   - `isActive: true`
   - `crossFilteringBehavior: oneDirection`
   - `fromCardinality: many`
   - `toCardinality: one`
   - `joinOnDateBehavior: dateAndTime`

### 2.3 Interpretation constraint

The v00 archive does not contain the remote measures' executable DAX; it contains 90 `EXTERNALMEASURE(...)` declarations. The comparison proves name retention and the transition to local v01 DAX, but it cannot prove that each v01 expression is logically identical to the remote v00 measure. Statement of Work reconciliation criteria must therefore be verified using report outputs and representative filter contexts, not source-text equality alone.

---

## 3. Measure Changelog

### 3.1 Inventory summary

| Metric | v00 | v01 | Delta |
|---|---:|---:|---:|
| Measure declarations | 90 | 95 | +5 |
| Unique measure names | 90 | 95 | +5 |
| Names retained from v00 | 90 | 90 | 0 lost |
| Local DAX definitions | 0 | 95 | +95 |
| `EXTERNALMEASURE(...)` references | 90 | 0 | -90 |
| Removed measures | — | 0 | 0 |
| Renamed measures | — | 0 | 0 |

All 90 v00 names are present in v01. Each moves from a thin external-measure declaration to a local DAX definition. This is a materialisation/change-of-ownership change; it is not, by itself, evidence that all 90 business calculations changed.

### 3.2 Measures added in v01

All five additions are stored in `_Measures.tmdl` under the `Referral Offers` display folder.

| Added measure | Archived v01 DAX | Provisional requirements alignment | Validation status |
|---|---|---|---|
| `Open Referral` | `CALCULATE(DISTINCTCOUNT(fact_referral[referral_id]), fact_referral[referral_status] IN {"OPEN", "UNDER_OFFER"})` | R24 — referral-status overview | Technically verified; business mapping to confirm |
| `Open Referral Previous Month` | `CALCULATE([Open Referral], DATEADD(dim_date[Date], -1, MONTH))` | R24 and R52 — status and period comparison | Technically verified; business mapping to confirm |
| `Open Referrals MoM %` | `DIVIDE([Open Referral] - [Open Referral Previous Month], [Open Referral Previous Month])` | R24 and R52 — month-on-month status trend | Technically verified; business mapping to confirm |
| `Closed Referral Previous Month` | `CALCULATE([Closed Referrals (by Reason)], DATEADD(dim_date[Date], -1, MONTH))` | Extends the existing R24/R54 closure measure with period comparison | Technically verified; does not by itself close the R54 decline-reason gap |
| `Closed Referrals MoM %` | `DIVIDE([Closed Referrals (by Reason)] - [Closed Referral Previous Month], [Closed Referral Previous Month])` | R24, R52 and the existing R54 closure analysis | Technically verified; does not by itself close the R54 decline-reason gap |

The requirements links above are a traceability proposal based on the existing checklist. They are not stakeholder acceptance or proof that a functional gap is closed.

### 3.3 Effect on the Measures Comparison Checklist

The checklist header correctly identifies v01 as a **95-measure** model, while Sections 1–9 map the **90 retained legacy names** and the original summary statistics are based on those 90 rows. The five measures above are not classified in that legacy row set.

For controlled use of the checklist:

- treat the checklist's **85 implemented, 2 partial and 3 extra** row classifications as a **legacy 90-measure assessment**;
- treat its duplicate analysis separately from those row classifications: exact-DAX comparison identifies **5 duplicate groups containing 11 measures**, or **6 redundant definitions**;
- treat the five v01 additions as **unclassified pending stakeholder validation**;
- use **95** as the current archived v01 measure count;
- do not reduce the checklist's 17 declared gaps solely because these five status-trend measures exist; and
- retain the R54 gap until referral-level decline reasons are demonstrably covered, because the two closed-referral trend measures depend on the existing `Closed Referrals (by Reason)` logic.

---

## 4. Relationship Changelog

### 4.1 Inventory summary

| Metric | v00 | v01 | Delta |
|---|---:|---:|---:|
| Total relationships | 54 | 48 | -6 |
| Active relationships | 50 | 43 | -7 |
| Inactive relationships | 4 | 5 | +1 |
| Bidirectional relationships | 5 | 7 | +2 |
| `datePartOnly` relationships | 0 | 19 | +19 |

After normalising the three endpoint reversals, v01 introduces no relationship between a wholly new pair of columns. The net reduction of six comes from the six removed auto-date relationships below.

### 4.2 Relationships removed

| From column | To column | v00 state | v01 state |
|---|---|---|---|
| `dim_provider.created_timestamp` | `LocalDateTable_028b54cc-b5ca-4596-92c3-03b7a602d970.Date` | Active, many-to-one | Removed |
| `dim_provider.last_regulating_body_inspection_date` | `LocalDateTable_da8a63b0-82df-48d8-a6fc-361a373f5eb1.Date` | Active, many-to-one | Removed |
| `rpt_provider_fostering.created_timestamp` | `LocalDateTable_35189341-4f41-416e-a7f2-179b0d5d0332.Date` | Active, many-to-one | Removed |
| `rpt_provider_fostering.last_regulating_body_inspection_date` | `LocalDateTable_ea69a351-efb4-4da7-9953-b0cb7b411e7e.Date` | Active, many-to-one | Removed |
| `rpt_provider_registry.'stg_provider.last_regulating_body_inspection_date'` | `LocalDateTable_e1ed68d9-90c8-434e-b7a1-065734bdd0f4.Date` | Active, many-to-one | Removed |
| `rpt_provider_registry.created_timestamp` | `LocalDateTable_0dfd875d-78fe-44d7-be28-3cc950a23cd7.Date` | Active, many-to-one | Removed |

### 4.3 Endpoint direction reversals

These remain active, one-to-one, and bidirectional in both archives. The logical column pair is retained, but the relationship object is recreated with opposite `fromColumn` and `toColumn` endpoints.

| v00 direction | v01 direction |
|---|---|
| `fact_referral.referral_id` → `fact_referral_gender.referral_id` | `fact_referral_gender.referral_id` → `fact_referral.referral_id` |
| `fact_referral.referral_id` → `tmp_referral_person_gender.referral_id` | `tmp_referral_person_gender.referral_id` → `fact_referral.referral_id` |
| `dim_provider_home.provider_home_id` → `rpt_provider_registry.provider_home_id` | `rpt_provider_registry.provider_home_id` → `dim_provider_home.provider_home_id` |

### 4.4 Date-join behaviour changed to `datePartOnly`

The following 19 retained relationships change from the omitted/default `dateAndTime` behaviour in v00 to explicit `datePartOnly` behaviour in v01.

| # | From column | To column |
|---:|---|---|
| 1 | `dim_category.framework_start_date` | `LocalDateTable_1d1f28af-4ee0-445d-932d-406e35e3ffc7.Date` |
| 2 | `dim_date.Date` | `LocalDateTable_bbbcde47-d5df-4426-b044-338ecb6b7c37.Date` |
| 3 | `dim_framework.start_date` | `LocalDateTable_3c610ead-1ead-40e8-a8cd-e61d9fa02e4d.Date` |
| 4 | `dim_person.export_date` | `LocalDateTable_06406ba6-a64f-4dbb-8f63-615e13ea27b3.Date` |
| 5 | `dim_provider.export_date` | `LocalDateTable_890337fe-8ea3-4060-a30b-2e84e230ab08.Date` |
| 6 | `dim_provider_framework.export_date` | `LocalDateTable_efcb9c79-f5af-4d12-b2d3-95377a4b1c64.Date` |
| 7 | `dim_provider_home.export_date` | `LocalDateTable_6d4ae097-14d6-4557-bdd5-62ecae22c3c2.Date` |
| 8 | `dim_provider_home.last_regulating_body_inspection_date` | `LocalDateTable_8f2a60c8-3c88-4eff-b199-beb431e63809.Date` |
| 9 | `fact_referral.'Export Date Clean'` | `LocalDateTable_45fe65dd-0b5c-4a92-892b-18a0d47ecc18.Date` |
| 10 | `fact_referral.'Response Required Date Clean'` | `LocalDateTable_8891e268-a5d2-4afb-b123-d5e7559b73b0.Date` |
| 11 | `fact_referral_provider_message.export_date` | `LocalDateTable_7a31c86c-072f-40cb-ba1c-e823599ebaec.Date` |
| 12 | `fact_ipa.export_date` | `LocalDateTable_5fb970bc-aa2a-4b57-9991-fc2ef569d2b3.Date` |
| 13 | `fact_offer.estimated_start_date` | `LocalDateTable_a7d1d006-5922-4cf6-9273-75b1c3c15f5b.Date` |
| 14 | `fact_offer.export_date` | `LocalDateTable_62f66eb0-ba0f-4926-a158-67ca75f4cea5.Date` |
| 15 | `fact_provider_message.export_date` | `LocalDateTable_cb1f7675-6be0-4d04-b7a5-22ae1fed1cb5.Date` |
| 16 | `fact_referral_category.export_date` | `LocalDateTable_85241257-bd71-4f71-b4ab-c05eb501e49e.Date` |
| 17 | `fact_referral_person.export_date` | `LocalDateTable_9aee7af0-8a2a-46fe-8cbd-b666a98670f9.Date` |
| 18 | `rpt_provider_fostering.export_date` | `LocalDateTable_09a85944-f641-4f4a-a66d-cf7464a2c1a1.Date` |
| 19 | `rpt_provider_registry.last_regulating_body_inspection_date` | `LocalDateTable_3f4b0f03-f3b5-48c7-ae80-c033233778a8.Date` |

### 4.5 Filter-direction and activation changes

| Relationship | v00 | v01 | Test implication |
|---|---|---|---|
| `fact_offer.offer_date_only` → `dim_date.Date` | Active, single-direction | Active, bidirectional | Check date filters, offer status totals, and ambiguity with other referral/date paths |
| `fact_offer.referral_id` → `fact_referral.referral_id` | Active, single-direction | Active, bidirectional | Check referral/offer propagation and double-filtering across `fact_referral_offer` |
| `fact_referral_offer.export_date` → `dim_date.Date` | Active | Inactive | Measures that require export-date context must activate the relationship explicitly or use another date path |

### 4.6 Required relationship regression tests

1. Reconcile all 95 v01 measures in default, date-filtered, provider-filtered, and referral-filtered contexts.
2. Test month and day filters against the 19 `datePartOnly` relationships using timestamps with non-midnight values.
3. Validate offer and referral totals with each of the two newly bidirectional paths enabled in combination with existing fact relationships.
4. Confirm measures that use `USERELATIONSHIP` still activate the intended inactive date path.
5. Validate report visuals that previously used the six removed auto-date hierarchies.
6. Check one-to-one gender and provider-registry filters after the three endpoint reversals, even though their bidirectional semantics are retained.

---

## 5. Statement of Work Alignment

### 5.1 Affected clauses

| Statement of Work reference | Current draft baseline | Archive evidence | Required disposition |
|---|---|---|---|
| §1.1 background; §1.2 Objective 3; §2.1.4; Phase 2 objective and activities; D2.2; Assumption 6.1(4); P5; AC1; Phase 2 timeline | 90 current/migrated measures | v01 contains 95; all 90 v00 names are retained and 5 are added | Confirm the accepted current-state baseline and amend through change control if v01 governs delivery |
| §1.3 expected outcomes; Phase 2 exit criteria; D2.1, D2.6 and D2.7; AC3 | 117 total KPIs = 90 migrated + 27 new | 95 + 27 = 122 unless the five v01 additions overlap the 27 | Record an explicit inclusion/exclusion mapping before changing the total |
| §2.1.5; Phase 2 reconciliation; D2.2; AC1 | One-to-one reconciliation with V13.1 | v00 provides external references, not remote DAX source; v01 provides local DAX | Reconcile outputs across representative contexts for every accepted baseline measure |
| §2.1.6; D3.1; AC4 and AC5 | Preserve report behaviour with no data loss | v01 changes relationship activation, direction and date matching | Add the relationship regression tests in §4.6 to the UAT and reconciliation evidence |

### 5.2 Count-baseline options requiring client decision

| Option | Migrated baseline | Remaining/new gap measures | Target total | Consequence |
|---|---:|---:|---:|---|
| A — five v01 additions are part of the agreed 27 | 95 | 22 net additions | 117 | Requires an approved mapping showing which five of the 27 are already delivered; current category descriptions do not establish that overlap |
| B — five v01 additions are additional to the agreed 27 | 95 | 27 | 122 | Preserves v01 parity and the complete gap backlog; requires count, effort, deliverable and acceptance updates |
| C — retain the v00 contractual baseline | 90 | 27 | 117 | Excludes five measures already present in v01; requires an explicit approved exclusion and creates a parity risk |

Until the client chooses an option, the Statement of Work retains its draft commercial figures and this changelog records the technical discrepancy.

---

## 6. Acceptance and Follow-Up Actions

| # | Action | Owner | Evidence required |
|---:|---|---|---|
| 1 | Confirm whether v00 or v01 is the contractual migration baseline | Client Sponsor / Technical Lead | Written baseline decision |
| 2 | Classify the five v01 additions against the agreed 27-measure scope | Product Owner / Technical Lead | Approved measure-to-requirement mapping |
| 3 | Raise a Section 10 change record if counts, timeline, effort or acceptance criteria change | Client Sponsor / Consultant Lead | Approved Change Request / Change Order |
| 4 | Reconcile all accepted baseline measures using outputs, not source-text comparison | Data Engineer / Power BI Developer | Measure-level reconciliation results within AC1 tolerance |
| 5 | Execute the relationship regression tests in §4.6 | Power BI Developer / QA | Test evidence for date, provider, referral and offer filter contexts |
| 6 | Update the checklist classification and future-state KPI dictionary after stakeholder sign-off | Product Owner / Documentation Owner | Approved checklist and KPI dictionary revision |

---

## 7. Verification Record

| Check | Result |
|---|---|
| Source archive hashes captured | Pass |
| Measure declaration counts independently verified | Pass — 90 in v00; 95 in v01 |
| Unique measure names equal declaration counts | Pass |
| Retained/added/removed measure names reconciled | Pass — 90 retained; 5 added; 0 removed |
| External-to-local measure transition verified | Pass — 90 external references in v00; 0 in v01 |
| Relationship declaration counts verified | Pass — 54 in v00; 48 in v01 |
| Relationship removals, reversals and property changes reconciled to totals | Pass |
| Statement of Work count conflict identified without silently changing commercial scope | Pass |
| Checklist row classifications reconciled | Pass — 85 implemented + 2 partial + 3 extra = 90 legacy rows |
| Checklist duplicate analysis reconciled | Pass — 5 exact-DAX groups contain 11 measures (6 redundant definitions); non-exclusive of row classifications |
| Checklist's legacy 90-row analysis separated from the v01 95-measure source count | Pass |

---

## 8. Addendum — report v02 to report v03

### 8.1 Scope and source controls

This addendum records a direct, read-only comparison of the **last preceding Power BI solution archive**, `project X/reoprt v02.zip` (the filename is retained as committed), against `project X/report v03.zip`. It is additive to the v00-to-v01 reconciliation above; it does not alter the earlier baseline decision or commercial count controls.

| Version | Source archive | Semantic-model path inside archive | SHA-256 | Archive members |
|---|---|---|---|---:|
| v02 | `project X/reoprt v02.zip` | `SM test/SM_WMPP.SemanticModel/definition/` | `39b1c4c8b3a368b6d0a6fc0d128355d62051f343495a2b099438d1ff70b7746e` | 623 |
| v03 | `project X/report v03.zip` | `SM Test v2/SM_WMPP.SemanticModel/definition/` | `4580a23493767e94039f5a636e7bf9efb8cf6d4164c68303951b2b4ebfbf4fa1` | 707 |

The comparison was performed against ZIP members, not an extracted working tree. The semantic-model root directory was renamed from `SM test` to `SM Test v2`; the root-name change is not treated as a semantic-model change.

### 8.2 Semantic-model summary

| Metric | v02 | v03 | Delta |
|---|---:|---:|---:|
| Table TMDL files | 80 | 80 | 0 |
| Tables added / removed | 0 / 0 | 0 / 0 | 0 |
| Table TMDL files changed | — | 1 (`_Measures`) | 1 |
| Measure declarations | 98 | 139 | +41 |
| Measures removed | — | 0 | 0 |
| Relationships | 49 | 49 | 0 net |
| Relationship additions / removals / property changes | — | 1 / 1 / 1 | See §8.4 |

`model.tmdl` and `database.tmdl` are byte-equivalent between the two archives. No table is added or removed; the only changed table definition is `_Measures.tmdl`.

### 8.3 Measures added in v03

All **98** v02 measure names are retained in v03. v03 adds **41** measures, predominantly previous-month comparisons, variances, and presentational indicator/color helpers for referral, offer, and provider-contact KPIs.

| Measure family | Added measures | Count |
|---|---|---:|
| Active-referral engagement | `Active Referral Engagement Rate Indicator`; `Active Referral Engagement Rate Previous Month`; `Active Referral Engagement Rate Variance`; `Active Referral Engagement Rate Variance Indicator Color` | 4 |
| Active referrals awaiting offers | `Active Referrals Awaiting Offers Previous Month`; `Active Referrals Awaiting Offers Variance`; `Active Referrals Awaiting Offers Variance Indicator`; `Active Referrals Awaiting Offers Variance Indicator Color` | 4 |
| Active referrals under offer | `Active Referrals Under Offer Indicator`; `Active Referrals Under Offer Previous Month`; `Active Referrals Under Offer Variance`; `Active Referrals Under Offer Variance Indicator Color` | 4 |
| Closed / cancelled referrals | `Closed Referral Change Indicator`; `Closed Referral Change Indicator Color`; `Closed Referrals Variance`; `Referrals Cancelled/Closed Indicator`; `Referrals Cancelled/Closed Previous Month`; `Referrals Cancelled/Closed Variance` | 6 |
| Open referrals | `Open Referral Change Indicator`; `Open Referral Change Indicator Color`; `Open Referrals Variance` | 3 |
| Provider-contact referrals | `Provider Contact Referral Indicator`; `Provider Contact Referral Indicator Color`; `Provider Contact Referral Variance` | 3 |
| Current referrals / referrals with offers | `Referrals Currently Active Indicator`; `Referrals Currently Active Previous Month`; `Referrals Currently Active Variance`; `Referrals With Offers Indicator`; `Referrals With Offers Previous Month`; `Referrals With Offers Variance` | 6 |
| Total offers | `Total Offers Made Previous Month`; `Total Offers Made Variance`; `Total Offers Made Variance Color`; `Total Offers Made Variance Indicator` | 4 |
| Total referrals / received offers | `Total Referrals Previous Month`; `Total Referrals Variance`; `Total Referrals Variance Indicator`; `Total Referrals Variance Indicator Color`; `Total Referrals That Recieved Offers Previous Month`; `Total Referrals That Recieved Offers Variance`; `Total Referrals That Recieved Offers Variance Indicator Color` | 7 |

The v02 measure `Provider Contact Referrals MoM %` has the same DAX expression, display folder, lineage tag, and format annotation in both archives. It is recorded as a non-functional serialization/table-file difference, not a changed calculation.

### 8.4 Relationship changes

The total relationship count remains **49**, but the offer-to-referral filter path changes materially.

| Change | v02 | v03 | Consequence / test focus |
|---|---|---|---|
| Removed | `fact_offer.referral_id` → `fact_referral.referral_id`, bidirectional | Removed | Direct offer-to-referral propagation is no longer available through this relationship. |
| Added | — | `fact_offer.referral_provider_id` → `fact_referral_offer.referral_provider_id`, bidirectional, many-to-many | Validate ambiguity and propagation between offers, provider/referral offers, providers, and referrals. |
| Modified | `fact_referral_offer.referral_id` → `fact_referral.referral_id`, default single direction | Same endpoints, **bidirectional** | Referral filters can now propagate from `fact_referral_offer` back to `fact_referral`; test totals and cross-filter interactions. |

**Required v03 regression tests:**

1. Reconcile all 41 new previous-month, variance, indicator, and color measures in unfiltered and month-filtered contexts.
2. Test `fact_offer`, `fact_referral_offer`, `fact_referral`, and `dim_provider` slicers independently and in combination for double-counting or ambiguous filter paths.
3. Validate visuals that use the new indicator/color helper measures for blank, zero, positive, and negative prior-period outcomes.
4. Confirm the many-to-many offer/provider-referral relationship produces expected totals for providers with multiple offers or referrals.

### 8.5 Primary dashboard report impact

The primary dashboard report was identified as `report v14/WMPP DASHBOARD.Report/`: both archives contain the same **10 pages**, while the small `SM_WMPP.Report` is a semantic-model authoring shell.

| Primary-report metric | v02 | v03 | Delta |
|---|---:|---:|---:|
| Pages | 10 | 10 | 0 |
| Visual containers | 204 | 240 | +36 net |
| Visual IDs added | — | 47 | +47 |
| Visual IDs removed | — | 11 | -11 |
| Added visual IDs on `REFERRALS` page | — | 47 | +47 |

The 47 additions on `REFERRALS` comprise **18 shapes, 13 cards, 7 visual containers without a declared visual type, 6 action buttons, 2 KPIs, and 1 image**. The 11 removals comprise **6 untyped visual containers, 2 shapes, 2 images, and 1 KPI**. No report page is added or removed. Because visual display names and titles are not consistently declared in the PBIR members, this is a structural inventory; functional UAT must verify the intended user-facing KPI labels, navigation, and data interactions.

### 8.6 v03 verification record

| Check | Result |
|---|---|
| v02/v03 archive hashes captured | Pass |
| Semantic-model roots selected directly from ZIP members | Pass |
| `model.tmdl` and `database.tmdl` byte comparison | Pass — unchanged |
| Table inventory reconciled | Pass — 80 in each archive; no table add/remove |
| Measure inventory reconciled | Pass — 98 retained, 41 added, 0 removed |
| Relationship inventory reconciled | Pass — 49 in each archive; 1 added, 1 removed, 1 property change |
| Primary dashboard identified and page inventory reconciled | Pass — 10 pages in each archive |
| Primary-report visual inventory reconciled | Pass — 204 to 240, with 47 added and 11 removed visual IDs |
| Runtime DAX evaluation / business-output equivalence | Not performed — requires a refreshed model and controlled test data/filter contexts |

*This document is Commercial in Confidence and should not be distributed outside the authorised stakeholder group without written approval.*
