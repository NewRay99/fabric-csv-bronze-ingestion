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
# Profiles low-cardinality string columns that are defined in the schema contract. Each run replaces the stored domain for the profiled Bronze table and column; domains with more than 40 values are deliberately not retained.

# PARAMETERS CELL ********************

BRONZE_SCHEMA = "bronze"
CONTRACT_TABLE = "monitoring.cfg_schema_contract_column"
DOMAIN_TABLE = "monitoring.cfg_data_domain"
MAX_DISTINCT_VALUES = 40
INCLUDE_EMPTY_STRING = False
CLEAR_TARGET_TABLE = True

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

if CLEAR_TARGET_TABLE:
    clear_data_domain_table(DOMAIN_TABLE)
    print(f"Cleared target data-domain table: {DOMAIN_TABLE}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

if not spark.catalog.tableExists(CONTRACT_TABLE):
    raise RuntimeError(f"Schema contract table does not exist: {CONTRACT_TABLE}")
if not spark.catalog.tableExists(DOMAIN_TABLE):
    raise RuntimeError(f"Data-domain table does not exist: {DOMAIN_TABLE}")

# Build a case- and punctuation-insensitive map from the contract. Conflicting
# entries are not profiled: the contract must be unambiguous before it governs a domain.
contract_definitions = {}
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
for key in ambiguous_contract_columns:
    contract_definitions.pop(key, None)

bronze_tables = {}
for row in spark.sql(f"SHOW TABLES IN {qident(BRONZE_SCHEMA)}").collect():
    if not row.isTemporary:
        bronze_tables.setdefault(normalise(row.tableName), row.tableName)

profiled_columns = 0
skipped_high_cardinality = 0
skipped_empty = 0
skipped_unsuitable = 0
skipped_by_reason = {}
missing_bronze_columns = 0

for (logical_table, logical_column), contract_data_type in sorted(contract_definitions.items()):
    source_table = bronze_tables.get(logical_table)
    if source_table is None:
        missing_bronze_columns += 1
        continue

    source_frame = spark.table(f"{qident(BRONZE_SCHEMA)}.{qident(source_table)}")
    actual_columns = {normalise(field.name): field.name for field in source_frame.schema.fields}
    source_column = actual_columns.get(logical_column)
    if source_column is None:
        missing_bronze_columns += 1
        continue

    exclusion_reason = data_domain_exclusion_reason(source_column, contract_data_type)
    if exclusion_reason:
        # Do not scan unsuitable values; remove a prior domain if policy has changed.
        remove_data_domain(DOMAIN_TABLE, BRONZE_SCHEMA, source_table, source_column)
        skipped_unsuitable += 1
        skipped_by_reason[exclusion_reason] = skipped_by_reason.get(exclusion_reason, 0) + 1
        continue

    values = collect_low_cardinality_domain_values(
        source_frame, source_column, MAX_DISTINCT_VALUES, INCLUDE_EMPTY_STRING
    )
    # A None value is an explicit high-cardinality result. The common helper
    # reads at most 41 values, so this branch is reached before any insert.
    if values is None:
        remove_data_domain(DOMAIN_TABLE, BRONZE_SCHEMA, source_table, source_column)
        skipped_high_cardinality += 1
        continue
    if not values:
        remove_data_domain(DOMAIN_TABLE, BRONZE_SCHEMA, source_table, source_column)
        skipped_empty += 1
        continue

    replace_data_domain(
        DOMAIN_TABLE, BRONZE_SCHEMA, source_table, source_column,
        contract_data_type, values, PROFILED_AT, RUN_ID, JOB_RUN_ID,
    )
    profiled_columns += 1

summary = {
    "run_id": RUN_ID,
    "profiled_columns": profiled_columns,
    "skipped_high_cardinality": skipped_high_cardinality,
    "skipped_empty": skipped_empty,
    "skipped_unsuitable": skipped_unsuitable,
    "skipped_by_reason": skipped_by_reason,
    "missing_bronze_columns": missing_bronze_columns,
    "ambiguous_contract_columns": len(ambiguous_contract_columns),
}
print(summary)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.sql("SELECT * FROM LH_BCT_WMPP.archived.IT 1000")
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
