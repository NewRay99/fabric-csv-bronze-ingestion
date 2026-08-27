# Gold DAX Schema Contract

**Project:** WMPP Fabric data platform
**Layer:** Gold (analytical model)
**Date:** 27 August 2026 (rev 2 — legacy v15 measure-library reconciliation)
**Status:** Current implementation baseline
**Baseline:** Active notebook set version 02 04

---

## 1. Purpose

This document defines the contract between the notebook-created Gold layer and the Power BI semantic model. It specifies:

- Which Gold tables and columns exist
- Which DAX measures consume each column
- Which source gaps remain blocked
- The rules for extending the Gold model when new source fields arrive

This is a companion to the [High-Level Design](HLD.md) and [Technical/Functional Design](TFD.md). It replaces the v01 proposal table inventory with the **active** Gold object set.

---

## 2. Active Gold object inventory

### 2.1 Fact tables

| Table | Grain | Created by | Key DAX consumers |
|---|---|---|---|
| `gold.fact_referral` | One current row per referral | `04_gold_model.ipynb` | All referral-count, status, target, duration and cost measures |
| `gold.fact_referral_snapshot` | One referral per reporting snapshot | `04_gold_model.ipynb` | All point-in-time and historic-trend measures |
| `gold.fact_offer` | One offer | `04_gold_model.ipynb` | Offer-count, acceptance, draft/pending age and spot/framework measures |
| `gold.fct_ipa` | One IPA | `04_gold_model.ipynb` | IPA-count, cost, closure and accepted-offer conversion measures |
| `gold.fact_referral_provider` | One referral-provider assignment | `04_gold_model.ipynb` | Provider-decline and assignment-overlap measures |
| `gold.fact_referral_lifecycle_event` | One derived event | `04_gold_model.ipynb` | Lifecycle-event count and provider-message proxy |

### 2.2 Dimension and bridge tables

| Table | Grain | Created by | Key DAX consumers |
|---|---|---|---|
| `gold.dim_date` | Calendar date | `05_gold_dimensions.ipynb` | Time-intelligence (MTD, YTD, prior period, financial year) |
| `gold.dim_provider` | Provider | `05_gold_dimensions.ipynb` | Provider-register counts, QA flags, onboarding status |
| `gold.dim_provider_home` | Provider home | `05_gold_dimensions.ipynb` | Home counts by service type, spot/framework flags |
| `gold.dim_framework` | Framework | `05_gold_dimensions.ipynb` | Framework dimension (see CFG-005 note) |
| `gold.dim_framework_category` | Framework category | `05_gold_dimensions.ipynb` | Framework category breakdown |
| `gold.dim_placement_type` | Placement type | `05_gold_dimensions.ipynb` | Placement-type filter dimension |
| `gold.dim_referral_status` | Referral status | `05_gold_dimensions.ipynb` | Status filter dimension |
| `gold.dim_provider_submission_document` | Submission document | `05_gold_dimensions.ipynb` | Document expiry and compliance measures |
| `gold.bridge_provider_framework` | Provider-framework link | `05_gold_dimensions.ipynb` | Framework vs non-framework provider counts |
| `gold.bridge_provider_sic_code` | Provider-SIC link | `05_gold_dimensions.ipynb` | Industry-classification breakdowns |

### 2.3 KPI views

| View | Purpose | Created by |
|---|---|---|
| `gold.vw_kpi_referral_board_summary` | Board headline totals by as-of date, urgency and target outcome | `04_gold_model.ipynb` |
| `gold.vw_kpi_referral_monthly` | Monthly created/offer/IPA trend | `04_gold_model.ipynb` |
| `gold.vw_provider_offer_performance` | Provider referral, offer, acceptance and target-placement totals | `04_gold_model.ipynb` |

---

## 3. Column-to-DAX mapping

