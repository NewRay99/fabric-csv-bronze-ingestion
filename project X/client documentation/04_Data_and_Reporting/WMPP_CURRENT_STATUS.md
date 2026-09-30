# WMPP reporting status as at 30 September 2026

## Delivery position

The local WIP now supports the reporting journey from overall performance to referral and provider exploration, then record-level drillthrough. The saved model contains **58 tables and 366 measures**. All **109 existing Dashboard Legend measures** resolve by name in that model. The revised Legend adds **35 existing business measures** that were missing from its catalogue, giving **144 catalogue entries**. The remaining model measures include compatibility measures, display logic, selectors, filter gates and other calculations; they are not 222 additional business KPIs.

This is a repository implementation assessment, not production acceptance. The latest journey-strip layout and click actions still require Desktop visual and interaction checks. A full refreshed-model reconciliation, identity-based RLS acceptance and client release approval are not recorded by this assessment. No Fabric deployment, data refresh, publication or report/model modification was performed for this documentation update.

The assessed project is:

`project X/reports/client-deliverables/WMPP v16/SM WMPP v16 updated WIP/SM_WMPP_v16.pbip`

The non-WIP delivery, older `reports/current` copies and ZIP exports are different baselines. Counts and test results from those copies must not be presented as current-WIP acceptance evidence.

## Requirement reassessment

The 80 existing requirement identifiers are preserved. A reporting measure can support a requirement without delivering its portal workflow, notification, security control or operational service level.

| Current assessment | Requirements | Meaning |
| --- | ---: | --- |
| Built; UAT pending | 8 | Reporting scope exists in saved definitions; business acceptance remains open. |
| Partial reporting | 31 | Useful reporting exists, but a source, semantic or workflow limit remains. |
| Open data gap | 3 | R22 out-of-region, R48 compliance/blocking and R58 framework-change history lack the necessary evidence. |
| Security acceptance pending | 5 | R12, R55, R76, R78 and R79 need access, disclosure and identity-based acceptance. |
| Delivery acceptance pending | 9 | Operational, accessibility, device, migration, support and sign-off evidence is separate from KPI implementation. |
| Outside report assessment | 24 | Source-platform, architecture, procurement or editing workflows cannot be certified from Power BI. |
| Total | 80 | These are requirement dispositions, not a percentage-complete score. |

See [the row-level assessment](WMPP_REQUIREMENT_REASSESSMENT.md) and the `RID` sheet in `configuration/Dashboard Legend.xlsx`. The old Status values are retained as **Previous assessment**, and the dated source notes remain intact.

`Req ID` is the existing workbook/model field for the business concept **Requirement_Id**. Keep R-identifiers separate from KPI identifiers. `KPI-01`–`KPI-117` are legacy references; `GOLD-KPI-001`–`GOLD-KPI-144` identify catalogue entries. New requirement associations are proposed for owner approval, not new requirements or signed-off coverage.

## What has materially changed

| Area | Current WIP evidence | Remaining boundary |
| --- | --- | --- |
| Referral exploration | Referral Explorer, persistent category/priority/status/open/overdue and offer filters, category-aware distinct counts | Priority and urgency band are both retained pending an owner decision. Categories are many-to-many and not additive. |
| Referral detail | Referral-key drillthrough, offers, provider messages, ordered lifecycle rows, provider/offer location directory and map | Current source records and derived events do not establish a complete immutable audit trail. |
| Provider exploration | Provider Explorer, provider/home/assignment/offer analysis and provider journey | A provider is counted once at its furthest evidenced stage in the selected cohort, not once per offer. |
| Provider detail | Hidden Provider Detail (Drillthrough) from Provider Explorer; provider/home/assignment/offer/message sections | Provider/home and role context must be tested in Desktop. |
| Referral journey | Created → provider search → offers received → accepted → IPA created → signed, with separate closed and review counts | Current stage is calculated at refresh; it is not historical transition or conversion-rate evidence. |
| Clickable steps | Explorer icons target stage-only selectors; Clear stage removes that selector. Detail icons focus lifecycle activity without changing referral selection | Newest click behaviour and rendering remain unverified. Provider confirmation is unavailable and deliberately not clickable. |
| Monthly performance | Overall Performance includes total/closed snapshots, prior-month change and a separate closure-flow measure | Snapshot state, creation-cohort metrics and closures during month are different populations. Missing prior month is not zero. |
| IPA signatures | `fact_ipa` contains both signing flags, `is_ipa_completed` and `is_ipa_pending`; IPA-grain measures exist | Signing workflow and exact signature event history are separate requirements. |
| Demographics | `dim_person` contains gender and other attributes; gender measures exist | Person linkage, unknowns, privacy and role access require validation. Search uses initials and ID, not an invented full name. |
| Messages and reasons | `dim_referral_provider_message` and `dim_referral_provider_reject_reason` exist in Gold code and model imports | Author role, paired responses, priority/unread semantics, complete reason history and attribution remain open. |
| Categories and location | Current referral/home category bridges; preferred-city location/distance fields; category-aware measures | Current bridges do not prove historic category membership. Support-needs reporting is not in the WIP model. |
| Navigation and presentation | Reordered main navigation, expandable menus/filter drawers, regular small labels, shared styles and category icon labels | Saved-file design changes are not accessibility, browser or mobile acceptance. Hidden legacy pages retain their historical dimensions. |

