# %% [markdown]
# # Notebook 3: Gold Translator — Measures & Transformations from PBI Model
# 
# **Purpose:** Translate the Power BI semantic model measures and transformations
# into Spark SQL views and Delta tables in the gold layer. This notebook recreates
# the WMPP PILOT DASHBOARD measures using PySpark SQL against silver tables.
# 
# **Source:** `silver.slv_<table_name>` (typed Delta tables from Notebook 2)
# **Target:** `gold.<view_or_table_name>` (analytical model for reporting)
# **Mode:** Overwrite (gold rebuilt from silver each run)
# 
# **PBI Model being translated (23 tables, 90 measures):**
# 
# **Fact tables (from PBI semantic model):**
#   - fact_referral_offer  ← silver.slv_referral_provider
#   - fact_offer           ← silver.slv_offer
#   - fact_ipa             ← silver.slv_ipa
#   - fact_referral_person ← silver.slv_person
#   - fact_referral_category ← silver.slv_referral_category
#   - fact_provider_message ← silver.slv_referral_provider_message
# 
# **Dimension tables:**
#   - dim_referral, dim_provider, dim_provider_home, dim_provider_framework
#   - dim_category, dim_framework, dim_offer_status, dim_person
#   - dim_referral_gender, dim_referral_provider_message
# 
# **Measure categories (90 total across 11 folders):**
#   - Referral Volume KPIs (10)
#   - Provider Activity KPIs (12)
#   - Timebased KPIs (2)
#   - Spot vs Framework (3)
#   - Referral Offers (12)
#   - Provider Registry (13)
#   - Draft/Pending Offers (11)
#   - Pending offers (9)
#   - IPA Measures (14)
#   - Dashboad Refresh DAX (1)
#   - Miscellaneous Queries (2)
#   - Uncategorized (1)

# %% [markdown]
# ## Step 1 — Configuration

# %%
SILVER_SCHEMA = "silver"
GOLD_SCHEMA   = "gold"
LOAD_MODE     = "overwrite"

# Create gold schema if not exists
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {GOLD_SCHEMA}")

# %% [markdown]
# ## Step 2 — Create Gold Fact Tables (SQL Views over Silver)
# 
# These views map the PBI semantic model fact/dim tables to the
# corresponding silver tables based on schema_definition.csv mappings.

# %%
# ── fact_referral_offer (from referral.referral_provider) ───────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_referral_offer AS
SELECT
    referral_provider_id,
    referral_id,
    provider_id,
    is_excluded,
    is_declined,
    is_cancelled,
    is_closed,
    is_spot,
    created_by,
    modified_by,
    created_timestamp,
    modified_timestamp,
    '_silver_transform_ts' AS _load_ts
FROM {SILVER_SCHEMA}.slv_referral_provider
""")

# ── fact_offer (from offer.offer) ────────────────────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_offer AS
SELECT
    offer_id,
    referral_provider_id,
    offer_status,
    provider_home_id,
    id_number,
    category,
    estimated_start_date,
    core_weekly_fee,
    includes_education,
    education_weekly_fee,
    child_summary_needs,
    offer_date,
    last_modified_date,
    decline_code,
    decline_reason,
    can_edit_offer,
    withdraw_reason,
    withdraw_code,
    offer_type,
    category_code
FROM {SILVER_SCHEMA}.slv_offer
""")

# ── fact_ipa (from ipa.ipa) ─────────────────────────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_ipa AS
SELECT
    ipa_id,
    offer_id,
    referral_id,
    child_full_name,
    child_date_of_birth,
    child_age_years,
    placement_type,
    placement_framework_or_spot,
    costs_total_weekly_fee,
    core_cost_weekly_fee,
    payment_method,
    status,
    signed_by_local_authority,
    signed_by_provider,
    signed_by_provider_name,
    signed_by_local_authority_name,
    closed,
    closed_datetime,
    provider_id,
    provider_name,
    home_name,
    created_datetime,
    updated_datetime
