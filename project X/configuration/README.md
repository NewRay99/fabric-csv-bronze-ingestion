# Fabric configuration files

## 17 October 2026 — KPI Definition reconciled to latest saved WIP

KPI Definition is now reconciled to the latest saved local WIP, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. These local report definitions include changes newer than default `master` (`0a65e96`); they are captured by source hashes and complete calculation snapshots, not represented as committed model changes or deployment evidence.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

Date Added means first catalogue registration. Original dates and evidenced dates of older Gold catalogue IDs remain intact; 366 newly registered current definitions are dated 17 October 2026. The 49 older Gold IDs newly surfaced in this sheet retain 26 August dates. No implementation/approval date is invented from file timestamps.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](../client%20documentation/04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

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