## Current report route and page inventory

The main route is **Home → Performance → Referrals → Referral Explorer → Referral Detail → Back**, with a parallel **Providers → Provider Explorer → Provider Detail → Back** route. Main navigation is ordered **Home, Performance, Referrals, Offers, Draft offers, IPAs, Providers, Requirements**.

There are **34 page definitions**, of which **12 are visible report pages**. The visible pages are WMPP Homepage, Overall Performance, Referrals, Referral Explorer, Offers Overview, Draft Offers, IPA Overview, Provider Explorer, Provider & Placement Supply, Target & Urgency Performance, Offer Locations and Requirement Matrix Overview. All 12 have a width of **1680 pixels**. Both drillthrough pages also use 1680 pixels. The remaining pages include hidden guides, tooltips and recoverable legacy pages; not every hidden helper is 1680 pixels wide.

Referral Geography and Referral Snapshots are hidden/recoverable, not deleted. Snapshot reporting has moved into Overall Performance. The older duplicate Referral Explorer (Original) is also hidden.

The report contains **158 bookmarks**: the 139 retained bookmarks plus 19 small journey-selector bookmarks. Navigation/display bookmarks and data-selector bookmarks have different purposes. Do not apply a blanket “Data off” cleanup: that would break the new step filters. The latest 19 are scoped to one selector each and suppress display/current-page changes. They were at most 1,028 bytes when created; after the latest save, their maximum formatted size is 3,266 bytes. The earlier cleanup reduced the retained bookmark set from 4,448,643 to 2,164,619 bytes without merging distinct states, according to its saved verification manifest; those are historical, not current file-size totals.

## Meaning of the journeys

### Referral journey

One current stage is assigned per referral at model refresh. Closed/cancelled/withdrawn/completed referrals go to a separate closed group before milestone checks. The remaining precedence is both-signed active IPA, active IPA, accepted offer, pending/submitted offer, review exception, provider assignment, then referral creation. A signed stage requires both signatures on the **same** active IPA. Draft, withdrawn and declined offers do not advance the current open stage.

Explorer stage counts keep the surrounding cohort filters and ignore only the stage selector so all stage counts remain visible while the page is filtered. Confirm this behaviour with category, offer status and activity-band selections in UAT.

Detail milestone evidence is separate from current stage. Clicking a detail milestone focuses event families: referral creation/modification, provider messages, offer submission/update, offer updates, IPA creation/update, or IPA updates. Acceptance and signature are **not explicit event types** in the inspected lifecycle feed; the labels say so. The selected referral remains unchanged.

### Provider journey

The observed stages are **message activity only → offers made → offer accepted → provider signed**. The design retains a disabled **provider confirmation** position labelled **Not captured**. Browsing/view telemetry is absent, and message activity may be authored by either party, so it must not be labelled “provider browsed/commented”.

Providers are classified by their highest evidenced stage in the current cohort. Assignment/draft/unclear providers are recorded separately. Both-signed providers are a subset of provider-signed providers, not an additional stage to add to the total. IPA attribution follows the accepted offer ID, avoiding attribution of another provider's IPA on the same referral.

## Business rules that must remain explicit

