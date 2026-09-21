# Mission Control semantic model DAX build guide

## Purpose

This guide defines the operational measures and job-to-step interaction for the
WMPP Mission Control model. They use monitoring control and reporting tables,
rather than referral, offer or placement facts.

## Job-run and step alignment — 21 September 2026

The repaired package
`reports/client-deliverables/SM WMPP Mission Control - SEM-02 repaired.zip`
was inspected against the interaction described by
`reports/mission-control/index.html`. The repaired model opened without the
SEM-02 automatic-date-table error, but it could not implement the Job steps &
errors experience because it contained neither a top-level job table nor a
job-step table and had no `job_run_id` relationship.

The aligned deliverable adds:

- `rpt_job_run_summary`, one row per orchestrated job run;
- `rpt_job_step_timing`, one row per notebook step in a job;
- an active, single-direction one-to-many relationship from
  `rpt_job_run_summary[job_run_id]` to
  `rpt_job_step_timing[job_run_id]`;
- `cfg_pipeline_run[job_run_id]` and a second single-direction relationship so
  the existing pipeline measures also respond to a selected job; and
- 20 job-run, step, error and latest-selection measures in
  `_MissionControl_Measures`.

The monitoring notebook publishes `rpt_job_run_summary` and
`rpt_job_step_timing` as materialised Lake views so they are discoverable by
the Lakehouse semantic model. Refresh `00_setup_cfg` before refreshing the
aligned semantic model.

## Client-site package reconciliation — 20 September 2026

`reports/current/MWPP Repo 20092026.zip` is the latest client-site export
reviewed for this update. It contains the business-report project
`SM_WMPP_v16`; it does **not** contain a Mission Control semantic model.

The static inventory is:

| Check | `SM_WMPP_v16` result | Mission Control consequence |
| --- | ---: | --- |
| Semantic tables | 117 TMDL tables: 29 business/model tables, 87 `LocalDateTable_*` tables and one `DateTableTemplate_*` | This is the business model, not the monitoring model. |
| Measures | 274 | None of the 67 `_MissionControl_Measures` are present. |
| `cfg_*` tables | 0 | The operational measures in this guide cannot run in this model. |
| `_MissionControl_Measures` table | Absent | Import the maintained artifact only into the dedicated Mission Control model. |
| RLS roles | 0 | Security is also not implemented in this business-model export; see [RLS and partial aggregate access guide](RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md). |

The client-site ZIP therefore does not replace or supersede the separate
Mission Control model. Do not add the monitoring measures to `SM_WMPP_v16`
unless the architecture is deliberately changed to import the eight required
monitoring tables. The preferred deployment remains two semantic models:

1. `SM_WMPP_v16` for Gold referral, offer, IPA and provider reporting; and
2. a dedicated Mission Control model for `cfg_pipeline_run`, archive controls,
   Gold replay controls, data-quality results and schema inventory.

Before the next Mission Control release, export the deployed monitoring PBIP
from the client site and repeat the table, relationship, partition and report-
binding checks. The latest client-site ZIP provides no evidence that the
Mission Control model or its 67 measures are deployed.

## Delivery assessment

The earlier client package at `reports/client-deliverables/SM WMPP Mission Control.zip` was extracted and inspected for the original assessment below. Its semantic model contains the monitoring configuration/control tables below, but no `_Measures.tmdl` table. The included Power BI report references `_Measures` and currently binds 18 referral-oriented measures such as `Total Referrals` and `Active Referrals Under Offer`; those measures cannot be calculated from the delivered monitoring tables. Replace or rebind those visuals to the measures in `reports/current/_MissionControl_Measures.tmdl` before publishing the operational report. This remains a historical package assessment until a newer Mission Control PBIP is supplied from the client site.

The package contains an `SM WMPP v15.zip` referral model as a separate nested deliverable. It is not a source for Mission Control operational KPIs.

## Tables available in the delivered model

