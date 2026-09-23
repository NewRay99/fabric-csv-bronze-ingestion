# WMPP v16 KPI and report reconciliation

## Scope and source evidence

This reconciliation was completed on 23 September 2026 against:

- `reports/current/WMPP v16.zip` and the separately supplied
  `reports/current/SM WMPP v16 updated.zip`;
- `reports/current/Dashboard Legend.xlsx`, especially the 117 rows on
  `KPI Definition`;
- `reports/current/WMPP_Dashboard_Overview_and_KPI_Logic_Final_Pack.docx`;
- the three supplied `end goal` dashboard images; and
- the maintained Gold and Mission Control guides in this directory.

The original ZIP remains source evidence. Work was applied to the extracted
repository candidate under `reports/current/SM WMPP v16 updated` and to the
styled report under `reports/current/RPT WMPP v16`.

## KPI outcome

The 117 source KPI rows were reconciled by business meaning, not by preserving
every historical measure name. This is important because the original model
contained multiple wrappers for the same DAX result.

| Outcome | KPI rows | Result |
| --- | ---: | --- |
| Implemented, covered by a visual split, or intentionally renamed to the canonical Gold measure | 101 | Available from the active Gold model. Historical aliases are rebound in report JSON instead of retained as duplicate measures. |
| Available only as an explicitly labelled proxy | 4 | KPI-107, KPI-110, KPI-113 and KPI-117. Do not present these as source-perfect equivalents. |
| Blocked by missing governed source fields or event grain | 12 | KPI-95, KPI-96, KPI-98, KPI-102, KPI-103, KPI-105, KPI-106, KPI-108, KPI-109, KPI-111, KPI-112 and KPI-115. |

The detailed 117-row disposition remains in
[Gold report implementation and requirements](GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md).

### Proxy KPIs

| KPI | Current proxy | Limitation |
| --- | --- | --- |
| KPI-107 Total Weekly Fee Liability | `Estimated Active Weekly Cost` | Estimated active cost, not signed-only actual liability. |
| KPI-110 Messages Sent | `Provider Messages Sent` | Lifecycle-event volume only; no complete message thread or unread-state evidence. |
| KPI-113 Audit Events by Type | `Referral Lifecycle Events` | Derived lifecycle roll-up, not a complete source audit log. |
| KPI-117 Bulk Onboarding Success Rate | `Provider Onboarding Success Rate` | Current provider approval-state proportion, not a bulk-operation success result. |

### Blocked KPIs

| KPI group | Required source evidence still absent |
| --- | --- |
| KPI-95–96 | Reliable referral and placement regions for out-of-region comparisons. |
| KPI-98 | Governed QA flag-type dimension/history. |
| KPI-102–103 | Expected-document set, completeness decision and blocking rule. |
| KPI-105 | Complete referral/provider decline-reason history. |
| KPI-106 | Framework-change history during an active referral. |
| KPI-108–109 | Payment method, invoice and IPA payment-lifecycle facts. |
| KPI-111–112 | Provider-authored message timestamps, response pairing, priority and unread status. |
| KPI-115 | Durable referral update-event history. |

## Semantic-model changes

- Reduced `_Measures` from 309 definitions to 258: 49 legacy aliases with a
  canonical replacement and two empty placeholder measures were removed.
- Rebound report references and remaining DAX dependencies before removal, so
  no report points to a deleted measure.
- Reduced `KPI Selector` from 91 entries to 74 canonical, unique entries.
- Added the eight-entry `Dashboard Metric Selector` field parameter for
  referral and provider analytical charts.
- Added `dim_person[person_search_label]` as `initials | person_id`. The source
  does not contain a full child/person name, so a full-name search was not
  invented.

The repeatable implementation is
`tools/enhance_wmpp_v16.py`; the acceptance check is
`tools/validate_wmpp_v16_enhancements.py`.

## Report changes

The subsequent end-goal design update adds Board Dashboard, Provider &
Placement Supply, Target & Urgency Performance, and Referral Snapshots to the
same report. The snapshot x-axis switches between the last six and twelve
available calendar months (default twelve). See the
[design implementation and outstanding items](WMPP_END_GOAL_DESIGN_IMPLEMENTATION.md)
for the 18 supporting measures, source gaps and client deployment dependency.

