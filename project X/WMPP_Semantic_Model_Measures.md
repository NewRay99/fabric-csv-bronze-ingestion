# WMPP v01 Semantic Model — Measure Catalogue

**Source project:** `project X/report v01 extracted/semantic_model __/SM_WMPP.pbip`
**Source file:** `SM_WMPP.SemanticModel/definition/tables/_Measures.tmdl`

## Current inventory

| Item | Count |
|---|---:|
| Tables | 79 |
| Columns | 850 |
| Relationships | 48 |
| Measures | 95 |

This catalogue is generated from the committed v01 TMDL and replaces the older V13.1 documentation that referred to 90 or 117 measures. Measure names are preserved exactly as defined in the semantic model.

## `Closed_Date` derivation

The v01 model now exposes `Closed_Date` in both `fact_referral_offer` and `dim_referral`:

1. `fact_referral_offer[Closed_Date]` returns the date portion of `modified_date` only when `has_offer = TRUE()`; otherwise it returns DAX `BLANK()`.
2. `dim_referral[Closed_Date]` returns the latest related `fact_referral_offer[Closed_Date]` across matching offer rows. If no related row has `has_offer = TRUE()`, it remains `BLANK()`/null.

The v01 `fact_referral_offer` table does not expose a separate upstream `closed_date` field. Therefore the implementation uses the available `modified_date` as the closure timestamp proxy. If the source system later provides a canonical closure timestamp, replace the row-level expression and retain the same null-handling rule.

## Measures by display folder

### Uncategorised

