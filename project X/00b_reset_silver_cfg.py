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
# META       "default_warehouse": "9a24911d-3f57-4c68-889f-88b1dbbc2cc0",
# META       "known_warehouses": [
# META         {
# META           "id": "9a24911d-3f57-4c68-889f-88b1dbbc2cc0",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 00b — Reset Silver controls and optionally rebuild the Silver schema
#
# Use this administrative notebook when Silver ingestion must be replayed from scratch. It removes only Silver execution state from the global `monitoring.cfg_*` tables and can drop physical `silver.*` tables.
#
# It deliberately preserves Bronze data, archive data, archive ZIP/file/table controls, Gold tables, and the configured DQ rule catalogue. The reset does nothing unless `CONFIRM_RESET` exactly matches `RESET SILVER`.

# CELL ********************

MONITORING_SCHEMA = "monitoring"
CFG_NOTEBOOK_NAME = "00_setup_cfg"
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
NOTEBOOK_TIMEOUT_SECONDS = 1800
SILVER_SCHEMA = "silver"
SILVER_TABLE_PREFIX = ""

# Safety lock. Set this exact value only after reviewing the preview.
CONFIRM_RESET = ""  # Required value: RESET SILVER

# Live and archive Silver execution controls can be reset independently.
RESET_LATEST_SILVER = True
RESET_ARCHIVE_SILVER = True

# A full rebuild normally drops * tables and clears dependent DQ output.
DROP_SILVER_TABLES = True
CLEAR_DQ_EXECUTION_HISTORY = True
CLEAR_SCHEMA_CONTRACT_CACHE = True

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

## spark.sql(f"drop schema IF EXISTS {SILVER_SCHEMA}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def qident(value):
    """Quote a Spark SQL identifier."""
    return "`" + str(value).replace("`", "``") + "`"


def table_exists(table_name):
    """Return False when an optional monitoring table is not deployed."""
    return spark.catalog.tableExists(table_name)


def selected_source_kinds():
    """Return current and legacy Silver source-kind values to reset."""
    kinds = []
    if RESET_LATEST_SILVER:
        kinds.append("LATEST")
    if RESET_ARCHIVE_SILVER:
        kinds.extend(["ARCHIVE_MONTH_END", "ARCHIVE"])
    return kinds


def sql_string_list(values):
    """Build a quoted SQL value list from fixed configuration values."""
    return ", ".join("'" + value.replace("'", "''") + "'" for value in values)


def count_where(table_name, predicate="1 = 1"):
    """Count rows that the reset would remove."""
    if not table_exists(table_name):
        return None
    return spark.sql(
        f"SELECT COUNT(*) AS row_count FROM {table_name} WHERE {predicate}"
    ).first()["row_count"]


def delete_where(table_name, predicate, label):
    """Delete scoped execution rows and report the before/after count."""
    before = count_where(table_name, predicate)
    if before is None:
        print(f"SKIP {label}: {table_name} does not exist")
        return 0
    spark.sql(f"DELETE FROM {table_name} WHERE {predicate}")
    after = count_where(table_name, predicate)
    removed = int(before) - int(after)
    print(f"CLEARED {label}: {removed:,} rows from {table_name}")
    return removed


