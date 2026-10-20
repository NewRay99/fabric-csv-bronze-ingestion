# BCT WMPP client documentation

## 19 October 2026 — WMPP_v16 linked referral status

Provider Explorer now shows Referral current status immediately after Offer statuses in the linked-provider results. The value uses referral UUIDs from the visible linked pairs and the current referral status; source reference IDs remain display labels. The current WMPP_v16 model contains 73 tables, 502 measure definitions and 35 report pages. This adds a display helper, not an additional business KPI. Refresh and visual acceptance remain pending.

## 18 October 2026 — Provider documents and missing requirement KPI visibility (SEM-004)

Both provider pages now show home-level document metadata, recorded expiry dates and a document-level `expired_docs` flag (1 expired, 0 dated/not expired, blank unknown). Removed the unrelated monthly-performance row filter. Four scoped document summaries extend the provider KPI list; 33 already implemented requirement-linked calculations are now surfaced on Requirement Matrix with explicit proxy labels.

The saved business model now has 73 tables/501 definitions/35 pages; relationships and roles remain 54/two. KPI Definition preserves all preceding 567 records and its column contract, appends GOLD-KPI-327–330 dated 18 October, and contains 571 dictionary records. Mission Control remains 34 tables/351 definitions/17 pages. These counts include helpers and historical dispositions; they do not establish accepted KPI scope.

Saved model and catalogue checks have passed. Refreshed results, report and mobile review, access checks and client acceptance remain pending. The data owner must confirm how documents are assigned to homes; the model link and schema contract currently differ. Document compliance, reminder delivery and referral blocking still require separate rules and evidence.

[Implementation, exact calculations, gaps and acceptance](04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

## 17 October 2026 - KPI Definition reconciled to latest saved WMPP_v16

KPI Definition is now reconciled to the latest saved local WMPP_v16. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. The calculation reference records these changes; production refresh and acceptance remain pending.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

## Report journey review 3 October 2026

The newer project under `WMPP_v16` now has entity-first explorers, selection-aware KPI tables, provider scoring evidence and record-key drillthrough controls. Read the [critical report journey review and route maps](04_Data_and_Reporting/WMPP_REPORT_JOURNEY_REVIEW.md) for implemented changes, redundant visuals, remaining gaps and acceptance checks. An overall provider score is still not approved. Saved-file checks do not establish Desktop or production acceptance.

The dated assessment below refers to the older client-deliverables baseline, not this WMPP_v16 version.

## Reporting reassessment 30 September 2026

Start with [Current reporting status](04_Data_and_Reporting/WMPP_CURRENT_STATUS.md), [Requirement reassessment](04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md) and the revised `configuration/Dashboard Legend.xlsx`. The assessed project under `WS_BCT_WMPP/NEW WMPP PILOT DASHBOARD (V13) Network Drive`.

The WMPP_v16 has 58 model tables, 366 measures and 34 page definitions (12 visible). The curated Legend now includes 144 business-measure entries. Saved-file implementation is separate from refreshed-model verification, client UAT and publication. The newest journey layout and step filtering still need Desktop acceptance.

Use the [document review register](06_Governance/DOCUMENT_REVIEW_REGISTER.md) to distinguish current guides from historical discovery, Word and slide packs. Source requirements and historical assessments are retained, not retroactively signed off.

See [current status and release checks](04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.

This is the controlled client-documentation set for the Birmingham Children's Trust WMPP Fabric implementation.

## Document map

| Folder | Contents |
|---|---|
| `01_Discovery_and_Scope/` | Discovery questionnaire and Statement of Work |
| `02_Assessment_and_Requirements/` | As-is assessment, gap analysis, and functional requirements |
| `03_Architecture_and_Design/` | HLD, TFD, proposed architecture, and supporting solution document |
| `04_Data_and_Reporting/` | KPI, semantic-model, dashboard, and enhancement documentation |
| `05_Operations_and_Runbooks/` | Notebook order, archive operations, validation, and support instructions |
| `06_Governance/` | Assumptions, constraints, dependencies, decisions, and open items |

Issue and change tracking is separate from client design documentation. See `../change tracking/ETL_ISSUE_LOG.md` for reports and resolutions, and `../change tracking/ETL_CHANGE_LOG.md` for delivered batches.

## Primary controlled documents

1. [High-Level Design](03_Architecture_and_Design/HLD.md)
2. [Technical/Functional Design](03_Architecture_and_Design/TFD.md)
3. [Notebook runbook](05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md)
4. [ETL Operations Control Tower](05_Operations_and_Runbooks/ETL_OPERATIONS_CONTROL_TOWER.md)
5. [HOLD register](06_Governance/HOLD_Register.md)
6. [Icon resource and provenance register](06_Governance/ICON_RESOURCE_REGISTER.md)

## Reporting implementation guides

1. [Gold semantic model DAX build guide](04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md)
2. [Mission Control semantic model DAX build guide](04_Data_and_Reporting/MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md)
3. [Snapshot Month-on-Month KPI guide](04_Data_and_Reporting/SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md)
4. [Provider engagement and value scoring implementation guide](04_Data_and_Reporting/PROVIDER_SCORING_IMPLEMENTATION_GUIDE.md)
5. [RLS and partial aggregate access guide](04_Data_and_Reporting/RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md)
6. [Dashboard icon implementation guide](../reports/templates/ICON_IMPLEMENTATION_GUIDE.md)
7. [Provider registry extract deployment and export guide](04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md)

Documents retained from earlier discovery phases may describe target-state features not yet implemented. The HLD, TFD, active notebooks, and current configuration files take precedence for the deployed data-engineering flow.
