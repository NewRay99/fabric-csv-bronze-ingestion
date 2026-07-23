# Measures Comparison Checklist — PBI Report vs Functional Specification

**Project:** WMPP (West Midlands Placement Portal)  
**Report:** WMPP PILOT DASHBOARD V13 (v0.1 project)
**Semantic model:** `SM_WMPP` — 95 measures in the current TMDL
**Current catalogue:** [`brand pack/WMPP_Semantic_Model_Measures.md`](brand%20pack/WMPP_Semantic_Model_Measures.md)
**v00 → v01 changelog:** [`client documentation/07_Semantic_Model_Changelog_v00_to_v01.md`](client%20documentation/07_Semantic_Model_Changelog_v00_to_v01.md)
**Date:** 10 July 2026  
**Prepared by:** Hermes Agent  

---

## Overview

This checklist is retained as a comparison of the legacy functional-specification mapping. The v01 semantic model is the current source of truth and contains **95 measures**, not the older 90-measure inventory. Sections 1–9 classify the 90 names retained from v00; the five v01 additions are recorded separately in WMPP-DE-CHG-001 and remain unclassified pending stakeholder validation. Use the generated catalogue linked above for the exact current names and display folders.

Each measure is checked for:
- ✅ **Implemented** — exists in the PBI model AND maps to a functional requirement
- ⚠️ **Partial** — exists in PBI but functional requirement is broader than what's measured
- ❌ **Missing** — functional requirement exists but no corresponding PBI measure found
- 📋 **Extra** — PBI measure exists but no functional requirement found (may be operational)

---

## 1. Referral Volume KPIs (10 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 1 | Total Referrals | ✅ "Unique referrals in selected period" | R24: Dashboard with referral status overview | ✅ Implemented | Core KPI — flow-based reporting |
| 2 | Referrals With Offers | ✅ "Open referrals with at least one offer" | R24, R51: Placement reporting | ✅ Implemented | |
| 3 | Referrals Awaiting Offer | ✅ "Open referrals with no offers" | R24: Referral status overview | ✅ Implemented | |
| 4 | Male Referrals | ✅ Gender cards support demographic monitoring | R51: Robust data model | ✅ Implemented | |
| 5 | Female Referrals | ✅ Gender cards support demographic monitoring | R51: Robust data model | ✅ Implemented | |
| 6 | Other Referrals | ✅ Gender cards support demographic monitoring | R51: Robust data model | ✅ Implemented | |
| 7 | Total Gendered Referrals | ✅ Aggregation of gender measures | R51: Robust data model | ✅ Implemented | |
| 8 | Referrals Not Yet Closed (Created in Period) | ✅ "Referrals still active" | R24, R57: Planned vs emergency | ✅ Implemented | |
| 9 | Referrals With Offers (Created in Period) | ✅ Period-based view | R51: Placement records | ✅ Implemented | |
| 10 | Total Referrals That Recieved Offers | ✅ Referral offer rate | R51: Value analysis | ✅ Implemented | Typo in measure name ("Recieved") |

**Gap:** ❌ No measure for **Emergency vs Planned referral split** — required by R18 and R57. The PBI model has `is_spot` but no KPI distinguishing emergency referrals.

---

## 2. Provider Activity KPIs (12 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 11 | No. Providers Who Made Offers | ✅ "Providers Who Made Offers: 86" | R25-R28: Provider activity | ✅ Implemented | |
| 12 | Total Offers Made Historically | ✅ "Total Offers Made: 427" | R25-R29: Provider offers | ✅ Implemented | |
| 13 | Avg Offers per Referral Under Offer | ✅ "Avg Offers per Referral: 2.74" | R51: Market intelligence | ✅ Implemented | |
| 14 | Avg Offers per Provider (Under Offer) | ✅ "Avg Offers per Provider: 4.97" | R51: Value analysis | ✅ Implemented | |
| 15 | Successful Offers (Under Offer Referrals) | ✅ "Successful Offers: 10" | R28: Accept placements | ✅ Implemented | |
| 16 | Unsuccessful Offers (Under Offer Referrals) | ✅ "Unsuccessful Offers: 40" | R28: Reject placements | ✅ Implemented | |
| 17 | Offers in Draft (Under Offer Referrals) | ✅ "Offers in Draft Status: 162" | — | 📋 Extra | Operational KPI, not in functional spec |
| 18 | Pending Offers (Under Offer Referrals) | ✅ "Pending Offers: 377" | R24: Referral status | ✅ Implemented | |
| 19 | Active Referrals With Provider Engagement | ✅ "Active Referral Engagement Rate: 94%" | R24, R26: Provider engagement | ✅ Implemented | |
| 20 | Active Referral Engagement Rate | ✅ "Active Referral Engagement Rate" | R24: Referral status overview | ✅ Implemented | |
| 21 | Active Awaiting Offers (Engaged) | ✅ Snapshot view | R24, R26 | ✅ Implemented | |
| 22 | Active Awaiting Offers (No Engagement) | ✅ Snapshot view | R24, R26 | ✅ Implemented | |

