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

from datetime import datetime, timezone
import uuid

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")
RUN_STARTED_AT = datetime.now(timezone.utc)
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

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Provider registry extract
# GLD-023 replaces the legacy Fostering-only queries with the COMPLETE
# dim_provider LEFT dim_provider_home population. No membership or activity is required.
# Contacts stay in this separate extract, not the general provider dimension.
# All framework memberships are optional, sorted/distinct descriptive attributes.
# This is a current directory, not a historical/as-of provider registry.

# CELL ********************


def provider_registry_columns():
    """Provider-source fields required by the legacy registry extract."""
    return [
        "provider_id", "holding_company_id", "provider_name", "provider_status",
        "town_city", "county", "postcode", "country", "qa_flag",
        "provider_email_address", "provider_phone_number",
        "responsible_individual_name", "responsible_individual_contact_number",
        "responsible_individual_email_address", "registrant_name", "registrant_role",
        "registrant_email_address", "registrant_contact_number",
    ]


def provider_registry_sources(silver_schema, gold_schema):
    """Explicit source contract; no message bodies or invented home attribution."""
    return {
        f"{silver_schema}.provider_home": [
            "provider_home_id", "provider_id", "home_name", "service_type", "status",
            "address_line_1", "address_line_2", "town_city", "county", "postcode", "country",
            "home_contact_number", "home_email_address", "number_of_registered_beds", "is_spot",
            "export_date", "_silver_load_ts",
        ],
        f"{gold_schema}.fact_offer": [
            "offer_id", "provider_id", "provider_home_id", "offer_status",
            "referral_to_home_distance_km", "as_of_date", "source_export_date",
        ],
        f"{gold_schema}.fact_ipa": [
            "ipa_id", "accepted_offer_id", "signed_by_provider", "is_ipa_completed",
            "is_placement_closed", "planned_placement_start_date", "placement_admission_date",
            "placement_ended_date", "estimated_weekly_cost", "as_of_date", "source_export_date",
        ],
        f"{gold_schema}.fact_referral_provider": [
            "referral_provider_id", "provider_id", "is_declined", "response_elapsed_minutes",
            "as_of_date", "export_date",
        ],
        f"{silver_schema}.referral_provider_message": [
            "message_id", "referral_provider_id", "created_timestamp", "export_date", "_silver_load_ts",
        ],
    }


def provider_registry_baseline_columns(gold_schema):
    """Authoritative directory population and basic fields, never eligibility."""
    return {
        f"{gold_schema}.dim_provider": [
            "provider_id", "holding_company_id", "provider_name", "provider_status",
            "town_city", "county", "postcode", "country", "qa_flag", "source_export_date", "export_date",
        ],
        f"{gold_schema}.dim_provider_home": [
            "provider_home_id", "provider_id", "home_name", "service_type", "town_city", "county", "postcode",
            "registered_beds", "is_spot", "home_contact_number", "source_export_date",
        ],
    }


