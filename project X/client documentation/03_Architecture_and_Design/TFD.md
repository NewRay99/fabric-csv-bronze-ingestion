# Technical/Functional Design (TFD)

**Project:** WMPP Fabric data platform
**Client:** Birmingham Children's Trust
**Baseline:** Active notebook set promoted from version 02 04

## 1. Scope

This document describes the implemented notebook responsibilities, data
contracts, control tables, processing rules, failure behaviour, and deployment
requirements for the BCT WMPP data-engineering solution.

## 2. Deployed notebook components

| Notebook | Inputs | Outputs / responsibility |
|---|---|---|
| `99_common_library` | Table/file names and contract rows | Shared exclusions, schema-conformance, audit, and Silver-formatting helpers |
| `00_setup_cfg` | Parameters | Creates/upgrades monitoring/config tables and stable Gold rules |
| `00_archive_load` | Archive ZIPs or dated CSV/Parquet folders | Source-named `archived.<table>` tables, ZIP/file controls, metrics |
| `00a_rehydrate_archive_cfg` | Existing archive tables, legacy controls, extracted ZIP folders | Reconstructed archive monitoring controls |
| `00b_reset_silver_cfg` | Explicit reset parameters | Guarded clearing of selected Silver execution state/tables |
| `01_bronze_get_latest` | Latest source files | Current `bronze.*` tables with lineage and export timestamp |
| `01a_cfg_schema_capture_live` | Bronze catalogue and schema contract | Definition snapshot, live schema, drift events, candidate definition |
| `01a_cfg_schema_capture_archive` | Archive catalogue and schema contract | Archive live-schema capture/comparison |
| `02_silver_formatter` | Current Bronze and schema contract | Current `silver.*`, audit rows, drift events, metrics |
| `02a_archive_silver` | Historical archive tables and contract | Canonical monthly `silver.*`, DQ/Gold orchestration |
| `03_silver_business_rules` | Silver, schema contract, DQ rule CSV | DQ results, rejected keys, referential exceptions |
| `04_gold_model` | Current/historical Silver plus `silver.referral_enrichment` | `fact_referral`, monthly referral snapshot, offer, placement, provider-response and lifecycle-event views; board/monthly/provider KPI views |
| `05_gold_dimensions` | Silver dimensions and provider bridges | Gold dimensions and bridges for reporting |

## 3. Configuration contract

### 3.1 `schema_definition.csv`

The schema contract contains one row per table/column. The active fields are:

- table and ordinal position;
- column name and source data type;
- nullability/default metadata;
- primary-key name/flag;
- foreign-key name and referenced table/column;
- optional column/table descriptions.

`schema_name` is not part of the active ETL contract. Physical layer names are
derived from notebook configuration and naming conventions.

### 3.2 `dq_rule_definition.csv`

Supplementary rules are combined with schema-generated PK completeness,
uniqueness, and FK checks. Supported implemented rule types include `NOT_NULL`,
`UNIQUE`, `REFERENTIAL_INTEGRITY`, `DATE_ORDER`, and `NON_NEGATIVE`.

### 3.3 Shared exclusion policy

`99_common_library.ipynb` uses source-named physical tables and excludes the
explicit internal tables plus every logical name beginning
`ref_`. Exclusion occurs before `export_date` or contract validation. A business
table such as `referral` is not excluded.

## 4. Data-processing rules

### 4.1 Latest ingestion

1. Discover source files under the configured latest path.
2. Exclude internal/reference names.
3. Read CSV/Parquet and add ingestion timestamp, source filename, batch ID, and
   `export_date` when the source does not supply one.
4. Write the current Bronze table using Delta with schema overwrite enabled.

### 4.2 Silver conformance

1. Resolve a physical table to one logical schema contract.
2. Select the latest valid export timestamp.
3. Apply configured casts, date/timestamp parsing, whitespace cleanup, and
   null handling.
4. Deduplicate by the ordered contracted primary key.
5. Write `silver.<logical_table>` and update audits/metrics.
6. Record missing/extra columns and missing contracts as drift events.

FK parent tables are dependency-ordered before their children where the
contract supplies valid relationships.

### 4.3 Archive ingestion and replay

- The containing `YYYY-MM-DD` folder is the authoritative archive export date.
- Each file represents a complete dated table export.
- Exact source-path/date slices are replaced before append, preventing replay
  duplicates.
- Existing archive targets are checked/migrated to a compatible timestamp type
  before deletion and append.
- Monthly replay uses one canonical date per month and each table's latest
  available snapshot on or before that date.