FROM {SILVER_SCHEMA}.slv_ipa
""")

# ── dim_referral (from referral.referral) ───────────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_referral AS
SELECT
    referral_id,
    placement_type_code,
    required_start_date,
    response_required_by_date,
    is_sibling_placement,
    sibling_count,
    is_parent_child_placement,
    is_spot,
    status,
    created_timestamp,
    modified_timestamp,
    created_by,
    modified_by
FROM {SILVER_SCHEMA}.slv_referral
""")

# ── dim_provider (from provider.provider) ──────────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_provider AS
SELECT
    provider_id,
    holding_company_id,
    provider_name,
    provider_status,
    town_city,
    county,
    postcode,
    country,
    is_fostering_spot,
    qa_flag,
    qa_flag_fostering_spot,
    qa_flag_sup_acc,
    qa_flag_resi,
    created_timestamp,
    modified_timestamp
FROM {SILVER_SCHEMA}.slv_provider
""")

# ── dim_provider_home (from provider.provider_home) ────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_provider_home AS
SELECT
    provider_home_id,
    provider_id,
    service_type,
    home_name,
    town_city,
    postcode,
    is_spot,
    number_of_registered_beds,
    qa_flag,
    qa_flag_spot,
    created_timestamp,
    modified_timestamp
FROM {SILVER_SCHEMA}.slv_provider_home
""")

# ── dim_provider_framework (from provider.provider_framework) ──
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_provider_framework AS
SELECT
    provider_framework_id,
    provider_id,
    framework_code,
    qa_flag
FROM {SILVER_SCHEMA}.slv_provider_framework
""")

# ── fact_referral_person (from referral.person) ─────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_referral_person AS
SELECT
    person_id,
    referral_id,
    initials,
    age_value,
    age_date_unit,
    has_restrictions,
    gender_code,
    gender_other,
    ethnicity_code,
    religion_code,
    preferred_language_code,
    child_index
FROM {SILVER_SCHEMA}.slv_person
""")

# ── fact_referral_category (from referral.referral_category) ──
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_referral_category AS
SELECT
    referral_id,
    framework_category_id
FROM {SILVER_SCHEMA}.slv_referral_category
""")

# ── fact_provider_message (from referral.referral_provider_message) ─
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.fact_provider_message AS
SELECT
    message_id,
    message_text,
    created_timestamp,
    created_by,
    referral_provider_id
FROM {SILVER_SCHEMA}.slv_referral_provider_message
""")

print("Gold fact/dim tables created:")
spark.sql(f"SHOW TABLES IN {GOLD_SCHEMA}").show(50, truncate=False)

# %% [markdown]
# ## Step 3 — Create Helper Tables (from PBI model)

# %%
# ── dim_date (local date table equivalent) ─────────────────────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_date AS
SELECT
    sequence(date('2023-01-01'), date('2027-12-31'), interval 1 day) AS date_val
""")
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_date AS
SELECT
    explode(sequence(date('2023-01-01'), date('2027-12-31'), interval 1 day)) AS date,
    year(date) AS year,
    month(date) AS month,
    quarter(date) AS quarter,
    date_format(date, 'MMMM') AS month_name,
    date_format(date, 'EEEE') AS day_name,
    dayofweek(date) AS day_of_week,
    dayofmonth(date) AS day_of_month,
    date_format(date, 'yyyy-MM') AS year_month
FROM (SELECT explode(sequence(date('2023-01-01'), date('2027-12-31'), interval 1 day)) AS date)
""")

# ── Draft Age Band Table (from PBI Draft Age Band Table) ───────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.draft_age_band AS
SELECT
    stack(4,
        'No Activity 7+ Days', 7,
        'No Activity 14+ Days', 14,
        'No Activity 30+ Days', 30,
        'Has Activity', 0
    ) AS (band_label, min_days)
""")

# ── Pending Age Buckets (from PBI Pending offers folder) ──────
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.pending_age_band AS
SELECT
    stack(4,
        '0-7 Days', 0, 7,
        '8-14 Days', 8, 14,
        '15-30 Days', 15, 30,
        '30+ Days', 31, 9999
    ) AS (band_label, min_days, max_days)
""")

print("Helper tables created.")

# %% [markdown]
# ## Step 4 — Gold Measures (SQL Views)
# 
# Each measure from the PBI model is translated to a SQL view.
# The measures use the same logic as described in the WMPP Dashboard
# Overview and KPI Logic Document.

