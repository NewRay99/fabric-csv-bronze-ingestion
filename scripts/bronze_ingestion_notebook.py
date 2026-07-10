# %% [markdown]
# # Fabric CSV -> Bronze Ingestion (Append)
# 
# **Purpose:** Read all CSVs from a lakehouse shortcut folder, apply type
# inference rules, and load each into its own bronze Delta table (append mode).
#
# **Folder structure expected:**
#   Files/Latest/filename1.csv
#   Files/Latest/filename2.csv
#   Files/Latest/filename3.csv
#
# **Type rules:**
#   - Columns named notes/description/comment -> STRING (text qualifier)
#   - Columns ending in _id -> INT
#   - Columns containing "date" -> DATE
#
# **Load mode:** append (stacks new daily rows)

# %% [markdown]
# ## Step 1 — Configuration

# %%
# ── Parameters (override via Fabric pipeline if needed) ──────────
SHORTCUT_FOLDER = "Files/Latest"     # Shortcut path in lakehouse
BRONZE_SCHEMA   = "bronze"           # Schema for bronze tables
TABLE_PREFIX    = "brz_"             # Prefix for bronze tables
LOAD_MODE       = "append"           # append | overwrite
DATE_FORMAT      = "yyyy-MM-dd"     # Adjust if source uses a different format
TEXT_QUALIFIER   = '"'              # CSV text qualifier character

# Column names that should always be STRING (free-text fields)
TEXT_QUALIFIER_COLUMNS = {'notes', 'description', 'comment'}

# %% [markdown]
# ## Step 2 — Discover CSV Files

# %%
from notebookutils import mssparkutils
import os

file_list = mssparkutils.fs.ls(SHORTCUT_FOLDER)
csv_files = [f.path for f in file_list if f.name.lower().endswith('.csv')]

print(f"Found {len(csv_files)} CSV file(s):")
for f in csv_files:
    print(f"  -> {f}")

if not csv_files:
    print("WARNING: No CSV files found. Check shortcut path and folder contents.")
    mssparkutils.notebook.exit("No files found")

# %% [markdown]
# ## Step 3 — Type Inference Rules

# %%
from pyspark.sql.functions import col, to_date, regexp_replace

def apply_type_rules(df, date_format=DATE_FORMAT):
    """
    Apply type inference rules to a DataFrame:
      1. notes/description/comment -> STRING
      2. *_id columns -> INT (strips non-numeric chars first)
      3. *date* columns -> DATE
    """
    for col_name in df.columns:
        col_lower = col_name.lower()

        # Rule 1: Free-text columns -> STRING
        if col_lower in TEXT_QUALIFIER_COLUMNS:
            df = df.withColumn(col_name, col(col_name).cast("string"))

        # Rule 2: ID columns -> INT
        elif col_lower.endswith('_id'):
            df = df.withColumn(
                col_name,
                regexp_replace(col(col_name), r'[^0-9\-]', '').cast("int")
            )

        # Rule 3: Date columns -> DATE
        elif 'date' in col_lower:
            df = df.withColumn(col_name, to_date(col(col_name), date_format))

    return df

# %% [markdown]
# ## Step 4 — Load Each CSV into Bronze (Append)

# %%
results = []

for csv_path in csv_files:
    # Derive table name: brz_<filename_without_ext>
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    table_name = f"{TABLE_PREFIX}{base_name.lower().replace(' ', '_').replace('-', '_')}"
    full_table = f"{BRONZE_SCHEMA}.{table_name}"

    try:
        # Read CSV with text qualifier and schema inference
        df = (spark.read
              .format("csv")
              .option("header", "true")
              .option("inferSchema", "true")
              .option("quote", TEXT_QUALIFIER)
              .option("escape", TEXT_QUALIFIER)
              .option("multiLine", "true")
              .load(csv_path))

        # Apply type inference rules
        df = apply_type_rules(df)

        # Write to bronze table (append)
        (df.write
           .format("delta")
           .mode(LOAD_MODE)
           .saveAsTable(full_table))

        row_count = df.count()
        col_count = len(df.columns)
        results.append({
            'file': csv_path,
            'table': full_table,
            'rows': row_count,
            'columns': col_count,
            'status': 'OK'
        })
        print(f"OK  {csv_path} -> {full_table} ({row_count} rows, {col_count} cols)")

    except Exception as e:
        results.append({
            'file': csv_path,
            'table': full_table,
            'rows': 0,
            'columns': 0,
            'status': f'ERROR: {str(e)[:200]}'
        })
        print(f"ERR {csv_path} -> {full_table}: {str(e)[:200]}")

# %% [markdown]
# ## Step 5 — Summary Report

# %%
print("\n" + "=" * 70)
print("BRONZE INGESTION SUMMARY")
print("=" * 70)

total_rows = 0
for r in results:
    status_icon = "OK" if r['status'] == 'OK' else "ERR"
    print(f"  [{status_icon}] {r['file']}")
    print(f"        -> {r['table']}  |  {r['rows']} rows  |  {r['columns']} cols")
    if r['status'] != 'OK':
        print(f"        {r['status']}")
    total_rows += r['rows']

print(f"\nTotal rows loaded: {total_rows}")
print(f"Files processed:  {len(results)}")
print("=" * 70)

# %% [markdown]
# ## Step 6 — Verification Queries
# 
# Run these in a new SQL cell to verify the load:

# %%
# Verify tables exist
tables = spark.sql(f"SHOW TABLES IN {BRONZE_SCHEMA}")
display(tables)

# %%
# Row count per table
for r in results:
    if r['status'] == 'OK':
        count_df = spark.sql(f"SELECT COUNT(*) AS cnt FROM {r['table']}")
        actual = count_df.collect()[0]['cnt']
        print(f"  {r['table']}: {actual} total rows (in Delta table)")
