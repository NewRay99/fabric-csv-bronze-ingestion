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

# # Create bronze tables
# 1. Use this notebook to create bronze lake tables.
# 2. Select **Run all** to run the notebook.
# 3. This will overwrite the data in the bronze layer
# 4. When the notebook run is completed, return to your lakehouse and refresh your lake views graph.


# CELL ********************

# ── Parameters ─────────────────────────────────────────────────
ROOT_PATH = "Files/wmpp-production-data-export-birmingham/latest"       # Shortcut path in lakehouse. Path to the "latest" folder inside your shortcut
BRONZE_SCHEMA    = "bronze"             # Schema for bronze tables
TABLE_PREFIX     = ""               # Prefix for bronze tables
LOAD_MODE        = "append"             # append | overwrite
TEXT_QUALIFIER   = '"'                  # CSV text qualifier character
REBUILD   = 0                           # Rebuild Bronze tables

print(f"ROOT_PATH=[{ROOT_PATH}]")
print(f"BRONZE_SCHEMA=[{BRONZE_SCHEMA}]")
print(f"TABLE_PREFIX=[{TABLE_PREFIX}]")
print(f"LOAD_MODE=[{LOAD_MODE}]")
print(f"TEXT_QUALIFIER=[{TEXT_QUALIFIER}]")
print(f"REBUILD=[{REBUILD}]")

# Shared configuration setup
CFG_NOTEBOOK_NAME = "00_setup_cfg"
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.
# Capture parent orchestration before this standalone notebook creates local state.
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

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import uuid
from notebookutils import mssparkutils
import os

table_count = 0
BATCH_ID = str(uuid.uuid4())

try:
    folders = mssparkutils.fs.ls(ROOT_PATH)

    for f in folders:
        folder_name = os.path.basename(f.path.rstrip("/"))
        if is_etl_excluded_table(folder_name):
            print(f"Skipping internal/reference latest file: {folder_name}")
            continue
        table_count += 1

        clean_name = folder_name.split(".")[-2]
        clean_name = f"{BRONZE_SCHEMA}.{clean_name}"

        table_path = f"{ROOT_PATH}/{folder_name}"

        print(f"Processing folder: {folder_name} -> table: {clean_name}")
        if REBUILD==1:
            print(f"\tDropping table: {clean_name}")
            sql_drop= f"DROP TABLE IF EXISTS {clean_name}"
            spark.sql(sql_drop)

        # Try parquet first (most common)
        if folder_name.lower().endswith(".parquet"):
            df = spark.read.format("parquet").load(table_path)
            print(f"\tLoaded parquet for {folder_name}")
        elif folder_name.lower().endswith(".csv"):
            # Try CSV if parquet fails
            try:
                df = (
                        spark.read
                        .format("csv")
                        .option("header", "true")
                        .option("quote", TEXT_QUALIFIER)
                        .option("escape", TEXT_QUALIFIER)
                        .option("multiLine", "true")
                        .load(table_path)
                    )
                print(f"\tLoaded CSV for {folder_name}")
            except Exception as e:
                print(f"FAILED: {folder_name}")
                print(type(e).__name__)
                print(str(e))
                #print(f"Skipping {folder_name}, unsupported format or empty folder")
                continue

        # Keep Bronze string-oriented while carrying lineage and the source export timestamp.
        df = (df.withColumn("_ingestion_timestamp", F.current_timestamp())
                .withColumn("_source_file", F.lit(folder_name))
                .withColumn("_ingestion_id", F.lit(BATCH_ID)))
        if "export_date" not in df.columns:
            df = df.withColumn("export_date", F.current_timestamp().cast("string"))
        else:
            df = df.withColumn("export_date", F.coalesce(F.col("export_date").cast("string"), F.current_timestamp().cast("string")))

        # Write to Lakehouse as Delta table
        try:
            df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(clean_name)
            print(f"\tCreated/updated table: {clean_name}")
        except Exception as e:
            print(f"\tWrite failed for {clean_name}")
            print(str(e))
            raise

except Exception as e:
    print("ERROR TYPE:", type(e).__name__)
    print("ERROR:", str(e))
    raise

print(f"Successfully processed {table_count} tables")
print("All tables processed successfully!")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Add missing table that do not appear in the latest batch

framework_path = "Files/deprecated_wmpp_files/framework.csv"
# extract framework
df = (
                        spark.read
                        .format("csv")
                        .option("header", "true")
                        .option("quote", TEXT_QUALIFIER)
                        .option("escape", TEXT_QUALIFIER)
                        .option("multiLine", "true")
                        .load(framework_path)
                    )

clean_name = f"{BRONZE_SCHEMA}.framework"
df = (df.withColumn("_ingestion_timestamp", F.current_timestamp())
        .withColumn("_source_file", F.lit("framework.csv"))
        .withColumn("_ingestion_id", F.lit(BATCH_ID))
        .withColumn("export_date", F.current_timestamp().cast("string")))


try:
    df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(clean_name)
    print(f"\tCreated/updated table: {clean_name}")
except Exception as e:
    print(f"\tWrite failed for {clean_name}")
    print(str(e))
    raise



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
