# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "known_lakehouses": [
# META         {
# META           "id": "d286fa39-f255-4ba7-a982-32cb69362ef7"
# META         }
# META       ],
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770"
# META     }
# META   },
# META   "spark_compute": {
# META     "compute_id": "/trident/default",
# META     "session_options": {
# META       "conf": {
# META         "spark.synapse.nbs.session.timeout": "1200000"
# META       }
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 02 — Resumable latest-to-Silver formatter
#
# Load the latest Bronze export into `silver.<table>`. Each source table and
# export timestamp is audited in `monitoring.cfg_silver_export_load`.
#
# - `SUCCESS` + `reload = false`: skip.
# - `FAILED` or missing audit row: process on the next run.
# - `reload = true`: force a successful export to run again, then reset the flag.
#
# This means a failure on the nth table can be resumed without reloading the
# tables that already completed successfully.

# PARAMETERS CELL ********************

BRONZE_SCHEMA = "bronze"
SILVER_SCHEMA = "silver"
LATEST_PREFIXES = ()
STRICT_SCHEMA = True
FAIL_ON_TABLE_ERROR = True
DATE_FORMATS = ["yyyy-MM-dd", "dd/MM/yyyy", "yyyy-MM-dd'T'HH:mm:ss"]
TIME_PARSER_POLICY = "CORRECTED"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.
FORCE_RERUN = False  # Bypass a prior successful Silver-export audit once.
TIMESTAMP_FORMATS = [
    "yyyy-MM-dd",
    "yyyy-MM-dd HH:mm:ss.SSSSSS",
    "yyyy-MM-dd HH:mm:ss.SSS",
    "yyyy-MM-dd HH:mm:ss.S",
    "yyyy-MM-dd HH:mm:ss",
    "yyyy-MM-dd'T'HH:mm:ss.SSSSSS",
    "yyyy-MM-dd'T'HH:mm:ss.SSS",
    "yyyy-MM-dd'T'HH:mm:ss.S",
    "yyyy-MM-dd'T'HH:mm:ss",
    "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
    "yyyy-MM-dd'T'HH:mm:ss.SSSSSSXXX",
    "yyyy-MM-dd'T'HH-mm-ssX",
]

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run ./99_common_library

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Shared imports, run identity, audit controls, and schema conformance
# functions are supplied by 99_common_library. Keep the preceding %run
# cell isolated: Fabric rejects a magic command combined with Python code.
JOB_RUN_ID = JOB_RUN_ID or RUN_ID
FORCE_RERUN = str(FORCE_RERUN).strip().lower() in {"true", "1", "yes", "y"}
# Pipeline status joins to the parent job; per-table metrics retain RUN_ID.
PIPELINE_RUN_ID = JOB_RUN_ID or RUN_ID
spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qident(SILVER_SCHEMA)}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

