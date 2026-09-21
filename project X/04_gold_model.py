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

# # 04 — Canonical Gold referral model and snapshots
#
# Build Gold referral facts and KPI views from the current Silver state. When
# `AS_OF_DATE` is supplied by the archive replay notebook, calculations and the
# snapshot use that historical export date. With a blank parameter, the notebook
# uses the current date for the live pipeline.

# PARAMETERS CELL ********************

AS_OF_DATE = ""  # Optional YYYY-MM-DD; archive replay passes the month-end export date.
GOLD_SCHEMA = "gold"
SNAPSHOT_TABLE = "gold.fact_referral_snapshot"

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

from datetime import date, datetime
import uuid
from delta.tables import DeltaTable
from pyspark.sql import functions as F

if AS_OF_DATE:
    AS_OF_DATE_VALUE = datetime.strptime(AS_OF_DATE, "%Y-%m-%d").date()
else:
    AS_OF_DATE_VALUE = date.today()
AS_OF_SQL = f"DATE '{AS_OF_DATE_VALUE.isoformat()}'"
GOLD_JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")
print(f"Gold as-of date: {AS_OF_DATE_VALUE}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

GOLD_SOURCE_REQUIREMENTS = {
    "silver.referral": {
        "referral_id", "required_start_date", "response_required_by_date",
        "placement_type", "referral_created_date", "referral_modified_date",
        "referral_status", "export_date",
    },
    "silver.offer": {
        "offer_id", "referral_provider_id", "offer_status", "provider_home_id",
        "offer_date", "last_modified_date", "offer_type",
        "estimated_start_date", "core_weekly_fee", "education_weekly_fee",
        "decline_reason_other", "decline_reason", "withdraw_reason",
        "child_summary_needs", "export_date",
    },
    "silver.referral_provider": {
        "referral_provider_id", "referral_id", "provider_id", "export_date",
        "created_date", "modified_date", "is_excluded", "is_declined",
        "is_cancelled", "is_closed", "is_spot",
    },
    "silver.referral_provider_cancel_reason": {
        "referral_provider_id", "created_date", "export_date",
    },
    "silver.referral_provider_decline_reason": {
        "referral_provider_id", "created_date", "export_date",
    },
    "silver.ipa": {
        "referral_id", "created_datetime", "updated_datetime",
        "ipa_id", "offer_id", "placement_admission_date",
        "costs_total_weekly_fee", "status", "closed", "closed_datetime",
        "signed_by_provider", "signed_by_local_authority",
        "export_date",
    },
    "silver.referral_person": {
        "person_id", "referral_id", "child_index",
    },
    "silver.referral_closure_reason_summary": {
        "referral_id", "closed_referral_reason_bucket",
    },
    "silver.referral_lifecycle_event": {
        "event_id", "referral_id", "event_type", "event_timestamp",
        "sequence_number", "created_by", "created_timestamp",
    },
    "silver.referral_enrichment": {
        "referral_id", "cnt_offer_made", "first_action_date",
        "unique_homes_offered", "estimated_weekly_cost",
        "first_offer_date", "offer_accepted_date", "ipa_issued_date",
        "referral_closed_date", "last_activity_date",
        "first_provider_seen_date", "is_not_seen_by_providers",
        "ipa_placement_admission_date", "ipa_2_signatures",
        "ipa_last_signature_date", "ipa_due_diligence_min_review_date",
        "is_open", "is_awaiting_offer", "is_spot", "provider_assignment_count",
    },
}

gold_input_issues = []
for table_name, required_columns in GOLD_SOURCE_REQUIREMENTS.items():
    if not spark.catalog.tableExists(table_name):
        gold_input_issues.append(f"{table_name}: table is missing")
        continue
    actual_columns = {field.name.lower() for field in spark.table(table_name).schema.fields}
    missing_columns = sorted(required_columns - actual_columns)
    if missing_columns:
        gold_input_issues.append(f"{table_name}: missing {missing_columns}")

if gold_input_issues:
    raise RuntimeError(
        "Gold source validation failed. "
        + "; ".join(gold_input_issues)
        + ". Deploy the current setup notebook so monitoring.cfg_schema_contract_column is refreshed, then rerun "
          "Silver for this snapshot before 04_gold_model."
    )

print("Gold source validation passed")
# Lifecycle events are an explicit Silver derivation from referral, offer, and
# IPA timestamps; they are not a source-system referral-event audit log.
EVENT_ROLLUP_SOURCE = "silver.referral_lifecycle_event"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Gold facts must be managed Delta tables: the Lakehouse semantic model
# discovers tables but does not surface these fact views reliably. Remove
# only the legacy view objects so the following CREATE OR REPLACE TABLE
# statements can retain the same public names during deployment.
GOLD_FACT_TABLES = [
    'gold.fact_referral', 'gold.fact_referral_lifecycle_event',
    'gold.fact_offer', 'gold.fact_ipa', 'gold.fact_referral_provider',
    'gold.fact_provider_kpi_monthly', 'gold.fact_referral_global_summary',
]
for gold_fact_table in GOLD_FACT_TABLES:
    if spark.catalog.tableExists(gold_fact_table):
        table_type = spark.catalog.getTable(gold_fact_table).tableType.upper()
        if table_type == 'VIEW':
            spark.sql(f"DROP VIEW {gold_fact_table}")
            print(f"Dropped legacy view: {gold_fact_table}")

# The IPA fact was formerly named fact_placement. Remove that retired
# object so semantic models cannot continue to bind to it after fact_ipa
# becomes the active Gold IPA fact.
RETIRED_GOLD_FACT_OBJECTS = ['gold.fact_placement']
for retired_object in RETIRED_GOLD_FACT_OBJECTS:
    if spark.catalog.tableExists(retired_object):
        retired_type = spark.catalog.getTable(retired_object).tableType.upper()
        if retired_type == 'VIEW':
            spark.sql(f"DROP VIEW {retired_object}")
        else:
            spark.sql(f"DROP TABLE {retired_object}")
        print(f"Dropped retired Gold object: {retired_object}")

spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral AS
WITH referral_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_id
    ORDER BY COALESCE(referral_modified_date, referral_created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral
),
referral_current AS (
  SELECT * FROM referral_history WHERE row_number_current = 1
),
referral_created AS (
  SELECT referral_id, MIN(referral_created_date) AS referral_created_date
  FROM silver.referral GROUP BY referral_id
),
referral_enrichment AS (
  SELECT * FROM silver.referral_enrichment
),
referral_child AS (
  SELECT referral_id, MIN(CAST(person_id AS STRING)) AS person_id
  FROM silver.referral_person
  GROUP BY referral_id
),
closure_reason AS (
  SELECT referral_id, closed_referral_reason_bucket AS referral_closure_reason
  FROM silver.referral_closure_reason_summary
),
provider_offer_response AS (
  SELECT referral_provider_id,
    MIN(CAST(offer_date AS TIMESTAMP)) AS first_offer_response_at
  FROM silver.offer
  WHERE offer_date IS NOT NULL AND TO_DATE(offer_date) <= {AS_OF_SQL}
  GROUP BY referral_provider_id
),
provider_reason_response AS (
  SELECT referral_provider_id, MIN(response_at) AS first_reason_response_at
  FROM (
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_cancel_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
    UNION ALL
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_decline_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
  ) reason_event
  GROUP BY referral_provider_id
),
referral_provider_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY COALESCE(modified_date, created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral_provider
  WHERE created_date IS NULL OR TO_DATE(created_date) <= {AS_OF_SQL}
),
referral_provider_current AS (
  SELECT * FROM referral_provider_history WHERE row_number_current = 1
),
provider_assignment_response AS (
  SELECT rp.referral_provider_id, rp.referral_id, rp.provider_id,
    COALESCE(CAST(rp.created_date AS TIMESTAMP), CAST(rp.export_date AS TIMESTAMP)) AS assigned_at,
    CASE
      WHEN offer_response.first_offer_response_at IS NULL
        THEN reason_response.first_reason_response_at
      WHEN reason_response.first_reason_response_at IS NULL
        THEN offer_response.first_offer_response_at
      ELSE LEAST(offer_response.first_offer_response_at, reason_response.first_reason_response_at)
    END AS response_at
  FROM referral_provider_current rp
  LEFT JOIN provider_offer_response offer_response
    ON rp.referral_provider_id = offer_response.referral_provider_id
  LEFT JOIN provider_reason_response reason_response
    ON rp.referral_provider_id = reason_response.referral_provider_id
),
provider_response AS (
  SELECT referral_id,
    COUNT(DISTINCT provider_id) AS provider_assignment_count,
    SUM(CASE WHEN response_at IS NOT NULL
      AND (assigned_at IS NULL OR response_at >= assigned_at) THEN 1 ELSE 0 END)
      AS provider_responded_count,
    MIN(CASE WHEN response_at IS NOT NULL
      AND (assigned_at IS NULL OR response_at >= assigned_at) THEN response_at END)
      AS first_provider_response_date
  FROM provider_assignment_response
  GROUP BY referral_id
),
base AS (
  SELECT r.referral_id AS referral_id, child.person_id, c.referral_created_date,
    CAST(r.export_date AS TIMESTAMP) AS export_date,
    r.required_start_date AS required_placement_date,
    r.response_required_by_date AS response_required_date,
    r.referral_modified_date AS referral_modified_timestamp,
    r.referral_status AS current_status, r.placement_type AS placement_type_required,
    -- GLD-014: provider assignment is authoritative; Silver aggregates it
    -- at referral grain so this remains one Gold row per referral.
    COALESCE(x.is_spot, false) AS is_spot,
    x.is_open, x.is_awaiting_offer,
    COALESCE(p.provider_assignment_count, x.provider_assignment_count, 0)
      AS provider_assignment_count,
    COALESCE(p.provider_responded_count, 0) AS provider_responded_count,
    p.first_provider_response_date,
    x.first_action_date, x.first_offer_date,
    x.offer_accepted_date, x.ipa_issued_date,
    x.referral_closed_date,
    closure.referral_closure_reason,
    x.last_activity_date,
    COALESCE(x.cnt_offer_made, 0) AS cnt_offer_made,
    x.first_provider_seen_date,
    x.is_not_seen_by_providers,
    x.ipa_placement_admission_date,
    x.ipa_2_signatures,
    x.ipa_last_signature_date,
    x.ipa_due_diligence_min_review_date,
    COALESCE(x.cnt_offer_made, 0) AS offer_count,
    x.unique_homes_offered,
    x.ipa_placement_admission_date AS planned_placement_start_date,
    x.estimated_weekly_cost,
    CASE
      WHEN r.required_start_date IS NULL THEN 'Unspecified'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 1 THEN 'Critical'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 3 THEN 'High'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 7 THEN 'Medium'
      ELSE 'Planned'
    END AS placement_urgency_band
  FROM referral_current r
  INNER JOIN referral_created c ON r.referral_id = c.referral_id
  LEFT JOIN referral_child child ON r.referral_id = child.referral_id
  LEFT JOIN closure_reason closure ON r.referral_id = closure.referral_id
  LEFT JOIN referral_enrichment x ON r.referral_id = x.referral_id
  LEFT JOIN provider_response p ON r.referral_id = p.referral_id
)
SELECT {AS_OF_SQL} AS as_of_date,
  export_date, referral_id, person_id, referral_created_date, required_placement_date,
  response_required_date, first_action_date, first_offer_date,
  offer_accepted_date, ipa_issued_date, referral_closed_date,
  referral_closure_reason, last_activity_date, current_status,
  placement_type_required,
  CAST(NULL AS STRING) AS region,
  placement_urgency_band AS priority,
  CAST(NULL AS STRING) AS complexity_band,
  placement_urgency_band, cnt_offer_made, first_provider_seen_date,
  is_not_seen_by_providers, ipa_placement_admission_date, ipa_2_signatures,
  ipa_last_signature_date, ipa_due_diligence_min_review_date,
  CAST(NULL AS STRING) AS child_criticality_code,
  offer_count, COALESCE(unique_homes_offered, 0) AS unique_homes_offered,
  COALESCE(offer_count, 0) > 0 AS has_offer,
  DATEDIFF(TO_DATE(first_action_date), TO_DATE(referral_created_date)) AS days_to_first_action,
  DATEDIFF(TO_DATE(first_offer_date), TO_DATE(referral_created_date)) AS days_to_first_offer,
  DATEDIFF(TO_DATE(offer_accepted_date), TO_DATE(referral_created_date)) AS days_to_accepted_offer,
  DATEDIFF(TO_DATE(ipa_issued_date), TO_DATE(referral_created_date)) AS days_to_ipa,
  DATEDIFF(COALESCE(TO_DATE(referral_closed_date), {AS_OF_SQL}),
    TO_DATE(referral_created_date)) AS days_open,
  DATEDIFF({AS_OF_SQL}, TO_DATE(last_activity_date)) AS days_without_activity,
  CASE WHEN required_placement_date IS NOT NULL AND required_placement_date < {AS_OF_SQL}
    THEN DATEDIFF({AS_OF_SQL}, required_placement_date) ELSE 0 END AS days_past_required_date,
  -- GLD-009/GLD-011: is_open and is_awaiting_offer implement the original
  -- business rules in silver.referral_enrichment; Gold propagates them.
  COALESCE(is_open, false) AS is_open,
  COALESCE(is_awaiting_offer, false) AS is_awaiting_offer,
  is_spot,
  -- GLD-013: semantic-model push-downs. provider_assignment_count replaces
  -- the distinct-provider-count DAX; is_emergency_placement mirrors the
  -- Emergency/Planned Referrals same-day rule; is_open_overdue mirrors the
  -- Open Overdue Referrals filter (open and past the required date).
  COALESCE(provider_assignment_count, 0) AS provider_assignment_count,
  COALESCE(provider_responded_count, 0) AS provider_responded_count,
  COALESCE(provider_responded_count, 0) > 0 AS has_provider_response,
  first_provider_response_date,
  required_placement_date IS NOT NULL AND referral_created_date IS NOT NULL
    AND DATEDIFF(TO_DATE(required_placement_date), TO_DATE(referral_created_date)) = 0
    AS is_emergency_placement,
  COALESCE(is_open, false) AND required_placement_date IS NOT NULL
    AND required_placement_date < {AS_OF_SQL} AS is_open_overdue,
  ipa_issued_date IS NOT NULL AND required_placement_date IS NOT NULL
    AND TO_DATE(ipa_issued_date) <= required_placement_date AS placed_by_required_date,
  CASE
    WHEN ipa_issued_date IS NOT NULL AND required_placement_date IS NOT NULL
      AND TO_DATE(ipa_issued_date) <= required_placement_date THEN 'Placed by target'
    WHEN ipa_issued_date IS NOT NULL THEN 'Placed after target'
    WHEN required_placement_date < {AS_OF_SQL} AND LOWER(COALESCE(current_status, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open overdue'
    WHEN LOWER(COALESCE(current_status, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open on track'
    ELSE 'Closed without placement'
  END AS required_placement_date_outcome,
  planned_placement_start_date, estimated_weekly_cost,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM base
WHERE TO_DATE(referral_created_date) <= {AS_OF_SQL}
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Preserve historic snapshot rows while migrating the physical field names
# from the former PascalCase contract to the Gold snake_case convention.
SNAPSHOT_COLUMN_RENAMES = {
    'SnapshotDate': 'snapshot_date', 'ReferralID': 'referral_id', 'ChildID': 'person_id',
    'child_id': 'person_id',
    'ReferralCreatedDate': 'referral_created_date', 'RequiredPlacementDate': 'required_placement_date',
    'FirstActionDate': 'first_action_date', 'FirstOfferDate': 'first_offer_date',
    'OfferAcceptedDate': 'offer_accepted_date', 'IPAIssuedDate': 'ipa_issued_date',
    'ReferralClosedDate': 'referral_closed_date', 'ReferralClosureReason': 'referral_closure_reason',
    'CurrentStatus': 'current_status', 'LastActivityDate': 'last_activity_date',
    'PlacementTypeRequired': 'placement_type_required', 'Region': 'region',
    'Priority': 'priority', 'ComplexityBand': 'complexity_band',
    'PlacementUrgencyBand': 'placement_urgency_band', 'CntOfferMade': 'cnt_offer_made',
    'FirstProviderSeenDate': 'first_provider_seen_date',
    'IsNotSeenByProviders': 'is_not_seen_by_providers',
    'IPAPlacementAdmissionDate': 'ipa_placement_admission_date',
    'IPA2Signatures': 'ipa_2_signatures', 'IPALastSignatureDate': 'ipa_last_signature_date',
    'IPADueDiligenceMinReviewDate': 'ipa_due_diligence_min_review_date',
    'IsOpen': 'is_open', 'HasOffer': 'has_offer', 'OfferCount': 'offer_count',
    'DaysOpen': 'days_open', 'DaysWithoutActivity': 'days_without_activity',
    'DaysPastRequiredDate': 'days_past_required_date',
    'PlacedByRequiredDate': 'placed_by_required_date',
    'RequiredPlacementDateOutcome': 'required_placement_date_outcome',
}
if spark.catalog.tableExists(SNAPSHOT_TABLE):
    snapshot_columns = {field.name for field in spark.table(SNAPSHOT_TABLE).schema.fields}
    for previous_name, current_name in SNAPSHOT_COLUMN_RENAMES.items():
        if previous_name in snapshot_columns and current_name not in snapshot_columns:
            spark.sql(
                f"ALTER TABLE {SNAPSHOT_TABLE} RENAME COLUMN `{previous_name}` TO `{current_name}`"
            )
            snapshot_columns.remove(previous_name)
            snapshot_columns.add(current_name)

snapshot = spark.table("gold.fact_referral").select(
    F.lit(AS_OF_DATE_VALUE).cast("date").alias("snapshot_date"),
    F.trunc(F.lit(AS_OF_DATE_VALUE).cast("date"), "month").alias("snapshot_month_start"),
    F.last_day(F.lit(AS_OF_DATE_VALUE).cast("date")).alias("snapshot_month_end"),
    F.lit("WMPP_SNAPSHOT_V2").alias("snapshot_rule_version"),
    "job_run_id", "export_date", "referral_id", "person_id", "referral_created_date", "required_placement_date",
    "first_action_date", "first_offer_date", "offer_accepted_date", "ipa_issued_date",
    "referral_closed_date", "referral_closure_reason", "current_status",
    "last_activity_date", "placement_type_required", "region", "priority",
    "complexity_band", "placement_urgency_band", "cnt_offer_made",
    "first_provider_seen_date", "is_not_seen_by_providers",
    "ipa_placement_admission_date", "ipa_2_signatures",
    "ipa_last_signature_date", "ipa_due_diligence_min_review_date",
    "is_open", "is_awaiting_offer", "is_spot", "has_offer", "offer_count", "days_open",
    "provider_assignment_count", "provider_responded_count", "has_provider_response",
    "first_provider_response_date", "is_emergency_placement", "is_open_overdue",
    "days_without_activity", "days_past_required_date",
    "placed_by_required_date", "required_placement_date_outcome",
)
month_start = AS_OF_DATE_VALUE.replace(day=1)
next_month_start = (
    month_start.replace(year=month_start.year + 1, month=1)
    if month_start.month == 12
    else month_start.replace(month=month_start.month + 1)
)
month_predicate = (
    f"snapshot_date >= DATE '{month_start.isoformat()}' AND "
    f"snapshot_date < DATE '{next_month_start.isoformat()}'"
)
if not spark.catalog.tableExists(SNAPSHOT_TABLE):
    snapshot.write.format("delta").mode("overwrite").saveAsTable(SNAPSHOT_TABLE)
else:
    # Replacement is scoped to the active calendar month.
    (snapshot.write.format("delta").mode("overwrite")
        .option("replaceWhere", month_predicate)
        .option("mergeSchema", "true")
        .saveAsTable(SNAPSHOT_TABLE))
# Older retained snapshots pre-date the explicit month key and response rule.
# Backfill only deterministic calendar metadata; leave response evidence NULL
# so an unavailable historic response KPI cannot be mistaken for zero.
spark.sql(f"""
UPDATE {SNAPSHOT_TABLE}
SET snapshot_month_start = TRUNC(snapshot_date, 'month'),
    snapshot_month_end = LAST_DAY(snapshot_date),
    snapshot_rule_version = COALESCE(snapshot_rule_version, 'LEGACY_PRE_V2')
WHERE snapshot_month_start IS NULL
   OR snapshot_month_end IS NULL
   OR snapshot_rule_version IS NULL
""")
print(
    f"Snapshot refreshed for {AS_OF_DATE_VALUE}: {snapshot.count():,} referrals; "
    f"replaced active month {month_start:%Y-%m}"
)

# Identifier-free aggregate used only by specifically approved market-wide
# visuals. It intentionally excludes referral, person, provider, authority and
# free-text identifiers so detail RLS cannot be bypassed through this table.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_global_summary AS
SELECT snapshot_month_start, snapshot_month_end, current_status,
  placement_type_required, priority, placement_urgency_band,
  required_placement_date_outcome,
  COUNT(DISTINCT referral_id) AS referral_count,
  SUM(CASE WHEN is_open THEN 1 ELSE 0 END) AS open_referral_count,
  SUM(CASE WHEN NOT is_open THEN 1 ELSE 0 END) AS closed_referral_count,
  SUM(CASE WHEN is_awaiting_offer THEN 1 ELSE 0 END) AS awaiting_offer_count,
  SUM(CASE WHEN has_offer THEN 1 ELSE 0 END) AS referrals_with_offer_count,
  SUM(COALESCE(offer_count, 0)) AS offer_count,
  SUM(CASE WHEN has_provider_response THEN 1 ELSE 0 END) AS provider_response_referral_count,
  SUM(CASE WHEN placed_by_required_date THEN 1 ELSE 0 END) AS placed_by_required_date_count,
  MAX(snapshot_rule_version) AS snapshot_rule_version,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM gold.fact_referral_snapshot
GROUP BY snapshot_month_start, snapshot_month_end, current_status,
  placement_type_required, priority, placement_urgency_band,
  required_placement_date_outcome
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_lifecycle_event AS
SELECT e.event_id, e.referral_id, e.event_type, e.event_timestamp,
  e.sequence_number, e.created_by, r.export_date, '{GOLD_JOB_RUN_ID}' AS job_run_id
FROM {EVENT_ROLLUP_SOURCE} e
LEFT JOIN (
  SELECT referral_id, MAX(CAST(export_date AS TIMESTAMP)) AS export_date
  FROM silver.referral
  GROUP BY referral_id
) r ON e.referral_id = r.referral_id
""")

# Source-grain Gold facts. These retain the individual offer, IPA placement
# and referral-provider records rather than collapsing them into FactReferral.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_offer AS
SELECT {AS_OF_SQL} AS as_of_date,
  o.offer_id AS offer_id, rp.referral_id AS referral_id,o.referral_provider_id,
  rp.provider_id AS provider_id, o.provider_home_id AS home_id,
  CAST(o.offer_date AS TIMESTAMP) AS offer_submitted_date,
  CAST(o.last_modified_date AS TIMESTAMP) AS offer_reviewed_date,
  CASE WHEN LOWER(COALESCE(o.offer_status, '')) IN
    ('offer_successful', 'offer_unsuccessful', 'offer_withdrawn',
     'accepted', 'approved', 'selected', 'declined', 'rejected', 'withdrawn')
    THEN CAST(o.last_modified_date AS TIMESTAMP) END AS offer_decision_date,
  o.offer_status AS offer_status, o.offer_type AS offer_type,
  CAST(o.estimated_start_date AS TIMESTAMP) AS proposed_placement_start_date,
  CAST(NULL AS INT) AS estimated_duration_weeks,
  CAST(COALESCE(o.core_weekly_fee, 0) + COALESCE(o.education_weekly_fee, 0)
    AS DECIMAL(19, 2)) AS estimated_weekly_cost,
  COALESCE(o.decline_reason_other, o.decline_reason, o.withdraw_reason)
    AS rejection_reason,
  o.child_summary_needs AS child_summary_needs,
  -- GLD-013: semantic-model push-downs. offer_age_days replaces the
  -- "Pending Offer Age (Days)" calculated column (as_of date instead of
  -- TODAY(), so snapshots stay reproducible); days_since_offer_activity
  -- backs the draft stalled 7+/14+ day measures; the is_draft_* flags back
  -- the draft data-quality cards; the is_*ipa* flags replace the
  -- per-offer Is Awaiting IPA Creation / Is IPA Pending / Is IPA Completed
  -- row measures.
  DATEDIFF({AS_OF_SQL}, TO_DATE(o.offer_date)) AS offer_age_days,
  DATEDIFF({AS_OF_SQL}, TO_DATE(COALESCE(o.last_modified_date, o.offer_date)))
    AS days_since_offer_activity,
  LOWER(COALESCE(o.offer_status, '')) = 'draft'
    AND (o.offer_date IS NULL OR o.last_modified_date IS NULL)
    AS is_draft_missing_dates,
  LOWER(COALESCE(o.offer_status, '')) = 'draft'
    AND o.offer_date IS NOT NULL AND o.last_modified_date IS NOT NULL
    AND CAST(o.offer_date AS TIMESTAMP) = CAST(o.last_modified_date AS TIMESTAMP)
    AS is_draft_no_activity,
  LOWER(COALESCE(o.offer_status, '')) IN
    ('accepted', 'approved', 'selected', 'offer_successful')
    AND COALESCE(ip.ipa_count, 0) = 0 AS is_awaiting_ipa_creation,
  COALESCE(ip.has_pending_ipa, 0) = 1 AS is_ipa_pending,
  COALESCE(ip.has_completed_ipa, 0) = 1 AS is_ipa_completed,
  CAST(o.export_date AS TIMESTAMP) AS export_date,
  CAST(o.export_date AS TIMESTAMP) AS source_export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM silver.offer o
INNER JOIN silver.referral_provider rp
  ON o.referral_provider_id = rp.referral_provider_id
LEFT JOIN (
  SELECT offer_id, COUNT(*) AS ipa_count,
    MAX(CASE WHEN COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_completed_ipa,
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      AND NOT (COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
        AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false))
      THEN 1 ELSE 0 END) AS has_pending_ipa
  FROM silver.ipa
  WHERE offer_id IS NOT NULL
    AND (created_datetime IS NULL OR TO_DATE(created_datetime) <= {AS_OF_SQL})
  GROUP BY offer_id
) ip ON o.offer_id = ip.offer_id
WHERE o.offer_date IS NULL OR TO_DATE(o.offer_date) <= {AS_OF_SQL}
""")

spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_ipa AS
SELECT {AS_OF_SQL} AS as_of_date,
  i.ipa_id AS ipa_id, i.referral_id AS referral_id,
  i.offer_id AS accepted_offer_id,
  COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false) AS signed_by_provider,
  COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false) AS signed_by_local_authority,
  COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false)
    AND COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false) AS is_ipa_completed,
  NOT COALESCE(CAST(i.closed AS BOOLEAN), false)
    AND NOT (COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false)) AS is_ipa_pending,
  CAST(i.created_datetime AS TIMESTAMP) AS ipa_issued_date,
  CAST(i.placement_admission_date AS TIMESTAMP) AS planned_placement_start_date,
  CAST(NULL AS TIMESTAMP) AS actual_placement_start_date,
  CAST(NULL AS TIMESTAMP) AS planned_placement_end_date,
  CAST(NULL AS TIMESTAMP) AS actual_placement_end_date,
  CAST(i.placement_admission_date AS TIMESTAMP) AS placement_admission_date,
  CAST(i.costs_total_weekly_fee AS DECIMAL(19, 2)) AS estimated_weekly_cost,
  CAST(NULL AS DECIMAL(19, 2)) AS actual_weekly_cost,
  i.status AS placement_status, CAST(i.closed AS BOOLEAN) AS is_placement_closed,
  CAST(i.closed_datetime AS TIMESTAMP) AS placement_ended_date,
  CAST(NULL AS STRING) AS placement_end_reason,
  CAST(i.export_date AS TIMESTAMP) AS export_date,
  CAST(i.export_date AS TIMESTAMP) AS source_export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM silver.ipa i
