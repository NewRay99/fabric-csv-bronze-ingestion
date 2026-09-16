# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770",
# META       "known_lakehouses": [
# META         {
# META           "id": "d286fa39-f255-4ba7-a982-32cb69362ef7"
# META         }
# META       ]
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 02a — Canonical month-end archive replay
#
# Materialise one canonical Silver state per archive month, then run the DQ
# and Gold notebooks for that snapshot. Archive ZIP exports are treated as
# complete table snapshots, so each table uses its latest available export
# on or before the month's final available export date.
#
# This avoids loading every daily export. Primary-key duplicates inside the
# selected export are resolved with `row_number()`. Row-level `export_date`
# is retained in `silver.<table>` and checked before Gold is invoked.
#
# When no archived `framework` snapshot exists on or before a canonical month,
# the replay reads the controlled framework fallback CSV, stamps that snapshot
# date, and writes `silver.framework` with explicit fallback provenance.

# PARAMETERS CELL ********************

ARCHIVE_SCHEMA = "archived"
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"
CFG_NOTEBOOK_NAME = "00_setup_cfg"
FRAMEWORK_FALLBACK_PATH = "Files/deprecated_wmpp_files/framework.csv"
FRAMEWORK_FALLBACK_TABLE = "framework"
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
EXCLUDED_ARCHIVE_TABLES = {"audit"}  # Raw change log has no schema contract.

# Optional YYYY-MM-DD. Any date selects that calendar month's canonical
# final export. Blank processes all archive months from the minimum to the
# maximum available export date.
BATCH_EXPORT_DATE = ""  # Optional YYYY-MM-DD canonical-month selector.

# Optional hands-on trace mode. PROCESS_ONLY takes YYYY-MM and resolves to the
# canonical final archive export for that month. The reset flags require the
# exact confirmation phrase below before deleting any state.
PROCESS_ONLY = ""  # Optional YYYY-MM, for example "2026-05".
RESET_MONTH_MONITORING = False
CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY = False
CONFIRM_PROCESS_ONLY_RESET = ""  # RESET YYYY-MM for one month, or RESET ALL for every archive month.

RESET_ALL_ARCHIVE_PROCESSING = (
    RESET_MONTH_MONITORING
    and not PROCESS_ONLY
    and CONFIRM_PROCESS_ONLY_RESET == "RESET ALL"
)
if CONFIRM_PROCESS_ONLY_RESET == "RESET ALL" and not RESET_ALL_ARCHIVE_PROCESSING:
    raise ValueError(
        "RESET ALL requires PROCESS_ONLY to be blank and RESET_MONTH_MONITORING = True."
    )
if (RESET_MONTH_MONITORING or CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY) and not PROCESS_ONLY and not RESET_ALL_ARCHIVE_PROCESSING:
    raise ValueError(
        "PROCESS_ONLY must be set to YYYY-MM when clearing one month. For a full archive rebuild, "
        "leave PROCESS_ONLY blank and set RESET_MONTH_MONITORING = True with CONFIRM_PROCESS_ONLY_RESET = 'RESET ALL'."
    )

RUN_GOLD_AT_MONTH_END = True
RUN_GOLD_DIMENSIONS_AT_MONTH_END = True
DQ_NOTEBOOK_NAME = "03_silver_business_rules"
GOLD_NOTEBOOK_NAME = "04_gold_model"
GOLD_DIMENSIONS_NOTEBOOK_NAME = "05_gold_dimensions"
# Archive Silver can rebuild multiple complete snapshots and then invoke DQ
# and Gold. Keep this aligned with the archive runner's two-hour allowance.
NOTEBOOK_TIMEOUT_SECONDS = 7200
STRICT_SCHEMA = True
FAIL_ON_TABLE_ERROR = True

# Diagnostics print only identifiers, dates and counts—not child details.
VERBOSE_DIAGNOSTICS = True
DIAGNOSTIC_KEY_SAMPLE_SIZE = 5

DATE_FORMATS = ["yyyy-MM-dd", "dd/MM/yyyy", "yyyy-MM-dd'T'HH:mm:ss"]
TIME_PARSER_POLICY = "CORRECTED"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.
IS_ORCHESTRATED_RUN = bool(JOB_RUN_ID)
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

import re
from bisect import bisect_right
import uuid
from collections import defaultdict
from datetime import datetime
from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType, IntegerType, LongType, StringType, StructField, StructType, TimestampType
)
from pyspark.sql.window import Window

