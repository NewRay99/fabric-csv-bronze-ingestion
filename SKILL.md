---
name: fabric-csv-bronze-ingestion
description: "Use when ingesting daily CSV extracts from a lakehouse shortcut folder into bronze Delta tables in Microsoft Fabric. Covers programmatic table creation via file listing, type inference rules (text qualifiers for notes/description/comment, date casting, _id to INT), append loading, and Fabric capacity tier limitations."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [fabric, data-lake, lakehouse, bronze, csv, pyspark, delta, medallion, ingestion, shortcuts]
    related_skills: [data-engineering-expert]
---

# Fabric CSV → Bronze Ingestion (Lakehouse Shortcuts)

## Overview

This skill ingests **daily CSV extracts** from a lakehouse shortcut folder into **bronze Delta tables** in Microsoft Fabric. Tables are created programmatically by listing files in the folder — no manual table creation. Type inference rules apply during the read. Load mode is **append** so each daily run stacks new rows.

**Scenario:**
```
Lakehouse Shortcut → Files/Latest/
                        ├── filename1.csv
                        ├── filename2.csv
                        └── filename3.csv
```

Each CSV becomes its own bronze table. New files appearing on subsequent days are picked up automatically.

## When to Use

- Daily CSV extracts land in a Fabric lakehouse shortcut folder
- You need each file auto-discovered and loaded into its own bronze Delta table
- You want type inference (dates, IDs, text qualifiers) applied during ingestion
- Append mode is required (stacking daily data without overwrites)

**Don't use for:**
- Full-refresh / overwrite patterns (change mode to `overwrite` if needed)
- Streaming ingestion (this is batch — use Spark Structured Streaming instead)
- Non-Fabric environments (Databricks ADF pipelines — see `data-engineering-expert`)

## Prerequisites

1. **Microsoft Fabric** workspace with a **Lakehouse** (gen1 or gen2)
2. A **shortcut** in the lakehouse pointing to the ADLS Gen2 container where CSVs land
3. **PySpark** notebook (Fabric provides this — no separate cluster needed)
4. CSVs must have **headers** in the first row

## Fabric Capacity Tier Limitations

The lowest Fabric SKU is **F2** (2 Capacity Units). This severely limits the solution:

| Constraint | F2 (Current) | F64+ (Upgraded) |
|------------|-------------|----------------|
| Spark session concurrency | 1 session at a time | Multiple parallel sessions |
| Execution time | Short timeout (~2 min for small jobs) | Up to 24 hours |
| Autoscale | Not available | Autoscale on/off |
| Max Spark workers | 1-2 nodes | Up to 50+ nodes |
| Storage throughput | Throttled on large files | Full bandwidth |
| Lakehouse shortcut refresh | Manual trigger only | Event-based auto-trigger |
| Data pipeline scheduling | Limited schedule frequency | Full scheduling + event triggers |
| Unity Catalog | Not available | Full governance + lineage |

**Upgrade advice:** Moving to **F8 or F16** gives autoscale and reasonable concurrency. **F64** unlocks full Spark power, Unity Catalog governance, and event-based triggers — the practical minimum for production pipelines.

> Full tier comparison: `references/fabric-tier-comparison.md`

## Solution: PySpark Notebook

### Step 1 — Configure Parameters

```python
# ── Configuration ──────────────────────────────────────────────
SHORTCUT_FOLDER = "Files/Latest"          # Shortcut path in lakehouse
BRONZE_SCHEMA   = "bronze"                # Schema/catalog for bronze tables
TABLE_PREFIX    = "brz_"                 # Prefix for bronze tables
LOAD_MODE       = "append"               # append | overwrite
```

### Step 2 — List CSV Files Programmatically

```python
from notebookutils import mssparkutils
import os

# Resolve the shortcut path
shortcut_path = f"{SHORTCUT_FOLDER}"
file_list = mssparkutils.fs.ls(shortcut_path)

# Filter to .csv files only
csv_files = [f.path for f in file_list if f.name.lower().endswith('.csv')]

print(f"Found {len(csv_files)} CSV file(s):")
for f in csv_files:
    print(f"  -> {f}")
```