WHERE i.created_datetime IS NULL OR TO_DATE(i.created_datetime) <= {AS_OF_SQL}
""")

spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_provider AS
WITH referral_provider_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY COALESCE(modified_date, created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral_provider
  WHERE created_date IS NULL OR TO_DATE(created_date) <= {AS_OF_SQL}
), referral_provider_current AS (
  SELECT * FROM referral_provider_history WHERE row_number_current = 1
), offer_response AS (
  SELECT referral_provider_id,
    MIN(CAST(offer_date AS TIMESTAMP)) AS first_offer_response_at
  FROM silver.offer
  WHERE offer_date IS NOT NULL AND TO_DATE(offer_date) <= {AS_OF_SQL}
  GROUP BY referral_provider_id
), reason_response AS (
  SELECT referral_provider_id, MIN(response_at) AS first_reason_response_at
  FROM (
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_cancel_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
    UNION ALL
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_decline_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
  ) response_event
  GROUP BY referral_provider_id
), assignment_response AS (
  SELECT rp.*,
    COALESCE(CAST(rp.created_date AS TIMESTAMP), CAST(rp.export_date AS TIMESTAMP)) AS assigned_at,
    offer_response.first_offer_response_at,
    reason_response.first_reason_response_at,
    CASE
      WHEN offer_response.first_offer_response_at IS NULL
        THEN reason_response.first_reason_response_at
      WHEN reason_response.first_reason_response_at IS NULL
        THEN offer_response.first_offer_response_at
      ELSE LEAST(offer_response.first_offer_response_at, reason_response.first_reason_response_at)
    END AS candidate_response_at
  FROM referral_provider_current rp
  LEFT JOIN offer_response
    ON rp.referral_provider_id = offer_response.referral_provider_id
  LEFT JOIN reason_response
    ON rp.referral_provider_id = reason_response.referral_provider_id
)
SELECT {AS_OF_SQL} AS as_of_date,
  rp.referral_provider_id AS referral_provider_id, rp.referral_id AS referral_id,
  rp.provider_id AS provider_id, rp.assigned_at,
  rp.assigned_at AS first_observed_date,
  rp.first_offer_response_at, rp.first_reason_response_at,
  CASE WHEN rp.candidate_response_at IS NOT NULL
    AND (rp.assigned_at IS NULL OR rp.candidate_response_at >= rp.assigned_at)
    THEN rp.candidate_response_at END AS first_qualifying_response_at,
  CASE WHEN rp.candidate_response_at IS NOT NULL
    AND (rp.assigned_at IS NULL OR rp.candidate_response_at >= rp.assigned_at)
    THEN true ELSE false END AS has_qualifying_response,
  CASE WHEN rp.candidate_response_at IS NOT NULL AND rp.assigned_at IS NOT NULL
    AND rp.candidate_response_at >= rp.assigned_at
    THEN CAST((UNIX_TIMESTAMP(rp.candidate_response_at) - UNIX_TIMESTAMP(rp.assigned_at)) / 60 AS BIGINT)
    END AS response_elapsed_minutes,
  'OFFER_OR_RECORDED_REASON_V1' AS response_evidence_scope,
  CAST(rp.export_date AS TIMESTAMP) AS export_date,
  CAST(rp.is_excluded AS BOOLEAN) AS is_excluded,
  CAST(rp.is_declined AS BOOLEAN) AS is_declined,
  CAST(rp.is_cancelled AS BOOLEAN) AS is_cancelled,
  CAST(rp.is_closed AS BOOLEAN) AS is_closed,
  -- GLD-012: a provider referral is engaged while it is not cancelled,
  -- not closed and not excluded.
  (NOT COALESCE(CAST(rp.is_cancelled AS BOOLEAN), false)
    AND NOT COALESCE(CAST(rp.is_closed AS BOOLEAN), false)
    AND NOT COALESCE(CAST(rp.is_excluded AS BOOLEAN), false)) AS is_engaged,
  CASE
    WHEN rp.is_cancelled THEN 'Cancelled'
    WHEN rp.is_declined THEN 'Declined'
    WHEN rp.is_closed THEN 'Closed'
    WHEN rp.is_excluded THEN 'Excluded'
    ELSE 'Assigned'
  END AS provider_response_status,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM assignment_response rp
""")

