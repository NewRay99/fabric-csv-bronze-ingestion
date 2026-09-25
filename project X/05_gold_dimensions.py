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

# # 05 — Gold dimensions
#
# Build reporting dimensions and bridges only from available Silver entities. The notebook fails before writing if an expected source or column is absent. It does not fabricate source-system closure, reopen, or status-history data.

# CELL ********************

AS_OF_DATE = ""  # Optional YYYY-MM-DD, passed by archive replay.
SILVER_SCHEMA = "silver"
GOLD_SCHEMA = "gold"
JOB_RUN_ID = ""  # Parent orchestration correlation ID.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from datetime import datetime
import uuid

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")
RUN_STARTED_AT = datetime.utcnow()
GOLD_EXPORT_DATE = AS_OF_DATE or RUN_STARTED_AT.date().isoformat()
GOLD_JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def require_columns(source_table, required_columns):
    if not spark.catalog.tableExists(source_table):
        raise ValueError(f"Required Silver source is missing: {source_table}")
    actual = {field.name.lower() for field in spark.table(source_table).schema.fields}
    missing = sorted(set(required_columns) - actual)
    if missing:
        raise ValueError(f"{source_table} is missing required columns: {missing}")


def latest_dimension(source_table, target_table, key_columns, select_columns):
    """Write one current row per natural key from an available Silver source."""
    require_columns(source_table, key_columns + [source for source, _ in select_columns])
    frame = spark.table(source_table)
    order_columns = [
        F.col("export_date").cast("timestamp").desc_nulls_last(),
        F.col("_silver_load_ts").cast("timestamp").desc_nulls_last(),
    ]
    current = (
        frame.withColumn(
            "_gold_dimension_rank",
            F.row_number().over(Window.partitionBy(*key_columns).orderBy(*order_columns)),
        )
        .where(F.col("_gold_dimension_rank") == 1)
        .drop("_gold_dimension_rank")
    )
    dimension = current.select(
        *[F.col(source).alias(target) for source, target in select_columns],
        F.col("export_date").cast("timestamp").alias("export_date"),
        F.lit(GOLD_JOB_RUN_ID).alias("job_run_id"),
    )
    (dimension.write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true").saveAsTable(target_table))
    print(f"{target_table}: {dimension.count():,} rows from {source_table}")


def copy_bridge(source_table, target_table, required_columns, select_columns, key_columns=None):
    require_columns(source_table, required_columns)
    bridge = spark.table(source_table).select(
        *[F.col(source).alias(target) for source, target in select_columns],
        F.col("export_date").cast("timestamp").alias("export_date"),
        F.lit(GOLD_JOB_RUN_ID).alias("job_run_id"),
    ).dropDuplicates()
    if key_columns:
        # Export metadata must not turn one category link into several links.
        tie_breakers = [F.col(name).cast("string").desc_nulls_last()
                        for name in sorted(bridge.columns) if name not in key_columns]
        bridge = (bridge.withColumn("_bridge_rank", F.row_number().over(
            Window.partitionBy(*key_columns).orderBy(F.col("export_date").desc_nulls_last(), *tie_breakers)))
            .where("_bridge_rank = 1").drop("_bridge_rank"))
    (bridge.write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true").saveAsTable(target_table))
    print(f"{target_table}: {bridge.count():,} rows from {source_table}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_date AS
SELECT
  date_value AS date,
  YEAR(date_value) AS calendar_year,
  QUARTER(date_value) AS calendar_quarter,
  MONTH(date_value) AS calendar_month_number,
  DATE_FORMAT(date_value, 'MMMM') AS calendar_month_name,
  DATE_FORMAT(date_value, 'yyyy-MM') AS year_month,
  DAYOFWEEK(date_value) AS day_of_week_number,
  DATE_FORMAT(date_value, 'EEEE') AS day_of_week_name,
  DAYOFMONTH(date_value) AS day_of_month,
  CASE WHEN DAYOFWEEK(date_value) IN (1, 7) THEN false ELSE true END AS is_weekday,
  CAST('{GOLD_EXPORT_DATE}' AS TIMESTAMP) AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM (
  SELECT EXPLODE(SEQUENCE(DATE '2020-01-01', DATE '2035-12-31', INTERVAL 1 DAY)) AS date_value
)
""")

latest_dimension(
    "silver.holding_company", "gold.dim_holding_company", ["holding_company_id"],
    [("holding_company_id", "holding_company_id"), ("company_name", "company_name"),
     ("town_city", "town_city"), ("county", "county"), ("postcode", "postcode"),
     ("country", "country"), ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.provider", "gold.dim_provider", ["provider_id"],
    [("provider_id", "provider_id"), ("holding_company_id", "holding_company_id"),
     ("provider_name", "provider_name"), ("provider_status", "provider_status"),
     ("town_city", "town_city"), ("county", "county"), ("postcode", "postcode"),
     ("country", "country"), ("qa_flag", "qa_flag"),
     ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.provider_home", "gold.dim_provider_home", ["provider_home_id"],
    [("provider_home_id", "provider_home_id"), ("provider_id", "provider_id"),
     ("service_type", "service_type"), ("home_name", "home_name"),
     ("town_city", "town_city"), ("county", "county"), ("postcode", "postcode"),
     ("number_of_registered_beds", "registered_beds"), ("is_spot", "is_spot"),
     ("home_contact_number", "home_contact_number"),
     ("registered_manager_contact_number", "registered_manager_contact_number"),
     ("qa_flag", "qa_flag"), ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.framework", "gold.dim_framework", ["framework_code"],
    [("framework_code", "framework_code"), ("framework_name", "framework_name"),
     ("placement_type", "placement_type"), ("start_date", "start_date"),
     ("end_date", "end_date"), ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.framework_category", "gold.dim_framework_category", ["framework_category_id"],
    [("framework_category_id", "framework_category_id"), ("framework_code", "framework_code"),
     ("category_name", "category_name"), ("export_date", "source_export_date")],
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

copy_bridge(
    "silver.provider_framework", "gold.bridge_provider_framework",
    ["provider_framework_id", "provider_id", "framework_code", "qa_flag", "export_date"],
    [("provider_framework_id", "provider_framework_id"), ("provider_id", "provider_id"),
     ("framework_code", "framework_code"), ("qa_flag", "qa_flag"),
     ("export_date", "source_export_date")],
)
copy_bridge(
    "silver.provider_home_category", "gold.bridge_provider_home_framework_category",
    ["provider_home_category_id", "provider_home_id", "framework_category_id", "export_date"],
    [("provider_home_category_id", "provider_home_category_id"),
     ("provider_home_id", "provider_home_id"),
     ("framework_category_id", "framework_category_id"),
     ("export_date", "source_export_date")],
    key_columns=["provider_home_id", "framework_category_id"],
)
copy_bridge(
    "silver.referral_category", "gold.bridge_referral_framework_category",
    ["referral_id", "framework_category_id", "export_date"],
    [("referral_id", "referral_id"), ("framework_category_id", "framework_category_id"),
     ("export_date", "source_export_date")],
    key_columns=["referral_id", "framework_category_id"],
)
copy_bridge(
    "silver.provider_home_spot_category", "gold.bridge_provider_home_spot_category",
    ["provider_home_spot_category_id", "provider_home_id", "spot_category_code", "export_date"],
    [("provider_home_spot_category_id", "provider_home_spot_category_id"),
     ("provider_home_id", "provider_home_id"), ("spot_category_code", "spot_category_code"),
     ("export_date", "source_export_date")],
    key_columns=["provider_home_spot_category_id"],
)
copy_bridge(
    "silver.referral_spot_category", "gold.bridge_referral_spot_category",
    ["referral_spot_category_id", "referral_id", "spot_category", "export_date"],
    [("referral_spot_category_id", "referral_spot_category_id"),
     ("referral_id", "referral_id"), ("spot_category", "spot_category"),
     ("export_date", "source_export_date")],
    key_columns=["referral_spot_category_id"],
)
copy_bridge(
    "silver.provider_sic_codes", "gold.bridge_provider_sic_code",
    ["provider_id", "sic_code", "export_date"],
    [("provider_id", "provider_id"), ("sic_code", "sic_code"),
     ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.provider_submission_docs", "gold.dim_provider_submission_document", ["document_id"],
    [("document_id", "document_id"), ("submission_id", "submission_id"),
     ("s3_file_metadata_id", "s3_file_metadata_id"), ("document_name", "document_name"),
     ("document_type", "document_type"), ("expiry_date", "expiry_date"),
     ("last_updated", "last_updated"), ("next_review_date", "next_review_date"),
     ("service_type", "service_type"), ("home_id", "home_id"),
     ("start_date", "start_date"), ("export_date", "source_export_date")],
)

# GLD-014: keep provider messages as a current-record dimension and combine
# cancellation and decline reasons into one consistently named lookup. The
# prefixed key preserves provenance because the two source ID sequences are
# independent and can overlap.
latest_dimension(
    "silver.referral_provider_message", "gold.dim_referral_provider_message", ["message_id"],
    [("message_id", "message_id"), ("referral_provider_id", "referral_provider_id"),
     ("message_read_by", "message_read_by"),
     ("message_read_timestamp", "message_read_timestamp"),
     ("message_text", "message_text"), ("created_timestamp", "created_timestamp"),
     ("created_by", "created_by"), ("export_date", "source_export_date")],
)

for closure_source, required_columns in {
    "silver.referral_provider_cancel_reason": {
        "cancel_reason_id", "referral_provider_id", "cancel_reason",
        "cancel_reason_other_text", "created_by", "created_date", "export_date",
    },
    "silver.referral_provider_decline_reason": {
        "decline_reason_id", "referral_provider_id", "decline_reason",
        "decline_reason_other_text", "created_by", "created_date", "export_date",
    },
}.items():
    require_columns(closure_source, required_columns)

closure_reasons = spark.sql(f"""
WITH closure_source AS (
  SELECT CONCAT('cancel:', CAST(cancel_reason_id AS STRING)) AS closure_reason_id,
    referral_provider_id, 'cancel' AS closure_type, cancel_reason AS reason,
    cancel_reason_other_text AS reason_other, created_by,
    CAST(created_date AS TIMESTAMP) AS created_date,
    CAST(export_date AS TIMESTAMP) AS source_export_date
  FROM silver.referral_provider_cancel_reason
  UNION ALL
  SELECT CONCAT('decline:', CAST(decline_reason_id AS STRING)) AS closure_reason_id,
    referral_provider_id, 'decline' AS closure_type, decline_reason AS reason,
    decline_reason_other_text AS reason_other, created_by,
    CAST(created_date AS TIMESTAMP) AS created_date,
    CAST(export_date AS TIMESTAMP) AS source_export_date
  FROM silver.referral_provider_decline_reason
), current_closure_reason AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY closure_reason_id
    ORDER BY source_export_date DESC NULLS LAST
  ) AS closure_reason_snapshot_rank
  FROM closure_source
), cleaned_closure_reason AS (
  SELECT closure_reason_id, referral_provider_id, closure_type, reason, reason_other,
    created_by, created_date, source_export_date,
    CASE
      WHEN TRIM(COALESCE(reason_other, reason, '')) = ''
        THEN 'No reason recorded'
      WHEN LOWER(TRIM(COALESCE(reason_other, reason, ''))) = 'test'
        THEN CAST(NULL AS STRING)
      ELSE TRIM(COALESCE(reason_other, reason))
    END AS closure_reason_clean
  FROM current_closure_reason
  WHERE closure_reason_snapshot_rank = 1
), grouped_closure_reason AS (
  SELECT *,
    CASE
      WHEN closure_reason_clean IS NULL
        OR LOWER(closure_reason_clean) = 'no reason recorded'
        THEN 'No reason recorded'
      WHEN LOWER(closure_reason_clean) LIKE '%location%'
        THEN 'Location / Matching issue'
      WHEN LOWER(closure_reason_clean) LIKE '%off portal%'
        OR LOWER(closure_reason_clean) LIKE '%not on the portal%'
        OR LOWER(closure_reason_clean) LIKE '%doesn''t have access%'
        THEN 'Off-portal / alternative placement'
      WHEN LOWER(closure_reason_clean) LIKE '%placed%'
        OR LOWER(closure_reason_clean) LIKE '%moved%'
        THEN 'Placement found elsewhere'
      WHEN LOWER(closure_reason_clean) LIKE '%case closed%'
        OR LOWER(closure_reason_clean) LIKE '%remove%'
        OR LOWER(closure_reason_clean) LIKE '%update%'
        THEN 'Case / administrative closure'
      WHEN LOWER(closure_reason_clean) LIKE '%email%'
        OR LOWER(closure_reason_clean) LIKE '%portal not working%'
        THEN 'System / process issue'
      ELSE 'Other'
    END AS closure_reason_grouped
  FROM cleaned_closure_reason
), ranked_closure_reason AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY created_date DESC NULLS LAST,
      source_export_date DESC NULLS LAST,
      closure_reason_id DESC
  ) AS sequence_order
  FROM grouped_closure_reason
)
SELECT closure_reason_id, referral_provider_id, closure_type, reason, reason_other,
  closure_reason_clean, closure_reason_grouped,
  closure_reason_grouped AS closed_referral_reason_bucket,
  sequence_order, created_by, created_date, source_export_date,
  source_export_date AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM ranked_closure_reason