| Semantic table | Grain | Measures supported |
| --- | --- | --- |
| `rpt_job_run_summary` | One orchestrated live/archive job (`job_run_id`) | Job outcome, latest/selected job, duration, steps succeeded/failed, job error, Silver volume, DQ and drift summaries |
| `rpt_job_step_timing` | One ordered notebook step per `job_run_id` | Step outcome, duration, preceding-step gap, child result and full step error |
| `cfg_pipeline_run` | Pipeline/layer run | Outcome, duration, table counts, processing volume and error evidence |
| `cfg_archive_zip_load` | Archive ZIP export | ZIP outcome, reload queue, file count and elapsed time |
| `cfg_archive_file_load` | Extracted archive file | File outcome, reload queue and row volume |
| `cfg_archive_table_export_load` | Archive source-table export | Export outcome, reload queue and source row count |
| `cfg_month_end_gold_run` | Gold snapshot/replay run | Snapshot outcome, replay queue and DQ result |
| `cfg_data_quality_result` | Rule execution | Check outcome, failed/checked rows, severity and sample-key availability |
| `cfg_data_quality_rule` | Configured rule | Active and critical rule inventory |
| `cfg_archived_schema_live` | Observed archived column | Schema capture, table count, data-type and nullable-column inventory |

## Model setup

Keep the technical table names in the measure expressions. They match the
tables in the aligned `.pbip` model.

Use `rpt_job_run_summary[job_run_id]` as the one-side reporting key. The
materialised reporting table is already one row per orchestrated job. Relate
it one-to-many, single-direction to:

- `rpt_job_step_timing[job_run_id]`; and
- `cfg_pipeline_run[job_run_id]`.

Do not make either relationship bidirectional. A selected run must filter its
steps and child pipeline rows; a step row must not unexpectedly filter the
historical job-run chart. `run_id` remains the child notebook execution key
and must not replace `job_run_id` for the Gantt-to-step interaction.

Relate `cfg_data_quality_rule[rule_id]` one-to-many to `cfg_data_quality_result[rule_id]` after confirming the rule table has one current row per ID. `cfg_archived_schema_live` has no run ID and should be shown as a separately dated schema-inventory subject.

Treat statuses case-insensitively. The measures recognise `SUCCESS`/`SUCCEEDED`, `FAILED`/`FAIL`/`ERROR`, and `RUNNING`/`IN_PROGRESS`/`STARTED` so the report remains resilient to current control-table values.

## TMDL build artifact

`reports/current/_MissionControl_Measures.tmdl` contains 87 measures: the
original 67 operational measures plus 20 job-run/step interaction measures.
It uses the project’s required triple-backtick TMDL expression format. Import
it as the `_MissionControl_Measures` table in the Mission Control semantic
model.

The aligned package includes this table at
`SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`,
with a matching `ref table` in `model.tmdl`. Keep the measure formulas and
partition definition aligned between source and deployment. Power BI adds
`lineageTag` IDs and changes serialization whitespace when saving; the
validator accepts these differences while preserving checks on expressions,
names, formats and the Import partition. Do not overwrite Desktop-generated
lineage tags merely to make the files textually identical.

### Opening the project after adding the measures

The initial table addition omitted its partition. Power BI Desktop then reported `Model validation failed. A composite model cannot be used with entity based query sources.` The TMDL parsed successfully, but `_MissionControl_Measures` was the only table without a partition; all 32 existing tables used Import mode. This made the new table's Desktop load definition incomplete.

Both measure-table copies now include an explicit Import Power Query partition returning an empty table: `#table ( type table [], {} )`. This supplies the measure container without loading business rows or introducing another external data source. Preserve that partition when editing or copying the measures. The triple-backtick DAX expression delimiters are valid and remain in place. Microsoft describes partitions as the table's data-source definition in its [tables documentation](https://learn.microsoft.com/en-us/analysis-services/tmsl/tables-object-tmsl).

Validation includes the Microsoft TMDL deserializer and `python "project X/tests/validate_mission_control_model.py"`, which also runs through the existing pytest validator wrapper. These checks verify syntax and the saved table structure; they do not execute Power BI Desktop's private model-load validator or the DAX against live data. Reopen the saved `.pbip` in Desktop to confirm the reported load error is resolved. If it persists, retain the new error details for further diagnosis.

