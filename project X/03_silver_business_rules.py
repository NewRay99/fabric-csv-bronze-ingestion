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

# # 03 — Silver business and data-quality rules
#
# Run metadata-driven checks against the schema-conformed Silver tables.
# Primary-key and foreign-key rules come from `schema_definition.csv`; additional
# date and numeric rules come from `dq_rule_definition.csv`.
#
# Rejected-row logging stores only key references, not complete child records.

# CELL ********************

SILVER_SCHEMA = "silver"
MAX_REJECT_REFERENCES_PER_RULE = 100
FAIL_ON_CRITICAL = True

JOB_RUN_ID = ""  # Parent orchestration correlation ID.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# 90_run_live_pipeline executes 00_setup_cfg before this child notebook.

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run ./99_common_library

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# LIVE-ETL-002 guard: fail fast with a clear message when the default
# lakehouse attachment is broken, and create the expected schemas so
# two-part names (silver.*, monitoring.*) never fall back to slow
# cross-artifact resolution — the resolver loop behind the "hang".
try:
    visible_schemas = {row[0] for row in spark.sql("SHOW SCHEMAS").collect()}
except Exception as exc:
    raise RuntimeError(
        "LIVE-ETL-002: cannot list schemas in the default lakehouse. "
        "Confirm LH_BCT_WMPP is attached to this notebook as the default "
        "lakehouse, then rerun. Original error: " + str(exc)[:500]
    )
for required_schema in (SILVER_SCHEMA, "monitoring"):
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {required_schema}")
print(f"Schemas visible to this session: {sorted(visible_schemas)}")
log_step("Schema guard complete")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import re, uuid
from datetime import datetime
from pyspark.sql import functions as F

RUN_ID = str(uuid.uuid4())
STARTED_AT = datetime.utcnow()
JOB_RUN_ID = JOB_RUN_ID or RUN_ID
# Pipeline status joins to the parent job; individual DQ results retain RUN_ID.
PIPELINE_RUN_ID = JOB_RUN_ID or RUN_ID

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

