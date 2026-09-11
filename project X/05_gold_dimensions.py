# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "known_lakehouses": [
# META         {
# META           "id": "d286fa39-f255-4ba7-a982-32cb69362ef7"
# META         }
# META       ],
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770"
# META     }
# META   },
# META   "spark_compute": {
# META     "compute_id": "/trident/default",
# META     "session_options": {
# META       "conf": {
# META         "spark.synapse.nbs.session.timeout": "1200000"
# META       }
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

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")
RUN_STARTED_AT = datetime.utcnow()

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
    dimension = current.select(*[
        F.col(source).alias(target) for source, target in select_columns
    ])
    (dimension.write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true").saveAsTable(target_table))
    print(f"{target_table}: {dimension.count():,} rows from {source_table}")


def copy_bridge(source_table, target_table, required_columns, select_columns):
    require_columns(source_table, required_columns)
    bridge = spark.table(source_table).select(*[
        F.col(source).alias(target) for source, target in select_columns
    ]).dropDuplicates()
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

require_columns("silver.referral", ["placement_type", "referral_status"])
require_columns("silver.ipa", ["placement_type"])
placement_types = (
    spark.table("silver.referral").select(F.col("placement_type").alias("placement_type"))
    .unionByName(spark.table("silver.ipa").select(F.col("placement_type").alias("placement_type")))
    .where(F.col("placement_type").isNotNull() & (F.trim(F.col("placement_type")) != ""))
    .dropDuplicates()
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(placement_types.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_placement_type"))

referral_statuses = (
    spark.table("silver.referral").select(F.col("referral_status").alias("referral_status"))
    .where(F.col("referral_status").isNotNull() & (F.trim(F.col("referral_status")) != ""))
    .dropDuplicates()
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(referral_statuses.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_referral_status"))

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
    F.col("export_date").alias("source_export_date"),
)
(dim_person.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_person"))
print(f"gold.dim_person: {dim_person.count():,} rows from silver.referral_person")

# GLD-008: offer-status dimension with labels and lifecycle flags, rebuilt
# from the distinct offer_status codes observed in Silver. Unknown future
# codes are kept with a null label, matching the legacy model behaviour.
require_columns("silver.offer", ["offer_status"])
offer_statuses = (
    spark.table("silver.offer")
    .select(F.col("offer_status").alias("offer_status"))
    .where(F.col("offer_status").isNotNull() & (F.trim(F.col("offer_status")) != ""))
    .dropDuplicates()
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
        "is_active_offer", "is_accepted", "is_terminal",
    )
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
