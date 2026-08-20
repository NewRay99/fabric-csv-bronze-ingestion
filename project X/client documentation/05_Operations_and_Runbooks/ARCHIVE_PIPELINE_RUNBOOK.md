# Archive pipeline runbook

## Purpose

Use this runbook to load dated archive files, materialise one canonical Silver
state per month, and rebuild the corresponding Gold facts, dimensions and
snapshot. Archive source tables retain their source names in the `archived`
schema; the active loader does not add an `archived_` table prefix.

## Initial or incremental archive sequence

1. Deploy `90_run_archive_pipeline.ipynb` and the child notebooks.
2. Run `90_run_archive_pipeline.ipynb`. It executes, under one `JOB_RUN_ID`:
   `00_setup_cfg`, `00_archive_load`, `01a_cfg_schema_capture_archive`,
   `02a_archive_silver`, and `05_gold_dimensions`.
3. The archive loader writes source-named Delta tables such as
   `archived.referral`, `archived.provider_submission_docs`, and
   `archived.audit` (when audit loading is enabled).
4. The runner lets archive Silver execute its per-month DQ and Gold-fact
   steps, then executes Gold dimensions once as its final step. It passes
   `RUN_GOLD_DIMENSIONS_AT_MONTH_END=False` to avoid duplicating that work.

Use the individual notebooks only for diagnosis or controlled replay. Set
`PROCESS_ONLY` to `YYYY-MM` in `02a_archive_silver` for a single canonical
month.

## Naming transition

Active notebooks use source-named physical tables: `bronze.<table>`,
`archived.<table>`, and `silver.<table>`. Prefixed physical tables are not read
by the active pipeline. Rebuild an existing estate using the guarded Silver
reset and the appropriate live or archive runner before retiring old tables
through normal change control.

## Safe single-month recovery

Set `PROCESS_ONLY` to the required `YYYY-MM`. Do not enable either reset flag
unless the confirmation text is exactly `RESET YYYY-MM`. The replay uses the
last available export in that calendar month and records the result in
`monitoring.cfg_month_end_gold_run`.

## Completion checks

- `archived` tables use original source names and have populated row-level
  `export_date`.
- `monitoring.cfg_silver_export_load` has successful `ARCHIVE_MONTH_END` rows.
- `monitoring.cfg_month_end_gold_run` has a successful row for each replayed
  month.
- `gold.fact_referral_snapshot` contains the replayed snapshot dates.
- `gold.dim_provider_submission_document` and `gold.bridge_provider_sic_code`
  refresh after the Gold dimensions step when their Silver sources are present.
