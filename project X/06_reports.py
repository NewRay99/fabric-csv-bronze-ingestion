# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770",
# META       "known_lakehouses": [
# META         {
# META           "id": "d286fa39-f255-4ba7-a982-32cb69362ef7"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 06 — Monitoring reports
# Define the monitoring materialized lake views after the Silver and Gold steps.
# `00_setup_cfg` creates their configuration and control sources. Schedule the
# materialized lake view refresh in the Lakehouse after the parent pipeline job
# completes so the final job and 06_reports step statuses are included.

# PARAMETERS CELL ********************

JOB_RUN_ID = ""  # Parent orchestration correlation ID.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_step_timing AS
WITH ordered_steps AS (
  SELECT
    job_run_id, step_sequence, notebook_name, started_at, ended_at, status,
    child_result, error_message,
    LAG(ended_at) OVER (PARTITION BY job_run_id ORDER BY step_sequence) AS previous_step_ended_at
  FROM monitoring.cfg_job_step_run
)
SELECT
  job_run_id, step_sequence, notebook_name, status, started_at, ended_at,
  ROUND(unix_timestamp(coalesce(ended_at, current_timestamp())) - unix_timestamp(started_at), 2) AS step_duration_seconds,
  ROUND(unix_timestamp(started_at) - unix_timestamp(previous_step_ended_at), 2) AS gap_from_previous_step_seconds,
  child_result, error_message
FROM ordered_steps
""")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_step_summary AS
WITH pipeline AS (
  SELECT job_run_id, pipeline_name, status, rows_read, rows_written,
         tables_succeeded, tables_failed, error_message
  FROM monitoring.cfg_pipeline_run
  WHERE job_run_id IS NOT NULL
), metric AS (
  SELECT job_run_id,
    CASE WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
         WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END AS notebook_name,
    COUNT(DISTINCT target_object) AS target_count,
    SUM(rows_read) AS rows_read, SUM(rows_written) AS rows_written,
    SUM(duplicate_key_count) AS duplicate_rows, SUM(null_primary_key_count) AS null_primary_keys
  FROM monitoring.cfg_table_load_metric
  WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, CASE WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
                            WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END
), dq AS (
  SELECT job_run_id, COUNT(*) AS checks_run,
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) AS checks_passed,
    SUM(CASE WHEN status IN ('FAIL', 'ERROR') THEN 1 ELSE 0 END) AS checks_failed,
    SUM(failed_row_count) AS failed_row_count
  FROM monitoring.cfg_data_quality_result
  WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), drift AS (
  SELECT job_run_id,
    CASE WHEN source_kind = 'LIVE' THEN '01a_cfg_schema_capture_live'
         WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
         WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END AS notebook_name,
    COUNT(*) AS drift_event_count,
    SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_drift_count
  FROM monitoring.cfg_schema_drift_event
  WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, CASE WHEN source_kind = 'LIVE' THEN '01a_cfg_schema_capture_live'
                             WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
                             WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END
)
SELECT s.*, p.rows_read AS pipeline_rows_read, p.rows_written AS pipeline_rows_written,
  p.tables_succeeded, p.tables_failed, p.error_message AS pipeline_error_message,
  m.target_count, m.rows_read AS metric_rows_read, m.rows_written AS metric_rows_written,
  m.duplicate_rows, m.null_primary_keys,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_run END AS dq_checks_run,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_passed END AS dq_checks_passed,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_failed END AS dq_checks_failed,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.failed_row_count END AS dq_failed_row_count,
  d.drift_event_count, d.active_drift_count
FROM monitoring.rpt_job_step_timing s
LEFT JOIN pipeline p ON p.job_run_id = s.job_run_id
  AND p.pipeline_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
LEFT JOIN metric m ON m.job_run_id = s.job_run_id
  AND m.notebook_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
LEFT JOIN dq ON dq.job_run_id = s.job_run_id
LEFT JOIN drift d ON d.job_run_id = s.job_run_id
  AND d.notebook_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_run_summary AS
WITH metric AS (
  SELECT job_run_id, COUNT(DISTINCT target_object) AS silver_targets,
         SUM(rows_read) AS rows_read, SUM(rows_written) AS rows_written,
         SUM(duplicate_key_count) AS duplicate_rows
  FROM monitoring.cfg_table_load_metric WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), dq AS (
  SELECT job_run_id, COUNT(*) AS dq_checks,
         SUM(CASE WHEN status IN ('FAIL', 'ERROR') THEN 1 ELSE 0 END) AS dq_failures
  FROM monitoring.cfg_data_quality_result WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), drift AS (
  SELECT job_run_id, COUNT(*) AS drift_events,
         SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_drift_events
  FROM monitoring.cfg_schema_drift_event WHERE job_run_id IS NOT NULL GROUP BY job_run_id
)
SELECT j.*, ROUND(unix_timestamp(coalesce(j.ended_at, current_timestamp())) - unix_timestamp(j.started_at), 2) AS job_duration_seconds,
  m.silver_targets, m.rows_read, m.rows_written, m.duplicate_rows,
  dq.dq_checks, dq.dq_failures, drift.drift_events, drift.active_drift_events
FROM monitoring.cfg_job_run j
LEFT JOIN metric m ON m.job_run_id = j.job_run_id
LEFT JOIN dq ON dq.job_run_id = j.job_run_id
LEFT JOIN drift ON drift.job_run_id = j.job_run_id
""")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_schema_drift AS
SELECT e.job_run_id, e.run_id, e.source_kind, e.source_table, e.target_table,
  e.drift_type, e.column_name, e.expected_type, e.actual_type,
  e.referenced_table, e.referenced_column, e.status, e.occurrence_count,
  e.first_detected_at, e.last_detected_at, e.resolved_at,
  d.definition_hash, d.join_class, d.join_evidence,
  CASE WHEN d.table_name IS NULL THEN false ELSE true END AS definition_match_found