def silver_tables():
    """Discover only managed Silver tables following <table>."""
    try:
        rows = spark.sql(f"SHOW TABLES IN {qident(SILVER_SCHEMA)}").collect()
    except Exception:
        return []
    return sorted(
        row.tableName for row in rows
        if not row.isTemporary and row.tableName.lower().startswith(SILVER_TABLE_PREFIX)
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from notebookutils import mssparkutils

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qident(SILVER_SCHEMA)}")
cfg_result = mssparkutils.notebook.run(
    CFG_NOTEBOOK_NAME,
    NOTEBOOK_TIMEOUT_SECONDS,
    {"AUDIT_TABLE": AUDIT_TABLE, "TIME_PARSER_POLICY": TIME_PARSER_POLICY},
)
print(f"Configuration setup completed: {cfg_result}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Preview the exact scope before allowing any destructive operation.
source_kinds = selected_source_kinds()
if not source_kinds:
    raise ValueError("Select RESET_LATEST_SILVER and/or RESET_ARCHIVE_SILVER")
source_predicate = f"source_kind IN ({sql_string_list(source_kinds)})"

preview_targets = [
    ("monitoring.cfg_silver_export_load", source_predicate),
    ("monitoring.cfg_pipeline_run", "layer = 'SILVER'"),
    ("monitoring.cfg_table_load_metric", "layer = 'SILVER'"),
    ("monitoring.cfg_schema_drift_event", source_predicate),
]
if RESET_ARCHIVE_SILVER:
    preview_targets.append(("monitoring.cfg_month_end_gold_run", "1 = 1"))
if CLEAR_DQ_EXECUTION_HISTORY:
    preview_targets.extend([
        ("monitoring.cfg_data_quality_result", "1 = 1"),
        ("monitoring.cfg_rejected_row", "1 = 1"),
        ("monitoring.cfg_referential_exception", "1 = 1"),
    ])
if CLEAR_SCHEMA_CONTRACT_CACHE:
    preview_targets.append(("monitoring.cfg_schema_contract_column", "1 = 1"))

print(f"Silver source kinds selected: {source_kinds}")
for table_name, predicate in preview_targets:
    count = count_where(table_name, predicate)
    print(f"PREVIEW {table_name}: {'not deployed' if count is None else f'{count:,} rows'}")

tables_to_drop = silver_tables() if DROP_SILVER_TABLES else []
print(f"PREVIEW Silver tables to drop ({len(tables_to_drop)}): {tables_to_drop}")
print("Preserved: bronze.*, archived.*, gold.*, monitoring.cfg_archive_*, and monitoring.cfg_data_quality_rule")
if CONFIRM_RESET != "RESET SILVER":
    print("PREVIEW ONLY: set CONFIRM_RESET = 'RESET SILVER' and rerun to execute")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Destructive execution is isolated in this cell behind an exact phrase.
if CONFIRM_RESET != "RESET SILVER":
    raise ValueError("Reset not executed. Set CONFIRM_RESET exactly to 'RESET SILVER'.")

# Drop physical Silver tables first. If a drop fails, audit controls remain
# available and the reset can be diagnosed safely before retrying.
dropped_tables = []
if DROP_SILVER_TABLES:
    for table_name in tables_to_drop:
        qualified_name = f"{qident(SILVER_SCHEMA)}.{qident(table_name)}"
        spark.sql(f"DROP TABLE IF EXISTS {qualified_name}")
        dropped_tables.append(f"{SILVER_SCHEMA}.{table_name}")
        print(f"DROPPED {SILVER_SCHEMA}.{table_name}")

removed_rows = 0
removed_rows += delete_where(
    "monitoring.cfg_silver_export_load", source_predicate,
    "Silver export audit",
)
removed_rows += delete_where(
    "monitoring.cfg_pipeline_run", "layer = 'SILVER'",
    "Silver pipeline runs",
)
removed_rows += delete_where(
    "monitoring.cfg_table_load_metric", "layer = 'SILVER'",
    "Silver table metrics",
)
removed_rows += delete_where(
    "monitoring.cfg_schema_drift_event", source_predicate,
    "Silver schema-drift events",
)
if RESET_ARCHIVE_SILVER:
    removed_rows += delete_where(
        "monitoring.cfg_month_end_gold_run", "1 = 1",
        "archive month-end orchestration",
    )
if CLEAR_DQ_EXECUTION_HISTORY:
    removed_rows += delete_where(
        "monitoring.cfg_data_quality_result", "1 = 1", "DQ results"
    )
    removed_rows += delete_where(
        "monitoring.cfg_rejected_row", "1 = 1", "DQ rejected rows"
    )
    removed_rows += delete_where(
        "monitoring.cfg_referential_exception", "1 = 1",
        "DQ referential exceptions",
    )
if CLEAR_SCHEMA_CONTRACT_CACHE:
    removed_rows += delete_where(
        "monitoring.cfg_schema_contract_column", "1 = 1",
        "Silver schema-contract cache",
    )

print(
    f"RESET COMPLETE: dropped {len(dropped_tables):,} Silver tables; "
    f"cleared {removed_rows:,} monitoring rows"
)
print("Next: run either 02_silver_formatter or 02a_archive_silver.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
