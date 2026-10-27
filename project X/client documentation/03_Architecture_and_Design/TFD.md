# Technical/Functional Design (TFD)

## 27 October 2026 — Referral creator (GLD-026)

Lineage: `bronze.referral.referral_created_by` → same-name contracted `silver.referral.referral_created_by` → `gold.fact_referral.referral_created_by`. Contract ordinal 16 is nullable `character varying(100)` and becomes a Silver string. Gold copies that string without trimming, lookup, default, or renaming to `created_by`. The base CTE selects `r.referral_created_by AS referral_created_by`; the final fact projection explicitly retains it.

The value comes from `referral_current`, selected by the existing descending `COALESCE(referral_modified_date, referral_created_date, export_date)` and export-date ordering. It is not taken from the earliest creation-date aggregation or `referral_updated_by`. NULLs and one-row-per-referral grain are preserved. Gold source preflight now rejects a missing creator column before creating facts, using the existing actionable recovery error. A present column containing NULL values is valid.

Scope is the current fact only: `fact_referral_snapshot`, retained months and snapshot migrations are unchanged. No key, relationship, KPI, scoring, or semantic-model definition changes are required by this request.

Portable validation executes the complete production fact SQL with synthetic Silver data using SQLite date/timestamp adaptations. It covers exact text/leading zeros/Unicode/100-character values, blanks, NULLs, current-row selection, export-date tie-breaking, empty inputs, missing-column preflight and snapshot exclusion. The mirrored SQL fixture must match production. The Spark simulation also asserts a known synthetic creator and NULL at every simulated month, but requires a compatible Spark/Delta runtime. Fabric Delta materialisation, SQL endpoint discovery and consuming-model refresh remain deployment checks.

## 18 October 2026 — Provider documents and missing requirement KPI visibility (SEM-004)

Both provider pages now show home-level document metadata, recorded expiry dates and a document-level `expired_docs` flag (1 expired, 0 dated/not expired, blank unknown). Removed the unrelated monthly-performance row filter. Four scoped document summaries extend the provider KPI list; 33 already implemented requirement-linked calculations are now surfaced on Requirement Matrix with explicit proxy labels.

The saved business model now has 73 tables/501 definitions/35 pages; relationships and roles remain 54/two. KPI Definition preserves all preceding 567 records and its column contract, appends GOLD-KPI-327–330 dated 18 October, and contains 571 dictionary records. Mission Control remains 34 tables/351 definitions/17 pages. These counts include helpers and historical dispositions; they do not establish accepted KPI scope.

Saved model and catalogue checks have passed. Refreshed results, report and mobile review, access checks and client acceptance remain pending. The data owner must confirm how documents are assigned to homes; the model link and schema contract currently differ. Document compliance, reminder delivery and referral blocking still require separate rules and evidence. Functional/technical changes: document-level UUID grouping, unknown-date expiry flag, provider/home interactions and exact requirement-token filtering. R47 remains partial, R48 open and R93 UAT pending.