### 3.1 `fact_referral` — core referral fact

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `referral_id` | STRING (PK) | `silver.referral` | Total Referrals, all referral-count measures |
| `is_open` | BOOLEAN | Derived from `current_status` | Open Referrals, Closed Referrals, Open Overdue, Stalled |
| `has_offer` | BOOLEAN | Derived from `silver.referral_enrichment` | Referrals With an Offer, Awaiting Offer, Engagement measures |
| `is_not_seen_by_providers` | BOOLEAN | Derived from `silver.referral_enrichment` | Referrals Without Provider Assignment |
| `required_placement_date` | DATE | `silver.referral` | Open Overdue, Emergency/Planned split, Target Hit Rate |
| `as_of_date` | DATE | Derived (run date) | Open Overdue, Age calculations |
| `placed_by_required_date` | BOOLEAN | Derived from IPA vs required date | Referrals Placed by Required Date, Target Hit Rate |
| `days_to_first_action` | INT | `silver.referral_enrichment` | Median Days to First Action |
| `days_to_first_offer` | INT | `silver.referral_enrichment` | Median Days to First Offer |
| `days_to_ipa` | INT | `silver.referral_enrichment` | Median Days to IPA |
| `days_without_activity` | INT | Derived | Open Referrals Stalled 7+ Days |
| `current_status` | STRING | `silver.referral` | Referrals Under Offer, Closed/Cancelled, Engagement |
| `referral_closure_reason` | STRING | `silver.referral` | Visual dimension — closure reason breakdown |
| `placement_type_required` | STRING | `silver.referral` | Visual dimension — placement type |
| `priority` | STRING | `silver.referral` | Visual dimension — urgency band |
| `estimated_weekly_cost` | DECIMAL | `silver.referral` | Average Estimated Weekly Cost — Confirmed Referrals |
| `ipa_2_signatures` | BOOLEAN | Derived from `silver.referral_enrichment` | Referrals With Fully Signed IPA, Signature Completion Rate |
| `ipa_issued_date` | DATE | `silver.referral_enrichment` | Placement Target Hit Rate, Fully Signed IPA |
| `gold_modelled_at` | TIMESTAMP | Derived | Gold Model Last Refreshed |
| `referral_created_date` | DATE | `silver.referral` | Time-intelligence measures (MTD, FY, etc.) |
| `region` | STRING | `CAST(NULL AS STRING)` | **Blocked** — see Section 5 |
| `complexity_band` | STRING | `CAST(NULL AS STRING)` | **Blocked** — see Section 5 |

### 3.2 `fact_referral_snapshot` — point-in-time store

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `snapshot_date` | DATE | Derived (canonical month date) | All snapshot measures |
| `referral_id` | STRING | `silver.referral` | Snapshot Referrals |
| `is_open` | BOOLEAN | Derived | Open/Closed at Snapshot |
| `referral_closed_date` | DATE | Derived | Closed Referrals at Snapshot |
| `ipa_issued_date` | DATE | Derived | Referrals with IPA at Snapshot |
| `required_placement_date_outcome` | STRING | Derived | Open Overdue / On-Track at Snapshot |
| *(all other `fact_referral` columns)* | — | — | Available for future snapshot measures |

### 3.3 `fact_offer` — offer grain

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `offer_id` | STRING (PK) | `silver.offer` | Offers Submitted, all offer-count measures |
| `referral_id` | STRING (FK) | `silver.offer` | Relationship to `fact_referral` |
| `provider_id` | STRING (FK) | `silver.offer` | Providers Who Made Offers, Average per Provider |
| `home_id` | STRING (FK) | `silver.offer` | Relationship to `dim_provider_home` |
| `offer_submitted_date` | DATE | `silver.offer` | Draft age, pending age measures |
| `offer_reviewed_date` | DATE | `silver.offer` | Draft age, pending age measures |
| `offer_decision_date` | DATE | `silver.offer` | Offers with a Decision |
| `offer_status` | STRING | `silver.offer` | Accepted, Draft, Pending, Unsuccessful measures |
| `offer_type` | STRING | `silver.offer` | Visual dimension |
| `rejection_reason` | STRING | `silver.offer` | Offers With Recorded Rejection Reason |
| `estimated_weekly_cost` | DECIMAL | `silver.offer` | Cost analysis |
| `source_export_date` | DATE | `silver.offer` | Latest Offer Source Export |