def provider_registry_sql(silver_schema, gold_schema, job_run_id, as_of_date=None):
    """Exactly dim_provider LEFT dim_provider_home, plus optional enrichment."""
    from datetime import date

    for schema in (silver_schema, gold_schema):
        if not schema.isascii() or not schema.isidentifier():
            raise ValueError("Registry schema names must be simple SQL identifiers")
    job_literal = str(job_run_id).replace("'", "''")
    metric_date = "CURRENT_DATE()"
    if as_of_date is not None:
        metric_date = f"CAST('{date.fromisoformat(str(as_of_date)).isoformat()}' AS DATE)"
    fields = provider_registry_columns()
    # Exact timestamp ties must not choose an arbitrary contact record. All
    # output provider fields participate; any remaining tie has identical output.
    tie_breakers = ",\n        ".join(
        f"CAST({name} AS STRING) DESC NULLS LAST"
        for name in sorted(fields) if name != "provider_id"
    )
    core_fields = provider_registry_baseline_columns(gold_schema)[f"{gold_schema}.dim_provider"]
    provider_projection = ",\n  ".join(
        f"CAST({'p' if name in core_fields else 'pc'}.{name} AS "
        f"{'BOOLEAN' if name == 'qa_flag' else 'STRING'}) AS {name}" for name in fields
    )
    # Deduplicate each natural key before aggregation or joining. All used fields
    # participate in ties; no fact-to-fact fan-out or averaging monthly averages.
    current_ctes = []
    for table, columns in provider_registry_sources(silver_schema, gold_schema).items():
        entity = table.split(".")[-1]
        natural_key = columns[0]
        order = [name for name in ("source_export_date", "export_date", "_silver_load_ts") if name in columns]
        order_sql = ", ".join(f"CAST({name} AS TIMESTAMP) DESC NULLS LAST" for name in order)
        ties = ", ".join(f"CAST({name} AS STRING) DESC NULLS LAST"
                         for name in sorted(columns) if name != natural_key and name not in order)
        current_ctes.append(f"""ranked_{entity} AS (
  SELECT {', '.join(columns)}, ROW_NUMBER() OVER (
    PARTITION BY {natural_key} ORDER BY {order_sql}, {ties}
  ) AS registry_rank FROM {table}
  WHERE {natural_key} IS NOT NULL AND TRIM(CAST({natural_key} AS STRING)) <> ''
), current_{entity} AS (
  SELECT * FROM ranked_{entity} WHERE registry_rank = 1
)""")
    metrics_ctes = []
    metrics_projection = []
    for grain, keys in (("provider", "provider_id"), ("home", "provider_id, provider_home_id")):
        metrics_ctes.append(f"""{grain}_offers AS (
  SELECT {keys}, COUNT(*) AS offer_count,
    SUM(CASE WHEN LOWER(TRIM(offer_status)) = 'draft' THEN 1 ELSE 0 END) AS draft_offer_count,
    SUM(CASE WHEN LOWER(TRIM(offer_status)) IN ('offer_successful', 'accepted', 'approved', 'selected')
      THEN 1 ELSE 0 END) AS accepted_offer_count,
    SUM(CASE WHEN LOWER(TRIM(offer_status)) IN ('offer_unsuccessful', 'declined', 'rejected')
      THEN 1 ELSE 0 END) AS rejected_offer_count,
    COUNT(CASE WHEN referral_to_home_distance_km >= 0 THEN 1 END) AS offers_with_distance_count,
    AVG(CASE WHEN referral_to_home_distance_km >= 0 THEN referral_to_home_distance_km END)
      AS average_offer_distance_km
  FROM current_fact_offer GROUP BY {keys}
), {grain}_ipas AS (
  SELECT {keys}, COUNT(*) AS ipa_count,
    SUM(CASE WHEN NOT COALESCE(is_placement_closed, false) THEN 1 ELSE 0 END) AS active_ipa_count,
    SUM(CASE WHEN signed_by_provider THEN 1 ELSE 0 END) AS provider_signed_ipa_count,
    SUM(CASE WHEN is_ipa_completed THEN 1 ELSE 0 END) AS completed_ipa_count,
    MAX(CASE WHEN signed_by_provider THEN 1 ELSE 0 END) = 1 AS has_provider_signed_ipa,
    MAX(CASE WHEN is_ipa_completed THEN 1 ELSE 0 END) = 1 AS has_completed_ipa,
    SUM(CASE WHEN NOT COALESCE(is_placement_closed, false) AND estimated_weekly_cost >= 0
      THEN estimated_weekly_cost END) AS estimated_active_weekly_cost,
    SUM(CASE WHEN NOT COALESCE(is_placement_closed, false)
      AND (estimated_weekly_cost IS NULL OR estimated_weekly_cost < 0) THEN 1 ELSE 0 END)
      AS active_ipas_missing_weekly_cost_count,
    SUM(estimated_lifetime_cost_to_date) AS estimated_lifetime_cost_to_date,
    SUM(CASE WHEN estimated_lifetime_cost_to_date IS NULL THEN 1 ELSE 0 END)
      AS ipas_missing_lifetime_cost_count
  FROM ipa_evidence GROUP BY {keys}
)""")
        for alias, columns in (("o", ["offer_count", "draft_offer_count", "accepted_offer_count",
                                      "rejected_offer_count", "offers_with_distance_count"]),
                               ("i", ["ipa_count", "active_ipa_count", "provider_signed_ipa_count",
                                      "completed_ipa_count", "active_ipas_missing_weekly_cost_count",
                                      "ipas_missing_lifetime_cost_count"])):
            metrics_projection.extend(f"COALESCE({grain}_{alias}.{name}, 0) AS {grain}_{name}" for name in columns)
        metrics_projection.extend([
            f"{grain}_o.average_offer_distance_km AS {grain}_average_offer_distance_km",
            f"COALESCE({grain}_i.has_provider_signed_ipa, false) AS {grain}_has_provider_signed_ipa",
            f"COALESCE({grain}_i.has_completed_ipa, false) AS {grain}_has_completed_ipa",
            # No IPAs (or no active IPAs) genuinely means zero. Present IPAs
            # with wholly missing cost evidence must remain NULL, not zero.
            f"CASE WHEN COALESCE({grain}_i.active_ipa_count, 0) = 0 THEN 0 "
            f"ELSE {grain}_i.estimated_active_weekly_cost END AS {grain}_estimated_active_weekly_cost",
            f"CASE WHEN COALESCE({grain}_i.ipa_count, 0) = 0 THEN 0 "
            f"ELSE {grain}_i.estimated_lifetime_cost_to_date END AS {grain}_estimated_lifetime_cost_to_date",
        ])
    metrics_projection_sql = ",\n  ".join(metrics_projection)
    return f"""
WITH {', '.join(current_ctes)}, ranked_provider AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY provider_id
    ORDER BY CAST(export_date AS TIMESTAMP) DESC NULLS LAST,
      CAST(_silver_load_ts AS TIMESTAMP) DESC NULLS LAST,
      {tie_breakers}
  ) AS registry_provider_rank
  FROM {silver_schema}.provider
  WHERE provider_id IS NOT NULL AND TRIM(CAST(provider_id AS STRING)) <> ''
), ranked_membership AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY provider_framework_id
    ORDER BY CAST(source_export_date AS TIMESTAMP) DESC NULLS LAST,
      CAST(provider_id AS STRING) DESC NULLS LAST,
      CAST(framework_code AS STRING) DESC NULLS LAST
  ) AS registry_membership_rank
  FROM {gold_schema}.bridge_provider_framework
  WHERE provider_framework_id IS NOT NULL
), membership_detail AS (
  SELECT DISTINCT CAST(b.provider_id AS STRING) AS provider_id,
    CAST(b.framework_code AS STRING) AS framework_code,
    CAST(f.placement_type AS STRING) AS placement_type
  FROM ranked_membership b
  LEFT JOIN {gold_schema}.dim_framework f ON f.framework_code = b.framework_code
  WHERE b.registry_membership_rank = 1
), provider_frameworks AS (
  SELECT provider_id,
    CONCAT_WS('; ', SORT_ARRAY(COLLECT_SET(framework_code))) AS framework_code,
    NULLIF(CONCAT_WS('; ', SORT_ARRAY(COLLECT_SET(placement_type))), '') AS placement_type,
    COUNT(DISTINCT framework_code) AS framework_count
  FROM membership_detail
  GROUP BY provider_id
), ipa_dates AS (
  SELECT i.*, o.provider_id, o.provider_home_id,
    CAST(COALESCE(i.planned_placement_start_date, i.placement_admission_date) AS DATE) AS cost_start_date,
    CASE WHEN CAST(i.placement_ended_date AS DATE) < {metric_date}
      THEN CAST(i.placement_ended_date AS DATE) ELSE {metric_date} END AS cost_end_date
  FROM current_fact_ipa i
  INNER JOIN current_fact_offer o ON o.offer_id = i.accepted_offer_id
), ipa_evidence AS (
  SELECT *, CASE
    WHEN cost_start_date IS NULL OR estimated_weekly_cost IS NULL OR estimated_weekly_cost < 0 THEN NULL
    WHEN is_placement_closed AND placement_ended_date IS NULL THEN NULL
    WHEN placement_ended_date IS NOT NULL AND CAST(placement_ended_date AS DATE) < cost_start_date THEN NULL
    WHEN cost_start_date > {metric_date} THEN 0
    ELSE estimated_weekly_cost * (DATEDIFF(cost_end_date, cost_start_date) + 1) / 7.0
    END AS estimated_lifetime_cost_to_date
  FROM ipa_dates
), {', '.join(metrics_ctes)}, provider_assignments AS (
  SELECT provider_id, COUNT(*) AS assignment_count,
    SUM(CASE WHEN is_declined THEN 1 ELSE 0 END) AS declined_assignment_count,
    COUNT(CASE WHEN response_elapsed_minutes >= 0 THEN 1 END) AS timed_response_count,
    AVG(CASE WHEN response_elapsed_minutes >= 0 THEN response_elapsed_minutes END) AS average_response_minutes
  FROM current_fact_referral_provider GROUP BY provider_id
), provider_messages AS (
  SELECT rp.provider_id, COUNT(DISTINCT m.message_id) AS message_count
  FROM current_referral_provider_message m
  INNER JOIN current_fact_referral_provider rp ON rp.referral_provider_id = m.referral_provider_id
  WHERE m.created_timestamp IS NULL OR CAST(m.created_timestamp AS DATE) <= {metric_date}
  GROUP BY rp.provider_id
)
SELECT
  {provider_projection},
  f.framework_code, COALESCE(f.framework_count, 0) AS framework_count,
  f.placement_type, CAST(h.home_name AS STRING) AS home_name,
  CAST(h.service_type AS STRING) AS service_type,
  CAST(h.provider_home_id AS STRING) AS provider_home_id,
  CAST(hc.status AS STRING) AS home_status,
  CAST(hc.address_line_1 AS STRING) AS home_address_line_1,
  CAST(hc.address_line_2 AS STRING) AS home_address_line_2,
  CAST(h.town_city AS STRING) AS home_town_city, CAST(h.county AS STRING) AS home_county,
  CAST(h.postcode AS STRING) AS home_postcode, CAST(hc.country AS STRING) AS home_country,
  CAST(h.home_contact_number AS STRING) AS home_contact_number,
  CAST(hc.home_email_address AS STRING) AS home_email_address,
  CAST(h.registered_beds AS BIGINT) AS home_registered_beds,
  CAST(h.is_spot AS BOOLEAN) AS home_is_spot,
  CAST(h.source_export_date AS TIMESTAMP) AS home_source_export_date,
  {metric_date} AS metrics_as_of_date,
  {metrics_projection_sql},
  COALESCE(a.assignment_count, 0) AS provider_assignment_count,
  COALESCE(a.declined_assignment_count, 0) AS provider_declined_assignment_count,
  COALESCE(a.timed_response_count, 0) AS provider_timed_response_count,
  a.average_response_minutes AS provider_average_response_minutes,
  COALESCE(m.message_count, 0) AS provider_message_count,
  CAST(p.source_export_date AS TIMESTAMP) AS source_export_date,
  CAST(p.export_date AS TIMESTAMP) AS export_date,
  '{job_literal}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM {gold_schema}.dim_provider p
LEFT JOIN {gold_schema}.dim_provider_home h ON h.provider_id = p.provider_id
LEFT JOIN ranked_provider pc ON pc.provider_id = p.provider_id AND pc.registry_provider_rank = 1
LEFT JOIN current_provider_home hc ON hc.provider_home_id = h.provider_home_id AND hc.provider_id = h.provider_id
LEFT JOIN provider_frameworks f ON f.provider_id = p.provider_id
LEFT JOIN provider_offers provider_o ON provider_o.provider_id = p.provider_id
LEFT JOIN provider_ipas provider_i ON provider_i.provider_id = p.provider_id
LEFT JOIN home_offers home_o ON home_o.provider_id = p.provider_id AND home_o.provider_home_id = h.provider_home_id
LEFT JOIN home_ipas home_i ON home_i.provider_id = p.provider_id AND home_i.provider_home_id = h.provider_home_id
LEFT JOIN provider_assignments a ON a.provider_id = p.provider_id
LEFT JOIN provider_messages m ON m.provider_id = p.provider_id
"""


