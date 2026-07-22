# West Midlands Placement Portal (WMPP)
## Dashboard Overview and KPI Logic Document

**Prepared by:** Hamant K Jakhu, Senior ICT Manager  
**Date:** 23 June 2026

*Final pack prepared to support shared understanding and consistent interpretation across the 14 Local Authorities.*

---

> This document has been written from the perspective of the dashboard creator and explains what each dashboard page shows, how each KPI is calculated, and how users should interpret the metrics when reviewing WMPP activity.

## 1. Executive Summary

The WMPP Power BI dashboard pack provides a consistent, transparent and operationally useful view of referral, offer, pending offer, draft offer and IPA activity.

The dashboard supports:

- Operational monitoring
- Strategic discussion
- Referral demand analysis
- Offer activity analysis
- IPA workflow tracking

A key principle is the use of distinct identifiers wherever possible:

- Referral ID
- Offer ID
- IPA ID

This reduces double counting and improves reporting accuracy.

### Dashboard Areas

| Dashboard Area | Main Question Answered | Primary Use |
|---------------|-----------------------|--------------|
| Referrals Overview | How much referral demand exists and what is the current referral status? | Referral demand monitoring and lifecycle overview |
| Offers Overview | How is the market responding to open referrals? | Offer activity and provider participation |
| Pending Offers in Progress | Which pending offers are ageing and where is intervention needed? | Operational backlog monitoring |
| Draft Offers | Are draft offers being progressed or left inactive? | Hidden backlog identification |
| IPA Overview | Are accepted offers progressing into created and completed IPAs? | Workflow conversion and placement formalisation |

---

## 2. Dashboard Methodology and Reporting Principles

| Principle | Explanation |
|-----------|-------------|
| Distinct counting | Uses DISTINCTCOUNT to avoid duplication |
| Latest offer record | Uses `fact_offer[Is_Latest_Record] = 1` |
| Flow-based referral reporting | Referrals created within the selected reporting period |
| Date relationship control | Uses USERELATIONSHIP between date and referral date |
| Operational ageing | Pending and draft offers use age bands |
| IPA completion evidence | Based on provider and local authority signatures |

---

## 3. KPI Dictionary – Summary

| KPI | Definition |
|------|-----------|
| Total Referrals | Unique referrals in selected period |
| Referrals Currently Open/Active | Referrals currently OPEN |
| Referrals Under Offer | Referrals currently UNDER_OFFER |
| Referrals Closed/Cancelled | Referrals with terminal status |
| Referrals With Offers | Open referrals with at least one offer |
| Referrals Awaiting First Offer | Open referrals with no offers |
| Total Offers Made | Distinct latest non-draft offers |
| Pending Offers | Distinct latest pending offers |
| Draft Offers | Distinct latest draft offers |
| Successful Offers | Distinct accepted offers |
| IPA Created | Distinct IPA records |
| IPA Completed | IPA records signed by both parties |
| IPAs Pending Completion | Created IPAs not yet completed |

---

## 4. Referrals Overview

### Flow (Period-Based View)

| KPI | Example Value | Description |
|------|------|-------------|
| Total Referrals | 161 | Total referrals created in period |
| Referrals Not Yet Closed | 119 | Referrals still active |
| Referrals Cancelled/Closed | 42 | Referrals now closed or cancelled |
| Total Referral Offer Rate | 68% | Referrals receiving at least one offer |

### Current Position (Snapshot View)

| KPI | Example Value | Description |
|------|------|-------------|
| Active Referrals | 72 | Currently progressing referrals |
| Active Referrals Awaiting Offers | 64 | Active referrals without offers |
| Active Referrals Under Offer | 8 | Active referrals with offers |
| Active Referral Engagement Rate | 94% | Referrals receiving engagement |

### Visual Interpretation

- Donut chart shows referral placement type distribution.
- Monthly activity chart shows referral status trends.
- Closure chart identifies reasons referrals failed to progress.
- Gender cards support demographic monitoring.

---

## 5. Offers Overview

This page shows how referral demand translates into market response.

