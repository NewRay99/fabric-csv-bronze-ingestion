# Latest KPI and measure calculations

Reviewed 19 October 2026 against WMPP_v16 and Mission Control. These definitions describe the saved models; refreshed results and client acceptance remain to be confirmed.

KPI Definition preserves its original A:H columns and Date Added in I. Its 567 existing records remain unchanged; four provider-scoped document aggregations are registered as GOLD-KPI-327–330 on 18 October. These reuse existing expiry logic and do not establish additional accepted KPI scope. Helper flags and presentation measures are classified separately.

## Source snapshots

| Model | Tables | Measures including helpers | Pages |
| --- | ---: | ---: | ---: |
| business | 73 | 502 | 35 |
| mission | 34 | 351 | 17 |

## KPI registration and helper classification

| Model | Measure | Classification | KPI IDs |
|---|---|---|---|
| business | [Accepted Offer to IPA Conversion %](#business-accepted-offer-to-ipa-conversion-percent) | Business metric | KPI-83 |
| business | [Accepted Offers](#business-accepted-offers) | Business metric | KPI-39, KPI-75 |
| business | [Accepted Offers Linked to IPA %](#business-accepted-offers-linked-to-ipa-percent) | Business metric | GOLD-KPI-145 |
| business | [Accepted Offers With IPA](#business-accepted-offers-with-ipa) | Business metric | GOLD-KPI-099 |
| business | [Active Awaiting Offers With Engagement](#business-active-awaiting-offers-with-engagement) | Business metric | KPI-21 |
| business | [Active Awaiting Offers Without Engagement](#business-active-awaiting-offers-without-engagement) | Business metric | KPI-22 |
| business | [Active IPAs](#business-active-ipas) | Business metric | GOLD-KPI-022 |
| business | [Active Provider Response Rate at Snapshot](#business-active-provider-response-rate-at-snapshot) | Business metric | GOLD-KPI-146 |
| business | [Active Referral Engagement Rate](#business-active-referral-engagement-rate) | Business metric | KPI-20 |
| business | [Active Referral Engagement Rate MoM %](#business-active-referral-engagement-rate-mom-percent) | Business metric | GOLD-KPI-147 |
| business | [Active Referral Engagement Rate Previous Month](#business-active-referral-engagement-rate-previous-month) | Business metric | GOLD-KPI-148 |
| business | [Active Referral Engagement Rate Variance](#business-active-referral-engagement-rate-variance) | Business metric | GOLD-KPI-149 |
| business | [Active Referral Engagement Rate Variance Indicator](#business-active-referral-engagement-rate-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Active Referral Engagement Rate Variance Indicator Color](#business-active-referral-engagement-rate-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Active Referrals Awaiting Offers Previous Month](#business-active-referrals-awaiting-offers-previous-month) | Business metric | GOLD-KPI-151 |
| business | [Active Referrals Awaiting Offers Variance](#business-active-referrals-awaiting-offers-variance) | Business metric | GOLD-KPI-152 |
| business | [Active Referrals Awaiting Offers Variance Indicator](#business-active-referrals-awaiting-offers-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Active Referrals Awaiting Offers Variance Indicator Color](#business-active-referrals-awaiting-offers-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Active Referrals Awaiting Offers at Snapshot](#business-active-referrals-awaiting-offers-at-snapshot) | Business metric | GOLD-KPI-150 |
| business | [Active Referrals Under Offer Indicator](#business-active-referrals-under-offer-indicator) | Display/filter helper | Helper/context only |
| business | [Active Referrals Under Offer Previous Month](#business-active-referrals-under-offer-previous-month) | Business metric | GOLD-KPI-154 |
| business | [Active Referrals Under Offer Variance](#business-active-referrals-under-offer-variance) | Business metric | GOLD-KPI-155 |
| business | [Active Referrals Under Offer Variance Indicator Color](#business-active-referrals-under-offer-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Active Referrals Under Offer at Snapshot](#business-active-referrals-under-offer-at-snapshot) | Business metric | GOLD-KPI-153 |
| business | [Active Referrals With Provider Engagement](#business-active-referrals-with-provider-engagement) | Business metric | KPI-19 |
| business | [Active Referrals With Provider Response at Snapshot](#business-active-referrals-with-provider-response-at-snapshot) | Business metric | GOLD-KPI-156 |
| business | [Average Active IPA Weekly Cost](#business-average-active-ipa-weekly-cost) | Business metric | GOLD-KPI-097 |
| business | [Average Days Early](#business-average-days-early) | Business metric | GOLD-KPI-157 |
| business | [Average Days in Draft](#business-average-days-in-draft) | Business metric | KPI-59 |
| business | [Average Estimated Weekly Cost — Confirmed Referrals](#business-average-estimated-weekly-cost-confirmed-referrals) | Business metric | GOLD-KPI-024 |
| business | [Average Lifecycle Events per Referral](#business-average-lifecycle-events-per-referral) | Business metric | GOLD-KPI-107 |
| business | [Average Offers per Provider](#business-average-offers-per-provider) | Business metric | GOLD-KPI-057 |
| business | [Average Offers per Provider - Under Offer](#business-average-offers-per-provider-under-offer) | Business metric | GOLD-KPI-158 |
| business | [Average Offers per Referral](#business-average-offers-per-referral) | Business metric | GOLD-KPI-018 |
| business | [Average Offers per Referral Under Offer](#business-average-offers-per-referral-under-offer) | Business metric | KPI-13 |
| business | [Avg Offers per Provider (Under Offer)](#business-avg-offers-per-provider-under-offer) | Business metric | KPI-14 |
| business | [Awaiting offer](#business-awaiting-offer) | Business metric | GOLD-KPI-159 |
| business | [Category-aware open referrals](#business-category-aware-open-referrals) | Business metric | GOLD-KPI-160 |
| business | [Closed IPAs](#business-closed-ipas) | Business metric | GOLD-KPI-096 |
| business | [Closed Referrals](#business-closed-referrals) | Business metric | GOLD-KPI-003 |
| business | [Closed Referrals MoM %](#business-closed-referrals-mom-percent) | Business metric | GOLD-KPI-165 |
| business | [Closed Referrals Previous Month](#business-closed-referrals-previous-month) | Business metric | GOLD-KPI-166 |
| business | [Closed Referrals Variance](#business-closed-referrals-variance) | Business metric | GOLD-KPI-167 |
| business | [Closed Referrals Variance Indicator](#business-closed-referrals-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Closed Referrals Variance Indicator Color](#business-closed-referrals-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Closed Referrals at Snapshot](#business-closed-referrals-at-snapshot) | Business metric | GOLD-KPI-030 |
| business | [Closed or Cancelled Referrals](#business-closed-or-cancelled-referrals) | Business metric | KPI-31 |
| business | [Closed or Cancelled Referrals MoM %](#business-closed-or-cancelled-referrals-mom-percent) | Business metric | GOLD-KPI-162 |
| business | [Closed or Cancelled Referrals Previous Month](#business-closed-or-cancelled-referrals-previous-month) | Business metric | GOLD-KPI-163 |
| business | [Closed or Cancelled Referrals Variance](#business-closed-or-cancelled-referrals-variance) | Business metric | GOLD-KPI-164 |
| business | [Closed or Cancelled Referrals Variance Indicator](#business-closed-or-cancelled-referrals-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Closed or Cancelled Referrals Variance Indicator Color](#business-closed-or-cancelled-referrals-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Closed or Cancelled Referrals at Snapshot](#business-closed-or-cancelled-referrals-at-snapshot) | Business metric | GOLD-KPI-161 |
| business | [Cohort Placement Within Window](#business-cohort-placement-within-window) | Business metric | GOLD-KPI-168 |
| business | [Completed IPAs](#business-completed-ipas) | Business metric | GOLD-KPI-169 |
| business | [Connection city](#business-connection-city) | Display/filter/context helper | Helper/context only |
| business | [Connection endpoint](#business-connection-endpoint) | Display/filter/context helper | Helper/context only |
| business | [Connection home](#business-connection-home) | Display/filter/context helper | Helper/context only |
| business | [Connection offer status](#business-connection-offer-status) | Display/filter/context helper | Helper/context only |
| business | [Connection postcode](#business-connection-postcode) | Display/filter/context helper | Helper/context only |
| business | [Connection provider](#business-connection-provider) | Display/filter/context helper | Helper/context only |
| business | [Connection quality](#business-connection-quality) | Display/filter/context helper | Helper/context only |
| business | [Connection referral](#business-connection-referral) | Display/filter/context helper | Helper/context only |
| business | [Connection straight-line km](#business-connection-straight-line-km) | Business metric | GOLD-KPI-170 |
| business | [Critical Overdue Referrals](#business-critical-overdue-referrals) | Business metric | GOLD-KPI-144 |
| business | [Critical Target Hit Rate](#business-critical-target-hit-rate) | Business metric | GOLD-KPI-171 |
| business | [Current Referral As Of](#business-current-referral-as-of) | Filter/context helper | Helper/context only |
| business | [Detail location matches offer](#business-detail-location-matches-offer) | Display/filter/context helper | Helper/context only |
| business | [Detail map points](#business-detail-map-points) | Business metric | GOLD-KPI-172 |
| business | [Detail referral selected](#business-detail-referral-selected) | Display/filter/context helper | Helper/context only |
| business | [Directory Summary Count](#business-directory-summary-count) | Business metric | KPI-48 |
| business | [Document expiry status](#business-document-expiry-status) | Display/filter helper | Helper/context only |
| business | [Documents Expired](#business-documents-expired) | Business metric | KPI-101 |
| business | [Documents Expiring Next 30 Days](#business-documents-expiring-next-30-days) | Business metric | KPI-100 |
| business | [Draft No Activity Since Creation (Under Offer Referrals)](#business-draft-no-activity-since-creation-under-offer-referrals) | Business metric | GOLD-KPI-173 |
| business | [Draft Offer Count (Under Offer Referrals)](#business-draft-offer-count-under-offer-referrals) | Business metric | GOLD-KPI-174 |
| business | [Draft Offers Missing Dates](#business-draft-offers-missing-dates) | Business metric | KPI-55 |
| business | [Draft Offers Stalled 14+ Days](#business-draft-offers-stalled-14-days) | Business metric | GOLD-KPI-066 |
| business | [Draft Offers Stalled 14+ Days - Under Offer Referrals](#business-draft-offers-stalled-14-days-under-offer-referrals) | Business metric | GOLD-KPI-175 |
| business | [Draft Offers Stalled 7+ Days](#business-draft-offers-stalled-7-days) | Business metric | GOLD-KPI-020 |
| business | [Draft Offers With Activity Since Creation](#business-draft-offers-with-activity-since-creation) | Business metric | KPI-56, KPI-54 |
| business | [Draft Offers With No Activity %](#business-draft-offers-with-no-activity-percent) | Business metric | KPI-62 |
| business | [Draft Offers With No Activity - Under Offer Referrals](#business-draft-offers-with-no-activity-under-offer-referrals) | Business metric | GOLD-KPI-176 |
| business | [Draft Offers With No Activity Since Creation](#business-draft-offers-with-no-activity-since-creation) | Business metric | KPI-53 |
| business | [Draft Offers on Referrals Under Offer](#business-draft-offers-on-referrals-under-offer) | Business metric | KPI-17 |
| business | [Drafts No Activity 14+ Days](#business-drafts-no-activity-14-days) | Business metric | KPI-58, KPI-63 |
| business | [Drafts No Activity 14+ Days (Under Offer Referrals)](#business-drafts-no-activity-14-days-under-offer-referrals) | Business metric | GOLD-KPI-177 |
| business | [Drafts With No Activity Since Creation (Under Offer) %](#business-drafts-with-no-activity-since-creation-under-offer-percent) | Business metric | GOLD-KPI-178 |
| business | [Emergency Placement Rate](#business-emergency-placement-rate) | Business metric | KPI-92  |
| business | [Emergency Referrals](#business-emergency-referrals) | Business metric | KPI-91  |
| business | [Estimated Active Weekly Cost](#business-estimated-active-weekly-cost) | Business metric | KPI-107 |
| business | [Explorer Gold accepted offers](#business-explorer-gold-accepted-offers) | Business metric | GOLD-KPI-179 |
| business | [Explorer Gold average response minutes](#business-explorer-gold-average-response-minutes) | Business metric | GOLD-KPI-180 |
| business | [Explorer Gold median response minutes](#business-explorer-gold-median-response-minutes) | Business metric | GOLD-KPI-181 |
| business | [Explorer Gold offer acceptance rate](#business-explorer-gold-offer-acceptance-rate) | Business metric | GOLD-KPI-182 |
| business | [Explorer Gold offers](#business-explorer-gold-offers) | Business metric | GOLD-KPI-183 |
| business | [Explorer Gold opportunities](#business-explorer-gold-opportunities) | Business metric | GOLD-KPI-184 |
| business | [Explorer Gold placed by target](#business-explorer-gold-placed-by-target) | Business metric | GOLD-KPI-185 |
| business | [Explorer Gold response rate](#business-explorer-gold-response-rate) | Business metric | GOLD-KPI-186 |
| business | [Explorer Gold responses](#business-explorer-gold-responses) | Business metric | GOLD-KPI-187 |
| business | [Explorer Gold successful referrals](#business-explorer-gold-successful-referrals) | Business metric | GOLD-KPI-188 |
| business | [Explorer Gold target placement rate](#business-explorer-gold-target-placement-rate) | Business metric | GOLD-KPI-189 |
| business | [Explorer provider IPAs](#business-explorer-provider-ipas) | Business metric | GOLD-KPI-198 |
| business | [Explorer provider accepted offers](#business-explorer-provider-accepted-offers) | Business metric | GOLD-KPI-190 |
| business | [Explorer provider assigned referrals](#business-explorer-provider-assigned-referrals) | Business metric | GOLD-KPI-191 |
| business | [Explorer provider assignment row visible](#business-explorer-provider-assignment-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer provider assignment table title](#business-explorer-provider-assignment-table-title) | Filter/context helper | Helper/context only |
| business | [Explorer provider assignments](#business-explorer-provider-assignments) | Business metric | GOLD-KPI-192 |
| business | [Explorer provider average response minutes](#business-explorer-provider-average-response-minutes) | Business metric | GOLD-KPI-193 |
| business | [Explorer provider beds](#business-explorer-provider-beds) | Business metric | GOLD-KPI-194 |
| business | [Explorer provider completed IPAs](#business-explorer-provider-completed-ipas) | Business metric | GOLD-KPI-195 |
| business | [Explorer provider documents](#business-explorer-provider-documents) | Business metric | GOLD-KPI-327 |
| business | [Explorer provider documents expired](#business-explorer-provider-documents-expired) | Business metric | GOLD-KPI-328 |
| business | [Explorer provider documents expiring 30 days](#business-explorer-provider-documents-expiring-30-days) | Business metric | GOLD-KPI-329 |
| business | [Explorer provider drafts](#business-explorer-provider-drafts) | Business metric | GOLD-KPI-196 |
| business | [Explorer provider homes](#business-explorer-provider-homes) | Business metric | GOLD-KPI-197 |
| business | [Explorer provider homes with expired documents](#business-explorer-provider-homes-with-expired-documents) | Business metric | GOLD-KPI-330 |
| business | [Explorer provider median response minutes](#business-explorer-provider-median-response-minutes) | Business metric | GOLD-KPI-199 |
| business | [Explorer provider message row visible](#business-explorer-provider-message-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer provider messages](#business-explorer-provider-messages) | Business metric | GOLD-KPI-200 |
| business | [Explorer provider monthly row visible](#business-explorer-provider-monthly-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer provider offer acceptance rate](#business-explorer-provider-offer-acceptance-rate) | Business metric | GOLD-KPI-201 |
| business | [Explorer provider offer row visible](#business-explorer-provider-offer-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer provider offer table title](#business-explorer-provider-offer-table-title) | Filter/context helper | Helper/context only |
| business | [Explorer provider offers](#business-explorer-provider-offers) | Business metric | GOLD-KPI-202 |
| business | [Explorer provider offers made](#business-explorer-provider-offers-made) | Business metric | GOLD-KPI-203 |
| business | [Explorer provider pending offers](#business-explorer-provider-pending-offers) | Business metric | GOLD-KPI-204 |
| business | [Explorer provider qualifying responses](#business-explorer-provider-qualifying-responses) | Business metric | GOLD-KPI-205 |
| business | [Explorer provider response rate](#business-explorer-provider-response-rate) | Business metric | GOLD-KPI-206 |
| business | [Explorer provider row visible](#business-explorer-provider-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer provider signed IPAs](#business-explorer-provider-signed-ipas) | Business metric | GOLD-KPI-207 |
| business | [Explorer providers](#business-explorer-providers) | Business metric | GOLD-KPI-208 |
| business | [Explorer providers without offers](#business-explorer-providers-without-offers) | Business metric | GOLD-KPI-209 |
| business | [Explorer referral IPAs](#business-explorer-referral-ipas) | Business metric | GOLD-KPI-213 |
| business | [Explorer referral accepted offers](#business-explorer-referral-accepted-offers) | Business metric | GOLD-KPI-210 |
| business | [Explorer referral assignments](#business-explorer-referral-assignments) | Business metric | GOLD-KPI-211 |
| business | [Explorer referral completed IPAs](#business-explorer-referral-completed-ipas) | Business metric | GOLD-KPI-212 |
| business | [Explorer referral messages](#business-explorer-referral-messages) | Business metric | GOLD-KPI-214 |
| business | [Explorer referral offer coverage](#business-explorer-referral-offer-coverage) | Business metric | GOLD-KPI-215 |
| business | [Explorer referral offers](#business-explorer-referral-offers) | Business metric | GOLD-KPI-216 |
| business | [Explorer referral row visible](#business-explorer-referral-row-visible) | Filter/context helper | Helper/context only |
| business | [Explorer referrals](#business-explorer-referrals) | Business metric | GOLD-KPI-217 |
| business | [Explorer referrals closed](#business-explorer-referrals-closed) | Business metric | GOLD-KPI-218 |
| business | [Explorer referrals open](#business-explorer-referrals-open) | Business metric | GOLD-KPI-219 |
| business | [Explorer referrals open overdue](#business-explorer-referrals-open-overdue) | Business metric | GOLD-KPI-220 |
| business | [Explorer referrals with offers](#business-explorer-referrals-with-offers) | Business metric | GOLD-KPI-221 |
| business | [Explorer referrals without offers](#business-explorer-referrals-without-offers) | Business metric | GOLD-KPI-222 |
| business | [Female Referrals](#business-female-referrals) | Business metric | KPI-05, GOLD-KPI-111 |
| business | [Fostering Homes](#business-fostering-homes) | Business metric | GOLD-KPI-083 |
| business | [Framework Offers (Under Offer Referrals)](#business-framework-offers-under-offer-referrals) | Business metric | KPI-38 |
| business | [Framework Offers on Referrals Under Offer](#business-framework-offers-on-referrals-under-offer) | Business metric | GOLD-KPI-223 |
| business | [Framework Providers](#business-framework-providers) | Business metric | KPI-45 |
| business | [Gold Model Last Refreshed](#business-gold-model-last-refreshed) | Business metric | KPI-87 |
| business | [Homes Offered](#business-homes-offered) | Business metric | GOLD-KPI-143 |
| business | [IPA Complete referral](#business-ipa-complete-referral) | Filter/context helper | Helper/context only |
| business | [IPA Completed](#business-ipa-completed) | Business metric | KPI-77, GOLD-KPI-114 |
| business | [IPA Created to Completion %](#business-ipa-created-to-completion-percent) | Business metric | KPI-85 |
| business | [IPA Exists](#business-ipa-exists) | Display/filter helper | KPI-73 |
| business | [IPA Signature Completion Rate](#business-ipa-signature-completion-rate) | Business metric | KPI-114 |
| business | [IPA Signature Pending Rate](#business-ipa-signature-pending-rate) | Business metric | GOLD-KPI-224 |
| business | [IPAs Created](#business-ipas-created) | Business metric | KPI-76 |
| business | [IPAs Issued This Month](#business-ipas-issued-this-month) | Business metric | GOLD-KPI-095 |
| business | [IPAs Pending Completion](#business-ipas-pending-completion) | Business metric | KPI-78, GOLD-KPI-115 |
| business | [IPAs Signed by Local Authority](#business-ipas-signed-by-local-authority) | Business metric | GOLD-KPI-117 |
| business | [IPAs Signed by Provider](#business-ipas-signed-by-provider) | Business metric | GOLD-KPI-116 |
| business | [Is Awaiting IPA Creation](#business-is-awaiting-ipa-creation) | Display/filter helper | KPI-81 |
| business | [Is IPA Completed](#business-is-ipa-completed) | Display/filter helper | KPI-82 |
| business | [Is IPA Pending](#business-is-ipa-pending) | Display/filter helper | KPI-80 |
| business | [Is In Accepted KPI](#business-is-in-accepted-kpi) | Display/filter helper | KPI-74 |
| business | [Is Non Framework Provider](#business-is-non-framework-provider) | Display/filter helper | KPI-47 |
| business | [Journey current position](#business-journey-current-position) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 1](#business-journey-detail-colour-1) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 2](#business-journey-detail-colour-2) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 3](#business-journey-detail-colour-3) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 4](#business-journey-detail-colour-4) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 5](#business-journey-detail-colour-5) | Display/filter helper | Helper/context only |
| business | [Journey detail colour 6](#business-journey-detail-colour-6) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 1](#business-journey-detail-evidence-1) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 2](#business-journey-detail-evidence-2) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 3](#business-journey-detail-evidence-3) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 4](#business-journey-detail-evidence-4) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 5](#business-journey-detail-evidence-5) | Display/filter helper | Helper/context only |
| business | [Journey detail evidence 6](#business-journey-detail-evidence-6) | Display/filter helper | Helper/context only |
| business | [Journey detail label 1](#business-journey-detail-label-1) | Display/filter helper | Helper/context only |
| business | [Journey detail label 2](#business-journey-detail-label-2) | Display/filter helper | Helper/context only |
| business | [Journey detail label 3](#business-journey-detail-label-3) | Display/filter helper | Helper/context only |
| business | [Journey detail label 4](#business-journey-detail-label-4) | Display/filter helper | Helper/context only |
| business | [Journey detail label 5](#business-journey-detail-label-5) | Display/filter helper | Helper/context only |
| business | [Journey detail label 6](#business-journey-detail-label-6) | Display/filter helper | Helper/context only |
| business | [Journey next action](#business-journey-next-action) | Display/filter helper | Helper/context only |
| business | [Journey provider coverage](#business-journey-provider-coverage) | Display/filter helper | Helper/context only |
| business | [Journey provider label](#business-journey-provider-label) | Display/filter helper | Helper/context only |
| business | [Journey provider stage](#business-journey-provider-stage) | Display/filter helper | Helper/context only |
| business | [Journey providers 0](#business-journey-providers-0) | Business metric | GOLD-KPI-131 |
| business | [Journey providers 1](#business-journey-providers-1) | Business metric | GOLD-KPI-132 |
| business | [Journey providers 2](#business-journey-providers-2) | Business metric | GOLD-KPI-133 |
| business | [Journey providers 3](#business-journey-providers-3) | Business metric | GOLD-KPI-134 |
| business | [Journey providers 4](#business-journey-providers-4) | Display/filter helper | Helper/context only |
| business | [Journey providers 5](#business-journey-providers-5) | Business metric | GOLD-KPI-135 |
| business | [Journey providers both signed](#business-journey-providers-both-signed) | Display/filter helper | GOLD-KPI-136 |
| business | [Journey referral exceptions](#business-journey-referral-exceptions) | Display/filter helper | Helper/context only |
| business | [Journey referral reconciliation](#business-journey-referral-reconciliation) | Business metric | GOLD-KPI-225 |
| business | [Journey referrals 1](#business-journey-referrals-1) | Business metric | GOLD-KPI-123 |
| business | [Journey referrals 2](#business-journey-referrals-2) | Business metric | GOLD-KPI-124 |
| business | [Journey referrals 3](#business-journey-referrals-3) | Business metric | GOLD-KPI-125 |
| business | [Journey referrals 4](#business-journey-referrals-4) | Business metric | GOLD-KPI-126 |
| business | [Journey referrals 5](#business-journey-referrals-5) | Business metric | GOLD-KPI-127 |
| business | [Journey referrals 6](#business-journey-referrals-6) | Business metric | GOLD-KPI-128 |
| business | [Journey referrals 7](#business-journey-referrals-7) | Business metric | GOLD-KPI-129 |
| business | [Journey referrals 8](#business-journey-referrals-8) | Business metric | GOLD-KPI-130 |
| business | [Journey selected stage](#business-journey-selected-stage) | Display/filter helper | Helper/context only |
| business | [KPI Tooltip Style 1](#business-kpi-tooltip-style-1) | Display/filter helper | Helper/context only |
| business | [KPIs catalogued](#business-kpis-catalogued) | Business metric | GOLD-KPI-226 |
| business | [Last Snapshot Date](#business-last-snapshot-date) | Business metric | GOLD-KPI-227 |
| business | [Latest Offer Source Export](#business-latest-offer-source-export) | Business metric | KPI-88 |
| business | [Lifetime Placement Cost](#business-lifetime-placement-cost) | Business metric | GOLD-KPI-228 |
| business | [Linked assignment count](#business-linked-assignment-count) | Business metric | GOLD-KPI-229 |
| business | [Linked debug](#business-linked-debug) | Display/filter helper | Helper/context only |
| business | [Linked latest message](#business-linked-latest-message) | Display/filter helper | Helper/context only |
| business | [Linked message count](#business-linked-message-count) | Business metric | GOLD-KPI-230 |
| business | [Linked offer count](#business-linked-offer-count) | Business metric | GOLD-KPI-231 |
| business | [Linked offer statuses](#business-linked-offer-statuses) | Display/filter helper | Helper/context only |
| business | [Linked provider row visible](#business-linked-provider-row-visible) | Display/filter helper | Helper/context only |
| business | [Linked providers in selection](#business-linked-providers-in-selection) | Business metric | GOLD-KPI-232 |
| business | [Linked response statuses](#business-linked-response-statuses) | Display/filter helper | Helper/context only |
| business | [Location review](#business-location-review) | Business metric | GOLD-KPI-233 |
| business | [Male Referrals](#business-male-referrals) | Business metric | KPI-04, GOLD-KPI-110 |
| business | [Map connection summary](#business-map-connection-summary) | Display/filter/context helper | Helper/context only |
| business | [Map connection visible](#business-map-connection-visible) | Display/filter/context helper | Helper/context only |
| business | [Mapped referrals](#business-mapped-referrals) | Business metric | GOLD-KPI-234 |
| business | [Matching referrals](#business-matching-referrals) | Business metric | GOLD-KPI-122 |
| business | [Median Days to First Action](#business-median-days-to-first-action) | Business metric | GOLD-KPI-010 |
| business | [Median Days to First Offer](#business-median-days-to-first-offer) | Business metric | GOLD-KPI-011 |
| business | [Median Days to IPA](#business-median-days-to-ipa) | Business metric | GOLD-KPI-012 |
| business | [Median Offered Weekly Cost](#business-median-offered-weekly-cost) | Business metric | GOLD-KPI-235 |
| business | [Median preferred-city distance km](#business-median-preferred-city-distance-km) | Business metric | GOLD-KPI-142 |
| business | [No. Providers Who Made Offers](#business-no-providers-who-made-offers) | Business metric | GOLD-KPI-236 |
| business | [Non-Draft Offers](#business-non-draft-offers) | Business metric | KPI-25, KPI-12 |
| business | [Non-Framework Providers](#business-non-framework-providers) | Business metric | KPI-46 |
| business | [Non-Spot Offers](#business-non-spot-offers) | Business metric | GOLD-KPI-061 |
| business | [Offer Acceptance Rate](#business-offer-acceptance-rate) | Business metric | GOLD-KPI-017 |
| business | [Offer Journey Count](#business-offer-journey-count) | Filter/context helper | Helper/context only |
| business | [Offer Receipt Rate (Created in Period)](#business-offer-receipt-rate-created-in-period) | Business metric | GOLD-KPI-237 |
| business | [Offer Receipt Rate (Created in Period) MoM %](#business-offer-receipt-rate-created-in-period-mom-percent) | Business metric | GOLD-KPI-238 |
| business | [Offer Receipt Rate (Created in Period) Previous Month](#business-offer-receipt-rate-created-in-period-previous-month) | Business metric | GOLD-KPI-239 |
| business | [Offer Receipt Rate (Created in Period) Variance](#business-offer-receipt-rate-created-in-period-variance) | Business metric | GOLD-KPI-240 |
| business | [Offer Receipt Rate (Created in Period) Variance Indicator](#business-offer-receipt-rate-created-in-period-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Offer Receipt Rate (Created in Period) Variance Indicator Color](#business-offer-receipt-rate-created-in-period-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Offers](#business-offers) | Business metric | GOLD-KPI-241 |
| business | [Offers Awaiting IPA Completion %](#business-offers-awaiting-ipa-completion-percent) | Business metric | GOLD-KPI-242 |
| business | [Offers Awaiting IPA Creation](#business-offers-awaiting-ipa-creation) | Business metric | KPI-79 |
| business | [Offers Still to Progress to IPA %](#business-offers-still-to-progress-to-ipa-percent) | Business metric | KPI-84 |
| business | [Offers Submitted](#business-offers-submitted) | Business metric | KPI-28 |
| business | [Offers With Recorded Rejection Reason](#business-offers-with-recorded-rejection-reason) | Business metric | GOLD-KPI-055 |
| business | [Offers in Draft](#business-offers-in-draft) | Business metric | KPI-61 |
| business | [Offers on Referrals Under Offer](#business-offers-on-referrals-under-offer) | Business metric | KPI-35 |
| business | [Offers on Referrals Under Offer MoM %](#business-offers-on-referrals-under-offer-mom-percent) | Business metric | GOLD-KPI-243 |
| business | [Offers on Referrals Under Offer Previous Month](#business-offers-on-referrals-under-offer-previous-month) | Business metric | GOLD-KPI-244 |
| business | [Offers on Referrals Under Offer Variance](#business-offers-on-referrals-under-offer-variance) | Business metric | GOLD-KPI-245 |
| business | [Offers on Referrals Under Offer Variance Indicator](#business-offers-on-referrals-under-offer-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Offers on Referrals Under Offer Variance Indicator Color](#business-offers-on-referrals-under-offer-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Offers per Provider (Under Offer Referrals)](#business-offers-per-provider-under-offer-referrals) | Business metric | KPI-37 |
| business | [Offers with a Decision](#business-offers-with-a-decision) | Business metric | GOLD-KPI-016 |
| business | [Offers with preferred-city distance](#business-offers-with-preferred-city-distance) | Business metric | GOLD-KPI-246 |
| business | [Offers without preferred-city distance](#business-offers-without-preferred-city-distance) | Business metric | GOLD-KPI-247 |
| business | [Oldest Draft Age Days](#business-oldest-draft-age-days) | Business metric | KPI-60 |
| business | [Open On-Track Referrals at Snapshot](#business-open-on-track-referrals-at-snapshot) | Business metric | GOLD-KPI-033 |
| business | [Open Overdue Referrals](#business-open-overdue-referrals) | Business metric | GOLD-KPI-007 |
| business | [Open Overdue Referrals at Snapshot](#business-open-overdue-referrals-at-snapshot) | Business metric | GOLD-KPI-032 |
| business | [Open Referral Rate at Snapshot](#business-open-referral-rate-at-snapshot) | Business metric | GOLD-KPI-034 |
| business | [Open Referrals](#business-open-referrals) | Business metric | KPI-08 |
| business | [Open Referrals Due in 3 Days](#business-open-referrals-due-in-3-days) | Business metric | GOLD-KPI-251 |
| business | [Open Referrals MoM %](#business-open-referrals-mom-percent) | Business metric | GOLD-KPI-252 |
| business | [Open Referrals Previous Month](#business-open-referrals-previous-month) | Business metric | GOLD-KPI-253 |
| business | [Open Referrals Stalled 7+ Days](#business-open-referrals-stalled-7-days) | Business metric | GOLD-KPI-013 |
| business | [Open Referrals Variance](#business-open-referrals-variance) | Business metric | GOLD-KPI-254 |
| business | [Open Referrals Variance Indicator](#business-open-referrals-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Open Referrals Variance Indicator Color](#business-open-referrals-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Open Referrals at Snapshot](#business-open-referrals-at-snapshot) | Business metric | GOLD-KPI-029 |
| business | [Open Referrals by Age](#business-open-referrals-by-age) | Business metric | GOLD-KPI-248 |
| business | [Open Referrals by Days to Target](#business-open-referrals-by-days-to-target) | Business metric | GOLD-KPI-249 |
| business | [Open Referrals by Target Status](#business-open-referrals-by-target-status) | Business metric | GOLD-KPI-250 |
| business | [Other Gender Referrals](#business-other-gender-referrals) | Business metric | KPI-06, GOLD-KPI-112 |
| business | [Other Referrals](#business-other-referrals) | Business metric | GOLD-KPI-255 |
| business | [Pending Offers](#business-pending-offers) | Business metric | GOLD-KPI-053 |
| business | [Pending Offers (Under Offer Referrals)](#business-pending-offers-under-offer-referrals) | Business metric | KPI-18 |
| business | [Pending Offers 0-7 Days](#business-pending-offers-0-7-days) | Business metric | KPI-67 |
| business | [Pending Offers 15-29 Days](#business-pending-offers-15-29-days) | Business metric | GOLD-KPI-072 |
| business | [Pending Offers 15–30 Days](#business-pending-offers-15-30-days) | Business metric | KPI-71, KPI-65 |
| business | [Pending Offers 30+ Days](#business-pending-offers-30-days) | Business metric | KPI-72, KPI-66 |
| business | [Pending Offers 8-14 Days](#business-pending-offers-8-14-days) | Business metric | KPI-70, KPI-68 |
| business | [Pending Offers Missing or Future Date](#business-pending-offers-missing-or-future-date) | Business metric | GOLD-KPI-256 |
| business | [Pending Offers on Referrals Under Offer](#business-pending-offers-on-referrals-under-offer) | Business metric | GOLD-KPI-257 |
| business | [Placement Rate at Snapshot](#business-placement-rate-at-snapshot) | Business metric | GOLD-KPI-035 |
| business | [Placement Target Hit Rate](#business-placement-target-hit-rate) | Business metric | GOLD-KPI-009 |
| business | [Planned Referrals](#business-planned-referrals) | Business metric | KPI-93  |
| business | [Preferred-city distance coverage](#business-preferred-city-distance-coverage) | Business metric | GOLD-KPI-141 |
| business | [Previous Snapshot Referrals](#business-previous-snapshot-referrals) | Business metric | GOLD-KPI-258 |
| business | [Provider Assignments](#business-provider-assignments) | Business metric | GOLD-KPI-025 |
| business | [Provider Average Response Hours](#business-provider-average-response-hours) | Business metric | GOLD-KPI-138 |
| business | [Provider Contact Referral](#business-provider-contact-referral) | Business metric | GOLD-KPI-259 |
| business | [Provider Contact Referral Indicator](#business-provider-contact-referral-indicator) | Display/filter helper | Helper/context only |
| business | [Provider Contact Referral Indicator Color](#business-provider-contact-referral-indicator-color) | Display/filter helper | Helper/context only |
| business | [Provider Contact Referral Previous Month](#business-provider-contact-referral-previous-month) | Business metric | GOLD-KPI-260 |
| business | [Provider Contact Referral Variance](#business-provider-contact-referral-variance) | Business metric | GOLD-KPI-261 |
| business | [Provider Contact Referrals MoM %](#business-provider-contact-referrals-mom-percent) | Business metric | GOLD-KPI-263 |
| business | [Provider Contact Referrals at Snapshot](#business-provider-contact-referrals-at-snapshot) | Business metric | GOLD-KPI-262 |
| business | [Provider Decline Rate](#business-provider-decline-rate) | Business metric | GOLD-KPI-027 |
| business | [Provider Declines](#business-provider-declines) | Business metric | GOLD-KPI-026 |
| business | [Provider Homes Registered](#business-provider-homes-registered) | Business metric | KPI-40 |
| business | [Provider Homes With Expired Documents](#business-provider-homes-with-expired-documents) | Business metric | GOLD-KPI-094 |
| business | [Provider Median Days to First Offer](#business-provider-median-days-to-first-offer) | Business metric | GOLD-KPI-268 |
| business | [Provider Messages Sent](#business-provider-messages-sent) | Business metric | KPI-110 |
| business | [Provider Offer Conversion Rate](#business-provider-offer-conversion-rate) | Business metric | GOLD-KPI-139 |
| business | [Provider Onboarding Success Rate](#business-provider-onboarding-success-rate) | Business metric | KPI-117 |
| business | [Provider QA flagged homes](#business-provider-qa-flagged-homes) | Business metric | GOLD-KPI-270 |
| business | [Provider Qualifying Responses](#business-provider-qualifying-responses) | Business metric | GOLD-KPI-271 |
| business | [Provider Response Opportunities](#business-provider-response-opportunities) | Business metric | GOLD-KPI-273 |
| business | [Provider Response Rate](#business-provider-response-rate) | Business metric | GOLD-KPI-137 |
| business | [Provider Submission Documents](#business-provider-submission-documents) | Business metric | GOLD-KPI-091 |
| business | [Provider Target Placement Rate](#business-provider-target-placement-rate) | Business metric | GOLD-KPI-140 |
| business | [Provider detail KPI value](#business-provider-detail-kpi-value) | Filter/context helper | Helper/context only |
| business | [Provider detail assignment rows](#business-provider-detail-assignment-rows) | Display/filter/context helper | Helper/context only |
| business | [Provider detail headline Explorer provider homes](#business-provider-detail-headline-explorer-provider-homes) | Display/context helper | Helper/context only |
| business | [Provider detail headline Explorer provider messages](#business-provider-detail-headline-explorer-provider-messages) | Display/context helper | Helper/context only |
| business | [Provider detail headline Explorer provider offers made](#business-provider-detail-headline-explorer-provider-offers-made) | Display/context helper | Helper/context only |
| business | [Provider detail headline Provider unanswered assignments](#business-provider-detail-headline-provider-unanswered-assignments) | Display/context helper | Helper/context only |
| business | [Provider detail home rows](#business-provider-detail-home-rows) | Display/filter/context helper | Helper/context only |
| business | [Provider detail message rows](#business-provider-detail-message-rows) | Display/filter/context helper | Helper/context only |
| business | [Provider detail offer rows](#business-provider-detail-offer-rows) | Display/filter/context helper | Helper/context only |
| business | [Provider detail profile rows](#business-provider-detail-profile-rows) | Display/filter/context helper | Helper/context only |
| business | [Provider detail scoring denominator](#business-provider-detail-scoring-denominator) | Display/context helper | Helper/context only |
| business | [Provider detail scoring evidence status](#business-provider-detail-scoring-evidence-status) | Display/context helper | Helper/context only |
| business | [Provider detail scoring numerator](#business-provider-detail-scoring-numerator) | Display/context helper | Helper/context only |
| business | [Provider detail scoring result](#business-provider-detail-scoring-result) | Display/context helper | Helper/context only |
| business | [Provider document row visible](#business-provider-document-row-visible) | Display/filter helper | Helper/context only |
| business | [Provider explorer KPI value](#business-provider-explorer-kpi-value) | Filter/context helper | Helper/context only |
| business | [Provider explorer matching homes](#business-provider-explorer-matching-homes) | Business metric | GOLD-KPI-264 |
| business | [Provider homes selected providers](#business-provider-homes-selected-providers) | Filter/context helper | Helper/context only |
| business | [Provider homes table accepted offers](#business-provider-homes-table-accepted-offers) | Business metric | GOLD-KPI-265 |
| business | [Provider homes table offers](#business-provider-homes-table-offers) | Business metric | GOLD-KPI-266 |
| business | [Provider homes table offers made](#business-provider-homes-table-offers-made) | Business metric | GOLD-KPI-267 |
| business | [Provider homes table row visible](#business-provider-homes-table-row-visible) | Filter/context helper | Helper/context only |
| business | [Provider homes table title](#business-provider-homes-table-title) | Filter/context helper | Helper/context only |
| business | [Provider matches offer status](#business-provider-matches-offer-status) | Filter/context helper | Helper/context only |
| business | [Provider no recorded activity](#business-provider-no-recorded-activity) | Business metric | GOLD-KPI-269 |
| business | [Provider response durations recorded](#business-provider-response-durations-recorded) | Business metric | GOLD-KPI-272 |
| business | [Provider response timing coverage](#business-provider-response-timing-coverage) | Business metric | GOLD-KPI-274 |
| business | [Provider scoring cohort months](#business-provider-scoring-cohort-months) | Display/context helper | Helper/context only |
| business | [Provider scoring denominator](#business-provider-scoring-denominator) | Display/context helper | Helper/context only |
| business | [Provider scoring evidence status](#business-provider-scoring-evidence-status) | Display/context helper | Helper/context only |
| business | [Provider scoring median response hours](#business-provider-scoring-median-response-hours) | Business metric | GOLD-KPI-275 |
| business | [Provider scoring numerator](#business-provider-scoring-numerator) | Display/context helper | Helper/context only |
| business | [Provider scoring qualifying responses](#business-provider-scoring-qualifying-responses) | Business metric | GOLD-KPI-276 |
| business | [Provider scoring result](#business-provider-scoring-result) | Display/context helper | Helper/context only |
| business | [Provider scoring timed responses](#business-provider-scoring-timed-responses) | Business metric | GOLD-KPI-277 |
| business | [Provider selection context](#business-provider-selection-context) | Display/context helper | Helper/context only |
| business | [Provider unanswered assignments](#business-provider-unanswered-assignments) | Business metric | GOLD-KPI-278 |
| business | [Providers - Fostering](#business-providers-fostering) | Business metric | KPI-51, KPI-42 |
| business | [Providers - Residential](#business-providers-residential) | Business metric | KPI-43 |
| business | [Providers - Supported Accommodation](#business-providers-supported-accommodation) | Business metric | KPI-44 |
| business | [Providers Approved](#business-providers-approved) | Business metric | KPI-104 |
| business | [Providers Pending Onboarding](#business-providers-pending-onboarding) | Business metric | KPI-104, KPI-116 |
| business | [Providers Registered](#business-providers-registered) | Business metric | KPI-41 |
| business | [Providers Who Made Offers](#business-providers-who-made-offers) | Business metric | KPI-11 |
| business | [Providers With Offers on Referrals Under Offer](#business-providers-with-offers-on-referrals-under-offer) | Business metric | GOLD-KPI-279 |
| business | [Providers With Pending Offers 30+ Days](#business-providers-with-pending-offers-30-days) | Business metric | KPI-69 |
| business | [Providers With QA Flags](#business-providers-with-qa-flags) | Business metric | KPI-97  |
| business | [QA Flagged Homes](#business-qa-flagged-homes) | Business metric | KPI-99  |
| business | [Rail activity caption](#business-rail-activity-caption) | Display/filter/context helper | Helper/context only |
| business | [Rail activity row visible](#business-rail-activity-row-visible) | Display/filter/context helper | Helper/context only |
| business | [Rail provider circle 1](#business-rail-provider-circle-1) | Display/filter/context helper | Helper/context only |
| business | [Rail provider circle 2](#business-rail-provider-circle-2) | Display/filter/context helper | Helper/context only |
| business | [Rail provider circle 3](#business-rail-provider-circle-3) | Display/filter/context helper | Helper/context only |
| business | [Rail provider circle 4](#business-rail-provider-circle-4) | Display/filter/context helper | Helper/context only |
| business | [Rail provider circle 5](#business-rail-provider-circle-5) | Display/filter/context helper | Helper/context only |
| business | [Rail provider cohort label](#business-rail-provider-cohort-label) | Display/filter/context helper | Helper/context only |
| business | [Rail provider row visible](#business-rail-provider-row-visible) | Display/filter/context helper | Helper/context only |
| business | [Rail provider selected metric](#business-rail-provider-selected-metric) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 1](#business-rail-referral-circle-1) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 2](#business-rail-referral-circle-2) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 3](#business-rail-referral-circle-3) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 4](#business-rail-referral-circle-4) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 5](#business-rail-referral-circle-5) | Display/filter/context helper | Helper/context only |
| business | [Rail referral circle 6](#business-rail-referral-circle-6) | Display/filter/context helper | Helper/context only |
| business | [Rail referral summary](#business-rail-referral-summary) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 1](#business-rail-referrals-1) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 2](#business-rail-referrals-2) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 3](#business-rail-referrals-3) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 4](#business-rail-referrals-4) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 5](#business-rail-referrals-5) | Display/filter/context helper | Helper/context only |
| business | [Rail referrals 6](#business-rail-referrals-6) | Display/filter/context helper | Helper/context only |
| business | [Referral IPAs awaiting signatures](#business-referral-ipas-awaiting-signatures) | Business metric | GOLD-KPI-281 |
| business | [Referral Lifecycle Events](#business-referral-lifecycle-events) | Business metric | KPI-113 |
| business | [Referral Volume Month on Month](#business-referral-volume-month-on-month) | Business metric | GOLD-KPI-038 |
| business | [Referral Volume Month on Month %](#business-referral-volume-month-on-month-percent) | Business metric | GOLD-KPI-039 |
| business | [Referral accepted without IPA](#business-referral-accepted-without-ipa) | Business metric | GOLD-KPI-280 |
| business | [Referral detail KPI value](#business-referral-detail-kpi-value) | Filter/context helper | Helper/context only |
| business | [Referral detail headline Explorer referral assignments](#business-referral-detail-headline-explorer-referral-assignments) | Display/context helper | Helper/context only |
| business | [Referral detail headline Explorer referral messages](#business-referral-detail-headline-explorer-referral-messages) | Display/context helper | Helper/context only |
| business | [Referral detail headline Explorer referral offers](#business-referral-detail-headline-explorer-referral-offers) | Display/context helper | Helper/context only |
| business | [Referral detail headline Referral IPAs awaiting signatures](#business-referral-detail-headline-referral-ipas-awaiting-signatures) | Display/context helper | Helper/context only |
| business | [Referral explorer KPI value](#business-referral-explorer-kpi-value) | Filter/context helper | Helper/context only |
| business | [Referral open overdue share](#business-referral-open-overdue-share) | Business metric | GOLD-KPI-282 |
| business | [Referral open without assignments](#business-referral-open-without-assignments) | Business metric | GOLD-KPI-283 |
| business | [Referral open without offers](#business-referral-open-without-offers) | Business metric | GOLD-KPI-284 |
| business | [Referral selection context](#business-referral-selection-context) | Display/context helper | Helper/context only |
| business | [Referrals](#business-referrals) | Business metric | GOLD-KPI-285 |
| business | [Referrals Awaiting Offer](#business-referrals-awaiting-offer) | Business metric | KPI-32, KPI-03 |
| business | [Referrals Awaiting Offer MoM %](#business-referrals-awaiting-offer-mom-percent) | Business metric | GOLD-KPI-286 |
| business | [Referrals Awaiting Offer Previous Month](#business-referrals-awaiting-offer-previous-month) | Business metric | GOLD-KPI-287 |
| business | [Referrals Awaiting Offer Variance](#business-referrals-awaiting-offer-variance) | Business metric | GOLD-KPI-288 |
| business | [Referrals Awaiting Offer Variance Indicator](#business-referrals-awaiting-offer-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Referrals Awaiting Offer Variance Indicator Color](#business-referrals-awaiting-offer-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Referrals Cancelled/Closed Indicator](#business-referrals-cancelled-closed-indicator) | Display/filter helper | Helper/context only |
| business | [Referrals Cancelled/Closed Previous Month](#business-referrals-cancelled-closed-previous-month) | Business metric | GOLD-KPI-289 |
| business | [Referrals Cancelled/Closed Variance](#business-referrals-cancelled-closed-variance) | Business metric | GOLD-KPI-290 |
| business | [Referrals Created Previous Month](#business-referrals-created-previous-month) | Business metric | GOLD-KPI-037 |
| business | [Referrals Created This Financial Year](#business-referrals-created-this-financial-year) | Business metric | KPI-24 |
| business | [Referrals Created This Month](#business-referrals-created-this-month) | Business metric | KPI-23 |
| business | [Referrals Currently Active](#business-referrals-currently-active) | Business metric | KPI-29 |
| business | [Referrals Currently Active MoM %](#business-referrals-currently-active-mom-percent) | Business metric | GOLD-KPI-291 |
| business | [Referrals Currently Active Previous Month](#business-referrals-currently-active-previous-month) | Business metric | GOLD-KPI-292 |
| business | [Referrals Currently Active Variance](#business-referrals-currently-active-variance) | Business metric | GOLD-KPI-293 |
| business | [Referrals Currently Active Variance Indicator](#business-referrals-currently-active-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Referrals Currently Active Variance Indicator Color](#business-referrals-currently-active-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Referrals Due This As Of Month](#business-referrals-due-this-as-of-month) | Business metric | GOLD-KPI-295 |
| business | [Referrals Due in Reporting Period](#business-referrals-due-in-reporting-period) | Business metric | GOLD-KPI-294 |
| business | [Referrals Not Yet Closed](#business-referrals-not-yet-closed) | Business metric | GOLD-KPI-296 |
| business | [Referrals Placed by Required Date](#business-referrals-placed-by-required-date) | Business metric | GOLD-KPI-008 |
| business | [Referrals Placed by Target at Snapshot](#business-referrals-placed-by-target-at-snapshot) | Business metric | GOLD-KPI-297 |
| business | [Referrals Under Offer](#business-referrals-under-offer) | Business metric | KPI-30 |
| business | [Referrals Under Offer MoM %](#business-referrals-under-offer-mom-percent) | Business metric | GOLD-KPI-298 |
| business | [Referrals Under Offer Previous Month](#business-referrals-under-offer-previous-month) | Business metric | GOLD-KPI-299 |
| business | [Referrals Under Offer Variance](#business-referrals-under-offer-variance) | Business metric | GOLD-KPI-300 |
| business | [Referrals Under Offer Variance Indicator](#business-referrals-under-offer-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Referrals Under Offer Variance Indicator Color](#business-referrals-under-offer-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Referrals With Fully Signed IPA](#business-referrals-with-fully-signed-ipa) | Business metric | GOLD-KPI-103 |
| business | [Referrals With IPA](#business-referrals-with-ipa) | Business metric | GOLD-KPI-305 |
| business | [Referrals With IPA Pending Signature](#business-referrals-with-ipa-pending-signature) | Business metric | GOLD-KPI-306 |
| business | [Referrals With Lifecycle Activity](#business-referrals-with-lifecycle-activity) | Business metric | GOLD-KPI-106 |
| business | [Referrals With Multiple Provider Assignments](#business-referrals-with-multiple-provider-assignments) | Business metric | KPI-90 |
| business | [Referrals With Offers](#business-referrals-with-offers) | Business metric | GOLD-KPI-308 |
| business | [Referrals With Offers %](#business-referrals-with-offers-percent) | Business metric | GOLD-KPI-309 |
| business | [Referrals With an Offer](#business-referrals-with-an-offer) | Business metric | KPI-02, KPI-09, KPI-33 |
| business | [Referrals With an Offer MoM %](#business-referrals-with-an-offer-mom-percent) | Business metric | GOLD-KPI-302 |
| business | [Referrals With an Offer Previous Month](#business-referrals-with-an-offer-previous-month) | Business metric | GOLD-KPI-303 |
| business | [Referrals With an Offer Variance](#business-referrals-with-an-offer-variance) | Business metric | GOLD-KPI-304 |
| business | [Referrals With an Offer Variance Indicator](#business-referrals-with-an-offer-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Referrals With an Offer Variance Indicator Color](#business-referrals-with-an-offer-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Referrals With an Offer at Snapshot](#business-referrals-with-an-offer-at-snapshot) | Business metric | GOLD-KPI-301 |
| business | [Referrals Without Provider Assignment](#business-referrals-without-provider-assignment) | Business metric | GOLD-KPI-006 |
| business | [Referrals closed during month](#business-referrals-closed-during-month) | Business metric | GOLD-KPI-121 |
| business | [Referrals with IPA at Snapshot](#business-referrals-with-ipa-at-snapshot) | Business metric | GOLD-KPI-031 |
| business | [Referrals with Missed Response Date](#business-referrals-with-missed-response-date) | Business metric | GOLD-KPI-307 |
| business | [Report Version Label](#business-report-version-label) | Display/filter/context helper | Helper/context only |
| business | [Requirement KPI row visible](#business-requirement-kpi-row-visible) | Display/filter helper | Helper/context only |
| business | [Requirement KPI value](#business-requirement-kpi-value) | Display/filter helper | Helper/context only |
| business | [Requirements catalogued](#business-requirements-catalogued) | Business metric | GOLD-KPI-310 |
| business | [Requirements linked to KPIs](#business-requirements-linked-to-kpis) | Business metric | GOLD-KPI-311 |
| business | [Residential Homes](#business-residential-homes) | Business metric | KPI-49 |
| business | [Snapshot Month In Window](#business-snapshot-month-in-window) | Filter/context helper | Helper/context only |
| business | [Snapshot Placement Target Hit Rate](#business-snapshot-placement-target-hit-rate) | Business metric | GOLD-KPI-312 |
| business | [Snapshot Referrals](#business-snapshot-referrals) | Business metric | GOLD-KPI-028 |
| business | [Snapshot Referrals Placed by Required Date](#business-snapshot-referrals-placed-by-required-date) | Business metric | GOLD-KPI-313 |
| business | [Snapshot Window Anchor](#business-snapshot-window-anchor) | Filter/context helper | Helper/context only |
| business | [Snapshot Window Months](#business-snapshot-window-months) | Filter/context helper | Helper/context only |
| business | [Snapshot referrals MoM change](#business-snapshot-referrals-mom-change) | Business metric | GOLD-KPI-119 |
| business | [Snapshot referrals MoM percent](#business-snapshot-referrals-mom-percent) | Business metric | GOLD-KPI-120 |
| business | [Snapshot referrals previous month](#business-snapshot-referrals-previous-month) | Business metric | GOLD-KPI-118 |
| business | [Spot Offer Rate](#business-spot-offer-rate) | Business metric | GOLD-KPI-062 |
| business | [Spot Offers](#business-spot-offers) | Business metric | GOLD-KPI-060 |
| business | [Spot Offers on Referrals Under Offer](#business-spot-offers-on-referrals-under-offer) | Business metric | KPI-27 |
| business | [Successful Offers on Referrals Under Offer](#business-successful-offers-on-referrals-under-offer) | Business metric | KPI-15 |
| business | [Successful Offers to IPA Completed %](#business-successful-offers-to-ipa-completed-percent) | Business metric | KPI-86 |
| business | [Supported Accommodation Homes](#business-supported-accommodation-homes) | Business metric | KPI-50 |
| business | [Target Hit Rate at Snapshot](#business-target-hit-rate-at-snapshot) | Business metric | GOLD-KPI-314 |
| business | [Total Gendered Referrals](#business-total-gendered-referrals) | Business metric | KPI-07, GOLD-KPI-113 |
| business | [Total IPA Weekly Cost](#business-total-ipa-weekly-cost) | Business metric | GOLD-KPI-098 |
| business | [Total Lifetime Cost](#business-total-lifetime-cost) | Business metric | GOLD-KPI-315 |
| business | [Total Offers Made Previous Month](#business-total-offers-made-previous-month) | Business metric | GOLD-KPI-317 |
| business | [Total Offers Made Variance](#business-total-offers-made-variance) | Business metric | GOLD-KPI-318 |
| business | [Total Offers Made Variance Color](#business-total-offers-made-variance-color) | Display/filter helper | Helper/context only |
| business | [Total Offers Made Variance Indicator](#business-total-offers-made-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Total Offers at Snapshot](#business-total-offers-at-snapshot) | Business metric | GOLD-KPI-316 |
| business | [Total Referrals](#business-total-referrals) | Business metric | KPI-26, KPI-01 |
| business | [Total Referrals MoM %](#business-total-referrals-mom-percent) | Business metric | GOLD-KPI-319 |
| business | [Total Referrals Previous Month](#business-total-referrals-previous-month) | Business metric | GOLD-KPI-320 |
| business | [Total Referrals That Received Offers (Ratio)](#business-total-referrals-that-received-offers-ratio) | Business metric | GOLD-KPI-321 |
| business | [Total Referrals That Received Offers Previous Month](#business-total-referrals-that-received-offers-previous-month) | Business metric | GOLD-KPI-322 |
| business | [Total Referrals That Received Offers Variance](#business-total-referrals-that-received-offers-variance) | Business metric | GOLD-KPI-323 |
| business | [Total Referrals That Received Offers Variance Indicator Color](#business-total-referrals-that-received-offers-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Total Referrals Variance](#business-total-referrals-variance) | Business metric | GOLD-KPI-324 |
| business | [Total Referrals Variance Indicator](#business-total-referrals-variance-indicator) | Display/filter helper | Helper/context only |
| business | [Total Referrals Variance Indicator Color](#business-total-referrals-variance-indicator-color) | Display/filter helper | Helper/context only |
| business | [Under offer](#business-under-offer) | Business metric | GOLD-KPI-325 |
| business | [Unsuccessful Offers](#business-unsuccessful-offers) | Business metric | GOLD-KPI-054 |
| business | [Unsuccessful Offers (Under Offer Referrals)](#business-unsuccessful-offers-under-offer-referrals) | Business metric | GOLD-KPI-326 |
| business | [Unsuccessful Offers on Referrals Under Offer](#business-unsuccessful-offers-on-referrals-under-offer) | Business metric | KPI-16 |
| business | [Username](#business-username) | Display/filter helper | Helper/context only |
| business | [expired_docs](#business-expired-docs) | Display/filter helper | Helper/context only |
| mission | [Active DQ Rules](#mission-active-dq-rules) | Operational metric | MC-KPI-001 |
| mission | [Archive Export Rows](#mission-archive-export-rows) | Operational metric | MC-KPI-002 |
| mission | [Archive File Failures](#mission-archive-file-failures) | Operational metric | MC-KPI-003 |
| mission | [Archive File Rows Read](#mission-archive-file-rows-read) | Operational metric | MC-KPI-004 |
| mission | [Archive File Rows Written](#mission-archive-file-rows-written) | Operational metric | MC-KPI-005 |
| mission | [Archive Files Awaiting Reload](#mission-archive-files-awaiting-reload) | Operational metric | MC-KPI-006 |
| mission | [Archive Files Processed](#mission-archive-files-processed) | Operational metric | MC-KPI-007 |
| mission | [Archive Pipeline Failures](#mission-archive-pipeline-failures) | Operational metric | MC-KPI-008 |
| mission | [Archive Pipeline Runs](#mission-archive-pipeline-runs) | Operational metric | MC-KPI-009 |
| mission | [Archive Table Exports](#mission-archive-table-exports) | Operational metric | MC-KPI-010 |
| mission | [Archive Table Exports Awaiting Reload](#mission-archive-table-exports-awaiting-reload) | Operational metric | MC-KPI-011 |
| mission | [Archive ZIP Batches](#mission-archive-zip-batches) | Operational metric | MC-KPI-012 |
| mission | [Archive ZIP Batches Awaiting Reload](#mission-archive-zip-batches-awaiting-reload) | Operational metric | MC-KPI-013 |
| mission | [Archive ZIP Files Declared](#mission-archive-zip-files-declared) | Operational metric | MC-KPI-014 |
| mission | [Archived Nullable Columns](#mission-archived-nullable-columns) | Operational metric | MC-KPI-015 |
| mission | [Archived Schema Columns](#mission-archived-schema-columns) | Operational metric | MC-KPI-016 |
| mission | [Archived Schema Data Types](#mission-archived-schema-data-types) | Operational metric | MC-KPI-017 |
| mission | [Archived Schema Tables](#mission-archived-schema-tables) | Operational metric | MC-KPI-018 |
| mission | [Average Archive ZIP Duration (min)](#mission-average-archive-zip-duration-min) | Operational metric | MC-KPI-019 |
| mission | [Average Pipeline Duration (min)](#mission-average-pipeline-duration-min) | Operational metric | MC-KPI-020 |
| mission | [Calendar Day Failures](#mission-calendar-day-failures) | Operational metric | MC-KPI-021 |
| mission | [Calendar Day In Window](#mission-calendar-day-in-window) | Operational metric | MC-KPI-022 |
| mission | [Calendar Day Other](#mission-calendar-day-other) | Operational metric | MC-KPI-023 |
| mission | [Calendar Day Runs](#mission-calendar-day-runs) | Operational metric | MC-KPI-024 |
| mission | [Completed Pipeline Runs](#mission-completed-pipeline-runs) | Operational metric | MC-KPI-025 |
| mission | [Control Failures](#mission-control-failures) | Operational metric | MC-KPI-026 |
| mission | [Critical Active DQ Rules](#mission-critical-active-dq-rules) | Operational metric | MC-KPI-027 |
| mission | [Critical Rules Failing](#mission-critical-rules-failing) | Operational metric | MC-KPI-028 |
| mission | [DQ Checked Rows](#mission-dq-checked-rows) | Operational metric | MC-KPI-090 |
| mission | [DQ Checks](#mission-dq-checks) | Operational metric | MC-KPI-091 |
| mission | [DQ Evaluated Checks](#mission-dq-evaluated-checks) | Operational metric | MC-KPI-092 |
| mission | [DQ Failed Checks](#mission-dq-failed-checks) | Operational metric | MC-KPI-093 |
| mission | [DQ Failed Rows](#mission-dq-failed-rows) | Operational metric | MC-KPI-094 |
| mission | [DQ Failure Rate](#mission-dq-failure-rate) | Operational metric | MC-KPI-095 |
| mission | [DQ Failures With Sample Keys](#mission-dq-failures-with-sample-keys) | Operational metric | MC-KPI-096 |
| mission | [Dashboard Last Refreshed](#mission-dashboard-last-refreshed) | Display/context helper | Helper/context only |
| mission | [Day Explorer Job Visible](#mission-day-explorer-job-visible) | Filter/context helper | Helper/context only |
| mission | [Day colour](#mission-day-colour) | Display/context helper | Helper/context only |
| mission | [Day text colour](#mission-day-text-colour) | Display/context helper | Helper/context only |
| mission | [Day tile](#mission-day-tile) | Display/context helper | Helper/context only |
| mission | [Discovery calendar failures](#mission-discovery-calendar-failures) | Operational metric | MC-KPI-029 |
| mission | [Discovery calendar jobs](#mission-discovery-calendar-jobs) | Operational metric | MC-KPI-030 |
| mission | [Discovery calendar other](#mission-discovery-calendar-other) | Operational metric | MC-KPI-031 |
| mission | [Discovery cfg_archive_zip_load Latest key](#mission-discovery-cfg-archive-zip-load-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_archive_zip_load Latest time](#mission-discovery-cfg-archive-zip-load-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_archive_zip_load Rows](#mission-discovery-cfg-archive-zip-load-rows) | Operational metric | MC-KPI-032 |
| mission | [Discovery cfg_archive_zip_load Selected time](#mission-discovery-cfg-archive-zip-load-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_archive_zip_load State](#mission-discovery-cfg-archive-zip-load-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_archive_zip_load Visible](#mission-discovery-cfg-archive-zip-load-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_archived_schema_live Latest time](#mission-discovery-cfg-archived-schema-live-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_archived_schema_live Rows](#mission-discovery-cfg-archived-schema-live-rows) | Operational metric | MC-KPI-033 |
| mission | [Discovery cfg_archived_schema_live Selected time](#mission-discovery-cfg-archived-schema-live-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_archived_schema_live State](#mission-discovery-cfg-archived-schema-live-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_archived_schema_live Visible](#mission-discovery-cfg-archived-schema-live-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live Context](#mission-discovery-cfg-bronze-schema-live-context) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live Discovery batches](#mission-discovery-cfg-bronze-schema-live-discovery-batches) | Operational metric | MC-KPI-034 |
| mission | [Discovery cfg_bronze_schema_live Distinct objects](#mission-discovery-cfg-bronze-schema-live-distinct-objects) | Operational metric | MC-KPI-035 |
| mission | [Discovery cfg_bronze_schema_live Latest key](#mission-discovery-cfg-bronze-schema-live-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live Latest time](#mission-discovery-cfg-bronze-schema-live-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live Rows](#mission-discovery-cfg-bronze-schema-live-rows) | Operational metric | MC-KPI-036 |
| mission | [Discovery cfg_bronze_schema_live Scope count](#mission-discovery-cfg-bronze-schema-live-scope-count) | Operational metric | MC-KPI-037 |
| mission | [Discovery cfg_bronze_schema_live Selected time](#mission-discovery-cfg-bronze-schema-live-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live State](#mission-discovery-cfg-bronze-schema-live-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_bronze_schema_live Visible](#mission-discovery-cfg-bronze-schema-live-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain Context](#mission-discovery-cfg-data-domain-context) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain Discovery batches](#mission-discovery-cfg-data-domain-discovery-batches) | Operational metric | MC-KPI-038 |
| mission | [Discovery cfg_data_domain Distinct objects](#mission-discovery-cfg-data-domain-distinct-objects) | Operational metric | MC-KPI-039 |
| mission | [Discovery cfg_data_domain Latest key](#mission-discovery-cfg-data-domain-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain Latest time](#mission-discovery-cfg-data-domain-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain Rows](#mission-discovery-cfg-data-domain-rows) | Operational metric | MC-KPI-040 |
| mission | [Discovery cfg_data_domain Scope count](#mission-discovery-cfg-data-domain-scope-count) | Operational metric | MC-KPI-041 |
| mission | [Discovery cfg_data_domain Selected time](#mission-discovery-cfg-data-domain-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain State](#mission-discovery-cfg-data-domain-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_data_domain Visible](#mission-discovery-cfg-data-domain-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_gold_lineage_mapping Rows](#mission-discovery-cfg-gold-lineage-mapping-rows) | Operational metric | MC-KPI-042 |
| mission | [Discovery cfg_gold_lineage_mapping State](#mission-discovery-cfg-gold-lineage-mapping-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_gold_lineage_mapping Visible](#mission-discovery-cfg-gold-lineage-mapping-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_location_coordinate Rows](#mission-discovery-cfg-location-coordinate-rows) | Operational metric | MC-KPI-043 |
| mission | [Discovery cfg_location_coordinate State](#mission-discovery-cfg-location-coordinate-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_location_coordinate Visible](#mission-discovery-cfg-location-coordinate-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_month_end_gold_run Latest key](#mission-discovery-cfg-month-end-gold-run-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_month_end_gold_run Latest time](#mission-discovery-cfg-month-end-gold-run-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_month_end_gold_run Rows](#mission-discovery-cfg-month-end-gold-run-rows) | Operational metric | MC-KPI-044 |
| mission | [Discovery cfg_month_end_gold_run Selected time](#mission-discovery-cfg-month-end-gold-run-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_month_end_gold_run State](#mission-discovery-cfg-month-end-gold-run-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_month_end_gold_run Visible](#mission-discovery-cfg-month-end-gold-run-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_referential_exception Latest key](#mission-discovery-cfg-referential-exception-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_referential_exception Latest time](#mission-discovery-cfg-referential-exception-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_referential_exception Rows](#mission-discovery-cfg-referential-exception-rows) | Operational metric | MC-KPI-045 |
| mission | [Discovery cfg_referential_exception Selected time](#mission-discovery-cfg-referential-exception-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_referential_exception State](#mission-discovery-cfg-referential-exception-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_referential_exception Visible](#mission-discovery-cfg-referential-exception-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_rejected_row Latest key](#mission-discovery-cfg-rejected-row-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_rejected_row Latest time](#mission-discovery-cfg-rejected-row-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_rejected_row Rows](#mission-discovery-cfg-rejected-row-rows) | Operational metric | MC-KPI-046 |
| mission | [Discovery cfg_rejected_row Selected time](#mission-discovery-cfg-rejected-row-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_rejected_row State](#mission-discovery-cfg-rejected-row-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_rejected_row Visible](#mission-discovery-cfg-rejected-row-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_contract_column Latest time](#mission-discovery-cfg-schema-contract-column-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_contract_column Rows](#mission-discovery-cfg-schema-contract-column-rows) | Operational metric | MC-KPI-047 |
| mission | [Discovery cfg_schema_contract_column Selected time](#mission-discovery-cfg-schema-contract-column-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_contract_column State](#mission-discovery-cfg-schema-contract-column-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_contract_column Visible](#mission-discovery-cfg-schema-contract-column-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_definition_candidate Rows](#mission-discovery-cfg-schema-definition-candidate-rows) | Operational metric | MC-KPI-048 |
| mission | [Discovery cfg_schema_definition_candidate State](#mission-discovery-cfg-schema-definition-candidate-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_definition_candidate Visible](#mission-discovery-cfg-schema-definition-candidate-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_definition Latest time](#mission-discovery-cfg-schema-drift-definition-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_definition Rows](#mission-discovery-cfg-schema-drift-definition-rows) | Operational metric | MC-KPI-049 |
| mission | [Discovery cfg_schema_drift_definition Selected time](#mission-discovery-cfg-schema-drift-definition-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_definition State](#mission-discovery-cfg-schema-drift-definition-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_definition Visible](#mission-discovery-cfg-schema-drift-definition-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event Context](#mission-discovery-cfg-schema-drift-event-context) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event Discovery batches](#mission-discovery-cfg-schema-drift-event-discovery-batches) | Operational metric | MC-KPI-050 |
| mission | [Discovery cfg_schema_drift_event Distinct objects](#mission-discovery-cfg-schema-drift-event-distinct-objects) | Operational metric | MC-KPI-051 |
| mission | [Discovery cfg_schema_drift_event Latest key](#mission-discovery-cfg-schema-drift-event-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event Latest time](#mission-discovery-cfg-schema-drift-event-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event Rows](#mission-discovery-cfg-schema-drift-event-rows) | Operational metric | MC-KPI-052 |
| mission | [Discovery cfg_schema_drift_event Scope count](#mission-discovery-cfg-schema-drift-event-scope-count) | Operational metric | MC-KPI-053 |
| mission | [Discovery cfg_schema_drift_event Selected time](#mission-discovery-cfg-schema-drift-event-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event State](#mission-discovery-cfg-schema-drift-event-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_schema_drift_event Visible](#mission-discovery-cfg-schema-drift-event-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_export_load Latest key](#mission-discovery-cfg-silver-export-load-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_silver_export_load Latest time](#mission-discovery-cfg-silver-export-load-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_export_load Rows](#mission-discovery-cfg-silver-export-load-rows) | Operational metric | MC-KPI-054 |
| mission | [Discovery cfg_silver_export_load Selected time](#mission-discovery-cfg-silver-export-load-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_export_load State](#mission-discovery-cfg-silver-export-load-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_silver_export_load Visible](#mission-discovery-cfg-silver-export-load-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_load_control Latest key](#mission-discovery-cfg-silver-load-control-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_silver_load_control Latest time](#mission-discovery-cfg-silver-load-control-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_load_control Rows](#mission-discovery-cfg-silver-load-control-rows) | Operational metric | MC-KPI-055 |
| mission | [Discovery cfg_silver_load_control Selected time](#mission-discovery-cfg-silver-load-control-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_silver_load_control State](#mission-discovery-cfg-silver-load-control-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_silver_load_control Visible](#mission-discovery-cfg-silver-load-control-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric Context](#mission-discovery-cfg-table-load-metric-context) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric Discovery batches](#mission-discovery-cfg-table-load-metric-discovery-batches) | Operational metric | MC-KPI-056 |
| mission | [Discovery cfg_table_load_metric Distinct objects](#mission-discovery-cfg-table-load-metric-distinct-objects) | Operational metric | MC-KPI-057 |
| mission | [Discovery cfg_table_load_metric Latest key](#mission-discovery-cfg-table-load-metric-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric Latest time](#mission-discovery-cfg-table-load-metric-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric Rows](#mission-discovery-cfg-table-load-metric-rows) | Operational metric | MC-KPI-058 |
| mission | [Discovery cfg_table_load_metric Scope count](#mission-discovery-cfg-table-load-metric-scope-count) | Operational metric | MC-KPI-059 |
| mission | [Discovery cfg_table_load_metric Selected time](#mission-discovery-cfg-table-load-metric-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric State](#mission-discovery-cfg-table-load-metric-state) | Display/context helper | Helper/context only |
| mission | [Discovery cfg_table_load_metric Visible](#mission-discovery-cfg-table-load-metric-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery contracts calendar changes](#mission-discovery-contracts-calendar-changes) | Operational metric | MC-KPI-060 |
| mission | [Discovery contracts calendar critical](#mission-discovery-contracts-calendar-critical) | Operational metric | MC-KPI-061 |
| mission | [Discovery contracts calendar discoveries](#mission-discovery-contracts-calendar-discoveries) | Operational metric | MC-KPI-062 |
| mission | [Discovery contracts calendar linked job visible](#mission-discovery-contracts-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery domains calendar changes](#mission-discovery-domains-calendar-changes) | Operational metric | MC-KPI-063 |
| mission | [Discovery domains calendar critical](#mission-discovery-domains-calendar-critical) | Operational metric | MC-KPI-064 |
| mission | [Discovery domains calendar discoveries](#mission-discovery-domains-calendar-discoveries) | Operational metric | MC-KPI-065 |
| mission | [Discovery domains calendar linked job visible](#mission-discovery-domains-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery drift calendar changes](#mission-discovery-drift-calendar-changes) | Operational metric | MC-KPI-066 |
| mission | [Discovery drift calendar critical](#mission-discovery-drift-calendar-critical) | Operational metric | MC-KPI-067 |
| mission | [Discovery drift calendar discoveries](#mission-discovery-drift-calendar-discoveries) | Operational metric | MC-KPI-068 |
| mission | [Discovery drift calendar linked job visible](#mission-discovery-drift-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery history selected](#mission-discovery-history-selected) | Filter/context helper | Helper/context only |
| mission | [Discovery job picker visible](#mission-discovery-job-picker-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery lineage calendar changes](#mission-discovery-lineage-calendar-changes) | Operational metric | MC-KPI-069 |
| mission | [Discovery lineage calendar critical](#mission-discovery-lineage-calendar-critical) | Operational metric | MC-KPI-070 |
| mission | [Discovery lineage calendar discoveries](#mission-discovery-lineage-calendar-discoveries) | Operational metric | MC-KPI-071 |
| mission | [Discovery lineage calendar linked job visible](#mission-discovery-lineage-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery loads calendar changes](#mission-discovery-loads-calendar-changes) | Operational metric | MC-KPI-072 |
| mission | [Discovery loads calendar critical](#mission-discovery-loads-calendar-critical) | Operational metric | MC-KPI-073 |
| mission | [Discovery loads calendar discoveries](#mission-discovery-loads-calendar-discoveries) | Operational metric | MC-KPI-074 |
| mission | [Discovery loads calendar linked job visible](#mission-discovery-loads-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery quality calendar changes](#mission-discovery-quality-calendar-changes) | Operational metric | MC-KPI-075 |
| mission | [Discovery quality calendar critical](#mission-discovery-quality-calendar-critical) | Operational metric | MC-KPI-076 |
| mission | [Discovery quality calendar discoveries](#mission-discovery-quality-calendar-discoveries) | Operational metric | MC-KPI-077 |
| mission | [Discovery quality calendar linked job visible](#mission-discovery-quality-calendar-linked-job-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality Context](#mission-discovery-rpt-job-data-quality-context) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality Discovery batches](#mission-discovery-rpt-job-data-quality-discovery-batches) | Operational metric | MC-KPI-078 |
| mission | [Discovery rpt_job_data_quality Distinct objects](#mission-discovery-rpt-job-data-quality-distinct-objects) | Operational metric | MC-KPI-079 |
| mission | [Discovery rpt_job_data_quality Latest key](#mission-discovery-rpt-job-data-quality-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality Latest time](#mission-discovery-rpt-job-data-quality-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality Rows](#mission-discovery-rpt-job-data-quality-rows) | Operational metric | MC-KPI-080 |
| mission | [Discovery rpt_job_data_quality Scope count](#mission-discovery-rpt-job-data-quality-scope-count) | Operational metric | MC-KPI-081 |
| mission | [Discovery rpt_job_data_quality Selected time](#mission-discovery-rpt-job-data-quality-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality State](#mission-discovery-rpt-job-data-quality-state) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_data_quality Visible](#mission-discovery-rpt-job-data-quality-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage Context](#mission-discovery-rpt-job-layer-lineage-context) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage Discovery batches](#mission-discovery-rpt-job-layer-lineage-discovery-batches) | Operational metric | MC-KPI-082 |
| mission | [Discovery rpt_job_layer_lineage Distinct objects](#mission-discovery-rpt-job-layer-lineage-distinct-objects) | Operational metric | MC-KPI-083 |
| mission | [Discovery rpt_job_layer_lineage Latest key](#mission-discovery-rpt-job-layer-lineage-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage Latest time](#mission-discovery-rpt-job-layer-lineage-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage Rows](#mission-discovery-rpt-job-layer-lineage-rows) | Operational metric | MC-KPI-084 |
| mission | [Discovery rpt_job_layer_lineage Scope count](#mission-discovery-rpt-job-layer-lineage-scope-count) | Operational metric | MC-KPI-085 |
| mission | [Discovery rpt_job_layer_lineage Selected time](#mission-discovery-rpt-job-layer-lineage-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage State](#mission-discovery-rpt-job-layer-lineage-state) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_layer_lineage Visible](#mission-discovery-rpt-job-layer-lineage-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_schema_drift Latest key](#mission-discovery-rpt-job-schema-drift-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_schema_drift Latest time](#mission-discovery-rpt-job-schema-drift-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_schema_drift Rows](#mission-discovery-rpt-job-schema-drift-rows) | Operational metric | MC-KPI-086 |
| mission | [Discovery rpt_job_schema_drift Selected time](#mission-discovery-rpt-job-schema-drift-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_schema_drift State](#mission-discovery-rpt-job-schema-drift-state) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_schema_drift Visible](#mission-discovery-rpt-job-schema-drift-visible) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_step_summary Latest key](#mission-discovery-rpt-job-step-summary-latest-key) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_step_summary Latest time](#mission-discovery-rpt-job-step-summary-latest-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_step_summary Rows](#mission-discovery-rpt-job-step-summary-rows) | Operational metric | MC-KPI-087 |
| mission | [Discovery rpt_job_step_summary Selected time](#mission-discovery-rpt-job-step-summary-selected-time) | Filter/context helper | Helper/context only |
| mission | [Discovery rpt_job_step_summary State](#mission-discovery-rpt-job-step-summary-state) | Display/context helper | Helper/context only |
| mission | [Discovery rpt_job_step_summary Visible](#mission-discovery-rpt-job-step-summary-visible) | Filter/context helper | Helper/context only |
| mission | [Domain value changes](#mission-domain-value-changes) | Display/context helper | Helper/context only |
| mission | [Domain values Added](#mission-domain-values-added) | Operational metric | MC-KPI-088 |
| mission | [Domain values Removed](#mission-domain-values-removed) | Operational metric | MC-KPI-089 |
| mission | [Failed Archive Table Exports](#mission-failed-archive-table-exports) | Operational metric | MC-KPI-097 |
| mission | [Failed Archive ZIP Batches](#mission-failed-archive-zip-batches) | Operational metric | MC-KPI-098 |
| mission | [Failed Gold Snapshots](#mission-failed-gold-snapshots) | Operational metric | MC-KPI-099 |
| mission | [Failed Job Runs](#mission-failed-job-runs) | Operational metric | MC-KPI-100 |
| mission | [Failed Job Steps](#mission-failed-job-steps) | Operational metric | MC-KPI-101 |
| mission | [Failed Pipeline Runs](#mission-failed-pipeline-runs) | Operational metric | MC-KPI-102 |
| mission | [Failures](#mission-failures) | Operational metric | MC-KPI-103 |
| mission | [Gold Snapshot DQ Failures](#mission-gold-snapshot-dq-failures) | Operational metric | MC-KPI-104 |
| mission | [Gold Snapshot Runs](#mission-gold-snapshot-runs) | Operational metric | MC-KPI-105 |
| mission | [Gold Snapshots Awaiting Replay](#mission-gold-snapshots-awaiting-replay) | Operational metric | MC-KPI-106 |
| mission | [High or Critical Rules Failing](#mission-high-or-critical-rules-failing) | Operational metric | MC-KPI-107 |
| mission | [In progress or other](#mission-in-progress-or-other) | Operational metric | MC-KPI-108 |
| mission | [Job Runs](#mission-job-runs) | Operational metric | MC-KPI-115 |
| mission | [Job Steps](#mission-job-steps) | Operational metric | MC-KPI-116 |
| mission | [Job Steps With Error](#mission-job-steps-with-error) | Operational metric | MC-KPI-117 |
| mission | [Job Success Rate](#mission-job-success-rate) | Operational metric | MC-KPI-118 |
| mission | [Job actual min](#mission-job-actual-min) | Operational metric | MC-KPI-109 |
| mission | [Job baseline n](#mission-job-baseline-n) | Operational metric | MC-KPI-110 |
| mission | [Job comparison](#mission-job-comparison) | Display/context helper | Helper/context only |
| mission | [Job prior mean min](#mission-job-prior-mean-min) | Operational metric | MC-KPI-111 |
| mission | [Job prior median min](#mission-job-prior-median-min) | Operational metric | MC-KPI-112 |
| mission | [Job prior p25 min](#mission-job-prior-p25-min) | Operational metric | MC-KPI-113 |
| mission | [Job prior p75 min](#mission-job-prior-p75-min) | Operational metric | MC-KPI-114 |
| mission | [Latest Archived Schema Capture](#mission-latest-archived-schema-capture) | Operational metric | MC-KPI-119 |
| mission | [Latest Job Run ID](#mission-latest-job-run-id) | Display/context helper | Helper/context only |
| mission | [Latest Job Run Started](#mission-latest-job-run-started) | Operational metric | MC-KPI-120 |
| mission | [Latest Load Critical Rules](#mission-latest-load-critical-rules) | Operational metric | MC-KPI-121 |
| mission | [Latest Load Evaluated Checks](#mission-latest-load-evaluated-checks) | Operational metric | MC-KPI-122 |
| mission | [Latest Load Failed Checks](#mission-latest-load-failed-checks) | Operational metric | MC-KPI-123 |
| mission | [Latest Load Failed Rows](#mission-latest-load-failed-rows) | Operational metric | MC-KPI-124 |
| mission | [Latest Load Quality Records](#mission-latest-load-quality-records) | Operational metric | MC-KPI-125 |
| mission | [Latest Load Quality Report](#mission-latest-load-quality-report) | Display/context helper | Helper/context only |
| mission | [Latest Load Run ID](#mission-latest-load-run-id) | Display/context helper | Helper/context only |
| mission | [Latest Load Started](#mission-latest-load-started) | Operational metric | MC-KPI-126 |
| mission | [Latest Load Status](#mission-latest-load-status) | Display/context helper | Helper/context only |
| mission | [Latest Pipeline End](#mission-latest-pipeline-end) | Operational metric | MC-KPI-131 |
| mission | [Latest Pipeline Row Visible](#mission-latest-pipeline-row-visible) | Filter/context helper | Helper/context only |
| mission | [Latest Pipeline Status](#mission-latest-pipeline-status) | Display/context helper | Helper/context only |
| mission | [Latest matching Archive ZIP Batches](#mission-latest-matching-archive-zip-batches) | Operational metric | MC-KPI-127 |
| mission | [Latest matching Archive ZIP Batches Awaiting Reload](#mission-latest-matching-archive-zip-batches-awaiting-reload) | Operational metric | MC-KPI-128 |
| mission | [Latest matching Failed Archive ZIP Batches](#mission-latest-matching-failed-archive-zip-batches) | Operational metric | MC-KPI-129 |
| mission | [Latest matching Failed Gold Snapshots](#mission-latest-matching-failed-gold-snapshots) | Operational metric | MC-KPI-130 |
| mission | [Latest or selected Failures](#mission-latest-or-selected-failures) | Filter/context helper | Helper/context only |
| mission | [Latest or selected P95 duration min](#mission-latest-or-selected-p95-duration-min) | Filter/context helper | Helper/context only |
| mission | [Latest or selected Rows written](#mission-latest-or-selected-rows-written) | Filter/context helper | Helper/context only |
| mission | [Latest or selected Runs](#mission-latest-or-selected-runs) | Filter/context helper | Helper/context only |
| mission | [Latest or selected Success rate](#mission-latest-or-selected-success-rate) | Filter/context helper | Helper/context only |
| mission | [Live Pipeline Failures](#mission-live-pipeline-failures) | Operational metric | MC-KPI-132 |
| mission | [Live Pipeline Runs](#mission-live-pipeline-runs) | Operational metric | MC-KPI-133 |
| mission | [Load Rows Read Delta](#mission-load-rows-read-delta) | Operational metric | MC-KPI-134 |
| mission | [Load Rows Read Delta %](#mission-load-rows-read-delta-percent) | Operational metric | MC-KPI-135 |
| mission | [Load Rows Read Previous](#mission-load-rows-read-previous) | Operational metric | MC-KPI-136 |
| mission | [Load Rows Read Sparkline](#mission-load-rows-read-sparkline) | Display/context helper | Helper/context only |
| mission | [Load Rows Written Delta](#mission-load-rows-written-delta) | Operational metric | MC-KPI-137 |
| mission | [Load Rows Written Delta %](#mission-load-rows-written-delta-percent) | Operational metric | MC-KPI-138 |
| mission | [Load Rows Written Previous](#mission-load-rows-written-previous) | Operational metric | MC-KPI-139 |
| mission | [Load Rows Written Sparkline](#mission-load-rows-written-sparkline) | Display/context helper | Helper/context only |
| mission | [Longest Job Step Duration (min)](#mission-longest-job-step-duration-min) | Operational metric | MC-KPI-140 |
| mission | [Operational Exception Count](#mission-operational-exception-count) | Operational metric | MC-KPI-141 |
| mission | [P95 Pipeline Duration (min)](#mission-p95-pipeline-duration-min) | Operational metric | MC-KPI-143 |
| mission | [P95 duration min](#mission-p95-duration-min) | Operational metric | MC-KPI-142 |
| mission | [Pipeline Rows Read](#mission-pipeline-rows-read) | Operational metric | MC-KPI-145 |
| mission | [Pipeline Rows Written](#mission-pipeline-rows-written) | Operational metric | MC-KPI-146 |
| mission | [Pipeline Rows per Minute](#mission-pipeline-rows-per-minute) | Operational metric | MC-KPI-144 |
| mission | [Pipeline Runs](#mission-pipeline-runs) | Operational metric | MC-KPI-147 |
| mission | [Pipeline Runs With Error](#mission-pipeline-runs-with-error) | Operational metric | MC-KPI-148 |
| mission | [Pipeline Success Rate](#mission-pipeline-success-rate) | Operational metric | MC-KPI-149 |
| mission | [Pipeline Tables Failed](#mission-pipeline-tables-failed) | Operational metric | MC-KPI-150 |
| mission | [Pipeline Tables Succeeded](#mission-pipeline-tables-succeeded) | Operational metric | MC-KPI-151 |
| mission | [RI Checked Rows](#mission-ri-checked-rows) | Operational metric | MC-KPI-153 |
| mission | [RI Failed Rows](#mission-ri-failed-rows) | Operational metric | MC-KPI-154 |
| mission | [RI Failure Rate](#mission-ri-failure-rate) | Operational metric | MC-KPI-155 |
| mission | [RI Rules Failing](#mission-ri-rules-failing) | Operational metric | MC-KPI-156 |
| mission | [Reload Requests](#mission-reload-requests) | Operational metric | MC-KPI-152 |
| mission | [Rows written](#mission-rows-written) | Operational metric | MC-KPI-157 |
| mission | [Running Pipeline Runs](#mission-running-pipeline-runs) | Operational metric | MC-KPI-158 |
| mission | [Runs](#mission-runs) | Operational metric | MC-KPI-159 |
| mission | [Selected Step Error Detail](#mission-selected-step-error-detail) | Display/context helper | Helper/context only |
| mission | [Selected or Latest Failed Steps](#mission-selected-or-latest-failed-steps) | Filter/context helper | Helper/context only |
| mission | [Selected or Latest Job Duration (min)](#mission-selected-or-latest-job-duration-min) | Filter/context helper | Helper/context only |
| mission | [Selected or Latest Job Error](#mission-selected-or-latest-job-error) | Display/context helper | Helper/context only |
| mission | [Selected or Latest Job Run ID](#mission-selected-or-latest-job-run-id) | Display/context helper | Helper/context only |
| mission | [Selected or Latest Job Status](#mission-selected-or-latest-job-status) | Display/context helper | Helper/context only |
| mission | [Selected or Latest Job Steps](#mission-selected-or-latest-job-steps) | Filter/context helper | Helper/context only |
| mission | [Show Latest Load Quality](#mission-show-latest-load-quality) | Operational metric | MC-KPI-160 |
| mission | [Show Step for Selected or Latest Job Run](#mission-show-step-for-selected-or-latest-job-run) | Filter/context helper | Helper/context only |
| mission | [Single calendar day](#mission-single-calendar-day) | Operational metric | MC-KPI-161 |
| mission | [Step actual min](#mission-step-actual-min) | Operational metric | MC-KPI-162 |
| mission | [Step baseline n](#mission-step-baseline-n) | Operational metric | MC-KPI-163 |
| mission | [Step comparison](#mission-step-comparison) | Display/context helper | Helper/context only |
| mission | [Step prior mean min](#mission-step-prior-mean-min) | Operational metric | MC-KPI-164 |
| mission | [Step prior median min](#mission-step-prior-median-min) | Operational metric | MC-KPI-165 |
| mission | [Step prior p25 min](#mission-step-prior-p25-min) | Operational metric | MC-KPI-166 |
| mission | [Step prior p75 min](#mission-step-prior-p75-min) | Operational metric | MC-KPI-167 |
| mission | [Success rate](#mission-success-rate) | Operational metric | MC-KPI-168 |
| mission | [Successful](#mission-successful) | Operational metric | MC-KPI-169 |
| mission | [Successful Archive Files](#mission-successful-archive-files) | Operational metric | MC-KPI-170 |
| mission | [Successful Archive ZIP Batches](#mission-successful-archive-zip-batches) | Operational metric | MC-KPI-171 |
| mission | [Successful Gold Snapshots](#mission-successful-gold-snapshots) | Operational metric | MC-KPI-172 |
| mission | [Successful Job Runs](#mission-successful-job-runs) | Operational metric | MC-KPI-173 |
| mission | [Successful Job Steps](#mission-successful-job-steps) | Operational metric | MC-KPI-174 |
| mission | [Successful Pipeline Runs](#mission-successful-pipeline-runs) | Operational metric | MC-KPI-175 |
| mission | [Timeline Job Visible](#mission-timeline-job-visible) | Filter/context helper | Helper/context only |
| mission | [Timeline Step Visible](#mission-timeline-step-visible) | Filter/context helper | Helper/context only |
| mission | [Total Job Step Duration (min)](#mission-total-job-step-duration-min) | Operational metric | MC-KPI-176 |
| mission | [Total Pipeline Duration (min)](#mission-total-pipeline-duration-min) | Operational metric | MC-KPI-177 |
| mission | [Watch Tower Contracts Count](#mission-watch-tower-contracts-count) | Operational metric | MC-KPI-178 |
| mission | [Watch Tower Contracts Date](#mission-watch-tower-contracts-date) | Display/context helper | Helper/context only |
| mission | [Watch Tower Contracts Detail](#mission-watch-tower-contracts-detail) | Display/context helper | Helper/context only |
| mission | [Watch Tower Contracts Flag](#mission-watch-tower-contracts-flag) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Contracts Flag Captured](#mission-watch-tower-contracts-flag-captured) | Display/context helper | Helper/context only |
| mission | [Watch Tower Contracts Flag Label](#mission-watch-tower-contracts-flag-label) | Display/context helper | Helper/context only |
| mission | [Watch Tower Contracts Flag Records](#mission-watch-tower-contracts-flag-records) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Contracts Flag Tooltip](#mission-watch-tower-contracts-flag-tooltip) | Display/context helper | Helper/context only |
| mission | [Watch Tower Contracts Reference](#mission-watch-tower-contracts-reference) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Count](#mission-watch-tower-domains-count) | Operational metric | MC-KPI-179 |
| mission | [Watch Tower Domains Date](#mission-watch-tower-domains-date) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Detail](#mission-watch-tower-domains-detail) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Flag](#mission-watch-tower-domains-flag) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Domains Flag Captured](#mission-watch-tower-domains-flag-captured) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Flag Label](#mission-watch-tower-domains-flag-label) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Flag Records](#mission-watch-tower-domains-flag-records) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Domains Flag Tooltip](#mission-watch-tower-domains-flag-tooltip) | Display/context helper | Helper/context only |
| mission | [Watch Tower Domains Reference](#mission-watch-tower-domains-reference) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Active](#mission-watch-tower-drift-active) | Operational metric | MC-KPI-180 |
| mission | [Watch Tower Drift Count](#mission-watch-tower-drift-count) | Operational metric | MC-KPI-181 |
| mission | [Watch Tower Drift Date](#mission-watch-tower-drift-date) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Detail](#mission-watch-tower-drift-detail) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Flag](#mission-watch-tower-drift-flag) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Drift Flag Captured](#mission-watch-tower-drift-flag-captured) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Flag Label](#mission-watch-tower-drift-flag-label) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Flag Records](#mission-watch-tower-drift-flag-records) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Drift Flag Tooltip](#mission-watch-tower-drift-flag-tooltip) | Display/context helper | Helper/context only |
| mission | [Watch Tower Drift Reference](#mission-watch-tower-drift-reference) | Display/context helper | Helper/context only |
| mission | [Watch Tower Flag Latest Load Day](#mission-watch-tower-flag-latest-load-day) | Display/context helper | Helper/context only |
| mission | [Watch Tower Flag Legend](#mission-watch-tower-flag-legend) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Count](#mission-watch-tower-quality-count) | Operational metric | MC-KPI-182 |
| mission | [Watch Tower Quality Date](#mission-watch-tower-quality-date) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Detail](#mission-watch-tower-quality-detail) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Failed Checks](#mission-watch-tower-quality-failed-checks) | Operational metric | MC-KPI-183 |
| mission | [Watch Tower Quality Flag](#mission-watch-tower-quality-flag) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Quality Flag Captured](#mission-watch-tower-quality-flag-captured) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Flag Label](#mission-watch-tower-quality-flag-label) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Flag Records](#mission-watch-tower-quality-flag-records) | Filter/context helper | Helper/context only |
| mission | [Watch Tower Quality Flag Tooltip](#mission-watch-tower-quality-flag-tooltip) | Display/context helper | Helper/context only |
| mission | [Watch Tower Quality Reference](#mission-watch-tower-quality-reference) | Display/context helper | Helper/context only |
| mission | [Weighted DQ Failure Percentage](#mission-weighted-dq-failure-percentage) | Operational metric | MC-KPI-184 |
| business | [Linked referral current status](#business-linked-referral-current-status) | Display helper | Helper/context only |

<a id="business-accepted-offer-to-ipa-conversion-percent"></a>
## Accepted Offer to IPA Conversion %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-83.

```dax
DIVIDE ( [IPAs Created], [Accepted Offers] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-accepted-offers"></a>
## Accepted Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-39, KPI-75.

```dax
CALCULATE (
			    [Offers Submitted],
			    FILTER (
			        'fact_offer',
			        LOWER ( 'fact_offer'[offer_status] ) IN { "accepted", "approved", "selected", "offer_successful" }
			    )
			)
```

Source tables: `gold.fact_offer`

<a id="business-accepted-offers-linked-to-ipa-percent"></a>
## Accepted Offers Linked to IPA %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-145.

```dax
DIVIDE ( [Accepted Offers With IPA], [Accepted Offers] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-accepted-offers-with-ipa"></a>
## Accepted Offers With IPA

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-099.

```dax
VAR linked_offers = VALUES ( 'fact_ipa'[accepted_offer_id] )
			RETURN CALCULATE ( [Accepted Offers], KEEPFILTERS ( TREATAS ( linked_offers, 'fact_offer'[offer_id] ) ) )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-active-awaiting-offers-with-engagement"></a>
## Active Awaiting Offers With Engagement

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-21.

```dax
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[is_awaiting_offer] = TRUE (),
				'fact_referral'[has_provider_response] = TRUE ()
			)
```

Source tables: `gold.fact_referral`

<a id="business-active-awaiting-offers-without-engagement"></a>
## Active Awaiting Offers Without Engagement

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-22.

```dax
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[is_awaiting_offer] = TRUE (),
				'fact_referral'[has_provider_response] = FALSE ()
			)
```

Source tables: `gold.fact_referral`

<a id="business-active-ipas"></a>
## Active IPAs

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-022.

```dax
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = FALSE () )
```

Source tables: `gold.fact_ipa`

<a id="business-active-provider-response-rate-at-snapshot"></a>
## Active Provider Response Rate at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-146.

```dax
VAR eligible_open_referrals =
				CALCULATE (
					[Snapshot Referrals],
					'fact_referral_snapshot'[is_open] = TRUE (),
					FILTER (
						'fact_referral_snapshot',
						NOT ISBLANK ( 'fact_referral_snapshot'[has_provider_response] )
					)
				)
			RETURN
				DIVIDE (
					[Active Referrals With Provider Response at Snapshot],
					eligible_open_referrals
				)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-active-referral-engagement-rate"></a>
## Active Referral Engagement Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-20.

```dax
DIVIDE ( [Active Referrals With Provider Engagement], [Referrals Currently Active] )
```

Source tables: `gold.fact_referral`

<a id="business-active-referral-engagement-rate-mom-percent"></a>
## Active Referral Engagement Rate MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-147.

```dax
DIVIDE ( [Active Referral Engagement Rate Variance], [Active Referral Engagement Rate Previous Month] )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referral-engagement-rate-previous-month"></a>
## Active Referral Engagement Rate Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-148.

```dax
CALCULATE ( [Active Provider Response Rate at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referral-engagement-rate-variance"></a>
## Active Referral Engagement Rate Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-149.

```dax
[Active Provider Response Rate at Snapshot] - [Active Referral Engagement Rate Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referral-engagement-rate-variance-indicator"></a>
## Active Referral Engagement Rate Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Active Referral Engagement Rate Variance] > 0, "▲", IF ( [Active Referral Engagement Rate Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referral-engagement-rate-variance-indicator-color"></a>
## Active Referral Engagement Rate Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Active Referral Engagement Rate Variance] > 0, "green", IF ( [Active Referral Engagement Rate Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-awaiting-offers-previous-month"></a>
## Active Referrals Awaiting Offers Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-151.

```dax
CALCULATE ( [Active Referrals Awaiting Offers at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-awaiting-offers-variance"></a>
## Active Referrals Awaiting Offers Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-152.

```dax
[Active Referrals Awaiting Offers at Snapshot] - [Active Referrals Awaiting Offers Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-awaiting-offers-variance-indicator"></a>
## Active Referrals Awaiting Offers Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Active Referrals Awaiting Offers Variance] > 0, "▲", IF([Active Referrals Awaiting Offers Variance]< 0, "▼", "–"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-awaiting-offers-variance-indicator-color"></a>
## Active Referrals Awaiting Offers Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Active Referrals Awaiting Offers Variance] > 0, "green", IF([Active Referrals Awaiting Offers Variance] < 0, "red", "grey"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-awaiting-offers-at-snapshot"></a>
## Active Referrals Awaiting Offers at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-150.

```dax
CALCULATE (
				[Snapshot Referrals],
				'fact_referral_snapshot'[is_open] = TRUE (),
				'fact_referral_snapshot'[is_awaiting_offer] = TRUE ()
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-active-referrals-under-offer-indicator"></a>
## Active Referrals Under Offer Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Active Referrals Under Offer Variance] > 0, "▲", IF([Active Referrals Under Offer Variance]< 0, "▼", "–"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-under-offer-previous-month"></a>
## Active Referrals Under Offer Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-154.

```dax
CALCULATE ( [Active Referrals Under Offer at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-under-offer-variance"></a>
## Active Referrals Under Offer Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-155.

```dax
[Active Referrals Under Offer at Snapshot] - [Active Referrals Under Offer Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-under-offer-variance-indicator-color"></a>
## Active Referrals Under Offer Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Active Referrals Under Offer Variance] > 0, "green", IF([Active Referrals Under Offer Variance] < 0, "red", "grey"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-active-referrals-under-offer-at-snapshot"></a>
## Active Referrals Under Offer at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-153.

```dax
CALCULATE (
				[Snapshot Referrals],
				'fact_referral_snapshot'[is_open] = TRUE (),
				'fact_referral_snapshot'[current_status] = "UNDER_OFFER"
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-active-referrals-with-provider-engagement"></a>
## Active Referrals With Provider Engagement

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-19.

```dax
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[has_provider_response] = TRUE ()
			)
```

Source tables: `gold.fact_referral`

<a id="business-active-referrals-with-provider-response-at-snapshot"></a>
## Active Referrals With Provider Response at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-156.

```dax
CALCULATE (
				[Snapshot Referrals],
				'fact_referral_snapshot'[is_open] = TRUE (),
				'fact_referral_snapshot'[has_provider_response] = TRUE ()
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-average-active-ipa-weekly-cost"></a>
## Average Active IPA Weekly Cost

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-097.

```dax
DIVIDE ( [Estimated Active Weekly Cost], [Active IPAs] )
```

Source tables: `gold.fact_ipa`

<a id="business-average-days-early"></a>
## Average Days Early

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-157.

Saved target, demand, time or cost metric

```dax
AVERAGEX ( FILTER ( 'fact_referral',
			    NOT ISBLANK ( 'fact_referral'[ipa_issued_date] ) && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
			    && 'fact_referral'[placed_by_required_date] = TRUE () ),
			    DATEDIFF ( 'fact_referral'[ipa_issued_date], 'fact_referral'[required_placement_date], DAY ) )
```

Source tables: `gold.fact_referral`

<a id="business-average-days-in-draft"></a>
## Average Days in Draft

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-59.

```dax
AVERAGEX (
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
				),
				'fact_offer'[offer_age_days]
			)
```

Source tables: `gold.fact_offer`

<a id="business-average-estimated-weekly-cost-confirmed-referrals"></a>
## Average Estimated Weekly Cost — Confirmed Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-024.

```dax
AVERAGEX (
			    FILTER (
			        'fact_referral',
			        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
			            && NOT ISBLANK ( 'fact_referral'[estimated_weekly_cost] )
			    ),
			    'fact_referral'[estimated_weekly_cost]
			)
```

Source tables: `gold.fact_referral`

<a id="business-average-lifecycle-events-per-referral"></a>
## Average Lifecycle Events per Referral

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-107.

```dax
DIVIDE ( [Referral Lifecycle Events], [Referrals With Lifecycle Activity] )
```

Source tables: `gold.fact_referral_lifecycle_event`

<a id="business-average-offers-per-provider"></a>
## Average Offers per Provider

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-057.

```dax
DIVIDE ( [Non-Draft Offers], [Providers Who Made Offers] )
```

Source tables: `gold.fact_offer`

<a id="business-average-offers-per-provider-under-offer"></a>
## Average Offers per Provider - Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-158.

```dax
DIVIDE (
			    [Offers on Referrals Under Offer],
			    [Providers With Offers on Referrals Under Offer]
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-average-offers-per-referral"></a>
## Average Offers per Referral

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-018.

```dax
DIVIDE ( [Offers Submitted], [Referrals With an Offer] )
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-average-offers-per-referral-under-offer"></a>
## Average Offers per Referral Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-13.

```dax
DIVIDE (
			    CALCULATE (
			        [Non-Draft Offers],
			        FILTER (
			            'fact_referral',
			            'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			        )
			    ),
			    [Referrals Under Offer]
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-avg-offers-per-provider-under-offer"></a>
## Avg Offers per Provider (Under Offer)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-14.

```dax
DIVIDE(
			    [Offers on Referrals Under Offer],
			    [No. Providers Who Made Offers],
			    0
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-awaiting-offer"></a>
## Awaiting offer

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-159.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([Referrals Awaiting Offer],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[Referrals Awaiting Offer])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-category-aware-open-referrals"></a>
## Category-aware open referrals

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-160.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([Referrals Currently Active],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[Referrals Currently Active])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-closed-ipas"></a>
## Closed IPAs

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-096.

```dax
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = TRUE () )
```

Source tables: `gold.fact_ipa`

<a id="business-closed-referrals"></a>
## Closed Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-003.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = FALSE () )
```

Source tables: `gold.fact_referral`

<a id="business-closed-referrals-mom-percent"></a>
## Closed Referrals MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-165.

```dax
DIVIDE ( [Closed Referrals Variance], [Closed Referrals Previous Month] )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-closed-referrals-previous-month"></a>
## Closed Referrals Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-166.

```dax
CALCULATE ( [Closed or Cancelled Referrals at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-closed-referrals-variance"></a>
## Closed Referrals Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-167.

```dax
[Closed or Cancelled Referrals at Snapshot] - [Closed Referrals Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-closed-referrals-variance-indicator"></a>
## Closed Referrals Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Closed Referrals Variance] > 0, "▲", IF ( [Closed Referrals Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-closed-referrals-variance-indicator-color"></a>
## Closed Referrals Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Closed Referrals Variance] > 0, "green", IF ( [Closed Referrals Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-closed-referrals-at-snapshot"></a>
## Closed Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-030.

```dax
CALCULATE (
			    [Snapshot Referrals],
			    FILTER (
			        'fact_referral_snapshot',
			        NOT ISBLANK ( 'fact_referral_snapshot'[referral_closed_date] )
			            && 'fact_referral_snapshot'[referral_closed_date] < 'fact_referral_snapshot'[snapshot_date] + 1
			    )
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-closed-or-cancelled-referrals"></a>
## Closed or Cancelled Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-31.

```dax
CALCULATE (
			    [Total Referrals],
			    FILTER (
			        'fact_referral',
			        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
			            IN { "closed", "cancelled", "withdrawn", "completed" }
			    )
			)
```

Source tables: `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-mom-percent"></a>
## Closed or Cancelled Referrals MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-162.

```dax
DIVIDE ( [Closed or Cancelled Referrals Variance], [Closed or Cancelled Referrals Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-previous-month"></a>
## Closed or Cancelled Referrals Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-163.

```dax
CALCULATE ( [Closed or Cancelled Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-variance"></a>
## Closed or Cancelled Referrals Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-164.

```dax
[Closed or Cancelled Referrals] - [Closed or Cancelled Referrals Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-variance-indicator"></a>
## Closed or Cancelled Referrals Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Closed or Cancelled Referrals Variance] > 0, "▲", IF ( [Closed or Cancelled Referrals Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-variance-indicator-color"></a>
## Closed or Cancelled Referrals Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Closed or Cancelled Referrals Variance] > 0, "green", IF ( [Closed or Cancelled Referrals Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-closed-or-cancelled-referrals-at-snapshot"></a>
## Closed or Cancelled Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-161.

```dax
CALCULATE (
				[Snapshot Referrals],
				FILTER (
					'fact_referral_snapshot',
					LOWER ( COALESCE ( 'fact_referral_snapshot'[current_status], "" ) )
						IN { "closed", "cancelled", "withdrawn", "completed" }
				)
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-cohort-placement-within-window"></a>
## Cohort Placement Within Window

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-168.

Saved target, demand, time or cost metric

```dax
VAR days = SELECTEDVALUE ( 'Placement Window'[Ordinal] )
			VAR eligible = FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[referral_created_date] )
			    && NOT ISBLANK ( 'fact_referral'[as_of_date] )
			    && 'fact_referral'[referral_created_date] + days <= 'fact_referral'[as_of_date] )
			VAR placed = FILTER ( eligible, NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
			    && 'fact_referral'[ipa_issued_date] >= 'fact_referral'[referral_created_date]
			    && 'fact_referral'[ipa_issued_date] <= 'fact_referral'[referral_created_date] + days )
			RETURN IF ( NOT ISBLANK ( days ), DIVIDE ( COUNTROWS ( placed ), COUNTROWS ( eligible ) ) )
```

Source tables: `gold.fact_referral`

<a id="business-completed-ipas"></a>
## Completed IPAs

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-169.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([IPA Completed],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[IPA Completed])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_referral`

<a id="business-connection-city"></a>
## Connection city

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Referral city] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-endpoint"></a>
## Connection endpoint

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Endpoint type] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-home"></a>
## Connection home

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Home] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-offer-status"></a>
## Connection offer status

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Offer status] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-postcode"></a>
## Connection postcode

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Home postcode] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-provider"></a>
## Connection provider

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Provider] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-quality"></a>
## Connection quality

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Location quality] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-referral"></a>
## Connection referral

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Referral ID] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-connection-straight-line-km"></a>
## Connection straight-line km

Model: **business**. Container: `Offer Location Paths`. Classification: **Business metric**. KPI records: GOLD-KPI-170.

Approximate record-level distance, not road distance or suitability

```dax
SELECTEDVALUE ( 'Offer Location Paths'[Distance km] )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-critical-overdue-referrals"></a>
## Critical Overdue Referrals

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-144.

Saved target, demand, time or cost metric

```dax
CALCULATE ( [Open Overdue Referrals],
			    KEEPFILTERS ( 'fact_referral'[placement_urgency_band] = "Critical" ) )
```

Source tables: `gold.fact_referral`

<a id="business-critical-target-hit-rate"></a>
## Critical Target Hit Rate

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-171.

Saved target, demand, time or cost metric

```dax
CALCULATE ( [Placement Target Hit Rate],
			    KEEPFILTERS ( 'fact_referral'[placement_urgency_band] = "Critical" ) )
```

Source tables: `gold.fact_referral`

<a id="business-current-referral-as-of"></a>
## Current Referral As Of

Model: **business**. Container: `_Design Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Reporting window, anchor or dynamic selector

```dax
MAX ( 'fact_referral'[as_of_date] )
```

Source tables: `gold.fact_referral`

<a id="business-detail-location-matches-offer"></a>
## Detail location matches offer

Model: **business**. Container: `_Story Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR offerSelected = ISFILTERED('fact_offer'[offer_id])
			VAR matchingLocations =
			    CALCULATE(
			        COUNTROWS('Referral Map Points'),
			        KEEPFILTERS(TREATAS(
			            VALUES('fact_offer'[offer_id]),
			            'Referral Map Points'[Offer]))
			    )
			RETURN IF([Detail referral selected] <> 1, BLANK(),
			    IF(NOT offerSelected,
			        IF(COUNTROWS('Referral Map Points') > 0, 1, BLANK()),
			        IF(matchingLocations > 0, 1, BLANK())))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-detail-map-points"></a>
## Detail map points

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-172.

Saved detail count in the required record context

```dax
IF([Detail referral selected] = 1, COUNTROWS('Referral Map Points'), BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-detail-referral-selected"></a>
## Detail referral selected

Model: **business**. Container: `_Story Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(COUNTROWS(ALLSELECTED('fact_referral')) = 1, 1, BLANK())
```

Source tables: `gold.fact_referral`

<a id="business-directory-summary-count"></a>
## Directory Summary Count

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-48.

```dax
SWITCH ( SELECTEDVALUE ( 'Directory Summary Axis'[Display Type] ),
			    "Fostering Providers", [Providers - Fostering],
			    "Residential Homes", [Residential Homes],
			    "Supported Accommodation Homes", [Supported Accommodation Homes],
			    BLANK ()
			)
```

Source tables: `gold.bridge_provider_framework`; `gold.dim_framework`; `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-document-expiry-status"></a>
## Document expiry status

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Expiry status only; does not certify required-document completeness.

```dax
VAR expiry = SELECTEDVALUE('dim_provider_submission_document'[expiry_date])
			RETURN IF(HASONEVALUE('dim_provider_submission_document'[document_id])
			    && COUNTROWS('dim_provider_submission_document') > 0,
			    SWITCH(TRUE(), ISBLANK(expiry), "Unknown expiry",
			        expiry < TODAY(), "Expired", expiry <= TODAY() + 30, "Expiring in 30 days", "Not expired"), BLANK())
```

<a id="business-documents-expired"></a>
## Documents Expired

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-101.

```dax
CALCULATE (
			    [Provider Submission Documents],
			    FILTER (
			        'dim_provider_submission_document',
			        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
			            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
			    )
			)
```

Source tables: `gold.dim_provider_submission_document`

<a id="business-documents-expiring-next-30-days"></a>
## Documents Expiring Next 30 Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-100.

```dax
CALCULATE (
			    [Provider Submission Documents],
			    FILTER (
			        'dim_provider_submission_document',
			        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
			            && 'dim_provider_submission_document'[expiry_date] >= TODAY ()
			            && 'dim_provider_submission_document'[expiry_date] <= TODAY () + 30
			    )
			)
```

Source tables: `gold.dim_provider_submission_document`

<a id="business-draft-no-activity-since-creation-under-offer-referrals"></a>
## Draft No Activity Since Creation (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-173.

```dax
CALCULATE (
				[Offers Submitted],
				'fact_offer'[is_draft_no_activity] = TRUE (),
				FILTER (
					'fact_referral',
					'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
				)
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-draft-offer-count-under-offer-referrals"></a>
## Draft Offer Count (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-174.

```dax
CALCULATE (
			    [Offers in Draft],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-draft-offers-missing-dates"></a>
## Draft Offers Missing Dates

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-55.

```dax
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_missing_dates] = TRUE () )
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-stalled-14-days"></a>
## Draft Offers Stalled 14+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-066.

```dax
CALCULATE (
				[Offers Submitted],
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& 'fact_offer'[days_since_offer_activity] >= 14
				)
			)
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-stalled-14-days-under-offer-referrals"></a>
## Draft Offers Stalled 14+ Days - Under Offer Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-175.

```dax
CALCULATE (
				[Draft Offers Stalled 14+ Days],
				FILTER (
					'fact_referral',
					'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
				)
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-draft-offers-stalled-7-days"></a>
## Draft Offers Stalled 7+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-020.

```dax
CALCULATE (
				[Offers Submitted],
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& 'fact_offer'[days_since_offer_activity] >= 7
				)
			)
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-with-activity-since-creation"></a>
## Draft Offers With Activity Since Creation

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-56, KPI-54.

```dax
CALCULATE (
			    [Offers in Draft],
			    KEEPFILTERS ( 'fact_offer'[is_draft_no_activity] = FALSE () ),
			    KEEPFILTERS ( 'fact_offer'[is_draft_missing_dates] = FALSE () )
			)
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-with-no-activity-percent"></a>
## Draft Offers With No Activity %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-62.

```dax
DIVIDE ( [Draft Offers With No Activity Since Creation], [Offers in Draft] )
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-with-no-activity-under-offer-referrals"></a>
## Draft Offers With No Activity - Under Offer Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-176.

```dax
CALCULATE (
				[Draft Offers With No Activity Since Creation],
				FILTER (
					'fact_referral',
					'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
				)
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-draft-offers-with-no-activity-since-creation"></a>
## Draft Offers With No Activity Since Creation

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-53.

```dax
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_no_activity] = TRUE () )
```

Source tables: `gold.fact_offer`

<a id="business-draft-offers-on-referrals-under-offer"></a>
## Draft Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-17.

```dax
CALCULATE (
			    [Offers in Draft],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-drafts-no-activity-14-days"></a>
## Drafts No Activity 14+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-58, KPI-63.

```dax
CALCULATE ( [Offers in Draft], KEEPFILTERS ( 'fact_offer'[offer_age_days] >= 14 ) )
```

Source tables: `gold.fact_offer`

<a id="business-drafts-no-activity-14-days-under-offer-referrals"></a>
## Drafts No Activity 14+ Days (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-177.

```dax
CALCULATE (
				[Offers Submitted],
				'fact_offer'[is_draft_no_activity] = TRUE (),
				'fact_offer'[days_since_offer_activity] >= 14,
				FILTER (
					'fact_referral',
					'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
				)
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-drafts-with-no-activity-since-creation-under-offer-percent"></a>
## Drafts With No Activity Since Creation (Under Offer) %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-178.

```dax
DIVIDE ( [Draft No Activity Since Creation (Under Offer Referrals)], [Draft Offer Count (Under Offer Referrals)] )
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-emergency-placement-rate"></a>
## Emergency Placement Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-92 .

```dax
DIVIDE ( [Emergency Referrals], [Total Referrals] )
```

Source tables: `gold.fact_referral`

<a id="business-emergency-referrals"></a>
## Emergency Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-91 .

```dax
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ), KEEPFILTERS ( 'fact_referral'[is_emergency_placement] = TRUE () ) )
```

Source tables: `gold.fact_referral`

<a id="business-estimated-active-weekly-cost"></a>
## Estimated Active Weekly Cost

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-107.

```dax
CALCULATE (
			    SUM ( 'fact_ipa'[estimated_weekly_cost] ),
			    'fact_ipa'[is_placement_closed] = FALSE ()
			)
```

Source tables: `gold.fact_ipa`

<a id="business-explorer-gold-accepted-offers"></a>
## Explorer Gold accepted offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-179.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[accepted_offer_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-average-response-minutes"></a>
## Explorer Gold average response minutes

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-180.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(IF(COUNTROWS('fact_provider_kpi_monthly') = 1, MAX('fact_provider_kpi_monthly'[average_response_minutes])), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-median-response-minutes"></a>
## Explorer Gold median response minutes

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-181.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(IF(COUNTROWS('fact_provider_kpi_monthly') = 1, MAX('fact_provider_kpi_monthly'[median_response_minutes])), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-offer-acceptance-rate"></a>
## Explorer Gold offer acceptance rate

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-182.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer Gold accepted offers],[Explorer Gold offers])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-offers"></a>
## Explorer Gold offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-183.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[offers_submitted_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-opportunities"></a>
## Explorer Gold opportunities

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-184.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[response_opportunity_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-placed-by-target"></a>
## Explorer Gold placed by target

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-185.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[placed_by_target_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-response-rate"></a>
## Explorer Gold response rate

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-186.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer Gold responses],[Explorer Gold opportunities])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-responses"></a>
## Explorer Gold responses

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-187.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[qualifying_response_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-successful-referrals"></a>
## Explorer Gold successful referrals

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-188.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('fact_provider_kpi_monthly'[successful_referral_count]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-gold-target-placement-rate"></a>
## Explorer Gold target placement rate

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-189.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer Gold placed by target],[Explorer Gold successful referrals])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-provider-ipas"></a>
## Explorer provider IPAs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-198.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home') VAR homes = VALUES('dim_provider_home'[provider_home_id]) VAR offers = CALCULATETABLE(VALUES('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))) RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(TREATAS(offers,'fact_ipa'[accepted_offer_id])), KEEPFILTERS(FILTER('fact_ipa', TRUE()))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-accepted-offers"></a>
## Explorer provider accepted offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-190.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR homes = VALUES('dim_provider_home'[provider_home_id])
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful"}))), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-assigned-referrals"></a>
## Explorer provider assigned referrals

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-191.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-assignment-row-visible"></a>
## Explorer provider assignment row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF([Explorer provider row visible] = 1 && COUNTROWS('fact_referral_provider') > 0, 1, BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-assignment-table-title"></a>
## Explorer provider assignment table title

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR visibleRows = FILTER(
			    SUMMARIZE(
			        'fact_referral_provider',
			        'fact_referral'[referral_id],
			        'dim_provider'[provider_id],
			        'dim_provider'[provider_name],
			        'fact_referral_provider'[referral_id],
			        'fact_referral_provider'[provider_response_status],
			        'fact_referral_provider'[assigned_at],
			        'fact_referral_provider'[first_qualifying_response_at],
			        'fact_referral_provider'[response_elapsed_minutes],
			        'fact_referral_provider'[is_engaged]
			    ),
			    CALCULATE([Explorer provider assignment row visible]) = 1
			)
			VAR providerJourney = IF(HASONEVALUE('dim_provider'[provider_id]), [Rail provider cohort label])
			RETURN "Referral assignment and response evidence" & SWITCH(TRUE(), ISEMPTY(visibleRows), " - No rows to return", NOT ISBLANK(providerJourney), " - " & providerJourney, "")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-explorer-provider-assignments"></a>
## Explorer provider assignments

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-192.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-average-response-minutes"></a>
## Explorer provider average response minutes

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-193.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(AVERAGE('fact_referral_provider'[response_elapsed_minutes]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-beds"></a>
## Explorer provider beds

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-194.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(SUM('dim_provider_home'[registered_beds]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-completed-ipas"></a>
## Explorer provider completed IPAs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-195.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home') VAR homes = VALUES('dim_provider_home'[provider_home_id]) VAR offers = CALCULATETABLE(VALUES('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))) RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(TREATAS(offers,'fact_ipa'[accepted_offer_id])), KEEPFILTERS(FILTER('fact_ipa', 'fact_ipa'[is_ipa_completed] == TRUE()))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-documents"></a>
## Explorer provider documents

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-327.

Existing expiry aggregation restricted to the current eligible provider selection; existing home join requires owner validation.

```dax
VAR eligible = FILTER(VALUES('dim_provider'[provider_id]),
			    NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Explorer provider row visible]) = 1)
			RETURN CALCULATE([Provider Submission Documents], KEEPFILTERS(eligible))
```

<a id="business-explorer-provider-documents-expired"></a>
## Explorer provider documents expired

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-328.

Existing expiry aggregation restricted to the current eligible provider selection; existing home join requires owner validation.

```dax
VAR eligible = FILTER(VALUES('dim_provider'[provider_id]),
			    NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Explorer provider row visible]) = 1)
			RETURN CALCULATE([Documents Expired], KEEPFILTERS(eligible))
```

<a id="business-explorer-provider-documents-expiring-30-days"></a>
## Explorer provider documents expiring 30 days

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-329.

Existing expiry aggregation restricted to the current eligible provider selection; existing home join requires owner validation.

```dax
VAR eligible = FILTER(VALUES('dim_provider'[provider_id]),
			    NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Explorer provider row visible]) = 1)
			RETURN CALCULATE([Documents Expiring Next 30 Days], KEEPFILTERS(eligible))
```

<a id="business-explorer-provider-drafts"></a>
## Explorer provider drafts

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-196.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR homes = VALUES('dim_provider_home'[provider_home_id])
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) = "draft"))), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-homes"></a>
## Explorer provider homes

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-197.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_provider_home'[provider_home_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-homes-with-expired-documents"></a>
## Explorer provider homes with expired documents

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-330.

Existing expiry aggregation restricted to the current eligible provider selection; existing home join requires owner validation.

```dax
VAR eligible = FILTER(VALUES('dim_provider'[provider_id]),
			    NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Explorer provider row visible]) = 1)
			RETURN CALCULATE([Provider Homes With Expired Documents], KEEPFILTERS(eligible))
```

<a id="business-explorer-provider-median-response-minutes"></a>
## Explorer provider median response minutes

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-199.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(MEDIAN('fact_referral_provider'[response_elapsed_minutes]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-message-row-visible"></a>
## Explorer provider message row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF([Explorer provider row visible] = 1 && COUNTROWS('dim_referral_provider_message') > 0, 1, BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-messages"></a>
## Explorer provider messages

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-200.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_referral_provider_message'[message_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-monthly-row-visible"></a>
## Explorer provider monthly row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF([Explorer provider row visible] = 1 && COUNTROWS('fact_provider_kpi_monthly') > 0, 1, BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-explorer-provider-offer-acceptance-rate"></a>
## Explorer provider offer acceptance rate

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-201.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer provider accepted offers],[Explorer provider offers made])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-offer-row-visible"></a>
## Explorer provider offer row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF (
			    COUNTROWS ( 'fact_offer' ) > 0,
			    IF (
			        [Explorer provider row visible] = 1,
			        1,
			        BLANK ()
			    ),
			    BLANK ()
			)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-offer-table-title"></a>
## Explorer provider offer table title

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR visibleRows = FILTER(
			    SUMMARIZE(
			        'fact_offer',
			        'fact_referral'[referral_id],
			        'dim_provider'[provider_id],
			        'dim_provider'[provider_name],
			        'fact_offer'[referral_id],
			        'fact_offer'[offer_id],
			        'fact_offer'[offer_status],
			        'fact_offer'[offer_submitted_date],
			        'fact_offer'[offer_decision_date],
			        'fact_offer'[estimated_weekly_cost],
			        'dim_provider_home (offer)'[home_name]
			    ),
			    CALCULATE([Explorer provider offer row visible]) = 1
			)
			VAR providerJourney = IF(HASONEVALUE('dim_provider'[provider_id]), [Rail provider cohort label])
			RETURN "Offer records and proposed homes" & SWITCH(TRUE(), ISEMPTY(visibleRows), " - No rows to return", NOT ISBLANK(providerJourney), " - " & providerJourney, "")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-explorer-provider-offers"></a>
## Explorer provider offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-202.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR homes = VALUES('dim_provider_home'[provider_home_id])
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-offers-made"></a>
## Explorer provider offers made

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-203.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR homes = VALUES('dim_provider_home'[provider_home_id])
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', NOT ISBLANK('fact_offer'[offer_status]) && LOWER(TRIM('fact_offer'[offer_status])) <> "draft"))), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-pending-offers"></a>
## Explorer provider pending offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-204.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR homes = VALUES('dim_provider_home'[provider_home_id])
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"pending", "submitted", "offered", "offer_made", "offer_pending", "under_review", "under review", "awaiting", "awaiting_decision", "awaiting decision"}))), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-qualifying-responses"></a>
## Explorer provider qualifying responses

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-205.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS('fact_referral_provider'[has_qualifying_response] == TRUE())), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-response-rate"></a>
## Explorer provider response rate

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-206.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer provider qualifying responses],[Explorer provider assignments])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-row-visible"></a>
## Explorer provider row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
			VAR homeFilter = ISFILTERED('dim_provider_home')
			VAR matchingHomes = CALCULATE(COUNTROWS('dim_provider_home'))
			VAR stage = SELECTEDVALUE('Journey Provider Selection'[Stage], -1)
			RETURN IF(NOT ISBLANK(providerKey) && (NOT homeFilter || matchingHomes > 0) && [Provider matches offer status] = 1 && (stage = -1 || [Journey provider stage] == stage), 1, BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-provider-signed-ipas"></a>
## Explorer provider signed IPAs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-207.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR homeFilter = ISFILTERED('dim_provider_home') VAR homes = VALUES('dim_provider_home'[provider_home_id]) VAR offers = CALCULATETABLE(VALUES('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))) RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(TREATAS(offers,'fact_ipa'[accepted_offer_id])), KEEPFILTERS(FILTER('fact_ipa', 'fact_ipa'[signed_by_provider] == TRUE()))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-providers"></a>
## Explorer providers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-208.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_provider'[provider_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-providers-without-offers"></a>
## Explorer providers without offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-209.

Explorer or detail metric with its saved selection context

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), CALCULATE([Explorer provider offers]) = 0)), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-explorer-referral-ipas"></a>
## Explorer referral IPAs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-213.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-accepted-offers"></a>
## Explorer referral accepted offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-210.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(CALCULATE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer',LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful"}))),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-assignments"></a>
## Explorer referral assignments

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-211.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-explorer-referral-completed-ipas"></a>
## Explorer referral completed IPAs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-212.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(CALCULATE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]), KEEPFILTERS('fact_ipa'[is_ipa_completed] == TRUE())),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-messages"></a>
## Explorer referral messages

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-214.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_referral_provider_message'[message_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-offer-coverage"></a>
## Explorer referral offer coverage

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-215.

Explorer or detail metric with its saved selection context

```dax
DIVIDE([Explorer referrals with offers],[Explorer referrals])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-offers"></a>
## Explorer referral offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-216.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referral-row-visible"></a>
## Explorer referral row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN IF(COUNTROWS(eligible) > 0, 1, BLANK())
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals"></a>
## Explorer referrals

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-217.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals-closed"></a>
## Explorer referrals closed

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-218.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0), KEEPFILTERS(FILTER('fact_referral',LOWER(TRIM('fact_referral'[current_status])) IN {"closed","cancelled","canceled","withdrawn","completed"}))), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals-open"></a>
## Explorer referrals open

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-219.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0), KEEPFILTERS(FILTER('fact_referral','fact_referral'[is_open] == TRUE()))), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals-open-overdue"></a>
## Explorer referrals open overdue

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-220.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0), KEEPFILTERS(FILTER('fact_referral','fact_referral'[is_open_overdue] == TRUE()))), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals-with-offers"></a>
## Explorer referrals with offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-221.

Explorer or detail metric with its saved selection context

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[referral_id]),0), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-explorer-referrals-without-offers"></a>
## Explorer referrals without offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-222.

Explorer or detail metric with its saved selection context

```dax
[Explorer referrals] - [Explorer referrals with offers]
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-female-referrals"></a>
## Female Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-05, GOLD-KPI-111.

```dax
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Female" )
```

Source tables: `gold.dim_person`; `gold.fact_referral`

<a id="business-fostering-homes"></a>
## Fostering Homes

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-083.

```dax
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Fostering" )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-framework-offers-under-offer-referrals"></a>
## Framework Offers (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-38.

```dax
// Preserve the original non-Spot fallback for blank/unmatched home flags.
			// These offers are not evidence of affirmative framework membership.
			VAR qualifyingOffers = [Offers on Referrals Under Offer]
			VAR spotOffers = COALESCE ( [Spot Offers on Referrals Under Offer], 0 )
			RETURN
			    IF ( ISBLANK ( qualifyingOffers ), BLANK (), qualifyingOffers - spotOffers )
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-framework-offers-on-referrals-under-offer"></a>
## Framework Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-223.

```dax
CALCULATE (
			    [Non-Spot Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-framework-providers"></a>
## Framework Providers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-45.

```dax
DISTINCTCOUNT(bridge_provider_framework[provider_id])
```

Source tables: `gold.bridge_provider_framework`

<a id="business-gold-model-last-refreshed"></a>
## Gold Model Last Refreshed

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-87.

```dax
MAX ( 'fact_referral'[gold_modelled_at] )
```

Source tables: `gold.fact_referral`

<a id="business-homes-offered"></a>
## Homes Offered

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-143.

Saved target, demand, time or cost metric

```dax
CALCULATE ( DISTINCTCOUNT ( 'fact_offer'[provider_home_id] ),
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[provider_home_id] ) && 'fact_offer'[provider_home_id] <> "" ) ) )
```

Source tables: `gold.fact_offer`

<a id="business-ipa-complete-referral"></a>
## IPA Complete referral

Model: **business**. Container: `_Explore Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Record eligibility helper

```dax
CALCULATE([Referrals], KEEPFILTERS ( fact_referral[ipa_2_signatures] = TRUE () ) )
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-ipa-completed"></a>
## IPA Completed

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-77, GOLD-KPI-114.

```dax
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-ipa-created-to-completion-percent"></a>
## IPA Created to Completion %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-85.

```dax
DIVIDE ( [IPA Completed], [IPAs Created] )
```

Source tables: `gold.fact_ipa`

<a id="business-ipa-exists"></a>
## IPA Exists

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-73.

Legacy presentation, flag or row-filter expression

```dax
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ) ) > 0, "Yes", "No" ),
			    IF ( [IPAs Created] > 0, "Yes", "No" )
			)
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-ipa-signature-completion-rate"></a>
## IPA Signature Completion Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-114.

```dax
DIVIDE ( [IPA Completed], [IPAs Created] )
```

Source tables: `gold.fact_ipa`

<a id="business-ipa-signature-pending-rate"></a>
## IPA Signature Pending Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-224.

```dax
DIVIDE ( [IPAs Pending Completion], [IPAs Created] )
```

Source tables: `gold.fact_ipa`

<a id="business-ipas-created"></a>
## IPAs Created

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-76.

```dax
DISTINCTCOUNT ( 'fact_ipa'[ipa_id] )
```

Source tables: `gold.fact_ipa`

<a id="business-ipas-issued-this-month"></a>
## IPAs Issued This Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-095.

```dax
VAR as_of = MAX ( 'fact_ipa'[as_of_date] )
			RETURN IF ( NOT ISBLANK ( as_of ),
			    CALCULATE ( [IPAs Created],
			        CROSSFILTER ( 'dim_date'[date], 'fact_referral'[referral_created_date], NONE ),
			        USERELATIONSHIP ( 'dim_date'[date], 'fact_ipa'[ipa_issued_date] ),
			        DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of )
			    )
			)
```

Source tables: `gold.dim_date`; `gold.fact_ipa`; `gold.fact_referral`

<a id="business-ipas-pending-completion"></a>
## IPAs Pending Completion

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-78, GOLD-KPI-115.

```dax
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_pending] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-ipas-signed-by-local-authority"></a>
## IPAs Signed by Local Authority

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-117.

```dax
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[signed_by_local_authority] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-ipas-signed-by-provider"></a>
## IPAs Signed by Provider

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-116.

```dax
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[signed_by_provider] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-is-awaiting-ipa-creation"></a>
## Is Awaiting IPA Creation

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-81.

Legacy presentation, flag or row-filter expression

```dax
IF ( COALESCE ( SELECTEDVALUE ( 'fact_offer'[is_awaiting_ipa_creation] ), FALSE () ), 1, 0 )
```

Source tables: `gold.fact_offer`

<a id="business-is-ipa-completed"></a>
## Is IPA Completed

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-82.

Legacy presentation, flag or row-filter expression

```dax
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_completed] = TRUE () ) > 0, 1, 0 ),
			    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_completed], FALSE () ), 1, 0 )
			)
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-is-ipa-pending"></a>
## Is IPA Pending

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-80.

Legacy presentation, flag or row-filter expression

```dax
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_pending] = TRUE () ) > 0, 1, 0 ),
			    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_pending], FALSE () ), 1, 0 )
			)
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-is-in-accepted-kpi"></a>
## Is In Accepted KPI

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-74.

Legacy presentation, flag or row-filter expression

```dax
IF (
			    LOWER ( COALESCE ( SELECTEDVALUE ( 'fact_offer'[offer_status] ), "" ) ) IN { "accepted", "approved", "selected", "offer_successful" },
			    "Yes",
			    "No"
			)
```

Source tables: `gold.fact_offer`

<a id="business-is-non-framework-provider"></a>
## Is Non Framework Provider

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: KPI-47.

Legacy presentation, flag or row-filter expression

```dax
IF ( CALCULATE ( COUNTROWS ( 'bridge_provider_framework' ) ) = 0, 1, 0 )
```

Source tables: `gold.bridge_provider_framework`

<a id="business-journey-current-position"></a>
## Journey current position

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(NOT HASONEVALUE('fact_referral'[referral_id]), "Select one referral to see its journey",
			"Current position: " & SELECTEDVALUE('fact_referral'[Journey stage]) &
			IF(SELECTEDVALUE('fact_referral'[is_open_overdue]) == TRUE(), " | Overdue", ""))
```

Source tables: `gold.fact_referral`

<a id="business-journey-detail-colour-1"></a>
## Journey detail colour 1

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 1, "#FCA356", IF([Journey detail evidence 1] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_referral`

<a id="business-journey-detail-colour-2"></a>
## Journey detail colour 2

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 2, "#FCA356", IF([Journey detail evidence 2] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-journey-detail-colour-3"></a>
## Journey detail colour 3

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 3, "#FCA356", IF([Journey detail evidence 3] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-colour-4"></a>
## Journey detail colour 4

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 4, "#FCA356", IF([Journey detail evidence 4] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-colour-5"></a>
## Journey detail colour 5

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 5, "#FCA356", IF([Journey detail evidence 5] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-detail-colour-6"></a>
## Journey detail colour 6

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF([Journey selected stage] = 6, "#FCA356", IF([Journey detail evidence 6] = 1, "#E4F1E9", "#F0EBE7"))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-detail-evidence-1"></a>
## Journey detail evidence 1

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(NOT ISBLANK(SELECTEDVALUE('fact_referral'[referral_created_date])), 1, 0))
```

Source tables: `gold.fact_referral`

<a id="business-journey-detail-evidence-2"></a>
## Journey detail evidence 2

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(COUNTROWS('fact_referral_provider') > 0, 1, 0))
```

Source tables: `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-journey-detail-evidence-3"></a>
## Journey detail evidence 3

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful", "pending", "submitted", "offered", "offer_made", "offer_pending", "under_review", "under review", "awaiting", "awaiting_decision", "awaiting decision", "declined", "rejected", "withdrawn", "closed", "cancelled", "canceled", "offer_unsuccessful", "unsuccessful"})) > 0, 1, 0))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-evidence-4"></a>
## Journey detail evidence 4

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful"})) > 0, 1, 0))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-evidence-5"></a>
## Journey detail evidence 5

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(COUNTROWS('fact_ipa') > 0, 1, 0))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-detail-evidence-6"></a>
## Journey detail evidence 6

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), IF(COUNTROWS(FILTER('fact_ipa', 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0, 1, 0))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-detail-label-1"></a>
## Journey detail label 1

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 1]
			VAR stamp = SELECTEDVALUE('fact_referral'[referral_created_date])
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 1, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy")),
			"Not evidenced"))
```

Source tables: `gold.fact_referral`

<a id="business-journey-detail-label-2"></a>
## Journey detail label 2

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 2]
			VAR stamp = BLANK()
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 2, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy")),
			"Not evidenced"))
```

Source tables: `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-journey-detail-label-3"></a>
## Journey detail label 3

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 3]
			VAR stamp = MINX(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful", "pending", "submitted", "offered", "offer_made", "offer_pending", "under_review", "under review", "awaiting", "awaiting_decision", "awaiting decision", "declined", "rejected", "withdrawn", "closed", "cancelled", "canceled", "offer_unsuccessful", "unsuccessful"}), 'fact_offer'[offer_submitted_date])
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 3, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy")),
			"Not evidenced"))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-label-4"></a>
## Journey detail label 4

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 4]
			VAR stamp = SELECTEDVALUE('fact_referral'[offer_accepted_date])
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 4, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy") & " (proxy)"),
			"Not evidenced"))
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-detail-label-5"></a>
## Journey detail label 5

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 5]
			VAR stamp = MIN('fact_ipa'[ipa_issued_date])
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 5, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy")),
			"Not evidenced"))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-detail-label-6"></a>
## Journey detail label 6

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey selected stage]
			VAR evidence = [Journey detail evidence 6]
			VAR stamp = BLANK()
			RETURN IF(ISBLANK(stage), "Select one referral",
			IF(evidence = 1,
			IF(stage = 6, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy")),
			"Not evidenced"))
```

Source tables: `gold.fact_ipa`; `gold.fact_referral`

<a id="business-journey-next-action"></a>
## Journey next action

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
SWITCH([Journey selected stage],
			1,"Next: assign providers and begin the search.",
			2,"Next: seek suitable offers; declined or withdrawn offers remain in the activity history.",
			3,"Next: review the available offers and record the decision.",
			4,"Next: prepare the IPA for the selected offer.",
			5,"Next: complete provider and local-authority signatures on the same IPA.",
			6,"Next: confirm admission separately. A planned admission date is not proof of placement start.",
			7,"Referral closed: retain its recorded reason and milestone evidence; closure does not prove placement.",
			8,"Review missing or unrecognised status evidence before assigning a stage.",
			"The pathway requires a single referral selection.")
```

Source tables: `gold.fact_referral`

<a id="business-journey-provider-coverage"></a>
## Journey provider coverage

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
"Assigned / draft / unclear: " & FORMAT([Journey providers 0], "#,0") & "     |     Both parties signed (subset): " & FORMAT([Journey providers both signed], "#,0")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-provider-label"></a>
## Journey provider label

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR stage = [Journey provider stage] RETURN IF(ISBLANK(stage), BLANK(), SWITCH(stage, 0,"Assigned / draft / unclear",1,"Message activity only",2,"Offers made",3,"Offer accepted",5,"Provider signed",BLANK()))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-provider-stage"></a>
## Journey provider stage

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
VAR homeScope = ISFILTERED('dim_provider_home')
			VAR matchingHomes = CALCULATE(COUNTROWS('dim_provider_home'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]), 'dim_provider_home'[provider_id])))
			VAR assignments = COUNTROWS('fact_referral_provider')
			VAR messages = COUNTROWS('dim_referral_provider_message')
			VAR offers = FILTER('fact_offer', NOT ISBLANK('fact_offer'[provider_id]))
			VAR offerIDs = SELECTCOLUMNS(offers, "OfferKey", 'fact_offer'[offer_id])
			VAR ipas = CALCULATETABLE('fact_ipa', KEEPFILTERS(TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])))
			VAR signed = COUNTROWS(FILTER(ipas, 'fact_ipa'[signed_by_provider] == TRUE())) > 0
			VAR accepted = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful"})) > 0
			VAR submitted = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful", "pending", "submitted", "offered", "offer_made", "offer_pending", "under_review", "under review", "awaiting", "awaiting_decision", "awaiting decision", "declined", "rejected", "withdrawn", "closed", "cancelled", "canceled", "offer_unsuccessful", "unsuccessful"})) > 0
			RETURN IF(NOT HASONEVALUE('dim_provider'[provider_id]) || (homeScope && matchingHomes = 0), BLANK(),
			SWITCH(TRUE(), signed, 5, accepted, 3, submitted, 2, messages > 0, 1, assignments > 0 || COUNTROWS(offers) > 0, 0, BLANK()))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-0"></a>
## Journey providers 0

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-131.

Saved stage count; current state, not historical conversion

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 0)), 0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-1"></a>
## Journey providers 1

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-132.

Saved stage count; current state, not historical conversion

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 1)), 0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-2"></a>
## Journey providers 2

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-133.

Saved stage count; current state, not historical conversion

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 2)), 0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-3"></a>
## Journey providers 3

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-134.

Saved stage count; current state, not historical conversion

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 3)), 0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-4"></a>
## Journey providers 4

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
"Not captured"
```

Source tables: No direct physical source asserted.

<a id="business-journey-providers-5"></a>
## Journey providers 5

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-135.

Saved stage count; current state, not historical conversion

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 5)), 0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-journey-providers-both-signed"></a>
## Journey providers both signed

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: GOLD-KPI-136.

Stage selector, evidence flag, narrative or colour

```dax
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]),
			VAR offerIDs = CALCULATETABLE(VALUES('fact_offer'[offer_id]))
			VAR signedIPAs = CALCULATETABLE('fact_ipa', KEEPFILTERS(TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])))
			RETURN NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && COUNTROWS(FILTER(signedIPAs, 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0)),0)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_ipa`; `gold.fact_offer`

<a id="business-journey-referral-exceptions"></a>
## Journey referral exceptions

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
"Closed / cancelled / withdrawn: " & FORMAT([Journey referrals 7], "#,0") & "     |     Needs review: " & FORMAT([Journey referrals 8], "#,0") & "     |     Matching referrals: " & FORMAT(COALESCE([Matching referrals],0), "#,0")
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referral-reconciliation"></a>
## Journey referral reconciliation

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-225.

Linked activity or stage reconciliation count

```dax
[Matching referrals] - ([Journey referrals 1] + [Journey referrals 2] + [Journey referrals 3] + [Journey referrals 4] + [Journey referrals 5] + [Journey referrals 6] + [Journey referrals 7] + [Journey referrals 8])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-1"></a>
## Journey referrals 1

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-123.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 1)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-2"></a>
## Journey referrals 2

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-124.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 2)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-3"></a>
## Journey referrals 3

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-125.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 3)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-4"></a>
## Journey referrals 4

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-126.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 4)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-5"></a>
## Journey referrals 5

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-127.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 5)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-6"></a>
## Journey referrals 6

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-128.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 6)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-7"></a>
## Journey referrals 7

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-129.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 7)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-referrals-8"></a>
## Journey referrals 8

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-130.

Saved stage count; current state, not historical conversion

```dax
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 8)), 0)
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-journey-selected-stage"></a>
## Journey selected stage

Model: **business**. Container: `_Journey Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Stage selector, evidence flag, narrative or colour

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), SELECTEDVALUE('fact_referral'[Journey stage order]))
```

Source tables: `gold.fact_referral`

<a id="business-kpi-tooltip-style-1"></a>
## KPI Tooltip Style 1

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
VAR SelectKPI = SELECTEDVALUE('KPI Selector'[KPI Selector Fields])
			 RETURN LOOKUPVALUE('ref_KPI'[ref FR IDs], 'ref_KPI'[KPI Description],SelectKPI)
```

Source tables: No direct physical source asserted.

<a id="business-kpis-catalogued"></a>
## KPIs catalogued

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-226.

Action metric, scoring evidence component or catalogue count

```dax
DISTINCTCOUNTNOBLANK('ref_KPI'[KPI ID])
```

Source tables: No direct physical source asserted.

<a id="business-last-snapshot-date"></a>
## Last Snapshot Date

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-227.

```dax
MAX ( 'fact_referral_snapshot'[snapshot_date] )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-latest-offer-source-export"></a>
## Latest Offer Source Export

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-88.

```dax
MAX ( 'fact_offer'[source_export_date] )
```

Source tables: `gold.fact_offer`

<a id="business-lifetime-placement-cost"></a>
## Lifetime Placement Cost

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-228.

```dax
SUMX (
				'fact_ipa',
				VAR start_date =
					COALESCE (
						'fact_ipa'[planned_placement_start_date],
						'fact_ipa'[placement_admission_date]
					)
				VAR end_date = COALESCE ( 'fact_ipa'[placement_ended_date], TODAY () )
				RETURN
					DIVIDE ( DATEDIFF ( start_date, end_date, DAY ) + 1, 7 )
						* 'fact_ipa'[estimated_weekly_cost]
			)
```

Source tables: `gold.fact_ipa`

<a id="business-linked-assignment-count"></a>
## Linked assignment count

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Business metric**. KPI records: GOLD-KPI-229.

Linked-pair activity/count with the current candidate and cancellation rules

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CALCULATE(
			        DISTINCTCOUNT('fact_referral_provider'[referral_provider_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]))
			    ), 0))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-debug"></a>
## Linked debug

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Linked-row visibility, debug or detail text

```dax
VAR searchDetected =
			    ISFILTERED ( 'dim_provider'[provider_name] )
			        || ISFILTERED ( 'dim_provider'[provider_id] )

			VAR searchedProviders =
			    VALUES ( 'dim_provider'[provider_id] )

			VAR searchedReferrals =
			    FILTER (
			        DISTINCT (
			            UNION (
			                VALUES ( 'fact_referral_provider'[referral_id] ),
			                VALUES ( 'fact_offer'[referral_id] )
			            )
			        ),
			        NOT ISBLANK ( [referral_id] )
			    )

			VAR candidatePairs =
			    CALCULATETABLE (
			        'Linked Provider Referrals',
			        REMOVEFILTERS ( 'dim_provider' )
			    )

			VAR otherPairs =
			    FILTER (
			        candidatePairs,
			        'Linked Provider Referrals'[referral_id] IN searchedReferrals
			            && NOT (
			                'Linked Provider Referrals'[provider_id]
			                    IN searchedProviders
			            )
			    )

			RETURN
			    "Search: " & IF ( searchDetected, "Yes", "No" )
			        & " | Providers: "
			        & FORMAT ( COALESCE ( COUNTROWS ( searchedProviders ), 0 ), "0" )
			        & " | Referrals: "
			        & FORMAT ( COALESCE ( COUNTROWS ( searchedReferrals ), 0 ), "0" )
			        & " | Other pairs: "
			        & FORMAT ( COALESCE ( COUNTROWS ( otherPairs ), 0 ), "0" )
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-latest-message"></a>
## Linked latest message

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Linked-row visibility, debug or detail text

```dax
VAR isSinglePair =
			    HASONEVALUE('Linked Provider Referrals'[referral_id])
			    && HASONEVALUE('Linked Provider Referrals'[provider_id])
			VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			VAR assignmentIds =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[referral_provider_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]))
			    )
			VAR latestMessage =
			    CALCULATETABLE(
			        TOPN(1, 'dim_referral_provider_message',
			            'dim_referral_provider_message'[created_timestamp], DESC,
			            'dim_referral_provider_message'[message_id], DESC),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(assignmentIds,
			            'dim_referral_provider_message'[referral_provider_id]))
			    )
			RETURN IF(isSinglePair && COUNTROWS(linkedPairs) > 0,
			    COALESCE(CONCATENATEX(
			        latestMessage,
			        FORMAT('dim_referral_provider_message'[created_timestamp], "dd MMM yyyy HH:mm")
			        & " — "
			        & LEFT(COALESCE('dim_referral_provider_message'[message_text],
			            "(No message text)"), 150),
			        ""
			    ), "No messages in scope"))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-message-count"></a>
## Linked message count

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Business metric**. KPI records: GOLD-KPI-230.

Linked-pair activity/count with the current candidate and cancellation rules

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			VAR assignmentIds =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[referral_provider_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]))
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CALCULATE(
			        DISTINCTCOUNT('dim_referral_provider_message'[message_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(assignmentIds,
			            'dim_referral_provider_message'[referral_provider_id]))
			    ), 0))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-offer-count"></a>
## Linked offer count

Model: **business**. Container: `_Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-231.

Linked activity or stage reconciliation count

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CALCULATE(
			        DISTINCTCOUNT('fact_offer'[offer_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_offer'[referral_id], 'fact_offer'[provider_id]))
			    ), 0))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-offer-statuses"></a>
## Linked offer statuses

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Linked-row visibility, debug or detail text

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			VAR statusValues =
			    CALCULATETABLE(
			        VALUES('fact_offer'[offer_status]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_offer'[referral_id], 'fact_offer'[provider_id]))
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CONCATENATEX(
			        statusValues,
			        COALESCE('fact_offer'[offer_status], "(Unknown status)"),
			        ", ",
			        'fact_offer'[offer_status], ASC
			    ), "No offers in scope"))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-provider-row-visible"></a>
## Linked provider row visible

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Linked-row visibility, debug or detail text

```dax
VAR hasProviderSearch =
			    ISFILTERED('dim_provider'[provider_name])
			    || ISFILTERED('dim_provider'[provider_id])
			VAR searchedProviderIds = VALUES('dim_provider'[provider_id])
			VAR cancelledReferralIds =
			    CALCULATETABLE(
			        SELECTCOLUMNS(FILTER('fact_referral',
			            UPPER(TRIM(COALESCE('fact_referral'[current_status], ""))) = "CANCELLED"),
			            "referral_id", 'fact_referral'[referral_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        REMOVEFILTERS('fact_referral'[current_status])
			    )
			VAR cancelledResponsePairs =
			    CALCULATETABLE(
			        SUMMARIZE(FILTER('fact_referral_provider',
			            UPPER(TRIM(COALESCE('fact_referral_provider'[provider_response_status], ""))) = "CANCELLED"),
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        REMOVEFILTERS('fact_referral_provider'[provider_response_status])
			    )
			VAR eligibleSearchedPairs =
			    EXCEPT(
			        FILTER(
			            CALCULATETABLE(
			                SUMMARIZE('Linked Provider Referrals',
			                    'Linked Provider Referrals'[referral_id],
			                    'Linked Provider Referrals'[provider_id]),
			                REMOVEFILTERS('Linked Provider Referrals'),
			                REMOVEFILTERS('dim_provider')
			            ),
			            'Linked Provider Referrals'[provider_id] IN searchedProviderIds
			            && NOT ('Linked Provider Referrals'[referral_id] IN cancelledReferralIds)
			        ),
			        cancelledResponsePairs
			    )
			VAR searchedAssignmentIds =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[referral_provider_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(eligibleSearchedPairs,
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]))
			    )
			VAR searchedMessageAssignmentIds =
			    CALCULATETABLE(
			        VALUES('dim_referral_provider_message'[referral_provider_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(searchedAssignmentIds,
			            'dim_referral_provider_message'[referral_provider_id]))
			    )
			VAR messagedReferralIds =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[referral_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(searchedProviderIds, 'fact_referral_provider'[provider_id])),
			        KEEPFILTERS(TREATAS(searchedMessageAssignmentIds,
			            'fact_referral_provider'[referral_provider_id]))
			    )
			VAR offeredReferralIds =
			    CALCULATETABLE(
			        VALUES('fact_offer'[referral_id]),
			        REMOVEFILTERS('Linked Provider Referrals'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(eligibleSearchedPairs,
			            'fact_offer'[referral_id], 'fact_offer'[provider_id]))
			    )
			VAR searchedReferralIds =
			    FILTER(DISTINCT(UNION(messagedReferralIds, offeredReferralIds)),
			        NOT ISBLANK([referral_id]))
			VAR linkedProviderId = SELECTEDVALUE('Linked Provider Referrals'[provider_id])
			VAR cancelledLinkedReferralIds =
			    SELECTCOLUMNS(FILTER(cancelledResponsePairs,
			        'fact_referral_provider'[provider_id] == linkedProviderId),
			        "referral_id", 'fact_referral_provider'[referral_id])
			VAR sharedReferralIds =
			    EXCEPT(
			        INTERSECT(VALUES('Linked Provider Referrals'[referral_id]), searchedReferralIds),
			        cancelledLinkedReferralIds
			    )
			VAR linkedOffers =
			    CALCULATE(
			        COUNTROWS('fact_offer'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS({linkedProviderId}, 'fact_offer'[provider_id])),
			        KEEPFILTERS(TREATAS(sharedReferralIds, 'fact_offer'[referral_id]))
			    )
			VAR linkedAssignmentIds =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[referral_provider_id]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS({linkedProviderId}, 'fact_referral_provider'[provider_id])),
			        KEEPFILTERS(TREATAS(sharedReferralIds, 'fact_referral_provider'[referral_id]))
			    )
			VAR linkedMessages =
			    CALCULATE(
			        COUNTROWS('dim_referral_provider_message'),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedAssignmentIds,
			            'dim_referral_provider_message'[referral_provider_id]))
			    )
			RETURN IF(
			    hasProviderSearch
			    && NOT ISBLANK(linkedProviderId)
			    && NOT (linkedProviderId IN searchedProviderIds)
			    && COUNTROWS(sharedReferralIds) > 0
			    && (linkedOffers > 0 || linkedMessages > 0),
			    1,
			    BLANK()
			)
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-providers-in-selection"></a>
## Linked providers in selection

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Business metric**. KPI records: GOLD-KPI-232.

Linked-pair activity/count with the current candidate and cancellation rules

```dax
VAR hasProviderSearch =
			    ISFILTERED('dim_provider'[provider_name])
			    || ISFILTERED('dim_provider'[provider_id])
			RETURN IF(hasProviderSearch,
			    COALESCE(COUNTROWS(FILTER(
			        VALUES('Linked Provider Referrals'[provider_id]),
			        NOT ISBLANK('Linked Provider Referrals'[provider_id])
			        && CALCULATE([Linked provider row visible]) = 1
			    )), 0), 0)
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-linked-response-statuses"></a>
## Linked response statuses

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Linked-row visibility, debug or detail text

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			VAR responseValues =
			    CALCULATETABLE(
			        VALUES('fact_referral_provider'[provider_response_status]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedPairs,
			            'fact_referral_provider'[referral_id],
			            'fact_referral_provider'[provider_id]))
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CONCATENATEX(
			        responseValues,
			        COALESCE('fact_referral_provider'[provider_response_status], "(Unknown response)"),
			        ", ",
			        'fact_referral_provider'[provider_response_status], ASC
			    ), "No assignment in scope"))
```

Source tables: `gold.dim_person`; `gold.dim_provider`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-location-review"></a>
## Location review

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-233.

Saved category-aware exploration metric

```dax
CALCULATE([Referrals],KEEPFILTERS(FILTER('fact_referral',ISBLANK('fact_referral'[location_match_status]) || 'fact_referral'[location_match_status]<>"CITY_MATCH")))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-male-referrals"></a>
## Male Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-04, GOLD-KPI-110.

```dax
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Male" )
```

Source tables: `gold.dim_person`; `gold.fact_referral`

<a id="business-map-connection-summary"></a>
## Map connection summary

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR selectedReferrals =
			    COUNTROWS ( FILTER ( VALUES ( 'fact_offer'[referral_id] ), NOT ISBLANK ( 'fact_offer'[referral_id] ) ) )
			VAR selectedOffers = COALESCE ( DISTINCTCOUNTNOBLANK ( 'fact_offer'[offer_id] ), 0 )
			VAR mappedOffers = COALESCE ( DISTINCTCOUNTNOBLANK ( 'Offer Location Paths'[Offer ID] ), 0 )
			VAR defaultOffers =
			    COALESCE ( CALCULATE ( DISTINCTCOUNTNOBLANK ( 'Offer Location Paths'[Offer ID] ),
			        'Offer Location Paths'[Location quality] = "Default-city estimate" ), 0 )
			RETURN
			    SWITCH ( TRUE (),
			        selectedOffers = 0, "No offers match these filters.",
			        selectedReferrals <> 1, "Select one referral above, or an offer row, to show its connections.",
			        mappedOffers = 0, "No connection available: endpoint coordinates are missing or the location needs review.",
			        FORMAT ( mappedOffers, "#,0" ) & " of " & FORMAT ( selectedOffers, "#,0" ) & " offers mapped"
			            & IF ( defaultOffers > 0, " | " & FORMAT ( defaultOffers, "#,0" ) & " use a default city", "" )
			            & IF ( selectedOffers > mappedOffers, " | " & FORMAT ( selectedOffers - mappedOffers, "#,0" ) & " unavailable / review", "" )
			    )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-map-connection-visible"></a>
## Map connection visible

Model: **business**. Container: `Offer Location Paths`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF (
			    HASONEVALUE ( 'fact_offer'[referral_id] )
			        && NOT ISBLANK ( SELECTEDVALUE ( 'fact_offer'[referral_id] ) ),
			    1
			)
```

Source tables: `gold.fact_offer`

<a id="business-mapped-referrals"></a>
## Mapped referrals

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-234.

Saved category-aware exploration metric

```dax
CALCULATE([Referrals],KEEPFILTERS('fact_referral'[location_match_status]="CITY_MATCH"))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-matching-referrals"></a>
## Matching referrals

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-122.

Saved detail count in the required record context

```dax
[Explorer referrals]
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-median-days-to-first-action"></a>
## Median Days to First Action

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-010.

```dax
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_action] ) ),
			    'fact_referral'[days_to_first_action]
			)
```

Source tables: `gold.fact_referral`

<a id="business-median-days-to-first-offer"></a>
## Median Days to First Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-011.

```dax
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_offer] ) ),
			    'fact_referral'[days_to_first_offer]
			)
```

Source tables: `gold.fact_referral`

<a id="business-median-days-to-ipa"></a>
## Median Days to IPA

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-012.

```dax
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_ipa] ) ),
			    'fact_referral'[days_to_ipa]
			)
```

Source tables: `gold.fact_referral`

<a id="business-median-offered-weekly-cost"></a>
## Median Offered Weekly Cost

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-235.

Saved target, demand, time or cost metric

```dax
MEDIAN ( 'fact_offer'[estimated_weekly_cost] )
```

Source tables: `gold.fact_offer`

<a id="business-median-preferred-city-distance-km"></a>
## Median preferred-city distance km

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-142.

Saved category-aware exploration metric

```dax
MEDIANX(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]="APPROXIMATE_PREFERENCE_CITY" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km])),'fact_offer'[referral_to_home_distance_km])
```

Source tables: `gold.fact_offer`

<a id="business-no-providers-who-made-offers"></a>
## No. Providers Who Made Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-236.

```dax
CALCULATE (
			    [Providers Who Made Offers],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-non-draft-offers"></a>
## Non-Draft Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-25, KPI-12.

```dax
CALCULATE (
			    [Offers Submitted],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_status] ) && LOWER ( 'fact_offer'[offer_status] ) <> "draft" ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-non-framework-providers"></a>
## Non-Framework Providers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-46.

```dax
COUNTROWS (
			    EXCEPT (
			        VALUES ( 'dim_provider'[provider_id] ),
			        VALUES ( 'bridge_provider_framework'[provider_id] )
			    )
			)
```

Source tables: `gold.bridge_provider_framework`; `gold.dim_provider`

<a id="business-non-spot-offers"></a>
## Non-Spot Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-061.

```dax
CALCULATE ( [Non-Draft Offers], 'dim_provider_home (offer)'[is_spot] = FALSE () )
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-offer-acceptance-rate"></a>
## Offer Acceptance Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-017.

```dax
DIVIDE ( [Accepted Offers], [Offers with a Decision] )
```

Source tables: `gold.fact_offer`

<a id="business-offer-journey-count"></a>
## Offer Journey Count

Model: **business**. Container: `_Design Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Reporting window, anchor or dynamic selector

```dax
SWITCH ( SELECTEDVALUE ( 'Offer Journey Stage'[Ordinal] ),
			    1, [Offers Submitted], 2, BLANK (), 3, BLANK (), 4, [Accepted Offers], 5, [Accepted Offers With IPA] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-offer-receipt-rate-created-in-period"></a>
## Offer Receipt Rate (Created in Period)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-237.

```dax
DIVIDE ( [Referrals With Offers], [Total Referrals] )
```

Source tables: `gold.fact_referral`

<a id="business-offer-receipt-rate-created-in-period-mom-percent"></a>
## Offer Receipt Rate (Created in Period) MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-238.

```dax
DIVIDE ( [Offer Receipt Rate (Created in Period) Variance], [Offer Receipt Rate (Created in Period) Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-offer-receipt-rate-created-in-period-previous-month"></a>
## Offer Receipt Rate (Created in Period) Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-239.

```dax
CALCULATE ( [Offer Receipt Rate (Created in Period)], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-offer-receipt-rate-created-in-period-variance"></a>
## Offer Receipt Rate (Created in Period) Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-240.

```dax
[Offer Receipt Rate (Created in Period)] - [Offer Receipt Rate (Created in Period) Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-offer-receipt-rate-created-in-period-variance-indicator"></a>
## Offer Receipt Rate (Created in Period) Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "▲", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-offer-receipt-rate-created-in-period-variance-indicator-color"></a>
## Offer Receipt Rate (Created in Period) Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Offer Receipt Rate (Created in Period) Variance] > 0, "green", IF ( [Offer Receipt Rate (Created in Period) Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-offers"></a>
## Offers

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-241.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([Offers Submitted],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[Offers Submitted])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-awaiting-ipa-completion-percent"></a>
## Offers Awaiting IPA Completion %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-242.

```dax
DIVIDE ( ([Accepted Offers]-[IPA Completed]), [Accepted Offers] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-offers-awaiting-ipa-creation"></a>
## Offers Awaiting IPA Creation

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-79.

```dax
CALCULATE ( [Offers Submitted], 'fact_offer'[is_awaiting_ipa_creation] = TRUE ())
```

Source tables: `gold.fact_offer`

<a id="business-offers-still-to-progress-to-ipa-percent"></a>
## Offers Still to Progress to IPA %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-84.

```dax
IF ( NOT ISBLANK ( [Accepted Offer to IPA Conversion %] ), 1 - [Accepted Offer to IPA Conversion %] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-offers-submitted"></a>
## Offers Submitted

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-28.

```dax
DISTINCTCOUNT ( 'fact_offer'[offer_id] )
```

Source tables: `gold.fact_offer`

<a id="business-offers-with-recorded-rejection-reason"></a>
## Offers With Recorded Rejection Reason

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-055.

```dax
CALCULATE (
			    [Offers Submitted],
			    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[rejection_reason] ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-offers-in-draft"></a>
## Offers in Draft

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-61.

```dax
CALCULATE ( [Offers Submitted], LOWER ( 'fact_offer'[offer_status] ) = "draft" )
```

Source tables: `gold.fact_offer`

<a id="business-offers-on-referrals-under-offer"></a>
## Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-35.

```dax
CALCULATE (
			    [Non-Draft Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-on-referrals-under-offer-mom-percent"></a>
## Offers on Referrals Under Offer MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-243.

```dax
DIVIDE ( [Offers on Referrals Under Offer Variance], [Offers on Referrals Under Offer Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-on-referrals-under-offer-previous-month"></a>
## Offers on Referrals Under Offer Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-244.

```dax
CALCULATE ( [Offers on Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-on-referrals-under-offer-variance"></a>
## Offers on Referrals Under Offer Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-245.

```dax
[Offers on Referrals Under Offer] - [Offers on Referrals Under Offer Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-on-referrals-under-offer-variance-indicator"></a>
## Offers on Referrals Under Offer Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Offers on Referrals Under Offer Variance] > 0, "▲", IF ( [Offers on Referrals Under Offer Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-on-referrals-under-offer-variance-indicator-color"></a>
## Offers on Referrals Under Offer Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Offers on Referrals Under Offer Variance] > 0, "green", IF ( [Offers on Referrals Under Offer Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-per-provider-under-offer-referrals"></a>
## Offers per Provider (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-37.

```dax
DIVIDE ( [Offers on Referrals Under Offer], [No. Providers Who Made Offers], 0 )
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-offers-with-a-decision"></a>
## Offers with a Decision

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-016.

```dax
CALCULATE (
			    [Offers Submitted],
			    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_decision_date] ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-offers-with-preferred-city-distance"></a>
## Offers with preferred-city distance

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-246.

Saved category-aware exploration metric

```dax
CALCULATE([Offers Submitted],KEEPFILTERS(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]="APPROXIMATE_PREFERENCE_CITY" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km]))))
```

Source tables: `gold.fact_offer`

<a id="business-offers-without-preferred-city-distance"></a>
## Offers without preferred-city distance

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-247.

Saved category-aware exploration metric

```dax
[Offers Submitted]-[Offers with preferred-city distance]
```

Source tables: `gold.fact_offer`

<a id="business-oldest-draft-age-days"></a>
## Oldest Draft Age Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-60.

```dax
MAXX (
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
				),
				'fact_offer'[offer_age_days]
			)
```

Source tables: `gold.fact_offer`

<a id="business-open-on-track-referrals-at-snapshot"></a>
## Open On-Track Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-033.

```dax
CALCULATE (
			    [Snapshot Referrals],
			    'fact_referral_snapshot'[required_placement_date_outcome] = "Open on track"
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-open-overdue-referrals"></a>
## Open Overdue Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-007.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open_overdue] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-open-overdue-referrals-at-snapshot"></a>
## Open Overdue Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-032.

```dax
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open_overdue] = TRUE () )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-open-referral-rate-at-snapshot"></a>
## Open Referral Rate at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-034.

```dax
DIVIDE ( [Open Referrals at Snapshot], [Snapshot Referrals] )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-open-referrals"></a>
## Open Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-08.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-open-referrals-due-in-3-days"></a>
## Open Referrals Due in 3 Days

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-251.

Saved target, demand, time or cost metric

```dax
COUNTROWS ( FILTER ( 'fact_referral',
			    'fact_referral'[is_open] = TRUE () && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
			    && NOT ISBLANK ( 'fact_referral'[as_of_date] )
			    && INT ( 'fact_referral'[required_placement_date] ) >= INT ( 'fact_referral'[as_of_date] )
			    && INT ( 'fact_referral'[required_placement_date] ) <= INT ( 'fact_referral'[as_of_date] ) + 3 ) )
```

Source tables: `gold.fact_referral`

<a id="business-open-referrals-mom-percent"></a>
## Open Referrals MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-252.

```dax
DIVIDE ( [Open Referrals Variance], [Open Referrals Previous Month] )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-open-referrals-previous-month"></a>
## Open Referrals Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-253.

```dax
CALCULATE ( [Open Referrals at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-open-referrals-stalled-7-days"></a>
## Open Referrals Stalled 7+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-013.

```dax
CALCULATE (
			    [Total Referrals],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[days_without_activity] >= 7 )
			)
```

Source tables: `gold.fact_referral`

<a id="business-open-referrals-variance"></a>
## Open Referrals Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-254.

```dax
[Open Referrals at Snapshot] - [Open Referrals Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-open-referrals-variance-indicator"></a>
## Open Referrals Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Open Referrals Variance] > 0, "▲", IF ( [Open Referrals Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-open-referrals-variance-indicator-color"></a>
## Open Referrals Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Open Referrals Variance] > 0, "green", IF ( [Open Referrals Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-open-referrals-at-snapshot"></a>
## Open Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-029.

```dax
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open] = TRUE () )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-open-referrals-by-age"></a>
## Open Referrals by Age

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-248.

Saved target, demand, time or cost metric

```dax
VAR band = SELECTEDVALUE ( 'Open Referral Age'[Ordinal] )
			RETURN COUNTROWS ( FILTER ( 'fact_referral',
			    VAR days = 'fact_referral'[days_open]
			    VAR bucket = SWITCH ( TRUE (), ISBLANK ( days ) || days < 0, 6, days <= 2, 1, days <= 7, 2, days <= 14, 3, days <= 28, 4, 5 )
			    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )
```

Source tables: `gold.fact_referral`

<a id="business-open-referrals-by-days-to-target"></a>
## Open Referrals by Days to Target

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-249.

Saved target, demand, time or cost metric

```dax
VAR band = SELECTEDVALUE ( 'Days to Target'[Ordinal] )
			RETURN COUNTROWS ( FILTER ( 'fact_referral',
			    VAR target = 'fact_referral'[required_placement_date]
			    VAR asof = 'fact_referral'[as_of_date]
			    VAR days = INT ( target ) - INT ( asof )
			    VAR bucket = SWITCH ( TRUE (), ISBLANK ( target ) || ISBLANK ( asof ), 6, days < 0, 5, days <= 1, 1, days <= 3, 2, days <= 7, 3, 4 )
			    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )
```

Source tables: `gold.fact_referral`

<a id="business-open-referrals-by-target-status"></a>
## Open Referrals by Target Status

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-250.

Saved target, demand, time or cost metric

```dax
VAR band = SELECTEDVALUE ( 'Target Status'[Ordinal] )
			RETURN COUNTROWS ( FILTER ( 'fact_referral',
			    VAR target = 'fact_referral'[required_placement_date]
			    VAR asof = 'fact_referral'[as_of_date]
			    VAR days = INT ( target ) - INT ( asof )
			    VAR bucket = SWITCH ( TRUE (), ISBLANK ( target ) || ISBLANK ( asof ), 4, days < 0, 3, days <= 3, 2, 1 )
			    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )
```

Source tables: `gold.fact_referral`

<a id="business-other-gender-referrals"></a>
## Other Gender Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-06, GOLD-KPI-112.

```dax
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Other" )
```

Source tables: `gold.dim_person`; `gold.fact_referral`

<a id="business-other-referrals"></a>
## Other Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-255.

```dax
[Total Gendered Referrals] - [Male Referrals] - [Female Referrals]
```

Source tables: `gold.dim_person`; `gold.fact_referral`

<a id="business-pending-offers"></a>
## Pending Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-053.

```dax
CALCULATE (
			    [Offers Submitted],
			    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-under-offer-referrals"></a>
## Pending Offers (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-18.

```dax
CALCULATE (
			    [Pending Offers],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-pending-offers-0-7-days"></a>
## Pending Offers 0-7 Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-67.

```dax
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 0 && 'fact_offer'[offer_age_days] <= 7 ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-15-29-days"></a>
## Pending Offers 15-29 Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-072.

```dax
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 15 && 'fact_offer'[offer_age_days] <= 29 ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-15-30-days"></a>
## Pending Offers 15–30 Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-71, KPI-65.

```dax
CALCULATE ( [Pending Offers], KEEPFILTERS ( FILTER ( 'fact_offer', 'fact_offer'[offer_age_days] >= 15 && 'fact_offer'[offer_age_days] <= 30 ) ) )
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-30-days"></a>
## Pending Offers 30+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-72, KPI-66.

```dax
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 30 ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-8-14-days"></a>
## Pending Offers 8-14 Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-70, KPI-68.

```dax
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 8 && 'fact_offer'[offer_age_days] <= 14 ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-missing-or-future-date"></a>
## Pending Offers Missing or Future Date

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-256.

```dax
CALCULATE ( [Pending Offers], KEEPFILTERS ( FILTER ( 'fact_offer', ISBLANK ( 'fact_offer'[offer_age_days] ) || 'fact_offer'[offer_age_days] < 0 ) ) )
```

Source tables: `gold.fact_offer`

<a id="business-pending-offers-on-referrals-under-offer"></a>
## Pending Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-257.

```dax
CALCULATE (
			    [Pending Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-placement-rate-at-snapshot"></a>
## Placement Rate at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-035.

```dax
DIVIDE ( [Referrals with IPA at Snapshot], [Snapshot Referrals] )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-placement-target-hit-rate"></a>
## Placement Target Hit Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-009.

```dax
DIVIDE (
			    [Referrals Placed by Required Date],
			    CALCULATE (
			        [Total Referrals],
			        FILTER (
			            'fact_referral',
			            NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
			                && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
			        )
			    )
			)
```

Source tables: `gold.fact_referral`

<a id="business-planned-referrals"></a>
## Planned Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-93 .

```dax
CALCULATE (
			    [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ),
			    KEEPFILTERS ( FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[referral_created_date] ) && NOT ISBLANK ( 'fact_referral'[required_placement_date] ) && 'fact_referral'[is_emergency_placement] = FALSE () ) )
			)
```

Source tables: `gold.fact_referral`

<a id="business-preferred-city-distance-coverage"></a>
## Preferred-city distance coverage

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-141.

Saved category-aware exploration metric

```dax
DIVIDE([Offers with preferred-city distance],[Offers Submitted])
```

Source tables: `gold.fact_offer`

<a id="business-previous-snapshot-referrals"></a>
## Previous Snapshot Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-258.

```dax
VAR current_month = [Snapshot Window Anchor]
			RETURN
				CALCULATE (
					[Snapshot Referrals],
					'dim_snapshot_month'[month_start] = EDATE ( current_month, -1 )
				)
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-provider-assignments"></a>
## Provider Assignments

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-025.

```dax
DISTINCTCOUNT ( 'fact_referral_provider'[referral_provider_id] )
```

Source tables: `gold.fact_referral_provider`

<a id="business-provider-average-response-hours"></a>
## Provider Average Response Hours

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-138.

```dax
DIVIDE (
				SUMX (
					'fact_provider_kpi_monthly',
					'fact_provider_kpi_monthly'[average_response_minutes]
						* 'fact_provider_kpi_monthly'[qualifying_response_count]
				),
				[Provider Qualifying Responses] * 60
			)
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-contact-referral"></a>
## Provider Contact Referral

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-259.

```dax
CALCULATE ( [Total Referrals], KEEPFILTERS ( FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[first_action_date] ) ) ) )
```

Source tables: `gold.fact_referral`

<a id="business-provider-contact-referral-indicator"></a>
## Provider Contact Referral Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Provider Contact Referral Variance] > 0, "▲", IF([Provider Contact Referral Variance] < 0, "▼", "–"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-provider-contact-referral-indicator-color"></a>
## Provider Contact Referral Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Provider Contact Referral Variance] > 0, "green", IF([Provider Contact Referral Variance] < 0, "red", "grey"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-provider-contact-referral-previous-month"></a>
## Provider Contact Referral Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-260.

```dax
CALCULATE ( [Provider Contact Referrals at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-provider-contact-referral-variance"></a>
## Provider Contact Referral Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-261.

```dax
[Provider Contact Referrals at Snapshot] - [Provider Contact Referral Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-provider-contact-referrals-mom-percent"></a>
## Provider Contact Referrals MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-263.

```dax
DIVIDE ([Provider Contact Referral]-[Provider Contact Referral Previous Month],[Provider Contact Referral Previous Month])
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral`; `gold.fact_referral_snapshot`

<a id="business-provider-contact-referrals-at-snapshot"></a>
## Provider Contact Referrals at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-262.

```dax
CALCULATE (
				[Snapshot Referrals],
				FILTER (
					'fact_referral_snapshot',
					NOT ISBLANK ( 'fact_referral_snapshot'[first_action_date] )
						&& 'fact_referral_snapshot'[first_action_date]
							< 'fact_referral_snapshot'[snapshot_date] + 1
				)
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-provider-decline-rate"></a>
## Provider Decline Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-027.

```dax
DIVIDE ( [Provider Declines], [Provider Assignments] )
```

Source tables: `gold.fact_referral_provider`

<a id="business-provider-declines"></a>
## Provider Declines

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-026.

```dax
CALCULATE ( [Provider Assignments], 'fact_referral_provider'[is_declined] = TRUE () )
```

Source tables: `gold.fact_referral_provider`

<a id="business-provider-homes-registered"></a>
## Provider Homes Registered

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-40.

```dax
IF ( ISFILTERED ( 'dim_provider' ),
			    CALCULATE ( DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] ), KEEPFILTERS ( TREATAS ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider_home'[provider_id] ) ) ),
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] )
			)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-provider-homes-with-expired-documents"></a>
## Provider Homes With Expired Documents

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-094.

```dax
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_submission_document'[home_id] ),
			    FILTER (
			        'dim_provider_submission_document',
			        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
			            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
			    )
			)
```

Source tables: `gold.dim_provider_submission_document`

<a id="business-provider-median-days-to-first-offer"></a>
## Provider Median Days to First Offer

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-268.

Saved target, demand, time or cost metric

```dax
VAR per_referral =
			    ADDCOLUMNS ( VALUES ( 'fact_offer'[referral_id] ),
			        "FirstOffer", CALCULATE ( MIN ( 'fact_offer'[offer_submitted_date] ) ),
			        "Created", LOOKUPVALUE ( 'fact_referral'[referral_created_date], 'fact_referral'[referral_id], 'fact_offer'[referral_id] ) )
			RETURN MEDIANX ( FILTER ( per_referral, NOT ISBLANK ( [Created] ) && NOT ISBLANK ( [FirstOffer] ) && [FirstOffer] >= [Created] ),
			    DIVIDE ( DATEDIFF ( [Created], [FirstOffer], HOUR ), 24.0 ) )
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-provider-messages-sent"></a>
## Provider Messages Sent

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-110.

```dax
CALCULATE (
			    [Referral Lifecycle Events],
			    'fact_referral_lifecycle_event'[event_type] = "ProviderMessageSent"
			)
```

Source tables: `gold.fact_referral_lifecycle_event`

<a id="business-provider-offer-conversion-rate"></a>
## Provider Offer Conversion Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-139.

```dax
DIVIDE (
				SUM ( 'fact_provider_kpi_monthly'[accepted_offer_count] ),
				SUM ( 'fact_provider_kpi_monthly'[offers_submitted_count] )
			)
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-onboarding-success-rate"></a>
## Provider Onboarding Success Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-117.

```dax
DIVIDE ( [Providers Approved], [Providers Registered] )
```

Source tables: `gold.dim_provider`

<a id="business-provider-qa-flagged-homes"></a>
## Provider QA flagged homes

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-270.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_provider_home'[provider_home_id]),0), KEEPFILTERS('dim_provider_home'[qa_flag] == TRUE())), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-qualifying-responses"></a>
## Provider Qualifying Responses

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-271.

```dax
SUM ( 'fact_provider_kpi_monthly'[qualifying_response_count] )
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-response-opportunities"></a>
## Provider Response Opportunities

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-273.

```dax
SUM ( 'fact_provider_kpi_monthly'[response_opportunity_count] )
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-response-rate"></a>
## Provider Response Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-137.

```dax
DIVIDE ( [Provider Qualifying Responses], [Provider Response Opportunities] )
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-submission-documents"></a>
## Provider Submission Documents

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-091.

```dax
DISTINCTCOUNT ( 'dim_provider_submission_document'[document_id] )
```

Source tables: `gold.dim_provider_submission_document`

<a id="business-provider-target-placement-rate"></a>
## Provider Target Placement Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-140.

```dax
DIVIDE (
				SUM ( 'fact_provider_kpi_monthly'[placed_by_target_count] ),
				SUM ( 'fact_provider_kpi_monthly'[successful_referral_count] )
			)
```

Source tables: `gold.fact_provider_kpi_monthly`

<a id="business-provider-detail-kpi-value"></a>
## Provider detail KPI value

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF(HASONEVALUE('dim_provider'[provider_id]), SWITCH(SELECTEDVALUE('Provider Explorer KPI'[Ordinal]),
			0, IF(ISBLANK([Explorer providers without offers]), "—", FORMAT([Explorer providers without offers], "#,0")),
			1, IF(ISBLANK([Explorer providers]), "—", FORMAT([Explorer providers], "#,0")),
			2, IF(ISBLANK([Explorer provider homes]), "—", FORMAT([Explorer provider homes], "#,0")),
			3, IF(ISBLANK([Explorer provider beds]), "—", FORMAT([Explorer provider beds], "#,0")),
			4, IF(ISBLANK([Explorer provider offers]), "—", FORMAT([Explorer provider offers], "#,0")),
			5, IF(ISBLANK([Explorer provider offers made]), "—", FORMAT([Explorer provider offers made], "#,0")),
			6, IF(ISBLANK([Explorer provider drafts]), "—", FORMAT([Explorer provider drafts], "#,0")),
			7, IF(ISBLANK([Explorer provider accepted offers]), "—", FORMAT([Explorer provider accepted offers], "#,0")),
			8, IF(ISBLANK([Explorer provider pending offers]), "—", FORMAT([Explorer provider pending offers], "#,0")),
			9, IF(ISBLANK([Explorer provider offer acceptance rate]), "—", FORMAT([Explorer provider offer acceptance rate], "0.0%")),
			10, IF(ISBLANK([Explorer provider assigned referrals]), "—", FORMAT([Explorer provider assigned referrals], "#,0")),
			11, IF(ISBLANK([Explorer provider assignments]), "—", FORMAT([Explorer provider assignments], "#,0")),
			12, IF(ISBLANK([Explorer provider messages]), "—", FORMAT([Explorer provider messages], "#,0")),
			13, IF(ISBLANK([Explorer provider qualifying responses]), "—", FORMAT([Explorer provider qualifying responses], "#,0")),
			14, IF(ISBLANK([Explorer provider response rate]), "—", FORMAT([Explorer provider response rate], "0.0%")),
			15, IF(ISBLANK([Explorer provider average response minutes]), "—", FORMAT([Explorer provider average response minutes], "0.0")),
			16, IF(ISBLANK([Explorer provider median response minutes]), "—", FORMAT([Explorer provider median response minutes], "0.0")),
			17, IF(ISBLANK([Explorer provider IPAs]), "—", FORMAT([Explorer provider IPAs], "#,0")),
			18, IF(ISBLANK([Explorer provider signed IPAs]), "—", FORMAT([Explorer provider signed IPAs], "#,0")),
			19, IF(ISBLANK([Explorer provider completed IPAs]), "—", FORMAT([Explorer provider completed IPAs], "#,0")),
			20, IF(ISBLANK([Provider unanswered assignments]), "—", FORMAT([Provider unanswered assignments], "#,0")),
			21, IF(ISBLANK([Provider response timing coverage]), "—", FORMAT([Provider response timing coverage], "0.0%")),
			22, IF(ISBLANK([Provider QA flagged homes]), "—", FORMAT([Provider QA flagged homes], "#,0")),
			23, IF(ISBLANK([Provider no recorded activity]), "—", FORMAT([Provider no recorded activity], "#,0")), 			24, IF(ISBLANK([Explorer provider documents]), "—", FORMAT([Explorer provider documents], "#,0")),
			25, IF(ISBLANK([Explorer provider documents expired]), "—", FORMAT([Explorer provider documents expired], "#,0")),
			26, IF(ISBLANK([Explorer provider documents expiring 30 days]), "—", FORMAT([Explorer provider documents expiring 30 days], "#,0")),
			27, IF(ISBLANK([Explorer provider homes with expired documents]), "—", FORMAT([Explorer provider homes with expired documents], "#,0")), BLANK()))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-detail-assignment-rows"></a>
## Provider detail assignment rows

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR n = COUNTROWS('fact_referral_provider') RETURN IF(COUNTROWS(ALLSELECTED('dim_provider')) = 1 && n > 0,n)
```

Source tables: `gold.dim_provider`; `gold.fact_referral_provider`

<a id="business-provider-detail-headline-explorer-provider-homes"></a>
## Provider detail headline Explorer provider homes

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Explorer provider homes])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-detail-headline-explorer-provider-messages"></a>
## Provider detail headline Explorer provider messages

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Explorer provider messages])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-detail-headline-explorer-provider-offers-made"></a>
## Provider detail headline Explorer provider offers made

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Explorer provider offers made])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-detail-headline-provider-unanswered-assignments"></a>
## Provider detail headline Provider unanswered assignments

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Provider unanswered assignments])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-detail-home-rows"></a>
## Provider detail home rows

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR n = CALCULATE(COUNTROWS('dim_provider_home'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]),'dim_provider_home'[provider_id]))) RETURN IF(COUNTROWS(ALLSELECTED('dim_provider')) = 1 && n > 0,n)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-provider-detail-message-rows"></a>
## Provider detail message rows

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR n = COUNTROWS('dim_referral_provider_message') RETURN IF(COUNTROWS(ALLSELECTED('dim_provider')) = 1 && n > 0,n)
```

Source tables: `gold.dim_provider`; `gold.dim_referral_provider_message`

<a id="business-provider-detail-offer-rows"></a>
## Provider detail offer rows

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR n = CALCULATE(COUNTROWS('fact_offer'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]), 'fact_offer'[provider_id]))) RETURN IF(HASONEVALUE('dim_provider'[provider_id]) && n > 0,n)
```

Source tables: `gold.dim_provider`; `gold.fact_offer`

<a id="business-provider-detail-profile-rows"></a>
## Provider detail profile rows

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR n = COUNTROWS('dim_provider') RETURN IF(COUNTROWS(ALLSELECTED('dim_provider')) = 1 && n > 0,n)
```

Source tables: `gold.dim_provider`

<a id="business-provider-detail-scoring-denominator"></a>
## Provider detail scoring denominator

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Provider scoring denominator])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-detail-scoring-evidence-status"></a>
## Provider detail scoring evidence status

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Provider scoring evidence status])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-detail-scoring-numerator"></a>
## Provider detail scoring numerator

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Provider scoring numerator])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-detail-scoring-result"></a>
## Provider detail scoring result

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('dim_provider'[provider_id]),[Provider scoring result])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-document-row-visible"></a>
## Provider document row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Document rows require an existing matching home and an eligible provider; no monthly-performance dependency.

```dax
VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
			VAR homeKey = SELECTEDVALUE('dim_provider_submission_document'[home_id])
			VAR matchingHome = CALCULATE(COUNTROWS('dim_provider_home'),
			    KEEPFILTERS(TREATAS({homeKey}, 'dim_provider_home'[provider_home_id])))
			RETURN IF(NOT ISBLANK(providerKey) && NOT ISBLANK(homeKey)
			    && matchingHome > 0 && [Explorer provider row visible] = 1
			    && COUNTROWS('dim_provider_submission_document') > 0, 1, BLANK())
```

<a id="business-provider-explorer-kpi-value"></a>
## Provider explorer KPI value

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
SWITCH(SELECTEDVALUE('Provider Explorer KPI'[Ordinal]),
			0, IF(ISBLANK([Explorer providers without offers]), "—", FORMAT([Explorer providers without offers], "#,0")),
			1, IF(ISBLANK([Explorer providers]), "—", FORMAT([Explorer providers], "#,0")),
			2, IF(ISBLANK([Explorer provider homes]), "—", FORMAT([Explorer provider homes], "#,0")),
			3, IF(ISBLANK([Explorer provider beds]), "—", FORMAT([Explorer provider beds], "#,0")),
			4, IF(ISBLANK([Explorer provider offers]), "—", FORMAT([Explorer provider offers], "#,0")),
			5, IF(ISBLANK([Explorer provider offers made]), "—", FORMAT([Explorer provider offers made], "#,0")),
			6, IF(ISBLANK([Explorer provider drafts]), "—", FORMAT([Explorer provider drafts], "#,0")),
			7, IF(ISBLANK([Explorer provider accepted offers]), "—", FORMAT([Explorer provider accepted offers], "#,0")),
			8, IF(ISBLANK([Explorer provider pending offers]), "—", FORMAT([Explorer provider pending offers], "#,0")),
			9, IF(ISBLANK([Explorer provider offer acceptance rate]), "—", FORMAT([Explorer provider offer acceptance rate], "0.0%")),
			10, IF(ISBLANK([Explorer provider assigned referrals]), "—", FORMAT([Explorer provider assigned referrals], "#,0")),
			11, IF(ISBLANK([Explorer provider assignments]), "—", FORMAT([Explorer provider assignments], "#,0")),
			12, IF(ISBLANK([Explorer provider messages]), "—", FORMAT([Explorer provider messages], "#,0")),
			13, IF(ISBLANK([Explorer provider qualifying responses]), "—", FORMAT([Explorer provider qualifying responses], "#,0")),
			14, IF(ISBLANK([Explorer provider response rate]), "—", FORMAT([Explorer provider response rate], "0.0%")),
			15, IF(ISBLANK([Explorer provider average response minutes]), "—", FORMAT([Explorer provider average response minutes], "0.0")),
			16, IF(ISBLANK([Explorer provider median response minutes]), "—", FORMAT([Explorer provider median response minutes], "0.0")),
			17, IF(ISBLANK([Explorer provider IPAs]), "—", FORMAT([Explorer provider IPAs], "#,0")),
			18, IF(ISBLANK([Explorer provider signed IPAs]), "—", FORMAT([Explorer provider signed IPAs], "#,0")),
			19, IF(ISBLANK([Explorer provider completed IPAs]), "—", FORMAT([Explorer provider completed IPAs], "#,0")),
			20, IF(ISBLANK([Provider unanswered assignments]), "—", FORMAT([Provider unanswered assignments], "#,0")),
			21, IF(ISBLANK([Provider response timing coverage]), "—", FORMAT([Provider response timing coverage], "0.0%")),
			22, IF(ISBLANK([Provider QA flagged homes]), "—", FORMAT([Provider QA flagged homes], "#,0")),
			23, IF(ISBLANK([Provider no recorded activity]), "—", FORMAT([Provider no recorded activity], "#,0")), 			24, IF(ISBLANK([Explorer provider documents]), "—", FORMAT([Explorer provider documents], "#,0")),
			25, IF(ISBLANK([Explorer provider documents expired]), "—", FORMAT([Explorer provider documents expired], "#,0")),
			26, IF(ISBLANK([Explorer provider documents expiring 30 days]), "—", FORMAT([Explorer provider documents expiring 30 days], "#,0")),
			27, IF(ISBLANK([Explorer provider homes with expired documents]), "—", FORMAT([Explorer provider homes with expired documents], "#,0")), BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-explorer-matching-homes"></a>
## Provider explorer matching homes

Model: **business**. Container: `_Provider Detail Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-264.

Matching-home count

```dax
VAR n = CALCULATE(COUNTROWS('dim_provider_home'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]),'dim_provider_home'[provider_id]))) RETURN IF(n > 0,n)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-provider-homes-selected-providers"></a>
## Provider homes selected providers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
CALCULATE([Explorer providers], ALLSELECTED())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-homes-table-accepted-offers"></a>
## Provider homes table accepted offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-265.

Explorer or detail metric with its saved selection context

```dax
VAR selectedProviders = [Provider homes selected providers]
			RETURN IF(selectedProviders > 0 && selectedProviders <= 5, [Explorer provider accepted offers])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-homes-table-offers"></a>
## Provider homes table offers

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-266.

Explorer or detail metric with its saved selection context

```dax
VAR selectedProviders = [Provider homes selected providers]
			RETURN IF(selectedProviders > 0 && selectedProviders <= 5, [Explorer provider offers])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-homes-table-offers-made"></a>
## Provider homes table offers made

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-267.

Explorer or detail metric with its saved selection context

```dax
VAR selectedProviders = [Provider homes selected providers]
			RETURN IF(selectedProviders > 0 && selectedProviders <= 5, [Explorer provider offers made])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-homes-table-row-visible"></a>
## Provider homes table row visible

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR selectedProviders = [Provider homes selected providers]
			RETURN IF(selectedProviders > 0 && selectedProviders <= 5, [Explorer provider row visible])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-homes-table-title"></a>
## Provider homes table title

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF([Provider homes selected providers] > 5,
			    "Please select 1 or fewer providers",
			    "Provider homes — including homes with no offers")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-matches-offer-status"></a>
## Provider matches offer status

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
			VAR limited = ISFILTERED('Provider Offer Status'[Status])
			VAR statuses = VALUES('Provider Offer Status'[Status])
			VAR homeFilter = CALCULATE(ISFILTERED('dim_provider_home'), ALLSELECTED())
			VAR homes = CALCULATETABLE(VALUES('dim_provider_home'[provider_home_id]), ALLSELECTED())
			VAR offerEvidence = CALCULATETABLE(
			    SUMMARIZE('fact_offer', 'fact_offer'[provider_id], 'fact_offer'[provider_home_id], 'fact_offer'[offer_status]),
			    ALLSELECTED())
			VAR providerOffers = FILTER(offerEvidence,
			    'fact_offer'[provider_id] == providerKey && (NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))
			VAR matchingOffers = COUNTROWS(FILTER(providerOffers,
			    COALESCE('fact_offer'[offer_status], "(Unknown status)") IN statuses))
			RETURN IF(ISBLANK(providerKey), BLANK(),
			    IF(NOT limited, 1,
			        IF(matchingOffers > 0 || ("(No offers)" IN statuses && COUNTROWS(providerOffers) = 0), 1, BLANK())))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-provider-no-recorded-activity"></a>
## Provider no recorded activity

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-269.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), CALCULATE(COUNTROWS('fact_referral_provider')) = 0 && CALCULATE(COUNTROWS('fact_offer')) = 0 && CALCULATE(COUNTROWS('dim_referral_provider_message')) = 0)), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-response-durations-recorded"></a>
## Provider response durations recorded

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-272.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[response_elapsed_minutes])))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-response-timing-coverage"></a>
## Provider response timing coverage

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-274.

Action metric, scoring evidence component or catalogue count

```dax
DIVIDE([Provider response durations recorded],[Explorer provider qualifying responses])
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-scoring-cohort-months"></a>
## Provider scoring cohort months

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(DISTINCTCOUNTNOBLANK('fact_provider_kpi_monthly'[assignment_month]), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-scoring-denominator"></a>
## Provider scoring denominator

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
SWITCH(SELECTEDVALUE('Provider Scoring Evidence'[Ordinal]),
			0,[Explorer Gold opportunities],1,[Explorer Gold offers],2,[Explorer Gold successful referrals],3,[Provider scoring qualifying responses],BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-scoring-evidence-status"></a>
## Provider scoring evidence status

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
VAR scoringOrdinal = SELECTEDVALUE('Provider Scoring Evidence'[Ordinal])
			VAR denominator = [Provider scoring denominator]
			VAR versions = CONCATENATEX(VALUES('fact_provider_kpi_monthly'[kpi_rule_version]),'fact_provider_kpi_monthly'[kpi_rule_version],", ")
			RETURN SWITCH(TRUE(), scoringOrdinal = 8, "Policy approval required", scoringOrdinal > 3, "Evidence or policy missing",
			scoringOrdinal = 3, "Activity-level timing; no SLA threshold",
			ISBLANK(denominator) || denominator = 0, "No eligible cohort evidence",
			"Assignment cohort | " & FORMAT([Provider scoring cohort months],"0") & " month(s) | " & COALESCE(versions,"Rule unknown"))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-scoring-median-response-hours"></a>
## Provider scoring median response hours

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-275.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR months = VALUES('dim_snapshot_month'[month_start]) VAR limited = ISFILTERED('dim_snapshot_month') RETURN CALCULATE(DIVIDE(MEDIAN('fact_referral_provider'[response_elapsed_minutes]),60), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[assigned_at]) && NOT ISBLANK('fact_referral_provider'[response_elapsed_minutes]) && (NOT limited || DATE(YEAR('fact_referral_provider'[assigned_at]),MONTH('fact_referral_provider'[assigned_at]),1) IN months)))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-scoring-numerator"></a>
## Provider scoring numerator

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
SWITCH(SELECTEDVALUE('Provider Scoring Evidence'[Ordinal]),
			0,[Explorer Gold responses],1,[Explorer Gold accepted offers],2,[Explorer Gold placed by target],3,[Provider scoring timed responses],BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-scoring-qualifying-responses"></a>
## Provider scoring qualifying responses

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-276.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR months = VALUES('dim_snapshot_month'[month_start]) VAR limited = ISFILTERED('dim_snapshot_month') RETURN CALCULATE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[assigned_at]) && (NOT limited || DATE(YEAR('fact_referral_provider'[assigned_at]),MONTH('fact_referral_provider'[assigned_at]),1) IN months)))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-scoring-result"></a>
## Provider scoring result

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
VAR scoringOrdinal = SELECTEDVALUE('Provider Scoring Evidence'[Ordinal])
			VAR opportunities = [Explorer Gold opportunities]
			VAR offers = [Explorer Gold offers]
			VAR successes = [Explorer Gold successful referrals]
			RETURN SWITCH(scoringOrdinal,
			0, IF(opportunities > 0, FORMAT([Explorer Gold response rate],"0.0%"), "Insufficient evidence"),
			1, IF(offers > 0, FORMAT([Explorer Gold offer acceptance rate],"0.0%"), "Insufficient evidence"),
			2, IF(successes > 0, FORMAT([Explorer Gold target placement rate],"0.0%"), "Insufficient evidence"),
			3, IF(ISBLANK([Provider scoring median response hours]), "Insufficient evidence", FORMAT([Provider scoring median response hours],"0.0") & " h"),
			8, "Not approved", "Not scored")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_provider_kpi_monthly`; `gold.fact_referral_provider`

<a id="business-provider-scoring-timed-responses"></a>
## Provider scoring timed responses

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-277.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(VAR months = VALUES('dim_snapshot_month'[month_start]) VAR limited = ISFILTERED('dim_snapshot_month') RETURN CALCULATE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[assigned_at]) && NOT ISBLANK('fact_referral_provider'[response_elapsed_minutes]) && (NOT limited || DATE(YEAR('fact_referral_provider'[assigned_at]),MONTH('fact_referral_provider'[assigned_at]),1) IN months)))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.dim_snapshot_month`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-selection-context"></a>
## Provider selection context

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
VAR message = (
			VAR n = [Explorer providers] RETURN IF(n = 0,"No matching providers - clear a filter or stage", IF(HASONEVALUE('dim_provider'[provider_id]),"Selected provider: " & SELECTEDVALUE('dim_provider'[provider_id]),FORMAT(n,"#,0") & " matching providers - select a row to open detail")))
			VAR statuses = VALUES('Provider Offer Status'[Status])
			VAR _sample = TOPN(3, statuses, 'Provider Offer Status'[Status], ASC)
			VAR label = CONCATENATEX(_sample, 'Provider Offer Status'[Status], ", ", 'Provider Offer Status'[Status], ASC)
			RETURN message & IF(ISFILTERED('Provider Offer Status'[Status]), " | With offer status: " & label & IF(COUNTROWS(statuses) > 3, " + " & FORMAT(COUNTROWS(statuses) - 3, "0") & " more", ""), "")
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-provider-unanswered-assignments"></a>
## Provider unanswered assignments

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-278.

Action metric, scoring evidence component or catalogue count

```dax
VAR unrestricted =
			    NOT ISFILTERED('Provider Offer Status'[Status])
			    && SELECTEDVALUE('Journey Provider Selection'[Stage], -1) = -1
			VAR homeFilterActive = ISFILTERED('dim_provider_home')
			VAR homeProviderIds = VALUES('dim_provider_home'[provider_id])
			VAR eligible =
			    FILTER(VALUES('dim_provider'[provider_id]),
			        NOT ISBLANK('dim_provider'[provider_id])
			        && IF(unrestricted,
			            NOT homeFilterActive || 'dim_provider'[provider_id] IN homeProviderIds,
			            CALCULATE([Explorer provider row visible]) = 1))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == FALSE() && NOT ISBLANK('fact_referral_provider'[assigned_at])))), KEEPFILTERS(eligible))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-providers-fostering"></a>
## Providers - Fostering

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-51, KPI-42.

```dax
VAR framework_providers = CALCULATETABLE ( VALUES ( 'bridge_provider_framework'[provider_id] ), FILTER ( 'dim_framework', LOWER ( 'dim_framework'[placement_type] ) IN { "fostering", "plcm-fost" } ) )
			VAR home_providers = CALCULATETABLE ( VALUES ( 'dim_provider_home'[provider_id] ), FILTER ( 'dim_provider_home', LOWER ( 'dim_provider_home'[service_type] ) IN { "fostering", "plcm-fost" } ) )
			RETURN CALCULATE ( [Providers Registered], KEEPFILTERS ( TREATAS ( DISTINCT ( UNION ( framework_providers, home_providers ) ), 'dim_provider'[provider_id] ) ) )
```

Source tables: `gold.bridge_provider_framework`; `gold.dim_framework`; `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-providers-residential"></a>
## Providers - Residential

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-43.

```dax
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
			    'dim_provider_home'[service_type] = "Residential"
			)
```

Source tables: `gold.dim_provider_home`

<a id="business-providers-supported-accommodation"></a>
## Providers - Supported Accommodation

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-44.

```dax
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
			    'dim_provider_home'[service_type] = "Supported Accommodation"
			)
```

Source tables: `gold.dim_provider_home`

<a id="business-providers-approved"></a>
## Providers Approved

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-104.

```dax
CALCULATE (
			    [Providers Registered],
			    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "approved" )
			)
```

Source tables: `gold.dim_provider`

<a id="business-providers-pending-onboarding"></a>
## Providers Pending Onboarding

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-104, KPI-116.

```dax
CALCULATE (
			    [Providers Registered],
			    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "pending" )
			)
```

Source tables: `gold.dim_provider`

<a id="business-providers-registered"></a>
## Providers Registered

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-41.

```dax
DISTINCTCOUNT(dim_provider[provider_id])
```

Source tables: `gold.dim_provider`

<a id="business-providers-who-made-offers"></a>
## Providers Who Made Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-11.

```dax
CALCULATE (
			    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
			    FILTER (
			        'fact_offer',
			        NOT (
			            LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
			                IN { "draft", "withdrawn", "offer_withdrawn" }
			        )
			    ))
```

Source tables: `gold.fact_offer`

<a id="business-providers-with-offers-on-referrals-under-offer"></a>
## Providers With Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-279.

```dax
CALCULATE (
			    [Providers Who Made Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-providers-with-pending-offers-30-days"></a>
## Providers With Pending Offers 30+ Days

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-69.

```dax
CALCULATE (
			    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
			    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } && 'fact_offer'[offer_age_days] >= 30 ) )
			)
```

Source tables: `gold.fact_offer`

<a id="business-providers-with-qa-flags"></a>
## Providers With QA Flags

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-97 .

```dax
CALCULATE ( [Providers Registered], KEEPFILTERS ( 'dim_provider'[qa_flag] = TRUE () ) )
```

Source tables: `gold.dim_provider`

<a id="business-qa-flagged-homes"></a>
## QA Flagged Homes

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-99 .

```dax
VAR flagged_providers = CALCULATETABLE ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider'[qa_flag] = TRUE () )
			VAR selected_providers = VALUES ( 'dim_provider'[provider_id] )
			RETURN
			    CALCULATE (
			        [Provider Homes Registered],
			        KEEPFILTERS ( TREATAS ( selected_providers, 'dim_provider_home'[provider_id] ) ),
			        KEEPFILTERS ( FILTER ( 'dim_provider_home', 'dim_provider_home'[qa_flag] = TRUE () || 'dim_provider_home'[provider_id] IN flagged_providers ) )
			    )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-rail-activity-caption"></a>
## Rail activity caption

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR stage = SELECTEDVALUE('Journey Detail Selection'[Stage], -1)
			VAR focus = SWITCH(stage, 1,"Referral activity",2,"Provider-message activity",3,"Offer activity",4,"Offer updates (acceptance is not an explicit event)",5,"IPA activity",6,"IPA updates (signature is not an explicit event)","All recorded activity")
			RETURN "Activity focus: " & focus & ". " & [Journey next action]
```

Source tables: `gold.fact_referral`

<a id="business-rail-activity-row-visible"></a>
## Rail activity row visible

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR stage = SELECTEDVALUE('Journey Detail Selection'[Stage], -1)
			VAR eventType = SELECTEDVALUE('fact_referral_lifecycle_event'[event_type])
			RETURN IF(stage = -1, 1, IF(SWITCH(stage,
			1, eventType IN {"ReferralCreated", "ReferralModified"},
			2, eventType = "ProviderMessageSent",
			3, eventType IN {"OfferSubmitted", "OfferUpdated"},
			4, eventType = "OfferUpdated",
			5, eventType IN {"IPACreated", "IPAUpdated"},
			6, eventType = "IPAUpdated", FALSE()), 1, BLANK()))
```

Source tables: `gold.fact_referral_lifecycle_event`

<a id="business-rail-provider-circle-1"></a>
## Rail provider circle 1

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(1=4, "#F0EBE7", IF(ISFILTERED('Journey Provider Selection'[Stage]), IF(SELECTEDVALUE('Journey Provider Selection'[Stage]) = 1, "#EF7911", "#F0EBE7"), "#FCA356"))
```

Source tables: No direct physical source asserted.

<a id="business-rail-provider-circle-2"></a>
## Rail provider circle 2

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(2=4, "#F0EBE7", IF(ISFILTERED('Journey Provider Selection'[Stage]), IF(SELECTEDVALUE('Journey Provider Selection'[Stage]) = 2, "#EF7911", "#F0EBE7"), "#FCA356"))
```

Source tables: No direct physical source asserted.

<a id="business-rail-provider-circle-3"></a>
## Rail provider circle 3

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(3=4, "#F0EBE7", IF(ISFILTERED('Journey Provider Selection'[Stage]), IF(SELECTEDVALUE('Journey Provider Selection'[Stage]) = 3, "#EF7911", "#F0EBE7"), "#FCA356"))
```

Source tables: No direct physical source asserted.

<a id="business-rail-provider-circle-4"></a>
## Rail provider circle 4

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(4=4, "#F0EBE7", IF(ISFILTERED('Journey Provider Selection'[Stage]), IF(SELECTEDVALUE('Journey Provider Selection'[Stage]) = 4, "#EF7911", "#F0EBE7"), "#FCA356"))
```

Source tables: No direct physical source asserted.

<a id="business-rail-provider-circle-5"></a>
## Rail provider circle 5

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(5=4, "#F0EBE7", IF(ISFILTERED('Journey Provider Selection'[Stage]), IF(SELECTEDVALUE('Journey Provider Selection'[Stage]) = 5, "#EF7911", "#F0EBE7"), "#FCA356"))
```

Source tables: No direct physical source asserted.

<a id="business-rail-provider-cohort-label"></a>
## Rail provider cohort label

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
			RETURN IF(NOT ISBLANK(providerKey), CALCULATE([Journey provider label], ALLSELECTED(), KEEPFILTERS(TREATAS({providerKey},'dim_provider'[provider_id]))))
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-rail-provider-row-visible"></a>
## Rail provider row visible

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
[Explorer provider row visible]
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-rail-provider-selected-metric"></a>
## Rail provider selected metric

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR metric = IF(NOT ISCROSSFILTERED('Dashboard Metric Selector'), 3, SELECTEDVALUE('Dashboard Metric Selector'[Dashboard Metric Selector Order]))
			RETURN SWITCH(metric, 0,[Explorer provider assigned referrals],3,[Explorer provider offers],4,[Explorer provider accepted offers],5,[Explorer provider pending offers],6,[Explorer provider IPAs],7,[Explorer provider completed IPAs],BLANK())
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral_provider`

<a id="business-rail-referral-circle-1"></a>
## Rail referral circle 1

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 1, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-circle-2"></a>
## Rail referral circle 2

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 2, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-circle-3"></a>
## Rail referral circle 3

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 3, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-circle-4"></a>
## Rail referral circle 4

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 4, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-circle-5"></a>
## Rail referral circle 5

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 5, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-circle-6"></a>
## Rail referral circle 6

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = 6, "#EF7911", "#F0EBE7"), "#FCA356")
```

Source tables: `gold.fact_referral`

<a id="business-rail-referral-summary"></a>
## Rail referral summary

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referral exceptions], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-1"></a>
## Rail referrals 1

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 1], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-2"></a>
## Rail referrals 2

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 2], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-3"></a>
## Rail referrals 3

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 3], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-4"></a>
## Rail referrals 4

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 4], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-5"></a>
## Rail referrals 5

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 5], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-rail-referrals-6"></a>
## Rail referrals 6

Model: **business**. Container: `_Journey Interaction`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
CALCULATE([Journey referrals 6], REMOVEFILTERS('fact_referral'[Journey stage order]))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-ipas-awaiting-signatures"></a>
## Referral IPAs awaiting signatures

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-281.

Action metric, scoring evidence component or catalogue count

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(FILTER('fact_ipa', NOT('fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())))), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-lifecycle-events"></a>
## Referral Lifecycle Events

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-113.

```dax
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[event_id] )
```

Source tables: `gold.fact_referral_lifecycle_event`

<a id="business-referral-volume-month-on-month"></a>
## Referral Volume Month on Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-038.

```dax
[Total Referrals] - [Referrals Created Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referral-volume-month-on-month-percent"></a>
## Referral Volume Month on Month %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-039.

```dax
DIVIDE ( [Referral Volume Month on Month], [Referrals Created Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referral-accepted-without-ipa"></a>
## Referral accepted without IPA

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-280.

Action metric, scoring evidence component or catalogue count

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COUNTROWS(FILTER(VALUES('fact_referral'[referral_id]), CALCULATE(COUNTROWS(FILTER('fact_referral', CALCULATE(COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {"accepted", "approved", "selected", "offer_successful"}))) > 0 && CALCULATE(COUNTROWS('fact_ipa')) = 0))) > 0)), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-detail-kpi-value"></a>
## Referral detail KPI value

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
IF(HASONEVALUE('fact_referral'[referral_id]), SWITCH(SELECTEDVALUE('Referral Explorer KPI'[Ordinal]),
			0, IF(ISBLANK([Explorer referrals]), "—", FORMAT([Explorer referrals], "#,0")),
			1, IF(ISBLANK([Explorer referrals open]), "—", FORMAT([Explorer referrals open], "#,0")),
			2, IF(ISBLANK([Explorer referrals open overdue]), "—", FORMAT([Explorer referrals open overdue], "#,0")),
			3, IF(ISBLANK([Explorer referrals closed]), "—", FORMAT([Explorer referrals closed], "#,0")),
			4, IF(ISBLANK([Explorer referrals with offers]), "—", FORMAT([Explorer referrals with offers], "#,0")),
			5, IF(ISBLANK([Explorer referrals without offers]), "—", FORMAT([Explorer referrals without offers], "#,0")),
			6, IF(ISBLANK([Explorer referral offer coverage]), "—", FORMAT([Explorer referral offer coverage], "0.0%")),
			7, IF(ISBLANK([Explorer referral offers]), "—", FORMAT([Explorer referral offers], "#,0")),
			8, IF(ISBLANK([Explorer referral accepted offers]), "—", FORMAT([Explorer referral accepted offers], "#,0")),
			9, IF(ISBLANK([Explorer referral assignments]), "—", FORMAT([Explorer referral assignments], "#,0")),
			10, IF(ISBLANK([Explorer referral messages]), "—", FORMAT([Explorer referral messages], "#,0")),
			11, IF(ISBLANK([Explorer referral IPAs]), "—", FORMAT([Explorer referral IPAs], "#,0")),
			12, IF(ISBLANK([Explorer referral completed IPAs]), "—", FORMAT([Explorer referral completed IPAs], "#,0")),
			13, IF(ISBLANK([Referral open without offers]), "—", FORMAT([Referral open without offers], "#,0")),
			14, IF(ISBLANK([Referral open without assignments]), "—", FORMAT([Referral open without assignments], "#,0")),
			15, IF(ISBLANK([Referral accepted without IPA]), "—", FORMAT([Referral accepted without IPA], "#,0")),
			16, IF(ISBLANK([Referral IPAs awaiting signatures]), "—", FORMAT([Referral IPAs awaiting signatures], "#,0")),
			17, IF(ISBLANK([Referral open overdue share]), "—", FORMAT([Referral open overdue share], "0.0%")), BLANK()))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-referral-detail-headline-explorer-referral-assignments"></a>
## Referral detail headline Explorer referral assignments

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('fact_referral'[referral_id]),[Explorer referral assignments])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-referral-detail-headline-explorer-referral-messages"></a>
## Referral detail headline Explorer referral messages

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('fact_referral'[referral_id]),[Explorer referral messages])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.dim_referral_provider_message`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-detail-headline-explorer-referral-offers"></a>
## Referral detail headline Explorer referral offers

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('fact_referral'[referral_id]),[Explorer referral offers])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-detail-headline-referral-ipas-awaiting-signatures"></a>
## Referral detail headline Referral IPAs awaiting signatures

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
IF(HASONEVALUE('fact_referral'[referral_id]),[Referral IPAs awaiting signatures])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-explorer-kpi-value"></a>
## Referral explorer KPI value

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Dynamic KPI selector, eligibility, table cap or title

```dax
SWITCH(SELECTEDVALUE('Referral Explorer KPI'[Ordinal]),
			0, IF(ISBLANK([Explorer referrals]), "—", FORMAT([Explorer referrals], "#,0")),
			1, IF(ISBLANK([Explorer referrals open]), "—", FORMAT([Explorer referrals open], "#,0")),
			2, IF(ISBLANK([Explorer referrals open overdue]), "—", FORMAT([Explorer referrals open overdue], "#,0")),
			3, IF(ISBLANK([Explorer referrals closed]), "—", FORMAT([Explorer referrals closed], "#,0")),
			4, IF(ISBLANK([Explorer referrals with offers]), "—", FORMAT([Explorer referrals with offers], "#,0")),
			5, IF(ISBLANK([Explorer referrals without offers]), "—", FORMAT([Explorer referrals without offers], "#,0")),
			6, IF(ISBLANK([Explorer referral offer coverage]), "—", FORMAT([Explorer referral offer coverage], "0.0%")),
			7, IF(ISBLANK([Explorer referral offers]), "—", FORMAT([Explorer referral offers], "#,0")),
			8, IF(ISBLANK([Explorer referral accepted offers]), "—", FORMAT([Explorer referral accepted offers], "#,0")),
			9, IF(ISBLANK([Explorer referral assignments]), "—", FORMAT([Explorer referral assignments], "#,0")),
			10, IF(ISBLANK([Explorer referral messages]), "—", FORMAT([Explorer referral messages], "#,0")),
			11, IF(ISBLANK([Explorer referral IPAs]), "—", FORMAT([Explorer referral IPAs], "#,0")),
			12, IF(ISBLANK([Explorer referral completed IPAs]), "—", FORMAT([Explorer referral completed IPAs], "#,0")),
			13, IF(ISBLANK([Referral open without offers]), "—", FORMAT([Referral open without offers], "#,0")),
			14, IF(ISBLANK([Referral open without assignments]), "—", FORMAT([Referral open without assignments], "#,0")),
			15, IF(ISBLANK([Referral accepted without IPA]), "—", FORMAT([Referral accepted without IPA], "#,0")),
			16, IF(ISBLANK([Referral IPAs awaiting signatures]), "—", FORMAT([Referral IPAs awaiting signatures], "#,0")),
			17, IF(ISBLANK([Referral open overdue share]), "—", FORMAT([Referral open overdue share], "0.0%")), BLANK())
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.dim_referral_provider_message`; `gold.fact_ipa`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-referral-open-overdue-share"></a>
## Referral open overdue share

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-282.

Action metric, scoring evidence component or catalogue count

```dax
DIVIDE([Explorer referrals open overdue],[Explorer referrals open])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-open-without-assignments"></a>
## Referral open without assignments

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-283.

Action metric, scoring evidence component or catalogue count

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COUNTROWS(FILTER(VALUES('fact_referral'[referral_id]), CALCULATE(COUNTROWS(FILTER('fact_referral', 'fact_referral'[is_open] == TRUE() && CALCULATE(COUNTROWS('fact_referral_provider')) = 0))) > 0)), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`; `gold.fact_referral_provider`

<a id="business-referral-open-without-offers"></a>
## Referral open without offers

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-284.

Action metric, scoring evidence component or catalogue count

```dax
VAR categories = VALUES('Referral Category'[Category ID])
			VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
			VAR statuses = VALUES('Explorer Offer Status'[Status])
			VAR bands = VALUES('Explorer Offer Activity'[Band])
			VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
			VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
			VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
			VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
			VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
			VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
			VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
			    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
			    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
			RETURN CALCULATE(COUNTROWS(FILTER(VALUES('fact_referral'[referral_id]), CALCULATE(COUNTROWS(FILTER('fact_referral', 'fact_referral'[is_open] == TRUE() && CALCULATE(COUNTROWS('fact_offer')) = 0))) > 0)), KEEPFILTERS(eligible))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referral-selection-context"></a>
## Referral selection context

Model: **business**. Container: `_Report Journey Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Context or dynamic projection; not an additional fixed KPI

```dax
VAR n = [Explorer referrals] RETURN IF(n = 0,"No matching referrals - clear a filter or stage", IF(HASONEVALUE('fact_referral'[referral_id]),"Selected referral: " & SELECTEDVALUE('fact_referral'[referral_id]),FORMAT(n,"#,0") & " matching referrals - select a row to open detail"))
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-referrals"></a>
## Referrals

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-285.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([Total Referrals],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[Total Referrals])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-referrals-awaiting-offer"></a>
## Referrals Awaiting Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-32, KPI-03.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_awaiting_offer] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-awaiting-offer-mom-percent"></a>
## Referrals Awaiting Offer MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-286.

```dax
DIVIDE ( [Referrals Awaiting Offer Variance], [Referrals Awaiting Offer Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-awaiting-offer-previous-month"></a>
## Referrals Awaiting Offer Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-287.

```dax
CALCULATE ( [Referrals Awaiting Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-awaiting-offer-variance"></a>
## Referrals Awaiting Offer Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-288.

```dax
[Referrals Awaiting Offer] - [Referrals Awaiting Offer Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-awaiting-offer-variance-indicator"></a>
## Referrals Awaiting Offer Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Awaiting Offer Variance] > 0, "▲", IF ( [Referrals Awaiting Offer Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-awaiting-offer-variance-indicator-color"></a>
## Referrals Awaiting Offer Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Awaiting Offer Variance] > 0, "green", IF ( [Referrals Awaiting Offer Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-cancelled-closed-indicator"></a>
## Referrals Cancelled/Closed Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Referrals Cancelled/Closed Variance] > 0, "▲", IF([Referrals Cancelled/Closed Variance]< 0, "▼", "–"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-cancelled-closed-previous-month"></a>
## Referrals Cancelled/Closed Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-289.

```dax
CALCULATE ( [Closed or Cancelled Referrals at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-cancelled-closed-variance"></a>
## Referrals Cancelled/Closed Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-290.

```dax
[Closed or Cancelled Referrals at Snapshot] - [Referrals Cancelled/Closed Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-created-previous-month"></a>
## Referrals Created Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-037.

```dax
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-created-this-financial-year"></a>
## Referrals Created This Financial Year

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-24.

```dax
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
			VAR year_start = DATE ( YEAR ( as_of ) - IF ( MONTH ( as_of ) < 4, 1, 0 ), 4, 1 )
			RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], year_start, as_of ) ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-created-this-month"></a>
## Referrals Created This Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-23.

```dax
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
			RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of ) ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-currently-active"></a>
## Referrals Currently Active

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-29.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-currently-active-mom-percent"></a>
## Referrals Currently Active MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-291.

```dax
DIVIDE ( [Referrals Currently Active Variance], [Referrals Currently Active Previous Month] )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-currently-active-previous-month"></a>
## Referrals Currently Active Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-292.

```dax
CALCULATE ( [Open Referrals at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-currently-active-variance"></a>
## Referrals Currently Active Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-293.

```dax
[Open Referrals at Snapshot] - [Referrals Currently Active Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-currently-active-variance-indicator"></a>
## Referrals Currently Active Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Currently Active Variance] > 0, "▲", IF ( [Referrals Currently Active Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-currently-active-variance-indicator-color"></a>
## Referrals Currently Active Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Currently Active Variance] > 0, "green", IF ( [Referrals Currently Active Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-due-this-as-of-month"></a>
## Referrals Due This As Of Month

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-295.

Saved target, demand, time or cost metric

```dax
VAR asof = [Current Referral As Of]
			VAR first_day = DATE ( YEAR ( asof ), MONTH ( asof ), 1 )
			RETURN IF ( NOT ISBLANK ( asof ), CALCULATE ( [Total Referrals], REMOVEFILTERS ( 'dim_date' ),
			    KEEPFILTERS ( 'fact_referral'[required_placement_date] >= first_day ),
			    KEEPFILTERS ( 'fact_referral'[required_placement_date] < EDATE ( first_day, 1 ) ) ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-due-in-reporting-period"></a>
## Referrals Due in Reporting Period

Model: **business**. Container: `_Design Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-294.

Saved target, demand, time or cost metric

```dax
CALCULATE ( [Total Referrals],
			    USERELATIONSHIP ( 'fact_referral'[required_placement_date], 'dim_date'[date] ),
			    KEEPFILTERS ( NOT ISBLANK ( 'fact_referral'[required_placement_date] ) ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-not-yet-closed"></a>
## Referrals Not Yet Closed

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-296.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-placed-by-required-date"></a>
## Referrals Placed by Required Date

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-008.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[placed_by_required_date] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-placed-by-target-at-snapshot"></a>
## Referrals Placed by Target at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-297.

```dax
CALCULATE (
			    [Snapshot Referrals],
			    'fact_referral_snapshot'[placed_by_required_date] = TRUE ()
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-referrals-under-offer"></a>
## Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-30.

```dax
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[is_open] = TRUE () ), KEEPFILTERS ( 'fact_referral'[current_status] = "UNDER_OFFER" ) )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-under-offer-mom-percent"></a>
## Referrals Under Offer MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-298.

```dax
DIVIDE ( [Referrals Under Offer Variance], [Referrals Under Offer Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-under-offer-previous-month"></a>
## Referrals Under Offer Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-299.

```dax
CALCULATE ( [Referrals Under Offer], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-under-offer-variance"></a>
## Referrals Under Offer Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-300.

```dax
[Referrals Under Offer] - [Referrals Under Offer Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-under-offer-variance-indicator"></a>
## Referrals Under Offer Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Under Offer Variance] > 0, "▲", IF ( [Referrals Under Offer Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-under-offer-variance-indicator-color"></a>
## Referrals Under Offer Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals Under Offer Variance] > 0, "green", IF ( [Referrals Under Offer Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-with-fully-signed-ipa"></a>
## Referrals With Fully Signed IPA

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-103.

```dax
CALCULATE ( DISTINCTCOUNT ( 'fact_ipa'[referral_id] ), KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-referrals-with-ipa"></a>
## Referrals With IPA

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-305.

```dax
DISTINCTCOUNT ( 'fact_ipa'[referral_id] )
```

Source tables: `gold.fact_ipa`

<a id="business-referrals-with-ipa-pending-signature"></a>
## Referrals With IPA Pending Signature

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-306.

```dax
CALCULATE ( DISTINCTCOUNT ( 'fact_ipa'[referral_id] ), KEEPFILTERS ( 'fact_ipa'[is_ipa_pending] = TRUE () ) )
```

Source tables: `gold.fact_ipa`

<a id="business-referrals-with-lifecycle-activity"></a>
## Referrals With Lifecycle Activity

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-106.

```dax
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[referral_id] )
```

Source tables: `gold.fact_referral_lifecycle_event`

<a id="business-referrals-with-multiple-provider-assignments"></a>
## Referrals With Multiple Provider Assignments

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-90.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[provider_assignment_count] > 1 )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-with-offers"></a>
## Referrals With Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-308.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-with-offers-percent"></a>
## Referrals With Offers %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-309.

```dax
DIVIDE( [Referrals With Offers], [Total Referrals])
```

Source tables: `gold.fact_referral`

<a id="business-referrals-with-an-offer"></a>
## Referrals With an Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-02, KPI-09, KPI-33.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-with-an-offer-mom-percent"></a>
## Referrals With an Offer MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-302.

```dax
DIVIDE ( [Referrals With an Offer Variance], [Referrals With an Offer Previous Month] )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-with-an-offer-previous-month"></a>
## Referrals With an Offer Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-303.

```dax
CALCULATE ( [Referrals With an Offer at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-with-an-offer-variance"></a>
## Referrals With an Offer Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-304.

```dax
[Referrals With an Offer at Snapshot] - [Referrals With an Offer Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-with-an-offer-variance-indicator"></a>
## Referrals With an Offer Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals With an Offer Variance] > 0, "▲", IF ( [Referrals With an Offer Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-with-an-offer-variance-indicator-color"></a>
## Referrals With an Offer Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Referrals With an Offer Variance] > 0, "green", IF ( [Referrals With an Offer Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-referrals-with-an-offer-at-snapshot"></a>
## Referrals With an Offer at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-301.

```dax
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[has_offer] = TRUE () )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-referrals-without-provider-assignment"></a>
## Referrals Without Provider Assignment

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-006.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_not_seen_by_providers] = TRUE () )
```

Source tables: `gold.fact_referral`

<a id="business-referrals-closed-during-month"></a>
## Referrals closed during month

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-121.

Saved detail count in the required record context

```dax
CALCULATE(DISTINCTCOUNT('fact_referral'[referral_id]), USERELATIONSHIP('fact_referral'[referral_closed_date],'dim_date'[date]), CROSSFILTER('fact_referral'[referral_created_date],'dim_date'[date],NONE), KEEPFILTERS(NOT ISBLANK('fact_referral'[referral_closed_date])))
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-referrals-with-ipa-at-snapshot"></a>
## Referrals with IPA at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-031.

```dax
CALCULATE (
			    [Snapshot Referrals],
			    FILTER (
			        'fact_referral_snapshot',
			        NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
			            && 'fact_referral_snapshot'[ipa_issued_date] < 'fact_referral_snapshot'[snapshot_date] + 1
			    )
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-referrals-with-missed-response-date"></a>
## Referrals with Missed Response Date

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-307.

```dax
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = FALSE (),  NOT(LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
			             IN { "closed", "cancelled", "withdrawn", "completed" }))
```

Source tables: `gold.fact_referral`

<a id="business-report-version-label"></a>
## Report Version Label

Model: **business**. Container: `Report Settings`. Classification: **Display/filter/context helper**. KPI records: Helper/context only.

Presentation, selected-record, interaction or technical helper

```dax
VAR versionText =
			    CALCULATE (
			        SELECTEDVALUE ( 'Report Settings'[ReportVersion] ),
			        REMOVEFILTERS ( 'Report Settings' )
			    )
			RETURN IF ( NOT ISBLANK ( versionText ), "Version: " & versionText )
```

Source tables: No direct physical source asserted.

<a id="business-requirement-kpi-row-visible"></a>
## Requirement KPI row visible

Model: **business**. Container: `Requirement KPI Monitor`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Local requirement presentation helper; reuses existing business calculations.

```dax
VAR requirementKeys = SELECTEDVALUE('Requirement KPI Monitor'[Requirement keys])
			VAR selectedRequirements = VALUES('ref_RID'[Req ID])
			VAR matches = COUNTROWS(FILTER(selectedRequirements,
			    CONTAINSSTRING(requirementKeys, "|" & TRIM('ref_RID'[Req ID]) & "|")))
			RETURN IF(NOT ISCROSSFILTERED('ref_RID') || matches > 0, 1, BLANK())
```

<a id="business-requirement-kpi-value"></a>
## Requirement KPI value

Model: **business**. Container: `Requirement KPI Monitor`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Local requirement presentation helper; reuses existing business calculations.

```dax
IF([Requirement KPI row visible] = 1, SWITCH(SELECTEDVALUE('Requirement KPI Monitor'[Ordinal]),
			    0, IF(ISBLANK('_Measures'[Active Awaiting Offers With Engagement]), "—", FORMAT('_Measures'[Active Awaiting Offers With Engagement], "#,0")),
			    1, IF(ISBLANK('_Measures'[Average Estimated Weekly Cost — Confirmed Referrals]), "—", FORMAT('_Measures'[Average Estimated Weekly Cost — Confirmed Referrals], "£#,0.00")),
			    2, IF(ISBLANK('_Measures'[Closed Referrals at Snapshot]), "—", FORMAT('_Measures'[Closed Referrals at Snapshot], "#,0")),
			    3, IF(ISBLANK('_Measures'[Documents Expired]), "—", FORMAT('_Measures'[Documents Expired], "#,0")),
			    4, IF(ISBLANK('_Measures'[Documents Expiring Next 30 Days]), "—", FORMAT('_Measures'[Documents Expiring Next 30 Days], "#,0")),
			    5, IF(ISBLANK('_Measures'[Draft Offers on Referrals Under Offer]), "—", FORMAT('_Measures'[Draft Offers on Referrals Under Offer], "#,0")),
			    6, IF(ISBLANK('_Measures'[Drafts No Activity 14+ Days]), "—", FORMAT('_Measures'[Drafts No Activity 14+ Days], "#,0")),
			    7, IF(ISBLANK('_Measures'[Emergency Placement Rate]), "—", FORMAT('_Measures'[Emergency Placement Rate], "0.0%")),
			    8, IF(ISBLANK('_Measures'[Emergency Referrals]), "—", FORMAT('_Measures'[Emergency Referrals], "#,0")),
			    9, IF(ISBLANK('_Measures'[IPA Signature Completion Rate]), "—", FORMAT('_Measures'[IPA Signature Completion Rate], "0.0%")),
			    10, IF(ISBLANK('_Measures'[IPAs Signed by Local Authority]), "—", FORMAT('_Measures'[IPAs Signed by Local Authority], "#,0")),
			    11, IF(ISBLANK('_Measures'[IPAs Signed by Provider]), "—", FORMAT('_Measures'[IPAs Signed by Provider], "#,0")),
			    12, IF(ISBLANK('_Measures'[Latest Offer Source Export]), "—", FORMAT('_Measures'[Latest Offer Source Export], "dd MMM yyyy HH:mm")),
			    13, IF(ISBLANK('_Measures'[Median Days to First Action]), "—", FORMAT('_Measures'[Median Days to First Action], "0.0")),
			    14, IF(ISBLANK('_Measures'[Median Days to First Offer]), "—", FORMAT('_Measures'[Median Days to First Offer], "0.0")),
			    15, IF(ISBLANK('_Measures'[Offers Still to Progress to IPA %]), "—", FORMAT('_Measures'[Offers Still to Progress to IPA %], "0.0%")),
			    16, IF(ISBLANK('_Measures'[Other Gender Referrals]), "—", FORMAT('_Measures'[Other Gender Referrals], "#,0")),
			    17, IF(ISBLANK('_Measures'[Planned Referrals]), "—", FORMAT('_Measures'[Planned Referrals], "#,0")),
			    18, IF(ISBLANK('_Measures'[Provider Average Response Hours]), "—", FORMAT('_Measures'[Provider Average Response Hours], "0.0")),
			    19, IF(ISBLANK('_Measures'[Provider Decline Rate]), "—", FORMAT('_Measures'[Provider Decline Rate], "0.0%")),
			    20, IF(ISBLANK('_Measures'[Provider Declines]), "—", FORMAT('_Measures'[Provider Declines], "#,0")),
			    21, IF(ISBLANK('_Measures'[Provider Messages Sent]), "—", FORMAT('_Measures'[Provider Messages Sent], "#,0")),
			    22, IF(ISBLANK('_Measures'[Provider Offer Conversion Rate]), "—", FORMAT('_Measures'[Provider Offer Conversion Rate], "0.0%")),
			    23, IF(ISBLANK('_Measures'[Provider Onboarding Success Rate]), "—", FORMAT('_Measures'[Provider Onboarding Success Rate], "0.0%")),
			    24, IF(ISBLANK('_Measures'[Provider Response Rate]), "—", FORMAT('_Measures'[Provider Response Rate], "0.0%")),
			    25, IF(ISBLANK('_Measures'[Provider Target Placement Rate]), "—", FORMAT('_Measures'[Provider Target Placement Rate], "0.0%")),
			    26, IF(ISBLANK('_Measures'[Providers Approved]), "—", FORMAT('_Measures'[Providers Approved], "#,0")),
			    27, IF(ISBLANK('_Measures'[Providers Pending Onboarding]), "—", FORMAT('_Measures'[Providers Pending Onboarding], "#,0")),
			    28, IF(ISBLANK('_Measures'[Providers With QA Flags]), "—", FORMAT('_Measures'[Providers With QA Flags], "#,0")),
			    29, IF(ISBLANK('_Measures'[QA Flagged Homes]), "—", FORMAT('_Measures'[QA Flagged Homes], "#,0")),
			    30, IF(ISBLANK('_Measures'[Referral Lifecycle Events]), "—", FORMAT('_Measures'[Referral Lifecycle Events], "#,0")),
			    31, IF(ISBLANK('_Measures'[Referrals Without Provider Assignment]), "—", FORMAT('_Measures'[Referrals Without Provider Assignment], "#,0")),
			    32, IF(ISBLANK('_Measures'[Unsuccessful Offers on Referrals Under Offer]), "—", FORMAT('_Measures'[Unsuccessful Offers on Referrals Under Offer], "#,0")), BLANK()))
```

<a id="business-requirements-catalogued"></a>
## Requirements catalogued

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-310.

Action metric, scoring evidence component or catalogue count

```dax
DISTINCTCOUNTNOBLANK('ref_RID'[Req ID])
```

Source tables: No direct physical source asserted.

<a id="business-requirements-linked-to-kpis"></a>
## Requirements linked to KPIs

Model: **business**. Container: `_Report Journey Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-311.

Action metric, scoring evidence component or catalogue count

```dax
COUNTROWS(INTERSECT(VALUES('ref_RID'[Req ID]), VALUES('ref_KPI_RID_Linkage'[Req ID])))
```

Source tables: No direct physical source asserted.

<a id="business-residential-homes"></a>
## Residential Homes

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-49.

```dax
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Residential" )
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-snapshot-month-in-window"></a>
## Snapshot Month In Window

Model: **business**. Container: `_Design Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Reporting window, anchor or dynamic selector

```dax
VAR anchor = [Snapshot Window Anchor]
			VAR axis_month = MAX ( 'dim_snapshot_month'[month_start] )
			VAR months = [Snapshot Window Months]
			RETURN IF ( NOT ISBLANK ( anchor ) && NOT ISBLANK ( axis_month )
			    && axis_month >= EDATE ( anchor, 1 - months ) && axis_month <= anchor, 1, 0 )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-snapshot-placement-target-hit-rate"></a>
## Snapshot Placement Target Hit Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-312.

```dax
DIVIDE (
			    [Snapshot Referrals Placed by Required Date],
			    CALCULATE (
			        [Snapshot Referrals],
			        FILTER (
			            'fact_referral_snapshot',
			            NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
			                && NOT ISBLANK ( 'fact_referral_snapshot'[required_placement_date] )
			        )
			    )
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-snapshot-referrals"></a>
## Snapshot Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-028.

```dax
DISTINCTCOUNT ( 'fact_referral_snapshot'[referral_id] )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-snapshot-referrals-placed-by-required-date"></a>
## Snapshot Referrals Placed by Required Date

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-313.

```dax
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[placed_by_required_date] = TRUE () )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-snapshot-window-anchor"></a>
## Snapshot Window Anchor

Model: **business**. Container: `_Design Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Reporting window, anchor or dynamic selector

```dax
CALCULATE ( MAX ( 'fact_referral_snapshot'[snapshot_month_start] ), REMOVEFILTERS ( 'dim_snapshot_month' ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-snapshot-window-months"></a>
## Snapshot Window Months

Model: **business**. Container: `_Design Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Reporting window, anchor or dynamic selector

```dax
SELECTEDVALUE ( 'Snapshot Window'[Ordinal], 12 )
```

Source tables: No direct physical source asserted.

<a id="business-snapshot-referrals-mom-change"></a>
## Snapshot referrals MoM change

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-119.

Saved detail count in the required record context

```dax
VAR currentTotal = [Snapshot Referrals]
			VAR previousTotal = [Snapshot referrals previous month]
			RETURN IF(NOT ISBLANK(currentTotal) && NOT ISBLANK(previousTotal), currentTotal - previousTotal)
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-snapshot-referrals-mom-percent"></a>
## Snapshot referrals MoM percent

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-120.

Saved detail count in the required record context

```dax
DIVIDE([Snapshot referrals MoM change],[Snapshot referrals previous month])
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-snapshot-referrals-previous-month"></a>
## Snapshot referrals previous month

Model: **business**. Container: `_Story Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-118.

Saved detail count in the required record context

```dax
VAR currentMonth = SELECTEDVALUE('dim_snapshot_month'[month_start])
			RETURN IF(NOT ISBLANK(currentMonth), CALCULATE([Snapshot Referrals], REMOVEFILTERS('dim_snapshot_month'), 'dim_snapshot_month'[month_start] = EDATE(currentMonth,-1)))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-spot-offer-rate"></a>
## Spot Offer Rate

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-062.

```dax
DIVIDE ( [Spot Offers], [Non-Draft Offers] )
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-spot-offers"></a>
## Spot Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-060.

```dax
CALCULATE ( [Non-Draft Offers], 'dim_provider_home (offer)'[is_spot] = TRUE () )
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`

<a id="business-spot-offers-on-referrals-under-offer"></a>
## Spot Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-27.

```dax
VAR homes =
			    CALCULATETABLE (
			        VALUES ( 'dim_provider_home'[provider_home_id] ),
			        KEEPFILTERS ( 'dim_provider_home'[is_spot] == TRUE () )
			    )
			RETURN
			    CALCULATE (
			        [Offers on Referrals Under Offer],
			        KEEPFILTERS ( TREATAS ( homes, 'fact_offer'[provider_home_id] ) )
			    )
```

Source tables: `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`

<a id="business-successful-offers-on-referrals-under-offer"></a>
## Successful Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-15.

```dax
CALCULATE (
			    [Accepted Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-successful-offers-to-ipa-completed-percent"></a>
## Successful Offers to IPA Completed %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-86.

```dax
DIVIDE ( [IPA Completed], [Accepted Offers] )
```

Source tables: `gold.fact_ipa`; `gold.fact_offer`

<a id="business-supported-accommodation-homes"></a>
## Supported Accommodation Homes

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-50.

```dax
CALCULATE (
			    [Provider Homes Registered],
			    'dim_provider_home'[service_type] = "Supported Accommodation"
			)
```

Source tables: `gold.dim_provider`; `gold.dim_provider_home`

<a id="business-target-hit-rate-at-snapshot"></a>
## Target Hit Rate at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-314.

```dax
DIVIDE (
			    [Referrals Placed by Target at Snapshot],
			    CALCULATE (
			        [Snapshot Referrals],
			        FILTER (
			            'fact_referral_snapshot',
			            NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
			                && NOT ISBLANK ( 'fact_referral_snapshot'[required_placement_date] )
			        )
			    )
			)
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-total-gendered-referrals"></a>
## Total Gendered Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-07, GOLD-KPI-113.

```dax
CALCULATE ( [Total Referrals], KEEPFILTERS ( FILTER ( 'dim_person', NOT ISBLANK ( 'dim_person'[gender_clean] ) && 'dim_person'[gender_clean] <> "Unknown" ) ) )
```

Source tables: `gold.dim_person`; `gold.fact_referral`

<a id="business-total-ipa-weekly-cost"></a>
## Total IPA Weekly Cost

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-098.

```dax
SUM ( 'fact_ipa'[estimated_weekly_cost] )
```

Source tables: `gold.fact_ipa`

<a id="business-total-lifetime-cost"></a>
## Total Lifetime Cost

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-315.

```dax
CALCULATE ( [Lifetime Placement Cost], REMOVEFILTERS ( 'fact_ipa' ) )
```

Source tables: `gold.fact_ipa`

<a id="business-total-offers-made-previous-month"></a>
## Total Offers Made Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-317.

```dax
CALCULATE ( [Total Offers at Snapshot], DATEADD ( 'dim_snapshot_month'[month_start], -1, MONTH ) )
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-total-offers-made-variance"></a>
## Total Offers Made Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-318.

```dax
[Total Offers at Snapshot] - [Total Offers Made Previous Month]
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-total-offers-made-variance-color"></a>
## Total Offers Made Variance Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Total Offers Made Variance] > 0, "green", IF([Total Offers Made Variance] < 0, "red", "grey"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-total-offers-made-variance-indicator"></a>
## Total Offers Made Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Total Offers Made Variance] > 0, "▲", IF([Total Offers Made Variance]< 0, "▼", "–"))
```

Source tables: `gold.dim_snapshot_month`; `gold.fact_referral_snapshot`

<a id="business-total-offers-at-snapshot"></a>
## Total Offers at Snapshot

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-316.

```dax
SUM ( 'fact_referral_snapshot'[offer_count] )
```

Source tables: `gold.fact_referral_snapshot`

<a id="business-total-referrals"></a>
## Total Referrals

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-26, KPI-01.

```dax
DISTINCTCOUNT ( 'fact_referral'[referral_id] )
```

Source tables: `gold.fact_referral`

<a id="business-total-referrals-mom-percent"></a>
## Total Referrals MoM %

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-319.

```dax
DIVIDE ( [Total Referrals Variance], [Total Referrals Previous Month] )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-previous-month"></a>
## Total Referrals Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-320.

```dax
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-that-received-offers-ratio"></a>
## Total Referrals That Received Offers (Ratio)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-321.

```dax
DIVIDE(
			    [Referrals With Offers],
			    [Total Referrals],
			    0
			)
```

Source tables: `gold.fact_referral`

<a id="business-total-referrals-that-received-offers-previous-month"></a>
## Total Referrals That Received Offers Previous Month

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-322.

```dax
CALCULATE ([Total Referrals That Received Offers (Ratio)], DATEADD(dim_date[Date],-1,MONTH))
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-that-received-offers-variance"></a>
## Total Referrals That Received Offers Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-323.

```dax
[Total Referrals That Received Offers (Ratio)]-[Total Referrals That Received Offers Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-that-received-offers-variance-indicator-color"></a>
## Total Referrals That Received Offers Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF([Total Referrals That Received Offers Variance] > 0, "green", IF([Total Referrals That Received Offers Variance] < 0, "red", "grey"))
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-variance"></a>
## Total Referrals Variance

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-324.

```dax
[Total Referrals] - [Total Referrals Previous Month]
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-variance-indicator"></a>
## Total Referrals Variance Indicator

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Total Referrals Variance] > 0, "▲", IF ( [Total Referrals Variance] < 0, "▼", "–" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-total-referrals-variance-indicator-color"></a>
## Total Referrals Variance Indicator Color

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
IF ( [Total Referrals Variance] > 0, "green", IF ( [Total Referrals Variance] < 0, "red", "grey" ) )
```

Source tables: `gold.dim_date`; `gold.fact_referral`

<a id="business-under-offer"></a>
## Under offer

Model: **business**. Container: `_Explore Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-325.

Saved category-aware exploration metric

```dax
VAR selectedCategories=VALUES('Referral Category'[Category ID])
			VAR ids=CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]),TREATAS(selectedCategories,'bridge_referral_framework_category'[framework_category_id]))
			RETURN IF(ISCROSSFILTERED('Referral Category'),CALCULATE([Referrals Under Offer],KEEPFILTERS(TREATAS(ids,'fact_referral'[referral_id]))),[Referrals Under Offer])
```

Source tables: `gold.bridge_referral_framework_category`; `gold.dim_framework_category`; `gold.fact_referral`

<a id="business-unsuccessful-offers"></a>
## Unsuccessful Offers

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-054.

```dax
CALCULATE (
			    [Offers Submitted],
			    FILTER (
			        'fact_offer',
			        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
			            IN { "declined", "rejected", "withdrawn", "offer_unsuccessful", "offer_withdrawn" }
			    )
			)
```

Source tables: `gold.fact_offer`

<a id="business-unsuccessful-offers-under-offer-referrals"></a>
## Unsuccessful Offers (Under Offer Referrals)

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: GOLD-KPI-326.

```dax
CALCULATE (
			    [Unsuccessful Offers],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-unsuccessful-offers-on-referrals-under-offer"></a>
## Unsuccessful Offers on Referrals Under Offer

Model: **business**. Container: `_Measures`. Classification: **Business metric**. KPI records: KPI-16.

```dax
CALCULATE (
			    [Unsuccessful Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

Source tables: `gold.fact_offer`; `gold.fact_referral`

<a id="business-username"></a>
## Username

Model: **business**. Container: `_Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Legacy presentation, flag or row-filter expression

```dax
USERPRINCIPALNAME()
```

Source tables: No direct physical source asserted.

<a id="business-expired-docs"></a>
## expired_docs

Model: **business**. Container: `_Explorer KPI Measures`. Classification: **Display/filter helper**. KPI records: Helper/context only.

Per-document expiry flag: 1 expired, 0 dated and not expired; blank for unknown date or non-document totals.

```dax
VAR oneDocument = HASONEVALUE('dim_provider_submission_document'[document_id])
			VAR expiry = SELECTEDVALUE('dim_provider_submission_document'[expiry_date])
			RETURN IF(oneDocument && COUNTROWS('dim_provider_submission_document') > 0
			    && NOT ISBLANK(expiry), IF(expiry < TODAY(), 1, 0), BLANK())
```

<a id="mission-active-dq-rules"></a>
## Active DQ Rules

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-001.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } ) )
```

Source tables: `monitoring.cfg_data_quality_rule`

<a id="mission-archive-export-rows"></a>
## Archive Export Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-002.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_archive_table_export_load'[row_count] )
```

Source tables: `monitoring.cfg_archive_table_export_load`

<a id="mission-archive-file-failures"></a>
## Archive File Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-003.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-archive-file-rows-read"></a>
## Archive File Rows Read

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-004.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_archive_file_load'[rows_read] )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-archive-file-rows-written"></a>
## Archive File Rows Written

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-005.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_archive_file_load'[rows_written] )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-archive-files-awaiting-reload"></a>
## Archive Files Awaiting Reload

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-006.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Archive Files Processed], 'cfg_archive_file_load'[reload] = TRUE () )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-archive-files-processed"></a>
## Archive Files Processed

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-007.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_archive_file_load' )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-archive-pipeline-failures"></a>
## Archive Pipeline Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-008.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-archive-pipeline-runs"></a>
## Archive Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-009.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-archive-table-exports"></a>
## Archive Table Exports

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-010.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_archive_table_export_load' )
```

Source tables: `monitoring.cfg_archive_table_export_load`

<a id="mission-archive-table-exports-awaiting-reload"></a>
## Archive Table Exports Awaiting Reload

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-011.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Archive Table Exports], 'cfg_archive_table_export_load'[reload] = TRUE () )
```

Source tables: `monitoring.cfg_archive_table_export_load`

<a id="mission-archive-zip-batches"></a>
## Archive ZIP Batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-012.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_archive_zip_load' )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-archive-zip-batches-awaiting-reload"></a>
## Archive ZIP Batches Awaiting Reload

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-013.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Archive ZIP Batches], 'cfg_archive_zip_load'[reload] = TRUE () )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-archive-zip-files-declared"></a>
## Archive ZIP Files Declared

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-014.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_archive_zip_load'[file_count] )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-archived-nullable-columns"></a>
## Archived Nullable Columns

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-015.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archived_schema_live', UPPER ( COALESCE ( 'cfg_archived_schema_live'[is_nullable], "" ) ) IN { "TRUE", "YES", "Y", "1" } ) )
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-archived-schema-columns"></a>
## Archived Schema Columns

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-016.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_archived_schema_live' )
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-archived-schema-data-types"></a>
## Archived Schema Data Types

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-017.

Numeric/date operational definition in the latest saved model

```dax
DISTINCTCOUNT ( 'cfg_archived_schema_live'[data_type] )
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-archived-schema-tables"></a>
## Archived Schema Tables

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-018.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( SUMMARIZE ( 'cfg_archived_schema_live', 'cfg_archived_schema_live'[schema_name], 'cfg_archived_schema_live'[table_name] ) )
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-average-archive-zip-duration-min"></a>
## Average Archive ZIP Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-019.

Numeric/date operational definition in the latest saved model

```dax
AVERAGEX ( FILTER ( 'cfg_archive_zip_load', NOT ISBLANK ( 'cfg_archive_zip_load'[started_at] ) && NOT ISBLANK ( 'cfg_archive_zip_load'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_archive_zip_load'[started_at], 'cfg_archive_zip_load'[ended_at], SECOND ), 60.0 ) )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-average-pipeline-duration-min"></a>
## Average Pipeline Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-020.

Numeric/date operational definition in the latest saved model

```dax
AVERAGEX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-calendar-day-failures"></a>
## Calendar Day Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-021.

Numeric/date operational definition in the latest saved model

```dax
COALESCE([Failed Job Runs], 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-calendar-day-in-window"></a>
## Calendar Day In Window

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-022.

Numeric/date operational definition in the latest saved model

```dax
VAR d = SELECTEDVALUE('Load Calendar'[Date])
			RETURN IF(NOT ISBLANK(d) && d >= TODAY() - 364 && d <= TODAY(), 1, 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-calendar-day-other"></a>
## Calendar Day Other

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-023.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE([Job Runs], KEEPFILTERS(rpt_job_run_summary[Outcome] IN {"Running", "Other"})), 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-calendar-day-runs"></a>
## Calendar Day Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-024.

Numeric/date operational definition in the latest saved model

```dax
COALESCE([Job Runs], 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-completed-pipeline-runs"></a>
## Completed Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-025.

Numeric/date operational definition in the latest saved model

```dax
[Successful Pipeline Runs] + [Failed Pipeline Runs]
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-control-failures"></a>
## Control Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-026.

Numeric/date operational definition in the latest saved model

```dax
[Failed Pipeline Runs] + [Failed Archive ZIP Batches] + [Archive File Failures] + [Failed Archive Table Exports] + [Failed Gold Snapshots]
```

Source tables: `monitoring.cfg_archive_file_load`; `monitoring.cfg_archive_table_export_load`; `monitoring.cfg_archive_zip_load`; `monitoring.cfg_month_end_gold_run`; `monitoring.cfg_pipeline_run`

<a id="mission-critical-active-dq-rules"></a>
## Critical Active DQ Rules

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-027.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } && UPPER ( COALESCE ( 'cfg_data_quality_rule'[severity], "" ) ) = "CRITICAL" ) )
```

Source tables: `monitoring.cfg_data_quality_rule`

<a id="mission-critical-rules-failing"></a>
## Critical Rules Failing

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-028.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) = "CRITICAL" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-checked-rows"></a>
## DQ Checked Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-090.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_data_quality_result'[checked_row_count] )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-checks"></a>
## DQ Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-091.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_data_quality_result' )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-evaluated-checks"></a>
## DQ Evaluated Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-092.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "PASS", "SUCCESS", "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-failed-checks"></a>
## DQ Failed Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-093.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-failed-rows"></a>
## DQ Failed Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-094.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_data_quality_result'[failed_row_count] )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-failure-rate"></a>
## DQ Failure Rate

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-095.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [DQ Failed Checks], [DQ Evaluated Checks] )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dq-failures-with-sample-keys"></a>
## DQ Failures With Sample Keys

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-096.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } && NOT ISBLANK ( 'cfg_data_quality_result'[sample_key_json] ) ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-dashboard-last-refreshed"></a>
## Dashboard Last Refreshed

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT ( UTCNOW (), "dd mmm yyyy HH:mm" )
```

Source tables: No direct physical source asserted.

<a id="mission-day-explorer-job-visible"></a>
## Day Explorer Job Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_run_summary),
			    CALCULATE(COUNTROWS(rpt_job_run_summary), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(ISFILTERED('Load Calendar'[Date]) && NOT HASONEVALUE('Load Calendar'[Date]), 0, IF(n > 0, 1, 0))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-day-colour"></a>
## Day colour

Model: **mission**. Container: `_Load Experience`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
SWITCH(TRUE(),[Failures]>0,"#A43C49",[In progress or other]>0,"#66512B",[Successful]>=10,"#4C854F",[Successful]>0,"#345B3D","#242F28")
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-day-text-colour"></a>
## Day text colour

Model: **mission**. Container: `_Load Experience`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
"#F3F7EF"
```

Source tables: No direct physical source asserted.

<a id="mission-day-tile"></a>
## Day tile

Model: **mission**. Container: `_Load Experience`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR d=SELECTEDVALUE('Load Calendar'[Date])
			VAR n=COALESCE([Runs],0)
			RETURN IF(NOT ISBLANK(d), FORMAT(d,"d") & UNICHAR(10) & IF(d>TODAY(),"Future",SWITCH(TRUE(),[Failures]>0,"! " & FORMAT([Failures],"0") & " failed",[In progress or other]>0,"~ " & FORMAT(n,"0") & " runs",n>0,FORMAT(n,"0") & " OK","No loads")))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-discovery-calendar-failures"></a>
## Discovery calendar failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-029.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
			    FILTER('Discovery Job Runs', UPPER('Discovery Job Runs'[status]) IN {"FAILED", "FAILURE", "ERROR"}
			        || 'Discovery Job Runs'[steps_failed] > 0)), 0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-calendar-jobs"></a>
## Discovery calendar jobs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-030.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), 0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-calendar-other"></a>
## Discovery calendar other

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-031.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
			    FILTER('Discovery Job Runs', NOT(UPPER('Discovery Job Runs'[status]) IN {"SUCCESS", "SUCCESSFUL", "SUCCEEDED", "FAILED", "FAILURE", "ERROR"})
			        && COALESCE('Discovery Job Runs'[steps_failed], 0) = 0)), 0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-archive-zip-load-latest-key"></a>
## Discovery cfg_archive_zip_load Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_archive_zip_load, cfg_archive_zip_load[run_id], "DiscoveryTime", MAX(cfg_archive_zip_load[started_at])), ALLSELECTED(cfg_archive_zip_load))
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])), [DiscoveryTime], DESC, cfg_archive_zip_load[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_archive_zip_load[run_id])
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-discovery-cfg-archive-zip-load-latest-time"></a>
## Discovery cfg_archive_zip_load Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_archive_zip_load[started_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-discovery-cfg-archive-zip-load-rows"></a>
## Discovery cfg_archive_zip_load Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-032.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS(cfg_archive_zip_load), KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id]))), 0)
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-discovery-cfg-archive-zip-load-selected-time"></a>
## Discovery cfg_archive_zip_load Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_archive_zip_load[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-discovery-cfg-archive-zip-load-state"></a>
## Discovery cfg_archive_zip_load State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n = [Discovery cfg_archive_zip_load Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Source tables: `monitoring.cfg_archive_zip_load`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-archive-zip-load-visible"></a>
## Discovery cfg_archive_zip_load Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_archive_zip_load Rows] > 0, 1, 0)
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-discovery-cfg-archived-schema-live-latest-time"></a>
## Discovery cfg_archived_schema_live Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_archived_schema_live[contract_loaded_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-discovery-cfg-archived-schema-live-rows"></a>
## Discovery cfg_archived_schema_live Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-033.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS(cfg_archived_schema_live), KEEPFILTERS(TREATAS({[Discovery cfg_archived_schema_live Latest time]}, cfg_archived_schema_live[contract_loaded_at]))), 0)
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-discovery-cfg-archived-schema-live-selected-time"></a>
## Discovery cfg_archived_schema_live Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_archived_schema_live[contract_loaded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_archived_schema_live Latest time]}, cfg_archived_schema_live[contract_loaded_at])))
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-discovery-cfg-archived-schema-live-state"></a>
## Discovery cfg_archived_schema_live State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n = [Discovery cfg_archived_schema_live Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Source tables: `monitoring.cfg_archived_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-archived-schema-live-visible"></a>
## Discovery cfg_archived_schema_live Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_archived_schema_live Rows] > 0, 1, 0)
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-discovery-cfg-bronze-schema-live-context"></a>
## Discovery cfg_bronze_schema_live Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Day=SELECTEDVALUE('Load Calendar'[Date])
			VAR Time=[Discovery cfg_bronze_schema_live Latest time]
			RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-discovery-batches"></a>
## Discovery cfg_bronze_schema_live Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-034.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[run_id]),KEEPFILTERS(FILTER('cfg_bronze_schema_live',(NOT DateChosen || ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days))) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]),CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time] },'cfg_bronze_schema_live'[captured_at]))),CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))),0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-distinct-objects"></a>
## Discovery cfg_bronze_schema_live Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-035.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[table_name]),KEEPFILTERS(FILTER('cfg_bronze_schema_live',(NOT DateChosen || ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days))) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]),CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[table_name]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time] },'cfg_bronze_schema_live'[captured_at]))),CALCULATE(DISTINCTCOUNT('cfg_bronze_schema_live'[table_name]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))),0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-latest-key"></a>
## Discovery cfg_bronze_schema_live Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_bronze_schema_live, cfg_bronze_schema_live[run_id],
			    "DiscoveryTime", MAX(cfg_bronze_schema_live[captured_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_bronze_schema_live[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_bronze_schema_live[run_id])
```

Source tables: `monitoring.cfg_bronze_schema_live`

<a id="mission-discovery-cfg-bronze-schema-live-latest-time"></a>
## Discovery cfg_bronze_schema_live Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_bronze_schema_live[captured_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_bronze_schema_live`

<a id="mission-discovery-cfg-bronze-schema-live-rows"></a>
## Discovery cfg_bronze_schema_live Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-036.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_bronze_schema_live'),KEEPFILTERS(FILTER('cfg_bronze_schema_live',(NOT DateChosen || ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days))) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]),CALCULATE(COUNTROWS('cfg_bronze_schema_live'),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time] },'cfg_bronze_schema_live'[captured_at]))),CALCULATE(COUNTROWS('cfg_bronze_schema_live'),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))),0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-scope-count"></a>
## Discovery cfg_bronze_schema_live Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-037.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS(SUMMARIZE('cfg_bronze_schema_live','cfg_bronze_schema_live'[table_name],'cfg_bronze_schema_live'[column_name])),KEEPFILTERS(FILTER('cfg_bronze_schema_live',(NOT DateChosen || ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days))) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]),CALCULATE(COUNTROWS(SUMMARIZE('cfg_bronze_schema_live','cfg_bronze_schema_live'[table_name],'cfg_bronze_schema_live'[column_name])),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time] },'cfg_bronze_schema_live'[captured_at]))),CALCULATE(COUNTROWS(SUMMARIZE('cfg_bronze_schema_live','cfg_bronze_schema_live'[table_name],'cfg_bronze_schema_live'[column_name])),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))),0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-selected-time"></a>
## Discovery cfg_bronze_schema_live Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_bronze_schema_live'[captured_at]),KEEPFILTERS(FILTER('cfg_bronze_schema_live',(NOT DateChosen || ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days))) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]),CALCULATE(MAX('cfg_bronze_schema_live'[captured_at]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time] },'cfg_bronze_schema_live'[captured_at]))),CALCULATE(MAX('cfg_bronze_schema_live'[captured_at]),KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-state"></a>
## Discovery cfg_bronze_schema_live State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_bronze_schema_live Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-bronze-schema-live-visible"></a>
## Discovery cfg_bronze_schema_live Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_bronze_schema_live Rows]>0,1,0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-context"></a>
## Discovery cfg_data_domain Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Historical=[Discovery history selected]=1
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			RETURN IF(Historical,"Selected discovery history",IF(AllVersions,"All retained discovery versions",
			    "Latest discovery · " & FORMAT([Discovery cfg_data_domain Latest time],"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-discovery-batches"></a>
## Discovery cfg_data_domain Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-038.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-distinct-objects"></a>
## Discovery cfg_data_domain Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-039.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-latest-key"></a>
## Discovery cfg_data_domain Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_data_domain, cfg_data_domain[run_id],
			    "DiscoveryTime", MAX(cfg_data_domain[profiled_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_data_domain[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_data_domain[run_id])
```

Source tables: `monitoring.cfg_data_domain`

<a id="mission-discovery-cfg-data-domain-latest-time"></a>
## Discovery cfg_data_domain Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_data_domain[profiled_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_data_domain`

<a id="mission-discovery-cfg-data-domain-rows"></a>
## Discovery cfg_data_domain Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-040.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(COUNTROWS(cfg_data_domain),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(COUNTROWS(cfg_data_domain),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(COUNTROWS(cfg_data_domain),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-scope-count"></a>
## Discovery cfg_data_domain Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-041.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(COUNTROWS(SUMMARIZE(FILTER(cfg_data_domain,COALESCE(cfg_data_domain[profile_status],"PROFILED") IN {"PROFILED","EMPTY"}),cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(COUNTROWS(SUMMARIZE(FILTER(cfg_data_domain,COALESCE(cfg_data_domain[profile_status],"PROFILED") IN {"PROFILED","EMPTY"}),cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(COUNTROWS(SUMMARIZE(FILTER(cfg_data_domain,COALESCE(cfg_data_domain[profile_status],"PROFILED") IN {"PROFILED","EMPTY"}),cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-selected-time"></a>
## Discovery cfg_data_domain Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(MAX(cfg_data_domain[profiled_at]),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(MAX(cfg_data_domain[profiled_at]),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(MAX(cfg_data_domain[profiled_at]),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-state"></a>
## Discovery cfg_data_domain State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_data_domain Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-data-domain-visible"></a>
## Discovery cfg_data_domain Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_data_domain Rows]>0,1,0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-gold-lineage-mapping-rows"></a>
## Discovery cfg_gold_lineage_mapping Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-042.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((COUNTROWS('cfg_gold_lineage_mapping')),0)
```

Source tables: `monitoring.cfg_gold_lineage_mapping`

<a id="mission-discovery-cfg-gold-lineage-mapping-state"></a>
## Discovery cfg_gold_lineage_mapping State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_gold_lineage_mapping Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_gold_lineage_mapping`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-gold-lineage-mapping-visible"></a>
## Discovery cfg_gold_lineage_mapping Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_gold_lineage_mapping Rows]>0,1,0)
```

Source tables: `monitoring.cfg_gold_lineage_mapping`

<a id="mission-discovery-cfg-location-coordinate-rows"></a>
## Discovery cfg_location_coordinate Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-043.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((COUNTROWS('cfg_location_coordinate')),0)
```

Source tables: `monitoring.cfg_location_coordinate`

<a id="mission-discovery-cfg-location-coordinate-state"></a>
## Discovery cfg_location_coordinate State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_location_coordinate Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_location_coordinate`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-location-coordinate-visible"></a>
## Discovery cfg_location_coordinate Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_location_coordinate Rows]>0,1,0)
```

Source tables: `monitoring.cfg_location_coordinate`

<a id="mission-discovery-cfg-month-end-gold-run-latest-key"></a>
## Discovery cfg_month_end_gold_run Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_month_end_gold_run, cfg_month_end_gold_run[run_id], "DiscoveryTime", MAX(cfg_month_end_gold_run[started_at])), ALLSELECTED(cfg_month_end_gold_run))
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])), [DiscoveryTime], DESC, cfg_month_end_gold_run[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_month_end_gold_run[run_id])
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-discovery-cfg-month-end-gold-run-latest-time"></a>
## Discovery cfg_month_end_gold_run Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_month_end_gold_run[started_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-discovery-cfg-month-end-gold-run-rows"></a>
## Discovery cfg_month_end_gold_run Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-044.

Numeric/date operational definition in the latest saved model

```dax
COALESCE(CALCULATE(COUNTROWS(cfg_month_end_gold_run), KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id]))), 0)
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-discovery-cfg-month-end-gold-run-selected-time"></a>
## Discovery cfg_month_end_gold_run Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_month_end_gold_run[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id])))
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-discovery-cfg-month-end-gold-run-state"></a>
## Discovery cfg_month_end_gold_run State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n = [Discovery cfg_month_end_gold_run Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_month_end_gold_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-month-end-gold-run-visible"></a>
## Discovery cfg_month_end_gold_run Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_month_end_gold_run Rows] > 0, 1, 0)
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-discovery-cfg-referential-exception-latest-key"></a>
## Discovery cfg_referential_exception Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_referential_exception, cfg_referential_exception[run_id],
			    "DiscoveryTime", MAX(cfg_referential_exception[detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_referential_exception[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_referential_exception[run_id])
```

Source tables: `monitoring.cfg_referential_exception`

<a id="mission-discovery-cfg-referential-exception-latest-time"></a>
## Discovery cfg_referential_exception Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_referential_exception[detected_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_referential_exception`

<a id="mission-discovery-cfg-referential-exception-rows"></a>
## Discovery cfg_referential_exception Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-045.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_referential_exception'),KEEPFILTERS(FILTER('cfg_referential_exception',(NOT DateChosen || ((NOT ISBLANK('cfg_referential_exception'[detected_at]) && INT('cfg_referential_exception'[detected_at]) IN Days))) && (NOT JobChosen || 'cfg_referential_exception'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_referential_exception Latest key]),CALCULATE(COUNTROWS('cfg_referential_exception'),KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest time] },'cfg_referential_exception'[detected_at]))),CALCULATE(COUNTROWS('cfg_referential_exception'),KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest key]}, cfg_referential_exception[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-referential-exception-selected-time"></a>
## Discovery cfg_referential_exception Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_referential_exception'[detected_at]),KEEPFILTERS(FILTER('cfg_referential_exception',(NOT DateChosen || ((NOT ISBLANK('cfg_referential_exception'[detected_at]) && INT('cfg_referential_exception'[detected_at]) IN Days))) && (NOT JobChosen || 'cfg_referential_exception'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_referential_exception Latest key]),CALCULATE(MAX('cfg_referential_exception'[detected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest time] },'cfg_referential_exception'[detected_at]))),CALCULATE(MAX('cfg_referential_exception'[detected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest key]}, cfg_referential_exception[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-referential-exception-state"></a>
## Discovery cfg_referential_exception State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_referential_exception Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-referential-exception-visible"></a>
## Discovery cfg_referential_exception Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_referential_exception Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-rejected-row-latest-key"></a>
## Discovery cfg_rejected_row Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_rejected_row, cfg_rejected_row[run_id],
			    "DiscoveryTime", MAX(cfg_rejected_row[rejected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_rejected_row[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_rejected_row[run_id])
```

Source tables: `monitoring.cfg_rejected_row`

<a id="mission-discovery-cfg-rejected-row-latest-time"></a>
## Discovery cfg_rejected_row Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_rejected_row[rejected_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_rejected_row`

<a id="mission-discovery-cfg-rejected-row-rows"></a>
## Discovery cfg_rejected_row Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-046.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_rejected_row'),KEEPFILTERS(FILTER('cfg_rejected_row',(NOT DateChosen || ((NOT ISBLANK('cfg_rejected_row'[rejected_at]) && INT('cfg_rejected_row'[rejected_at]) IN Days))) && (NOT JobChosen || 'cfg_rejected_row'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_rejected_row Latest key]),CALCULATE(COUNTROWS('cfg_rejected_row'),KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest time] },'cfg_rejected_row'[rejected_at]))),CALCULATE(COUNTROWS('cfg_rejected_row'),KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest key]}, cfg_rejected_row[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-rejected-row-selected-time"></a>
## Discovery cfg_rejected_row Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_rejected_row'[rejected_at]),KEEPFILTERS(FILTER('cfg_rejected_row',(NOT DateChosen || ((NOT ISBLANK('cfg_rejected_row'[rejected_at]) && INT('cfg_rejected_row'[rejected_at]) IN Days))) && (NOT JobChosen || 'cfg_rejected_row'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_rejected_row Latest key]),CALCULATE(MAX('cfg_rejected_row'[rejected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest time] },'cfg_rejected_row'[rejected_at]))),CALCULATE(MAX('cfg_rejected_row'[rejected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest key]}, cfg_rejected_row[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-rejected-row-state"></a>
## Discovery cfg_rejected_row State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_rejected_row Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-rejected-row-visible"></a>
## Discovery cfg_rejected_row Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_rejected_row Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-contract-column-latest-time"></a>
## Discovery cfg_schema_contract_column Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_schema_contract_column[contract_loaded_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_schema_contract_column`

<a id="mission-discovery-cfg-schema-contract-column-rows"></a>
## Discovery cfg_schema_contract_column Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-047.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(COUNTROWS('cfg_schema_contract_column'),KEEPFILTERS(FILTER('cfg_schema_contract_column',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_contract_column'[contract_loaded_at]) && INT('cfg_schema_contract_column'[contract_loaded_at]) IN Days)))))),CALCULATE(COUNTROWS('cfg_schema_contract_column'),KEEPFILTERS(TREATAS({[Discovery cfg_schema_contract_column Latest time]}, cfg_schema_contract_column[contract_loaded_at]))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-contract-column-selected-time"></a>
## Discovery cfg_schema_contract_column Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(MAX('cfg_schema_contract_column'[contract_loaded_at]),KEEPFILTERS(FILTER('cfg_schema_contract_column',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_contract_column'[contract_loaded_at]) && INT('cfg_schema_contract_column'[contract_loaded_at]) IN Days)))))),CALCULATE(MAX('cfg_schema_contract_column'[contract_loaded_at]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_contract_column Latest time]}, cfg_schema_contract_column[contract_loaded_at]))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-contract-column-state"></a>
## Discovery cfg_schema_contract_column State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_schema_contract_column Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-contract-column-visible"></a>
## Discovery cfg_schema_contract_column Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_schema_contract_column Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-definition-candidate-rows"></a>
## Discovery cfg_schema_definition_candidate Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-048.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((COUNTROWS('cfg_schema_definition_candidate')),0)
```

Source tables: `monitoring.cfg_schema_definition_candidate`

<a id="mission-discovery-cfg-schema-definition-candidate-state"></a>
## Discovery cfg_schema_definition_candidate State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_schema_definition_candidate Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_definition_candidate`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-definition-candidate-visible"></a>
## Discovery cfg_schema_definition_candidate Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_schema_definition_candidate Rows]>0,1,0)
```

Source tables: `monitoring.cfg_schema_definition_candidate`

<a id="mission-discovery-cfg-schema-drift-definition-latest-time"></a>
## Discovery cfg_schema_drift_definition Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_schema_drift_definition[definition_loaded_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_schema_drift_definition`

<a id="mission-discovery-cfg-schema-drift-definition-rows"></a>
## Discovery cfg_schema_drift_definition Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-049.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(COUNTROWS('cfg_schema_drift_definition'),KEEPFILTERS(FILTER('cfg_schema_drift_definition',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_definition'[definition_loaded_at]) && INT('cfg_schema_drift_definition'[definition_loaded_at]) IN Days)))))),CALCULATE(COUNTROWS('cfg_schema_drift_definition'),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_definition Latest time]}, cfg_schema_drift_definition[definition_loaded_at]))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-definition-selected-time"></a>
## Discovery cfg_schema_drift_definition Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(MAX('cfg_schema_drift_definition'[definition_loaded_at]),KEEPFILTERS(FILTER('cfg_schema_drift_definition',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_definition'[definition_loaded_at]) && INT('cfg_schema_drift_definition'[definition_loaded_at]) IN Days)))))),CALCULATE(MAX('cfg_schema_drift_definition'[definition_loaded_at]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_definition Latest time]}, cfg_schema_drift_definition[definition_loaded_at]))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-definition-state"></a>
## Discovery cfg_schema_drift_definition State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_schema_drift_definition Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-definition-visible"></a>
## Discovery cfg_schema_drift_definition Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_schema_drift_definition Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-context"></a>
## Discovery cfg_schema_drift_event Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Day=SELECTEDVALUE('Load Calendar'[Date])
			VAR Time=[Discovery cfg_schema_drift_event Latest time]
			RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-discovery-batches"></a>
## Discovery cfg_schema_drift_event Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-050.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[run_id]),KEEPFILTERS(FILTER('cfg_schema_drift_event',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days))) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]),CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time] },'cfg_schema_drift_event'[detected_at]))),CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-distinct-objects"></a>
## Discovery cfg_schema_drift_event Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-051.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[target_table]),KEEPFILTERS(FILTER('cfg_schema_drift_event',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days))) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]),CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[target_table]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time] },'cfg_schema_drift_event'[detected_at]))),CALCULATE(DISTINCTCOUNT('cfg_schema_drift_event'[target_table]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-latest-key"></a>
## Discovery cfg_schema_drift_event Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_schema_drift_event, cfg_schema_drift_event[run_id],
			    "DiscoveryTime", MAX(cfg_schema_drift_event[detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_schema_drift_event[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_schema_drift_event[run_id])
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-discovery-cfg-schema-drift-event-latest-time"></a>
## Discovery cfg_schema_drift_event Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_schema_drift_event[detected_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-discovery-cfg-schema-drift-event-rows"></a>
## Discovery cfg_schema_drift_event Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-052.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_schema_drift_event'),KEEPFILTERS(FILTER('cfg_schema_drift_event',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days))) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]),CALCULATE(COUNTROWS('cfg_schema_drift_event'),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time] },'cfg_schema_drift_event'[detected_at]))),CALCULATE(COUNTROWS('cfg_schema_drift_event'),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-scope-count"></a>
## Discovery cfg_schema_drift_event Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-053.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS(SUMMARIZE('cfg_schema_drift_event','cfg_schema_drift_event'[drift_key])),KEEPFILTERS(FILTER('cfg_schema_drift_event',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days))) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]),CALCULATE(COUNTROWS(SUMMARIZE('cfg_schema_drift_event','cfg_schema_drift_event'[drift_key])),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time] },'cfg_schema_drift_event'[detected_at]))),CALCULATE(COUNTROWS(SUMMARIZE('cfg_schema_drift_event','cfg_schema_drift_event'[drift_key])),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-selected-time"></a>
## Discovery cfg_schema_drift_event Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_schema_drift_event'[detected_at]),KEEPFILTERS(FILTER('cfg_schema_drift_event',(NOT DateChosen || ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days))) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]),CALCULATE(MAX('cfg_schema_drift_event'[detected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time] },'cfg_schema_drift_event'[detected_at]))),CALCULATE(MAX('cfg_schema_drift_event'[detected_at]),KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-state"></a>
## Discovery cfg_schema_drift_event State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_schema_drift_event Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-schema-drift-event-visible"></a>
## Discovery cfg_schema_drift_event Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_schema_drift_event Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-export-load-latest-key"></a>
## Discovery cfg_silver_export_load Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_silver_export_load, cfg_silver_export_load[run_id],
			    "DiscoveryTime", MAX(cfg_silver_export_load[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_silver_export_load[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_silver_export_load[run_id])
```

Source tables: `monitoring.cfg_silver_export_load`

<a id="mission-discovery-cfg-silver-export-load-latest-time"></a>
## Discovery cfg_silver_export_load Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_silver_export_load[started_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_silver_export_load`

<a id="mission-discovery-cfg-silver-export-load-rows"></a>
## Discovery cfg_silver_export_load Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-054.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_silver_export_load'),KEEPFILTERS(FILTER('cfg_silver_export_load',(NOT DateChosen || (NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days)) && (NOT JobChosen || 'cfg_silver_export_load'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_silver_export_load Latest key]),CALCULATE(COUNTROWS('cfg_silver_export_load'),KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest time] },'cfg_silver_export_load'[started_at]))),CALCULATE(COUNTROWS('cfg_silver_export_load'),KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest key]}, cfg_silver_export_load[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-export-load-selected-time"></a>
## Discovery cfg_silver_export_load Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_silver_export_load'[started_at]),KEEPFILTERS(FILTER('cfg_silver_export_load',(NOT DateChosen || (NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days)) && (NOT JobChosen || 'cfg_silver_export_load'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_silver_export_load Latest key]),CALCULATE(MAX('cfg_silver_export_load'[started_at]),KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest time] },'cfg_silver_export_load'[started_at]))),CALCULATE(MAX('cfg_silver_export_load'[started_at]),KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest key]}, cfg_silver_export_load[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-export-load-state"></a>
## Discovery cfg_silver_export_load State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_silver_export_load Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-export-load-visible"></a>
## Discovery cfg_silver_export_load Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_silver_export_load Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-load-control-latest-key"></a>
## Discovery cfg_silver_load_control Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_silver_load_control, cfg_silver_load_control[run_id],
			    "DiscoveryTime", MAX(cfg_silver_load_control[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_silver_load_control[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_silver_load_control[run_id])
```

Source tables: `monitoring.cfg_silver_load_control`

<a id="mission-discovery-cfg-silver-load-control-latest-time"></a>
## Discovery cfg_silver_load_control Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_silver_load_control[started_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_silver_load_control`

<a id="mission-discovery-cfg-silver-load-control-rows"></a>
## Discovery cfg_silver_load_control Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-055.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(COUNTROWS('cfg_silver_load_control'),KEEPFILTERS(FILTER('cfg_silver_load_control',(NOT DateChosen || (NOT ISBLANK(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) && INT(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) IN Days))))),IF(ISBLANK([Discovery cfg_silver_load_control Latest key]),CALCULATE(COUNTROWS('cfg_silver_load_control'),KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest time] },'cfg_silver_load_control'[started_at]))),CALCULATE(COUNTROWS('cfg_silver_load_control'),KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest key]}, cfg_silver_load_control[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_load_control`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-load-control-selected-time"></a>
## Discovery cfg_silver_load_control Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen,CALCULATE(MAX('cfg_silver_load_control'[started_at]),KEEPFILTERS(FILTER('cfg_silver_load_control',(NOT DateChosen || (NOT ISBLANK(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) && INT(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) IN Days))))),IF(ISBLANK([Discovery cfg_silver_load_control Latest key]),CALCULATE(MAX('cfg_silver_load_control'[started_at]),KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest time] },'cfg_silver_load_control'[started_at]))),CALCULATE(MAX('cfg_silver_load_control'[started_at]),KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest key]}, cfg_silver_load_control[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_load_control`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-load-control-state"></a>
## Discovery cfg_silver_load_control State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_silver_load_control Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_load_control`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-silver-load-control-visible"></a>
## Discovery cfg_silver_load_control Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_silver_load_control Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_load_control`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-context"></a>
## Discovery cfg_table_load_metric Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Day=SELECTEDVALUE('Load Calendar'[Date])
			VAR Time=[Discovery cfg_table_load_metric Latest time]
			RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-discovery-batches"></a>
## Discovery cfg_table_load_metric Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-056.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[run_id]),KEEPFILTERS(FILTER('cfg_table_load_metric',(NOT DateChosen || ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days))) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_table_load_metric Latest key]),CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time] },'cfg_table_load_metric'[recorded_at]))),CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[run_id]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-distinct-objects"></a>
## Discovery cfg_table_load_metric Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-057.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[source_object]),KEEPFILTERS(FILTER('cfg_table_load_metric',(NOT DateChosen || ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days))) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_table_load_metric Latest key]),CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[source_object]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time] },'cfg_table_load_metric'[recorded_at]))),CALCULATE(DISTINCTCOUNT('cfg_table_load_metric'[source_object]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-latest-key"></a>
## Discovery cfg_table_load_metric Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_table_load_metric, cfg_table_load_metric[run_id],
			    "DiscoveryTime", MAX(cfg_table_load_metric[recorded_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_table_load_metric[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_table_load_metric[run_id])
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-discovery-cfg-table-load-metric-latest-time"></a>
## Discovery cfg_table_load_metric Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(cfg_table_load_metric[recorded_at]), REMOVEFILTERS())
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-discovery-cfg-table-load-metric-rows"></a>
## Discovery cfg_table_load_metric Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-058.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('cfg_table_load_metric'),KEEPFILTERS(FILTER('cfg_table_load_metric',(NOT DateChosen || ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days))) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_table_load_metric Latest key]),CALCULATE(COUNTROWS('cfg_table_load_metric'),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time] },'cfg_table_load_metric'[recorded_at]))),CALCULATE(COUNTROWS('cfg_table_load_metric'),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-scope-count"></a>
## Discovery cfg_table_load_metric Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-059.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS(SUMMARIZE('cfg_table_load_metric','cfg_table_load_metric'[target_object])),KEEPFILTERS(FILTER('cfg_table_load_metric',(NOT DateChosen || ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days))) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_table_load_metric Latest key]),CALCULATE(COUNTROWS(SUMMARIZE('cfg_table_load_metric','cfg_table_load_metric'[target_object])),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time] },'cfg_table_load_metric'[recorded_at]))),CALCULATE(COUNTROWS(SUMMARIZE('cfg_table_load_metric','cfg_table_load_metric'[target_object])),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-selected-time"></a>
## Discovery cfg_table_load_metric Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('cfg_table_load_metric'[recorded_at]),KEEPFILTERS(FILTER('cfg_table_load_metric',(NOT DateChosen || ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days))) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery cfg_table_load_metric Latest key]),CALCULATE(MAX('cfg_table_load_metric'[recorded_at]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time] },'cfg_table_load_metric'[recorded_at]))),CALCULATE(MAX('cfg_table_load_metric'[recorded_at]),KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-state"></a>
## Discovery cfg_table_load_metric State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery cfg_table_load_metric Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-cfg-table-load-metric-visible"></a>
## Discovery cfg_table_load_metric Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery cfg_table_load_metric Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-contracts-calendar-changes"></a>
## Discovery contracts calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-060.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_schema_drift_event'), ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)),'cfg_schema_drift_event'[drift_key])),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-contracts-calendar-critical"></a>
## Discovery contracts calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-061.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(0,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-contracts-calendar-discoveries"></a>
## Discovery contracts calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-062.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_bronze_schema_live'), ((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_bronze_schema_live'[job_run_id] IN Jobs)),'cfg_bronze_schema_live'[run_id])) + COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_schema_contract_column'), ((NOT ISBLANK('cfg_schema_contract_column'[contract_loaded_at]) && INT('cfg_schema_contract_column'[contract_loaded_at]) IN Days)) && (TRUE())),'cfg_schema_contract_column'[contract_loaded_at])),0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-contracts-calendar-linked-job-visible"></a>
## Discovery contracts calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('cfg_schema_drift_event'),((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days)) && (TRUE()) && 'cfg_schema_drift_event'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_bronze_schema_live'),((NOT ISBLANK('cfg_bronze_schema_live'[captured_at]) && INT('cfg_bronze_schema_live'[captured_at]) IN Days)) && (TRUE()) && 'cfg_bronze_schema_live'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-domains-calendar-changes"></a>
## Discovery domains calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-063.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('cfg_data_domain'), ((NOT ISBLANK('cfg_data_domain'[profiled_at]) && INT('cfg_data_domain'[profiled_at]) IN Days)) && (cfg_data_domain[change_type] IN {"ADDED","REMOVED"}) && (NOT JobChosen || 'cfg_data_domain'[job_run_id] IN Jobs))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-domains-calendar-critical"></a>
## Discovery domains calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-064.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(0,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-domains-calendar-discoveries"></a>
## Discovery domains calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-065.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_data_domain'), ((NOT ISBLANK('cfg_data_domain'[profiled_at]) && INT('cfg_data_domain'[profiled_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_data_domain'[job_run_id] IN Jobs)),'cfg_data_domain'[run_id])),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-domains-calendar-linked-job-visible"></a>
## Discovery domains calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('cfg_data_domain'),((NOT ISBLANK('cfg_data_domain'[profiled_at]) && INT('cfg_data_domain'[profiled_at]) IN Days)) && (TRUE()) && 'cfg_data_domain'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-drift-calendar-changes"></a>
## Discovery drift calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-066.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_schema_drift_event'), ((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_schema_drift_event'[job_run_id] IN Jobs)),'cfg_schema_drift_event'[drift_key])),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-drift-calendar-critical"></a>
## Discovery drift calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-067.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(0,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-drift-calendar-discoveries"></a>
## Discovery drift calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-068.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_schema_drift_definition'), ((NOT ISBLANK('cfg_schema_drift_definition'[definition_loaded_at]) && INT('cfg_schema_drift_definition'[definition_loaded_at]) IN Days)) && (TRUE())),'cfg_schema_drift_definition'[definition_loaded_at])),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-drift-calendar-linked-job-visible"></a>
## Discovery drift calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('cfg_schema_drift_event'),((NOT ISBLANK('cfg_schema_drift_event'[first_detected_at]) && INT('cfg_schema_drift_event'[first_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[detected_at]) && INT('cfg_schema_drift_event'[detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[last_detected_at]) && INT('cfg_schema_drift_event'[last_detected_at]) IN Days) || (NOT ISBLANK('cfg_schema_drift_event'[resolved_at]) && INT('cfg_schema_drift_event'[resolved_at]) IN Days)) && (TRUE()) && 'cfg_schema_drift_event'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-history-selected"></a>
## Discovery history selected

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF(ISFILTERED('Load Calendar'[Date]) || ISFILTERED('Discovery Job Runs'[job_run_id]), 1, 0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-job-picker-visible"></a>
## Discovery job picker visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))) > 0, 1, 0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-lineage-calendar-changes"></a>
## Discovery lineage calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-069.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('rpt_job_layer_lineage'), ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days)) && ((UPPER(COALESCE(rpt_job_layer_lineage[lineage_status],""))
			    IN {"FAIL","FAILED","FAILURE","ERROR","MISSING","UNMATCHED","BROKEN","NOT_FOUND","STALE"}) || COALESCE(rpt_job_layer_lineage[duplicate_key_count],0)>0) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('rpt_job_step_summary'), (NOT ISBLANK(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) && INT(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) IN Days) && ((UPPER(COALESCE(rpt_job_step_summary[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || COALESCE(rpt_job_step_summary[tables_failed],0)>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[error_message],"")))>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[pipeline_error_message],"")))>0) || COALESCE(rpt_job_step_summary[dq_checks_failed],0)>0
			                        || COALESCE(rpt_job_step_summary[drift_event_count],0)>0
			                        || COALESCE(rpt_job_step_summary[active_drift_count],0)>0
			                        || COALESCE(rpt_job_step_summary[duplicate_rows],0)>0
			                        || COALESCE(rpt_job_step_summary[null_primary_keys],0)>0) && (NOT JobChosen || 'rpt_job_step_summary'[job_run_id] IN Jobs))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-lineage-calendar-critical"></a>
## Discovery lineage calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-070.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('rpt_job_layer_lineage'), ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days)) && (UPPER(COALESCE(rpt_job_layer_lineage[lineage_status],""))
			    IN {"FAIL","FAILED","FAILURE","ERROR","MISSING","UNMATCHED","BROKEN","NOT_FOUND","STALE"}) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('rpt_job_step_summary'), (NOT ISBLANK(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) && INT(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) IN Days) && (UPPER(COALESCE(rpt_job_step_summary[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || COALESCE(rpt_job_step_summary[tables_failed],0)>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[error_message],"")))>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[pipeline_error_message],"")))>0) && (NOT JobChosen || 'rpt_job_step_summary'[job_run_id] IN Jobs))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-lineage-calendar-discoveries"></a>
## Discovery lineage calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-071.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('rpt_job_layer_lineage'), ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)),'rpt_job_layer_lineage'[job_run_id])),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-lineage-calendar-linked-job-visible"></a>
## Discovery lineage calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('rpt_job_layer_lineage'),((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days)) && ((UPPER(COALESCE(rpt_job_layer_lineage[lineage_status],""))
			    IN {"FAIL","FAILED","FAILURE","ERROR","MISSING","UNMATCHED","BROKEN","NOT_FOUND","STALE"}) || COALESCE(rpt_job_layer_lineage[duplicate_key_count],0)>0) && 'rpt_job_layer_lineage'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('rpt_job_step_summary'),(NOT ISBLANK(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) && INT(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) IN Days) && ((UPPER(COALESCE(rpt_job_step_summary[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || COALESCE(rpt_job_step_summary[tables_failed],0)>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[error_message],"")))>0
			    || LEN(TRIM(COALESCE(rpt_job_step_summary[pipeline_error_message],"")))>0) || COALESCE(rpt_job_step_summary[dq_checks_failed],0)>0
			                        || COALESCE(rpt_job_step_summary[drift_event_count],0)>0
			                        || COALESCE(rpt_job_step_summary[active_drift_count],0)>0
			                        || COALESCE(rpt_job_step_summary[duplicate_rows],0)>0
			                        || COALESCE(rpt_job_step_summary[null_primary_keys],0)>0) && 'rpt_job_step_summary'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('rpt_job_layer_lineage'),((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days)) && (TRUE()) && 'rpt_job_layer_lineage'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-loads-calendar-changes"></a>
## Discovery loads calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-072.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('cfg_table_load_metric'), ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days)) && (COALESCE(cfg_table_load_metric[duplicate_key_count],0)>0 || COALESCE(cfg_table_load_metric[null_primary_key_count],0)>0) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_silver_export_load'), (NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days) && ((UPPER(COALESCE(cfg_silver_export_load[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || LEN(TRIM(COALESCE(cfg_silver_export_load[error_message],"")))>0) || COALESCE(cfg_silver_export_load[duplicate_key_count],0)>0) && (NOT JobChosen || 'cfg_silver_export_load'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_silver_load_control'), (NOT ISBLANK(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) && INT(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) IN Days) && ((UPPER(COALESCE(cfg_silver_load_control[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || LEN(TRIM(COALESCE(cfg_silver_load_control[error_message],"")))>0) || COALESCE(cfg_silver_load_control[missing_column_count],0)>0 || COALESCE(cfg_silver_load_control[extra_column_count],0)>0))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.cfg_silver_load_control`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-loads-calendar-critical"></a>
## Discovery loads calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-073.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('cfg_table_load_metric'), ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days)) && (COALESCE(cfg_table_load_metric[null_primary_key_count],0)>0) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_silver_export_load'), (NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days) && (UPPER(COALESCE(cfg_silver_export_load[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || LEN(TRIM(COALESCE(cfg_silver_export_load[error_message],"")))>0) && (NOT JobChosen || 'cfg_silver_export_load'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_silver_load_control'), (NOT ISBLANK(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) && INT(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) IN Days) && (UPPER(COALESCE(cfg_silver_load_control[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || LEN(TRIM(COALESCE(cfg_silver_load_control[error_message],"")))>0))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.cfg_silver_load_control`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-loads-calendar-discoveries"></a>
## Discovery loads calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-074.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_table_load_metric'), ((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_table_load_metric'[job_run_id] IN Jobs)),'cfg_table_load_metric'[run_id])) + COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_silver_export_load'), (NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days) && (TRUE()) && (NOT JobChosen || 'cfg_silver_export_load'[job_run_id] IN Jobs)),'cfg_silver_export_load'[run_id])) + COUNTROWS(SUMMARIZE(FILTER(ALL('cfg_silver_load_control'), (NOT ISBLANK(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) && INT(COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])) IN Days) && (TRUE())),'cfg_silver_load_control'[run_id])),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.cfg_silver_load_control`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-loads-calendar-linked-job-visible"></a>
## Discovery loads calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('cfg_table_load_metric'),((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days)) && (COALESCE(cfg_table_load_metric[duplicate_key_count],0)>0 || COALESCE(cfg_table_load_metric[null_primary_key_count],0)>0) && 'cfg_table_load_metric'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_silver_export_load'),(NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days) && ((UPPER(COALESCE(cfg_silver_export_load[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
			    || LEN(TRIM(COALESCE(cfg_silver_export_load[error_message],"")))>0) || COALESCE(cfg_silver_export_load[duplicate_key_count],0)>0) && 'cfg_silver_export_load'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_table_load_metric'),((NOT ISBLANK('cfg_table_load_metric'[recorded_at]) && INT('cfg_table_load_metric'[recorded_at]) IN Days)) && (TRUE()) && 'cfg_table_load_metric'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_silver_export_load'),(NOT ISBLANK(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) && INT(COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))) IN Days) && (TRUE()) && 'cfg_silver_export_load'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_silver_export_load`; `monitoring.cfg_table_load_metric`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-quality-calendar-changes"></a>
## Discovery quality calendar changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-075.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('rpt_job_data_quality'), ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days)) && (COALESCE(rpt_job_data_quality[failed_row_count],0)>0
			    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
			    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
			    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_rejected_row'), ((NOT ISBLANK('cfg_rejected_row'[rejected_at]) && INT('cfg_rejected_row'[rejected_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_rejected_row'[job_run_id] IN Jobs))) + COUNTROWS(FILTER(ALL('cfg_referential_exception'), ((NOT ISBLANK('cfg_referential_exception'[detected_at]) && INT('cfg_referential_exception'[detected_at]) IN Days)) && (TRUE()) && (NOT JobChosen || 'cfg_referential_exception'[job_run_id] IN Jobs))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-quality-calendar-critical"></a>
## Discovery quality calendar critical

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-076.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(COUNTROWS(FILTER(ALL('rpt_job_data_quality'), ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days)) && ((COALESCE(rpt_job_data_quality[failed_row_count],0)>0
			    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
			    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
			    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}) && UPPER(COALESCE(rpt_job_data_quality[severity],"")) IN {"CRITICAL","ERROR","FATAL"}) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-quality-calendar-discoveries"></a>
## Discovery quality calendar discoveries

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-077.

Numeric/date operational definition in the latest saved model

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN COALESCE(0,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-quality-calendar-linked-job-visible"></a>
## Discovery quality calendar linked job visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(COUNTROWS(FILTER(ALL('rpt_job_data_quality'),((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days)) && (COALESCE(rpt_job_data_quality[failed_row_count],0)>0
			    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
			    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
			    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}) && 'rpt_job_data_quality'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_rejected_row'),((NOT ISBLANK('cfg_rejected_row'[rejected_at]) && INT('cfg_rejected_row'[rejected_at]) IN Days)) && (TRUE()) && 'cfg_rejected_row'[job_run_id] IN Jobs)) + COUNTROWS(FILTER(ALL('cfg_referential_exception'),((NOT ISBLANK('cfg_referential_exception'[detected_at]) && INT('cfg_referential_exception'[detected_at]) IN Days)) && (TRUE()) && 'cfg_referential_exception'[job_run_id] IN Jobs))>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-context"></a>
## Discovery rpt_job_data_quality Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Day=SELECTEDVALUE('Load Calendar'[Date])
			VAR Time=[Discovery rpt_job_data_quality Latest time]
			RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-discovery-batches"></a>
## Discovery rpt_job_data_quality Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-078.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[run_id]),KEEPFILTERS(FILTER('rpt_job_data_quality',(NOT DateChosen || ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days))) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_data_quality Latest key]),CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[run_id]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time] },'rpt_job_data_quality'[checked_at]))),CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[run_id]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-distinct-objects"></a>
## Discovery rpt_job_data_quality Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-079.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[source_table]),KEEPFILTERS(FILTER('rpt_job_data_quality',(NOT DateChosen || ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days))) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_data_quality Latest key]),CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[source_table]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time] },'rpt_job_data_quality'[checked_at]))),CALCULATE(DISTINCTCOUNT('rpt_job_data_quality'[source_table]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-latest-key"></a>
## Discovery rpt_job_data_quality Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_data_quality, rpt_job_data_quality[run_id],
			    "DiscoveryTime", MAX(rpt_job_data_quality[checked_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_data_quality[run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_data_quality[run_id])
```

Source tables: `monitoring.rpt_job_data_quality`

<a id="mission-discovery-rpt-job-data-quality-latest-time"></a>
## Discovery rpt_job_data_quality Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(rpt_job_data_quality[checked_at]), REMOVEFILTERS())
```

Source tables: `monitoring.rpt_job_data_quality`

<a id="mission-discovery-rpt-job-data-quality-rows"></a>
## Discovery rpt_job_data_quality Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-080.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('rpt_job_data_quality'),KEEPFILTERS(FILTER('rpt_job_data_quality',(NOT DateChosen || ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days))) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_data_quality Latest key]),CALCULATE(COUNTROWS('rpt_job_data_quality'),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time] },'rpt_job_data_quality'[checked_at]))),CALCULATE(COUNTROWS('rpt_job_data_quality'),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-scope-count"></a>
## Discovery rpt_job_data_quality Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-081.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_data_quality','rpt_job_data_quality'[rule_id])),KEEPFILTERS(FILTER('rpt_job_data_quality',(NOT DateChosen || ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days))) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_data_quality Latest key]),CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_data_quality','rpt_job_data_quality'[rule_id])),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time] },'rpt_job_data_quality'[checked_at]))),CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_data_quality','rpt_job_data_quality'[rule_id])),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-selected-time"></a>
## Discovery rpt_job_data_quality Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('rpt_job_data_quality'[checked_at]),KEEPFILTERS(FILTER('rpt_job_data_quality',(NOT DateChosen || ((NOT ISBLANK('rpt_job_data_quality'[checked_at]) && INT('rpt_job_data_quality'[checked_at]) IN Days))) && (NOT JobChosen || 'rpt_job_data_quality'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_data_quality Latest key]),CALCULATE(MAX('rpt_job_data_quality'[checked_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time] },'rpt_job_data_quality'[checked_at]))),CALCULATE(MAX('rpt_job_data_quality'[checked_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-state"></a>
## Discovery rpt_job_data_quality State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery rpt_job_data_quality Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-data-quality-visible"></a>
## Discovery rpt_job_data_quality Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery rpt_job_data_quality Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-context"></a>
## Discovery rpt_job_layer_lineage Context

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Day=SELECTEDVALUE('Load Calendar'[Date])
			VAR Time=[Discovery rpt_job_layer_lineage Latest time]
			RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-discovery-batches"></a>
## Discovery rpt_job_layer_lineage Discovery batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-082.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[job_run_id]),KEEPFILTERS(FILTER('rpt_job_layer_lineage',(NOT DateChosen || ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days))) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]),CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[job_run_id]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time] },'rpt_job_layer_lineage'[observed_at]))),CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[job_run_id]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-distinct-objects"></a>
## Discovery rpt_job_layer_lineage Distinct objects

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-083.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[source_object]),KEEPFILTERS(FILTER('rpt_job_layer_lineage',(NOT DateChosen || ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days))) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]),CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[source_object]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time] },'rpt_job_layer_lineage'[observed_at]))),CALCULATE(DISTINCTCOUNT('rpt_job_layer_lineage'[source_object]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-latest-key"></a>
## Discovery rpt_job_layer_lineage Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_layer_lineage, rpt_job_layer_lineage[job_run_id],
			    "DiscoveryTime", MAX(rpt_job_layer_lineage[observed_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_layer_lineage[job_run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_layer_lineage[job_run_id])
```

Source tables: `monitoring.rpt_job_layer_lineage`

<a id="mission-discovery-rpt-job-layer-lineage-latest-time"></a>
## Discovery rpt_job_layer_lineage Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(rpt_job_layer_lineage[observed_at]), REMOVEFILTERS())
```

Source tables: `monitoring.rpt_job_layer_lineage`

<a id="mission-discovery-rpt-job-layer-lineage-rows"></a>
## Discovery rpt_job_layer_lineage Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-084.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('rpt_job_layer_lineage'),KEEPFILTERS(FILTER('rpt_job_layer_lineage',(NOT DateChosen || ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days))) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]),CALCULATE(COUNTROWS('rpt_job_layer_lineage'),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time] },'rpt_job_layer_lineage'[observed_at]))),CALCULATE(COUNTROWS('rpt_job_layer_lineage'),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-scope-count"></a>
## Discovery rpt_job_layer_lineage Scope count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-085.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_layer_lineage','rpt_job_layer_lineage'[target_layer],'rpt_job_layer_lineage'[target_object])),KEEPFILTERS(FILTER('rpt_job_layer_lineage',(NOT DateChosen || ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days))) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]),CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_layer_lineage','rpt_job_layer_lineage'[target_layer],'rpt_job_layer_lineage'[target_object])),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time] },'rpt_job_layer_lineage'[observed_at]))),CALCULATE(COUNTROWS(SUMMARIZE('rpt_job_layer_lineage','rpt_job_layer_lineage'[target_layer],'rpt_job_layer_lineage'[target_object])),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-selected-time"></a>
## Discovery rpt_job_layer_lineage Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('rpt_job_layer_lineage'[observed_at]),KEEPFILTERS(FILTER('rpt_job_layer_lineage',(NOT DateChosen || ((NOT ISBLANK('rpt_job_layer_lineage'[observed_at]) && INT('rpt_job_layer_lineage'[observed_at]) IN Days))) && (NOT JobChosen || 'rpt_job_layer_lineage'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]),CALCULATE(MAX('rpt_job_layer_lineage'[observed_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time] },'rpt_job_layer_lineage'[observed_at]))),CALCULATE(MAX('rpt_job_layer_lineage'[observed_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-state"></a>
## Discovery rpt_job_layer_lineage State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery rpt_job_layer_lineage Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-layer-lineage-visible"></a>
## Discovery rpt_job_layer_lineage Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery rpt_job_layer_lineage Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_layer_lineage`; `monitoring.rpt_job_run_summary`

<a id="mission-discovery-rpt-job-schema-drift-latest-key"></a>
## Discovery rpt_job_schema_drift Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_schema_drift, rpt_job_schema_drift[run_id],
			    "DiscoveryTime", MAX(rpt_job_schema_drift[last_detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_schema_drift[run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_schema_drift[run_id])
```

Source tables: `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-schema-drift-latest-time"></a>
## Discovery rpt_job_schema_drift Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(rpt_job_schema_drift[last_detected_at]), REMOVEFILTERS())
```

Source tables: `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-schema-drift-rows"></a>
## Discovery rpt_job_schema_drift Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-086.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('rpt_job_schema_drift'),KEEPFILTERS(FILTER('rpt_job_schema_drift',(NOT DateChosen || ((NOT ISBLANK('rpt_job_schema_drift'[first_detected_at]) && INT('rpt_job_schema_drift'[first_detected_at]) IN Days) || (NOT ISBLANK('rpt_job_schema_drift'[last_detected_at]) && INT('rpt_job_schema_drift'[last_detected_at]) IN Days) || (NOT ISBLANK('rpt_job_schema_drift'[resolved_at]) && INT('rpt_job_schema_drift'[resolved_at]) IN Days))) && (NOT JobChosen || 'rpt_job_schema_drift'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_schema_drift Latest key]),CALCULATE(COUNTROWS('rpt_job_schema_drift'),KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest time] },'rpt_job_schema_drift'[last_detected_at]))),CALCULATE(COUNTROWS('rpt_job_schema_drift'),KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest key]}, rpt_job_schema_drift[run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-schema-drift-selected-time"></a>
## Discovery rpt_job_schema_drift Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('rpt_job_schema_drift'[last_detected_at]),KEEPFILTERS(FILTER('rpt_job_schema_drift',(NOT DateChosen || ((NOT ISBLANK('rpt_job_schema_drift'[first_detected_at]) && INT('rpt_job_schema_drift'[first_detected_at]) IN Days) || (NOT ISBLANK('rpt_job_schema_drift'[last_detected_at]) && INT('rpt_job_schema_drift'[last_detected_at]) IN Days) || (NOT ISBLANK('rpt_job_schema_drift'[resolved_at]) && INT('rpt_job_schema_drift'[resolved_at]) IN Days))) && (NOT JobChosen || 'rpt_job_schema_drift'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_schema_drift Latest key]),CALCULATE(MAX('rpt_job_schema_drift'[last_detected_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest time] },'rpt_job_schema_drift'[last_detected_at]))),CALCULATE(MAX('rpt_job_schema_drift'[last_detected_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest key]}, rpt_job_schema_drift[run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-schema-drift-state"></a>
## Discovery rpt_job_schema_drift State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery rpt_job_schema_drift Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-schema-drift-visible"></a>
## Discovery rpt_job_schema_drift Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery rpt_job_schema_drift Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_schema_drift`

<a id="mission-discovery-rpt-job-step-summary-latest-key"></a>
## Discovery rpt_job_step_summary Latest key

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_step_summary, rpt_job_step_summary[job_run_id],
			    "DiscoveryTime", MAX(rpt_job_step_summary[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_step_summary[job_run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_step_summary[job_run_id])
```

Source tables: `monitoring.rpt_job_step_summary`

<a id="mission-discovery-rpt-job-step-summary-latest-time"></a>
## Discovery rpt_job_step_summary Latest time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
CALCULATE(MAX(rpt_job_step_summary[started_at]), REMOVEFILTERS())
```

Source tables: `monitoring.rpt_job_step_summary`

<a id="mission-discovery-rpt-job-step-summary-rows"></a>
## Discovery rpt_job_step_summary Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-087.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(COUNTROWS('rpt_job_step_summary'),KEEPFILTERS(FILTER('rpt_job_step_summary',(NOT DateChosen || (NOT ISBLANK(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) && INT(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) IN Days)) && (NOT JobChosen || 'rpt_job_step_summary'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_step_summary Latest key]),CALCULATE(COUNTROWS('rpt_job_step_summary'),KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest time] },'rpt_job_step_summary'[started_at]))),CALCULATE(COUNTROWS('rpt_job_step_summary'),KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest key]}, rpt_job_step_summary[job_run_id])))))),0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-rpt-job-step-summary-selected-time"></a>
## Discovery rpt_job_step_summary Selected time

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			RETURN IF(DateChosen || JobChosen,CALCULATE(MAX('rpt_job_step_summary'[started_at]),KEEPFILTERS(FILTER('rpt_job_step_summary',(NOT DateChosen || (NOT ISBLANK(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) && INT(COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])) IN Days)) && (NOT JobChosen || 'rpt_job_step_summary'[job_run_id] IN Jobs)))),IF(ISBLANK([Discovery rpt_job_step_summary Latest key]),CALCULATE(MAX('rpt_job_step_summary'[started_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest time] },'rpt_job_step_summary'[started_at]))),CALCULATE(MAX('rpt_job_step_summary'[started_at]),KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest key]}, rpt_job_step_summary[job_run_id])))))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-rpt-job-step-summary-state"></a>
## Discovery rpt_job_step_summary State

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Discovery rpt_job_step_summary Rows]
			RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-discovery-rpt-job-step-summary-visible"></a>
## Discovery rpt_job_step_summary Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
IF([Discovery rpt_job_step_summary Rows]>0,1,0)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_summary`

<a id="mission-domain-value-changes"></a>
## Domain value changes

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
"Added " & FORMAT(COALESCE([Domain values Added],0),"#,0") & " · Removed " & FORMAT(COALESCE([Domain values Removed],0),"#,0")
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-domain-values-added"></a>
## Domain values Added

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-088.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="ADDED")),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="ADDED")),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="ADDED")),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-domain-values-removed"></a>
## Domain values Removed

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-089.

Numeric/date operational definition in the latest saved model

```dax
COALESCE((VAR DateChosen=ISFILTERED('Load Calendar'[Date])
			VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
			VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
			VAR Days=VALUES('Load Calendar'[Date])
			VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
			VAR LatestKey=[Discovery cfg_data_domain Latest key]
			VAR LatestTime=[Discovery cfg_data_domain Latest time]
			RETURN IF(DateChosen || JobChosen || AllVersions,
			    CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="REMOVED")),KEEPFILTERS(FILTER(cfg_data_domain,
			        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
			        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
			    IF(ISBLANK(LatestKey),
			        CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="REMOVED")),KEEPFILTERS(TREATAS({LatestTime},cfg_data_domain[profiled_at]))),
			        CALCULATE(COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="REMOVED")),KEEPFILTERS(TREATAS({LatestKey},cfg_data_domain[run_id])))))),0)
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-failed-archive-table-exports"></a>
## Failed Archive Table Exports

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-097.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archive_table_export_load', UPPER ( COALESCE ( 'cfg_archive_table_export_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_archive_table_export_load`

<a id="mission-failed-archive-zip-batches"></a>
## Failed Archive ZIP Batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-098.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-failed-gold-snapshots"></a>
## Failed Gold Snapshots

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-099.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-failed-job-runs"></a>
## Failed Job Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-100.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-failed-job-steps"></a>
## Failed Job Steps

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-101.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-failed-pipeline-runs"></a>
## Failed Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-102.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-failures"></a>
## Failures

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-103.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome]="Failed"))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-gold-snapshot-dq-failures"></a>
## Gold Snapshot DQ Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-104.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[dq_result], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-gold-snapshot-runs"></a>
## Gold Snapshot Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-105.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'cfg_month_end_gold_run' )
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-gold-snapshots-awaiting-replay"></a>
## Gold Snapshots Awaiting Replay

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-106.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Gold Snapshot Runs], 'cfg_month_end_gold_run'[reload] = TRUE () )
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-high-or-critical-rules-failing"></a>
## High or Critical Rules Failing

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-107.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) IN { "CRITICAL", "HIGH" } && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-in-progress-or-other"></a>
## In progress or other

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-108.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome] IN {"Running","Other"}))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-runs"></a>
## Job Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-115.

Numeric/date operational definition in the latest saved model

```dax
DISTINCTCOUNT ( 'rpt_job_run_summary'[job_run_id] )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-steps"></a>
## Job Steps

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-116.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( 'rpt_job_step_timing' )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-job-steps-with-error"></a>
## Job Steps With Error

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-117.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'rpt_job_step_timing', NOT ISBLANK ( 'rpt_job_step_timing'[error_message] ) && 'rpt_job_step_timing'[error_message] <> "" ) )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-job-success-rate"></a>
## Job Success Rate

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-118.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [Successful Job Runs], [Successful Job Runs] + [Failed Job Runs] )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-actual-min"></a>
## Job actual min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-109.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE(SELECTEDVALUE('rpt_job_run_summary'[job_duration_seconds]),60)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-baseline-n"></a>
## Job baseline n

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-110.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_run_summary'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_run_summary'[pipeline_name])
			VAR currentJob=SELECTEDVALUE('rpt_job_run_summary'[job_run_id])
			VAR history=FILTER(CALCULATETABLE('rpt_job_run_summary',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_run_summary')),
			    'rpt_job_run_summary'[pipeline_name]=pipeline && 'rpt_job_run_summary'[job_run_id]<>currentJob
			    && 'rpt_job_run_summary'[started_at]>=anchor-30 && 'rpt_job_run_summary'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_run_summary'[ended_at]) && 'rpt_job_run_summary'[ended_at]>='rpt_job_run_summary'[started_at]
			    && NOT ISBLANK('rpt_job_run_summary'[job_duration_seconds]) && 'rpt_job_run_summary'[job_duration_seconds]>=0
			    && 'rpt_job_run_summary'[Outcome]="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob),COUNTROWS(history))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-comparison"></a>
## Job comparison

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Job baseline n]
			VAR actual=[Job actual min]
			RETURN SWITCH(TRUE(),ISBLANK(n),"Select one job",n<5,"Insufficient history",ISBLANK(actual),"No duration recorded",actual<[Job prior p25 min],"Below prior P25",actual>[Job prior p75 min],"Above prior P75","Within prior IQR")
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-prior-mean-min"></a>
## Job prior mean min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-111.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_run_summary'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_run_summary'[pipeline_name])
			VAR currentJob=SELECTEDVALUE('rpt_job_run_summary'[job_run_id])
			VAR history=FILTER(CALCULATETABLE('rpt_job_run_summary',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_run_summary')),
			    'rpt_job_run_summary'[pipeline_name]=pipeline && 'rpt_job_run_summary'[job_run_id]<>currentJob
			    && 'rpt_job_run_summary'[started_at]>=anchor-30 && 'rpt_job_run_summary'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_run_summary'[ended_at]) && 'rpt_job_run_summary'[ended_at]>='rpt_job_run_summary'[started_at]
			    && NOT ISBLANK('rpt_job_run_summary'[job_duration_seconds]) && 'rpt_job_run_summary'[job_duration_seconds]>=0
			    && 'rpt_job_run_summary'[Outcome]="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && COUNTROWS(history)>=5,AVERAGEX(history,DIVIDE('rpt_job_run_summary'[job_duration_seconds],60)))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-prior-median-min"></a>
## Job prior median min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-112.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_run_summary'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_run_summary'[pipeline_name])
			VAR currentJob=SELECTEDVALUE('rpt_job_run_summary'[job_run_id])
			VAR history=FILTER(CALCULATETABLE('rpt_job_run_summary',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_run_summary')),
			    'rpt_job_run_summary'[pipeline_name]=pipeline && 'rpt_job_run_summary'[job_run_id]<>currentJob
			    && 'rpt_job_run_summary'[started_at]>=anchor-30 && 'rpt_job_run_summary'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_run_summary'[ended_at]) && 'rpt_job_run_summary'[ended_at]>='rpt_job_run_summary'[started_at]
			    && NOT ISBLANK('rpt_job_run_summary'[job_duration_seconds]) && 'rpt_job_run_summary'[job_duration_seconds]>=0
			    && 'rpt_job_run_summary'[Outcome]="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && COUNTROWS(history)>=5,MEDIANX(history,DIVIDE('rpt_job_run_summary'[job_duration_seconds],60)))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-prior-p25-min"></a>
## Job prior p25 min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-113.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_run_summary'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_run_summary'[pipeline_name])
			VAR currentJob=SELECTEDVALUE('rpt_job_run_summary'[job_run_id])
			VAR history=FILTER(CALCULATETABLE('rpt_job_run_summary',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_run_summary')),
			    'rpt_job_run_summary'[pipeline_name]=pipeline && 'rpt_job_run_summary'[job_run_id]<>currentJob
			    && 'rpt_job_run_summary'[started_at]>=anchor-30 && 'rpt_job_run_summary'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_run_summary'[ended_at]) && 'rpt_job_run_summary'[ended_at]>='rpt_job_run_summary'[started_at]
			    && NOT ISBLANK('rpt_job_run_summary'[job_duration_seconds]) && 'rpt_job_run_summary'[job_duration_seconds]>=0
			    && 'rpt_job_run_summary'[Outcome]="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && COUNTROWS(history)>=5,PERCENTILEX.INC(history,DIVIDE('rpt_job_run_summary'[job_duration_seconds],60),0.25))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-job-prior-p75-min"></a>
## Job prior p75 min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-114.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_run_summary'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_run_summary'[pipeline_name])
			VAR currentJob=SELECTEDVALUE('rpt_job_run_summary'[job_run_id])
			VAR history=FILTER(CALCULATETABLE('rpt_job_run_summary',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_run_summary')),
			    'rpt_job_run_summary'[pipeline_name]=pipeline && 'rpt_job_run_summary'[job_run_id]<>currentJob
			    && 'rpt_job_run_summary'[started_at]>=anchor-30 && 'rpt_job_run_summary'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_run_summary'[ended_at]) && 'rpt_job_run_summary'[ended_at]>='rpt_job_run_summary'[started_at]
			    && NOT ISBLANK('rpt_job_run_summary'[job_duration_seconds]) && 'rpt_job_run_summary'[job_duration_seconds]>=0
			    && 'rpt_job_run_summary'[Outcome]="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && COUNTROWS(history)>=5,PERCENTILEX.INC(history,DIVIDE('rpt_job_run_summary'[job_duration_seconds],60),0.75))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-archived-schema-capture"></a>
## Latest Archived Schema Capture

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-119.

Numeric/date operational definition in the latest saved model

```dax
MAX ( 'cfg_archived_schema_live'[contract_loaded_at] )
```

Source tables: `monitoring.cfg_archived_schema_live`

<a id="mission-latest-job-run-id"></a>
## Latest Job Run ID

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR latest_job =
				TOPN (
					1,
					FILTER ( ALLSELECTED ( 'rpt_job_run_summary' ), NOT ISBLANK ( 'rpt_job_run_summary'[started_at] ) ),
					'rpt_job_run_summary'[started_at], DESC,
					'rpt_job_run_summary'[job_run_id], DESC
				)
			RETURN
				MAXX ( latest_job, 'rpt_job_run_summary'[job_run_id] )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-job-run-started"></a>
## Latest Job Run Started

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-120.

Numeric/date operational definition in the latest saved model

```dax
MAXX ( FILTER ( ALLSELECTED ( 'rpt_job_run_summary' ), NOT ISBLANK ( 'rpt_job_run_summary'[started_at] ) ), 'rpt_job_run_summary'[started_at] )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-critical-rules"></a>
## Latest Load Critical Rules

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-121.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([Critical Rules Failing], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-evaluated-checks"></a>
## Latest Load Evaluated Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-122.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Evaluated Checks], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-failed-checks"></a>
## Latest Load Failed Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-123.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Failed Checks], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-failed-rows"></a>
## Latest Load Failed Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-124.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Failed Rows], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-quality-records"></a>
## Latest Load Quality Records

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-125.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id), COALESCE(CALCULATE(COUNTROWS(cfg_data_quality_result), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = _id), 0))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-quality-report"></a>
## Latest Load Quality Report

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR _id = [Latest Load Run ID]
			VAR lastCheck = CALCULATE(MAX(cfg_data_quality_result[checked_at]), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = _id)
			RETURN IF(ISBLANK(_id), "No load recorded in this model",
			    "Load started " & FORMAT([Latest Load Started], "dd MMM yyyy HH:mm") & " | " &
			    IF([Latest Load Quality Records] = 0, "No quality report for this load yet",
			       "Quality checked " & FORMAT(lastCheck, "dd MMM yyyy HH:mm")))
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-run-id"></a>
## Latest Load Run ID

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR latest = TOPN(1,
			    FILTER(CALCULATETABLE(rpt_job_run_summary, REMOVEFILTERS()), NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC)
			RETURN CALCULATE(MAXX(latest, rpt_job_run_summary[job_run_id]), REMOVEFILTERS())
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-started"></a>
## Latest Load Started

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-126.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id), CALCULATE(MAX(rpt_job_run_summary[started_at]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = _id))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-load-status"></a>
## Latest Load Status

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF(ISBLANK(_id), "No loads", CALCULATE(SELECTEDVALUE(rpt_job_run_summary[status]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = _id))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-pipeline-end"></a>
## Latest Pipeline End

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-131.

Numeric/date operational definition in the latest saved model

```dax
MAX ( 'cfg_pipeline_run'[ended_at] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-latest-pipeline-row-visible"></a>
## Latest Pipeline Row Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(cfg_pipeline_run),
			    CALCULATE(COUNTROWS(cfg_pipeline_run), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-pipeline-status"></a>
## Latest Pipeline Status

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR latest_end = [Latest Pipeline End]
			RETURN
			    CALCULATE ( CONCATENATEX ( VALUES ( 'cfg_pipeline_run'[status] ), 'cfg_pipeline_run'[status], ", " ), 'cfg_pipeline_run'[ended_at] = latest_end )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-latest-matching-archive-zip-batches"></a>
## Latest matching Archive ZIP Batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-127.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Archive ZIP Batches], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-latest-matching-archive-zip-batches-awaiting-reload"></a>
## Latest matching Archive ZIP Batches Awaiting Reload

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-128.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Archive ZIP Batches Awaiting Reload], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-latest-matching-failed-archive-zip-batches"></a>
## Latest matching Failed Archive ZIP Batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-129.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Failed Archive ZIP Batches], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-latest-matching-failed-gold-snapshots"></a>
## Latest matching Failed Gold Snapshots

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-130.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Failed Gold Snapshots], KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id])))
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-latest-or-selected-failures"></a>
## Latest or selected Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Failures],
			    CALCULATE([Failures], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-or-selected-p95-duration-min"></a>
## Latest or selected P95 duration min

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [P95 duration min],
			    CALCULATE([P95 duration min], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-or-selected-rows-written"></a>
## Latest or selected Rows written

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Rows written],
			    CALCULATE([Rows written], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-or-selected-runs"></a>
## Latest or selected Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Runs],
			    CALCULATE([Runs], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-latest-or-selected-success-rate"></a>
## Latest or selected Success rate

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Success rate],
			    CALCULATE([Success rate], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-live-pipeline-failures"></a>
## Live Pipeline Failures

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-132.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-live-pipeline-runs"></a>
## Live Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-133.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-load-rows-read-delta"></a>
## Load Rows Read Delta

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-134.

Numeric/date operational definition in the latest saved model

```dax
VAR CurrentCount=SELECTEDVALUE(cfg_table_load_metric[rows_read])
			VAR PreviousCount=[Load Rows Read Previous]
			RETURN IF(NOT ISBLANK(CurrentCount) && NOT ISBLANK(PreviousCount),CurrentCount-PreviousCount)
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-read-delta-percent"></a>
## Load Rows Read Delta %

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-135.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE([Load Rows Read Delta],[Load Rows Read Previous])
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-read-previous"></a>
## Load Rows Read Previous

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-136.

Numeric/date operational definition in the latest saved model

```dax
VAR ThisTime=SELECTEDVALUE(cfg_table_load_metric[recorded_at])
			VAR ThisRun=SELECTEDVALUE(cfg_table_load_metric[run_id])
			VAR ThisLayer=SELECTEDVALUE(cfg_table_load_metric[layer])
			VAR ThisKind=SELECTEDVALUE(cfg_table_load_metric[source_kind])
			VAR ThisSource=SELECTEDVALUE(cfg_table_load_metric[source_object])
			VAR ThisTarget=SELECTEDVALUE(cfg_table_load_metric[target_object])
			VAR History=FILTER(ALL(cfg_table_load_metric),
			    cfg_table_load_metric[layer]=ThisLayer && cfg_table_load_metric[source_kind]=ThisKind
			    && cfg_table_load_metric[source_object]=ThisSource && cfg_table_load_metric[target_object]=ThisTarget)

			VAR Prior=TOPN(1,FILTER(History,(cfg_table_load_metric[recorded_at]<ThisTime || (cfg_table_load_metric[recorded_at]=ThisTime && cfg_table_load_metric[run_id]<ThisRun))),
			    cfg_table_load_metric[recorded_at],DESC,cfg_table_load_metric[run_id],DESC)
			RETURN IF(NOT ISBLANK(ThisTime),MAXX(Prior,cfg_table_load_metric[rows_read]))
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-read-sparkline"></a>
## Load Rows Read Sparkline

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR ThisTime=SELECTEDVALUE(cfg_table_load_metric[recorded_at])
			VAR ThisRun=SELECTEDVALUE(cfg_table_load_metric[run_id])
			VAR ThisLayer=SELECTEDVALUE(cfg_table_load_metric[layer])
			VAR ThisKind=SELECTEDVALUE(cfg_table_load_metric[source_kind])
			VAR ThisSource=SELECTEDVALUE(cfg_table_load_metric[source_object])
			VAR ThisTarget=SELECTEDVALUE(cfg_table_load_metric[target_object])
			VAR History=FILTER(ALL(cfg_table_load_metric),
			    cfg_table_load_metric[layer]=ThisLayer && cfg_table_load_metric[source_kind]=ThisKind
			    && cfg_table_load_metric[source_object]=ThisSource && cfg_table_load_metric[target_object]=ThisTarget)

			VAR Points=SUMMARIZE(FILTER(History,NOT ISBLANK(cfg_table_load_metric[rows_read])
			    && (cfg_table_load_metric[recorded_at]<ThisTime || (cfg_table_load_metric[recorded_at]=ThisTime && cfg_table_load_metric[run_id]<=ThisRun))),
			    cfg_table_load_metric[recorded_at],cfg_table_load_metric[run_id],"LoadValue",MAX(cfg_table_load_metric[rows_read]))
			VAR TrendWindow=TOPN(12,Points,cfg_table_load_metric[recorded_at],DESC,cfg_table_load_metric[run_id],DESC)
			VAR N=COUNTROWS(TrendWindow)
			VAR Low=MINX(TrendWindow,[LoadValue])
			VAR High=MAXX(TrendWindow,[LoadValue])
			VAR Indexed=ADDCOLUMNS(TrendWindow,"PointIndex",
			    VAR T=cfg_table_load_metric[recorded_at] VAR R=cfg_table_load_metric[run_id]
			    RETURN COUNTROWS(FILTER(TrendWindow,cfg_table_load_metric[recorded_at]<T
			        || (cfg_table_load_metric[recorded_at]=T && cfg_table_load_metric[run_id]<R))))
			VAR XY=CONCATENATEX(Indexed,
			    FORMAT(4+112*DIVIDE([PointIndex],MAX(1,N-1)),"0.0","en-US") & "," &
			    FORMAT(IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)),"0.0","en-US"),
			    " ",[PointIndex],ASC)
			VAR LastPoint=TOPN(1,Indexed,[PointIndex],DESC)
			VAR EndX=IF(N=1,4,116)
			VAR EndY=MAXX(LastPoint,IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)))
			RETURN IF(N>0 && NOT ISBLANK(ThisTime),
			    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='28' viewBox='0 0 120 28'><polyline fill='none' stroke='%23CBF576' stroke-width='2' points='" & XY & "'/><circle fill='%23CBF576' r='2.5' cx='" & FORMAT(EndX,"0.0","en-US") & "' cy='" & FORMAT(EndY,"0.0","en-US") & "'/></svg>")
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-written-delta"></a>
## Load Rows Written Delta

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-137.

Numeric/date operational definition in the latest saved model

```dax
VAR CurrentCount=SELECTEDVALUE(cfg_table_load_metric[rows_written])
			VAR PreviousCount=[Load Rows Written Previous]
			RETURN IF(NOT ISBLANK(CurrentCount) && NOT ISBLANK(PreviousCount),CurrentCount-PreviousCount)
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-written-delta-percent"></a>
## Load Rows Written Delta %

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-138.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE([Load Rows Written Delta],[Load Rows Written Previous])
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-written-previous"></a>
## Load Rows Written Previous

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-139.

Numeric/date operational definition in the latest saved model

```dax
VAR ThisTime=SELECTEDVALUE(cfg_table_load_metric[recorded_at])
			VAR ThisRun=SELECTEDVALUE(cfg_table_load_metric[run_id])
			VAR ThisLayer=SELECTEDVALUE(cfg_table_load_metric[layer])
			VAR ThisKind=SELECTEDVALUE(cfg_table_load_metric[source_kind])
			VAR ThisSource=SELECTEDVALUE(cfg_table_load_metric[source_object])
			VAR ThisTarget=SELECTEDVALUE(cfg_table_load_metric[target_object])
			VAR History=FILTER(ALL(cfg_table_load_metric),
			    cfg_table_load_metric[layer]=ThisLayer && cfg_table_load_metric[source_kind]=ThisKind
			    && cfg_table_load_metric[source_object]=ThisSource && cfg_table_load_metric[target_object]=ThisTarget)

			VAR Prior=TOPN(1,FILTER(History,(cfg_table_load_metric[recorded_at]<ThisTime || (cfg_table_load_metric[recorded_at]=ThisTime && cfg_table_load_metric[run_id]<ThisRun))),
			    cfg_table_load_metric[recorded_at],DESC,cfg_table_load_metric[run_id],DESC)
			RETURN IF(NOT ISBLANK(ThisTime),MAXX(Prior,cfg_table_load_metric[rows_written]))
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-load-rows-written-sparkline"></a>
## Load Rows Written Sparkline

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR ThisTime=SELECTEDVALUE(cfg_table_load_metric[recorded_at])
			VAR ThisRun=SELECTEDVALUE(cfg_table_load_metric[run_id])
			VAR ThisLayer=SELECTEDVALUE(cfg_table_load_metric[layer])
			VAR ThisKind=SELECTEDVALUE(cfg_table_load_metric[source_kind])
			VAR ThisSource=SELECTEDVALUE(cfg_table_load_metric[source_object])
			VAR ThisTarget=SELECTEDVALUE(cfg_table_load_metric[target_object])
			VAR History=FILTER(ALL(cfg_table_load_metric),
			    cfg_table_load_metric[layer]=ThisLayer && cfg_table_load_metric[source_kind]=ThisKind
			    && cfg_table_load_metric[source_object]=ThisSource && cfg_table_load_metric[target_object]=ThisTarget)

			VAR Points=SUMMARIZE(FILTER(History,NOT ISBLANK(cfg_table_load_metric[rows_written])
			    && (cfg_table_load_metric[recorded_at]<ThisTime || (cfg_table_load_metric[recorded_at]=ThisTime && cfg_table_load_metric[run_id]<=ThisRun))),
			    cfg_table_load_metric[recorded_at],cfg_table_load_metric[run_id],"LoadValue",MAX(cfg_table_load_metric[rows_written]))
			VAR TrendWindow=TOPN(12,Points,cfg_table_load_metric[recorded_at],DESC,cfg_table_load_metric[run_id],DESC)
			VAR N=COUNTROWS(TrendWindow)
			VAR Low=MINX(TrendWindow,[LoadValue])
			VAR High=MAXX(TrendWindow,[LoadValue])
			VAR Indexed=ADDCOLUMNS(TrendWindow,"PointIndex",
			    VAR T=cfg_table_load_metric[recorded_at] VAR R=cfg_table_load_metric[run_id]
			    RETURN COUNTROWS(FILTER(TrendWindow,cfg_table_load_metric[recorded_at]<T
			        || (cfg_table_load_metric[recorded_at]=T && cfg_table_load_metric[run_id]<R))))
			VAR XY=CONCATENATEX(Indexed,
			    FORMAT(4+112*DIVIDE([PointIndex],MAX(1,N-1)),"0.0","en-US") & "," &
			    FORMAT(IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)),"0.0","en-US"),
			    " ",[PointIndex],ASC)
			VAR LastPoint=TOPN(1,Indexed,[PointIndex],DESC)
			VAR EndX=IF(N=1,4,116)
			VAR EndY=MAXX(LastPoint,IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)))
			RETURN IF(N>0 && NOT ISBLANK(ThisTime),
			    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='28' viewBox='0 0 120 28'><polyline fill='none' stroke='%23CBF576' stroke-width='2' points='" & XY & "'/><circle fill='%23CBF576' r='2.5' cx='" & FORMAT(EndX,"0.0","en-US") & "' cy='" & FORMAT(EndY,"0.0","en-US") & "'/></svg>")
```

Source tables: `monitoring.cfg_table_load_metric`

<a id="mission-longest-job-step-duration-min"></a>
## Longest Job Step Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-140.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( MAX ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-operational-exception-count"></a>
## Operational Exception Count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-141.

Numeric/date operational definition in the latest saved model

```dax
[Control Failures] + [DQ Failed Checks]
```

Source tables: `monitoring.cfg_archive_file_load`; `monitoring.cfg_archive_table_export_load`; `monitoring.cfg_archive_zip_load`; `monitoring.cfg_data_quality_result`; `monitoring.cfg_month_end_gold_run`; `monitoring.cfg_pipeline_run`

<a id="mission-p95-pipeline-duration-min"></a>
## P95 Pipeline Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-143.

Numeric/date operational definition in the latest saved model

```dax
PERCENTILEX.INC ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ), 0.95 )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-p95-duration-min"></a>
## P95 duration min

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-142.

Numeric/date operational definition in the latest saved model

```dax
PERCENTILEX.INC(FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[ended_at]) && rpt_job_run_summary[job_duration_seconds]>=0), DIVIDE(rpt_job_run_summary[job_duration_seconds],60),0.95)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-pipeline-rows-read"></a>
## Pipeline Rows Read

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-145.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_pipeline_run'[rows_read] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-rows-written"></a>
## Pipeline Rows Written

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-146.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_pipeline_run'[rows_written] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-rows-per-minute"></a>
## Pipeline Rows per Minute

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-144.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [Pipeline Rows Written], [Total Pipeline Duration (min)] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-runs"></a>
## Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-147.

Numeric/date operational definition in the latest saved model

```dax
DISTINCTCOUNT ( 'cfg_pipeline_run'[run_id] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-runs-with-error"></a>
## Pipeline Runs With Error

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-148.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[error_message] ) ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-success-rate"></a>
## Pipeline Success Rate

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-149.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [Successful Pipeline Runs], [Completed Pipeline Runs] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-tables-failed"></a>
## Pipeline Tables Failed

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-150.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_pipeline_run'[tables_failed] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-pipeline-tables-succeeded"></a>
## Pipeline Tables Succeeded

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-151.

Numeric/date operational definition in the latest saved model

```dax
SUM ( 'cfg_pipeline_run'[tables_succeeded] )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-ri-checked-rows"></a>
## RI Checked Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-153.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [DQ Checked Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-ri-failed-rows"></a>
## RI Failed Rows

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-154.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [DQ Failed Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-ri-failure-rate"></a>
## RI Failure Rate

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-155.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [RI Failed Rows], [RI Checked Rows] )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-ri-rules-failing"></a>
## RI Rules Failing

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-156.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Source tables: `monitoring.cfg_data_quality_result`

<a id="mission-reload-requests"></a>
## Reload Requests

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-152.

Numeric/date operational definition in the latest saved model

```dax
[Archive ZIP Batches Awaiting Reload] + [Archive Files Awaiting Reload] + [Archive Table Exports Awaiting Reload] + [Gold Snapshots Awaiting Replay]
```

Source tables: `monitoring.cfg_archive_file_load`; `monitoring.cfg_archive_table_export_load`; `monitoring.cfg_archive_zip_load`; `monitoring.cfg_month_end_gold_run`

<a id="mission-rows-written"></a>
## Rows written

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-157.

Numeric/date operational definition in the latest saved model

```dax
SUM(rpt_job_run_summary[rows_written])
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-running-pipeline-runs"></a>
## Running Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-158.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "RUNNING", "IN_PROGRESS", "STARTED" } ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-runs"></a>
## Runs

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-159.

Numeric/date operational definition in the latest saved model

```dax
DISTINCTCOUNT(rpt_job_run_summary[job_run_id])
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-selected-step-error-detail"></a>
## Selected Step Error Detail

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
CONCATENATEX (
				FILTER (
					VALUES ( 'rpt_job_step_timing'[error_message] ),
					NOT ISBLANK ( 'rpt_job_step_timing'[error_message] )
						&& 'rpt_job_step_timing'[error_message] <> ""
				),
				'rpt_job_step_timing'[error_message],
				UNICHAR ( 10 ) & UNICHAR ( 10 )
			)
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-selected-or-latest-failed-steps"></a>
## Selected or Latest Failed Steps

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					[Failed Job Steps],
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-selected-or-latest-job-duration-min"></a>
## Selected or Latest Job Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					DIVIDE ( MAX ( 'rpt_job_run_summary'[job_duration_seconds] ), 60.0 ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-selected-or-latest-job-error"></a>
## Selected or Latest Job Error

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					SELECTEDVALUE ( 'rpt_job_run_summary'[error_message] ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-selected-or-latest-job-run-id"></a>
## Selected or Latest Job Run ID

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
COALESCE ( SELECTEDVALUE ( 'rpt_job_run_summary'[job_run_id] ), [Latest Job Run ID] )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-selected-or-latest-job-status"></a>
## Selected or Latest Job Status

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					SELECTEDVALUE ( 'rpt_job_run_summary'[status] ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-selected-or-latest-job-steps"></a>
## Selected or Latest Job Steps

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					[Job Steps],
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-show-latest-load-quality"></a>
## Show Latest Load Quality

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-160.

Numeric/date operational definition in the latest saved model

```dax
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id) && CALCULATE(COUNTROWS(cfg_data_quality_result),
			    KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))) > 0, 1, 0)
```

Source tables: `monitoring.cfg_data_quality_result`; `monitoring.rpt_job_run_summary`

<a id="mission-show-step-for-selected-or-latest-job-run"></a>
## Show Step for Selected or Latest Job Run

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			VAR matching_steps =
				CALCULATE (
					COUNTROWS ( 'rpt_job_step_timing' ),
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
			RETURN
				IF ( NOT ISBLANK ( selected_job_run_id ) && matching_steps > 0, 1, 0 )
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-single-calendar-day"></a>
## Single calendar day

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-161.

Numeric/date operational definition in the latest saved model

```dax
IF(HASONEVALUE('Load Calendar'[Date]),1,0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-step-actual-min"></a>
## Step actual min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-162.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE(SELECTEDVALUE('rpt_job_step_timing'[step_duration_seconds]),60)
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-step-baseline-n"></a>
## Step baseline n

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-163.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_step_timing'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_step_timing'[Pipeline])
			VAR currentJob=SELECTEDVALUE('rpt_job_step_timing'[job_run_id])
			VAR notebook=SELECTEDVALUE('rpt_job_step_timing'[notebook_name])
			VAR _sequence=SELECTEDVALUE('rpt_job_step_timing'[step_sequence])
			VAR history=FILTER(CALCULATETABLE('rpt_job_step_timing',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_step_timing')),
			    'rpt_job_step_timing'[Pipeline]=pipeline && 'rpt_job_step_timing'[job_run_id]<>currentJob
			    && 'rpt_job_step_timing'[started_at]>=anchor-30 && 'rpt_job_step_timing'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_step_timing'[ended_at]) && 'rpt_job_step_timing'[ended_at]>='rpt_job_step_timing'[started_at]
			    && NOT ISBLANK('rpt_job_step_timing'[step_duration_seconds]) && 'rpt_job_step_timing'[step_duration_seconds]>=0
			    && 'rpt_job_step_timing'[Outcome]="Successful" && 'rpt_job_step_timing'[notebook_name]=notebook && 'rpt_job_step_timing'[step_sequence]=_sequence && RELATED('rpt_job_run_summary'[Outcome])="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && NOT ISBLANK(notebook) && NOT ISBLANK(_sequence),COUNTROWS(history))
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-step-comparison"></a>
## Step comparison

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR n=[Step baseline n]
			VAR actual=[Step actual min]
			RETURN SWITCH(TRUE(),ISBLANK(n),"Select one step",n<5,"Insufficient history",ISBLANK(actual),"No duration recorded",actual<[Step prior p25 min],"Below prior P25",actual>[Step prior p75 min],"Above prior P75","Within prior IQR")
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-step-prior-mean-min"></a>
## Step prior mean min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-164.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_step_timing'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_step_timing'[Pipeline])
			VAR currentJob=SELECTEDVALUE('rpt_job_step_timing'[job_run_id])
			VAR notebook=SELECTEDVALUE('rpt_job_step_timing'[notebook_name])
			VAR _sequence=SELECTEDVALUE('rpt_job_step_timing'[step_sequence])
			VAR history=FILTER(CALCULATETABLE('rpt_job_step_timing',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_step_timing')),
			    'rpt_job_step_timing'[Pipeline]=pipeline && 'rpt_job_step_timing'[job_run_id]<>currentJob
			    && 'rpt_job_step_timing'[started_at]>=anchor-30 && 'rpt_job_step_timing'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_step_timing'[ended_at]) && 'rpt_job_step_timing'[ended_at]>='rpt_job_step_timing'[started_at]
			    && NOT ISBLANK('rpt_job_step_timing'[step_duration_seconds]) && 'rpt_job_step_timing'[step_duration_seconds]>=0
			    && 'rpt_job_step_timing'[Outcome]="Successful" && 'rpt_job_step_timing'[notebook_name]=notebook && 'rpt_job_step_timing'[step_sequence]=_sequence && RELATED('rpt_job_run_summary'[Outcome])="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && NOT ISBLANK(notebook) && NOT ISBLANK(_sequence) && COUNTROWS(history)>=5,AVERAGEX(history,DIVIDE('rpt_job_step_timing'[step_duration_seconds],60)))
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-step-prior-median-min"></a>
## Step prior median min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-165.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_step_timing'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_step_timing'[Pipeline])
			VAR currentJob=SELECTEDVALUE('rpt_job_step_timing'[job_run_id])
			VAR notebook=SELECTEDVALUE('rpt_job_step_timing'[notebook_name])
			VAR _sequence=SELECTEDVALUE('rpt_job_step_timing'[step_sequence])
			VAR history=FILTER(CALCULATETABLE('rpt_job_step_timing',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_step_timing')),
			    'rpt_job_step_timing'[Pipeline]=pipeline && 'rpt_job_step_timing'[job_run_id]<>currentJob
			    && 'rpt_job_step_timing'[started_at]>=anchor-30 && 'rpt_job_step_timing'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_step_timing'[ended_at]) && 'rpt_job_step_timing'[ended_at]>='rpt_job_step_timing'[started_at]
			    && NOT ISBLANK('rpt_job_step_timing'[step_duration_seconds]) && 'rpt_job_step_timing'[step_duration_seconds]>=0
			    && 'rpt_job_step_timing'[Outcome]="Successful" && 'rpt_job_step_timing'[notebook_name]=notebook && 'rpt_job_step_timing'[step_sequence]=_sequence && RELATED('rpt_job_run_summary'[Outcome])="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && NOT ISBLANK(notebook) && NOT ISBLANK(_sequence) && COUNTROWS(history)>=5,MEDIANX(history,DIVIDE('rpt_job_step_timing'[step_duration_seconds],60)))
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-step-prior-p25-min"></a>
## Step prior p25 min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-166.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_step_timing'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_step_timing'[Pipeline])
			VAR currentJob=SELECTEDVALUE('rpt_job_step_timing'[job_run_id])
			VAR notebook=SELECTEDVALUE('rpt_job_step_timing'[notebook_name])
			VAR _sequence=SELECTEDVALUE('rpt_job_step_timing'[step_sequence])
			VAR history=FILTER(CALCULATETABLE('rpt_job_step_timing',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_step_timing')),
			    'rpt_job_step_timing'[Pipeline]=pipeline && 'rpt_job_step_timing'[job_run_id]<>currentJob
			    && 'rpt_job_step_timing'[started_at]>=anchor-30 && 'rpt_job_step_timing'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_step_timing'[ended_at]) && 'rpt_job_step_timing'[ended_at]>='rpt_job_step_timing'[started_at]
			    && NOT ISBLANK('rpt_job_step_timing'[step_duration_seconds]) && 'rpt_job_step_timing'[step_duration_seconds]>=0
			    && 'rpt_job_step_timing'[Outcome]="Successful" && 'rpt_job_step_timing'[notebook_name]=notebook && 'rpt_job_step_timing'[step_sequence]=_sequence && RELATED('rpt_job_run_summary'[Outcome])="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && NOT ISBLANK(notebook) && NOT ISBLANK(_sequence) && COUNTROWS(history)>=5,PERCENTILEX.INC(history,DIVIDE('rpt_job_step_timing'[step_duration_seconds],60),0.25))
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-step-prior-p75-min"></a>
## Step prior p75 min

Model: **mission**. Container: `_Run Benchmarks`. Classification: **Operational metric**. KPI records: MC-KPI-167.

Numeric/date operational definition in the latest saved model

```dax
VAR anchor=SELECTEDVALUE('rpt_job_step_timing'[started_at])
			VAR pipeline=SELECTEDVALUE('rpt_job_step_timing'[Pipeline])
			VAR currentJob=SELECTEDVALUE('rpt_job_step_timing'[job_run_id])
			VAR notebook=SELECTEDVALUE('rpt_job_step_timing'[notebook_name])
			VAR _sequence=SELECTEDVALUE('rpt_job_step_timing'[step_sequence])
			VAR history=FILTER(CALCULATETABLE('rpt_job_step_timing',REMOVEFILTERS('Load Calendar'),REMOVEFILTERS('rpt_job_run_summary'),REMOVEFILTERS('rpt_job_step_timing')),
			    'rpt_job_step_timing'[Pipeline]=pipeline && 'rpt_job_step_timing'[job_run_id]<>currentJob
			    && 'rpt_job_step_timing'[started_at]>=anchor-30 && 'rpt_job_step_timing'[ended_at]<anchor
			    && NOT ISBLANK('rpt_job_step_timing'[ended_at]) && 'rpt_job_step_timing'[ended_at]>='rpt_job_step_timing'[started_at]
			    && NOT ISBLANK('rpt_job_step_timing'[step_duration_seconds]) && 'rpt_job_step_timing'[step_duration_seconds]>=0
			    && 'rpt_job_step_timing'[Outcome]="Successful" && 'rpt_job_step_timing'[notebook_name]=notebook && 'rpt_job_step_timing'[step_sequence]=_sequence && RELATED('rpt_job_run_summary'[Outcome])="Successful")
			RETURN IF(NOT ISBLANK(anchor) && NOT ISBLANK(pipeline) && NOT ISBLANK(currentJob) && NOT ISBLANK(notebook) && NOT ISBLANK(_sequence) && COUNTROWS(history)>=5,PERCENTILEX.INC(history,DIVIDE('rpt_job_step_timing'[step_duration_seconds],60),0.75))
```

Source tables: `monitoring.rpt_job_run_summary`; `monitoring.rpt_job_step_timing`

<a id="mission-success-rate"></a>
## Success rate

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-168.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE([Successful],[Successful]+[Failures])
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-successful"></a>
## Successful

Model: **mission**. Container: `_Load Experience`. Classification: **Operational metric**. KPI records: MC-KPI-169.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome]="Successful"))
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-successful-archive-files"></a>
## Successful Archive Files

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-170.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.cfg_archive_file_load`

<a id="mission-successful-archive-zip-batches"></a>
## Successful Archive ZIP Batches

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-171.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.cfg_archive_zip_load`

<a id="mission-successful-gold-snapshots"></a>
## Successful Gold Snapshots

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-172.

Numeric/date operational definition in the latest saved model

```dax
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.cfg_month_end_gold_run`

<a id="mission-successful-job-runs"></a>
## Successful Job Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-173.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-successful-job-steps"></a>
## Successful Job Steps

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-174.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-successful-pipeline-runs"></a>
## Successful Pipeline Runs

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-175.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-timeline-job-visible"></a>
## Timeline Job Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_run_summary),
			    CALCULATE(COUNTROWS(rpt_job_run_summary), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-timeline-step-visible"></a>
## Timeline Step Visible

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_step_timing),
			    CALCULATE(COUNTROWS(rpt_job_step_timing), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Source tables: `monitoring.rpt_job_run_summary`

<a id="mission-total-job-step-duration-min"></a>
## Total Job Step Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-176.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( SUM ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )
```

Source tables: `monitoring.rpt_job_step_timing`

<a id="mission-total-pipeline-duration-min"></a>
## Total Pipeline Duration (min)

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-177.

Numeric/date operational definition in the latest saved model

```dax
SUMX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )
```

Source tables: `monitoring.cfg_pipeline_run`

<a id="mission-watch-tower-contracts-count"></a>
## Watch Tower Contracts Count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-178.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Discovery cfg_bronze_schema_live Scope count], REMOVEFILTERS())
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-contracts-date"></a>
## Watch Tower Contracts Date

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t = CALCULATE([Discovery cfg_bronze_schema_live Latest time], REMOVEFILTERS())
			RETURN IF(ISBLANK(t), "No retained discovery", "Schema captured: " & FORMAT(t, "dd MMM yyyy HH:mm"))
```

Source tables: `monitoring.cfg_bronze_schema_live`

<a id="mission-watch-tower-contracts-detail"></a>
## Watch Tower Contracts Detail

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery cfg_bronze_schema_live Distinct objects], REMOVEFILTERS()), "#,0") & " captured tables · " & FORMAT(CALCULATE([Discovery cfg_schema_contract_column Rows], REMOVEFILTERS()), "#,0") & " contract columns"
```

Source tables: `monitoring.cfg_bronze_schema_live`; `monitoring.cfg_job_run`; `monitoring.cfg_schema_contract_column`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-contracts-flag"></a>
## Watch Tower Contracts Flag

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR n=[Watch Tower Contracts Flag Records]
			VAR t=[Watch Tower Contracts Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),n=0,0,ISBLANK(t)||ISBLANK(anchor),1,
			    INT(t)=INT(anchor),3,
			    INT(t)>=INT(anchor)-7 && INT(t)<INT(anchor),2,1)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-contracts-flag-captured"></a>
## Watch Tower Contracts Flag Captured

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
MAXX(SELECTCOLUMNS(FILTER(CALCULATETABLE('cfg_schema_drift_event',REMOVEFILTERS()),(TRUE())),"Captured",COALESCE(cfg_schema_drift_event[last_detected_at],cfg_schema_drift_event[detected_at],cfg_schema_drift_event[first_detected_at])),[Captured])
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-contracts-flag-label"></a>
## Watch Tower Contracts Flag Label

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR code=[Watch Tower Contracts Flag]
			VAR captured=[Watch Tower Contracts Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),code=0,"No record",code=3,"Latest day",code=2,"Prior 7 days",
			    ISBLANK(captured),"Undated",ISBLANK(anchor),"No load date",INT(captured)>anchor,"Unlinked date","History")
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-contracts-flag-records"></a>
## Watch Tower Contracts Flag Records

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
COALESCE(COUNTROWS(FILTER(CALCULATETABLE('cfg_schema_drift_event',REMOVEFILTERS()),(TRUE()))),0)
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-contracts-flag-tooltip"></a>
## Watch Tower Contracts Flag Tooltip

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t=[Watch Tower Contracts Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN "Contracts & Schema: " & [Watch Tower Contracts Flag Label] & ". " &
			    IF([Watch Tower Contracts Flag Records]=0,"No retained problems recorded. ",IF(ISBLANK(t),"Capture date is not recorded. ","Last captured: " & FORMAT(t,"dd MMM yyyy HH:mm") & ". ")) &
			    IF(ISBLANK(anchor),"Latest load date is unavailable. ","Latest cached load day: " & FORMAT(anchor,"dd MMM yyyy") & ". ") &
			    "Red means the same load day; amber is the previous seven days; grey is older or undated. Date matching does not prove an exact job link. Schema/contract problem evidence uses recorded schema drift. Schema and contract captures alone are not problems."
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-contracts-reference"></a>
## Watch Tower Contracts Reference

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t = CALCULATE([Discovery cfg_schema_contract_column Latest time], REMOVEFILTERS())
			RETURN IF(ISBLANK(t), "No dated contract capture", "Contract: " & FORMAT(t, "dd MMM yyyy HH:mm"))
```

Source tables: `monitoring.cfg_schema_contract_column`

<a id="mission-watch-tower-domains-count"></a>
## Watch Tower Domains Count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-179.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Discovery cfg_data_domain Scope count], REMOVEFILTERS())
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-domains-date"></a>
## Watch Tower Domains Date

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t = CALCULATE([Discovery cfg_data_domain Latest time], REMOVEFILTERS())
			RETURN IF(ISBLANK(t), "No retained discovery", "Profiled: " & FORMAT(t, "dd MMM yyyy HH:mm"))
```

Source tables: `monitoring.cfg_data_domain`

<a id="mission-watch-tower-domains-detail"></a>
## Watch Tower Domains Detail

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery cfg_data_domain Distinct objects], REMOVEFILTERS()), "#,0") & " tables · " & FORMAT(CALCULATE([Discovery cfg_data_domain Rows], REMOVEFILTERS()), "#,0") & " snapshot records"
```

Source tables: `monitoring.cfg_data_domain`; `monitoring.cfg_job_run`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-domains-flag"></a>
## Watch Tower Domains Flag

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR n=[Watch Tower Domains Flag Records]
			VAR t=[Watch Tower Domains Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),n=0,0,ISBLANK(t)||ISBLANK(anchor),1,
			    INT(t)=INT(anchor),3,
			    INT(t)>=INT(anchor)-7 && INT(t)<INT(anchor),2,1)
```

Source tables: `monitoring.cfg_job_run`

<a id="mission-watch-tower-domains-flag-captured"></a>
## Watch Tower Domains Flag Captured

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
BLANK()
```

Source tables: No direct physical source asserted.

<a id="mission-watch-tower-domains-flag-label"></a>
## Watch Tower Domains Flag Label

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR code=[Watch Tower Domains Flag]
			VAR captured=[Watch Tower Domains Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),code=0,"No record",code=3,"Latest day",code=2,"Prior 7 days",
			    ISBLANK(captured),"Undated",ISBLANK(anchor),"No load date",INT(captured)>anchor,"Unlinked date","History")
```

Source tables: `monitoring.cfg_job_run`

<a id="mission-watch-tower-domains-flag-records"></a>
## Watch Tower Domains Flag Records

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
COALESCE(0,0)
```

Source tables: No direct physical source asserted.

<a id="mission-watch-tower-domains-flag-tooltip"></a>
## Watch Tower Domains Flag Tooltip

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t=[Watch Tower Domains Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN "Domains & Reference: " & [Watch Tower Domains Flag Label] & ". " &
			    IF([Watch Tower Domains Flag Records]=0,"No retained problems recorded. ",IF(ISBLANK(t),"Capture date is not recorded. ","Last captured: " & FORMAT(t,"dd MMM yyyy HH:mm") & ". ")) &
			    IF(ISBLANK(anchor),"Latest load date is unavailable. ","Latest cached load day: " & FORMAT(anchor,"dd MMM yyyy") & ". ") &
			    "Red means the same load day; amber is the previous seven days; grey is older or undated. Date matching does not prove an exact job link. Domain profiles contain no explicit problem register. Profile captures alone do not create a problem flag."
```

Source tables: `monitoring.cfg_job_run`

<a id="mission-watch-tower-domains-reference"></a>
## Watch Tower Domains Reference

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE(COUNTROWS(cfg_location_coordinate), REMOVEFILTERS()), "#,0") & " coordinate references · current"
```

Source tables: No direct physical source asserted.

<a id="mission-watch-tower-drift-active"></a>
## Watch Tower Drift Active

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-180.

Numeric/date operational definition in the latest saved model

```dax
VAR BatchKey = CALCULATE([Discovery cfg_schema_drift_event Latest key], REMOVEFILTERS())
			VAR BatchTime = CALCULATE([Discovery cfg_schema_drift_event Latest time], REMOVEFILTERS())
			VAR BatchRows = FILTER(CALCULATETABLE('cfg_schema_drift_event', REMOVEFILTERS()),
			    IF(ISBLANK(BatchKey), 'cfg_schema_drift_event'[detected_at] = BatchTime,
			       'cfg_schema_drift_event'[run_id] = BatchKey))
			RETURN COALESCE(COUNTROWS(FILTER(BatchRows, UPPER(cfg_schema_drift_event[status]) IN {"ACTIVE", "OPEN", "NEW", "DETECTED", "PENDING"})), 0)
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-count"></a>
## Watch Tower Drift Count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-181.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Discovery cfg_schema_drift_event Scope count], REMOVEFILTERS())
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-drift-date"></a>
## Watch Tower Drift Date

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t = CALCULATE([Discovery cfg_schema_drift_event Latest time], REMOVEFILTERS())
			RETURN IF(ISBLANK(t), "No retained discovery", "Detected: " & FORMAT(t, "dd MMM yyyy HH:mm"))
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-detail"></a>
## Watch Tower Drift Detail

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery cfg_schema_drift_event Distinct objects], REMOVEFILTERS()), "#,0") & " target tables · " & FORMAT([Watch Tower Drift Active], "#,0") & " active keys"
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-drift-flag"></a>
## Watch Tower Drift Flag

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR n=[Watch Tower Drift Flag Records]
			VAR t=[Watch Tower Drift Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),n=0,0,ISBLANK(t)||ISBLANK(anchor),1,
			    INT(t)=INT(anchor),3,
			    INT(t)>=INT(anchor)-7 && INT(t)<INT(anchor),2,1)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-flag-captured"></a>
## Watch Tower Drift Flag Captured

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
MAXX(SELECTCOLUMNS(FILTER(CALCULATETABLE('cfg_schema_drift_event',REMOVEFILTERS()),(TRUE())),"Captured",COALESCE(cfg_schema_drift_event[last_detected_at],cfg_schema_drift_event[detected_at],cfg_schema_drift_event[first_detected_at])),[Captured])
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-flag-label"></a>
## Watch Tower Drift Flag Label

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR code=[Watch Tower Drift Flag]
			VAR captured=[Watch Tower Drift Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),code=0,"No record",code=3,"Latest day",code=2,"Prior 7 days",
			    ISBLANK(captured),"Undated",ISBLANK(anchor),"No load date",INT(captured)>anchor,"Unlinked date","History")
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-flag-records"></a>
## Watch Tower Drift Flag Records

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
COALESCE(COUNTROWS(FILTER(CALCULATETABLE('cfg_schema_drift_event',REMOVEFILTERS()),(TRUE()))),0)
```

Source tables: `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-flag-tooltip"></a>
## Watch Tower Drift Flag Tooltip

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t=[Watch Tower Drift Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN "Schema & Drift: " & [Watch Tower Drift Flag Label] & ". " &
			    IF([Watch Tower Drift Flag Records]=0,"No retained problems recorded. ",IF(ISBLANK(t),"Capture date is not recorded. ","Last captured: " & FORMAT(t,"dd MMM yyyy HH:mm") & ". ")) &
			    IF(ISBLANK(anchor),"Latest load date is unavailable. ","Latest cached load day: " & FORMAT(anchor,"dd MMM yyyy") & ". ") &
			    "Red means the same load day; amber is the previous seven days; grey is older or undated. Date matching does not prove an exact job link. Recorded schema drift detections are problem evidence; resolution dates do not create a new detection."
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_drift_event`

<a id="mission-watch-tower-drift-reference"></a>
## Watch Tower Drift Reference

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery cfg_schema_drift_definition Rows], REMOVEFILTERS()), "#,0") & " definitions · " & FORMAT(CALCULATE([Discovery cfg_schema_definition_candidate Rows], REMOVEFILTERS()), "#,0") & " current candidates"
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_schema_definition_candidate`; `monitoring.cfg_schema_drift_definition`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-flag-latest-load-day"></a>
## Watch Tower Flag Latest Load Day

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t=CALCULATE(MAX('Discovery Job Runs'[started_at]),REMOVEFILTERS())
			RETURN IF(NOT ISBLANK(t),INT(t))
```

Source tables: `monitoring.cfg_job_run`

<a id="mission-watch-tower-flag-legend"></a>
## Watch Tower Flag Legend

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN "Problems recency · latest cached load day " & IF(ISBLANK(anchor),"unavailable",FORMAT(anchor,"dd MMM yyyy")) &
			    "   |   RED latest day   ·   AMBER prior 7 days   ·   GREY older / undated   ·   WHITE no recorded problems"
```

Source tables: `monitoring.cfg_job_run`

<a id="mission-watch-tower-quality-count"></a>
## Watch Tower Quality Count

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-182.

Numeric/date operational definition in the latest saved model

```dax
CALCULATE([Discovery rpt_job_data_quality Scope count], REMOVEFILTERS())
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-quality-date"></a>
## Watch Tower Quality Date

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t = CALCULATE([Discovery rpt_job_data_quality Latest time], REMOVEFILTERS())
			RETURN IF(ISBLANK(t), "No retained discovery", "Quality checked: " & FORMAT(t, "dd MMM yyyy HH:mm"))
```

Source tables: `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-detail"></a>
## Watch Tower Quality Detail

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery rpt_job_data_quality Rows], REMOVEFILTERS()), "#,0") & " checks · " & FORMAT([Watch Tower Quality Failed Checks], "#,0") & " failed"
```

Source tables: `monitoring.cfg_job_run`; `monitoring.rpt_job_data_quality`; `monitoring.rpt_job_run_summary`

<a id="mission-watch-tower-quality-failed-checks"></a>
## Watch Tower Quality Failed Checks

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-183.

Numeric/date operational definition in the latest saved model

```dax
VAR BatchKey = CALCULATE([Discovery rpt_job_data_quality Latest key], REMOVEFILTERS())
			VAR BatchTime = CALCULATE([Discovery rpt_job_data_quality Latest time], REMOVEFILTERS())
			VAR BatchRows = FILTER(CALCULATETABLE('rpt_job_data_quality', REMOVEFILTERS()),
			    IF(ISBLANK(BatchKey), 'rpt_job_data_quality'[checked_at] = BatchTime,
			       'rpt_job_data_quality'[run_id] = BatchKey))
			RETURN COALESCE(COUNTROWS(FILTER(BatchRows, rpt_job_data_quality[failed_row_count] > 0 || UPPER(rpt_job_data_quality[status]) IN {"FAIL", "FAILED", "ERROR"})), 0)
```

Source tables: `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-flag"></a>
## Watch Tower Quality Flag

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
VAR n=[Watch Tower Quality Flag Records]
			VAR t=[Watch Tower Quality Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),n=0,0,ISBLANK(t)||ISBLANK(anchor),1,
			    INT(t)=INT(anchor),3,
			    INT(t)>=INT(anchor)-7 && INT(t)<INT(anchor),2,1)
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-flag-captured"></a>
## Watch Tower Quality Flag Captured

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
MAXX(UNION(SELECTCOLUMNS(FILTER(CALCULATETABLE('rpt_job_data_quality',REMOVEFILTERS()),(COALESCE(rpt_job_data_quality[failed_row_count],0)>0
			    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
			    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
			    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"})),"Captured",rpt_job_data_quality[checked_at]),SELECTCOLUMNS(FILTER(CALCULATETABLE('cfg_rejected_row',REMOVEFILTERS()),(TRUE())),"Captured",cfg_rejected_row[rejected_at]),SELECTCOLUMNS(FILTER(CALCULATETABLE('cfg_referential_exception',REMOVEFILTERS()),(TRUE())),"Captured",cfg_referential_exception[detected_at])),[Captured])
```

Source tables: `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-flag-label"></a>
## Watch Tower Quality Flag Label

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR code=[Watch Tower Quality Flag]
			VAR captured=[Watch Tower Quality Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN SWITCH(TRUE(),code=0,"No record",code=3,"Latest day",code=2,"Prior 7 days",
			    ISBLANK(captured),"Undated",ISBLANK(anchor),"No load date",INT(captured)>anchor,"Unlinked date","History")
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-flag-records"></a>
## Watch Tower Quality Flag Records

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Filter/context helper**. KPI records: Helper/context only.

Selection, visibility, latest-batch or flag control

```dax
COALESCE(COUNTROWS(FILTER(CALCULATETABLE('rpt_job_data_quality',REMOVEFILTERS()),(COALESCE(rpt_job_data_quality[failed_row_count],0)>0
			    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
			    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
			    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}))) + COUNTROWS(FILTER(CALCULATETABLE('cfg_rejected_row',REMOVEFILTERS()),(TRUE()))) + COUNTROWS(FILTER(CALCULATETABLE('cfg_referential_exception',REMOVEFILTERS()),(TRUE()))),0)
```

Source tables: `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-flag-tooltip"></a>
## Watch Tower Quality Flag Tooltip

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
VAR t=[Watch Tower Quality Flag Captured]
			VAR anchor=[Watch Tower Flag Latest Load Day]
			RETURN "Quality & Exceptions: " & [Watch Tower Quality Flag Label] & ". " &
			    IF([Watch Tower Quality Flag Records]=0,"No retained problems recorded. ",IF(ISBLANK(t),"Capture date is not recorded. ","Last captured: " & FORMAT(t,"dd MMM yyyy HH:mm") & ". ")) &
			    IF(ISBLANK(anchor),"Latest load date is unavailable. ","Latest cached load day: " & FORMAT(anchor,"dd MMM yyyy") & ". ") &
			    "Red means the same load day; amber is the previous seven days; grey is older or undated. Date matching does not prove an exact job link. Failed/error quality findings, rejected rows and referential exceptions are problem evidence. Passing checks alone are not problems."
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_data_quality`

<a id="mission-watch-tower-quality-reference"></a>
## Watch Tower Quality Reference

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Display/context helper**. KPI records: Helper/context only.

Text, SVG or context expression; full definition retained separately

```dax
FORMAT(CALCULATE([Discovery cfg_rejected_row Rows], REMOVEFILTERS()), "#,0") & " rejected (" & FORMAT(CALCULATE([Discovery cfg_rejected_row Latest time], REMOVEFILTERS()), "dd MMM") & ") · " & FORMAT(CALCULATE([Discovery cfg_referential_exception Rows], REMOVEFILTERS()), "#,0") & " FK exceptions (" & FORMAT(CALCULATE([Discovery cfg_referential_exception Latest time], REMOVEFILTERS()), "dd MMM") & ")"
```

Source tables: `monitoring.cfg_job_run`; `monitoring.cfg_referential_exception`; `monitoring.cfg_rejected_row`; `monitoring.rpt_job_run_summary`

<a id="mission-weighted-dq-failure-percentage"></a>
## Weighted DQ Failure Percentage

Model: **mission**. Container: `_MissionControl_Measures`. Classification: **Operational metric**. KPI records: MC-KPI-184.

Numeric/date operational definition in the latest saved model

```dax
DIVIDE ( [DQ Failed Rows], [DQ Checked Rows] )
```

Source tables: `monitoring.cfg_data_quality_result`


<a id="business-linked-referral-current-status"></a>
## Linked referral current status

Model: **business**. Container: `Linked Provider Referrals`. Classification: **Display helper**.

Shows the distinct current referral statuses for visible linked-provider pairs, matched by referral UUID. A blank source status is shown as Unknown status. This is a current-state display field rather than a historical status or offer-status KPI.

```dax
VAR linkedPairs =
			    FILTER(
			        SUMMARIZE('Linked Provider Referrals',
			            'Linked Provider Referrals'[referral_id],
			            'Linked Provider Referrals'[provider_id]),
			        CALCULATE([Linked provider row visible]) = 1
			    )
			VAR linkedReferralIds =
			    DISTINCT(SELECTCOLUMNS(linkedPairs,
			        "referral_id", 'Linked Provider Referrals'[referral_id]))
			VAR statusValues =
			    CALCULATETABLE(
			        VALUES('fact_referral'[current_status]),
			        REMOVEFILTERS('dim_provider'),
			        KEEPFILTERS(TREATAS(linkedReferralIds,
			            'fact_referral'[referral_id]))
			    )
			RETURN IF(COUNTROWS(linkedPairs) > 0,
			    COALESCE(CONCATENATEX(
			        statusValues,
			        COALESCE('fact_referral'[current_status], "(Unknown status)"),
			        ", ",
			        'fact_referral'[current_status], ASC
			    ), "Referral not found"))
```

Source tables: `gold.fact_referral`; the existing linked-provider pair table.

# Current calculated-table logic

<a id="calculated-business-dashboard-metric-selector"></a>
## business: Dashboard Metric Selector

Saved source: `WMPP_v16`.

```dax
{
				    ("Total Referrals", NAMEOF('_Measures'[Total Referrals]), 0),
				    ("Referrals Awaiting Offer", NAMEOF('_Measures'[Referrals Awaiting Offer]), 1),
				    ("Referrals Under Offer", NAMEOF('_Measures'[Referrals Under Offer]), 2),
				    ("Offers Submitted", NAMEOF('_Measures'[Offers Submitted]), 3),
				    ("Accepted Offers", NAMEOF('_Measures'[Accepted Offers]), 4),
				    ("Pending Offers", NAMEOF('_Measures'[Pending Offers]), 5),
				    ("IPAs Created", NAMEOF('_Measures'[IPAs Created]), 6),
				    ("IPA Completed", NAMEOF('_Measures'[IPA Completed]), 7)
				}
```

<a id="calculated-business-days-to-target"></a>
## business: Days to Target

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "0 → 1 days", 1 },
				    { "2 → 3 days", 2 },
				    { "4 → 7 days", 3 },
				    { "8+ days", 4 },
				    { "Overdue", 5 },
				    { "No target", 6 }
				} )
```

<a id="calculated-business-directory-summary-axis"></a>
## business: Directory Summary Axis

Saved source: `WMPP_v16`.

```dax
DATATABLE(
				    "Display Type", STRING,
				    {
				        { "Residential Homes" },
				        { "Supported Accommodation Homes" },
				        { "Fostering Providers" }
				    }
				)
```

<a id="calculated-business-explorer-offer-activity"></a>
## business: Explorer Offer Activity

Saved source: `WMPP_v16`.

```text
table 'Explorer Offer Activity'
	lineageTag: 5fe39e33-d88b-5383-bfdf-9a179094decf

	column Band
		dataType: string
		lineageTag: cddcb83b-4a1d-588b-b9e0-c6434c5d5ffb
		summarizeBy: none
		sourceColumn: [Band]

	partition 'Explorer Offer Activity' = calculated
		mode: import
		source = DISTINCT(UNION(ROW("Band","(No offers)"), SELECTCOLUMNS('fact_offer',"Band",COALESCE('fact_offer'[Offer activity band],"(Unknown activity)"))))

```

<a id="calculated-business-explorer-offer-status"></a>
## business: Explorer Offer Status

Saved source: `WMPP_v16`.

```text
table 'Explorer Offer Status'
	lineageTag: 95892983-8d4c-5bfd-b252-e63bc5b54901

	column Status
		dataType: string
		lineageTag: fb0c2361-8c72-5514-a7e8-4ec2b0fe48f6
		summarizeBy: none
		sourceColumn: [Status]

	partition 'Explorer Offer Status' = calculated
		mode: import
		source = DISTINCT(UNION(ROW("Status","(No offers)"), SELECTCOLUMNS('fact_offer',"Status",COALESCE('fact_offer'[offer_status],"(Unknown status)"))))

```

<a id="calculated-business-kpi-selector"></a>
## business: KPI Selector

Saved source: `WMPP_v16`.

```dax
{
				    ("Gold Model Last Refreshed", NAMEOF('_Measures'[Gold Model Last Refreshed]), 0),
				    ("Average Days in Draft", NAMEOF('_Measures'[Average Days in Draft]), 1),
				    ("Draft Offers Stalled 7+ Days", NAMEOF('_Measures'[Draft Offers Stalled 7+ Days]), 2),
				    ("Draft No Activity Since Creation (Under Offer Referrals)", NAMEOF('_Measures'[Draft No Activity Since Creation (Under Offer Referrals)]), 3),
				    ("Draft Offers Missing Dates", NAMEOF('_Measures'[Draft Offers Missing Dates]), 4),
				    ("Draft Offer Count (Under Offer Referrals)", NAMEOF('_Measures'[Draft Offer Count (Under Offer Referrals)]), 5),
				    ("Draft Offers With Activity Since Creation", NAMEOF('_Measures'[Draft Offers With Activity Since Creation]), 6),
				    ("Draft Offers With No Activity %", NAMEOF('_Measures'[Draft Offers With No Activity %]), 7),
				    ("Drafts No Activity 14+ Days (Under Offer Referrals)", NAMEOF('_Measures'[Drafts No Activity 14+ Days (Under Offer Referrals)]), 8),
				    ("Draft Offers Stalled 14+ Days", NAMEOF('_Measures'[Draft Offers Stalled 14+ Days]), 9),
				    ("Oldest Draft Age Days", NAMEOF('_Measures'[Oldest Draft Age Days]), 10),
				    ("Accepted Offers", NAMEOF('_Measures'[Accepted Offers]), 11),
				    ("IPA Completed", NAMEOF('_Measures'[IPA Completed]), 12),
				    ("IPAs Created", NAMEOF('_Measures'[IPAs Created]), 13),
				    ("IPA Exists", NAMEOF('_Measures'[IPA Exists]), 14),
				    ("IPAs Pending Completion", NAMEOF('_Measures'[IPAs Pending Completion]), 15),
				    ("Is Awaiting IPA Creation", NAMEOF('_Measures'[Is Awaiting IPA Creation]), 16),
				    ("Is In Accepted KPI", NAMEOF('_Measures'[Is In Accepted KPI]), 17),
				    ("Is IPA Completed", NAMEOF('_Measures'[Is IPA Completed]), 18),
				    ("Is IPA Pending", NAMEOF('_Measures'[Is IPA Pending]), 19),
				    ("Offers Awaiting IPA Creation", NAMEOF('_Measures'[Offers Awaiting IPA Creation]), 20),
				    ("Successful Offers to IPA Completed %", NAMEOF('_Measures'[Successful Offers to IPA Completed %]), 21),
				    ("Referrals With Multiple Provider Assignments", NAMEOF('_Measures'[Referrals With Multiple Provider Assignments]), 22),
				    ("IPA Created to Completion %", NAMEOF('_Measures'[IPA Created to Completion %]), 23),
				    ("Pending Offers 30+ Days", NAMEOF('_Measures'[Pending Offers 30+ Days]), 24),
				    ("Pending Offers 8-14 Days", NAMEOF('_Measures'[Pending Offers 8-14 Days]), 25),
				    ("Pending Offers 15–30 Days", NAMEOF('_Measures'[Pending Offers 15–30 Days]), 26),
				    ("Pending Offers 0-7 Days", NAMEOF('_Measures'[Pending Offers 0-7 Days]), 27),
				    ("Pending Offers", NAMEOF('_Measures'[Pending Offers]), 28),
				    ("Providers With Pending Offers 30+ Days", NAMEOF('_Measures'[Providers With Pending Offers 30+ Days]), 29),
				    ("Active Referrals With Provider Engagement", NAMEOF('_Measures'[Active Referrals With Provider Engagement]), 30),
				    ("Active Awaiting Offers Without Engagement", NAMEOF('_Measures'[Active Awaiting Offers Without Engagement]), 31),
				    ("Active Referral Engagement Rate", NAMEOF('_Measures'[Active Referral Engagement Rate]), 32),
				    ("Avg Offers per Provider (Under Offer)", NAMEOF('_Measures'[Avg Offers per Provider (Under Offer)]), 33),
				    ("Average Offers per Referral Under Offer", NAMEOF('_Measures'[Average Offers per Referral Under Offer]), 34),
				    ("No. Providers Who Made Offers", NAMEOF('_Measures'[No. Providers Who Made Offers]), 35),
				    ("Pending Offers (Under Offer Referrals)", NAMEOF('_Measures'[Pending Offers (Under Offer Referrals)]), 36),
				    ("Successful Offers on Referrals Under Offer", NAMEOF('_Measures'[Successful Offers on Referrals Under Offer]), 37),
				    ("Offers Submitted", NAMEOF('_Measures'[Offers Submitted]), 38),
				    ("Unsuccessful Offers (Under Offer Referrals)", NAMEOF('_Measures'[Unsuccessful Offers (Under Offer Referrals)]), 39),
				    ("Directory Summary Count", NAMEOF('_Measures'[Directory Summary Count]), 40),
				    ("Providers - Fostering", NAMEOF('_Measures'[Providers - Fostering]), 41),
				    ("Framework Providers", NAMEOF('_Measures'[Framework Providers]), 42),
				    ("Is Non Framework Provider", NAMEOF('_Measures'[Is Non Framework Provider]), 43),
				    ("Non-Framework Providers", NAMEOF('_Measures'[Non-Framework Providers]), 44),
				    ("Provider Homes Registered", NAMEOF('_Measures'[Provider Homes Registered]), 45),
				    ("Providers - Residential", NAMEOF('_Measures'[Providers - Residential]), 46),
				    ("Providers - Supported Accommodation", NAMEOF('_Measures'[Providers - Supported Accommodation]), 47),
				    ("Providers Registered", NAMEOF('_Measures'[Providers Registered]), 48),
				    ("Residential Homes", NAMEOF('_Measures'[Residential Homes]), 49),
				    ("Supported Accommodation Homes", NAMEOF('_Measures'[Supported Accommodation Homes]), 50),
				    ("Referrals Awaiting Offer", NAMEOF('_Measures'[Referrals Awaiting Offer]), 51),
				    ("Referrals Under Offer", NAMEOF('_Measures'[Referrals Under Offer]), 52),
				    ("Closed Referrals", NAMEOF('_Measures'[Closed Referrals]), 53),
				    ("Framework Offers (Under Offer Referrals)", NAMEOF('_Measures'[Framework Offers (Under Offer Referrals)]), 54),
				    ("Offers on Referrals Under Offer", NAMEOF('_Measures'[Offers on Referrals Under Offer]), 55),
				    ("Offers per Provider (Under Offer Referrals)", NAMEOF('_Measures'[Offers per Provider (Under Offer Referrals)]), 56),
				    ("Open Referrals", NAMEOF('_Measures'[Open Referrals]), 57),
				    ("Provider Contact Referral", NAMEOF('_Measures'[Provider Contact Referral]), 58),
				    ("Provider Contact Referral Indicator", NAMEOF('_Measures'[Provider Contact Referral Indicator]), 59),
				    ("Closed or Cancelled Referrals", NAMEOF('_Measures'[Closed or Cancelled Referrals]), 60),
				    ("Referrals Currently Active", NAMEOF('_Measures'[Referrals Currently Active]), 61),
				    ("Referrals With an Offer Variance Indicator", NAMEOF('_Measures'[Referrals With an Offer Variance Indicator]), 62),
				    ("Referrals With an Offer", NAMEOF('_Measures'[Referrals With an Offer]), 63),
				    ("Female Referrals", NAMEOF('_Measures'[Female Referrals]), 64),
				    ("Male Referrals", NAMEOF('_Measures'[Male Referrals]), 65),
				    ("Other Referrals", NAMEOF('_Measures'[Other Referrals]), 66),
				    ("Referrals Not Yet Closed (Created in Period)", NAMEOF('_Measures'[Referrals Not Yet Closed]), 67),
				    ("Referrals With Offers (Created in Period)", NAMEOF('_Measures'[Referrals With Offers]), 68),
				    ("Total Gendered Referrals", NAMEOF('_Measures'[Total Gendered Referrals]), 69),
				    ("Total Referrals", NAMEOF('_Measures'[Total Referrals]), 70),
				    ("Spot Offers on Referrals Under Offer", NAMEOF('_Measures'[Spot Offers on Referrals Under Offer]), 71),
				    ("Referrals Created This Financial Year", NAMEOF('_Measures'[Referrals Created This Financial Year]), 72),
				    ("Referrals Created This Month", NAMEOF('_Measures'[Referrals Created This Month]), 73)
				}
```

<a id="calculated-business-linked-provider-referrals"></a>
## business: Linked Provider Referrals

Saved source: `WMPP_v16`.

```dax
VAR providerPairs =
				    DISTINCT(
				        SELECTCOLUMNS(
				            FILTER('fact_offer',
				                'fact_offer'[offer_status] IN {
				                    "OFFER_MADE",
				                    "OFFER_SUCCESSFUL",
				                    "OFFER_UNSUCCESSFUL"
				                }),
				            "referral_id", 'fact_offer'[referral_id],
				            "provider_id", 'fact_offer'[provider_id]
				        )
				    )
				RETURN
				    ADDCOLUMNS(
				        FILTER(providerPairs,
				            NOT ISBLANK([referral_id]) && NOT ISBLANK([provider_id])),
				        "provider_name",
				            VAR linkedProviderId = [provider_id]
				            RETURN COALESCE(
				                LOOKUPVALUE('dim_provider'[provider_name],
				                    'dim_provider'[provider_id], linkedProviderId),
				                "Unknown provider"),
				        "Source Reference ID",
				            VAR linkedReferralId = [referral_id]
				            VAR linkedPersonId =
				                LOOKUPVALUE('fact_referral'[person_id],
				                    'fact_referral'[referral_id], linkedReferralId)
				            RETURN IF(NOT ISBLANK(linkedPersonId),
				                LOOKUPVALUE('dim_person'[Source Reference ID],
				                    'dim_person'[person_id], linkedPersonId))
				    )
```

<a id="calculated-business-offer-journey-stage"></a>
## business: Offer Journey Stage

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "Offers received", 1 },
				    { "Reviewed — unavailable", 2 },
				    { "Shortlisted — unavailable", 3 },
				    { "Accepted", 4 },
				    { "Accepted with IPA", 5 }
				} )
```

<a id="calculated-business-offer-location-paths"></a>
## business: Offer Location Paths

Saved source: `WMPP_v16`.

```dax
VAR eligibleOffers =
				    FILTER ( 'fact_offer',
				        NOT ISBLANK ( 'fact_offer'[offer_id] )
				            && NOT ISBLANK ( 'fact_offer'[referral_id] )
				            && 'fact_offer'[referral_to_home_distance_status] IN { "APPROXIMATE_PREFERENCE_CITY", "APPROXIMATE_DEFAULT_CITY" }
				            && NOT ( 'fact_offer'[location_requires_review] == TRUE () )
				            && NOT ISBLANK ( 'fact_offer'[referral_latitude] )
				            && NOT ISBLANK ( 'fact_offer'[referral_longitude] )
				            && NOT ISBLANK ( 'fact_offer'[provider_home_latitude] )
				            && NOT ISBLANK ( 'fact_offer'[provider_home_longitude] )
				            && 'fact_offer'[referral_latitude] >= -90 && 'fact_offer'[referral_latitude] <= 90
				            && 'fact_offer'[provider_home_latitude] >= -90 && 'fact_offer'[provider_home_latitude] <= 90
				            && 'fact_offer'[referral_longitude] >= -180 && 'fact_offer'[referral_longitude] <= 180
				            && 'fact_offer'[provider_home_longitude] >= -180 && 'fact_offer'[provider_home_longitude] <= 180
				    )
				RETURN
				    UNION (
				        SELECTCOLUMNS ( eligibleOffers,
				            "Offer ID", 'fact_offer'[offer_id], "Referral ID", 'fact_offer'[referral_id],
				            "Provider", RELATED ( 'dim_provider'[provider_name] ),
				            "Home", RELATED ( 'dim_provider_home (offer)'[home_name] ),
				            "Referral city", 'fact_offer'[referral_location], "Home postcode", 'fact_offer'[provider_home_postcode],
				            "Offer status", 'fact_offer'[offer_status], "Distance km", 'fact_offer'[referral_to_home_distance_km],
				            "Location quality", IF ( 'fact_offer'[location_is_default], "Default-city estimate", "Preferred-city estimate" ),
				            "Endpoint type", "Referral city representative point", "Point order", 0,
				            "Latitude", 'fact_offer'[referral_latitude], "Longitude", 'fact_offer'[referral_longitude]
				        ),
				        SELECTCOLUMNS ( eligibleOffers,
				            "Offer ID", 'fact_offer'[offer_id], "Referral ID", 'fact_offer'[referral_id],
				            "Provider", RELATED ( 'dim_provider'[provider_name] ),
				            "Home", RELATED ( 'dim_provider_home (offer)'[home_name] ),
				            "Referral city", 'fact_offer'[referral_location], "Home postcode", 'fact_offer'[provider_home_postcode],
				            "Offer status", 'fact_offer'[offer_status], "Distance km", 'fact_offer'[referral_to_home_distance_km],
				            "Location quality", IF ( 'fact_offer'[location_is_default], "Default-city estimate", "Preferred-city estimate" ),
				            "Endpoint type", "Provider home postcode representative point", "Point order", 1,
				            "Latitude", 'fact_offer'[provider_home_latitude], "Longitude", 'fact_offer'[provider_home_longitude]
				        )
				    )
```

<a id="calculated-business-open-referral-age"></a>
## business: Open Referral Age

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "0 → 2 days", 1 },
				    { "3 → 7 days", 2 },
				    { "8 → 14 days", 3 },
				    { "15 → 28 days", 4 },
				    { "29+ days", 5 },
				    { "Unknown", 6 }
				} )
```

<a id="calculated-business-placement-window"></a>
## business: Placement Window

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "Within 1 day", 1 },
				    { "Within 3 days", 3 },
				    { "Within 7 days", 7 },
				    { "Within 14 days", 14 }
				} )
```

<a id="calculated-business-provider-explorer-kpi"></a>
## business: Provider Explorer KPI

Saved source: `WMPP_v16`.

```dax
DATATABLE("Group",STRING,"Metric",STRING,"Ordinal",INTEGER,"Definition",STRING,{
				{"Directory","Providers without any offers",0,"No offer record, including no draft records"},
				{"Directory","Providers in selection",1,"Distinct provider IDs, including providers without offers"},
				{"Directory","Provider homes",2,"All matching registered homes; no offer required"},
				{"Directory","Registered beds",3,"Recorded capacity, not vacancies; missing values remain unknown"},
				{"Activity","Distinct offer records",4,"Distinct offer IDs, including drafts"},
				{"Activity","Distinct offers made",5,"Non-draft records with a recorded status"},
				{"Activity","Draft offers",6,"Distinct draft offer IDs"},
				{"Activity","Accepted offers",7,"Distinct accepted/approved/selected/successful offers"},
				{"Activity","Pending offers",8,"Distinct awaiting-decision offer IDs"},
				{"Activity","Offer acceptance rate",9,"Accepted offers / non-draft offers made"},
				{"Engagement","Assigned referrals",10,"Distinct referrals assigned to matching providers"},
				{"Engagement","Referral assignments",11,"Distinct referral-provider assignment IDs"},
				{"Engagement","Recorded messages",12,"Messages in either direction; browsing is not captured"},
				{"Engagement","Qualifying responses",13,"Offer/reason response evidence, not every message"},
				{"Engagement","Qualifying response rate",14,"Qualifying response assignments / assignments"},
				{"Engagement","Average response minutes",15,"From assignment-level observations; excludes missing durations"},
				{"Engagement","Median response minutes",16,"Recomputed from assignment-level observations"},
				{"Placement","IPAs linked to offers",17,"Linked by accepted offer ID, not all IPAs on a shared referral"},
				{"Placement","Provider-signed IPAs",18,"Provider signature evidence only"},
				{"Placement","Completed IPAs",19,"Recorded completion flag"},
				{"Action","Assignments without qualifying response",20,"Recorded no-response assignments with a start time; not an SLA failure count"},
				{"Evidence","Response timing coverage",21,"Qualifying responses with an elapsed duration / qualifying responses"},
				{"Directory","QA flagged homes",22,"Current home QA flag only; not a quality-of-care score"},
				{"Directory","Providers without recorded activity",23,"No assignment, offer or message records in the current context"},
				{"Documents","Recorded documents",24,"Latest document IDs for eligible homes; home attribution awaits owner validation"},
				{"Documents","Expired documents",25,"Expiry before today; unknown dates excluded; not compliance"},
				{"Documents","Documents expiring in 30 days",26,"Expiry from today through today + 30 inclusive"},
				{"Documents","Homes with expired documents",27,"Distinct recorded home IDs with a past expiry; not blocked providers"}
				})
```

<a id="calculated-business-provider-offer-status"></a>
## business: Provider Offer Status

Saved source: `WMPP_v16`.

```text
table 'Provider Offer Status'
	lineageTag: 746957bb-4cec-5ee6-a4db-5304d4220229

	column Status
		dataType: string
		lineageTag: 6e0f853d-43e2-5acb-a4ec-496346d9eea0
		summarizeBy: none
		sourceColumn: [Status]

	partition 'Provider Offer Status' = calculated
		mode: import
		source = DISTINCT(UNION(ROW("Status","(No offers)"), SELECTCOLUMNS('fact_offer',"Status",COALESCE('fact_offer'[offer_status],"(Unknown status)"))))

```

<a id="calculated-business-provider-scoring-evidence"></a>
## business: Provider Scoring Evidence

Saved source: `WMPP_v16`.

```dax
DATATABLE("Group",STRING,"Metric",STRING,"Ordinal",INTEGER,"Definition",STRING,{
				{"Response","Qualifying response rate",0,"Qualifying responses / assignment-cohort opportunities; offers or recorded reasons, not message volume"},
				{"Conversion","Accepted offer share",1,"Accepted / offer records attributed to assignment cohorts; Gold includes draft records in its offer component"},
				{"Target","Placed by target share",2,"Placed by target / referrals with an accepted offer; recorded target outcome, not independently confirmed admission"},
				{"Speed","Median response hours",3,"Assignment-level median elapsed minutes / 60; not a business-calendar SLA score"},
				{"Documents","Required document compliance",4,"Not scored: required-document rules and home-ID contract approval are missing"},
				{"Feedback","Officer feedback",5,"Not scored: structured moderated ratings are unavailable; message sentiment is excluded"},
				{"Handling","Decline and closure handling",6,"Not scored: business-owned reason attribution is not approved"},
				{"Cost","Comparable cost",7,"Not scored: comparable service cohorts, fee completeness and minimum samples are not approved"},
				{"Overall","Overall provider score",8,"Not approved: no composite weights, minimum samples, version or quality-of-care rating"}
				})
```

<a id="calculated-business-referral-category"></a>
## business: Referral Category

Saved source: `WMPP_v16`.

```text
table 'Referral Category'
	lineageTag: 5d93563f-851b-512b-9e5b-369f3bfb5ddb

	column 'Category ID'
		dataType: int64
		isHidden
		lineageTag: 2d605b90-690a-5b78-bc87-dae3fbc5cc18
		summarizeBy: none
		sourceColumn: [Category ID]

	column Category
		dataType: string
		lineageTag: 81ca59cc-6eb1-550c-b1dc-7b1552bc67c2
		summarizeBy: none
		sourceColumn: [Category]

	column Framework
		dataType: string
		lineageTag: 2060aedc-6d1d-5030-856d-34c9b176bc51
		summarizeBy: none
		sourceColumn: [Framework]

	partition 'Referral Category' = calculated
		mode: import
		source = SELECTCOLUMNS('dim_framework_category', "Category ID", 'dim_framework_category'[framework_category_id], "Category", 'dim_framework_category'[category_name], "Framework", 'dim_framework_category'[framework_code])

```

<a id="calculated-business-referral-explorer-kpi"></a>
## business: Referral Explorer KPI

Saved source: `WMPP_v16`.

```dax
DATATABLE("Group",STRING,"Metric",STRING,"Ordinal",INTEGER,"Definition",STRING,{
				{"Referrals","Referrals in selection",0,"Master referral list; an offer is not required"},
				{"Referrals","Open referrals",1,"Recorded open flag"},
				{"Referrals","Open and overdue",2,"Recorded overdue flag"},
				{"Referrals","Closed / cancelled / withdrawn",3,"Recorded closed/terminal referral status"},
				{"Offers","Referrals with offers",4,"At least one offer record, including drafts"},
				{"Offers","Referrals without offers",5,"No offer record in the current source context"},
				{"Offers","Offer coverage",6,"Referrals with offers / matching referrals"},
				{"Offers","Distinct offer records",7,"Distinct offer IDs linked to matching referrals"},
				{"Offers","Accepted offers",8,"Distinct accepted/approved/selected/successful offers"},
				{"Engagement","Provider assignments",9,"Distinct referral-provider assignment IDs"},
				{"Engagement","Recorded messages",10,"Message count in either direction, not browsing events"},
				{"Placement","IPAs",11,"Distinct IPA IDs linked to matching referrals"},
				{"Placement","Completed IPAs",12,"Recorded completion flag"},
				{"Action","Open referrals without offers",13,"Open referrals with no offer records, including no drafts"},
				{"Action","Open referrals without assignments",14,"Open referrals with no referral-provider assignment records"},
				{"Action","Accepted offer but no IPA",15,"Referrals with accepted offer evidence and no IPA record"},
				{"Action","IPAs awaiting either signature",16,"Distinct IPAs without both signatures on the same IPA; missing signature evidence is included"},
				{"Action","Open overdue share",17,"Open overdue referrals / open referrals in the same selection"}
				})
```

<a id="calculated-business-referral-map-points"></a>
## business: Referral Map Points

Saved source: `WMPP_v16`.

```dax
UNION(SELECTCOLUMNS('fact_referral_provider',
				        "Referral", [referral_id], "Point ID", "P:" & [referral_provider_id], "Location type", "Assigned provider",
				        "Provider", RELATED('dim_provider'[provider_name]), "Home", BLANK(), "Offer", BLANK(),
				        "Address", RELATED('dim_provider'[town_city]) & ", " & RELATED('dim_provider'[county]) & ", " & RELATED('dim_provider'[postcode]),
				        "Map location", IF(NOT ISBLANK(RELATED('dim_provider'[postcode])), RELATED('dim_provider'[postcode]) & ", United Kingdom")), SELECTCOLUMNS('fact_offer',
				        "Referral", [referral_id], "Point ID", "O:" & [offer_id], "Location type", "Offer home",
				        "Provider", RELATED('dim_provider'[provider_name]), "Home", RELATED('dim_provider_home (offer)'[home_name]), "Offer", [offer_id],
				        "Address", RELATED('dim_provider_home (offer)'[town_city]) & ", " & RELATED('dim_provider_home (offer)'[county]) & ", " & RELATED('dim_provider_home (offer)'[postcode]),
				        "Map location", IF(NOT ISBLANK(RELATED('dim_provider_home (offer)'[postcode])), RELATED('dim_provider_home (offer)'[postcode]) & ", United Kingdom")))
```

<a id="calculated-business-requirement-kpi-monitor"></a>
## business: Requirement KPI Monitor

Saved source: `WMPP_v16`.

```dax
DATATABLE("KPI IDs",STRING,"Requirement IDs",STRING,"Metric",STRING,"Interpretation",STRING,"Requirement keys",STRING,"Ordinal",INTEGER,{
			    {"KPI-21","R24, R26","Active Awaiting Offers With Engagement","Existing reporting definition; refreshed totals and requirement acceptance remain pending.","|R24|R26|",0},
			    {"GOLD-KPI-024","R62","Average estimated weekly cost (IPA issued)","Estimate for referrals with IPA issue dates; not actual spend.","|R62|",1},
			    {"GOLD-KPI-030","R13","Closed referrals at selected snapshot","Snapshot-state metric; select a snapshot month. Not closures occurring during a period.","|R13|",2},
			    {"KPI-101","R47, R48","Expired documents","Expiry before today; a document count, not a compliance decision.","|R47|R48|",3},
			    {"KPI-100","R47","Documents expiring in 30 days","Expiry from today through today + 30 inclusive; missing dates excluded.","|R47|",4},
			    {"KPI-17","R24","Draft Offers on Referrals Under Offer","Existing reporting definition; refreshed totals and requirement acceptance remain pending.","|R24|",5},
			    {"KPI-58; KPI-63","R24","Draft offers aged 14+ days","Existing measure uses offer_age_days; does not establish 14 days without activity.","|R24|",6},
			    {"KPI-92","R18, R57","Same-day referral share","Gold emergency proxy / all referrals; not a placement success rate. Owner approval pending.","|R18|R57|",7},
			    {"KPI-91; KPI-94","R18, R57","Same-day referrals (current open/under offer)","Gold same-day-date proxy, not a statutory emergency classification.","|R18|R57|",8},
			    {"KPI-114","R20, R35","Recorded IPA completion rate","IPA Completed / IPAs Created; completion flag does not certify both signatures.","|R20|R35|",9},
			    {"GOLD-KPI-117","R15, R35, R62","IPAs Signed by Local Authority","Recorded signature evidence at IPA grain; does not perform signing or certify the other party.","|R15|R35|R62|",10},
			    {"GOLD-KPI-116","R15, R35, R62","IPAs Signed by Provider","Recorded signature evidence at IPA grain; does not perform signing or certify the other party.","|R15|R35|R62|",11},
			    {"KPI-88","R53","Latest offer source export","Latest source export timestamp in context; not a Service refresh or SLA.","|R53|",12},
			    {"GOLD-KPI-010","R24","Median Days to First Action","Existing reporting definition; refreshed totals and requirement acceptance remain pending.","|R24|",13},
			    {"GOLD-KPI-011","R24","Median Days to First Offer","Existing reporting definition; refreshed totals and requirement acceptance remain pending.","|R24|",14},
			    {"KPI-84","R35","Accepted-offer share without linked IPA","Complement of accepted-offer-to-IPA conversion; respects existing blank denominator handling.","|R35|",15},
			    {"KPI-06; GOLD-KPI-112","R51","Referrals in recorded Other gender group","Uses gender_clean = Other; missing/unknown categories retain current source treatment.","|R51|",16},
			    {"KPI-94; KPI-93","R18, R57","Planned referrals (current open/under offer)","Dated non-emergency proxy; undated records excluded. Definition approval pending.","|R18|R57|",17},
			    {"GOLD-KPI-138","R26, R51","Provider Average Response Hours","Assignment-month Gold component; not a provider score. Choose the cohort deliberately; business approval pending.","|R26|R51|",18},
			    {"GOLD-KPI-027","R54","Provider Decline Rate","Recorded assignment decline status; reasons, cancellation distinction and history need owner reconciliation.","|R54|",19},
			    {"GOLD-KPI-026","R54","Provider Declines","Recorded assignment decline status; reasons, cancellation distinction and history need owner reconciliation.","|R54|",20},
			    {"KPI-110","R14","ProviderMessageSent lifecycle events","Counts recorded event type; authorship and complete message audit require validation.","|R14|",21},
			    {"GOLD-KPI-139","R26, R51","Provider Offer Conversion Rate","Assignment-month Gold component; not a provider score. Choose the cohort deliberately; business approval pending.","|R26|R51|",22},
			    {"KPI-117","R59","Approved provider share","Approved / registered providers; does not measure bulk-job success or due diligence.","|R59|",23},
			    {"GOLD-KPI-137","R26, R51","Provider Response Rate","Assignment-month Gold component; not a provider score. Choose the cohort deliberately; business approval pending.","|R26|R51|",24},
			    {"GOLD-KPI-140","R26, R51","Provider Target Placement Rate","Assignment-month Gold component; not a provider score. Choose the cohort deliberately; business approval pending.","|R26|R51|",25},
			    {"KPI-104","R49","Providers approved","Current approval status only; does not certify required documents.","|R49|",26},
			    {"KPI-104; KPI-116","R49, R59","Providers pending approval","Current provider-status proxy; no bulk process or due-diligence certification.","|R49|R59|",27},
			    {"KPI-97","R41","Providers with current QA flags","Current flags only; historical flag types and apply/remove workflow are absent.","|R41|",28},
			    {"KPI-99","R41","Homes flagged directly or through provider","Home QA flag OR flagged provider; not a quality-of-care score.","|R41|",29},
			    {"KPI-113","R20","Recorded lifecycle events","Distinct event IDs; not a complete application audit trail.","|R20|",30},
			    {"GOLD-KPI-006","R24, R26","Referrals flagged not seen by providers","Uses Gold is_not_seen_by_providers; validate the proxy against assignment records.","|R24|R26|",31},
			    {"KPI-16","R28","Unsuccessful Offers on Referrals Under Offer","Existing reporting definition; refreshed totals and requirement acceptance remain pending.","|R28|",32}
			})
```

<a id="calculated-business-snapshot-window"></a>
## business: Snapshot Window

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "Last 6 months", 6 },
				    { "Last 12 months", 12 }
				} )
```

<a id="calculated-business-target-status"></a>
## business: Target Status

Saved source: `WMPP_v16`.

```dax
DATATABLE ( "Label", STRING, "Ordinal", INTEGER, {
				    { "On Track", 1 },
				    { "Due Soon", 2 },
				    { "Overdue", 3 },
				    { "No target", 4 }
				} )
```

<a id="calculated-mission-domain-history-view"></a>
## mission: Domain History View

Saved source: `project X/reports/WMPP_v16/SM WMPP Mission Control/SM WMPP Mission Control.SemanticModel/definition/tables/Domain History View.tmdl`.

```text
table 'Domain History View'
	lineageTag: 8c8d3552-bc5c-56d9-9bbd-7a7ad46cc870

	column Mode
		dataType: string
		lineageTag: cdd53d99-d443-5323-a5e4-c958cc185f99
		summarizeBy: none
		sourceColumn: [Mode]

	partition 'Domain History View' = calculated
		mode: import
		source = DATATABLE("Mode", STRING, {{"Latest version"}, {"All retained versions"}})

```

<a id="calculated-mission-load-calendar"></a>
## mission: Load Calendar

Saved source: `project X/reports/WMPP_v16/SM WMPP Mission Control/SM WMPP Mission Control.SemanticModel/definition/tables/Load Calendar.tmdl`.

```dax
VAR _firstDate = MIN(COALESCE(MIN(rpt_job_run_summary[Run Date]), TODAY()), TODAY() - 364)
				VAR _lastDate = MAX(TODAY(), MAX(rpt_job_run_summary[Run Date]))
				RETURN ADDCOLUMNS(CALENDAR(DATE(YEAR(_firstDate),MONTH(_firstDate),1), EOMONTH(_lastDate,0)),
				"Week", INT((DAY([Date]) + WEEKDAY(DATE(YEAR([Date]),MONTH([Date]),1),2) - 2)/7)+1,
				"Weekday", FORMAT([Date],"ddd"), "WeekdayOrder", WEEKDAY([Date],2),
				"Month", IF(YEAR([Date])=YEAR(TODAY()) && MONTH([Date])=MONTH(TODAY()),"This month",FORMAT([Date],"yyyy MMM")),
				"MonthOrder", YEAR([Date])*100+MONTH([Date]))
```

# Notebook / Python / Spark SQL evidence

These are verbatim source spans from the inspected notebook files. A setup/reference span does not on its own prove population or runtime execution.

<a id="python-00-archive-load-py-635"></a>
## 00_archive_load.py:635

Source: [project X/00_archive_load.py:635](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_archive_load.py#L635).

```python
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qident(ARCHIVE_SCHEMA)}")

append_rows(
    "monitoring.cfg_pipeline_run",
    [(PIPELINE_RUN_ID, PIPELINE_NAME, "ARCHIVE", "ARCHIVE_ZIP", STARTED_AT, None,
      "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string",
)
```

<a id="python-00-archive-load-py-653"></a>
## 00_archive_load.py:653

Source: [project X/00_archive_load.py:653](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_archive_load.py#L653).

```python
zip_root_posix = f"/lakehouse/default/{ARCHIVE_ZIP_ROOT}"
extract_root_posix = f"/lakehouse/default/{EXTRACT_ROOT}"
os.makedirs(extract_root_posix, exist_ok=True)

# ZIP discovery/extraction is one optional producer of files. The archive
# loading stage below no longer depends on this list.
zip_batches = []
if RUN_ZIP_EXTRACTION:
    for root, _, files in os.walk(zip_root_posix):
        for file_name in files:
            if not file_name.lower().endswith(".zip"):
                continue
            full_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(
                full_path, "/lakehouse/default"
            ).replace("\\", "/")
            export_date = (
                parse_export_date(file_name)
                or parse_export_date(relative_path)
            )
            if export_date is None:
                print(
                    f"Skipping ZIP without YYYY-MM-DD export date: "
                    f"{relative_path}"
                )
                continue
            if (PROCESS_EXPORT_DATE
                    and export_date.strftime("%Y-%m-%d")
                    != PROCESS_EXPORT_DATE):
                continue
            zip_batches.append((export_date, relative_path, full_path))

zip_batches.sort(key=lambda item: (item[0], item[1]))
if RESET_ARCHIVE_TABLES and PROCESS_EXPORT_DATE:
    spark.sql(f'''UPDATE monitoring.cfg_pipeline_run
        SET ended_at=current_timestamp(), status='FAILED', tables_failed=1,
            error_message='RESET_ARCHIVE_TABLES requires all export dates'
        WHERE run_id={sql_string(PIPELINE_RUN_ID)} AND pipeline_name={sql_string(PIPELINE_NAME)}''')
    raise ValueError(
        "RESET_ARCHIVE_TABLES=True must be run with PROCESS_EXPORT_DATE "
        "blank so every historical export is rebuilt."
    )

zip_batches_by_month = {}
for batch_date, _, _ in zip_batches:
    month_key = batch_date.strftime("%Y-%m")
    zip_batches_by_month[month_key] = (
        zip_batches_by_month.get(month_key, 0) + 1
    )
if zip_batches:
    print(
        f"Discovered dated ZIPs: {len(zip_batches):,}; "
        f"min={zip_batches[0][0]:%Y-%m-%d}; "
        f"max={zip_batches[-1][0]:%Y-%m-%d}; "
        f"months={zip_batches_by_month}; "
        f"filter={PROCESS_EXPORT_DATE or '<all>'}"
    )
else:
    reason = "disabled" if not RUN_ZIP_EXTRACTION else "none discovered"
    print(
        f"ZIP extraction {reason}; archive inventory will scan "
        f"{EXTRACT_ROOT} independently"
    )

extracted_zips = skipped_zips = failed_zips = 0
zip_errors = []
for export_date, relative_zip, full_zip in zip_batches:
    extract_relative = f"{EXTRACT_ROOT}/{export_date:%Y-%m-%d}"
    extract_posix = f"/lakehouse/default/{extract_relative}"
    existing = audit_record(
        "monitoring.cfg_archive_zip_load",
        {"zip_path": relative_zip, "export_date": export_date},
    )
    if (existing and existing["status"] == "SUCCESS"
            and not existing["reload"]
            and os.path.isdir(extract_posix)):
        skipped_zips += 1
        print(f"Skipped extracted ZIP: {relative_zip}")
        continue
    if (existing and existing["status"] == "SUCCESS"
            and not os.path.isdir(extract_posix)):
        print(
            f"ZIP audit is SUCCESS but extraction folder is missing; "
            f"re-extracting {relative_zip}"
        )

    now = datetime.now(timezone.utc)
    attempt = int(existing["attempt_count"] or 0) + 1 if existing else 1
    first_loaded = existing.get("first_loaded_at") if existing else None
    running = (
        relative_zip, export_date, extract_relative, "RUNNING",
        bool(existing["reload"]) if existing else False, attempt, None,
        RUN_ID, now, None, None, first_loaded, now,
    )
    merge_audit(
        "monitoring.cfg_archive_zip_load", ZIP_AUDIT_SCHEMA, running,
        ["zip_path", "export_date"],
    )
    try:
        os.makedirs(extract_posix, exist_ok=True)
        file_count = safe_extract(full_zip, extract_posix)
        ended = datetime.now(timezone.utc)
        success = (
            relative_zip, export_date, extract_relative, "SUCCESS", False,
            attempt, file_count, RUN_ID, now, ended, None,
            first_loaded or ended, ended,
        )
        merge_audit(
            "monitoring.cfg_archive_zip_load", ZIP_AUDIT_SCHEMA, success,
            ["zip_path", "export_date"],
        )
        extracted_zips += 1
        print(f"Extracted {relative_zip}: {file_count:,} files")
    except Exception as exc:
        ended = datetime.now(timezone.utc)
        error = str(exc)[:4000]
        failed = (
            relative_zip, export_date, extract_relative, "FAILED",
            bool(existing["reload"]) if existing else False, attempt, None,
            RUN_ID, now, ended, error, first_loaded, ended,
        )
        merge_audit(
            "monitoring.cfg_archive_zip_load", ZIP_AUDIT_SCHEMA, failed,
            ["zip_path", "export_date"],
        )
        zip_errors.append(f"{relative_zip}: {error}")
        failed_zips += 1
        if STOP_ON_FIRST_ERROR:
            break

print(
    f"ZIP stage complete: extracted={extracted_zips}, "
    f"skipped={skipped_zips}, failed={failed_zips}, "
    f"discovered={len(zip_batches)}"
)
```

<a id="python-00-archive-load-py-798"></a>
## 00_archive_load.py:798

Source: [project X/00_archive_load.py:798](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_archive_load.py#L798).

```python
# Build one inventory dataframe directly from ARCHIVE_FILE_ROOT. This is
# independent of zip_batches and includes files copied manually to dated folders.
archive_file_root_posix = f"/lakehouse/default/{ARCHIVE_FILE_ROOT}"
os.makedirs(archive_file_root_posix, exist_ok=True)

raw_archive_files_df = discover_archive_files_dataframe(
    archive_file_root_posix, PROCESS_EXPORT_DATE
).cache()
raw_discovered_count = raw_archive_files_df.count()

# Apply optional source-type controls before consulting CFG audit state. When
# disabled, audit files incur no per-file reads, counts, deletes, or writes.
archive_files_df = filter_archive_file_types(
    raw_archive_files_df, LOAD_ARCHIVE_AUDIT
).cache()
discovered_count = archive_files_df.count()
audit_toggle_skipped = raw_discovered_count - discovered_count

archive_audit_df = spark.table("monitoring.cfg_archive_file_load")
pending_files_df = filter_pending_archive_files(
    archive_files_df, archive_audit_df, RESET_ARCHIVE_TABLES
).cache()

pending_count = pending_files_df.count()
audit_skipped = discovered_count - pending_count

files_by_export_date = {
    row["export_day"]: row["count"]
    for row in (
        archive_files_df
        .withColumn("export_day", F.date_format("export_date", "yyyy-MM-dd"))
        .groupBy("export_day")
        .count()
        .collect()
    )
}
pending_by_export_date = {
    row["export_day"]: row["count"]
    for row in (
        pending_files_df
        .withColumn("export_day", F.date_format("export_date", "yyyy-MM-dd"))
        .groupBy("export_day")
        .count()
        .collect()
    )
}
print(
    f"Archive inventory root: {ARCHIVE_FILE_ROOT}; "
    f"raw_discovered={raw_discovered_count:,}; "
    f"selected={discovered_count:,}; pending={pending_count:,}; "
    f"audit_toggle_skipped={audit_toggle_skipped:,}; "
    f"cfg_skipped={audit_skipped:,}; batches={files_by_export_date}; "
    f"pending_batches={pending_by_export_date}"
)
if audit_toggle_skipped:
    print(
        f"Skipped {audit_toggle_skipped:,} archived_audit files because "
        "LOAD_ARCHIVE_AUDIT=False. Set it to True to load them later."
    )
print("Pending archive files (no processing order is required):")
pending_files_df.select(
    "file_path", "export_date", "audit_status", "audit_reload"
).show(100, truncate=False)

reset_targets = set()
file_errors = []
metric_errors = []
processed = 0
skipped = audit_skipped
total_read = total_written = 0

# toLocalIterator streams the already-filtered dataframe to the driver. It does
# not issue an audit query for each file and does not impose an ordering.
for pending_row in pending_files_df.toLocalIterator():
    export_date = pending_row["export_date"]
    source_zip = pending_row["source_zip"]
    relative_path = pending_row["file_path"]
    file_name = pending_row["filename"]
    existing = None
    if pending_row["audit_status"] is not None:
        existing = {
            "status": pending_row["audit_status"],
            "reload": bool(pending_row["audit_reload"]),
            "attempt_count": pending_row["audit_attempt_count"],
            "first_loaded_at": pending_row["audit_first_loaded_at"],
        }

    physical_table = clean_table_name(file_name)
    audit_file_date = (
        parse_export_date(file_name)
        if physical_table.lower() == "audit"
        else None
    )
    target_object = f"{ARCHIVE_SCHEMA}.{physical_table}"

    now = datetime.now(timezone.utc)
    attempt = int(existing["attempt_count"] or 0) + 1 if existing else 1
    first_loaded = existing.get("first_loaded_at") if existing else None
    running = (
        relative_path, file_name, export_date, source_zip, target_object,
        "RUNNING", bool(existing["reload"]) if existing else False,
        attempt, None, None, RUN_ID, now, None, None, first_loaded, now,
    )
    merge_audit(
        "monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, running,
        ["file_path", "export_date"],
    )

    try:
        if file_name.lower().endswith(".parquet"):
            frame = spark.read.format("parquet").load(relative_path)
        else:
            frame = (
                spark.read.format("csv")
                .option("header", "true")
                .option("inferSchema", "false")
                .option("mode", "PERMISSIVE")
                .option("badRecordsPath", f"{ERROR_LOG_ROOT}/corrupt_rows")
                .option("quote", TEXT_QUALIFIER)
                .option("escape", TEXT_QUALIFIER)
                .option("multiLine", "true")
                .load(relative_path)
            )

        if audit_file_date is not None:
            frame = frame.withColumn(
                "audit_file_date",
                F.to_date(
                    F.lit(audit_file_date.strftime("%Y-%m-%d")),
                    "yyyy-MM-dd",
                ),
            )

        # Load every source row and overwrite any source export_date value with
        # the authoritative date inherited from the containing archive folder.
        frame = (
            frame
            .withColumn(
                "export_date",
                F.to_timestamp(
                    F.lit(export_date.strftime("%Y-%m-%d")),
                    "yyyy-MM-dd",
                ),
            )
            .withColumn("_archive_source_path", F.lit(relative_path))
            .withColumn("_archive_source_zip", F.lit(source_zip))
            .withColumn("_archive_run_id", F.lit(RUN_ID))
            .withColumn("_archive_load_ts", F.current_timestamp())
        )
        row_count = frame.count()

        if RESET_ARCHIVE_TABLES and target_object not in reset_targets:
            spark.sql(
                f"DROP TABLE IF EXISTS {qident(ARCHIVE_SCHEMA)}."
                f"{qident(physical_table)}"
            )
            reset_targets.add(target_object)

        # Legacy audit tables may pre-date export_date and archive
        # lineage. Add nullable loader-managed columns before replacement. Old
        # rows remain untouched; rows loaded from now on are replay-safe.
        if (
            physical_table.lower() == "audit"
            and spark.catalog.tableExists(target_object)
        ):
            ensure_legacy_audit_lineage(target_object)

        # Folder-derived export_date is the sole contract field. Migrate any
        # legacy STRING/DATE/TIMESTAMP_NTZ target before destructive replacement.
        # The incoming CSV export_date is intentionally not retained separately.
        if spark.catalog.tableExists(target_object):
            ensure_archive_export_date_timestamp(target_object)

        # Re-read the migrated target and cast the incoming field to its exact
        # Spark datatype. Any mismatch fails here, before Delta deletion.
        frame = align_frame_export_date_to_target(frame, target_object)

        # A pending file always replaces its previous target slice before all
        # rows are appended. This protects both normal reruns and manual reloads.
        if spark.catalog.tableExists(target_object):
            target_columns = spark.table(target_object).columns
            target_delta = DeltaTable.forName(spark, target_object)
            if "_archive_source_path" in target_columns:
                target_delta.delete(
                    F.col("_archive_source_path") == F.lit(relative_path)
                )
                print(f"Deleted prior source-path rows from {target_object}")
            elif "export_date" in target_columns:
                target_delta.delete(
                    F.to_date("export_date") == F.lit(export_date.date())
                )
                print(
                    f"Deleted legacy export-date rows from {target_object} "
                    f"for {export_date:%Y-%m-%d}"
                )
            else:
                raise ValueError(
                    f"{target_object} has neither export_date nor "
                    "source-file lineage, so a safe replacement is impossible."
                )

        (
            frame.write.format("delta").mode("append")
            .option("mergeSchema", "true").saveAsTable(target_object)
        )
        ended = datetime.now(timezone.utc)
        success = (
            relative_path, file_name, export_date, source_zip,
            target_object, "SUCCESS", False, attempt, row_count,
            row_count, RUN_ID, now, ended, None, first_loaded or ended,
            ended,
        )
        merge_audit(
            "monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, success,
            ["file_path", "export_date"],
        )
        # Metrics use the shared setup/Silver contract. A telemetry
        # failure is recorded as a warning and must not change a completed
        # archive file from SUCCESS to FAILED.
        try:
            append_rows(
                "monitoring.cfg_table_load_metric",
                [(
                    RUN_ID, "ARCHIVE", "ARCHIVE_FILE", relative_path,
                    target_object, row_count, row_count, 0, None, ended,
                    JOB_RUN_ID or None,
                )],
                "run_id string,layer string,source_kind string,"
                "source_object string,target_object string,rows_read long,"
                "rows_written long,duplicate_key_count long,"
                "null_primary_key_count long,recorded_at timestamp,job_run_id string",
            )
        except Exception as metric_exc:
            metric_error = (
                f"{relative_path}: {str(metric_exc)[:2000]}"
            )
            metric_errors.append(metric_error)
            print(f"WARNING metric write failed: {metric_error}")
        processed += 1
        total_read += row_count
        total_written += row_count
        print(
            f"Loaded all {row_count:,} rows: {relative_path} -> "
            f"{target_object}; export_date={export_date:%Y-%m-%d}"
        )
    except Exception as exc:
        ended = datetime.now(timezone.utc)
        error = str(exc)[:4000]
        failed = (
            relative_path, file_name, export_date, source_zip,
            target_object, "FAILED",
            bool(existing["reload"]) if existing else False,
            attempt, None, None, RUN_ID, now, ended, error,
            first_loaded, ended,
        )
        merge_audit(
            "monitoring.cfg_archive_file_load", FILE_AUDIT_SCHEMA, failed,
            ["file_path", "export_date"],
        )
        file_errors.append(f"{relative_path}: {error}")
        print(f"FAILED {relative_path}: {error}")
        if STOP_ON_FIRST_ERROR:
            break
```

<a id="python-00-setup-cfg-py-96"></a>
## 00_setup_cfg.py:96

Source: [project X/00_setup_cfg.py:96](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_setup_cfg.py#L96).

```python
CONFIG_TABLE_DEFINITIONS = {
    # Approved local reference data only. Setup never seeds or replaces coordinates.
    # Use 00c_load_location_coordinates to preview/merge uploaded OS reference files.
    "monitoring.cfg_location_coordinate": [
        "location_type STRING", "location_key STRING", "latitude DOUBLE",
        "longitude DOUBLE", "reference_source STRING", "reference_version STRING",
    ],
    "monitoring.cfg_silver_export_load": [
        "source_kind STRING", "source_schema STRING", "source_table STRING",
        "target_table STRING", "export_date TIMESTAMP", "status STRING",
        "reload BOOLEAN", "attempt_count INT", "run_id STRING",
        "rows_read BIGINT", "rows_written BIGINT", "duplicate_key_count BIGINT",
        "started_at TIMESTAMP", "ended_at TIMESTAMP", "error_message STRING",
        "last_updated_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_pipeline_run": [
        "run_id STRING", "pipeline_name STRING", "layer STRING",
        "source_kind STRING", "started_at TIMESTAMP", "ended_at TIMESTAMP",
        "status STRING", "tables_succeeded INT", "tables_failed INT",
        "rows_read BIGINT", "rows_written BIGINT", "error_message STRING",
        "job_run_id STRING",
    ],
    "monitoring.cfg_table_load_metric": [
        "run_id STRING", "layer STRING", "source_kind STRING",
        "source_object STRING", "target_object STRING", "rows_read BIGINT",
        "rows_written BIGINT", "duplicate_key_count BIGINT",
        "null_primary_key_count BIGINT", "recorded_at TIMESTAMP",
        "job_run_id STRING",
    ],
    "monitoring.cfg_job_run": [
        "job_run_id STRING", "pipeline_name STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "status STRING", "steps_succeeded INT",
        "steps_failed INT", "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_job_step_run": [
        "job_run_id STRING", "step_sequence INT", "notebook_name STRING",
        "started_at TIMESTAMP", "ended_at TIMESTAMP", "status STRING",
        "child_result STRING", "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_drift_definition": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
        "join_class STRING", "join_evidence STRING",
        "definition_hash STRING", "definition_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_drift_event": [
        "run_id STRING", "source_kind STRING", "source_table STRING",
        "target_table STRING", "drift_type STRING", "column_name STRING",
        "expected_type STRING", "actual_type STRING", "referenced_table STRING",
        "referenced_column STRING", "drift_key STRING", "status STRING",
        "occurrence_count BIGINT", "first_detected_at TIMESTAMP",
        "last_detected_at TIMESTAMP", "resolved_at TIMESTAMP",
        "detected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_month_end_gold_run": [
        "snapshot_date DATE", "status STRING", "reload BOOLEAN",
        "attempt_count INT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "dq_result STRING", "gold_result STRING",
        "error_message STRING", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_zip_load": [
        "zip_path STRING", "export_date TIMESTAMP", "extract_path STRING",
        "status STRING", "reload BOOLEAN", "attempt_count INT",
        "file_count INT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "error_message STRING",
        "first_loaded_at TIMESTAMP", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_file_load": [
        "file_path STRING", "filename STRING", "export_date TIMESTAMP",
        "source_zip STRING", "target_object STRING", "status STRING",
        "reload BOOLEAN", "attempt_count INT", "rows_read BIGINT",
        "rows_written BIGINT", "run_id STRING", "started_at TIMESTAMP",
        "ended_at TIMESTAMP", "error_message STRING",
        "first_loaded_at TIMESTAMP", "last_updated_at TIMESTAMP",
    ],
    "monitoring.cfg_archive_table_export_load": [
        "source_schema STRING", "source_table STRING", "export_date TIMESTAMP",
        "status STRING", "reload BOOLEAN", "row_count BIGINT",
        "run_id STRING", "first_seen_at TIMESTAMP",
        "last_updated_at TIMESTAMP", "error_message STRING",
    ],
    "monitoring.cfg_schema_contract_column": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
        "join_class STRING", "join_evidence STRING",
        "contract_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_bronze_schema_live": [
        "table_name STRING", "ordinal_position INT", "column_name STRING",
        "live_data_type STRING", "is_nullable BOOLEAN",
        "captured_at TIMESTAMP", "run_id STRING", "job_run_id STRING",
    ],
    "monitoring.cfg_archived_schema_live": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "contract_loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_schema_definition_candidate": [
        "table_name STRING", "ordinal_position STRING", "column_name STRING",
        "data_type STRING", "is_nullable STRING", "column_default STRING",
        "primary_key_name STRING", "is_primary_key STRING",
        "foreign_key_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "column_description STRING", "table_description STRING",
    ],
    "monitoring.cfg_data_quality_result": [
        "run_id STRING", "rule_id STRING", "severity STRING",
        "rule_type STRING", "source_table STRING", "column_name STRING",
        "status STRING", "failed_row_count BIGINT", "checked_row_count BIGINT",
        "failure_percentage DOUBLE", "sample_key_json STRING",
        "checked_at TIMESTAMP", "message STRING", "job_run_id STRING",
    ],
    "monitoring.cfg_rejected_row": [
        "run_id STRING", "rule_id STRING", "source_table STRING",
        "business_key_json STRING", "rejection_reason STRING",
        "rejected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_referential_exception": [
        "run_id STRING", "rule_id STRING", "child_table STRING",
        "child_column STRING", "child_key STRING", "parent_table STRING",
        "parent_column STRING", "detected_at TIMESTAMP", "job_run_id STRING",
    ],
    "monitoring.cfg_data_domain": [
        "source_schema STRING", "source_table STRING", "column_name STRING",
        "contract_data_type STRING", "data_domain STRING",
        "distinct_value_count BIGINT", "profiled_at TIMESTAMP",
        "run_id STRING", "job_run_id STRING",
        "previous_run_id STRING", "previous_profiled_at TIMESTAMP",
        "change_type STRING", "is_present BOOLEAN", "profile_status STRING",
    ],
    "monitoring.cfg_data_quality_rule": [
        "rule_id STRING", "active STRING", "severity STRING",
        "rule_type STRING", "source_schema STRING", "table_name STRING",
        "column_name STRING", "referenced_schema STRING",
        "referenced_table STRING", "referenced_column STRING",
        "operator STRING", "rule_value STRING", "description STRING",
        "loaded_at TIMESTAMP",
    ],
    "monitoring.cfg_gold_lineage_mapping": [
        "gold_object STRING", "source_object STRING", "source_layer STRING",
        "transformation_notebook STRING", "relationship_role STRING",
        "is_required BOOLEAN", "description STRING",
    ],
    # Security mappings are deliberately configuration-driven. Empty tables
    # produce deny-by-default RLS once the semantic-model role is deployed;
    # access is never inferred from the currently-null fact_referral.region.
    "monitoring.cfg_security_scope": [
        "security_scope_key STRING", "scope_type STRING", "scope_code STRING",
        "scope_name STRING", "allows_global_summary BOOLEAN", "is_active BOOLEAN",
        "valid_from DATE", "valid_to DATE", "approved_by STRING",
        "updated_at TIMESTAMP",
    ],
    "monitoring.cfg_user_scope_access": [
        "user_principal_name STRING", "security_scope_key STRING",
        "is_active BOOLEAN", "valid_from DATE", "valid_to DATE",
        "approved_by STRING", "access_reason STRING", "updated_at TIMESTAMP",
    ],
    "monitoring.cfg_referral_scope": [
        "referral_id STRING", "security_scope_key STRING", "is_active BOOLEAN",
        "valid_from DATE", "valid_to DATE", "assigned_by STRING",
        "assignment_reason STRING", "updated_at TIMESTAMP",
    ],
    "gold.cfg_placement_urgency_rule": [
        "PlacementUrgencyBand STRING", "MaximumTargetDays INT",
        "WarningHoursBeforeTarget INT", "SortOrder INT", "IsActive BOOLEAN",
    ],
}


upgraded_tables = {}
for config_table, definitions in CONFIG_TABLE_DEFINITIONS.items():
    missing_columns = ensure_delta_table(config_table, definitions)
    if missing_columns:
        upgraded_tables[config_table] = missing_columns

print(
    f"Configuration tables ready: {len(CONFIG_TABLE_DEFINITIONS)}; "
    f"upgraded: {len(upgraded_tables)}"
)
```

<a id="python-01a-cfg-schema-capture-archive-py-107"></a>
## 01a_cfg_schema_capture_archive.py:107

Source: [project X/01a_cfg_schema_capture_archive.py:107](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_archive.py#L107).

```python
# 1. define target schema
schema_def = StructType([
    StructField("table_name", StringType(), True),
    StructField("ordinal_position", StringType(), True),
    StructField("column_name", StringType(), True),
    StructField("data_type", StringType(), True),
    StructField("is_nullable", StringType(), True),
])

schema_records=[]

all_tables = spark.catalog.listTables(COMPARED_SCHEMA)
excluded_tables = sorted(tbl.name for tbl in all_tables if is_etl_excluded_table(tbl.name))
tables = [tbl for tbl in all_tables if not is_etl_excluded_table(tbl.name)]
if excluded_tables:
    print(f"Excluded internal/reference archive-capture tables: {excluded_tables}")

for tbl in tables:
    columns= spark.catalog.listColumns(f"{COMPARED_SCHEMA}.{tbl.name}")
    for idx,col in enumerate(columns, start=1):
        if col.name.startswith("_"):
            continue
        schema_records.append((tbl.name, str(idx), col.name, col.dataType, "true" if col.nullable else "false"))

schema_df=spark.createDataFrame(schema_records, schema=schema_def)

schema_df.withColumn("contract_loaded_at", F.current_timestamp()) \
        .write.format("delta").mode("append")\
            .saveAsTable("monitoring.cfg_archived_schema_live")
```

<a id="python-01a-cfg-schema-capture-live-py-120"></a>
## 01a_cfg_schema_capture_live.py:120

Source: [project X/01a_cfg_schema_capture_live.py:120](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_live.py#L120).

```python
schema_df = spark.table("monitoring.cfg_schema_contract_column")
missing_columns = set(CONTRACT_COLUMNS) - set(schema_df.columns)
if missing_columns:
    raise ValueError(f"monitoring.cfg_schema_contract_column is missing: {sorted(missing_columns)}")
definition_df = (schema_df.select(*CONTRACT_COLUMNS)
    .withColumn(
        "definition_hash",
        F.sha2(F.concat_ws("||", *[F.coalesce(F.col(name), F.lit("")) for name in CONTRACT_COLUMNS]), 256),
    )
    .withColumn("definition_loaded_at", F.current_timestamp()))
(definition_df.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_schema_drift_definition"))

previous_live = None
if spark.catalog.tableExists("monitoring.cfg_bronze_schema_live"):
    old_live = spark.table("monitoring.cfg_bronze_schema_live")
    old_type = "live_data_type" if "live_data_type" in old_live.columns else "data_type"
    old_time = "captured_at" if "captured_at" in old_live.columns else "contract_loaded_at"
    previous_live = old_live.select(
        F.lower("table_name").alias("table_name"),
        F.col("column_name"),
        F.col(old_type).alias("live_data_type"),
        F.col(old_time).alias("captured_at"),
    )

captured_at = datetime.now(timezone.utc)
records = []
excluded_live_tables = []
for table in spark.catalog.listTables(BRONZE_SCHEMA):
    if table.isTemporary:
        continue
    if is_etl_excluded_table(table.name):
        excluded_live_tables.append(table.name)
        continue
    logical_table = etl_logical_table_name(table.name)
    for position, column in enumerate(
        spark.catalog.listColumns(f"{BRONZE_SCHEMA}.{table.name}"), start=1
    ):
        if column.name.startswith("_"):
            continue
        records.append((
            logical_table, position, column.name, column.dataType,
            bool(column.nullable), captured_at, RUN_ID, JOB_RUN_ID or None,
        ))

current_live = spark.createDataFrame(records, LIVE_SCHEMA)
if excluded_live_tables:
    print(f"Excluded internal/reference Bronze tables: {sorted(excluded_live_tables)}")
if previous_live is None:
    previous_live = current_live.limit(0).select(
        "table_name", "column_name", "live_data_type", "captured_at"
    )

definition_df.createOrReplaceTempView("_schema_definition")
current_live.createOrReplaceTempView("_schema_live_current")
previous_live.createOrReplaceTempView("_schema_live_previous")
print(f"Loaded {definition_df.count():,} definition rows; captured {current_live.count():,} live columns")
```

<a id="python-01a-cfg-schema-capture-live-py-189"></a>
## 01a_cfg_schema_capture_live.py:189

Source: [project X/01a_cfg_schema_capture_live.py:189](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_live.py#L189).

```python
current_drifts = spark.sql(f"""
WITH definition AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name,
         data_type, referenced_table, referenced_column
  FROM _schema_definition
  WHERE substring(column_name, 1, 1) <> '_'
), live AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name, live_data_type
  FROM _schema_live_current
  WHERE substring(column_name, 1, 1) <> '_'
), previous AS (
  SELECT lower(table_name) table_name, lower(column_name) column_name, live_data_type
  FROM _schema_live_previous
  WHERE substring(column_name, 1, 1) <> '_'
), definition_tables AS (SELECT DISTINCT table_name FROM definition),
live_tables AS (SELECT DISTINCT table_name FROM live),
drifts AS (
  SELECT l.table_name, CAST(NULL AS STRING) column_name, 'TABLE_ADDED' drift_type,
         CAST(NULL AS STRING) expected_type, CAST(NULL AS STRING) actual_type,
         CAST(NULL AS STRING) referenced_table, CAST(NULL AS STRING) referenced_column
  FROM live_tables l LEFT ANTI JOIN definition_tables d ON l.table_name=d.table_name
  UNION ALL
  SELECT d.table_name, CAST(NULL AS STRING), 'TABLE_REMOVED', NULL, NULL, NULL, NULL
  FROM definition_tables d LEFT ANTI JOIN live_tables l ON d.table_name=l.table_name
  UNION ALL
  SELECT l.table_name, l.column_name, 'COLUMN_ADDED', NULL, l.live_data_type, NULL, NULL
  FROM live l LEFT ANTI JOIN definition d
    ON l.table_name=d.table_name AND l.column_name=d.column_name
  UNION ALL
  SELECT d.table_name, d.column_name, 'COLUMN_REMOVED', d.data_type, NULL,
         d.referenced_table, d.referenced_column
  FROM definition d LEFT ANTI JOIN live l
    ON l.table_name=d.table_name AND l.column_name=d.column_name
  UNION ALL
  SELECT l.table_name, l.column_name, 'LIVE_TYPE_CHANGED', p.live_data_type,
         l.live_data_type, NULL, NULL
  FROM live l JOIN previous p
    ON l.table_name=p.table_name AND l.column_name=p.column_name
  WHERE coalesce(l.live_data_type, '') <> coalesce(p.live_data_type, '')
  UNION ALL
  SELECT d.table_name, d.column_name,
         CASE WHEN lt.table_name IS NULL THEN 'FK_TARGET_TABLE_MISSING'
              ELSE 'FK_TARGET_COLUMN_MISSING' END,
         d.data_type, CAST(NULL AS STRING), d.referenced_table, d.referenced_column
  FROM definition d
  LEFT JOIN live_tables lt ON lower(d.referenced_table)=lt.table_name
  LEFT JOIN live lc ON lower(d.referenced_table)=lc.table_name
                   AND lower(d.referenced_column)=lc.column_name
  WHERE coalesce(d.referenced_table, '') <> ''
    AND coalesce(d.referenced_column, '') <> ''
    AND lc.column_name IS NULL
)
SELECT
  '{RUN_ID}' run_id, '{SOURCE_KIND}' source_kind,
  concat('{BRONZE_SCHEMA}.', table_name) source_table,
  concat('silver.', table_name) target_table,
  drift_type, column_name, expected_type, actual_type,
  referenced_table, referenced_column,
  sha2(concat_ws('||', '{SOURCE_KIND}', table_name, coalesce(column_name, ''),
      drift_type, coalesce(referenced_table, ''), coalesce(referenced_column, '')), 256) drift_key,
  'ACTIVE' status, CAST(1 AS BIGINT) occurrence_count,
  current_timestamp() first_detected_at, current_timestamp() last_detected_at,
  CAST(NULL AS TIMESTAMP) resolved_at, current_timestamp() detected_at,
  '{JOB_RUN_ID}' job_run_id
FROM drifts
""")

# Candidate keeps approved metadata for observed columns. Invalid FK metadata is
# excluded from the candidate and remains visible as an FK_* drift event.
definition = definition_df.alias("d")
live = current_live.alias("l")
targets = current_live.select(
    F.lower("table_name").alias("target_table"),
    F.lower("column_name").alias("target_column"),
).distinct().alias("t")

candidate = (live.join(
        definition,
        (F.lower(F.col("l.table_name")) == F.lower(F.col("d.table_name")))
        & (F.lower(F.col("l.column_name")) == F.lower(F.col("d.column_name"))),
        "left",
    )
    .join(
        targets,
        (F.lower(F.col("d.referenced_table")) == F.col("t.target_table"))
        & (F.lower(F.col("d.referenced_column")) == F.col("t.target_column")),
        "left",
    ))
valid_fk = F.col("d.referenced_table").isNull() | F.col("t.target_column").isNotNull()
candidate = candidate.select(
    F.col("l.table_name").alias("table_name"),
    F.col("l.ordinal_position").cast("string").alias("ordinal_position"),
    F.col("l.column_name").alias("column_name"),
    F.coalesce(F.col("d.data_type"), F.col("l.live_data_type")).alias("data_type"),
    F.coalesce(F.col("d.is_nullable"), F.when(F.col("l.is_nullable"), "YES").otherwise("NO")).alias("is_nullable"),
    F.coalesce(F.col("d.column_default"), F.lit("NULL")).alias("column_default"),
    F.col("d.primary_key_name").alias("primary_key_name"),
    F.coalesce(F.col("d.is_primary_key"), F.lit("NO")).alias("is_primary_key"),
    F.when(valid_fk, F.col("d.foreign_key_name")).alias("foreign_key_name"),
    F.when(valid_fk, F.col("d.referenced_schema")).alias("referenced_schema"),
    F.when(valid_fk, F.col("d.referenced_table")).alias("referenced_table"),
    F.when(valid_fk, F.col("d.referenced_column")).alias("referenced_column"),
    F.col("d.column_description").alias("column_description"),
    F.col("d.table_description").alias("table_description"),
)
(candidate.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_schema_definition_candidate"))
```

<a id="python-01a-cfg-schema-capture-live-py-308"></a>
## 01a_cfg_schema_capture_live.py:308

Source: [project X/01a_cfg_schema_capture_live.py:308](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_live.py#L308).

```python
event_table = DeltaTable.forName(spark, "monitoring.cfg_schema_drift_event")
(event_table.alias("target")
    .merge(current_drifts.alias("source"), "target.drift_key = source.drift_key")
    .whenMatchedUpdate(set={
        "run_id": "source.run_id",
        "job_run_id": "source.job_run_id",
        "source_table": "source.source_table",
        "target_table": "source.target_table",
        "expected_type": "source.expected_type",
        "actual_type": "source.actual_type",
        "status": "'ACTIVE'",
        "occurrence_count": "coalesce(target.occurrence_count, 0) + 1",
        "last_detected_at": "source.last_detected_at",
        "resolved_at": "CAST(NULL AS TIMESTAMP)",
        "detected_at": "source.detected_at",
    })
    .whenNotMatchedInsertAll()
    .execute())

active_keys = current_drifts.select("drift_key").distinct()
resolved = (spark.table("monitoring.cfg_schema_drift_event")
    .where((F.col("source_kind") == SOURCE_KIND) & (F.col("status") == "ACTIVE"))
    .join(active_keys, "drift_key", "left_anti")
    .withColumn("status", F.lit("RESOLVED"))
    .withColumn("resolved_at", F.current_timestamp())
    .withColumn("last_detected_at", F.current_timestamp()))
if not resolved.rdd.isEmpty():
    (event_table.alias("target")
        .merge(resolved.alias("source"), "target.drift_key = source.drift_key")
        .whenMatchedUpdate(set={
            "status": "source.status",
            "resolved_at": "source.resolved_at",
            "last_detected_at": "source.last_detected_at",
        })
        .execute())

(current_live.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("monitoring.cfg_bronze_schema_live"))
```

<a id="python-02-silver-formatter-py-110"></a>
## 02_silver_formatter.py:110

Source: [project X/02_silver_formatter.py:110](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02_silver_formatter.py#L110).

```python
append_rows(
    "monitoring.cfg_pipeline_run",
    [(PIPELINE_RUN_ID, "02_silver_formatter", "SILVER", "LATEST", STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string",
)
```

<a id="python-02-silver-formatter-py-153"></a>
## 02_silver_formatter.py:153

Source: [project X/02_silver_formatter.py:153](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02_silver_formatter.py#L153).

```python
source_kind = "LATEST"
table_rows = spark.sql(f"SHOW TABLES IN {qident(BRONZE_SCHEMA)}").collect()
all_physical_tables = sorted(row.tableName for row in table_rows if not row.isTemporary)
excluded_physical_tables = excluded_etl_tables(all_physical_tables)
physical_tables = [name for name in all_physical_tables if not is_etl_excluded_table(name)]
if excluded_physical_tables:
    print(f"Excluded internal/reference Bronze tables: {excluded_physical_tables}")
metric_schema = "run_id string,layer string,source_kind string,source_object string,target_object string,rows_read long,rows_written long,duplicate_key_count long,null_primary_key_count long,recorded_at timestamp,job_run_id string"
drift_schema = "run_id string,source_kind string,source_table string,target_table string,drift_type string,column_name string,expected_type string,actual_type string,referenced_table string,referenced_column string,drift_key string,status string,occurrence_count long,first_detected_at timestamp,last_detected_at timestamp,resolved_at timestamp,detected_at timestamp,job_run_id string"

ok = failed = skipped = total_read = total_written = 0
errors = []

# Order tables so that FK parents are formatted before their children. The
# schema contract carries referenced_table for each FK; build a dependency
# graph over the contracted tables and topologically sort it. Alphabetical
# order alone can format a child (e.g. offer.additional_fee) before its parent
# (offer.offer), breaking downstream referential-integrity checks.
def order_tables_by_dependency(physical_tables):
    # Resolve each table's contract (metadata only, no data read) so we can
    # map normalised contract table name -> physical table.
    contract_name_to_physical = {}
    table_contract = {}
    for physical_table in physical_tables:
        contract_key = resolve_contract(physical_table, LATEST_PREFIXES)
        if contract_key is None:
            continue  # no contract: handled (and skipped) in the main loop
        table_contract[physical_table] = contract_key
        contract_name_to_physical.setdefault(
            normalise(contract_key), physical_table
        )

    # dependencies[physical] = set of physical tables that must load first.
    dependencies = {t: set() for t in physical_tables}
    for physical_table, contract_key in table_contract.items():
        for col in contracts[contract_key]:
            ref_table = (col.get("referenced_table") or "").strip()
            if not ref_table:
                continue
            parent = contract_name_to_physical.get(normalise(ref_table))
            if parent and parent != physical_table:
                dependencies[physical_table].add(parent)

    # Kahn's algorithm with deterministic (alphabetical) tie-breaking.
    ordered = []
    remaining = {t: set(deps) for t, deps in dependencies.items()}
    while remaining:
        ready = sorted(t for t, deps in remaining.items() if not deps)
        if not ready:  # cycle: break deterministically to avoid an infinite loop
            ready = [sorted(remaining)[0]]
        for physical_table in ready:
            ordered.append(physical_table)
            del remaining[physical_table]
            for deps in remaining.values():
                deps.discard(physical_table)
    return ordered


physical_tables = order_tables_by_dependency(physical_tables)
print("Dependency-ordered format: " + ", ".join(physical_tables))

for physical_table in physical_tables:
    source_table = f"{BRONZE_SCHEMA}.{physical_table}"
    target_table = None
    contract_key = None
    export_date = None
    try:
        # Read the export timestamp before contract resolution so a missing
        # table contract can still be recorded against a real source batch.
        frame = spark.table(source_table)
        if "export_date" not in frame.columns:
            raise ValueError(f"{source_table} has no export_date; rerun 01_bronze_get_latest first")

        export_date = (frame.select(F.max(F.to_timestamp("export_date")).alias("export_date"))
            .first()["export_date"])
        if export_date is None:
            raise ValueError(f"{source_table} has no valid export_date values")

        contract_key = resolve_contract(physical_table, LATEST_PREFIXES)
        if contract_key is None:
            message = f"No schema contract for {source_table}; table skipped"
            audit_finish(
                source_kind, BRONZE_SCHEMA, source_table, None, export_date,
                "SKIPPED_NO_CONTRACT", error_message=message,
            )
            append_rows(
                "monitoring.cfg_schema_drift_event",
                [drift_event_row(source_kind, source_table, None, "MISSING_TABLE_CONTRACT")],
                drift_schema,
            )
            skipped += 1
            print(f"SKIP {source_table} @ {export_date}: missing schema contract")
            continue

        contract_table = contract_key
        # SI-025: guarantee export_date reaches Silver even when the deployed
        # contract table is stale; also triggers a target schema refresh.
        schema_cols = ensure_export_date_contract(contracts[contract_key])
        target_table = f"{SILVER_SCHEMA}.{contract_table}"

        if (not FORCE_RERUN
                and should_skip(source_kind, BRONZE_SCHEMA, source_table, export_date)
                and not target_requires_refresh(target_table, schema_cols)):
            skipped += 1
            print(f"SKIP {source_table} @ {export_date}: already successful")
            continue
        if FORCE_RERUN:
            print(f"FORCE RERUN {source_table} @ {export_date}: bypassing prior success")

        audit_begin(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date)
        batch = frame.where(F.to_timestamp("export_date") == F.lit(export_date).cast("timestamp"))
        source_count = batch.count()
        contract_columns = {c["column_name"] for c in schema_cols}
        technical_columns = {c for c in batch.columns if c.startswith("_")}
        missing = sorted(contract_columns - set(batch.columns))
        extra = sorted(set(batch.columns) - contract_columns - technical_columns)
        drift_rows = [drift_event_row(
            source_kind, source_table, target_table, "MISSING", name,
            map_data_type(next(c["data_type"] for c in schema_cols if c["column_name"] == name)),
        ) for name in missing]
        drift_rows += [drift_event_row(
            source_kind, source_table, target_table, "EXTRA", name, actual_type=dict(batch.dtypes).get(name),
        ) for name in extra]
        append_rows("monitoring.cfg_schema_drift_event", drift_rows, drift_schema)

        deduplicated, duplicate_count = deduplicate_with_count(batch, schema_cols)
        formatted = format_frame(deduplicated, schema_cols, source_kind, source_table)
        formatted.write.format("delta").mode("overwrite").option("overwriteSchema", "true")             .saveAsTable(target_table)
        written = formatted.count()
        audit_finish(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date,
            "SUCCESS", source_count, written, duplicate_count)
        append_rows("monitoring.cfg_table_load_metric", [(RUN_ID, "SILVER", source_kind,
            source_table, target_table, source_count, written, duplicate_count, None,
            datetime.now(timezone.utc), JOB_RUN_ID or None)], metric_schema)
        ok += 1; total_read += source_count; total_written += written
        print(f"OK {source_table} -> {target_table} @ {export_date}: {written:,} rows")
    except Exception as exc:
        message = str(exc)[:4000]
        errors.append(f"{source_table}: {message}")
        failed += 1
        if export_date is not None:
            audit_finish(source_kind, BRONZE_SCHEMA, source_table, target_table, export_date,
                "FAILED", error_message=message)
        print(f"FAILED {source_table}: {message}")

status = "FAILED" if errors else "SUCCESS"
error_text = " | ".join(errors)[:4000] if errors else None
error_sql = "NULL" if error_text is None else "'" + error_text.replace("'", "''") + "'"
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run SET ended_at=current_timestamp(), status='{status}',
tables_succeeded={ok}, tables_failed={failed}, rows_read={total_read}, rows_written={total_written},
error_message={error_sql} WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='02_silver_formatter'""")
print(f"Latest Silver run {RUN_ID}: {status}; loaded={ok}, skipped={skipped}, failed={failed}")
if errors and FAIL_ON_TABLE_ERROR:
    raise RuntimeError(f"Silver formatting failed for {failed} table(s): {error_text}")
```

<a id="python-02a-archive-silver-py-195"></a>
## 02a_archive_silver.py:195

Source: [project X/02a_archive_silver.py:195](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02a_archive_silver.py#L195).

```python
append_rows(
    "monitoring.cfg_pipeline_run",
    [(PIPELINE_RUN_ID, "02a_archive_silver", "SILVER", "ARCHIVE", STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string",
)
```

<a id="python-02a-archive-silver-py-295"></a>
## 02a_archive_silver.py:295

Source: [project X/02a_archive_silver.py:295](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02a_archive_silver.py#L295).

```python
# Resolve every archive table to its contract once. We also collect each
# table's available export dates once, avoiding a max-date Spark job for
# every table in every month.
table_rows = spark.sql(f"SHOW TABLES IN {qident(ARCHIVE_SCHEMA)}").collect()
candidate_tables = sorted(
    row.tableName for row in table_rows
    if not row.isTemporary
    and not row.tableName.lower().startswith("cfg_")
    and row.tableName.lower() not in {
        name.lower() for name in EXCLUDED_ARCHIVE_TABLES
    }
    and not is_etl_excluded_table(row.tableName)
)


def archive_logical_name(physical_table):
    """Return the normalised source-named archive table."""
    return normalise(physical_table)


physical_tables = candidate_tables


framework_archive_present = any(
    archive_logical_name(table) == normalise(FRAMEWORK_FALLBACK_TABLE)
    for table in physical_tables
)

excluded_present = sorted(
    row.tableName for row in table_rows
    if row.tableName.lower() in {
        name.lower() for name in EXCLUDED_ARCHIVE_TABLES
    }
)
if excluded_present:
    print(f"Excluded raw archive-only tables: {excluded_present}")
excluded_internal_tables = sorted(
    row.tableName for row in table_rows
    if is_etl_excluded_table(row.tableName)
)
if excluded_internal_tables:
    print(f"Excluded internal/reference archive tables: {excluded_internal_tables}")

source_tables = []
skipped_contract_tables = []
all_available_dates = set()
contract_drift_schema = "run_id string,source_kind string,source_table string,target_table string,drift_type string,column_name string,expected_type string,actual_type string,referenced_table string,referenced_column string,drift_key string,status string,occurrence_count long,first_detected_at timestamp,last_detected_at timestamp,resolved_at timestamp,detected_at timestamp,job_run_id string"


def complete_framework_schema(schema_cols, source_table, target_table):
    """Supplement a stale framework contract with its controlled schema.

    Framework is required by Gold dimensions. A populated but older runtime
    contract can otherwise omit a source column (for example framework_name)
    and still let Archive Silver overwrite the target successfully.
    """
    present = {column["column_name"].lower() for column in schema_cols}
    missing = [
        column for column in FRAMEWORK_FALLBACK_SCHEMA
        if column["column_name"].lower() not in present
    ]
    if not missing:
        return schema_cols

    append_rows(
        "monitoring.cfg_schema_drift_event",
        [drift_event_row(
            "ARCHIVE_MONTH_END", source_table, target_table,
            "MISSING_REQUIRED_CONTRACT_COLUMN",
            column_name=column["column_name"],
            expected_type=column["data_type"],
        ) for column in missing],
        contract_drift_schema,
    )
    missing_names = [column["column_name"] for column in missing]
    print(
        f"WARN {source_table}: central framework contract is missing "
        f"{missing_names}; using the controlled framework schema and "
        "marking schema drift. Reload the central contract."
    )
    return sorted(
        list(schema_cols) + missing,
        key=lambda column: int(column.get("ordinal_position") or 999999),
    )

def parsed_archive_export_timestamp(column):
    """Parse both canonical and legacy archive export-date representations."""
    return first_parsed(F.trim(column.cast("string")), TIMESTAMP_FORMATS, F.to_timestamp)


for physical_table in physical_tables:
    source_table = f"{ARCHIVE_SCHEMA}.{physical_table}"
    source_frame = spark.table(source_table)
    if "export_date" not in source_frame.columns:
        raise ValueError(f"{source_table} has no row-level export_date")

    # Collect dates before resolving the contract. This gives an otherwise
    # unmodelled archive table a real export date in the audit controls.
    table_dates = sorted(
        row["export_date"]
        for row in source_frame
            .select(F.to_date(
                parsed_archive_export_timestamp(F.col("export_date"))
            ).alias("export_date"))
            .where(F.col("export_date").isNotNull())
            .distinct().collect()
    )
    if not table_dates:
        print(f"WARN {source_table} has no valid export_date values")
        continue

    logical_table = archive_logical_name(physical_table)
    is_framework_table = (
        logical_table == normalise(FRAMEWORK_FALLBACK_TABLE)
    )
    contract_key = resolve_contract(archive_logical_name(physical_table), ())
    if contract_key is None and is_framework_table:
        contract_table = FRAMEWORK_FALLBACK_TABLE
        schema_cols = FRAMEWORK_FALLBACK_SCHEMA
        append_rows(
            "monitoring.cfg_schema_drift_event",
            [drift_event_row(
                "ARCHIVE_MONTH_END", source_table,
                f"{SILVER_SCHEMA}.{contract_table}",
                "MISSING_TABLE_CONTRACT",
            )],
            contract_drift_schema,
        )
        print(
            f"WARN {source_table} has no central contract; "
            "using the temporary framework contract"
        )
    elif contract_key is None:
        message = f"No schema contract for {source_table}; table skipped"
        latest_export = datetime.combine(table_dates[-1], datetime.min.time())
        audit_finish(
            "ARCHIVE_MONTH_END", ARCHIVE_SCHEMA, source_table, None,
            latest_export, "SKIPPED_NO_CONTRACT", error_message=message,
        )
        append_rows(
            "monitoring.cfg_schema_drift_event",
            [drift_event_row("ARCHIVE_MONTH_END", source_table, None, "MISSING_TABLE_CONTRACT")],
            contract_drift_schema,
        )
        skipped_contract_tables.append(source_table)
        print(f"SKIP {source_table} @ {table_dates[-1]}: missing schema contract")
        continue
    else:
        contract_table = contract_key
        # SI-025: guarantee export_date reaches Silver even when the deployed
        # contract table is stale; also flags the target schema as stale.
        schema_cols = ensure_export_date_contract(contracts[contract_key])

    target_table = f"{SILVER_SCHEMA}.{contract_table}"
    if is_framework_table:
        schema_cols = complete_framework_schema(
            schema_cols, source_table, target_table
        )

    all_available_dates.update(table_dates)
    source_tables.append({
        "physical_table": physical_table,
        "source_schema": ARCHIVE_SCHEMA,
        "source_table": source_table,
        "target_table": target_table,
        "schema_cols": schema_cols,
        "available_dates": table_dates,
        "fallback_path": (
            FRAMEWORK_FALLBACK_PATH if is_framework_table else None
        ),
        "is_fallback_only": False,
    })
    if VERBOSE_DIAGNOSTICS:
        print(
            f"TABLE {source_table} -> {target_table}: "
            f"exports={len(table_dates):,}, min={table_dates[0]}, max={table_dates[-1]}"
        )

if not framework_archive_present:
    framework_contract_matches = contracts_by_table.get(
        normalise(FRAMEWORK_FALLBACK_TABLE), []
    )
    if len(framework_contract_matches) > 1:
        raise ValueError(
            "Ambiguous framework contracts: "
            f"{framework_contract_matches}"
        )
    framework_schema_cols = (
        contracts[framework_contract_matches[0]]
        if framework_contract_matches
        else FRAMEWORK_FALLBACK_SCHEMA
    )
    framework_schema_cols = complete_framework_schema(
        framework_schema_cols, FRAMEWORK_FALLBACK_PATH,
        f"{SILVER_SCHEMA}.{FRAMEWORK_FALLBACK_TABLE}",
    )
    source_tables.append({
        "physical_table": FRAMEWORK_FALLBACK_TABLE,
        "source_schema": "Files",
        "source_table": FRAMEWORK_FALLBACK_PATH,
        "target_table": f"{SILVER_SCHEMA}.{FRAMEWORK_FALLBACK_TABLE}",
        "schema_cols": framework_schema_cols,
        "available_dates": [],
        "fallback_path": FRAMEWORK_FALLBACK_PATH,
        "is_fallback_only": True,
    })
    print(
        "WARN archived framework table is completely absent; "
        f"using controlled fallback {FRAMEWORK_FALLBACK_PATH} for every month"
    )

# Order tables so that FK parents are materialised before their children.
# The schema contract carries referenced_table for each FK; build a dependency
# graph over the replayable set and topologically sort it. Alphabetical order
# alone can load a child (e.g. offer.additional_fee) before its parent
# (offer.offer), breaking downstream referential-integrity checks.
def order_tables_by_dependency(source_tables):
    # normalised contract table name -> target_table for the replayable set.
    contract_name_to_target = {}
    for entry in source_tables:
        contract_name_to_target.setdefault(
            normalise(entry["target_table"].split(".")[-1]),
            entry["target_table"],
        )

    # dependencies[target] = set of targets that must load first.
    dependencies = {entry["target_table"]: set() for entry in source_tables}
    for entry in source_tables:
        target = entry["target_table"]
        for col in entry["schema_cols"]:
            ref_table = (col.get("referenced_table") or "").strip()
            if not ref_table:
                continue
            parent_target = contract_name_to_target.get(normalise(ref_table))
            if parent_target and parent_target != target:
                dependencies[target].add(parent_target)

    # Kahn's algorithm with deterministic (alphabetical) tie-breaking.
    replayable = {entry["target_table"]: entry for entry in source_tables}
    ordered = []
    remaining = {t: set(deps) for t, deps in dependencies.items()}
    while remaining:
        ready = sorted(t for t, deps in remaining.items() if not deps)
        if not ready:  # cycle: break deterministically to avoid an infinite loop
            ready = [sorted(remaining)[0]]
        for target in ready:
            ordered.append(replayable[target])
            del remaining[target]
            for deps in remaining.values():
                deps.discard(target)
    return ordered


source_tables = order_tables_by_dependency(source_tables)
print(
    "Dependency-ordered replay: "
    + ", ".join(entry["physical_table"] for entry in source_tables)
)

if not source_tables or not all_available_dates:
    raise ValueError(f"No replayable archive tables found in {ARCHIVE_SCHEMA}")

available_dates = sorted(all_available_dates)
minimum_export_date = available_dates[0]
maximum_export_date = available_dates[-1]

# The final available export in each calendar month is the canonical
# snapshot date. A table that was not exported on that exact date carries
# forward its own latest available full snapshot on or before the date.
month_last_dates = {}
for export_date in available_dates:
    month_last_dates[(export_date.year, export_date.month)] = export_date
month_end_dates = sorted(month_last_dates.values())

if PROCESS_ONLY:
    if BATCH_EXPORT_DATE:
        raise ValueError("Set either PROCESS_ONLY (YYYY-MM) or BATCH_EXPORT_DATE (YYYY-MM-DD), not both")
    try:
        requested_month_date = datetime.strptime(PROCESS_ONLY, "%Y-%m")
    except ValueError as exc:
        raise ValueError("PROCESS_ONLY must use YYYY-MM, for example 2026-05") from exc
    requested_month = (requested_month_date.year, requested_month_date.month)
    if requested_month not in month_last_dates:
        raise ValueError(f"No archive exports found in requested month {PROCESS_ONLY}")
    canonical_date = month_last_dates[requested_month]
    month_end_dates = [canonical_date]
    print(f"PROCESS_ONLY {PROCESS_ONLY}; canonical month-end export is {canonical_date}")
elif BATCH_EXPORT_DATE:
    requested_date = datetime.strptime(BATCH_EXPORT_DATE, "%Y-%m-%d").date()
    requested_month = (requested_date.year, requested_date.month)
    if requested_month not in month_last_dates:
        raise ValueError(f"No archive exports found in requested month {requested_date:%Y-%m}")
    canonical_date = month_last_dates[requested_month]
    month_end_dates = [canonical_date]
    print(
        f"Requested {requested_date}; canonical month-end export is {canonical_date}"
    )

print(
    f"Archive export range: {minimum_export_date} to {maximum_export_date}; "
    f"{len(available_dates):,} distinct export days"
)
print(
    f"Month-end batches: {len(month_end_dates):,}; "
    f"{', '.join(str(value) for value in month_end_dates)}"
)
```

<a id="python-02a-archive-silver-py-611"></a>
## 02a_archive_silver.py:611

Source: [project X/02a_archive_silver.py:611](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02a_archive_silver.py#L611).

```python
from notebookutils import mssparkutils

SOURCE_KIND = "ARCHIVE_MONTH_END"
METRIC_SCHEMA = "run_id string,layer string,source_kind string,source_object string,target_object string,rows_read long,rows_written long,duplicate_key_count long,null_primary_key_count long,recorded_at timestamp,job_run_id string"
ok = failed = total_read = total_written = 0
skipped_months = 0
skipped_contracts = len(skipped_contract_tables)
errors = []


def month_end_record(snapshot_date):
    """Return the orchestration state for one canonical month-end."""
    rows = (spark.table("monitoring.cfg_month_end_gold_run")
        .where(F.col("snapshot_date") == F.lit(snapshot_date).cast("date"))
        .limit(1).collect())
    return rows[0].asDict() if rows else None


def update_month_end(snapshot_date, status, dq_result=None,
                     gold_result=None, error_message=None):
    """Upsert the DQ/Gold orchestration state for a snapshot."""
    now = datetime.now(timezone.utc)
    existing = month_end_record(snapshot_date) or {}
    attempt_count = int(existing.get("attempt_count") or 0) + (
        1 if status == "RUNNING" else 0
    )
    row = spark.createDataFrame([(
        snapshot_date,
        status,
        False if status in ("RUNNING", "SUCCESS") else bool(existing.get("reload", False)),
        attempt_count,
        RUN_ID,
        now if status == "RUNNING" else existing.get("started_at"),
        None if status == "RUNNING" else now,
        dq_result,
        gold_result,
        error_message[:4000] if error_message else None,
        now,
    )], "snapshot_date date,status string,reload boolean,attempt_count int,run_id string,started_at timestamp,ended_at timestamp,dq_result string,gold_result string,error_message string,last_updated_at timestamp")
    target = DeltaTable.forName(spark, "monitoring.cfg_month_end_gold_run")
    (target.alias("t").merge(row.alias("s"), "t.snapshot_date = s.snapshot_date")
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())


def latest_table_export(table_dates, snapshot_date):
    """Choose a table's latest full export on or before the snapshot."""
    position = bisect_right(table_dates, snapshot_date) - 1
    return table_dates[position] if position >= 0 else None



def materialise_table_month_end(table_info, snapshot_date):
    """Overwrite one Silver table with its canonical month-end state."""
    archive_source_schema = table_info.get(
        "source_schema", ARCHIVE_SCHEMA
    )
    archive_source_table = table_info["source_table"]
    target_table = table_info["target_table"]
    schema_cols = table_info["schema_cols"]
    fallback_path = table_info.get("fallback_path")
    archive_source_date = latest_table_export(
        table_info["available_dates"], snapshot_date
    )
    use_fallback = bool(table_info.get("is_fallback_only", False)) or (
        bool(fallback_path) and archive_source_date is None
    )
    source_schema = "Files" if use_fallback else archive_source_schema
    source_table = fallback_path if use_fallback else archive_source_table
    source_date = snapshot_date if use_fallback else archive_source_date
    if source_date is None:
        print(
            f"SKIP {archive_source_table}: "
            f"no export on or before {snapshot_date}"
        )
        return 0, 0, 0

    audit_timestamp = datetime.combine(snapshot_date, datetime.min.time())
    audit_begin(
        SOURCE_KIND, source_schema, source_table,
        target_table, audit_timestamp,
    )
    formatted = None
    try:
        # Each dated archive file is a complete snapshot. Selecting only
        # the final available file avoids scanning every daily snapshot. The
        # framework fallback is used only when that archive entity is absent.
        raw_frame = (
            read_framework_fallback(snapshot_date)
            if use_fallback
            else spark.table(source_table).where(
                F.to_date(parsed_archive_export_timestamp(F.col("export_date")))
                == F.lit(source_date)
            )
        )
        source_count = raw_frame.count()
        if source_count == 0:
            raise ValueError(f"No rows found for selected export {source_date}")

        deduplicated, key_columns = deduplicate_frame(raw_frame, schema_cols)

        # Persist so validation, diagnostics and the Delta write reuse the
        # same conformed result instead of recomputing the Spark plan.
        formatted = format_frame(
            deduplicated, schema_cols, SOURCE_KIND, source_table
        )
        if use_fallback:
            formatted = (formatted
                .withColumn("_archive_fallback", F.lit(True))
                .withColumn("_source_file", F.lit(FRAMEWORK_FALLBACK_PATH)))
        formatted = formatted.persist()
        written = formatted.count()
        duplicate_count = source_count - written
        formatted_export_non_null = formatted.where(
            F.col("export_date").isNotNull()
        ).count()
        if formatted_export_non_null != written:
            raise ValueError(
                f"export_date parse failure in {source_table}: "
                f"{written - formatted_export_non_null} of {written} rows are null"
            )

        print(f"MONTH END {snapshot_date}: {source_table} -> {target_table}")
        print_load_diagnostics(
            source_table, target_table, snapshot_date, source_date,
            raw_frame, formatted, key_columns, source_count, written,
            duplicate_count, formatted_export_non_null,
        )

        (formatted.write.format("delta").mode("overwrite")
            .option("overwriteSchema", "true").saveAsTable(target_table))

        if VERBOSE_DIAGNOSTICS:
            target_stats = spark.table(target_table).agg(
                F.count(F.lit(1)).alias("rows"),
                F.sum(F.when(F.col("export_date").isNull(), 1).otherwise(0)).alias("null_dates"),
                F.min("export_date").alias("min_export_date"),
                F.max("export_date").alias("max_export_date"),
            ).first().asDict()
            print(f"  TARGET CHECK {target_table}: {target_stats}")

        audit_finish(
            SOURCE_KIND, source_schema, source_table, target_table,
            audit_timestamp, "SUCCESS", source_count, written,
            duplicate_count,
        )
        append_rows(
            "monitoring.cfg_table_load_metric",
            [(RUN_ID, "SILVER", SOURCE_KIND, source_table, target_table,
              source_count, written, duplicate_count, None, datetime.now(timezone.utc),
              JOB_RUN_ID or None)],
            METRIC_SCHEMA,
        )
        return source_count, written, duplicate_count
    except Exception as exc:
        audit_finish(
            SOURCE_KIND, source_schema, source_table, target_table,
            audit_timestamp, "FAILED", error_message=str(exc)[:4000],
        )
        raise
    finally:
        if formatted is not None:
            formatted.unpersist()


def delete_monitoring_rows(table_name, predicate, label):
    """Delete a scoped operational-monitoring slice and report its count."""
    if not spark.catalog.tableExists(table_name):
        print(f"SKIP {label}: {table_name} does not exist")
        return 0
    before = spark.table(table_name).where(predicate).count()
    spark.sql(f"DELETE FROM {table_name} WHERE {predicate}")
    print(f"CLEARED {label}: {before:,} rows from {table_name}")
    return before


def drop_rebuildable_schema_objects(schema_name, preserved_objects=()):
    """Drop managed tables/views rebuilt by the archive replay."""
    preserved = {name.lower() for name in preserved_objects}
    rows = spark.sql(f"SHOW TABLES IN {qident(schema_name)}").collect()
    dropped = []
    for row in rows:
        object_name = row.tableName
        if row.isTemporary or object_name.lower() in preserved:
            continue
        object_type = spark.catalog.getTable(
            f"{schema_name}.{object_name}"
        ).tableType.upper()
        qualified_name = f"{qident(schema_name)}.{qident(object_name)}"
        statement = "DROP VIEW" if object_type == "VIEW" else "DROP TABLE"
        spark.sql(f"{statement} IF EXISTS {qualified_name}")
        dropped.append(f"{schema_name}.{object_name}")
    return dropped


def reset_all_archive_processing():
    """Clear archive replay state and rebuildable Silver/Gold objects."""
    if not RESET_ALL_ARCHIVE_PROCESSING:
        return

    print("RESET ALL preview: clearing archive replay state and rebuildable Silver/Gold objects")
    reset_slices = [
        ("monitoring.cfg_month_end_gold_run", "1 = 1", "month-end Gold runs"),
        ("monitoring.cfg_silver_export_load", "source_kind = 'ARCHIVE_MONTH_END'", "archive Silver export loads"),
        ("monitoring.cfg_table_load_metric", "source_kind = 'ARCHIVE_MONTH_END'", "archive table metrics"),
        ("monitoring.cfg_pipeline_run", "source_kind IN ('ARCHIVE', 'ARCHIVE_MONTH_END')", "archive pipeline runs"),
        ("monitoring.cfg_schema_drift_event", "source_kind IN ('ARCHIVE', 'ARCHIVE_MONTH_END')", "archive schema-drift events"),
    ]
    cleared_rows = sum(
        delete_monitoring_rows(table_name, predicate, label)
        for table_name, predicate, label in reset_slices
    )
    dropped_silver = drop_rebuildable_schema_objects(SILVER_SCHEMA)
    dropped_gold = drop_rebuildable_schema_objects(
        GOLD_SCHEMA, preserved_objects=("cfg_placement_urgency_rule",)
    )
    print(
        f"RESET ALL complete: cleared {cleared_rows:,} archive monitoring rows; "
        f"dropped {len(dropped_silver):,} Silver and {len(dropped_gold):,} Gold objects"
    )
    print(
        "RESET ALL preserved Bronze/archive data and preserved configuration catalogues: "
        "schema contract, DQ rules, file configuration, Gold lineage mapping and urgency rules."
    )


if RESET_ALL_ARCHIVE_PROCESSING:
    reset_all_archive_processing()


if PROCESS_ONLY and (RESET_MONTH_MONITORING or CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY):
    expected_confirmation = f"RESET {PROCESS_ONLY}"
    if CONFIRM_PROCESS_ONLY_RESET != expected_confirmation:
        raise ValueError(
            f"Reset not executed. Set CONFIRM_PROCESS_ONLY_RESET exactly to {expected_confirmation!r}."
        )
    selected_snapshot = month_end_dates[0]
    if RESET_MONTH_MONITORING:
        spark.sql(
            "DELETE FROM monitoring.cfg_month_end_gold_run "
            f"WHERE snapshot_date = DATE '{selected_snapshot.isoformat()}'"
        )
        spark.sql(
            "DELETE FROM monitoring.cfg_silver_export_load "
            "WHERE source_kind = 'ARCHIVE_MONTH_END' "
            f"AND DATE(export_date) = DATE '{selected_snapshot.isoformat()}'"
        )
        print(f"RESET monitoring state for {selected_snapshot}")
    elif CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY:
        # Retain the audit history, but flag the selected archive month as
        # deliberately reloaded. This prevents a prior SUCCESS state from
        # skipping the Silver, DQ and Gold rebuild after targets are cleared.
        spark.sql(
            "UPDATE monitoring.cfg_month_end_gold_run "
            "SET reload = true, last_updated_at = current_timestamp() "
            f"WHERE snapshot_date = DATE '{selected_snapshot.isoformat()}'"
        )
        spark.sql(
            "UPDATE monitoring.cfg_silver_export_load "
            "SET reload = true, last_updated_at = current_timestamp() "
            "WHERE source_kind = 'ARCHIVE_MONTH_END' "
            f"AND DATE(export_date) = DATE '{selected_snapshot.isoformat()}'"
        )
        print(f"FLAGGED monitoring state for reload: {selected_snapshot}")
    if CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY:
        for target_table in sorted({info["target_table"] for info in source_tables}):
            spark.sql(f"DROP TABLE IF EXISTS {target_table}")
        print(f"RESET Silver targets for {PROCESS_ONLY}")

for snapshot_date in month_end_dates:
    existing = month_end_record(snapshot_date)
    stale_targets = [
        info["target_table"] for info in source_tables
        if target_requires_refresh(info["target_table"], info["schema_cols"])
    ]
    if existing and existing["status"] == "SUCCESS" and not existing["reload"] and not stale_targets:
        skipped_months += 1
        print(f"SKIP MONTH {snapshot_date}: Silver, DQ and Gold already successful")
        continue
    if stale_targets:
        print(f"REFRESH MONTH {snapshot_date}: stale Silver targets {stale_targets}")

    print(f"\n=== PROCESSING CANONICAL MONTH END {snapshot_date} ===")
    update_month_end(snapshot_date, "RUNNING")
    month_errors = []

    # Rebuild every Silver table for a month being retried. Individual
    # table audit rows cannot be used to skip here because shared Silver
    # may currently contain a later month's state.
    for table_info in source_tables:
        try:
            rows_read, rows_written, _ = materialise_table_month_end(
                table_info, snapshot_date
            )
            ok += 1
            total_read += rows_read
            total_written += rows_written
        except Exception as exc:
            message = str(exc)[:4000]
            failed += 1
            month_errors.append(f"{table_info['source_table']}: {message}")
            print(f"FAILED {table_info['source_table']} @ {snapshot_date}: {message}")

    if month_errors:
        message = " | ".join(month_errors)[:4000]
        errors.append(f"{snapshot_date}: {message}")
        update_month_end(snapshot_date, "FAILED", error_message=message)
        if FAIL_ON_TABLE_ERROR:
            break
        continue

    if RUN_GOLD_AT_MONTH_END:
        try:
            dq_result = mssparkutils.notebook.run(
                DQ_NOTEBOOK_NAME, NOTEBOOK_TIMEOUT_SECONDS,
                {"DEFAULT_LOCATION_CITY": DEFAULT_LOCATION_CITY, "JOB_RUN_ID": JOB_RUN_ID},
            )
            gold_result = mssparkutils.notebook.run(
                GOLD_NOTEBOOK_NAME,
                NOTEBOOK_TIMEOUT_SECONDS,
                {"AS_OF_DATE": snapshot_date.isoformat()},
            )
            # Dimensions are current-state tables. Rebuilding them for every
            # historical month adds repeated work and leaves only the final
            # result, so publish them once after the final selected batch.
            is_final_month_end_batch = snapshot_date == month_end_dates[-1]
            dimensions_result = None
            if RUN_GOLD_DIMENSIONS_AT_MONTH_END and is_final_month_end_batch:
                dimensions_result = mssparkutils.notebook.run(
                    GOLD_DIMENSIONS_NOTEBOOK_NAME,
                    NOTEBOOK_TIMEOUT_SECONDS,
                    {"AS_OF_DATE": snapshot_date.isoformat()},
                )
            elif RUN_GOLD_DIMENSIONS_AT_MONTH_END:
                print(
                    f"Gold dimensions deferred until final batch {month_end_dates[-1]}; current batch is {snapshot_date}"
                )
            gold_status = str(gold_result)
            if dimensions_result is not None:
                gold_status += f"; dimensions={dimensions_result}"
            elif RUN_GOLD_DIMENSIONS_AT_MONTH_END:
                gold_status += "; dimensions=deferred until final batch"
            update_month_end(
                snapshot_date, "SUCCESS", str(dq_result), gold_status
            )
            completed_steps = (
                "DQ, Gold and dimensions"
                if dimensions_result is not None else "DQ and Gold"
            )
            print(f"MONTH END COMPLETE {snapshot_date}: {completed_steps} succeeded")
        except Exception as exc:
            message = str(exc)[:4000]
            errors.append(f"{snapshot_date} DQ/Gold: {message}")
            update_month_end(snapshot_date, "FAILED", error_message=message)
            print(f"MONTH END FAILED {snapshot_date}: {message}")
            if FAIL_ON_TABLE_ERROR:
                break
    else:
        update_month_end(snapshot_date, "SUCCESS")

status = "FAILED" if errors else "SUCCESS"
error_text = " | ".join(errors)[:4000] if errors else None
error_sql = "NULL" if error_text is None else "'" + error_text.replace("'", "''") + "'"
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run
SET ended_at=current_timestamp(), status='{status}',
    tables_succeeded={ok}, tables_failed={failed},
    rows_read={total_read}, rows_written={total_written},
    error_message={error_sql}
WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='02a_archive_silver'""")
print(
    f"Archive month-end run {RUN_ID}: {status}; "
    f"loaded={ok}, skipped_months={skipped_months}, "
    f"skipped_contracts={skipped_contracts}, failed={failed}"
)
if errors and FAIL_ON_TABLE_ERROR:
    raise RuntimeError(error_text)
```

<a id="python-03-silver-business-rules-py-119"></a>
## 03_silver_business_rules.py:119

Source: [project X/03_silver_business_rules.py:119](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L119).

```python
append_rows("monitoring.cfg_pipeline_run", [(PIPELINE_RUN_ID, "03_silver_business_rules", "SILVER", f"LATEST_{DQ_RUN_MODE}",
    STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string")
log_step("Pipeline run row registered")
```

<a id="python-03-silver-business-rules-py-133"></a>
## 03_silver_business_rules.py:133

Source: [project X/03_silver_business_rules.py:133](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L133).

```python
schema_df = spark.table("monitoring.cfg_schema_contract_column")
custom_rules_df = spark.table("monitoring.cfg_data_quality_rule")
if schema_df.rdd.isEmpty() or custom_rules_df.rdd.isEmpty():
    raise ValueError("Configuration tables are empty; run setup CSV bootstrap first")
schema_rows = [r.asDict() for r in schema_df.collect()]
rules = []

# Contract-generated PK completeness and table-level uniqueness checks.
primary_keys = {}
for row in schema_rows:
    if (row.get("is_primary_key") or "").upper() == "YES":
        primary_keys.setdefault(row["table_name"], []).append(row["column_name"])
        base = {"source_schema": SILVER_SCHEMA, "table_name": row["table_name"],
                "column_name": row["column_name"], "severity": "CRITICAL", "active": "true"}
        rules.append({**base, "rule_id": f"PK_NOT_NULL_{row['table_name']}_{row['column_name']}", "rule_type": "NOT_NULL"})
for table_name, key_columns in primary_keys.items():
    rules.append({"source_schema": SILVER_SCHEMA, "table_name": table_name,
        "column_name": ",".join(key_columns), "severity": "CRITICAL", "active": "true",
        "rule_id": f"PK_UNIQUE_{table_name}", "rule_type": "UNIQUE"})

# Contract-generated referential-integrity checks.
for row in schema_rows:
    if row.get("referenced_table") and row.get("referenced_column"):
        rules.append({
            "rule_id": f"FK_{row['table_name']}_{row['column_name']}",
            "active": "true", "severity": "ERROR", "rule_type": "REFERENTIAL_INTEGRITY",
            "source_schema": SILVER_SCHEMA, "table_name": row["table_name"],
            "column_name": row["column_name"], "referenced_schema": SILVER_SCHEMA,
            "referenced_table": row["referenced_table"], "referenced_column": row["referenced_column"],
        })

rules.extend(r.asDict() for r in custom_rules_df.where("lower(active) = 'true'").collect())
# Derived referral checks run after Cell 8 materialises the current Silver
# enrichment, rather than validating a prior run's table state.
derived_dq_rules = [
    rule for rule in rules
    if rule.get("table_name") == "referral_enrichment"
]
validation_rules = [
    rule for rule in rules
    if rule.get("table_name") != "referral_enrichment"
]
if RUN_ESSENTIAL_DQ:
    # The weekday path retains every blocking integrity rule. Full
    # referential, date-order and advisory business checks run in THOROUGH
    # mode, normally scheduled for the weekend.
    validation_rules = [
        rule for rule in validation_rules
        if (rule.get("severity") or "").upper() == "CRITICAL"
    ]
    derived_dq_rules = [
        rule for rule in derived_dq_rules
        if (rule.get("severity") or "").upper() == "CRITICAL"
    ]
rule_fields = ["rule_id", "active", "severity", "rule_type", "source_schema", "table_name",
    "column_name", "referenced_schema", "referenced_table", "referenced_column",
    "operator", "rule_value", "description"]
normalised_rule_rows = [tuple(rule.get(field) for field in rule_fields) + (datetime.now(timezone.utc),) for rule in rules]
spark.createDataFrame(normalised_rule_rows,
    "rule_id string,active string,severity string,rule_type string,source_schema string,table_name string,column_name string,referenced_schema string,referenced_table string,referenced_column string,operator string,rule_value string,description string,loaded_at timestamp") \
    .write.format("delta").mode("overwrite").option("overwriteSchema", "true") \
    .saveAsTable("monitoring.cfg_data_quality_rule")
scheduled_rule_count = len(validation_rules) + len(derived_dq_rules)
print(f"Prepared {len(rules):,} data-quality rules; {DQ_RUN_MODE} mode will run {scheduled_rule_count:,}")
log_step(f"Prepared {len(rules):,} data-quality rules; DQ mode={DQ_RUN_MODE}; scheduled={scheduled_rule_count:,}")
```

<a id="python-03-silver-business-rules-py-208"></a>
## 03_silver_business_rules.py:208

Source: [project X/03_silver_business_rules.py:208](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L208).

```python
result_schema = "run_id string,rule_id string,severity string,rule_type string,source_table string,column_name string,status string,failed_row_count long,checked_row_count long,failure_percentage double,sample_key_json string,checked_at timestamp,message string,job_run_id string"
reject_schema = "run_id string,rule_id string,source_table string,business_key_json string,rejection_reason string,rejected_at timestamp,job_run_id string"
reference_schema = "run_id string,rule_id string,child_table string,child_column string,child_key string,parent_table string,parent_column string,detected_at timestamp,job_run_id string"
result_rows = []
critical_failures = []

# LIVE-ETL-003: scan each Silver table once per run. Rules are grouped by
# source table; the row count is computed once per table and multi-rule
# tables are cached for the duration of their checks.
table_rule_counts = {}
for rule in validation_rules:
    table_rule_counts[rule["table_name"]] = table_rule_counts.get(rule["table_name"], 0) + 1
checked_counts = {}
cached_frames = {}


def log_rule(rule_id, status, detail, rule_started):
    elapsed = (datetime.now(timezone.utc) - rule_started).total_seconds()
    print(f"  [{rule_id}] {status}: {detail} (+{elapsed:,.1f}s)")


for rule in validation_rules:
    rule_id = rule["rule_id"]
    rule_type = rule["rule_type"].upper()
    severity = (rule.get("severity") or "ERROR").upper()
    source = silver_table(rule["table_name"])
    column_name = rule["column_name"]
    checked_at = datetime.now(timezone.utc)
    rule_started = datetime.now(timezone.utc)
    try:
        if not spark.catalog.tableExists(source):
            result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, 0, 0.0, None, checked_at, "Missing Silver source table"))
            log_rule(rule_id, "SKIPPED", "missing Silver source table", rule_started)
            continue
        frame = spark.table(source)
        if table_rule_counts.get(rule["table_name"], 0) > 1 and source not in cached_frames:
            frame = frame.cache()
            cached_frames[source] = frame
        missing_columns = [c.strip() for c in column_name.split(",") if c.strip() and c.strip() not in frame.columns]
        if missing_columns:
            result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, 0, 0.0, None, checked_at, f"Missing Silver column(s): {missing_columns}"))
            log_rule(rule_id, "SKIPPED", f"missing Silver column(s): {missing_columns}", rule_started)
            continue
        checked = checked_counts.get(source)
        if checked is None:
            checked = frame.count()
            checked_counts[source] = checked
        failed_frame = None
        failed = 0

        if rule_type == "NOT_NULL":
            failed_frame = frame.where(F.col(qident(column_name)).isNull())
            failed = failed_frame.count()
        elif rule_type == "UNIQUE":
            key_columns = [name.strip() for name in column_name.split(",") if name.strip()]
            non_null = frame
            for key_column in key_columns:
                non_null = non_null.where(F.col(qident(key_column)).isNotNull())
            duplicates = non_null.groupBy(*key_columns).count().where("count > 1")
            failed = duplicates.select(F.sum(F.col("count") - 1).alias("failed")).first()["failed"] or 0
            failed_frame = duplicates.select(F.to_json(F.struct(*[F.col(qident(c)) for c in key_columns])).alias("_key"))
        elif rule_type == "REFERENTIAL_INTEGRITY":
            parent = silver_table(rule["referenced_table"])
            if not spark.catalog.tableExists(parent):
                result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, checked, 0.0, None, checked_at, "Missing Silver parent table"))
                log_rule(rule_id, "SKIPPED", "missing Silver parent table", rule_started)
                continue
            parent_frame = spark.table(parent)
            parent_column = rule["referenced_column"]
            if parent_column not in parent_frame.columns:
                result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "SKIPPED", 0, checked, 0.0, None, checked_at, f"Missing Silver parent column: {parent_column}"))
                log_rule(rule_id, "SKIPPED", f"missing Silver parent column: {parent_column}", rule_started)
                continue
            parent_frame = parent_frame.select(F.trim(F.col(qident(parent_column)).cast("string")).alias("_parent_key")).distinct()
            failed_frame = (frame.where(F.col(qident(column_name)).isNotNull())
                .select(F.trim(F.col(qident(column_name)).cast("string")).alias("_key")).distinct()
                .join(parent_frame, F.col("_key") == F.col("_parent_key"), "left_anti"))
            failed = failed_frame.count()
            refs = [(RUN_ID, rule_id, source, column_name, r["_key"], parent,
                rule["referenced_column"], checked_at) for r in failed_frame.limit(MAX_REJECT_REFERENCES_PER_RULE).collect()]
            append_rows("monitoring.cfg_referential_exception", [tuple(row) + (JOB_RUN_ID or None,) for row in refs], reference_schema)
        elif rule_type == "DATE_ORDER":
            other = rule["referenced_column"]
            operator = (rule.get("operator") or "<=").strip()
            left = F.col(qident(column_name))
            right = F.col(qident(other))
            if operator == "<=":
                invalid_order = left > right
            elif operator == ">=":
                invalid_order = left < right
            else:
                raise ValueError(
                    f"Unsupported DATE_ORDER operator: {operator}. Use <= or >="
                )
            failed_frame = frame.where(
                left.isNotNull() & right.isNotNull() & invalid_order
            )
            failed = failed_frame.count()
        elif rule_type == "CONDITIONAL_NOT_NULL":
            other = rule["referenced_column"]
            failed_frame = frame.where(
                F.col(qident(other)).isNotNull()
                & F.col(qident(column_name)).isNull()
            )
            failed = failed_frame.count()
        elif rule_type == "NON_NEGATIVE":
            failed_frame = frame.where(F.col(qident(column_name)) < F.lit(0))
            failed = failed_frame.count()
        else:
            raise ValueError(f"Unsupported rule type: {rule_type}")

        status = "PASS" if failed == 0 else "FAIL"
        pct = (failed / checked * 100.0) if checked else 0.0
        sample_key = None
        if failed_frame is not None and failed:
            key_column = "_key" if "_key" in failed_frame.columns else column_name.split(",")[0].strip()
            samples = failed_frame.select(F.col(qident(key_column)).cast("string").alias("key")) \
                .limit(MAX_REJECT_REFERENCES_PER_RULE).collect()
            sample_key = samples[0]["key"] if samples else None
            rejects = [(RUN_ID, rule_id, source, '{"key":"' + str(r["key"]).replace('"', '\\"') + '"}',
                rule.get("description") or rule_type, checked_at) for r in samples]
            append_rows("monitoring.cfg_rejected_row", [tuple(row) + (JOB_RUN_ID or None,) for row in rejects], reject_schema)
        result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, status,
            int(failed), int(checked), float(pct), sample_key, checked_at, rule.get("description")))
        log_rule(rule_id, status, f"{int(failed):,}/{int(checked):,} failed", rule_started)
        if status == "FAIL" and severity == "CRITICAL":
            critical_failures.append(rule_id)
    except Exception as exc:
        result_rows.append((RUN_ID, rule_id, severity, rule_type, source, column_name, "ERROR",
            0, 0, 0.0, None, checked_at, str(exc)[:2000]))
        log_rule(rule_id, "ERROR", str(exc)[:200], rule_started)
        if severity == "CRITICAL":
            critical_failures.append(rule_id)

for cached_frame in cached_frames.values():
    cached_frame.unpersist()

append_rows("monitoring.cfg_data_quality_result", [tuple(row) + (JOB_RUN_ID or None,) for row in result_rows], result_schema)
failed_checks = sum(1 for row in result_rows if row[6] in ("FAIL", "ERROR"))
skipped_checks = sum(1 for row in result_rows if row[6] == "SKIPPED")
run_status = "FAILED" if critical_failures else ("SUCCESS_WITH_WARNINGS" if failed_checks else "SUCCESS")
spark.sql(f"""UPDATE monitoring.cfg_pipeline_run SET ended_at=current_timestamp(), status='{run_status}',
tables_succeeded={len(result_rows) - failed_checks}, tables_failed={failed_checks},
rows_read=0, rows_written={len(result_rows)}, error_message=NULL WHERE run_id='{PIPELINE_RUN_ID}' AND pipeline_name='03_silver_business_rules'""")
if critical_failures and FAIL_ON_CRITICAL:
    raise RuntimeError(f"Critical DQ failures: {critical_failures[:20]}")
print(f"DQ run {RUN_ID}: {len(result_rows)} checks; {len(critical_failures)} critical failures; {skipped_checks} skipped")
log_step(f"Main DQ pass complete: {len(result_rows)} checks, {len(critical_failures)} critical failures")
```

<a id="python-03-silver-business-rules-py-366"></a>
## 03_silver_business_rules.py:366

Source: [project X/03_silver_business_rules.py:366](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L366).

```python
# SI-008 to SI-012 — Silver materialisations used by reporting.
# These are deterministic derived tables, not source-contract entities.
from pyspark.sql.types import DateType, IntegerType, StringType, StructField, StructType

def replace_silver_materialisation(frame, table_name):
    (frame.withColumn("job_run_id", F.lit(JOB_RUN_ID).cast("string"))
        .write.format("delta").mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(f"{SILVER_SCHEMA}.{table_name}"))


def classify_referral_location(value, default_city="Birmingham", city_names=()):
    """Conservative local place-name extraction; never geocode referral free text."""
    import re

    default_city = str(default_city or "").strip()
    if not default_city:
        raise ValueError("DEFAULT_LOCATION_CITY must be a non-empty city/locality")
    text = re.sub(r"\s+", " ", str(value or "")).strip().casefold()
    if not text:
        return default_city, "DEFAULT_MISSING", True, False
    # A preference can describe prohibited locations, not a positive origin.
    if re.search(r"\b(outside|out of|avoid\w*|not|no|away from|exclud\w*|except)\b", text):
        return default_city, "DEFAULT_REVIEW_EXCLUSION", True, True
    known_places = (
        "Birmingham", "Coventry", "Wolverhampton", "Walsall", "Dudley", "Solihull",
        "Nottingham", "Leicester", "London", "Liverpool", "Manchester", "Sheffield",
        "Leeds", "Worcester", "Oxford", "Bristol", "Derby", "Stoke-on-Trent",
    )
    aliases = {city.strip().casefold(): city.strip() for city in (*known_places, *city_names, default_city)
               if city and city.strip()}
    aliases.update({"bham": "Birmingham", "b'ham": "Birmingham"})
    matches = {city for alias, city in aliases.items()
               if re.search(r"(?<!\w)" + re.escape(alias) + r"(?!\w)", text)}
    if len(matches) > 1 or re.search(r"\b(or|either)\b|/", text):
        return default_city, "DEFAULT_REVIEW_MULTIPLE", True, True
    if len(matches) == 1:
        return next(iter(matches)), "CITY_MATCH", False, False
    return default_city, "DEFAULT_REVIEW_UNRECOGNISED", True, True


def approved_location_reference():
    """Validate local reference keys before any join; duplicates must not fan out facts."""
    table = "monitoring.cfg_location_coordinate"
    schema = ("location_type string, location_key string, latitude double, longitude double, "
              "reference_source string, reference_version string")
    frame = spark.table(table) if spark.catalog.tableExists(table) else spark.createDataFrame([], schema)
    frame = (frame.selectExpr(*[field.split()[0] for field in schema.split(", ")])
        .withColumn("location_type", F.upper(F.trim("location_type")))
        .withColumn("location_key", F.trim("location_key"))
        .withColumn("_key", F.when(F.col("location_type") == "POSTCODE",
            F.regexp_replace(F.upper("location_key"), r"\s+", ""))
            .otherwise(F.lower("location_key")))
        .dropDuplicates())
    invalid = (
        F.col("location_type").isNull() | ~F.col("location_type").isin("CITY", "POSTCODE")
        | F.col("_key").isNull() | (F.length("_key") == 0)
        | (F.col("latitude").isNull() != F.col("longitude").isNull())
        | F.isnan("latitude") | F.isnan("longitude")
        | (F.abs("latitude") > 90) | (F.abs("longitude") > 180)
        | (F.col("latitude").isNotNull() & (
            F.col("reference_source").isNull() | (F.length(F.trim("reference_source")) == 0)
            | F.col("reference_version").isNull() | (F.length(F.trim("reference_version")) == 0)))
    )
    if frame.where(invalid).limit(1).count():
        raise ValueError(f"{table}: invalid type/key/coordinate/provenance; correct approved reference data")
    if frame.groupBy("location_type", "_key").count().where("count > 1").limit(1).count():
        raise ValueError(f"{table}: conflicting duplicate normalised keys; retain one approved row per key")
    return frame


def latest_location_source(table, key, value):
    from pyspark.sql.window import Window

    frame = spark.table(table)
    date_columns = [name for name in ("referral_modified_date", "referral_created_date", "export_date")
                    if name in frame.columns]
    ordering = [F.coalesce(*[F.col(name).cast("timestamp") for name in date_columns]).desc_nulls_last(),
                F.col("export_date").desc_nulls_last(), F.col(value).desc_nulls_last()]
    return (frame.withColumn("_location_rank", F.row_number().over(Window.partitionBy(key).orderBy(*ordering)))
        .where("_location_rank = 1").select(key, value, "export_date"))


# SLV-001: derived tables leave the schema-conformed source entities unchanged.
# Empty reference data is valid: the output remains usable with NULL coordinates.
geo_reference = approved_location_reference()
city_reference = geo_reference.where("location_type = 'CITY'")
city_rows = city_reference.select("location_key").limit(10001).collect()
if len(city_rows) > 10000:
    raise ValueError("City reference exceeds the 10,000-name local matching limit")
city_names = tuple(row.location_key for row in city_rows)
location_classifier = F.udf(
    lambda value: classify_referral_location(value, DEFAULT_LOCATION_CITY, city_names),
    "location string, location_match_status string, location_is_default boolean, location_requires_review boolean",
)
referral_locations = (latest_location_source(f"{SILVER_SCHEMA}.referral", "referral_id", "location_preference_details")
    .withColumn("_location", location_classifier("location_preference_details"))
    .select("referral_id", "export_date", "_location.*"))
referral_locations = (referral_locations.alias("r").join(city_reference.alias("g"),
    F.lower(F.col("r.location")) == F.col("g._key"), "left")
    .select("r.*", F.col("g.latitude").alias("location_latitude"),
        F.col("g.longitude").alias("location_longitude"),
        F.col("g.reference_source").alias("location_reference_source"),
        F.col("g.reference_version").alias("location_reference_version")))
replace_silver_materialisation(referral_locations, "referral_location")

home_locations = (latest_location_source(f"{SILVER_SCHEMA}.provider_home", "provider_home_id", "postcode")
    .withColumn("postcode_normalized", F.regexp_replace(F.upper(F.trim("postcode")), r"\s+", "")))
home_locations = (home_locations.alias("h").join(
    geo_reference.where("location_type = 'POSTCODE'").alias("g"),
    F.col("h.postcode_normalized") == F.col("g._key"), "left")
    .select("h.provider_home_id", "h.export_date", "h.postcode_normalized",
        F.col("g.latitude").alias("home_latitude"), F.col("g.longitude").alias("home_longitude"),
        F.col("g.reference_source").alias("home_reference_source"),
        F.col("g.reference_version").alias("home_reference_version")))
replace_silver_materialisation(home_locations, "provider_home_location")
log_step("Local city/postcode enrichment complete; no referral text sent to external services")


# SI-008: stable age-band axis.
replace_silver_materialisation(
    spark.createDataFrame(
        [("0-7 days", 1), ("8-14 days", 2), ("15-30 days", 3), ("31+ days", 4)],
        "age_band string, sort_order int",
    ),
    "age_band",
)

# SI-009 and SI-010: disconnected presentation axes.
replace_silver_materialisation(
    spark.createDataFrame(
        [("Residential Homes",), ("Supported Accommodation Homes",), ("Fostering Providers",)],
        "display_type string",
    ),
    "directory_summary_axis",
)
replace_silver_materialisation(
    spark.createDataFrame([("Fostering Providers",)], "display_type string"),
    "fostering_axis",
)

# SI-011: one closure-reason bucket per referral, using only available Silver
# referral-provider and offer fields. This replaces the former Gold/DAX-only
# calculated table and remains empty, rather than failing, when those inputs
# are not present for a historical month.
if (spark.catalog.tableExists("silver.referral_provider")
        and spark.catalog.tableExists("silver.offer")):
    closure_summary = spark.sql("""
        SELECT rp.referral_id,
          MAX(CASE
            WHEN LOWER(CAST(COALESCE(rp.is_cancelled, false) AS STRING)) IN ('true', '1', 'yes')
              THEN 'Cancelled'
            WHEN LOWER(CAST(COALESCE(rp.is_declined, false) AS STRING)) IN ('true', '1', 'yes')
              OR LOWER(COALESCE(o.offer_status, '')) IN ('declined', 'rejected')
              THEN 'Declined'
            WHEN LOWER(CAST(COALESCE(rp.is_closed, false) AS STRING)) IN ('true', '1', 'yes')
              OR LOWER(COALESCE(o.offer_status, '')) IN ('closed', 'withdrawn')
              THEN 'Closed/Withdrawn'
            WHEN COALESCE(o.decline_reason_other, o.decline_reason, o.withdraw_reason) IS NOT NULL
              THEN 'Other'
            ELSE NULL
          END) AS closed_referral_reason_bucket
        FROM silver.referral_provider rp
        LEFT JOIN silver.offer o
          ON rp.referral_provider_id = o.referral_provider_id
        GROUP BY rp.referral_id
    """)
else:
    closure_summary = spark.createDataFrame(
        [], "referral_id string, closed_referral_reason_bucket string"
    )
replace_silver_materialisation(closure_summary, "referral_closure_reason_summary")
log_step("Materialised referral_closure_reason_summary")

# PERF-001: scan provider assignments and offers once, then materialise the
# referral-grain values reused by referral_enrichment. Keeping the write at
# the rollup grain avoids recomputing the same join for counts, first-seen
# dates and engagement flags inside the enrichment query.
provider_rollup_schema = (
    "referral_id string, cnt_offer_made long, unique_homes_offered long, "
    "provider_assignment_count long, first_offer_date timestamp, "
    "offer_accepted_date timestamp, first_provider_seen_date timestamp, "
    "has_live_provider boolean, has_engaged_provider boolean"
)
if (spark.catalog.tableExists("silver.referral_provider")
        and spark.catalog.tableExists("silver.offer")):
    referral_provider_rollup = spark.sql("""
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          COUNT(DISTINCT o.offer_id) AS cnt_offer_made,
          COUNT(DISTINCT o.provider_home_id) AS unique_homes_offered,
          COUNT(DISTINCT rp.provider_id) AS provider_assignment_count,
          MIN(CAST(o.offer_date AS TIMESTAMP)) AS first_offer_date,
          MIN(CASE WHEN LOWER(COALESCE(o.offer_status, '')) IN
            ('accepted', 'approved', 'selected', 'offer_successful')
            THEN CAST(COALESCE(o.last_modified_date, o.offer_date) AS TIMESTAMP)
          END) AS offer_accepted_date,
          MIN(CAST(rp.export_date AS TIMESTAMP)) AS first_provider_seen_date,
          MAX(CASE WHEN NOT COALESCE(rp.is_closed, false)
              AND NOT COALESCE(rp.is_declined, false)
              AND NOT COALESCE(rp.is_excluded, false)
              AND NOT COALESCE(rp.is_cancelled, false)
            THEN 1 ELSE 0 END) = 1 AS has_live_provider,
          MAX(CASE WHEN NOT COALESCE(rp.is_cancelled, false)
              AND NOT COALESCE(rp.is_closed, false)
              AND NOT COALESCE(rp.is_excluded, false)
            THEN 1 ELSE 0 END) = 1 AS has_engaged_provider
        FROM silver.referral_provider rp
        LEFT JOIN silver.offer o
          ON rp.referral_provider_id = o.referral_provider_id
        GROUP BY rp.referral_id
    """)
else:
    referral_provider_rollup = spark.createDataFrame([], provider_rollup_schema)
replace_silver_materialisation(referral_provider_rollup, "referral_provider_rollup")
log_step("Materialised referral_provider_rollup")

# SI-018/SI-019: referral-level enrichment is intentionally a separate
# derived Silver relation. The source-conformed silver.referral contract
# remains immutable; this relation makes cross-table KPI logic reusable by
# Gold, snapshots, and ad-hoc reporting.
enrichment_schema = (
    "referral_id string, referral_created_date timestamp, cnt_offer_made long, "
    "unique_homes_offered long, provider_assignment_count long, is_spot boolean, "
    "estimated_weekly_cost decimal(19,2), "
    "first_action_date timestamp, first_offer_date timestamp, offer_accepted_date timestamp, "
    "ipa_issued_date timestamp, referral_closed_date timestamp, last_activity_date timestamp, "
    "first_provider_seen_date timestamp, "
    "is_not_seen_by_providers boolean, ipa_placement_admission_date timestamp, "
    "ipa_2_signatures boolean, ipa_last_signature_date timestamp, "
    "ipa_due_diligence_min_review_date timestamp, "
    "is_open boolean, is_awaiting_offer boolean"
)
if (spark.catalog.tableExists("silver.referral")
        and spark.catalog.tableExists("silver.referral_provider")
        and spark.catalog.tableExists("silver.offer")
        and spark.catalog.tableExists("silver.ipa")):
    documents_cte = (
        """
        ipa_documents AS (
          SELECT i.referral_id,
            MIN(CAST(d.next_review_date AS TIMESTAMP))
              AS ipa_due_diligence_min_review_date
          FROM silver.ipa i
          INNER JOIN silver.offer o ON i.offer_id = o.offer_id
          INNER JOIN silver.provider_submission_docs d
            ON d.home_id = o.provider_home_id
          WHERE i.placement_admission_date IS NOT NULL
            AND d.next_review_date IS NOT NULL
            AND d.next_review_date > i.placement_admission_date
          GROUP BY i.referral_id
        )
        """
        if spark.catalog.tableExists("silver.provider_submission_docs")
        else "ipa_documents AS (SELECT CAST(NULL AS STRING) AS referral_id, CAST(NULL AS TIMESTAMP) AS ipa_due_diligence_min_review_date WHERE 1 = 0)"
    )
    referral_enrichment = spark.sql(f"""
        WITH activity_candidates AS (
          SELECT CAST(referral_id AS STRING) AS referral_id,
            CAST(referral_created_date AS TIMESTAMP) AS activity_timestamp,
            'ReferralCreated' AS activity_type
          FROM silver.referral WHERE referral_created_date IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(referral_modified_date AS TIMESTAMP),
            'ReferralModified'
          FROM silver.referral
          WHERE referral_modified_date IS NOT NULL
            AND referral_modified_date > referral_created_date
          UNION ALL
          SELECT CAST(rp.referral_id AS STRING), CAST(o.offer_date AS TIMESTAMP),
            'OfferSubmitted'
          FROM silver.offer o INNER JOIN silver.referral_provider rp
            ON o.referral_provider_id = rp.referral_provider_id
          WHERE o.offer_date IS NOT NULL
          UNION ALL
          SELECT CAST(rp.referral_id AS STRING), CAST(o.last_modified_date AS TIMESTAMP),
            'OfferUpdated'
          FROM silver.offer o INNER JOIN silver.referral_provider rp
            ON o.referral_provider_id = rp.referral_provider_id
          WHERE o.last_modified_date IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(created_datetime AS TIMESTAMP),
            'IPACreated'
          FROM silver.ipa WHERE created_datetime IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(updated_datetime AS TIMESTAMP),
            'IPAUpdated'
          FROM silver.ipa WHERE updated_datetime IS NOT NULL
          UNION ALL
          SELECT CAST(referral_id AS STRING), CAST(placement_admission_date AS TIMESTAMP),
            'IPAAdmission'
          FROM silver.ipa WHERE placement_admission_date IS NOT NULL
        ),
        activity_rollup AS (
          SELECT referral_id,
            MIN(CASE WHEN activity_type <> 'ReferralCreated' THEN activity_timestamp END)
              AS first_action_date,
            MAX(activity_timestamp) AS last_activity_date
          FROM activity_candidates
          GROUP BY referral_id
        ),
        provider_spot AS (
          -- GLD-014: provider assignment is the authoritative spot signal.
          -- fact_referral is referral-grain, so any spot assignment is spot.
          SELECT CAST(c.referral_id AS STRING) AS referral_id,
            MAX(CASE WHEN COALESCE(CAST(is_spot AS BOOLEAN), false)
              THEN 1 ELSE 0 END) = 1 AS is_spot
          FROM  LH_BCT_WMPP.silver.offer a
            inner join LH_BCT_WMPP.silver.ipa b on a.offer_id=b.offer_id
            inner join LH_BCT_WMPP.silver.referral_provider c on c.referral_provider_id = a.referral_provider_id
          GROUP BY c.referral_id
        ),
        ipa_rollup AS (
          SELECT referral_id, MIN(CAST(created_datetime AS TIMESTAMP))
              AS ipa_issued_date,
            CAST(SUM(costs_total_weekly_fee) AS DECIMAL(19, 2))
              AS estimated_weekly_cost,
            MIN(CAST(placement_admission_date AS TIMESTAMP))
              AS ipa_placement_admission_date,
            MAX(CASE WHEN UPPER(COALESCE(status, '')) = 'SIGNED'
              THEN 1 ELSE 0 END) = 1 AS ipa_2_signatures,
            MAX(GREATEST(
              CAST(signed_datetime_for_local_authority AS TIMESTAMP),
              CAST(signed_datetime_for_provider AS TIMESTAMP),
              CAST(can_sign_date AS TIMESTAMP)
            )) AS ipa_last_signature_date
          FROM silver.ipa
          GROUP BY referral_id
        ),
        latest_export AS (
          SELECT MAX(TO_DATE(export_date)) AS latest_export_date
          FROM silver.referral
        ),
        {documents_cte}
        SELECT CAST(r.referral_id AS STRING) AS referral_id,
          CAST(r.referral_created_date AS TIMESTAMP) AS referral_created_date,
          COALESCE(pr.cnt_offer_made, 0) AS cnt_offer_made,
          COALESCE(pr.unique_homes_offered, 0) AS unique_homes_offered,
          COALESCE(pr.provider_assignment_count, 0) AS provider_assignment_count,
          COALESCE(ps.is_spot, false) AS is_spot,
          i.estimated_weekly_cost,
          a.first_action_date, pr.first_offer_date, pr.offer_accepted_date,
          i.ipa_issued_date,
          CASE WHEN LOWER(COALESCE(r.referral_status, '')) IN
            ('closed', 'cancelled', 'withdrawn', 'completed')
            THEN CAST(COALESCE(r.referral_modified_date, r.export_date) AS TIMESTAMP)
          END AS referral_closed_date,
          a.last_activity_date, pr.first_provider_seen_date,
          pr.referral_id IS NULL AS is_not_seen_by_providers,
          i.ipa_placement_admission_date,
          COALESCE(i.ipa_2_signatures, false) AS ipa_2_signatures,
          i.ipa_last_signature_date,
          d.ipa_due_diligence_min_review_date,
          -- GLD-009: original business rule for the open flag. A referral is
          -- open when its status is OPEN or UNDER_OFFER and it either has a
          -- live provider referral, is under offer, or is still inside its
          -- response-required window (response date on/after the latest
          -- export date).
          CASE WHEN UPPER(COALESCE(r.referral_status, '')) IN ('OPEN', 'UNDER_OFFER')
            AND (
              COALESCE(pr.has_live_provider, false)
              OR UPPER(COALESCE(r.referral_status, '')) = 'UNDER_OFFER'
              OR (
                UPPER(COALESCE(r.referral_status, '')) = 'OPEN'
                AND r.response_required_by_date IS NOT NULL
                AND TO_DATE(r.response_required_by_date) >= le.latest_export_date
              )
            ) THEN TRUE ELSE FALSE END AS is_open,
          -- GLD-011: Active Referrals Awaiting Offers. An OPEN referral that
          -- either has an engaged provider referral (not cancelled, not
          -- closed, not excluded) or is still inside its response-required
          -- window.
          CASE WHEN UPPER(COALESCE(r.referral_status, '')) = 'OPEN'
            AND (
              COALESCE(pr.has_engaged_provider, false)
              OR (
                r.response_required_by_date IS NOT NULL
                AND TO_DATE(r.response_required_by_date) >= le.latest_export_date
              )
            ) THEN TRUE ELSE FALSE END AS is_awaiting_offer
        FROM silver.referral r
        CROSS JOIN latest_export le
        LEFT JOIN silver.referral_provider_rollup pr ON r.referral_id = pr.referral_id
        LEFT JOIN activity_rollup a ON r.referral_id = a.referral_id
        LEFT JOIN provider_spot ps ON r.referral_id = ps.referral_id
        LEFT JOIN ipa_rollup i ON r.referral_id = i.referral_id
        LEFT JOIN ipa_documents d ON r.referral_id = d.referral_id
    """)
else:
    referral_enrichment = spark.createDataFrame([], enrichment_schema)
replace_silver_materialisation(referral_enrichment, "referral_enrichment")
print("Silver referral enrichment ready: offer, provider-observation, IPA-signature, "
      "due-diligence, is_open, is_awaiting_offer, provider-assignment and spot fields")
log_step("Materialised referral_enrichment")

# Run derived checks only after the current enrichment has been written.
# Results use the same monitoring tables as the main DQ pass above.
derived_result_rows = []
derived_critical_failures = []
for rule in derived_dq_rules:
    rule_id = rule["rule_id"]
    rule_type = rule["rule_type"].upper()
    severity = (rule.get("severity") or "ERROR").upper()
    column_name = rule["column_name"]
    checked_at = datetime.now(timezone.utc)
    frame = spark.table(f"{SILVER_SCHEMA}.referral_enrichment")
    try:
        missing = [name.strip() for name in column_name.split(',')
                   if name.strip() not in frame.columns]
        referenced_column = rule.get("referenced_column")
        if referenced_column and referenced_column not in frame.columns:
            missing.append(referenced_column)
        if missing:
            derived_result_rows.append((
                RUN_ID, rule_id, severity, rule_type,
                f"{SILVER_SCHEMA}.referral_enrichment", column_name,
                "SKIPPED", 0, 0, 0.0, None, checked_at,
                f"Missing Silver column(s): {sorted(set(missing))}", JOB_RUN_ID or None,
            ))
            continue
        checked = frame.count()
        target = F.col(qident(column_name))
        failed_frame = None
        if rule_type == "NOT_NULL":
            failed_frame = frame.where(target.isNull())
        elif rule_type == "CONDITIONAL_NOT_NULL":
            failed_frame = frame.where(
                F.col(qident(referenced_column)).isNotNull() & target.isNull()
            )
        elif rule_type == "NON_NEGATIVE":
            failed_frame = frame.where(target < F.lit(0))
        elif rule_type == "UNIQUE":
            key_columns = [name.strip() for name in column_name.split(',') if name.strip()]
            failed_frame = (frame.dropna(subset=key_columns).groupBy(*key_columns)
                .count().where("count > 1"))
        elif rule_type == "DATE_ORDER":
            other = F.col(qident(referenced_column))
            operator = (rule.get("operator") or "<=").strip()
            invalid_order = target > other if operator == "<=" else target < other
            if operator not in {"<=", ">="}:
                raise ValueError(f"Unsupported DATE_ORDER operator: {operator}")
            failed_frame = frame.where(
                target.isNotNull() & other.isNotNull() & invalid_order
            )
        else:
            raise ValueError(f"Unsupported derived DQ rule type: {rule_type}")
        failed = failed_frame.count()
        status = "PASS" if failed == 0 else "FAIL"
        sample = (failed_frame.select(F.col("referral_id").cast("string").alias("key"))
            .limit(MAX_REJECT_REFERENCES_PER_RULE).collect()) if failed else []
        sample_key = sample[0]["key"] if sample else None
        rejects = [(
            RUN_ID, rule_id, f"{SILVER_SCHEMA}.referral_enrichment",
            '{\"referral_id\":\"' + str(row["key"]).replace('\"', '\\\"') + '\"}',
            rule.get("description") or rule_type, checked_at, JOB_RUN_ID or None,
        ) for row in sample]
        append_rows("monitoring.cfg_rejected_row", rejects, reject_schema)
        derived_result_rows.append((
            RUN_ID, rule_id, severity, rule_type,
            f"{SILVER_SCHEMA}.referral_enrichment", column_name, status,
            int(failed), int(checked), (failed / checked * 100.0) if checked else 0.0,
            sample_key, checked_at, rule.get("description"), JOB_RUN_ID or None,
        ))
        if status == "FAIL" and severity == "CRITICAL":
            derived_critical_failures.append(rule_id)
    except Exception as exc:
        derived_result_rows.append((
            RUN_ID, rule_id, severity, rule_type,
            f"{SILVER_SCHEMA}.referral_enrichment", column_name,
            "ERROR", 0, 0, 0.0, None, checked_at, str(exc)[:2000], JOB_RUN_ID or None,
        ))
        if severity == "CRITICAL":
            derived_critical_failures.append(rule_id)
append_rows("monitoring.cfg_data_quality_result", derived_result_rows, result_schema)
derived_failed = sum(1 for row in derived_result_rows if row[6] in ("FAIL", "ERROR"))
if derived_failed:
    spark.sql(f"""
      UPDATE monitoring.cfg_pipeline_run
      SET status = 'SUCCESS_WITH_WARNINGS',
          tables_failed = COALESCE(tables_failed, 0) + {derived_failed}
      WHERE run_id = '{PIPELINE_RUN_ID}' AND pipeline_name = '03_silver_business_rules'
    """)
if derived_critical_failures and FAIL_ON_CRITICAL:
    raise RuntimeError(f"Critical derived DQ failures: {derived_critical_failures[:20]}")
print(f"Derived referral DQ: {len(derived_result_rows)} checks; {derived_failed} failures")
log_step(f"Derived referral DQ complete: {len(derived_result_rows)} checks, {derived_failed} failures")

# SI-013: derived referral lifecycle events. These are not a source-system
# audit log; each event is derived only from timestamps delivered in Silver.
lifecycle_sources = []
if spark.catalog.tableExists("silver.referral"):
    lifecycle_sources.extend([
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'ReferralCreated' AS event_type,
          CAST(referral_created_date AS TIMESTAMP) AS event_timestamp,
          CAST(referral_created_by AS STRING) AS created_by,
          CAST(referral_created_date AS TIMESTAMP) AS created_timestamp,
          CAST(referral_id AS STRING) AS source_record_id,
          'silver.referral' AS source_table
        FROM silver.referral
        WHERE referral_created_date IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'ReferralModified' AS event_type,
          CAST(referral_modified_date AS TIMESTAMP) AS event_timestamp,
          CAST(referral_updated_by AS STRING) AS created_by,
          CAST(referral_modified_date AS TIMESTAMP) AS created_timestamp,
          CAST(referral_id AS STRING) AS source_record_id,
          'silver.referral' AS source_table
        FROM silver.referral
        WHERE referral_modified_date IS NOT NULL
        """,
    ])
if (spark.catalog.tableExists("silver.offer")
        and spark.catalog.tableExists("silver.referral_provider")):
    lifecycle_sources.extend([
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'OfferSubmitted' AS event_type,
          CAST(o.offer_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(o.offer_date AS TIMESTAMP) AS created_timestamp,
          CAST(o.offer_id AS STRING) AS source_record_id,
          'silver.offer' AS source_table
        FROM silver.offer o
        INNER JOIN silver.referral_provider rp
          ON o.referral_provider_id = rp.referral_provider_id
        WHERE o.offer_date IS NOT NULL
        """,
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'OfferUpdated' AS event_type,
          CAST(o.last_modified_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(o.last_modified_date AS TIMESTAMP) AS created_timestamp,
          CAST(o.offer_id AS STRING) AS source_record_id,
          'silver.offer' AS source_table
        FROM silver.offer o
        INNER JOIN silver.referral_provider rp
          ON o.referral_provider_id = rp.referral_provider_id
        WHERE o.last_modified_date IS NOT NULL
        """,
    ])
if (spark.catalog.tableExists("silver.referral_provider_message")
        and spark.catalog.tableExists("silver.referral_provider")):
    lifecycle_sources.append(
        """
        SELECT CAST(rp.referral_id AS STRING) AS referral_id,
          'ProviderMessageSent' AS event_type,
          CAST(m.created_timestamp AS TIMESTAMP) AS event_timestamp,
          CAST(m.created_by AS STRING) AS created_by,
          CAST(m.created_timestamp AS TIMESTAMP) AS created_timestamp,
          CAST(m.message_id AS STRING) AS source_record_id,
          'silver.referral_provider_message' AS source_table
        FROM silver.referral_provider_message m
        INNER JOIN silver.referral_provider rp
          ON m.referral_provider_id = rp.referral_provider_id
        WHERE m.created_timestamp IS NOT NULL
        """
    )

if spark.catalog.tableExists("silver.ipa"):
    lifecycle_sources.extend([
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPACreated' AS event_type,
          CAST(created_datetime AS TIMESTAMP) AS event_timestamp,
          CAST(created_by AS STRING) AS created_by,
          CAST(created_datetime AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE created_datetime IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPAUpdated' AS event_type,
          CAST(updated_datetime AS TIMESTAMP) AS event_timestamp,
          CAST(updated_by AS STRING) AS created_by,
          CAST(updated_datetime AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE updated_datetime IS NOT NULL
        """,
        """
        SELECT CAST(referral_id AS STRING) AS referral_id,
          'IPAAdmission' AS event_type,
          CAST(placement_admission_date AS TIMESTAMP) AS event_timestamp,
          CAST(NULL AS STRING) AS created_by,
          CAST(placement_admission_date AS TIMESTAMP) AS created_timestamp,
          CAST(ipa_id AS STRING) AS source_record_id,
          'silver.ipa' AS source_table
        FROM silver.ipa
        WHERE placement_admission_date IS NOT NULL
        """,
    ])

if lifecycle_sources:
    lifecycle_events = spark.sql(f"""
        WITH raw_events AS ({' UNION ALL '.join(lifecycle_sources)}),
        sequenced AS (
          SELECT referral_id, event_type, event_timestamp, created_by,
            created_timestamp, source_record_id, source_table,
            ROW_NUMBER() OVER (
              PARTITION BY referral_id
              ORDER BY event_timestamp, event_type, source_record_id
            ) AS sequence_number
          FROM raw_events
          WHERE referral_id IS NOT NULL AND event_timestamp IS NOT NULL
        )
        SELECT SHA2(CONCAT_WS('||', referral_id, event_type,
                    CAST(event_timestamp AS STRING), source_record_id), 256) AS event_id,
          referral_id, event_type, event_timestamp, sequence_number,
          created_by, created_timestamp,
          'DERIVED_SILVER' AS event_source, source_table,
          CURRENT_TIMESTAMP() AS event_materialised_at
        FROM sequenced
    """)
else:
    lifecycle_events = spark.createDataFrame(
        [],
        "event_id string, referral_id string, event_type string, event_timestamp timestamp, "
        "sequence_number int, created_by string, created_timestamp timestamp, "
        "event_source string, source_table string, event_materialised_at timestamp",
    )
replace_silver_materialisation(lifecycle_events, "referral_lifecycle_event")
log_step("Materialised referral_lifecycle_event")

# SI-012: one marked calendar covering the dates present in the current Silver
# state. The range is rebuilt idempotently with each Silver run.
date_sources = []
for table_name, date_column in [
    ("referral", "referral_created_date"),
    ("offer", "offer_date"),
    ("ipa", "created_datetime"),
    ("ipa", "placement_admission_date"),
]:
    qualified = f"{SILVER_SCHEMA}.{table_name}"
    if spark.catalog.tableExists(qualified) and date_column in spark.table(qualified).columns:
        date_sources.append(
            f"SELECT TO_DATE(`{date_column}`) AS date_value FROM {qualified} "
            f"WHERE `{date_column}` IS NOT NULL"
        )

if date_sources:
    date_union = " UNION ALL ".join(date_sources)
    date_dimension = spark.sql(f"""
        WITH source_dates AS ({date_union}),
        bounds AS (
          SELECT MIN(date_value) AS min_date, MAX(date_value) AS max_date
          FROM source_dates
        ),
        calendar AS (
          SELECT EXPLODE(SEQUENCE(min_date, max_date, INTERVAL 1 DAY)) AS date
          FROM bounds
          WHERE min_date IS NOT NULL AND max_date IS NOT NULL
        )
        SELECT date,
          YEAR(date) AS year,
          MONTH(date) AS month_number,
          DATE_FORMAT(date, 'MMMM') AS month_name,
          CONCAT('Q', QUARTER(date)) AS quarter,
          DATE_FORMAT(date, 'EEEE') AS day_of_week
        FROM calendar
    """)
else:
    date_dimension = spark.createDataFrame(
        [],
        StructType([
            StructField("date", DateType(), True),
            StructField("year", IntegerType(), True),
            StructField("month_number", IntegerType(), True),
            StructField("month_name", StringType(), True),
            StructField("quarter", StringType(), True),
            StructField("day_of_week", StringType(), True),
        ]),
    )
replace_silver_materialisation(date_dimension, "dim_date")
print("Silver materialisations ready: age_band, directory_summary_axis, "
      "fostering_axis, referral_closure_reason_summary, dim_date")
log_step("All Silver materialisations complete")
```

<a id="python-04-gold-model-py-232"></a>
## 04_gold_model.py:232

Source: [project X/04_gold_model.py:232](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L232).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral AS
WITH referral_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_id
    ORDER BY COALESCE(referral_modified_date, referral_created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral
),
referral_current AS (
  SELECT * FROM referral_history WHERE row_number_current = 1
),
referral_created AS (
  SELECT referral_id, MIN(referral_created_date) AS referral_created_date
  FROM silver.referral GROUP BY referral_id
),
referral_enrichment AS (
  SELECT * FROM silver.referral_enrichment
),
referral_person_history AS (
  SELECT referral_id, CAST(person_id AS STRING) AS person_id,
    NULLIF(TRIM(CAST(source_reference_id AS STRING)), '') AS source_reference_id,
    ROW_NUMBER() OVER (
      PARTITION BY referral_id, person_id
      ORDER BY export_date DESC NULLS LAST, _silver_load_ts DESC NULLS LAST,
               source_reference_id ASC NULLS LAST, child_index ASC NULLS LAST
    ) AS person_version
  FROM silver.referral_person
  WHERE person_id IS NOT NULL
    AND (export_date IS NULL OR TO_DATE(export_date) <= {AS_OF_SQL})
),
referral_person_selected AS (
  -- Preserve the existing MIN(person_id) selection for multi-person referrals.
  -- Rank source versions first so historical exports cannot multiply fact rows.
  SELECT referral_id, person_id, source_reference_id,
    ROW_NUMBER() OVER (PARTITION BY referral_id ORDER BY person_id ASC) AS person_selection
  FROM referral_person_history
  WHERE person_version = 1
),
referral_child AS (
  SELECT referral_id, person_id, source_reference_id
  FROM referral_person_selected WHERE person_selection = 1
),
referral_framework_category AS (
  SELECT referral_id,
    CASE WHEN COUNT(DISTINCT framework_category_id) = 1
      THEN MIN(framework_category_id) END AS framework_category_id,
    COUNT(DISTINCT framework_category_id) AS framework_category_count
  FROM silver.referral_category
  GROUP BY referral_id
),
closure_reason AS (
  SELECT referral_id, closed_referral_reason_bucket AS referral_closure_reason
  FROM silver.referral_closure_reason_summary
),
provider_offer_response AS (
  SELECT referral_provider_id,
    MIN(CAST(offer_date AS TIMESTAMP)) AS first_offer_response_at
  FROM silver.offer
  WHERE offer_date IS NOT NULL AND TO_DATE(offer_date) <= {AS_OF_SQL}
  GROUP BY referral_provider_id
),
provider_reason_response AS (
  SELECT referral_provider_id, MIN(response_at) AS first_reason_response_at
  FROM (
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_cancel_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
    UNION ALL
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_decline_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
  ) reason_event
  GROUP BY referral_provider_id
),
referral_provider_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY COALESCE(modified_date, created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral_provider
  WHERE created_date IS NULL OR TO_DATE(created_date) <= {AS_OF_SQL}
),
referral_provider_current AS (
  SELECT * FROM referral_provider_history WHERE row_number_current = 1
),
provider_assignment_response AS (
  SELECT rp.referral_provider_id, rp.referral_id, rp.provider_id,
    COALESCE(CAST(rp.created_date AS TIMESTAMP), CAST(rp.export_date AS TIMESTAMP)) AS assigned_at,
    CASE
      WHEN offer_response.first_offer_response_at IS NULL
        THEN reason_response.first_reason_response_at
      WHEN reason_response.first_reason_response_at IS NULL
        THEN offer_response.first_offer_response_at
      ELSE LEAST(offer_response.first_offer_response_at, reason_response.first_reason_response_at)
    END AS response_at
  FROM referral_provider_current rp
  LEFT JOIN provider_offer_response offer_response
    ON rp.referral_provider_id = offer_response.referral_provider_id
  LEFT JOIN provider_reason_response reason_response
    ON rp.referral_provider_id = reason_response.referral_provider_id
),
provider_response AS (
  SELECT referral_id,
    COUNT(*) AS journey_assignment_count,
    COUNT(DISTINCT provider_id) AS provider_assignment_count,
    SUM(CASE WHEN response_at IS NOT NULL
      AND (assigned_at IS NULL OR response_at >= assigned_at) THEN 1 ELSE 0 END)
      AS provider_responded_count,
    MIN(CASE WHEN response_at IS NOT NULL
      AND (assigned_at IS NULL OR response_at >= assigned_at) THEN response_at END)
      AS first_provider_response_date
  FROM provider_assignment_response
  GROUP BY referral_id
),
-- Aggregate journey evidence before joining so offers/IPAs cannot multiply
-- referral rows. Source-grain Gold facts are built later, so read Silver.
journey_offer_evidence AS (
  SELECT rp.referral_id,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) IN
      ('accepted', 'approved', 'selected', 'offer_successful')
      THEN 1 ELSE 0 END) AS has_accepted_offer,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) IN
      ('pending', 'submitted', 'offered', 'offer_made', 'offer_pending',
       'under_review', 'under review', 'awaiting', 'awaiting_decision', 'awaiting decision')
      THEN 1 ELSE 0 END) AS has_pending_offer,
    MAX(CASE WHEN LOWER(TRIM(COALESCE(o.offer_status, ''))) NOT IN
      ('accepted', 'approved', 'selected', 'offer_successful',
       'pending', 'submitted', 'offered', 'offer_made', 'offer_pending',
       'under_review', 'under review', 'awaiting', 'awaiting_decision', 'awaiting decision',
       'declined', 'rejected', 'withdrawn', 'closed', 'cancelled', 'canceled',
       'offer_unsuccessful', 'unsuccessful', 'draft')
      THEN 1 ELSE 0 END) AS has_unknown_offer
  FROM silver.offer o
  INNER JOIN referral_provider_current rp
    ON o.referral_provider_id = rp.referral_provider_id
  WHERE o.offer_date IS NULL OR TO_DATE(o.offer_date) <= {AS_OF_SQL}
  GROUP BY rp.referral_id
),
journey_ipa_evidence AS (
  SELECT referral_id,
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_active_ipa,
    -- Both signatures must belong to the same active IPA.
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_signed_active_ipa
  FROM silver.ipa
  WHERE created_datetime IS NULL OR TO_DATE(created_datetime) <= {AS_OF_SQL}
  GROUP BY referral_id
),
base AS (
  SELECT r.referral_id AS referral_id, child.person_id, child.source_reference_id,
    c.referral_created_date,
    category.framework_category_id,
    COALESCE(category.framework_category_count, 0) AS framework_category_count,
    loc.location, loc.location_match_status, loc.location_is_default, loc.location_requires_review,
    CAST(r.export_date AS TIMESTAMP) AS export_date,
    r.required_start_date AS required_placement_date,
    r.response_required_by_date AS response_required_date,
    r.referral_modified_date AS referral_modified_timestamp,
    r.referral_status AS current_status, r.placement_type AS placement_type_required,
    r.is_sibling_placement, r.sibling_count,
    COALESCE(p.journey_assignment_count, 0) AS journey_assignment_count,
    COALESCE(jo.has_accepted_offer, 0) AS has_accepted_offer,
    COALESCE(jo.has_pending_offer, 0) AS has_pending_offer,
    COALESCE(jo.has_unknown_offer, 0) AS has_unknown_offer,
    COALESCE(ji.has_active_ipa, 0) AS has_active_ipa,
    COALESCE(ji.has_signed_active_ipa, 0) AS has_signed_active_ipa,
    -- GLD-014: provider assignment is authoritative; Silver aggregates it
    -- at referral grain so this remains one Gold row per referral.
    COALESCE(x.is_spot, false) AS is_spot,
    x.is_open, x.is_awaiting_offer,
    COALESCE(p.provider_assignment_count, x.provider_assignment_count, 0)
      AS provider_assignment_count,
    COALESCE(p.provider_responded_count, 0) AS provider_responded_count,
    p.first_provider_response_date,
    x.first_action_date, x.first_offer_date,
    x.offer_accepted_date, x.ipa_issued_date,
    x.referral_closed_date,
    closure.referral_closure_reason,
    x.last_activity_date,
    COALESCE(x.cnt_offer_made, 0) AS cnt_offer_made,
    x.first_provider_seen_date,
    x.is_not_seen_by_providers,
    x.ipa_placement_admission_date,
    x.ipa_2_signatures,
    x.ipa_last_signature_date,
    x.ipa_due_diligence_min_review_date,
    COALESCE(x.cnt_offer_made, 0) AS offer_count,
    x.unique_homes_offered,
    x.ipa_placement_admission_date AS planned_placement_start_date,
    x.estimated_weekly_cost,
    CASE
      WHEN r.required_start_date IS NULL THEN 'Unspecified'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 1 THEN 'Critical'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 3 THEN 'High'
      WHEN DATEDIFF(r.required_start_date, TO_DATE(c.referral_created_date)) <= 7 THEN 'Medium'
      ELSE 'Planned'
    END AS placement_urgency_band
  FROM referral_current r
  INNER JOIN referral_created c ON r.referral_id = c.referral_id
  LEFT JOIN referral_child child ON r.referral_id = child.referral_id
  LEFT JOIN closure_reason closure ON r.referral_id = closure.referral_id
  LEFT JOIN referral_enrichment x ON r.referral_id = x.referral_id
  LEFT JOIN provider_response p ON r.referral_id = p.referral_id
  LEFT JOIN journey_offer_evidence jo ON r.referral_id = jo.referral_id
  LEFT JOIN journey_ipa_evidence ji ON r.referral_id = ji.referral_id
  LEFT JOIN referral_framework_category category ON r.referral_id = category.referral_id
  LEFT JOIN silver.referral_location loc ON r.referral_id = loc.referral_id
),
journey_classified AS (
  SELECT base.*,
    -- This is a current overall stage, not the latest event or an offer status.
    -- Preserve the existing journey precedence; do not modify current_status.
    CASE
      WHEN LOWER(TRIM(COALESCE(current_status, ''))) IN
        ('closed', 'cancelled', 'canceled', 'withdrawn', 'completed') THEN 7
      WHEN has_signed_active_ipa = 1 THEN 6
      WHEN has_active_ipa = 1 THEN 5
      WHEN has_accepted_offer = 1 THEN 4
      WHEN has_pending_offer = 1 THEN 3
      WHEN has_unknown_offer = 1 OR TRIM(COALESCE(current_status, '')) = '' THEN 8
      WHEN journey_assignment_count > 0 THEN 2
      WHEN referral_created_date IS NOT NULL THEN 1
      ELSE 8
    END AS journey_stage_order
  FROM base
),
eligible_referrals AS (
  SELECT journey_classified.*,
    LOWER(source_reference_id) AS source_reference_match_key
  FROM journey_classified
  WHERE TO_DATE(referral_created_date) <= {AS_OF_SQL}
),
reference_profile AS (
  SELECT eligible_referrals.*,
    CASE WHEN source_reference_match_key IS NULL THEN 0
      ELSE COUNT(*) OVER (PARTITION BY source_reference_match_key)
    END AS source_reference_referral_count,
    -- A stable sequence also distinguishes missing-reference rows in report
    -- drillthrough. Missing references are never flagged as duplicate people.
    ROW_NUMBER() OVER (
      PARTITION BY source_reference_match_key
      ORDER BY referral_created_date ASC, referral_id ASC
    ) AS order_dupe
  FROM eligible_referrals
)
SELECT {AS_OF_SQL} AS as_of_date,
  export_date, referral_id, person_id, source_reference_id,
  source_reference_referral_count, source_reference_referral_count > 1 AS has_multiple_referrals,
  order_dupe, referral_created_date, required_placement_date,
  framework_category_id, framework_category_count,
  location, location_match_status, location_is_default, location_requires_review,
  response_required_date, first_action_date, first_offer_date,
  offer_accepted_date, ipa_issued_date, referral_closed_date,
  referral_closure_reason, last_activity_date, current_status,
  CASE journey_stage_order
    WHEN 1 THEN 'Referral created'
    WHEN 2 THEN 'Provider search'
    WHEN 3 THEN 'Offers received'
    WHEN 4 THEN 'Offer accepted'
    WHEN 5 THEN 'IPA created'
    WHEN 6 THEN 'IPA signed'
    WHEN 7 THEN 'Closed / cancelled / withdrawn'
    ELSE 'Needs review'
  END AS journey_stage,
  journey_stage_order,
  placement_type_required,
  is_sibling_placement, sibling_count,
  CAST(NULL AS STRING) AS region,
  placement_urgency_band AS priority,
  CAST(NULL AS STRING) AS complexity_band,
  placement_urgency_band, cnt_offer_made, first_provider_seen_date,
  is_not_seen_by_providers, ipa_placement_admission_date, ipa_2_signatures,
  ipa_last_signature_date, ipa_due_diligence_min_review_date,
  CAST(NULL AS STRING) AS child_criticality_code,
  offer_count, COALESCE(unique_homes_offered, 0) AS unique_homes_offered,
  COALESCE(offer_count, 0) > 0 AS has_offer,
  DATEDIFF(TO_DATE(first_action_date), TO_DATE(referral_created_date)) AS days_to_first_action,
  DATEDIFF(TO_DATE(first_offer_date), TO_DATE(referral_created_date)) AS days_to_first_offer,
  DATEDIFF(TO_DATE(offer_accepted_date), TO_DATE(referral_created_date)) AS days_to_accepted_offer,
  DATEDIFF(TO_DATE(ipa_issued_date), TO_DATE(referral_created_date)) AS days_to_ipa,
  DATEDIFF(COALESCE(TO_DATE(referral_closed_date), {AS_OF_SQL}),
    TO_DATE(referral_created_date)) AS days_open,
  DATEDIFF({AS_OF_SQL}, TO_DATE(last_activity_date)) AS days_without_activity,
  CASE WHEN required_placement_date IS NOT NULL AND required_placement_date < {AS_OF_SQL}
    THEN DATEDIFF({AS_OF_SQL}, required_placement_date) ELSE 0 END AS days_past_required_date,
  -- GLD-009/GLD-011: is_open and is_awaiting_offer implement the original
  -- business rules in silver.referral_enrichment; Gold propagates them.
  COALESCE(is_open, false) AS is_open,
  COALESCE(is_awaiting_offer, false) AS is_awaiting_offer,
  is_spot,
  -- GLD-013: semantic-model push-downs. provider_assignment_count replaces
  -- the distinct-provider-count DAX; is_emergency_placement mirrors the
  -- Emergency/Planned Referrals same-day rule; is_open_overdue mirrors the
  -- Open Overdue Referrals filter (open and past the required date).
  COALESCE(provider_assignment_count, 0) AS provider_assignment_count,
  COALESCE(provider_responded_count, 0) AS provider_responded_count,
  COALESCE(provider_responded_count, 0) > 0 AS has_provider_response,
  first_provider_response_date,
  required_placement_date IS NOT NULL AND referral_created_date IS NOT NULL
    AND DATEDIFF(TO_DATE(required_placement_date), TO_DATE(referral_created_date)) = 0
    AS is_emergency_placement,
  COALESCE(is_open, false) AND required_placement_date IS NOT NULL
    AND required_placement_date < {AS_OF_SQL} AS is_open_overdue,
  ipa_issued_date IS NOT NULL AND required_placement_date IS NOT NULL
    AND TO_DATE(ipa_issued_date) <= required_placement_date AS placed_by_required_date,
  CASE
    WHEN ipa_issued_date IS NOT NULL AND required_placement_date IS NOT NULL
      AND TO_DATE(ipa_issued_date) <= required_placement_date THEN 'Placed by target'
    WHEN ipa_issued_date IS NOT NULL THEN 'Placed after target'
    WHEN required_placement_date < {AS_OF_SQL} AND LOWER(COALESCE(current_status, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open overdue'
    WHEN LOWER(COALESCE(current_status, '')) NOT IN
      ('closed','cancelled','withdrawn','completed') THEN 'Open on track'
    ELSE 'Closed without placement'
  END AS required_placement_date_outcome,
  planned_placement_start_date, estimated_weekly_cost,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM reference_profile
""")
```

<a id="python-04-gold-model-py-567"></a>
## 04_gold_model.py:567

Source: [project X/04_gold_model.py:567](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L567).

```python
# Preserve historic snapshot rows while migrating the physical field names
# from the former PascalCase contract to the Gold snake_case convention.
SNAPSHOT_COLUMN_RENAMES = {
    'SnapshotDate': 'snapshot_date', 'ReferralID': 'referral_id', 'ChildID': 'person_id',
    'child_id': 'person_id',
    'ReferralCreatedDate': 'referral_created_date', 'RequiredPlacementDate': 'required_placement_date',
    'FirstActionDate': 'first_action_date', 'FirstOfferDate': 'first_offer_date',
    'OfferAcceptedDate': 'offer_accepted_date', 'IPAIssuedDate': 'ipa_issued_date',
    'ReferralClosedDate': 'referral_closed_date', 'ReferralClosureReason': 'referral_closure_reason',
    'CurrentStatus': 'current_status', 'LastActivityDate': 'last_activity_date',
    'PlacementTypeRequired': 'placement_type_required', 'Region': 'region',
    'Priority': 'priority', 'ComplexityBand': 'complexity_band',
    'PlacementUrgencyBand': 'placement_urgency_band', 'CntOfferMade': 'cnt_offer_made',
    'FirstProviderSeenDate': 'first_provider_seen_date',
    'IsNotSeenByProviders': 'is_not_seen_by_providers',
    'IPAPlacementAdmissionDate': 'ipa_placement_admission_date',
    'IPA2Signatures': 'ipa_2_signatures', 'IPALastSignatureDate': 'ipa_last_signature_date',
    'IPADueDiligenceMinReviewDate': 'ipa_due_diligence_min_review_date',
    'IsOpen': 'is_open', 'HasOffer': 'has_offer', 'OfferCount': 'offer_count',
    'DaysOpen': 'days_open', 'DaysWithoutActivity': 'days_without_activity',
    'DaysPastRequiredDate': 'days_past_required_date',
    'PlacedByRequiredDate': 'placed_by_required_date',
    'RequiredPlacementDateOutcome': 'required_placement_date_outcome',
}
if spark.catalog.tableExists(SNAPSHOT_TABLE):
    snapshot_columns = {field.name for field in spark.table(SNAPSHOT_TABLE).schema.fields}
    for previous_name, current_name in SNAPSHOT_COLUMN_RENAMES.items():
        if previous_name in snapshot_columns and current_name not in snapshot_columns:
            spark.sql(
                f"ALTER TABLE {SNAPSHOT_TABLE} RENAME COLUMN `{previous_name}` TO `{current_name}`"
            )
            snapshot_columns.remove(previous_name)
            snapshot_columns.add(current_name)

snapshot = spark.table("gold.fact_referral").select(
    F.lit(AS_OF_DATE_VALUE).cast("date").alias("snapshot_date"),
    F.trunc(F.lit(AS_OF_DATE_VALUE).cast("date"), "month").alias("snapshot_month_start"),
    F.last_day(F.lit(AS_OF_DATE_VALUE).cast("date")).alias("snapshot_month_end"),
    F.lit("WMPP_SNAPSHOT_V2").alias("snapshot_rule_version"),
    "job_run_id", "export_date", "referral_id", "person_id", "referral_created_date", "required_placement_date",
    "source_reference_id", "source_reference_referral_count", "has_multiple_referrals", "order_dupe",
    "framework_category_id", "framework_category_count",
    "location", "location_match_status", "location_is_default", "location_requires_review",
    "first_action_date", "first_offer_date", "offer_accepted_date", "ipa_issued_date",
    "referral_closed_date", "referral_closure_reason", "current_status",
    "journey_stage", "journey_stage_order",
    "last_activity_date", "placement_type_required", "region", "priority",
    "is_sibling_placement", "sibling_count",
    "complexity_band", "placement_urgency_band", "cnt_offer_made",
    "first_provider_seen_date", "is_not_seen_by_providers",
    "ipa_placement_admission_date", "ipa_2_signatures",
    "ipa_last_signature_date", "ipa_due_diligence_min_review_date",
    "is_open", "is_awaiting_offer", "is_spot", "has_offer", "offer_count", "days_open",
    "provider_assignment_count", "provider_responded_count", "has_provider_response",
    "first_provider_response_date", "is_emergency_placement", "is_open_overdue",
    "days_without_activity", "days_past_required_date",
    "placed_by_required_date", "required_placement_date_outcome",
)
month_start = AS_OF_DATE_VALUE.replace(day=1)
next_month_start = (
    month_start.replace(year=month_start.year + 1, month=1)
    if month_start.month == 12
    else month_start.replace(month=month_start.month + 1)
)
month_predicate = (
    f"snapshot_date >= DATE '{month_start.isoformat()}' AND "
    f"snapshot_date < DATE '{next_month_start.isoformat()}'"
)
if not spark.catalog.tableExists(SNAPSHOT_TABLE):
    snapshot.write.format("delta").mode("overwrite").saveAsTable(SNAPSHOT_TABLE)
else:
    # Replacement is scoped to the active calendar month.
    (snapshot.write.format("delta").mode("overwrite")
        .option("replaceWhere", month_predicate)
        .option("mergeSchema", "true")
        .saveAsTable(SNAPSHOT_TABLE))
# Older retained snapshots pre-date the explicit month key and response rule.
# Backfill only deterministic calendar metadata; leave response evidence NULL
# so an unavailable historic response KPI cannot be mistaken for zero.
# New journey fields also stay NULL in retained months until archive replay;
# today's offer/IPA evidence must never relabel an older referral snapshot.
# Reference/duplicate annotations also remain NULL in retained months until
# archive replay: today's reference history must not overwrite an older month.
# Sibling placement fields also remain NULL in retained months until replay.
spark.sql(f"""
UPDATE {SNAPSHOT_TABLE}
SET snapshot_month_start = TRUNC(snapshot_date, 'month'),
    snapshot_month_end = LAST_DAY(snapshot_date),
    snapshot_rule_version = COALESCE(snapshot_rule_version, 'LEGACY_PRE_V2')
WHERE snapshot_month_start IS NULL
   OR snapshot_month_end IS NULL
   OR snapshot_rule_version IS NULL
""")
print(
    f"Snapshot refreshed for {AS_OF_DATE_VALUE}: {snapshot.count():,} referrals; "
    f"replaced active month {month_start:%Y-%m}"
)

# Identifier-free aggregate used only by specifically approved market-wide
# visuals. It intentionally excludes referral, person, provider, authority and
# free-text identifiers so detail RLS cannot be bypassed through this table.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_global_summary AS
SELECT snapshot_month_start, snapshot_month_end, current_status,
  placement_type_required, priority, placement_urgency_band,
  required_placement_date_outcome,
  COUNT(DISTINCT referral_id) AS referral_count,
  SUM(CASE WHEN is_open THEN 1 ELSE 0 END) AS open_referral_count,
  SUM(CASE WHEN NOT is_open THEN 1 ELSE 0 END) AS closed_referral_count,
  SUM(CASE WHEN is_awaiting_offer THEN 1 ELSE 0 END) AS awaiting_offer_count,
  SUM(CASE WHEN has_offer THEN 1 ELSE 0 END) AS referrals_with_offer_count,
  SUM(COALESCE(offer_count, 0)) AS offer_count,
  SUM(CASE WHEN has_provider_response THEN 1 ELSE 0 END) AS provider_response_referral_count,
  SUM(CASE WHEN placed_by_required_date THEN 1 ELSE 0 END) AS placed_by_required_date_count,
  MAX(snapshot_rule_version) AS snapshot_rule_version,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM gold.fact_referral_snapshot
GROUP BY snapshot_month_start, snapshot_month_end, current_status,
  placement_type_required, priority, placement_urgency_band,
  required_placement_date_outcome
""")
```

<a id="python-04-gold-model-py-698"></a>
## 04_gold_model.py:698

Source: [project X/04_gold_model.py:698](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L698).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_lifecycle_event AS
SELECT e.event_id, e.referral_id, e.event_type, e.event_timestamp,
  e.sequence_number, e.created_by, r.export_date, '{GOLD_JOB_RUN_ID}' AS job_run_id
FROM {EVENT_ROLLUP_SOURCE} e
LEFT JOIN (
  SELECT referral_id, MAX(CAST(export_date AS TIMESTAMP)) AS export_date
  FROM silver.referral
  GROUP BY referral_id
) r ON e.referral_id = r.referral_id
""")
```

<a id="python-04-gold-model-py-712"></a>
## 04_gold_model.py:712

Source: [project X/04_gold_model.py:712](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L712).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_offer AS
WITH home_framework_category AS (
  SELECT provider_home_id,
    CASE WHEN COUNT(DISTINCT framework_category_id) = 1
      THEN MIN(framework_category_id) END AS framework_category_id,
    COUNT(DISTINCT framework_category_id) AS framework_category_count
  FROM silver.provider_home_category
  GROUP BY provider_home_id
)
SELECT {AS_OF_SQL} AS as_of_date,
  o.offer_id AS offer_id, rp.referral_id AS referral_id,o.referral_provider_id,
  rp.provider_id AS provider_id, o.provider_home_id AS provider_home_id,
  o.category AS framework_category_id,
  category.framework_category_id AS provider_home_framework_category_id,
  COALESCE(category.framework_category_count, 0) AS provider_home_framework_category_count,
  loc.location AS referral_location,
  loc.location_match_status, loc.location_is_default, loc.location_requires_review,
  home.postcode_normalized AS provider_home_postcode,
  -- Publish offline-reference endpoints for the Offer Locations path map.
  -- A location requiring review must not imply an approved referral origin.
  CASE WHEN NOT COALESCE(loc.location_requires_review, true)
    THEN CAST(loc.location_latitude AS DOUBLE) END AS referral_latitude,
  CASE WHEN NOT COALESCE(loc.location_requires_review, true)
    THEN CAST(loc.location_longitude AS DOUBLE) END AS referral_longitude,
  CAST(home.home_latitude AS DOUBLE) AS provider_home_latitude,
  CAST(home.home_longitude AS DOUBLE) AS provider_home_longitude,
  CASE WHEN loc.location_requires_review THEN NULL
    ELSE {OFFER_DISTANCE_KM_SQL} END AS referral_to_home_distance_km,
  CASE
    WHEN loc.referral_id IS NULL THEN 'MISSING_REFERRAL_LOCATION'
    WHEN loc.location_requires_review THEN 'LOCATION_REQUIRES_REVIEW'
    WHEN loc.location_latitude IS NULL OR loc.location_longitude IS NULL THEN 'MISSING_CITY_COORDINATES'
    WHEN home.home_latitude IS NULL OR home.home_longitude IS NULL THEN 'MISSING_HOME_COORDINATES'
    WHEN loc.location_is_default THEN 'APPROXIMATE_DEFAULT_CITY'
    ELSE 'APPROXIMATE_PREFERENCE_CITY'
  END AS referral_to_home_distance_status,
  CASE WHEN loc.location_reference_source LIKE 'OS Open Names representative%'
    THEN 'CITY_REPRESENTATIVE_POINT_TO_POSTCODE_STRAIGHT_LINE'
    ELSE 'CITY_CENTROID_TO_POSTCODE_STRAIGHT_LINE'
  END AS referral_to_home_distance_basis,
  loc.location_reference_source, loc.location_reference_version,
  home.home_reference_source, home.home_reference_version,
  CAST(o.offer_date AS TIMESTAMP) AS offer_submitted_date,
  CAST(o.last_modified_date AS TIMESTAMP) AS offer_reviewed_date,
  CASE WHEN LOWER(COALESCE(o.offer_status, '')) IN
    ('offer_successful', 'offer_unsuccessful', 'offer_withdrawn',
     'accepted', 'approved', 'selected', 'declined', 'rejected', 'withdrawn')
    THEN CAST(o.last_modified_date AS TIMESTAMP) END AS offer_decision_date,
  o.offer_status AS offer_status, o.offer_type AS offer_type,
  CAST(o.estimated_start_date AS TIMESTAMP) AS proposed_placement_start_date,
  CAST(NULL AS INT) AS estimated_duration_weeks,
  CAST(COALESCE(o.core_weekly_fee, 0) + COALESCE(o.education_weekly_fee, 0)
    AS DECIMAL(19, 2)) AS estimated_weekly_cost,
  COALESCE(o.decline_reason_other, o.decline_reason, o.withdraw_reason)
    AS rejection_reason,
  o.child_summary_needs AS child_summary_needs,
  -- GLD-013: semantic-model push-downs. offer_age_days replaces the
  -- "Pending Offer Age (Days)" calculated column (as_of date instead of
  -- TODAY(), so snapshots stay reproducible); days_since_offer_activity
  -- backs the draft stalled 7+/14+ day measures; the is_draft_* flags back
  -- the draft data-quality cards; the is_*ipa* flags replace the
  -- per-offer Is Awaiting IPA Creation / Is IPA Pending / Is IPA Completed
  -- row measures.
  DATEDIFF({AS_OF_SQL}, TO_DATE(o.offer_date)) AS offer_age_days,
  DATEDIFF({AS_OF_SQL}, TO_DATE(COALESCE(o.last_modified_date, o.offer_date)))
    AS days_since_offer_activity,
  LOWER(COALESCE(o.offer_status, '')) = 'draft'
    AND (o.offer_date IS NULL OR o.last_modified_date IS NULL)
    AS is_draft_missing_dates,
  LOWER(COALESCE(o.offer_status, '')) = 'draft'
    AND o.offer_date IS NOT NULL AND o.last_modified_date IS NOT NULL
    AND CAST(o.offer_date AS TIMESTAMP) = CAST(o.last_modified_date AS TIMESTAMP)
    AS is_draft_no_activity,
  LOWER(COALESCE(o.offer_status, '')) IN
    ('accepted', 'approved', 'selected', 'offer_successful')
    AND COALESCE(ip.ipa_count, 0) = 0 AS is_awaiting_ipa_creation,
  COALESCE(ip.has_pending_ipa, 0) = 1 AS is_ipa_pending,
  COALESCE(ip.has_completed_ipa, 0) = 1 AS is_ipa_completed,
  CAST(o.export_date AS TIMESTAMP) AS export_date,
  CAST(o.export_date AS TIMESTAMP) AS source_export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM silver.offer o
INNER JOIN silver.referral_provider rp
  ON o.referral_provider_id = rp.referral_provider_id
LEFT JOIN home_framework_category category ON o.provider_home_id = category.provider_home_id
LEFT JOIN silver.referral_location loc ON rp.referral_id = loc.referral_id
LEFT JOIN silver.provider_home_location home ON o.provider_home_id = home.provider_home_id
LEFT JOIN (
  SELECT offer_id, COUNT(*) AS ipa_count,
    MAX(CASE WHEN COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false)
      THEN 1 ELSE 0 END) AS has_completed_ipa,
    MAX(CASE WHEN NOT COALESCE(CAST(closed AS BOOLEAN), false)
      AND NOT (COALESCE(CAST(signed_by_provider AS BOOLEAN), false)
        AND COALESCE(CAST(signed_by_local_authority AS BOOLEAN), false))
      THEN 1 ELSE 0 END) AS has_pending_ipa
  FROM silver.ipa
  WHERE offer_id IS NOT NULL
    AND (created_datetime IS NULL OR TO_DATE(created_datetime) <= {AS_OF_SQL})
  GROUP BY offer_id
) ip ON o.offer_id = ip.offer_id
WHERE o.offer_date IS NULL OR TO_DATE(o.offer_date) <= {AS_OF_SQL}
""")
```

<a id="python-04-gold-model-py-817"></a>
## 04_gold_model.py:817

Source: [project X/04_gold_model.py:817](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L817).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_ipa AS
SELECT {AS_OF_SQL} AS as_of_date,
  i.ipa_id AS ipa_id, i.referral_id AS referral_id,
  i.offer_id AS accepted_offer_id,
  COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false) AS signed_by_provider,
  COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false) AS signed_by_local_authority,
  COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false)
    AND COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false) AS is_ipa_completed,
  NOT COALESCE(CAST(i.closed AS BOOLEAN), false)
    AND NOT (COALESCE(CAST(i.signed_by_provider AS BOOLEAN), false)
      AND COALESCE(CAST(i.signed_by_local_authority AS BOOLEAN), false)) AS is_ipa_pending,
  CAST(i.created_datetime AS TIMESTAMP) AS ipa_issued_date,
  CAST(i.placement_admission_date AS TIMESTAMP) AS planned_placement_start_date,
  CAST(NULL AS TIMESTAMP) AS actual_placement_start_date,
  CAST(NULL AS TIMESTAMP) AS planned_placement_end_date,
  CAST(NULL AS TIMESTAMP) AS actual_placement_end_date,
  CAST(i.placement_admission_date AS TIMESTAMP) AS placement_admission_date,
  CAST(i.costs_total_weekly_fee AS DECIMAL(19, 2)) AS estimated_weekly_cost,
  CAST(NULL AS DECIMAL(19, 2)) AS actual_weekly_cost,
  i.status AS placement_status, CAST(i.closed AS BOOLEAN) AS is_placement_closed,
  CAST(i.closed_datetime AS TIMESTAMP) AS placement_ended_date,
  CAST(NULL AS STRING) AS placement_end_reason,
  CAST(i.export_date AS TIMESTAMP) AS export_date,
  CAST(i.export_date AS TIMESTAMP) AS source_export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM silver.ipa i
WHERE i.created_datetime IS NULL OR TO_DATE(i.created_datetime) <= {AS_OF_SQL}
""")
```

<a id="python-04-gold-model-py-847"></a>
## 04_gold_model.py:847

Source: [project X/04_gold_model.py:847](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L847).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_referral_provider AS
WITH referral_provider_history AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY COALESCE(modified_date, created_date, export_date) DESC,
             export_date DESC
  ) AS row_number_current
  FROM silver.referral_provider
  WHERE created_date IS NULL OR TO_DATE(created_date) <= {AS_OF_SQL}
), referral_provider_current AS (
  SELECT * FROM referral_provider_history WHERE row_number_current = 1
), offer_response AS (
  SELECT referral_provider_id,
    MIN(CAST(offer_date AS TIMESTAMP)) AS first_offer_response_at
  FROM silver.offer
  WHERE offer_date IS NOT NULL AND TO_DATE(offer_date) <= {AS_OF_SQL}
  GROUP BY referral_provider_id
), reason_response AS (
  SELECT referral_provider_id, MIN(response_at) AS first_reason_response_at
  FROM (
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_cancel_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
    UNION ALL
    SELECT referral_provider_id, CAST(created_date AS TIMESTAMP) AS response_at
    FROM silver.referral_provider_decline_reason
    WHERE TO_DATE(created_date) <= {AS_OF_SQL}
  ) response_event
  GROUP BY referral_provider_id
), assignment_response AS (
  SELECT rp.*,
    COALESCE(CAST(rp.created_date AS TIMESTAMP), CAST(rp.export_date AS TIMESTAMP)) AS assigned_at,
    offer_response.first_offer_response_at,
    reason_response.first_reason_response_at,
    CASE
      WHEN offer_response.first_offer_response_at IS NULL
        THEN reason_response.first_reason_response_at
      WHEN reason_response.first_reason_response_at IS NULL
        THEN offer_response.first_offer_response_at
      ELSE LEAST(offer_response.first_offer_response_at, reason_response.first_reason_response_at)
    END AS candidate_response_at
  FROM referral_provider_current rp
  LEFT JOIN offer_response
    ON rp.referral_provider_id = offer_response.referral_provider_id
  LEFT JOIN reason_response
    ON rp.referral_provider_id = reason_response.referral_provider_id
)
SELECT {AS_OF_SQL} AS as_of_date,
  rp.referral_provider_id AS referral_provider_id, rp.referral_id AS referral_id,
  rp.provider_id AS provider_id, rp.assigned_at,
  rp.assigned_at AS first_observed_date,
  rp.first_offer_response_at, rp.first_reason_response_at,
  CASE WHEN rp.candidate_response_at IS NOT NULL
    AND (rp.assigned_at IS NULL OR rp.candidate_response_at >= rp.assigned_at)
    THEN rp.candidate_response_at END AS first_qualifying_response_at,
  CASE WHEN rp.candidate_response_at IS NOT NULL
    AND (rp.assigned_at IS NULL OR rp.candidate_response_at >= rp.assigned_at)
    THEN true ELSE false END AS has_qualifying_response,
  CASE WHEN rp.candidate_response_at IS NOT NULL AND rp.assigned_at IS NOT NULL
    AND rp.candidate_response_at >= rp.assigned_at
    THEN CAST((UNIX_TIMESTAMP(rp.candidate_response_at) - UNIX_TIMESTAMP(rp.assigned_at)) / 60 AS BIGINT)
    END AS response_elapsed_minutes,
  'OFFER_OR_RECORDED_REASON_V1' AS response_evidence_scope,
  CAST(rp.export_date AS TIMESTAMP) AS export_date,
  CAST(rp.is_excluded AS BOOLEAN) AS is_excluded,
  CAST(rp.is_declined AS BOOLEAN) AS is_declined,
  CAST(rp.is_cancelled AS BOOLEAN) AS is_cancelled,
  CAST(rp.is_closed AS BOOLEAN) AS is_closed,
  -- GLD-012: a provider referral is engaged while it is not cancelled,
  -- not closed and not excluded.
  (NOT COALESCE(CAST(rp.is_cancelled AS BOOLEAN), false)
    AND NOT COALESCE(CAST(rp.is_closed AS BOOLEAN), false)
    AND NOT COALESCE(CAST(rp.is_excluded AS BOOLEAN), false)) AS is_engaged,
  CASE
    WHEN rp.is_cancelled THEN 'Cancelled'
    WHEN rp.is_declined THEN 'Declined'
    WHEN rp.is_closed THEN 'Closed'
    WHEN rp.is_excluded THEN 'Excluded'
    ELSE 'Assigned'
  END AS provider_response_status,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM assignment_response rp
""")
```

<a id="python-04-gold-model-py-935"></a>
## 04_gold_model.py:935

Source: [project X/04_gold_model.py:935](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L935).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.fact_provider_kpi_monthly AS
WITH offer_component AS (
  SELECT referral_provider_id,
    COUNT(DISTINCT offer_id) AS offers_submitted_count,
    COUNT(DISTINCT CASE WHEN LOWER(COALESCE(offer_status, '')) IN
      ('accepted', 'approved', 'selected', 'offer_successful') THEN offer_id END)
      AS accepted_offer_count
  FROM gold.fact_offer
  GROUP BY referral_provider_id
), assignment_component AS (
  SELECT rp.provider_id, DATE_TRUNC('month', rp.assigned_at) AS assignment_month,
    scope.security_scope_key, rp.referral_provider_id, rp.referral_id,
    rp.has_qualifying_response,
    rp.response_elapsed_minutes,
    COALESCE(o.offers_submitted_count, 0) AS offers_submitted_count,
    COALESCE(o.accepted_offer_count, 0) AS accepted_offer_count,
    COALESCE(f.placed_by_required_date, false) AS placed_by_required_date
  FROM gold.fact_referral_provider rp
  LEFT JOIN offer_component o
    ON rp.referral_provider_id = o.referral_provider_id
  LEFT JOIN gold.fact_referral f ON rp.referral_id = f.referral_id
  LEFT JOIN monitoring.cfg_referral_scope scope
    ON rp.referral_id = scope.referral_id
    AND COALESCE(scope.is_active, false)
    AND (scope.valid_from IS NULL OR scope.valid_from <= {AS_OF_SQL})
    AND (scope.valid_to IS NULL OR scope.valid_to >= {AS_OF_SQL})
  WHERE rp.assigned_at IS NOT NULL
)
SELECT provider_id, CAST(assignment_month AS DATE) AS assignment_month,
  security_scope_key,
  COUNT(DISTINCT referral_provider_id) AS response_opportunity_count,
  SUM(CASE WHEN has_qualifying_response THEN 1 ELSE 0 END) AS qualifying_response_count,
  SUM(offers_submitted_count) AS offers_submitted_count,
  SUM(accepted_offer_count) AS accepted_offer_count,
  COUNT(DISTINCT CASE WHEN accepted_offer_count > 0 THEN referral_id END)
    AS successful_referral_count,
  COUNT(DISTINCT CASE WHEN accepted_offer_count > 0 AND placed_by_required_date
    THEN referral_id END) AS placed_by_target_count,
  AVG(CAST(response_elapsed_minutes AS DOUBLE)) AS average_response_minutes,
  PERCENTILE_APPROX(response_elapsed_minutes, 0.5) AS median_response_minutes,
  'ASSIGNMENT_COHORT_OFFER_OR_REASON_V1' AS kpi_rule_version,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM assignment_component
GROUP BY provider_id, assignment_month, security_scope_key
""")
```

<a id="python-05-gold-dimensions-py-128"></a>
## 05_gold_dimensions.py:128

Source: [project X/05_gold_dimensions.py:128](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L128).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE {GOLD_SCHEMA}.dim_date AS
SELECT
  date_value AS date,
  YEAR(date_value) AS calendar_year,
  QUARTER(date_value) AS calendar_quarter,
  MONTH(date_value) AS calendar_month_number,
  DATE_FORMAT(date_value, 'MMMM') AS calendar_month_name,
  DATE_FORMAT(date_value, 'yyyy-MM') AS year_month,
  DAYOFWEEK(date_value) AS day_of_week_number,
  DATE_FORMAT(date_value, 'EEEE') AS day_of_week_name,
  DAYOFMONTH(date_value) AS day_of_month,
  CASE WHEN DAYOFWEEK(date_value) IN (1, 7) THEN false ELSE true END AS is_weekday,
  CAST('{GOLD_EXPORT_DATE}' AS TIMESTAMP) AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM (
  SELECT EXPLODE(SEQUENCE(DATE '2020-01-01', DATE '2035-12-31', INTERVAL 1 DAY)) AS date_value
)
""")
```

<a id="python-05-gold-dimensions-py-155"></a>
## 05_gold_dimensions.py:155

Source: [project X/05_gold_dimensions.py:155](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L155).

```python
latest_dimension(
    "silver.provider", "gold.dim_provider", ["provider_id"],
    [("provider_id", "provider_id"), ("holding_company_id", "holding_company_id"),
     ("provider_name", "provider_name"), ("provider_status", "provider_status"),
     ("town_city", "town_city"), ("county", "county"), ("postcode", "postcode"),
     ("country", "country"), ("qa_flag", "qa_flag"),
     ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-163"></a>
## 05_gold_dimensions.py:163

Source: [project X/05_gold_dimensions.py:163](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L163).

```python
latest_dimension(
    "silver.provider_home", "gold.dim_provider_home", ["provider_home_id"],
    [("provider_home_id", "provider_home_id"), ("provider_id", "provider_id"),
     ("service_type", "service_type"), ("home_name", "home_name"),
     ("town_city", "town_city"), ("county", "county"), ("postcode", "postcode"),
     ("number_of_registered_beds", "registered_beds"), ("is_spot", "is_spot"),
     ("home_contact_number", "home_contact_number"),
     ("registered_manager_contact_number", "registered_manager_contact_number"),
     ("qa_flag", "qa_flag"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-173"></a>
## 05_gold_dimensions.py:173

Source: [project X/05_gold_dimensions.py:173](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L173).

```python
latest_dimension(
    "silver.framework", "gold.dim_framework", ["framework_code"],
    [("framework_code", "framework_code"), ("framework_name", "framework_name"),
     ("placement_type", "placement_type"), ("start_date", "start_date"),
     ("end_date", "end_date"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-179"></a>
## 05_gold_dimensions.py:179

Source: [project X/05_gold_dimensions.py:179](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L179).

```python
latest_dimension(
    "silver.framework_category", "gold.dim_framework_category", ["framework_category_id"],
    [("framework_category_id", "framework_category_id"), ("framework_code", "framework_code"),
     ("category_name", "category_name"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-194"></a>
## 05_gold_dimensions.py:194

Source: [project X/05_gold_dimensions.py:194](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L194).

```python
copy_bridge(
    "silver.provider_framework", "gold.bridge_provider_framework",
    ["provider_framework_id", "provider_id", "framework_code", "qa_flag", "export_date"],
    [("provider_framework_id", "provider_framework_id"), ("provider_id", "provider_id"),
     ("framework_code", "framework_code"), ("qa_flag", "qa_flag"),
     ("export_date", "source_export_date")],
)
copy_bridge(
    "silver.provider_home_category", "gold.bridge_provider_home_framework_category",
    ["provider_home_category_id", "provider_home_id", "framework_category_id", "export_date"],
    [("provider_home_category_id", "provider_home_category_id"),
     ("provider_home_id", "provider_home_id"),
     ("framework_category_id", "framework_category_id"),
     ("export_date", "source_export_date")],
    key_columns=["provider_home_id", "framework_category_id"],
)
copy_bridge(
    "silver.referral_category", "gold.bridge_referral_framework_category",
    ["referral_id", "framework_category_id", "export_date"],
    [("referral_id", "referral_id"), ("framework_category_id", "framework_category_id"),
     ("export_date", "source_export_date")],
    key_columns=["referral_id", "framework_category_id"],
)
copy_bridge(
    "silver.provider_home_spot_category", "gold.bridge_provider_home_spot_category",
    ["provider_home_spot_category_id", "provider_home_id", "spot_category_code", "export_date"],
    [("provider_home_spot_category_id", "provider_home_spot_category_id"),
     ("provider_home_id", "provider_home_id"), ("spot_category_code", "spot_category_code"),
     ("export_date", "source_export_date")],
    key_columns=["provider_home_spot_category_id"],
)
copy_bridge(
    "silver.referral_spot_category", "gold.bridge_referral_spot_category",
    ["referral_spot_category_id", "referral_id", "spot_category", "export_date"],
    [("referral_spot_category_id", "referral_spot_category_id"),
     ("referral_id", "referral_id"), ("spot_category", "spot_category"),
     ("export_date", "source_export_date")],
    key_columns=["referral_spot_category_id"],
)
copy_bridge(
    "silver.provider_sic_codes", "gold.bridge_provider_sic_code",
    ["provider_id", "sic_code", "export_date"],
    [("provider_id", "provider_id"), ("sic_code", "sic_code"),
     ("export_date", "source_export_date")],
)
latest_dimension(
    "silver.provider_submission_docs", "gold.dim_provider_submission_document", ["document_id"],
    [("document_id", "document_id"), ("submission_id", "submission_id"),
     ("s3_file_metadata_id", "s3_file_metadata_id"), ("document_name", "document_name"),
     ("document_type", "document_type"), ("expiry_date", "expiry_date"),
     ("last_updated", "last_updated"), ("next_review_date", "next_review_date"),
     ("service_type", "service_type"), ("home_id", "home_id"),
     ("start_date", "start_date"), ("export_date", "source_export_date")],
)

# GLD-014: keep provider messages as a current-record dimension and combine
# cancellation and decline reasons into one consistently named lookup. The
# prefixed key preserves provenance because the two source ID sequences are
# independent and can overlap.
latest_dimension(
    "silver.referral_provider_message", "gold.dim_referral_provider_message", ["message_id"],
    [("message_id", "message_id"), ("referral_provider_id", "referral_provider_id"),
     ("message_read_by", "message_read_by"),
     ("message_read_timestamp", "message_read_timestamp"),
     ("message_text", "message_text"), ("created_timestamp", "created_timestamp"),
     ("created_by", "created_by"), ("export_date", "source_export_date")],
)

for closure_source, required_columns in {
    "silver.referral_provider_cancel_reason": {
        "cancel_reason_id", "referral_provider_id", "cancel_reason",
        "cancel_reason_other_text", "created_by", "created_date", "export_date",
    },
    "silver.referral_provider_decline_reason": {
        "decline_reason_id", "referral_provider_id", "decline_reason",
        "decline_reason_other_text", "created_by", "created_date", "export_date",
    },
}.items():
    require_columns(closure_source, required_columns)

closure_reasons = spark.sql(f"""
WITH closure_source AS (
  SELECT CONCAT('cancel:', CAST(cancel_reason_id AS STRING)) AS closure_reason_id,
    referral_provider_id, 'cancel' AS closure_type, cancel_reason AS reason,
    cancel_reason_other_text AS reason_other, created_by,
    CAST(created_date AS TIMESTAMP) AS created_date,
    CAST(export_date AS TIMESTAMP) AS source_export_date
  FROM silver.referral_provider_cancel_reason
  UNION ALL
  SELECT CONCAT('decline:', CAST(decline_reason_id AS STRING)) AS closure_reason_id,
    referral_provider_id, 'decline' AS closure_type, decline_reason AS reason,
    decline_reason_other_text AS reason_other, created_by,
    CAST(created_date AS TIMESTAMP) AS created_date,
    CAST(export_date AS TIMESTAMP) AS source_export_date
  FROM silver.referral_provider_decline_reason
), current_closure_reason AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY closure_reason_id
    ORDER BY source_export_date DESC NULLS LAST
  ) AS closure_reason_snapshot_rank
  FROM closure_source
), cleaned_closure_reason AS (
  SELECT closure_reason_id, referral_provider_id, closure_type, reason, reason_other,
    created_by, created_date, source_export_date,
    CASE
      WHEN TRIM(COALESCE(reason_other, reason, '')) = ''
        THEN 'No reason recorded'
      WHEN LOWER(TRIM(COALESCE(reason_other, reason, ''))) = 'test'
        THEN CAST(NULL AS STRING)
      ELSE TRIM(COALESCE(reason_other, reason))
    END AS closure_reason_clean
  FROM current_closure_reason
  WHERE closure_reason_snapshot_rank = 1
), grouped_closure_reason AS (
  SELECT *,
    CASE
      WHEN closure_reason_clean IS NULL
        OR LOWER(closure_reason_clean) = 'no reason recorded'
        THEN 'No reason recorded'
      WHEN LOWER(closure_reason_clean) LIKE '%location%'
        THEN 'Location / Matching issue'
      WHEN LOWER(closure_reason_clean) LIKE '%off portal%'
        OR LOWER(closure_reason_clean) LIKE '%not on the portal%'
        OR LOWER(closure_reason_clean) LIKE '%doesn''t have access%'
        THEN 'Off-portal / alternative placement'
      WHEN LOWER(closure_reason_clean) LIKE '%placed%'
        OR LOWER(closure_reason_clean) LIKE '%moved%'
        THEN 'Placement found elsewhere'
      WHEN LOWER(closure_reason_clean) LIKE '%case closed%'
        OR LOWER(closure_reason_clean) LIKE '%remove%'
        OR LOWER(closure_reason_clean) LIKE '%update%'
        THEN 'Case / administrative closure'
      WHEN LOWER(closure_reason_clean) LIKE '%email%'
        OR LOWER(closure_reason_clean) LIKE '%portal not working%'
        THEN 'System / process issue'
      ELSE 'Other'
    END AS closure_reason_grouped
  FROM cleaned_closure_reason
), ranked_closure_reason AS (
  SELECT *, ROW_NUMBER() OVER (
    PARTITION BY referral_provider_id
    ORDER BY created_date DESC NULLS LAST,
      source_export_date DESC NULLS LAST,
      closure_reason_id DESC
  ) AS sequence_order
  FROM grouped_closure_reason
)
SELECT closure_reason_id, referral_provider_id, closure_type, reason, reason_other,
  closure_reason_clean, closure_reason_grouped,
  closure_reason_grouped AS closed_referral_reason_bucket,
  sequence_order, created_by, created_date, source_export_date,
  source_export_date AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM ranked_closure_reason
""")
(closure_reasons.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("gold.dim_referral_provider_closure_reason"))
print("gold.dim_referral_provider_closure_reason: "
      f"{closure_reasons.count():,} rows from cancellation and decline reasons")

require_columns("silver.referral", ["placement_type", "referral_status", "export_date"])
require_columns("silver.ipa", ["placement_type", "export_date"])
placement_types = (
    spark.table("silver.referral").select(
        F.col("placement_type").alias("placement_type"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .unionByName(spark.table("silver.ipa").select(
        F.col("placement_type").alias("placement_type"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    ))
    .where(F.col("placement_type").isNotNull() & (F.trim(F.col("placement_type")) != ""))
    .groupBy("placement_type").agg(F.max("export_date").alias("export_date"))
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(placement_types.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_placement_type"))

referral_statuses = (
    spark.table("silver.referral").select(
        F.col("referral_status").alias("referral_status"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .where(F.col("referral_status").isNotNull() & (F.trim(F.col("referral_status")) != ""))
    .groupBy("referral_status").agg(F.max("export_date").alias("export_date"))
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(referral_statuses.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_referral_status"))

# A separate month dimension keeps state-at-snapshot time intelligence away
# from the active referral-created date role. One row is emitted per calendar
# month and the month_start key joins directly to the snapshot fact.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.dim_snapshot_month AS
SELECT
  date_value AS month_start,
  LAST_DAY(date_value) AS month_end,
  YEAR(date_value) AS calendar_year,
  MONTH(date_value) AS calendar_month_number,
  DATE_FORMAT(date_value, 'MMMM') AS calendar_month_name,
  DATE_FORMAT(date_value, 'yyyy-MM') AS year_month,
  CAST('{GOLD_EXPORT_DATE}' AS TIMESTAMP) AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM (
  SELECT EXPLODE(SEQUENCE(DATE '2020-01-01', DATE '2035-12-01', INTERVAL 1 MONTH)) AS date_value
)
""")

# Dynamic RLS inputs. The setup notebook creates these configuration tables
# empty, so a newly deployed role denies detail until explicitly approved
# mappings are loaded. Effective dates are applied in Gold to keep the model
# role small and deterministic.
spark.sql(f"""
CREATE OR REPLACE TABLE gold.dim_security_scope AS
SELECT security_scope_key, UPPER(TRIM(scope_type)) AS scope_type,
  TRIM(scope_code) AS scope_code, scope_name,
  COALESCE(allows_global_summary, false) AS allows_global_summary,
  valid_from, valid_to, approved_by, updated_at,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_security_scope
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")
spark.sql(f"""
CREATE OR REPLACE TABLE gold.sec_user_scope_access AS
SELECT LOWER(TRIM(user_principal_name)) AS user_principal_name,
  security_scope_key, valid_from, valid_to, approved_by, access_reason,
  updated_at, '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_user_scope_access
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")
spark.sql(f"""
CREATE OR REPLACE TABLE gold.bridge_referral_scope AS
SELECT CAST(referral_id AS STRING) AS referral_id, security_scope_key,
  valid_from, valid_to, assigned_by, assignment_reason, updated_at,
  '{GOLD_JOB_RUN_ID}' AS job_run_id, CURRENT_TIMESTAMP() AS gold_modelled_at
FROM monitoring.cfg_referral_scope
WHERE COALESCE(is_active, false)
  AND (valid_from IS NULL OR valid_from <= CURRENT_DATE())
  AND (valid_to IS NULL OR valid_to >= CURRENT_DATE())
""")

# GLD-006/GLD-007: person dimension with the legacy "Gender Clean" mapping.
# One current row per person; fact_referral[person_id] relates to this
# dimension for the gender KPIs (KPI-04-07). Null/unrecognised gender
# becomes "Unknown", matching the legacy model behaviour.
require_columns(
    "silver.referral_person",
    ["person_id", "initials", "age_value", "age_date_unit", "has_restrictions",
     "gender", "ethnicity", "religion", "preferred_language", "export_date",
     "source_reference_id"],
)
person_current = (
    spark.table("silver.referral_person")
    .withColumn(
        "_gold_dimension_rank",
        F.row_number().over(
            Window.partitionBy("person_id").orderBy(
                F.col("export_date").cast("timestamp").desc_nulls_last(),
                F.col("_silver_load_ts").cast("timestamp").desc_nulls_last(),
                F.col("source_reference_id").asc_nulls_last(),
            )
        ),
    )
    .where(F.col("_gold_dimension_rank") == 1)
)
dim_person = person_current.select(
    F.col("person_id").alias("person_id"),
    # A source person reference, not a unique referral key. Preserve leading zeros.
    F.when(F.trim(F.col("source_reference_id")) != "",
           F.trim(F.col("source_reference_id").cast("string")))
    .alias("source_reference_id"),
    F.col("initials").alias("initials"),
    F.col("age_value").alias("age_value"),
    F.col("age_date_unit").alias("age_date_unit"),
    F.col("has_restrictions").alias("has_restrictions"),
    F.col("gender").alias("gender"),
    F.when(F.col("gender") == "Male", "Male")
    .when(F.col("gender") == "Female", "Female")
    .when(F.col("gender").isin("Another Gender", "Other"), "Other")
    .otherwise("Unknown")
    .alias("gender_clean"),
    F.col("ethnicity").alias("ethnicity"),
    F.col("religion").alias("religion"),
    F.col("preferred_language").alias("preferred_language"),
    F.col("export_date").cast("timestamp").alias("export_date"),
    F.lit(GOLD_JOB_RUN_ID).alias("job_run_id"),
    F.col("export_date").alias("source_export_date"),
)
(dim_person.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_person"))
print(f"gold.dim_person: {dim_person.count():,} rows from silver.referral_person")

# GLD-008: offer-status dimension with labels and lifecycle flags, rebuilt
# from the distinct offer_status codes observed in Silver. Unknown future
# codes are kept with a null label, matching the legacy model behaviour.
require_columns("silver.offer", ["offer_status", "export_date"])
offer_statuses = (
    spark.table("silver.offer")
    .select(
        F.col("offer_status").alias("offer_status"),
        F.col("export_date").cast("timestamp").alias("export_date"),
    )
    .where(F.col("offer_status").isNotNull() & (F.trim(F.col("offer_status")) != ""))
    .groupBy("offer_status").agg(F.max("export_date").alias("export_date"))
    .withColumn(
        "offer_status_label",
        F.when(F.col("offer_status") == "OFFER_SUCCESSFUL", "Accepted")
        .when(F.col("offer_status") == "DRAFT", "Draft")
        .when(F.col("offer_status") == "OFFER_MADE", "Pending")
        .when(F.col("offer_status") == "OFFER_UNSUCCESSFUL", "Unsuccessful")
        .when(F.col("offer_status") == "OFFER_WITHDRAWN", "Withdrawn"),
    )
    .withColumn("is_active_offer", F.col("offer_status") == "OFFER_MADE")
    .withColumn("is_accepted", F.col("offer_status") == "OFFER_SUCCESSFUL")
    .withColumn(
        "is_terminal",
        F.col("offer_status").isin("OFFER_UNSUCCESSFUL", "OFFER_WITHDRAWN"),
    )
    .withColumn(
        "offer_status_sk",
        F.row_number().over(Window.orderBy("offer_status")),
    )
    .select(
        "offer_status_sk", "offer_status", "offer_status_label",
        "is_active_offer", "is_accepted", "is_terminal", "export_date",
    )
    .withColumn("job_run_id", F.lit(GOLD_JOB_RUN_ID))
    .withColumn("gold_modelled_at", F.current_timestamp())
)
(offer_statuses.write.format("delta").mode("overwrite")
    .option("overwriteSchema", "true").saveAsTable("gold.dim_offer_status"))
print(f"gold.dim_offer_status: {offer_statuses.count():,} rows from silver.offer")
```

<a id="python-05-gold-dimensions-py-210"></a>
## 05_gold_dimensions.py:210

Source: [project X/05_gold_dimensions.py:210](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L210).

```python
copy_bridge(
    "silver.referral_category", "gold.bridge_referral_framework_category",
    ["referral_id", "framework_category_id", "export_date"],
    [("referral_id", "referral_id"), ("framework_category_id", "framework_category_id"),
     ("export_date", "source_export_date")],
    key_columns=["referral_id", "framework_category_id"],
)
```

<a id="python-05-gold-dimensions-py-239"></a>
## 05_gold_dimensions.py:239

Source: [project X/05_gold_dimensions.py:239](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L239).

```python
latest_dimension(
    "silver.provider_submission_docs", "gold.dim_provider_submission_document", ["document_id"],
    [("document_id", "document_id"), ("submission_id", "submission_id"),
     ("s3_file_metadata_id", "s3_file_metadata_id"), ("document_name", "document_name"),
     ("document_type", "document_type"), ("expiry_date", "expiry_date"),
     ("last_updated", "last_updated"), ("next_review_date", "next_review_date"),
     ("service_type", "service_type"), ("home_id", "home_id"),
     ("start_date", "start_date"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-253"></a>
## 05_gold_dimensions.py:253

Source: [project X/05_gold_dimensions.py:253](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L253).

```python
latest_dimension(
    "silver.referral_provider_message", "gold.dim_referral_provider_message", ["message_id"],
    [("message_id", "message_id"), ("referral_provider_id", "referral_provider_id"),
     ("message_read_by", "message_read_by"),
     ("message_read_timestamp", "message_read_timestamp"),
     ("message_text", "message_text"), ("created_timestamp", "created_timestamp"),
     ("created_by", "created_by"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-390"></a>
## 05_gold_dimensions.py:390

Source: [project X/05_gold_dimensions.py:390](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L390).

```python
spark.sql(f"""
CREATE OR REPLACE TABLE gold.dim_snapshot_month AS
SELECT
  date_value AS month_start,
  LAST_DAY(date_value) AS month_end,
  YEAR(date_value) AS calendar_year,
  MONTH(date_value) AS calendar_month_number,
  DATE_FORMAT(date_value, 'MMMM') AS calendar_month_name,
  DATE_FORMAT(date_value, 'yyyy-MM') AS year_month,
  CAST('{GOLD_EXPORT_DATE}' AS TIMESTAMP) AS export_date,
  '{GOLD_JOB_RUN_ID}' AS job_run_id,
  CURRENT_TIMESTAMP() AS gold_modelled_at
FROM (
  SELECT EXPLODE(SEQUENCE(DATE '2020-01-01', DATE '2035-12-01', INTERVAL 1 MONTH)) AS date_value
)
""")
```

<a id="python-06-reports-py-45"></a>
## 06_reports.py:45

Source: [project X/06_reports.py:45](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L45).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_step_timing AS
WITH ordered_steps AS (
  SELECT
    job_run_id, step_sequence, notebook_name, started_at, ended_at, status,
    child_result, error_message,
    LAG(ended_at) OVER (PARTITION BY job_run_id ORDER BY step_sequence) AS previous_step_ended_at
  FROM monitoring.cfg_job_step_run
)
SELECT
  job_run_id, step_sequence, notebook_name, status, started_at, ended_at,
  ROUND(unix_timestamp(coalesce(ended_at, current_timestamp())) - unix_timestamp(started_at), 2) AS step_duration_seconds,
  ROUND(unix_timestamp(started_at) - unix_timestamp(previous_step_ended_at), 2) AS gap_from_previous_step_seconds,
  child_result, error_message
FROM ordered_steps
""")
```

<a id="python-06-reports-py-74"></a>
## 06_reports.py:74

Source: [project X/06_reports.py:74](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L74).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_step_summary AS
WITH pipeline AS (
  SELECT job_run_id, pipeline_name, status, rows_read, rows_written,
         tables_succeeded, tables_failed, error_message
  FROM monitoring.cfg_pipeline_run
  WHERE job_run_id IS NOT NULL
), metric AS (
  SELECT job_run_id,
    CASE WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
         WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END AS notebook_name,
    COUNT(DISTINCT target_object) AS target_count,
    SUM(rows_read) AS rows_read, SUM(rows_written) AS rows_written,
    SUM(duplicate_key_count) AS duplicate_rows, SUM(null_primary_key_count) AS null_primary_keys
  FROM monitoring.cfg_table_load_metric
  WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, CASE WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
                            WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END
), dq AS (
  SELECT job_run_id, COUNT(*) AS checks_run,
    SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) AS checks_passed,
    SUM(CASE WHEN status IN ('FAIL', 'ERROR') THEN 1 ELSE 0 END) AS checks_failed,
    SUM(failed_row_count) AS failed_row_count
  FROM monitoring.cfg_data_quality_result
  WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), drift AS (
  SELECT job_run_id,
    CASE WHEN source_kind = 'LIVE' THEN '01a_cfg_schema_capture_live'
         WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
         WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END AS notebook_name,
    COUNT(*) AS drift_event_count,
    SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_drift_count
  FROM monitoring.cfg_schema_drift_event
  WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, CASE WHEN source_kind = 'LIVE' THEN '01a_cfg_schema_capture_live'
                             WHEN source_kind = 'LATEST' THEN '02_silver_formatter'
                             WHEN source_kind LIKE 'ARCHIVE%' THEN '02a_archive_silver' END
)
SELECT s.*, p.rows_read AS pipeline_rows_read, p.rows_written AS pipeline_rows_written,
  p.tables_succeeded, p.tables_failed, p.error_message AS pipeline_error_message,
  m.target_count, m.rows_read AS metric_rows_read, m.rows_written AS metric_rows_written,
  m.duplicate_rows, m.null_primary_keys,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_run END AS dq_checks_run,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_passed END AS dq_checks_passed,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.checks_failed END AS dq_checks_failed,
  CASE WHEN s.notebook_name = '03_silver_business_rules' THEN dq.failed_row_count END AS dq_failed_row_count,
  d.drift_event_count, d.active_drift_count
FROM monitoring.rpt_job_step_timing s
LEFT JOIN pipeline p ON p.job_run_id = s.job_run_id
  AND p.pipeline_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
LEFT JOIN metric m ON m.job_run_id = s.job_run_id
  AND m.notebook_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
LEFT JOIN dq ON dq.job_run_id = s.job_run_id
LEFT JOIN drift d ON d.job_run_id = s.job_run_id
  AND d.notebook_name = regexp_replace(s.notebook_name, '\\.ipynb$', '')
""")
```

<a id="python-06-reports-py-141"></a>
## 06_reports.py:141

Source: [project X/06_reports.py:141](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L141).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_run_summary AS
WITH metric AS (
  SELECT job_run_id, COUNT(DISTINCT target_object) AS silver_targets,
         SUM(rows_read) AS rows_read, SUM(rows_written) AS rows_written,
         SUM(duplicate_key_count) AS duplicate_rows
  FROM monitoring.cfg_table_load_metric WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), dq AS (
  SELECT job_run_id, COUNT(*) AS dq_checks,
         SUM(CASE WHEN status IN ('FAIL', 'ERROR') THEN 1 ELSE 0 END) AS dq_failures
  FROM monitoring.cfg_data_quality_result WHERE job_run_id IS NOT NULL GROUP BY job_run_id
), drift AS (
  SELECT job_run_id, COUNT(*) AS drift_events,
         SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) AS active_drift_events
  FROM monitoring.cfg_schema_drift_event WHERE job_run_id IS NOT NULL GROUP BY job_run_id
)
SELECT j.*, ROUND(unix_timestamp(coalesce(j.ended_at, current_timestamp())) - unix_timestamp(j.started_at), 2) AS job_duration_seconds,
  m.silver_targets, m.rows_read, m.rows_written, m.duplicate_rows,
  dq.dq_checks, dq.dq_failures, drift.drift_events, drift.active_drift_events
FROM monitoring.cfg_job_run j
LEFT JOIN metric m ON m.job_run_id = j.job_run_id
LEFT JOIN dq ON dq.job_run_id = j.job_run_id
LEFT JOIN drift ON drift.job_run_id = j.job_run_id
""")
```

<a id="python-06-reports-py-177"></a>
## 06_reports.py:177

Source: [project X/06_reports.py:177](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L177).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_schema_drift AS
SELECT e.job_run_id, e.run_id, e.source_kind, e.source_table, e.target_table,
  e.drift_type, e.column_name, e.expected_type, e.actual_type,
  e.referenced_table, e.referenced_column, e.status, e.occurrence_count,
  e.first_detected_at, e.last_detected_at, e.resolved_at,
  d.definition_hash, d.join_class, d.join_evidence,
  CASE WHEN d.table_name IS NULL THEN false ELSE true END AS definition_match_found
FROM monitoring.cfg_schema_drift_event e
LEFT JOIN monitoring.cfg_schema_drift_definition d
  ON lower(d.table_name) = lower(regexp_replace(e.source_table, '^[^.]+\\.', ''))
 AND (e.column_name IS NULL OR lower(d.column_name) = lower(e.column_name))
""")
```

<a id="python-06-reports-py-202"></a>
## 06_reports.py:202

Source: [project X/06_reports.py:202](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L202).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_data_quality AS
WITH rejected AS (
  SELECT job_run_id, run_id, rule_id, COUNT(*) AS rejected_key_count
  FROM monitoring.cfg_rejected_row WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, run_id, rule_id
), exceptions AS (
  SELECT job_run_id, run_id, rule_id, COUNT(*) AS referential_exception_count
  FROM monitoring.cfg_referential_exception WHERE job_run_id IS NOT NULL
  GROUP BY job_run_id, run_id, rule_id
)
SELECT r.job_run_id, r.run_id, r.rule_id, r.severity, r.rule_type,
  r.source_table, r.column_name, r.status, r.checked_row_count,
  r.failed_row_count, r.failure_percentage, r.sample_key_json, r.checked_at,
  r.message, coalesce(x.rejected_key_count, 0) AS rejected_key_count,
  coalesce(e.referential_exception_count, 0) AS referential_exception_count
FROM monitoring.cfg_data_quality_result r
LEFT JOIN rejected x ON x.job_run_id = r.job_run_id AND x.run_id = r.run_id AND x.rule_id = r.rule_id
LEFT JOIN exceptions e ON e.job_run_id = r.job_run_id AND e.run_id = r.run_id AND e.rule_id = r.rule_id
WHERE r.job_run_id IS NOT NULL
""")
```

<a id="python-06-reports-py-235"></a>
## 06_reports.py:235

Source: [project X/06_reports.py:235](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L235).

```python
spark.sql("""
CREATE MATERIALIZED LAKE VIEW IF NOT EXISTS monitoring.rpt_job_layer_lineage AS
SELECT a.job_run_id,
  CASE WHEN a.source_kind = 'LATEST' THEN 'BRONZE' ELSE 'ARCHIVE' END AS source_layer,
  a.source_table AS source_object, 'SILVER' AS target_layer, a.target_table AS target_object,
  'SOURCE_TO_SILVER' AS lineage_stage,
  CASE WHEN a.status = 'SUCCESS' THEN 'MATCHED' ELSE a.status END AS lineage_status,
  a.rows_read, a.rows_written, a.duplicate_key_count, a.export_date AS observed_at,
  CAST(NULL AS STRING) AS relationship_role
FROM monitoring.cfg_silver_export_load a
WHERE a.job_run_id IS NOT NULL
UNION ALL
SELECT s.job_run_id, m.source_layer, m.source_object, 'GOLD', m.gold_object,
  'SILVER_TO_GOLD',
  CASE WHEN s.status = 'SUCCESS' THEN 'MATCHED' ELSE s.status END,
  CAST(NULL AS BIGINT), CAST(NULL AS BIGINT), CAST(NULL AS BIGINT), s.ended_at,
  m.relationship_role
FROM monitoring.cfg_job_step_run s
INNER JOIN monitoring.cfg_gold_lineage_mapping m
  ON m.transformation_notebook = regexp_replace(s.notebook_name, '\\.ipynb$', '')
WHERE s.notebook_name IN ('04_gold_model', '05_gold_dimensions', '04_gold_model.ipynb', '05_gold_dimensions.ipynb')
""")
```

<a id="python-90-run-archive-pipeline-py-144"></a>
## 90_run_archive_pipeline.py:144

Source: [project X/90_run_archive_pipeline.py:144](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/90_run_archive_pipeline.py#L144).

```python
import uuid
from datetime import datetime, timezone

from notebookutils import mssparkutils

PIPELINE_NAME = "90_run_archive_pipeline"
JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())
started_at = datetime.now(timezone.utc)
results = []
def record_step(step_sequence, notebook_name, status, step_started,
                child_result=None, error_message=None):
    merge_monitor_row(
        "monitoring.cfg_job_step_run",
        (JOB_RUN_ID, step_sequence, notebook_name, step_started,
         None if status == "RUNNING" else datetime.now(timezone.utc), status,
         child_result[:4000] if child_result else None,
         error_message[:4000] if error_message else None, datetime.now(timezone.utc)),
        "job_run_id string,step_sequence int,notebook_name string,started_at timestamp,ended_at timestamp,status string,child_result string,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence",
    )


# Setup is deliberately first: it creates or upgrades the two orchestration
# monitor tables before this runner writes its first status record.
setup_name, setup_parameters = ARCHIVE_STEPS[0]
setup_started = datetime.now(timezone.utc)
print(f"JOB_RUN_ID={JOB_RUN_ID}")
print(f"=== START {setup_name} ===")
try:
    setup_result = mssparkutils.notebook.run(
        setup_name, NOTEBOOK_TIMEOUT_SECONDS,
        {**setup_parameters, "JOB_RUN_ID": JOB_RUN_ID},
    )
except Exception:
    # Monitoring tables may not yet exist, so Fabric's notebook error is the
    # authoritative failure record for a failed setup bootstrap.
    raise

merge_monitor_row(
    "monitoring.cfg_job_run",
    (JOB_RUN_ID, PIPELINE_NAME, started_at, None, "RUNNING", 1, 0, None,
     datetime.now(timezone.utc)),
    "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
    "target.job_run_id = source.job_run_id",
)
record_step(1, setup_name, "SUCCESS", setup_started, str(setup_result))
results.append((setup_name, "SUCCESS", str(setup_result)))
print(f"=== SUCCESS {setup_name} ===")

try:
    for step_sequence, (notebook_name, parameters) in enumerate(ARCHIVE_STEPS[1:], start=2):
        step_started = datetime.now(timezone.utc)
        print(f"=== START {notebook_name}; JOB_RUN_ID={JOB_RUN_ID} ===")
        record_step(step_sequence, notebook_name, "RUNNING", step_started)
        try:
            result = mssparkutils.notebook.run(
                notebook_name, NOTEBOOK_TIMEOUT_SECONDS,
                {**parameters, "JOB_RUN_ID": JOB_RUN_ID},
            )
            result_text = str(result)
            record_step(step_sequence, notebook_name, "SUCCESS", step_started,
                        child_result=result_text)
            results.append((notebook_name, "SUCCESS", result_text))
            print(f"=== SUCCESS {notebook_name} ===")
        except Exception as exc:
            error_text = str(exc)[:4000]
            record_step(step_sequence, notebook_name, "FAILED", step_started,
                        error_message=error_text)
            results.append((notebook_name, "FAILED", error_text))
            print(f"=== FAILED {notebook_name}: {error_text} ===")
            if STOP_ON_ERROR:
                raise
finally:
    failed = [name for name, status, _ in results if status == "FAILED"]
    succeeded = sum(1 for _, status, _ in results if status == "SUCCESS")
    status = "FAILED" if failed else "SUCCESS"
    error_message = f"Failed notebook(s): {failed}" if failed else None
    merge_monitor_row(
        "monitoring.cfg_job_run",
        (JOB_RUN_ID, PIPELINE_NAME, started_at, datetime.now(timezone.utc), status,
         succeeded, len(failed), error_message, datetime.now(timezone.utc)),
        "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id",
    )

    # 06_reports only creates missing views; publish all six after closing the job.
    try:
        for view in (
            "rpt_job_step_timing",
            "rpt_job_step_summary",
            "rpt_job_run_summary",
            "rpt_job_schema_drift",
            "rpt_job_data_quality",
            "rpt_job_layer_lineage",
        ):
            spark.sql(
                f"REFRESH MATERIALIZED LAKE VIEW monitoring.{view} FULL"
            )
    except Exception as refresh_error:
        # A reporting refresh failure must not mask the original ETL outcome.
        print(f"WARNING: Monitoring refresh failed: {refresh_error}")

failed = [name for name, status, _ in results if status == "FAILED"]
print(
    f"Archive pipeline {status}; JOB_RUN_ID={JOB_RUN_ID}; "
    f"started={started_at.isoformat()}; results={results}"
)
if failed:
    raise RuntimeError(f"Archive pipeline failed notebook(s): {failed}")
```

<a id="python-90-run-live-pipeline-py-78"></a>
## 90_run_live_pipeline.py:78

Source: [project X/90_run_live_pipeline.py:78](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/90_run_live_pipeline.py#L78).

```python
import uuid
from datetime import datetime, timezone

from notebookutils import mssparkutils

PIPELINE_NAME = "90_run_live_pipeline"
JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())
FORCE_RERUN = str(FORCE_RERUN).strip().lower() in {"true", "1", "yes", "y"}
RUN_ESSENTIAL_DQ = str(RUN_ESSENTIAL_DQ).strip().lower() in {"true", "1", "yes", "y"}
started_at = datetime.now(timezone.utc)
results = []
def record_step(step_sequence, notebook_name, status, step_started,
                child_result=None, error_message=None):
    merge_monitor_row(
        "monitoring.cfg_job_step_run",
        (JOB_RUN_ID, step_sequence, notebook_name, step_started,
         None if status == "RUNNING" else datetime.now(timezone.utc), status,
         child_result[:4000] if child_result else None,
         error_message[:4000] if error_message else None, datetime.now(timezone.utc)),
        "job_run_id string,step_sequence int,notebook_name string,started_at timestamp,ended_at timestamp,status string,child_result string,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence",
    )


# Setup is deliberately first: it creates or upgrades the two orchestration
# monitor tables before this runner writes its first status record.
setup_name, setup_parameters = LIVE_STEPS[0]
setup_started = datetime.now(timezone.utc)
print(f"JOB_RUN_ID={JOB_RUN_ID}")
print(f"FORCE_RERUN={FORCE_RERUN}")
print(f"RUN_ESSENTIAL_DQ={RUN_ESSENTIAL_DQ}")
print(f"=== START {setup_name} ===")
try:
    setup_result = mssparkutils.notebook.run(
        setup_name, NOTEBOOK_TIMEOUT_SECONDS,
        {**setup_parameters, "JOB_RUN_ID": JOB_RUN_ID},
    )
except Exception:
    # Monitoring tables may not yet exist, so Fabric's notebook error is the
    # authoritative failure record for a failed setup bootstrap.
    raise

merge_monitor_row(
    "monitoring.cfg_job_run",
    (JOB_RUN_ID, PIPELINE_NAME, started_at, None, "RUNNING", 1, 0, None,
     datetime.now(timezone.utc)),
    "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
    "target.job_run_id = source.job_run_id",
)
record_step(1, setup_name, "SUCCESS", setup_started, str(setup_result))
results.append((setup_name, "SUCCESS", str(setup_result)))
print(f"=== SUCCESS {setup_name} ===")

try:
    for step_sequence, (notebook_name, parameters) in enumerate(LIVE_STEPS[1:], start=2):
        step_started = datetime.now(timezone.utc)
        print(f"=== START {notebook_name}; JOB_RUN_ID={JOB_RUN_ID} ===")
        record_step(step_sequence, notebook_name, "RUNNING", step_started)
        try:
            child_parameters = {**parameters, "JOB_RUN_ID": JOB_RUN_ID}
            if notebook_name == "02_silver_formatter":
                child_parameters["FORCE_RERUN"] = str(FORCE_RERUN).lower()
            if notebook_name == "03_silver_business_rules":
                child_parameters["RUN_ESSENTIAL_DQ"] = str(RUN_ESSENTIAL_DQ).lower()
                child_parameters["DEFAULT_LOCATION_CITY"] = DEFAULT_LOCATION_CITY
            result = mssparkutils.notebook.run(
                notebook_name, NOTEBOOK_TIMEOUT_SECONDS,
                child_parameters,
            )
            result_text = str(result)
            record_step(step_sequence, notebook_name, "SUCCESS", step_started,
                        child_result=result_text)
            results.append((notebook_name, "SUCCESS", result_text))
            print(f"=== SUCCESS {notebook_name} ===")
        except Exception as exc:
            error_text = str(exc)[:4000]
            record_step(step_sequence, notebook_name, "FAILED", step_started,
                        error_message=error_text)
            results.append((notebook_name, "FAILED", error_text))
            print(f"=== FAILED {notebook_name}: {error_text} ===")
            if STOP_ON_ERROR:
                raise
finally:
    failed = [name for name, status, _ in results if status == "FAILED"]
    succeeded = sum(1 for _, status, _ in results if status == "SUCCESS")
    status = "FAILED" if failed else "SUCCESS"
    error_message = f"Failed notebook(s): {failed}" if failed else None
    merge_monitor_row(
        "monitoring.cfg_job_run",
        (JOB_RUN_ID, PIPELINE_NAME, started_at, datetime.now(timezone.utc), status,
         succeeded, len(failed), error_message, datetime.now(timezone.utc)),
        "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id",
    )

    # 06_reports only creates missing views; publish all six after closing the job.
    try:
        for view in (
            "rpt_job_step_timing",
            "rpt_job_step_summary",
            "rpt_job_run_summary",
            "rpt_job_schema_drift",
            "rpt_job_data_quality",
            "rpt_job_layer_lineage",
        ):
            spark.sql(
                f"REFRESH MATERIALIZED LAKE VIEW monitoring.{view} FULL"
            )
    except Exception as refresh_error:
        # A reporting refresh failure must not mask the original ETL outcome.
        print(f"WARNING: Monitoring refresh failed: {refresh_error}")

failed = [name for name, status, _ in results if status == "FAILED"]
print(
    f"Live pipeline {status}; JOB_RUN_ID={JOB_RUN_ID}; "
    f"started={started_at.isoformat()}; results={results}"
)
if failed:
    raise RuntimeError(f"Live pipeline failed notebook(s): {failed}")
```

<a id="python-99-common-library-py-124"></a>
## 99_common_library.py:124

Source: [project X/99_common_library.py:124](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/99_common_library.py#L124).

```python
def qident(value):
    return "`" + str(value).replace("`", "``") + "`"


def normalise(value):
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def append_rows(table_name, rows, schema):
    if rows:
        spark.createDataFrame(rows, schema).write.format("delta").mode("append").saveAsTable(table_name)


def merge_monitor_row(table_name, row, schema, condition):
    """Upsert one parent-job or child-step monitoring record."""
    source = spark.createDataFrame([row], schema)
    target = DeltaTable.forName(spark, table_name)
    (target.alias("target").merge(source.alias("source"), condition)
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())


def drift_event_row(source_kind, source_table, target_table, drift_type,
                    column_name=None, expected_type=None, actual_type=None,
                    referenced_table=None, referenced_column=None):
    """Build a consistently keyed Silver schema-drift monitoring row."""
    now = datetime.now(timezone.utc)
    identity = "||".join(str(value or "") for value in (
        source_kind, source_table, column_name, drift_type,
        referenced_table, referenced_column,
    ))
    drift_key = str(uuid.uuid5(uuid.NAMESPACE_URL, identity))
    return (
        RUN_ID, source_kind, source_table, target_table, drift_type,
        column_name, expected_type, actual_type, referenced_table,
        referenced_column, drift_key, "ACTIVE", 1, now, now, None, now, JOB_RUN_ID or None,
    )


def map_data_type(pg_type):
    value = (pg_type or "").lower().strip()
    if "[]" in value:
        return "ARRAY<STRING>"
    if any(token in value for token in ("uuid", "json", "text", "character", "varchar")):
        return "STRING"
    if value in {"smallint", "int2", "integer", "int", "int4"}:
        return "INT"
    if value in {"bigint", "int8"}:
        return "BIGINT"
    match = re.search(r"(?:numeric|decimal)\s*\((\d+)\s*,\s*(\d+)\)", value)
    if match:
        precision = min(int(match.group(1)), 38)
        scale = min(int(match.group(2)), precision)
        return f"DECIMAL({precision},{scale})"
    if "numeric" in value or "decimal" in value:
        return "DECIMAL(38,18)"
    if any(token in value for token in ("double", "float", "real")):
        return "DOUBLE"
    if "boolean" in value or value == "bool":
        return "BOOLEAN"
    if value == "date":
        return "DATE"
    if "timestamp" in value:
        return "TIMESTAMP"
    return "STRING"


def first_parsed(column, formats, parser):
    return F.coalesce(*[parser(column, fmt) for fmt in formats])


def cast_column(frame, definition):
    name = definition["column_name"]
    spark_type = map_data_type(definition["data_type"])
    if name not in frame.columns:
        return F.lit(None).cast(spark_type).alias(name)
    source = F.col(qident(name))
    if spark_type == "BOOLEAN":
        clean = F.lower(F.trim(source.cast("string")))
        return (F.when(clean.isin("true", "t", "1", "yes", "y"), F.lit(True))
            .when(clean.isin("false", "f", "0", "no", "n"), F.lit(False))
            .otherwise(F.lit(None).cast("boolean")).alias(name))
    if spark_type == "DATE":
        return first_parsed(source.cast("string"), DATE_FORMATS, F.to_date).alias(name)
    if spark_type == "TIMESTAMP":
        return first_parsed(source.cast("string"), TIMESTAMP_FORMATS, F.to_timestamp).alias(name)
    if spark_type.startswith("DECIMAL") or spark_type in {"INT", "BIGINT", "DOUBLE"}:
        return F.regexp_replace(source.cast("string"), r"[^0-9eE+\.\-]", "").cast(spark_type).alias(name)
    if spark_type == "ARRAY<STRING>":
        return F.when(source.isNull(), F.lit(None).cast("array<string>"))             .otherwise(F.split(F.regexp_replace(source.cast("string"), r"^[\{\[]|[\}\]]$", ""), r"\s*,\s*")).alias(name)
    return F.trim(source.cast("string")).alias(name)


def resolve_contract(physical_table, prefixes):
    base = physical_table.lower()
    for prefix in prefixes:
        if base.startswith(prefix):
            base = base[len(prefix):]
    matches = contracts_by_table.get(normalise(base), [])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous table contract for {physical_table}: {matches}")
    return None


def primary_key_columns(schema_cols):
    """Return the ordered business key defined by the schema contract."""
    return [
        column["column_name"] for column in schema_cols
        if (column.get("is_primary_key") or "").upper() == "YES"
    ]


def deduplicate_frame(frame, schema_cols):
    """Keep one row per contracted PK without triggering count jobs here."""
    key_columns = primary_key_columns(schema_cols)
    if not key_columns:
        return frame, key_columns
    if "_archive_load_ts" in frame.columns:
        ordering = F.col("_archive_load_ts").cast("timestamp").desc_nulls_last()
    elif "_ingestion_timestamp" in frame.columns:
        ordering = F.col("_ingestion_timestamp").cast("timestamp").desc_nulls_last()
    else:
        ordering = F.col(qident("export_date")).cast("timestamp").desc_nulls_last()
    window = Window.partitionBy(
        *[F.col(qident(column)) for column in key_columns]
    ).orderBy(ordering)
    ranked = frame.withColumn("_silver_row_number", F.row_number().over(window))
    return ranked.where(F.col("_silver_row_number") == 1).drop("_silver_row_number"), key_columns


def diagnostic_key_sample(frame, key_columns):
    """Collect a small identifier-only sample for operational tracing."""
    if not VERBOSE_DIAGNOSTICS or not key_columns:
        return []
    return [
        row.asDict(recursive=True)
        for row in frame.select(*[F.col(qident(column)) for column in key_columns])
            .limit(DIAGNOSTIC_KEY_SAMPLE_SIZE).collect()
    ]


def print_load_diagnostics(source_table, target_table, snapshot_date, source_date,
                           raw_frame, formatted_frame, key_columns,
                           source_count, written_count, duplicate_count,
                           formatted_export_non_null):
    """Print dates, counts and PK identifiers needed to diagnose a batch."""
    if not VERBOSE_DIAGNOSTICS:
        return
    raw_export_type = next(
        field.dataType.simpleString() for field in raw_frame.schema.fields
        if field.name == "export_date"
    )
    formatted_dates = [
        str(row["export_date"])
        for row in formatted_frame.select(F.to_date("export_date").alias("export_date"))
            .where(F.col("export_date").isNotNull()).distinct().orderBy("export_date").collect()
    ]
    print(f"  Source: {source_table}; selected export={source_date}; raw type={raw_export_type}")
    print(f"  Target: {target_table}; Gold snapshot={snapshot_date}")
    print(f"  Rows: source={source_count:,}; written={written_count:,}; duplicates removed={duplicate_count:,}")
    print(f"  Primary keys: {key_columns or ['<none>']}")
    print(f"  Primary-key sample: {diagnostic_key_sample(formatted_frame, key_columns)}")
    print(
        f"  Silver export_date: non-null={formatted_export_non_null:,}; "
        f"null={written_count - formatted_export_non_null:,}; values={formatted_dates}"
    )


# SI-025: every Bronze/Archive frame carries a row-level export_date (the
# formatters reject sources without one), so every Silver table must publish
# it. A deployed cfg_schema_contract_column that pre-dates the export_date
# contract rows would otherwise silently drop the column; the bootstrap only
# loads the CSV into an empty table, so the stale contract never self-heals.
# Patch the in-memory contract instead: the Silver write gains export_date,
# the drift check stops reporting it as EXTRA, and target_requires_refresh
# flags existing Silver tables that lack the column for rebuild.
EXPORT_DATE_CONTRACT_COLUMN = {
    "ordinal_position": 999999,
    "column_name": "export_date",
    "data_type": "timestamp without time zone",
    "is_primary_key": "NO",
    "referenced_table": "",
    "referenced_column": "",
}


def ensure_export_date_contract(schema_cols):
    """Append the export_date contract column when the deployed contract lacks it."""
    if any(definition["column_name"].lower() == "export_date" for definition in schema_cols):
        return schema_cols
    return [*schema_cols, dict(EXPORT_DATE_CONTRACT_COLUMN)]


def format_frame(frame, schema_cols, source_kind, source_table):
    expressions = [cast_column(frame, definition) for definition in schema_cols]
    return (frame.select(*expressions)
        .withColumn("_record_source", F.lit(source_kind))
        .withColumn("_source_table", F.lit(source_table))
        .withColumn("_silver_run_id", F.lit(RUN_ID))
        .withColumn("job_run_id", F.lit(JOB_RUN_ID).cast("string"))
        .withColumn("_silver_load_ts", F.current_timestamp()))


AUDIT_SCHEMA = StructType([
    StructField("source_kind", StringType(), False),
    StructField("source_schema", StringType(), False),
    StructField("source_table", StringType(), False),
    StructField("target_table", StringType(), True),
    StructField("export_date", TimestampType(), False),
    StructField("status", StringType(), False),
    StructField("reload", BooleanType(), False),
    StructField("attempt_count", IntegerType(), False),
    StructField("run_id", StringType(), True),
    StructField("rows_read", LongType(), True),
    StructField("rows_written", LongType(), True),
    StructField("duplicate_key_count", LongType(), True),
    StructField("started_at", TimestampType(), True),
    StructField("ended_at", TimestampType(), True),
    StructField("error_message", StringType(), True),
    StructField("last_updated_at", TimestampType(), True),
    StructField("job_run_id", StringType(), True),
])


def audit_record(source_kind, source_schema, source_table, export_date):
    rows = (spark.table(AUDIT_TABLE)
        .where((F.col("source_kind") == source_kind)
            & (F.col("source_schema") == source_schema)
            & (F.col("source_table") == source_table)
            & (F.col("export_date") == F.lit(export_date).cast("timestamp")))
        .limit(1).collect())
    return rows[0].asDict() if rows else None


def should_skip(source_kind, source_schema, source_table, export_date):
    record = audit_record(source_kind, source_schema, source_table, export_date)
    return bool(record and record["status"] == "SUCCESS" and not record["reload"])


def audit_begin(source_kind, source_schema, source_table, target_table, export_date):
    now = datetime.now(timezone.utc)
    existing = audit_record(source_kind, source_schema, source_table, export_date)
    attempt_count = int(existing["attempt_count"] or 0) + 1 if existing else 1
    row = [(source_kind, source_schema, source_table, target_table, export_date, "RUNNING",
            bool(existing["reload"]) if existing else False, attempt_count, RUN_ID,
            None, None, None, now, None, None, now, JOB_RUN_ID or None)]
    source = spark.createDataFrame(row, AUDIT_SCHEMA)
    target = DeltaTable.forName(spark, AUDIT_TABLE)
    condition = " AND ".join([
        "t.source_kind = s.source_kind", "t.source_schema = s.source_schema",
        "t.source_table = s.source_table", "t.export_date = s.export_date",
    ])
    (target.alias("t").merge(source.alias("s"), condition)
        .whenMatchedUpdate(set={
            "target_table": "s.target_table", "status": "s.status",
            "attempt_count": "s.attempt_count", "run_id": "s.run_id",
            "started_at": "s.started_at", "ended_at": "s.ended_at",
            "error_message": "s.error_message", "last_updated_at": "s.last_updated_at",
            "job_run_id": "s.job_run_id",
        }).whenNotMatchedInsertAll().execute())


def audit_finish(source_kind, source_schema, source_table, target_table, export_date,
                 status, rows_read=0, rows_written=0, duplicate_count=0, error_message=None):
    now = datetime.now(timezone.utc)
    existing = audit_record(source_kind, source_schema, source_table, export_date) or {}
    row = [(source_kind, source_schema, source_table, target_table, export_date, status,
            False if status == "SUCCESS" else bool(existing.get("reload", False)),
            int(existing.get("attempt_count") or 1), RUN_ID, int(rows_read), int(rows_written),
            int(duplicate_count), existing.get("started_at") or now, now,
            error_message[:4000] if error_message else None, now, JOB_RUN_ID or None)]
    source = spark.createDataFrame(row, AUDIT_SCHEMA)
    target = DeltaTable.forName(spark, AUDIT_TABLE)
    condition = " AND ".join([
        "t.source_kind = s.source_kind", "t.source_schema = s.source_schema",
        "t.source_table = s.source_table", "t.export_date = s.export_date",
    ])
    (target.alias("t").merge(source.alias("s"), condition)
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())
```

<a id="python-99-common-library-py-462"></a>
## 99_common_library.py:462

Source: [project X/99_common_library.py:462](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/99_common_library.py#L462).

```python
DATA_DOMAIN_SCHEMA = StructType([
    StructField("source_schema", StringType(), False),
    StructField("source_table", StringType(), False),
    StructField("column_name", StringType(), False),
    StructField("contract_data_type", StringType(), True),
    StructField("data_domain", StringType(), False),
    StructField("distinct_value_count", LongType(), False),
    StructField("profiled_at", TimestampType(), False),
    StructField("run_id", StringType(), False),
    StructField("job_run_id", StringType(), True),
])

DATA_DOMAIN_HISTORY_SCHEMA = StructType([
    StructField(field.name, field.dataType, True) for field in DATA_DOMAIN_SCHEMA.fields
] + [
    StructField("previous_run_id", StringType(), True),
    StructField("previous_profiled_at", TimestampType(), True),
    StructField("change_type", StringType(), True),
    StructField("is_present", BooleanType(), True),
    StructField("profile_status", StringType(), True),
])


def build_data_domain_snapshot(source_schema, source_table, column_name,
                               contract_data_type, values, profiled_at, run_id,
                               job_run_id, previous=None, profile_status="PROFILED"):
    """Build one immutable column version; skipped scans never imply removals."""
    comparable = profile_status in {"PROFILED", "EMPTY"}
    current_values = set(values or []) if comparable else set()
    previous_values = set(previous["values"]) if previous is not None else set()
    if comparable:
        profile_status = "PROFILED" if current_values else "EMPTY"
    metadata = {
        "source_schema": source_schema, "source_table": source_table,
        "column_name": column_name, "contract_data_type": contract_data_type,
        "distinct_value_count": len(current_values) if comparable else None,
        "profiled_at": profiled_at, "run_id": run_id, "job_run_id": job_run_id or run_id,
        "previous_run_id": previous["run_id"] if previous is not None else None,
        "previous_profiled_at": previous["profiled_at"] if previous is not None else None,
        "profile_status": profile_status,
    }
    rows = []
    for value in sorted(current_values | previous_values) if comparable else []:
        present = value in current_values
        change = ("BASELINE" if previous is None else "REMOVED" if not present
                  else "UNCHANGED" if value in previous_values else "ADDED")
        rows.append({**metadata, "data_domain": value, "change_type": change,
                     "is_present": present})
    # Empty and skipped profiles need a retained row even when there are no values.
    return rows or [{**metadata, "data_domain": None, "change_type": None,
                     "is_present": False}]


def latest_data_domain_profiles(domain_table):
    """Read the last comparable version per column, including legacy snapshots."""
    identifier = ".".join(qident(part) for part in domain_table.split("."))
    rows = spark.sql(f"""
        WITH batches AS (
          SELECT source_schema, source_table, column_name, run_id, MAX(profiled_at) profiled_at
          FROM {identifier}
          WHERE coalesce(profile_status, 'PROFILED') IN ('PROFILED', 'EMPTY')
          GROUP BY source_schema, source_table, column_name, run_id
        ), ranked AS (
          SELECT *, ROW_NUMBER() OVER (
            PARTITION BY source_schema, source_table, column_name
            ORDER BY profiled_at DESC, run_id DESC
          ) version_order FROM batches
        )
        SELECT d.* FROM {identifier} d JOIN ranked r
          ON d.source_schema = r.source_schema AND d.source_table = r.source_table
         AND d.column_name = r.column_name AND d.run_id <=> r.run_id
        WHERE r.version_order = 1
    """).collect()
    profiles = {}
    for row in rows:
        key = (row.source_schema, row.source_table, row.column_name)
        profile = profiles.setdefault(key, {"run_id": row.run_id,
                                          "profiled_at": row.profiled_at, "values": set()})
        if row.data_domain is not None and row.is_present is not False:
            profile["values"].add(row.data_domain)
    return profiles


def append_data_domain_snapshots(domain_table, rows):
    """Commit the entire discovery batch in one append; prior versions stay intact."""
    if rows:
        (spark.createDataFrame(rows, DATA_DOMAIN_HISTORY_SCHEMA)
            .write.format("delta").mode("append").saveAsTable(domain_table))


def sql_literal(value):
    return "'" + str(value).replace("'", "''") + "'"


def is_contract_string(data_type):
    """Return whether a PostgreSQL contract type is represented as a Spark string."""
    type_name = (data_type or "").strip().lower()
    return any(marker in type_name for marker in ("character", "varchar", "text", "uuid", "json", "string"))


def data_domain_exclusion_reason(column_name, data_type):
    """Return why a string column is unsuitable for a reusable value domain.

Domains are intended for stable lookup-like values, not keys, audit users,
personal/contact data, or free text. The policy is name- and contract-based
so unsuitable columns are skipped before their Bronze values are scanned.
"""
    raw_name = str(column_name or "").lower()
    compact_name = normalise(raw_name)
    name_tokens = set(re.findall(r"[a-z0-9]+", raw_name))
    type_name = (data_type or "").strip().lower()

    if raw_name.startswith("_"):
        return "system_generated"
    if any(marker in type_name for marker in ("uuid", "guid", "uniqueidentifier")):
        return "identifier_type"
    if compact_name in {"id", "uid", "uuid", "guid"} or raw_name.endswith(("_id", "_uid", "_uuid", "_guid")):
        return "identifier_column"
    if compact_name.endswith(("uuid", "guid")) or "identifier" in name_tokens:
        return "identifier_column"

    if compact_name in {"createdby", "updatedby", "modifiedby", "lastupdatedby", "deletedby"}:
        return "audit_user"
    if "email" in name_tokens or "email" in compact_name:
        return "email_address"
    if name_tokens.intersection({"phone", "telephone", "mobile", "fax"}) or ("contact" in name_tokens and "number" in name_tokens):
        return "contact_detail"
    if name_tokens.intersection({"address", "postcode", "post"}):
        return "address_detail"
    if name_tokens.intersection({"name", "initials", "username", "user"}):
        return "personal_or_user_name"
    if name_tokens.intersection({"description", "detail", "details", "message", "comment", "note", "notes", "summary", "text", "information", "instruction", "content", "narrative"}):
        return "free_text"
    return None


def is_data_domain_candidate(column_name, data_type):
    """Return True only for a contract string column suitable for value-domain profiling."""
    return is_contract_string(data_type) and data_domain_exclusion_reason(column_name, data_type) is None


def data_domain_predicate(source_schema, source_table, column_name):
    return (
        f"source_schema = {sql_literal(source_schema)} AND "
        f"source_table = {sql_literal(source_table)} AND "
        f"column_name = {sql_literal(column_name)}"
    )


def collect_low_cardinality_domain_values(frame, column_name, max_distinct_values, include_empty_string=False):
    """Return sorted values when the column has at most the threshold, else None.

    The extra value proves that a high-cardinality column is skipped before any
    domain row can be written. Values are kept as stored; whitespace is only
    used when deciding whether a value is empty.
    """
    string_value = F.col(qident(column_name)).cast("string")
    candidates = frame.select(string_value.alias("data_domain")).where(F.col("data_domain").isNotNull())
    if not include_empty_string:
        candidates = candidates.where(F.length(F.trim(F.col("data_domain"))) > 0)
    values = [
        row.data_domain
        for row in candidates.distinct().limit(max_distinct_values + 1).collect()
    ]
    if len(values) > max_distinct_values:
        return None
    return sorted(values)


def clear_data_domain_table(domain_table):
    """Clear all stored domains only when the caller explicitly requests it."""
    DeltaTable.forName(spark, domain_table).delete()


def remove_data_domain(domain_table, source_schema, source_table, column_name):
    """Remove a stale domain for one source column."""
    DeltaTable.forName(spark, domain_table).delete(
        data_domain_predicate(source_schema, source_table, column_name)
    )


def replace_data_domain(domain_table, source_schema, source_table, column_name,
                        contract_data_type, values, profiled_at, run_id, job_run_id):
    """Atomically replace the stored low-cardinality domain for one column."""
    if values is None or not values:
        remove_data_domain(domain_table, source_schema, source_table, column_name)
        return
    predicate = data_domain_predicate(source_schema, source_table, column_name)
    distinct_value_count = len(values)
    rows = [
        (
            source_schema, source_table, column_name, contract_data_type, value,
            distinct_value_count, profiled_at, run_id, job_run_id or None,
        )
        for value in values
    ]
    (
        spark.createDataFrame(rows, DATA_DOMAIN_SCHEMA)
        .write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", predicate)
        .saveAsTable(domain_table)
    )
```

<a id="python-99-data-domain-py-110"></a>
## 99_data_domain.py:110

Source: [project X/99_data_domain.py:110](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/99_data_domain.py#L110).

```python
def record_domain_job(status, error_message=None):
    # A supplied parent owns its job; standalone profiles receive their own job.
    if IS_ORCHESTRATED_RUN:
        return
    ended_at = None if status == "RUNNING" else datetime.now(timezone.utc)
    merge_monitor_row(
        "monitoring.cfg_job_run",
        (JOB_RUN_ID, "99_data_domain", PROFILED_AT, ended_at, status,
         int(status == "SUCCESS"), int(status == "FAILED"), error_message,
         datetime.now(timezone.utc)),
        "job_run_id string,pipeline_name string,started_at timestamp,ended_at timestamp,status string,steps_succeeded int,steps_failed int,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id",
    )
    merge_monitor_row(
        "monitoring.cfg_job_step_run",
        (JOB_RUN_ID, 1, "99_data_domain", PROFILED_AT, ended_at, status,
         None, error_message, datetime.now(timezone.utc)),
        "job_run_id string,step_sequence int,notebook_name string,started_at timestamp,ended_at timestamp,status string,child_result string,error_message string,last_updated_at timestamp",
        "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence",
    )


def profile_data_domains():
    if not spark.catalog.tableExists(CONTRACT_TABLE):
        raise RuntimeError(f"Schema contract table does not exist: {CONTRACT_TABLE}")
    if not spark.catalog.tableExists(DOMAIN_TABLE):
        raise RuntimeError(f"Data-domain table does not exist: {DOMAIN_TABLE}")
    maximum = int(MAX_DISTINCT_VALUES)
    if maximum < 1:
        raise ValueError("MAX_DISTINCT_VALUES must be at least 1")
    include_empty = str(INCLUDE_EMPTY_STRING).strip().lower() in {"true", "1", "yes", "y"}
    previous_profiles = latest_data_domain_profiles(DOMAIN_TABLE)
    contract_definitions = {}
    contract_names = {}
    ambiguous_contract_columns = set()
    for row in spark.table(CONTRACT_TABLE).select("table_name", "column_name", "data_type").collect():
        if not row.table_name or not row.column_name or not is_contract_string(row.data_type):
            continue
        key = (normalise(row.table_name), normalise(row.column_name))
        existing_type = contract_definitions.get(key)
        if existing_type is not None and existing_type != row.data_type:
            ambiguous_contract_columns.add(key)
        else:
            contract_definitions[key] = row.data_type
            contract_names[key] = (row.table_name, row.column_name)
    for key in ambiguous_contract_columns:
        contract_definitions.pop(key, None)

    bronze_tables = {}
    for row in spark.sql(f"SHOW TABLES IN {qident(BRONZE_SCHEMA)}").collect():
        if not row.isTemporary:
            bronze_tables.setdefault(normalise(row.tableName), row.tableName)
    summary = {
        "run_id": RUN_ID, "job_run_id": JOB_RUN_ID, "profiled_columns": 0,
        "skipped_high_cardinality": 0, "skipped_empty": 0, "skipped_unsuitable": 0,
        "skipped_by_reason": {}, "missing_bronze_columns": 0,
        "ambiguous_contract_columns": len(ambiguous_contract_columns),
    }
    snapshots = []
    for key, contract_data_type in sorted(contract_definitions.items()):
        logical_table, logical_column = key
        contract_table, contract_column = contract_names[key]
        source_table = bronze_tables.get(logical_table)
        source_column = None
        source_frame = None
        if source_table is not None:
            source_frame = spark.table(f"{qident(BRONZE_SCHEMA)}.{qident(source_table)}")
            actual_columns = {normalise(field.name): field.name for field in source_frame.schema.fields}
            source_column = actual_columns.get(logical_column)
        table_name = source_table or contract_table
        column_name = source_column or contract_column
        previous = previous_profiles.get((BRONZE_SCHEMA, table_name, column_name))
        reason = data_domain_exclusion_reason(column_name, contract_data_type)
        values = None
        if reason:
            status = "EXCLUDED"
            summary["skipped_unsuitable"] += 1
            reasons = summary["skipped_by_reason"]
            reasons[reason] = reasons.get(reason, 0) + 1
        elif source_frame is None or source_column is None:
            status = "SOURCE_MISSING"
            summary["missing_bronze_columns"] += 1
        else:
            values = collect_low_cardinality_domain_values(source_frame, source_column, maximum, include_empty)
            if values is None:
                status = "HIGH_CARDINALITY"
                summary["skipped_high_cardinality"] += 1
            else:
                status = "PROFILED"
                summary["profiled_columns"] += 1
                if not values:
                    summary["skipped_empty"] += 1
        snapshots.extend(build_data_domain_snapshot(
            BRONZE_SCHEMA, table_name, column_name, contract_data_type,
            values, PROFILED_AT, RUN_ID, JOB_RUN_ID, previous, status,
        ))
    # One atomic Delta append publishes the whole batch after all scans succeed.
    append_data_domain_snapshots(DOMAIN_TABLE, snapshots)
    summary["retained_records"] = len(snapshots)
    summary["values_added"] = sum(row["change_type"] == "ADDED" for row in snapshots)
    summary["values_removed"] = sum(row["change_type"] == "REMOVED" for row in snapshots)
    return summary


record_domain_job("RUNNING")
try:
    summary = profile_data_domains()
except Exception as exc:
    record_domain_job("FAILED", str(exc)[:4000])
    raise
else:
    record_domain_job("SUCCESS")
    print(summary)
```