# %%
# ── REFERRAL VOLUME KPIs (10 measures) ──────────────────────────

# Total Referrals — unique referrals in selected period
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_total_referrals AS
SELECT COUNT(DISTINCT referral_id) AS total_referrals
FROM {GOLD_SCHEMA}.dim_referral
WHERE status IS NOT NULL
""")

# Referrals With Offers — open referrals with at least one offer
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_referrals_with_offers AS
SELECT COUNT(DISTINCT r.referral_id) AS referrals_with_offers
FROM {GOLD_SCHEMA}.dim_referral r
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON r.referral_id = rpo.referral_id
WHERE rpo.is_excluded = false
  AND rpo.is_declined = false
""")

# Referrals Awaiting Offer — open referrals with no offers
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_referrals_awaiting_offer AS
SELECT COUNT(DISTINCT r.referral_id) AS referrals_awaiting_offer
FROM {GOLD_SCHEMA}.dim_referral r
WHERE r.status IN ('OPEN', 'UNDER_OFFER')
  AND r.referral_id NOT IN (
      SELECT DISTINCT referral_id
      FROM {GOLD_SCHEMA}.fact_referral_offer
      WHERE is_excluded = false AND is_declined = false
  )
""")

# Male/Female/Other Referrals — from person data
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_gender_referrals AS
SELECT
    gender_code,
    COUNT(DISTINCT referral_id) AS referral_count
FROM {GOLD_SCHEMA}.fact_referral_person
WHERE gender_code IS NOT NULL
GROUP BY gender_code
""")

# Referrals Not Yet Closed (created in period)
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_referrals_not_yet_closed AS
SELECT COUNT(DISTINCT referral_id) AS referrals_not_yet_closed
FROM {GOLD_SCHEMA}.dim_referral
WHERE status NOT IN ('CLOSED', 'CANCELLED')
""")

# ── PROVIDER ACTIVITY KPIs (12 measures) ────────────────────────

# No. Providers Who Made Offers
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_providers_who_made_offers AS
SELECT COUNT(DISTINCT f.provider_id) AS providers_who_made_offers
FROM {GOLD_SCHEMA}.fact_offer f
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON f.referral_provider_id = rpo.referral_provider_id
WHERE f.offer_status NOT IN ('DRAFT', 'WITHDRAWN')
""")

# Total Offers Made (Active Referrals Under Offer)
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_total_offers_made AS
SELECT COUNT(DISTINCT f.offer_id) AS total_offers_made
FROM {GOLD_SCHEMA}.fact_offer f
WHERE f.offer_status NOT IN ('DRAFT')
""")

# Avg Offers per Referral (Under Offer)
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_avg_offers_per_referral AS
SELECT
    COUNT(DISTINCT f.offer_id) * 1.0 / NULLIF(COUNT(DISTINCT rpo.referral_id), 0) AS avg_offers_per_referral
FROM {GOLD_SCHEMA}.fact_offer f
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON f.referral_provider_id = rpo.referral_provider_id
WHERE f.offer_status NOT IN ('DRAFT')
""")

# Avg Offers per Provider (Under Offer)
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_avg_offers_per_provider AS
SELECT
    COUNT(DISTINCT f.offer_id) * 1.0 / NULLIF(COUNT(DISTINCT f.provider_id), 0) AS avg_offers_per_provider
FROM {GOLD_SCHEMA}.fact_offer f
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON f.referral_provider_id = rpo.referral_provider_id
WHERE f.offer_status NOT IN ('DRAFT')
""")

# Successful / Unsuccessful / Draft / Pending Offers
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_offer_status_counts AS
SELECT
    offer_status,
    COUNT(DISTINCT offer_id) AS offer_count
FROM {GOLD_SCHEMA}.fact_offer
GROUP BY offer_status
""")

# Active Referrals With Provider Engagement
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_active_engagement AS
SELECT
    COUNT(DISTINCT CASE WHEN has_offer THEN 1 END) AS active_with_engagement,
    COUNT(DISTINCT r.referral_id) AS total_active,
    COUNT(DISTINCT CASE WHEN has_offer THEN 1 END) * 100.0 / NULLIF(COUNT(DISTINCT r.referral_id), 0) AS engagement_rate