### 3.4 `fct_ipa` — IPA grain

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `ipa_id` | STRING (PK) | `silver.ipa` | IPAs Created, all IPA-count measures |
| `referral_id` | STRING (FK) | `silver.ipa` | Relationship to `fact_referral` |
| `accepted_offer_id` | STRING (FK) | `silver.ipa` | Accepted Offers With IPA (TREATAS pattern) |
| `ipa_issued_date` | DATE | `silver.ipa` | IPAs Issued This Month |
| `estimated_weekly_cost` | DECIMAL | `silver.ipa` | Estimated Active Weekly Cost, Total IPA Weekly Cost |
| `is_placement_closed` | BOOLEAN | Derived | Active IPAs, Closed IPAs, cost measures |

### 3.5 `fact_referral_provider` — provider response grain

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `referral_provider_id` | STRING (PK) | `silver.referral_provider` | Provider Assignments |
| `referral_id` | STRING (FK) | `silver.referral_provider` | Relationship to `fact_referral` |
| `provider_id` | STRING (FK) | `silver.referral_provider` | Relationship to `dim_provider` |
| `is_declined` | BOOLEAN | Derived | Provider Declines, Decline Rate |

### 3.6 `fact_referral_lifecycle_event` — derived event grain

| Column | Data type | Source | DAX measures using it |
|---|---|---|---|
| `event_id` | STRING (PK) | Derived | Referral Lifecycle Events |
| `referral_id` | STRING (FK) | Derived | Referrals With Lifecycle Activity |
| `event_type` | STRING | Derived | Provider Messages Sent (proxy) |

**Note:** This table is derived from available Silver timestamps. It is **not** a complete source-system audit trail. Do not use it for compliance audit requirements without validating coverage.

---

## 4. Relationship rules for the semantic model

### 4.1 Active relationships (required)

| From | To | Cardinality | Notes |
|---|---|---|---|
| `fact_referral[referral_id]` | `fact_offer[referral_id]` | 1:* | |
| `fact_referral[referral_id]` | `fct_ipa[referral_id]` | 1:* | |
| `fact_referral[referral_id]` | `fact_referral_provider[referral_id]` | 1:* | |
| `dim_provider[provider_id]` | `fact_offer[provider_id]` | 1:* | |
| `dim_provider[provider_id]` | `fact_referral_provider[provider_id]` | 1:* | |
| `dim_provider_home[provider_home_id]` | `fact_offer[home_id]` | 1:* | |
| `dim_provider[provider_id]` | `dim_provider_home[provider_id]` | 1:* | |
| `dim_provider[provider_id]` | `bridge_provider_framework[provider_id]` | 1:* | |
| `dim_provider_home[provider_home_id]` | `dim_provider_submission_document[home_id]` | 1:* | |

### 4.2 Date relationships

| Date table | Fact column | Status | Purpose |
|---|---|---|---|
| `dim_date[date]` | `fact_referral[referral_created_date]` | Active (or role-playing) | Referral-created time intelligence |
| `dim_date[date]` | `fact_referral_snapshot[snapshot_date]` | Active (or role-playing) | Snapshot timeline |
| `dim_date[date]` | `fct_ipa[ipa_issued_date]` | **Inactive** — use USERELATIONSHIP | IPA-issued time intelligence |
| `dim_date[date]` | `fact_referral[required_placement_date]` | Inactive | Target date analysis |
| `dim_date[date]` | `fact_referral[referral_closed_date]` | Inactive | Closure date analysis |

### 4.3 Relationship to avoid

Do **not** create an active `fact_offer[offer_id]` → `fct_ipa[accepted_offer_id]` relationship when it creates an ambiguous route. Use `USERELATIONSHIP` or `TREATAS` in specific conversion measures only.

---

## 5. Blocked fields and source gaps

