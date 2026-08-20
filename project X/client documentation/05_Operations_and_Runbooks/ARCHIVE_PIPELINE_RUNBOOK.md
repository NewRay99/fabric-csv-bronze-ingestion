# Archive pipeline runbook

## Purpose

Use this runbook to load dated archive files, materialise one canonical Silver
state per month, and rebuild the corresponding Gold facts, dimensions and
snapshot. Archive source tables retain their source names in the `archived`
schema; the active loader does not add an `archived_` table prefix.

## Initial or incremental archive sequence

1. Deploy `00_archive_load.ipynb`, `02a_archive_silver.ipynb`,
   `03_silver_business_rules.ipynb`, `04_gold_model.ipynb`, and
   `05_gold_dimensions.ipynb`.
2. Run `00_setup_cfg.ipynb` to load the schema and DQ configuration
   tables.
3. Run `00_archive_load.ipynb`. It writes source-named Delta tables such as
   `archived.referral`, `archived.provider_submission_docs`, and
   `archived.audit` (when audit loading is enabled).
4. Run `01a_cfg_schema_capture_archive.ipynb`; investigate
   missing-contract or type drift before replay.
5. Run `02a_archive_silver.ipynb`. Leave `PROCESS_ONLY` blank for all
   months, or set it to `YYYY-MM` to diagnose a single canonical month.
6. With `RUN_GOLD_AT_MONTH_END=True`, the replay runs DQ, Gold facts, and Gold
   dimensions for every completed canonical month.

## Legacy-table transition

Existing `archived_<table>` tables remain readable only while a source-named
replacement does not exist. To create source-named tables across an existing
estate, rerun `00_archive_load.ipynb` once with `RESET_ARCHIVE_TABLES=True`.
Validate the new outputs before retiring legacy tables through normal
change-control. Where both versions exist, the source-named table wins.

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
