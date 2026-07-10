# KPI Reference Guide — Tables, Calculations, and Functional Requirements

**Project:** WMPP (West Midlands Placement Portal)  
**Date:** 10 July 2026  

This document lists every KPI in the gold layer — both the 90 existing measures translated from the Power BI semantic model and the 17 new measures created to close functional spec gaps. Each KPI documents the source tables, calculation logic, and the functional requirement(s) it satisfies.

---

## Table Mapping — Silver to Gold

| Gold Table | Silver Source | Schema Definition Table | Functional Area |
|-----------|--------------|----------------------|-----------------|
| fact_referral_offer | slv_referral_provider | referral.referral_provider | Referral → Provider mapping |
| fact_offer | slv_offer | offer.offer | Provider offers |
| fact_ipa | slv_ipa | ipa.ipa | Individual Placement Agreements |
| dim_referral | slv_referral | referral.referral | Referral header |
| dim_provider | slv_provider | provider.provider | Provider master |
| dim_provider_home | slv_provider_home | provider.provider_home | Provider homes |
| dim_provider_framework | slv_provider_framework | provider.provider_framework | Provider-framework link |
| fact_referral_person | slv_person | referral.person | Child demographics |
| fact_referral_category | slv_referral_category | referral.referral_category | Referral categories |
| fact_provider_message | slv_referral_provider_message | referral.referral_provider_message | Inter-party messages |
| dim_referral_gender | slv_person | referral.person | Gender aggregation |
| fact_referral_event_log | slv_referral_event_log | referral.referral_event_log | Audit trail |
| dim_s3_file_metadata | slv_s3_file_metadata | document.s3_file_metadata | Document metadata |
| dim_provider_document | slv_provider_document | provider.provider_document | Provider docs |
| dim_submission_documents | slv_submission_documents | provider.submission_documents | Onboarding docs |
| dim_referral_provider_decline_reason | slv_referral_provider_decline_reason | referral.referral_provider_decline_reason | Decline reasons |
| dim_offer_status | slv_offer (derived) | offer.offer | Offer status lookup |

---

## Section 1 — Referral Volume KPIs (10 existing)

### KPI-01: Total Referrals `[R24, R51]`
- **Functional ref:** R24 (dashboard referral status overview), R51 (robust data model)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IS NOT NULL`
- **PBI measure:** `Total Referrals` → `EXTERNALMEASURE("Total Referrals", INTEGER, ...)`

### KPI-02: Referrals With Offers `[R24, R36]`
- **Functional ref:** R24 (referral status), R36 (providers with outstanding offers)
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT r.referral_id) JOIN fact_referral_offer rpo WHERE rpo.is_excluded = false AND rpo.is_declined = false`
- **PBI measure:** `Referrals With Offers`

### KPI-03: Referrals Awaiting Offer `[R24, R36]`
- **Functional ref:** R24, R36
- **Tables:** `gold.dim_referral`, `gold.fact_referral_offer` (NOT IN subquery)
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN','UNDER_OFFER') AND referral_id NOT IN (SELECT referral_id FROM fact_referral_offer WHERE is_excluded = false AND is_declined = false)`
- **PBI measure:** `Referrals Awaiting Offer`

### KPI-04: Male Referrals `[R51]`
- **Functional ref:** R51 (demographic monitoring)
- **Tables:** `gold.fact_referral_person`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE gender_code = 'M'` (from `mv_gender_referrals` grouped view)
- **PBI measure:** `Male Referrals`

### KPI-05: Female Referrals `[R51]`
- **Functional ref:** R51
- **Tables:** `gold.fact_referral_person`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE gender_code = 'F'`
- **PBI measure:** `Female Referrals`

### KPI-06: Other Referrals `[R51]`
- **Functional ref:** R51
- **Tables:** `gold.fact_referral_person`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE gender_code NOT IN ('M','F')`
- **PBI measure:** `Other Referrals`

### KPI-07: Total Gendered Referrals `[R51]`
- **Functional ref:** R51
- **Tables:** `gold.fact_referral_person`
- **Calculation:** `SUM(referral_count)` from `mv_gender_referrals` (aggregation of KPI-04, KPI-05, KPI-06)
- **PBI measure:** `Total Gendered Referrals`

### KPI-08: Referrals Not Yet Closed (Created in Period) `[R24]`
- **Functional ref:** R24
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status NOT IN ('CLOSED', 'CANCELLED')`
- **PBI measure:** `Referrals Not Yet Closed (Created in Period)`

