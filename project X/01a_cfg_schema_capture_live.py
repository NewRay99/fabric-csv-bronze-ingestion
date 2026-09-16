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

# # 01a — Capture Schema in Catalogue
#
# Run this to capture the live schema so we can compare it against what was provided by NEC, we will compare the live schema against the loaded schema contract table;
#
# This will help the downstream silver layer as the silver layer reuires that the data has references keys.

# CELL ********************

BRONZE_SCHEMA = "bronze"
SOURCE_KIND = "LIVE"
TABLE_PREFIXES = ()

JOB_RUN_ID = ""  # Parent orchestration correlation ID.

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

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.
# Run the pipeline runner rather than this notebook for a fresh environment.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import re
import uuid
from datetime import datetime

from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType, IntegerType, StringType, StructField, StructType,
    TimestampType,
)

RUN_ID = str(uuid.uuid4())
STARTED_AT = datetime.utcnow()
JOB_RUN_ID = JOB_RUN_ID or RUN_ID

CONTRACT_COLUMNS = [
    "table_name", "ordinal_position", "column_name", "data_type",
    "is_nullable", "column_default", "primary_key_name", "is_primary_key",
    "foreign_key_name", "referenced_schema", "referenced_table",
    "referenced_column", "column_description", "table_description",
]

LIVE_SCHEMA = StructType([
    StructField("table_name", StringType(), False),
    StructField("ordinal_position", IntegerType(), False),
    StructField("column_name", StringType(), False),
    StructField("live_data_type", StringType(), True),
    StructField("is_nullable", BooleanType(), True),
    StructField("captured_at", TimestampType(), False),
    StructField("run_id", StringType(), False),
    StructField("job_run_id", StringType(), True),
])

DRIFT_SCHEMA = "run_id string,source_kind string,source_table string,target_table string,drift_type string,column_name string,expected_type string,actual_type string,referenced_table string,referenced_column string,drift_key string,status string,occurrence_count long,first_detected_at timestamp,last_detected_at timestamp,resolved_at timestamp,detected_at timestamp,job_run_id string"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema_df = spark.table("monitoring.cfg_schema_contract_column")
missing_columns = set(CONTRACT_COLUMNS) - set(schema_df.columns)
if missing_columns:
    raise ValueError(f"monitoring.cfg_schema_contract_column is missing: {sorted(missing_columns)}")
definition_df = (schema_df.select(*CONTRACT_COLUMNS)
    .withColumn(
        "definition_hash",
        F.sha2(F.concat_ws("||", *[F.coalesce(F.col(name), F.lit("")) for name in CONTRACT_COLUMNS]), 256),
    )
    .withColumn("definition_loaded_at", F.current_timestamp()))