---

## 3. Timebased KPIs (2 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 23 | Referrals This Month | ✅ Monthly activity chart | R24, R52: Accurate reporting | ✅ Implemented | |
| 24 | Referrals This FY | ✅ Time-based reporting | R52: Customisable reporting | ✅ Implemented | |

---

## 4. Spot vs Framework (3 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 25 | (NEW)Total Offers Made | ✅ Spot vs framework chart | R67, R68: Framework management | ✅ Implemented | |
| 26 | Placement Type Totals (Visual) | ✅ Donut chart placement type | R13: Filter by placement type | ✅ Implemented | |
| 27 | Spot Offers (Under Offer Referrals) | ✅ Spot vs framework | R18: Emergency placements | ⚠️ Partial | Spot ≠ emergency; R18 needs emergency-specific KPI |

**Gap:** ❌ No measure specifically for **emergency placement tracking** (R18 requires "same-day placement, distinct identification, separate reporting and finance categorisation"). Spot ≠ emergency.

---

## 5. Referral Offers (12 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 28 | Offer Count | ✅ Offer-level counting | R25-R29 | ✅ Implemented | |
| 29 | Referrals Currently Active | ✅ "Active Referrals: 72" | R24: Referral status | ✅ Implemented | |
| 30 | Active Referrals Under Offer | ✅ "Active Referrals Under Offer: 8" | R24, R36 | ✅ Implemented | |
| 31 | Referrals Cancelled/Closed | ✅ "Referrals Cancelled/Closed: 42" | R13: Placement status | ✅ Implemented | |
| 32 | Active Referrals Awaiting Offers | ✅ "Active Referrals Awaiting Offers: 64" | R24, R36 | ✅ Implemented | |
| 33 | Referrals With One or More Offers | ✅ "Referrals With One or More Offers: 55" | R24 | ✅ Implemented | |
| 34 | Closed Referrals (by Reason) | ✅ Closure chart identifies reasons | R54: Capture decline reasons | ✅ Implemented | |
| 35 | Total Offers Made (Active Referrals Under Offer) | ✅ "Total Offers Made: 427" | R25-R29 | ✅ Implemented | |
| 36 | Offer IDs (Under Offer Referrals) | ✅ Distinct offer ID counting | R25-R29 | ✅ Implemented | |
| 37 | Offers per Provider (Under Offer Referrals) | ✅ Provider ranking | R26: Prioritise by match | ✅ Implemented | |
| 38 | Framework Offers (Under Offer Referrals) | ✅ Spot vs framework chart | R67, R68 | ✅ Implemented | |
| 39 | Accepted Offers (Scoped Table) | ✅ Accepted offers in funnel | R28, R35: IPA | ✅ Implemented | |

---