### KPI-09: Referrals With Offers (Created in Period) `[R24, R51]`
- **Functional ref:** R24, R51
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** Same as KPI-02 but filtered by `created_timestamp >= period_start`
- **PBI measure:** `Referrals With Offers (Created in Period)`

### KPI-10: Total Referrals That Received Offers `[R51]`
- **Functional ref:** R51 (value analysis — referral offer rate)
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT r.referral_id) WHERE EXISTS (SELECT 1 FROM fact_referral_offer rpo WHERE rpo.referral_id = r.referral_id AND rpo.is_excluded = false AND rpo.is_declined = false)`
- **PBI measure:** `Total Referrals That Recieved Offers`

---

## Section 2 — Provider Activity KPIs (12 existing)

### KPI-11: No. Providers Who Made Offers `[R25, R26]`
- **Functional ref:** R25 (review placement requests), R26 (prioritise requests)
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT provider_id) JOIN fact_referral_offer WHERE offer_status NOT IN ('DRAFT', 'WITHDRAWN')`
- **PBI measure:** `No. Providers Who Made Offers`

### KPI-12: Total Offers Made Historically `[R25-R29]`
- **Functional ref:** R25-R29 (provider offer management)
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status NOT IN ('DRAFT')`
- **PBI measure:** `Total Offers Made Historically`

### KPI-13: Avg Offers per Referral (Under Offer) `[R51]`
- **Functional ref:** R51 (market intelligence)
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) / COUNT(DISTINCT referral_id)` WHERE offer_status NOT IN ('DRAFT')
- **PBI measure:** `Avg Offers per Referral Under Offer`

### KPI-14: Avg Offers per Provider (Under Offer) `[R51]`
- **Functional ref:** R51
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) / COUNT(DISTINCT provider_id)`
- **PBI measure:** `Avg Offers per Provider (Under Offer)`

### KPI-15: Successful Offers (Under Offer Referrals) `[R28]`
- **Functional ref:** R28 (accept placements)
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'ACCEPTED'`
- **PBI measure:** `Successful Offers (Under Offer Referrals)`

### KPI-16: Unsuccessful Offers (Under Offer Referrals) `[R28]`
- **Functional ref:** R28 (reject placements)
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status IN ('DECLINED', 'REJECTED', 'WITHDRAWN')`
- **PBI measure:** `Unsuccessful Offers (Under Offer Referrals)`

### KPI-17: Offers in Draft (Under Offer Referrals) `[R24]`
- **Functional ref:** R24 (dashboard task management)
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT'`
- **PBI measure:** `Offers in Draft (Under Offer Referrals)`

### KPI-18: Pending Offers (Under Offer Referrals) `[R24]`
- **Functional ref:** R24
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING'`
- **PBI measure:** `Pending Offers (Under Offer Referrals)`

### KPI-19: Active Referrals With Provider Engagement `[R24, R26]`
- **Functional ref:** R24, R26
- **Tables:** `gold.dim_referral`, `gold.fact_referral_offer` (EXISTS subquery)
- **Calculation:** `COUNT(DISTINCT CASE WHEN has_offer THEN 1 END)` where `has_offer = EXISTS (SELECT 1 FROM fact_referral_offer WHERE ...)`
- **PBI measure:** `Active Referrals With Provider Engagement`

### KPI-20: Active Referral Engagement Rate `[R24, R26]`
- **Functional ref:** R24, R26
- **Tables:** Same as KPI-19
- **Calculation:** `KPI-19 / COUNT(DISTINCT referral_id WHERE status IN ('OPEN','UNDER_OFFER')) * 100`
- **PBI measure:** `Active Referral Engagement Rate`

### KPI-21: Active Awaiting Offers (Engaged) `[R24, R26]`
- **Functional ref:** R24, R26
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status = 'OPEN' AND has_offer = true`
- **PBI measure:** `Active Awaiting Offers (Engaged)`

### KPI-22: Active Awaiting Offers (No Engagement) `[R24, R26]`
- **Functional ref:** R24, R26
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status = 'OPEN' AND has_offer = false`
- **PBI measure:** `Active Awaiting Offers (No Engagement)`

---

## Section 3 — Timebased KPIs (2 existing)

