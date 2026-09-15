# Mission Control semantic model DAX build guide

## Purpose

This guide defines the operational measures for the WMPP Mission Control model. They use the monitoring control tables present in the client-delivered semantic-model package, rather than referral, offer or placement facts.

## Delivery assessment

The client package at `reports/client-deliverables/SM WMPP Mission Control.zip` was extracted and inspected. Its semantic model contains the monitoring configuration/control tables below, but no `_Measures.tmdl` table. The included Power BI report references `_Measures` and currently binds 18 referral-oriented measures such as `Total Referrals` and `Active Referrals Under Offer`; those measures cannot be calculated from the delivered monitoring tables. Replace or rebind those visuals to the measures in `reports/current/_MissionControl_Measures.tmdl` before publishing the operational report.

The package contains an `SM WMPP v15.zip` referral model as a separate nested deliverable. It is not a source for Mission Control operational KPIs.

## Tables available in the delivered model

| Semantic table | Grain | Measures supported |
| --- | --- | --- |
| `cfg_pipeline_run` | Pipeline/layer run | Outcome, duration, table counts, processing volume and error evidence |
| `cfg_archive_zip_load` | Archive ZIP export | ZIP outcome, reload queue, file count and elapsed time |
| `cfg_archive_file_load` | Extracted archive file | File outcome, reload queue and row volume |
| `cfg_archive_table_export_load` | Archive source-table export | Export outcome, reload queue and source row count |
| `cfg_month_end_gold_run` | Gold snapshot/replay run | Snapshot outcome, replay queue and DQ result |
| `cfg_data_quality_result` | Rule execution | Check outcome, failed/checked rows, severity and sample-key availability |
| `cfg_data_quality_rule` | Configured rule | Active and critical rule inventory |
| `cfg_archived_schema_live` | Observed archived column | Schema capture, table count, data-type and nullable-column inventory |

## Model setup

Keep the technical table names in the measure expressions. They match the tables in the delivered `.pbip` model.

Before creating relationships, check whether `cfg_pipeline_run[run_id]` is unique. If it is unique, create one-to-many, single-direction relationships from it to `run_id` in `cfg_archive_zip_load`, `cfg_archive_file_load`, `cfg_archive_table_export_load`, `cfg_month_end_gold_run`, and `cfg_data_quality_result`. If it is not unique because one pipeline run has several layer records, create a Power Query `Job Run` dimension with one row per `run_id` and relate the operational tables to that dimension instead.

Relate `cfg_data_quality_rule[rule_id]` one-to-many to `cfg_data_quality_result[rule_id]` after confirming the rule table has one current row per ID. `cfg_archived_schema_live` has no run ID and should be shown as a separately dated schema-inventory subject.

Treat statuses case-insensitively. The measures recognise `SUCCESS`/`SUCCEEDED`, `FAILED`/`FAIL`/`ERROR`, and `RUNNING`/`IN_PROGRESS`/`STARTED` so the report remains resilient to current control-table values.

## TMDL build artifact

`reports/current/_MissionControl_Measures.tmdl` contains the 67 measures below using the project’s required triple-backtick TMDL expression format. Import it as the `_MissionControl_Measures` table in the Mission Control semantic model.

The extracted PBIP includes this table at `reports/client-deliverables/SM WMPP Mission Control/SM WMPP Mission Control/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, with a matching `ref table` in `model.tmdl`. Keep the measure formulas and partition definition aligned between source and deployment. Power BI adds `lineageTag` IDs and changes serialization whitespace when saving; the validator accepts these differences while preserving checks on expressions, names, formats and the Import partition. Do not overwrite Desktop-generated lineage tags merely to make the files textually identical.

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

The delivered model does not contain a job-step timing table, table-load metric table, schema-drift event table, referential-exception table, rejected-row table, or data-domain profile table. Do not create cards for failed notebook steps, slow steps, active drift, RI exception counts, domain values, or new-domain values until those tables or views are imported.

The dashboard wireframe at `reports/mission-control/index.html` shows those future pages. Use it to shape the visual layout, but bind only the current-source measures to published visuals. Mark unavailable pages as planned or hide them until their data sources are present.

## Formatting and visual use

| Measure group | Card/visual use | Format |
| --- | --- | --- |
| Pipeline execution | Executive health, Live ETL and Archive ETL outcome cards; duration and volume trends | Whole counts; minutes to one decimal; rates as percentages |
| Archive control | Archive readiness, retry/reload queue and Gold snapshot replay | Whole counts and row volumes |
| Data quality | Failed checks, failed rows, severity and RI rule outcome | Whole counts and percentages |
| Schema inventory | Archived schema coverage and capture recency | Whole counts and date/time |
| Control health | Executive exception and reload cards | Whole counts; it is a category total, not a unique-event total |

## Deployment checklist

1. Create or import `_MissionControl_Measures` from the TMDL artifact.
2. Validate the `run_id` grain before enabling run-level relationships.
3. Add a date-only dimension only when a consistent reporting-date field is agreed; do not mix `export_date`, `snapshot_date`, `checked_at`, and `contract_loaded_at` in one relationship.
4. Validate the actual status vocabulary with a table visual before relying on success/failure cards.
5. Rebind the client report’s old referral cards to the operational cards defined here.
6. Keep sample-key JSON and error messages on authorised drillthrough pages; do not surface them on executive pages.