FROM (
    SELECT
        r.referral_id,
        EXISTS (
            SELECT 1 FROM {GOLD_SCHEMA}.fact_referral_offer rpo
            WHERE rpo.referral_id = r.referral_id
              AND rpo.is_excluded = false AND rpo.is_declined = false
        ) AS has_offer
    FROM {GOLD_SCHEMA}.dim_referral r
    WHERE r.status IN ('OPEN', 'UNDER_OFFER')
) r
""")

# ── SPOT vs FRAMEWORK (3 measures) ──────────────────────────────

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_spot_vs_framework AS
SELECT
    CASE WHEN rpo.is_spot THEN 'SPOT' ELSE 'Framework' END AS placement_type,
    COUNT(DISTINCT f.offer_id) AS offer_count
FROM {GOLD_SCHEMA}.fact_offer f
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON f.referral_provider_id = rpo.referral_provider_id
WHERE f.offer_status NOT IN ('DRAFT')
GROUP BY CASE WHEN rpo.is_spot THEN 'SPOT' ELSE 'Framework' END
""")

# ── REFERRAL OFFERS (12 measures) ───────────────────────────────

# Referrals Currently Active
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_referrals_currently_active AS
SELECT COUNT(DISTINCT referral_id) AS active_referrals
FROM {GOLD_SCHEMA}.dim_referral
WHERE status IN ('OPEN', 'UNDER_OFFER')
""")

# Active Referrals Under Offer
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_active_under_offer AS
SELECT COUNT(DISTINCT r.referral_id) AS active_under_offer
FROM {GOLD_SCHEMA}.dim_referral r
INNER JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON r.referral_id = rpo.referral_id
WHERE r.status = 'UNDER_OFFER'
  AND rpo.is_excluded = false AND rpo.is_declined = false
""")

# Referrals Cancelled/Closed
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_referrals_closed AS
SELECT COUNT(DISTINCT referral_id) AS closed_referrals
FROM {GOLD_SCHEMA}.dim_referral
WHERE status IN ('CLOSED', 'CANCELLED')
""")

# Active Referrals Awaiting Offers
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_active_awaiting_offers AS
SELECT COUNT(DISTINCT r.referral_id) AS active_awaiting
FROM {GOLD_SCHEMA}.dim_referral r
WHERE r.status = 'OPEN'
  AND r.referral_id NOT IN (
      SELECT DISTINCT referral_id FROM {GOLD_SCHEMA}.fact_referral_offer
      WHERE is_excluded = false AND is_declined = false
  )
""")

# Closed Referrals by Reason
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_closed_by_reason AS
SELECT
    COALESCE(f.decline_code, f.decline_reason, 'Unknown') AS closure_reason,
    COUNT(DISTINCT r.referral_id) AS referral_count
FROM {GOLD_SCHEMA}.dim_referral r
LEFT JOIN {GOLD_SCHEMA}.fact_referral_offer rpo ON r.referral_id = rpo.referral_id
LEFT JOIN {GOLD_SCHEMA}.fact_offer f ON rpo.referral_provider_id = f.referral_provider_id
WHERE r.status IN ('CLOSED', 'CANCELLED')
GROUP BY COALESCE(f.decline_code, f.decline_reason, 'Unknown')
""")

# ── PROVIDER REGISTRY (13 measures) ─────────────────────────────

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_provider_registry AS
SELECT
    COUNT(DISTINCT provider_id) AS providers_registered,
    COUNT(DISTINCT CASE WHEN provider_status = 'Approved' THEN provider_id END) AS approved_providers,
    COUNT(DISTINCT CASE WHEN provider_status = 'Pending' THEN provider_id END) AS pending_providers,
    COUNT(DISTINCT CASE WHEN is_fostering_spot = true THEN provider_id END) AS spot_providers
FROM {GOLD_SCHEMA}.dim_provider
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_provider_homes AS
SELECT
    ph.service_type,
    COUNT(DISTINCT ph.provider_home_id) AS homes_registered,
    COUNT(DISTINCT p.provider_id) AS providers
FROM {GOLD_SCHEMA}.dim_provider_home ph
INNER JOIN {GOLD_SCHEMA}.dim_provider p ON ph.provider_id = p.provider_id
GROUP BY ph.service_type
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_framework_providers AS
SELECT
    pf.framework_code,
    COUNT(DISTINCT pf.provider_id) AS framework_providers,
    COUNT(DISTINCT CASE WHEN pf.qa_flag = false THEN pf.provider_id END) AS non_framework_providers
FROM {GOLD_SCHEMA}.dim_provider_framework pf
GROUP BY pf.framework_code
""")

