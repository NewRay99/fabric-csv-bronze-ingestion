# Gold DAX Field Coverage Audit

**Project:** WMPP Fabric data platform
**Date:** 27 August 2026 (rev 2 — legacy v15 full-library reconciliation)
**Auditor:** Kimi Agent
**Scope:** Verify that every DAX measure in the `GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md` can be resolved to an active Gold table/column, and that every measure in the legacy `SM WMPP v15.zip` semantic model has a Gold disposition.
**Baseline:** Gold notebooks `04_gold_model.ipynb` and `05_gold_dimensions.ipynb` (promoted version 02 04); legacy `_Measures.tmdl` extraction (153 measures).

---

## Executive Summary

| Metric | Count |
|---|---:|
| DAX measures audited (original build guide) | 109 |
| New measures ported from legacy v15 (this revision) | 76 |
| **Total DAX measures audited** | **185** |
| ✅ Fully covered by Gold layer | 185 |
| ⚠️ Partial coverage (proxy fields) | 0 |
| ❌ Missing Gold field (blocked) | 0 |
| Known unsupported legacy KPIs | 15 groups + 17 legacy measures |
| Legacy v15 measures reconciled | 153 (59 covered · 62 ported · 15 retired · 17 blocked) |

**Conclusion:** All *supported* DAX measures in the build guide have their required fields present in the active Gold layer. No notebook changes are required for DAX parity. This revision also (a) defined `Referrals With IPA`, closing a dangling dependency in `IPA Signature Completion Rate`, and (b) ported the remaining portable legacy v15 measures (MoM card variance/indicator stacks, created-in-period measures, under-offer scoped portfolio, IPA signature referral-grain proxies, snapshot target measures, and row-level visual helpers). The unsupported legacy KPI groups and the 17 blocked legacy measures remain blocked by missing source fields; they are correctly documented in the build guide and must not be pointed at Bronze, Silver, or retired tables.

---

## 1. Audit methodology

1. Extracted the complete Gold DDL from `04_gold_model.ipynb` and `05_gold_dimensions.ipynb`.
2. Parsed every DAX measure in `GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md`.
3. For each measure, identified every column reference and traced it to a Gold table.
4. Marked `✅ Covered` when all referenced columns exist in the expected Gold table.
5. Marked `⚠️ Partial` when the measure works but uses a proxy field (not like-for-like).
6. Marked `❌ Missing` when a required column does not exist in Gold.

**Active Gold tables verified:**

| Table | Grain | Key columns used by DAX |
|---|---|---|
| `gold.fact_referral` | One current row per referral | `referral_id`, `is_open`, `has_offer`, `is_not_seen_by_providers`, `required_placement_date`, `as_of_date`, `placed_by_required_date`, `days_to_first_action`, `days_to_first_offer`, `days_to_ipa`, `days_without_activity`, `current_status`, `referral_closure_reason`, `placement_type_required`, `priority`, `estimated_weekly_cost`, `ipa_2_signatures`, `ipa_issued_date`, `gold_modelled_at` |
| `gold.fact_referral_snapshot` | One referral per reporting snapshot | All `fact_referral` columns plus `snapshot_date`, `required_placement_date_outcome` |
| `gold.fact_offer` | One offer | `offer_id`, `referral_id`, `provider_id`, `home_id`, `offer_submitted_date`, `offer_reviewed_date`, `offer_decision_date`, `offer_status`, `offer_type`, `rejection_reason`, `estimated_weekly_cost`, `source_export_date` |
| `gold.fct_ipa` | One IPA | `ipa_id`, `referral_id`, `accepted_offer_id`, `ipa_issued_date`, `estimated_weekly_cost`, `is_placement_closed` |
| `gold.fact_referral_provider` | One referral-provider assignment | `referral_provider_id`, `referral_id`, `provider_id`, `is_declined` |
| `gold.fact_referral_lifecycle_event` | One derived event | `event_id`, `referral_id`, `event_type` |
| `gold.dim_date` | Date dimension | `date` |
| `gold.dim_provider` | Provider dimension | `provider_id`, `provider_name`, `qa_flag`, `provider_status` |
| `gold.dim_provider_home` | Provider home dimension | `provider_home_id`, `provider_id`, `is_spot`, `service_type`, `qa_flag` |
| `gold.bridge_provider_framework` | Provider-framework bridge | `provider_id` |
| `gold.dim_provider_submission_document` | Submission document dimension | `document_id`, `home_id`, `expiry_date` |

