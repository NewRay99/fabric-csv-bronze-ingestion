CREATE OR REPLACE VIEW gold.fact_referral AS
WITH referral_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_id
    ORDER BY COALESCE(modified_timestamp, created_timestamp) DESC, rev DESC
  ) AS row_number_current
  FROM silver.slv_referral_aud
),
referral_current AS (
  SELECT * FROM referral_history WHERE row_number_current = 1
),
referral_created AS (
  SELECT referral_id, MIN(created_timestamp) AS ReferralCreatedDate
  FROM silver.slv_referral_aud GROUP BY referral_id
),
offer_rollup AS (
  SELECT rp.referral_id,
    MIN(o.offer_date) AS FirstOfferDate,
    MIN(CASE WHEN LOWER(o.offer_status) IN ('accepted','approved','selected')
        THEN o.last_modified_date END) AS OfferAcceptedDate,
    COUNT(DISTINCT o.offer_id) AS OfferCount,
    COUNT(DISTINCT o.provider_home_id) AS UniqueHomesOffered,
    MAX(COALESCE(o.last_modified_date, o.offer_date)) AS LastOfferActivityDate
  FROM silver.slv_offer o
  INNER JOIN silver.slv_referral_provider rp
    ON o.referral_provider_id = rp.referral_provider_id
  GROUP BY rp.referral_id
),
ipa_rollup AS (
  SELECT referral_id, MIN(created_datetime) AS IPAIssuedDate,
    MIN(placement_admission_date) AS PlannedPlacementStartDate,
    SUM(costs_total_weekly_fee) AS EstimatedWeeklyCost,
    MAX(COALESCE(updated_datetime, created_datetime)) AS LastIPAActivityDate
  FROM silver.slv_ipa GROUP BY referral_id
),
event_rollup AS (
  SELECT referral_id, MIN(event_timestamp) AS FirstActionDate,
    MAX(COALESCE(event_timestamp, created_timestamp)) AS LastEventActivityDate
  FROM silver.slv_referral_event_log GROUP BY referral_id
),
base AS (
  SELECT r.referral_id AS ReferralID, c.ReferralCreatedDate,
    r.required_start_date AS RequiredPlacementDate,
    r.response_required_by_date AS ResponseRequiredDate,
    r.modified_timestamp AS ReferralModifiedTimestamp,
    r.status AS CurrentStatus, r.placement_type_code AS PlacementTypeRequired,
    e.FirstActionDate, o.FirstOfferDate, o.OfferAcceptedDate, i.IPAIssuedDate,
    CASE WHEN LOWER(COALESCE(r.status, '')) IN ('closed','cancelled','withdrawn','completed')
      THEN r.modified_timestamp END AS ReferralClosedDate,
    CAST(NULL AS STRING) AS ReferralClosureReason,
    GREATEST(COALESCE(r.modified_timestamp, r.created_timestamp),
      e.LastEventActivityDate, o.LastOfferActivityDate, i.LastIPAActivityDate) AS LastActivityDate,
    o.OfferCount, o.UniqueHomesOffered,
    i.PlannedPlacementStartDate, i.EstimatedWeeklyCost,
    CASE
      WHEN r.required_start_date IS NULL THEN 'Unspecified'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.ReferralCreatedDate)) <= 1 THEN 'Critical'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.ReferralCreatedDate)) <= 3 THEN 'High'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.ReferralCreatedDate)) <= 7 THEN 'Medium'
      ELSE 'Planned'
    END AS PlacementUrgencyBand
  FROM referral_current r
  INNER JOIN referral_created c ON r.referral_id = c.referral_id
  LEFT JOIN offer_rollup o ON r.referral_id = o.referral_id
  LEFT JOIN ipa_rollup i ON r.referral_id = i.referral_id
  LEFT JOIN event_rollup e ON r.referral_id = e.referral_id
)
SELECT {AS_OF_SQL} AS AsOfDate,
  ReferralID, ReferralCreatedDate, RequiredPlacementDate, ResponseRequiredDate,
  FirstActionDate, FirstOfferDate, OfferAcceptedDate, IPAIssuedDate,
  ReferralClosedDate, ReferralClosureReason, LastActivityDate, CurrentStatus,
  PlacementTypeRequired, PlacementUrgencyBand,
  CAST(NULL AS STRING) AS ChildCriticalityCode,
  COALESCE(OfferCount, 0) AS OfferCount,
  COALESCE(UniqueHomesOffered, 0) AS UniqueHomesOffered,
  COALESCE(OfferCount, 0) > 0 AS HasOffer,
  DATEDIFF(TO_DATE(FirstActionDate), TO_DATE(ReferralCreatedDate)) AS DaysToFirstAction,
  DATEDIFF(TO_DATE(FirstOfferDate), TO_DATE(ReferralCreatedDate)) AS DaysToFirstOffer,
  DATEDIFF(TO_DATE(OfferAcceptedDate), TO_DATE(ReferralCreatedDate)) AS DaysToAcceptedOffer,
  DATEDIFF(TO_DATE(IPAIssuedDate), TO_DATE(ReferralCreatedDate)) AS DaysToIPA,
  DATEDIFF(COALESCE(TO_DATE(ReferralClosedDate), {AS_OF_SQL}),
    TO_DATE(ReferralCreatedDate)) AS DaysOpen,
  DATEDIFF({AS_OF_SQL}, TO_DATE(LastActivityDate)) AS DaysWithoutActivity,
  CASE WHEN RequiredPlacementDate IS NOT NULL AND RequiredPlacementDate < {AS_OF_SQL}
    THEN DATEDIFF({AS_OF_SQL}, RequiredPlacementDate) ELSE 0 END AS DaysPastRequiredDate,
  LOWER(COALESCE(CurrentStatus, '')) NOT IN
    ('closed','cancelled','withdrawn','completed') AS IsOpen,
  IPAIssuedDate IS NOT NULL AND RequiredPlacementDate IS NOT NULL
    AND TO_DATE(IPAIssuedDate) <= RequiredPlacementDate AS PlacedByRequiredDate,
  CASE
    WHEN IPAIssuedDate IS NOT NULL AND RequiredPlacementDate IS NOT NULL
      AND TO_DATE(IPAIssuedDate) <= RequiredPlacementDate THEN 'Placed by target'
    WHEN IPAIssuedDate IS NOT NULL THEN 'Placed after target'
    WHEN RequiredPlacementDate < {AS_OF_SQL} AND LOWER(COALESCE(CurrentStatus, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open overdue'
    WHEN LOWER(COALESCE(CurrentStatus, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open on track'
    ELSE 'Closed without placement'
  END AS RequiredPlacementDateOutcome,
  PlannedPlacementStartDate, EstimatedWeeklyCost,
  CURRENT_TIMESTAMP() AS GoldModelledAt
FROM base
WHERE TO_DATE(ReferralCreatedDate) <= {AS_OF_SQL}
