# Gold measures and requirements coverage audit

Audit date: 15 September 2026. **Historical baseline: the model has since been migrated. See [implemented changes and remaining requirements](GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md) for current status.** Scope: the extracted **SM WMPP v15 - bu 15092026.zip** project, not Mission Control.

## Pre-migration result

**All 195 concrete WIP-guide measures are already present in the extracted model. Zero measures need adding to satisfy that inventory. This does not mean all business requirements are implemented.**

| Check | Result |
| --- | --- |
| Extracted v15 model | 87 tables; 270 measures |
| WIP guide | 195 distinct concrete measures; all present |
| Generic `<Base>` examples | 5 templates; excluded from the measure inventory |
| `reports/current/_Measures.tmdl` | 271 measures; all 195 guide names also present |
| Formula comparison | 172 match after ignoring comments, whitespace, identifier case and optional table quotes; 23 differ |
| KPI traceability | All KPI-01 through KPI-117 accounted for below |
| Requirements traceability | All 80 R-ID rows actually listed in Assessment section 0 accounted for below |
| Required relationship checks | 4 active; 8 missing; 1 inactive |
| Live metadata | Open SM_WMPP instance reports 87 tables, 270 measures, 87 partitions, 82 relationships and 0 roles |
| Runtime calculations | Not verified: the DAX query confirmation was declined; no further DAX queries were run |

No measure definitions were replaced simply to match a WIP document. The tables below distinguish name presence, formula differences, source/relationship prerequisites and original business acceptance. Existing report layout helpers and aliases are not counted as new missing measures.

## Evidence and limits

- [WIP DAX guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE%20WIP.md): concrete formula inventory and intended Gold relationships.
- [KPI Reference Guide](KPI_Reference_Guide.md): current KPI dispositions and aliases.
- [As-Is Assessment](../02_Assessment_and_Requirements/As_Is_Assessment_Report.md): section 0 lists 80 requirements; section 4.7 lists 117 historical KPIs.
- Saved model: `reports/client-deliverables/SM WMPP v15/SM_WMPP.SemanticModel/definition`; measures in `tables/_Measures.tmdl`; relationships in `relationships.tmdl`.
- Microsoft TMDL deserialization succeeds. Direct table/column references in all 270 saved measure expressions resolve against the saved model catalog. This is not a DAX execution or business-results certification.
- Desktop metadata matches the inventory. No live rows or KPI results were used to sign off correctness. The live instance path was not independently verified from its window title alone.
- The assessment omits R10, R23, R30, R37, R40, R42-R44, R50, R56, R60-R61 and R63-R66. This audit cannot claim coverage of unspecified requirements merely because the numbering reaches R96.

## Findings that prevent full requirement sign-off

1. **Missing filter relationships.** Eight expected links are missing and the provider-to-home link is inactive. The shared date table is not actively related to referral creation or snapshot dates. Time comparisons and cross-fact cohorts can return plausible but unfiltered totals. Add relationships only after checking key uniqueness, orphan keys and existing ambiguous paths; do not enable every old path.
2. **Draft and QA formulas need correction.** Draft Offers With Activity Since Creation omits the draft-status condition. Both QA measures filter the framework bridge instead of the documented provider/home flag, without a valid reverse filtering route. The exact review expressions appear below.
3. **Cohorts and grains differ.** Pending bands use different age clocks; IPA counts, offer counts and referral signature proxies are not interchangeable. Several aliases map a count to a percentage or an active subset to a broader population.
4. **Gold-only sourcing is incomplete.** `dim_person` derives from the query named `bronze referral_person`, whose actual partition reads `silver.referral_person`. It creates `[Gender Clean]`, whereas the WIP expects Gold `[gender_clean]`. `fact_referral_category` and `dim_referral_gender` also read Silver. A Gold-looking semantic table name alone is not proof of Gold lineage.
5. **Source gaps remain.** The reference explicitly blocks 13 KPIs and labels 4 as proxies. Payment lifecycle, expected-document completeness/blocking, reliable referral region, framework-change history, message response/unread state and durable update/audit evidence cannot be supplied by inventing measures.
6. **Security and non-measure acceptance remain separate.** The inspected model has zero roles. R12/R55/R76/R78/R79 require security/access evidence; application features, reminders, notifications, accessibility, disaster recovery and SLAs require their own acceptance tests.

The physical IPA source is `gold.fact_ipa`, imported under semantic table name `fact_ipa`. Use `fact_ipa` in this report’s DAX. The two spellings in the documents refer to different layers; do not rename the model table to match the physical source.

Saved `PBI_ResultType = Exception` annotations exist on dim_provider, bridge_provider_framework, dim_person, fact_referral_person and the Silver-backed query. They are refresh-investigation signals, not proof of a current runtime failure; confirm refresh status separately.

## Required relationships

The two date roles below support current and snapshot reporting separately. Review the active-date design and avoid paths between the two fact grains.

| Intended dimension/key | Target | Saved state |
| --- | --- | --- |
| `fact_referral.referral_id` | `fact_offer.referral_id` | Missing |
| `fact_referral.referral_id` | `fact_ipa.referral_id` | Missing |
| `fact_referral.referral_id` | `fact_referral_provider.referral_id` | Missing |
| `dim_provider.provider_id` | `fact_offer.provider_id` | Present, active |
| `dim_provider.provider_id` | `fact_referral_provider.provider_id` | Missing |
| `dim_provider_home.provider_home_id` | `fact_offer.home_id` | Missing |
| `dim_provider.provider_id` | `dim_provider_home.provider_id` | Present, inactive |
| `dim_provider.provider_id` | `bridge_provider_framework.provider_id` | Present, active |
| `dim_provider_home.provider_home_id` | `dim_provider_submission_document.home_id` | Missing |
| `dim_person.person_id` | `fact_referral.person_id` | Present, active |
| `dim_offer_status.offer_status` | `fact_offer.offer_status` | Present, active |
| `dim_date.date` | `fact_referral.referral_created_date` | Missing |
| `dim_date.date` | `fact_referral_snapshot.snapshot_date` | Missing |

## Formula differences requiring disposition

The initial raw comparison found 36 differences. Thirteen were only comments, optional quotes or identifier case; the 23 meaningful syntax differences are listed here. A difference can be a valid adaptation rather than an error.

