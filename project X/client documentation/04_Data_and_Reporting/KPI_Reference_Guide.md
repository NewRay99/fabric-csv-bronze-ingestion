# KPI Reference Guide — Active Gold semantic model

This is the authoritative KPI reference for the notebook-created Gold model.
Do not create a new KPI against Bronze, Silver, an extracted v15 table, or a
retired Gold object.

## Naming convention

All active Gold table and column names are lower-case `snake_case`, matching
Silver. The IPA fact is `gold.fct_ipa`; the retired `gold.fact_placement`
object is removed by the Gold model deployment.

| Role | Active Gold table | Grain | Key |
| --- | --- | --- | --- |
| Current referral | `gold.fact_referral` | One current row per referral | `referral_id` |
| Historic referral state | `gold.fact_referral_snapshot` | One referral per reporting snapshot | `snapshot_date`, `referral_id` |
| Offer | `gold.fact_offer` | One offer | `offer_id` |
| IPA | `gold.fct_ipa` | One IPA | `ipa_id` |
| Provider response | `gold.fact_referral_provider` | One referral-provider assignment | `referral_provider_id` |
| Lifecycle evidence | `gold.fact_referral_lifecycle_event` | One derived event | `event_id` |

The active supporting tables are `gold.dim_date`, `gold.dim_provider`,
`gold.dim_provider_home`, `gold.dim_framework`,
`gold.dim_framework_category`, `gold.dim_placement_type`,
`gold.dim_referral_status`, `gold.dim_provider_submission_document`,
`gold.dim_person` (GLD-006), `gold.dim_offer_status` (GLD-008),
`gold.bridge_provider_framework`, and `gold.bridge_provider_sic_code`.

## Semantic-model build rules

Import only the active tables above. Create single-direction relationships from
`fact_referral[referral_id]` to the referral keys on `fact_offer`, `fct_ipa`,
and `fact_referral_provider`. Use inactive role-playing date relationships for
creation, required-placement, IPA-issued and closure dates. Keep
`fact_referral_snapshot` separate from current-state facts and use its
`snapshot_date` for historic trends. GLD-006–008 add two further
single-direction relationships: `dim_person` → `fact_referral[person_id]`
and `dim_offer_status` → `fact_offer[offer_status]`.

## Requirement mapping

| KPI area | Requirement IDs | Active evidence |
| --- | --- | --- |
| Referral status, target, responsiveness and snapshot trend | R24, R51–R53, R69 | Referral and snapshot facts |
| Offer submission, decision and acceptance | R28, R29, R36, R51 | Offer fact |
| Digitised IPA, current IPA and cost analysis | R35, R51, R62, R71 | `fct_ipa` and referral IPA fields |
| Provider assignment and decline analysis | R25, R28, R51, R54 | Referral-provider fact |

### Full KPI-to-requirement mapping (KPI-01–117)