append_rows("monitoring.cfg_pipeline_run", [(PIPELINE_RUN_ID, "03_silver_business_rules", "SILVER", "LATEST",
    STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string")
log_step("Pipeline run row registered")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

schema_df = spark.table("monitoring.cfg_schema_contract_column")
custom_rules_df = spark.table("monitoring.cfg_data_quality_rule")
if schema_df.rdd.isEmpty() or custom_rules_df.rdd.isEmpty():
    raise ValueError("Configuration tables are empty; run setup CSV bootstrap first")
schema_rows = [r.asDict() for r in schema_df.collect()]
rules = []

# Contract-generated PK completeness and table-level uniqueness checks.
primary_keys = {}
for row in schema_rows:
    if (row.get("is_primary_key") or "").upper() == "YES":
        primary_keys.setdefault(row["table_name"], []).append(row["column_name"])
        base = {"source_schema": SILVER_SCHEMA, "table_name": row["table_name"],
                "column_name": row["column_name"], "severity": "CRITICAL", "active": "true"}
        rules.append({**base, "rule_id": f"PK_NOT_NULL_{row['table_name']}_{row['column_name']}", "rule_type": "NOT_NULL"})
for table_name, key_columns in primary_keys.items():
    rules.append({"source_schema": SILVER_SCHEMA, "table_name": table_name,
        "column_name": ",".join(key_columns), "severity": "CRITICAL", "active": "true",
        "rule_id": f"PK_UNIQUE_{table_name}", "rule_type": "UNIQUE"})

# Contract-generated referential-integrity checks.
for row in schema_rows:
    if row.get("referenced_table") and row.get("referenced_column"):
        rules.append({
            "rule_id": f"FK_{row['table_name']}_{row['column_name']}",
            "active": "true", "severity": "ERROR", "rule_type": "REFERENTIAL_INTEGRITY",
            "source_schema": SILVER_SCHEMA, "table_name": row["table_name"],
            "column_name": row["column_name"], "referenced_schema": SILVER_SCHEMA,
            "referenced_table": row["referenced_table"], "referenced_column": row["referenced_column"],
        })

rules.extend(r.asDict() for r in custom_rules_df.where("lower(active) = 'true'").collect())
# Derived referral checks run after Cell 8 materialises the current Silver
# enrichment, rather than validating a prior run's table state.
derived_dq_rules = [
    rule for rule in rules
    if rule.get("table_name") == "referral_enrichment"
]
validation_rules = [
    rule for rule in rules
    if rule.get("table_name") != "referral_enrichment"
]
rule_fields = ["rule_id", "active", "severity", "rule_type", "source_schema", "table_name",
    "column_name", "referenced_schema", "referenced_table", "referenced_column",
    "operator", "rule_value", "description"]
normalised_rule_rows = [tuple(rule.get(field) for field in rule_fields) + (datetime.utcnow(),) for rule in rules]
spark.createDataFrame(normalised_rule_rows,
    "rule_id string,active string,severity string,rule_type string,source_schema string,table_name string,column_name string,referenced_schema string,referenced_table string,referenced_column string,operator string,rule_value string,description string,loaded_at timestamp") \
    .write.format("delta").mode("overwrite").option("overwriteSchema", "true") \
    .saveAsTable("monitoring.cfg_data_quality_rule")
print(f"Prepared {len(rules):,} data-quality rules")
log_step(f"Prepared {len(rules):,} data-quality rules")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

result_schema = "run_id string,rule_id string,severity string,rule_type string,source_table string,column_name string,status string,failed_row_count long,checked_row_count long,failure_percentage double,sample_key_json string,checked_at timestamp,message string,job_run_id string"
reject_schema = "run_id string,rule_id string,source_table string,business_key_json string,rejection_reason string,rejected_at timestamp,job_run_id string"
reference_schema = "run_id string,rule_id string,child_table string,child_column string,child_key string,parent_table string,parent_column string,detected_at timestamp,job_run_id string"
result_rows = []
critical_failures = []

# LIVE-ETL-003: scan each Silver table once per run. Rules are grouped by
# source table; the row count is computed once per table and multi-rule
# tables are cached for the duration of their checks.
table_rule_counts = {}
for rule in validation_rules:
    table_rule_counts[rule["table_name"]] = table_rule_counts.get(rule["table_name"], 0) + 1
checked_counts = {}
cached_frames = {}


def log_rule(rule_id, status, detail, rule_started):
    elapsed = (datetime.utcnow() - rule_started).total_seconds()
    print(f"  [{rule_id}] {status}: {detail} (+{elapsed:,.1f}s)")


for rule in validation_rules:
    rule_id = rule["rule_id"]
    rule_type = rule["rule_type"].upper()
    severity = (rule.get("severity") or "ERROR").upper()
    source = silver_table(rule["table_name"])
    column_name = rule["column_name"]
    checked_at = datetime.utcnow()
    rule_started = datetime.utcnow()
    try:
        if not spark.catalog.tableExists(source):
            result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, 0, 0.0, None, checked_at, "Missing Silver source table"))
            log_rule(rule_id, "SKIPPED", "missing Silver source table", rule_started)
            continue
        frame = spark.table(source)
        if table_rule_counts.get(rule["table_name"], 0) > 1 and source not in cached_frames:
            frame = frame.cache()
            cached_frames[source] = frame
        missing_columns = [c.strip() for c in column_name.split(",") if c.strip() and c.strip() not in frame.columns]
        if missing_columns:
            result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, 0, 0.0, None, checked_at, f"Missing Silver column(s): {missing_columns}"))
            log_rule(rule_id, "SKIPPED", f"missing Silver column(s): {missing_columns}", rule_started)
            continue
        checked = checked_counts.get(source)
        if checked is None:
            checked = frame.count()
            checked_counts[source] = checked
        failed_frame = None
        failed = 0

        if rule_type == "NOT_NULL":
            failed_frame = frame.where(F.col(qident(column_name)).isNull())
            failed = failed_frame.count()
        elif rule_type == "UNIQUE":
            key_columns = [name.strip() for name in column_name.split(",") if name.strip()]
            non_null = frame
            for key_column in key_columns:
                non_null = non_null.where(F.col(qident(key_column)).isNotNull())
            duplicates = non_null.groupBy(*key_columns).count().where("count > 1")
            failed = duplicates.select(F.sum(F.col("count") - 1).alias("failed")).first()["failed"] or 0
            failed_frame = duplicates.select(F.to_json(F.struct(*[F.col(qident(c)) for c in key_columns])).alias("_key"))
        elif rule_type == "REFERENTIAL_INTEGRITY":
            parent = silver_table(rule["referenced_table"])
            if not spark.catalog.tableExists(parent):
                result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, checked, 0.0, None, checked_at, "Missing Silver parent table"))
                log_rule(rule_id, "SKIPPED", "missing Silver parent table", rule_started)
                continue
            parent_frame = spark.table(parent)
            parent_column = rule["referenced_column"]
            if parent_column not in parent_frame.columns:
                result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, checked, 0.0, None, checked_at, f"Missing Silver parent column: {parent_column}"))
                log_rule(rule_id, "SKIPPED", f"missing Silver parent column: {parent_column}", rule_started)
                continue
            parent_frame = parent_frame.select(F.trim(F.col(qident(parent_column)).cast("string")).alias("_parent_key")).distinct()
            failed_frame = (frame.where(F.col(qident(column_name)).isNotNull())
                .select(F.trim(F.col(qident(column_name)).cast("string")).alias("_key")).distinct()
                .join(parent_frame, F.col("_key") == F.col("_parent_key"), "left_anti"))
            failed = failed_frame.count()
            refs = [(RUN_ID, rule_id, source, column_name, r["_key"], parent,
                rule["referenced_column"], checked_at) for r in failed_frame.limit(MAX_REJECT_REFERENCES_PER_RULE).collect()]
            append_rows("monitoring.cfg_referential_exception", [tuple(row) + (JOB_RUN_ID or None,) for row in refs], reference_schema)
        elif rule_type == "DATE_ORDER":
            other = rule["referenced_column"]
            operator = (rule.get("operator") or "<=").strip()
            left = F.col(qident(column_name))
            right = F.col(qident(other))
            if operator == "<=":
                invalid_order = left > right
            elif operator == ">=":
                invalid_order = left < right
            else:
                raise ValueError(
                    f"Unsupported DATE_ORDER operator: {operator}. Use <= or >="
                )
            failed_frame = frame.where(
                left.isNotNull() & right.isNotNull() & invalid_order
            )
            failed = failed_frame.count()
        elif rule_type == "CONDITIONAL_NOT_NULL":
            other = rule["referenced_column"]
            failed_frame = frame.where(
                F.col(qident(other)).isNotNull()
                & F.col(qident(column_name)).isNull()
            )
            failed = failed_frame.count()
        elif rule_type == "NON_NEGATIVE":
            failed_frame = frame.where(F.col(qident(column_name)) < F.lit(0))
            failed = failed_frame.count()
        else:
            raise ValueError(f"Unsupported rule type: {rule_type}")

        status = "PASS" if failed == 0 else "FAIL"
        pct = (failed / checked * 100.0) if checked else 0.0
        sample_key = None
        if failed_frame is not None and failed:
            key_column = "_key" if "_key" in failed_frame.columns else column_name.split(",")[0].strip()
            samples = failed_frame.select(F.col(qident(key_column)).cast("string").alias("key")) \
                .limit(MAX_REJECT_REFERENCES_PER_RULE).collect()
            sample_key = samples[0]["key"] if samples else None
            rejects = [(RUN_ID, rule_id, source, '{"key":"' + str(r["key"]).replace('"', '\\"') + '"}',
                rule.get("description") or rule_type, checked_at) for r in samples]
            append_rows("monitoring.cfg_rejected_row", [tuple(row) + (JOB_RUN_ID or None,) for row in rejects], reject_schema)
        result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, status,
            int(failed), int(checked), float(pct), sample_key, checked_at, rule.get("description")))
        log_rule(rule_id, status, f"{int(failed):,}/{int(checked):,} failed", rule_started)
        if status == "FAIL" and severity == "CRITICAL":
            critical_failures.append(rule_id)
    except Exception as exc:
        result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "ERROR",
            0, 0, 0.0, None, checked_at, str(exc)[:2000]))
        log_rule(rule_id, "ERROR", str(exc)[:200], rule_started)
        if severity == "CRITICAL":
            critical_failures.append(rule_id)