append_rows(
    "monitoring.cfg_pipeline_run",
    [(PIPELINE_RUN_ID, "02_silver_formatter", "SILVER", "LATEST", STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string",
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema_df = spark.table("monitoring.cfg_schema_contract_column")
if schema_df.rdd.isEmpty():
    raise ValueError("monitoring.cfg_schema_contract_column is empty; run setup CSV bootstrap first")
schema_rows = [row.asDict(recursive=True) for row in schema_df.collect()]

contracts = defaultdict(list)
for row in schema_rows:
    if row.get("table_name") and row.get("column_name"):
        row["ordinal_position"] = int(row.get("ordinal_position") or 999999)
        contracts[row["table_name"].lower()].append(row)
for key in contracts:
    contracts[key].sort(key=lambda item: item["ordinal_position"])

contracts_by_table = defaultdict(list)
for key in contracts:
    contracts_by_table[normalise(key)].append(key)

print(f"Loaded {len(schema_rows):,} column definitions for {len(contracts):,} tables")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

source_kind = "LATEST"
table_rows = spark.sql(f"SHOW TABLES IN {qident(BRONZE_SCHEMA)}").collect()
all_physical_tables = sorted(row.tableName for row in table_rows if not row.isTemporary)
excluded_physical_tables = excluded_etl_tables(all_physical_tables)
physical_tables = [name for name in all_physical_tables if not is_etl_excluded_table(name)]
if excluded_physical_tables:
    print(f"Excluded internal/reference Bronze tables: {excluded_physical_tables}")
metric_schema = "run_id string,layer string,source_kind string,source_object string,target_object string,rows_read long,rows_written long,duplicate_key_count long,null_primary_key_count long,recorded_at timestamp,job_run_id string"
drift_schema = "run_id string,source_kind string,source_table string,target_table string,drift_type string,column_name string,expected_type string,actual_type string,referenced_table string,referenced_column string,drift_key string,status string,occurrence_count long,first_detected_at timestamp,last_detected_at timestamp,resolved_at timestamp,detected_at timestamp,job_run_id string"

ok = failed = skipped = total_read = total_written = 0
errors = []

# Order tables so that FK parents are formatted before their children. The
# schema contract carries referenced_table for each FK; build a dependency
# graph over the contracted tables and topologically sort it. Alphabetical
# order alone can format a child (e.g. offer.additional_fee) before its parent
# (offer.offer), breaking downstream referential-integrity checks.
def order_tables_by_dependency(physical_tables):
    # Resolve each table's contract (metadata only, no data read) so we can
    # map normalised contract table name -> physical table.
    contract_name_to_physical = {}
    table_contract = {}
    for physical_table in physical_tables:
        contract_key = resolve_contract(physical_table, LATEST_PREFIXES)
        if contract_key is None:
            continue  # no contract: handled (and skipped) in the main loop
        table_contract[physical_table] = contract_key
        contract_name_to_physical.setdefault(
            normalise(contract_key), physical_table
        )

    # dependencies[physical] = set of physical tables that must load first.
    dependencies = {t: set() for t in physical_tables}
    for physical_table, contract_key in table_contract.items():
        for col in contracts[contract_key]:
            ref_table = (col.get("referenced_table") or "").strip()
            if not ref_table:
                continue
            parent = contract_name_to_physical.get(normalise(ref_table))
            if parent and parent != physical_table:
                dependencies[physical_table].add(parent)

    # Kahn's algorithm with deterministic (alphabetical) tie-breaking.
    ordered = []
    remaining = {t: set(deps) for t, deps in dependencies.items()}
    while remaining:
        ready = sorted(t for t, deps in remaining.items() if not deps)
        if not ready:  # cycle: break deterministically to avoid an infinite loop
            ready = [sorted(remaining)[0]]
        for physical_table in ready:
            ordered.append(physical_table)
            del remaining[physical_table]
            for deps in remaining.values():
                deps.discard(physical_table)
    return ordered


physical_tables = order_tables_by_dependency(physical_tables)
print("Dependency-ordered format: " + ", ".join(physical_tables))

for physical_table in physical_tables:
    source_table = f"{BRONZE_SCHEMA}.{physical_table}"
    target_table = None
    contract_key = None
    export_date = None
    try:
        # Read the export timestamp before contract resolution so a missing
        # table contract can still be recorded against a real source batch.
        frame = spark.table(source_table)
        if "export_date" not in frame.columns:
            raise ValueError(f"{source_table} has no export_date; rerun 01_bronze_get_latest first")

        export_date = (frame.select(F.max(F.to_timestamp("export_date")).alias("export_date"))
            .first()["export_date"])
        if export_date is None:
            raise ValueError(f"{source_table} has no valid export_date values")

        contract_key = resolve_contract(physical_table, LATEST_PREFIXES)
        if contract_key is None:
            message = f"No schema contract for {source_table}; table skipped"
            audit_finish(
                source_kind, BRONZE_SCHEMA, source_table, None, export_date,
                "SKIPPED_NO_CONTRACT", error_message=message,
            )
            append_rows(
                "monitoring.cfg_schema_drift_event",
                [drift_event_row(source_kind, source_table, None, "MISSING_TABLE_CONTRACT")],
                drift_schema,
            )
            skipped += 1
            print(f"SKIP {source_table} @ {export_date}: missing schema contract")
            continue

        contract_table = contract_key
        # SI-025: guarantee export_date reaches Silver even when the deployed
        # contract table is stale; also triggers a target schema refresh.
        schema_cols = ensure_export_date_contract(contracts[contract_key])
        target_table = f"{SILVER_SCHEMA}.{contract_table}"

        if (not FORCE_RERUN
                and should_skip(source_kind, BRONZE_SCHEMA, source_table, export_date)
                and not target_requires_refresh(target_table, schema_cols)):
            skipped += 1
            print(f"SKIP {source_table} @ {export_date}: already successful")
            continue
        if FORCE_RERUN:
            print(f"FORCE RERUN {source_table} @ {export_date}: bypassing prior success")

        audit_begin(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date)
        batch = frame.where(F.to_timestamp("export_date") == F.lit(export_date).cast("timestamp"))
        source_count = batch.count()
        contract_columns = {c["column_name"] for c in schema_cols}
        technical_columns = {c for c in batch.columns if c.startswith("_")}
        missing = sorted(contract_columns - set(batch.columns))
        extra = sorted(set(batch.columns) - contract_columns - technical_columns)
        drift_rows = [drift_event_row(
            source_kind, source_table, target_table, "MISSING", name,
            map_data_type(next(c["data_type"] for c in schema_cols if c["column_name"] == name)),
        ) for name in missing]
        drift_rows += [drift_event_row(
            source_kind, source_table, target_table, "EXTRA", name, actual_type=dict(batch.dtypes).get(name),
        ) for name in extra]
        append_rows("monitoring.cfg_schema_drift_event", drift_rows, drift_schema)

        deduplicated, duplicate_count = deduplicate_with_count(batch, schema_cols)
        formatted = format_frame(deduplicated, schema_cols, source_kind, source_table)
        formatted.write.format("delta").mode("overwrite").option("overwriteSchema", "true")             .saveAsTable(target_table)
        written = formatted.count()
        audit_finish(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date,
            "SUCCESS", source_count, written, duplicate_count)
        append_rows("monitoring.cfg_table_load_metric", [(RUN_ID, "SILVER", source_kind,
            source_table, target_table, source_count, written, duplicate_count, None,
            datetime.utcnow(), JOB_RUN_ID or None)], metric_schema)
        ok += 1; total_read += source_count; total_written += written
        print(f"OK {source_table} -> {target_table} @ {export_date}: {written:,} rows")
    except Exception as exc:
        message = str(exc)[:4000]
        errors.append(f"{source_table}: {message}")
        failed += 1
        if export_date is not None:
            audit_finish(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date,
                "FAILED", error_message=message)
        print(f"FAILED {source_table}: {message}")

status = "FAILED" if errors else "SUCCESS"
error_text = " | ".join(errors)[:4000] if errors else None
error_sql = "NULL" if error_text is None else "'" + error_text.replace("'", "''") + "'"
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run SET ended_at=current_timestamp(), status='{status}',
tables_succeeded={ok}, tables_failed={failed}, rows_read={total_read}, rows_written={total_written},
error_message={error_sql} WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='02_silver_formatter'""")
print(f"Latest Silver run {RUN_ID}: {status}; loaded={ok}, skipped={skipped}, failed={failed}")
if errors and FAIL_ON_TABLE_ERROR:
    raise RuntimeError(f"Silver formatting failed for {failed} table(s): {error_text}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
