# %% [markdown]
# # Notebook 1: Bronze Loader — CSV to Delta (Append)
# 
# **Purpose:** Loop through the `Latest/` shortcut folder, read each CSV with
# text qualifiers, and append into bronze Delta tables. Tables are created
# programmatically — one per CSV file.
#
# **Source:** `Files/Latest/*.csv` (lakehouse shortcut to ADLS Gen2)
# **Target:** `bronze.brz_<filename>` (Delta tables in lakehouse)
# **Mode:** Append (stacks daily rows on each run)
#
# **Type inference rules applied during read:**
#   - Columns named `notes`, `description`, `comment` → STRING (text qualifier)
#   - Columns ending in `_id` → STRING (preserve UUID format in bronze)
#   - Date columns (containing "date") → STRING (preserve raw value in bronze)
#
# **Note:** Bronze keeps raw data as-is. Type casting to proper types happens
# in Notebook 2 (Silver Formatter) using the schema_definition.csv spec.

# %% [markdown]
# ## Step 1 — Configuration

# %%
# ── Parameters ─────────────────────────────────────────────────
SHORTCUT_FOLDER  = "Files/Latest"     # Shortcut path in lakehouse
BRONZE_SCHEMA    = "bronze"           # Schema for bronze tables
TABLE_PREFIX     = "brz_"             # Prefix for bronze tables
LOAD_MODE        = "append"           # append | overwrite
TEXT_QUALIFIER   = '"'               # CSV text qualifier character

# Columns that should always be read as STRING (free-text fields)
TEXT_QUALIFIER_COLUMNS = {'notes', 'description', 'comment', 'additional_information',
                          'child_summary_needs', 'location_preference_details',
                          'location_restriction_details', 'approval_details',
                          'pets_details', 'school_transport_details',
                          'family_transport_details', 'restriction_details',
                          'event_message', 'cancel_reason_other_text',
                          'decline_reason_other_text', 'message_text',
                          'outcomes_of_placement', 'expected_destination_other_text',
                          'placement_needs_summary', 'placement_type_other_text',
                          'do_not_send_invoices_note', 'foster_additional_approval_details',
                          'foster_primary_approval_details',
                          'foster_transport_can_provide_for_family_details',
                          'foster_vehicle_details', 'foster_home_pets_details',
                          'review_comments'}

# %% [markdown]
# ## Step 2 — Discover CSV Files

# %%
from notebookutils import mssparkutils
import os

file_list = mssparkutils.fs.ls(SHORTCUT_FOLDER)
csv_files = [f.path for f in file_list if f.name.lower().endswith('.csv')]

print(f"Found {len(csv_files)} CSV file(s) in {SHORTCUT_FOLDER}:")
for f in csv_files:
    print(f"  -> {os.path.basename(f)}")

if not csv_files:
    print("WARNING: No CSV files found. Check shortcut path and folder contents.")
    mssparkutils.notebook.exit("No files found")

# %% [markdown]
# ## Step 3 — Bronze Load Function
# 
# Bronze layer keeps raw data. All columns are read as STRING to preserve
# the original values. Type casting happens in Silver (Notebook 2).

# %%
from pyspark.sql.functions import col, lit, current_timestamp, input_file_name
from pyspark.sql.types import StringType

def load_csv_to_bronze(csv_path, schema_name, table_prefix, load_mode):
    """
    Load a single CSV file into a bronze Delta table.
    
    All columns are forced to STRING type in bronze to preserve raw values.
    Adds _ingestion_timestamp and _source_file metadata columns.
    """
    # Derive table name from filename
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    table_name = f"{table_prefix}{base_name.lower().replace(' ', '_').replace('-', '_')}"
    full_table = f"{schema_name}.{table_name}"
    
    try:
        # Read CSV with text qualifier — all columns as string
        df = (spark.read
              .format("csv")
              .option("header", "true")
              .option("quote", TEXT_QUALIFIER)
              .option("escape", TEXT_QUALIFIER)
              .option("multiLine", "true")
              .option("mode", "PERMISSIVE")    # Bad rows go to _corrupt_record
              .option("columnNameOfCorruptRecord", "_corrupt_record")
              .schema(_infer_all_string_schema(csv_path))  # Force STRING for all
              .load(csv_path))
        
        # Add metadata columns
        df = (df
              .withColumn("_ingestion_timestamp", current_timestamp())
              .withColumn("_source_file", lit(os.path.basename(csv_path))))
        
        # Write to bronze table
        (df.write
           .format("delta")
           .mode(load_mode)
           .option("mergeSchema", "true")   # Allow new columns if schema drifts
           .saveAsTable(full_table))
        
        row_count = df.count()
        col_count = len(df.columns)
        print(f"  OK  {full_table} ({row_count} rows, {col_count} cols)")
        return {"file": csv_path, "table": full_table, "rows": row_count, "cols": col_count, "status": "OK"}
    
    except Exception as e:
        print(f"  ERR {full_table}: {str(e)[:300]}")
        return {"file": csv_path, "table": full_table, "rows": 0, "cols": 0, "status": f"ERROR: {str(e)[:300]}"}


def _infer_all_string_schema(csv_path):
    """Read the CSV header and create a schema where every column is STRING."""
    from pyspark.sql.types import StructType, StructField
    
    # Read just the header
    header_df = (spark.read
                 .format("csv")
                 .option("header", "true")
                 .option("quote", TEXT_QUALIFIER)
                 .option("escape", TEXT_QUALIFIER)
                 .option("multiLine", "true")
                 .load(csv_path))
    
    fields = [StructField(c, StringType(), True) for c in header_df.columns]
    return StructType(fields)

# %% [markdown]
# ## Step 4 — Execute Bronze Load

# %%
print(f"\n{'='*60}")
print(f"BRONZE LOAD — {len(csv_files)} file(s)")
print(f"{'='*60}\n")

results = []
for csv_path in csv_files:
    result = load_csv_to_bronze(csv_path, BRONZE_SCHEMA, TABLE_PREFIX, LOAD_MODE)
    results.append(result)

# %% [markdown]
# ## Step 5 — Summary Report

# %%
print(f"\n{'='*60}")
print("BRONZE LOAD SUMMARY")
print(f"{'='*60}")

total_rows = 0
ok_count = 0
err_count = 0

for r in results:
    status = "OK" if r["status"] == "OK" else "ERR"
    print(f"  [{status}] {r['table']}")
    print(f"        file: {os.path.basename(r['file'])}")
    print(f"        rows: {r['rows']}  cols: {r['cols']}")
    if r["status"] != "OK":
        print(f"        {r['status']}")
        err_count += 1
    else:
        ok_count += 1
    total_rows += r["rows"]

print(f"\n  Files loaded:  {ok_count} OK, {err_count} errors")
print(f"  Total rows:    {total_rows}")
print(f"  Load mode:     {LOAD_MODE}")
print(f"{'='*60}")

# %% [markdown]
# ## Step 6 — Verification

# %%
# List all bronze tables
print("\nBronze tables:")
tables = spark.sql(f"SHOW TABLES IN {BRONZE_SCHEMA}")
display(tables)

# %%
# Row count per table
for r in results:
    if r["status"] == "OK":
        try:
            cnt = spark.sql(f"SELECT COUNT(*) AS cnt FROM {r['table']}").collect()[0]["cnt"]
            print(f"  {r['table']}: {cnt} total rows in Delta table")
        except Exception as e:
            print(f"  {r['table']}: verification failed — {e}")
