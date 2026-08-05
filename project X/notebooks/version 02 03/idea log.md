in the .00_archive_load 02 03.ipynb i need the following changes


extract_root_posix = f"/lakehouse/default/{EXTRACT_ROOT}"
os.makedirs(extract_root_posix, exist_ok=True)

zip_batches = []
for root, _, files in os.walk(extract_root_posix):
    for file_name in files:
        if not file_name.lower().endswith(".csv"):
            continue
        full_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(full_path, "/lakehouse/default").replace("\\", "/")
        export_date = parse_export_date(file_name) or parse_export_date(relative_path)
        
        if export_date is None:
            print(f"Skipping ZIP without YYYY-MM-DD export date: {relative_path}")
            continue
        if PROCESS_EXPORT_DATE and export_date.strftime("%Y-%m-%d") != PROCESS_EXPORT_DATE:
            continue
        zip_batches.append((export_date, relative_path, full_path))



files_to_load = []
for zip_export_date, relative_zip, _ in zip_batches:
    # Never load a stale or partially extracted directory after a ZIP failure.
    
    extract_relative = f"{EXTRACT_ROOT}/{zip_export_date:%Y-%m-%d}"
    extract_posix = f"/lakehouse/default/{extract_relative}"
    if not os.path.isdir(extract_posix):
        continue
    for root, _, files in os.walk(extract_posix):
        for file_name in files:
            if not file_name.lower().endswith((".csv", ".parquet")):
                continue
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(full_path, "/lakehouse/default").replace("\\", "/")
            files_to_load.append((zip_export_date, relative_zip, relative_path, full_path, file_name))

files_to_load.sort(key=lambda item: (item[0], item[2]))

## i want to check the monitoring.cfg_archive_file_load  and reload<>0 to prevent reloading the same file twice
files_by_export_date = {}
for batch_date, _, _, _, _ in files_to_load:
    date_key = batch_date.strftime("%Y-%m-%d")
    files_by_export_date[date_key] = files_by_export_date.get(date_key, 0) + 1
print(
    f"Prepared archive files: {len(files_to_load):,}; "
    f"batches={files_by_export_date}"
)
reset_targets = set()
file_errors = []
processed = skipped = total_read = total_written = 0