### KPI-23: Referrals This Month `[R24, R52]`
- **Functional ref:** R24 (dashboard), R52 (accurate reporting)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE created_timestamp >= trunc(current_date(), 'month')`
- **PBI measure:** `Referrals This Month`

### KPI-24: Referrals This FY `[R52]`
- **Functional ref:** R52 (customisable reporting)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE created_timestamp >= date_trunc('year', current_date())`
- **PBI measure:** `Referrals This FY`

---

## Section 4 — Spot vs Framework (3 existing)

### KPI-25: (NEW) Total Offers Made `[R67, R68]`
- **Functional ref:** R67 (add new frameworks), R68 (configure frameworks)
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status NOT IN ('DRAFT')` — used as denominator for spot vs framework split
- **PBI measure:** `(NEW)Total Offers Made`

### KPI-26: Placement Type Totals (Visual) `[R13]`
- **Functional ref:** R13 (filter by placement type)
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) GROUP BY CASE WHEN rpo.is_spot THEN 'SPOT' ELSE 'Framework' END`
- **PBI measure:** `Placement Type Totals (Visual)`

### KPI-27: Spot Offers (Under Offer Referrals) `[R18]`
- **Functional ref:** R18 (emergency placements — partial, spot ≠ emergency)
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE rpo.is_spot = true AND offer_status NOT IN ('DRAFT')`
- **PBI measure:** `Spot Offers (Under Offer Referrals)`

---

## Section 5 — Referral Offers (12 existing)

### KPI-28: Offer Count `[R25-R29]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id)` — base offer count

### KPI-29: Referrals Currently Active `[R24]`
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN', 'UNDER_OFFER')`

### KPI-30: Active Referrals Under Offer `[R24, R36]`
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT r.referral_id) WHERE r.status = 'UNDER_OFFER' AND rpo.is_excluded = false AND rpo.is_declined = false`

### KPI-31: Referrals Cancelled/Closed `[R13]`
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IN ('CLOSED', 'CANCELLED')`

### KPI-32: Active Referrals Awaiting Offers `[R24, R36]`
- **Tables:** `gold.dim_referral`, `gold.fact_referral_offer` (NOT IN)
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status = 'OPEN' AND referral_id NOT IN (SELECT ... FROM fact_referral_offer)`

### KPI-33: Referrals With One or More Offers `[R24]`
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT r.referral_id) JOIN fact_referral_offer WHERE is_excluded = false AND is_declined = false`

### KPI-34: Closed Referrals (by Reason) `[R54]`
- **Functional ref:** R54 (capture reasons for declined placements)
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer` ⟕ `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT r.referral_id) GROUP BY COALESCE(f.decline_code, f.decline_reason, 'Unknown') WHERE r.status IN ('CLOSED', 'CANCELLED')`

### KPI-35: Total Offers Made (Active Referrals Under Offer) `[R25-R29]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status NOT IN ('DRAFT')`

### KPI-36: Offer IDs (Under Offer Referrals) `[R25-R29]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** Distinct offer_id listing — used for DISTINCTCOUNT of offers

### KPI-37: Offers per Provider (Under Offer Referrals) `[R26]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) GROUP BY provider_id` — provider ranking

### KPI-38: Framework Offers (Under Offer Referrals) `[R67, R68]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE rpo.is_spot = false`

### KPI-39: Accepted Offers (Scoped Table) `[R28, R35]`
- **Functional ref:** R28 (accept), R35 (digitised IPA)
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'ACCEPTED'` — base for IPA funnel

---

## Section 6 — Provider Registry (13 existing)

### KPI-40: Provider Homes Registered `[R91, R93]`
- **Functional ref:** R91 (provider registration), R93 (provider directory)
- **Tables:** `gold.dim_provider_home`
- **Calculation:** `COUNT(DISTINCT provider_home_id)`

### KPI-41: Providers Registered `[R91, R93]`
- **Tables:** `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id)`

### KPI-42: Providers - Fostering `[R95]`
- **Functional ref:** R95 (Fostering Framework changes)
- **Tables:** `gold.dim_provider_home` ⟕ `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE service_type = 'Fostering'`

### KPI-43: Providers - Residential `[R96]`
- **Functional ref:** R96 (Residential Framework 2.0)
- **Tables:** `gold.dim_provider_home` ⟕ `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE service_type = 'Residential'`

### KPI-44: Providers - Supported Accommodation `[R91]`
- **Tables:** `gold.dim_provider_home` ⟕ `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE service_type = 'Supported Accommodation'`

### KPI-45: Framework Providers `[R67]`
- **Tables:** `gold.dim_provider_framework`
- **Calculation:** `COUNT(DISTINCT provider_id) GROUP BY framework_code`

### KPI-46: NON Framework Providers `[R46]`
- **Functional ref:** R46 (QA for non-framework providers)
- **Tables:** `gold.dim_provider_framework`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE qa_flag = false`

