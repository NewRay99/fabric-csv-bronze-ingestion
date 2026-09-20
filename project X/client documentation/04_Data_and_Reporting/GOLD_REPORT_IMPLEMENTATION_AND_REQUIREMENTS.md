# Gold report implementation and requirements

Implementation date: 15 September 2026.

## Current client-site status — 20 September 2026

The current client-site baseline is now
`reports/current/MWPP Repo 20092026.zip` (`SM_WMPP_v16`), not the v15 project
described below. The v16 model differs materially: it has 117 tables, 274
measures, two DirectQuery tables, four bidirectional business relationships,
an active current-referral-to-snapshot fact relationship, no RLS roles and 73
broken report field-reference occurrences across nine missing fields.

Use the [v16 reconciliation and required model updates](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE%20WIP.md)
as the current action list. In particular, implement snapshot-based historical
state KPIs, repair report bindings, restore the single-direction star and add
the documented RLS/security data before acceptance. The remainder of this
document records the 15 September v15 migration and should not be read as a
current v16 deployment sign-off.

A repository implementation candidate is now available at
`reports/current/SM WMPP v16 updated`. It completes those structural changes
and is generated repeatably by `tools/reconcile_semantic_model_v16.py` from the
immutable ZIP baseline. The supporting Gold contracts are in the current
`00_setup_cfg.py`, `04_gold_model.py` and `05_gold_dimensions.py`. Static
validation passes, but Fabric refresh, Power BI Desktop open/save, DAX result
reconciliation, populated security mappings and identity-based RLS UAT remain
deployment prerequisites.

## Delivered model

`reports/client-deliverables/SM WMPP v15/SM_WMPP.pbip` now contains 281 measures across 67 tables (including automatic date tables and local report metadata). `reports/current/_Measures.tmdl` contains 283 measures, retaining its extra source-only measure. All 195 concrete WIP definitions are present. This is the business report, separate from Mission Control.

**Deployment prerequisite:** publish and execute the changed `04_gold_model.py` against the intended Lakehouse before refreshing Power BI. It adds four real fields to `gold.fact_ipa`: `signed_by_provider`, `signed_by_local_authority`, `is_ipa_completed`, `is_ipa_pending`. Run `05_gold_dimensions.py` if the latest Gold dimensions are not already deployed. The report retains the existing Lakehouse SQL endpoint and uses Import mode for a consistent snapshot.

## Source contract

- Business SQL queries select only `Schema="gold"` objects. `fact_ipa` is the semantic name for physical `gold.fact_ipa`.
- `dim_person` imports Gold `gender_clean`; `dim_offer_status` imports the Gold status dimension. Silver person staging, category/person joins and unused legacy directory views were removed. Unsupported contact/inspection placeholders were not copied into the Gold model.
- `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage` are embedded documentation metadata derived from the versioned Markdown. They do not access Bronze. Their assessment status is historical evidence, not a deployment sign-off.
- Existing calculated date/age helpers use Gold timestamps and age fields. No calculated column refers to retired `offer_date`, `last_modified_date`, `created_datetime` or `fact_ipa[offer_id]` fields.
- 31 report JSON files were rebound to available Gold fields, including referral, snapshot, date, gender and IPA visuals. Visuals using closure reasons now use `fact_referral[referral_closure_reason]`; this is not a provider-decline history measure.

## Relationship and filter behaviour

The active business graph is single direction and has no duplicate filter paths. Referral filters flow to offers, IPAs, assignments and lifecycle events. Person filters flow to referrals. Provider filters flow directly to offers, assignments and framework/SIC bridges. Home filters flow to offers and submission documents.

The provider-to-home relationship is deliberately inactive: making it active alongside both provider-to-offer and home-to-offer produces two provider-to-offer paths. Provider Homes Registered and QA Flagged Homes explicitly transfer the selected provider IDs. A home slicer does not automatically cascade from a provider slicer. Test the intended directory navigation before enabling alternative relationships.

`dim_date` is marked as the date table. Referral creation and snapshot date links are active; the snapshot fact has no relationship to current referrals. Required-placement, referral-closure and IPA-issued dates are inactive roles. IPAs Issued This Month disables the referral-creation date path before activating the IPA-issued role. Current measures compared by creation month describe current state of a creation cohort; historic state must use snapshot measures.

Natural keys on the one side must be unique. Static graph checks cannot prove that the deployed rows satisfy this; run the refresh acceptance checks below.

## Requirement-driven corrections