| KPI | Example Value |
|------|-------------|
| Referrals Currently Open/Active | 106 |
| Referrals With One or More Offers | 55 |
| Referrals Awaiting First Offer | 51 |
| Referral Offer Rate | 52% |
| Total Offers Made | 427 |
| Avg Offers per Referral | 2.74 |
| Providers Who Made Offers | 86 |
| Avg Offers per Provider | 4.97 |
| Pending Offers | 377 |
| Successful Offers | 10 |
| Unsuccessful Offers | 40 |
| Offers in Draft Status | 162 |

### Visual Interpretation

- Provider ranking highlights active providers.
- Spot versus framework chart compares routes.
- Referral metrics and offer metrics remain separated to avoid confusion.

---

## 6. Pending Offers in Progress

| KPI | Value | Category |
|------|------|----------|
| Pending Offers | 377 | Total live pending |
| Pending Offers 0–7 Days | 60 | Healthy Pipeline |
| Pending Offers 8–14 Days | 66 | At Risk |
| Pending Offers 15–30 Days | 95 | Outside Timeframe |
| Pending Offers 30+ Days | 156 | Critical Pipeline |

### Interpretation

- Ageing reveals operational bottlenecks.
- Provider charts identify organisations with delayed pending offers.
- Total ageing bands should reconcile to overall pending offers.

---

## 7. Draft Offers

| KPI | Value |
|------|------|
| Offers in Draft Status | 166 |
| Draft No Activity Since Creation | 165 |
| Draft Offers With Activity Since Creation | 1 |
| Drafts No Activity for 14+ Days | 114 |
| Draft With No Activity Since Creation (%) | 99% |

### Interpretation

- Reveals hidden backlog.
- Highlights abandoned draft activity.
- Supports process improvement conversations.

---

## 8. IPA Overview

| KPI | Value |
|------|------|
| Successful Offers | 10 |
| IPA Created | 6 |
| IPA Completed | 1 |
| IPAs Pending Completion | 5 |
| Offers Awaiting IPA Creation | 4 |
| Accepted Offers to IPA Creation | 60% |
| Offers Still to Progress to IPA | 40% |
| IPAs Created to Completion | 17% |
| Successful Offers to Completed IPAs | 10% |

### Interpretation

The workflow funnel demonstrates progression from:

1. Successful Offer
2. IPA Created
3. IPA Pending Completion
4. IPA Completed

This identifies delays in both:

- Creating IPAs after offer acceptance
- Completing created IPAs

---

## 9. Technical Definitions

| Term | Meaning |
|------|---------|
| Referral-level measure | Counted using referral_id |
| Offer-level measure | Counted using offer_id |
| IPA-level measure | Counted using ipa_id |
| Is_Latest_Record = 1 | Latest version of offer only |
| USERELATIONSHIP | Activates date filtering relationship |
| Pending Offer Age | Used for ageing buckets |
| Draft No Activity | Last modified date equals creation date |
| IPA Completed | Both signatures present |
| IPAs Pending Completion | Created but not completed |

---

## 10. Overall Interpretation for Local Authorities

The dashboard should be viewed as an end-to-end workflow:

1. Referral Demand
2. Market Response
3. Pending Progression
4. Draft Inactivity
5. Placement Formalisation

This supports consistent interpretation and comparison across all 14 Local Authorities.

---

## 11. Suggested Use of This Pack

Use this document alongside the Power BI dashboard to:

- Understand KPI definitions
- Understand reporting logic
- Promote transparency
- Support consistent interpretation

Users should distinguish between:

- Referral-level metrics
- Offer-level metrics
- IPA-level metrics

---

## 12. Closing Note

This dashboard and accompanying logic pack provide both a user-friendly reporting overview and a technical reference to support consistent discussion and decision-making across the 14 Local Authorities.

---

*WMPP Dashboard Overview and KPI Logic Document – Final Pack*

> **v01 semantic-model note:** The current `SM_WMPP` project contains 95 measures. The exact measure inventory, display folders, table/relationship counts, and `Closed_Date` derivation are maintained in [`brand pack/WMPP_Semantic_Model_Measures.md`](brand%20pack/WMPP_Semantic_Model_Measures.md).
