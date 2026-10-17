# Fabric configuration files

## 17 October 2026 — KPI Date Added metadata

The user-approved `Date Added` column is appended as **column I** on `KPI Definition`; the original eight columns A:H retain their names, order and definitions. All 117 existing KPI rows are dated **26 August 2026**, because every one was already present in the first workbook upload, commit [`b372181`](https://github.com/NewRay99/fabric-csv-bronze-ingestion/commit/b372181ac72ce43ac274b2928ca8473f32921891). The untouched v1 workbook is the same original content.

`Date Added` means **first recorded in the version-controlled Dashboard Legend**, not the KPI's original business creation, approval, implementation, deployment or latest modification date. Values are typed Excel dates displayed as `dd mmm yyyy`. Future additions must use evidenced first-appearance dates; do not infer them from a last-modified timestamp. Existing model import fields remain unchanged; the embedded model reference tables were not modified.

## 17 October 2026 — Legend v1 compatibility and verified coverage

`configuration/Dashboard Legend.xlsx` now follows the exact three-sheet import contract in `Dashboard Legend v1.xlsx`: same first three sheet names/order, exact row-1 headers (including `Oiriginal ID`), original RID formulas/IDs/wording/dated notes and original 117 KPI IDs/order/descriptions/Section values. RID column J remains an empty spacer. The v1 file is unchanged. Gold Source Coverage is the only additional sheet; it holds source coverage, the 80-requirement assessment, the separate 144-entry catalogue, current Mission Control calculations and model inventory. The `Calculation` field retains the original specification and adds verified DAX plus notebook evidence. Long expressions have explicitly labelled excerpts linked to the full traceability document.

This restores a workbook contract, not a refreshed semantic model. The saved `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage` remain embedded M data; their values, relationships and stable model column names have not been rewritten. Owner approval and refreshed-model reconciliation remain required.

See [calculation traceability](../client%20documentation/04_Data_and_Reporting/KPI_CALCULATION_TRACEABILITY.md) and [release runbook](../client%20documentation/05_Operations_and_Runbooks/DASHBOARD_LEGEND_RUNBOOK.md).

Deploy these files to the configured Fabric Lakehouse location, normally
`Files/cfg_files/`:

- `schema_definition.csv` — approved column, type, PK, and FK contract;
- `dq_rule_definition.csv` — additional data-quality rules;
- `schema drift.xlsx` — review workbook comparing captured schemas.

The notebooks do not read these files from the Git repository at runtime. The
repository copy is the controlled source that must be published to Fabric.

## Coordinate lookup hydration

Use [the offline location-reference runbook](location-reference/README.md) and
`00c_load_location_coordinates.py` to load approved OS Code-Point Open and OS Open
Names CSV data uploaded to Lakehouse Files. This fills the lookup that setup only
creates. No geocoding/API calls, address export or runtime package download occurs.
The loader defaults to preview; it has not been run in the client Fabric workspace.

## Dashboard Legend — 30 September 2026 reassessment

`Dashboard Legend.xlsx` is the reporting requirement/KPI catalogue, not an ETL
configuration input. It now records all 80 original requirement assessments,
144 catalogued business measures (109 retained and 35 added), and the 58-table
WIP semantic model inventory. Original requirement wording, identifiers,
formulas, source notes and previous assessments are preserved.

Use the [current reporting status](../client%20documentation/04_Data_and_Reporting/WMPP_CURRENT_STATUS.md)
for scope, source limitations and release checks. “Built; UAT pending” is not
client acceptance. Proposed KPI-to-requirement associations require owner approval.
The report's embedded reference tables are historical: editing this workbook
does not automatically refresh Requirement Matrix Overview.