## Copy-ready DAX

```DAX

// Pipeline execution
Pipeline Runs =
DISTINCTCOUNT ( 'cfg_pipeline_run'[run_id] )

Successful Pipeline Runs =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Failed Pipeline Runs =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Running Pipeline Runs =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "RUNNING", "IN_PROGRESS", "STARTED" } ) )

Completed Pipeline Runs =
[Successful Pipeline Runs] + [Failed Pipeline Runs]

Pipeline Success Rate =
DIVIDE ( [Successful Pipeline Runs], [Completed Pipeline Runs] )

Live Pipeline Runs =
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )

Archive Pipeline Runs =
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )

Live Pipeline Failures =
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )

Archive Pipeline Failures =
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )

Pipeline Tables Succeeded =
SUM ( 'cfg_pipeline_run'[tables_succeeded] )

Pipeline Tables Failed =
SUM ( 'cfg_pipeline_run'[tables_failed] )

Pipeline Rows Read =
SUM ( 'cfg_pipeline_run'[rows_read] )

Pipeline Rows Written =
SUM ( 'cfg_pipeline_run'[rows_written] )

Pipeline Runs With Error =
COUNTROWS ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[error_message] ) ) )

Average Pipeline Duration (min) =
AVERAGEX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )

P95 Pipeline Duration (min) =
PERCENTILEX.INC ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ), 0.95 )

Total Pipeline Duration (min) =
SUMX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )

Pipeline Rows per Minute =
DIVIDE ( [Pipeline Rows Written], [Total Pipeline Duration (min)] )

Latest Pipeline End =
MAX ( 'cfg_pipeline_run'[ended_at] )

Latest Pipeline Status =
VAR latest_end = [Latest Pipeline End]
RETURN
    CALCULATE ( CONCATENATEX ( VALUES ( 'cfg_pipeline_run'[status] ), 'cfg_pipeline_run'[status], ", " ), 'cfg_pipeline_run'[ended_at] = latest_end )

// Orchestrated jobs and same-page job-to-step interaction
Job Runs =
DISTINCTCOUNT ( 'rpt_job_run_summary'[job_run_id] )

Successful Job Runs =
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Failed Job Runs =
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Job Success Rate =
DIVIDE ( [Successful Job Runs], [Successful Job Runs] + [Failed Job Runs] )

Latest Job Run Started =
MAXX ( FILTER ( ALLSELECTED ( 'rpt_job_run_summary' ), NOT ISBLANK ( 'rpt_job_run_summary'[started_at] ) ), 'rpt_job_run_summary'[started_at] )

Latest Job Run ID =
VAR latest_job =
    TOPN (
        1,
        FILTER ( ALLSELECTED ( 'rpt_job_run_summary' ), NOT ISBLANK ( 'rpt_job_run_summary'[started_at] ) ),
        'rpt_job_run_summary'[started_at], DESC,
        'rpt_job_run_summary'[job_run_id], DESC
    )
RETURN
    MAXX ( latest_job, 'rpt_job_run_summary'[job_run_id] )

Selected or Latest Job Run ID =
COALESCE ( SELECTEDVALUE ( 'rpt_job_run_summary'[job_run_id] ), [Latest Job Run ID] )

Selected or Latest Job Status =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
RETURN
    CALCULATE ( SELECTEDVALUE ( 'rpt_job_run_summary'[status] ), 'rpt_job_run_summary'[job_run_id] = selected_job_run_id )

Selected or Latest Job Error =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
RETURN
    CALCULATE ( SELECTEDVALUE ( 'rpt_job_run_summary'[error_message] ), 'rpt_job_run_summary'[job_run_id] = selected_job_run_id )

Selected or Latest Job Duration (min) =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
RETURN
    CALCULATE ( DIVIDE ( MAX ( 'rpt_job_run_summary'[job_duration_seconds] ), 60.0 ), 'rpt_job_run_summary'[job_run_id] = selected_job_run_id )

Job Steps =
COUNTROWS ( 'rpt_job_step_timing' )

Successful Job Steps =
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Failed Job Steps =
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Job Steps With Error =
COUNTROWS ( FILTER ( 'rpt_job_step_timing', NOT ISBLANK ( 'rpt_job_step_timing'[error_message] ) && 'rpt_job_step_timing'[error_message] <> "" ) )

Selected or Latest Job Steps =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
RETURN
    CALCULATE ( [Job Steps], KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id ) )

Selected or Latest Failed Steps =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
RETURN
    CALCULATE ( [Failed Job Steps], KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id ) )

Total Job Step Duration (min) =
DIVIDE ( SUM ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )

Longest Job Step Duration (min) =
DIVIDE ( MAX ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )

Show Step for Selected or Latest Job Run =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
VAR matching_steps =
    CALCULATE (
        COUNTROWS ( 'rpt_job_step_timing' ),
        KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
    )
RETURN
    IF ( NOT ISBLANK ( selected_job_run_id ) && matching_steps > 0, 1, 0 )

Selected Step Error Detail =
CONCATENATEX (
    FILTER (
        VALUES ( 'rpt_job_step_timing'[error_message] ),
        NOT ISBLANK ( 'rpt_job_step_timing'[error_message] )
            && 'rpt_job_step_timing'[error_message] <> ""
    ),
    'rpt_job_step_timing'[error_message],
    UNICHAR ( 10 ) & UNICHAR ( 10 )
)

// Archive and replay control
Archive ZIP Batches =
COUNTROWS ( 'cfg_archive_zip_load' )

Successful Archive ZIP Batches =
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Failed Archive ZIP Batches =
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Archive ZIP Batches Awaiting Reload =
CALCULATE ( [Archive ZIP Batches], 'cfg_archive_zip_load'[reload] = TRUE () )

Archive ZIP Files Declared =
SUM ( 'cfg_archive_zip_load'[file_count] )

Average Archive ZIP Duration (min) =
AVERAGEX ( FILTER ( 'cfg_archive_zip_load', NOT ISBLANK ( 'cfg_archive_zip_load'[started_at] ) && NOT ISBLANK ( 'cfg_archive_zip_load'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_archive_zip_load'[started_at], 'cfg_archive_zip_load'[ended_at], SECOND ), 60.0 ) )

Archive Files Processed =
COUNTROWS ( 'cfg_archive_file_load' )

Successful Archive Files =
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Archive File Failures =
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Archive Files Awaiting Reload =
CALCULATE ( [Archive Files Processed], 'cfg_archive_file_load'[reload] = TRUE () )

Archive File Rows Read =
SUM ( 'cfg_archive_file_load'[rows_read] )

Archive File Rows Written =
SUM ( 'cfg_archive_file_load'[rows_written] )

Archive Table Exports =
COUNTROWS ( 'cfg_archive_table_export_load' )

Failed Archive Table Exports =
COUNTROWS ( FILTER ( 'cfg_archive_table_export_load', UPPER ( COALESCE ( 'cfg_archive_table_export_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Archive Table Exports Awaiting Reload =
CALCULATE ( [Archive Table Exports], 'cfg_archive_table_export_load'[reload] = TRUE () )

Archive Export Rows =
SUM ( 'cfg_archive_table_export_load'[row_count] )

Gold Snapshot Runs =
COUNTROWS ( 'cfg_month_end_gold_run' )

Successful Gold Snapshots =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )

Failed Gold Snapshots =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

Gold Snapshots Awaiting Replay =
CALCULATE ( [Gold Snapshot Runs], 'cfg_month_end_gold_run'[reload] = TRUE () )

Gold Snapshot DQ Failures =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[dq_result], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

// Data quality and referential rules
DQ Checks =
COUNTROWS ( 'cfg_data_quality_result' )

DQ Evaluated Checks =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "PASS", "SUCCESS", "FAILED", "FAIL", "ERROR" } ) )

DQ Failed Checks =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

DQ Failure Rate =
DIVIDE ( [DQ Failed Checks], [DQ Evaluated Checks] )

DQ Checked Rows =
SUM ( 'cfg_data_quality_result'[checked_row_count] )

DQ Failed Rows =
SUM ( 'cfg_data_quality_result'[failed_row_count] )

Weighted DQ Failure Percentage =
DIVIDE ( [DQ Failed Rows], [DQ Checked Rows] )

Critical Rules Failing =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) = "CRITICAL" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

High or Critical Rules Failing =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) IN { "CRITICAL", "HIGH" } && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

DQ Failures With Sample Keys =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } && NOT ISBLANK ( 'cfg_data_quality_result'[sample_key_json] ) ) )

Active DQ Rules =
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } ) )

Critical Active DQ Rules =
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } && UPPER ( COALESCE ( 'cfg_data_quality_rule'[severity], "" ) ) = "CRITICAL" ) )

RI Rules Failing =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )

RI Checked Rows =
CALCULATE ( [DQ Checked Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )

RI Failed Rows =
CALCULATE ( [DQ Failed Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )

RI Failure Rate =
DIVIDE ( [RI Failed Rows], [RI Checked Rows] )

// Archived schema inventory
Archived Schema Columns =
COUNTROWS ( 'cfg_archived_schema_live' )

Archived Schema Tables =
COUNTROWS ( SUMMARIZE ( 'cfg_archived_schema_live', 'cfg_archived_schema_live'[schema_name], 'cfg_archived_schema_live'[table_name] ) )

Latest Archived Schema Capture =
MAX ( 'cfg_archived_schema_live'[contract_loaded_at] )

Archived Nullable Columns =
COUNTROWS ( FILTER ( 'cfg_archived_schema_live', UPPER ( COALESCE ( 'cfg_archived_schema_live'[is_nullable], "" ) ) IN { "TRUE", "YES", "Y", "1" } ) )

Archived Schema Data Types =
DISTINCTCOUNT ( 'cfg_archived_schema_live'[data_type] )

// Control health
Reload Requests =
[Archive ZIP Batches Awaiting Reload] + [Archive Files Awaiting Reload] + [Archive Table Exports Awaiting Reload] + [Gold Snapshots Awaiting Replay]

Control Failures =
[Failed Pipeline Runs] + [Failed Archive ZIP Batches] + [Archive File Failures] + [Failed Archive Table Exports] + [Failed Gold Snapshots]

Operational Exception Count =
[Control Failures] + [DQ Failed Checks]

Dashboard Last Refreshed =
FORMAT ( UTCNOW (), "dd mmm yyyy HH:mm" )

```