### KPI-47: Is Non Framework Provider `[R46]`
- **Tables:** `gold.dim_provider_framework`
- **Calculation:** Boolean flag per provider — `qa_flag = false`

### KPI-48: Directory Summary Count `[R93]`
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_provider_home`
- **Calculation:** Aggregated provider count for directory view

### KPI-49: Residential Homes `[R96]`
- **Tables:** `gold.dim_provider_home`
- **Calculation:** `COUNT(DISTINCT provider_home_id) WHERE service_type = 'Residential'`

### KPI-50: Supported Accommodation Homes `[R91]`
- **Tables:** `gold.dim_provider_home`
- **Calculation:** `COUNT(DISTINCT provider_home_id) WHERE service_type = 'Supported Accommodation'`

### KPI-51: Fostering Providers `[R95]`
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_provider_home`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE service_type = 'Fostering'`

### KPI-52: Fostering Chart Count `[R95]`
- **Tables:** `gold.dim_provider_home`
- **Calculation:** Fostering-specific chart aggregation

---

## Section 7 — Draft/Pending Offers (20 existing)

### KPI-53: Draft No Activity Since Creation `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date = last_modified_date`

### KPI-54: Draft Offers With Activity Since Creation `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date != last_modified_date`

### KPI-55: Draft Offers Missing Dates `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND (offer_date IS NULL OR last_modified_date IS NULL)`

### KPI-56: Draft Offers Updated After Creation `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND last_modified_date > offer_date`

### KPI-57: Draft No Activity 7+ Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 7`

### KPI-58: Drafts No Activity 14+ Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 14`

### KPI-59: Average Days in Draft `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `AVG(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'`

### KPI-60: Oldest Draft Age (Days) `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `MAX(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'`

### KPI-61: Draft Offer Count `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT'`

### KPI-62: Draft With No Activity Since Creation (%) `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `KPI-53 / KPI-61 * 100`

### KPI-63: Drafts With No Activity 14+ Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** Same as KPI-58 (duplicate measure in PBI)

### KPI-64: Pending Offers by Age Bucket `[R24]`
- **Tables:** `gold.fact_offer` ⨝ `gold.pending_age_band`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN min_days AND max_days GROUP BY band_label`

### KPI-65: Pending Offers 15–30 Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 15 AND 30`

### KPI-66: Pending Offers 30+ Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30`

### KPI-67: Pending Offers 0–7 Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 0 AND 7`

### KPI-68: Pending Offers 8–14 Days `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 8 AND 14`

### KPI-69: Provider with Offers over 30+ Days `[R24, R26]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_referral_offer`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30`

### KPI-70: Offers At Risk (8–14 Days) `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** Same as KPI-68 (duplicate)

### KPI-71: Offers Outside Timeframe (15–30 Days) `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** Same as KPI-65 (duplicate)

### KPI-72: Critical Offers (30+ Days) `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** Same as KPI-66 (duplicate)

---

## Section 8 — IPA Measures (14 existing)

### KPI-73: IPA Exists `[R35]`
- **Functional ref:** R35 (digitised IPA)
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) > 0` (boolean)

### KPI-74: Is In Accepted KPI `[R28]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa`
- **Calculation:** `offer_status = 'ACCEPTED'` flag — base for IPA funnel

### KPI-75: Accepted Offers Base `[R28, R35]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) WHERE offer_status = 'ACCEPTED'`

### KPI-76: IPA Created `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id)`

### KPI-77: IPA Completed `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) WHERE signed_by_local_authority = true AND signed_by_provider = true`

### KPI-78: IPAs Pending Completion `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) WHERE (signed_by_local_authority = false OR signed_by_provider = false) AND closed = false`

### KPI-79: Offers Awaiting IPA Creation `[R35]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa` (LEFT JOIN, IS NULL)
- **Calculation:** `COUNT(DISTINCT f.offer_id) LEFT JOIN fact_ipa i ON f.offer_id = i.offer_id WHERE f.offer_status = 'ACCEPTED' AND i.ipa_id IS NULL`

### KPI-80: Is IPA Pending `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** Boolean flag — IPA exists but not signed

