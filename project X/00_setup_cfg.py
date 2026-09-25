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
# META     },
# META     "warehouse": {
# META       "known_warehouses": []
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Central configuration setup
#
# Creates and upgrades every ETL configuration table before any pipeline notebook reads or writes configuration state.

# PARAMETERS CELL ********************

# Parameters
AUDIT_TABLE = "monitoring.cfg_silver_export_load"
TIME_PARSER_POLICY = "CORRECTED"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.


LOAD_FILE_CONFIG = False  # Set True for an intentional one-off bootstrap/reload.
SCHEMA_CONTRACT_CSV_PATH = "Files/cfg_files/schema_definition.csv"
DQ_RULE_CSV_PATH = "Files/cfg_files/dq_rule_definition.csv"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)


def qident(value):
    return "`" + str(value).replace("`", "``") + "`"


def qualified_name(table_name):
    schema_name, object_name = table_name.split(".", 1)
    return f"{qident(schema_name)}.{qident(object_name)}"


def ensure_delta_table(table_name, column_definitions):
    # Create a config table and add fields missing from an older deployment.
    schema_name, _ = table_name.split(".", 1)
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qident(schema_name)}")
    ddl_columns = ",\n  ".join(column_definitions)
    spark.sql(
        f"CREATE TABLE IF NOT EXISTS {qualified_name(table_name)} (\n"
        f"  {ddl_columns}\n) USING DELTA"
    )
    existing = {field.name.lower() for field in spark.table(table_name).schema.fields}
    missing = [
        definition for definition in column_definitions
        if definition.split()[0].lower() not in existing
    ]
    if missing:
        spark.sql(
            f"ALTER TABLE {qualified_name(table_name)} "
            f"ADD COLUMNS ({', '.join(missing)})"
        )
        print(f"Upgraded {table_name}: {missing}")
    return missing

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