for cached_frame in cached_frames.values():
    cached_frame.unpersist()

append_rows("monitoring.cfg_data_quality_result", [tuple(row) + (JOB_RUN_ID or None,) for row in result_rows], result_schema)
failed_checks = sum(1 for row in result_rows if row[6] in ("FAIL", "ERROR"))
skipped_checks = sum(1 for row in result_rows if row[6] == "SKIPPED")
run_status = "FAILED" if critical_failures else ("SUCCESS_WITH_WARNINGS" if failed_checks else "SUCCESS")
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run SET ended_at=current_timestamp(), status='{run_status}',
tables_succeeded={len(result_rows) - failed_checks}, tables_failed={failed_checks},
rows_read=0, rows_written={len(result_rows)}, error_message=NULL WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='03_silver_business_rules'""")
if critical_failures and FAIL_ON_CRITICAL:
    raise RuntimeError(f"Critical DQ failures: {critical_failures[:20]}")
print(f"DQ run {RUN_ID}: {len(result_rows)} checks; {len(critical_failures)} critical failures; {skipped_checks} skipped")
log_step(f"Main DQ pass complete: {len(result_rows)} checks, {len(critical_failures)} critical failures")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# SI-008 to SI-012 — Silver materialisations used by reporting.
# These are deterministic derived tables, not source-contract entities.
from pyspark.sql.types import DateType, IntegerType, StringType, StructField, StructType

def replace_silver_materialisation(frame, table_name):
    (frame.write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"{SILVER_SCHEMA}.{table_name}"))


# SI-008: stable age-band axis.
replace_silver_materialisation(
    spark.createDataFrame(
        [("0-7 days", 1), ("8-14 days", 2), ("15-30 days", 3), ("31+ days", 4)],
        "age_band string, sort_order int",
    ),
    "age_band",
)

# SI-009 and SI-010: disconnected presentation axes.
replace_silver_materialisation(
    spark.createDataFrame(
        [("Residential Homes",), ("Supported Accommodation Homes",), ("Fostering Providers",)],
        "display_type string",
    ),
    "directory_summary_axis",
)
replace_silver_materialisation(
    spark.createDataFrame([("Fostering Providers",)], "display_type string"),
    "fostering_axis",
)

# SI-011: one closure-reason bucket per referral, using only available Silver
# referral-provider and offer fields. This replaces the former Gold/DAX-only
# calculated table and remains empty, rather than failing, when those inputs
# are not present for a historical month.
if (spark.catalog.tableExists("silver.referral_provider")
        and spark.catalog.tableExists("silver.offer")):
    closure_summary = spark.sql("""
        SELECT rp.referral_id,
          MAX(CASE
            WHEN LOWER(CAST(COALESCE(rp.is_cancelled, false) AS STRING)) IN ('true', '1', 'yes')
              THEN 'Cancelled'
            WHEN LOWER(CAST(COALESCE(rp.is_declined, false) AS STRING)) IN ('true', '1', 'yes')
              OR LOWER(COALESCE(o.offer_status, '')) IN ('declined', 'rejected')
              THEN 'Declined'
            WHEN LOWER(CAST(COALESCE(rp.is_closed, false) AS STRING)) IN ('true', '1', 'yes')
              OR LOWER(COALESCE(o.offer_status, '')) IN ('closed', 'withdrawn')
              THEN 'Closed/Withdrawn'
            WHEN COALESCE(o.decline_reason_other, o.decline_reason, o.withdraw_reason) IS NOT NULL
              THEN 'Other'
            ELSE NULL
          END) AS closed_referral_reason_bucket
        FROM silver.referral_provider rp
        LEFT JOIN silver.offer o
          ON rp.referral_provider_id = o.referral_provider_id
        GROUP BY rp.referral_id
    """)
else:
    closure_summary = spark.createDataFrame(
        [], "referral_id string, closed_referral_reason_bucket string"
    )
replace_silver_materialisation(closure_summary, "referral_closure_reason_summary")
log_step("Materialised referral_closure_reason_summary")

# SI-018/SI-019: referral-level enrichment is intentionally a separate
# derived Silver relation. The source-conformed silver.referral contract
# remains immutable; this relation makes cross-table KPI logic reusable by
# Gold, snapshots, and ad-hoc reporting.
enrichment_schema = (
    "referral_id string, referral_created_date timestamp, cnt_offer_made long, "
    "unique_homes_offered long, estimated_weekly_cost decimal(19,2), "
    "first_action_date timestamp, first_offer_date timestamp, offer_accepted_date timestamp, "
    "ipa_issued_date timestamp, referral_closed_date timestamp, last_activity_date timestamp, "
    "first_provider_seen_date timestamp, "
    "is_not_seen_by_providers boolean, ipa_placement_admission_date timestamp, "
    "ipa_2_signatures boolean, ipa_last_signature_date timestamp, "
    "ipa_due_diligence_min_review_date timestamp"
)
if (spark.catalog.tableExists("silver.referral")
        and spark.catalog.tableExists("silver.referral_provider")
        and spark.catalog.tableExists("silver.offer")
        and spark.catalog.tableExists("silver.ipa")):
    documents_cte = (
        """
        ipa_documents AS (
          SELECT i.referral_id,
            MIN(CAST(d.next_review_date AS TIMESTAMP))
              AS ipa_due_diligence_min_review_date
          FROM silver.ipa i
          INNER JOIN silver.offer o ON i.offer_id = o.offer_id
          INNER JOIN silver.provider_submission_docs d
            ON d.home_id = o.provider_home_id
          WHERE i.placement_admission_date IS NOT NULL
            AND d.next_review_date IS NOT NULL
            AND d.next_review_date > i.placement_admission_date
          GROUP BY i.referral_id
        )
        """
        if spark.catalog.tableExists("silver.provider_submission_docs")
        else "ipa_documents AS (SELECT CAST(NULL AS STRING) AS referral_id, CAST(NULL AS TIMESTAMP) AS ipa_due_diligence_min_review_date WHERE 1 = 0)"
    )
    referral_enrichment = spark.sql(f"""
        WITH offer_rollup AS (
          SELECT rp.referral_id, COUNT(DISTINCT o.offer_id) AS cnt_offer_made,
            COUNT(DISTINCT o.provider_home_id) AS unique_homes_offered,
            MIN(CAST(o.offer_date AS TIMESTAMP)) AS first_offer_date,
            MIN(CASE WHEN LOWER(COALESCE(o.offer_status, '')) IN
              ('accepted', 'approved', 'selected', 'offer_successful')
              THEN CAST(COALESCE(o.last_modified_date, o.offer_date) AS TIMESTAMP)
            END) AS offer_accepted_date
          FROM silver.referral_provider rp
          LEFT JOIN silver.offer o
            ON rp.referral_provider_id = o.referral_provider_id
          GROUP BY rp.referral_id
        ),
        activity_candidates AS (
          SELECT CAST(referral_id AS STRING) AS referral_id,
            CAST(referral_created_date AS TIMESTAMP) AS activity_timestamp,
            'ReferralCreated' AS activity_type
          FROM silver.referral WHERE referral_created_date IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(referral_modified_date AS TIMESTAMP),
            'ReferralModified'
          FROM silver.referral
          WHERE referral_modified_date IS NOT NULL
            AND referral_modified_date > referral_created_date
          UNION ALL
          SELECT CAST(rp.referral_id AS STRING), CAST(o.offer_date AS TIMESTAMP),
            'OfferSubmitted'
          FROM silver.offer o INNER JOIN silver.referral_provider rp
            ON o.referral_provider_id = rp.referral_provider_id
          WHERE o.offer_date IS NOT NULL
          UNION ALL
          SELECT CAST(rp.referral_id AS STRING), CAST(o.last_modified_date AS TIMESTAMP),
            'OfferUpdated'
          FROM silver.offer o INNER JOIN silver.referral_provider rp
            ON o.referral_provider_id = rp.referral_provider_id
          WHERE o.last_modified_date IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(created_datetime AS TIMESTAMP),
            'IPACreated'
          FROM silver.ipa WHERE created_datetime IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(updated_datetime AS TIMESTAMP),
            'IPAUpdated'
          FROM silver.ipa WHERE updated_datetime IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(placement_admission_date AS TIMESTAMP),
            'IPAAdmission'
          FROM silver.ipa WHERE placement_admission_date IS NOT NULL
        ),
        activity_rollup AS (
          SELECT referral_id,
            MIN(CASE WHEN activity_type <> 'ReferralCreated' THEN activity_timestamp END)
              AS first_action_date,
            MAX(activity_timestamp) AS last_activity_date
          FROM activity_candidates
          GROUP BY referral_id
        ),
        provider_seen AS (
          SELECT referral_id, MIN(CAST(export_date AS TIMESTAMP))
            AS first_provider_seen_date
          FROM silver.referral_provider
          GROUP BY referral_id
        ),
        ipa_rollup AS (
          SELECT referral_id, MIN(CAST(created_datetime AS TIMESTAMP))
              AS ipa_issued_date,
            CAST(SUM(costs_total_weekly_fee) AS DECIMAL(19, 2))
              AS estimated_weekly_cost,
            MIN(CAST(placement_admission_date AS TIMESTAMP))
              AS ipa_placement_admission_date,
            MAX(CASE WHEN UPPER(COALESCE(status, '')) = 'SIGNED'
              THEN 1 ELSE 0 END) = 1 AS ipa_2_signatures,
            MAX(GREATEST(
              CAST(signed_datetime_for_local_authority AS TIMESTAMP),
              CAST(signed_datetime_for_provider AS TIMESTAMP),
              CAST(can_sign_date AS TIMESTAMP)
            )) AS ipa_last_signature_date
          FROM silver.ipa
          GROUP BY referral_id
        ),
        {documents_cte}
        SELECT CAST(r.referral_id AS STRING) AS referral_id,
          CAST(r.referral_created_date AS TIMESTAMP) AS referral_created_date,
          COALESCE(o.cnt_offer_made, 0) AS cnt_offer_made,
          COALESCE(o.unique_homes_offered, 0) AS unique_homes_offered,
          i.estimated_weekly_cost,
          a.first_action_date, o.first_offer_date, o.offer_accepted_date,
          i.ipa_issued_date,
          CASE WHEN LOWER(COALESCE(r.referral_status, '')) IN
            ('closed', 'cancelled', 'withdrawn', 'completed')
            THEN CAST(COALESCE(r.referral_modified_date, r.export_date) AS TIMESTAMP)
          END AS referral_closed_date,
          a.last_activity_date, p.first_provider_seen_date,
          p.referral_id IS NULL AS is_not_seen_by_providers,
          i.ipa_placement_admission_date,
          COALESCE(i.ipa_2_signatures, false) AS ipa_2_signatures,
          i.ipa_last_signature_date,
          d.ipa_due_diligence_min_review_date
        FROM silver.referral r
        LEFT JOIN offer_rollup o ON r.referral_id = o.referral_id
        LEFT JOIN activity_rollup a ON r.referral_id = a.referral_id
        LEFT JOIN provider_seen p ON r.referral_id = p.referral_id
        LEFT JOIN ipa_rollup i ON r.referral_id = i.referral_id
        LEFT JOIN ipa_documents d ON r.referral_id = d.referral_id
    """)
else:
    referral_enrichment = spark.createDataFrame([], enrichment_schema)
replace_silver_materialisation(referral_enrichment, "referral_enrichment")
print("Silver referral enrichment ready: offer, provider-observation, IPA-signature and due-diligence fields")
log_step("Materialised referral_enrichment")

# Run derived checks only after the current enrichment has been written.
# Results use the same monitoring tables as the main DQ pass above.
derived_result_rows = []
derived_critical_failures = []
for rule in derived_dq_rules:
    rule_id = rule["rule_id"]
    rule_type = rule["rule_type"].upper()
    severity = (rule.get("severity") or "ERROR").upper()
    column_name = rule["column_name"]
    checked_at = datetime.utcnow()
    frame = spark.table(f"{SILVER_SCHEMA}.referral_enrichment")
    try:
        missing = [name.strip() for name in column_name.split(',')
                   if name.strip() not in frame.columns]
        referenced_column = rule.get("referenced_column")
        if referenced_column and referenced_column not in frame.columns:
            missing.append(referenced_column)
        if missing:
            derived_result_rows.append((
                RUN_ID, rule_id, severity, rule_type,
                f"{SILVER_SCHEMA}.referral_enrichment", column_name,
                "SKIPPED", 0, 0, 0.0, None, checked_at,
                f"Missing Silver column(s): {sorted(set(missing))}", JOB_RUN_ID or None,
            ))
            continue
        checked = frame.count()
        target = F.col(qident(column_name))
        failed_frame = None
        if rule_type == "NOT_NULL":
            failed_frame = frame.where(target.isNull())
        elif rule_type == "CONDITIONAL_NOT_NULL":
            failed_frame = frame.where(
                F.col(qident(referenced_column)).isNotNull() & target.isNull()
            )
        elif rule_type == "NON_NEGATIVE":
            failed_frame = frame.where(target < F.lit(0))
        elif rule_type == "UNIQUE":
            key_columns = [name.strip() for name in column_name.split(',') if name.strip()]
            failed_frame = (frame.dropna(subset=key_columns).groupBy(*key_columns)
                .count().where("count > 1"))
        elif rule_type == "DATE_ORDER":
            other = F.col(qident(referenced_column))
            operator = (rule.get("operator") or "<=").strip()
            invalid_order = target > other if operator == "<=" else target < other
            if operator not in {"<=", ">="}:
                raise ValueError(f"Unsupported DATE_ORDER operator: {operator}")
            failed_frame = frame.where(
                target.isNotNull() & other.isNotNull() & invalid_order
            )
        else:
            raise ValueError(f"Unsupported derived DQ rule type: {rule_type}")
        failed = failed_frame.count()
        status = "PASS" if failed == 0 else "FAIL"
        sample = (failed_frame.select(F.col("referral_id").cast("string").alias("key"))
            .limit(MAX_REJECT_REFERENCES_PER_RULE).collect()) if failed else []
        sample_key = sample[0]["key"] if sample else None
        rejects = [(
            RUN_ID, rule_id, f"{SILVER_SCHEMA}.referral_enrichment",
            '{\"referral_id\":\"' + str(row["key"]).replace('\"', '\\\"') + '\"}',
            rule.get("description") or rule_type, checked_at, JOB_RUN_ID or None,
        ) for row in sample]
        append_rows("monitoring.cfg_rejected_row", rejects, reject_schema)
        derived_result_rows.append((
            RUN_ID, rule_id, severity, rule_type,
            f"{SILVER_SCHEMA}.referral_enrichment", column_name, status,
            int(failed), int(checked), (failed / checked * 100.0) if checked else 0.0,
            sample_key, checked_at, rule.get("description"), JOB_RUN_ID or None,
        ))
        if status == "FAIL" and severity == "CRITICAL":
            derived_critical_failures.append(rule_id)
    except Exception as exc:
        derived_result_rows.append((
            RUN_ID, rule_id, severity, rule_type,
            f"{SILVER_SCHEMA}.referral_enrichment", column_name,
            "ERROR", 0, 0, 0.0, None, checked_at, str(exc)[:2000], JOB_RUN_ID or None,
        ))
        if severity == "CRITICAL":
            derived_critical_failures.append(rule_id)
append_rows("monitoring.cfg_data_quality_result", derived_result_rows, result_schema)
derived_failed = sum(1 for row in derived_result_rows if row[6] in ("FAIL", "ERROR"))
if derived_failed:
    spark.sql(f"""
      UPDATE monitoring.cfg_pipeline_run
      SET status = 'SUCCESS_WITH_WARNINGS',
          tables_failed = COALESCE(tables_failed, 0) + {derived_failed}
      WHERE run_id = '{PIPELINE_RUN_ID}' AND pipeline_name = '03_silver_business_rules'
    """)
if derived_critical_failures and FAIL_ON_CRITICAL:
    raise RuntimeError(f"Critical derived DQ failures: {derived_critical_failures[:20]}")
print(f"Derived referral DQ: {len(derived_result_rows)} checks; {derived_failed} failures")
log_step(f"Derived referral DQ complete: {len(derived_result_rows)} checks, {derived_failed} failures")

# SI-013: derived referral lifecycle events. These are not a source-system
# audit log; each event is derived only from timestamps delivered in Silver.
lifecycle_sources = []
if spark.catalog.tableExists("silver.referral"):
    lifecycle_sources.extend([
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'ReferralCreated' AS event_type,
          CAST(referral_created_date AS TIMESTAMP) AS event_timestamp,
          CAST(referral_created_by AS STRING) AS created_by,
          CAST(referral_created_date AS TIMESTAMP) AS created_timestamp,
          CAST(referral_id AS STRING) AS source_record_id,
          'silver.referral' AS source_table
        FROM silver.referral
        WHERE referral_created_date IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'ReferralModified' AS event_type,
          CAST(referral_modified_date AS TIMESTAMP) AS event_timestamp,
          CAST(referral_updated_by AS STRING) AS created_by,
          CAST(referral_modified_date AS TIMESTAMP) AS created_timestamp,
          CAST(referral_id AS STRING) AS source_record_id,
          'silver.referral' AS source_table
        FROM silver.referral
        WHERE referral_modified_date IS NOT NULL
        """,
    ])