FROM monitoring.cfg_schema_drift_event e
LEFT JOIN monitoring.cfg_schema_drift_definition d
  ON lower(d.table_name) = lower(regexp_replace(e.source_table, '^[^.]+\\.', ''))
 AND (e.column_name IS NULL OR lower(d.column_name) = lower(e.column_name))
""")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_data_quality AS
WITH rejected AS (
  SELECT job_run_id, run_id, rule_id, COUNT(*) AS rejected_key_count
  FROM monitoring.cfg_rejected_row WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, run_id, rule_id
), exceptions AS (
  SELECT job_run_id, run_id, rule_id, COUNT(*) AS referential_exception_count
  FROM monitoring.cfg_referential_exception WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, run_id, rule_id
)
SELECT r.job_run_id, r.run_id, r.rule_id, r.severity, r.rule_type,
  r.source_table, r.column_name, r.status, r.checked_row_count,
  r.failed_row_count, r.failure_percentage, r.sample_key_json, r.checked_at,
  r.message, coalesce(x.rejected_key_count, 0) AS rejected_key_count,
  coalesce(e.referential_exception_count, 0) AS referential_exception_count
FROM monitoring.cfg_data_quality_result r
LEFT JOIN rejected x ON x.job_run_id = r.job_run_id AND x.run_id = r.run_id AND x.rule_id = r.rule_id
LEFT JOIN exceptions e ON e.job_run_id = r.job_run_id AND e.run_id = r.run_id AND e.rule_id = r.rule_id
WHERE r.job_run_id IS NOT NULL
""")


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_layer_lineage AS
SELECT a.job_run_id,
  CASE WHEN a.source_kind = 'LATEST' THEN 'BRONZE' ELSE 'ARCHIVE' END AS source_layer,
  a.source_table AS source_object, 'SILVER' AS target_layer, a.target_table AS target_object,
  'SOURCE_TO_SILVER' AS lineage_stage,
  CASE WHEN a.status = 'SUCCESS' THEN 'MATCHED' ELSE a.status END AS lineage_status,
  a.rows_read, a.rows_written, a.duplicate_key_count, a.export_date AS observed_at,
  CAST(NULL AS STRING) AS relationship_role
FROM monitoring.cfg_silver_export_load a
WHERE a.job_run_id IS NOT NULL
UNION ALL
SELECT s.job_run_id, m.source_layer, m.source_object, 'GOLD', m.gold_object,
  'SILVER_TO_GOLD',
  CASE WHEN s.status = 'SUCCESS' THEN 'MATCHED' ELSE s.status END,
  CAST(NULL AS BIGINT), CAST(NULL AS BIGINT), CAST(NULL AS BIGINT), s.ended_at,
  m.relationship_role
FROM monitoring.cfg_job_step_run s
INNER JOIN monitoring.cfg_gold_lineage_mapping m
  ON m.transformation_notebook = regexp_replace(s.notebook_name, '\\.ipynb$', '')
WHERE s.notebook_name IN ('04_gold_model', '05_gold_dimensions', '04_gold_model.ipynb', '05_gold_dimensions.ipynb')
""")

print("Monitoring reporting objects created: materialised rpt_* tables")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