## Measures deliberately deferred

The aligned model now contains job-run and job-step timing tables, so failed
notebook steps, slow steps and job/step error evidence are no longer deferred.
It still does not import the table-load metric, schema-drift event,
referential-exception, rejected-row or data-domain profile reporting tables.
Do not create detail visuals for those subjects until the corresponding
`rpt_job_*` tables are imported.

The dashboard wireframe at `reports/mission-control/index.html` remains the
layout reference. Its Job steps & errors concept can now be implemented from
the two imported `rpt_job_*` tables.

## Same-page latest job, historical Gantt and step detail

Build the feature on one report page as follows.

### 1. Page filters and latest-job behaviour

Add a `pipeline_name` slicer from `rpt_job_run_summary`. For a today-only
operations page, add a relative date filter on
`rpt_job_run_summary[started_at]` set to **is in this day**. The runner writes
UTC timestamps, so agree the report/service timezone before using a local-day
operational cut-off.

Use these cards:

| Card | Field |
| --- | --- |
| Selected/latest run | `[Selected or Latest Job Run ID]` |
| Status | `[Selected or Latest Job Status]` |
| Duration | `[Selected or Latest Job Duration (min)]` |
| Step count | `[Selected or Latest Job Steps]` |
| Failed steps | `[Selected or Latest Failed Steps]` |
| Job error | `[Selected or Latest Job Error]` |

