# Fabric CSV → Bronze Ingestion

A reusable skill for ingesting **daily CSV extracts** from a Microsoft Fabric lakehouse shortcut folder into **bronze Delta tables** — programmatically, with type inference and append loading.

## What It Does

- **Auto-discovers** all `.csv` files in a lakehouse shortcut folder (`Files/Latest/`)
- **Creates bronze tables programmatically** — no manual DDL
- **Type inference rules** applied during read:
  - Columns named `notes`, `description`, `comment` → **STRING** (with text qualifier)
  - Columns ending in `_id` → **INT**
  - Columns containing `date` → **DATE**
- **Append mode** — stacks new daily rows without overwriting
- **Fabric tier guidance** — what works on F2 (lowest) and what you gain by upgrading

## Scenario

```
Lakehouse Shortcut → Files/Latest/
                        ├── filename1.csv  →  bronze.brz_filename1 (Delta)
                        ├── filename2.csv  →  bronze.brz_filename2 (Delta)
                        └── filename3.csv  →  bronze.brz_filename3 (Delta)
```

New files appearing on subsequent days are picked up automatically on the next run.

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Main skill — concise instructions, type rules, code, pitfalls, checklist |
| `scripts/bronze_ingestion_notebook.py` | Full PySpark notebook (Fabric-ready, cell-delimited) |
| `references/fabric-tier-comparison.md` | F2 → F64+ tier comparison with upgrade advice and cost tips |

## Quick Start

1. Open a **PySpark notebook** in your Fabric workspace
2. Copy the code from `scripts/bronze_ingestion_notebook.py` (or reference `SKILL.md` for the inline version)
3. Update the configuration cell:
   ```python
   SHORTCUT_FOLDER = "Files/Latest"   # your shortcut path
   BRONZE_SCHEMA   = "bronze"
   TABLE_PREFIX    = "brz_"
   LOAD_MODE       = "append"
   ```
4. Run the notebook — all CSVs are discovered, typed, and loaded into bronze Delta tables

## Fabric Tier Notes

The lowest tier (**F2**, 2 Capacity Units) works for small files but is impeded:

- ❌ 1 concurrent Spark session
- ❌ Short execution timeout (~2 min)
- ❌ No autoscale
- ❌ No event-based triggers
- ❌ No Unity Catalog

Upgrading to **F64** unlocks full Spark power, governance, and event triggers — the practical minimum for production. See `references/fabric-tier-comparison.md` for the full breakdown.

## Related Skills

- `data-engineering-expert` — broader Azure Data Factory + Databricks medallion architecture patterns

## License

MIT