""")
(closure_reasons.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold.dim_referral_provider_closure_reason"))
print("gold.dim_referral_provider_closure_reason: "
      f"{closure_reasons.count():,} rows from cancellation and decline reasons")

require_columns("silver.referral", ["placement_type", "referral_status", "export_date"])
require_columns("silver.ipa", ["placement_type", "export_date"])
placement_types = (
    spark.table("silver.referral").select(
        F.col("placement_type").alias("placement_type"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .unionByName(spark.table("silver.ipa").select(
        F.col("placement_type").alias("placement_type"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    ))
    .where(F.col("placement_type").isNotNull() & (F.trim(F.col("placement_type")) != ""))
    .groupBy("placement_type").agg(F.max("export_date").alias("export_date"))
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(placement_types.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_placement_type"))

referral_statuses = (
    spark.table("silver.referral").select(
        F.col("referral_status").alias("referral_status"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .where(F.col("referral_status").isNotNull() & (F.trim(F.col("referral_status")) != ""))
    .groupBy("referral_status").agg(F.max("export_date").alias("export_date"))
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(referral_statuses.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_referral_status"))

# A separate month dimension keeps state-at-snapshot time intelligence away
# from the active referral-created date role. One row is emitted per calendar
# month and the month_start key joins directly to the snapshot fact.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.dim_snapshot_month AS
SELECT
  date_value AS month_start,
  LAST_DAY(date_value) AS month_end,
  YEAR(date_value) AS calendar_year,
  MONTH(date_value) AS calendar_month_number,
  DATE_FORMAT(date_value, 'MMMM') AS calendar_month_name,
  DATE_FORMAT(date_value, 'yyyy-MM') AS year_month,
  CAST('{GOLD_EXPORT_DATE}' AS TIMESTAMP) AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM (
  SELECT EXPLODE(SEQUENCE(DATE '2020-01-01', DATE '2035-12-01', INTERVAL 1 MONTH)) AS date_value
)
""")

