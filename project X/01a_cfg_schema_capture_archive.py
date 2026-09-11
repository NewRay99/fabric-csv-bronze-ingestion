# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark",
# META     "jupyter_kernel_name": null
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
# META   },
# META   "spark_compute": {
# META     "compute_id": "/trident/default",
# META     "session_options": {
# META       "conf": {
# META         "spark.synapse.nbs.session.timeout": "1200000"
# META       }
# META     }
# META   },
# META   "sessionKeepAliveTimeout": 0,
# META   "a365ComputeOptions": null
# META }

# MARKDOWN ********************

# # 01a — Capture Schema in Archive Catalogue
#
# Run this to capture the Archive schema so we can compare it against what was provided by NEC, we will compare the live schema against the loaded schema contract table;
#
# This will help the downstream silver layer as the silver layer requires that the data has references keys.

# CELL ********************

COMPARED_SCHEMA = "Bronze"
FAIL_ON_CRITICAL = True

# Shared configuration setup
CFG_NOTEBOOK_NAME = "00_setup_cfg"
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.
IS_ORCHESTRATED_RUN = bool(JOB_RUN_ID)
NOTEBOOK_TIMEOUT_SECONDS = 1800

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

from notebookutils import mssparkutils

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

import re, uuid
from datetime import datetime
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType

RUN_ID = str(uuid.uuid4())
STARTED_AT = datetime.utcnow()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 1. define target schema
schema_def = StructType([
    StructField("table_name", StringType(), True),
    StructField("ordinal_position", StringType(), True),
    StructField("column_name", StringType(), True),
    StructField("data_type", StringType(), True),
    StructField("is_nullable", StringType(), True),
])

schema_records=[]

all_tables = spark.catalog.listTables(COMPARED_SCHEMA)
excluded_tables = sorted(tbl.name for tbl in all_tables if is_etl_excluded_table(tbl.name))
tables = [tbl for tbl in all_tables if not is_etl_excluded_table(tbl.name)]
if excluded_tables:
    print(f"Excluded internal/reference archive-capture tables: {excluded_tables}")

for tbl in tables:
    columns= spark.catalog.listColumns(f"{COMPARED_SCHEMA}.{tbl.name}")
    for idx,col in enumerate(columns, start=1):
        schema_records.append((tbl.name, str(idx), col.name, col.dataType, "true" if col.nullable else "false"))

schema_df=spark.createDataFrame(schema_records, schema=schema_def)

schema_df.withColumn("contract_loaded_at", F.current_timestamp()) \
        .write.format("delta").mode("append")\
            .saveAsTable("monitoring.cfg_archived_schema_live")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# MAGIC %%sql
# MAGIC
# MAGIC SELECT
# MAGIC     COALESCE(c.table_name, l.table_name) AS table_name,
# MAGIC     COALESCE(c.column_name, l.column_name) AS column_name,
# MAGIC     c.data_type AS contract_data_type,
# MAGIC     l.data_type AS live_data_type,
# MAGIC     CASE
# MAGIC         WHEN c.column_name IS NULL THEN 'UNCONTRACTED_COLUMN_ADDED'
# MAGIC         WHEN l.column_name IS NULL THEN 'CONTRACTED_COLUMN_MISSING'
# MAGIC         ELSE 'MATCH'
# MAGIC     END AS validation_status
# MAGIC FROM monitoring.cfg_schema_contract_column c
# MAGIC FULL OUTER JOIN monitoring.cfg_archived_schema_live l
# MAGIC     ON c.table_name = l.table_name
# MAGIC    AND c.column_name = l.column_name
# MAGIC WHERE c.column_name IS NULL
# MAGIC    OR l.column_name IS NULL
# MAGIC    OR c.data_type <> l.data_type;

# METADATA ********************

# META {
# META   "language": "sparksql",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/wmpp-production-data-export-birmingham/audit/jul26/2026-07-31.csv")
# df now is a Spark DataFrame containing CSV data from "Files/wmpp-production-data-export-birmingham/audit/jul26/2026-07-31.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

df = spark.read.format("csv").option("header","true").load("Files/wmpp-production-data-export-birmingham/latest/provider_submission_docs.csv")
# df now is a Spark DataFrame containing CSV data from "Files/wmpp-production-data-export-birmingham/latest/provider_submission_docs.csv".
display(df)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