| Measure | Source |
|---|---|
| `'(NEW)Total Offers Made'` | `_Measures.tmdl` |
| `'Accepted Offer to IPA Conversion %'` | `_Measures.tmdl` |
| `'Accepted Offers (Scoped Table)'` | `_Measures.tmdl` |
| `'Accepted Offers Base'` | `_Measures.tmdl` |
| `'Active Awaiting Offers (Engaged)'` | `_Measures.tmdl` |
| `'Active Awaiting Offers (No Engagement)'` | `_Measures.tmdl` |
| `'Active Referral Engagement Rate'` | `_Measures.tmdl` |
| `'Active Referrals Awaiting Offers'` | `_Measures.tmdl` |
| `'Active Referrals Under Offer'` | `_Measures.tmdl` |
| `'Active Referrals With Provider Engagement'` | `_Measures.tmdl` |
| `'Average Days in Draft'` | `_Measures.tmdl` |
| `'Avg Offers per Provider (Under Offer)'` | `_Measures.tmdl` |
| `'Avg Offers per Referral Under Offer'` | `_Measures.tmdl` |
| `'Closed Referral Previous Month'` | `_Measures.tmdl` |
| `'Closed Referrals (by Reason)'` | `_Measures.tmdl` |
| `'Closed Referrals MoM %'` | `_Measures.tmdl` |
| `'Critical Offers (30+ Days)'` | `_Measures.tmdl` |
| `'Dashboard Last Refreshed:'` | `_Measures.tmdl` |
| `'Directory Summary Count'` | `_Measures.tmdl` |
| `'Draft No Activity 7+ Days'` | `_Measures.tmdl` |
| `'Draft No Activity Since Creation (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Draft Offer Count (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Draft Offers Missing Dates'` | `_Measures.tmdl` |
| `'Draft Offers Updated After Creation'` | `_Measures.tmdl` |
| `'Draft Offers With Activity Since Creation'` | `_Measures.tmdl` |
| `'Draft With No Activity Since Creation (%)'` | `_Measures.tmdl` |
| `'Drafts No Activity 14+ Days (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Drafts With No Activity 14+ Days'` | `_Measures.tmdl` |
| `'Female Referrals'` | `_Measures.tmdl` |
| `'Fostering Chart Count'` | `_Measures.tmdl` |
| `'Fostering Providers'` | `_Measures.tmdl` |
| `'Framework Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Framework Providers'` | `_Measures.tmdl` |
| `'IPA Completed'` | `_Measures.tmdl` |
| `'IPA Created to Completion %'` | `_Measures.tmdl` |
| `'IPA Created'` | `_Measures.tmdl` |
| `'IPA Exists'` | `_Measures.tmdl` |
| `'IPAs Pending Completion'` | `_Measures.tmdl` |
| `'Is Awaiting IPA Creation'` | `_Measures.tmdl` |
| `'Is In Accepted KPI'` | `_Measures.tmdl` |
| `'Is IPA Completed'` | `_Measures.tmdl` |
| `'Is IPA Pending'` | `_Measures.tmdl` |
| `'Is Non Framework Provider'` | `_Measures.tmdl` |
| `'Latest Export per Offer'` | `_Measures.tmdl` |
| `'Latest Offer Status Count'` | `_Measures.tmdl` |
| `'Male Referrals'` | `_Measures.tmdl` |
| `'No. Providers Who Made Offers'` | `_Measures.tmdl` |
| `'NON Framework Providers'` | `_Measures.tmdl` |
| `'Offer Count'` | `_Measures.tmdl` |
| `'Offer IDs (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers At Risk (8–14 Days)'` | `_Measures.tmdl` |
| `'Offers Awaiting IPA Creation'` | `_Measures.tmdl` |
| `'Offers in Draft (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers Outside Timeframe (15–30 Days)'` | `_Measures.tmdl` |
| `'Offers per Provider (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Offers Still to Progress to IPA'` | `_Measures.tmdl` |
| `'Oldest Draft Age (Days)'` | `_Measures.tmdl` |
| `'Open Referral Previous Month'` | `_Measures.tmdl` |
| `'Open Referral'` | `_Measures.tmdl` |
| `'Open Referrals MoM %'` | `_Measures.tmdl` |
| `'Other Referrals'` | `_Measures.tmdl` |
| `'Overlap Referrals'` | `_Measures.tmdl` |
| `'Pending Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Pending Offers 0–7 Days'` | `_Measures.tmdl` |
| `'Pending Offers 15–30 Days'` | `_Measures.tmdl` |
| `'Pending Offers 30+ Days'` | `_Measures.tmdl` |
| `'Pending Offers 8–14 Days'` | `_Measures.tmdl` |
| `'Pending Offers by Age Bucket'` | `_Measures.tmdl` |
| `'Placement Type Totals (Visual)'` | `_Measures.tmdl` |
| `'Provider Homes Registered'` | `_Measures.tmdl` |
| `'Provider with Offers over 30+ Days'` | `_Measures.tmdl` |
| `'Providers - Fostering'` | `_Measures.tmdl` |
| `'Providers - Residential'` | `_Measures.tmdl` |
| `'Providers - Supported Accommodation'` | `_Measures.tmdl` |
| `'Providers Registered'` | `_Measures.tmdl` |
| `'Referrals Awaiting Offer'` | `_Measures.tmdl` |
| `'Referrals Cancelled/Closed'` | `_Measures.tmdl` |
| `'Referrals Currently Active'` | `_Measures.tmdl` |
| `'Referrals Not Yet Closed (Created in Period)'` | `_Measures.tmdl` |
| `'Referrals This FY'` | `_Measures.tmdl` |
| `'Referrals This Month'` | `_Measures.tmdl` |
| `'Referrals With Offers (Created in Period)'` | `_Measures.tmdl` |
| `'Referrals With Offers'` | `_Measures.tmdl` |
| `'Referrals With One or More Offers'` | `_Measures.tmdl` |
| `'Residential Homes'` | `_Measures.tmdl` |
| `'Spot Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Successful Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
| `'Successful Offers to IPA Completed %'` | `_Measures.tmdl` |
| `'Supported Accommodation Homes'` | `_Measures.tmdl` |
| `'Total Gendered Referrals'` | `_Measures.tmdl` |
| `'Total Offers Made (Active Referrals Under Offer)'` | `_Measures.tmdl` |
| `'Total Offers Made Historically'` | `_Measures.tmdl` |
| `'Total Referrals That Recieved Offers'` | `_Measures.tmdl` |
| `'Total Referrals'` | `_Measures.tmdl` |
| `'Unsuccessful Offers (Under Offer Referrals)'` | `_Measures.tmdl` |
