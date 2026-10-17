# BCT WMPP client documentation

## 17 October 2026 — Legend v1 compatibility and verified coverage

The inspected source baseline is `master` at `0a65e962ff3ab9681ed87d9a0a54df610774b736`. The saved business archive has **71 tables, 490 measure definitions and 35 pages**. The current Mission Control Im archive has **33 tables, 276 measure definitions and 17 pages (10 visible)**. These counts include local tables, display helpers, selectors and benchmarks; they are not approved business KPI totals. The September 58/366 and 87-measure Mission Control statements below describe earlier baselines.

Mission Control now supplies saved reporting evidence for contracts/schema/drift, domains/reference, DQ/RI/rejected keys, lineage, load metrics, pipeline/job/step timing and archive/replay. It partially supports R53, R69, R75, R82, R83, R84, R85, R87 and R88; R20 receives operational context only, not a business audit trail. A mapped measure/page is not proof of uptime, DR, alert delivery, SLA compliance, export/security policy or client acceptance. See the 80-row reassessment and exact calculation trace.

Start with [the requirement assessment](04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md), [calculation trace](04_Data_and_Reporting/KPI_CALCULATION_TRACEABILITY.md) and [workbook release runbook](05_Operations_and_Runbooks/DASHBOARD_LEGEND_RUNBOOK.md).

## Report journey review 3 October 2026

The newer project under `reports/WIP/SM WMPP v16 updated WIP` now has entity-first explorers, selection-aware KPI tables, provider scoring evidence and record-key drillthrough controls. Read the [critical report journey review and route maps](04_Data_and_Reporting/WMPP_REPORT_JOURNEY_REVIEW.md) for implemented changes, redundant visuals, remaining gaps and acceptance checks. An overall provider score is still not approved. Saved-file checks do not establish Desktop or production acceptance.

The dated assessment below refers to the older client-deliverables baseline, not this newer WIP.

## Reporting reassessment 30 September 2026

Start with [Current reporting status](04_Data_and_Reporting/WMPP_CURRENT_STATUS.md), [Requirement reassessment](04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md) and the revised `configuration/Dashboard Legend.xlsx`. The assessed project is **SM WMPP v16 updated WIP** under `reports/client-deliverables/WMPP v16`.

The WIP has 58 model tables, 366 measures and 34 page definitions (12 visible). The curated Legend now includes 144 business-measure entries. Saved-file implementation is separate from refreshed-model verification, client UAT and publication. The newest journey layout and step filtering still need Desktop acceptance.

Use the [document review register](06_Governance/DOCUMENT_REVIEW_REGISTER.md) to distinguish current guides from historical discovery, Word and slide packs. Source requirements and historical assessments are retained, not retroactively signed off.

See [current status and release checks](04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


This is the controlled client-documentation set for the Birmingham Children's
Trust WMPP Fabric implementation.

## Document map

| Folder | Contents |
|---|---|
| `01_Discovery_and_Scope/` | Discovery questionnaire and Statement of Work |
| `02_Assessment_and_Requirements/` | As-is assessment, gap analysis, and functional requirements |
| `03_Architecture_and_Design/` | HLD, TFD, proposed architecture, and supporting solution document |
| `04_Data_and_Reporting/` | KPI, semantic-model, dashboard, and enhancement documentation |
| `05_Operations_and_Runbooks/` | Notebook order, archive operations, validation, and support instructions |
| `06_Governance/` | Assumptions, constraints, dependencies, decisions, and open items |

Issue and change tracking is separate from client design documentation. See
`../change tracking/ETL_ISSUE_LOG.md` for reports and resolutions, and
`../change tracking/ETL_CHANGE_LOG.md` for delivered batches.

## Primary controlled documents

1. [High-Level Design](03_Architecture_and_Design/HLD.md)
2. [Technical/Functional Design](03_Architecture_and_Design/TFD.md)
3. [Notebook runbook](05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md)
4. [ETL Operations Control Tower](05_Operations_and_Runbooks/ETL_OPERATIONS_CONTROL_TOWER.md)
5. [HOLD register](06_Governance/HOLD_Register.md)
6. [Icon resource and provenance register](06_Governance/ICON_RESOURCE_REGISTER.md)

## Reporting implementation guides

1. [Gold semantic model DAX build guide](04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE%20WIP.md)
2. [Mission Control semantic model DAX build guide](04_Data_and_Reporting/MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md)
3. [Snapshot Month-on-Month KPI guide](04_Data_and_Reporting/SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md)
4. [Provider engagement and value scoring implementation guide](04_Data_and_Reporting/PROVIDER_SCORING_IMPLEMENTATION_GUIDE.md)
5. [RLS and partial aggregate access guide](04_Data_and_Reporting/RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md)
6. [Dashboard icon implementation guide](../reports/templates/ICON_IMPLEMENTATION_GUIDE.md)
7. [Provider registry extract deployment and export guide](04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md)

Documents retained from earlier discovery phases may describe target-state
features not yet implemented. The HLD, TFD, active notebooks, and current
configuration files take precedence for the deployed data-engineering flow.
