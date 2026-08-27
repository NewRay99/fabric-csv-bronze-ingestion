# Mission Control dashboard overview and KPI logic

## Purpose

Mission Control is the operational Power BI report for the WMPP data platform.
It shows whether the live and archive pipelines ran, completed successfully,
processed the expected tables and batches, and produced data-quality,
schema-contract and referential-integrity exceptions. It is not a referral or
placement performance dashboard.

Use this overview with the [Mission Control semantic model DAX build guide](MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md) and the wireframe at
`reports/mission-control/index.html`.

## Reporting model and scope

The report uses `monitoring` views and configuration tables. `Job Run` is the
hub, joined one-to-many by `job_run_id` to operational evidence. This gives one
filter context for a selected job run while preserving the detail in job steps,
quality results, drift events, load metrics and referential exceptions.

| Reporting area | Main source | Key outcome |
| --- | --- | --- |
| Job execution | `monitoring.vw_job_run_summary` | Run status, timing and pipeline identity |
| Notebook timing | `monitoring.vw_job_step_timing` | Failed, slow and stalled child steps |
| Table processing | `monitoring.cfg_table_load_metric` | Tables processed and rows read/written |
| Archive control | `monitoring.cfg_archive_zip_load`, `cfg_archive_file_load`, `cfg_month_end_gold_run` | Batch, reload and snapshot-replay status |
| Data quality | `monitoring.vw_job_data_quality` | Rule failures, failed rows and rejected keys |
| Schema and RI | `monitoring.vw_job_schema_drift`, `cfg_referential_exception` | Active contract drift and broken relationships |
| Data domain | `monitoring.cfg_data_domain` | Latest low-cardinality lookup/domain profile |

## Pages and required filters

| Page | Primary question | Mandatory filter | Primary KPIs |
| --- | --- | --- | --- |
| Executive overview | Is the platform healthy today? | None; use a report date slicer | Job Runs, Job Success Rate, Failed Job Runs, DQ Failed Checks, Active Drift Events |
| Live ETL | Did the live pipeline complete and process its tables? | `pipeline_name = "90_run_live_pipeline"` | Live Pipeline Job Runs, Live Pipeline Failed Jobs, Average Job Duration, Rows Written |
| Archive ETL | Did historical batches, files and Gold snapshots complete? | `pipeline_name = "90_run_archive_pipeline"` | Archive Pipeline Job Runs, Archive File Failures, Archive Files Awaiting Reload, Gold Snapshots Awaiting Replay |
| Job-step performance | Which notebook step failed, ran slowly or had a gap? | Inherit the selected pipeline/job run | Failed Job Steps, Average Step Duration, Slow Steps Over 30 Minutes, Maximum Step Gap |
| Data quality | Which rules failed and how materially? | Inherit the selected pipeline/job run | DQ Failure Rate, Weighted DQ Failure Percentage, Critical Rules Failing, Rejected Keys |
| Schema and referential integrity | Has the contract changed or a relationship broken? | Inherit the selected pipeline/job run | Active Drift Events, Type Mismatch Events, Referential Exceptions, RI Failure Rate |
| Data domains | What controlled values were observed in the latest profile? | Latest profile timestamp; optional schema/table/column slicers | Profiled Domain Columns, Domain Values, New Domain Values Since Previous Profile |

## KPI logic

| KPI | Calculation principle | Interpretation |
| --- | --- | --- |
| Job Runs | Distinct `job_run_id` | The count of orchestration-level runs, not individual notebook calls. |
| Job Success Rate | Successful Job Runs / Job Runs | Percentage of completed runs with `SUCCESS` status. |
| Failed Job Runs | Status is `FAILED` or `ERROR` | Needs drillthrough to the job and failed step/error detail. |
| Average / P95 Job Duration | Average or 95th percentile of `job_duration_seconds` / 60 | Shows normal elapsed time and the slower tail in minutes. |
| Failed Job Steps | Job-step status is `FAILED` or `ERROR` | Identifies child-notebook failure, separate from job-level outcome. |
| Slow Steps Over 30 Minutes | Step duration exceeds 1,800 seconds | A fixed operational attention threshold. |
| Rows Read / Written | Sum of table-load metrics | Processing volume; it is not a true database insert/update/delete audit. |
| Rows per Minute | Rows Written / Average Job Duration | High-level throughput indicator for the current filter context. |
| Archive Files Awaiting Reload | Archive file `reload = TRUE()` | Identifies archive extracts selected for reprocessing. |
| Gold Snapshots Awaiting Replay | Month-end Gold run `reload = TRUE()` | Identifies requested snapshot rebuilds. |
| DQ Failure Rate | Failed/error checks / evaluated checks | Rule-level failure rate, not the percentage of rows failed. |
| Weighted DQ Failure Percentage | Failed rows / checked rows | Row-weighted impact of data-quality failures. |
| Critical Rules Failing | Distinct critical rule IDs with failure/error | Escalation indicator for severe validation failures. |
| Active Drift Events | Distinct active drift keys | Unresolved schema-contract differences. |
| RI Failure Rate | Referential exceptions / RI checked rows | Estimated broken-reference rate, subject to the configured RI check coverage. |
| New Domain Values Since Previous Profile | Current domain keys minus preceding profile keys | Newly observed controlled lookup/domain values. |

## Visual and drillthrough guidance

- Use KPI cards for current health: run success rate, failed jobs, failed DQ
  checks and active drift events.
- Use a run timeline/status matrix for Jobs, then drill through by `job_run_id`
  to show its child notebook timings, failures, DQ results and load metrics.
- Use a duration trend and a table of the slowest job steps for performance.
- Use separate archived-batch visuals for export date, snapshot date and reload
  status; do not combine them with Live ETL metrics.
- Use exception tables for failed DQ rules, active schema drift and referential
  exceptions. Include rule ID, severity, source/target object and error detail.
- Use a matrix or searchable table for data domains, sliced by source schema,
  table and column. The source notebook intentionally excludes unsuitable
  high-cardinality and personally identifiable fields.

## Important limitations

The current monitoring model does not capture a full table and column
lifecycle history or true inserted, updated and deleted row counts. Do not
derive those measures from overwrite/snapshot row counts. Report this boundary
explicitly until the ETL emits dedicated lifecycle and DML audit events.