[Implementation, exact calculations, gaps and acceptance](../04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

## 17 October 2026 - KPI Definition reconciled to latest saved WMPP_v16

KPI Definition is now reconciled to the latest saved local WMPP_v16, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. The calculation reference records these changes; production refresh and acceptance remain pending.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

Date Added means first catalogue registration. Original dates and evidenced dates of older Gold catalogue IDs remain intact; 366 newly registered current definitions are dated 17 October 2026. The 49 older Gold IDs newly surfaced in this sheet retain 26 August dates. No implementation/approval date is invented from file timestamps.

Complete DAX, calculated-table partitions and 45 verified Python/Spark producer/reference spans are maintained in the current calculation snapshot. Native reference-data synchronisation is a separate action.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](../04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

## Reporting reassessment 30 September 2026

Use the saved WMPP_v16 TMDL/PBIR definitions for the current report implementation: 58 tables, 366 measures, 34 pages and 158 bookmarks. `fact_ipa` is the active IPA table; `provider_home_id` is the offer home key. Local selectors, map points and measure containers must not be documented as new physical Gold tables.

The 19 new data bookmarks target individual journey selectors only. Preserve them separately from display-only navigation bookmarks. Referral stage is refresh-time current state; provider stage is evaluated in the current cohort; detail step selection focuses event families. These changes do not establish extra source event types, browse telemetry or separate provider acceptance.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.

**Project:** WMPP Fabric data platform **Client:** Birmingham Children's Trust **Baseline:** Active notebook set promoted from version 02 04

## 1. Scope

This document describes the implemented notebook responsibilities, data contracts, control tables, processing rules, failure behaviour, and deployment requirements for the BCT WMPP data-engineering solution.

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

`schema_name` is not part of the active ETL contract. Physical layer names are derived from notebook configuration and naming conventions.

### 3.2 `dq_rule_definition.csv`

Supplementary rules are combined with schema-generated PK completeness, uniqueness, and FK checks. Supported implemented rule types include `NOT_NULL`, `UNIQUE`, `REFERENTIAL_INTEGRITY`, `DATE_ORDER`, and `NON_NEGATIVE`.

### 3.3 Shared exclusion policy

`99_common_library.ipynb` uses source-named physical tables and excludes the explicit internal tables plus every logical name beginning `ref_`. Exclusion occurs before `export_date` or contract validation. A business table such as `referral` is not excluded.

## 4. Data-processing rules

### 4.1 Latest ingestion

1. Discover source files under the configured latest path.
2. Exclude internal/reference names.
3. Read CSV/Parquet and add ingestion timestamp, source filename, batch ID, and `export_date` when the source does not supply one.
4. Write the current Bronze table using Delta with schema overwrite enabled.

### 4.2 Silver conformance

1. Resolve a physical table to one logical schema contract.
2. Select the latest valid export timestamp.
3. Apply configured casts, date/timestamp parsing, whitespace cleanup, and null handling.
4. Deduplicate by the ordered contracted primary key.
5. Write `silver.<logical_table>` and update audits/metrics.
6. Record missing/extra columns and missing contracts as drift events.

FK parent tables are dependency-ordered before their children where the contract supplies valid relationships.

#### Worked example: `bronze.referral` to `silver.referral`

This is a **same-name, contract-driven mapping**. `02_silver_formatter` resolves the physical Bronze table name `referral` to the `referral` rows in `configuration/schema_definition.csv`, then writes `silver.referral`. It does not join to `referral_aud`, rename fields, or derive business values at this stage. The contract therefore remains the authoritative field-mapping record.

| Bronze field | Silver field | Contract treatment |
| --- | --- | --- |
| `referral_id` | `referral_id` | Primary key; UUID represented as a trimmed Spark `STRING`. |
| `placement_type`, `location_preference_details`, `location_restriction_details`, `additional_information`, `referral_created_by`, `referral_updated_by`, `referral_status` | Same field name | Trimmed `STRING`. |
| `required_start_date`, `response_required_by_date` | Same field name | Parsed to Spark `DATE` using the approved date formats. |
| `referral_created_date`, `referral_modified_date`, `export_date` | Same field name | Parsed to Spark `TIMESTAMP` using the approved timestamp formats. `export_date` identifies the selected Bronze export and is retained for lineage and point-in-time reporting. |
| `is_sibling_placement`, `is_parent_child_placement`, `has_location_preferrence`, `has_location_restriction`, `is_spot` | Same field name | Normalised to `BOOLEAN`: `true/t/1/yes/y` and `false/f/0/no/n` are recognised; other values become null. |
| `sibling_count` | `sibling_count` | Cast to Spark `INT` after stripping non-numeric characters permitted by the formatter. |

For the selected `export_date`, duplicate Bronze rows are ranked by the contracted primary key (`referral_id`) and the newest `_ingestion_timestamp`; only one row per key is written. The formatter selects only contracted business fields, so an unapproved non-technical Bronze field is not written to Silver. It is recorded as `EXTRA` schema drift; a contracted field absent from Bronze is written as a typed null and recorded as `MISSING` drift. Technical Bronze fields such as `_ingestion_timestamp`, `_source_file`, and `_ingestion_id` are not copied as business columns.

Every output row additionally receives `_record_source = 'LATEST'`, `_source_table = 'referral'`, `_silver_run_id`, and `_silver_load_ts`. The formatter replaces the current `silver.referral` table for the selected latest export and records source/written/duplicate counts in the Silver audit and table-load metrics. Business derivations occur later: for example, `03_silver_business_rules` produces `silver.referral_enrichment`, while Gold uses that relation alongside `silver.referral`.

### 4.3 Archive ingestion and replay

- The containing `YYYY-MM-DD` folder is the authoritative archive export date.
- Each file represents a complete dated table export.
- Exact source-path/date slices are replaced before append, preventing replay duplicates.
- Existing archive targets are checked/migrated to a compatible timestamp type before deletion and append.
- Monthly replay uses one canonical date per month and each table's latest available snapshot on or before that date.
- Silver is rebuilt for the month before DQ and Gold are invoked.
- If no archived `framework` snapshot exists on or before a canonical month, `02a_archive_silver` reads `Files/deprecated_wmpp_files/framework.csv`, stamps the canonical monthly snapshot date as `export_date`, and writes `silver.framework` through the normal deduplication, formatting, audit, and metric path.
- An eligible archived framework snapshot always takes precedence. The fallback also covers complete physical-table absence and does not create `archived.framework`. Its Silver output retains `_archive_fallback = true` and `_source_file`; missing, empty, or structurally incompatible fallback data fails the affected month.
- The fallback currently uses an explicit local six-column contract because `framework` is missing from `schema_definition.csv`. Replace that temporary contract with the approved CSV contract when framework metadata is signed off.

### 4.4 Data quality

- Missing Silver tables/columns and missing FK parents generate auditable `SKIPPED` results.
- Rule failures record counts and limited key references.
- Critical failures can stop the downstream run when `FAIL_ON_CRITICAL` is enabled.
- Complete child records are not written to exception tables.

## 5. Monitoring model

`00_setup_cfg.ipynb` centrally owns the configuration catalogue. Core tables include:

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

The archive notebook normally accumulates independent ZIP/file errors and raises a combined failure after later eligible items have been attempted.

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
6. Confirm child-notebook names used by `mssparkutils.notebook.run` match the imported Fabric item names.
7. Run `00_setup_cfg` and verify all configuration tables.
8. Execute the appropriate stream from the runbook.

## 9. Verification and acceptance

- Run all portable validators in `WMPP/tests`.
- In Fabric, confirm setup completion and absence of config DDL failures.
- Reconcile source/target row counts and duplicate/null-PK metrics.
- Review active schema drift and DQ failures/skips.
- For archive replay, reconcile canonical month dates and Gold snapshot rows.
- For BAU, confirm the newest Bronze export becomes the current Silver/Gold state and that completed exports are skipped on rerun.

### 3.4 Flattened referral contract

The Bronze referral CSV is a flattened reporting extract. Its operational columns are `placement_type`, `referral_created_date`, `referral_modified_date`, `referral_created_by`, `referral_updated_by`, and `referral_status`; they must not be substituted with similarly named fields from `referral_aud`. Silver retains these fields through the central contract, and Gold uses the created/modified/export timestamps in that priority order for current-row selection and activity dates.

`04_gold_model` validates its complete Silver input contract before view creation. This makes a stale Lakehouse contract or incomplete Silver rerun an explicit deployment error rather than an unresolved SQL-column exception.