(definition_df.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_schema_drift_definition"))

previous_live = None
if spark.catalog.tableExists("monitoring.cfg_bronze_schema_live"):
    old_live = spark.table("monitoring.cfg_bronze_schema_live")
    old_type = "live_data_type" if "live_data_type" in old_live.columns else "data_type"
    old_time = "captured_at" if "captured_at" in old_live.columns else "contract_loaded_at"
    previous_live = old_live.select(
        F.lower("table_name").alias("table_name"),
        F.col("column_name"),
        F.col(old_type).alias("live_data_type"),
        F.col(old_time).alias("captured_at"),
    )

captured_at = datetime.utcnow()
records = []
excluded_live_tables = []
for table in spark.catalog.listTables(BRONZE_SCHEMA):
    if table.isTemporary:
        continue
    if is_etl_excluded_table(table.name):
        excluded_live_tables.append(table.name)
        continue
    logical_table = etl_logical_table_name(table.name)
    for position, column in enumerate(
        spark.catalog.listColumns(f"{BRONZE_SCHEMA}.{table.name}"), start=1
    ):
        records.append((
            logical_table, position, column.name, column.dataType,
            bool(column.nullable), captured_at, RUN_ID, JOB_RUN_ID or None,
        ))

current_live = spark.createDataFrame(records, LIVE_SCHEMA)
if excluded_live_tables:
    print(f"Excluded internal/reference Bronze tables: {sorted(excluded_live_tables)}")
if previous_live is None:
    previous_live = current_live.limit(0).select(
        "table_name", "column_name", "live_data_type", "captured_at"
    )

definition_df.createOrReplaceTempView("_schema_definition")
current_live.createOrReplaceTempView("_schema_live_current")
previous_live.createOrReplaceTempView("_schema_live_previous")
print(f"Loaded {definition_df.count():,} definition rows; captured {current_live.count():,} live columns")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

current_drifts = spark.sql(f"""
WITH definition AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name,
         data_type, referenced_table, referenced_column
  FROM _schema_definition
), live AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name, live_data_type
  FROM _schema_live_current
), previous AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name, live_data_type
  FROM _schema_live_previous
), definition_tables AS (SELECT DISTINCT table_name FROM definition),
live_tables AS (SELECT DISTINCT table_name FROM live),
drifts AS (
  SELECT l.table_name, CAST(NULL AS STRING) column_name, 'TABLE_ADDED' drift_type,
         CAST(NULL AS STRING) expected_type, CAST(NULL AS STRING) actual_type,
         CAST(NULL AS STRING) referenced_table, CAST(NULL AS STRING) referenced_column
  FROM live_tables l LEFT ANTI JOIN definition_tables d ON l.table_name=d.table_name
  UNION ALL
  SELECT d.table_name, CAST(NULL AS STRING), 'TABLE_REMOVED', NULL, NULL, NULL, NULL
  FROM definition_tables d LEFT ANTI JOIN live_tables l ON d.table_name=l.table_name
  UNION ALL
  SELECT l.table_name, l.column_name, 'COLUMN_ADDED', NULL, l.live_data_type, NULL, NULL
  FROM live l LEFT ANTI JOIN definition d
    ON l.table_name=d.table_name AND l.column_name=d.column_name
  UNION ALL
  SELECT d.table_name, d.column_name, 'COLUMN_REMOVED', d.data_type, NULL,
         d.referenced_table, d.referenced_column
  FROM definition d LEFT ANTI JOIN live l
    ON l.table_name=d.table_name AND l.column_name=d.column_name
  UNION ALL
  SELECT l.table_name, l.column_name, 'LIVE_TYPE_CHANGED', p.live_data_type,
         l.live_data_type, NULL, NULL
  FROM live l JOIN previous p
    ON l.table_name=p.table_name AND l.column_name=p.column_name
  WHERE coalesce(l.live_data_type, '') <> coalesce(p.live_data_type, '')
  UNION ALL
  SELECT d.table_name, d.column_name,
         CASE WHEN lt.table_name IS NULL THEN 'FK_TARGET_TABLE_MISSING'
              ELSE 'FK_TARGET_COLUMN_MISSING' END,
         d.data_type, CAST(NULL AS STRING), d.referenced_table, d.referenced_column
  FROM definition d
  LEFT JOIN live_tables lt ON lower(d.referenced_table)=lt.table_name
  LEFT JOIN live lc ON lower(d.referenced_table)=lc.table_name
                   AND lower(d.referenced_column)=lc.column_name
  WHERE coalesce(d.referenced_table, '') <> ''
    AND coalesce(d.referenced_column, '') <> ''
    AND lc.column_name IS NULL
)
SELECT
  '{RUN_ID}' run_id, '{SOURCE_KIND}' source_kind,
  concat('{BRONZE_SCHEMA}.', table_name) source_table,
  concat('silver.', table_name) target_table,
  drift_type, column_name, expected_type, actual_type,
  referenced_table, referenced_column,
  sha2(concat_ws('||', '{SOURCE_KIND}', table_name, coalesce(column_name, ''),
      drift_type, coalesce(referenced_table, ''), coalesce(referenced_column, '')), 256) drift_key,
  'ACTIVE' status, CAST(1 AS BIGINT) occurrence_count,
  current_timestamp() first_detected_at, current_timestamp() last_detected_at,
  CAST(NULL AS TIMESTAMP) resolved_at, current_timestamp() detected_at,
  '{JOB_RUN_ID}' job_run_id
FROM drifts
""")

# Candidate keeps approved metadata for observed columns. Invalid FK metadata is
# excluded from the candidate and remains visible as an FK_* drift event.
definition = definition_df.alias("d")
live = current_live.alias("l")
targets = current_live.select(
    F.lower("table_name").alias("target_table"),
    F.lower("column_name").alias("target_column"),
).distinct().alias("t")

candidate = (live.join(
        definition,
        (F.lower(F.col("l.table_name")) == F.lower(F.col("d.table_name")))
        & (F.lower(F.col("l.column_name")) == F.lower(F.col("d.column_name"))),
        "left",
    )
    .join(
        targets,
        (F.lower(F.col("d.referenced_table")) == F.col("t.target_table"))
        & (F.lower(F.col("d.referenced_column")) == F.col("t.target_column")),
        "left",
    ))
valid_fk = F.col("d.referenced_table").isNull() | F.col("t.target_column").isNotNull()
candidate = candidate.select(
    F.col("l.table_name").alias("table_name"),
    F.col("l.ordinal_position").cast("string").alias("ordinal_position"),
    F.col("l.column_name").alias("column_name"),
    F.coalesce(F.col("d.data_type"), F.col("l.live_data_type")).alias("data_type"),
    F.coalesce(F.col("d.is_nullable"), F.when(F.col("l.is_nullable"), "YES").otherwise("NO")).alias("is_nullable"),
    F.coalesce(F.col("d.column_default"), F.lit("NULL")).alias("column_default"),
    F.col("d.primary_key_name").alias("primary_key_name"),
    F.coalesce(F.col("d.is_primary_key"), F.lit("NO")).alias("is_primary_key"),
    F.when(valid_fk, F.col("d.foreign_key_name")).alias("foreign_key_name"),
    F.when(valid_fk, F.col("d.referenced_schema")).alias("referenced_schema"),
    F.when(valid_fk, F.col("d.referenced_table")).alias("referenced_table"),
    F.when(valid_fk, F.col("d.referenced_column")).alias("referenced_column"),
    F.col("d.column_description").alias("column_description"),
    F.col("d.table_description").alias("table_description"),
)
(candidate.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_schema_definition_candidate"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

event_table = DeltaTable.forName(spark, "monitoring.cfg_schema_drift_event")
(event_table.alias("target")
    .merge(current_drifts.alias("source"), "target.drift_key = source.drift_key")
    .whenMatchedUpdate(set={
        "run_id": "source.run_id",
        "job_run_id": "source.job_run_id",
        "source_table": "source.source_table",
        "target_table": "source.target_table",
        "expected_type": "source.expected_type",
        "actual_type": "source.actual_type",
        "status": "'ACTIVE'",
        "occurrence_count": "coalesce(target.occurrence_count, 0) + 1",
        "last_detected_at": "source.last_detected_at",
        "resolved_at": "CAST(NULL AS TIMESTAMP)",
        "detected_at": "source.detected_at",
    })
    .whenNotMatchedInsertAll()
    .execute())

active_keys = current_drifts.select("drift_key").distinct()
resolved = (spark.table("monitoring.cfg_schema_drift_event")
    .where((F.col("source_kind") == SOURCE_KIND) & (F.col("status") == "ACTIVE"))
    .join(active_keys, "drift_key", "left_anti")
    .withColumn("status", F.lit("RESOLVED"))
    .withColumn("resolved_at", F.current_timestamp())
    .withColumn("last_detected_at", F.current_timestamp()))
if not resolved.rdd.isEmpty():
    (event_table.alias("target")
        .merge(resolved.alias("source"), "target.drift_key = source.drift_key")
        .whenMatchedUpdate(set={
            "status": "source.status",
            "resolved_at": "source.resolved_at",
            "last_detected_at": "source.last_detected_at",
        })
        .execute())

(current_live.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_bronze_schema_live"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

active = (spark.table("monitoring.cfg_schema_drift_event")
    .where((F.col("source_kind") == SOURCE_KIND) & (F.col("status") == "ACTIVE"))
    .orderBy("drift_type", "source_table", "column_name"))
print(f"Schema drift run {RUN_ID}: {active.count():,} active drift events")
display(active)

print("Candidate definition (same columns as the loaded schema contract):")
display(spark.table("monitoring.cfg_schema_definition_candidate").orderBy("table_name", "ordinal_position"))

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