if (spark.catalog.tableExists("silver.offer")
        and spark.catalog.tableExists("silver.referral_provider")):
    lifecycle_sources.extend([
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'OfferSubmitted' AS event_type,
          CAST(o.offer_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(o.offer_date AS TIMESTAMP) AS created_timestamp,
          CAST(o.offer_id AS STRING) AS source_record_id,
          'silver.offer' AS source_table
        FROM silver.offer o
        INNER JOIN silver.referral_provider rp
          ON o.referral_provider_id = rp.referral_provider_id
        WHERE o.offer_date IS NOT NULL
        """,
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'OfferUpdated' AS event_type,
          CAST(o.last_modified_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(o.last_modified_date AS TIMESTAMP) AS created_timestamp,
          CAST(o.offer_id AS STRING) AS source_record_id,
          'silver.offer' AS source_table
        FROM silver.offer o
        INNER JOIN silver.referral_provider rp
          ON o.referral_provider_id = rp.referral_provider_id
        WHERE o.last_modified_date IS NOT NULL
        """,
    ])
if (spark.catalog.tableExists("silver.referral_provider_message")
        and spark.catalog.tableExists("silver.referral_provider")):
    lifecycle_sources.append(
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'ProviderMessageSent' AS event_type,
          CAST(m.created_timestamp AS TIMESTAMP) AS event_timestamp,
          CAST(m.created_by AS STRING) AS created_by,
          CAST(m.created_timestamp AS TIMESTAMP) AS created_timestamp,
          CAST(m.message_id AS STRING) AS source_record_id,
          'silver.referral_provider_message' AS source_table
        FROM silver.referral_provider_message m
        INNER JOIN silver.referral_provider rp
          ON m.referral_provider_id = rp.referral_provider_id
        WHERE m.created_timestamp IS NOT NULL
        """
    )

if spark.catalog.tableExists("silver.ipa"):
    lifecycle_sources.extend([
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPACreated' AS event_type,
          CAST(created_datetime AS TIMESTAMP) AS event_timestamp,
          CAST(created_by AS STRING) AS created_by,
          CAST(created_datetime AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE created_datetime IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPAUpdated' AS event_type,
          CAST(updated_datetime AS TIMESTAMP) AS event_timestamp,
          CAST(updated_by AS STRING) AS created_by,
          CAST(updated_datetime AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE updated_datetime IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPAAdmission' AS event_type,
          CAST(placement_admission_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(placement_admission_date AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE placement_admission_date IS NOT NULL
        """,
    ])

