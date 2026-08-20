# Resumable Silver and archive batch processing

## Archive ZIP and file ingestion

`00_archive_load.ipynb` extracts dated ZIPs and appends each CSV/Parquet file to
`archived.<source_table>`. It stamps every business row with:

- `export_date` as a TIMESTAMP derived from the dated ZIP/folder;
- `_archive_source_path`;
- `_archive_source_zip`;
- `_archive_run_id`;
- `_archive_load_ts`.

The global controls are:

- `monitoring.cfg_archive_table_export_load` — one row per archive table/export date;
- `monitoring.cfg_archive_zip_load` — one row per ZIP/export date;
- `monitoring.cfg_archive_file_load` — one row per extracted file/export date;
- `monitoring.cfg_pipeline_run` — notebook-run outcome;
- `monitoring.cfg_table_load_metric` — table/file row counts.

At either ZIP or file level, `SUCCESS` plus `reload = false` is skipped. A
`FAILED`, interrupted `RUNNING`, unseen row, or `reload = true` row is retried.
On a file reload, rows carrying that `_archive_source_path` are deleted before
the replacement file is appended, preventing duplicates.

To force one archived file to reload:

```sql
UPDATE monitoring.cfg_archive_file_load
SET reload = true
WHERE file_path = 'Files/archive_unzipped/2026-06-15/Offer.csv'
  AND export_date = TIMESTAMP '2026-06-15 00:00:00';
```

The date-named change-log files are retained as `archived.audit`.
They are deliberately excluded from standard Silver replay because
`schema_definition.csv` does not define a generic `audit` entity.

## Rehydrate monitoring controls

`00a_rehydrate_archive_cfg.ipynb` reconstructs global table/export, ZIP,
and file controls from three sources: existing archive tables, the legacy
`archived.cfg_load_control`, and already extracted ZIP folders. Rehydration
does not reload or modify business rows and preserves an existing manual
`reload = true` flag.

The notebook rebuilds `monitoring.cfg_archive_table_export_load` directly from
the `export_date` values already held in each archive table. Therefore an
existing table with `export_date` is replay-ready even if it has no
`_archive_source_path`. Missing file-path lineage is reported separately and
only limits exact deletion/replacement of an older individual file. A rebuild
is required only for a table that genuinely has no valid `export_date` values.

## Latest Bronze to Silver

`02_silver_formatter.ipynb` records one row per Bronze table and export
timestamp in `monitoring.cfg_silver_export_load`.

| Audit state | Next run behaviour |
|---|---|
| No row | Load the table |
| `FAILED` | Retry the table |
| `RUNNING` from an interrupted run | Retry the table |
| `SUCCESS`, `reload = false` | Skip the table |
| `SUCCESS`, `reload = true` | Reload the table and reset `reload` to false |

If the nth table fails, successful earlier tables are therefore skipped on the
next run and the failed table is attempted again.

To force a latest export to reload:

```sql
UPDATE monitoring.cfg_silver_export_load
SET reload = true
WHERE source_kind = 'LATEST'
  AND source_table = 'bronze.offer'
  AND export_date = TIMESTAMP '2026-08-04 08:00:00';
```

Use the exact timestamp shown in the audit table.

## Archive to Silver

`02a_archive_silver.ipynb` reads row-level archive batches from
`archived.<source_table>` and writes them to the same
`silver.slv_<table>` targets. CamelCase/underscore differences are normalised
against the schema contract; the CSV `schema_name` value is not embedded in
the physical target name.

Archive exports are treated as complete table snapshots. The notebook scans
each table once to obtain its available dates, calculates the global minimum
and maximum, and selects the final available export date in each calendar
month. For each monthly snapshot, every table uses its own latest export on or
before that date. It filters that exact export and applies `row_number()` over
the contracted primary key before overwriting `silver.slv_<table>`. It does
not replay every daily export.

`BATCH_EXPORT_DATE` now selects a calendar month. For example, any date in
July 2026 selects July's actual final available archive export. Leave it blank
to process all canonical months chronologically.

The historical source must retain `export_date` on every row. The inspected
archive tables already contain this field, so they can be replayed directly;
`_archive_source_path` is not required by `02a_archive_silver.ipynb`.

Both Silver formatters use Spark's `CORRECTED` time-parser policy and explicitly
support date-only `yyyy-MM-dd` values plus space-separated timestamps with one,
three, or six fractional-second digits. This covers `2026-07-26`,
`2026-05-19 08:51:41.0`, and `2026-06-05 09:28:43.959135` without reverting to
the legacy parser. A monthly archive batch fails before Gold if any conformed
row has a null `export_date`.

Table-level outcomes are still written to `monitoring.cfg_silver_export_load`
with `source_kind = 'ARCHIVE_MONTH_END'`. The safe replay control is the
month-level row because shared Silver tables may currently hold a later month.
To reload a month, set its month-end row to `reload = true`:

```sql
UPDATE monitoring.cfg_month_end_gold_run
SET reload = true
WHERE snapshot_date = DATE '2026-06-30';
```

When a failed or reloaded month runs, all its Silver tables are rebuilt before
DQ and Gold. This avoids mixing an older month with Silver tables left over
from a later run.

With `VERBOSE_DIAGNOSTICS = true`, each table prints its selected source date,
raw `export_date` type, target snapshot date, row counts, duplicate count,
primary-key column names, a small identifier-only key sample, conformed date
values, null-date count, and a post-write target check. Reduce
`DIAGNOSTIC_KEY_SAMPLE_SIZE` or disable verbose diagnostics when no longer
needed.

## Month-end Gold snapshots

The final available export date in each calendar month is treated as the
month-end batch, even when it is earlier than the calendar month end. After all
Silver tables for that batch succeed, the archive notebook runs:

1. `03_silver_business_rules`
2. `04_gold_model` with `AS_OF_DATE=<last export date>`

Gold writes or updates `gold.fact_referral_snapshot` for that historical date.
The orchestration result is recorded in
`monitoring.cfg_month_end_gold_run`.

To force DQ and Gold to rerun for a completed month:

```sql
UPDATE monitoring.cfg_month_end_gold_run
SET reload = true
WHERE snapshot_date = DATE '2026-06-30';
```

Use the actual last export date recorded for that month, which may not be the
calendar month end.

For a historical month followed by later exports, leave `BATCH_EXPORT_DATE`
blank when the shared Silver layer must finish at the latest state. The
notebook processes each remaining canonical month in order and runs Gold after
each successful monthly Silver state.