With no explicit job selected, the measures choose the most recent
`started_at` within the page's current date and pipeline filters. Selecting a
single historical run replaces that fallback automatically.

### 2. Historical job-run Gantt

Configure the Gantt from `rpt_job_run_summary`:

| Gantt role | Field |
| --- | --- |
| Task/category | `job_run_id` |
| Parent/resource | `pipeline_name` |
| Start | `started_at` |
| End | `ended_at` |
| Legend/colour | `status` |
| Tooltip | `job_run_id`, `status`, `steps_succeeded`, `steps_failed`, `error_message` |

Use `job_run_id`, not `run_id`, as the selectable bar identity. If the chosen
Gantt visual requires duration rather than an end time, use
`job_duration_seconds`. Apply status colours consistently: succeeded green,
running amber/blue and failed red.

In **Format → Edit interactions**, select the Gantt and set its interaction
with the step table to **Filter**, not Highlight or None. The active
single-direction relationship then filters the table to every step belonging
to the clicked job. Clearing the Gantt selection returns the table to the
latest job in the current page filters.

### 3. Step table on the same page

Build a table from `rpt_job_step_timing` using:

1. `step_sequence`;
2. `notebook_name`;
3. `status`;
4. `started_at`;
5. `ended_at`;
6. `step_duration_seconds`;
7. `gap_from_previous_step_seconds`; and
8. `error_message`.