## 6. Provider Registry (13 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 40 | Provider Homes Registered | — | R91, R93: Provider directory | ✅ Implemented | |
| 41 | Providers Registered | — | R91, R93: Provider directory | ✅ Implemented | |
| 42 | Providers - Fostering | — | R95: Fostering Framework | ✅ Implemented | |
| 43 | Providers - Residential | — | R96: Residential Framework 2.0 | ✅ Implemented | |
| 44 | Providers - Supported Accommodation | — | R91: Provider services | ✅ Implemented | |
| 45 | Framework Providers | — | R67: Framework management | ✅ Implemented | |
| 46 | NON Framework Providers | — | R46: Non-framework QA | ✅ Implemented | |
| 47 | Is Non Framework Provider | — | R46 | ✅ Implemented | |
| 48 | Directory Summary Count | — | R93: Provider directory | ✅ Implemented | |
| 49 | Residential Homes | — | R96 | ✅ Implemented | |
| 50 | Supported Accommodation Homes | — | R91 | ✅ Implemented | |
| 51 | Fostering Providers | — | R95 | ✅ Implemented | |
| 52 | Fostering Chart Count | — | R95 | ✅ Implemented | |

**Gap:** ❌ No measure for **QA flag tracking** — R41 requires "advisory notices and flags against providers" but no KPI shows flagged provider counts or flag types (safeguarding, information notices).

---

## 7. Draft/Pending Offers (11 + 9 = 20 measures in PBI)

### Draft Offers (11 measures)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 53 | Draft No Activity Since Creation (Under Offer Referrals) | ✅ "Draft No Activity Since Creation: 165" | R24: Dashboard task management | ✅ Implemented | |
| 54 | Draft Offers With Activity Since Creation | ✅ "Draft Offers With Activity: 1" | R24 | ✅ Implemented | |
| 55 | Draft Offers Missing Dates | — | — | 📋 Extra | Data quality KPI |
| 56 | Draft Offers Updated After Creation | — | — | 📋 Extra | |
| 57 | Draft No Activity 7+ Days | — | R24 | ✅ Implemented | |
| 58 | Drafts No Activity 14+ Days (Under Offer Referrals) | ✅ "Drafts No Activity 14+ Days: 114" | R24 | ✅ Implemented | |
| 59 | Average Days in Draft | ✅ "Average Days in Draft" | R24 | ✅ Implemented | |
| 60 | Oldest Draft Age (Days) | — | R24 | ✅ Implemented | |
| 61 | Draft Offer Count (Under Offer Referrals) | ✅ "Offers in Draft Status: 166" | R24 | ✅ Implemented | |
| 62 | Draft With No Activity Since Creation (%) | ✅ "99%" | R24 | ✅ Implemented | |
| 63 | Drafts With No Activity 14+ Days | ✅ "114" | R24 | ✅ Implemented | Duplicate of #58 |

### Pending Offers (9 measures)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 64 | Pending Offers by Age Bucket | ✅ Ageing reveals bottlenecks | R24: Task management | ✅ Implemented | |
| 65 | Pending Offers 15–30 Days | ✅ "Outside Timeframe: 95" | R24 | ✅ Implemented | |
| 66 | Pending Offers 30+ Days | ✅ "Critical Pipeline: 156" | R24 | ✅ Implemented | |
| 67 | Pending Offers 0–7 Days | ✅ "Healthy Pipeline: 60" | R24 | ✅ Implemented | |
| 68 | Pending Offers 8–14 Days | ✅ "At Risk: 66" | R24 | ✅ Implemented | |
| 69 | Provider with Offers over 30+ Days | ✅ Provider charts | R24, R26 | ✅ Implemented | |
| 70 | Offers At Risk (8–14 Days) | ✅ "At Risk" | R24 | ✅ Implemented | Duplicate of #68 |
| 71 | Offers Outside Timeframe (15–30 Days) | ✅ "Outside Timeframe" | R24 | ✅ Implemented | Duplicate of #65 |
| 72 | Critical Offers (30+ Days) | ✅ "Critical Pipeline" | R24 | ✅ Implemented | Duplicate of #66 |

---

