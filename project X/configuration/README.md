# Fabric configuration files

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
