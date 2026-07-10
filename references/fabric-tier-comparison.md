# Fabric Capacity Tier Comparison

## Overview

Microsoft Fabric capacities are purchased as **F-SKUs** (P-SKUs for Power BI Premium — equivalent). The SKU determines how much compute is available for Spark, SQL endpoints, data pipelines, and other workloads.

This reference explains what works and what breaks at the lowest tier, and what you gain by upgrading.

## Current Tier: F2 (2 Capacity Units)

### What Works

- **Small CSV ingestion** (< 50MB per file, < 5 files per run)
- **Simple PySpark notebooks** with short execution time
- **Lakehouse shortcuts** to ADLS Gen2 (read-only)
- **Delta Lake** table creation and append
- **Basic SQL queries** via the Lakehouse SQL endpoint

### What Breaks / Is Impeded

| Limitation | Impact on This Solution |
|-----------|------------------------|
| **1 concurrent Spark session** | Cannot run ingestion and ad-hoc queries simultaneously. Other users are blocked while your notebook runs. |
| **Short execution timeout** | Large files (>100MB) or many files (>10) may timeout mid-load. Partial appends create incomplete data. |
| **No autoscale** | Spark runs with fixed small cluster. Slow on wide DataFrames. No dynamic scaling to handle data skew. |
| **No event-based triggers** | Cannot trigger the pipeline when new CSVs arrive. Must use scheduled triggers only. |
| **Throttled storage throughput** | ADLS Gen2 reads are throttled. Large files take disproportionately long. |
| **No Unity Catalog** | Tables live in the lakehouse default schema only. No cross-workspace governance, lineage, or column-level security. |
| **Limited pipeline scheduling** | Data Pipeline triggers have minimum 15-minute intervals and limited concurrency. |
| **No V-ordering / Z-ordering** | Delta optimization features may timeout on F2. Tables are not optimized for query performance. |

### Workarounds for F2

```python
# Reduce shuffle partitions (less memory pressure)
spark.conf.set("spark.sql.shuffle.partitions", "50")

# Use smaller batch reads
spark.conf.set("spark.sql.files.maxPartitionBytes", "32MB")

# Disable adaptive query execution overhead for small datasets
spark.conf.set("spark.sql.adaptive.enabled", "false")
```

## Upgrade Path

### F8 (8 CU) — ~$0.54/hr

- **Autoscale** available (Spark clusters can scale up/down)
- Slightly longer execution timeout
- 1-2 concurrent sessions (better for dev/test)
- Good for **development** environments

### F16 (16 CU) — ~$1.08/hr

- Autoscale with more headroom
- Multiple concurrent Spark sessions
- Can handle 50+ CSV files per run
- Reasonable for **small production** workloads
- Still no Unity Catalog

### F64 (64 CU) — ~$4.32/hr

- **Full Spark power** — large clusters, long-running jobs
- **Unity Catalog** — governance, lineage, column-level security
- **Event-based triggers** — pipeline fires when new files land in ADLS Gen2
- **Multiple concurrent users** — no blocking
- **V-ordering and Z-ordering** — optimized Delta tables
- **Practical minimum for production** data engineering

### F128 — F2048

- Enterprise scale
- Reserved capacity discounts available
- Multi-workspace isolation
- Suitable for **mission-critical** pipelines

## Cost Optimization Tips

1. **Start/stop capacity** — Pause F2 capacity outside business hours. Pausing stops billing (you pay only for storage). Resume before scheduled pipeline runs.

2. **Use Data Pipeline (not notebook) for simple copies** — If you only need to copy CSVs to Delta without type inference, use a Fabric Data Pipeline Copy activity. It's cheaper than spinning up Spark.

3. **Batch file processing** — Process all CSVs in a single notebook run rather than separate runs. F2's session startup time (~30s) is amortized.

4. **Reserved capacity** — 1-year or 3-year reservations reduce cost by 20-40%.

5. **Separate dev and prod capacities** — Use F2 for dev, F64+ for prod. Don't run both on the same capacity.

## Summary Recommendation

| Scenario | Minimum SKU | Notes |
|----------|------------|-------|
| Dev / testing | F2 | Works for small files, expect timeouts |
| Small production (< 10 files/day) | F16 | Autoscale + reasonable concurrency |
| Production (daily schedule) | F64 | Full features, governance, reliability |
| Enterprise (multiple pipelines) | F128+ | Reserved capacity recommended |