if lifecycle_sources:
    lifecycle_events = spark.sql(f"""
        WITH raw_events AS ({' UNION ALL '.join(lifecycle_sources)}),
        sequenced AS (
          SELECT referral_id, event_type, event_timestamp, created_by,
            created_timestamp, source_record_id, source_table,
            ROW_NUMBER() OVER (
              PARTITION BY referral_id
              ORDER BY event_timestamp, event_type, source_record_id
            ) AS sequence_number
          FROM raw_events
          WHERE referral_id IS NOT NULL AND event_timestamp IS NOT NULL
        )
        SELECT SHA2(CONCAT_WS('||', referral_id, event_type,
                    CAST(event_timestamp AS STRING), source_record_id), 256) AS event_id,
          referral_id, event_type, event_timestamp, sequence_number,
          created_by, created_timestamp,
          'DERIVED_SILVER' AS event_source, source_table,
          CURRENT_TIMESTAMP() AS event_materialised_at
        FROM sequenced
    """)
else:
    lifecycle_events = spark.createDataFrame(
        [],
        "event_id string, referral_id string, event_type string, event_timestamp timestamp, "
        "sequence_number int, created_by string, created_timestamp timestamp, "
        "event_source string, source_table string, event_materialised_at timestamp",
    )
replace_silver_materialisation(lifecycle_events, "referral_lifecycle_event")
log_step("Materialised referral_lifecycle_event")