Sort ascending by `step_sequence`. Add
`[Show Step for Selected or Latest Job Run]` to **Filters on this visual** and
set it to `1`. This is the important fallback: it limits the table to the
latest run when no Gantt bar is selected, while the relationship handles a
clicked historical run.

Turn on word wrap for `error_message`, give it enough width, and conditionally
format failed/error statuses red. Successful steps naturally show a blank
error. Use `[Selected Step Error Detail]` in a multi-row card or tooltip when
the full error is too long for the table. `child_result` may be added to an
authorised drillthrough page, but it should not replace `error_message` as the
failure field.

### 4. Expected interaction

```text
Date/pipeline filters
        ↓
Historical job Gantt ──click job_run_id──→ selected job
        ↓ active 1:* relationship
Step table + error text

No Gantt selection ──latest-job measures──→ latest run in current filters
```

This design keeps the operational context on one page. A drillthrough page is
optional for untruncated `error_message` and `child_result`, not required for
the basic latest-job and clicked-history workflow.

## Formatting and visual use

| Measure group | Card/visual use | Format |
| --- | --- | --- |
| Job runs and selection | Historical Gantt, latest/selected job status, duration and job error | Whole counts; minutes to one decimal; error text with word wrap |
| Job steps | Same-page ordered step table, failed-step cards and error detail | Whole counts; seconds or minutes; untruncated error text |
| Pipeline execution | Executive health, Live ETL and Archive ETL outcome cards; duration and volume trends | Whole counts; minutes to one decimal; rates as percentages |
| Archive control | Archive readiness, retry/reload queue and Gold snapshot replay | Whole counts and row volumes |
| Data quality | Failed checks, failed rows, severity and RI rule outcome | Whole counts and percentages |
| Schema inventory | Archived schema coverage and capture recency | Whole counts and date/time |
| Control health | Executive exception and reload cards | Whole counts; it is a category total, not a unique-event total |

## Deployment checklist

1. Run the current `00_setup_cfg` so `rpt_job_run_summary` and
   `rpt_job_step_timing` exist as materialised Lake views.
2. Open the aligned PBIP, set the Lakehouse connection if prompted, and run a
   full semantic-model refresh.
3. Confirm `rpt_job_run_summary[job_run_id]` is unique and the two
   relationships are active, one-to-many and single-direction.
4. Validate the actual status vocabulary with a table visual before relying
   on success/failure cards.
5. Build the Gantt and step table using the field assignments above; set the
   Gantt-to-table interaction to Filter and the step-table fallback measure to
   `1`.
6. Test three cases: no selection shows today's latest job, a successful job
   shows all steps with blank errors, and a failed historical job shows its
   failed step and complete `error_message`.
7. Add a date-only dimension only when a consistent reporting-date field is
   agreed; do not mix `started_at`, `export_date`, `snapshot_date`,
   `checked_at`, and `contract_loaded_at` in one relationship.
8. Keep sample-key JSON, child results and full errors on authorised
   operational pages; do not surface sensitive evidence on executive pages.