# ── DRAFT/PENDING OFFERS (11 + 9 measures) ──────────────────────

# Draft offers analysis
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_draft_offers AS
SELECT
    COUNT(DISTINCT offer_id) AS draft_offer_count,
    COUNT(DISTINCT CASE WHEN offer_date = last_modified_date THEN offer_id END) AS draft_no_activity,
    COUNT(DISTINCT CASE WHEN offer_date != last_modified_date THEN offer_id END) AS draft_with_activity,
    COUNT(DISTINCT CASE WHEN DATEDIFF(current_date(), offer_date) >= 7 THEN offer_id END) AS draft_7plus_days,
    COUNT(DISTINCT CASE WHEN DATEDIFF(current_date(), offer_date) >= 14 THEN offer_id END) AS draft_14plus_days,
    AVG(DATEDIFF(current_date(), offer_date)) AS avg_days_in_draft,
    MAX(DATEDIFF(current_date(), offer_date)) AS oldest_draft_age
FROM {GOLD_SCHEMA}.fact_offer
WHERE offer_status = 'DRAFT'
""")

# Pending offers by age bucket
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_pending_offers_by_age AS
SELECT
    ab.band_label AS age_bucket,
    COUNT(DISTINCT f.offer_id) AS pending_count
FROM {GOLD_SCHEMA}.fact_offer f
CROSS JOIN {GOLD_SCHEMA}.pending_age_band ab
WHERE f.offer_status = 'PENDING'
  AND DATEDIFF(current_date(), f.offer_date) >= ab.min_days
  AND DATEDIFF(current_date(), f.offer_date) <= ab.max_days
GROUP BY ab.band_label, ab.min_days
ORDER BY ab.min_days
""")

# ── IPA MEASURES (14 measures) ─────────────────────────────────

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_ipa_funnel AS
SELECT
    (SELECT COUNT(DISTINCT offer_id) FROM {GOLD_SCHEMA}.fact_offer WHERE offer_status = 'ACCEPTED') AS successful_offers,
    (SELECT COUNT(DISTINCT ipa_id) FROM {GOLD_SCHEMA}.fact_ipa) AS ipa_created,
    (SELECT COUNT(DISTINCT ipa_id) FROM {GOLD_SCHEMA}.fact_ipa WHERE signed_by_local_authority = true AND signed_by_provider = true) AS ipa_completed,
    (SELECT COUNT(DISTINCT ipa_id) FROM {GOLD_SCHEMA}.fact_ipa WHERE (signed_by_local_authority = false OR signed_by_provider = false) AND closed = false) AS ipa_pending_completion,
    (SELECT COUNT(DISTINCT f.offer_id)
     FROM {GOLD_SCHEMA}.fact_offer f
     LEFT JOIN {GOLD_SCHEMA}.fact_ipa i ON f.offer_id = i.offer_id
     WHERE f.offer_status = 'ACCEPTED' AND i.ipa_id IS NULL) AS offers_awaiting_ipa_creation