for expected_export_date, relative_zip, relative_path, full_path, file_name in files_to_load:
    # Derive the row-level timestamp from the ZIP that produced this file.
    export_date = parse_export_date(os.path.basename(relative_zip))
    if export_date is None:
        raise ValueError(f"Source ZIP has no YYYY-MM-DD date: {relative_zip}")
    if export_date != expected_export_date:
        raise ValueError(
            f"ZIP/export folder date mismatch for {relative_path}: "
            f"ZIP={export_date:%Y-%m-%d}, folder={expected_export_date:%Y-%m-%d}"
        )
    physical_table = clean_table_name(file_name)
    audit_file_date = (
        parse_export_date(file_name)
        if physical_table.lower() == f"{TABLE_PREFIX}audit".lower() else None
    )
    target_object = f"{ARCHIVE_SCHEMA}.{physical_table}"
    target_exists = spark.catalog.tableExists(target_object)
    target_columns = spark.table(target_object).columns if target_exists else []
    existing_export_rows = 0
    if target_exists and "export_date" in target_columns:
        existing_export_rows = (spark.table(target_object)
            .where(F.to_date("export_date") == F.lit(export_date.date()))
            .count())
    existing = audit_record(
        "monitoring.cfg_archive_file_load",
        {"file_path": relative_path, "export_date": export_date},
    )
    if (existing and existing["status"] == "SUCCESS"
            and not existing["reload"] and not RESET_ARCHIVE_TABLES):
        skipped += 1
        print(f"Skipped loaded file: {relative_path}")
        continue

    # Existing dated rows are already replay-ready. If their older load did
    # not retain source-path lineage, infer a successful file audit and do
    # not append the same export again.
    if (existing_export_rows > 0 and "_archive_source_path" not in target_columns
            and not (existing and existing.get("reload"))
            and not RESET_ARCHIVE_TABLES):
        now = datetime.utcnow()
        attempt = int(existing["attempt_count"] or 0) + 1 if existing else 1
        first_loaded = existing.get("first_loaded_at") if existing else now
        inferred = (relative_path, file_name, export_date, relative_zip, target_object,
                    "SUCCESS", False, attempt, existing_export_rows, 0, RUN_ID,
                    now, now, "Inferred from existing archive export_date rows",
                    first_loaded, now)
        merge_audit("monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, inferred,
                    ["file_path", "export_date"])
        skipped += 1
        print(f"Skipped existing dated archive rows: {target_object} @ {export_date:%Y-%m-%d}")
        continue

    now = datetime.utcnow()
    attempt = int(existing["attempt_count"] or 0) + 1 if existing else 1
    first_loaded = existing.get("first_loaded_at") if existing else None
    running = (relative_path, file_name, export_date, relative_zip, target_object,
               "RUNNING", bool(existing["reload"]) if existing else False,
               attempt, None, None, RUN_ID, now, None, None, first_loaded, now)
    merge_audit("monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, running,
                ["file_path", "export_date"])

    try:
        if file_name.lower().endswith(".parquet"):
            frame = spark.read.format("parquet").load(relative_path)
        else:
            frame = (spark.read.format("csv")
                .option("header", "true")
                .option("inferSchema", "false")
                .option("mode", "PERMISSIVE")
                .option("badRecordsPath", f"{ERROR_LOG_ROOT}/corrupt_rows")
                .option("quote", TEXT_QUALIFIER)
                .option("escape", TEXT_QUALIFIER)
                .option("multiLine", "true")
                .load(relative_path))

        if audit_file_date is not None:
            # This is the event-file date; export_date below remains the ZIP
            # snapshot date used by archive lineage and replay controls.
            frame = frame.withColumn(
                "audit_file_date",
                F.to_date(F.lit(audit_file_date.strftime("%Y-%m-%d")), "yyyy-MM-dd"),
            )

        frame = (frame
            .withColumn(
                "export_date",
                F.to_timestamp(F.lit(export_date.strftime("%Y-%m-%d")), "yyyy-MM-dd"),
            )
            .withColumn("_archive_source_path", F.lit(relative_path))
            .withColumn("_archive_source_zip", F.lit(relative_zip))
            .withColumn("_archive_run_id", F.lit(RUN_ID))
            .withColumn("_archive_load_ts", F.current_timestamp()))
        row_count = frame.count()

        if RESET_ARCHIVE_TABLES and target_object not in reset_targets:
            spark.sql(f"DROP TABLE IF EXISTS {qident(ARCHIVE_SCHEMA)}.{qident(physical_table)}")
            reset_targets.add(target_object)

        if spark.catalog.tableExists(target_object):
            target_columns = spark.table(target_object).columns
            if "_archive_source_path" in target_columns:
                DeltaTable.forName(spark, target_object).delete(
                    F.col("_archive_source_path") == F.lit(relative_path)
                )
            elif "export_date" not in target_columns:
                raise ValueError(
                    f"{target_object} has neither export_date nor source-file lineage."
                )
            elif existing and existing.get("reload"):
                if physical_table.lower() == "archived_audit":
                    raise ValueError(
                        "A legacy archived_audit file cannot be replaced individually "
                        "without _archive_source_path."
                    )
                DeltaTable.forName(spark, target_object).delete(
                    F.to_date("export_date") == F.lit(export_date.date())
                )

        (frame.write.format("delta").mode("append")
            .option("mergeSchema", "true").saveAsTable(target_object))
        ended = datetime.utcnow()
        success = (relative_path, file_name, export_date, relative_zip, target_object,
                   "SUCCESS", False, attempt, row_count, row_count, RUN_ID, now,
                   ended, None, first_loaded or ended, ended)
        merge_audit("monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, success,
                    ["file_path", "export_date"])
        append_rows(
            "monitoring.cfg_table_load_metric",
            [(RUN_ID, "ARCHIVE", "ARCHIVE_FILE", relative_path, target_object,
              row_count, row_count, 0, None, ended)],
            "run_id string,layer string,source_kind string,source_object string,target_object string,rows_read long,rows_written long,duplicate_key_count long,rejected_row_count long,recorded_at timestamp",
        )
        processed += 1
        total_read += row_count
        total_written += row_count
        print(f"Loaded {relative_path} -> {target_object}: {row_count:,} rows")
    except Exception as exc:
        ended = datetime.utcnow()
        error = str(exc)[:4000]
        failed = (relative_path, file_name, export_date, relative_zip, target_object,
                  "FAILED", bool(existing["reload"]) if existing else False,
                  attempt, None, None, RUN_ID, now, ended, error, first_loaded, ended)
        merge_audit("monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, failed,
                    ["file_path", "export_date"])
        file_errors.append(f"{relative_path}: {error}")
        print(f"FAILED {relative_path}: {error}")
        if STOP_ON_FIRST_ERROR:
            break