### KPI-81: Is Awaiting IPA Creation `[R35]**
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa`
- **Calculation:** Boolean flag — accepted offer with no IPA

### KPI-82: Is IPA Completed `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** Boolean flag — both signatures present

### KPI-83: Accepted Offer to IPA Conversion % `[R35]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) / COUNT(DISTINCT accepted_offers) * 100`

### KPI-84: Offers Still to Progress to IPA `[R35]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa`
- **Calculation:** `100 - KPI-83` (complement of conversion rate)

### KPI-85: IPA Created to Completion % `[R35]`
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT all_ipa) * 100`

### KPI-86: Successful Offers to IPA Completed % `[R35]`
- **Tables:** `gold.fact_offer` ⟕ `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT accepted_offers) * 100`

---

## Section 9 — Other Measures (4 existing)

### KPI-87: Dashboard Last Refreshed `[R82]`
- **Tables:** N/A (system timestamp)
- **Calculation:** `current_timestamp()`

### KPI-88: Latest Export per Offer `[R53]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `MAX(offer_date) GROUP BY offer_id`

### KPI-89: Latest Offer Status Count `[R24]`
- **Tables:** `gold.fact_offer`
- **Calculation:** `COUNT(DISTINCT offer_id) GROUP BY offer_status ORDER BY count DESC`

### KPI-90: Overlap Referrals `[R22]`
- **Functional ref:** R22 (out-of-region placements — partial)
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer`
- **Calculation:** Referrals appearing in multiple provider referral-provider mappings

---

## Section 10 — NEW Outstanding Measures (17 measures for functional gaps)

### KPI-91: Emergency Referrals `[R18, R57]` ⭐ HIGH PRIORITY
- **Functional ref:** R18 (emergency placements — distinct identification, separate reporting), R57 (emergency vs planned separately reportable)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN', 'UNDER_OFFER') AND created_timestamp::date = required_start_date`
- **Logic:** A referral is "emergency" when `created_timestamp` date equals `required_start_date` (same-day placement required). This distinguishes from planned placements where there's lead time.
- **Note:** The schema doesn't have an explicit `is_emergency` flag. This is the best proxy using available fields. Consider adding an `is_emergency` boolean to `referral.referral` table in future schema revision.

### KPI-92: Emergency Placement Rate `[R18, R57]` ⭐ HIGH PRIORITY
- **Functional ref:** R18, R57
- **Tables:** `gold.dim_referral`
- **Calculation:** `KPI-91 / KPI-01 * 100` (Emergency Referrals / Total Referrals * 100)

### KPI-93: Planned Referrals `[R57]`
- **Functional ref:** R57 (planned placements separately reportable)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN', 'UNDER_OFFER') AND created_timestamp::date != required_start_date`

### KPI-94: Emergency vs Planned Split `[R18, R57]`
- **Functional ref:** R18, R57
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) GROUP BY CASE WHEN created_timestamp::date = required_start_date THEN 'Emergency' ELSE 'Planned' END`

### KPI-95: Out-of-Region Referrals `[R22]`
- **Functional ref:** R22 (out-of-region placements tagged, finance informed)
- **Tables:** `gold.dim_referral` ⟕ `gold.fact_referral_offer` ⟕ `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT r.referral_id) JOIN fact_referral_offer rpo JOIN dim_provider p WHERE p.country != 'United Kingdom' OR p.county NOT LIKE '%West Midlands%'`
- **Note:** The referral table has no explicit region field. Provider location is used as proxy. Consider adding `is_out_of_region` flag to referral table.

### KPI-96: Out-of-Region Placement Rate `[R22]`
- **Functional ref:** R22
- **Tables:** Same as KPI-95
- **Calculation:** `KPI-95 / KPI-01 * 100`

### KPI-97: Providers with QA Flags `[R41]` ⭐ HIGH PRIORITY
- **Functional ref:** R41 (advisory notices and flags against providers)
- **Tables:** `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE qa_flag = true OR qa_flag_fostering_spot = true OR qa_flag_sup_acc = true OR qa_flag_resi = true`

### KPI-98: QA Flag Type Breakdown `[R41]` ⭐ HIGH PRIORITY
- **Functional ref:** R41 (information notices, safeguarding concerns)
- **Tables:** `gold.dim_provider`
- **Calculation:** `UNPIVOT qa_flag columns → COUNT(DISTINCT provider_id) GROUP BY flag_type`
- **SQL:** Stack the 4 QA flag columns (qa_flag, qa_flag_fostering_spot, qa_flag_sup_acc, qa_flag_resi) into rows with flag_type labels

### KPI-99: QA Flagged Providers by Home `[R41]`
- **Functional ref:** R41
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_provider_home`
- **Calculation:** `COUNT(DISTINCT ph.provider_home_id) JOIN dim_provider p WHERE p.qa_flag = true OR ph.qa_flag = true`

