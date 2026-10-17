# Client document review register

## 17 October 2026 — KPI Definition reconciled to latest saved WIP

Reviewed/updated project/configuration/client entry points, As-Is and functional scope notes, HLD/TFD, KPI reference/calculation/lineage/current-status/requirement guides, Mission Control overview/build guide, notebook/control-tower/workbook runbooks, validation, issue/change logs and project state. Added the source-hashed release manifest and complete current calculation snapshot.

KPI Definition is now reconciled to the latest saved local WIP, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. These local report definitions include changes newer than default `master` (`0a65e96`); they are captured by source hashes and complete calculation snapshots, not represented as committed model changes or deployment evidence.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](../04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

## 17 October 2026 — New catalogue entries in KPI Definition

Appended `GOLD-KPI-110`–`GOLD-KPI-144` to **KPI Definition rows 119–153** using the existing A:I fields. The sheet now contains 152 records: the unchanged 117 legacy records plus 35 later catalogue entries. Stable Gold identifiers are retained. These are existing WIP measures newly included in this import sheet; no calculation was implemented by this workbook change. The overlapping 144-entry Gold catalogue is unchanged, and 152 is a workbook record count, not an accepted KPI scope baseline. Updated project/configuration/client entry points, As-Is/functional scope notes, TFD, KPI reference/calculation/lineage/current-status/requirement guides, release runbook, validation, change logs and project state. HLD, schema contracts and Mission Control documentation were reviewed; this reference-data change introduces no architectural, ETL or operational-measure change. Owner requirement-association/acceptance decisions remain pending.

## 17 October 2026 — KPI Date Added metadata

Appended the user-requested `Date Added` field as KPI Definition column I. All 117 original KPI rows first appear in the repository on 26 August 2026 (`b372181`); this is a first-recorded date, not business creation or approval. Original A:H column names/order, KPI values and v1 remain unchanged. Dates are native Excel dates (`dd mmm yyyy`). The definition, first-upload provenance, permitted contract extension and validation record were updated in the configuration/project entry points, TFD, KPI reference/calculation guides and release runbook. No requirement disposition changed.

## 17 October 2026 — Legend v1 compatibility and verified coverage

This work item reviewed and updated the workbook/configuration/project entry points; As-Is and functional requirements; HLD/TFD; requirement reassessment; current status; KPI reference/lineage/semantic inventory; Mission Control overview/build guide; notebook/control-tower runbooks; ETL issue/change log; semantic changelog; and project state. Added calculation traceability and the workbook release runbook. Original requirements, v1 and dated historical assessments are preserved. Current source inventory is static; deployment, query refresh, runtime correctness and client acceptance remain unverified. LEGEND-001 owner decisions: semantic alternatives, operational requirement mapping, embedded-model reference synchronisation and release acceptance.

Reviewed 30 September 2026. The current WIP status, requirement reassessment and Dashboard Legend govern reporting readiness. Existing source requirements, historical Word/slide packs and operational evidence are not retroactively rewritten or signed off.

| Document | Disposition |
| --- | --- |
| [01_Discovery_and_Scope/Client_Discovery_Questionnaire.md](../01_Discovery_and_Scope/Client_Discovery_Questionnaire.md) | Dated status update; previous content retained |
| [01_Discovery_and_Scope/Statement_of_Work.md](../01_Discovery_and_Scope/Statement_of_Work.md) | Dated status update; previous content retained |
| [02_Assessment_and_Requirements/AM_Functional_Specification.csv](../02_Assessment_and_Requirements/AM_Functional_Specification.csv) | Source/baseline data retained unchanged; current assessment in Legend |
| [02_Assessment_and_Requirements/As_Is_Assessment_Report.md](../02_Assessment_and_Requirements/As_Is_Assessment_Report.md) | Dated status update; previous content retained |
| [02_Assessment_and_Requirements/Functional_Specification.md](../02_Assessment_and_Requirements/Functional_Specification.md) | Dated status update; previous content retained |
| [02_Assessment_and_Requirements/Gap_Analysis_Report.md](../02_Assessment_and_Requirements/Gap_Analysis_Report.md) | Dated status update; previous content retained |
| [02_Assessment_and_Requirements/KPI_Enhancement_Requirements.md](../02_Assessment_and_Requirements/KPI_Enhancement_Requirements.md) | Dated status update; previous content retained |
| [03_Architecture_and_Design/Fabric_Data_Solution.docx](../03_Architecture_and_Design/Fabric_Data_Solution.docx) | Historical pack retained unchanged; not current release status |
| [03_Architecture_and_Design/Gold_DAX_Schema_Contract.md](../03_Architecture_and_Design/Gold_DAX_Schema_Contract.md) | Dated status update; previous content retained |
| [03_Architecture_and_Design/HLD.md](../03_Architecture_and_Design/HLD.md) | Dated status update; previous content retained |
| [03_Architecture_and_Design/Proposed_Solution_Architecture.md](../03_Architecture_and_Design/Proposed_Solution_Architecture.md) | Dated status update; previous content retained |
| [03_Architecture_and_Design/TFD.md](../03_Architecture_and_Design/TFD.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/CATEGORY_AND_LOCATION_ETL_IMPLEMENTATION.md](../04_Data_and_Reporting/CATEGORY_AND_LOCATION_ETL_IMPLEMENTATION.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/ENHANCEMENT_BACKLOG.md](../04_Data_and_Reporting/ENHANCEMENT_BACKLOG.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md](../04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/GOLD_MEASURE_REQUIREMENT_COVERAGE_AUDIT.md](../04_Data_and_Reporting/GOLD_MEASURE_REQUIREMENT_COVERAGE_AUDIT.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md](../04_Data_and_Reporting/GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE WIP.md](../04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE%20WIP.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/KPI_Lineage.md](../04_Data_and_Reporting/KPI_Lineage.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/KPI_Reference_Guide.md](../04_Data_and_Reporting/KPI_Reference_Guide.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/Measures_Comparison_Checklist.md](../04_Data_and_Reporting/Measures_Comparison_Checklist.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/MISSION_CONTROL_DASHBOARD_OVERVIEW_AND_KPI_LOGIC.md](../04_Data_and_Reporting/MISSION_CONTROL_DASHBOARD_OVERVIEW_AND_KPI_LOGIC.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md](../04_Data_and_Reporting/MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/PROVIDER_SCORING_IMPLEMENTATION_GUIDE.md](../04_Data_and_Reporting/PROVIDER_SCORING_IMPLEMENTATION_GUIDE.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md](../04_Data_and_Reporting/RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md](../04_Data_and_Reporting/SNAPSHOT_MONTH_ON_MONTH_KPI_GUIDE.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/WMPP_CURRENT_STATUS.md](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md) | Current inventory |
| [04_Data_and_Reporting/WMPP_Dashboard_Overview_and_KPI_Logic.md](../04_Data_and_Reporting/WMPP_Dashboard_Overview_and_KPI_Logic.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/WMPP_END_GOAL_DESIGN_IMPLEMENTATION.md](../04_Data_and_Reporting/WMPP_END_GOAL_DESIGN_IMPLEMENTATION.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/WMPP_REFERENCE_DESIGN_REVIEW.md](../04_Data_and_Reporting/WMPP_REFERENCE_DESIGN_REVIEW.md) | Dated status update; previous content retained |
| [04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md](../04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md) | Current inventory |
| [04_Data_and_Reporting/WMPP_Semantic_Model_Measures.md](../04_Data_and_Reporting/WMPP_Semantic_Model_Measures.md) | Current inventory |
| [04_Data_and_Reporting/WMPP_V16_KPI_AND_REPORT_RECONCILIATION.md](../04_Data_and_Reporting/WMPP_V16_KPI_AND_REPORT_RECONCILIATION.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/ARCHIVE_BATCH_PROCESS.md](../05_Operations_and_Runbooks/ARCHIVE_BATCH_PROCESS.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/ARCHIVE_LOAD_NOTES.md](../05_Operations_and_Runbooks/ARCHIVE_LOAD_NOTES.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/ARCHIVE_PIPELINE_RUNBOOK.md](../05_Operations_and_Runbooks/ARCHIVE_PIPELINE_RUNBOOK.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/ETL_OPERATIONS_CONTROL_TOWER.md](../05_Operations_and_Runbooks/ETL_OPERATIONS_CONTROL_TOWER.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md](../05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md) | Dated status update; previous content retained |
| [05_Operations_and_Runbooks/VALIDATION.md](../05_Operations_and_Runbooks/VALIDATION.md) | Dated status update; previous content retained |
| [06_Governance/HOLD_Register.md](HOLD_Register.md) | Dated status update; previous content retained |
| [06_Governance/ICON_RESOURCE_REGISTER.md](ICON_RESOURCE_REGISTER.md) | Dated status update; previous content retained |
| [README.md](../README.md) | Dated status update; previous content retained |
| [Supplementary/02_00_As_Is_Assessment_Report.md](../Supplementary/02_00_As_Is_Assessment_Report.md) | Dated status update; previous content retained |
| [Supplementary/02_01_As_Is_KPI.md](../Supplementary/02_01_As_Is_KPI.md) | Dated status update; previous content retained |
| [Supplementary/07_Semantic_Model_Changelog.md](../Supplementary/07_Semantic_Model_Changelog.md) | Dated status update; previous content retained |
| [Supplementary/dashboard-design-notes.md](../Supplementary/dashboard-design-notes.md) | Dated status update; previous content retained |
| [Supplementary/dax-guidance.md](../Supplementary/dax-guidance.md) | Dated status update; previous content retained |
| [Supplementary/ENHANCEMENT_BACKLOG.md](../Supplementary/ENHANCEMENT_BACKLOG.md) | Dated status update; previous content retained |
| [Supplementary/ETL_FIELD_IMPLEMENTATION_STATUS.md](../Supplementary/ETL_FIELD_IMPLEMENTATION_STATUS.md) | Dated status update; previous content retained |
| [Supplementary/kpi-catalogue.md](../Supplementary/kpi-catalogue.md) | Dated status update; previous content retained |
| [Supplementary/KPI_Reference_Guide.md](../Supplementary/KPI_Reference_Guide.md) | Dated status update; previous content retained |
| [Supplementary/Measures_Comparison_Checklist.md](../Supplementary/Measures_Comparison_Checklist.md) | Dated status update; previous content retained |
| [Supplementary/page-blueprints.md](../Supplementary/page-blueprints.md) | Dated status update; previous content retained |
| [Supplementary/README.md](../Supplementary/README.md) | Dated status update; previous content retained |
| [Supplementary/reporting-framework.md](../Supplementary/reporting-framework.md) | Dated status update; previous content retained |
| [Supplementary/sankey-guidance.md](../Supplementary/sankey-guidance.md) | Dated status update; previous content retained |
| [Supplementary/schema drift.csv](../Supplementary/schema%20drift.csv) | Source/baseline data retained unchanged; current assessment in Legend |
| [Supplementary/WMPP_Dashboard_Overview_and_KPI_Logic.md](../Supplementary/WMPP_Dashboard_Overview_and_KPI_Logic.md) | Dated status update; previous content retained |
| [Supplementary/WMPP_Data_Platform_Progress_Pastel_Pink_v2.pptx](../Supplementary/WMPP_Data_Platform_Progress_Pastel_Pink_v2.pptx) | Historical pack retained unchanged; not current release status |
| [Supplementary/WMPP_Data_Platform_Progress_Report_Pastel_Pink_v2.docx](../Supplementary/WMPP_Data_Platform_Progress_Report_Pastel_Pink_v2.docx) | Historical pack retained unchanged; not current release status |
| [Supplementary/WMPP_Semantic_Model_Measures.md](../Supplementary/WMPP_Semantic_Model_Measures.md) | Dated status update; previous content retained |

## Review boundary

The review updated current guidance and placed explicit supersession notices on older Markdown material. The two Word documents and August progress slides remain historical evidence; do not distribute them as the current status pack. `AM_Functional_Specification.csv` and `schema drift.csv` remain original reference data, not current implementation registers.

The current-status document records outstanding Desktop, refresh, security and business acceptance. No client production deployment is implied.
