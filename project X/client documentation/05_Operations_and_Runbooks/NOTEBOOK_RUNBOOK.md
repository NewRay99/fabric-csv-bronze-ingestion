# Fabric notebook runbook

**Client:** Birmingham Children's Trust  
**Solution:** WMPP Fabric Lakehouse  
**Active baseline:** version 02 04 promoted to `project X` root

## 1. Before the first run

1. Import every active `.ipynb` file from `project X` into the same Fabric
   workspace. Keep the item names aligned with the filenames (without the
   `.ipynb` extension).
2. Attach the target Lakehouse to every notebook.
3. Publish the files from `project X/configuration` to
   `Files/cfg_files/` in the Lakehouse:
   - `schema_definition.csv`
   - `dq_rule_definition.csv`
4. Confirm the latest extract shortcut/path and archive ZIP/folder paths in the
   parameter cells.
5. Run `00_setup_cfg 02 03` once and confirm that the `monitoring` configuration
   tables and `gold.cfg_placement_urgency_rule` are created.

Every ETL/control notebook also calls setup itself, so later schema additions
are applied automatically. The manual first run makes deployment errors easier
to isolate.

## 2. Stream A — historical archive hydration

Use this stream to build the historical `archived` layer and replay canonical
monthly Silver/Gold states.

### 2.1 Standard initial archive load

Run in this order:

1. `00_setup_cfg 02 03`
2. `00_archive_load 02 03`
3. `01a_cfg_schema_capture_archive 02 03`
4. Review the archive schema comparison and correct critical contract issues.
5. `02a_archive_silver 02 03`

Before step 3, verify that `COMPARED_SCHEMA` points to the deployed archive
schema. Before step 5, confirm archive business tables contain a valid row-level
`export_date`. If any canonical month lacks an eligible archived `framework`
snapshot—or the table is absent—confirm
`Files/deprecated_wmpp_files/framework.csv` exists and contains
`framework_code`, `framework_name`, `start_date`, `end_date`, and
`placement_type` before starting archive Silver replay.

With `RUN_GOLD_AT_MONTH_END = True`, step 5 processes each canonical month in
chronological order and invokes:

1. `03_silver_business_rules 02 03`
2. `04_gold_model 02 03` with that month's `AS_OF_DATE`

The orchestration result is recorded in
`monitoring.cfg_month_end_gold_run`.

### 2.2 Existing archive estate or recovered controls

If archive tables already exist but global monitoring controls are missing or
were created by an older version, run:

1. `00_setup_cfg 02 03`
2. `00a_rehydrate_archive_cfg 02 03`
3. Review tables reported as missing a valid `export_date`.
4. Continue with archive schema capture and `02a_archive_silver 02 03`.

Rehydration reconstructs controls; it does not reload business rows.

### 2.3 Archive parameters

| Parameter | Guidance |
|---|---|
| `PROCESS_EXPORT_DATE` | Blank for all archive dates; set `YYYY-MM-DD` to restrict archive ingestion |
| `RUN_ZIP_EXTRACTION` | `True` to discover/extract ZIPs; `False` to process existing dated files only |
| `LOAD_ARCHIVE_AUDIT` | Normally `False`; enable only for an audit-event catch-up |
| `RESET_ARCHIVE_TABLES` | Administrative rebuild only; do not combine with one selected date |
| `STOP_ON_FIRST_ERROR` | Normally `False` so independent files continue and failures are summarised |
| `BATCH_EXPORT_DATE` | Blank for all canonical months; any date selects that calendar month |
| `RUN_GOLD_AT_MONTH_END` | `True` for complete historical Silver/DQ/Gold replay |
| `FRAMEWORK_FALLBACK_PATH` | Controlled framework CSV used only when no archived framework snapshot exists on or before the canonical month; default `Files/deprecated_wmpp_files/framework.csv` |

### 2.4 Archive completion checks

- `cfg_archive_zip_load` and `cfg_archive_file_load` show expected success/skip
  states and no unexplained failures.
- Archive tables contain the expected dated slices and valid `export_date`.
- `cfg_silver_export_load` has successful `ARCHIVE_MONTH_END` outcomes.
- When fallback was required, `silver.slv_framework` has the canonical monthly
  `export_date`, `_archive_fallback = true`, and the expected `_source_file`.