def validate_provider_registry_baseline(registry, gold_schema):
    """Fail before overwrite if ANY baseline row is lost, added or multiplied."""
    baseline = spark.sql(f"""SELECT CAST(p.provider_id AS STRING) AS provider_id,
      CAST(h.provider_home_id AS STRING) AS provider_home_id
      FROM {gold_schema}.dim_provider p
      LEFT JOIN {gold_schema}.dim_provider_home h ON p.provider_id = h.provider_id""")
    actual = registry.select("provider_id", "provider_home_id")
    baseline_count = baseline.count()
    if actual.count() != baseline_count:
        raise ValueError("Registry row count must exactly equal dim_provider LEFT dim_provider_home")
    if baseline.exceptAll(actual).limit(1).count() or actual.exceptAll(baseline).limit(1).count():
        raise ValueError("Registry provider/home rows must exactly match the dimension LEFT JOIN baseline")
    return baseline_count


require_columns(f"{SILVER_SCHEMA}.provider",
                provider_registry_columns() + ["export_date", "_silver_load_ts"])
require_columns(f"{GOLD_SCHEMA}.bridge_provider_framework",
                ["provider_framework_id", "provider_id", "framework_code", "source_export_date"])
require_columns(f"{GOLD_SCHEMA}.dim_framework", ["framework_code", "placement_type"])
for registry_source, registry_columns in provider_registry_sources(SILVER_SCHEMA, GOLD_SCHEMA).items():
    require_columns(registry_source, registry_columns)
