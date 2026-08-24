# BCT WMPP client documentation

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

Issue and change tracking is deliberately separate at
`../change tracking/ETL_ISSUE_AND_CHANGE_LOG.md`.

## Primary controlled documents

1. [High-Level Design](03_Architecture_and_Design/HLD.md)
2. [Technical/Functional Design](03_Architecture_and_Design/TFD.md)
3. [Notebook runbook](05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md)
4. [ETL Operations Control Tower](05_Operations_and_Runbooks/ETL_OPERATIONS_CONTROL_TOWER.md)
5. [HOLD register](06_Governance/HOLD_Register.md)

Documents retained from earlier discovery phases may describe target-state
features not yet implemented. The HLD, TFD, active notebooks, and current
configuration files take precedence for the deployed data-engineering flow.