| Measure | Finding / acceptance action |
| --- | --- |
| Draft Offers Stalled 7+ Days | Blank handling added with COALESCE; expected equivalent for the draft filter. Not a missing measure. |
| Female Referrals | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| Male Referrals | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| Other Gender Referrals | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| Total Gendered Referrals | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| Active Awaiting Offers With Engagement | Model omits is_open. Confirm the Gold is_awaiting_offer flag already guarantees an active referral before treating this as equivalent. |
| Active Awaiting Offers Without Engagement | Model omits is_open from the awaiting cohort. Same active-cohort check as the engaged companion. |
| Planned Referrals | Model requires required date after creation; guide uses non-emergency with dates present. Negative date intervals differ. Define the invalid-date treatment and emergency/planned denominator. |
| Draft Offers With Activity Since Creation | Model filters two FALSE flags but omits offer_status = draft. Non-draft offers can satisfy both FALSE flags. Restore the draft-status predicate before using KPI-54/56. |
| Pending Offers 0-7 Days | Model delegates to the legacy en-dash name; its expression matches the Gold days_since_offer_activity band. Alias, not a missing measure. |
| Pending Offers 8-14 Days | Model delegates to the legacy en-dash name; its expression matches the Gold days_since_offer_activity band. Alias, not a missing measure. |
| Pending Offers 15-29 Days | Model computes age at query time from reviewed/submitted date; guide uses the Gold activity-age field. Use one clock and one age origin across all bands; assess null/future dates. |
| Pending Offers 30+ Days | Model computes age at query time from reviewed/submitted date; 0-7/8-14 use stored Gold age. Mixed clocks can cause overlaps/gaps between bands. |
| Providers With Pending Offers 30+ Days | Uses query-time age instead of Gold days_since_offer_activity. Align with the pending-offer cohort chosen for KPI-65-69. |
| Providers With QA Flags | Model filters bridge_provider_framework[qa_flag] while counting dim_provider. With the saved one-way relationship, the bridge cannot filter the provider dimension back. Use the provider QA flag for the documented KPI, or explicitly transfer framework-provider IDs if framework QA is intended. |
| QA Flagged Homes | Model filters bridge_provider_framework[qa_flag] while counting dim_provider_home; there is no active filtering route to homes. Use home QA flags for the guide definition; a provider-to-home inherited flag requires an explicit agreed rule. |
| IPA Created to Completion % | Model uses [IPA Created] with alternate result 0; the helper counts accepted offers with IPA. Guide uses [Accepted Offers With IPA]. Both are offer-grain, but confirm accepted-status cohorts and blank-versus-zero reporting. |
| Successful Offers to IPA Completed % | Same numerator/denominator; model returns zero on an empty denominator and guide returns blank. Confirm empty-population display policy. |
| Referrals With IPA Pending Signature | Model counts referral IDs from pending offer flags; guide counts issued referrals without both signatures. A referral with multiple offers can differ. Pending-rate denominator is referral-grain; reconcile cohorts. |
| IPA Exists | Model adds accepted-status gating, preventing non-accepted offers with a FALSE awaiting flag from appearing as IPA-present. Retain safeguard; validate behaviour for blank/total-row selections. |
| Is Awaiting IPA Creation | Model explicitly coalesces blank selection to FALSE. Row-helper output is consistent with the guide; test multi-select and total-row use. |
| Is IPA Completed | Model explicitly coalesces blank selection to FALSE. Row-helper output is consistent with the guide; test multi-select and total-row use. |
| Is IPA Pending | Model explicitly coalesces blank selection to FALSE. Row-helper output is consistent with the guide; test multi-select and total-row use. |

### Exact candidate corrections for the three clear filter defects

These are review expressions for the documented KPI meanings, not applied changes to the loaded report. Framework-level QA needs a different, explicitly agreed scope.

```DAX
Draft Offers With Activity Since Creation =
CALCULATE (
    [Offers Submitted],
    FILTER (
        'fact_offer',
        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
            && 'fact_offer'[is_draft_no_activity] = FALSE ()
            && 'fact_offer'[is_draft_missing_dates] = FALSE ()
    )
)

Providers With QA Flags =
CALCULATE ( [Providers Registered], 'dim_provider'[qa_flag] = TRUE () )

QA Flagged Homes =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[qa_flag] = TRUE () )
```

## Complete WIP measure inventory

Presence is confirmed by name across every table in the extracted model. “Matches” means normalized expression match, not business sign-off. Formatting, source lineage, relationships and visual context are separate checks.

