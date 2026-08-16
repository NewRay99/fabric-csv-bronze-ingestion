# %% [markdown]
# # Notebook 2: Silver Formatter — Apply Schema Spec to Bronze Tables
# 
# **Purpose:** Read bronze tables, apply type casting and column transformations
# based on `schema_definition.csv`, and write to silver Delta tables.
# 
# **Source:** `bronze.brz_<table_name>` (raw STRING columns)
# **Target:** `silver.slv_<table_name>` (typed columns per schema spec)
# **Mode:** Overwrite (silver is rebuilt from bronze each run)
# 
# **Schema spec (from schema_definition.csv):**
#   - `uuid` columns → STRING (preserve UUID format)
#   - `integer` columns → INT
#   - `numeric(p,s)` columns → DECIMAL(p,s)
#   - `boolean` columns → BOOLEAN
#   - `date` columns → DATE
#   - `timestamp` columns → TIMESTAMP
#   - `character varying(n)` columns → STRING (with text qualifiers for free-text)
#   - `text` columns → STRING
#   - `jsonb` columns → STRING (JSON text preserved)
#   - `character varying[]` columns → ARRAY<STRING>
# 
# **Additional transformations:**
#   - Columns ending in `_id` → preserve as STRING (UUID format)
#   - Text qualifier columns (notes, description, comment, etc.) → STRING, trimmed
#   - Boolean columns → parse 'true'/'false'/'TRUE'/'FALSE' strings
#   - Add `_bronze_load_ts` lineage column

# %% [markdown]
# ## Step 1 — Configuration

# %%
# ── Parameters ─────────────────────────────────────────────────
BRONZE_SCHEMA     = "bronze"
SILVER_SCHEMA     = "silver"
BRONZE_PREFIX     = "brz_"
SILVER_PREFIX     = "slv_"
LOAD_MODE         = "overwrite"    # Silver rebuilt each run
DATE_FORMAT       = "yyyy-MM-dd"
TIMESTAMP_FORMAT  = "yyyy-MM-dd HH:mm:ss"

# Path to schema definition CSV (loaded as a DataFrame)
SCHEMA_CSV_PATH   = "Files/schema_definition.csv"  # Upload to lakehouse or use shortcut

# %% [markdown]
# ## Step 2 — Load Schema Definition

# %%
from pyspark.sql.functions import col, to_date, to_timestamp, trim, regexp_replace, when, lit, current_timestamp
from pyspark.sql.types import *
import re

# Load schema definition CSV
schema_df = (spark.read
             .format("csv")
             .option("header", "true")
             .option("quote", '"')
             .option("escape", '"')
             .option("multiLine", "true")
             .load(SCHEMA_CSV_PATH))

print(f"Schema definition loaded: {schema_df.count()} column definitions")
print(f"Schemas: {', '.join([r.schema_name for r in schema_df.select('schema_name').distinct().collect()])}")

# Build a lookup: {table_name: [{column_name, data_type, is_nullable, ...}]}
from collections import defaultdict
schema_lookup = defaultdict(list)

for row in schema_df.collect():
    table = row.table_name
    if table:
        schema_lookup[table].append({
            "column_name": row.column_name,
            "data_type": row.data_type or "",
            "is_nullable": row.is_nullable or "YES",
            "is_primary_key": row.is_primary_key == "YES",
            "column_description": row.column_description or "",
        })

print(f"\nTables in schema: {len(schema_lookup)}")
for t, cols in sorted(schema_lookup.items()):
    print(f"  {t}: {len(cols)} columns")

# %% [markdown]
# ## Step 3 — Type Mapping Functions

# %%
# Columns that should always be STRING (free-text / text qualifier columns)
TEXT_QUALIFIER_COLUMNS = {
    'notes', 'description', 'comment', 'additional_information',
    'child_summary_needs', 'location_preference_details',
    'location_restriction_details', 'approval_details',
    'pets_details', 'school_transport_details',
    'family_transport_details', 'restriction_details',
    'event_message', 'cancel_reason_other_text',
    'decline_reason_other_text', 'message_text',
    'outcomes_of_placement', 'expected_destination_other_text',
    'placement_needs_summary', 'placement_type_other_text',
    'schedule_do_not_send_invoices_note',
    'foster_additional_approval_details', 'foster_primary_approval_details',
    'foster_transport_can_provide_for_family_details',
    'foster_vehicle_details', 'foster_home_pets_details',
    'review_comments', 'object_key', 'sic_codes',
    'national_contract_external_link'
}

