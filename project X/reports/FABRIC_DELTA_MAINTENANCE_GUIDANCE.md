# Fabric Delta maintenance guidance for `03_silver_business_rules`

## Decision

Do **not** add `VACUUM`, `OPTIMIZE`, V-Order, Z-Order, liquid clustering, or
extra statistics/index settings to `03_silver_business_rules.py` yet. The
notebook overwrites four small, deterministic derived tables (`age_band`,
`directory_summary_axis`, `fostering_axis`, and
`referral_closure_reason_summary`) and the potentially larger
`referral_enrichment` table. It also writes monitoring results. There is no
file-count, file-size, query-duration, or predicate-selectivity evidence that
the cost of another physical rewrite would be repaid.

The first performance concern in this notebook is its full-table DQ scans and
joins, rather than a missing index. Layout maintenance can reduce input/output
file overhead on a genuinely fragmented, frequently read table; it cannot make
`VACUUM` accelerate those checks or turn a full scan into a selective lookup.

## What each Fabric feature would do here

| Feature | Relevance to this notebook | Recommendation |
| --- | --- | --- |
| `VACUUM` | The overwrite writes leave previous data files unreferenced. `VACUUM` permanently removes only unreferenced files older than retention; it is storage cleanup, not a query-speed optimization. | Keep out of the notebook. If storage accumulation is measured, run a separate scheduled maintenance step against selected high-churn Delta tables. Keep the default seven-day-or-longer retention unless the agreed rollback, audit, time-travel, and concurrent-reader requirements permit less. |
| `OPTIMIZE` / compaction | Can consolidate many small files and improve scan performance. It is appropriate after major ingestion/updates or measured fragmentation. | Consider only for a *large* source Silver table or `silver.referral_enrichment` after health metrics show many small files and the table has material read demand. Do not run after every overwrite of the small derived tables. |
| V-Order | A Parquet write-layout optimization for read-heavy dashboard, interactive, or repeated-scan workloads. Writes are typically slower (Microsoft states about 15% on average). | Consider for a large reporting/Direct Lake table after a read-heavy workload is confirmed. It is not justified for the small axes or simply because the DQ notebook writes Delta. |
| Z-Order | Improves file skipping when queries have selective filters on two or more recurring columns. The notebook's main DQ path counts, groups, and joins whole tables; it does not supply a selective access pattern for this feature. | Do not infer a key from join columns alone. Assess actual report/query predicates first; then use one stable, selective filter combination on a large table if measured scans support it. |
| Liquid clustering | A persistent clustering policy and current alternative to manual Z-Order/partitioning. It applies when `OPTIMIZE` runs. Runtime 2.0+ can be incremental; Runtime 1.3 can rewrite every sub-100-GB Z-Cube on each `OPTIMIZE`. | Do not introduce it for these small outputs. Consider it only for a large, long-lived query target with stable, selective filters, after confirming the Fabric Spark runtime is 2.0+ and choosing it instead of Z-Order. |

## Indexing and statistics

Lakehouse Delta uses file-level statistics and file skipping rather than a
traditional B-tree index added to this notebook. Delta records per-file min,
max, and null-count statistics for indexed columns when files are written.
Fabric collects those statistics for the first 32 columns by default. The
existing tables therefore already have the relevant baseline optimisation.

An additional `delta.dataSkippingStatsColumns` or
`delta.dataSkippingNumIndexedCols` setting is only worth considering when a
large table has frequently filtered columns beyond that coverage. It adds write
overhead for every file, and the notebook's unfiltered DQ counts and full
dataset joins would not benefit. Fabric also maintains extended table/column
statistics automatically for Delta tables, which improve Spark planning for
joins, filters, aggregations, and partition pruning; no repeated manual
statistics collection is needed here.

## Evidence-gated next step

Before changing code or table properties, collect evidence outside the business
rules run:

1. Run `DESCRIBE DETAIL` and `DESCRIBE HISTORY` for the candidate table.
2. For a Lakehouse table read through the SQL analytics endpoint, run
   `sys.sp_get_table_health_metrics` and record `PotentialAnomalyType`, file
   count, average file size, and deleted-row count.
3. Compare representative DQ/report query elapsed time and scan metrics before
   and after a one-table maintenance trial in a quiet window.

Only if the data shows fragmentation or a material read bottleneck should a
separate maintenance workflow be added. Fabric supports scheduling this with a
Lakehouse Maintenance activity, notebook, or REST API. Keep it separate from
the DQ notebook so business validation stays deterministic, the retention
policy is explicit, and maintenance can be monitored independently.

## Source basis

- Microsoft: [Compacting Delta tables](https://learn.microsoft.com/en-us/fabric/data-engineering/table-compaction) — compaction purpose, Z-Order applicability, V-Order sequencing, auto-compaction, write amplification, and maintenance cadence.
- Microsoft: [VACUUM Delta tables](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-lake-vacuum) — permanent deletion, retention, overwrite behaviour, and the fact that `VACUUM` does not itself improve query performance.
- Microsoft: [Lakehouse table maintenance](https://learn.microsoft.com/en-us/fabric/data-engineering/lakehouse-table-maintenance) — scheduling options and the seven-day default/minimum safety behaviour.
- Microsoft: [V-Order](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-optimization-and-v-order) — read-heavy use case and write-time trade-off.
- Microsoft: [Liquid clustering](https://learn.microsoft.com/en-us/fabric/data-engineering/liquid-clustering) — clustering semantics, Runtime 2.0 incremental behavior, and the Runtime 1.3 rewrite caution.
- Microsoft: [File skipping for Delta tables](https://learn.microsoft.com/en-us/fabric/data-engineering/delta-lake-file-skipping) — automatic file statistics, 32-column default, and write-cost trade-off.
- Microsoft: [Automated table statistics](https://learn.microsoft.com/en-us/fabric/data-engineering/automated-table-statistics) — automatic extended statistics and Spark optimizer use.
- Microsoft: [`sys.sp_get_table_health_metrics`](https://learn.microsoft.com/en-us/sql/relational-databases/system-stored-procedures/sp-get-table-health-metrics-transact-sql?view=fabric) — evidence to use before compaction and the SQL endpoint's file-layout thresholds.
