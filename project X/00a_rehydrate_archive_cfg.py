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

# # 00a - Rehydrate archive monitoring controls
#
# Reconstruct the global archive controls from existing archive tables, the
# legacy `archived.cfg_load_control`, and extracted ZIP folders.
#
# An archive table containing row-level `export_date` is already suitable for
# `02a_archive_silver.ipynb`, even when older rows do not contain
# `_archive_source_path`. File-path lineage is used only for exact per-file
# replacement and is not a prerequisite for Silver or Gold replay.

# PARAMETERS CELL ********************

CFG_NOTEBOOK_NAME = "00_setup_cfg"
ARCHIVE_SCHEMA = "archived"
ARCHIVE_ZIP_ROOT = "Files/wmpp-production-data-export-birmingham/archive"
EXTRACT_ROOT = "Files/archive_unzipped"
INCLUDE_LEGACY_CONTROL = True
INCLUDE_LINEAGE_TABLE_SCAN = True
INCLUDE_ZIP_SCAN = True

AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
NOTEBOOK_TIMEOUT_SECONDS = 1800

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import os
import re
import uuid
import zipfile
from datetime import datetime

from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType, IntegerType, LongType, StringType, StructField, StructType,
    TimestampType,
)

RUN_ID = str(uuid.uuid4())


def parse_export_date(value):
    match = re.search(r"(\d{4}-\d{2}-\d{2})", value or "")
    return datetime.strptime(match.group(1), "%Y-%m-%d") if match else None


def merge_frame(target_name, source, condition):
    updates = {column: f"s.`{column}`" for column in source.columns}
    if "reload" in updates:
        updates["reload"] = "coalesce(t.reload, s.reload)"
    (DeltaTable.forName(spark, target_name).alias("t")
        .merge(source.alias("s"), condition)
        .whenMatchedUpdate(set=updates)
        .whenNotMatchedInsertAll()
        .execute())