| Measure | Present | Formula comparison |
| --- | --- | --- |
| Total Referrals | Yes | Matches |
| Open Referrals | Yes | Matches |
| Closed Referrals | Yes | Matches |
| Referrals With an Offer | Yes | Matches |
| Referrals Awaiting Offer | Yes | Matches |
| Referrals Without Provider Assignment | Yes | Matches |
| Open Overdue Referrals | Yes | Matches |
| Referrals Placed by Required Date | Yes | Matches |
| Placement Target Hit Rate | Yes | Matches |
| Median Days to First Action | Yes | Matches |
| Median Days to First Offer | Yes | Matches |
| Median Days to IPA | Yes | Matches |
| Open Referrals Stalled 7+ Days | Yes | Matches |
| Offers Submitted | Yes | Matches |
| Accepted Offers | Yes | Matches |
| Offers with a Decision | Yes | Matches |
| Offer Acceptance Rate | Yes | Matches |
| Average Offers per Referral | Yes | Matches |
| Offers in Draft | Yes | Matches |
| Draft Offers Stalled 7+ Days | Yes | Review/adaptation listed above |
| IPAs Created | Yes | Matches |
| Active IPAs | Yes | Matches |
| Estimated Active Weekly Cost | Yes | Matches |
| Average Estimated Weekly Cost — Confirmed Referrals | Yes | Matches |
| Provider Assignments | Yes | Matches |
| Provider Declines | Yes | Matches |
| Provider Decline Rate | Yes | Matches |
| Snapshot Referrals | Yes | Matches |
| Open Referrals at Snapshot | Yes | Matches |
| Closed Referrals at Snapshot | Yes | Matches |
| Referrals with IPA at Snapshot | Yes | Matches |
| Open Overdue Referrals at Snapshot | Yes | Matches |
| Open On-Track Referrals at Snapshot | Yes | Matches |
| Open Referral Rate at Snapshot | Yes | Matches |
| Placement Rate at Snapshot | Yes | Matches |
| Female Referrals | Yes | Review/adaptation listed above |
| Male Referrals | Yes | Review/adaptation listed above |
| Other Gender Referrals | Yes | Review/adaptation listed above |
| Total Gendered Referrals | Yes | Review/adaptation listed above |
| Referrals Created This Month | Yes | Matches |
| Referrals Created Previous Month | Yes | Matches |
| Referral Volume Month on Month | Yes | Matches |
| Referral Volume Month on Month % | Yes | Matches |
| Referrals Created This Financial Year | Yes | Matches |
| Referrals Currently Active | Yes | Matches |
| Referrals Under Offer | Yes | Matches |
| Closed or Cancelled Referrals | Yes | Matches |
| Active Referrals With Provider Engagement | Yes | Matches |
| Active Referral Engagement Rate | Yes | Matches |
| Active Awaiting Offers With Engagement | Yes | Review/adaptation listed above |
| Active Awaiting Offers Without Engagement | Yes | Review/adaptation listed above |
| Emergency Referrals | Yes | Matches |
| Planned Referrals | Yes | Review/adaptation listed above |
| Emergency Placement Rate | Yes | Matches |
| Referrals With Multiple Provider Assignments | Yes | Matches |
| Non-Draft Offers | Yes | Matches |
| Pending Offers | Yes | Matches |
| Unsuccessful Offers | Yes | Matches |
| Offers With Recorded Rejection Reason | Yes | Matches |
| Providers Who Made Offers | Yes | Matches |
| Average Offers per Provider | Yes | Matches |
| Average Offers per Referral Under Offer | Yes | Matches |
| Offers on Referrals Under Offer | Yes | Matches |
| Spot Offers | Yes | Matches |
| Non-Spot Offers | Yes | Matches |
| Spot Offer Rate | Yes | Matches |
| Draft Offers With No Activity Since Creation | Yes | Matches |
| Draft Offers With Activity Since Creation | Yes | Review/adaptation listed above |
| Draft Offers Missing Dates | Yes | Matches |
| Draft Offers Stalled 14+ Days | Yes | Matches |
| Average Days in Draft | Yes | Matches |
| Oldest Draft Age Days | Yes | Matches |
| Draft Offers With No Activity % | Yes | Matches |
| Pending Offers 0-7 Days | Yes | Review/adaptation listed above |
| Pending Offers 8-14 Days | Yes | Review/adaptation listed above |
| Pending Offers 15-29 Days | Yes | Review/adaptation listed above |
| Pending Offers 30+ Days | Yes | Review/adaptation listed above |
| Providers With Pending Offers 30+ Days | Yes | Review/adaptation listed above |
| Latest Offer Source Export | Yes | Matches |
| Provider Homes Registered | Yes | Matches |
| Providers Registered | Yes | Matches |
| Providers - Fostering | Yes | Matches |
| Providers - Residential | Yes | Matches |
| Providers - Supported Accommodation | Yes | Matches |
| Residential Homes | Yes | Matches |
| Supported Accommodation Homes | Yes | Matches |
| Fostering Homes | Yes | Matches |
| Framework Providers | Yes | Matches |
| Non-Framework Providers | Yes | Matches |
| Providers With QA Flags | Yes | Review/adaptation listed above |
| QA Flagged Homes | Yes | Review/adaptation listed above |
| Providers Pending Onboarding | Yes | Matches |
| Providers Approved | Yes | Matches |
| Provider Onboarding Success Rate | Yes | Matches |
| Provider Submission Documents | Yes | Matches |
| Documents Expiring Next 30 Days | Yes | Matches |
| Documents Expired | Yes | Matches |
| Provider Homes With Expired Documents | Yes | Matches |
| IPAs Issued This Month | Yes | Matches |
| Closed IPAs | Yes | Matches |
| Average Active IPA Weekly Cost | Yes | Matches |
| Total IPA Weekly Cost | Yes | Matches |
| Accepted Offers With IPA | Yes | Matches |
| Offers Awaiting IPA Creation | Yes | Matches |
| Accepted Offer to IPA Conversion % | Yes | Matches |
| Offers Still to Progress to IPA % | Yes | Matches |
| Referrals With Fully Signed IPA | Yes | Matches |
| IPA Signature Completion Rate | Yes | Matches |
| Referral Lifecycle Events | Yes | Matches |
| Referrals With Lifecycle Activity | Yes | Matches |
| Average Lifecycle Events per Referral | Yes | Matches |
| Provider Messages Sent | Yes | Matches |
| Gold Model Last Refreshed | Yes | Matches |
| Total Referrals Previous Month | Yes | Matches |
| Total Referrals Variance | Yes | Matches |
| Total Referrals MoM % | Yes | Matches |
| Total Referrals Variance Indicator | Yes | Matches |
| Total Referrals Variance Indicator Color | Yes | Matches |
| Open Referrals Previous Month | Yes | Matches |
| Open Referrals Variance | Yes | Matches |
| Open Referrals MoM % | Yes | Matches |
| Open Referrals Variance Indicator | Yes | Matches |
| Open Referrals Variance Indicator Color | Yes | Matches |
| Closed Referrals Previous Month | Yes | Matches |
| Closed Referrals Variance | Yes | Matches |
| Closed Referrals MoM % | Yes | Matches |
| Closed Referrals Variance Indicator | Yes | Matches |
| Closed Referrals Variance Indicator Color | Yes | Matches |
| Referrals With an Offer Previous Month | Yes | Matches |
| Referrals With an Offer Variance | Yes | Matches |
| Referrals With an Offer MoM % | Yes | Matches |
| Referrals With an Offer Variance Indicator | Yes | Matches |
| Referrals With an Offer Variance Indicator Color | Yes | Matches |
| Referrals Awaiting Offer Previous Month | Yes | Matches |
| Referrals Awaiting Offer Variance | Yes | Matches |
| Referrals Awaiting Offer MoM % | Yes | Matches |
| Referrals Awaiting Offer Variance Indicator | Yes | Matches |
| Referrals Awaiting Offer Variance Indicator Color | Yes | Matches |
| Referrals Under Offer Previous Month | Yes | Matches |
| Referrals Under Offer Variance | Yes | Matches |
| Referrals Under Offer MoM % | Yes | Matches |
| Referrals Under Offer Variance Indicator | Yes | Matches |
| Referrals Under Offer Variance Indicator Color | Yes | Matches |
| Referrals Currently Active Previous Month | Yes | Matches |
| Referrals Currently Active Variance | Yes | Matches |
| Referrals Currently Active MoM % | Yes | Matches |
| Referrals Currently Active Variance Indicator | Yes | Matches |
| Referrals Currently Active Variance Indicator Color | Yes | Matches |
| Closed or Cancelled Referrals Previous Month | Yes | Matches |
| Closed or Cancelled Referrals Variance | Yes | Matches |
| Closed or Cancelled Referrals MoM % | Yes | Matches |
| Closed or Cancelled Referrals Variance Indicator | Yes | Matches |
| Closed or Cancelled Referrals Variance Indicator Color | Yes | Matches |
| Active Referral Engagement Rate Previous Month | Yes | Matches |
| Active Referral Engagement Rate Variance | Yes | Matches |
| Active Referral Engagement Rate MoM % | Yes | Matches |
| Active Referral Engagement Rate Variance Indicator | Yes | Matches |
| Active Referral Engagement Rate Variance Indicator Color | Yes | Matches |
| Offers on Referrals Under Offer Previous Month | Yes | Matches |
| Offers on Referrals Under Offer Variance | Yes | Matches |
| Offers on Referrals Under Offer MoM % | Yes | Matches |
| Offers on Referrals Under Offer Variance Indicator | Yes | Matches |
| Offers on Referrals Under Offer Variance Indicator Color | Yes | Matches |
| Offer Receipt Rate (Created in Period) Previous Month | Yes | Matches |
| Offer Receipt Rate (Created in Period) Variance | Yes | Matches |
| Offer Receipt Rate (Created in Period) MoM % | Yes | Matches |
| Offer Receipt Rate (Created in Period) Variance Indicator | Yes | Matches |
| Offer Receipt Rate (Created in Period) Variance Indicator Color | Yes | Matches |
| Referrals Not Yet Closed (Created in Period) | Yes | Matches |
| Referrals With Offers (Created in Period) | Yes | Matches |
| Offer Receipt Rate (Created in Period) | Yes | Matches |
| Draft Offers on Referrals Under Offer | Yes | Matches |
| Pending Offers on Referrals Under Offer | Yes | Matches |
| Successful Offers on Referrals Under Offer | Yes | Matches |
| Unsuccessful Offers on Referrals Under Offer | Yes | Matches |
| Spot Offers on Referrals Under Offer | Yes | Matches |
| Framework Offers on Referrals Under Offer | Yes | Matches |
| Providers With Offers on Referrals Under Offer | Yes | Matches |
| Average Offers per Provider - Under Offer | Yes | Matches |
| Draft Offers With No Activity - Under Offer Referrals | Yes | Matches |
| Draft Offers Stalled 14+ Days - Under Offer Referrals | Yes | Matches |
| IPA Completed | Yes | Matches |
| IPAs Pending Completion | Yes | Matches |
| IPA Created to Completion % | Yes | Review/adaptation listed above |
| Successful Offers to IPA Completed % | Yes | Review/adaptation listed above |
| Referrals With IPA | Yes | Matches |
| Referrals With IPA Pending Signature | Yes | Review/adaptation listed above |
| IPA Signature Pending Rate | Yes | Matches |
| Referrals Placed by Target at Snapshot | Yes | Matches |
| Target Hit Rate at Snapshot | Yes | Matches |
| Is Non Framework Provider | Yes | Matches |
| IPA Exists | Yes | Review/adaptation listed above |
| Is Awaiting IPA Creation | Yes | Review/adaptation listed above |
| Is IPA Completed | Yes | Review/adaptation listed above |
| Is IPA Pending | Yes | Review/adaptation listed above |