- Silver is rebuilt for the month before DQ and Gold are invoked.
- If no archived `framework` snapshot exists on or before a canonical month,
  `02a_archive_silver` reads
  `Files/deprecated_wmpp_files/framework.csv`, stamps the canonical monthly
  snapshot date as `export_date`, and writes `silver.framework` through the
  normal deduplication, formatting, audit, and metric path.
- An eligible archived framework snapshot always takes precedence. The fallback
  also covers complete physical-table absence and does not create
  `archived.framework`. Its
  Silver output retains `_archive_fallback = true` and `_source_file`; missing,
  empty, or structurally incompatible fallback data fails the affected month.
- The fallback currently uses an explicit local six-column contract because
  `framework` is missing from `schema_definition.csv`. Replace that temporary
  contract with the approved CSV contract when framework metadata is signed
  off.

### 4.4 Data quality

- Missing Silver tables/columns and missing FK parents generate auditable
  `SKIPPED` results.
- Rule failures record counts and limited key references.
- Critical failures can stop the downstream run when `FAIL_ON_CRITICAL` is
  enabled.
- Complete child records are not written to exception tables.

## 5. Monitoring model

`00_setup_cfg.ipynb` centrally owns the configuration catalogue. Core
tables include:

| Control area | Tables |
|---|---|
| Pipeline and metrics | `cfg_pipeline_run`, `cfg_table_load_metric` |
| Linked live jobs | `cfg_job_run`, `cfg_job_step_run` and shared `job_run_id` |
| Current/archive Silver | `cfg_silver_export_load`, `cfg_month_end_gold_run` |
| Archive ingestion | `cfg_archive_zip_load`, `cfg_archive_file_load`, `cfg_archive_table_export_load` |
| Schema governance | `cfg_schema_drift_definition`, `cfg_schema_drift_event`, `cfg_schema_contract_column`, live/candidate schema tables |
| Data quality | `cfg_data_quality_rule`, `cfg_data_quality_result`, `cfg_rejected_row`, `cfg_referential_exception` |
| Reporting views | `vw_job_run_summary`, `vw_job_step_summary`, `vw_job_schema_drift`, `vw_job_data_quality`, `vw_job_layer_lineage` |

## 6. Status and retry semantics

| State | Behaviour on next eligible run |
|---|---|
| No control row | Process |
| `RUNNING` from interruption | Retry |
| `FAILED` | Retry |
| `SUCCESS`, `reload = false` | Skip |
| `SUCCESS`, `reload = true` | Replace/reprocess and clear reload state |

The archive notebook normally accumulates independent ZIP/file errors and
raises a combined failure after later eligible items have been attempted.

## 7. Naming conventions

| Object | Convention |
|---|---|
| Current raw | `bronze.<source_table>` or physical `` input variant |
| Historical raw | `archived.<source_table>` |
| Conformed | `silver.<table>` |
| Reporting | `gold.fact_*`, Gold views and configuration |
| Controls | `monitoring.cfg_*` |

## 8. Deployment requirements

1. Create/identify the Fabric workspace and Lakehouse.
2. Import the active root `.ipynb` files as notebooks with matching item names.
3. Publish repository configuration files to `Files/cfg_files/`.
4. Configure the latest and archive Lakehouse file paths/shortcuts.
5. Attach the same default Lakehouse to every notebook.
6. Confirm child-notebook names used by `mssparkutils.notebook.run` match the
   imported Fabric item names.
7. Run `00_setup_cfg` and verify all configuration tables.
8. Execute the appropriate stream from the runbook.

## 9. Verification and acceptance

- Run all portable validators in `project X/tests`.
- In Fabric, confirm setup completion and absence of config DDL failures.
- Reconcile source/target row counts and duplicate/null-PK metrics.
- Review active schema drift and DQ failures/skips.
- For archive replay, reconcile canonical month dates and Gold snapshot rows.
- For BAU, confirm the newest Bronze export becomes the current Silver/Gold
  state and that completed exports are skipped on rerun.

### 3.4 Flattened referral contract

The Bronze referral CSV is a flattened reporting extract. Its operational
columns are `placement_type`, `referral_created_date`,
`referral_modified_date`, `referral_created_by`, `referral_updated_by`, and
`referral_status`; they must not be substituted with similarly named fields
from `referral_aud`. Silver retains these fields through the central contract,
and Gold uses the created/modified/export timestamps in that priority order for
current-row selection and activity dates.

`04_gold_model` validates its complete Silver input contract before view
creation. This makes a stale Lakehouse contract or incomplete Silver rerun an
explicit deployment error rather than an unresolved SQL-column exception.