- Cost cards show estimated weekly liability. `Lifetime Placement Cost` and `Total Lifetime Cost` also exist, but are estimates based on dates and weekly cost, not invoices or actual expenditure. The lifetime formula uses TODAY for open records and `Total Lifetime Cost` removes ordinary IPA filters; date boundaries and filter intent need finance review before acceptance.
- The source table is now `gold.fact_ipa`, imported as `fact_ipa`. `fct_ipa` and `fact_placement` references in old packs are historical names.
- `Provider Messages Sent` still counts `ProviderMessageSent` lifecycle events even though detailed message records now exist. Do not silently reinterpret it as provider-authored messages or a message response SLA.
- Provider response components use qualifying offers or recorded reasons (`OFFER_OR_RECORDED_REASON_V1`). They are not a composite score, care-quality rating or automatic suitability assessment.
- The emergency flag is a same-day-date derivation, restricted to the specified active statuses in the current measures. Spot purchasing is not synonymous with emergency placement.
- Offer activity bands on Explorer are **0–3, 4–7, 8–14, 15+**, with Unknown/Review handling. These are distinct from submission-age bands on older pending-offer KPIs. Owner approval of the activity-band boundaries is pending.
- Referral/category memberships are current state. A category may contain the same referral as another category. Count distinct referral IDs and do not add category totals.
- Preferred-city distance is approximate centroid-to-postcode straight-line distance using an approved coordinate reference. It is not road distance, travel time, a child's address or out-of-region evidence. Missing coordinates must not become zero distance.

## Remaining release decisions

1. Refresh the WIP model and populate its new calculated/helper objects. Reconcile all journey stages including closed/review exceptions and provider assignment/draft/unclear cases.
2. Visually inspect all three journey strips, test step clicks and Clear stage, and confirm other slicers and navigation/filter drawers remain unchanged. In Desktop edit mode, action icons normally require Ctrl+click.
3. Exercise referral and provider drillthrough, Back, one-record selection guards, messages, reasons, homes and maps with known records.
4. Reconcile two consecutive snapshot months and a known closure. Test missing prior periods, multiple IPAs per offer, closed unsigned IPAs and same-IPA signature rules.
5. Resolve priority versus urgency-band naming, activity-band boundaries, emergency semantics, provider confirmation/browsing gaps and all proposed new KPI-to-requirement associations.
6. Complete identity-based RLS, message/free-text access, map permissions, small-cell disclosure, Build/export and break-glass acceptance. A defined role is not evidence of a secure deployment.
7. Synchronise the embedded `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage` reference tables through a controlled model update. They are embedded historical data, not a live connection to Dashboard Legend. Updating this workbook does **not** update Requirement Matrix Overview.
8. Obtain business, operational and client publication sign-off. Preserve the source and historical packs rather than reusing their old “implemented” counts as current acceptance.

## Evidence and limits

Evidence inspected: WIP PBIR pages/visuals/bookmarks; TMDL tables, measures, columns, relationships and role; the storyboard, category-icon, bookmark-cleanup and journey manifests; active `04_gold_model.py` / `05_gold_dimensions.py`; the existing Legend and controlled client documents.

The journey repair originally recorded 10 passing regression checks and schema validation of 138 changed documents, with five existing visuals skipped because their 2.13 schema was unavailable. Subsequent Desktop saves exposed brittle byte-comparison/default-property assumptions, not evidence of a rendering failure. Following owner approval, the checks were simplified to seven business-rule, reference and action-safety checks: no historical file equality, byte-size limits or frozen appearance/layout assertions. Single-selector scoping, target existence and action links remain checked; omitted false defaults are accepted.

The full current Python suite now records **107 tests passed, with 158 subtests passed**. A fresh temporary directory was required because the existing `.pytest_tmp` had a permissions error. Data-pipeline tests remain unchanged. See [validation scope](../05_Operations_and_Runbooks/VALIDATION.md). Passing these checks does not certify DAX-engine results, visual layout or rendered filter behaviour.

Limited read-only DAX checks recorded during the preceding journey work matched three provider-stage gate counts to their stage measures before the Desktop connection closed. This is **not** full DAX, report-render or end-to-end filter acceptance. No report/model files were changed by the documentation reassessment or subsequent test cleanup.

The current inventory and its assessment scope are recorded in [the semantic model catalogue](WMPP_Semantic_Model_Measures.md), [the requirement assessment](WMPP_REQUIREMENT_REASSESSMENT.md) and [the document review register](../06_Governance/DOCUMENT_REVIEW_REGISTER.md). Older dated sections remain historical evidence. Active ETL runbooks still govern pipeline operations; this reporting reassessment does not certify a fresh Fabric run.