CONFIG_TABLE_DEFINITIONS = {
    # Approved local reference data only. Setup never seeds or replaces coordinates.
    "monitoring.cfg_location_coordinate": [
        "location_type STRING", "location_key STRING", "latitude DOUBLE",
        "longitude DOUBLE", "reference_source STRING", "reference_version STRING",
    ],
    "monitoring.cfg_silver_export_load": [
        "source_kind STRING", "source_schema STRING", "source_table STRING",
        "target_table STRING", "export_date TIMESTAMP", "status STRING",
        "reload BOOLEAN", "attempt_count INT", "run_id STRING",
        "rows_read BIGINT", "rows_written BIGINT", "duplicate_key_count BIGINT",
        "started_at TIMESTAMP", "ended_at TIMESTAMP", "error_message STRING",
        "last_updated_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_pipeline_run": [
        "run_id STRING", "pipeline_name STRING", "layer STRING",
        "source_kind STRING", "started_at TIMESTAMP", "ended_at TIMESTAMP",
        "status STRING", "tables_succeeded INT", "tables_failed INT",
        "rows_read BIGINT", "rows_written BIGINT", "error_message STRING",
        "job_run_id STRING",
    ],
    "monitoring.cfg_table_load_metric": [
        "run_id STRING", "layer STRING", "source_kind STRING",
        "source_object STRING", "target_object STRING", "rows_read BIGINT",
        "rows_written BIGINT", "duplicate_key_count BIGINT",
        "null_primary_key_count BIGINT", "recorded_at TIMESTAMP",
        "job_run_id STRING",
    ],
    "monitoring.cfg_job_run": [
        "job_run_id STRING", "pipeline_name STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "status STRING", "steps_succeeded INT",
        "steps_failed INT", "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_job_step_run": [
        "job_run_id STRING", "step_sequence INT", "notebook_name STRING",
        "started_at TIMESTAMP", "ended_at TIMESTAMP", "status STRING",
        "child_result STRING", "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_drift_definition": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
        "join_class STRING", "join_evidence STRING",
        "definition_hash STRING", "definition_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_drift_event": [
        "run_id STRING", "source_kind STRING", "source_table STRING",
        "target_table STRING", "drift_type STRING", "column_name STRING",
        "expected_type STRING", "actual_type STRING", "referenced_table STRING",
        "referenced_column STRING", "drift_key STRING", "status STRING",
        "occurrence_count BIGINT", "first_detected_at TIMESTAMP",
        "last_detected_at TIMESTAMP", "resolved_at TIMESTAMP",
        "detected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_month_end_gold_run": [
        "snapshot_date DATE", "status STRING", "reload BOOLEAN",
        "attempt_count INT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "dq_result STRING", "gold_result STRING",
        "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_zip_load": [
        "zip_path STRING", "export_date TIMESTAMP", "extract_path STRING",
        "status STRING", "reload BOOLEAN", "attempt_count INT",
        "file_count INT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "error_message STRING",
        "first_loaded_at TIMESTAMP", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_file_load": [
        "file_path STRING", "filename STRING", "export_date TIMESTAMP",
        "source_zip STRING", "target_object STRING", "status STRING",
        "reload BOOLEAN", "attempt_count INT", "rows_read BIGINT",
        "rows_written BIGINT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "error_message STRING",
        "first_loaded_at TIMESTAMP", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_table_export_load": [
        "source_schema STRING", "source_table STRING", "export_date TIMESTAMP",
        "status STRING", "reload BOOLEAN", "row_count BIGINT",
        "run_id STRING", "first_seen_at TIMESTAMP",
        "last_updated_at TIMESTAMP", "error_message STRING",
    ],
    "monitoring.cfg_schema_contract_column": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
        "join_class STRING", "join_evidence STRING",
        "contract_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_bronze_schema_live": [
        "table_name STRING", "ordinal_position INT", "column_name STRING",
        "live_data_type STRING", "is_nullable BOOLEAN",
        "captured_at TIMESTAMP", "run_id STRING", "job_run_id STRING",
    ],
    "monitoring.cfg_archived_schema_live": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "contract_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_definition_candidate": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
    ],
    "monitoring.cfg_data_quality_result": [
        "run_id STRING", "rule_id STRING", "severity STRING",
        "rule_type STRING", "source_table STRING", "column_name STRING",
        "status STRING", "failed_row_count BIGINT", "checked_row_count BIGINT",
        "failure_percentage DOUBLE", "sample_key_json STRING",
        "checked_at TIMESTAMP", "message STRING", "job_run_id STRING",
    ],
    "monitoring.cfg_rejected_row": [
        "run_id STRING", "rule_id STRING", "source_table STRING",
        "business_key_json STRING", "rejection_reason STRING",
        "rejected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_referential_exception": [
        "run_id STRING", "rule_id STRING", "child_table STRING",
        "child_column STRING", "child_key STRING", "parent_table STRING",
        "parent_column STRING", "detected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_data_domain": [
        "source_schema STRING", "source_table STRING", "column_name STRING",
        "contract_data_type STRING", "data_domain STRING",
        "distinct_value_count BIGINT", "profiled_at TIMESTAMP",
        "run_id STRING", "job_run_id STRING",
    ],
    "monitoring.cfg_data_quality_rule": [
        "rule_id STRING", "active STRING", "severity STRING",
        "rule_type STRING", "source_schema STRING", "table_name STRING",
        "column_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "operator STRING", "rule_value STRING", "description STRING",
        "loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_gold_lineage_mapping": [
        "gold_object STRING", "source_object STRING", "source_layer STRING",
        "transformation_notebook STRING", "relationship_role STRING",
        "is_required BOOLEAN", "description STRING",
    ],
    # Security mappings are deliberately configuration-driven. Empty tables
    # produce deny-by-default RLS once the semantic-model role is deployed;
    # access is never inferred from the currently-null fact_referral.region.
    "monitoring.cfg_security_scope": [
        "security_scope_key STRING", "scope_type STRING", "scope_code STRING",
        "scope_name STRING", "allows_global_summary BOOLEAN", "is_active BOOLEAN",
        "valid_from DATE", "valid_to DATE", "approved_by STRING",
        "updated_at TIMESTAMP",
    ],
    "monitoring.cfg_user_scope_access": [
        "user_principal_name STRING", "security_scope_key STRING",
        "is_active BOOLEAN", "valid_from DATE", "valid_to DATE",
        "approved_by STRING", "access_reason STRING", "updated_at TIMESTAMP",
    ],
    "monitoring.cfg_referral_scope": [
        "referral_id STRING", "security_scope_key STRING", "is_active BOOLEAN",
        "valid_from DATE", "valid_to DATE", "assigned_by STRING",
        "assignment_reason STRING", "updated_at TIMESTAMP",
    ],
    "gold.cfg_placement_urgency_rule": [
        "PlacementUrgencyBand STRING", "MaximumTargetDays INT",
        "WarningHoursBeforeTarget INT", "SortOrder INT", "IsActive BOOLEAN",
    ],
}


upgraded_tables = {}
for config_table, definitions in CONFIG_TABLE_DEFINITIONS.items():
    missing_columns = ensure_delta_table(config_table, definitions)
    if missing_columns:
        upgraded_tables[config_table] = missing_columns

print(
    f"Configuration tables ready: {len(CONFIG_TABLE_DEFINITIONS)}; "
    f"upgraded: {len(upgraded_tables)}"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Stable Gold configuration belongs to setup, not the Gold model notebook.
spark.sql("""
MERGE INTO gold.cfg_placement_urgency_rule AS t
USING (
  SELECT * FROM VALUES
    ('Critical', 1, 6, 1, true), ('High', 3, 24, 2, true),
    ('Medium', 7, 48, 3, true), ('Planned', 99999, 72, 4, true),
    ('Unspecified', 99999, 72, 5, true)
  AS v(PlacementUrgencyBand, MaximumTargetDays, WarningHoursBeforeTarget, SortOrder, IsActive)
) AS s
ON t.PlacementUrgencyBand = s.PlacementUrgencyBand
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")
print("Configuration setup completed")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# One-off configuration bootstrap.
# Child notebooks read the Delta tables below; they never read the CSV files.
from pyspark.sql import functions as F
def bootstrap_csv_table(csv_path, target_table, required_columns):
    if not LOAD_FILE_CONFIG and spark.catalog.tableExists(target_table):
        # Setup creates the table shell before this cell runs. Only skip the
        # import when the existing table actually contains configuration rows.
        if spark.table(target_table).limit(1).count() > 0:
            print(f"Using existing populated {target_table}; CSV bootstrap not requested")
            return
        print(f"{target_table} exists but is empty; loading the CSV bootstrap")
    frame = (spark.read.format("csv").option("header", "true")
        .option("quote", '"').option("escape", '"').option("multiLine", "true")
        # schema_definition.csv includes quoted multiline descriptions and
        # mixed CRLF/LF line endings. Pin LF so Spark does not absorb a
        # following contract row into the preceding final field.
        .option("lineSep", "\n")
        .load(csv_path))
    # lineSep=LF preserves all mixed-ending CSV rows, but retains a trailing
    # CR on the final header when the file starts with CRLF. Normalise headers
    # before checking the schema or writing the configuration table.
    frame = frame.toDF(*[column.strip() for column in frame.columns])
    missing = set(required_columns) - set(frame.columns)
    if missing:
        raise ValueError(f"{csv_path} is missing required columns: {sorted(missing)}")
    if frame.rdd.isEmpty():
        raise ValueError(f"{csv_path} is empty")
    (frame.withColumn("contract_loaded_at", F.current_timestamp())
        .write.format("delta").mode("overwrite").option("overwriteSchema", "true")
        .saveAsTable(target_table))
    print(f"Loaded {csv_path} into {target_table}: {frame.count():,} rows")


def validate_csv_target_parity(csv_path, target_table, required_columns):
    """Fail a requested reload if the target loses or gains CSV rows."""
    source = (spark.read.format("csv").option("header", "true")
        .option("quote", '"').option("escape", '"').option("multiLine", "true")
        .option("lineSep", "\n")
        .load(csv_path))
    source = source.toDF(*[column.strip() for column in source.columns])
    missing = set(required_columns) - set(source.columns)
    if missing:
        raise ValueError(f"{csv_path} is missing required columns: {sorted(missing)}")
    source_columns = source.columns
    target = spark.table(target_table).select(*source_columns)
    source_count = source.count()
    target_count = target.count()
    missing_target_rows = source.exceptAll(target).count()
    unexpected_target_rows = target.exceptAll(source).count()
    if source_count != target_count or missing_target_rows or unexpected_target_rows:
        raise ValueError(
            f"CSV/target parity failed for {target_table}: "
            f"source_rows={source_count}, target_rows={target_count}, "
            f"missing_target_rows={missing_target_rows}, "
            f"unexpected_target_rows={unexpected_target_rows}"
        )
    print(f"CSV/target parity passed for {target_table}: {source_count:,} rows")

bootstrap_csv_table(
    SCHEMA_CONTRACT_CSV_PATH,
    "monitoring.cfg_schema_contract_column",
    ["table_name", "ordinal_position", "column_name", "data_type", "is_nullable",
     "is_primary_key", "referenced_schema", "referenced_table", "referenced_column",
     "join_class", "join_evidence"],
)
bootstrap_csv_table(
    DQ_RULE_CSV_PATH,
    "monitoring.cfg_data_quality_rule",
    ["rule_id", "active", "severity", "rule_type", "source_schema", "table_name",
     "column_name", "referenced_schema", "referenced_table", "referenced_column",
     "operator", "rule_value", "description"],
)

# A requested file reload must prove both source CSVs reached their Delta
# targets without excluded, missing or unexpected rows. Normal runs keep
# existing runtime configuration and therefore do not assert parity.
if LOAD_FILE_CONFIG:
    validate_csv_target_parity(
        SCHEMA_CONTRACT_CSV_PATH,
        "monitoring.cfg_schema_contract_column",
        ["table_name", "ordinal_position", "column_name", "data_type", "is_nullable",
         "is_primary_key", "referenced_schema", "referenced_table", "referenced_column",
         "join_class", "join_evidence"],
    )
    validate_csv_target_parity(
        DQ_RULE_CSV_PATH,
        "monitoring.cfg_data_quality_rule",
        ["rule_id", "active", "severity", "rule_type", "source_schema", "table_name",
         "column_name", "referenced_schema", "referenced_table", "referenced_column",
         "operator", "rule_value", "description"],
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Gold lineage mapping is configuration; 06_reports defines the reporting views.
spark.sql("""
MERGE INTO monitoring.cfg_gold_lineage_mapping AS target
USING (
  SELECT * FROM VALUES
    ('gold.fact_referral', 'silver.referral', 'SILVER', '04_gold_model', 'PRIMARY', true, 'Current referral reporting fact'),
    ('gold.fact_referral', 'silver.referral_category', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Single category key only when unambiguous; full membership retained in bridge'),
    ('gold.fact_referral', 'silver.referral_location', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Generalised preference city with default and review flags'),
    ('gold.fact_offer', 'silver.offer', 'SILVER', '04_gold_model', 'PRIMARY', true, 'Offer grain and proposed framework category'),
    ('gold.fact_offer', 'silver.provider_home_category', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Home category roll-up without multiplying offers'),
    ('gold.fact_offer', 'silver.referral_location', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Approximate city-centroid distance origin'),
    ('gold.fact_offer', 'silver.provider_home_location', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Locally matched postcode coordinates; distance provenance retained'),
    ('gold.fact_referral', 'silver.offer', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Offer roll-up'),
    ('gold.fact_referral', 'silver.referral_provider', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Referral/provider bridge'),
    ('gold.fact_referral', 'silver.ipa', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Placement agreement roll-up'),
    ('gold.fact_referral', 'silver.referral_lifecycle_event', 'SILVER', '04_gold_model', 'SUPPORTING', true, 'Derived referral lifecycle events'),
    ('gold.fact_referral_lifecycle_event', 'silver.referral_lifecycle_event', 'SILVER', '04_gold_model', 'PRIMARY', true, 'Referral lifecycle event fact'),
    ('gold.dim_holding_company', 'silver.holding_company', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Holding company dimension'),
    ('gold.dim_provider', 'silver.provider', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider dimension'),
    ('gold.dim_provider_home', 'silver.provider_home', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider home dimension'),
    ('gold.dim_framework', 'silver.framework', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Framework dimension'),
    ('gold.dim_framework_category', 'silver.framework_category', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Framework category dimension'),
    ('gold.bridge_provider_home_framework_category', 'silver.provider_home_category', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider-home/framework-category bridge used for category-scoped provider KPI analysis'),
    ('gold.bridge_referral_framework_category', 'silver.referral_category', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Complete referral/framework category membership'),
    ('gold.bridge_provider_home_spot_category', 'silver.provider_home_spot_category', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider-home spot categories preserving source field names'),
    ('gold.bridge_referral_spot_category', 'silver.referral_spot_category', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Referral spot categories preserving source field names'),
    ('gold.bridge_provider_framework', 'silver.provider_framework', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider/framework bridge'),
    ('gold.bridge_provider_sic_code', 'silver.provider_sic_codes', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider SIC bridge'),
    ('gold.dim_provider_submission_document', 'silver.provider_submission_docs', 'SILVER', '05_gold_dimensions', 'PRIMARY', true, 'Provider submission-document dimension'),
    ('gold.dim_placement_type', 'silver.referral', 'SILVER', '05_gold_dimensions', 'DERIVED', true, 'Distinct referral placement types'),
    ('gold.dim_referral_status', 'silver.referral', 'SILVER', '05_gold_dimensions', 'DERIVED', true, 'Distinct referral statuses'),
    ('gold.dim_snapshot_month', 'gold.dim_date', 'GOLD', '05_gold_dimensions', 'DERIVED', true, 'Dedicated month role for state-at-snapshot reporting'),
    ('gold.dim_security_scope', 'monitoring.cfg_security_scope', 'CONFIG', '05_gold_dimensions', 'SECURITY', true, 'Approved reporting security scopes'),
    ('gold.sec_user_scope_access', 'monitoring.cfg_user_scope_access', 'CONFIG', '05_gold_dimensions', 'SECURITY', true, 'Normalised UPN-to-scope access mapping'),
    ('gold.bridge_referral_scope', 'monitoring.cfg_referral_scope', 'CONFIG', '05_gold_dimensions', 'SECURITY', true, 'Many-to-many referral-to-security-scope mapping'),
    ('gold.fact_provider_kpi_monthly', 'gold.fact_referral_provider', 'GOLD', '04_gold_model', 'DERIVED', true, 'Auditable unweighted provider KPI components by assignment cohort month'),
    ('gold.fact_referral_global_summary', 'gold.fact_referral_snapshot', 'GOLD', '04_gold_model', 'DERIVED', true, 'Identifier-free monthly snapshot summary for approved partial-RLS visuals')
  AS source(gold_object, source_object, source_layer, transformation_notebook,
            relationship_role, is_required, description)
) AS source
ON target.gold_object = source.gold_object
 AND target.source_object = source.source_object
WHEN MATCHED THEN UPDATE SET *
WHEN NOT MATCHED THEN INSERT *
""")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
