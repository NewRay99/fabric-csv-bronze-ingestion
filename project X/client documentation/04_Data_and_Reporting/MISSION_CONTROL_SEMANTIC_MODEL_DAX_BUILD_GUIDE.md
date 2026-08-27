# Mission Control semantic model DAX build guide

## Purpose

Use this guide to build the separate Power BI semantic model for the WMPP ETL
Operations Control Tower. It is intentionally separate from the referral Gold
semantic model: these measures use `monitoring` operational views and control
tables rather than `gold` referral facts.

The interactive report wireframe remains in `reports/mission-control/index.html`.
This document is the copy-ready DAX source of truth for that report.

## Import and relationship instructions

Import the following objects with the semantic-model names shown. Use
`monitoring.vw_job_run_summary` as the Job Run hub.

| Semantic-model name | Lakehouse object | Purpose |
| --- | --- | --- |
| `Job Run` | `monitoring.vw_job_run_summary` | One row per pipeline job run |
| `Job Step` | `monitoring.vw_job_step_timing` | Child-notebook timing and status |
| `Data Quality` | `monitoring.vw_job_data_quality` | Data-quality execution results |
| `Schema Drift` | `monitoring.vw_job_schema_drift` | Detected schema-contract drift |
| `Table Load Metric` | `monitoring.cfg_table_load_metric` | Per-table processing and quality metrics |
| `Archive ZIP Load` | `monitoring.cfg_archive_zip_load` | Archive package processing status |
| `Archive File Load` | `monitoring.cfg_archive_file_load` | Archive extract-file processing status |
| `Month End Gold Run` | `monitoring.cfg_month_end_gold_run` | Gold snapshot/replay control |
| `Referential Exception` | `monitoring.cfg_referential_exception` | Referential-integrity exceptions |
| `Data Domain` | `monitoring.cfg_data_domain` | Low-cardinality data-domain profiles |
| `Schema Contract Column` | `monitoring.cfg_schema_contract_column` | Configured schema-contract columns |

Create one-to-many, single-direction relationships from
`Job Run[job_run_id]` to the corresponding `job_run_id` in `Job Step`, `Data
Quality`, `Schema Drift`, `Table Load Metric`, and `Referential Exception`.
Use date-only columns in Power Query when a report-level date relationship is
needed.

Create two distinct ETL pages and apply the stated page filter to every
job-based visual and drillthrough path:

| Page | Required filter |
| --- | --- |
| Live ETL | `Job Run[pipeline_name] = "90_run_live_pipeline"` |
| Archive ETL | `Job Run[pipeline_name] = "90_run_archive_pipeline"` |

Do not place archive `export_date` or `snapshot_date` batch metrics on the
Live ETL page.

## Copy-ready DAX

Create the measures below in a dedicated `_measures` table.