""")

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_ipa_conversion_rates AS
SELECT
    COUNT(DISTINCT CASE WHEN f.offer_status = 'ACCEPTED' THEN f.offer_id END) AS accepted_offers,
    COUNT(DISTINCT i.ipa_id) AS ipa_created,
    COUNT(DISTINCT CASE WHEN i.signed_by_local_authority = true AND i.signed_by_provider = true THEN i.ipa_id END) AS ipa_completed,
    COUNT(DISTINCT CASE WHEN i.signed_by_local_authority = true AND i.signed_by_provider = true THEN i.ipa_id END) * 100.0
        / NULLIF(COUNT(DISTINCT i.ipa_id), 0) AS ipa_created_to_completion_pct,
    COUNT(DISTINCT i.ipa_id) * 100.0
        / NULLIF(COUNT(DISTINCT CASE WHEN f.offer_status = 'ACCEPTED' THEN f.offer_id END), 0) AS accepted_to_ipa_created_pct,
    COUNT(DISTINCT CASE WHEN i.signed_by_local_authority = true AND i.signed_by_provider = true THEN i.ipa_id END) * 100.0
        / NULLIF(COUNT(DISTINCT CASE WHEN f.offer_status = 'ACCEPTED' THEN f.offer_id END), 0) AS successful_to_completed_pct
FROM {GOLD_SCHEMA}.fact_offer f
LEFT JOIN {GOLD_SCHEMA}.fact_ipa i ON f.offer_id = i.offer_id
""")

# ── TIMEBASED KPIs (2 measures) ─────────────────────────────────

spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_timebased_referrals AS
SELECT
    COUNT(DISTINCT CASE WHEN created_timestamp >= trunc(current_date(), 'month') THEN referral_id END) AS referrals_this_month,
    COUNT(DISTINCT CASE WHEN created_timestamp >= date_trunc('year', current_date()) THEN referral_id END) AS referrals_this_fy
FROM {GOLD_SCHEMA}.dim_referral
""")

# ── MISCELLANEOUS (2 measures) ──────────────────────────────────

# Latest Offer Status Count
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_latest_offer_status AS
SELECT
    offer_status,
    COUNT(DISTINCT offer_id) AS status_count
FROM {GOLD_SCHEMA}.fact_offer
GROUP BY offer_status
ORDER BY status_count DESC
""")

# Dashboard Refresh
spark.sql(f"""
CREATE OR REPLACE VIEW {GOLD_SCHEMA}.mv_dashboard_refresh AS
SELECT current_timestamp() AS dashboard_last_refreshed
""")

print(f"\nAll gold measures/views created.")
print(f"Total gold objects:")

# %% [markdown]
# ## Step 5 — Summary Report

# %%
gold_tables = spark.sql(f"SHOW TABLES IN {GOLD_SCHEMA}").collect()
gold_views_query = spark.sql(f"SHOW VIEWS IN {GOLD_SCHEMA}").collect()

print(f"\n{'='*60}")
print("GOLD LAYER SUMMARY")
print(f"{'='*60}")
print(f"  Tables: {len(gold_tables)}")
print(f"  Views:  {len(gold_views_query)}")
print(f"\n  Tables:")
for t in gold_tables:
    print(f"    {t.tableName}")
print(f"\n  Views (measures):")
for v in gold_views_query:
    print(f"    {v.viewName}")

# %% [markdown]
# ## Step 6 — Verification — Sample Measure Results

# %%
print(f"\n{'='*60}")
print("SAMPLE MEASURE RESULTS")
print(f"{'='*60}")

# Total Referrals
try:
    result = spark.sql(f"SELECT * FROM {GOLD_SCHEMA}.mv_total_referrals").collect()
    print(f"  Total Referrals: {result[0]['total_referrals']}")
except Exception as e:
    print(f"  Total Referrals: (pending data) — {e}")

# Referrals Currently Active
try:
    result = spark.sql(f"SELECT * FROM {GOLD_SCHEMA}.mv_referrals_currently_active").collect()
    print(f"  Active Referrals: {result[0]['active_referrals']}")
except Exception as e:
    print(f"  Active Referrals: (pending data)")

# IPA Funnel
try:
    result = spark.sql(f"SELECT * FROM {GOLD_SCHEMA}.mv_ipa_funnel").collect()
    r = result[0]
    print(f"  Successful Offers: {r['successful_offers']}")
    print(f"  IPA Created: {r['ipa_created']}")
    print(f"  IPA Completed: {r['ipa_completed']}")
    print(f"  IPAs Pending Completion: {r['ipa_pending_completion']}")
except Exception as e:
    print(f"  IPA Funnel: (pending data)")

print(f"\n{'='*60}")
print("Gold layer build complete.")
print("Connect Power BI to the lakehouse and use these gold tables/views")
print("as the new data source, replacing the DirectQuery to AS connection.")
print(f"{'='*60}")