| Requirement/KPI group | Implemented behaviour |
| --- | --- |
| KPI-01–10 / R24,R51 | Gold referral grain and Gold person attributes; separate received-offer count and rate; referral creation date filters the current cohort. |
| KPI-12,25,28,35 / R25–29,R67–68 | Non-draft submission totals are distinct from all offer records; under-offer measures require active UNDER_OFFER referrals. |
| KPI-19–22,29–33 / R24,R26,R36 | Active, awaiting and under-offer counts use the correct referral cohort. Engagement transfers the eligible assignment referral IDs. |
| KPI-40–52,97,99 / R41,R91–96 | Provider/home counts read Gold; QA counts provider flags and home-or-provider flags; fostering includes framework registrations without a home. |
| KPI-53–63 / R24 | Draft activity requires draft status and valid timestamps. Same-day edits are activity. Original age cards and inactivity/stall measures are explicitly separate. |
| KPI-65–72 / R24,R26 | Pending includes PENDING and OFFER_MADE; age is Gold offer_age_days (since submission, as of Gold build), with a separate unknown/future-date count. |
| KPI-73–86,114 / R28,R35 | IPA-level signatures and counts now use fact_ipa. Closed unsigned IPAs do not count as pending. Offer/IPA ratios follow the assessment and retain their distinct grains. |
| KPI-87–88 / R53,R82 | Refresh labels show persisted Gold build/export timestamps; opening the report no longer falsely changes the displayed refresh time. |
| KPI-91–94 / R18,R57 | Emergency is the Gold same-day flag on OPEN/UNDER_OFFER statuses, independent of spot purchasing. Planned requires both dates and different dates. |

## Deliberate differences and boundary rules

- The original KPI-65 and KPI-71 use inclusive 15–30 days. Those measures are retained with that exact boundary. The WIP 15–29 measure remains for a mutually exclusive dashboard. Day 30 belongs to both original 15–30 and original 30+; do not add those two original cards to reconcile the total.
- All pending bands use `offer_age_days`, not time since last edit. Blank/future submission dates are excluded from the four bands and counted separately. Refresh Gold to advance the clock; report queries do not mix TODAY with stored ages.
- Draft No Activity 7+ Days and Drafts No Activity 14+ Days follow the original assessment’s age predicates (all drafts beyond the age). Draft Offers Stalled 7+/14+ Days measure time since activity. The names in the historic document are imperfect; tooltips should explain the distinction.
- The original IPA conversion and successful-offer completion ratios divide an IPA count by an offer count. Multiple IPAs per offer can produce a value over 100%; the complement can be negative. They are retained to match the assessment. Use Accepted Offers Linked to IPA % for a bounded offer conversion KPI. Do not treat either as interchangeable with the IPA completion rate.
- IPA Completed includes all fully signed IPAs, including closed ones, as requested. IPAs Pending Completion includes only open unsigned IPAs. Therefore completed plus pending need not equal all IPAs: closed unsigned records form a separate state.
- QA Flagged Homes uses a home flag OR its parent provider flag. A framework flag alone is a different scope and is not silently treated as a home flag.
- Gold is_open includes the approved operational response-window/provider-engagement rules. Emergency/planned KPIs follow the assessment’s OPEN/UNDER_OFFER status predicate plus the Gold same-day flag. A status-open referral need not satisfy operational is_open.
- Planned follows the assessment’s different-date rule, including negative date intervals. Data-quality review must distinguish invalid dates from valid planned placements; missing dates are excluded from both emergency and planned.

## Still blocked or partial

The 117-row mapping below records each KPI disposition. Covered means a definition is implemented against available Gold fields, **not** that UAT has passed or that every linked requirement is fulfilled. The 80 assessed R-IDs remain linked in the [baseline traceability audit](GOLD_MEASURE_REQUIREMENT_COVERAGE_AUDIT.md); no unlisted R-ID is assumed satisfied.

- R22 / KPI-95–96: no reliable referral/placement region. Overlap Referrals is a cohort diagnostic, not evidence of out-of-region placement.
- R41 / KPI-98: no QA flag-type breakdown. R47/R48 / KPI-102–103: expiry dates support expiry KPIs, but not reminder delivery, an expected-document set or blocking decisions.
- R54/R58 / KPI-105–106: no complete referral-provider decline reason or framework-change history.
- R62 / KPI-108–109: no payment method, invoice or payment-status data. Weekly cost is an estimate, not verified signed fee liability.
- R14 / KPI-111–112: offer/reason-based assignment-to-response evidence is now implemented, but provider-authored message classification, unread-state semantics, business-calendar SLA and approved threshold remain open.
- R19 / KPI-115: no durable referral update history; R20 audit events are derived events, not a complete source audit trail.
- R59 / KPI-117: approval-state proportion is a proxy for onboarding and cannot certify bulk-job success.
- R12/R55/R76/R78/R79: deny-by-default security tables and a dynamic role now exist in the repository candidate, but authoritative mappings, aggregate-disclosure policy, Service role assignment and identity-based acceptance evidence remain open. R31 resolved-request visibility, notification delivery, accessibility, disaster recovery and performance/SLA requirements also need separate acceptance evidence.