- `cfg_data_quality_result` has no unresolved critical failures.
- `cfg_month_end_gold_run` has one successful row per canonical snapshot date.
- `gold.fact_referral_snapshot` contains the expected historical dates.

## 3. Stream B — BAU latest extracts

Run this stream for each new latest-extract delivery:

1. `00_setup_cfg 02 03`
2. `01_bronze_get_latest 02 03`
3. `01a_cfg_schema_capture_live 02 03`
4. Review `monitoring.cfg_schema_drift_event` and the schema-definition
   candidate. Approve contract changes before relying on new/changed columns.
5. `02_silver_formatter 02 03`
6. `03_silver_business_rules 02 03`
7. `04_gold_model 02 03`

`common_util` excludes explicit internal reference tables and every logical
`ref_*` table before extract-date/contract checks. Do not add synthetic
`export_date` fields to internal reference/configuration tables to make them
look like business extracts.

### 3.1 BAU completion checks

- Bronze reports the expected business-table count and newest export timestamp.
- Schema drift contains no unapproved critical table/column/FK changes.
- Latest Silver run summary has no failed tables; missing contracts are visible
  as auditable skips.
- DQ has no unresolved critical failures; expected missing sources/parents are
  visible as `SKIPPED`, not silent omissions.
- Gold views and the current referral snapshot refresh successfully.

## 4. Controlled reruns

### Latest Silver table/export

Set `reload = true` for the exact `source_kind`, source table, and export
timestamp in `monitoring.cfg_silver_export_load`, then rerun the latest Silver
formatter and downstream notebooks.

### Archive file/date

Set `reload = true` in `cfg_archive_zip_load` and/or
`cfg_archive_file_load` for the intended date/file, then rerun archive loading.

### Historical month

Set `reload = true` for the actual canonical snapshot date in
`monitoring.cfg_month_end_gold_run`, then rerun archive Silver replay.

## 5. Administrative reset

`00b_reset_silver_cfg 02 03` is not a routine pipeline step. It previews the
scope and performs destructive work only when `CONFIRM_RESET` exactly equals
`RESET SILVER`. Review all reset flags and the preview before enabling it.

## 6. Validation

Portable static checks are held in `project X/tests`. Run them with a Python
environment before deployment. Spark/Delta and cross-notebook execution must
be validated in Fabric because they require the Lakehouse and `notebookutils`.

For operational detail, also read:

- `ARCHIVE_BATCH_PROCESS.md`
- `ARCHIVE_LOAD_NOTES.md`
- `VALIDATION.md`

### SI-006 recovery — Gold referral source validation

If Gold reports missing referral fields, do not run `04_gold_model 02 03` by
itself. First deploy the updated Gold notebook and replace
`Files/cfg_files/schema_definition.csv` with the project copy. Rerun
`02a_archive_silver 02 03` for the affected month so `silver.slv_referral` is
rebuilt with `placement_type`, `referral_created_date`,
`referral_modified_date`, and `referral_status`. If 2026-04-30 already has a
successful month-control row, set its reload flag before rerunning.

If the replay reports that `silver.slv_referral_event_log` is missing, this is
not by itself a failed referral fact. Historical event-log delivery is optional
enrichment: Gold creates a typed empty event relation for that month. Deploy
the current Gold notebook and contract first, rerun the affected Silver month,
and verify that `gold.fact_referral_snapshot` is populated. If an event-log
table is present, Gold validates its required columns before creating views.

### SI-007 onwards — Contract and Silver materialisation recovery

The project contract is evidence-based. Deploy the rebuilt
`configuration/schema_definition.csv` together with the notebooks; do not
copy the retired 57-table contract. `join_class=TRIAL_JOIN` entries are
diagnostic mappings and must be reconciled in Fabric before being promoted to
contract foreign keys. `INVALID_JOIN` entries are intentionally excluded from
DQ referential rules until their parent source is delivered.

The Silver business-rules notebook rebuilds these tables on every successful
run: `slv_age_band`, `slv_directory_summary_axis`, `slv_fostering_axis`,
`slv_referral_closure_reason_summary`, and `slv_dim_date`. Verify their schemas
and row counts before refreshing the semantic model.
