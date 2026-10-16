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
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Bronze data-domain profile
#
# Retains a version of each eligible low-cardinality domain on every run. Values are
# labelled BASELINE, ADDED, UNCHANGED or REMOVED against the previous comparable
# version. Empty and skipped profiles are recorded without deleting history.
# Domains with more than 40 values remain deliberately uncollected.

# PARAMETERS CELL ********************

BRONZE_SCHEMA = "bronze"
CONTRACT_TABLE = "monitoring.cfg_schema_contract_column"
DOMAIN_TABLE = "monitoring.cfg_data_domain"
MAX_DISTINCT_VALUES = 40
INCLUDE_EMPTY_STRING = False

# This standalone control notebook owns its configuration bootstrap.
CFG_NOTEBOOK_NAME = "00_setup_cfg"
COMMON_LIBRARY_NOTEBOOK = "99_common_library"
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
NOTEBOOK_TIMEOUT_SECONDS = 1800
JOB_RUN_ID = ""


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils

cfg_result = mssparkutils.notebook.run(
    CFG_NOTEBOOK_NAME,
    NOTEBOOK_TIMEOUT_SECONDS,
    {
        "AUDIT_TABLE": AUDIT_TABLE,
        "TIME_PARSER_POLICY": TIME_PARSER_POLICY,
        "JOB_RUN_ID": JOB_RUN_ID,
    },
)
print(f"Configuration setup completed: {cfg_result}")

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

from datetime import datetime, timezone
from uuid import uuid4

RUN_ID = str(uuid4())
PROFILED_AT = datetime.now(timezone.utc)

IS_ORCHESTRATED_RUN = bool(JOB_RUN_ID)
JOB_RUN_ID = JOB_RUN_ID or RUN_ID


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def record_domain_job(status, error_message=None):
    # A supplied parent owns its job; standalone profiles receive their own job.
    if IS_ORCHESTRATED_RUN:
        return
    ended_at = None if status == "RUNNING" else datetime.now(timezone.utc)
    merge_monitor_row(
        "monitoring.cfg_job_run",
        (JOB_RUN_ID, "99_data_domain", PROFILED_AT, ended_at, status,
         int(status == "SUCCESS"), int(status == "FAILED"), error_message,
         datetime.now(timezone.utc)),
        "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id",
    )
    merge_monitor_row(
        "monitoring.cfg_job_step_run",
        (JOB_RUN_ID, 1, "99_data_domain", PROFILED_AT, ended_at, status,
         None, error_message, datetime.now(timezone.utc)),
        "job_run_id string,step_sequence int,notebook_name string,started_at timestamp,ended_at timestamp,status string,child_result string,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence",
    )


def profile_data_domains():
    if not spark.catalog.tableExists(CONTRACT_TABLE):
        raise RuntimeError(f"Schema contract table does not exist: {CONTRACT_TABLE}")
    if not spark.catalog.tableExists(DOMAIN_TABLE):
        raise RuntimeError(f"Data-domain table does not exist: {DOMAIN_TABLE}")
    maximum = int(MAX_DISTINCT_VALUES)
    if maximum < 1:
        raise ValueError("MAX_DISTINCT_VALUES must be at least 1")
    include_empty = str(INCLUDE_EMPTY_STRING).strip().lower() in {"true", "1", "yes", "y"}
    previous_profiles = latest_data_domain_profiles(DOMAIN_TABLE)
    contract_definitions = {}
    contract_names = {}
    ambiguous_contract_columns = set()
    for row in spark.table(CONTRACT_TABLE).select("table_name", "column_name", "data_type").collect():
        if not row.table_name or not row.column_name or not is_contract_string(row.data_type):
            continue
        key = (normalise(row.table_name), normalise(row.column_name))
        existing_type = contract_definitions.get(key)
        if existing_type is not None and existing_type != row.data_type:
            ambiguous_contract_columns.add(key)
        else:
            contract_definitions[key] = row.data_type
            contract_names[key] = (row.table_name, row.column_name)
    for key in ambiguous_contract_columns:
        contract_definitions.pop(key, None)

    bronze_tables = {}
    for row in spark.sql(f"SHOW TABLES IN {qident(BRONZE_SCHEMA)}").collect():
        if not row.isTemporary:
            bronze_tables.setdefault(normalise(row.tableName), row.tableName)
    summary = {
        "run_id": RUN_ID, "job_run_id": JOB_RUN_ID, "profiled_columns": 0,
        "skipped_high_cardinality": 0, "skipped_empty": 0, "skipped_unsuitable": 0,
        "skipped_by_reason": {}, "missing_bronze_columns": 0,
        "ambiguous_contract_columns": len(ambiguous_contract_columns),
    }
    snapshots = []
    for key, contract_data_type in sorted(contract_definitions.items()):
        logical_table, logical_column = key
        contract_table, contract_column = contract_names[key]
        source_table = bronze_tables.get(logical_table)
        source_column = None
        source_frame = None
        if source_table is not None:
            source_frame = spark.table(f"{qident(BRONZE_SCHEMA)}.{qident(source_table)}")
            actual_columns = {normalise(field.name): field.name for field in source_frame.schema.fields}
            source_column = actual_columns.get(logical_column)
        table_name = source_table or contract_table
        column_name = source_column or contract_column
        previous = previous_profiles.get((BRONZE_SCHEMA, table_name, column_name))
        reason = data_domain_exclusion_reason(column_name, contract_data_type)
        values = None
        if reason:
            status = "EXCLUDED"
            summary["skipped_unsuitable"] += 1
            reasons = summary["skipped_by_reason"]
            reasons[reason] = reasons.get(reason, 0) + 1
        elif source_frame is None or source_column is None:
            status = "SOURCE_MISSING"
            summary["missing_bronze_columns"] += 1
        else:
            values = collect_low_cardinality_domain_values(source_frame, source_column, maximum, include_empty)
            if values is None:
                status = "HIGH_CARDINALITY"
                summary["skipped_high_cardinality"] += 1
            else:
                status = "PROFILED"
                summary["profiled_columns"] += 1
                if not values:
                    summary["skipped_empty"] += 1
        snapshots.extend(build_data_domain_snapshot(
            BRONZE_SCHEMA, table_name, column_name, contract_data_type,
            values, PROFILED_AT, RUN_ID, JOB_RUN_ID, previous, status,
        ))
    # One atomic Delta append publishes the whole batch after all scans succeed.
    append_data_domain_snapshots(DOMAIN_TABLE, snapshots)
    summary["retained_records"] = len(snapshots)
    summary["values_added"] = sum(row["change_type"] == "ADDED" for row in snapshots)
    summary["values_removed"] = sum(row["change_type"] == "REMOVED" for row in snapshots)
    return summary


record_domain_job("RUNNING")
try:
    summary = profile_data_domains()
except Exception as exc:
    record_domain_job("FAILED", str(exc)[:4000])
    raise
else:
    record_domain_job("SUCCESS")
    print(summary)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