def qident(value):
    return "`" + str(value).replace("`", "``") + "`"

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
    {"AUDIT_TABLE": AUDIT_TABLE, "TIME_PARSER_POLICY": TIME_PARSER_POLICY},
)
print(f"Configuration setup completed: {cfg_result}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

rehydrated_legacy = 0
legacy_without_export_date = 0
if INCLUDE_LEGACY_CONTROL and spark.catalog.tableExists(f"{ARCHIVE_SCHEMA}.cfg_load_control"):
    legacy = spark.table(f"{ARCHIVE_SCHEMA}.cfg_load_control")
    legacy_without_export_date = legacy.where(
        F.to_timestamp("export_date", "yyyy-MM-dd").isNull()
    ).count()
    source = (legacy
        .withColumn("parsed_export_date", F.to_timestamp("export_date", "yyyy-MM-dd"))
        .where(F.col("parsed_export_date").isNotNull())
        .select(
            F.col("table_path").alias("file_path"),
            F.col("filename"),
            F.col("parsed_export_date").alias("export_date"),
            F.lit(None).cast("string").alias("source_zip"),
            F.concat_ws(".", F.col("schema_name"), F.col("table_name")).alias("target_object"),
            F.lit("SUCCESS").alias("status"),
            F.coalesce(F.col("reload"), F.lit(False)).alias("reload"),
            F.lit(1).cast("int").alias("attempt_count"),
            F.col("load_count").cast("long").alias("rows_read"),
            F.col("load_count").cast("long").alias("rows_written"),
            F.lit(RUN_ID).alias("run_id"),
            F.col("first_load_date").alias("started_at"),
            F.col("last_load_date").alias("ended_at"),
            F.lit(None).cast("string").alias("error_message"),
            F.col("first_load_date").alias("first_loaded_at"),
            F.coalesce(F.col("last_load_date"), F.current_timestamp()).alias("last_updated_at"),
        ))
    rehydrated_legacy = source.count()
    merge_frame(
        "monitoring.cfg_archive_file_load", source,
        "t.file_path = s.file_path AND t.export_date = s.export_date",
    )

print(f"Legacy control rows rehydrated: {rehydrated_legacy:,}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

rehydrated_table_exports = 0
rehydrated_file_lineage = 0
tables_missing_export_date = []
tables_without_file_lineage = []

if INCLUDE_LINEAGE_TABLE_SCAN:
    for table in spark.sql(f"SHOW TABLES IN {qident(ARCHIVE_SCHEMA)}").collect():
        physical_name = table.tableName
        if table.isTemporary or physical_name.lower().startswith("cfg_"):
            continue

        target_object = f"{ARCHIVE_SCHEMA}.{physical_name}"
        frame = spark.table(target_object)
        if "export_date" not in frame.columns:
            tables_missing_export_date.append(target_object)
            continue

        dated = (frame
            .withColumn("_rehydrate_export_date", F.to_timestamp("export_date"))
            .where(F.col("_rehydrate_export_date").isNotNull()))
        table_exports = dated.groupBy("_rehydrate_export_date").agg(
            F.count(F.lit(1)).alias("row_count")
        ).select(
            F.lit(ARCHIVE_SCHEMA).alias("source_schema"),
            F.lit(physical_name).alias("source_table"),
            F.col("_rehydrate_export_date").alias("export_date"),
            F.lit("SUCCESS").alias("status"),
            F.lit(False).alias("reload"),
            F.col("row_count").cast("long"),
            F.lit(RUN_ID).alias("run_id"),
            F.current_timestamp().alias("first_seen_at"),
            F.current_timestamp().alias("last_updated_at"),
            F.lit(None).cast("string").alias("error_message"),
        )
        rehydrated_table_exports += table_exports.count()
        merge_frame(
            "monitoring.cfg_archive_table_export_load",
            table_exports,
            "t.source_schema = s.source_schema AND t.source_table = s.source_table "
            "AND t.export_date = s.export_date",
        )

        if "_archive_source_path" not in frame.columns:
            tables_without_file_lineage.append(target_object)
            continue

        source_zip = (F.first("_archive_source_zip", ignorenulls=True)
            if "_archive_source_zip" in frame.columns
            else F.first(F.lit(None).cast("string"), ignorenulls=True))
        load_timestamp = (F.max("_archive_load_ts")
            if "_archive_load_ts" in frame.columns
            else F.max(F.lit(None).cast("timestamp")))
        grouped = dated.groupBy(
            "_archive_source_path", "_rehydrate_export_date"
        ).agg(
            F.count(F.lit(1)).alias("row_count"),
            source_zip.alias("source_zip"),
            load_timestamp.alias("last_load_ts"),
        )
        file_exports = grouped.select(
            F.col("_archive_source_path").alias("file_path"),
            F.regexp_extract("_archive_source_path", r"([^/]+)$", 1).alias("filename"),
            F.col("_rehydrate_export_date").alias("export_date"),
            F.col("source_zip"),
            F.lit(target_object).alias("target_object"),
            F.lit("SUCCESS").alias("status"),
            F.lit(False).alias("reload"),
            F.lit(1).cast("int").alias("attempt_count"),
            F.col("row_count").cast("long").alias("rows_read"),
            F.col("row_count").cast("long").alias("rows_written"),
            F.lit(RUN_ID).alias("run_id"),
            F.col("last_load_ts").alias("started_at"),
            F.col("last_load_ts").alias("ended_at"),
            F.lit(None).cast("string").alias("error_message"),
            F.col("last_load_ts").alias("first_loaded_at"),
            F.current_timestamp().alias("last_updated_at"),
        )
        rehydrated_file_lineage += file_exports.count()
        merge_frame(
            "monitoring.cfg_archive_file_load", file_exports,
            "t.file_path = s.file_path AND t.export_date = s.export_date",
        )

print(f"Table/export audit rows rehydrated: {rehydrated_table_exports:,}")
print(f"File-lineage audit rows rehydrated: {rehydrated_file_lineage:,}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

rehydrated_zips = 0
if INCLUDE_ZIP_SCAN:
    zip_root_posix = f"/lakehouse/default/{ARCHIVE_ZIP_ROOT}"
    rows = []
    for root, _, files in os.walk(zip_root_posix):
        for file_name in files:
            if not file_name.lower().endswith(".zip"):
                continue
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(full_path, "/lakehouse/default").replace("\\", "/")
            export_date = parse_export_date(file_name) or parse_export_date(relative_path)
            if export_date is None:
                continue
            extract_relative = f"{EXTRACT_ROOT}/{export_date:%Y-%m-%d}"
            extract_posix = f"/lakehouse/default/{extract_relative}"
            if not os.path.isdir(extract_posix):
                continue
            file_count = sum(len(names) for _, _, names in os.walk(extract_posix))
            if file_count == 0:
                continue
            modified = datetime.utcfromtimestamp(os.path.getmtime(full_path))
            rows.append((relative_path, export_date, extract_relative, "SUCCESS", False,
                         1, file_count, RUN_ID, modified, modified, None, modified,
                         datetime.utcnow()))

    if rows:
        schema = "zip_path string,export_date timestamp,extract_path string,status string,reload boolean,attempt_count int,file_count int,run_id string,started_at timestamp,ended_at timestamp,error_message string,first_loaded_at timestamp,last_updated_at timestamp"
        source = spark.createDataFrame(rows, schema)
        rehydrated_zips = source.count()
        merge_frame(
            "monitoring.cfg_archive_zip_load", source,
            "t.zip_path = s.zip_path AND t.export_date = s.export_date",
        )

print(f"ZIP rows rehydrated: {rehydrated_zips:,}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

print("Rehydration reconciliation")
print(f"  table/export audit rows: {rehydrated_table_exports:,}")
print(f"  legacy file audit rows: {rehydrated_legacy:,}")
print(f"  file-lineage audit rows: {rehydrated_file_lineage:,}")
print(f"  ZIP audit rows: {rehydrated_zips:,}")
print(f"  legacy control rows with invalid/missing export_date: {legacy_without_export_date:,}")
print(f"  replay-ready tables without file-path lineage: {len(tables_without_file_lineage):,}")
for table_name in tables_without_file_lineage:
    print(f"    - {table_name}")

if tables_without_file_lineage:
    print(
        "These tables are valid for 02a Silver/Gold replay because export_date "
        "exists. Only exact per-file deletion/replacement is unavailable for "
        "their older rows."
    )

print(f"  tables missing export_date: {len(tables_missing_export_date):,}")
for table_name in tables_missing_export_date:
    print(f"    - {table_name}")
if tables_missing_export_date:
    print(
        "Only the tables listed as missing export_date require correction or "
        "re-ingestion before historical replay."
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