# Dynamic RLS inputs. The setup notebook creates these configuration tables
# empty, so a newly deployed role denies detail until explicitly approved
# mappings are loaded. Effective dates are applied in Gold to keep the model
# role small and deterministic.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.dim_security_scope AS
SELECT security_scope_key, UPPER(TRIM(scope_type)) AS scope_type,
  TRIM(scope_code) AS scope_code, scope_name,
  COALESCE(allows_global_summary, false) AS allows_global_summary,
  valid_from, valid_to, approved_by, updated_at,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_security_scope
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")
spark.sql(f"""
CREATE OR REPLACE TABLE gold.sec_user_scope_access AS
SELECT LOWER(TRIM(user_principal_name)) AS user_principal_name,
  security_scope_key, valid_from, valid_to, approved_by, access_reason,
  updated_at, '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_user_scope_access
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")
spark.sql(f"""
CREATE OR REPLACE TABLE gold.bridge_referral_scope AS
SELECT CAST(referral_id AS STRING) AS referral_id, security_scope_key,
  valid_from, valid_to, assigned_by, assignment_reason, updated_at,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_referral_scope
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")

# GLD-006/GLD-007: person dimension with the legacy "Gender Clean" mapping.
# One current row per person; fact_referral[person_id] relates to this
# dimension for the gender KPIs (KPI-04-07). Null/unrecognised gender
# becomes "Unknown", matching the legacy model behaviour.
require_columns(
    "silver.referral_person",
    ["person_id", "initials", "age_value", "age_date_unit", "has_restrictions",
     "gender", "ethnicity", "religion", "preferred_language", "export_date"],
)
person_current = (
    spark.table("silver.referral_person")
    .withColumn(
        "_gold_dimension_rank",
        F.row_number().over(
            Window.partitionBy("person_id").orderBy(
                F.col("export_date").cast("timestamp").desc_nulls_last(),
                F.col("_silver_load_ts").cast("timestamp").desc_nulls_last(),
            )
        ),
    )
    .where(F.col("_gold_dimension_rank") == 1)
)
dim_person = person_current.select(
    F.col("person_id").alias("person_id"),
    F.col("initials").alias("initials"),
    F.col("age_value").alias("age_value"),
    F.col("age_date_unit").alias("age_date_unit"),
    F.col("has_restrictions").alias("has_restrictions"),
    F.col("gender").alias("gender"),
    F.when(F.col("gender") == "Male", "Male")
    .when(F.col("gender") == "Female", "Female")
    .when(F.col("gender").isin("Another Gender", "Other"), "Other")
    .otherwise("Unknown")
    .alias("gender_clean"),
    F.col("ethnicity").alias("ethnicity"),
    F.col("religion").alias("religion"),
    F.col("preferred_language").alias("preferred_language"),
    F.col("export_date").cast("timestamp").alias("export_date"),
    F.lit(GOLD_JOB_RUN_ID).alias("job_run_id"),
    F.col("export_date").alias("source_export_date"),
)
(dim_person.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_person"))
print(f"gold.dim_person: {dim_person.count():,} rows from silver.referral_person")

# GLD-008: offer-status dimension with labels and lifecycle flags, rebuilt
# from the distinct offer_status codes observed in Silver. Unknown future
# codes are kept with a null label, matching the legacy model behaviour.
require_columns("silver.offer", ["offer_status", "export_date"])
offer_statuses = (
    spark.table("silver.offer")
    .select(
        F.col("offer_status").alias("offer_status"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .where(F.col("offer_status").isNotNull() & (F.trim(F.col("offer_status")) != ""))
    .groupBy("offer_status").agg(F.max("export_date").alias("export_date"))
    .withColumn(
        "offer_status_label",
        F.when(F.col("offer_status") == "OFFER_SUCCESSFUL", "Accepted")
        .when(F.col("offer_status") == "DRAFT", "Draft")
        .when(F.col("offer_status") == "OFFER_MADE", "Pending")
        .when(F.col("offer_status") == "OFFER_UNSUCCESSFUL", "Unsuccessful")
        .when(F.col("offer_status") == "OFFER_WITHDRAWN", "Withdrawn"),
    )
    .withColumn("is_active_offer", F.col("offer_status") == "OFFER_MADE")
    .withColumn("is_accepted", F.col("offer_status") == "OFFER_SUCCESSFUL")
    .withColumn(
        "is_terminal",
        F.col("offer_status").isin("OFFER_UNSUCCESSFUL", "OFFER_WITHDRAWN"),
    )
    .withColumn(
        "offer_status_sk",
        F.row_number().over(Window.orderBy("offer_status")),
    )
    .select(
        "offer_status_sk", "offer_status", "offer_status_label",
        "is_active_offer", "is_accepted", "is_terminal", "export_date",
    )
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(offer_statuses.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_offer_status"))
print(f"gold.dim_offer_status: {offer_statuses.count():,} rows from silver.offer")

print(f"Gold dimensions completed; AS_OF_DATE={AS_OF_DATE or 'latest'}; started={RUN_STARTED_AT.isoformat()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