# SI-012: one marked calendar covering the dates present in the current Silver
# state. The range is rebuilt idempotently with each Silver run.
date_sources = []
for table_name, date_column in [
    ("referral", "referral_created_date"),
    ("offer", "offer_date"),
    ("ipa", "created_datetime"),
    ("ipa", "placement_admission_date"),
]:
    qualified = f"{SILVER_SCHEMA}.{table_name}"
    if spark.catalog.tableExists(qualified) and date_column in spark.table(qualified).columns:
        date_sources.append(
            f"SELECT TO_DATE(`{date_column}`) AS date_value FROM {qualified} "
            f"WHERE `{date_column}` IS NOT NULL"
        )

if date_sources:
    date_union = " UNION ALL ".join(date_sources)
    date_dimension = spark.sql(f"""
        WITH source_dates AS ({date_union}),
        bounds AS (
          SELECT MIN(date_value) AS min_date, MAX(date_value) AS max_date
          FROM source_dates
        ),
        calendar AS (
          SELECT EXPLODE(SEQUENCE(min_date, max_date, INTERVAL 1 DAY)) AS date
          FROM bounds
          WHERE min_date IS NOT NULL AND max_date IS NOT NULL
        )
        SELECT date,
          YEAR(date) AS year,
          MONTH(date) AS month_number,
          DATE_FORMAT(date, 'MMMM') AS month_name,
          CONCAT('Q', QUARTER(date)) AS quarter,
          DATE_FORMAT(date, 'EEEE') AS day_of_week
        FROM calendar
    """)
else:
    date_dimension = spark.createDataFrame(
        [],
        StructType([
            StructField("date", DateType(), True),
            StructField("year", IntegerType(), True),
            StructField("month_number", IntegerType(), True),
            StructField("month_name", StringType(), True),
            StructField("quarter", StringType(), True),
            StructField("day_of_week", StringType(), True),
        ]),
    )
replace_silver_materialisation(date_dimension, "dim_date")
print("Silver materialisations ready: age_band, directory_summary_axis, "
      "fostering_axis, referral_closure_reason_summary, dim_date")
log_step("All Silver materialisations complete")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
