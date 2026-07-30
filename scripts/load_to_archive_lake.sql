# ── Parameters ─────────────────────────────────────────────────
ROOT_PATH = "Files/archive_unzipped"       # Shortcut path in lakehouse. Path to the "archived" folder inside filestore
ARCHIVE_SCHEMA    = "archived"             # Schema for archived tables
TABLE_PREFIX     = "archived_"               # Prefix for brarchivedonze tables
LOAD_MODE        = "append"             # append | overwrite
TEXT_QUALIFIER   = '"'                  # CSV text qualifier character
REBUILD   = 0                           # Rebuild Bronze tables

print(f"ROOT_PATH=[{ROOT_PATH}]")
print(f"BRONZE_SCHEMA=[{ARCHIVE_SCHEMA}]")
print(f"TABLE_PREFIX=[{TABLE_PREFIX}]")
print(f"LOAD_MODE=[{LOAD_MODE}]")
print(f"TEXT_QUALIFIER=[{TEXT_QUALIFIER}]")
print(f"REBUILD=[{REBUILD}]")

script = """create table if not exists archived.cfg_load_control 
(
    filename VARCHAR(500)
    , reload BOOLEAN
    , table_path  VARCHAR(500)
    , schema_name  VARCHAR(500)
    , table_name VARCHAR(500)
    , load_count int
    , export_date varchar(14)
    , first_load_date timestamp
    , last_load_date timestamp
)"""

spark.sql(script)



from pyspark.sql import SparkSession
from notebookutils import mssparkutils
import os

table_count = 0

df_cfg_lc = spark.table("archived.cfg_load_control").where("reload == FALSE")

try:
    folders = mssparkutils.fs.ls(ROOT_PATH)

    for f in folders:
        # inside loop after successful write
        table_count += 1
        folder_name = os.path.basename(f.path.rstrip("/"))

        clean_name = folder_name.split(".")[-2]
        clean_name = f"{ARCHIVE_SCHEMA}.{clean_name}"

        table_path = f"{ROOT_PATH}/{folder_name}"
        file_exists = df_cfg_lc.where(F.col(""==table_path))
        if (file_exists): 
            print(f"😅 Skipping this file:{table_path}")
        else:
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
                    
            # Write to Lakehouse as Delta table
            try:
                df.write.format("delta").mode(LOAD_MODE).option("overwriteSchema", "true").saveAsTable(clean_name)
                
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