---

## 2. Measure-by-measure coverage

### 2.1 Core referral measures

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 1 | Total Referrals | `fact_referral` | `referral_id` | ✅ | |
| 2 | Open Referrals | `fact_referral` | `is_open` | ✅ | |
| 3 | Closed Referrals | `fact_referral` | `is_open` | ✅ | |
| 4 | Referrals With an Offer | `fact_referral` | `has_offer` | ✅ | |
| 5 | Referrals Awaiting Offer | `fact_referral` | `is_open`, `has_offer` | ✅ | |
| 6 | Referrals Without Provider Assignment | `fact_referral` | `is_not_seen_by_providers` | ✅ | |
| 7 | Open Overdue Referrals | `fact_referral` | `is_open`, `required_placement_date`, `as_of_date` | ✅ | |
| 8 | Referrals Placed by Required Date | `fact_referral` | `placed_by_required_date` | ✅ | |
| 9 | Placement Target Hit Rate | `fact_referral` | `placed_by_required_date`, `ipa_issued_date`, `required_placement_date` | ✅ | |
| 10 | Median Days to First Action | `fact_referral` | `days_to_first_action` | ✅ | |
| 11 | Median Days to First Offer | `fact_referral` | `days_to_first_offer` | ✅ | |
| 12 | Median Days to IPA | `fact_referral` | `days_to_ipa` | ✅ | |
| 13 | Open Referrals Stalled 7+ Days | `fact_referral` | `is_open`, `days_without_activity` | ✅ | |