RUN_ID = str(uuid.uuid4())
STARTED_AT = datetime.utcnow()
JOB_RUN_ID = JOB_RUN_ID or RUN_ID
# Pipeline status joins to the parent job; per-table metrics retain RUN_ID.
PIPELINE_RUN_ID = JOB_RUN_ID or RUN_ID
spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qident(SILVER_SCHEMA)}")
if not IS_ORCHESTRATED_RUN:
    cfg_result = mssparkutils.notebook.run(
        CFG_NOTEBOOK_NAME,
        NOTEBOOK_TIMEOUT_SECONDS,
        {"AUDIT_TABLE": AUDIT_TABLE, "TIME_PARSER_POLICY": TIME_PARSER_POLICY},
    )
    print(f"Configuration setup completed: {cfg_result}")
else:
    print("SKIP configuration setup: parent runner completed 00_setup_cfg")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


append_rows(
    "monitoring.cfg_pipeline_run",
    [(PIPELINE_RUN_ID, "02a_archive_silver", "SILVER", "ARCHIVE", STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
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

# `framework` is represented by the SI-007 contract key and the archive
# replay fallback remains available only when no dated framework snapshot exists.
# The fallback retains explicit provenance and is conformed through the same
# contract path as an archived framework source.
FRAMEWORK_FALLBACK_SCHEMA = [
    {"ordinal_position": 1, "column_name": "framework_code", "data_type": "text",
     "is_primary_key": "YES", "referenced_table": "", "referenced_column": ""},
    {"ordinal_position": 2, "column_name": "framework_name", "data_type": "text",
     "is_primary_key": "NO", "referenced_table": "", "referenced_column": ""},
    {"ordinal_position": 3, "column_name": "start_date", "data_type": "date",
     "is_primary_key": "NO", "referenced_table": "", "referenced_column": ""},
    {"ordinal_position": 4, "column_name": "end_date", "data_type": "text",
     "is_primary_key": "NO", "referenced_table": "", "referenced_column": ""},
    {"ordinal_position": 5, "column_name": "placement_type", "data_type": "text",
     "is_primary_key": "NO", "referenced_table": "", "referenced_column": ""},
    {"ordinal_position": 6, "column_name": "export_date",
     "data_type": "timestamp without time zone", "is_primary_key": "NO",
     "referenced_table": "", "referenced_column": ""},
]


def read_framework_fallback(snapshot_date):
    """Read the controlled framework CSV and stamp the replay snapshot date."""
    frame = (
        spark.read.format("csv")
        .option("header", "true")
        .option("quote", '"')
        .option("escape", '"')
        .option("multiLine", "true")
        .load(FRAMEWORK_FALLBACK_PATH)
    )

    if frame.rdd.isEmpty():
        raise ValueError(
            f"Framework fallback is empty: {FRAMEWORK_FALLBACK_PATH}"
        )

    required_columns = {
        "framework_code", "framework_name", "start_date", "end_date",
        "placement_type",
    }
    missing_columns = required_columns - set(frame.columns)
    if missing_columns:
        raise ValueError(
            "Framework fallback is missing required columns: "
            f"{sorted(missing_columns)}"
        )

    return (
        frame
        .withColumn("export_date", F.lit(snapshot_date).cast("timestamp"))
        .withColumn("_source_file", F.lit(FRAMEWORK_FALLBACK_PATH))
        .withColumn("_archive_fallback", F.lit(True))
        .withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_ingestion_id", F.lit(RUN_ID))
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Resolve every archive table to its contract once. We also collect each
# table's available export dates once, avoiding a max-date Spark job for
# every table in every month.
table_rows = spark.sql(f"SHOW TABLES IN {qident(ARCHIVE_SCHEMA)}").collect()
candidate_tables = sorted(
    row.tableName for row in table_rows
    if not row.isTemporary
    and not row.tableName.lower().startswith("cfg_")
    and row.tableName.lower() not in {
        name.lower() for name in EXCLUDED_ARCHIVE_TABLES
    }
    and not is_etl_excluded_table(row.tableName)
)


def archive_logical_name(physical_table):
    """Return the normalised source-named archive table."""
    return normalise(physical_table)


physical_tables = candidate_tables


framework_archive_present = any(
    archive_logical_name(table) == normalise(FRAMEWORK_FALLBACK_TABLE)
    for table in physical_tables
)

excluded_present = sorted(
    row.tableName for row in table_rows
    if row.tableName.lower() in {
        name.lower() for name in EXCLUDED_ARCHIVE_TABLES
    }
)
if excluded_present:
    print(f"Excluded raw archive-only tables: {excluded_present}")
excluded_internal_tables = sorted(
    row.tableName for row in table_rows
    if is_etl_excluded_table(row.tableName)
)
if excluded_internal_tables:
    print(f"Excluded internal/reference archive tables: {excluded_internal_tables}")

source_tables = []
skipped_contract_tables = []
all_available_dates = set()
contract_drift_schema = "run_id string,source_kind string,source_table string,target_table string,drift_type string,column_name string,expected_type string,actual_type string,referenced_table string,referenced_column string,drift_key string,status string,occurrence_count long,first_detected_at timestamp,last_detected_at timestamp,resolved_at timestamp,detected_at timestamp,job_run_id string"


def complete_framework_schema(schema_cols, source_table, target_table):
    """Supplement a stale framework contract with its controlled schema.

    Framework is required by Gold dimensions. A populated but older runtime
    contract can otherwise omit a source column (for example framework_name)
    and still let Archive Silver overwrite the target successfully.
    """
    present = {column["column_name"].lower() for column in schema_cols}
    missing = [
        column for column in FRAMEWORK_FALLBACK_SCHEMA
        if column["column_name"].lower() not in present
    ]
    if not missing:
        return schema_cols

    append_rows(
        "monitoring.cfg_schema_drift_event",
        [drift_event_row(
            "ARCHIVE_MONTH_END", source_table, target_table,
            "MISSING_REQUIRED_CONTRACT_COLUMN",
            column_name=column["column_name"],
            expected_type=column["data_type"],
        ) for column in missing],
        contract_drift_schema,
    )
    missing_names = [column["column_name"] for column in missing]
    print(
        f"WARN {source_table}: central framework contract is missing "
        f"{missing_names}; using the controlled framework schema and "
        "marking schema drift. Reload the central contract."
    )
    return sorted(
        list(schema_cols) + missing,
        key=lambda column: int(column.get("ordinal_position") or 999999),
    )

def parsed_archive_export_timestamp(column):
    """Parse both canonical and legacy archive export-date representations."""
    return first_parsed(F.trim(column.cast("string")), TIMESTAMP_FORMATS, F.to_timestamp)


for physical_table in physical_tables:
    source_table = f"{ARCHIVE_SCHEMA}.{physical_table}"
    source_frame = spark.table(source_table)
    if "export_date" not in source_frame.columns:
        raise ValueError(f"{source_table} has no row-level export_date")

    # Collect dates before resolving the contract. This gives an otherwise
    # unmodelled archive table a real export date in the audit controls.
    table_dates = sorted(
        row["export_date"]
        for row in source_frame
            .select(F.to_date(
                parsed_archive_export_timestamp(F.col("export_date"))
            ).alias("export_date"))
            .where(F.col("export_date").isNotNull())
            .distinct().collect()
    )
    if not table_dates:
        print(f"WARN {source_table} has no valid export_date values")
        continue

    logical_table = archive_logical_name(physical_table)
    is_framework_table = (
        logical_table == normalise(FRAMEWORK_FALLBACK_TABLE)
    )
    contract_key = resolve_contract(archive_logical_name(physical_table), ())
    if contract_key is None and is_framework_table:
        contract_table = FRAMEWORK_FALLBACK_TABLE
        schema_cols = FRAMEWORK_FALLBACK_SCHEMA
        append_rows(
            "monitoring.cfg_schema_drift_event",
            [drift_event_row(
                "ARCHIVE_MONTH_END", source_table,
                f"{SILVER_SCHEMA}.{contract_table}",
                "MISSING_TABLE_CONTRACT",
            )],
            contract_drift_schema,
        )
        print(
            f"WARN {source_table} has no central contract; "
            "using the temporary framework contract"
        )
    elif contract_key is None:
        message = f"No schema contract for {source_table}; table skipped"
        latest_export = datetime.combine(table_dates[-1], datetime.min.time())
        audit_finish(
            "ARCHIVE_MONTH_END", ARCHIVE_SCHEMA, source_table, None,
            latest_export, "SKIPPED_NO_CONTRACT", error_message=message,
        )
        append_rows(
            "monitoring.cfg_schema_drift_event",
            [drift_event_row("ARCHIVE_MONTH_END", source_table, None, "MISSING_TABLE_CONTRACT")],
            contract_drift_schema,
        )
        skipped_contract_tables.append(source_table)
        print(f"SKIP {source_table} @ {table_dates[-1]}: missing schema contract")
        continue
    else:
        contract_table = contract_key
        # SI-025: guarantee export_date reaches Silver even when the deployed
        # contract table is stale; also flags the target schema as stale.
        schema_cols = ensure_export_date_contract(contracts[contract_key])

    target_table = f"{SILVER_SCHEMA}.{contract_table}"
    if is_framework_table:
        schema_cols = complete_framework_schema(
            schema_cols, source_table, target_table
        )

    all_available_dates.update(table_dates)
    source_tables.append({
        "physical_table": physical_table,
        "source_schema": ARCHIVE_SCHEMA,
        "source_table": source_table,
        "target_table": target_table,
        "schema_cols": schema_cols,
        "available_dates": table_dates,
        "fallback_path": (
            FRAMEWORK_FALLBACK_PATH if is_framework_table else None
        ),
        "is_fallback_only": False,
    })
    if VERBOSE_DIAGNOSTICS:
        print(
            f"TABLE {source_table} -> {target_table}: "
            f"exports={len(table_dates):,}, min={table_dates[0]}, max={table_dates[-1]}"
        )

if not framework_archive_present:
    framework_contract_matches = contracts_by_table.get(
        normalise(FRAMEWORK_FALLBACK_TABLE), []
    )
    if len(framework_contract_matches) > 1:
        raise ValueError(
            "Ambiguous framework contracts: "
            f"{framework_contract_matches}"
        )
    framework_schema_cols = (
        contracts[framework_contract_matches[0]]
        if framework_contract_matches
        else FRAMEWORK_FALLBACK_SCHEMA
    )
    framework_schema_cols = complete_framework_schema(
        framework_schema_cols, FRAMEWORK_FALLBACK_PATH,
        f"{SILVER_SCHEMA}.{FRAMEWORK_FALLBACK_TABLE}",
    )
    source_tables.append({
        "physical_table": FRAMEWORK_FALLBACK_TABLE,
        "source_schema": "Files",
        "source_table": FRAMEWORK_FALLBACK_PATH,
        "target_table": f"{SILVER_SCHEMA}.{FRAMEWORK_FALLBACK_TABLE}",
        "schema_cols": framework_schema_cols,
        "available_dates": [],
        "fallback_path": FRAMEWORK_FALLBACK_PATH,
        "is_fallback_only": True,
    })
    print(
        "WARN archived framework table is completely absent; "
        f"using controlled fallback {FRAMEWORK_FALLBACK_PATH} for every month"
    )

# Order tables so that FK parents are materialised before their children.
# The schema contract carries referenced_table for each FK; build a dependency
# graph over the replayable set and topologically sort it. Alphabetical order
# alone can load a child (e.g. offer.additional_fee) before its parent
# (offer.offer), breaking downstream referential-integrity checks.
def order_tables_by_dependency(source_tables):
    # normalised contract table name -> target_table for the replayable set.
    contract_name_to_target = {}
    for entry in source_tables:
        contract_name_to_target.setdefault(
            normalise(entry["target_table"].split(".")[-1]),
            entry["target_table"],
        )

    # dependencies[target] = set of targets that must load first.
    dependencies = {entry["target_table"]: set() for entry in source_tables}
    for entry in source_tables:
        target = entry["target_table"]
        for col in entry["schema_cols"]:
            ref_table = (col.get("referenced_table") or "").strip()
            if not ref_table:
                continue
            parent_target = contract_name_to_target.get(normalise(ref_table))
            if parent_target and parent_target != target:
                dependencies[target].add(parent_target)

    # Kahn's algorithm with deterministic (alphabetical) tie-breaking.
    replayable = {entry["target_table"]: entry for entry in source_tables}
    ordered = []
    remaining = {t: set(deps) for t, deps in dependencies.items()}
    while remaining:
        ready = sorted(t for t, deps in remaining.items() if not deps)
        if not ready:  # cycle: break deterministically to avoid an infinite loop
            ready = [sorted(remaining)[0]]
        for target in ready:
            ordered.append(replayable[target])
            del remaining[target]
            for deps in remaining.values():
                deps.discard(target)
    return ordered


source_tables = order_tables_by_dependency(source_tables)
print(
    "Dependency-ordered replay: "
    + ", ".join(entry["physical_table"] for entry in source_tables)
)

if not source_tables or not all_available_dates:
    raise ValueError(f"No replayable archive tables found in {ARCHIVE_SCHEMA}")

available_dates = sorted(all_available_dates)
minimum_export_date = available_dates[0]
maximum_export_date = available_dates[-1]

# The final available export in each calendar month is the canonical
# snapshot date. A table that was not exported on that exact date carries
# forward its own latest available full snapshot on or before the date.
month_last_dates = {}
for export_date in available_dates:
    month_last_dates[(export_date.year, export_date.month)] = export_date
month_end_dates = sorted(month_last_dates.values())

if PROCESS_ONLY:
    if BATCH_EXPORT_DATE:
        raise ValueError("Set either PROCESS_ONLY (YYYY-MM) or BATCH_EXPORT_DATE (YYYY-MM-DD), not both")
    try:
        requested_month_date = datetime.strptime(PROCESS_ONLY, "%Y-%m")
    except ValueError as exc:
        raise ValueError("PROCESS_ONLY must use YYYY-MM, for example 2026-05") from exc
    requested_month = (requested_month_date.year, requested_month_date.month)
    if requested_month not in month_last_dates:
        raise ValueError(f"No archive exports found in requested month {PROCESS_ONLY}")
    canonical_date = month_last_dates[requested_month]
    month_end_dates = [canonical_date]
    print(f"PROCESS_ONLY {PROCESS_ONLY}; canonical month-end export is {canonical_date}")
elif BATCH_EXPORT_DATE:
    requested_date = datetime.strptime(BATCH_EXPORT_DATE, "%Y-%m-%d").date()
    requested_month = (requested_date.year, requested_date.month)
    if requested_month not in month_last_dates:
        raise ValueError(f"No archive exports found in requested month {requested_date:%Y-%m}")
    canonical_date = month_last_dates[requested_month]
    month_end_dates = [canonical_date]
    print(
        f"Requested {requested_date}; canonical month-end export is {canonical_date}"
    )

print(
    f"Archive export range: {minimum_export_date} to {maximum_export_date}; "
    f"{len(available_dates):,} distinct export days"
)
print(
    f"Month-end batches: {len(month_end_dates):,}; "
    f"{', '.join(str(value) for value in month_end_dates)}"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils

SOURCE_KIND = "ARCHIVE_MONTH_END"
METRIC_SCHEMA = "run_id string,layer string,source_kind string,source_object string,target_object string,rows_read long,rows_written long,duplicate_key_count long,null_primary_key_count long,recorded_at timestamp,job_run_id string"
ok = failed = total_read = total_written = 0
skipped_months = 0
skipped_contracts = len(skipped_contract_tables)
errors = []


def month_end_record(snapshot_date):
    """Return the orchestration state for one canonical month-end."""
    rows = (spark.table("monitoring.cfg_month_end_gold_run")
        .where(F.col("snapshot_date") == F.lit(snapshot_date).cast("date"))
        .limit(1).collect())
    return rows[0].asDict() if rows else None


def update_month_end(snapshot_date, status, dq_result=None,
                     gold_result=None, error_message=None):
    """Upsert the DQ/Gold orchestration state for a snapshot."""
    now = datetime.utcnow()
    existing = month_end_record(snapshot_date) or {}
    attempt_count = int(existing.get("attempt_count") or 0) + (
        1 if status == "RUNNING" else 0
    )
    row = spark.createDataFrame([(
        snapshot_date,
        status,
        False if status in ("RUNNING", "SUCCESS") else bool(existing.get("reload", False)),
        attempt_count,
        RUN_ID,
        now if status == "RUNNING" else existing.get("started_at"),
        None if status == "RUNNING" else now,
        dq_result,
        gold_result,
        error_message[:4000] if error_message else None,
        now,
    )], "snapshot_date date,status string,reload boolean,attempt_count int,run_id string,started_at timestamp,ended_at timestamp,dq_result string,gold_result string,error_message string,last_updated_at timestamp")
    target = DeltaTable.forName(spark, "monitoring.cfg_month_end_gold_run")
    (target.alias("t").merge(row.alias("s"), "t.snapshot_date = s.snapshot_date")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())


def latest_table_export(table_dates, snapshot_date):
    """Choose a table's latest full export on or before the snapshot."""
    position = bisect_right(table_dates, snapshot_date) - 1
    return table_dates[position] if position >= 0 else None



def materialise_table_month_end(table_info, snapshot_date):
    """Overwrite one Silver table with its canonical month-end state."""
    archive_source_schema = table_info.get(
        "source_schema", ARCHIVE_SCHEMA
    )
    archive_source_table = table_info["source_table"]
    target_table = table_info["target_table"]
    schema_cols = table_info["schema_cols"]
    fallback_path = table_info.get("fallback_path")
    archive_source_date = latest_table_export(
        table_info["available_dates"], snapshot_date
    )
    use_fallback = bool(table_info.get("is_fallback_only", False)) or (
        bool(fallback_path) and archive_source_date is None
    )
    source_schema = "Files" if use_fallback else archive_source_schema
    source_table = fallback_path if use_fallback else archive_source_table
    source_date = snapshot_date if use_fallback else archive_source_date
    if source_date is None:
        print(
            f"SKIP {archive_source_table}: "
            f"no export on or before {snapshot_date}"
        )
        return 0, 0, 0

    audit_timestamp = datetime.combine(snapshot_date, datetime.min.time())
    audit_begin(
        SOURCE_KIND, source_schema, source_table,
        target_table, audit_timestamp,
    )
    formatted = None
    try:
        # Each dated archive file is a complete snapshot. Selecting only
        # the final available file avoids scanning every daily snapshot. The
        # framework fallback is used only when that archive entity is absent.
        raw_frame = (
            read_framework_fallback(snapshot_date)
            if use_fallback
            else spark.table(source_table).where(
                F.to_date(parsed_archive_export_timestamp(F.col("export_date")))
                == F.lit(source_date)
            )
        )
        source_count = raw_frame.count()
        if source_count == 0:
            raise ValueError(f"No rows found for selected export {source_date}")

        deduplicated, key_columns = deduplicate_frame(raw_frame, schema_cols)

        # Persist so validation, diagnostics and the Delta write reuse the
        # same conformed result instead of recomputing the Spark plan.
        formatted = format_frame(
            deduplicated, schema_cols, SOURCE_KIND, source_table
        )
        if use_fallback:
            formatted = (formatted
                .withColumn("_archive_fallback", F.lit(True))
                .withColumn("_source_file", F.lit(FRAMEWORK_FALLBACK_PATH)))
        formatted = formatted.persist()
        written = formatted.count()
        duplicate_count = source_count - written
        formatted_export_non_null = formatted.where(
            F.col("export_date").isNotNull()
        ).count()
        if formatted_export_non_null != written:
            raise ValueError(
                f"export_date parse failure in {source_table}: "
                f"{written - formatted_export_non_null} of {written} rows are null"
            )

        print(f"MONTH END {snapshot_date}: {source_table} -> {target_table}")
        print_load_diagnostics(
            source_table, target_table, snapshot_date, source_date,
            raw_frame, formatted, key_columns, source_count, written,
            duplicate_count, formatted_export_non_null,
        )

        (formatted.write.format("delta").mode("overwrite")
            .option("overwriteSchema", "true").saveAsTable(target_table))

        if VERBOSE_DIAGNOSTICS:
            target_stats = spark.table(target_table).agg(
                F.count(F.lit(1)).alias("rows"),
                F.sum(F.when(F.col("export_date").isNull(), 1).otherwise(0)).alias("null_dates"),
                F.min("export_date").alias("min_export_date"),
                F.max("export_date").alias("max_export_date"),
            ).first().asDict()
            print(f"  TARGET CHECK {target_table}: {target_stats}")

        audit_finish(
            SOURCE_KIND, source_schema, source_table, target_table,
            audit_timestamp, "SUCCESS", source_count, written,
            duplicate_count,
        )
        append_rows(
            "monitoring.cfg_table_load_metric",
            [(RUN_ID, "SILVER", SOURCE_KIND, source_table, target_table,
              source_count, written, duplicate_count, None, datetime.utcnow(),
              JOB_RUN_ID or None)],
            METRIC_SCHEMA,
        )
        return source_count, written, duplicate_count
    except Exception as exc:
        audit_finish(
            SOURCE_KIND, source_schema, source_table, target_table,
            audit_timestamp, "FAILED", error_message=str(exc)[:4000],
        )
        raise
    finally:
        if formatted is not None:
            formatted.unpersist()


def delete_monitoring_rows(table_name, predicate, label):
    """Delete a scoped operational-monitoring slice and report its count."""
    if not spark.catalog.tableExists(table_name):
        print(f"SKIP {label}: {table_name} does not exist")
        return 0
    before = spark.table(table_name).where(predicate).count()
    spark.sql(f"DELETE FROM {table_name} WHERE {predicate}")
    print(f"CLEARED {label}: {before:,} rows from {table_name}")
    return before


def drop_rebuildable_schema_objects(schema_name, preserved_objects=()):
    """Drop managed tables/views rebuilt by the archive replay."""
    preserved = {name.lower() for name in preserved_objects}
    rows = spark.sql(f"SHOW TABLES IN {qident(schema_name)}").collect()
    dropped = []
    for row in rows:
        object_name = row.tableName
        if row.isTemporary or object_name.lower() in preserved:
            continue
        object_type = spark.catalog.getTable(
            f"{schema_name}.{object_name}"
        ).tableType.upper()
        qualified_name = f"{qident(schema_name)}.{qident(object_name)}"
        statement = "DROP VIEW" if object_type == "VIEW" else "DROP TABLE"
        spark.sql(f"{statement} IF EXISTS {qualified_name}")
        dropped.append(f"{schema_name}.{object_name}")
    return dropped


def reset_all_archive_processing():
    """Clear archive replay state and rebuildable Silver/Gold objects."""
    if not RESET_ALL_ARCHIVE_PROCESSING:
        return

    print("RESET ALL preview: clearing archive replay state and rebuildable Silver/Gold objects")
    reset_slices = [
        ("monitoring.cfg_month_end_gold_run", "1 = 1", "month-end Gold runs"),
        ("monitoring.cfg_silver_export_load", "source_kind = 'ARCHIVE_MONTH_END'", "archive Silver export loads"),
        ("monitoring.cfg_table_load_metric", "source_kind = 'ARCHIVE_MONTH_END'", "archive table metrics"),
        ("monitoring.cfg_pipeline_run", "source_kind IN ('ARCHIVE', 'ARCHIVE_MONTH_END')", "archive pipeline runs"),
        ("monitoring.cfg_schema_drift_event", "source_kind IN ('ARCHIVE', 'ARCHIVE_MONTH_END')", "archive schema-drift events"),
    ]
    cleared_rows = sum(
        delete_monitoring_rows(table_name, predicate, label)
        for table_name, predicate, label in reset_slices
    )
    dropped_silver = drop_rebuildable_schema_objects(SILVER_SCHEMA)
    dropped_gold = drop_rebuildable_schema_objects(
        GOLD_SCHEMA, preserved_objects=("cfg_placement_urgency_rule",)
    )
    print(
        f"RESET ALL complete: cleared {cleared_rows:,} archive monitoring rows; "
        f"dropped {len(dropped_silver):,} Silver and {len(dropped_gold):,} Gold objects"
    )
    print(
        "RESET ALL preserved Bronze/archive data and preserved configuration catalogues: "
        "schema contract, DQ rules, file configuration, Gold lineage mapping and urgency rules."
    )


if RESET_ALL_ARCHIVE_PROCESSING:
    reset_all_archive_processing()


if PROCESS_ONLY and (RESET_MONTH_MONITORING or CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY):
    expected_confirmation = f"RESET {PROCESS_ONLY}"
    if CONFIRM_PROCESS_ONLY_RESET != expected_confirmation:
        raise ValueError(
            f"Reset not executed. Set CONFIRM_PROCESS_ONLY_RESET exactly to {expected_confirmation!r}."
        )
    selected_snapshot = month_end_dates[0]
    if RESET_MONTH_MONITORING:
        spark.sql(
            "DELETE FROM monitoring.cfg_month_end_gold_run "
            f"WHERE snapshot_date = DATE '{selected_snapshot.isoformat()}'"
        )
        spark.sql(
            "DELETE FROM monitoring.cfg_silver_export_load "
            "WHERE source_kind = 'ARCHIVE_MONTH_END' "
            f"AND DATE(export_date) = DATE '{selected_snapshot.isoformat()}'"
        )
        print(f"RESET monitoring state for {selected_snapshot}")
    elif CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY:
        # Retain the audit history, but flag the selected archive month as
        # deliberately reloaded. This prevents a prior SUCCESS state from
        # skipping the Silver, DQ and Gold rebuild after targets are cleared.
        spark.sql(
            "UPDATE monitoring.cfg_month_end_gold_run "
            "SET reload = true, last_updated_at = current_timestamp() "
            f"WHERE snapshot_date = DATE '{selected_snapshot.isoformat()}'"
        )
        spark.sql(
            "UPDATE monitoring.cfg_silver_export_load "
            "SET reload = true, last_updated_at = current_timestamp() "
            "WHERE source_kind = 'ARCHIVE_MONTH_END' "
            f"AND DATE(export_date) = DATE '{selected_snapshot.isoformat()}'"
        )
        print(f"FLAGGED monitoring state for reload: {selected_snapshot}")
    if CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY:
        for target_table in sorted({info["target_table"] for info in source_tables}):
            spark.sql(f"DROP TABLE IF EXISTS {target_table}")
        print(f"RESET Silver targets for {PROCESS_ONLY}")

for snapshot_date in month_end_dates:
    existing = month_end_record(snapshot_date)
    stale_targets = [
        info["target_table"] for info in source_tables
        if target_requires_refresh(info["target_table"], info["schema_cols"])
    ]
    if existing and existing["status"] == "SUCCESS" and not existing["reload"] and not stale_targets:
        skipped_months += 1
        print(f"SKIP MONTH {snapshot_date}: Silver, DQ and Gold already successful")
        continue
    if stale_targets:
        print(f"REFRESH MONTH {snapshot_date}: stale Silver targets {stale_targets}")

    print(f"\n=== PROCESSING CANONICAL MONTH END {snapshot_date} ===")
    update_month_end(snapshot_date, "RUNNING")
    month_errors = []

    # Rebuild every Silver table for a month being retried. Individual
    # table audit rows cannot be used to skip here because shared Silver
    # may currently contain a later month's state.
    for table_info in source_tables:
        try:
            rows_read, rows_written, _ = materialise_table_month_end(
                table_info, snapshot_date
            )
            ok += 1
            total_read += rows_read
            total_written += rows_written
        except Exception as exc:
            message = str(exc)[:4000]
            failed += 1
            month_errors.append(f"{table_info['source_table']}: {message}")
            print(f"FAILED {table_info['source_table']} @ {snapshot_date}: {message}")

    if month_errors:
        message = " | ".join(month_errors)[:4000]
        errors.append(f"{snapshot_date}: {message}")
        update_month_end(snapshot_date, "FAILED", error_message=message)
        if FAIL_ON_TABLE_ERROR:
            break
        continue

    if RUN_GOLD_AT_MONTH_END:
        try:
            dq_result = mssparkutils.notebook.run(
                DQ_NOTEBOOK_NAME, NOTEBOOK_TIMEOUT_SECONDS
            )
            gold_result = mssparkutils.notebook.run(
                GOLD_NOTEBOOK_NAME,
                NOTEBOOK_TIMEOUT_SECONDS,
                {"AS_OF_DATE": snapshot_date.isoformat()},
            )
            # Dimensions are current-state tables. Rebuilding them for every
            # historical month adds repeated work and leaves only the final
            # result, so publish them once after the final selected batch.
            is_final_month_end_batch = snapshot_date == month_end_dates[-1]
            dimensions_result = None
            if RUN_GOLD_DIMENSIONS_AT_MONTH_END and is_final_month_end_batch:
                dimensions_result = mssparkutils.notebook.run(
                    GOLD_DIMENSIONS_NOTEBOOK_NAME,
                    NOTEBOOK_TIMEOUT_SECONDS,
                    {"AS_OF_DATE": snapshot_date.isoformat()},
                )
            elif RUN_GOLD_DIMENSIONS_AT_MONTH_END:
                print(
                    f"Gold dimensions deferred until final batch {month_end_dates[-1]}; current batch is {snapshot_date}"
                )
            gold_status = str(gold_result)
            if dimensions_result is not None:
                gold_status += f"; dimensions={dimensions_result}"
            elif RUN_GOLD_DIMENSIONS_AT_MONTH_END:
                gold_status += "; dimensions=deferred until final batch"
            update_month_end(
                snapshot_date, "SUCCESS", str(dq_result), gold_status
            )
            completed_steps = (
                "DQ, Gold and dimensions"
                if dimensions_result is not None else "DQ and Gold"
            )
            print(f"MONTH END COMPLETE {snapshot_date}: {completed_steps} succeeded")
        except Exception as exc:
            message = str(exc)[:4000]
            errors.append(f"{snapshot_date} DQ/Gold: {message}")
            update_month_end(snapshot_date, "FAILED", error_message=message)
            print(f"MONTH END FAILED {snapshot_date}: {message}")
            if FAIL_ON_TABLE_ERROR:
                break
    else:
        update_month_end(snapshot_date, "SUCCESS")

status = "FAILED" if errors else "SUCCESS"
error_text = " | ".join(errors)[:4000] if errors else None
error_sql = "NULL" if error_text is None else "'" + error_text.replace("'", "''") + "'"
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run
SET ended_at=current_timestamp(), status='{status}',
    tables_succeeded={ok}, tables_failed={failed},
    rows_read={total_read}, rows_written={total_written},
    error_message={error_sql}
WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='02a_archive_silver'""")
print(
    f"Archive month-end run {RUN_ID}: {status}; "
    f"loaded={ok}, skipped_months={skipped_months}, "
    f"skipped_contracts={skipped_contracts}, failed={failed}"
)
if errors and FAIL_ON_TABLE_ERROR:
    raise RuntimeError(error_text)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
