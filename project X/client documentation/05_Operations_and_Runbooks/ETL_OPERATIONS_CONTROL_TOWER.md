# ETL Operations Control Tower

This guide defines the metadata available for an **ETL Operations Control
Tower** report: a run-operations report for Fabric pipelines, batches,
tables, data quality and schema drift. It is deliberately more descriptive
than “Mission Control”, while still being suitable as the report title.

## What this report can answer today

| Question | Recommended source | Key fields |
| --- | --- | --- |
| When did a pipeline run and did it pass? | `monitoring.vw_job_run_summary` | `job_run_id`, `pipeline_name`, `started_at`, `ended_at`, `status`, `job_duration_seconds`, `steps_succeeded`, `steps_failed` |
| How long did each notebook take? | `monitoring.vw_job_step_timing` | `job_run_id`, `notebook_name`, `status`, `started_at`, `ended_at`, `step_duration_seconds`, `error_message` |
| How many Silver targets ran and how many rows were read/written? | `monitoring.vw_job_step_summary` or `monitoring.cfg_table_load_metric` | `target_count`, `rows_read`, `rows_written`, `duplicate_rows`, `null_primary_keys` |
| What archive ZIP/file batch was processed? | `monitoring.cfg_archive_zip_load`, `monitoring.cfg_archive_file_load` | `zip_path`/`file_path`, `export_date`, `source_zip`, `target_object`, row counts, attempt, timestamps, status |
| What source-to-Silver and Silver-to-Gold relationships were involved? | `monitoring.vw_job_layer_lineage` | `job_run_id`, source/target layer and object, lineage stage, status, observed time |
| Did a source or contract column drift? | `monitoring.vw_job_schema_drift` | source/target table, `drift_type`, `column_name`, expected/actual type, first/last detected, status |
| What DQ checks failed? | `monitoring.vw_job_data_quality` | rule, source table/column, severity, failure count and percentage, sample/rejection counts |

All runner and child activity is correlated by `job_run_id`. Use it as the
primary relationship in the semantic model; `run_id` identifies an individual
notebook execution within that job.

## Where tables and columns are created or changed

| Layer | Physical object writer | Schema/column authority | Monitoring evidence |
| --- | --- | --- | --- |
| Bronze | `01_bronze_get_latest` creates/replaces `bronze.<source_table>` | Incoming source file/schema | `01a_cfg_schema_capture_live` captures current source columns in `monitoring.cfg_bronze_schema_live` |
| Archive | `00_archive_load` creates/appends `archived.<source_table>` | Archive file columns plus loader-owned lineage fields | `cfg_archive_file_load`, `cfg_archive_zip_load`; `01a_cfg_schema_capture_archive` captures columns in `monitoring.cfg_archived_schema_live` |
| Silver | `02_silver_formatter` (live) and `02a_archive_silver` (archive) create/replace `silver.<contract_table>` | `configuration/schema_definition.csv`, deployed to `monitoring.cfg_schema_contract_column` | `cfg_silver_export_load`, `cfg_table_load_metric`, `cfg_schema_drift_event` |
| Derived Silver | `03_silver_business_rules` creates/replaces derived `silver.*` relations | Notebook transformation logic and DQ rules | `cfg_pipeline_run`, `cfg_data_quality_result`, `cfg_schema_drift_event` where applicable |
| Gold facts/snapshots | `04_gold_model` creates/replaces Gold views and the referral snapshot Delta table | Gold notebook SQL and `monitoring.cfg_gold_lineage_mapping` | job/step monitoring and `vw_job_layer_lineage` |
| Gold dimensions/bridges | `05_gold_dimensions` creates/replaces `gold.dim_*` and `gold.bridge_*` | Gold notebook projection and required-column checks | job/step monitoring and `vw_job_layer_lineage` |

`monitoring.cfg_schema_contract_column` is the active runtime contract. A
change in the repository CSV does not change a populated runtime contract
until `00_setup_cfg` is run with `LOAD_FILE_CONFIG=True`. `AR-GL-01` exposed
why this distinction matters: the archive source had `framework_name`, while
the runtime framework contract did not, so Silver wrote an incomplete target.
Archive Silver now supplements the mandatory framework schema, logs
`MISSING_REQUIRED_CONTRACT_COLUMN` in `cfg_schema_drift_event`, and refreshes
the target on its next snapshot replay.

## Important current limits

The current monitoring model does **not** record a durable DDL event for
“table created”, “column added”, “column removed”, or “column type changed”.
It records source/contract observations and run outcomes instead. Do not infer
an exact physical table creation time from a successful load; that only proves
the table existed or was written at that time.

Likewise, the pipeline uses snapshot replacement for many archive/Silver
writes. `rows_written` is the resulting write count, not a SQL `INSERT`
count. There is currently no authoritative monitoring field for per-table
`inserted_rows`, `updated_rows`, or `deleted_rows`; Gold writes are also not
emitted to `cfg_table_load_metric`. The Operations Control Tower should label
these as **not captured** rather than deriving misleading DML figures.

For a future enhancement, introduce `monitoring.cfg_table_lifecycle_event`
with `event_type` (`CREATED`, `COLUMN_ADDED`, `COLUMN_REMOVED`,
`COLUMN_TYPE_CHANGED`), layer, table, column, before/after type, `run_id`,
`job_run_id` and event timestamp. Add a Delta-change-data-feed or merge
metric where true insert/update/delete counts are required.

## Starter report queries

```sql
-- Pipeline health and duration
SELECT *
FROM monitoring.vw_job_run_summary
ORDER BY started_at DESC;

-- Notebook timings and failures for one selected job
SELECT job_run_id, step_sequence, notebook_name, status,
       started_at, ended_at, step_duration_seconds, error_message
FROM monitoring.vw_job_step_timing
WHERE job_run_id = '<job_run_id>'
ORDER BY step_sequence;

-- Silver table throughput and data-quality indicators
SELECT job_run_id, target_object,
       SUM(rows_read) AS rows_read,
       SUM(rows_written) AS rows_written,
       SUM(duplicate_key_count) AS duplicate_rows,
       SUM(null_primary_key_count) AS null_primary_keys
FROM monitoring.cfg_table_load_metric
GROUP BY job_run_id, target_object;

-- Active schema issues requiring attention
SELECT *
FROM monitoring.vw_job_schema_drift
WHERE status = 'ACTIVE'
ORDER BY last_detected_at DESC;
```

## Recommended report pages

1. **Run health** — latest jobs, pass/fail, duration, tables succeeded/failed,
   rows read/written, and direct links to the failed notebook error.
2. **Batch and table throughput** — archive ZIP/file date, source-to-target
   lineage, target count, row counts, duplicates and null-key counts.
3. **Schema and contract watch** — active drift by table/column, contract
   reload date, unresolved issues and first/last detection date.
4. **Data quality** — failures by severity, source table, rule and rejected
   key count.
5. **Coverage and limitations** — display unavailable DDL/DML metrics as
   explicit gaps until lifecycle and change-count instrumentation is added.