### KPI-100: Documents Expiring (30 Days) `[R47]`
- **Functional ref:** R47 (monitor documentation expiry, send reminders)
- **Tables:** `gold.dim_s3_file_metadata` (from `document.s3_file_metadata`)
- **Calculation:** `COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date IS NOT NULL AND expiry_date BETWEEN current_date() AND date_add(current_date(), 30)`

### KPI-101: Documents Expired `[R47, R48]`
- **Functional ref:** R47 (highlight missing documentation), R48 (exclude providers with incomplete documentation)
- **Tables:** `gold.dim_s3_file_metadata`
- **Calculation:** `COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date IS NOT NULL AND expiry_date < current_date()`

### KPI-102: Providers Blocked (Incomplete Docs) `[R48]`
- **Functional ref:** R48 (providers with incomplete documentation excluded from referrals)
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_provider_document` ⟕ `gold.dim_s3_file_metadata`
- **Calculation:** `COUNT(DISTINCT p.provider_id) WHERE EXISTS (SELECT 1 FROM s3_file_metadata WHERE expiry_date < current_date() AND linked to provider)`
- **SQL:** Join provider → provider_document → s3_file_metadata, filter where expiry_date < current_date()

### KPI-103: Document Compliance Rate `[R48]`
- **Functional ref:** R48
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_s3_file_metadata`
- **Calculation:** `(Total Providers - KPI-102) / Total Providers * 100`

### KPI-104: Provider Due Diligence Status `[R49]`
- **Functional ref:** R49 (identify provider due diligence status)
- **Tables:** `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT provider_id) GROUP BY provider_status` (Approved, Pending, Declined)

### KPI-105: Decline Reasons (Referral Level) `[R54]`
- **Functional ref:** R54 (capture reasons for declined placements)
- **Tables:** `gold.fact_referral_offer` ⟕ `gold.dim_referral_provider_decline_reason` (from `referral.referral_provider_decline_reason`)
- **Calculation:** `COUNT(DISTINCT rpo.referral_id) JOIN decline_reason dr WHERE dr.decline_reason_code IS NOT NULL GROUP BY dr.decline_reason_code`

### KPI-106: Framework Changes During Active Referrals `[R58]`
- **Functional ref:** R58 (commissioners alerted when framework changes during referral activity)
- **Tables:** `gold.fact_referral_category` ⟕ `gold.fact_referral_offer` ⟕ `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT r.referral_id) WHERE r.status IN ('OPEN', 'UNDER_OFFER') AND r.referral_id IN (SELECT referral_id FROM fact_referral_category)` AND the referral_category has been modified (check `modified_timestamp` vs `created_timestamp` on referral)

### KPI-107: Total Weekly Fee Liability `[R62]` ⭐ HIGH PRIORITY
- **Functional ref:** R62 (finance officer — view completed placements, extract payment info)
- **Tables:** `gold.fact_ipa`
- **Calculation:** `SUM(costs_total_weekly_fee) WHERE signed_by_local_authority = true AND signed_by_provider = true AND closed = false`

### KPI-108: Payment Method Breakdown `[R62]`
- **Functional ref:** R62
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) GROUP BY payment_method WHERE closed = false`

### KPI-109: IPA Payment Status `[R62]`
- **Functional ref:** R62
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT ipa_id) GROUP BY CASE WHEN closed = true THEN 'Completed' WHEN signed_by_local_authority = true AND signed_by_provider = true THEN 'Signed' ELSE 'Pending' END`