def map_data_type(pg_type):
    """Map PostgreSQL data type from schema_definition.csv to Spark type."""
    pg_type_lower = pg_type.lower().strip()
    
    # UUID → STRING (preserve format)
    if 'uuid' in pg_type_lower:
        return "string"
    
    # Integer types
    if pg_type_lower in ('integer', 'int', 'int4', 'bigint', 'int8', 'smallint', 'int2'):
        if 'big' in pg_type_lower:
            return "long"
        return "integer"
    
    # Numeric/decimal
    m = re.match(r'numeric\((\d+),\s*(\d+)\)', pg_type_lower)
    if m:
        precision, scale = int(m.group(1)), int(m.group(2))
        return f"decimal({precision},{scale})"
    
    if 'numeric' in pg_type_lower or 'decimal' in pg_type_lower:
        return "decimal(19,2)"
    
    # Boolean
    if 'boolean' in pg_type_lower or 'bool' in pg_type_lower:
        return "boolean"
    
    # Date
    if pg_type_lower == 'date':
        return "date"
    
    # Timestamp
    if 'timestamp' in pg_type_lower:
        return "timestamp"
    
    # Arrays
    if '[]' in pg_type_lower or 'varying[]' in pg_type_lower:
        return "string"  # Store as string, parse in gold if needed
    
    # JSON
    if 'json' in pg_type_lower:
        return "string"
    
    # Text / character varying → STRING
    if 'text' in pg_type_lower or 'character' in pg_type_lower or 'varchar' in pg_type_lower:
        return "string"
    
    # Default → STRING
    return "string"


def apply_type_cast(df, table_name, schema_cols):
    """Apply type casting to a bronze DataFrame based on schema definition."""
    cast_exprs = []
    
    for col_def in schema_cols:
        col_name = col_def["column_name"]
        pg_type = col_def["data_type"]
        col_lower = col_name.lower()
        
        if col_name not in df.columns:
            continue  # Column not in bronze data
        
        spark_type = map_data_type(pg_type)
        
        # Force text qualifier columns to STRING with trim
        if col_lower in TEXT_QUALIFIER_COLUMNS:
            cast_exprs.append(trim(col(col_name)).alias(col_name))
        
        # _id columns → STRING (UUID format)
        elif col_lower.endswith('_id'):
            cast_exprs.append(col(col_name).cast("string").alias(col_name))
        
        # Boolean parsing (handle string 'true'/'false'/'TRUE'/'FALSE')
        elif spark_type == "boolean":
            cast_exprs.append(
                when(col(col_name).isNull(), lit(None))
                .when(lower(col(col_name)).isin("true", "t", "1", "yes"), lit(True))
                .when(lower(col(col_name)).isin("false", "f", "0", "no"), lit(False))
                .otherwise(lit(None))
                .alias(col_name)
            )
        
        # Date casting
        elif spark_type == "date":
            cast_exprs.append(to_date(col(col_name), DATE_FORMAT).alias(col_name))
        
        # Timestamp casting
        elif spark_type == "timestamp":
            cast_exprs.append(to_timestamp(col(col_name), TIMESTAMP_FORMAT).alias(col_name))
        
        # Integer casting (strip non-numeric first)
        elif spark_type == "integer":
            cast_exprs.append(
                regexp_replace(col(col_name), r'[^0-9\-]', '').cast("int").alias(col_name)
            )
        
        # Long (bigint)
        elif spark_type == "long":
            cast_exprs.append(
                regexp_replace(col(col_name), r'[^0-9\-]', '').cast("long").alias(col_name)
            )
        
        # Decimal
        elif spark_type.startswith("decimal"):
            cast_exprs.append(
                regexp_replace(col(col_name), r'[^\d.\-]', '').cast(spark_type).alias(col_name)
            )
        
        # Default: STRING
        else:
            cast_exprs.append(col(col_name).cast("string").alias(col_name))
    
    # Apply all casts
    if cast_exprs:
        df = df.select(*cast_exprs, *[
            col(c) for c in df.columns 
            if c not in [col_def["column_name"] for col_def in schema_cols] 
            and not c.startswith("_")
        ])
    
    # Add lineage column
    df = df.withColumn("_silver_transform_ts", current_timestamp())
    
    return df