## 8. IPA Measures (14 measures in PBI)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 73 | IPA Exists | — | R35: Digitised IPA | ✅ Implemented | |
| 74 | Is In Accepted KPI | — | R28: Accept placements | ✅ Implemented | |
| 75 | Accepted Offers Base | ✅ "Successful Offers: 10" | R28, R35 | ✅ Implemented | |
| 76 | IPA Created | ✅ "IPA Created: 6" | R35: Digitised IPA | ✅ Implemented | |
| 77 | IPA Completed | ✅ "IPA Completed: 1" (both signatures) | R35: Electronic signatures | ✅ Implemented | |
| 78 | IPAs Pending Completion | ✅ "IPAs Pending Completion: 5" | R35 | ✅ Implemented | |
| 79 | Offers Awaiting IPA Creation | ✅ "Offers Awaiting IPA Creation: 4" | R35 | ✅ Implemented | |
| 80 | Is IPA Pending | — | R35 | ✅ Implemented | |
| 81 | Is Awaiting IPA Creation | — | R35 | ✅ Implemented | |
| 82 | Is IPA Completed | — | R35 | ✅ Implemented | |
| 83 | Accepted Offer to IPA Conversion % | ✅ "Accepted Offers to IPA Creation: 60%" | R35 | ✅ Implemented | |
| 84 | Offers Still to Progress to IPA | ✅ "Offers Still to Progress to IPA: 40%" | R35 | ✅ Implemented | |
| 85 | IPA Created to Completion % | ✅ "IPAs Created to Completion: 17%" | R35 | ✅ Implemented | |
| 86 | Successful Offers to IPA Completed % | ✅ "Successful Offers to Completed IPAs: 10%" | R35 | ✅ Implemented | |

---

## 9. Other Measures (4 remaining)

| # | PBI Measure | KPI Logic Document | Functional Requirement | Status | Notes |
|---|-------------|--------------------|-----------------------|--------|-------|
| 87 | Dashboard Last Refreshed: | — | R82: Performance reporting | ✅ Implemented | Operational |
| 88 | Latest Export per Offer | — | R53: Data exportable | ✅ Implemented | |
| 89 | Latest Offer Status Count | — | R24: Referral status | ✅ Implemented | |
| 90 | Overlap Referrals | — | R22: Out-of-region placements | ⚠️ Partial | May support R22 but unclear if it tracks external placements |

---

## Outstanding / Missing Features (Functional Requirements Not in PBI)

These are functional requirements from the spec that have **no corresponding measure** in the Power BI model:

### High Priority Gaps

| Req ID | Requirement | Gap Description | Suggested Action |
|--------|------------|-----------------|-----------------|
| **R18** | Emergency placements — distinct identification, separate reporting | No KPI distinguishes emergency from planned/spot. `is_spot` ≠ emergency. | Add `Emergency Referrals` and `Emergency Placement Rate` measures. Add `is_emergency` flag to dim_referral. |
| **R22** | Out-of-region placements tagged and finance-informed | `Overlap Referrals` measure exists but unclear if it tracks external (non-WM) placements specifically. | Add `Out-of-Region Referrals` measure with geographic tagging. |
| **R41** | QA advisory notices and flags against providers | No KPI shows flagged provider counts or flag types (safeguarding, info notices). | Add `Providers with QA Flags`, `QA Flag Type Breakdown` measures. Use provider.qa_flag_* fields. |
| **R47** | Document expiry monitoring and reminders | No KPI for documents nearing expiry or expired. | Add `Documents Expiring (30 days)`, `Documents Expired` measures. Use s3_file_metadata.expiry_date. |
| **R48** | Providers with incomplete documentation excluded from referrals | No measure showing providers blocked due to incomplete docs. | Add `Providers Blocked (Incomplete Docs)` measure. |
| **R54** | Capture reasons for declined placements | `Closed Referrals (by Reason)` exists but only covers offer decline codes, not full referral-level decline reasons. | Expand to include `referral_provider_decline_reason` data. |
| **R58** | Commissioners alerted when framework changes during referral activity | No KPI for framework change tracking during active referrals. | Add `Framework Changes During Active Referrals` measure. |
| **R62** | Finance officer — view completed placements, current IPAs, extract payment info | IPA funnel exists but no finance-specific views (weekly fees, payment methods, invoice details). | Add `Total Weekly Fee Liability`, `Payment Method Breakdown`, `IPA Payment Status` measures. |

### Medium Priority Gaps

