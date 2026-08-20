
from delta.tables import DeltaTable

# 1. Create the single-row logging DataFrame for the current file
log_data = [(
    file_name,
    False,
    relative_path,
    ARCHIVE_SCHEMA,
    clean_table_name,
    row_count,
    export_date,
    now, # first_load_date
    now  # last_load_date
)]

log_df = spark.createDataFrame(log_data, log_schema)

# 2. Load the Delta table reference
control_delta_table = DeltaTable.forName(spark, f"{ARCHIVE_SCHEMA}.cfg_load_control")

# 3. Perform the Upsert (Merge)
control_delta_table.alias("target") \
    .merge(
        log_df.alias("source"),
        "target.table_path = source.table_path"
    ) \
    .whenMatchedUpdate(set = {
        # Update existing record: add new row_count to previous total
        "load_count": "target.load_count + source.load_count",
        "last_load_date": "source.last_last_load_date" if "source.last_last_load_date" in log_df.columns else "source.last_load_date"
    }) \
    .whenNotMatchedInsertAll() \
    .execute()

print(f"\t📝 Logged metadata to {ARCHIVE_SCHEMA}.cfg_load_control")




import os
from datetime import datetime
from pyspark.sql.types import StructType, StructField, StringType, BooleanType, IntegerType, TimestampType

# ── 1. Parameters ─────────────────────────────────────────────────────────────
ROOT_PATH        = "Files/archive_unzipped"      # Relative path inside Lakehouse
POSIX_ROOT_PATH  = f"/lakehouse/default/{ROOT_PATH}"
ARCHIVE_SCHEMA   = "archived"
TABLE_PREFIX     = "archived_"                  # Prefix for bronze tables
LOAD_MODE        = "append"                     # append | overwrite
TEXT_QUALIFIER   = '"'
REBUILD          = 0                            # Set to 1 to drop & rebuild tables

print(f"ROOT_PATH=[{ROOT_PATH}]")
print(f"ARCHIVE_SCHEMA=[{ARCHIVE_SCHEMA}]")
print(f"TABLE_PREFIX=[{TABLE_PREFIX}]")
print(f"LOAD_MODE=[{LOAD_MODE}]")
print(f"REBUILD=[{REBUILD}]")

# ── 2. Create Schema & Control Table ──────────────────────────────────────────
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {ARCHIVE_SCHEMA}")

spark.sql(f"""
CREATE TABLE IF NOT EXISTS {ARCHIVE_SCHEMA}.cfg_load_control
(
    filename STRING,
    reload BOOLEAN,
    table_path STRING,
    schema_name STRING,
    table_name STRING,
    load_count INT,
    export_date STRING,
    first_load_date TIMESTAMP,
    last_load_date TIMESTAMP
)
""")

# ── 3. Load Previously Logged Paths into Memory ────────────────────────────────
loaded_df = spark.table(f"{ARCHIVE_SCHEMA}.cfg_load_control").where("reload = false").select("table_path")
loaded_paths = set(row["table_path"] for row in loaded_df.collect())

print(f"Found {len(loaded_paths)} previously logged file path(s) in control table.\n")

# ── 4. Recursively Process All Files Across All Date Folders ──────────────────
processed_count = 0
skipped_count = 0

for root, dirs, files in os.walk(POSIX_ROOT_PATH):
    for file_name in files:
        # Only target CSV or Parquet files
        if not (file_name.lower().endswith('.csv') or file_name.lower().endswith('.parquet')):
            continue

        # Paths
        full_posix_path = os.path.join(root, file_name)
        relative_path = os.path.relpath(full_posix_path, "/lakehouse/default")

        # Check control table for skip
        if relative_path in loaded_paths:
            print(f"⏩ Skipped (already logged): {relative_path}")
            skipped_count += 1
            continue

        # Extract target table name (e.g. ProviderHome.csv -> archived.archived_ProviderHome)
        raw_entity_name = os.path.splitext(file_name)[0]
        clean_table_name = f"{TABLE_PREFIX}{raw_entity_name}"
        full_table_target = f"{ARCHIVE_SCHEMA}.{clean_table_name}"

        print(f"\n🔄 Processing: {relative_path}")
        print(f"   └── Target Table: {full_table_target}")

        # Drop table if REBUILD flag is active
        if REBUILD == 1:
            print(f"\t🔥 REBUILD=1: Dropping table {full_table_target}")
            spark.sql(f"DROP TABLE IF EXISTS {full_table_target}")

        # Load file into DataFrame
        try:
            if file_name.lower().endswith('.parquet'):
                df = spark.read.format("parquet").load(relative_path)
            elif file_name.lower().endswith('.csv'):
                df = (
                    spark.read
                    .format("csv")
                    .option("header", "true")
                    .option("inferSchema", "true")
                    .option("quote", TEXT_QUALIFIER)
                    .option("escape", TEXT_QUALIFIER)
                    .option("multiLine", "true")
                    .load(relative_path)
                )

            row_count = df.count()
            print(f"\tLoaded {row_count:,} rows.")

            # Write DataFrame into Lakehouse Delta table
            df.write.format("delta") \
                .mode(LOAD_MODE) \
                .option("mergeSchema", "true") \
                .saveAsTable(full_table_target)

            print(f"\t✅ Written to {full_table_target}")

            # Extract parent folder name as export date (e.g. '2026-07-01')
            parent_folder = os.path.basename(root)
            export_date = parent_folder if parent_folder != "archive_unzipped" else ""
            now = datetime.now()

            # Append metadata record to control table
            log_schema = StructType([
                StructField("filename", StringType(), True),
                StructField("reload", BooleanType(), True),
                StructField("table_path", StringType(), True),
                StructField("schema_name", StringType(), True),
                StructField("table_name", StringType(), True),
                StructField("load_count", IntegerType(), True),
                StructField("export_date", StringType(), True),
                StructField("first_load_date", TimestampType(), True),
                StructField("last_load_date", TimestampType(), True)
            ])

            log_data = [(
                file_name,
                False,
                relative_path,
                ARCHIVE_SCHEMA,
                clean_table_name,
                row_count,
                export_date,
                now,
                now
            )]

            log_df = spark.createDataFrame(log_data, log_schema)
            log_df.write.format("delta").mode("append").saveAsTable(f"{ARCHIVE_SCHEMA}.cfg_load_control")

            # Memory update to prevent duplicate work in current run
            loaded_paths.add(relative_path)
            processed_count += 1

        except Exception as e:
            print(f"❌ FAILED to process {file_name}: {str(e)}")
            raise e

print(f"\n🎉 Completed! Total files processed: {processed_count} | Skipped: {skipped_count}")