## Complete KPI traceability: KPI-01–117

The reference status is reproduced as a claim from that document. “Definition present” means a matching existing measure or documented visual composition is available; it does not promote proxies or failed prerequisites to business coverage. Use the original assessment meaning in the acceptance column to resolve disagreements.

| KPI | Req IDs in reference | Original KPI | Existing measure / disposition | Reference status | Audit finding / acceptance |
| --- | --- | --- | --- | --- | --- |
| KPI-01 | [R24,R51] | Total Referrals | Total Referrals | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-02 | [R24,R36] | Referrals With Offers | Referrals With an Offer | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-03 | [R24,R36] | Referrals Awaiting Offer | Referrals Awaiting Offer | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-04 | [R51] | Male Referrals | Male Referrals | ✅ Covered | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| KPI-05 | [R51] | Female Referrals | Female Referrals | ✅ Covered | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| KPI-06 | [R51] | Other Referrals | Other Gender Referrals | ✅ Covered | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| KPI-07 | [R51] | Total Gendered Referrals | Total Gendered Referrals | ✅ Covered | Model uses the actual [Gender Clean] column instead of guide [gender_clean]. Name adaptation is valid, but dim_person is built via a Silver-backed query, so Gold-only source compliance remains open. |
| KPI-08 | [R24] | Referrals Not Yet Closed (Created in Period) | Referrals Not Yet Closed (Created in Period) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-09 | [R24,R51] | Referrals With Offers (Created in Period) | Referrals With Offers (Created in Period) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-10 | [R51] | Total Referrals That Received Offers | Offer Receipt Rate (Created in Period) | ✅ Covered | Assessment describes a referral count; the reference maps it to Offer Receipt Rate, a percentage. Count and rate are not interchangeable; retain a count and label the rate separately. |
| KPI-11 | [R25,R26] | No. Providers Who Made Offers | Providers Who Made Offers | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-12 | [R25-R29] | Total Offers Made Historically | Offers Submitted | 🔁 Alias | Assessment excludes Draft; reference alias Offers Submitted counts all offers. Use Non-Draft Offers for that original cohort. |
| KPI-13 | [R51] | Avg Offers per Referral (Under Offer) | Average Offers per Referral Under Offer | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-14 | [R51] | Avg Offers per Provider (Under Offer) | Average Offers per Provider (Under Offer Referrals) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-15 | [R28] | Successful Offers (Under Offer Referrals) | Successful Offers (Under Offer Referrals) | ✅ Covered | Visual/alias definition; reconcile the named disposition with report bindings. |
| KPI-16 | [R28] | Unsuccessful Offers (Under Offer Referrals) | Unsuccessful Offers | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-17 | [R24] | Offers in Draft (Under Offer Referrals) | Offers in Draft | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-18 | [R24] | Pending Offers (Under Offer Referrals) | Pending Offers (Under Offer Referrals) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-19 | [R24,R26] | Active Referrals With Provider Engagement | Active Referrals With Provider Engagement | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-20 | [R24,R26] | Active Referral Engagement Rate | Active Referral Engagement Rate | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-21 | [R24,R26] | Active Awaiting Offers (Engaged) | Active Referrals With Provider Engagement | 🔁 Alias | Reference aliases an awaiting-offer subset to all active engaged referrals. Active Awaiting Offers With Engagement is the closer existing definition; verify its active filter. |
| KPI-22 | [R24,R26] | Active Awaiting Offers (No Engagement) | Active Awaiting Offers Without Engagement | 🔁 Alias | Verify awaiting and active cohort; model and guide differ on is_open. |
| KPI-23 | [R24,R52] | Referrals This Month | Referrals Created This Month | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-24 | [R52] | Referrals This FY | Referrals Created This Financial Year | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-25 | [R67,R68] | Total Offers Made | Offers Submitted | 🔁 Alias | Assessment specifies non-draft offers; Offers Submitted includes Draft. Reconcile with Non-Draft Offers. |
| KPI-26 | [R13] | Placement Type Totals (Visual) | Total Referrals + `fact_referral[placement_type_required]` visual dimension | 🔁 Alias | Assessment table mixes placement type with spot/framework. These are separate dimensions; agree visual scope. |
| KPI-27 | [R18] | Spot Offers (Under Offer Referrals) | Spot Offers | ✅ Covered | Spot does not mean emergency. Use is_emergency_placement for R18/R34/R57; spot is a separate commercial classification. |
| KPI-28 | [R25-R29] | Offer Count | Offers Submitted | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-29 | [R24] | Referrals Currently Active | Referrals Currently Active | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-30 | [R24,R36] | Active Referrals Under Offer | Referrals Under Offer | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-31 | [R13] | Referrals Cancelled/Closed | Closed or Cancelled Referrals | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-32 | [R24,R36] | Active Referrals Awaiting Offers | Referrals Awaiting Offer | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-33 | [R24] | Referrals With One or More Offers | Referrals With an Offer | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-34 | [R54] | Closed Referrals (by Reason) | Closed Referrals + `fact_referral[referral_closure_reason]` visual dimension | ✅ Covered | Closure reasons and provider decline reasons have different grains. This cannot close all of R54. |
| KPI-35 | [R25-R29] | Total Offers Made (Active Referrals Under Offer) | Offers on Referrals Under Offer | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-36 | [R25-R29] | Offer IDs (Under Offer Referrals) | Retired — internal CALCULATETABLE helper; Gold relationship graph + TREATAS make it unnecessary | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — internal CALCULATETABLE helper; Gold relationship graph + TREATAS make it unnecessary |
| KPI-37 | [R26] | Offers per Provider (Under Offer Referrals) | Offers per Provider (Under Offer Referrals) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-38 | [R67,R68] | Framework Offers (Under Offer Referrals) | Framework Offers (Under Offer Referrals) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-39 | [R28,R35] | Accepted Offers (Scoped Table) | Retired — internal scoped-table helper (see KPI-36) | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — internal scoped-table helper (see KPI-36) |
| KPI-40 | [R91,R93] | Provider Homes Registered | Provider Homes Registered | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-41 | [R91,R93] | Providers Registered | Providers Registered | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-42 | [R95] | Providers - Fostering | Providers - Fostering | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-43 | [R96] | Providers - Residential | Providers - Residential | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-44 | [R91] | Providers - Supported Accommodation | Providers - Supported Accommodation | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-45 | [R67] | Framework Providers | Framework Providers | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-46 | [R46] | NON Framework Providers | Non-Framework Providers | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-47 | [R46] | Is Non Framework Provider | Is Non Framework Provider (row helper) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-48 | [R93] | Directory Summary Count | Retired — depended on report-view axis tables; rebuild with field parameters over `dim_provider_home[service_type]` if needed | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — depended on report-view axis tables; rebuild with field parameters over `dim_provider_home[service_type]` if needed |
| KPI-49 | [R96] | Residential Homes | Residential Homes | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-50 | [R91] | Supported Accommodation Homes | Supported Accommodation Homes | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-51 | [R95] | Fostering Providers | Providers - Fostering | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-52 | [R95] | Fostering Chart Count | Retired — depended on `rpt_provider_fostering` report-view table (see KPI-48) | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — depended on `rpt_provider_fostering` report-view table (see KPI-48) |
| KPI-53 | [R24] | Draft No Activity Since Creation | Draft Offers With No Activity Since Creation | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-54 | [R24] | Draft Offers With Activity Since Creation | Draft Offers With Activity Since Creation | ✅ Covered | Model filters two FALSE flags but omits offer_status = draft. Non-draft offers can satisfy both FALSE flags. Restore the draft-status predicate before using KPI-54/56. |
| KPI-55 | [R24] | Draft Offers Missing Dates | Draft Offers Missing Dates | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-56 | [R24] | Draft Offers Updated After Creation | Draft Offers With Activity Since Creation | 🔁 Alias | Model filters two FALSE flags but omits offer_status = draft. Non-draft offers can satisfy both FALSE flags. Restore the draft-status predicate before using KPI-54/56. |
| KPI-57 | [R24] | Draft No Activity 7+ Days | Draft Offers Stalled 7+ Days | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-58 | [R24] | Drafts No Activity 14+ Days | Draft Offers Stalled 14+ Days | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-59 | [R24] | Average Days in Draft | Average Days in Draft | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-60 | [R24] | Oldest Draft Age (Days) | Oldest Draft Age Days | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-61 | [R24] | Draft Offer Count | Offers in Draft | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-62 | [R24] | Draft With No Activity Since Creation (%) | Draft Offers With No Activity % | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-63 | [R24] | Drafts With No Activity 14+ Days | Draft Offers Stalled 14+ Days | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-64 | [R24] | Pending Offers by Age Bucket | Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands |
| KPI-65 | [R24] | Pending Offers 15–30 Days | Pending Offers 15-29 Days | ✅ Covered | Reference changes 15-30 inclusive to 15-29 to avoid overlap with 30+. Confirm the boundary; model also mixes query-time and stored age. |
| KPI-66 | [R24] | Pending Offers 30+ Days | Pending Offers 30+ Days | ✅ Covered | Model computes age at query time from reviewed/submitted date; 0-7/8-14 use stored Gold age. Mixed clocks can cause overlaps/gaps between bands. |
| KPI-67 | [R24] | Pending Offers 0–7 Days | Pending Offers 0-7 Days | ✅ Covered | Stored activity-age band; test blanks, negative ages and day-7 boundary. Must use the same clock as 15-29/30+. |
| KPI-68 | [R24] | Pending Offers 8–14 Days | Pending Offers 8-14 Days | ✅ Covered | Stored activity-age band; test day-8/day-14 boundaries. Must use the same clock as 15-29/30+. |
| KPI-69 | [R24,R26] | Provider with Offers over 30+ Days | Providers With Pending Offers 30+ Days | ✅ Covered | Uses query-time age instead of Gold days_since_offer_activity. Align with the pending-offer cohort chosen for KPI-65-69. |
| KPI-70 | [R24] | Offers At Risk (8–14 Days) | Pending Offers 8-14 Days | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-71 | [R24] | Offers Outside Timeframe (15–30 Days) | Pending Offers 15-29 Days | 🔁 Alias | Alias must use non-overlapping 15-29 band and the agreed common age clock. |
| KPI-72 | [R24] | Critical Offers (30+ Days) | Pending Offers 30+ Days | 🔁 Alias | Model computes age at query time from reviewed/submitted date; 0-7/8-14 use stored Gold age. Mixed clocks can cause overlaps/gaps between bands. |
| KPI-73 | [R35] | IPA Exists | IPA Exists (row helper) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-74 | [R28] | Is In Accepted KPI | Blocked — no IPA-grain signature status; use the referral-grain IPA funnel instead | ❌ Blocked | Reference marks this blocked; WIP describes a retired layout helper. Use Accepted Offers and explicit IPA row flags rather than asserting this proves an IPA signature. |
| KPI-75 | [R28,R35] | Accepted Offers Base | Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it |
| KPI-76 | [R35] | IPA Created | IPAs Created | ✅ Covered | IPAs Created counts ipa_id; legacy IPA Created counts accepted offer_id with IPA. Use the correct named measure for the requested grain. |
| KPI-77 | [R35] | IPA Completed | IPA Completed — offer-grain, GLD-013 | ✅ Covered | Present at offer grain using is_ipa_completed. Original assessment asks for distinct signed IPAs; not evidence of per-IPA signature completion. |
| KPI-78 | [R35] | IPAs Pending Completion | IPAs Pending Completion — offer-grain, GLD-013 (referral-grain proxy [Referrals With IPA Pending Signature] also available) | ✅ Covered | Present at offer grain using is_ipa_pending. Original asks for unsigned, non-closed IPAs; agree scope before marking exact coverage. |
| KPI-79 | [R35] | Offers Awaiting IPA Creation | Offers Awaiting IPA Creation | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-80 | [R35] | Is IPA Pending | Is IPA Pending (row helper) — GLD-013 | ✅ Covered | Offer-grain row helper; does not supply missing per-IPA signature history. |
| KPI-81 | [R35] | Is Awaiting IPA Creation | Is Awaiting IPA Creation (row helper) | ✅ Covered | Definition present; relationship, source and result acceptance still required. |
| KPI-82 | [R35] | Is IPA Completed | Is IPA Completed (row helper) — GLD-013 | ✅ Covered | Offer-grain row helper; does not supply missing per-IPA signature history. |
| KPI-83 | [R35] | Accepted Offer to IPA Conversion % | Accepted Offer to IPA Conversion % | ✅ Covered | Offer-to-IPA flag conversion; do not interpret as a count of IPAs per offer. |
| KPI-84 | [R35] | Offers Still to Progress to IPA | Offers Still to Progress to IPA % | ✅ Covered | Assessment asks for a count; reference maps to a percentage. Offers Awaiting IPA Creation supplies the count and Offers Still to Progress to IPA % supplies the rate. |
| KPI-85 | [R35] | IPA Created to Completion % | IPA Created to Completion % — GLD-013 | ✅ Covered | Model uses [IPA Created] with alternate result 0; the helper counts accepted offers with IPA. Guide uses [Accepted Offers With IPA]. Both are offer-grain, but confirm accepted-status cohorts and blank-versus-zero reporting. |
| KPI-86 | [R35] | Successful Offers to IPA Completed % | Successful Offers to IPA Completed % — GLD-013 | ✅ Covered | Offer-grain completion ratio and empty-denominator policy require sign-off, not an IPA-grain signature KPI. |
| KPI-87 | [R82] | Dashboard Last Refreshed | Gold Model Last Refreshed | 🔁 Alias | Gold model timestamp measures data freshness, not rendering latency, scalability or an R82 performance SLA. |
| KPI-88 | [R53] | Latest Export per Offer | Latest Offer Source Export | 🔁 Alias | Definition present; relationship, source and result acceptance still required. |
| KPI-89 | [R24] | Latest Offer Status Count | Retired — Gold `fact_offer` is already deduplicated to the latest state per offer | 🗄 Retired | Intentional retirement; verify replacement visual behaviour. Retired — Gold `fact_offer` is already deduplicated to the latest state per offer |
| KPI-90 | [R22] | Overlap Referrals | Referrals With Multiple Provider Assignments | ✅ Covered | Multiple provider assignments are not evidence of an out-of-region placement. R22 remains open. |
| KPI-91 | [R18,R57] | Emergency Referrals | Emergency Referrals | ✅ Covered | Emergency reporting is present; original asks for active same-day cases. Reconcile Gold flag semantics and active/all denominator; distinct emergency IDs and finance workflow are outside DAX. |
| KPI-92 | [R18,R57] | Emergency Placement Rate | Emergency Placement Rate | ✅ Covered | Confirm active emergency numerator and denominator scope; do not substitute spot for emergency. |
| KPI-93 | [R57] | Planned Referrals | Planned Referrals | ✅ Covered | Model requires required date after creation; guide uses non-emergency with dates present. Negative date intervals differ. Define the invalid-date treatment and emergency/planned denominator. |
| KPI-94 | [R18,R57] | Emergency vs Planned Split | Visual split using [Emergency Referrals] and [Planned Referrals]; no separate measure | ✅ Covered | Two existing measures can drive a visual; emergency/planned scope and invalid-date handling need agreement. |
| KPI-95 | [R22] | Out-of-Region Referrals | Blocked — `fact_referral[region]` is null until a reliable source supplies it | ❌ Blocked | Open data/definition gap. Blocked — `fact_referral[region]` is null until a reliable source supplies it |
| KPI-96 | [R22] | Out-of-Region Placement Rate | Blocked — as KPI-95 | ❌ Blocked | Open data/definition gap. Blocked — as KPI-95 |
| KPI-97 | [R41] | Providers with QA Flags | Providers With QA Flags | ✅ Covered | Model filters bridge_provider_framework[qa_flag] while counting dim_provider. With the saved one-way relationship, the bridge cannot filter the provider dimension back. Use the provider QA flag for the documented KPI, or explicitly transfer framework-provider IDs if framework QA is intended. |
| KPI-98 | [R41] | QA Flag Type Breakdown | Blocked — no QA flag-type dimension to unpivot in Gold | ❌ Blocked | Open data/definition gap. Blocked — no QA flag-type dimension to unpivot in Gold |
| KPI-99 | [R41] | QA Flagged Providers by Home | QA Flagged Homes | ✅ Covered | Model filters bridge_provider_framework[qa_flag] while counting dim_provider_home; there is no active filtering route to homes. Use home QA flags for the guide definition; a provider-to-home inherited flag requires an explicit agreed rule. |
| KPI-100 | [R47] | Documents Expiring (30 Days) | Documents Expiring Next 30 Days | ✅ Covered | Expiry dates support the metric; reminder delivery and missing-document completeness require separate workflow evidence. |
| KPI-101 | [R47,R48] | Documents Expired | Documents Expired | ✅ Covered | Expired-document count is present; it does not prove referral exclusion for R48. |
| KPI-102 | [R48] | Providers Blocked (Incomplete Docs) | Blocked — no expected-document set in Gold to test completeness against | ❌ Blocked | Open data/definition gap. Blocked — no expected-document set in Gold to test completeness against |
| KPI-103 | [R48] | Document Compliance Rate | Blocked — as KPI-102 | ❌ Blocked | Open data/definition gap. Blocked — as KPI-102 |
| KPI-104 | [R49] | Provider Due Diligence Status | Providers Pending Onboarding / Providers Approved (provider_status split) | ✅ Covered | Provider status is available; verify it represents due-diligence approval rather than just registration status. |
| KPI-105 | [R54] | Decline Reasons (Referral Level) | Blocked — no decline-reason history in active Gold | ❌ Blocked | Open data/definition gap. Blocked — no decline-reason history in active Gold |
| KPI-106 | [R58] | Framework Changes During Active Referrals | Blocked — no framework-change history in active Gold | ❌ Blocked | Open data/definition gap. Blocked — no framework-change history in active Gold |
| KPI-107 | [R62] | Total Weekly Fee Liability | Estimated Active Weekly Cost — estimate, not signed-only actuals | ⚠️ Proxy | Estimated active cost is not signed-only weekly fee liability or actual payments. R62 remains partial. |
| KPI-108 | [R62] | Payment Method Breakdown | Blocked — no payment method / payment facts in Gold | ❌ Blocked | Open data/definition gap. Blocked — no payment method / payment facts in Gold |
| KPI-109 | [R62] | IPA Payment Status | Blocked — no payment lifecycle facts in Gold | ❌ Blocked | Open data/definition gap. Blocked — no payment lifecycle facts in Gold |
| KPI-110 | [R14] | Messages Sent | Provider Messages Sent — lifecycle-event proxy for volume only; no response-time or unread analysis | ⚠️ Proxy | Lifecycle-event volume proxy; verify event coverage. No response-time or unread-message evidence. |
| KPI-111 | [R14] | Avg Message Response Time (Hours) | Blocked — no message response-time facts in Gold | ❌ Blocked | Open data/definition gap. Blocked — no message response-time facts in Gold |
| KPI-112 | [R14] | Priority Messages Unread | Blocked — no message-status facts in Gold | ❌ Blocked | Open data/definition gap. Blocked — no message-status facts in Gold |
| KPI-113 | [R20] | Audit Events by Type | Referral Lifecycle Events — derived roll-up, not the source audit log | ⚠️ Proxy | Derived lifecycle events are not the source audit trail for signatures, approvals and negotiations. |
| KPI-114 | [R20,R35] | IPA Signature Completion Rate | IPA Signature Completion Rate — referral-grain proxy | ⚠️ Proxy | Referral signature proxy, not original per-IPA signature completion; pending cohort also differs from the guide. |
| KPI-115 | [R19] | Referral Updates per Day | Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure | ❌ Blocked | Open data/definition gap. Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure |
| KPI-116 | [R59] | Provider Onboarding Pipeline | Providers Pending Onboarding | ✅ Covered | Registration-state reporting supports onboarding visibility, not bulk onboarding execution. |
| KPI-117 | [R59] | Bulk Onboarding Success Rate | Provider Onboarding Success Rate | ✅ Covered | Approved/registered proportion has no batch/job denominator. It is not a measured bulk-import success rate. |