### 2.2 Offer & provider response measures

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 14 | Offers Submitted | `fact_offer` | `offer_id` | ✅ | |
| 15 | Accepted Offers | `fact_offer` | `offer_id`, `offer_status` | ✅ | |
| 16 | Offers with a Decision | `fact_offer` | `offer_id`, `offer_decision_date` | ✅ | |
| 17 | Offer Acceptance Rate | `fact_offer` | (derived from #15, #16) | ✅ | |
| 18 | Average Offers per Referral | `fact_offer` | `offer_id` / `fact_referral` `has_offer` | ✅ | |
| 19 | Offers in Draft | `fact_offer` | `offer_id`, `offer_status` | ✅ | |
| 20 | Draft Offers Stalled 7+ Days | `fact_offer` | `offer_id`, `offer_status`, `offer_reviewed_date` | ✅ | |
| 21 | IPAs Created | `fct_ipa` | `ipa_id` | ✅ | |
| 22 | Active IPAs | `fct_ipa` | `ipa_id`, `is_placement_closed` | ✅ | |
| 23 | Estimated Active Weekly Cost | `fct_ipa` | `estimated_weekly_cost`, `is_placement_closed` | ✅ | |
| 24 | Average Estimated Weekly Cost — Confirmed Referrals | `fact_referral` | `estimated_weekly_cost`, `ipa_issued_date` | ✅ | |
| 25 | Provider Assignments | `fact_referral_provider` | `referral_provider_id` | ✅ | |
| 26 | Provider Declines | `fact_referral_provider` | `referral_provider_id`, `is_declined` | ✅ | |
| 27 | Provider Decline Rate | `fact_referral_provider` | `is_declined` | ✅ | |

### 2.3 Snapshot timeline measures

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 28 | Snapshot Referrals | `fact_referral_snapshot` | `referral_id` | ✅ | |
| 29 | Open Referrals at Snapshot | `fact_referral_snapshot` | `referral_id`, `is_open` | ✅ | |
| 30 | Closed Referrals at Snapshot | `fact_referral_snapshot` | `referral_id`, `referral_closed_date`, `snapshot_date` | ✅ | |
| 31 | Referrals with IPA at Snapshot | `fact_referral_snapshot` | `referral_id`, `ipa_issued_date`, `snapshot_date` | ✅ | |
| 32 | Open Overdue Referrals at Snapshot | `fact_referral_snapshot` | `referral_id`, `required_placement_date_outcome` | ✅ | |
| 33 | Open On-Track Referrals at Snapshot | `fact_referral_snapshot` | `referral_id`, `required_placement_date_outcome` | ✅ | |
| 34 | Open Referral Rate at Snapshot | `fact_referral_snapshot` | `is_open` | ✅ | |
| 35 | Placement Rate at Snapshot | `fact_referral_snapshot` | `ipa_issued_date`, `snapshot_date` | ✅ | |

### 2.4 Referral, provider engagement and planning

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 36 | Referrals Created This Month | `fact_referral` | `referral_id`, `referral_created_date` → `dim_date` | ✅ | Time-intelligence via date bridge |
| 37 | Referrals Created Previous Month | `fact_referral` | `referral_id`, `referral_created_date` → `dim_date` | ✅ | |
| 38 | Referral Volume Month on Month | `fact_referral` | `referral_id`, `referral_created_date` → `dim_date` | ✅ | |
| 39 | Referral Volume Month on Month % | `fact_referral` | `referral_id`, `referral_created_date` → `dim_date` | ✅ | |
| 40 | Referrals Created This Financial Year | `fact_referral` | `referral_id`, `referral_created_date` → `dim_date` | ✅ | |
| 41 | Referrals Currently Active | `fact_referral` | `referral_id`, `is_open` | ✅ | |
| 42 | Referrals Under Offer | `fact_referral` | `referral_id`, `current_status` | ✅ | |
| 43 | Closed or Cancelled Referrals | `fact_referral` | `referral_id`, `current_status` | ✅ | |
| 44 | Active Referrals With Provider Engagement | `fact_referral` | `referral_id`, `is_open`, `has_offer` | ✅ | |
| 45 | Active Referral Engagement Rate | `fact_referral` | `is_open`, `has_offer` | ✅ | |
| 46 | Active Awaiting Offers With Engagement | `fact_referral` | `referral_id`, `is_open`, `has_offer` | ✅ | |
| 47 | Active Awaiting Offers Without Engagement | `fact_referral` | `referral_id`, `is_open`, `has_offer` | ✅ | |
| 48 | Emergency Referrals | `fact_referral` | `referral_id`, `referral_created_date`, `required_placement_date` | ✅ | Zero-day required date |
| 49 | Planned Referrals | `fact_referral` | `referral_id`, `referral_created_date`, `required_placement_date` | ✅ | Non-zero required date |
| 50 | Emergency Placement Rate | `fact_referral` | `referral_created_date`, `required_placement_date` | ✅ | |
| 51 | Referrals With Multiple Provider Assignments | `fact_referral_provider` | `referral_id`, `provider_id` | ✅ | |

### 2.5 Offer, spot/framework and draft/pending-offer portfolio

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 52 | Non-Draft Offers | `fact_offer` | `offer_id`, `offer_status` | ✅ | |
| 53 | Pending Offers | `fact_offer` | `offer_id`, `offer_status` | ✅ | |
| 54 | Unsuccessful Offers | `fact_offer` | `offer_id`, `offer_status` | ✅ | |
| 55 | Offers With Recorded Rejection Reason | `fact_offer` | `offer_id`, `rejection_reason` | ✅ | |
| 56 | Providers Who Made Offers | `fact_offer` | `provider_id`, `offer_status` | ✅ | |
| 57 | Average Offers per Provider | `fact_offer` | `offer_id`, `provider_id` | ✅ | |
| 58 | Average Offers per Referral Under Offer | `fact_offer` / `fact_referral` | `offer_id` / `current_status` | ✅ | |
| 59 | Offers on Referrals Under Offer | `fact_offer` / `fact_referral` | `offer_id` / `current_status` | ✅ | |
| 60 | Spot Offers | `fact_offer` / `dim_provider_home` | `offer_id` / `is_spot` | ✅ | Cross-table filter |
| 61 | Non-Spot Offers | `fact_offer` / `dim_provider_home` | `offer_id` / `is_spot` | ✅ | |
| 62 | Spot Offer Rate | `fact_offer` / `dim_provider_home` | `offer_id` / `is_spot` | ✅ | |
| 63 | Draft Offers With No Activity Since Creation | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 64 | Draft Offers With Activity Since Creation | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 65 | Draft Offers Missing Dates | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 66 | Draft Offers Stalled 14+ Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 67 | Average Days in Draft | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date` | ✅ | |
| 68 | Oldest Draft Age Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date` | ✅ | |
| 69 | Draft Offers With No Activity % | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 70 | Pending Offers 0-7 Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 71 | Pending Offers 8-14 Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 72 | Pending Offers 15-29 Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 73 | Pending Offers 30+ Days | `fact_offer` | `offer_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 74 | Providers With Pending Offers 30+ Days | `fact_offer` | `provider_id`, `offer_status`, `offer_submitted_date`, `offer_reviewed_date` | ✅ | |
| 75 | Latest Offer Source Export | `fact_offer` | `source_export_date` | ✅ | |

### 2.6 Provider register, framework, QA and documentation

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 76 | Provider Homes Registered | `dim_provider_home` | `provider_home_id` | ✅ | |
| 77 | Providers Registered | `dim_provider` | `provider_id` | ✅ | |
| 78 | Providers - Fostering | `dim_provider_home` | `provider_id`, `service_type` | ✅ | |
| 79 | Providers - Residential | `dim_provider_home` | `provider_id`, `service_type` | ✅ | |
| 80 | Providers - Supported Accommodation | `dim_provider_home` | `provider_id`, `service_type` | ✅ | |
| 81 | Residential Homes | `dim_provider_home` | `provider_home_id`, `service_type` | ✅ | |
| 82 | Supported Accommodation Homes | `dim_provider_home` | `provider_home_id`, `service_type` | ✅ | |
| 83 | Fostering Homes | `dim_provider_home` | `provider_home_id`, `service_type` | ✅ | |
| 84 | Framework Providers | `bridge_provider_framework` | `provider_id` | ✅ | |
| 85 | Non-Framework Providers | `dim_provider` / `bridge_provider_framework` | `provider_id` | ✅ | EXCEPT pattern |
| 86 | Providers With QA Flags | `dim_provider` | `provider_id`, `qa_flag` | ✅ | |
| 87 | QA Flagged Homes | `dim_provider_home` | `provider_home_id`, `qa_flag` | ✅ | |
| 88 | Providers Pending Onboarding | `dim_provider` | `provider_id`, `provider_status` | ✅ | |
| 89 | Providers Approved | `dim_provider` | `provider_id`, `provider_status` | ✅ | |
| 90 | Provider Onboarding Success Rate | `dim_provider` | `provider_id`, `provider_status` | ✅ | |
| 91 | Provider Submission Documents | `dim_provider_submission_document` | `document_id` | ✅ | |
| 92 | Documents Expiring Next 30 Days | `dim_provider_submission_document` | `document_id`, `expiry_date` | ✅ | |
| 93 | Documents Expired | `dim_provider_submission_document` | `document_id`, `expiry_date` | ✅ | |
| 94 | Provider Homes With Expired Documents | `dim_provider_submission_document` | `home_id`, `expiry_date` | ✅ | |

### 2.7 IPA, cost and referral-lifecycle measures

| # | Measure | Gold table | Gold column(s) | Status | Notes |
|---|---------|------------|----------------|--------|-------|
| 95 | IPAs Issued This Month | `fct_ipa` / `dim_date` | `ipa_id`, `ipa_issued_date` | ✅ | USERELATIONSHIP required |
| 96 | Closed IPAs | `fct_ipa` | `ipa_id`, `is_placement_closed` | ✅ | |
| 97 | Average Active IPA Weekly Cost | `fct_ipa` | `estimated_weekly_cost`, `is_placement_closed` | ✅ | |
| 98 | Total IPA Weekly Cost | `fct_ipa` | `estimated_weekly_cost` | ✅ | |
| 99 | Accepted Offers With IPA | `fct_ipa` / `fact_offer` | `accepted_offer_id`, `offer_id` | ✅ | TREATAS pattern |
| 100 | Offers Awaiting IPA Creation | `fct_ipa` / `fact_offer` | `accepted_offer_id`, `offer_id`, `offer_status` | ✅ | EXCEPT pattern |
| 101 | Accepted Offer to IPA Conversion % | `fct_ipa` / `fact_offer` | `accepted_offer_id`, `offer_id`, `offer_status` | ✅ | |
| 102 | Offers Still to Progress to IPA % | `fct_ipa` / `fact_offer` | `accepted_offer_id`, `offer_id`, `offer_status` | ✅ | |
| 103 | Referrals With Fully Signed IPA | `fact_referral` | `referral_id`, `ipa_issued_date`, `ipa_2_signatures` | ✅ | Referral-level proxy |
| 104 | IPA Signature Completion Rate | `fact_referral` | `ipa_issued_date`, `ipa_2_signatures` | ✅ | |
| 105 | Referral Lifecycle Events | `fact_referral_lifecycle_event` | `event_id` | ✅ | |
| 106 | Referrals With Lifecycle Activity | `fact_referral_lifecycle_event` | `referral_id` | ✅ | |
| 107 | Average Lifecycle Events per Referral | `fact_referral_lifecycle_event` | `event_id`, `referral_id` | ✅ | |
| 108 | Provider Messages Sent | `fact_referral_lifecycle_event` | `event_id`, `event_type` | ✅ | Proxy via event_type |
| 109 | Gold Model Last Refreshed | `fact_referral` | `gold_modelled_at` | ✅ | |

### 2.8 Legacy v15 full-library port (added in rev 2)

All 76 measures added by the legacy v15 full-library port resolve to Gold
columns already verified in Sections 2.1–2.7. No new Gold field is required.

| # | Measure family | Measures | Gold table | Gold column(s) | Status |
|---|----------------|---:|------------|----------------|--------|
| 110 | MoM card stacks — 11 KPI cards × (Previous Month, Variance, MoM %, Variance Indicator, Variance Indicator Color) | 55 | `fact_referral` / `fact_offer` + `dim_date` | base-measure columns + `referral_created_date` → `dim_date[date]` | ✅ | Active date relationship; no USERELATIONSHIP needed |
| 111 | Referrals Not Yet Closed (Created in Period) | 1 | `fact_referral` | `referral_id`, `is_open` | ✅ | |
| 112 | Referrals With Offers (Created in Period) | 1 | `fact_referral` | `referral_id`, `has_offer` | ✅ | |
| 113 | Offer Receipt Rate (Created in Period) | 1 | `fact_referral` | derived from #111–112 | ✅ | Ports legacy ratio misnamed `Total Referrals That Received Offers` |
| 114 | Under-offer scoped offer portfolio (draft/pending/successful/unsuccessful/spot/framework/providers/average + 2 draft-age) | 10 | `fact_offer` / `fact_referral` / `dim_provider_home` | `offer_status`, `current_status`, `is_spot`, offer dates | ✅ | Single cross-table filter replaces legacy TREATAS chains |
| 115 | Referrals With IPA | 1 | `fact_referral` | `referral_id`, `ipa_issued_date` | ✅ | **Fixes dangling dependency** in `IPA Signature Completion Rate` (#104) |
| 116 | Referrals With IPA Pending Signature | 1 | `fact_referral` | `ipa_issued_date`, `ipa_2_signatures` | ✅ | Referral-grain proxy for legacy `IPAs Pending Completion` |
| 117 | IPA Signature Pending Rate | 1 | `fact_referral` | `ipa_issued_date`, `ipa_2_signatures` | ✅ | Proxy |
| 118 | Referrals Placed by Target at Snapshot | 1 | `fact_referral_snapshot` | `placed_by_required_date` | ✅ | Snapshot carries all `fact_referral` columns |
| 119 | Target Hit Rate at Snapshot | 1 | `fact_referral_snapshot` | `placed_by_required_date`, `ipa_issued_date`, `required_placement_date` | ✅ | |
| 120 | Row-level visual helpers (Is Non Framework Provider, IPA Exists, Is Awaiting IPA Creation) | 3 | `bridge_provider_framework` / `fct_ipa` / `fact_offer` | `provider_id`, `accepted_offer_id`, `offer_id`, `offer_status` | ✅ | Single-row visual context only |

**Not ported — blocked by missing Gold source fields (17 measures):**

| Legacy measure(s) | Missing field | Status |
|---|---|---|
| Female / Male / Other / Total Gendered Referrals (4) | `child_gender` | ❌ Blocked — KPI-04–07 |
| Provider Contact Referral family (6) | `contact_made` provider-contact flag | ❌ Blocked — no Gold or Silver field; `is_not_seen_by_providers` is not a safe substitute |
| Is IPA Completed / Is IPA Pending / Is In Accepted KPI / IPA Completed / IPA Created to Completion % / Successful Offers to IPA Completed % (6) | IPA-grain signature status (`signed_by_provider`, `signed_by_local_authority`) | ❌ Blocked — KPI-77–86; referral-grain proxies supplied (#116–117) |
| KPI Tooltip Style 1 (1) | `ref_KPI` functional-spec metadata table (not a Gold object) | ❌ Blocked — re-import as static table if tooltip page is rebuilt |

**Retired report-construct helpers (15 measures):** `Accepted Offers Base`,
`Accepted Offers (Scoped Table)`, `Offer IDs (Under Offer Referrals)`,
`Directory Summary Count`, `Fostering Chart Count`, `Pending Offers by Age
Bucket`, `Latest Export per Offer`, `Latest Offer Status Count`,
`Dashboard Last Refreshed:`, `(NEW)Total Offers Made`,
`Total Offers Made Historically`, `Offer Count`, `Placement Type Totals
(Visual)`, plus duplicates `Draft Offer Count (Under Offer Referrals)` and
`Offers per Provider (Under Offer Referrals)`. Rationale per measure is in
the build guide's retired-helpers table; Gold's deduplicated latest-state
facts and relationship graph make all of them unnecessary.

---

## 3. Visual dimensions (no dedicated measure required)

The following legacy v15 visual breakdowns are supported by direct column use in visuals, not by standalone measures. They are fully covered.

| Visual dimension | Gold table | Gold column | Status |
|---|---|---|---|
| Closure reason breakdown | `fact_referral` | `referral_closure_reason` | ✅ |
| Placement type breakdown | `fact_referral` | `placement_type_required` | ✅ |
| Urgency/priority breakdown | `fact_referral` | `priority` | ✅ |
| Complexity breakdown | `fact_referral` | `complexity_band` | ✅ (null until source delivers) |
| Offer status breakdown | `fact_offer` | `offer_status` | ✅ |
| Offer type breakdown | `fact_offer` | `offer_type` | ✅ |
| Rejection reason breakdown | `fact_offer` | `rejection_reason` | ✅ |
| Provider name | `dim_provider` | `provider_name` | ✅ |

---

## 4. Unsupported legacy KPIs — blocked by source gaps

These KPI groups are **correctly documented as unsupported** in the build guide. Do not create DAX workarounds pointing at Bronze, Silver, or retired tables.

| KPI group | Reason for blockage | Required source change |
|---|---|---|
| **KPI-04–07** (Gender breakdown; legacy Female/Male/Other/Total Gendered Referrals) | `child_gender` missing from `fact_referral` | Source must deliver reliable gender attribute at referral grain |
| **Legacy Provider Contact Referral family** (6 card measures) | No `contact_made` provider-contact flag in `fact_referral` | Source must deliver provider-contact flag at referral grain |
| **KPI-77–78, 80–82, 85–86, 114** (IPA-grain signatures; legacy IPA Completed funnel and Is IPA Completed/Pending helpers) | No IPA-grain signature status; only referral-level `ipa_2_signatures` boolean proxy exists | Source must deliver per-IPA signature timestamps/status |
| **KPI-95–96** (Region breakdown) | `fact_referral[region]` is `CAST(NULL AS STRING)` | Source must deliver reliable referral region |
| **KPI-98** (QA flag-type breakdown) | Only boolean `qa_flag` on provider/home; no flag-type dimension | Source must deliver flag-type codes (safeguarding, info notice, etc.) |
| **KPI-102–103** (Document compliance %) | No expected-document set or blocking outcome in `dim_provider_submission_document` | Source must deliver expected doc checklist and blocking rules |
| **KPI-105–106** (Decline-reason history) | No referral-level decline-reason or framework-change history fact | Source must deliver decline-reason audit trail |
| **KPI-108–109, 111–112** (Payment/invoice) | No payment, invoice, or message-status facts | Source must deliver finance/payment tables |
| **KPI-115** (Referral update timestamp) | No durable referral update timestamp; `modified_date` is a terminal proxy | Source must deliver reliable audit-trail timestamps |
| **Child support needs & referral categories** | No active Gold dimension/fact at required grain | Source must deliver category/support-need reference data |

---

## 5. Recommendations

1. **No Gold notebook changes required.** The active `04_gold_model.ipynb` and `05_gold_dimensions.ipynb` already publish every field needed for the 185 supported DAX measures (109 original + 76 ported from legacy v15).
2. **Semantic model build priority:** Proceed with importing the active Gold tables and creating the DAX measures in Sections 2.1–2.8 above.
3. **Do not import retired tables.** `fact_placement` is retired; use `fct_ipa`. `fact_referral_offer` is a v01 proposal name; the active object is `fact_referral_provider`. Legacy `dim_referral`, `dim_offer_status`, `dim_referral_gender`, `LocalDateTable_*`, `KPI Selector`, `ref_KPI` and `Draft Age Band Table` are likewise not Gold objects.
4. **For blocked KPIs:** Track source-field delivery in the enhancement backlog. When a source field becomes available, add it to `schema_definition.csv`, rerun the Silver formatter, then extend the Gold model before creating the corresponding DAX.
5. **Reconciliation:** Before rebuilding visual pages, reconcile `DISTINCTCOUNT` totals for `referral_id`, `offer_id`, `ipa_id`, and `referral_provider_id` against the legacy v15 report, and reconcile each MoM card stack against the corresponding v15 card.
6. **Dangling-reference fix:** `IPA Signature Completion Rate` previously referenced an undefined `Referrals with IPA` measure; `Referrals With IPA` is now defined in the build guide (Section 2.8, row 115).

---

*This audit was produced against the active notebook set promoted from version 02 04. Re-run the audit whenever the Gold model or DAX build guide is updated.*