The table below maps every as-is KPI from the V13.1 assessment ([§4.7 of the As-Is Assessment Report](../02_Assessment_and_Requirements/As_Is_Assessment_Report.md#47-kpi-calculation-inventory-as-is), ported from `Supplementary/02_01_As_Is_KPI.md`) to the **active Gold semantic model**, including the GLD-005–008 additions (`dim_person`, `dim_offer_status`, provider-home contact fields, `person_id` on `fact_referral`). Copy-ready DAX for each covered measure is in the [DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md); field-level evidence is in the [Field Coverage Audit](GOLD_DAX_FIELD_COVERAGE_AUDIT.md).

Status legend: **✅ Covered** — active Gold measure; **🔁 Alias** — served by an existing Gold measure under a different name (rename the visual, do not recreate); **⚠️ Proxy** — supported at a different grain or with estimated logic, caveat applies; **🗄 Retired** — report-construct helper, deliberately not recreated; **❌ Blocked** — required field/grain missing from Gold, do not point DAX at Bronze, Silver or legacy tables.

| KPI | Req IDs | As-is KPI (V13.1) | Active Gold object(s) | Gold measure / disposition | Status |
|---|---|---|---|---|---|
| KPI-01 | [R24,R51] | Total Referrals | `fact_referral` | Total Referrals | ✅ Covered |
| KPI-02 | [R24,R36] | Referrals With Offers | `fact_referral` + `fact_offer` | Referrals With an Offer | ✅ Covered |
| KPI-03 | [R24,R36] | Referrals Awaiting Offer | `fact_referral` + `fact_offer` | Referrals Awaiting Offer | ✅ Covered |
| KPI-04 | [R51] | Male Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` (GLD-006/007) | Male Referrals | ✅ Covered |
| KPI-05 | [R51] | Female Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Female Referrals | ✅ Covered |
| KPI-06 | [R51] | Other Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Other Gender Referrals | ✅ Covered |
| KPI-07 | [R51] | Total Gendered Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Total Gendered Referrals | ✅ Covered |
| KPI-08 | [R24] | Referrals Not Yet Closed (Created in Period) | `fact_referral` + `dim_date` | Referrals Not Yet Closed (Created in Period) | ✅ Covered |
| KPI-09 | [R24,R51] | Referrals With Offers (Created in Period) | `fact_referral` + `fact_offer` + `dim_date` | Referrals With Offers (Created in Period) | ✅ Covered |
| KPI-10 | [R51] | Total Referrals That Received Offers | `fact_referral` + `fact_offer` + `dim_date` | Offer Receipt Rate (Created in Period) | ✅ Covered |
| KPI-11 | [R25,R26] | No. Providers Who Made Offers | `fact_offer` | Providers Who Made Offers | ✅ Covered |
| KPI-12 | [R25-R29] | Total Offers Made Historically | `fact_offer` | Offers Submitted | 🔁 Alias |
| KPI-13 | [R51] | Avg Offers per Referral (Under Offer) | `fact_offer` + `fact_referral` | Average Offers per Referral Under Offer | ✅ Covered |
| KPI-14 | [R51] | Avg Offers per Provider (Under Offer) | `fact_offer` | Average Offers per Provider (Under Offer Referrals) | ✅ Covered |
| KPI-15 | [R28] | Successful Offers (Under Offer Referrals) | `fact_offer` + `dim_offer_status` | Successful Offers (Under Offer Referrals) | ✅ Covered |
| KPI-16 | [R28] | Unsuccessful Offers (Under Offer Referrals) | `fact_offer` + `dim_offer_status` | Unsuccessful Offers | ✅ Covered |
| KPI-17 | [R24] | Offers in Draft (Under Offer Referrals) | `fact_offer` + `dim_offer_status` | Offers in Draft | ✅ Covered |
| KPI-18 | [R24] | Pending Offers (Under Offer Referrals) | `fact_offer` + `dim_offer_status` | Pending Offers (Under Offer Referrals) | ✅ Covered |
| KPI-19 | [R24,R26] | Active Referrals With Provider Engagement | `fact_referral` + `fact_referral_provider` | Active Referrals With Provider Engagement | ✅ Covered |
| KPI-20 | [R24,R26] | Active Referral Engagement Rate | `fact_referral` + `fact_referral_provider` | Active Referral Engagement Rate | ✅ Covered |
| KPI-21 | [R24,R26] | Active Awaiting Offers (Engaged) | `fact_referral` + `fact_referral_provider` | Active Referrals With Provider Engagement | 🔁 Alias |
| KPI-22 | [R24,R26] | Active Awaiting Offers (No Engagement) | `fact_referral` + `fact_referral_provider` | Active Awaiting Offers Without Engagement | 🔁 Alias |
| KPI-23 | [R24,R52] | Referrals This Month | `fact_referral` + `dim_date` | Referrals Created This Month | 🔁 Alias |
| KPI-24 | [R52] | Referrals This FY | `fact_referral` + `dim_date` | Referrals Created This Financial Year | 🔁 Alias |
| KPI-25 | [R67,R68] | Total Offers Made | `fact_offer` | Offers Submitted | 🔁 Alias |
| KPI-26 | [R13] | Placement Type Totals (Visual) | `fact_referral` | Total Referrals + `fact_referral[placement_type_required]` visual dimension | 🔁 Alias |
| KPI-27 | [R18] | Spot Offers (Under Offer Referrals) | `fact_offer` | Spot Offers | ✅ Covered |
| KPI-28 | [R25-R29] | Offer Count | `fact_offer` | Offers Submitted | 🔁 Alias |
| KPI-29 | [R24] | Referrals Currently Active | `fact_referral` + `dim_referral_status` | Referrals Currently Active | ✅ Covered |
| KPI-30 | [R24,R36] | Active Referrals Under Offer | `fact_referral` + `fact_offer` | Referrals Under Offer | ✅ Covered |
| KPI-31 | [R13] | Referrals Cancelled/Closed | `fact_referral` + `dim_referral_status` | Closed or Cancelled Referrals | ✅ Covered |
| KPI-32 | [R24,R36] | Active Referrals Awaiting Offers | `fact_referral` + `fact_offer` | Referrals Awaiting Offer | 🔁 Alias |
| KPI-33 | [R24] | Referrals With One or More Offers | `fact_referral` + `fact_offer` | Referrals With an Offer | 🔁 Alias |
| KPI-34 | [R54] | Closed Referrals (by Reason) | `fact_referral` | Closed Referrals + `fact_referral[referral_closure_reason]` visual dimension | ✅ Covered |
| KPI-35 | [R25-R29] | Total Offers Made (Active Referrals Under Offer) | `fact_offer` | Offers on Referrals Under Offer | ✅ Covered |
| KPI-36 | [R25-R29] | Offer IDs (Under Offer Referrals) | — | Retired — internal CALCULATETABLE helper; Gold relationship graph + TREATAS make it unnecessary | 🗄 Retired |
| KPI-37 | [R26] | Offers per Provider (Under Offer Referrals) | `fact_offer` | Offers per Provider (Under Offer Referrals) | ✅ Covered |
| KPI-38 | [R67,R68] | Framework Offers (Under Offer Referrals) | `fact_offer` (framework flag) | Framework Offers (Under Offer Referrals) | ✅ Covered |
| KPI-39 | [R28,R35] | Accepted Offers (Scoped Table) | — | Retired — internal scoped-table helper (see KPI-36) | 🗄 Retired |
| KPI-40 | [R91,R93] | Provider Homes Registered | `dim_provider_home` | Provider Homes Registered | ✅ Covered |
| KPI-41 | [R91,R93] | Providers Registered | `dim_provider` | Providers Registered | ✅ Covered |
| KPI-42 | [R95] | Providers - Fostering | `dim_provider` + `dim_provider_home` | Providers - Fostering | ✅ Covered |
| KPI-43 | [R96] | Providers - Residential | `dim_provider` + `dim_provider_home` | Providers - Residential | ✅ Covered |
| KPI-44 | [R91] | Providers - Supported Accommodation | `dim_provider` + `dim_provider_home` | Providers - Supported Accommodation | ✅ Covered |
| KPI-45 | [R67] | Framework Providers | `dim_provider` + `bridge_provider_framework` + `dim_framework` | Framework Providers | ✅ Covered |
| KPI-46 | [R46] | NON Framework Providers | `dim_provider` + `bridge_provider_framework` | Non-Framework Providers | ✅ Covered |
| KPI-47 | [R46] | Is Non Framework Provider | `dim_provider` + `bridge_provider_framework` | Is Non Framework Provider (row helper) | ✅ Covered |
| KPI-48 | [R93] | Directory Summary Count | — | Retired — depended on report-view axis tables; rebuild with field parameters over `dim_provider_home[service_type]` if needed | 🗄 Retired |
| KPI-49 | [R96] | Residential Homes | `dim_provider_home` | Residential Homes | ✅ Covered |
| KPI-50 | [R91] | Supported Accommodation Homes | `dim_provider_home` | Supported Accommodation Homes | ✅ Covered |
| KPI-51 | [R95] | Fostering Providers | `dim_provider` + `dim_provider_home` | Providers - Fostering | 🔁 Alias |
| KPI-52 | [R95] | Fostering Chart Count | — | Retired — depended on `rpt_provider_fostering` report-view table (see KPI-48) | 🗄 Retired |
| KPI-53 | [R24] | Draft No Activity Since Creation | `fact_offer` | Draft Offers With No Activity Since Creation | ✅ Covered |
| KPI-54 | [R24] | Draft Offers With Activity Since Creation | `fact_offer` | Draft Offers With Activity Since Creation | ✅ Covered |
| KPI-55 | [R24] | Draft Offers Missing Dates | `fact_offer` | Draft Offers Missing Dates | ✅ Covered |
| KPI-56 | [R24] | Draft Offers Updated After Creation | `fact_offer` | Draft Offers With Activity Since Creation | 🔁 Alias |
| KPI-57 | [R24] | Draft No Activity 7+ Days | `fact_offer` | Draft Offers Stalled 7+ Days | ✅ Covered |
| KPI-58 | [R24] | Drafts No Activity 14+ Days | `fact_offer` | Draft Offers Stalled 14+ Days | ✅ Covered |
| KPI-59 | [R24] | Average Days in Draft | `fact_offer` | Average Days in Draft | ✅ Covered |
| KPI-60 | [R24] | Oldest Draft Age (Days) | `fact_offer` | Oldest Draft Age Days | ✅ Covered |
| KPI-61 | [R24] | Draft Offer Count | `fact_offer` | Offers in Draft | 🔁 Alias |
| KPI-62 | [R24] | Draft With No Activity Since Creation (%) | `fact_offer` | Draft Offers With No Activity % | ✅ Covered |
| KPI-63 | [R24] | Drafts With No Activity 14+ Days | `fact_offer` | Draft Offers Stalled 14+ Days | 🔁 Alias |
| KPI-64 | [R24] | Pending Offers by Age Bucket | — | Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands | 🗄 Retired |
| KPI-65 | [R24] | Pending Offers 15–30 Days | `fact_offer` | Pending Offers 15-29 Days | ✅ Covered |
| KPI-66 | [R24] | Pending Offers 30+ Days | `fact_offer` | Pending Offers 30+ Days | ✅ Covered |
| KPI-67 | [R24] | Pending Offers 0–7 Days | `fact_offer` | Pending Offers 0-7 Days | ✅ Covered |
| KPI-68 | [R24] | Pending Offers 8–14 Days | `fact_offer` | Pending Offers 8-14 Days | ✅ Covered |
| KPI-69 | [R24,R26] | Provider with Offers over 30+ Days | `fact_offer` + `fact_referral_provider` | Providers With Pending Offers 30+ Days | ✅ Covered |
| KPI-70 | [R24] | Offers At Risk (8–14 Days) | `fact_offer` | Pending Offers 8-14 Days | 🔁 Alias |
| KPI-71 | [R24] | Offers Outside Timeframe (15–30 Days) | `fact_offer` | Pending Offers 15-29 Days | 🔁 Alias |
| KPI-72 | [R24] | Critical Offers (30+ Days) | `fact_offer` | Pending Offers 30+ Days | 🔁 Alias |
| KPI-73 | [R35] | IPA Exists | `fct_ipa` | IPA Exists (row helper) | ✅ Covered |
| KPI-74 | [R28] | Is In Accepted KPI | — | Blocked — no IPA-grain signature status; use the referral-grain IPA funnel instead | ❌ Blocked |
| KPI-75 | [R28,R35] | Accepted Offers Base | — | Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it | 🗄 Retired |
| KPI-76 | [R35] | IPA Created | `fct_ipa` | IPAs Created | ✅ Covered |
| KPI-77 | [R35] | IPA Completed | `fact_offer` (`is_ipa_completed`) | IPA Completed — offer-grain, GLD-013 | ✅ Covered |
| KPI-78 | [R35] | IPAs Pending Completion | `fact_offer` (`is_ipa_pending`) | IPAs Pending Completion — offer-grain, GLD-013 (referral-grain proxy [Referrals With IPA Pending Signature] also available) | ✅ Covered |
| KPI-79 | [R35] | Offers Awaiting IPA Creation | `fact_offer` (`is_awaiting_ipa_creation`) | Offers Awaiting IPA Creation | ✅ Covered |
| KPI-80 | [R35] | Is IPA Pending | `fact_offer` (`is_ipa_pending`) | Is IPA Pending (row helper) — GLD-013 | ✅ Covered |
| KPI-81 | [R35] | Is Awaiting IPA Creation | `fact_offer` (`is_awaiting_ipa_creation`) | Is Awaiting IPA Creation (row helper) | ✅ Covered |
| KPI-82 | [R35] | Is IPA Completed | `fact_offer` (`is_ipa_completed`) | Is IPA Completed (row helper) — GLD-013 | ✅ Covered |
| KPI-83 | [R35] | Accepted Offer to IPA Conversion % | `fact_offer` (`is_awaiting_ipa_creation`) | Accepted Offer to IPA Conversion % | ✅ Covered |
| KPI-84 | [R35] | Offers Still to Progress to IPA | `fact_offer` (`is_awaiting_ipa_creation`) | Offers Still to Progress to IPA % | ✅ Covered |
| KPI-85 | [R35] | IPA Created to Completion % | `fact_offer` (`is_ipa_completed`, `is_awaiting_ipa_creation`) | IPA Created to Completion % — GLD-013 | ✅ Covered |
| KPI-86 | [R35] | Successful Offers to IPA Completed % | `fact_offer` (`is_ipa_completed`, `offer_status`) | Successful Offers to IPA Completed % — GLD-013 | ✅ Covered |
| KPI-87 | [R82] | Dashboard Last Refreshed | `fact_referral[gold_modelled_at]` | Gold Model Last Refreshed | 🔁 Alias |
| KPI-88 | [R53] | Latest Export per Offer | `fact_offer[source_export_date]` | Latest Offer Source Export | 🔁 Alias |
| KPI-89 | [R24] | Latest Offer Status Count | — | Retired — Gold `fact_offer` is already deduplicated to the latest state per offer | 🗄 Retired |
| KPI-90 | [R22] | Overlap Referrals | `fact_referral_provider` | Referrals With Multiple Provider Assignments | ✅ Covered |
| KPI-91 | [R18,R57] | Emergency Referrals | `fact_referral` (`required_start_date` vs created date) | Emergency Referrals | ✅ Covered |
| KPI-92 | [R18,R57] | Emergency Placement Rate | `fact_referral` | Emergency Placement Rate | ✅ Covered |
| KPI-93 | [R57] | Planned Referrals | `fact_referral` | Planned Referrals | ✅ Covered |
| KPI-94 | [R18,R57] | Emergency vs Planned Split | `fact_referral` | Visual split using [Emergency Referrals] and [Planned Referrals]; no separate measure | ✅ Covered |
| KPI-95 | [R22] | Out-of-Region Referrals | — | Blocked — `fact_referral[region]` is null until a reliable source supplies it | ❌ Blocked |
| KPI-96 | [R22] | Out-of-Region Placement Rate | — | Blocked — as KPI-95 | ❌ Blocked |
| KPI-97 | [R41] | Providers with QA Flags | `dim_provider` QA flag columns | Providers With QA Flags | ✅ Covered |
| KPI-98 | [R41] | QA Flag Type Breakdown | — | Blocked — no QA flag-type dimension to unpivot in Gold | ❌ Blocked |
| KPI-99 | [R41] | QA Flagged Providers by Home | `dim_provider_home` ⟕ `dim_provider` | QA Flagged Homes | ✅ Covered |
| KPI-100 | [R47] | Documents Expiring (30 Days) | `dim_provider_submission_document` | Documents Expiring Next 30 Days | ✅ Covered |
| KPI-101 | [R47,R48] | Documents Expired | `dim_provider_submission_document` | Documents Expired | ✅ Covered |
| KPI-102 | [R48] | Providers Blocked (Incomplete Docs) | — | Blocked — no expected-document set in Gold to test completeness against | ❌ Blocked |
| KPI-103 | [R48] | Document Compliance Rate | — | Blocked — as KPI-102 | ❌ Blocked |
| KPI-104 | [R49] | Provider Due Diligence Status | `dim_provider[provider_status]` | Providers Pending Onboarding / Providers Approved (provider_status split) | ✅ Covered |
| KPI-105 | [R54] | Decline Reasons (Referral Level) | — | Blocked — no decline-reason history in active Gold | ❌ Blocked |
| KPI-106 | [R58] | Framework Changes During Active Referrals | — | Blocked — no framework-change history in active Gold | ❌ Blocked |
| KPI-107 | [R62] | Total Weekly Fee Liability | `fct_ipa[estimated_weekly_cost]` | Estimated Active Weekly Cost — estimate, not signed-only actuals | ⚠️ Proxy |
| KPI-108 | [R62] | Payment Method Breakdown | — | Blocked — no payment method / payment facts in Gold | ❌ Blocked |
| KPI-109 | [R62] | IPA Payment Status | — | Blocked — no payment lifecycle facts in Gold | ❌ Blocked |
| KPI-110 | [R14] | Messages Sent | `fact_referral_lifecycle_event` | Provider Messages Sent — lifecycle-event proxy for volume only; no response-time or unread analysis | ⚠️ Proxy |
| KPI-111 | [R14] | Avg Message Response Time (Hours) | — | Blocked — no message response-time facts in Gold | ❌ Blocked |
| KPI-112 | [R14] | Priority Messages Unread | — | Blocked — no message-status facts in Gold | ❌ Blocked |
| KPI-113 | [R20] | Audit Events by Type | `fact_referral_lifecycle_event` | Referral Lifecycle Events — derived roll-up, not the source audit log | ⚠️ Proxy |
| KPI-114 | [R20,R35] | IPA Signature Completion Rate | `fact_referral` IPA fields | IPA Signature Completion Rate — referral-grain proxy | ⚠️ Proxy |
| KPI-115 | [R19] | Referral Updates per Day | — | Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure | ❌ Blocked |
| KPI-116 | [R59] | Provider Onboarding Pipeline | `dim_provider[provider_status]` | Providers Pending Onboarding | ✅ Covered |
| KPI-117 | [R59] | Bulk Onboarding Success Rate | `dim_provider[provider_status]` | Provider Onboarding Success Rate | ✅ Covered |

#### Disposition summary

| Status | Count | Meaning |
|---|---:|---|
| ✅ Covered | 74 | Active Gold measure computes the KPI |
| 🔁 Alias | 19 | Existing Gold measure under a different name; rename the visual |
| ⚠️ Proxy | 4 | Supported at a different grain or with estimated logic |
| 🗄 Retired | 7 | v15 report-construct helper, not recreated |
| ❌ Blocked | 13 | Missing Gold field/grain; add the data first |
| **Total** | **117** | KPI-01–117 |

> **Gender measures (KPI-04–07)** were blocked in earlier revisions and are now covered: `gold.dim_person[gender_clean]` joins to `fact_referral[person_id]` (GLD-006/GLD-007). **Offer-status measures** filter through `gold.dim_offer_status` (GLD-008) rather than hard-coded status strings. **IPA-signature measures (KPI-77–78, 80–82, 85–86)** moved from blocked/proxy to covered in GLD-013: `gold.fact_offer` now carries `is_ipa_completed`, `is_ipa_pending` and `is_awaiting_ipa_creation` at offer grain. KPI-74 (Is In Accepted KPI) remains blocked.

## DAX implementation

Copy-ready DAX, the v15 reconciliation, required relationships, and the
measures that cannot yet be recreated are in
[Gold Semantic Model DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md).

## Maintained catalogue and lineage

`configuration/Dashboard Legend.xlsx` is the maintained Excel catalogue of
the Gold v02 DAX measure names, legacy mappings, requirement IDs, Gold source
objects and publication status. It currently contains **109 active measures**:
**108 Ready** measures and **one Gold lifecycle-event proxy**. It also records
ten roadmap gaps that must not be published until their fields exist in Gold.
The [DAX Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md) and the
[Field Coverage Audit](GOLD_DAX_FIELD_COVERAGE_AUDIT.md) (rev 4) carry the wider
supported set of **195 measures**: the 109 catalogue measures plus the 82
legacy v15 ports (76 from rev 2 plus 6 offer-grain IPA-signature measures from
GLD-013) and the 4 gender referral measures enabled by GLD-006/GLD-007.

The workbook is deliberately a DAX catalogue, not the system-of-record for
technical lineage. Use [KPI Lineage](KPI_Lineage.md) to trace each KPI family
from functional requirement through the source extract, Bronze, Silver,
Gold object and DAX measure. The original assessment documents remain useful
as historic evidence, but are not the current implementation record:

- [KPI Enhancement Requirements](../02_Assessment_and_Requirements/KPI_Enhancement_Requirements.md)
- [Gap Analysis Report](../02_Assessment_and_Requirements/Gap_Analysis_Report.md)

### Latest Gold-only calculations

These measures are included in the active DAX catalogue and are repeated here
because they close the most recent reporting requests. Both use active Gold
fields only.

```DAX
Average Estimated Weekly Cost — Confirmed Referrals =
AVERAGEX (
    FILTER (
        'fact_referral',
        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
            && NOT ISBLANK ( 'fact_referral'[estimated_weekly_cost] )
    ),
    'fact_referral'[estimated_weekly_cost]
)

Provider Messages Sent =
CALCULATE (
    [Referral Lifecycle Events],
    'fact_referral_lifecycle_event'[event_type] = "ProviderMessageSent"
)
```

`Average Estimated Weekly Cost — Confirmed Referrals` uses a referral with an
issued IPA as confirmation; it is not an actual-payment measure. `Provider
Messages Sent` is a Gold lifecycle-event proxy for message volume only. It
does not provide response-time, unread-message or message-content analysis.

## Source limitations

`estimated_weekly_cost` is an estimate, not an invoice or actual payment.
`region`, `complexity_band`, actual placement dates/cost, duration and end
reason remain null until a reliable source supplies them. A measure should not
turn those nulls into invented business values.