### Step 3 — Define Type Inference Rules

```python
from pyspark.sql.functions import col, to_date, regexp_replace

TEXT_QUALIFIER_COLUMNS = {'notes', 'description', 'comment'}

def apply_type_rules(df):
    """Apply type inference rules to a DataFrame."""
    for col_name in df.columns:
        col_lower = col_name.lower()

        # Rule 1: notes/description/comment -> STRING (text qualifier)
        if col_lower in TEXT_QUALIFIER_COLUMNS:
            df = df.withColumn(col_name, col(col_name).cast("string"))

        # Rule 2: columns ending in _id -> INT
        elif col_lower.endswith('_id'):
            df = df.withColumn(col_name,
                regexp_replace(col(col_name), r'[^0-9\-]', '').cast("int"))

        # Rule 3: date columns -> DATE
        elif 'date' in col_lower:
            df = df.withColumn(col_name, to_date(col(col_name)))

    return df
```

### Step 4 — Create Tables and Load (Append)

```python
for csv_path in csv_files:
    # Derive table name from filename
    base_name = os.path.splitext(os.path.basename(csv_path))[0]
    table_name = f"{TABLE_PREFIX}{base_name.lower().replace(' ', '_').replace('-', '_')}"
    full_table = f"{BRONZE_SCHEMA}.{table_name}"

    # Read CSV with header, quote, and schema inference
    df = (spark.read
          .format("csv")
          .option("header", "true")
          .option("inferSchema", "true")
          .option("quote", '"')           # text qualifier
          .option("escape", '"')          # handle embedded quotes
          .option("multiLine", "true")     # newlines inside quoted fields
          .load(csv_path))

    # Apply type rules
    df = apply_type_rules(df)

    # Write to bronze table (append)
    (df.write
       .format("delta")
       .mode(LOAD_MODE)
       .saveAsTable(full_table))

    print(f"OK {csv_path} -> {full_table} ({df.count()} rows)")
```

### Step 5 — Verify

```sql
-- Check all bronze tables exist
SHOW TABLES IN bronze;

-- Row counts per table
SELECT 'brz_filename1' AS tbl, COUNT(*) AS rows FROM bronze.brz_filename1
UNION ALL
SELECT 'brz_filename2', COUNT(*) FROM bronze.brz_filename2;
```

## Common Pitfalls

1. **Duplicate appends on re-runs.** If the notebook runs twice on the same day, rows duplicate. Add an idempotency check: load only files modified today or track loaded filenames in a `_load_log` table.

2. **Schema drift across daily files.** If column names or counts change between days, the append will fail. Use `spark.read.option("mergeSchema", "true")` or enforce a fixed schema.

3. **F2 timeout on large files.** Files over 100MB may timeout on F2. Either split files upstream or upgrade capacity. Workaround: set `spark.conf.set("spark.sql.shuffle.partitions", "50")` to reduce overhead.

4. **Embedded commas in notes/description.** The `quote` + `escape` + `multiLine` options handle this. If CSVs use a different qualifier (e.g., pipe `|`), update the option.

5. **Date format ambiguity.** `to_date()` defaults to `yyyy-MM-dd`. If your CSVs use `dd/MM/yyyy`, specify: `to_date(col(c), "dd/MM/yyyy")`.

6. **_id columns with non-numeric values.** The `regexp_replace` strips non-numeric characters before casting. Nulls appear if the value is purely non-numeric. Check for data quality issues if null counts are high.

## Verification Checklist

- [ ] Shortcut path resolves correctly (`mssparkutils.fs.ls()` returns files)
- [ ] All CSVs discovered (check file count matches expectation)
- [ ] Bronze tables created in the correct schema
- [ ] Text qualifier columns (notes/description/comment) are STRING type
- [ ] `_id` columns are INT type (check for nulls = non-numeric source data)
- [ ] Date columns are DATE type (verify format matches source)
- [ ] Append mode confirmed (row counts increase on re-run with new data)
- [ ] No F2 timeout errors (check Spark UI for stage failures)
- [ ] Daily schedule configured (Fabric Data Pipeline or Power Automate trigger)