## Complete requirement traceability: 80 assessed requirements

This retains the assessment’s original requirement text and KPI links. The original “Implemented” label is not reused as proof of the current build. For platform/feature/security rows, no DAX measure can by itself close the requirement.

| Req | Requirement | Assessment KPI links | Current audit status | Remaining acceptance evidence |
| --- | --- | --- | --- | --- |
| R1 | Place children with complex care needs | KPI-01, KPI-08 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R2 | Consider current incumbent solution | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R3 | Single regional platform (cross-boundary) | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R4 | Open source suitability | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R5 | Agile / MVP / backlog | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R6 | COTS preferred over bespoke | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R7 | APIs across WM IT ecosystem | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R8 | Open-source API compliance | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R9 | Form pre-population (referral, OFSTED, auth) | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R11 | Publish placement requirements to providers | KPI-01, KPI-08 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R12 | GDPR / DPA 2018 compliance for vulnerable-child data | — | Security acceptance open | No roles in inspected model. Verify effective workspace/app permissions, RLS where required, audit and access procedures. |
| R13 | Filter by specialisms, placement type, placement status | KPI-26, KPI-34 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R14 | In-system messaging (auditable, prioritised, urgent) | KPI-110, KPI-111, KPI-112 | Partial / open | Message-volume proxy present; response times, priority/unread state and messaging workflow remain unproven. |
| R15 | Digital info & signatures for IPA | KPI-73, KPI-76, KPI-77 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R16 | Priority information flagged in placement requests | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R17 | Placement info immediately available on accept | KPI-75 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R18 | Emergency placements: same-day, distinct ID, separate reporting & finance | KPI-91, KPI-92, KPI-94 | Partial / open | Emergency metrics present; validate active/same-day cohort, distinct emergency ID, separate reporting and finance workflow. |
| R19 | Update referrals; auto-notify providers | KPI-115 | Partial / open | Missing durable update/notification evidence. Lifecycle activity cannot prove updates or notification delivery. |
| R20 | Full audit tracking (placements, IPA, signatures, approvals, negotiations) | KPI-113, KPI-114 | Partial / open | Derived lifecycle and referral-signature proxies do not prove a complete source audit trail. |
| R21 | Auto-notify unsuccessful providers; optional rejection feedback | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R22 | Out-of-region placements tagged; finance informed | KPI-90 (partial), KPI-95, KPI-96 | Partial / open | Out-of-region KPIs remain blocked; overlap/provider assignments are not a substitute for geographic tagging or finance notification. |
| R24 | Dashboard: status overview, provider updates, task mgmt, quick updates | KPI-01–KPI-89 (85 measures) | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R25 | Quickly review detailed placement requests | KPI-11, KPI-12 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R26 | Prioritise by match suitability, SOP, existing placements | KPI-19, KPI-20, KPI-37 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R27 | Request additional info, raise queries, see responses | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R28 | Accept / reject / request further info | KPI-15, KPI-16, KPI-75 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R29 | Streamlined offer process | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R31 | Resolved requests auto-removed from provider views | — | Partial / open | Open gap with no mapped KPI: resolved-request visibility/outcome data and a Resolved Requests Visible check are absent from the WIP inventory. |
| R32 | Matching by SOP and care specialisms | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R33 | Upload and manage placement documentation | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R34 | Emergency referrals identifiable and prioritised | KPI-91, KPI-94 | Partial / open | Emergency flag/reporting support exists; provider prioritisation workflow and cohort require acceptance. |
| R35 | Digitised IPA (review, approvals, signing, audit) | KPI-73–KPI-86 | Partial / open | Offer-grain IPA funnel present; per-IPA signatures, approval workflow and full audit are not fully evidenced. |
| R36 | Dedicated view: referrals with outstanding offers / open offers | KPI-10, KPI-29 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R38 | Record QA assessment outcomes against providers | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R39 | Desk-based research; identify missing documentation | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R41 | Apply advisory notices and flags (information notices, safeguarding) | KPI-97, KPI-98, KPI-99 | Partial / open | QA count formulas need filter correction; flag-type breakdown and apply/remove workflow remain open. |
| R45 | SPOT providers upload registration documentation | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R46 | QA intelligence for non-framework providers shared appropriately | KPI-46, KPI-47 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R47 | Monitor documentation expiry; send reminders; highlight missing | KPI-100, KPI-101 | Partial / open | Expiry counts present; missing-document completeness and reminder delivery require more data/workflow evidence. |
| R48 | Providers with incomplete docs excluded from referrals | KPI-102, KPI-103 | Partial / open | Expected-document set and exclusion outcome missing. Expired documents alone do not prove provider blocking. |
| R49 | Easily identify provider due diligence status | KPI-104 | Partial / open | Provider-status reporting exists; verify it is authoritative due-diligence status. |
| R51 | Robust data model: placement records, market intelligence, value analysis | KPI-01–KPI-10, KPI-13, KPI-14, KPI-20 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R52 | Accurate and customisable reporting | KPI-23, KPI-24 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R53 | Data consistent, exportable, supports bespoke analysis | KPI-88 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R54 | Capture reasons for declined placements | KPI-34 (partial), KPI-105 | Partial / open | Closure/offer rejection measures do not supply full provider/referral decline history. |
| R55 | RBAC: commissioners access regional data, market-wide trends | — | Security acceptance open | No roles in inspected model. Verify effective workspace/app permissions, RLS where required, audit and access procedures. |
| R57 | Emergency and planned placements separately reportable | KPI-91, KPI-93, KPI-94 | Partial / open | Emergency/planned formulas exist, but date/case scope differs and the split needs visual acceptance. |
| R58 | Alert when framework changes during active referrals | KPI-106 | Partial / open | Framework-change history and alert-delivery evidence absent. |
| R59 | Bulk provider onboarding supported | KPI-116, KPI-117 | Partial / open | Provider status/proportion available; bulk onboarding requires batch/job outcomes and a defined denominator. |
| R62 | View completed placements, access IPAs, extract payment info | KPI-107, KPI-108, KPI-109 | Partial / open | Estimated cost and IPA counts support partial analysis; actual payments, payment methods and signed fee liability remain open. |
| R67 | Support adding new frameworks | KPI-25, KPI-38 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R68 | Frameworks configurable: display, hide, isolate by region | KPI-25, KPI-38 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R69 | Robust analytical data model | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R70 | Auto-save across workflows | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R71 | Digitised IPA: review, approvals, signing, full audit | KPI-73–KPI-86 | Partial / open | Same offer-versus-IPA grain and signature/audit limitations as R35. |
| R72 | Digitise paper processes: workflow, auditable, trackable, lifecycle | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R73 | Support future enhancements and Agile delivery | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R74 | COTS preferred | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R75 | High availability, scalability, fault tolerance, DR | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R76 | Access restricted to authorised users | — | Security acceptance open | No roles in inspected model. Verify effective workspace/app permissions, RLS where required, audit and access procedures. |
| R77 | Admin: user management, org onboarding, ownership transfer | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R78 | RBAC and full auditing mandatory | — | Security acceptance open | No roles in inspected model. Verify effective workspace/app permissions, RLS where required, audit and access procedures. |
| R79 | Break-glass access: controlled, auditable, emergency | — | Security acceptance open | No roles in inspected model. Verify effective workspace/app permissions, RLS where required, audit and access procedures. |
| R80 | Fast document upload/retrieval, RBAC-protected access | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R81 | WCAG 2.0/2.1/2.2 compliance | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R82 | Fast response times, scalability, performance reporting | KPI-87 | Partial / open | Freshness timestamp present; performance, scalability and response-time targets need measured SLA evidence. |
| R83 | Migrate placements, purchases, providers, OFSTED, frameworks, active placements | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R84 | Data integrity, retention, export, configurable policies | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R85 | Deployment: FAQs, user guides, demos, support materials | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R86 | Device agnostic, browser compatible, mobile friendly | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R87 | Incident management, issue reporting, SLAs | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R88 | Modular growth, controlled change, product roadmaps | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R89 | Stakeholder demos, UAT, formal sign-off | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R90 | Hosting options, deployment models, cloud strategy | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R91 | Provider registration: company, services, homes, docs | KPI-40, KPI-41 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R92 | LA review and approve/reject registrations | — | Outside measure scope; not signed off | Requires platform, workflow, service or UAT evidence for the stated requirement; no dedicated KPI is specified in the assessment. |
| R93 | Placement officer: provider directory, services, homes, docs | KPI-40–KPI-52 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R94 | QA: search providers, apply/remove flags | KPI-97, KPI-98 (partial) | Partial / open | QA filters need correction; flag-type breakdown and search/apply/remove behaviour remain open. |
| R95 | Reflect Fostering Framework changes (Q3 2024) | KPI-42, KPI-51 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |
| R96 | Reflect Residential Framework 2.0 (Spring 2025) | KPI-43, KPI-49 | Reporting definitions present; acceptance open | Resolve relevant KPI audit findings and shared relationship/source gaps; verify visuals, filter context and source totals. Report measures alone do not prove the full application requirement. |

## Acceptance checks to complete next

1. Correct the three identified filter defects after confirming QA scope; align all pending-age bands to one source clock and non-overlapping boundaries (7/8, 14/15, 29/30), including blank/future dates.
2. Validate unique dimension keys and orphan facts, then repair the required relationships. Check that each month/provider/referral slicer actually changes the intended measure cohort; use snapshot date for historic states.
3. Replace Silver-backed reporting queries with the intended Gold dimensions and verify the actual imported column names. Preserve the semantic `fact_ipa` name over physical `gold.fact_ipa`.
4. Agree count-versus-rate, accepted/non-draft and offer/referral/IPA grain differences with the KPI owner. Keep historical assessment definitions as evidence, not current acceptance claims.
5. Close the data prerequisites for blocked KPIs, or record explicit accepted deferrals. No dummy zero/blank measures should masquerade as implementation.
6. When DAX query execution is authorised, reconcile distinct IDs and totals against source data, test empty denominators and selection context, inspect every report page and refresh errors, and test security as each target role.
7. Obtain separate evidence for R31 visibility, notification/reminder workflows, performance, accessibility, retention, recovery and formal UAT. No full-requirement sign-off is asserted by this audit.