# %% [markdown]
# ## Step 4 — Process All Bronze Tables

# %%
# Get all bronze tables
bronze_tables = spark.sql(f"SHOW TABLES IN {BRONZE_SCHEMA}").collect()
bronze_table_names = [r.tableName for r in bronze_tables if r.tableName.startswith(BRONZE_PREFIX)]

print(f"Bronze tables to process: {len(bronze_table_names)}")
for t in bronze_table_names:
    print(f"  -> {t}")

# %% [markdown]
# ## Step 5 — Transform Bronze → Silver

# %%
results = []

for btable in bronze_table_names:
    # Derive the base table name (strip prefix)
    base_name = btable.replace(BRONZE_PREFIX, "")
    stable_name = f"{SILVER_PREFIX}{base_name}"
    full_silver = f"{SILVER_SCHEMA}.{stable_name}"
    full_bronze = f"{BRONZE_SCHEMA}.{btable}"
    
    try:
        # Read bronze table
        df = spark.table(full_bronze)
        
        # Find matching schema definition
        # Try exact match, then partial match
        schema_cols = schema_lookup.get(base_name, [])
        
        if not schema_cols:
            # Try without underscores / variations
            for sname, scols in schema_lookup.items():
                if sname.replace('_', '') == base_name.replace('_', ''):
                    schema_cols = scols
                    break
        
        if schema_cols:
            df = apply_type_cast(df, base_name, schema_cols)
            print(f"  OK  {full_bronze} -> {full_silver} (schema applied: {len(schema_cols)} cols)")
        else:
            # No schema spec — pass through as-is (strip metadata cols)
            print(f"  WARN {full_bronze} -> {full_silver} (no schema spec, passthrough)")
        
        # Write to silver
        (df.write
           .format("delta")
           .mode(LOAD_MODE)
           .option("overwriteSchema", "true")
           .saveAsTable(full_silver))
        
        row_count = df.count()
        results.append({"bronze": full_bronze, "silver": full_silver, "rows": row_count, "status": "OK"})
    
    except Exception as e:
        print(f"  ERR {full_bronze} -> {full_silver}: {str(e)[:300]}")
        results.append({"bronze": full_bronze, "silver": full_silver, "rows": 0, "status": f"ERROR: {str(e)[:300]}"})

# %% [markdown]
# ## Step 6 — Summary Report

# %%
print(f"\n{'='*60}")
print("SILVER TRANSFORM SUMMARY")
print(f"{'='*60}")

total_rows = 0
ok_count = 0
err_count = 0

for r in results:
    status = "OK" if r["status"] == "OK" else "ERR"
    print(f"  [{status}] {r['silver']} ({r['rows']} rows)")
    if r["status"] != "OK":
        print(f"        {r['status']}")
        err_count += 1
    else:
        ok_count += 1
    total_rows += r["rows"]

print(f"\n  Tables processed: {ok_count} OK, {err_count} errors")
print(f"  Total rows:       {total_rows}")
print(f"  Load mode:        {LOAD_MODE}")
print(f"{'='*60}")

# %% [markdown]
# ## Step 7 — Verification

# %%
print("\nSilver tables:")
spark.sql(f"SHOW TABLES IN {SILVER_SCHEMA}").show(50, truncate=False)

# %%
# Verify a sample table's schema
if results:
    sample = results[0]
    print(f"\nSchema for {sample['silver']}:")
    spark.sql(f"DESCRIBE {sample['silver']}").show(50, truncate=False)
