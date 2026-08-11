# Archive loader issue and regression log

This file records resolved defects in `00_archive_load 02 03.ipynb`. Before
publishing future changes, run:

```text
python validate_archive_load_v02_04.py
```

Fabric runtime behaviour must also be confirmed in a development Lakehouse.

## AR-001 — Only one archive batch processed

- **Symptom:** later dated ZIP/file batches were not attempted after a failure.
- **Cause:** processing could stop at the first batch error.
- **Fix:** `STOP_ON_FIRST_ERROR = False` is the default; failures are collected
  and raised after remaining selected batches are attempted.
- **Regression guard:** validator checks both ZIP and file error paths continue.

## AR-002 — Archive loading coupled to ZIP extraction

- **Symptom:** a file copied directly into the archive folder was absent from
  the load queue when no corresponding ZIP was processed in that run.
- **Cause:** the file queue was derived from the current ZIP batch list.
- **Fix:** ZIP extraction and archive inventory are independent. Every run scans
  `ARCHIVE_FILE_ROOT` and builds a new archive inventory dataframe.
- **Regression guard:** validator rejects any file loop derived from
  `zip_batches`.

## AR-003 — One audit query executed per archive file

- **Symptom:** archive preparation was slow and generated many small Spark jobs.
- **Cause:** `monitoring.cfg_archive_file_load` was queried inside the file loop.
- **Fix:** the complete inventory is filtered with one dataframe `left_anti`
  join against the latest audit state.
- **Regression guard:** validator requires `filter_pending_archive_files()` and
  prohibits `audit_record()` in the archive file loop.

## AR-004 — Export date source was ambiguous

- **Symptom:** manually added files or date-named audit files could receive the
  wrong snapshot date.
- **Cause:** filename/ZIP parsing was mixed with folder-date parsing.
- **Fix:** the containing `YYYY-MM-DD` archive folder is authoritative for
  `export_date`. A date-named audit CSV separately receives `audit_file_date`
  from its filename.
- **Regression guard:** validator requires folder-derived export dates and both
  audit date fields.

## AR-005 — Archive file reruns could duplicate target rows

- **Symptom:** replaying a file could append a second copy of its full export.
- **Cause:** prior target rows were not always removed before append.
- **Fix:** a pending file first deletes rows by `_archive_source_path`; legacy
  targets fall back to deleting the matching `export_date`. All file rows are
  then appended without deduplication or ordering requirements.
- **Regression guard:** validator checks both replacement predicates and the
  full-file append path.

## AR-006 — Legacy archived_audit rejected for missing lineage

- **Symptom:** audit files failed with `archived.archived_audit has neither
  export_date nor source-file lineage`.
- **Cause:** the existing audit table pre-dated loader-managed metadata, while
  delete-before-append required that metadata before the incoming frame could
  add it.
- **Fix:** before replacement, the loader adds any missing nullable columns:
  `audit_file_date`, `export_date`, `_archive_source_path`,
  `_archive_source_zip`, `_archive_run_id`, and `_archive_load_ts`. Historical
  rows remain unchanged with null metadata. New audit rows receive folder and
  filename dates plus source lineage, making subsequent reruns safe.
- **Regression guard:** validator requires the legacy audit schema upgrade to
  execute before Delta replacement logic.

## AR-007 — Archive metric schema mismatch marked loaded files failed

- **Symptom:** after archive rows were written, Delta reported that
  `monitoring.cfg_table_load_metric` contained `null_primary_key_count` while
  the archive writer supplied `rejected_row_count`. The file was then recorded
  as `FAILED` even though its archive rows had already been committed.
- **Cause:** the archive notebook used a private metric schema that differed
  from the shared setup/Silver monitoring contract, and metric logging was
  inside the file-load failure boundary.
- **Fix:** archive metrics now use canonical `null_primary_key_count` and supply
  `None` because archive ingestion does not calculate that measure. Metric
  writes have dedicated error handling; failures are retained as pipeline
  warnings without changing a successfully loaded file audit to `FAILED`.
- **Regression guard:** validator prohibits `rejected_row_count`, requires the
  canonical metric schema, and requires non-fatal metric exception handling.

### CFG table inspection and migration script

For the reported AR-007 error, the live CFG table already contained the correct
`null_primary_key_count` field. Only the archive notebook writer was wrong, so
the CFG table did not require alteration.

Run this Fabric/PySpark cell when deploying to another environment. It reports
the current position and adds the canonical field only when it is genuinely
missing and no conflicting legacy field exists:

```python
METRIC_TABLE = "monitoring.cfg_table_load_metric"

metric_columns = {
    column.name.lower(): column.dataType.simpleString()
    for column in spark.table(METRIC_TABLE).schema.fields
}
print(f"Current {METRIC_TABLE} columns: {metric_columns}")

has_canonical = "null_primary_key_count" in metric_columns
has_legacy = "rejected_row_count" in metric_columns

if has_canonical and not has_legacy:
    print("CFG metric schema is already canonical; no change required.")
elif not has_canonical and not has_legacy:
    spark.sql(f"""
        ALTER TABLE {METRIC_TABLE}
        ADD COLUMNS (null_primary_key_count BIGINT)
    """)
    print("Added null_primary_key_count BIGINT.")
else:
    print(
        "Legacy rejected_row_count is present. Use the controlled rebuild "
        "below so the table does not retain both competing columns."
    )
```

If an older environment contains `rejected_row_count`, use this controlled
rebuild. It first creates a timestamped backup, then recreates the original
table with the canonical schema. Review the backup before deleting it:

```python
from datetime import datetime
from pyspark.sql import functions as F

METRIC_TABLE = "monitoring.cfg_table_load_metric"
backup_suffix = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
BACKUP_TABLE = (
    f"monitoring.cfg_table_load_metric_backup_{backup_suffix}"
)

source_df = spark.table(METRIC_TABLE)
source_columns = {name.lower() for name in source_df.columns}

if "rejected_row_count" not in source_columns:
    print("No rejected_row_count column exists; controlled rebuild skipped.")
else:
    (
        source_df.write.format("delta")
        .mode("errorifexists")
        .saveAsTable(BACKUP_TABLE)
    )

    canonical_value = (
        F.coalesce(
            F.col("null_primary_key_count").cast("long"),
            F.col("rejected_row_count").cast("long"),
        )
        if "null_primary_key_count" in source_columns
        else F.col("rejected_row_count").cast("long")
    )

    canonical_df = spark.table(BACKUP_TABLE).select(
        "run_id",
        "layer",
        "source_kind",
        "source_object",
        "target_object",
        F.col("rows_read").cast("long").alias("rows_read"),
        F.col("rows_written").cast("long").alias("rows_written"),
        F.col("duplicate_key_count").cast("long").alias(
            "duplicate_key_count"
        ),
        canonical_value.alias("null_primary_key_count"),
        F.col("recorded_at").cast("timestamp").alias("recorded_at"),
    )

    (
        canonical_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(METRIC_TABLE)
    )
    print(
        f"Rebuilt {METRIC_TABLE} with the canonical schema. "
        f"Backup retained as {BACKUP_TABLE}."
    )
```

Do not solve AR-007 by enabling automatic schema merging. That would preserve
both metric columns and reintroduce inconsistent writers.

## AR-008 — Archive audit files made general archive runs too slow

- **Symptom:** the large number of date-named audit CSV files made the archive
  notebook take too long when the immediate requirement was to load business
  archive tables.
- **Cause:** audit files entered the same monitoring join and full
  read/count/delete/write path as every other archive file.
- **Fix:** the top-level `LOAD_ARCHIVE_AUDIT` control defaults to `False`.
  Archive inventory rows targeting `archived.archived_audit` are removed at the
  inventory seam before CFG filtering or file processing. Set the control to
  `True` for a dedicated audit catch-up run.
- **Audit behaviour:** skipped audit files are not recorded as successful and
  their existing `monitoring.cfg_archive_file_load` state is not changed.
- **Regression guard:** validator checks filename classification, the default
  toggle value, and that filtering happens before the archive audit-state join.

## AR-009 — Delta could not merge legacy export_date types

- **Symptom:** archive files failed with `[DELTA_FAILED_TO_MERGE_FIELDS] Failed
  to merge fields 'export_date' and 'export_date'` after the legacy target slice
  had already been deleted.
- **Cause:** incoming rows correctly used folder-derived Spark `TIMESTAMP`, but
  some existing `archived.*` Delta tables stored the same column as `STRING`,
  `DATE`, or `TIMESTAMP_NTZ`. Delta `mergeSchema` cannot change an existing
  column's datatype.
- **Fix:** before any source-path or export-date deletion, the loader inspects
  the existing target. A noncanonical `export_date` is converted to `TIMESTAMP`
  in a staging Delta table. Conversion values, row count and staged datatype are
  validated before the original target is atomically overwritten. A failed
  migration retains its staging table for investigation and leaves file-level
  replacement unstarted.
- **Contract decision:** folder-derived `export_date` is the sole archive
  contract field. Any CSV field with the same name is overwritten and no
  `_source_export_date` field is retained.
- **Recovery:** affected CFG file rows remain `FAILED` and are selected on the
  next run. The loader migrates their targets, removes any prior source/date
  slice, and reloads the complete source files.
- **Regression guard:** validator requires migration to run before Delta delete,
  requires `TIMESTAMP` staging and invalid-value checks, and prohibits
  `_source_export_date`.

## AR-010 — Migrated target and incoming timestamp variants could still differ

- **Symptom:** `DELTA_FAILED_TO_MERGE_FIELDS` could still be raised after target
  migration, and only after the existing source/date slice had been deleted.
- **Cause:** the target migration validated the target table in isolation but
  did not re-read its exact Spark datatype and align the incoming dataframe to
  it. `TIMESTAMP` and `TIMESTAMP_NTZ`, or duplicate case-insensitive field names,
  can still fail Delta schema merging even when displayed date values match.
- **Fix:** after migration, `align_frame_export_date_to_target()` requires one
  case-insensitive `export_date`, casts it to the target field's exact Spark
  datatype, verifies equality, and returns the aligned dataframe. This safety
  gate runs before `DeltaTable.delete()`.
- **Regression guard:** validator requires alignment and type verification to
  occur before the first file-level Delta deletion.

### Bronze-to-Silver decision

`02_silver_formatter 02 03.ipynb` does not require archive-style target
migration. It casts all fields from `schema_definition.csv` and performs an
atomic full overwrite with `overwriteSchema = true`, rather than deleting a
slice and appending. It now calls `validate_silver_export_date()` before the
overwrite to require exactly one non-null `TIMESTAMP` export field. Missing
table contracts continue to be logged and skipped.

## Operational reminders

- New files under `ARCHIVE_FILE_ROOT/YYYY-MM-DD/...` are automatically pending.
- A file already recorded as `SUCCESS` is skipped unless `reload = true`.
- Overwriting a file at the same path therefore requires setting its audit row's
  reload flag.
- Keep `PROCESS_EXPORT_DATE` blank to discover every archive date, or set it to
  the exact folder date being replayed.
- Keep `LOAD_ARCHIVE_AUDIT = False` for normal business archive runs. Set it to
  `True` only when `archived.archived_audit` should be loaded or caught up.