for registry_source, registry_columns in provider_registry_baseline_columns(GOLD_SCHEMA).items():
    require_columns(registry_source, registry_columns)
# Use the fact refresh's date, not today's date against stale/archive facts.
registry_fact_dates = set()
for registry_fact in ("fact_offer", "fact_ipa", "fact_referral_provider"):
    for registry_fact_date in spark.table(f"{GOLD_SCHEMA}.{registry_fact}").select("as_of_date").distinct().limit(2).collect():
        if registry_fact_date[0] is None:
            raise ValueError("Registry fact metrics require a known as-of date; refresh the Gold facts")
        registry_fact_dates.add(str(registry_fact_date[0]))
if len(registry_fact_dates) > 1 or (AS_OF_DATE and registry_fact_dates and AS_OF_DATE not in registry_fact_dates):
    raise ValueError("Registry requires offer, IPA and assignment facts from the same as-of date")
REGISTRY_METRICS_DATE = next(iter(registry_fact_dates), GOLD_EXPORT_DATE)
provider_registry = spark.sql(provider_registry_sql(
    SILVER_SCHEMA, GOLD_SCHEMA, GOLD_JOB_RUN_ID, REGISTRY_METRICS_DATE))
registry_target = f"{GOLD_SCHEMA}.rpt_provider_registry"
REGISTRY_BASELINE_COUNT = validate_provider_registry_baseline(provider_registry, GOLD_SCHEMA)
if provider_registry.groupBy("provider_id", "provider_home_id").count().where("count > 1").limit(1).count():
    raise ValueError("Registry contains duplicate provider/home pairs; do not silently deduplicate them")
(provider_registry.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable(registry_target))
print(f"{registry_target}: {REGISTRY_BASELINE_COUNT:,} provider/home rows; exact dimension LEFT JOIN baseline; metrics as of {REGISTRY_METRICS_DATE}")

print(f"Gold dimensions and registry completed; AS_OF_DATE={AS_OF_DATE or 'latest'}; started={RUN_STARTED_AT.isoformat()}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