## New error
FAILED Files/archive_unzipped/2026-07-05/audit/jun26/2026-06-11.csv: archived.archived_audit has neither export_date nor source-file lineage, so a safe replacement is impossible.
FAILED Files/archive_unzipped/2026-07-14/audit/jun26/2026-06-12.csv: archived.archived_audit has neither export_date nor source-file lineage, so a safe replacement is impossible.
FAILED Files/archive_unzipped/2026-07-14/audit/jun26/2026-06-28.csv: archived.archived_audit has neither export_date nor source-file lineage, so a safe replacement is impossible.
FAILED Files/archive_unzipped/2026-07-18/audit/jun26/2026-06-23.csv: archived.archived_audit has neither export_date nor source-file lineage, so a safe replacement is impossible.

## next error 

Table schema:
root
-- run_id: string (nullable = true)
-- layer: string (nullable = true)
-- source_kind: string (nullable = true)
-- source_object: string (nullable = true)
-- target_object: string (nullable = true)
-- rows_read: long (nullable = true)
-- rows_written: long (nullable = true)
-- duplicate_key_count: long (nullable = true)
-- null_primary_key_count: long (nullable = true)
-- recorded_at: timestamp (nullable = true)


Data schema:
root
-- run_id: string (nullable = true)
-- layer: string (nullable = true)
-- source_kind: string (nullable = true)
-- source_object: string (nullable = true)
-- target_object: string (nullable = true)
-- rows_read: long (nullable = true)
-- rows_written: long (nullable = true)
-- duplicate_key_count: long (nullable = true)
-- rejected_row_count: long (nullable = true)
-- recorded_at: timestamp (nullable = true)

         
Deleted prior source-path rows from archived.archived_audit
FAILED Files/archive_unzipped/2026-07-14/audit/jun26/2026-06-12.csv: [_LEGACY_ERROR_TEMP_DELTA_0007] A schema mismatch detected when writing to the Delta table (Table ID: 25740aa1-4437-4811-8c8b-f819b2933166).
To enable schema migration using DataFrameWriter or DataStreamWriter, please set:
'.option("mergeSchema", "true")'.
For other operations, set the session configuration
spark.databricks.delta.schema.autoMerge.enabled to "true". See the documentation
specific to the operation for details.

Table schema:
root
-- run_id: string (nullable = true)
-- layer: string (nullable = true)
-- source_kind: string (nullable = true)
-- source_object: string (nullable = true)
-- target_object: string (nullable = true)
-- rows_read: long (nullable = true)
-- rows_written: long (nullable = true)
-- duplicate_key_count: long (nullable = true)
-- null_primary_key_count: long (nullable = true)
-- recorded_at: timestamp (nullable = true)


Data schema:
root
-- run_id: string (nullable = true)
-- layer: string (nullable = true)
-- source_kind: string (nullable = true)
-- source_object: string (nullable = true)
-- target_object: string (nullable = true)
-- rows_read: long (nullable = true)
-- rows_written: long (nullable = true)
-- duplicate_key_count: long (nullable = true)
-- rejected_row_count: long (nullable = true)
-- recorded_at: timestamp (nullable = true)

         
Deleted prior source-path rows from archived.archived_audit
FAILED Files/archive_unzipped/2026-07-14/audit/jun26/2026-06-28.csv: [_LEGACY_ERROR_TEMP_DELTA_0007] A schema mismatch detected when writing to the Delta table (Table ID: 25740aa1-4437-4811-8c8b-f819b2933166).
To enable schema migration using DataFrameWriter or DataStreamWriter, please set:
'.option("mergeSchema", "true")'.
For other operations, set the session configuration
spark.databricks.delta.schema.autoMerge.enabled to "true". See the documentation
specific to the operation for details.