# Provider score inputs are materialised without a composite score. Weighting,
# SLA thresholds and minimum-volume rules remain governed business decisions;
# this fact keeps the underlying components auditable until they are approved.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_provider_kpi_monthly AS
WITH offer_component AS (
  SELECT referral_provider_id,
    COUNT(DISTINCT offer_id) AS offers_submitted_count,
    COUNT(DISTINCT CASE WHEN LOWER(COALESCE(offer_status, '')) IN
      ('accepted', 'approved', 'selected', 'offer_successful') THEN offer_id END)
      AS accepted_offer_count
  FROM gold.fact_offer
  GROUP BY referral_provider_id
), assignment_component AS (
  SELECT rp.provider_id, DATE_TRUNC('month', rp.assigned_at) AS assignment_month,
    scope.security_scope_key, rp.referral_provider_id, rp.referral_id,
    rp.has_qualifying_response,
    rp.response_elapsed_minutes,
    COALESCE(o.offers_submitted_count, 0) AS offers_submitted_count,
    COALESCE(o.accepted_offer_count, 0) AS accepted_offer_count,
    COALESCE(f.placed_by_required_date, false) AS placed_by_required_date
  FROM gold.fact_referral_provider rp
  LEFT JOIN offer_component o
    ON rp.referral_provider_id = o.referral_provider_id
  LEFT JOIN gold.fact_referral f ON rp.referral_id = f.referral_id
  LEFT JOIN monitoring.cfg_referral_scope scope
    ON rp.referral_id = scope.referral_id
    AND COALESCE(scope.is_active, false)
    AND (scope.valid_from IS NULL OR scope.valid_from <= {AS_OF_SQL})
    AND (scope.valid_to IS NULL OR scope.valid_to >= {AS_OF_SQL})
  WHERE rp.assigned_at IS NOT NULL
)
SELECT provider_id, CAST(assignment_month AS DATE) AS assignment_month,
  security_scope_key,
  COUNT(DISTINCT referral_provider_id) AS response_opportunity_count,
  SUM(CASE WHEN has_qualifying_response THEN 1 ELSE 0 END) AS qualifying_response_count,
  SUM(offers_submitted_count) AS offers_submitted_count,
  SUM(accepted_offer_count) AS accepted_offer_count,
  COUNT(DISTINCT CASE WHEN accepted_offer_count > 0 THEN referral_id END)
    AS successful_referral_count,
  COUNT(DISTINCT CASE WHEN accepted_offer_count > 0 AND placed_by_required_date
    THEN referral_id END) AS placed_by_target_count,
  AVG(CAST(response_elapsed_minutes AS DOUBLE)) AS average_response_minutes,
  PERCENTILE_APPROX(response_elapsed_minutes, 0.5) AS median_response_minutes,
  'ASSIGNMENT_COHORT_OFFER_OR_REASON_V1' AS kpi_rule_version,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM assignment_component