### KPI-110: Messages Sent `[R14]`
- **Functional ref:** R14 (in-system messaging between placement officers and providers)
- **Tables:** `gold.fact_provider_message` (from `referral.referral_provider_message`)
- **Calculation:** `COUNT(DISTINCT message_id)`

### KPI-111: Avg Message Response Time (Hours) `[R14]`
- **Functional ref:** R14 (auditable messaging, prioritised message types)
- **Tables:** `gold.fact_provider_message` ⟕ `gold.fact_referral_offer`
- **Calculation:** `AVG(HOURS BETWEEN message.created_timestamp AND next_message.created_timestamp)` for same referral_provider_id
- **Note:** This requires a self-join on fact_provider_message ordered by created_timestamp per referral_provider_id

### KPI-112: Priority Messages Unread `[R14]`
- **Functional ref:** R14 (highlight urgent responses)
- **Tables:** `gold.fact_provider_message` ⟕ `gold.fact_provider_message_status` (from `referral.referral_provider_message_status`)
- **Calculation:** `COUNT(DISTINCT m.message_id) WHERE NOT EXISTS (SELECT 1 FROM message_status ms WHERE ms.message_id = m.message_id)`

### KPI-113: Audit Events by Type `[R20]`
- **Functional ref:** R20 (full audit tracking across placement activities, IPA, signatures, approvals)
- **Tables:** `gold.fact_referral_event_log` (from `referral.referral_event_log`)
- **Calculation:** `COUNT(DISTINCT event_id) GROUP BY event_type`

### KPI-114: IPA Signature Completion Rate `[R20, R35]`
- **Functional ref:** R20 (signatures tracked), R35 (electronic signatures)
- **Tables:** `gold.fact_ipa`
- **Calculation:** `COUNT(DISTINCT CASE WHEN signed_by_local_authority = true THEN ipa_id END) AS la_signed, COUNT(DISTINCT CASE WHEN signed_by_provider = true THEN ipa_id END) AS provider_signed, COUNT(DISTINCT CASE WHEN signed_by_local_authority = true AND signed_by_provider = true THEN ipa_id END) AS both_signed, COUNT(DISTINCT ipa_id) AS total_ipa`

### KPI-115: Referral Updates per Day `[R19]`
- **Functional ref:** R19 (placement officers update referrals, auto-notify providers)
- **Tables:** `gold.dim_referral`
- **Calculation:** `COUNT(DISTINCT referral_id) / COUNT(DISTINCT DATE(modified_timestamp)) WHERE modified_timestamp IS NOT NULL`

### KPI-116: Provider Onboarding Pipeline `[R59]`
- **Functional ref:** R59 (bulk provider onboarding)
- **Tables:** `gold.dim_provider` ⟕ `gold.dim_submission_documents` (from `provider.submission_documents`)
- **Calculation:** `COUNT(DISTINCT provider_id) WHERE provider_status = 'Pending'` (providers in onboarding pipeline)

### KPI-117: Bulk Onboarding Success Rate `[R59]`
- **Functional ref:** R59
- **Tables:** `gold.dim_provider`
- **Calculation:** `COUNT(DISTINCT CASE WHEN provider_status = 'Approved' THEN provider_id END) / COUNT(DISTINCT provider_id) * 100`

---

## Summary

| Category | Existing KPIs | New KPIs | Total |
|----------|-------------|----------|-------|
| Referral Volume | 10 | 4 (emergency/planned) | 14 |
| Provider Activity | 12 | 0 | 12 |
| Timebased | 2 | 0 | 2 |
| Spot vs Framework | 3 | 0 | 3 |
| Referral Offers | 12 | 1 (decline reasons) | 13 |
| Provider Registry | 13 | 3 (QA flags, due diligence) | 16 |
| Draft/Pending | 20 | 0 | 20 |
| IPA Measures | 14 | 3 (finance, signatures) | 17 |
| Out-of-Region | 1 | 2 (out-of-region, rate) | 3 |
| Document Compliance | 0 | 4 (expiry, blocked, rate) | 4 |
| Messaging | 0 | 3 (sent, response, unread) | 3 |
| Audit Trail | 0 | 2 (events, signatures) | 2 |
| Onboarding | 0 | 2 (pipeline, success) | 2 |
| Finance | 0 | 3 (fees, payment, status) | 3 |
| **Total** | **90** (existing) | **27** (new) | **117** |
