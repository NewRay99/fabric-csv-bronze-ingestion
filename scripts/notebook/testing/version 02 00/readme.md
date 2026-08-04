# Fabric CSV ingestion — version 02

Version 02 fixes the Silver schema-contract problem and adds archive-to-Silver,
monitoring, data-quality, and Gold referral reporting.

## Run order

1. Upload `schema_definition.csv` and `dq_rule_definition.csv` to `Files/cfg_files/`.
2. Run `00_archive_load.ipynb` for historical ZIPs.
3. Run `01_bronze_get_latest.ipynb` for the current export.
4. Run `02_silver_formatter.ipynb` to create DDL-driven latest and archive Silver tables.
5. Run `03_silver_business_rules.ipynb` for contract, PK, FK, and custom checks.
6. Run `03_gold_model.ipynb` for referral lifecycle and board-reporting fields.

## Layer design

- `bronze`: current raw export.
- `archived`: raw historical exports with archive/file lineage.
- `silver`: current schema-conformed tables.
- `silver_archive`: historical schema-conformed tables, kept separate to prevent double counting.
- `gold`: referral lifecycle facts, snapshots, urgency targets, and provider performance.
- `monitoring`: control tables and exceptions.

## Monitoring tables

- `cfg_pipeline_run`
- `cfg_archive_file_control`
- `cfg_bronze_load_control`
- `cfg_silver_load_control`
- `cfg_table_load_metric`
- `cfg_schema_drift_event`
- `cfg_schema_contract_column`
- `cfg_data_quality_rule`
- `cfg_data_quality_result`
- `cfg_rejected_row`
- `cfg_referential_exception`

`PlacementUrgencyBand` in Gold is an operational band based on the interval between
referral creation and required placement date. `ChildCriticalityCode` is left null
until a governed source field exists; safeguarding criticality is never inferred.