GROUP BY provider_id, assignment_month, security_scope_key
""")
spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.rpt_kpi_referral_board_summary AS
SELECT as_of_date, placement_urgency_band, required_placement_date_outcome,
  COUNT(DISTINCT referral_id) AS referral_count,
  SUM(CASE WHEN is_open THEN 1 ELSE 0 END) AS open_referral_count,
  SUM(CASE WHEN is_open AND required_placement_date < as_of_date THEN 1 ELSE 0 END) AS open_overdue_count,
  SUM(CASE WHEN placed_by_required_date THEN 1 ELSE 0 END) AS placed_by_required_date_count,
  SUM(CASE WHEN has_offer THEN 1 ELSE 0 END) AS referrals_with_offer_count,
  PERCENTILE_APPROX(days_to_ipa, 0.5) AS median_days_to_ipa,
  SUM(COALESCE(estimated_weekly_cost, 0)) AS estimated_weekly_cost
FROM gold.fact_referral
GROUP BY as_of_date, placement_urgency_band, required_placement_date_outcome
""")
spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.rpt_kpi_referral_monthly AS
SELECT DATE_TRUNC('month', referral_created_date) AS referral_created_month,
  COUNT(DISTINCT referral_id) AS new_referral_count,
  SUM(CASE WHEN has_offer THEN 1 ELSE 0 END) AS referrals_with_offer_count,
  SUM(CASE WHEN ipa_issued_date IS NOT NULL THEN 1 ELSE 0 END) AS ipa_count,
  SUM(CASE WHEN placed_by_required_date THEN 1 ELSE 0 END) AS placed_by_required_date_count,
  SUM(CASE WHEN is_open THEN 1 ELSE 0 END) AS open_referral_count
FROM gold.fact_referral
GROUP BY DATE_TRUNC('month', referral_created_date)
""")
spark.sql("""
CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.rpt_provider_offer_performance AS
SELECT rp.provider_id AS provider_id,
  COUNT(DISTINCT rp.referral_id) AS referrals_received,
  COUNT(DISTINCT o.offer_id) AS offers_submitted,
  COUNT(DISTINCT CASE WHEN LOWER(o.offer_status) IN ('accepted','approved','selected')
    THEN o.offer_id END) AS offers_accepted,
  COUNT(DISTINCT CASE WHEN f.placed_by_required_date THEN f.referral_id END) AS referrals_placed_by_target
FROM silver.referral_provider rp
LEFT JOIN silver.offer o ON rp.referral_provider_id = o.referral_provider_id
LEFT JOIN gold.fact_referral f ON rp.referral_id = f.referral_id
GROUP BY rp.provider_id
""")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