- Preserved the client-service connection in
  `WMPP_DASHBOARD_v16.Report/definition.pbir`.
- Added `definition-local.pbir`, which binds the styled report to the local
  reconciled `SM_WMPP_v16.SemanticModel` for repository review.
- Rebuilt **Provider Single View** with provider-name search, service and KPI
  selectors, a dynamic KPI chart, provider/home detail, referral-provider
  response detail and provider offer detail.
- Added **Referral Single View** with referral-ID search, person search using
  `initials | person_id`, a dynamic KPI chart, referral journey detail, offer
  detail and IPA detail.
- Added hidden **Referral Detail (Drillthrough)**, bound to
  `fact_referral[referral_id]`, with the same offer, provider-response and IPA
  journey evidence.
- Repaired legacy report bindings to the normalized Gold fields, including
  placement type, closure reason, provider/home fields and IPA offer linkage.
- Removed the two obsolete provider-view bookmarks after replacing the legacy
  `rpt_provider_registry` / `rpt_provider_fostering` visuals.

### Mission Control report rebuild

- Replaced the copied referral-dashboard visuals with six monitoring-only
  Mission Control pages.
- Added a locked 14-day job window, job-run Gantt and cross-filtered notebook-
  step Gantt plus job/step detail tables.
- Added a hidden `job_run_id` drillthrough page containing the job summary,
  ordered notebook steps and child pipeline execution detail.
- Corrected the step Gantt duration calculation, which previously multiplied
  the day fraction by zero.
- Added overview, data-quality/schema and archive/replay pages that surface all
  87 Mission Control measures and the supporting operational rows.
- Added `tools/rebuild_mission_control_dashboard_v16.py` and
  `tools/validate_mission_control_dashboard_v16.py` so the report can be
  rebuilt and checked deterministically without Power BI Desktop.

## Validation completed

The repository checks pass for:

- all PBIR JSON parsing;
- all report table, column and measure references resolving in the reconciled
  semantic model;
- drillthrough filter and page-binding structure;
- client binding preservation and local binding path resolution;
- 258 business-model measures, 74 canonical KPI-selector entries and eight
  dynamic metric-selector entries;
- the 38-table Gold semantic-model reconciliation and dynamic RLS structure;
  and
- the extracted Mission Control model's 87 measures and explicit Import
  partitions; and
- the rebuilt Mission Control report's six pages, 137 visuals, 87 referenced
  measures, two Gantt visuals, explicit job-to-step cross-filter interactions,
  locked 14-day filter, drillthrough binding and zero unresolved fields.

These are static repository checks. They do not execute a Fabric refresh, DAX
queries or Power BI Desktop's private load validator.

## What's outstanding

1. Deploy/refresh the current Gold notebooks and confirm the required tables,
   relationships and source values in the target Fabric environment.
2. Decide whether the available `initials | person_id` person search is
   acceptable. If full child/person name search is required, add an approved
   governed name/display field to Gold and apply the required information-
   governance and RLS controls before exposing it.
3. Supply and approve the missing source data for the 12 blocked KPIs, then
   implement those measures without falling back to Bronze, Silver or an
   unrelated proxy.
4. Review the four proxy KPIs with the business owner and either accept the
   labels/limitations or replace them when source-perfect facts exist.
5. In Power BI Desktop, open `definition-local.pbir`, refresh the model, run
   representative DAX/card checks, exercise both search pages and the referral
   drillthrough, inspect responsive layout, and execute the RLS test matrix.
6. Open the Mission Control PBIP against refreshed client monitoring data and
   exercise its 14-day job Gantt, job-to-step cross-filter, drillthrough,
   complete error text, sensitive child-result visibility and long-value
   formatting. Confirm the custom Gantt visual is approved and available in
   the tenant.
7. After the user has reviewed and checked in all repository work above, make
   the client-environment connection the final task: open the preserved
   client-bound `definition.pbir` inside the client environment, repair
   workspace credentials/binding if required, complete a full refresh, and
   confirm every page and semantic model opens without errors before publish.