## Validation and rollout

1. Deploy the updated Gold notebook; run the pipeline/Gold rebuild using the intended export date and job_run_id. Verify the new IPA signature columns in the Lakehouse SQL endpoint.
2. Check unique keys for referral_id, offer_id, ipa_id, provider_id, provider_home_id and person_id, plus offer_status in its dimension. Check orphan referral/provider/home keys and that date ranges fit dim_date.
3. Close the old Desktop project without overwriting these externally edited files, then reopen SM_WMPP.pbip and refresh from Gold. The saved model now expects the new IPA columns.
4. Reconcile a known export: male/female/other/unknown; active/awaiting/under-offer; draft timestamp changes within one day; pending day 7/8/14/15/29/30, blank/future dates; multiple IPAs per offer; closed unsigned IPAs; provider-only and home-only QA.
5. Exercise referral, provider, home, gender and date slicers. Verify creation-cohort comparisons versus snapshot trends and IPA-issued date selection. Check original versus non-overlapping age cards separately.
6. Sign off each supported KPI with expected results. Record unsupported data/security/workflow requirements as open rather than interpreting blank or proxy values as completion.

**Validation result: 73 tests passed; Microsoft TMDL parser accepted 67 tables, 281 measures and 64 relationships.** Automatic relationship detection/import is disabled to preserve the reviewed graph. The unchanged extracted cache was removed after verifying it matched the original ZIP; the ZIP remains the rollback copy.

Repository validation checks every table/column/measure visual binding, Gold-only SQL navigation, single-direction unambiguous relationships and IPA signature predicates. Microsoft TMDL deserialization succeeds. Live DAX execution was not run because its earlier confirmation was declined; a file parse is not a successful Fabric refresh or runtime calculation test.

## Complete KPI disposition