```DAX
// Pipeline execution
Job Runs =
DISTINCTCOUNT ( 'Job Run'[job_run_id] )

Successful Job Runs =
CALCULATE ( [Job Runs], 'Job Run'[status] = "SUCCESS" )

Failed Job Runs =
CALCULATE ( [Job Runs], 'Job Run'[status] IN { "FAILED", "ERROR" } )

Job Success Rate =
DIVIDE ( [Successful Job Runs], [Job Runs] )

Live Pipeline Job Runs =
CALCULATE ( [Job Runs], 'Job Run'[pipeline_name] = "90_run_live_pipeline" )

Archive Pipeline Job Runs =
CALCULATE ( [Job Runs], 'Job Run'[pipeline_name] = "90_run_archive_pipeline" )

Live Pipeline Failed Jobs =
CALCULATE ( [Failed Job Runs], 'Job Run'[pipeline_name] = "90_run_live_pipeline" )

Archive Pipeline Failed Jobs =
CALCULATE ( [Failed Job Runs], 'Job Run'[pipeline_name] = "90_run_archive_pipeline" )

Average Job Duration (min) =
DIVIDE ( AVERAGE ( 'Job Run'[job_duration_seconds] ), 60 )

P95 Job Duration (min) =
DIVIDE (
    PERCENTILEX.INC ( 'Job Run', 'Job Run'[job_duration_seconds], 0.95 ),
    60
)

Latest Job End =
MAX ( 'Job Run'[ended_at] )

// Notebook and table processing
Job Steps =
COUNTROWS ( 'Job Step' )

Failed Job Steps =
CALCULATE ( [Job Steps], 'Job Step'[status] IN { "FAILED", "ERROR" } )

Average Step Duration (min) =
DIVIDE ( AVERAGE ( 'Job Step'[step_duration_seconds] ), 60 )

Slow Steps Over 30 Minutes =
COUNTROWS ( FILTER ( 'Job Step', 'Job Step'[step_duration_seconds] > 1800 ) )

Maximum Step Gap (min) =
DIVIDE ( MAX ( 'Job Step'[gap_from_previous_step_seconds] ), 60 )

Silver Targets Processed =
DISTINCTCOUNT ( 'Table Load Metric'[target_object] )

Rows Read =
SUM ( 'Table Load Metric'[rows_read] )

Rows Written =
SUM ( 'Table Load Metric'[rows_written] )

Duplicate Rows =
SUM ( 'Table Load Metric'[duplicate_key_count] )

Null Primary Keys =
SUM ( 'Table Load Metric'[null_primary_key_count] )

Rows per Minute =
DIVIDE ( [Rows Written], [Average Job Duration (min)] )

// Archive and Gold replay control
Archive ZIP Batches =
COUNTROWS ( 'Archive ZIP Load' )

Archive File Failures =
CALCULATE (
    COUNTROWS ( 'Archive File Load' ),
    'Archive File Load'[status] IN { "FAILED", "ERROR" }
)

Archive Files Awaiting Reload =
CALCULATE ( COUNTROWS ( 'Archive File Load' ), 'Archive File Load'[reload] = TRUE () )

Successful Gold Snapshots =
CALCULATE ( COUNTROWS ( 'Month End Gold Run' ), 'Month End Gold Run'[status] = "SUCCESS" )

Gold Snapshots Awaiting Replay =
CALCULATE ( COUNTROWS ( 'Month End Gold Run' ), 'Month End Gold Run'[reload] = TRUE () )

// Data quality and schema contract
DQ Checks =
COUNTROWS ( 'Data Quality' )

DQ Failed Checks =
CALCULATE ( [DQ Checks], 'Data Quality'[status] IN { "FAIL", "ERROR" } )

DQ Failure Rate =
DIVIDE (
    [DQ Failed Checks],
    CALCULATE ( [DQ Checks], 'Data Quality'[status] IN { "PASS", "FAIL", "ERROR" } )
)

DQ Failed Rows =
SUM ( 'Data Quality'[failed_row_count] )

Weighted DQ Failure Percentage =
DIVIDE ( [DQ Failed Rows], SUM ( 'Data Quality'[checked_row_count] ) )

Critical Rules Failing =
CALCULATE (
    DISTINCTCOUNT ( 'Data Quality'[rule_id] ),
    'Data Quality'[severity] = "CRITICAL",
    'Data Quality'[status] IN { "FAIL", "ERROR" }
)

Rejected Keys =
SUM ( 'Data Quality'[rejected_key_count] )

Active Drift Events =
CALCULATE (
    DISTINCTCOUNT ( 'Schema Drift'[drift_key] ),
    'Schema Drift'[status] = "ACTIVE"
)

Resolved Drift Events =
CALCULATE (
    DISTINCTCOUNT ( 'Schema Drift'[drift_key] ),
    NOT ISBLANK ( 'Schema Drift'[resolved_at] )
)

New Drift Events (24h) =
CALCULATE (
    DISTINCTCOUNT ( 'Schema Drift'[drift_key] ),
    'Schema Drift'[first_detected_at] >= NOW () - 1
)

Type Mismatch Events =
CALCULATE ( [Active Drift Events], 'Schema Drift'[drift_type] = "TYPE_MISMATCH" )

Contract Columns =
COUNTROWS ( 'Schema Contract Column' )

// Referential integrity
Referential Exceptions =
COUNTROWS ( 'Referential Exception' )

Affected RI Relationships =
COUNTROWS (
    SUMMARIZE (
        'Referential Exception',
        'Referential Exception'[child_table],
        'Referential Exception'[child_column],
        'Referential Exception'[parent_table],
        'Referential Exception'[parent_column]
    )
)

RI Rules Failing =
CALCULATE (
    DISTINCTCOUNT ( 'Data Quality'[rule_id] ),
    'Data Quality'[rule_type] = "REFERENTIAL_INTEGRITY",
    'Data Quality'[status] IN { "FAIL", "ERROR" }
)

RI Failure Rate =
DIVIDE (
    [Referential Exceptions],
    CALCULATE (
        SUM ( 'Data Quality'[checked_row_count] ),
        'Data Quality'[rule_type] = "REFERENTIAL_INTEGRITY"
    )
)

// Data-domain profile
Latest Domain Profile =
MAX ( 'Data Domain'[profiled_at] )

Profiled Domain Columns =
VAR LatestProfile = [Latest Domain Profile]
RETURN
    CALCULATE (
        DISTINCTCOUNT ( 'Data Domain'[Domain Column Key] ),
        'Data Domain'[profiled_at] = LatestProfile
    )

Domain Values =
VAR LatestProfile = [Latest Domain Profile]
RETURN
    CALCULATE (
        DISTINCTCOUNT ( 'Data Domain'[Domain Value Key] ),
        'Data Domain'[profiled_at] = LatestProfile
    )

New Domain Values Since Previous Profile =
VAR LatestProfile = [Latest Domain Profile]
VAR PreviousProfile =
    CALCULATE (
        MAX ( 'Data Domain'[profiled_at] ),
        FILTER ( ALL ( 'Data Domain'[profiled_at] ), 'Data Domain'[profiled_at] < LatestProfile )
    )
VAR CurrentValues =
    CALCULATETABLE (
        VALUES ( 'Data Domain'[Domain Value Key] ),
        'Data Domain'[profiled_at] = LatestProfile
    )
VAR PreviousValues =
    CALCULATETABLE (
        VALUES ( 'Data Domain'[Domain Value Key] ),
        'Data Domain'[profiled_at] = PreviousProfile
    )
RETURN
    IF ( ISBLANK ( PreviousProfile ), BLANK (), COUNTROWS ( EXCEPT ( CurrentValues, PreviousValues ) ) )
```

## Required calculated columns

Create these calculated columns in `Data Domain` before using the final three
domain-profile measures. They form stable keys across a profile run.

```DAX
Domain Column Key =
'Data Domain'[source_schema] & "|" &
'Data Domain'[source_table] & "|" &
'Data Domain'[column_name]

Domain Value Key =
'Data Domain'[Domain Column Key] & "|" &
'Data Domain'[data_domain]
```

## Deployment checklist

1. Import the listed monitoring views and tables using the exact display names.
2. Create the `job_run_id` hub relationships and retain single-direction filtering.
3. Create the `Data Domain` calculated columns before adding domain measures.
4. Add the DAX measures to an `_measures` table; format rates as percentages and duration measures as decimal minutes.
5. Build separate Live ETL and Archive ETL pages using their mandatory filters.
6. State in the report that table/column lifecycle events and true insert,
   update and delete counts are not currently captured. Do not infer them from
   snapshot overwrite counts.
