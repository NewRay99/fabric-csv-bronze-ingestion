# Archive load behaviour

## Date-named audit CSV files

Files named `YYYY-MM-DD.csv` are audit-event files and are loaded by
`00_archive_load.ipynb` into `archived.audit`. A separate
archive notebook is not required.

The source fields are retained, including `correlation_id`, `commit_date`,
`event_subject_name`, `user_id`, `user_name`, `entity_type`, `entity_id`,
`property_name`, `change_type`, `old_value`, and `new_value`. The loader adds:

- `audit_file_date`: the date in the CSV filename;
- `export_date`: the dated archive-folder snapshot (normally derived from the
  containing ZIP when it was extracted);
- `_archive_source_path`, `_archive_source_zip`, `_archive_run_id`, and
  `_archive_load_ts`.

If `archived.audit` was created by an older loader and has none of
these managed fields, the notebook first adds them as nullable Delta columns.
Historical rows remain unchanged because their original archive snapshot date
cannot be reconstructed safely. Newly loaded rows receive complete dates and
source lineage, so they can be replaced by file path on future reruns.

`archived.audit` should remain excluded from the normal
contract-driven Silver replay. If audit-event reporting is later required,
create a dedicated audit Silver/Gold model with event semantics rather than
treating these rows as monthly entity snapshots.

`LOAD_ARCHIVE_AUDIT = False` is the default and excludes files targeting
`archived.audit` before CFG joins or file processing. This is useful
for normal business archive runs when audit ingestion is too expensive. Set it
to `True` for an audit catch-up run; the skipped files retain their existing CFG
state and have not been marked as loaded.

## Independent ZIP and archive stages

ZIP extraction and archive loading are independent. Set
`RUN_ZIP_EXTRACTION = False` to skip ZIP discovery/extraction and load only
from files already present beneath `ARCHIVE_FILE_ROOT`. By default,
`ARCHIVE_FILE_ROOT = EXTRACT_ROOT`, but it is an explicit input boundary so it
can be pointed at the folder used for manually maintained archive files.

The loader walks `ARCHIVE_FILE_ROOT` once and builds a Spark dataframe containing
every CSV and Parquet file. Files must be beneath a dated folder, for example
`Files/archive_unzipped/2026-04-30/ipa.csv`. The containing folder supplies the
authoritative `export_date`, so manually added files do not require a ZIP audit
record.

The complete inventory dataframe is filtered against
`monitoring.cfg_archive_file_load` with one dataframe anti-join on
`file_path + export_date`; the loader does not issue one audit query per file:

- `SUCCESS` and `reload = false`: excluded from the pending queue;
- unseen, `FAILED`, or interrupted `RUNNING`: included;
- `reload = true`: included for controlled replacement.

The configuration is therefore `reload = 0/false` to prevent a second load;
`reload <> 0/true` explicitly requests a reload.

No file ordering is required. Each pending file is treated as a full dated
export. Before all of its rows are appended, the loader deletes the prior
target rows for `_archive_source_path`; legacy targets without that lineage
fall back to deleting the matching `export_date`. Thus reloading
`2026-04-30/ipa.csv` replaces the existing 30 April IPA slice rather than
duplicating it.

The folder-derived `export_date` is always a Spark `TIMESTAMP` and replaces any
CSV field with the same name. No `_source_export_date` is retained. Before the
file-level deletion, an existing archive target with a legacy `STRING`, `DATE`,
or `TIMESTAMP_NTZ` export field is staged, converted, row-count checked, and
rewritten with the canonical timestamp schema. This prevents a datatype merge
failure from occurring after the target slice has been deleted.

After migration, the loader re-reads the target schema and casts the incoming
`export_date` to that exact Spark datatype. It also rejects duplicate
case-insensitive date columns and verifies source/target datatype equality
before any Delta delete. Displayed values alone are not treated as proof of
schema compatibility.

## Multiple archive batches

The loader discovers every dated ZIP. `PROCESS_EXPORT_DATE` restricts the run
only when it contains a date. With the value blank, all dates are selected.
ZIPs may be handled chronologically for extraction diagnostics, but archive
files have no processing-order dependency.

`STOP_ON_FIRST_ERROR = False` is the default. ZIP and file failures are logged,
later batches continue, and a combined error is raised at the end. The file
stage reads the extracted archive folder independently, so a ZIP does not need
to appear in the current run for its files to be considered.

The notebook prints:

- discovered ZIP count, minimum/maximum date, and count by month;
- extracted, previously completed, and failed ZIP counts;
- files prepared for each export date; and
- final loaded, skipped, and failed file counts.

A batch can legitimately show as skipped when its ZIP or files already have
`SUCCESS` and `reload = false` in the monitoring controls.

Archive rows written to `monitoring.cfg_table_load_metric` follow the shared
setup/Silver contract and use `null_primary_key_count`. Archive ingestion does
not calculate this measure, so its value is null. A metric-write failure is
reported as a pipeline warning and does not invalidate an archive file whose
target rows and file audit were successfully committed.

To inspect the position:

```sql
SELECT zip_path, export_date, status, reload, attempt_count, error_message
FROM monitoring.cfg_archive_zip_load
ORDER BY export_date, zip_path;

SELECT file_path, export_date, target_object, status, reload,
       attempt_count, error_message
FROM monitoring.cfg_archive_file_load
ORDER BY export_date, file_path;
```

To replay an entire export date, mark both its ZIP and file controls:

```sql
UPDATE monitoring.cfg_archive_zip_load
SET reload = true
WHERE CAST(export_date AS DATE) = DATE '2026-06-30';

UPDATE monitoring.cfg_archive_file_load
SET reload = true
WHERE CAST(export_date AS DATE) = DATE '2026-06-30';
```
