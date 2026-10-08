# Archive pipeline runbook

## Reporting reassessment 30 September 2026

The reporting layer has changed to the current WIP explorers, drillthroughs, snapshots and journey selectors. The processing instructions below remain applicable within their stated scope; this documentation reassessment did not deploy notebooks, replay archives or verify a new Fabric run. After the governed Gold build, refresh WIP, reconcile its business totals, test the new interactions and complete role-based acceptance before publication.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


## Purpose

Use this runbook to retain dated raw exports nightly, or explicitly replay
canonical monthly Silver/Gold states. Archive source tables retain their source
names in the `archived` schema; no `archived_` table prefix is added.

## Choose the run mode — updated 8 October 2026

The active source is `project X/90_run_archive_pipeline.py`, not the retained
pre-conversion `.ipynb`. Its Fabric parameter cell exposes `ARCHIVE_RUN_MODE`:

- `ARCHIVE_ONLY` (default): setup → archive load → archive schema capture →
  monitoring reports. No Silver, DQ, Gold facts, dimensions or business
  snapshots are rebuilt.
- `REPLAY`: the full six-step sequence below. Successful months can be skipped;
  selecting this mode alone does not clear state or force an entire rebuild.

Invalid modes or conflicting controls stop before any child runs. Nightly
mode requires blank `PROCESS_ONLY` and confirmation text, with both replay
reset flags false. Archive schema capture now reads `archived`, not Bronze.

## Nightly raw archive retention

1. Deploy the active sources for `90_run_archive_pipeline`, `00_archive_load`,
   `01a_cfg_schema_capture_archive`, and `02a_archive_silver`, plus the existing
   setup/library/report dependencies. Preserve Lakehouse bindings and parameter
   cell designations.
2. Deliver complete dated exports to
   `Files/wmpp-production-data-export-birmingham/archive` (date-named ZIPs), or
   `Files/archive_unzipped/YYYY-MM-DD/` (CSV/Parquet files). This runner does
   **not** copy `latest/` or `bronze.*` into the archive. If the feed only
   replaces `latest/`, arrange a dated archive copy before scheduling.
3. Create a Fabric Data Factory pipeline with a Notebook activity selecting
   `90_run_archive_pipeline`. In **Settings → Base parameters**, set the
   string `ARCHIVE_RUN_MODE` to `ARCHIVE_ONLY`. Leave replay controls at their
   defaults and the loader's `RESET_ARCHIVE_TABLES=False`.
4. Save, test once, then use **Home → Schedule → Add Schedule**. Choose daily
   frequency, a time after the completed export arrives, the intended time zone
   and start/end dates. Enable failure notifications for the responsible
   operator. Do not allow overlapping archive ingestion runs.
5. Refresh the monitoring materialized lake views after the parent job ends.
   `06_reports` defines monitoring views only; it does not refresh the business
   semantic model or turn raw exports into Gold history.

The loader skips successful files unless explicitly marked for reload. A
requested reload replaces only that file's slice before appending; ordinary
nightly runs preserve earlier exports. Audit ingestion remains disabled by
default (`LOAD_ARCHIVE_AUDIT=False`); enable it separately if required.

See [Fabric notebook activity](https://learn.microsoft.com/en-us/fabric/data-factory/notebook-activity)
and [scheduled pipeline runs](https://learn.microsoft.com/en-us/fabric/data-factory/pipeline-runs).
This repository change does not deploy notebooks or activate a schedule.

## Initial or incremental Silver/Gold archive replay

1. Deploy the active `.py` sources and child notebooks.
2. Set `ARCHIVE_RUN_MODE="REPLAY"` and run `90_run_archive_pipeline`.
   It executes, under one `JOB_RUN_ID`:
   `00_setup_cfg`, `00_archive_load`, `01a_cfg_schema_capture_archive`,
   `02a_archive_silver`, `05_gold_dimensions`, and `06_reports`.
3. The archive loader writes source-named Delta tables such as
   `archived.referral`, `archived.provider_submission_docs`, and
   `archived.audit` (when audit loading is enabled).
4. The runner lets archive Silver execute its per-month DQ and Gold-fact
   steps, then executes Gold dimensions once and defines the monitoring reports
   as its final step. It passes
   `RUN_GOLD_DIMENSIONS_AT_MONTH_END=False` to avoid duplicating that work.

Refresh the materialized lake views after the parent archive job finishes so
the completed job and `06_reports` step statuses appear in reporting. Configure
that refresh in the Fabric Lakehouse; `06_reports` defines the views.

Use the individual notebooks only for diagnosis or controlled replay. Pass
`PROCESS_ONLY="YYYY-MM"` through the runner for a single canonical month.
Run replays in a maintenance window, not alongside live processing. Replay
leaves current Silver/Gold facts at the last replayed archive state; run the
live pipeline afterwards to restore current reporting data.

## Naming transition

Active notebooks use source-named physical tables: `bronze.<table>`,
`archived.<table>`, and `silver.<table>`. Prefixed physical tables are not read
by the active pipeline. Rebuild an existing estate using the guarded Silver
reset and the appropriate live or archive runner before retiring old tables
through normal change control.

## Safe single-month recovery

Set `ARCHIVE_RUN_MODE="REPLAY"` and `PROCESS_ONLY` to the required `YYYY-MM`.
Do not enable either reset flag
unless the confirmation text is exactly `RESET YYYY-MM`. The replay uses the
last available export in that calendar month and records the result in
`monitoring.cfg_month_end_gold_run`.

## Guarded full archive rebuild

To rebuild every canonical archive month from the retained `archived.*` data,
set the following parameters in `02a_archive_silver` or pass them through
`90_run_archive_pipeline`:

```python
ARCHIVE_RUN_MODE = "REPLAY"  # Runner only; direct Archive Silver has no mode parameter.
PROCESS_ONLY = ""
RESET_MONTH_MONITORING = True
CONFIRM_PROCESS_ONLY_RESET = "RESET ALL"
```

This drops the rebuildable `silver.*` and reporting `gold.*` objects, clears
archive replay state from `cfg_month_end_gold_run`, `cfg_silver_export_load`,
`cfg_table_load_metric`, `cfg_pipeline_run` and `cfg_schema_drift_event`, then
replays every canonical archive month. It preserves `bronze.*`, `archived.*`,
the schema contract, DQ rules, file configuration, Gold lineage configuration
and the Gold placement-urgency rule. It deliberately does **not** clear archive
file/ZIP controls, avoiding duplicate archive ingestion.

## Completion checks

- `archived` tables use original source names and have populated row-level
  `export_date`.
- Nightly mode: pending files have `SUCCESS` in `cfg_archive_file_load` and
  `cfg_job_run` succeeds with four successful steps. No new Gold snapshots
  are expected. The remaining checks apply to replay mode (six runner steps).
- `monitoring.cfg_silver_export_load` has successful `ARCHIVE_MONTH_END` rows.
- `monitoring.cfg_month_end_gold_run` has a successful row for each replayed
  month.
- `gold.fact_referral_snapshot` contains the replayed snapshot dates.
- `gold.fact_referral`, `gold.fact_offer`, `gold.fact_ipa` and
  `gold.fact_referral_provider` are recreated successfully for the canonical
  archive date; their snapshot-safe historical representation is
  `gold.fact_referral_snapshot`.
- `gold.dim_provider_submission_document` and `gold.bridge_provider_sic_code`
  refresh after the Gold dimensions step when their Silver sources are present.