| KPI | Requirement IDs | Original KPI | Gold object(s) | Implemented measure / remaining gap | Disposition |
| --- | --- | --- | --- | --- | --- |
| KPI-01 | [R24,R51] | Total Referrals | `fact_referral` | Total Referrals | ✅ Covered |
| KPI-02 | [R24,R36] | Referrals With Offers | `fact_referral` + `fact_offer` | Referrals With an Offer | ✅ Covered |
| KPI-03 | [R24,R36] | Referrals Awaiting Offer | `fact_referral` + `fact_offer` | Referrals Awaiting Offer | ✅ Covered |
| KPI-04 | [R51] | Male Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` (GLD-006/007) | Male Referrals | ✅ Covered |
| KPI-05 | [R51] | Female Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Female Referrals | ✅ Covered |
| KPI-06 | [R51] | Other Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Other Gender Referrals | ✅ Covered |
| KPI-07 | [R51] | Total Gendered Referrals | `fact_referral[person_id]` → `dim_person[gender_clean]` | Total Gendered Referrals | ✅ Covered |
| KPI-08 | [R24] | Referrals Not Yet Closed (Created in Period) | `fact_referral` + `dim_date` | Referrals Not Yet Closed (Created in Period) | ✅ Covered |
| KPI-09 | [R24,R51] | Referrals With Offers (Created in Period) | `fact_referral` + `fact_offer` + `dim_date` | Referrals With Offers (Created in Period) | ✅ Covered |
| KPI-10 | [R51] | Total Referrals That Received Offers | fact_referral | Total Referrals That Received Offers | Covered |
| KPI-11 | [R25,R26] | No. Providers Who Made Offers | `fact_offer` | Providers Who Made Offers | ✅ Covered |
| KPI-12 | [R25-R29] | Total Offers Made Historically | fact_offer | Non-Draft Offers | Alias |
| KPI-13 | [R51] | Avg Offers per Referral (Under Offer) | `fact_offer` + `fact_referral` | Average Offers per Referral Under Offer | ✅ Covered |
| KPI-14 | [R51] | Avg Offers per Provider (Under Offer) | `fact_offer` | Average Offers per Provider (Under Offer Referrals) | ✅ Covered |
| KPI-15 | [R28] | Successful Offers on Referrals Under Offer | `fact_offer` + `dim_offer_status` | Successful Offers on Referrals Under Offer | ✅ Covered |
| KPI-16 | [R28] | Unsuccessful Offers (Under Offer Referrals) | fact_offer + fact_referral | Unsuccessful Offers on Referrals Under Offer | Covered |
| KPI-17 | [R24] | Offers in Draft (Under Offer Referrals) | fact_offer + fact_referral | Draft Offers on Referrals Under Offer | Covered |
| KPI-18 | [R24] | Pending Offers (Under Offer Referrals) | `fact_offer` + `dim_offer_status` | Pending Offers (Under Offer Referrals) | ✅ Covered |
| KPI-19 | [R24,R26] | Active Referrals With Provider Engagement | `fact_referral` + `fact_referral_provider` | Active Referrals With Provider Engagement | ✅ Covered |
| KPI-20 | [R24,R26] | Active Referral Engagement Rate | `fact_referral` + `fact_referral_provider` | Active Referral Engagement Rate | ✅ Covered |
| KPI-21 | [R24,R26] | Active Awaiting Offers (Engaged) | fact_referral + fact_referral_provider | Active Awaiting Offers With Engagement | Alias |
| KPI-22 | [R24,R26] | Active Awaiting Offers (No Engagement) | `fact_referral` + `fact_referral_provider` | Active Awaiting Offers Without Engagement | 🔁 Alias |
| KPI-23 | [R24,R52] | Referrals This Month | `fact_referral` + `dim_date` | Referrals Created This Month | 🔁 Alias |
| KPI-24 | [R52] | Referrals This FY | `fact_referral` + `dim_date` | Referrals Created This Financial Year | 🔁 Alias |
| KPI-25 | [R67,R68] | Total Offers Made | fact_offer | Non-Draft Offers | Alias |
| KPI-26 | [R13] | Placement Type Totals (Visual) | `fact_referral` | Total Referrals + `fact_referral[placement_type_required]` visual dimension | 🔁 Alias |
| KPI-27 | [R18] | Spot Offers (Under Offer Referrals) | fact_offer + dim_provider_home + fact_referral | Spot Offers on Referrals Under Offer; spot is not emergency | Covered |
| KPI-28 | [R25-R29] | Offer Count | `fact_offer` | Offers Submitted | 🔁 Alias |
| KPI-29 | [R24] | Referrals Currently Active | `fact_referral` + `dim_referral_status` | Referrals Currently Active | ✅ Covered |
| KPI-30 | [R24,R36] | Active Referrals Under Offer | `fact_referral` + `fact_offer` | Referrals Under Offer | ✅ Covered |
| KPI-31 | [R13] | Referrals Cancelled/Closed | `fact_referral` + `dim_referral_status` | Closed or Cancelled Referrals | ✅ Covered |
| KPI-32 | [R24,R36] | Active Referrals Awaiting Offers | `fact_referral` + `fact_offer` | Referrals Awaiting Offer | 🔁 Alias |
| KPI-33 | [R24] | Referrals With One or More Offers | `fact_referral` + `fact_offer` | Referrals With an Offer | 🔁 Alias |
| KPI-34 | [R54] | Closed Referrals (by Reason) | fact_referral | Closed Referrals (by Reason) with referral_closure_reason; does not supply provider decline history | Partial |
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
| KPI-57 | [R24] | Draft No Activity 7+ Days | fact_offer[offer_age_days] | Draft No Activity 7+ Days; original definition counts draft age, not time since last activity | Covered |
| KPI-58 | [R24] | Drafts No Activity 14+ Days | fact_offer[offer_age_days] | Drafts No Activity 14+ Days; original draft-age definition | Covered |
| KPI-59 | [R24] | Average Days in Draft | `fact_offer` | Average Days in Draft | ✅ Covered |
| KPI-60 | [R24] | Oldest Draft Age (Days) | `fact_offer` | Oldest Draft Age Days | ✅ Covered |
| KPI-61 | [R24] | Draft Offer Count | `fact_offer` | Offers in Draft | 🔁 Alias |
| KPI-62 | [R24] | Draft With No Activity Since Creation (%) | `fact_offer` | Draft Offers With No Activity % | ✅ Covered |
| KPI-63 | [R24] | Drafts With No Activity 14+ Days | fact_offer[offer_age_days] | Drafts With No Activity 14+ Days; count, not percentage | Alias |
| KPI-64 | [R24] | Pending Offers by Age Bucket | — | Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands | 🗄 Retired |
| KPI-65 | [R24] | Pending Offers 15–30 Days | fact_offer[offer_age_days] | Pending Offers 15–30 Days; original inclusive range. Use Pending Offers 15-29 Days for non-overlapping bands | Covered |
| KPI-66 | [R24] | Pending Offers 30+ Days | `fact_offer` | Pending Offers 30+ Days | ✅ Covered |
| KPI-67 | [R24] | Pending Offers 0–7 Days | `fact_offer` | Pending Offers 0-7 Days | ✅ Covered |
| KPI-68 | [R24] | Pending Offers 8–14 Days | `fact_offer` | Pending Offers 8-14 Days | ✅ Covered |
| KPI-69 | [R24,R26] | Provider with Offers over 30+ Days | `fact_offer` + `fact_referral_provider` | Providers With Pending Offers 30+ Days | ✅ Covered |
| KPI-70 | [R24] | Offers At Risk (8–14 Days) | `fact_offer` | Pending Offers 8-14 Days | 🔁 Alias |
| KPI-71 | [R24] | Offers Outside Timeframe (15–30 Days) | fact_offer[offer_age_days] | Offers Outside Timeframe (15–30 Days); inclusive original range | Alias |
| KPI-72 | [R24] | Critical Offers (30+ Days) | `fact_offer` | Pending Offers 30+ Days | 🔁 Alias |
| KPI-73 | [R35] | IPA Exists | `fact_ipa` | IPA Exists (row helper) | ✅ Covered |
| KPI-74 | [R28] | Is In Accepted KPI | fact_offer[offer_status] | Is In Accepted KPI; accepted-status row helper | Covered |
| KPI-75 | [R28,R35] | Accepted Offers Base | — | Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it | 🗄 Retired |
| KPI-76 | [R35] | IPA Created | fact_ipa[ipa_id] | IPA Created / IPAs Created; individual IPA count | Covered |
| KPI-77 | [R35] | IPA Completed | fact_ipa[is_ipa_completed] | IPA Completed; both signatures present | Covered |
| KPI-78 | [R35] | IPAs Pending Completion | fact_ipa[is_ipa_pending] | IPAs Pending Completion; unsigned and not closed | Covered |
| KPI-79 | [R35] | Offers Awaiting IPA Creation | `fact_offer` (`is_awaiting_ipa_creation`) | Offers Awaiting IPA Creation | ✅ Covered |
| KPI-80 | [R35] | Is IPA Pending | fact_ipa[is_ipa_pending] | Is IPA Pending; IPA rows, with explicit offer-context transfer | Covered |
| KPI-81 | [R35] | Is Awaiting IPA Creation | `fact_offer` (`is_awaiting_ipa_creation`) | Is Awaiting IPA Creation (row helper) | ✅ Covered |
| KPI-82 | [R35] | Is IPA Completed | fact_ipa[is_ipa_completed] | Is IPA Completed; IPA rows, with explicit offer-context transfer | Covered |
| KPI-83 | [R35] | Accepted Offer to IPA Conversion % | fact_ipa + fact_offer | Accepted Offer to IPA Conversion %; original IPA-count / accepted-offer count. Accepted Offers Linked to IPA % is the distinct-offer alternative | Covered |
| KPI-84 | [R35] | Offers Still to Progress to IPA | fact_ipa + fact_offer | Offers Still to Progress to IPA %; complement of KPI-83 per assessment; Offers Awaiting IPA Creation supplies the actual count | Covered |
| KPI-85 | [R35] | IPA Created to Completion % | fact_ipa | IPA Created to Completion %; completed IPAs / all IPAs | Covered |
| KPI-86 | [R35] | Successful Offers to IPA Completed % | fact_ipa + fact_offer | Successful Offers to IPA Completed %; completed IPAs / accepted offers | Covered |
| KPI-87 | [R82] | Dashboard Last Refreshed | `fact_referral[gold_modelled_at]` | Gold Model Last Refreshed | 🔁 Alias |
| KPI-88 | [R53] | Latest Export per Offer | `fact_offer[source_export_date]` | Latest Offer Source Export | 🔁 Alias |
| KPI-89 | [R24] | Latest Offer Status Count | — | Retired — Gold `fact_offer` is already deduplicated to the latest state per offer | 🗄 Retired |
| KPI-90 | [R22] | Overlap Referrals | fact_referral | Overlap Referrals; diagnostic intersection of active awaiting/under-offer cohorts. Does not satisfy R22 geography | Diagnostic |
| KPI-91 | [R18,R57] | Emergency Referrals | fact_referral | Emergency Referrals; OPEN/UNDER_OFFER status and Gold same-day flag | Covered |
| KPI-92 | [R18,R57] | Emergency Placement Rate | `fact_referral` | Emergency Placement Rate | ✅ Covered |
| KPI-93 | [R57] | Planned Referrals | fact_referral | Planned Referrals; OPEN/UNDER_OFFER status, both dates present and not same-day | Covered |
| KPI-94 | [R18,R57] | Emergency vs Planned Split | `fact_referral` | Visual split using [Emergency Referrals] and [Planned Referrals]; no separate measure | ✅ Covered |
| KPI-95 | [R22] | Out-of-Region Referrals | — | Blocked — `fact_referral[region]` is null until a reliable source supplies it | ❌ Blocked |
| KPI-96 | [R22] | Out-of-Region Placement Rate | — | Blocked — as KPI-95 | ❌ Blocked |
| KPI-97 | [R41] | Providers with QA Flags | `dim_provider` QA flag columns | Providers With QA Flags | ✅ Covered |
| KPI-98 | [R41] | QA Flag Type Breakdown | — | Blocked — no QA flag-type dimension to unpivot in Gold | ❌ Blocked |
| KPI-99 | [R41] | QA Flagged Providers by Home | dim_provider + dim_provider_home | QA Flagged Homes; home flag OR parent-provider flag | Covered |
| KPI-100 | [R47] | Documents Expiring (30 Days) | `dim_provider_submission_document` | Documents Expiring Next 30 Days | ✅ Covered |
| KPI-101 | [R47,R48] | Documents Expired | `dim_provider_submission_document` | Documents Expired | ✅ Covered |
| KPI-102 | [R48] | Providers Blocked (Incomplete Docs) | — | Blocked — no expected-document set in Gold to test completeness against | ❌ Blocked |
| KPI-103 | [R48] | Document Compliance Rate | — | Blocked — as KPI-102 | ❌ Blocked |
| KPI-104 | [R49] | Provider Due Diligence Status | `dim_provider[provider_status]` | Providers Pending Onboarding / Providers Approved (provider_status split) | ✅ Covered |
| KPI-105 | [R54] | Decline Reasons (Referral Level) | — | Blocked — no decline-reason history in active Gold | ❌ Blocked |
| KPI-106 | [R58] | Framework Changes During Active Referrals | — | Blocked — no framework-change history in active Gold | ❌ Blocked |
| KPI-107 | [R62] | Total Weekly Fee Liability | `fact_ipa[estimated_weekly_cost]` | Estimated Active Weekly Cost — estimate, not signed-only actuals | ⚠️ Proxy |
| KPI-108 | [R62] | Payment Method Breakdown | — | Blocked — no payment method / payment facts in Gold | ❌ Blocked |
| KPI-109 | [R62] | IPA Payment Status | — | Blocked — no payment lifecycle facts in Gold | ❌ Blocked |
| KPI-110 | [R14] | Messages Sent | `fact_referral_lifecycle_event` | Provider Messages Sent — lifecycle-event proxy for volume only; no response-time or unread analysis | ⚠️ Proxy |
| KPI-111 | [R14] | Avg Message Response Time (Hours) | — | Blocked — no message response-time facts in Gold | ❌ Blocked |
| KPI-112 | [R14] | Priority Messages Unread | — | Blocked — no message-status facts in Gold | ❌ Blocked |
| KPI-113 | [R20] | Audit Events by Type | `fact_referral_lifecycle_event` | Referral Lifecycle Events — derived roll-up, not the source audit log | ⚠️ Proxy |
| KPI-114 | [R20,R35] | IPA Signature Completion Rate | fact_ipa signature fields | IPAs Signed by Provider; IPAs Signed by Local Authority; IPA Completed; IPA Signature Completion Rate | Covered |
| KPI-115 | [R19] | Referral Updates per Day | — | Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure | ❌ Blocked |
| KPI-116 | [R59] | Provider Onboarding Pipeline | `dim_provider[provider_status]` | Providers Pending Onboarding | ✅ Covered |
| KPI-117 | [R59] | Bulk Onboarding Success Rate | dim_provider[provider_status] | Provider Onboarding Success Rate; current approval-state proportion, not bulk-operation outcome | Proxy |
