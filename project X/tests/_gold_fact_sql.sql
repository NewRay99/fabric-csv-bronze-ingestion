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
referral_framework_category AS (
  SELECT referral_id,
    CASE WHEN COUNT(DISTINCT framework_category_id) = 1
      THEN MIN(framework_category_id) END AS framework_category_id,
    COUNT(DISTINCT framework_category_id) AS framework_category_count
  FROM silver.referral_category
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
    COUNT(*) AS journey_assignment_count,
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
-- Aggregate journey evidence before joining so offers/IPAs cannot multiply
-- referral rows. Source-grain Gold facts are built later, so read Silver.
journey_offer_evidence AS (
  SELECT rp.referral_id,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) IN
      ('accepted', 'approved', 'selected', 'offer_successful')
      THEN 1 ELSE 0 END) AS has_accepted_offer,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) IN
      ('pending', 'submitted', 'offered', 'offer_made', 'offer_pending',
       'under_review', 'under review', 'awaiting', 'awaiting_decision', 'awaiting decision')
      THEN 1 ELSE 0 END) AS has_pending_offer,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) NOT IN
      ('accepted', 'approved', 'selected', 'offer_successful',
       'pending', 'submitted', 'offered', 'offer_made', 'offer_pending',
       'under_review', 'under review', 'awaiting', 'awaiting_decision', 'awaiting decision',
       'declined', 'rejected', 'withdrawn', 'closed', 'cancelled', 'canceled',
       'offer_unsuccessful', 'unsuccessful', 'draft')
      THEN 1 ELSE 0 END) AS has_unknown_offer
  FROM silver.offer o
  INNER JOIN referral_provider_current rp
    ON o.referral_provider_id = rp.referral_provider_id
  WHERE o.offer_date IS NULL OR TO_DATE(o.offer_date) <= {AS_OF_SQL}
  GROUP BY rp.referral_id
),
journey_ipa_evidence AS (
  SELECT referral_id,
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_active_ipa,
    -- Both signatures must belong to the same active IPA.
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_signed_active_ipa
  FROM silver.ipa
  WHERE created_datetime IS NULL OR TO_DATE(created_datetime) <= {AS_OF_SQL}
  GROUP BY referral_id
),
base AS (
  SELECT r.referral_id AS referral_id, child.person_id, c.referral_created_date,
    category.framework_category_id,
    COALESCE(category.framework_category_count, 0) AS framework_category_count,
    loc.location, loc.location_match_status, loc.location_is_default, loc.location_requires_review,
    CAST(r.export_date AS TIMESTAMP) AS export_date,
    r.required_start_date AS required_placement_date,
    r.response_required_by_date AS response_required_date,
    r.referral_modified_date AS referral_modified_timestamp,
    r.referral_status AS current_status, r.placement_type AS placement_type_required,
    COALESCE(p.journey_assignment_count, 0) AS journey_assignment_count,
    COALESCE(jo.has_accepted_offer, 0) AS has_accepted_offer,
    COALESCE(jo.has_pending_offer, 0) AS has_pending_offer,
    COALESCE(jo.has_unknown_offer, 0) AS has_unknown_offer,
    COALESCE(ji.has_active_ipa, 0) AS has_active_ipa,
    COALESCE(ji.has_signed_active_ipa, 0) AS has_signed_active_ipa,
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
  LEFT JOIN journey_offer_evidence jo ON r.referral_id = jo.referral_id
  LEFT JOIN journey_ipa_evidence ji ON r.referral_id = ji.referral_id
  LEFT JOIN referral_framework_category category ON r.referral_id = category.referral_id
  LEFT JOIN silver.referral_location loc ON r.referral_id = loc.referral_id
),
journey_classified AS (
  SELECT base.*,
    -- This is a current overall stage, not the latest event or an offer status.
    -- Preserve the existing journey precedence; do not modify current_status.
    CASE
      WHEN LOWER(TRIM(COALESCE(current_status, ''))) IN
        ('closed', 'cancelled', 'canceled', 'withdrawn', 'completed') THEN 7
      WHEN has_signed_active_ipa = 1 THEN 6
      WHEN has_active_ipa = 1 THEN 5
      WHEN has_accepted_offer = 1 THEN 4
      WHEN has_pending_offer = 1 THEN 3
      WHEN has_unknown_offer = 1 OR TRIM(COALESCE(current_status, '')) = '' THEN 8
      WHEN journey_assignment_count > 0 THEN 2
      WHEN referral_created_date IS NOT NULL THEN 1
      ELSE 8
    END AS journey_stage_order
  FROM base
)
SELECT {AS_OF_SQL} AS as_of_date,
  export_date, referral_id, person_id, referral_created_date, required_placement_date,
  framework_category_id, framework_category_count,
  location, location_match_status, location_is_default, location_requires_review,
  response_required_date, first_action_date, first_offer_date,
  offer_accepted_date, ipa_issued_date, referral_closed_date,
  referral_closure_reason, last_activity_date, current_status,
  CASE journey_stage_order
    WHEN 1 THEN 'Referral created'
    WHEN 2 THEN 'Provider search'
    WHEN 3 THEN 'Offers received'
    WHEN 4 THEN 'Offer accepted'
    WHEN 5 THEN 'IPA created'
    WHEN 6 THEN 'IPA signed'
    WHEN 7 THEN 'Closed / cancelled / withdrawn'
    ELSE 'Needs review'
  END AS journey_stage,
  journey_stage_order,
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
FROM journey_classified
WHERE TO_DATE(referral_created_date) <= {AS_OF_SQL}