| Req ID | Requirement | Gap Description | Suggested Action |
|--------|------------|-----------------|-----------------|
| **R14** | In-system messaging between placement officers and providers | Message table exists (`fact_provider_message`) but no KPI for message volume, response times, or priority handling. | Add `Messages Sent`, `Avg Response Time`, `Priority Messages Unread` measures. |
| **R20** | Full audit tracking across placement activities, IPA, signatures, approvals, negotiations | No audit trail KPIs. | Add `Audit Events by Type`, `IPA Signature Completion Rate` measures. |
| **R31** | Resolved requests automatically removed from provider views | No measure tracking resolved-but-not-hidden requests. | Add `Resolved Requests Visible` measure for data quality. |
| **R49** | QA officer — easily identify provider due diligence status | No KPI for due diligence status. | Add `Providers by Due Diligence Status` measure. |
| **R55** | RBAC for commissioners — access regional data, market-wide trends | This is a security requirement, not a measure gap. Verify RLS is configured. | Check if RLS is implemented in the semantic model. |
| **R57** | Emergency and planned placements separately reportable | Same as R18. | See R18 action. |

### Low Priority Gaps

| Req ID | Requirement | Gap Description | Suggested Action |
|--------|------------|-----------------|-----------------|
| **R13** | Filter by specialisms, placement type, placement status | Filters exist in the PBI report but the functional spec mentions "nested filters" which may need testing. | Verify nested filtering works in the report visuals. |
| **R19** | Placement officers can update referrals; auto-notify providers | No KPI for referral update frequency or notification delivery. | Add `Referral Updates per Day`, `Provider Notification Rate` measures. |
| **R59** | Bulk provider onboarding | No KPI for onboarding pipeline. | Add `Providers in Onboarding Pipeline`, `Bulk Onboarding Success Rate` measures. |

---

## Summary Statistics

| Metric | Count |
|--------|-------|
| Legacy measures classified in Sections 1–9 | 90 |
| v01 additions pending classification | 5 |
| Current v01 semantic-model measures | 95 |
| ✅ Implemented (measure maps to requirement) | 85 |
| ⚠️ Partial (measure exists but gap in requirement coverage) | 2 |
| 📋 Extra (PBI measure, no functional requirement) | 3 |
| 🔁 Exact-DAX duplicate groups (non-exclusive) | 5 groups: 11 measures, 6 redundant definitions |
| ❌ Missing (requirement exists, no PBI measure) | 8 high + 6 medium + 3 low = 17 |

The first three status rows reconcile the 90 legacy catalogue entries (85 + 2 + 3 = 90). Duplicate grouping is a separate, non-exclusive source comparison: some measures marked implemented or extra share the same archived v01 DAX.

### Coverage by Functional Area

| Functional Area | Requirements | Measures Covering | Coverage |
|----------------|-------------|-------------------|----------|
| Placement Officer (R11-R24) | 14 | 11 | 79% |
| Provider (R25-R36) | 12 | 10 | 83% |
| QA Officer (R38-R49) | 8 | 2 | 25% ← LOWEST |
| Commissioner (R51-R59) | 9 | 5 | 56% |
| Finance Officer (R62) | 1 | 0 | 0% ← MISSING |
| General (R67-R70) | 4 | 3 | 75% |
| Digitised IPA (R71-R72) | 2 | 2 | 100% |

---

## Recommended Next Steps

1. **Immediate (sprint 1):**
   - Add emergency placement KPIs (R18, R57) — highest business impact
   - Add QA flag tracking measures (R41) — safeguarding critical
   - Add finance measures (R62) — payment tracking required

2. **Short-term (sprint 2):**
   - Add document expiry monitoring (R47, R48)
   - Add messaging KPIs (R14)
   - Add framework change tracking (R58)

3. **Medium-term (sprint 3):**
   - Add audit trail KPIs (R20)
   - Add provider onboarding metrics (R59)
   - Expand decline reason analytics (R54)

4. **Data quality:**
   - Deduplicate pending offer age bucket measures (3 duplicate pairs)
   - Fix typo in "Recieved" measure name
   - Verify `Overlap Referrals` covers out-of-region placements (R22)

---

*Legacy classification generated from: v00 Power BI semantic-model TMDL (90 `EXTERNALMEASURE` declarations), functional spec.md (87 requirements), am_functional_specification.csv (81 requirements), and WMPP KPI Logic Document. The archived v01 model contains 95 measures; see WMPP-DE-CHG-001 for the controlled delta.*