The following fields exist in the Gold schema but are **not populated** by the current source extracts. DAX measures must not invent values for them.

| Field | Why blocked | What would unblock it |
|---|---|---|
| `fact_referral[region]` | `CAST(NULL AS STRING)` | Source CSV must deliver reliable referral region |
| `fact_referral[complexity_band]` | `CAST(NULL AS STRING)` | Source must deliver complexity/need classification |
| `fact_referral[contact_made]` | Not in source (legacy `dim_referral[contact_made]`) | Source must deliver a provider-contact flag at referral grain (legacy Provider Contact Referral card family) |
| `fct_ipa[actual_placement_start_date]` | Not in source | Source must deliver actual placement dates |
| `fct_ipa[actual_placement_end_date]` | Not in source | Source must deliver actual placement dates |
| `fct_ipa[actual_weekly_cost]` | Not in source | Source must deliver actual cost/invoice data |
| `fct_ipa[end_reason]` | Not in source | Source must deliver placement end reason |

The following KPI groups require fields that do not exist in **any** Gold table:

| KPI group | Missing field/grain | Required source change |
|---|---|---|
| KPI-04–07 | `child_gender` | Add gender to referral extract |
| Legacy Provider Contact Referral family (6 measures) | `contact_made` | Add provider-contact flag to referral extract |
| KPI-77–78, 80–82, 85–86, 114 | IPA-grain signature status | Add signature audit trail to IPA extract |
| KPI-98 | QA flag-type dimension | Add flag-type codes to provider extract |
| KPI-102–103 | Expected-document checklist | Add document compliance rules to source |
| KPI-105–106 | Referral-level decline-reason history | Add decline-reason audit to referral extract |
| KPI-108–109, 111–112 | Payment/invoice facts | Add finance tables to extract |
| KPI-115 | Durable update timestamp | Add reliable audit trail to source |

---

## 6. Extension rules

When a new source field becomes available:

1. **Schema contract:** Add the column to `schema_definition.csv` with the correct type, PK/FK flags, and description.
2. **Silver:** The `02_silver_formatter.ipynb` will automatically cast and deduplicate the new column.
3. **Gold enrichment:** If the field is used for KPIs, add it to `silver.referral_enrichment` in `03_silver_business_rules.ipynb` or directly in `04_gold_model.ipynb`.
4. **Gold fact/dimension:** Add the column to the appropriate Gold table in `04_gold_model.ipynb` or `05_gold_dimensions.ipynb`.
5. **DAX:** Update `GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md` with the new measure(s).
6. **This contract:** Update the column-to-DAX mapping in Section 3 and remove the field from Section 5.
7. **ETL log:** Record the change in `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md` with prefix `GLD`.

---

## 7. Verification checklist

Before declaring the semantic model ready:

- [ ] All tables in Section 2.1–2.2 are imported
- [ ] All relationships in Section 4.1 are created
- [ ] Date relationships in Section 4.2 are configured (active or inactive as specified)
- [ ] No ambiguous `fact_offer` → `fct_ipa` relationship exists
- [ ] All 185 measures in `GOLD_DAX_FIELD_COVERAGE_AUDIT.md` (109 original + 76 legacy v15 ports) are created and total correctly
- [ ] Every measure extracted from the legacy `SM WMPP v15.zip` model has a disposition in the build guide's legacy v15 full-library port section (ported, alias, retired, or blocked)
- [ ] `DISTINCTCOUNT` totals reconcile for `referral_id`, `offer_id`, `ipa_id`, `referral_provider_id`
- [ ] No DAX references `bronze.*`, `silver.*`, or retired table names (`fact_placement`, `fact_referral_offer`, `dim_referral`, `dim_offer_status`, `dim_referral_gender`, `LocalDateTable_*`, `KPI Selector`, `ref_KPI`, `Draft Age Band Table`)
- [ ] Blocked fields in Section 5 are not used in published measures

---

*This contract is a living document. Update it whenever the Gold model schema or DAX measure library changes.*
