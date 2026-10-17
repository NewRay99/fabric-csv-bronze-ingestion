# KPI calculation traceability

## 17 October 2026 — New catalogue entries in KPI Definition

Appended `GOLD-KPI-110`–`GOLD-KPI-144` to **KPI Definition rows 119–153** using the existing A:I fields. The sheet now contains 152 records: the unchanged 117 legacy records plus 35 later catalogue entries. Stable Gold identifiers are retained. These are existing WIP measures newly included in this import sheet; no calculation was implemented by this workbook change. The overlapping 144-entry Gold catalogue is unchanged, and 152 is a workbook record count, not an accepted KPI scope baseline.

The 35 rows carry **30 September 2026** as `Date Added`, their first evidenced appearance anywhere in the version-controlled Dashboard Legend, commit [`70b71eb`](https://github.com/NewRay99/fabric-csv-bronze-ingestion/commit/70b71eb95648eaea487830bdcd8f9931b527a05e). The four earlier workbook revisions contain no `GOLD-KPI-110`–`GOLD-KPI-144`. This date predates their move into KPI Definition on 17 October. The original 117 dates remain 26 August 2026. This field records catalogue provenance, not business creation, model implementation or approval.

Each appended row includes the exact saved measure name/DAX, existing source-table and Python/Spark SQL locators, full calculation-trace reference, existing Section classification and proposed requirement links. Requirement descriptions explicitly retain owner approval pending; implementation status remains Built; UAT pending. The original rows, headers, v1 reference and all other workbook cells are unchanged. Embedded Power BI reference tables still need separate synchronisation and refreshed-model/UAT checks.

## 17 October 2026 — KPI Date Added metadata

The user-approved `Date Added` column is appended as **column I** on `KPI Definition`; the original eight columns A:H retain their names, order and definitions. All 117 existing KPI rows are dated **26 August 2026**, because every one was already present in the first workbook upload, commit [`b372181`](https://github.com/NewRay99/fabric-csv-bronze-ingestion/commit/b372181ac72ce43ac274b2928ca8473f32921891). The untouched v1 workbook is the same original content.

`Date Added` means **first recorded in the version-controlled Dashboard Legend**, not the KPI's original business creation, approval, implementation, deployment or latest modification date. Values are typed Excel dates displayed as `dd mmm yyyy`. Future additions must use evidenced first-appearance dates; do not infer them from a last-modified timestamp. Existing model import fields remain unchanged; the embedded model reference tables were not modified.

Reviewed 17 October 2026; source default branch `master`, commit `0a65e962ff3ab9681ed87d9a0a54df610774b736`. This is a static source assessment, not a Fabric execution, DAX-engine reconciliation, deployment or signed client acceptance.

The workbook keeps the original 117 `KPI-xx` records. The separate 144-entry `GOLD-KPI-xxx` catalogue is retained without converting either list into an accepted KPI total. Mission Control has 276 saved measures, including selectors, state/display helpers and benchmarks; they are not 276 new business KPIs.

Original requirement wording, IDs, dated notes, KPI descriptions, original specification calculations and original Section values remain preserved. New operational requirement associations are proposed and require business/operations-owner approval. A similarly named measure or explicit old catalogue mapping does not prove equal population, grain, filter context or security behaviour.

## Inspected source baselines

| Package | SHA-256 | Saved inventory |
|---|---|---|
| Business WIP: `project X\reports\WIP\SM WMPP v16 updated WIP.zip` | `96e11470a29966e7fb91cb900a2ed3a53262b99d639b3f4a1ee48750557dbe7c` | 71 tables; 490 measures; 35 pages |
| Mission Control current Im: `project X\reports\current\SM WMPP Mission Control Im.zip` | `ab11841888301e8d262efa6c0df2354d4ef1043d8edc4e95105423c7da068b27` | 33 tables; 276 measures; 17 pages |
| Mission Control older LM: `project X\reports\WIP\SM WMPP Mission Control (LM).zip` | `fcd58bcdd9c2640e6cd072ba4a0e972670acd9bb8757198da7166f7cacdf3660` | 33 tables; 67 measures; 4 pages |

Archive member paths below are paths *inside* these ZIP files. Notebook links are pinned to the inspected commit. Current models use Import M partitions for physical sources; saved files are not proof of deployment or Direct Lake.

## Legacy KPI assessments

### KPI-83

**Accepted Offer to IPA Conversion %**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) / COUNT(DISTINCT accepted_offers) * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Accepted Offer to IPA Conversion %; original IPA-count / accepted-offer count. Accepted Offers Linked to IPA % is the distinct-offer alternative; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Accepted Offer to IPA Conversion %](#dax-business-accepted-offer-to-ipa-conversion-percent)

Existing Gold-catalogue associations: GOLD-KPI-101

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Accepted Offer to IPA Conversion %](#dax-business-accepted-offer-to-ipa-conversion-percent); [IPAs Created](#dax-business-ipas-created); [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-39

**Accepted Offers (Scoped Table)**. Requirements (original association): `[R28,R35]`.

Original calculation/specification:

```text
Accepted offers
```

Assessment: **Legacy helper retired; original specification retained**. Retired — internal scoped-table helper (see KPI-36); historical classification: 🗄 Retired Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Accepted Offers](#dax-business-accepted-offers)

Existing Gold-catalogue associations: GOLD-KPI-015

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-75

**Accepted Offers Base**. Requirements (original association): `[R28,R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'ACCEPTED'`
```

Assessment: **Legacy helper retired; original specification retained**. Retired — internal base helper; [Successful Offers (Under Offer Referrals)] + `dim_offer_status` cover it; historical classification: 🗄 Retired Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Accepted Offers](#dax-business-accepted-offers)

Existing Gold-catalogue associations: GOLD-KPI-015

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-21

**Active Awaiting Offers (Engaged)**. Requirements (original association): `[R24,R26]`.

Original calculation/specification:

```text
Open referrals with engagement
```

Assessment: **Defined in saved model; runtime/UAT pending**. Active Awaiting Offers With Engagement; historical classification: Alias

Current named measures: [Active Awaiting Offers With Engagement](#dax-business-active-awaiting-offers-with-engagement)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Active Awaiting Offers With Engagement](#dax-business-active-awaiting-offers-with-engagement); [Total Referrals](#dax-business-total-referrals)

### KPI-22

**Active Awaiting Offers (No Engagement)**. Requirements (original association): `[R24,R26]`.

Original calculation/specification:

```text
Open referrals without engagement
```

Assessment: **Defined in saved model; runtime/UAT pending**. Active Awaiting Offers Without Engagement; historical classification: 🔁 Alias

Current named measures: [Active Awaiting Offers Without Engagement](#dax-business-active-awaiting-offers-without-engagement)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Active Awaiting Offers Without Engagement](#dax-business-active-awaiting-offers-without-engagement); [Total Referrals](#dax-business-total-referrals)

### KPI-20

**Active Referral Engagement Rate**. Requirements (original association): `[R24,R26]`.

Original calculation/specification:

```text
KPI-19 / Active referrals
```

Assessment: **Defined in saved model; runtime/UAT pending**. Active Referral Engagement Rate; historical classification: ✅ Covered

Current named measures: [Active Referral Engagement Rate](#dax-business-active-referral-engagement-rate)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Active Referral Engagement Rate](#dax-business-active-referral-engagement-rate); [Active Referrals With Provider Engagement](#dax-business-active-referrals-with-provider-engagement); [Total Referrals](#dax-business-total-referrals); [Referrals Currently Active](#dax-business-referrals-currently-active)

### KPI-32

**Active Referrals Awaiting Offers**. Requirements (original association): `[R24,R36]`.

Original calculation/specification:

```text
Open referrals without offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Awaiting Offer; historical classification: 🔁 Alias

Current named measures: [Referrals Awaiting Offer](#dax-business-referrals-awaiting-offer)

Existing Gold-catalogue associations: GOLD-KPI-005

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Awaiting Offer](#dax-business-referrals-awaiting-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-30

**Active Referrals Under Offer**. Requirements (original association): `[R24,R36]`.

Original calculation/specification:

```text
Under-offer referrals with valid offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Under Offer; historical classification: ✅ Covered

Current named measures: [Referrals Under Offer](#dax-business-referrals-under-offer)

Existing Gold-catalogue associations: GOLD-KPI-042

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Under Offer](#dax-business-referrals-under-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-19

**Active Referrals With Provider Engagement**. Requirements (original association): `[R24,R26]`.

Original calculation/specification:

```text
Active referrals with offer activity
```

Assessment: **Defined in saved model; runtime/UAT pending**. Active Referrals With Provider Engagement; historical classification: ✅ Covered

Current named measures: [Active Referrals With Provider Engagement](#dax-business-active-referrals-with-provider-engagement)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Active Referrals With Provider Engagement](#dax-business-active-referrals-with-provider-engagement); [Total Referrals](#dax-business-total-referrals)

### KPI-113

**Audit Events by Type**. Requirements (original association): `[R20]`.

Original calculation/specification:

```text
`COUNT(DISTINCT event_id) GROUP BY event_type`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referral Lifecycle Events — derived roll-up, not the source audit log; historical classification: ⚠️ Proxy Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Referral Lifecycle Events](#dax-business-referral-lifecycle-events)

Existing Gold-catalogue associations: GOLD-KPI-105

Physical/model source evidence: `gold.fact_referral_lifecycle_event`

Python/Spark SQL producer definitions: [`04_gold_model.py:698`](#python-04-gold-model-py-698)

DAX dependency definitions: [Referral Lifecycle Events](#dax-business-referral-lifecycle-events)

### KPI-59

**Average Days in Draft**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`AVG(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Average Days in Draft; historical classification: ✅ Covered

Current named measures: [Average Days in Draft](#dax-business-average-days-in-draft)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Average Days in Draft](#dax-business-average-days-in-draft)

### KPI-111

**Avg Message Response Time (Hours)**. Requirements (original association): `[R14]`.

Original calculation/specification:

```text
`AVG(response hours between messages)`
```

Assessment: **Source/business-definition gap remains**. Blocked — no message response-time facts in Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-14

**Avg Offers per Provider (Under Offer)**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Offers / Providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Average Offers per Provider (Under Offer Referrals); historical classification: ✅ Covered

Current named measures: [Avg Offers per Provider (Under Offer)](#dax-business-avg-offers-per-provider-under-offer)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Avg Offers per Provider (Under Offer)](#dax-business-avg-offers-per-provider-under-offer); [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted); [No. Providers Who Made Offers](#dax-business-no-providers-who-made-offers); [Providers Who Made Offers](#dax-business-providers-who-made-offers)

### KPI-13

**Avg Offers per Referral (Under Offer)**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Offers / Referrals
```

Assessment: **Defined in saved model; runtime/UAT pending**. Average Offers per Referral Under Offer; historical classification: ✅ Covered

Current named measures: [Average Offers per Referral Under Offer](#dax-business-average-offers-per-referral-under-offer)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Average Offers per Referral Under Offer](#dax-business-average-offers-per-referral-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted); [Referrals Under Offer](#dax-business-referrals-under-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-117

**Bulk Onboarding Success Rate**. Requirements (original association): `[R59]`.

Original calculation/specification:

```text
`COUNT(DISTINCT approved providers) / COUNT(DISTINCT providers) * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Provider Onboarding Success Rate; current approval-state proportion, not bulk-operation outcome; historical classification: Proxy Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Provider Onboarding Success Rate](#dax-business-provider-onboarding-success-rate)

Existing Gold-catalogue associations: GOLD-KPI-090

Physical/model source evidence: `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Provider Onboarding Success Rate](#dax-business-provider-onboarding-success-rate); [Providers Approved](#dax-business-providers-approved); [Providers Registered](#dax-business-providers-registered)

### KPI-34

**Closed Referrals (by Reason)**. Requirements (original association): `[R54]`.

Original calculation/specification:

```text
Group by decline reason
```

Assessment: **No current standalone implementation verified**. Closed Referrals (by Reason) with referral_closure_reason; does not supply provider decline history; historical classification: Partial

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-72

**Critical Offers (30+ Days)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Same as KPI-66 (duplicate)
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 30+ Days; historical classification: 🔁 Alias

Current named measures: [Pending Offers 30+ Days](#dax-business-pending-offers-30-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 30+ Days](#dax-business-pending-offers-30-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-87

**Dashboard Last Refreshed**. Requirements (original association): `[R82]`.

Original calculation/specification:

```text
`current_timestamp()`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Gold Model Last Refreshed; historical classification: 🔁 Alias

Current named measures: [Gold Model Last Refreshed](#dax-business-gold-model-last-refreshed)

Existing Gold-catalogue associations: GOLD-KPI-108

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Gold Model Last Refreshed](#dax-business-gold-model-last-refreshed)

### KPI-105

**Decline Reasons (Referral Level)**. Requirements (original association): `[R54]`.

Original calculation/specification:

```text
`COUNT(DISTINCT referral_id) GROUP BY decline_reason_code`
```

Assessment: **Source/business-definition gap remains**. Blocked — no decline-reason history in active Gold; historical classification: ❌ Blocked Current closure-reason lookup logic is present in 05_gold_dimensions.py; that is not an approved referral-level decline-history KPI.

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-48

**Directory Summary Count**. Requirements (original association): `[R93]`.

Original calculation/specification:

```text
Aggregated provider count
```

Assessment: **Legacy helper retired; original specification retained**. Retired — depended on report-view axis tables; rebuild with field parameters over `dim_provider_home[service_type]` if needed; historical classification: 🗄 Retired

Current named measures: [Directory Summary Count](#dax-business-directory-summary-count)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `Directory Summary Axis (local/calculated model object; no direct notebook producer asserted)`; `gold.bridge_provider_framework`; `gold.dim_framework`; `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`05_gold_dimensions.py:173`](#python-05-gold-dimensions-py-173); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Directory Summary Count](#dax-business-directory-summary-count); [Providers - Fostering](#dax-business-providers-fostering); [Providers Registered](#dax-business-providers-registered); [Residential Homes](#dax-business-residential-homes); [Provider Homes Registered](#dax-business-provider-homes-registered); [Supported Accommodation Homes](#dax-business-supported-accommodation-homes)

### KPI-103

**Document Compliance Rate**. Requirements (original association): `[R48]`.

Original calculation/specification:

```text
`(Total Providers - KPI-102) / Total Providers * 100`
```

Assessment: **Source/business-definition gap remains**. Blocked — as KPI-102; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-101

**Documents Expired**. Requirements (original association): `[R47,R48]`.

Original calculation/specification:

```text
`COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date < current_date()`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Documents Expired; historical classification: ✅ Covered

Current named measures: [Documents Expired](#dax-business-documents-expired)

Existing Gold-catalogue associations: GOLD-KPI-093

Physical/model source evidence: `gold.dim_provider_submission_document`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:239`](#python-05-gold-dimensions-py-239)

DAX dependency definitions: [Documents Expired](#dax-business-documents-expired); [Provider Submission Documents](#dax-business-provider-submission-documents)

### KPI-100

**Documents Expiring (30 Days)**. Requirements (original association): `[R47]`.

Original calculation/specification:

```text
`COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date BETWEEN current_date() AND date_add(current_date(),30)`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Documents Expiring Next 30 Days; historical classification: ✅ Covered

Current named measures: [Documents Expiring Next 30 Days](#dax-business-documents-expiring-next-30-days)

Existing Gold-catalogue associations: GOLD-KPI-092

Physical/model source evidence: `gold.dim_provider_submission_document`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:239`](#python-05-gold-dimensions-py-239)

DAX dependency definitions: [Documents Expiring Next 30 Days](#dax-business-documents-expiring-next-30-days); [Provider Submission Documents](#dax-business-provider-submission-documents)

### KPI-57

**Draft No Activity 7+ Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 7`
```

Assessment: **No current standalone implementation verified**. Draft No Activity 7+ Days; original definition counts draft age, not time since last activity; historical classification: Covered Draft Offers Stalled 7+ Days exists but uses days_since_offer_activity; the original uses offer age. These are different definitions.

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-53

**Draft No Activity Since Creation**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date = last_modified_date`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers With No Activity Since Creation; historical classification: ✅ Covered

Current named measures: [Draft Offers With No Activity Since Creation](#dax-business-draft-offers-with-no-activity-since-creation)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers With No Activity Since Creation](#dax-business-draft-offers-with-no-activity-since-creation); [Offers Submitted](#dax-business-offers-submitted)

### KPI-61

**Draft Offer Count**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT'`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers in Draft; historical classification: 🔁 Alias

Current named measures: [Offers in Draft](#dax-business-offers-in-draft)

Existing Gold-catalogue associations: GOLD-KPI-019

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-55

**Draft Offers Missing Dates**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND (offer_date IS NULL OR last_modified_date IS NULL)`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers Missing Dates; historical classification: ✅ Covered

Current named measures: [Draft Offers Missing Dates](#dax-business-draft-offers-missing-dates)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers Missing Dates](#dax-business-draft-offers-missing-dates); [Offers Submitted](#dax-business-offers-submitted)

### KPI-56

**Draft Offers Updated After Creation**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND last_modified_date > offer_date`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers With Activity Since Creation; historical classification: 🔁 Alias

Current named measures: [Draft Offers With Activity Since Creation](#dax-business-draft-offers-with-activity-since-creation)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers With Activity Since Creation](#dax-business-draft-offers-with-activity-since-creation); [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-54

**Draft Offers With Activity Since Creation**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date != last_modified_date`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers With Activity Since Creation; historical classification: ✅ Covered

Current named measures: [Draft Offers With Activity Since Creation](#dax-business-draft-offers-with-activity-since-creation)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers With Activity Since Creation](#dax-business-draft-offers-with-activity-since-creation); [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-62

**Draft With No Activity Since Creation (%)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`KPI-53 / KPI-61 * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers With No Activity %; historical classification: ✅ Covered

Current named measures: [Draft Offers With No Activity %](#dax-business-draft-offers-with-no-activity-percent)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers With No Activity %](#dax-business-draft-offers-with-no-activity-percent); [Draft Offers With No Activity Since Creation](#dax-business-draft-offers-with-no-activity-since-creation); [Offers Submitted](#dax-business-offers-submitted); [Offers in Draft](#dax-business-offers-in-draft)

### KPI-58

**Drafts No Activity 14+ Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 14`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Drafts No Activity 14+ Days; original draft-age definition; historical classification: Covered

Current named measures: [Drafts No Activity 14+ Days](#dax-business-drafts-no-activity-14-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Drafts No Activity 14+ Days](#dax-business-drafts-no-activity-14-days); [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-63

**Drafts With No Activity 14+ Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Same as KPI-58 (duplicate measure in PBI)
```

Assessment: **Defined in saved model; runtime/UAT pending**. Drafts With No Activity 14+ Days; count, not percentage; historical classification: Alias Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Drafts No Activity 14+ Days](#dax-business-drafts-no-activity-14-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Drafts No Activity 14+ Days](#dax-business-drafts-no-activity-14-days); [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-92

**Emergency Placement Rate**. Requirements (original association): `[R18,R57]`.

Original calculation/specification:

```text
`KPI-91 / KPI-01 * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Emergency Placement Rate; historical classification: ✅ Covered

Current named measures: [Emergency Placement Rate](#dax-business-emergency-placement-rate)

Existing Gold-catalogue associations: GOLD-KPI-050

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Emergency Placement Rate](#dax-business-emergency-placement-rate); [Emergency Referrals](#dax-business-emergency-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-91

**Emergency Referrals**. Requirements (original association): `[R18,R57]`.

Original calculation/specification:

```text
`COUNT(DISTINCT referral_id) WHERE status IN ('OPEN','UNDER_OFFER') AND created_timestamp::date = required_start_date`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Emergency Referrals; OPEN/UNDER_OFFER status and Gold same-day flag; historical classification: Covered

Current named measures: [Emergency Referrals](#dax-business-emergency-referrals)

Existing Gold-catalogue associations: GOLD-KPI-048

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Emergency Referrals](#dax-business-emergency-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-94

**Emergency vs Planned Split**. Requirements (original association): `[R18,R57]`.

Original calculation/specification:

```text
`COUNT(DISTINCT referral_id) GROUP BY CASE WHEN created_timestamp::date = required_start_date THEN 'Emergency' ELSE 'Planned' END`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Visual split using [Emergency Referrals] and [Planned Referrals]; no separate measure; historical classification: ✅ Covered

Current named measures: [Emergency Referrals](#dax-business-emergency-referrals); [Planned Referrals](#dax-business-planned-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Emergency Referrals](#dax-business-emergency-referrals); [Total Referrals](#dax-business-total-referrals); [Planned Referrals](#dax-business-planned-referrals)

### KPI-05

**Female Referrals**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Gender='F'
```

Assessment: **Defined in saved model; runtime/UAT pending**. Female Referrals; historical classification: ✅ Covered

Current named measures: [Female Referrals](#dax-business-female-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_person`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Female Referrals](#dax-business-female-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-52

**Fostering Chart Count**. Requirements (original association): `[R95]`.

Original calculation/specification:

```text
Chart aggregation
```

Assessment: **Legacy helper retired; original specification retained**. Retired — depended on `rpt_provider_fostering` report-view table (see KPI-48); historical classification: 🗄 Retired

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-51

**Fostering Providers**. Requirements (original association): `[R95]`.

Original calculation/specification:

```text
Fostering providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers - Fostering; historical classification: 🔁 Alias

Current named measures: [Providers - Fostering](#dax-business-providers-fostering)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.bridge_provider_framework`; `gold.dim_framework`; `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`05_gold_dimensions.py:173`](#python-05-gold-dimensions-py-173); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Providers - Fostering](#dax-business-providers-fostering); [Providers Registered](#dax-business-providers-registered)

### KPI-106

**Framework Changes During Active Referrals**. Requirements (original association): `[R58]`.

Original calculation/specification:

```text
Active referrals where referral category changed during lifecycle
```

Assessment: **Source/business-definition gap remains**. Blocked — no framework-change history in active Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-38

**Framework Offers (Under Offer Referrals)**. Requirements (original association): `[R67,R68]`.

Original calculation/specification:

```text
Non-spot offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Framework Offers (Under Offer Referrals); historical classification: ✅ Covered

Current named measures: [Framework Offers (Under Offer Referrals)](#dax-business-framework-offers-under-offer-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Framework Offers (Under Offer Referrals)](#dax-business-framework-offers-under-offer-referrals); [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted); [Spot Offers on Referrals Under Offer](#dax-business-spot-offers-on-referrals-under-offer)

### KPI-45

**Framework Providers**. Requirements (original association): `[R67]`.

Original calculation/specification:

```text
Providers by framework
```

Assessment: **Defined in saved model; runtime/UAT pending**. Framework Providers; historical classification: ✅ Covered

Current named measures: [Framework Providers](#dax-business-framework-providers)

Existing Gold-catalogue associations: GOLD-KPI-084

Physical/model source evidence: `gold.bridge_provider_framework`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194)

DAX dependency definitions: [Framework Providers](#dax-business-framework-providers)

### KPI-77

**IPA Completed**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) WHERE signed_by_local_authority = true AND signed_by_provider = true`
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPA Completed; both signatures present; historical classification: Covered

Current named measures: [IPA Completed](#dax-business-ipa-completed)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [IPA Completed](#dax-business-ipa-completed); [IPAs Created](#dax-business-ipas-created)

### KPI-76

**IPA Created**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id)`
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPA Created / IPAs Created; individual IPA count; historical classification: Covered

Current named measures: [IPAs Created](#dax-business-ipas-created)

Existing Gold-catalogue associations: GOLD-KPI-021

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [IPAs Created](#dax-business-ipas-created)

### KPI-85

**IPA Created to Completion %**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT all_ipa) * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPA Created to Completion %; completed IPAs / all IPAs; historical classification: Covered

Current named measures: [IPA Created to Completion %](#dax-business-ipa-created-to-completion-percent)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [IPA Created to Completion %](#dax-business-ipa-created-to-completion-percent); [IPA Completed](#dax-business-ipa-completed); [IPAs Created](#dax-business-ipas-created)

### KPI-73

**IPA Exists**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) > 0` (boolean)
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPA Exists (row helper); historical classification: ✅ Covered

Current named measures: [IPA Exists](#dax-business-ipa-exists)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [IPA Exists](#dax-business-ipa-exists); [IPAs Created](#dax-business-ipas-created)

### KPI-109

**IPA Payment Status**. Requirements (original association): `[R62]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) GROUP BY payment lifecycle status`
```

Assessment: **Source/business-definition gap remains**. Blocked — no payment lifecycle facts in Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-114

**IPA Signature Completion Rate**. Requirements (original association): `[R20,R35]`.

Original calculation/specification:

```text
Counts and rates for LA signed, provider signed, both signed, total IPA
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPAs Signed by Provider; IPAs Signed by Local Authority; IPA Completed; IPA Signature Completion Rate; historical classification: Covered

Current named measures: [IPA Signature Completion Rate](#dax-business-ipa-signature-completion-rate)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [IPA Signature Completion Rate](#dax-business-ipa-signature-completion-rate); [IPA Completed](#dax-business-ipa-completed); [IPAs Created](#dax-business-ipas-created)

### KPI-78

**IPAs Pending Completion**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) WHERE (signed_by_local_authority = false OR signed_by_provider = false) AND closed = false`
```

Assessment: **Defined in saved model; runtime/UAT pending**. IPAs Pending Completion; unsigned and not closed; historical classification: Covered

Current named measures: [IPAs Pending Completion](#dax-business-ipas-pending-completion)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [IPAs Pending Completion](#dax-business-ipas-pending-completion); [IPAs Created](#dax-business-ipas-created)

### KPI-81

**Is Awaiting IPA Creation**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
Boolean flag, accepted offer with no IPA
```

Assessment: **Defined in saved model; runtime/UAT pending**. Is Awaiting IPA Creation (row helper); historical classification: ✅ Covered

Current named measures: [Is Awaiting IPA Creation](#dax-business-is-awaiting-ipa-creation)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Is Awaiting IPA Creation](#dax-business-is-awaiting-ipa-creation)

### KPI-74

**Is In Accepted KPI**. Requirements (original association): `[R28]`.

Original calculation/specification:

```text
`offer_status = 'ACCEPTED'` flag, base for IPA funnel
```

Assessment: **Defined in saved model; runtime/UAT pending**. Is In Accepted KPI; accepted-status row helper; historical classification: Covered

Current named measures: [Is In Accepted KPI](#dax-business-is-in-accepted-kpi)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Is In Accepted KPI](#dax-business-is-in-accepted-kpi)

### KPI-82

**Is IPA Completed**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
Boolean flag, both signatures present
```

Assessment: **Defined in saved model; runtime/UAT pending**. Is IPA Completed; IPA rows, with explicit offer-context transfer; historical classification: Covered

Current named measures: [Is IPA Completed](#dax-business-is-ipa-completed)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Is IPA Completed](#dax-business-is-ipa-completed); [IPAs Created](#dax-business-ipas-created)

### KPI-80

**Is IPA Pending**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
Boolean flag, IPA exists but not signed
```

Assessment: **Defined in saved model; runtime/UAT pending**. Is IPA Pending; IPA rows, with explicit offer-context transfer; historical classification: Covered

Current named measures: [Is IPA Pending](#dax-business-is-ipa-pending)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Is IPA Pending](#dax-business-is-ipa-pending); [IPAs Created](#dax-business-ipas-created)

### KPI-47

**Is Non Framework Provider**. Requirements (original association): `[R46]`.

Original calculation/specification:

```text
Boolean flag
```

Assessment: **Defined in saved model; runtime/UAT pending**. Is Non Framework Provider (row helper); historical classification: ✅ Covered

Current named measures: [Is Non Framework Provider](#dax-business-is-non-framework-provider)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.bridge_provider_framework`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194)

DAX dependency definitions: [Is Non Framework Provider](#dax-business-is-non-framework-provider)

### KPI-88

**Latest Export per Offer**. Requirements (original association): `[R53]`.

Original calculation/specification:

```text
`MAX(offer_date) GROUP BY offer_id`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Latest Offer Source Export; historical classification: 🔁 Alias

Current named measures: [Latest Offer Source Export](#dax-business-latest-offer-source-export)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Latest Offer Source Export](#dax-business-latest-offer-source-export)

### KPI-89

**Latest Offer Status Count**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) GROUP BY offer_status ORDER BY count DESC`
```

Assessment: **Legacy helper retired; original specification retained**. Retired — Gold `fact_offer` is already deduplicated to the latest state per offer; historical classification: 🗄 Retired

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-04

**Male Referrals**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Gender='M'
```

Assessment: **Defined in saved model; runtime/UAT pending**. Male Referrals; historical classification: ✅ Covered

Current named measures: [Male Referrals](#dax-business-male-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_person`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Male Referrals](#dax-business-male-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-110

**Messages Sent**. Requirements (original association): `[R14]`.

Original calculation/specification:

```text
`COUNT(DISTINCT message_id)`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Provider Messages Sent — lifecycle-event proxy for volume only; no response-time or unread analysis; historical classification: ⚠️ Proxy Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Provider Messages Sent](#dax-business-provider-messages-sent)

Existing Gold-catalogue associations: GOLD-KPI-109

Physical/model source evidence: `gold.fact_referral_lifecycle_event`

Python/Spark SQL producer definitions: [`04_gold_model.py:698`](#python-04-gold-model-py-698)

DAX dependency definitions: [Provider Messages Sent](#dax-business-provider-messages-sent); [Referral Lifecycle Events](#dax-business-referral-lifecycle-events)

### KPI-11

**No. Providers Who Made Offers**. Requirements (original association): `[R25,R26]`.

Original calculation/specification:

```text
Distinct providers with offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers Who Made Offers; historical classification: ✅ Covered

Current named measures: [Providers Who Made Offers](#dax-business-providers-who-made-offers)

Existing Gold-catalogue associations: GOLD-KPI-056

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Providers Who Made Offers](#dax-business-providers-who-made-offers)

### KPI-46

**NON Framework Providers**. Requirements (original association): `[R46]`.

Original calculation/specification:

```text
QA flag false
```

Assessment: **Defined in saved model; runtime/UAT pending**. Non-Framework Providers; historical classification: ✅ Covered

Current named measures: [Non-Framework Providers](#dax-business-non-framework-providers)

Existing Gold-catalogue associations: GOLD-KPI-085

Physical/model source evidence: `gold.bridge_provider_framework`; `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Non-Framework Providers](#dax-business-non-framework-providers)

### KPI-28

**Offer Count**. Requirements (original association): `[R25-R29]`.

Original calculation/specification:

```text
Distinct offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers Submitted; historical classification: 🔁 Alias

Current named measures: [Offers Submitted](#dax-business-offers-submitted)

Existing Gold-catalogue associations: GOLD-KPI-014

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers Submitted](#dax-business-offers-submitted)

### KPI-36

**Offer IDs (Under Offer Referrals)**. Requirements (original association): `[R25-R29]`.

Original calculation/specification:

```text
Distinct offer IDs
```

Assessment: **Legacy helper retired; original specification retained**. Retired — internal CALCULATETABLE helper; Gold relationship graph + TREATAS make it unnecessary; historical classification: 🗄 Retired

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-70

**Offers At Risk (8–14 Days)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Same as KPI-68 (duplicate)
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 8-14 Days; historical classification: 🔁 Alias

Current named measures: [Pending Offers 8-14 Days](#dax-business-pending-offers-8-14-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 8-14 Days](#dax-business-pending-offers-8-14-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-79

**Offers Awaiting IPA Creation**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT f.offer_id) LEFT JOIN fact_ipa i ON f.offer_id = i.offer_id WHERE f.offer_status = 'ACCEPTED' AND i.ipa_id IS NULL`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers Awaiting IPA Creation; historical classification: ✅ Covered

Current named measures: [Offers Awaiting IPA Creation](#dax-business-offers-awaiting-ipa-creation)

Existing Gold-catalogue associations: GOLD-KPI-099, GOLD-KPI-100

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers Awaiting IPA Creation](#dax-business-offers-awaiting-ipa-creation); [Offers Submitted](#dax-business-offers-submitted)

### KPI-17

**Offers in Draft (Under Offer Referrals)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Draft offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Draft Offers on Referrals Under Offer; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Draft Offers on Referrals Under Offer](#dax-business-draft-offers-on-referrals-under-offer)

Existing Gold-catalogue associations: GOLD-KPI-019

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Draft Offers on Referrals Under Offer](#dax-business-draft-offers-on-referrals-under-offer); [Offers in Draft](#dax-business-offers-in-draft); [Offers Submitted](#dax-business-offers-submitted)

### KPI-71

**Offers Outside Timeframe (15–30 Days)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Same as KPI-65 (duplicate)
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers Outside Timeframe (15–30 Days); inclusive original range; historical classification: Alias Original specification explicitly duplicates KPI-65; Pending Offers 15–30 Days supplies that saved inclusive-band calculation. Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Pending Offers 15–30 Days](#dax-business-pending-offers-15-30-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 15–30 Days](#dax-business-pending-offers-15-30-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-37

**Offers per Provider (Under Offer Referrals)**. Requirements (original association): `[R26]`.

Original calculation/specification:

```text
Offers grouped by provider
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers per Provider (Under Offer Referrals); historical classification: ✅ Covered

Current named measures: [Offers per Provider (Under Offer Referrals)](#dax-business-offers-per-provider-under-offer-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers per Provider (Under Offer Referrals)](#dax-business-offers-per-provider-under-offer-referrals); [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted); [No. Providers Who Made Offers](#dax-business-no-providers-who-made-offers); [Providers Who Made Offers](#dax-business-providers-who-made-offers)

### KPI-84

**Offers Still to Progress to IPA**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`100 - KPI-83`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers Still to Progress to IPA %; complement of KPI-83 per assessment; Offers Awaiting IPA Creation supplies the actual count; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Offers Still to Progress to IPA %](#dax-business-offers-still-to-progress-to-ipa-percent)

Existing Gold-catalogue associations: GOLD-KPI-102

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers Still to Progress to IPA %](#dax-business-offers-still-to-progress-to-ipa-percent); [Accepted Offer to IPA Conversion %](#dax-business-accepted-offer-to-ipa-conversion-percent); [IPAs Created](#dax-business-ipas-created); [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-60

**Oldest Draft Age (Days)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`MAX(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Oldest Draft Age Days; historical classification: ✅ Covered

Current named measures: [Oldest Draft Age Days](#dax-business-oldest-draft-age-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Oldest Draft Age Days](#dax-business-oldest-draft-age-days)

### KPI-06

**Other Referrals**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Gender not M/F
```

Assessment: **Defined in saved model; runtime/UAT pending**. Other Gender Referrals; historical classification: ✅ Covered

Current named measures: [Other Gender Referrals](#dax-business-other-gender-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_person`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Other Gender Referrals](#dax-business-other-gender-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-96

**Out-of-Region Placement Rate**. Requirements (original association): `[R22]`.

Original calculation/specification:

```text
`KPI-95 / KPI-01 * 100`
```

Assessment: **Source/business-definition gap remains**. Blocked — as KPI-95; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-95

**Out-of-Region Referrals**. Requirements (original association): `[R22]`.

Original calculation/specification:

```text
`COUNT(DISTINCT r.referral_id) JOIN fact_referral_offer rpo JOIN dim_provider p WHERE p.country != 'United Kingdom' OR p.county NOT LIKE '%West Midlands%'`
```

Assessment: **Source/business-definition gap remains**. Blocked — `fact_referral[region]` is null until a reliable source supplies it; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-90

**Overlap Referrals**. Requirements (original association): `[R22]`.

Original calculation/specification:

```text
Referrals appearing in multiple provider referral-provider mappings
```

Assessment: **Defined in saved model; runtime/UAT pending**. Overlap Referrals; diagnostic intersection of active awaiting/under-offer cohorts. Does not satisfy R22 geography; historical classification: Diagnostic Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Referrals With Multiple Provider Assignments](#dax-business-referrals-with-multiple-provider-assignments)

Existing Gold-catalogue associations: GOLD-KPI-051

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals With Multiple Provider Assignments](#dax-business-referrals-with-multiple-provider-assignments); [Total Referrals](#dax-business-total-referrals)

### KPI-108

**Payment Method Breakdown**. Requirements (original association): `[R62]`.

Original calculation/specification:

```text
`COUNT(DISTINCT ipa_id) GROUP BY payment_method WHERE closed = false`
```

Assessment: **Source/business-definition gap remains**. Blocked — no payment method / payment facts in Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-18

**Pending Offers (Under Offer Referrals)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Pending offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers (Under Offer Referrals); historical classification: ✅ Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Pending Offers (Under Offer Referrals)](#dax-business-pending-offers-under-offer-referrals)

Existing Gold-catalogue associations: GOLD-KPI-053

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers (Under Offer Referrals)](#dax-business-pending-offers-under-offer-referrals); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-67

**Pending Offers 0–7 Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 0 AND 7`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 0-7 Days; historical classification: ✅ Covered

Current named measures: [Pending Offers 0-7 Days](#dax-business-pending-offers-0-7-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 0-7 Days](#dax-business-pending-offers-0-7-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-65

**Pending Offers 15–30 Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 15 AND 30`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 15–30 Days; original inclusive range. Use Pending Offers 15-29 Days for non-overlapping bands; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Pending Offers 15–30 Days](#dax-business-pending-offers-15-30-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 15–30 Days](#dax-business-pending-offers-15-30-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-66

**Pending Offers 30+ Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 30+ Days; historical classification: ✅ Covered

Current named measures: [Pending Offers 30+ Days](#dax-business-pending-offers-30-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 30+ Days](#dax-business-pending-offers-30-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-68

**Pending Offers 8–14 Days**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 8 AND 14`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Pending Offers 8-14 Days; historical classification: ✅ Covered

Current named measures: [Pending Offers 8-14 Days](#dax-business-pending-offers-8-14-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Pending Offers 8-14 Days](#dax-business-pending-offers-8-14-days); [Pending Offers](#dax-business-pending-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-64

**Pending Offers by Age Bucket**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
`COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN min_days AND max_days GROUP BY band_label`
```

Assessment: **Legacy helper retired; original specification retained**. Retired — disconnected age-band table; the four pending-age measures (KPI-65–68) cover the same bands; historical classification: 🗄 Retired

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-26

**Placement Type Totals (Visual)**. Requirements (original association): `[R13]`.

Original calculation/specification:

```text
Spot vs Framework split
```

Assessment: **Defined in saved model; runtime/UAT pending**. Total Referrals + `fact_referral[placement_type_required]` visual dimension; historical classification: 🔁 Alias Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Total Referrals](#dax-business-total-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Total Referrals](#dax-business-total-referrals)

### KPI-93

**Planned Referrals**. Requirements (original association): `[R57]`.

Original calculation/specification:

```text
`COUNT(DISTINCT referral_id) WHERE status IN ('OPEN','UNDER_OFFER') AND created_timestamp::date != required_start_date`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Planned Referrals; OPEN/UNDER_OFFER status, both dates present and not same-day; historical classification: Covered

Current named measures: [Planned Referrals](#dax-business-planned-referrals)

Existing Gold-catalogue associations: GOLD-KPI-049

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Planned Referrals](#dax-business-planned-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-112

**Priority Messages Unread**. Requirements (original association): `[R14]`.

Original calculation/specification:

```text
`COUNT(DISTINCT message_id) WHERE no message status exists`
```

Assessment: **Source/business-definition gap remains**. Blocked — no message-status facts in Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-104

**Provider Due Diligence Status**. Requirements (original association): `[R49]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_id) GROUP BY provider_status`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers Pending Onboarding / Providers Approved (provider_status split); historical classification: ✅ Covered

Current named measures: [Providers Pending Onboarding](#dax-business-providers-pending-onboarding); [Providers Approved](#dax-business-providers-approved)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Providers Pending Onboarding](#dax-business-providers-pending-onboarding); [Providers Registered](#dax-business-providers-registered); [Providers Approved](#dax-business-providers-approved)

### KPI-40

**Provider Homes Registered**. Requirements (original association): `[R91,R93]`.

Original calculation/specification:

```text
Count homes
```

Assessment: **Defined in saved model; runtime/UAT pending**. Provider Homes Registered; historical classification: ✅ Covered

Current named measures: [Provider Homes Registered](#dax-business-provider-homes-registered)

Existing Gold-catalogue associations: GOLD-KPI-076

Physical/model source evidence: `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Provider Homes Registered](#dax-business-provider-homes-registered)

### KPI-116

**Provider Onboarding Pipeline**. Requirements (original association): `[R59]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_id) WHERE provider_status = 'Pending'`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers Pending Onboarding; historical classification: ✅ Covered

Current named measures: [Providers Pending Onboarding](#dax-business-providers-pending-onboarding)

Existing Gold-catalogue associations: GOLD-KPI-088

Physical/model source evidence: `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Providers Pending Onboarding](#dax-business-providers-pending-onboarding); [Providers Registered](#dax-business-providers-registered)

### KPI-69

**Provider with Offers over 30+ Days**. Requirements (original association): `[R24,R26]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers With Pending Offers 30+ Days; historical classification: ✅ Covered

Current named measures: [Providers With Pending Offers 30+ Days](#dax-business-providers-with-pending-offers-30-days)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Providers With Pending Offers 30+ Days](#dax-business-providers-with-pending-offers-30-days)

### KPI-42

**Providers - Fostering**. Requirements (original association): `[R95]`.

Original calculation/specification:

```text
Fostering providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers - Fostering; historical classification: ✅ Covered

Current named measures: [Providers - Fostering](#dax-business-providers-fostering)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.bridge_provider_framework`; `gold.dim_framework`; `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`05_gold_dimensions.py:173`](#python-05-gold-dimensions-py-173); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Providers - Fostering](#dax-business-providers-fostering); [Providers Registered](#dax-business-providers-registered)

### KPI-43

**Providers - Residential**. Requirements (original association): `[R96]`.

Original calculation/specification:

```text
Residential providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers - Residential; historical classification: ✅ Covered

Current named measures: [Providers - Residential](#dax-business-providers-residential)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Providers - Residential](#dax-business-providers-residential)

### KPI-44

**Providers - Supported Accommodation**. Requirements (original association): `[R91]`.

Original calculation/specification:

```text
Supported Accommodation providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers - Supported Accommodation; historical classification: ✅ Covered

Current named measures: [Providers - Supported Accommodation](#dax-business-providers-supported-accommodation)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [Providers - Supported Accommodation](#dax-business-providers-supported-accommodation)

### KPI-102

**Providers Blocked (Incomplete Docs)**. Requirements (original association): `[R48]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_id) WHERE expired documentation exists`
```

Assessment: **Source/business-definition gap remains**. Blocked — no expected-document set in Gold to test completeness against; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-41

**Providers Registered**. Requirements (original association): `[R91,R93]`.

Original calculation/specification:

```text
Count providers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers Registered; historical classification: ✅ Covered

Current named measures: [Providers Registered](#dax-business-providers-registered)

Existing Gold-catalogue associations: GOLD-KPI-077

Physical/model source evidence: `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Providers Registered](#dax-business-providers-registered)

### KPI-97

**Providers with QA Flags**. Requirements (original association): `[R41]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_id) WHERE qa_flag = true OR qa_flag_fostering_spot = true OR qa_flag_sup_acc = true OR qa_flag_resi = true`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Providers With QA Flags; historical classification: ✅ Covered

Current named measures: [Providers With QA Flags](#dax-business-providers-with-qa-flags)

Existing Gold-catalogue associations: GOLD-KPI-086

Physical/model source evidence: `gold.dim_provider`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Providers With QA Flags](#dax-business-providers-with-qa-flags); [Providers Registered](#dax-business-providers-registered)

### KPI-98

**QA Flag Type Breakdown**. Requirements (original association): `[R41]`.

Original calculation/specification:

```text
`UNPIVOT qa_flag columns → COUNT(DISTINCT provider_id) GROUP BY flag_type`
```

Assessment: **Source/business-definition gap remains**. Blocked — no QA flag-type dimension to unpivot in Gold; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-99

**QA Flagged Providers by Home**. Requirements (original association): `[R41]`.

Original calculation/specification:

```text
`COUNT(DISTINCT provider_home_id) WHERE provider/home QA flags exist`
```

Assessment: **Defined in saved model; runtime/UAT pending**. QA Flagged Homes; home flag OR parent-provider flag; historical classification: Covered

Current named measures: [QA Flagged Homes](#dax-business-qa-flagged-homes)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155); [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163)

DAX dependency definitions: [QA Flagged Homes](#dax-business-qa-flagged-homes); [Provider Homes Registered](#dax-business-provider-homes-registered)

### KPI-115

**Referral Updates per Day**. Requirements (original association): `[R19]`.

Original calculation/specification:

```text
`COUNT(DISTINCT referral_id) / COUNT(DISTINCT DATE(modified_timestamp))`
```

Assessment: **Source/business-definition gap remains**. Blocked — no durable referral update timestamp; lifecycle events provide the supported activity measure; historical classification: ❌ Blocked

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-03

**Referrals Awaiting Offer**. Requirements (original association): `[R24,R36]`.

Original calculation/specification:

```text
Open/Under Offer referrals without valid offer
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Awaiting Offer; historical classification: ✅ Covered

Current named measures: [Referrals Awaiting Offer](#dax-business-referrals-awaiting-offer)

Existing Gold-catalogue associations: GOLD-KPI-005

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Awaiting Offer](#dax-business-referrals-awaiting-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-31

**Referrals Cancelled/Closed**. Requirements (original association): `[R13]`.

Original calculation/specification:

```text
Closed or Cancelled
```

Assessment: **Defined in saved model; runtime/UAT pending**. Closed or Cancelled Referrals; historical classification: ✅ Covered

Current named measures: [Closed or Cancelled Referrals](#dax-business-closed-or-cancelled-referrals)

Existing Gold-catalogue associations: GOLD-KPI-003

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Closed or Cancelled Referrals](#dax-business-closed-or-cancelled-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-29

**Referrals Currently Active**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Open or Under Offer
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Currently Active; historical classification: ✅ Covered

Current named measures: [Referrals Currently Active](#dax-business-referrals-currently-active)

Existing Gold-catalogue associations: GOLD-KPI-002

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Currently Active](#dax-business-referrals-currently-active); [Total Referrals](#dax-business-total-referrals)

### KPI-08

**Referrals Not Yet Closed (Created in Period)**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Status not Closed/Cancelled
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Not Yet Closed (Created in Period); historical classification: ✅ Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Open Referrals](#dax-business-open-referrals)

Existing Gold-catalogue associations: GOLD-KPI-002

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Open Referrals](#dax-business-open-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-24

**Referrals This FY**. Requirements (original association): `[R52]`.

Original calculation/specification:

```text
Created current FY
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Created This Financial Year; historical classification: 🔁 Alias

Current named measures: [Referrals Created This Financial Year](#dax-business-referrals-created-this-financial-year)

Existing Gold-catalogue associations: GOLD-KPI-040

Physical/model source evidence: `gold.dim_date`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:128`](#python-05-gold-dimensions-py-128); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Created This Financial Year](#dax-business-referrals-created-this-financial-year); [Total Referrals](#dax-business-total-referrals)

### KPI-23

**Referrals This Month**. Requirements (original association): `[R24,R52]`.

Original calculation/specification:

```text
Created current month
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals Created This Month; historical classification: 🔁 Alias

Current named measures: [Referrals Created This Month](#dax-business-referrals-created-this-month)

Existing Gold-catalogue associations: GOLD-KPI-036

Physical/model source evidence: `gold.dim_date`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:128`](#python-05-gold-dimensions-py-128); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals Created This Month](#dax-business-referrals-created-this-month); [Total Referrals](#dax-business-total-referrals)

### KPI-02

**Referrals With Offers**. Requirements (original association): `[R24,R36]`.

Original calculation/specification:

```text
COUNT DISTINCT referrals with valid offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals With an Offer; historical classification: ✅ Covered

Current named measures: [Referrals With an Offer](#dax-business-referrals-with-an-offer)

Existing Gold-catalogue associations: GOLD-KPI-004

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals With an Offer](#dax-business-referrals-with-an-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-09

**Referrals With Offers (Created in Period)**. Requirements (original association): `[R24,R51]`.

Original calculation/specification:

```text
KPI-02 filtered by created period
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals With Offers (Created in Period); historical classification: ✅ Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Referrals With an Offer](#dax-business-referrals-with-an-offer)

Existing Gold-catalogue associations: GOLD-KPI-004

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals With an Offer](#dax-business-referrals-with-an-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-33

**Referrals With One or More Offers**. Requirements (original association): `[R24]`.

Original calculation/specification:

```text
Referrals with valid offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Referrals With an Offer; historical classification: 🔁 Alias

Current named measures: [Referrals With an Offer](#dax-business-referrals-with-an-offer)

Existing Gold-catalogue associations: GOLD-KPI-004

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Referrals With an Offer](#dax-business-referrals-with-an-offer); [Total Referrals](#dax-business-total-referrals)

### KPI-49

**Residential Homes**. Requirements (original association): `[R96]`.

Original calculation/specification:

```text
Residential homes
```

Assessment: **Defined in saved model; runtime/UAT pending**. Residential Homes; historical classification: ✅ Covered

Current named measures: [Residential Homes](#dax-business-residential-homes)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Residential Homes](#dax-business-residential-homes); [Provider Homes Registered](#dax-business-provider-homes-registered)

### KPI-27

**Spot Offers (Under Offer Referrals)**. Requirements (original association): `[R18]`.

Original calculation/specification:

```text
Spot offers only
```

Assessment: **Defined in saved model; runtime/UAT pending**. Spot Offers on Referrals Under Offer; spot is not emergency; historical classification: Covered

Current named measures: [Spot Offers on Referrals Under Offer](#dax-business-spot-offers-on-referrals-under-offer)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider_home`; `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163); [`04_gold_model.py:712`](#python-04-gold-model-py-712); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Spot Offers on Referrals Under Offer](#dax-business-spot-offers-on-referrals-under-offer); [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-15

**Successful Offers (Under Offer Referrals)**. Requirements (original association): `[R28]`.

Original calculation/specification:

```text
Accepted offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Successful Offers on Referrals Under Offer; historical classification: ✅ Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Successful Offers on Referrals Under Offer](#dax-business-successful-offers-on-referrals-under-offer)

Existing Gold-catalogue associations: GOLD-KPI-015

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Successful Offers on Referrals Under Offer](#dax-business-successful-offers-on-referrals-under-offer); [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-86

**Successful Offers to IPA Completed %**. Requirements (original association): `[R35]`.

Original calculation/specification:

```text
`COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT accepted_offers) * 100`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Successful Offers to IPA Completed %; completed IPAs / accepted offers; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Successful Offers to IPA Completed %](#dax-business-successful-offers-to-ipa-completed-percent)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_ipa`; `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Successful Offers to IPA Completed %](#dax-business-successful-offers-to-ipa-completed-percent); [IPA Completed](#dax-business-ipa-completed); [IPAs Created](#dax-business-ipas-created); [Accepted Offers](#dax-business-accepted-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-50

**Supported Accommodation Homes**. Requirements (original association): `[R91]`.

Original calculation/specification:

```text
Supported homes
```

Assessment: **Defined in saved model; runtime/UAT pending**. Supported Accommodation Homes; historical classification: ✅ Covered

Current named measures: [Supported Accommodation Homes](#dax-business-supported-accommodation-homes)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_provider`; `gold.dim_provider_home`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:163`](#python-05-gold-dimensions-py-163); [`05_gold_dimensions.py:155`](#python-05-gold-dimensions-py-155)

DAX dependency definitions: [Supported Accommodation Homes](#dax-business-supported-accommodation-homes); [Provider Homes Registered](#dax-business-provider-homes-registered)

### KPI-07

**Total Gendered Referrals**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Sum of gender counts
```

Assessment: **Defined in saved model; runtime/UAT pending**. Total Gendered Referrals; historical classification: ✅ Covered

Current named measures: [Total Gendered Referrals](#dax-business-total-gendered-referrals)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.dim_person`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`05_gold_dimensions.py:194`](#python-05-gold-dimensions-py-194); [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Total Gendered Referrals](#dax-business-total-gendered-referrals); [Total Referrals](#dax-business-total-referrals)

### KPI-25

**Total Offers Made**. Requirements (original association): `[R67,R68]`.

Original calculation/specification:

```text
Non-draft offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Non-Draft Offers; historical classification: Alias

Current named measures: [Non-Draft Offers](#dax-business-non-draft-offers)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-35

**Total Offers Made (Active Referrals Under Offer)**. Requirements (original association): `[R25-R29]`.

Original calculation/specification:

```text
Non-draft offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Offers on Referrals Under Offer; historical classification: ✅ Covered

Current named measures: [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer)

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer); [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-12

**Total Offers Made Historically**. Requirements (original association): `[R25-R29]`.

Original calculation/specification:

```text
Distinct offers excluding Draft
```

Assessment: **Defined in saved model; runtime/UAT pending**. Non-Draft Offers; historical classification: Alias

Current named measures: [Non-Draft Offers](#dax-business-non-draft-offers)

Existing Gold-catalogue associations: GOLD-KPI-014

Physical/model source evidence: `gold.fact_offer`

Python/Spark SQL producer definitions: [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Non-Draft Offers](#dax-business-non-draft-offers); [Offers Submitted](#dax-business-offers-submitted)

### KPI-01

**Total Referrals**. Requirements (original association): `[R24,R51]`.

Original calculation/specification:

```text
COUNT(DISTINCT referral_id) WHERE status IS NOT NULL
```

Assessment: **Defined in saved model; runtime/UAT pending**. Total Referrals; historical classification: ✅ Covered

Current named measures: [Total Referrals](#dax-business-total-referrals)

Existing Gold-catalogue associations: GOLD-KPI-001

Physical/model source evidence: `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232)

DAX dependency definitions: [Total Referrals](#dax-business-total-referrals)

### KPI-10

**Total Referrals That Received Offers**. Requirements (original association): `[R51]`.

Original calculation/specification:

```text
Referrals having valid offer
```

Assessment: **No current standalone implementation verified**. Total Referrals That Received Offers; historical classification: Covered The current suffixed Ratio measure returns a proportion with a zero fallback, not the original count; it is not silently substituted.

Current named measures: None verified. No DAX or source data has been fabricated.

Existing Gold-catalogue associations: None recorded; original requirement/KPI associations retained.

Physical/model source evidence: See source gap/retirement assessment.

Python/Spark SQL producer definitions: No producer for this requested calculation asserted.

DAX dependency definitions: None.

### KPI-107

**Total Weekly Fee Liability**. Requirements (original association): `[R62]`.

Original calculation/specification:

```text
`SUM(costs_total_weekly_fee) WHERE signed_by_local_authority = true AND signed_by_provider = true AND closed = false`
```

Assessment: **Defined in saved model; runtime/UAT pending**. Estimated Active Weekly Cost — estimate, not signed-only actuals; historical classification: ⚠️ Proxy Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Estimated Active Weekly Cost](#dax-business-estimated-active-weekly-cost)

Existing Gold-catalogue associations: GOLD-KPI-023

Physical/model source evidence: `gold.fact_ipa`

Python/Spark SQL producer definitions: [`04_gold_model.py:817`](#python-04-gold-model-py-817)

DAX dependency definitions: [Estimated Active Weekly Cost](#dax-business-estimated-active-weekly-cost)

### KPI-16

**Unsuccessful Offers (Under Offer Referrals)**. Requirements (original association): `[R28]`.

Original calculation/specification:

```text
Declined/Rejected/Withdrawn offers
```

Assessment: **Defined in saved model; runtime/UAT pending**. Unsuccessful Offers on Referrals Under Offer; historical classification: Covered Compare population, grain and filters with the original specification; a named alternative does not establish semantic equivalence.

Current named measures: [Unsuccessful Offers on Referrals Under Offer](#dax-business-unsuccessful-offers-on-referrals-under-offer)

Existing Gold-catalogue associations: GOLD-KPI-054

Physical/model source evidence: `gold.fact_offer`; `gold.fact_referral`

Python/Spark SQL producer definitions: [`04_gold_model.py:232`](#python-04-gold-model-py-232); [`04_gold_model.py:712`](#python-04-gold-model-py-712)

DAX dependency definitions: [Unsuccessful Offers on Referrals Under Offer](#dax-business-unsuccessful-offers-on-referrals-under-offer); [Unsuccessful Offers](#dax-business-unsuccessful-offers); [Offers Submitted](#dax-business-offers-submitted)

## Retained Gold catalogue

These 144 entries are a separate catalogue with its existing identifiers; the 35 later entries remain catalogue additions, not newly accepted requirements. Each entry resolves by exact measure name in the inspected business model. Requirement associations marked proposed remain proposed.

| Catalogue ID | Measure | Legacy mapping | Requirement association | Current interpretation |
|---|---|---|---|---|
| GOLD-KPI-001 | [Total Referrals](#dax-business-total-referrals) | KPI-01 | R24, R51 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-002 | [Open Referrals](#dax-business-open-referrals) | KPI-08, KPI-29 | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-003 | [Closed Referrals](#dax-business-closed-referrals) | KPI-31 | R13 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-004 | [Referrals With an Offer](#dax-business-referrals-with-an-offer) | KPI-02, KPI-09, KPI-33 | R24, R36, R51 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-005 | [Referrals Awaiting Offer](#dax-business-referrals-awaiting-offer) | KPI-03, KPI-32 | R24, R36 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-006 | [Referrals Without Provider Assignment](#dax-business-referrals-without-provider-assignment) | New Gold KPI | R24, R26 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-007 | [Open Overdue Referrals](#dax-business-open-overdue-referrals) | New Gold KPI | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-008 | [Referrals Placed by Required Date](#dax-business-referrals-placed-by-required-date) | New Gold KPI | R18, R57 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-009 | [Placement Target Hit Rate](#dax-business-placement-target-hit-rate) | New Gold KPI | R18, R57 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-010 | [Median Days to First Action](#dax-business-median-days-to-first-action) | New Gold KPI | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-011 | [Median Days to First Offer](#dax-business-median-days-to-first-offer) | New Gold KPI | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-012 | [Median Days to IPA](#dax-business-median-days-to-ipa) | New Gold KPI | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-013 | [Open Referrals Stalled 7+ Days](#dax-business-open-referrals-stalled-7-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-014 | [Offers Submitted](#dax-business-offers-submitted) | KPI-12, KPI-28 | R25–R29 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-015 | [Accepted Offers](#dax-business-accepted-offers) | KPI-15, KPI-39, KPI-75 | R28, R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-016 | [Offers with a Decision](#dax-business-offers-with-a-decision) | New Gold KPI | R28 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-017 | [Offer Acceptance Rate](#dax-business-offer-acceptance-rate) | New Gold KPI | R28 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-018 | [Average Offers per Referral](#dax-business-average-offers-per-referral) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-019 | [Offers in Draft](#dax-business-offers-in-draft) | KPI-17, KPI-61 | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-020 | [Draft Offers Stalled 7+ Days](#dax-business-draft-offers-stalled-7-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-021 | [IPAs Created](#dax-business-ipas-created) | KPI-76 | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-022 | [Active IPAs](#dax-business-active-ipas) | New Gold KPI | R35, R62 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-023 | [Estimated Active Weekly Cost](#dax-business-estimated-active-weekly-cost) | KPI-107 replacement | R62 | Estimated active weekly liability, not actual spend or verified signed fee liability. |
| GOLD-KPI-024 | [Average Estimated Weekly Cost — Confirmed Referrals](#dax-business-average-estimated-weekly-cost-confirmed-referrals) | New Gold KPI | R62 | Average referral-level estimated weekly cost for issued IPAs, not actual cost. |
| GOLD-KPI-025 | [Provider Assignments](#dax-business-provider-assignments) | New Gold KPI | R24, R26 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-026 | [Provider Declines](#dax-business-provider-declines) | New Gold KPI | R54 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-027 | [Provider Decline Rate](#dax-business-provider-decline-rate) | New Gold KPI | R54 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-028 | [Snapshot Referrals](#dax-business-snapshot-referrals) | New Gold KPI | R24, R52 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-029 | [Open Referrals at Snapshot](#dax-business-open-referrals-at-snapshot) | New Gold KPI | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-030 | [Closed Referrals at Snapshot](#dax-business-closed-referrals-at-snapshot) | New Gold KPI | R13 | Closure-date predicate at the retained snapshot date; distinguish closed/cancelled status snapshot measure. |
| GOLD-KPI-031 | [Referrals with IPA at Snapshot](#dax-business-referrals-with-ipa-at-snapshot) | New Gold KPI | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-032 | [Open Overdue Referrals at Snapshot](#dax-business-open-overdue-referrals-at-snapshot) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-033 | [Open On-Track Referrals at Snapshot](#dax-business-open-on-track-referrals-at-snapshot) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-034 | [Open Referral Rate at Snapshot](#dax-business-open-referral-rate-at-snapshot) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-035 | [Placement Rate at Snapshot](#dax-business-placement-rate-at-snapshot) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-036 | [Referrals Created This Month](#dax-business-referrals-created-this-month) | KPI-23 | R24, R52 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-037 | [Referrals Created Previous Month](#dax-business-referrals-created-previous-month) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-038 | [Referral Volume Month on Month](#dax-business-referral-volume-month-on-month) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-039 | [Referral Volume Month on Month %](#dax-business-referral-volume-month-on-month-percent) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-040 | [Referrals Created This Financial Year](#dax-business-referrals-created-this-financial-year) | KPI-24 | R52 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-041 | [Referrals Currently Active](#dax-business-referrals-currently-active) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-042 | [Referrals Under Offer](#dax-business-referrals-under-offer) | KPI-30 | R24, R36 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-043 | [Closed or Cancelled Referrals](#dax-business-closed-or-cancelled-referrals) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-044 | [Active Referrals With Provider Engagement](#dax-business-active-referrals-with-provider-engagement) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-045 | [Active Referral Engagement Rate](#dax-business-active-referral-engagement-rate) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-046 | [Active Awaiting Offers With Engagement](#dax-business-active-awaiting-offers-with-engagement) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-047 | [Active Awaiting Offers Without Engagement](#dax-business-active-awaiting-offers-without-engagement) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-048 | [Emergency Referrals](#dax-business-emergency-referrals) | KPI-91 | R18, R57 | Same-day-date flag and active statuses; not an approved statutory emergency classification. |
| GOLD-KPI-049 | [Planned Referrals](#dax-business-planned-referrals) | KPI-93 | R57 | Different-date rule; missing dates excluded and reversed dates require review. |
| GOLD-KPI-050 | [Emergency Placement Rate](#dax-business-emergency-placement-rate) | KPI-92 | R18, R57 | Emergency-referral numerator divided by all selected referrals; not actual placement completion. |
| GOLD-KPI-051 | [Referrals With Multiple Provider Assignments](#dax-business-referrals-with-multiple-provider-assignments) | KPI-90 | R24, R26 (proposed) | Assignment overlap only; unrelated to out-of-region placement. |
| GOLD-KPI-052 | [Non-Draft Offers](#dax-business-non-draft-offers) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-053 | [Pending Offers](#dax-business-pending-offers) | KPI-18 | R24 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-054 | [Unsuccessful Offers](#dax-business-unsuccessful-offers) | KPI-16 | R28 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-055 | [Offers With Recorded Rejection Reason](#dax-business-offers-with-recorded-rejection-reason) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-056 | [Providers Who Made Offers](#dax-business-providers-who-made-offers) | KPI-11 | R25, R26 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-057 | [Average Offers per Provider](#dax-business-average-offers-per-provider) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-058 | [Average Offers per Referral Under Offer](#dax-business-average-offers-per-referral-under-offer) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-059 | [Offers on Referrals Under Offer](#dax-business-offers-on-referrals-under-offer) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-060 | [Spot Offers](#dax-business-spot-offers) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-061 | [Non-Spot Offers](#dax-business-non-spot-offers) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-062 | [Spot Offer Rate](#dax-business-spot-offer-rate) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-063 | [Draft Offers With No Activity Since Creation](#dax-business-draft-offers-with-no-activity-since-creation) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-064 | [Draft Offers With Activity Since Creation](#dax-business-draft-offers-with-activity-since-creation) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-065 | [Draft Offers Missing Dates](#dax-business-draft-offers-missing-dates) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-066 | [Draft Offers Stalled 14+ Days](#dax-business-draft-offers-stalled-14-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-067 | [Average Days in Draft](#dax-business-average-days-in-draft) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-068 | [Oldest Draft Age Days](#dax-business-oldest-draft-age-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-069 | [Draft Offers With No Activity %](#dax-business-draft-offers-with-no-activity-percent) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-070 | [Pending Offers 0-7 Days](#dax-business-pending-offers-0-7-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-071 | [Pending Offers 8-14 Days](#dax-business-pending-offers-8-14-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-072 | [Pending Offers 15-29 Days](#dax-business-pending-offers-15-29-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-073 | [Pending Offers 30+ Days](#dax-business-pending-offers-30-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-074 | [Providers With Pending Offers 30+ Days](#dax-business-providers-with-pending-offers-30-days) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-075 | [Latest Offer Source Export](#dax-business-latest-offer-source-export) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-076 | [Provider Homes Registered](#dax-business-provider-homes-registered) | KPI-40 | R91, R93 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-077 | [Providers Registered](#dax-business-providers-registered) | KPI-41 | R91, R93 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-078 | [Providers - Fostering](#dax-business-providers-fostering) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-079 | [Providers - Residential](#dax-business-providers-residential) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-080 | [Providers - Supported Accommodation](#dax-business-providers-supported-accommodation) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-081 | [Residential Homes](#dax-business-residential-homes) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-082 | [Supported Accommodation Homes](#dax-business-supported-accommodation-homes) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-083 | [Fostering Homes](#dax-business-fostering-homes) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-084 | [Framework Providers](#dax-business-framework-providers) | KPI-45 | R67 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-085 | [Non-Framework Providers](#dax-business-non-framework-providers) | KPI-46 | R46 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-086 | [Providers With QA Flags](#dax-business-providers-with-qa-flags) | KPI-97 | R41 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-087 | [QA Flagged Homes](#dax-business-qa-flagged-homes) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-088 | [Providers Pending Onboarding](#dax-business-providers-pending-onboarding) | KPI-116 | R59 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-089 | [Providers Approved](#dax-business-providers-approved) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-090 | [Provider Onboarding Success Rate](#dax-business-provider-onboarding-success-rate) | KPI-117 | R59 | Approved-provider share, not bulk onboarding job success. |
| GOLD-KPI-091 | [Provider Submission Documents](#dax-business-provider-submission-documents) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-092 | [Documents Expiring Next 30 Days](#dax-business-documents-expiring-next-30-days) | KPI-100 | R47 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-093 | [Documents Expired](#dax-business-documents-expired) | KPI-101 | R47, R48 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-094 | [Provider Homes With Expired Documents](#dax-business-provider-homes-with-expired-documents) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-095 | [IPAs Issued This Month](#dax-business-ipas-issued-this-month) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-096 | [Closed IPAs](#dax-business-closed-ipas) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-097 | [Average Active IPA Weekly Cost](#dax-business-average-active-ipa-weekly-cost) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-098 | [Total IPA Weekly Cost](#dax-business-total-ipa-weekly-cost) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-099 | [Accepted Offers With IPA](#dax-business-accepted-offers-with-ipa) | KPI-79 replacement | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-100 | [Offers Awaiting IPA Creation](#dax-business-offers-awaiting-ipa-creation) | KPI-79 | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-101 | [Accepted Offer to IPA Conversion %](#dax-business-accepted-offer-to-ipa-conversion-percent) | KPI-83 | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-102 | [Offers Still to Progress to IPA %](#dax-business-offers-still-to-progress-to-ipa-percent) | KPI-84 | R35 | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-103 | [Referrals With Fully Signed IPA](#dax-business-referrals-with-fully-signed-ipa) | New Gold KPI | — | Distinct referral IDs with at least one completed IPA; not a count of IPAs. |
| GOLD-KPI-104 | [IPA Signature Completion Rate](#dax-business-ipa-signature-completion-rate) | New Gold KPI | — | IPA Completed / IPAs Created at IPA grain; both signature flags required. |
| GOLD-KPI-105 | [Referral Lifecycle Events](#dax-business-referral-lifecycle-events) | KPI-113 | R20 | Derived activity roll-up, not a complete source audit trail. |
| GOLD-KPI-106 | [Referrals With Lifecycle Activity](#dax-business-referrals-with-lifecycle-activity) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-107 | [Average Lifecycle Events per Referral](#dax-business-average-lifecycle-events-per-referral) | New Gold KPI | — | Definition present in WIP _Measures. Reconcile against refreshed Gold and approved business rules. |
| GOLD-KPI-108 | [Gold Model Last Refreshed](#dax-business-gold-model-last-refreshed) | KPI-87 | R82 | Persisted Gold build timestamp; not source completeness or service-performance evidence. |
| GOLD-KPI-109 | [Provider Messages Sent](#dax-business-provider-messages-sent) | KPI-110 proxy | R14 | Counts ProviderMessageSent lifecycle events; either sender may be represented. Not provider-authored response time. |
| GOLD-KPI-110 | [Male Referrals](#dax-business-male-referrals) | WIP addition | R51 (proposed) | Gender-based referral analysis; reconcile unknowns and validate access controls. |
| GOLD-KPI-111 | [Female Referrals](#dax-business-female-referrals) | WIP addition | R51 (proposed) | Gender-based referral analysis; reconcile unknowns and validate access controls. |
| GOLD-KPI-112 | [Other Gender Referrals](#dax-business-other-gender-referrals) | WIP addition | R51 (proposed) | Gender-based referral analysis; reconcile unknowns and validate access controls. |
| GOLD-KPI-113 | [Total Gendered Referrals](#dax-business-total-gendered-referrals) | WIP addition | R51 (proposed) | Gender-based referral analysis; reconcile unknowns and validate access controls. |
| GOLD-KPI-114 | [IPA Completed](#dax-business-ipa-completed) | WIP addition | R15, R35, R62 (proposed) | IPA-grain completion/signing backlog; completed includes closed signed records; pending excludes closed unsigned records. |
| GOLD-KPI-115 | [IPAs Pending Completion](#dax-business-ipas-pending-completion) | WIP addition | R15, R35, R62 (proposed) | IPA-grain completion/signing backlog; completed includes closed signed records; pending excludes closed unsigned records. |
| GOLD-KPI-116 | [IPAs Signed by Provider](#dax-business-ipas-signed-by-provider) | WIP addition | R15, R35, R62 (proposed) | IPA-grain completion/signing backlog; completed includes closed signed records; pending excludes closed unsigned records. |
| GOLD-KPI-117 | [IPAs Signed by Local Authority](#dax-business-ipas-signed-by-local-authority) | WIP addition | R15, R35, R62 (proposed) | IPA-grain completion/signing backlog; completed includes closed signed records; pending excludes closed unsigned records. |
| GOLD-KPI-118 | [Snapshot referrals previous month](#dax-business-snapshot-referrals-previous-month) | WIP addition | R24, R51, R52 (proposed) | Compare retained month-end state with the prior calendar month; missing prior data remains blank. |
| GOLD-KPI-119 | [Snapshot referrals MoM change](#dax-business-snapshot-referrals-mom-change) | WIP addition | R24, R51, R52 (proposed) | Compare retained month-end state with the prior calendar month; missing prior data remains blank. |
| GOLD-KPI-120 | [Snapshot referrals MoM percent](#dax-business-snapshot-referrals-mom-percent) | WIP addition | R24, R51, R52 (proposed) | Compare retained month-end state with the prior calendar month; missing prior data remains blank. |
| GOLD-KPI-121 | [Referrals closed during month](#dax-business-referrals-closed-during-month) | WIP addition | R24, R51 (proposed) | Distinct referrals by closure date in month; a flow measure, not closed state at snapshot. Closure date is derived. |
| GOLD-KPI-122 | [Matching referrals](#dax-business-matching-referrals) | WIP addition | R13, R24, R25 (proposed) | Distinct referrals after category and matching-offer filters; category totals are not additive. |
| GOLD-KPI-123 | [Journey referrals 1](#dax-business-journey-referrals-1) | WIP addition | R24, R25, R35, R51 (proposed) | Referral created. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-124 | [Journey referrals 2](#dax-business-journey-referrals-2) | WIP addition | R24, R25, R35, R51 (proposed) | Provider search. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-125 | [Journey referrals 3](#dax-business-journey-referrals-3) | WIP addition | R24, R25, R35, R51 (proposed) | Offers received. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-126 | [Journey referrals 4](#dax-business-journey-referrals-4) | WIP addition | R24, R25, R35, R51 (proposed) | Offer accepted. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-127 | [Journey referrals 5](#dax-business-journey-referrals-5) | WIP addition | R24, R25, R35, R51 (proposed) | IPA created. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-128 | [Journey referrals 6](#dax-business-journey-referrals-6) | WIP addition | R24, R25, R35, R51 (proposed) | IPA signed. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-129 | [Journey referrals 7](#dax-business-journey-referrals-7) | WIP addition | R24, R25, R35, R51 (proposed) | Closed / cancelled / withdrawn. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-130 | [Journey referrals 8](#dax-business-journey-referrals-8) | WIP addition | R24, R25, R35, R51 (proposed) | Needs review. One current stage per referral at refresh. Closed status overrides milestones; counts are not historic funnel conversion. |
| GOLD-KPI-131 | [Journey providers 0](#dax-business-journey-providers-0) | WIP addition | R24, R26, R28, R35 (proposed) | Assigned / draft / unclear. Distinct provider at furthest evidenced stage in current cohort; not additive offer counts. No browsing evidence. |
| GOLD-KPI-132 | [Journey providers 1](#dax-business-journey-providers-1) | WIP addition | R24, R26, R28, R35 (proposed) | Message activity only. Distinct provider at furthest evidenced stage in current cohort; not additive offer counts. No browsing evidence. |
| GOLD-KPI-133 | [Journey providers 2](#dax-business-journey-providers-2) | WIP addition | R24, R26, R28, R35 (proposed) | Offers made. Distinct provider at furthest evidenced stage in current cohort; not additive offer counts. No browsing evidence. |
| GOLD-KPI-134 | [Journey providers 3](#dax-business-journey-providers-3) | WIP addition | R24, R26, R28, R35 (proposed) | Offer accepted. Distinct provider at furthest evidenced stage in current cohort; not additive offer counts. No browsing evidence. |
| GOLD-KPI-135 | [Journey providers 5](#dax-business-journey-providers-5) | WIP addition | R24, R26, R28, R35 (proposed) | Provider signed. Distinct provider at furthest evidenced stage in current cohort; not additive offer counts. No browsing evidence. |
| GOLD-KPI-136 | [Journey providers both signed](#dax-business-journey-providers-both-signed) | WIP addition | R35, R62 (proposed) | Providers with both-signed IPA evidence; subset of provider-signed, not a further stage. |
| GOLD-KPI-137 | [Provider Response Rate](#dax-business-provider-response-rate) | WIP addition | R26, R51 (proposed) | Assignment-cohort component based on qualifying offers/reasons. Not a message SLA, composite score or suitability rating. |
| GOLD-KPI-138 | [Provider Average Response Hours](#dax-business-provider-average-response-hours) | WIP addition | R26, R51 (proposed) | Assignment-cohort component based on qualifying offers/reasons. Not a message SLA, composite score or suitability rating. |
| GOLD-KPI-139 | [Provider Offer Conversion Rate](#dax-business-provider-offer-conversion-rate) | WIP addition | R26, R51 (proposed) | Assignment-cohort component based on qualifying offers/reasons. Not a message SLA, composite score or suitability rating. |
| GOLD-KPI-140 | [Provider Target Placement Rate](#dax-business-provider-target-placement-rate) | WIP addition | R26, R51 (proposed) | Assignment-cohort component based on qualifying offers/reasons. Not a message SLA, composite score or suitability rating. |
| GOLD-KPI-141 | [Preferred-city distance coverage](#dax-business-preferred-city-distance-coverage) | WIP addition | R13, R51 (proposed) | Share of offers with preference-city distance evidence. Missing coordinates are not zero distance. |
| GOLD-KPI-142 | [Median preferred-city distance km](#dax-business-median-preferred-city-distance-km) | WIP addition | R13, R51 (proposed) | City-centroid to postcode straight-line estimate, not child-address or road distance; approved coordinates required. |
| GOLD-KPI-143 | [Homes Offered](#dax-business-homes-offered) | WIP addition | R26, R51, R93 (proposed) | Distinct offered homes in current context; not spare capacity or available beds. |
| GOLD-KPI-144 | [Critical Overdue Referrals](#dax-business-critical-overdue-referrals) | WIP addition | R16, R24 (proposed) | Operational overdue/critical cohort; validate urgency rule with owner before escalation. |

## Mission Control operational coverage

Current source is `reports/current/SM WMPP Mission Control Im.zip`, not the smaller LM package. Its 33 tables include contracts, schema/drift, DQ results, referential exceptions, rejected keys, domain profiles, lineage, load metrics and archive/replay controls. There are 17 page definitions (10 visible, seven hidden guides/tooltips/drillthrough helpers). Exactly 102 measures are directly bound on visible pages; further measures are dependencies or unbound helpers. A visual binding establishes saved wiring, not correct rendering, current source data or role acceptance.

| Requirement | Contribution | Boundary / remaining decision | Named operational measures (proposed association) |
|---|---|---|---|
| R20 | Operational context only: Pipeline/job execution is not the business placement, signature or notification audit trail. | Derived lifecycle events do not provide durable full audit history, exact signature events or notification delivery. Mission Control: Operational context only. Pipeline/job execution is not the business placement, signature or notification audit trail. Historical v1 status: ❌ Missing. | [Job Runs](#dax-mission-job-runs); [Failed Job Runs](#dax-mission-failed-job-runs) |
| R53 | Partial operational support: DQ results, rejected keys, lineage and load metrics support consistency; export rights and reconciliation still need acceptance. | Saved-file definitions exist. Full refreshed DAX reconciliation, data completeness and business acceptance remain open. Mission Control: Partial operational support. DQ results, rejected keys, lineage and load metrics support consistency; export rights and reconciliation still need acceptance. Historical v1 status: ✅ Implemented. | [DQ Failed Rows](#dax-mission-dq-failed-rows); [Weighted DQ Failure Percentage](#dax-mission-weighted-dq-failure-percentage) |
| R69 | Supporting design evidence: Governed contract/schema and lineage imports support model controls; robustness and performance need runtime tests. | Saved-file definitions exist. Full refreshed DAX reconciliation, data completeness and business acceptance remain open. Mission Control: Supporting design evidence. Governed contract/schema and lineage imports support model controls; robustness and performance need runtime tests. Historical v1 status: ℹ️ Non-functional. | [Discovery cfg_schema_contract_column Rows](#dax-mission-discovery-cfg-schema-contract-column-rows); [Discovery rpt_job_layer_lineage Rows](#dax-mission-discovery-rpt-job-layer-lineage-rows) |
| R75 | Partial operational support: Run status and timing support operations; availability, scalability, DR/RTO/RPO and failover are not proven. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Partial operational support. Run status and timing support operations; availability, scalability, DR/RTO/RPO and failover are not proven. Historical v1 status: ℹ️ Non-functional. | [Job Success Rate](#dax-mission-job-success-rate); [P95 Pipeline Duration (min)](#dax-mission-p95-pipeline-duration-min) |
| R82 | Partial operational support: Pipeline duration, throughput and prior-run benchmarks exist; these do not measure portal/report response latency or certify an SLA. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Partial operational support. Pipeline duration, throughput and prior-run benchmarks exist; these do not measure portal/report response latency or certify an SLA. Historical v1 status: ✅ Implemented. | [Pipeline Rows per Minute](#dax-mission-pipeline-rows-per-minute); [P95 Pipeline Duration (min)](#dax-mission-p95-pipeline-duration-min); [Job prior median min](#dax-mission-job-prior-median-min) |
| R83 | Partial operational support: Archive/replay controls and load rows provide migration evidence, not complete source-to-target migration acceptance. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Partial operational support. Archive/replay controls and load rows provide migration evidence, not complete source-to-target migration acceptance. Historical v1 status: ℹ️ Non-functional. | [Archive File Rows Written](#dax-mission-archive-file-rows-written); [Gold Snapshot Runs](#dax-mission-gold-snapshot-runs) |
| R84 | Partial operational support: DQ/RI exceptions, drift, lineage and retained domain evidence exist; retention/export policy and security acceptance remain open. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Partial operational support. DQ/RI exceptions, drift, lineage and retained domain evidence exist; retention/export policy and security acceptance remain open. Historical v1 status: ℹ️ Non-functional. | [RI Failed Rows](#dax-mission-ri-failed-rows); [Discovery cfg_schema_drift_event Rows](#dax-mission-discovery-cfg-schema-drift-event-rows); [Discovery cfg_data_domain Rows](#dax-mission-discovery-cfg-data-domain-rows) |
| R85 | Supporting documentation evidence: Operational pages and runbooks support handover; FAQs, user training, support readiness and client approval remain separate. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Supporting documentation evidence. Operational pages and runbooks support handover; FAQs, user training, support readiness and client approval remain separate. Historical v1 status: ℹ️ Non-functional. | [Operational Exception Count](#dax-mission-operational-exception-count) |
| R87 | Partial operational support: Failures, error detail and reload queues support incident triage; notification delivery, ticket workflow and SLA ownership are not implemented by these cards. | Report/model files do not establish availability, accessibility, SLA, device compatibility, migration completeness, retention or formal sign-off. Mission Control: Partial operational support. Failures, error detail and reload queues support incident triage; notification delivery, ticket workflow and SLA ownership are not implemented by these cards. Historical v1 status: ℹ️ Non-functional. | [Operational Exception Count](#dax-mission-operational-exception-count); [Reload Requests](#dax-mission-reload-requests); [Failed Pipeline Runs](#dax-mission-failed-pipeline-runs) |
| R88 | Supporting change-control evidence: Versioned contracts, source-controlled notebooks and discovery evidence support controlled change, not full roadmap/governance acceptance. | Design and roadmap evidence is separate from KPI coverage or production acceptance. Mission Control: Supporting change-control evidence. Versioned contracts, source-controlled notebooks and discovery evidence support controlled change, not full roadmap/governance acceptance. Historical v1 status: ℹ️ Non-functional. | [Discovery cfg_schema_contract_column Rows](#dax-mission-discovery-cfg-schema-contract-column-rows) |

### Mission Control page inventory

| Page | Visibility |
|---|---|
| Job Step Detail (Drillthrough) | HiddenInViewMode |
| Contracts & Schema | visible |
| Domains & Reference | visible |
| Job & Step Timelines - guide | HiddenInViewMode |
| Job Run Tooltip | HiddenInViewMode |
| Lineage & Step Summary | visible |
| Archive & Replay | visible |
| Job Step Detail (Drillthrough) - guide | HiddenInViewMode |
| Quality & Schema - guide | HiddenInViewMode |
| Load Calendar | visible |
| Quality & Exceptions | visible |
| Load Metrics & Control | visible |
| Archive & Replay - guide | HiddenInViewMode |
| Quality & Schema | visible |
| Job & Step Timelines | visible |
| Schema & Drift | visible |
| Load Calendar - guide | HiddenInViewMode |

### Operational measure inventory

All saved measures are included for calculation transparency; helper measures are not additional accepted KPIs.

| Measure | Container | Direct visible-page binding | Requirement association |
|---|---|---|---|
| [Runs](#dax-mission-runs) | `_Load Experience` | No direct visible binding verified | None asserted |
| [Successful](#dax-mission-successful) | `_Load Experience` | No direct visible binding verified | None asserted |
| [Failures](#dax-mission-failures) | `_Load Experience` | No direct visible binding verified | None asserted |
| [In progress or other](#dax-mission-in-progress-or-other) | `_Load Experience` | No direct visible binding verified | None asserted |
| [Success rate](#dax-mission-success-rate) | `_Load Experience` | No direct visible binding verified | None asserted |
| [P95 duration min](#dax-mission-p95-duration-min) | `_Load Experience` | No direct visible binding verified | None asserted |
| [Rows written](#dax-mission-rows-written) | `_Load Experience` | No direct visible binding verified | None asserted |
| [Day tile](#dax-mission-day-tile) | `_Load Experience` | Load Calendar | None asserted |
| [Day colour](#dax-mission-day-colour) | `_Load Experience` | Load Calendar | None asserted |
| [Day text colour](#dax-mission-day-text-colour) | `_Load Experience` | Load Calendar | None asserted |
| [Pipeline Runs](#dax-mission-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Successful Pipeline Runs](#dax-mission-successful-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Pipeline Runs](#dax-mission-failed-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | R87 (proposed) |
| [Running Pipeline Runs](#dax-mission-running-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Completed Pipeline Runs](#dax-mission-completed-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Success Rate](#dax-mission-pipeline-success-rate) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Live Pipeline Runs](#dax-mission-live-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Pipeline Runs](#dax-mission-archive-pipeline-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Live Pipeline Failures](#dax-mission-live-pipeline-failures) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Pipeline Failures](#dax-mission-archive-pipeline-failures) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Tables Succeeded](#dax-mission-pipeline-tables-succeeded) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Tables Failed](#dax-mission-pipeline-tables-failed) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Rows Read](#dax-mission-pipeline-rows-read) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Rows Written](#dax-mission-pipeline-rows-written) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Runs With Error](#dax-mission-pipeline-runs-with-error) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Average Pipeline Duration (min)](#dax-mission-average-pipeline-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [P95 Pipeline Duration (min)](#dax-mission-p95-pipeline-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | R75, R82 (proposed) |
| [Total Pipeline Duration (min)](#dax-mission-total-pipeline-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Pipeline Rows per Minute](#dax-mission-pipeline-rows-per-minute) | `_MissionControl_Measures` | No direct visible binding verified | R82 (proposed) |
| [Latest Pipeline End](#dax-mission-latest-pipeline-end) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Pipeline Status](#dax-mission-latest-pipeline-status) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive ZIP Batches](#dax-mission-archive-zip-batches) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Successful Archive ZIP Batches](#dax-mission-successful-archive-zip-batches) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Archive ZIP Batches](#dax-mission-failed-archive-zip-batches) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive ZIP Batches Awaiting Reload](#dax-mission-archive-zip-batches-awaiting-reload) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive ZIP Files Declared](#dax-mission-archive-zip-files-declared) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Average Archive ZIP Duration (min)](#dax-mission-average-archive-zip-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Files Processed](#dax-mission-archive-files-processed) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Successful Archive Files](#dax-mission-successful-archive-files) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive File Failures](#dax-mission-archive-file-failures) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Files Awaiting Reload](#dax-mission-archive-files-awaiting-reload) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive File Rows Read](#dax-mission-archive-file-rows-read) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive File Rows Written](#dax-mission-archive-file-rows-written) | `_MissionControl_Measures` | No direct visible binding verified | R83 (proposed) |
| [Archive Table Exports](#dax-mission-archive-table-exports) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Archive Table Exports](#dax-mission-failed-archive-table-exports) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Table Exports Awaiting Reload](#dax-mission-archive-table-exports-awaiting-reload) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archive Export Rows](#dax-mission-archive-export-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Gold Snapshot Runs](#dax-mission-gold-snapshot-runs) | `_MissionControl_Measures` | No direct visible binding verified | R83 (proposed) |
| [Successful Gold Snapshots](#dax-mission-successful-gold-snapshots) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Gold Snapshots](#dax-mission-failed-gold-snapshots) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Gold Snapshots Awaiting Replay](#dax-mission-gold-snapshots-awaiting-replay) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Gold Snapshot DQ Failures](#dax-mission-gold-snapshot-dq-failures) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Checks](#dax-mission-dq-checks) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Evaluated Checks](#dax-mission-dq-evaluated-checks) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Failed Checks](#dax-mission-dq-failed-checks) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Failure Rate](#dax-mission-dq-failure-rate) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Checked Rows](#dax-mission-dq-checked-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Failed Rows](#dax-mission-dq-failed-rows) | `_MissionControl_Measures` | No direct visible binding verified | R53 (proposed) |
| [Weighted DQ Failure Percentage](#dax-mission-weighted-dq-failure-percentage) | `_MissionControl_Measures` | No direct visible binding verified | R53 (proposed) |
| [Critical Rules Failing](#dax-mission-critical-rules-failing) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [High or Critical Rules Failing](#dax-mission-high-or-critical-rules-failing) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [DQ Failures With Sample Keys](#dax-mission-dq-failures-with-sample-keys) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Active DQ Rules](#dax-mission-active-dq-rules) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Critical Active DQ Rules](#dax-mission-critical-active-dq-rules) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [RI Rules Failing](#dax-mission-ri-rules-failing) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [RI Checked Rows](#dax-mission-ri-checked-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [RI Failed Rows](#dax-mission-ri-failed-rows) | `_MissionControl_Measures` | No direct visible binding verified | R84 (proposed) |
| [RI Failure Rate](#dax-mission-ri-failure-rate) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archived Schema Columns](#dax-mission-archived-schema-columns) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archived Schema Tables](#dax-mission-archived-schema-tables) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Archived Schema Capture](#dax-mission-latest-archived-schema-capture) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archived Nullable Columns](#dax-mission-archived-nullable-columns) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Archived Schema Data Types](#dax-mission-archived-schema-data-types) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Reload Requests](#dax-mission-reload-requests) | `_MissionControl_Measures` | No direct visible binding verified | R87 (proposed) |
| [Control Failures](#dax-mission-control-failures) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Operational Exception Count](#dax-mission-operational-exception-count) | `_MissionControl_Measures` | No direct visible binding verified | R85, R87 (proposed) |
| [Dashboard Last Refreshed](#dax-mission-dashboard-last-refreshed) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Job Runs](#dax-mission-job-runs) | `_MissionControl_Measures` | No direct visible binding verified | R20 (proposed) |
| [Successful Job Runs](#dax-mission-successful-job-runs) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Job Runs](#dax-mission-failed-job-runs) | `_MissionControl_Measures` | No direct visible binding verified | R20 (proposed) |
| [Job Success Rate](#dax-mission-job-success-rate) | `_MissionControl_Measures` | No direct visible binding verified | R75 (proposed) |
| [Latest Job Run Started](#dax-mission-latest-job-run-started) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Job Run ID](#dax-mission-latest-job-run-id) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Job Run ID](#dax-mission-selected-or-latest-job-run-id) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Job Status](#dax-mission-selected-or-latest-job-status) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Job Error](#dax-mission-selected-or-latest-job-error) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Job Duration (min)](#dax-mission-selected-or-latest-job-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Job Steps](#dax-mission-job-steps) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Successful Job Steps](#dax-mission-successful-job-steps) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Failed Job Steps](#dax-mission-failed-job-steps) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Job Steps With Error](#dax-mission-job-steps-with-error) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Job Steps](#dax-mission-selected-or-latest-job-steps) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected or Latest Failed Steps](#dax-mission-selected-or-latest-failed-steps) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Total Job Step Duration (min)](#dax-mission-total-job-step-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Longest Job Step Duration (min)](#dax-mission-longest-job-step-duration-min) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Show Step for Selected or Latest Job Run](#dax-mission-show-step-for-selected-or-latest-job-run) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Selected Step Error Detail](#dax-mission-selected-step-error-detail) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Load Run ID](#dax-mission-latest-load-run-id) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Started](#dax-mission-latest-load-started) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Load Status](#dax-mission-latest-load-status) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Quality Records](#dax-mission-latest-load-quality-records) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest Load Evaluated Checks](#dax-mission-latest-load-evaluated-checks) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Failed Checks](#dax-mission-latest-load-failed-checks) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Failed Rows](#dax-mission-latest-load-failed-rows) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Critical Rules](#dax-mission-latest-load-critical-rules) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Show Latest Load Quality](#dax-mission-show-latest-load-quality) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Latest Load Quality Report](#dax-mission-latest-load-quality-report) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Calendar Day Runs](#dax-mission-calendar-day-runs) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Calendar Day Failures](#dax-mission-calendar-day-failures) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Calendar Day Other](#dax-mission-calendar-day-other) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Calendar Day In Window](#dax-mission-calendar-day-in-window) | `_MissionControl_Measures` | Contracts & Schema; Domains & Reference; Lineage & Step Summary; Load Calendar; Load Metrics & Control; Quality & Exceptions; Schema & Drift | None asserted |
| [Day Explorer Job Visible](#dax-mission-day-explorer-job-visible) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Timeline Job Visible](#dax-mission-timeline-job-visible) | `_MissionControl_Measures` | Job & Step Timelines | None asserted |
| [Timeline Step Visible](#dax-mission-timeline-step-visible) | `_MissionControl_Measures` | Job & Step Timelines | None asserted |
| [Discovery history selected](#dax-mission-discovery-history-selected) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_data_domain Latest time](#dax-mission-discovery-cfg-data-domain-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_data_domain Latest key](#dax-mission-discovery-cfg-data-domain-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_data_domain Rows](#dax-mission-discovery-cfg-data-domain-rows) | `_MissionControl_Measures` | Domains & Reference | R84 (proposed) |
| [Discovery cfg_data_domain Visible](#dax-mission-discovery-cfg-data-domain-visible) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_data_domain Selected time](#dax-mission-discovery-cfg-data-domain-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_data_domain State](#dax-mission-discovery-cfg-data-domain-state) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_location_coordinate Rows](#dax-mission-discovery-cfg-location-coordinate-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_location_coordinate Visible](#dax-mission-discovery-cfg-location-coordinate-visible) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_location_coordinate State](#dax-mission-discovery-cfg-location-coordinate-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_event Latest time](#dax-mission-discovery-cfg-schema-drift-event-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_event Latest key](#dax-mission-discovery-cfg-schema-drift-event-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_event Rows](#dax-mission-discovery-cfg-schema-drift-event-rows) | `_MissionControl_Measures` | Schema & Drift | R84 (proposed) |
| [Discovery cfg_schema_drift_event Visible](#dax-mission-discovery-cfg-schema-drift-event-visible) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_drift_event Selected time](#dax-mission-discovery-cfg-schema-drift-event-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_event State](#dax-mission-discovery-cfg-schema-drift-event-state) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery rpt_job_schema_drift Latest time](#dax-mission-discovery-rpt-job-schema-drift-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_schema_drift Latest key](#dax-mission-discovery-rpt-job-schema-drift-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_schema_drift Rows](#dax-mission-discovery-rpt-job-schema-drift-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_schema_drift Visible](#dax-mission-discovery-rpt-job-schema-drift-visible) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery rpt_job_schema_drift Selected time](#dax-mission-discovery-rpt-job-schema-drift-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_schema_drift State](#dax-mission-discovery-rpt-job-schema-drift-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_definition Latest time](#dax-mission-discovery-cfg-schema-drift-definition-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_definition Rows](#dax-mission-discovery-cfg-schema-drift-definition-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_definition Visible](#dax-mission-discovery-cfg-schema-drift-definition-visible) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_drift_definition Selected time](#dax-mission-discovery-cfg-schema-drift-definition-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_drift_definition State](#dax-mission-discovery-cfg-schema-drift-definition-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_definition_candidate Rows](#dax-mission-discovery-cfg-schema-definition-candidate-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_definition_candidate Visible](#dax-mission-discovery-cfg-schema-definition-candidate-visible) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_definition_candidate State](#dax-mission-discovery-cfg-schema-definition-candidate-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_bronze_schema_live Latest time](#dax-mission-discovery-cfg-bronze-schema-live-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_bronze_schema_live Latest key](#dax-mission-discovery-cfg-bronze-schema-live-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_bronze_schema_live Rows](#dax-mission-discovery-cfg-bronze-schema-live-rows) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_bronze_schema_live Visible](#dax-mission-discovery-cfg-bronze-schema-live-visible) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_bronze_schema_live Selected time](#dax-mission-discovery-cfg-bronze-schema-live-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_bronze_schema_live State](#dax-mission-discovery-cfg-bronze-schema-live-state) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_schema_contract_column Latest time](#dax-mission-discovery-cfg-schema-contract-column-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_contract_column Rows](#dax-mission-discovery-cfg-schema-contract-column-rows) | `_MissionControl_Measures` | No direct visible binding verified | R69, R88 (proposed) |
| [Discovery cfg_schema_contract_column Visible](#dax-mission-discovery-cfg-schema-contract-column-visible) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_schema_contract_column Selected time](#dax-mission-discovery-cfg-schema-contract-column-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_schema_contract_column State](#dax-mission-discovery-cfg-schema-contract-column-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_data_quality Latest time](#dax-mission-discovery-rpt-job-data-quality-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_data_quality Latest key](#dax-mission-discovery-rpt-job-data-quality-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_data_quality Rows](#dax-mission-discovery-rpt-job-data-quality-rows) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery rpt_job_data_quality Visible](#dax-mission-discovery-rpt-job-data-quality-visible) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery rpt_job_data_quality Selected time](#dax-mission-discovery-rpt-job-data-quality-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_data_quality State](#dax-mission-discovery-rpt-job-data-quality-state) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery cfg_rejected_row Latest time](#dax-mission-discovery-cfg-rejected-row-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_rejected_row Latest key](#dax-mission-discovery-cfg-rejected-row-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_rejected_row Rows](#dax-mission-discovery-cfg-rejected-row-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_rejected_row Visible](#dax-mission-discovery-cfg-rejected-row-visible) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery cfg_rejected_row Selected time](#dax-mission-discovery-cfg-rejected-row-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_rejected_row State](#dax-mission-discovery-cfg-rejected-row-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_referential_exception Latest time](#dax-mission-discovery-cfg-referential-exception-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_referential_exception Latest key](#dax-mission-discovery-cfg-referential-exception-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_referential_exception Rows](#dax-mission-discovery-cfg-referential-exception-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_referential_exception Visible](#dax-mission-discovery-cfg-referential-exception-visible) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery cfg_referential_exception Selected time](#dax-mission-discovery-cfg-referential-exception-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_referential_exception State](#dax-mission-discovery-cfg-referential-exception-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_table_load_metric Latest time](#dax-mission-discovery-cfg-table-load-metric-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_table_load_metric Latest key](#dax-mission-discovery-cfg-table-load-metric-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_table_load_metric Rows](#dax-mission-discovery-cfg-table-load-metric-rows) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_table_load_metric Visible](#dax-mission-discovery-cfg-table-load-metric-visible) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_table_load_metric Selected time](#dax-mission-discovery-cfg-table-load-metric-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_table_load_metric State](#dax-mission-discovery-cfg-table-load-metric-state) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_silver_export_load Latest time](#dax-mission-discovery-cfg-silver-export-load-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_export_load Latest key](#dax-mission-discovery-cfg-silver-export-load-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_export_load Rows](#dax-mission-discovery-cfg-silver-export-load-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_export_load Visible](#dax-mission-discovery-cfg-silver-export-load-visible) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_silver_export_load Selected time](#dax-mission-discovery-cfg-silver-export-load-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_export_load State](#dax-mission-discovery-cfg-silver-export-load-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_load_control Latest time](#dax-mission-discovery-cfg-silver-load-control-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_load_control Latest key](#dax-mission-discovery-cfg-silver-load-control-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_load_control Rows](#dax-mission-discovery-cfg-silver-load-control-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_load_control Visible](#dax-mission-discovery-cfg-silver-load-control-visible) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_silver_load_control Selected time](#dax-mission-discovery-cfg-silver-load-control-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_silver_load_control State](#dax-mission-discovery-cfg-silver-load-control-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_layer_lineage Latest time](#dax-mission-discovery-rpt-job-layer-lineage-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_layer_lineage Latest key](#dax-mission-discovery-rpt-job-layer-lineage-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_layer_lineage Rows](#dax-mission-discovery-rpt-job-layer-lineage-rows) | `_MissionControl_Measures` | Lineage & Step Summary | R69 (proposed) |
| [Discovery rpt_job_layer_lineage Visible](#dax-mission-discovery-rpt-job-layer-lineage-visible) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_layer_lineage Selected time](#dax-mission-discovery-rpt-job-layer-lineage-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_layer_lineage State](#dax-mission-discovery-rpt-job-layer-lineage-state) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_step_summary Latest time](#dax-mission-discovery-rpt-job-step-summary-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_step_summary Latest key](#dax-mission-discovery-rpt-job-step-summary-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_step_summary Rows](#dax-mission-discovery-rpt-job-step-summary-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_step_summary Visible](#dax-mission-discovery-rpt-job-step-summary-visible) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_step_summary Selected time](#dax-mission-discovery-rpt-job-step-summary-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery rpt_job_step_summary State](#dax-mission-discovery-rpt-job-step-summary-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_gold_lineage_mapping Rows](#dax-mission-discovery-cfg-gold-lineage-mapping-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_gold_lineage_mapping Visible](#dax-mission-discovery-cfg-gold-lineage-mapping-visible) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery cfg_gold_lineage_mapping State](#dax-mission-discovery-cfg-gold-lineage-mapping-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_data_domain Context](#dax-mission-discovery-cfg-data-domain-context) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_data_domain Scope count](#dax-mission-discovery-cfg-data-domain-scope-count) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_data_domain Distinct objects](#dax-mission-discovery-cfg-data-domain-distinct-objects) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_data_domain Discovery batches](#dax-mission-discovery-cfg-data-domain-discovery-batches) | `_MissionControl_Measures` | Domains & Reference | None asserted |
| [Discovery cfg_schema_drift_event Context](#dax-mission-discovery-cfg-schema-drift-event-context) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_drift_event Scope count](#dax-mission-discovery-cfg-schema-drift-event-scope-count) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_drift_event Distinct objects](#dax-mission-discovery-cfg-schema-drift-event-distinct-objects) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_schema_drift_event Discovery batches](#dax-mission-discovery-cfg-schema-drift-event-discovery-batches) | `_MissionControl_Measures` | Schema & Drift | None asserted |
| [Discovery cfg_bronze_schema_live Context](#dax-mission-discovery-cfg-bronze-schema-live-context) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_bronze_schema_live Scope count](#dax-mission-discovery-cfg-bronze-schema-live-scope-count) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_bronze_schema_live Distinct objects](#dax-mission-discovery-cfg-bronze-schema-live-distinct-objects) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery cfg_bronze_schema_live Discovery batches](#dax-mission-discovery-cfg-bronze-schema-live-discovery-batches) | `_MissionControl_Measures` | Contracts & Schema | None asserted |
| [Discovery rpt_job_data_quality Context](#dax-mission-discovery-rpt-job-data-quality-context) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery rpt_job_data_quality Scope count](#dax-mission-discovery-rpt-job-data-quality-scope-count) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery rpt_job_data_quality Distinct objects](#dax-mission-discovery-rpt-job-data-quality-distinct-objects) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery rpt_job_data_quality Discovery batches](#dax-mission-discovery-rpt-job-data-quality-discovery-batches) | `_MissionControl_Measures` | Quality & Exceptions | None asserted |
| [Discovery cfg_table_load_metric Context](#dax-mission-discovery-cfg-table-load-metric-context) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_table_load_metric Scope count](#dax-mission-discovery-cfg-table-load-metric-scope-count) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_table_load_metric Distinct objects](#dax-mission-discovery-cfg-table-load-metric-distinct-objects) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery cfg_table_load_metric Discovery batches](#dax-mission-discovery-cfg-table-load-metric-discovery-batches) | `_MissionControl_Measures` | Load Metrics & Control | None asserted |
| [Discovery rpt_job_layer_lineage Context](#dax-mission-discovery-rpt-job-layer-lineage-context) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_layer_lineage Scope count](#dax-mission-discovery-rpt-job-layer-lineage-scope-count) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_layer_lineage Distinct objects](#dax-mission-discovery-rpt-job-layer-lineage-distinct-objects) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Discovery rpt_job_layer_lineage Discovery batches](#dax-mission-discovery-rpt-job-layer-lineage-discovery-batches) | `_MissionControl_Measures` | Lineage & Step Summary | None asserted |
| [Latest Pipeline Row Visible](#dax-mission-latest-pipeline-row-visible) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest or selected Runs](#dax-mission-latest-or-selected-runs) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Latest or selected Success rate](#dax-mission-latest-or-selected-success-rate) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Latest or selected Failures](#dax-mission-latest-or-selected-failures) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Latest or selected P95 duration min](#dax-mission-latest-or-selected-p95-duration-min) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Latest or selected Rows written](#dax-mission-latest-or-selected-rows-written) | `_MissionControl_Measures` | Load Calendar | None asserted |
| [Discovery cfg_archived_schema_live Latest time](#dax-mission-discovery-cfg-archived-schema-live-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archived_schema_live Rows](#dax-mission-discovery-cfg-archived-schema-live-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archived_schema_live Visible](#dax-mission-discovery-cfg-archived-schema-live-visible) | `_MissionControl_Measures` | Quality & Schema | None asserted |
| [Discovery cfg_archived_schema_live Selected time](#dax-mission-discovery-cfg-archived-schema-live-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archived_schema_live State](#dax-mission-discovery-cfg-archived-schema-live-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archive_zip_load Latest time](#dax-mission-discovery-cfg-archive-zip-load-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archive_zip_load Latest key](#dax-mission-discovery-cfg-archive-zip-load-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archive_zip_load Rows](#dax-mission-discovery-cfg-archive-zip-load-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archive_zip_load Visible](#dax-mission-discovery-cfg-archive-zip-load-visible) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Discovery cfg_archive_zip_load Selected time](#dax-mission-discovery-cfg-archive-zip-load-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_archive_zip_load State](#dax-mission-discovery-cfg-archive-zip-load-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_month_end_gold_run Latest time](#dax-mission-discovery-cfg-month-end-gold-run-latest-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_month_end_gold_run Latest key](#dax-mission-discovery-cfg-month-end-gold-run-latest-key) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_month_end_gold_run Rows](#dax-mission-discovery-cfg-month-end-gold-run-rows) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_month_end_gold_run Visible](#dax-mission-discovery-cfg-month-end-gold-run-visible) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Discovery cfg_month_end_gold_run Selected time](#dax-mission-discovery-cfg-month-end-gold-run-selected-time) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Discovery cfg_month_end_gold_run State](#dax-mission-discovery-cfg-month-end-gold-run-state) | `_MissionControl_Measures` | No direct visible binding verified | None asserted |
| [Latest matching Archive ZIP Batches](#dax-mission-latest-matching-archive-zip-batches) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Latest matching Archive ZIP Batches Awaiting Reload](#dax-mission-latest-matching-archive-zip-batches-awaiting-reload) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Latest matching Failed Archive ZIP Batches](#dax-mission-latest-matching-failed-archive-zip-batches) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Latest matching Failed Gold Snapshots](#dax-mission-latest-matching-failed-gold-snapshots) | `_MissionControl_Measures` | Archive & Replay | None asserted |
| [Discovery calendar jobs](#dax-mission-discovery-calendar-jobs) | `_MissionControl_Measures` | Contracts & Schema; Domains & Reference; Lineage & Step Summary; Load Metrics & Control; Quality & Exceptions; Schema & Drift | None asserted |
| [Discovery calendar failures](#dax-mission-discovery-calendar-failures) | `_MissionControl_Measures` | Contracts & Schema; Domains & Reference; Lineage & Step Summary; Load Metrics & Control; Quality & Exceptions; Schema & Drift | None asserted |
| [Discovery calendar other](#dax-mission-discovery-calendar-other) | `_MissionControl_Measures` | Contracts & Schema; Domains & Reference; Lineage & Step Summary; Load Metrics & Control; Quality & Exceptions; Schema & Drift | None asserted |
| [Discovery job picker visible](#dax-mission-discovery-job-picker-visible) | `_MissionControl_Measures` | Contracts & Schema; Domains & Reference; Lineage & Step Summary; Load Metrics & Control; Quality & Exceptions; Schema & Drift | None asserted |
| [Job baseline n](#dax-mission-job-baseline-n) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Job prior mean min](#dax-mission-job-prior-mean-min) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Job prior median min](#dax-mission-job-prior-median-min) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | R82 (proposed) |
| [Job prior p25 min](#dax-mission-job-prior-p25-min) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Job prior p75 min](#dax-mission-job-prior-p75-min) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Job actual min](#dax-mission-job-actual-min) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Job comparison](#dax-mission-job-comparison) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |
| [Step baseline n](#dax-mission-step-baseline-n) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step prior mean min](#dax-mission-step-prior-mean-min) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step prior median min](#dax-mission-step-prior-median-min) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step prior p25 min](#dax-mission-step-prior-p25-min) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step prior p75 min](#dax-mission-step-prior-p75-min) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step actual min](#dax-mission-step-actual-min) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Step comparison](#dax-mission-step-comparison) | `_Run Benchmarks` | Job & Step Timelines | None asserted |
| [Single calendar day](#dax-mission-single-calendar-day) | `_Run Benchmarks` | Job & Step Timelines; Load Calendar | None asserted |

## Exact saved DAX — business

<a id="dax-business-accepted-offer-to-ipa-conversion-percent"></a>
### Accepted Offer to IPA Conversion %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 447. Measure container: `_Measures`.

```dax
[Accepted Offer to IPA Conversion %] =
DIVIDE ( [IPAs Created], [Accepted Offers] )
```

<a id="dax-business-accepted-offers"></a>
### Accepted Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 967. Measure container: `_Measures`.

```dax
[Accepted Offers] =
CALCULATE (
			    [Offers Submitted],
			    FILTER (
			        'fact_offer',
			        LOWER ( 'fact_offer'[offer_status] ) IN { "accepted", "approved", "selected", "offer_successful" }
			    )
			)
```

<a id="dax-business-accepted-offers-with-ipa"></a>
### Accepted Offers With IPA

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1193. Measure container: `_Measures`.

```dax
[Accepted Offers With IPA] =
VAR linked_offers = VALUES ( 'fact_ipa'[accepted_offer_id] )
			RETURN CALCULATE ( [Accepted Offers], KEEPFILTERS ( TREATAS ( linked_offers, 'fact_offer'[offer_id] ) ) )
```

<a id="dax-business-active-awaiting-offers-with-engagement"></a>
### Active Awaiting Offers With Engagement

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 343. Measure container: `_Measures`.

```dax
[Active Awaiting Offers With Engagement] =
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[is_awaiting_offer] = TRUE (),
				'fact_referral'[has_provider_response] = TRUE ()
			)
```

<a id="dax-business-active-awaiting-offers-without-engagement"></a>
### Active Awaiting Offers Without Engagement

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 354. Measure container: `_Measures`.

```dax
[Active Awaiting Offers Without Engagement] =
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[is_awaiting_offer] = TRUE (),
				'fact_referral'[has_provider_response] = FALSE ()
			)
```

<a id="dax-business-active-ipas"></a>
### Active IPAs

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 983. Measure container: `_Measures`.

```dax
[Active IPAs] =
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = FALSE () )
```

<a id="dax-business-active-referral-engagement-rate"></a>
### Active Referral Engagement Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 338. Measure container: `_Measures`.

```dax
[Active Referral Engagement Rate] =
DIVIDE ( [Active Referrals With Provider Engagement], [Referrals Currently Active] )
```

<a id="dax-business-active-referrals-with-provider-engagement"></a>
### Active Referrals With Provider Engagement

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 328. Measure container: `_Measures`.

```dax
[Active Referrals With Provider Engagement] =
CALCULATE (
				[Total Referrals],
				'fact_referral'[is_open] = TRUE (),
				'fact_referral'[has_provider_response] = TRUE ()
			)
```

<a id="dax-business-average-active-ipa-weekly-cost"></a>
### Average Active IPA Weekly Cost

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1183. Measure container: `_Measures`.

```dax
[Average Active IPA Weekly Cost] =
DIVIDE ( [Estimated Active Weekly Cost], [Active IPAs] )
```

<a id="dax-business-average-days-in-draft"></a>
### Average Days in Draft

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 163. Measure container: `_Measures`.

```dax
[Average Days in Draft] =
AVERAGEX (
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
				),
				'fact_offer'[offer_age_days]
			)
```

<a id="dax-business-average-estimated-weekly-cost-confirmed-referrals"></a>
### Average Estimated Weekly Cost — Confirmed Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 987. Measure container: `_Measures`.

```dax
[Average Estimated Weekly Cost — Confirmed Referrals] =
AVERAGEX (
			    FILTER (
			        'fact_referral',
			        NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
			            && NOT ISBLANK ( 'fact_referral'[estimated_weekly_cost] )
			    ),
			    'fact_referral'[estimated_weekly_cost]
			)
```

<a id="dax-business-average-lifecycle-events-per-referral"></a>
### Average Lifecycle Events per Referral

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1522. Measure container: `_Measures`.

```dax
[Average Lifecycle Events per Referral] =
DIVIDE ( [Referral Lifecycle Events], [Referrals With Lifecycle Activity] )
```

<a id="dax-business-average-offers-per-provider"></a>
### Average Offers per Provider

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1106. Measure container: `_Measures`.

```dax
[Average Offers per Provider] =
DIVIDE ( [Non-Draft Offers], [Providers Who Made Offers] )
```

<a id="dax-business-average-offers-per-referral"></a>
### Average Offers per Referral

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 978. Measure container: `_Measures`.

```dax
[Average Offers per Referral] =
DIVIDE ( [Offers Submitted], [Referrals With an Offer] )
```

<a id="dax-business-average-offers-per-referral-under-offer"></a>
### Average Offers per Referral Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1091. Measure container: `_Measures`.

```dax
[Average Offers per Referral Under Offer] =
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

<a id="dax-business-avg-offers-per-provider-under-offer"></a>
### Avg Offers per Provider (Under Offer)

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 23. Measure container: `_Measures`.

```dax
[Avg Offers per Provider (Under Offer)] =
DIVIDE(
			    [Offers on Referrals Under Offer],
			    [No. Providers Who Made Offers],
			    0
			)
```

<a id="dax-business-closed-ipas"></a>
### Closed IPAs

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1179. Measure container: `_Measures`.

```dax
[Closed IPAs] =
CALCULATE ( [IPAs Created], 'fact_ipa'[is_placement_closed] = TRUE () )
```

<a id="dax-business-closed-referrals"></a>
### Closed Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 896. Measure container: `_Measures`.

```dax
[Closed Referrals] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = FALSE () )
```

<a id="dax-business-closed-referrals-at-snapshot"></a>
### Closed Referrals at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 797. Measure container: `_Measures`.

```dax
[Closed Referrals at Snapshot] =
CALCULATE (
			    [Snapshot Referrals],
			    FILTER (
			        'fact_referral_snapshot',
			        NOT ISBLANK ( 'fact_referral_snapshot'[referral_closed_date] )
			            && 'fact_referral_snapshot'[referral_closed_date] < 'fact_referral_snapshot'[snapshot_date] + 1
			    )
			)
```

<a id="dax-business-closed-or-cancelled-referrals"></a>
### Closed or Cancelled Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 108. Measure container: `_Measures`.

```dax
[Closed or Cancelled Referrals] =
CALCULATE (
			    [Total Referrals],
			    FILTER (
			        'fact_referral',
			        LOWER ( COALESCE ( 'fact_referral'[current_status], "" ) )
			            IN { "closed", "cancelled", "withdrawn", "completed" }
			    )
			)
```

<a id="dax-business-critical-overdue-referrals"></a>
### Critical Overdue Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Design Measures.tmdl`, line 31. Measure container: `_Design Measures`.

```dax
[Critical Overdue Referrals] =
CALCULATE ( [Open Overdue Referrals],
			    KEEPFILTERS ( 'fact_referral'[placement_urgency_band] = "Critical" ) )
```

<a id="dax-business-directory-summary-count"></a>
### Directory Summary Count

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 246. Measure container: `_Measures`.

```dax
[Directory Summary Count] =
SWITCH ( SELECTEDVALUE ( 'Directory Summary Axis'[Display Type] ),
			    "Fostering Providers", [Providers - Fostering],
			    "Residential Homes", [Residential Homes],
			    "Supported Accommodation Homes", [Supported Accommodation Homes],
			    BLANK ()
			)
```

<a id="dax-business-documents-expired"></a>
### Documents Expired

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1490. Measure container: `_Measures`.

```dax
[Documents Expired] =
CALCULATE (
			    [Provider Submission Documents],
			    FILTER (
			        'dim_provider_submission_document',
			        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
			            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
			    )
			)
```

<a id="dax-business-documents-expiring-next-30-days"></a>
### Documents Expiring Next 30 Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1477. Measure container: `_Measures`.

```dax
[Documents Expiring Next 30 Days] =
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

<a id="dax-business-draft-offers-missing-dates"></a>
### Draft Offers Missing Dates

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 144. Measure container: `_Measures`.

```dax
[Draft Offers Missing Dates] =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_missing_dates] = TRUE () )
```

<a id="dax-business-draft-offers-stalled-14-days"></a>
### Draft Offers Stalled 14+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1448. Measure container: `_Measures`.

```dax
[Draft Offers Stalled 14+ Days] =
CALCULATE (
				[Offers Submitted],
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& 'fact_offer'[days_since_offer_activity] >= 14
				)
			)
```

<a id="dax-business-draft-offers-stalled-7-days"></a>
### Draft Offers Stalled 7+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1416. Measure container: `_Measures`.

```dax
[Draft Offers Stalled 7+ Days] =
CALCULATE (
				[Offers Submitted],
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& 'fact_offer'[days_since_offer_activity] >= 7
				)
			)
```

<a id="dax-business-draft-offers-with-activity-since-creation"></a>
### Draft Offers With Activity Since Creation

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 134. Measure container: `_Measures`.

```dax
[Draft Offers With Activity Since Creation] =
CALCULATE (
			    [Offers in Draft],
			    KEEPFILTERS ( 'fact_offer'[is_draft_no_activity] = FALSE () ),
			    KEEPFILTERS ( 'fact_offer'[is_draft_missing_dates] = FALSE () )
			)
```

<a id="dax-business-draft-offers-with-no-activity-percent"></a>
### Draft Offers With No Activity %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1460. Measure container: `_Measures`.

```dax
[Draft Offers With No Activity %] =
DIVIDE ( [Draft Offers With No Activity Since Creation], [Offers in Draft] )
```

<a id="dax-business-draft-offers-with-no-activity-since-creation"></a>
### Draft Offers With No Activity Since Creation

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1444. Measure container: `_Measures`.

```dax
[Draft Offers With No Activity Since Creation] =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_draft_no_activity] = TRUE () )
```

<a id="dax-business-draft-offers-on-referrals-under-offer"></a>
### Draft Offers on Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1328. Measure container: `_Measures`.

```dax
[Draft Offers on Referrals Under Offer] =
CALCULATE (
			    [Offers in Draft],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

<a id="dax-business-drafts-no-activity-14-days"></a>
### Drafts No Activity 14+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1632. Measure container: `_Measures`.

```dax
[Drafts No Activity 14+ Days] =
CALCULATE ( [Offers in Draft], KEEPFILTERS ( 'fact_offer'[offer_age_days] >= 14 ) )
```

<a id="dax-business-emergency-placement-rate"></a>
### Emergency Placement Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1046. Measure container: `_Measures`.

```dax
[Emergency Placement Rate] =
DIVIDE ( [Emergency Referrals], [Total Referrals] )
```

<a id="dax-business-emergency-referrals"></a>
### Emergency Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1034. Measure container: `_Measures`.

```dax
[Emergency Referrals] =
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ), KEEPFILTERS ( 'fact_referral'[is_emergency_placement] = TRUE () ) )
```

<a id="dax-business-estimated-active-weekly-cost"></a>
### Estimated Active Weekly Cost

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 862. Measure container: `_Measures`.

```dax
[Estimated Active Weekly Cost] =
CALCULATE (
			    SUM ( 'fact_ipa'[estimated_weekly_cost] ),
			    'fact_ipa'[is_placement_closed] = FALSE ()
			)
```

<a id="dax-business-explorer-referrals"></a>
### Explorer referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explorer KPI Measures.tmdl`, line 530. Measure container: `_Explorer KPI Measures`.

```dax
[Explorer referrals] =
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

<a id="dax-business-female-referrals"></a>
### Female Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 74. Measure container: `_Measures`.

```dax
[Female Referrals] =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Female" )
```

<a id="dax-business-fostering-homes"></a>
### Fostering Homes

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1126. Measure container: `_Measures`.

```dax
[Fostering Homes] =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Fostering" )
```

<a id="dax-business-framework-offers-under-offer-referrals"></a>
### Framework Offers (Under Offer Referrals)

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 375. Measure container: `_Measures`.

```dax
[Framework Offers (Under Offer Referrals)] =
// Preserve the original non-Spot fallback for blank/unmatched home flags.
			// These offers are not evidence of affirmative framework membership.
			VAR qualifyingOffers = [Offers on Referrals Under Offer]
			VAR spotOffers = COALESCE ( [Spot Offers on Referrals Under Offer], 0 )
			RETURN
			    IF ( ISBLANK ( qualifyingOffers ), BLANK (), qualifyingOffers - spotOffers )
```

<a id="dax-business-framework-providers"></a>
### Framework Providers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 225. Measure container: `_Measures`.

```dax
[Framework Providers] =
DISTINCTCOUNT(bridge_provider_framework[provider_id])
```

<a id="dax-business-gold-model-last-refreshed"></a>
### Gold Model Last Refreshed

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1215. Measure container: `_Measures`.

```dax
[Gold Model Last Refreshed] =
MAX ( 'fact_referral'[gold_modelled_at] )
```

<a id="dax-business-homes-offered"></a>
### Homes Offered

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Design Measures.tmdl`, line 82. Measure container: `_Design Measures`.

```dax
[Homes Offered] =
CALCULATE ( DISTINCTCOUNT ( 'fact_offer'[provider_home_id] ),
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[provider_home_id] ) && 'fact_offer'[provider_home_id] <> "" ) ) )
```

<a id="dax-business-ipa-completed"></a>
### IPA Completed

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 405. Measure container: `_Measures`.

```dax
[IPA Completed] =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )
```

<a id="dax-business-ipa-created-to-completion-percent"></a>
### IPA Created to Completion %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 453. Measure container: `_Measures`.

```dax
[IPA Created to Completion %] =
DIVIDE ( [IPA Completed], [IPAs Created] )
```

<a id="dax-business-ipa-exists"></a>
### IPA Exists

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 386. Measure container: `_Measures`.

```dax
[IPA Exists] =
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ) ) > 0, "Yes", "No" ),
			    IF ( [IPAs Created] > 0, "Yes", "No" )
			)
```

<a id="dax-business-ipa-signature-completion-rate"></a>
### IPA Signature Completion Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1208. Measure container: `_Measures`.

```dax
[IPA Signature Completion Rate] =
DIVIDE ( [IPA Completed], [IPAs Created] )
```

<a id="dax-business-ipas-created"></a>
### IPAs Created

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 873. Measure container: `_Measures`.

```dax
[IPAs Created] =
DISTINCTCOUNT ( 'fact_ipa'[ipa_id] )
```

<a id="dax-business-ipas-issued-this-month"></a>
### IPAs Issued This Month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1167. Measure container: `_Measures`.

```dax
[IPAs Issued This Month] =
VAR as_of = MAX ( 'fact_ipa'[as_of_date] )
			RETURN IF ( NOT ISBLANK ( as_of ),
			    CALCULATE ( [IPAs Created],
			        CROSSFILTER ( 'dim_date'[date], 'fact_referral'[referral_created_date], NONE ),
			        USERELATIONSHIP ( 'dim_date'[date], 'fact_ipa'[ipa_issued_date] ),
			        DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of )
			    )
			)
```

<a id="dax-business-ipas-pending-completion"></a>
### IPAs Pending Completion

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 410. Measure container: `_Measures`.

```dax
[IPAs Pending Completion] =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[is_ipa_pending] = TRUE () ) )
```

<a id="dax-business-ipas-signed-by-local-authority"></a>
### IPAs Signed by Local Authority

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1617. Measure container: `_Measures`.

```dax
[IPAs Signed by Local Authority] =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[signed_by_local_authority] = TRUE () ) )
```

<a id="dax-business-ipas-signed-by-provider"></a>
### IPAs Signed by Provider

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1612. Measure container: `_Measures`.

```dax
[IPAs Signed by Provider] =
CALCULATE ( [IPAs Created], KEEPFILTERS ( 'fact_ipa'[signed_by_provider] = TRUE () ) )
```

<a id="dax-business-is-awaiting-ipa-creation"></a>
### Is Awaiting IPA Creation

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 431. Measure container: `_Measures`.

```dax
[Is Awaiting IPA Creation] =
IF ( COALESCE ( SELECTEDVALUE ( 'fact_offer'[is_awaiting_ipa_creation] ), FALSE () ), 1, 0 )
```

<a id="dax-business-is-ipa-completed"></a>
### Is IPA Completed

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 436. Measure container: `_Measures`.

```dax
[Is IPA Completed] =
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_completed] = TRUE () ) > 0, 1, 0 ),
			    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_completed], FALSE () ), 1, 0 )
			)
```

<a id="dax-business-is-ipa-pending"></a>
### Is IPA Pending

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 420. Measure container: `_Measures`.

```dax
[Is IPA Pending] =
IF (
			    ISINSCOPE ( 'fact_offer'[offer_id] ) || ( HASONEVALUE ( 'fact_offer'[offer_id] ) && NOT ISINSCOPE ( 'fact_ipa'[ipa_id] ) ),
			    VAR offer_ids = VALUES ( 'fact_offer'[offer_id] )
			    RETURN IF ( CALCULATE ( [IPAs Created], KEEPFILTERS ( TREATAS ( offer_ids, 'fact_ipa'[accepted_offer_id] ) ), 'fact_ipa'[is_ipa_pending] = TRUE () ) > 0, 1, 0 ),
			    IF ( SELECTEDVALUE ( 'fact_ipa'[is_ipa_pending], FALSE () ), 1, 0 )
			)
```

<a id="dax-business-is-in-accepted-kpi"></a>
### Is In Accepted KPI

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 396. Measure container: `_Measures`.

```dax
[Is In Accepted KPI] =
IF (
			    LOWER ( COALESCE ( SELECTEDVALUE ( 'fact_offer'[offer_status] ), "" ) ) IN { "accepted", "approved", "selected", "offer_successful" },
			    "Yes",
			    "No"
			)
```

<a id="dax-business-is-non-framework-provider"></a>
### Is Non Framework Provider

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 241. Measure container: `_Measures`.

```dax
[Is Non Framework Provider] =
IF ( CALCULATE ( COUNTROWS ( 'bridge_provider_framework' ) ) = 0, 1, 0 )
```

<a id="dax-business-journey-provider-stage"></a>
### Journey provider stage

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 199. Measure container: `_Journey Measures`.

```dax
[Journey provider stage] =
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

<a id="dax-business-journey-providers-0"></a>
### Journey providers 0

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 216. Measure container: `_Journey Measures`.

```dax
[Journey providers 0] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 0)), 0)
```

<a id="dax-business-journey-providers-1"></a>
### Journey providers 1

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 221. Measure container: `_Journey Measures`.

```dax
[Journey providers 1] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 1)), 0)
```

<a id="dax-business-journey-providers-2"></a>
### Journey providers 2

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 226. Measure container: `_Journey Measures`.

```dax
[Journey providers 2] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 2)), 0)
```

<a id="dax-business-journey-providers-3"></a>
### Journey providers 3

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 231. Measure container: `_Journey Measures`.

```dax
[Journey providers 3] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 3)), 0)
```

<a id="dax-business-journey-providers-5"></a>
### Journey providers 5

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 236. Measure container: `_Journey Measures`.

```dax
[Journey providers 5] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && CALCULATE([Journey provider stage]) == 5)), 0)
```

<a id="dax-business-journey-providers-both-signed"></a>
### Journey providers both signed

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 249. Measure container: `_Journey Measures`.

```dax
[Journey providers both signed] =
COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]),
			VAR offerIDs = CALCULATETABLE(VALUES('fact_offer'[offer_id]))
			VAR signedIPAs = CALCULATETABLE('fact_ipa', KEEPFILTERS(TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])))
			RETURN NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Provider matches offer status]) = 1 && COUNTROWS(FILTER(signedIPAs, 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0)),0)
```

<a id="dax-business-journey-referrals-1"></a>
### Journey referrals 1

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 4. Measure container: `_Journey Measures`.

```dax
[Journey referrals 1] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 1)), 0)
```

<a id="dax-business-journey-referrals-2"></a>
### Journey referrals 2

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 9. Measure container: `_Journey Measures`.

```dax
[Journey referrals 2] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 2)), 0)
```

<a id="dax-business-journey-referrals-3"></a>
### Journey referrals 3

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 14. Measure container: `_Journey Measures`.

```dax
[Journey referrals 3] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 3)), 0)
```

<a id="dax-business-journey-referrals-4"></a>
### Journey referrals 4

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 19. Measure container: `_Journey Measures`.

```dax
[Journey referrals 4] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 4)), 0)
```

<a id="dax-business-journey-referrals-5"></a>
### Journey referrals 5

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 24. Measure container: `_Journey Measures`.

```dax
[Journey referrals 5] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 5)), 0)
```

<a id="dax-business-journey-referrals-6"></a>
### Journey referrals 6

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 29. Measure container: `_Journey Measures`.

```dax
[Journey referrals 6] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 6)), 0)
```

<a id="dax-business-journey-referrals-7"></a>
### Journey referrals 7

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 34. Measure container: `_Journey Measures`.

```dax
[Journey referrals 7] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 7)), 0)
```

<a id="dax-business-journey-referrals-8"></a>
### Journey referrals 8

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Journey Measures.tmdl`, line 39. Measure container: `_Journey Measures`.

```dax
[Journey referrals 8] =
COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = 8)), 0)
```

<a id="dax-business-latest-offer-source-export"></a>
### Latest Offer Source Export

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1590. Measure container: `_Measures`.

```dax
[Latest Offer Source Export] =
MAX ( 'fact_offer'[source_export_date] )
```

<a id="dax-business-male-referrals"></a>
### Male Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 69. Measure container: `_Measures`.

```dax
[Male Referrals] =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Male" )
```

<a id="dax-business-matching-referrals"></a>
### Matching referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl`, line 4. Measure container: `_Story Measures`.

```dax
[Matching referrals] =
[Explorer referrals]
```

<a id="dax-business-median-days-to-first-action"></a>
### Median Days to First Action

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 928. Measure container: `_Measures`.

```dax
[Median Days to First Action] =
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_action] ) ),
			    'fact_referral'[days_to_first_action]
			)
```

<a id="dax-business-median-days-to-first-offer"></a>
### Median Days to First Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 937. Measure container: `_Measures`.

```dax
[Median Days to First Offer] =
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_first_offer] ) ),
			    'fact_referral'[days_to_first_offer]
			)
```

<a id="dax-business-median-days-to-ipa"></a>
### Median Days to IPA

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 946. Measure container: `_Measures`.

```dax
[Median Days to IPA] =
MEDIANX (
			    FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[days_to_ipa] ) ),
			    'fact_referral'[days_to_ipa]
			)
```

<a id="dax-business-median-preferred-city-distance-km"></a>
### Median preferred-city distance km

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explore Measures.tmdl`, line 62. Measure container: `_Explore Measures`.

```dax
[Median preferred-city distance km] =
MEDIANX(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]="APPROXIMATE_PREFERENCE_CITY" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km])),'fact_offer'[referral_to_home_distance_km])
```

<a id="dax-business-no-providers-who-made-offers"></a>
### No. Providers Who Made Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 14. Measure container: `_Measures`.

```dax
[No. Providers Who Made Offers] =
CALCULATE (
			    [Providers Who Made Offers],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

<a id="dax-business-non-draft-offers"></a>
### Non-Draft Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1051. Measure container: `_Measures`.

```dax
[Non-Draft Offers] =
CALCULATE (
			    [Offers Submitted],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_status] ) && LOWER ( 'fact_offer'[offer_status] ) <> "draft" ) )
			)
```

<a id="dax-business-non-framework-providers"></a>
### Non-Framework Providers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 230. Measure container: `_Measures`.

```dax
[Non-Framework Providers] =
COUNTROWS (
			    EXCEPT (
			        VALUES ( 'dim_provider'[provider_id] ),
			        VALUES ( 'bridge_provider_framework'[provider_id] )
			    )
			)
```

<a id="dax-business-non-spot-offers"></a>
### Non-Spot Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1122. Measure container: `_Measures`.

```dax
[Non-Spot Offers] =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home (offer)'[is_spot] = FALSE () )
```

<a id="dax-business-offer-acceptance-rate"></a>
### Offer Acceptance Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1411. Measure container: `_Measures`.

```dax
[Offer Acceptance Rate] =
DIVIDE ( [Accepted Offers], [Offers with a Decision] )
```

<a id="dax-business-offers-awaiting-ipa-creation"></a>
### Offers Awaiting IPA Creation

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 415. Measure container: `_Measures`.

```dax
[Offers Awaiting IPA Creation] =
CALCULATE ( [Offers Submitted], 'fact_offer'[is_awaiting_ipa_creation] = TRUE ())
```

<a id="dax-business-offers-still-to-progress-to-ipa-percent"></a>
### Offers Still to Progress to IPA %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1199. Measure container: `_Measures`.

```dax
[Offers Still to Progress to IPA %] =
IF ( NOT ISBLANK ( [Accepted Offer to IPA Conversion %] ), 1 - [Accepted Offer to IPA Conversion %] )
```

<a id="dax-business-offers-submitted"></a>
### Offers Submitted

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 963. Measure container: `_Measures`.

```dax
[Offers Submitted] =
DISTINCTCOUNT ( 'fact_offer'[offer_id] )
```

<a id="dax-business-offers-with-recorded-rejection-reason"></a>
### Offers With Recorded Rejection Reason

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1431. Measure container: `_Measures`.

```dax
[Offers With Recorded Rejection Reason] =
CALCULATE (
			    [Offers Submitted],
			    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[rejection_reason] ) )
			)
```

<a id="dax-business-offers-in-draft"></a>
### Offers in Draft

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 55. Measure container: `_Measures`.

```dax
[Offers in Draft] =
CALCULATE ( [Offers Submitted], LOWER ( 'fact_offer'[offer_status] ) = "draft" )
```

<a id="dax-business-offers-on-referrals-under-offer"></a>
### Offers on Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1111. Measure container: `_Measures`.

```dax
[Offers on Referrals Under Offer] =
CALCULATE (
			    [Non-Draft Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

<a id="dax-business-offers-per-provider-under-offer-referrals"></a>
### Offers per Provider (Under Offer Referrals)

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 365. Measure container: `_Measures`.

```dax
[Offers per Provider (Under Offer Referrals)] =
DIVIDE ( [Offers on Referrals Under Offer], [No. Providers Who Made Offers], 0 )
```

<a id="dax-business-offers-with-a-decision"></a>
### Offers with a Decision

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1404. Measure container: `_Measures`.

```dax
[Offers with a Decision] =
CALCULATE (
			    [Offers Submitted],
			    FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_decision_date] ) )
			)
```

<a id="dax-business-offers-with-preferred-city-distance"></a>
### Offers with preferred-city distance

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explore Measures.tmdl`, line 67. Measure container: `_Explore Measures`.

```dax
[Offers with preferred-city distance] =
CALCULATE([Offers Submitted],KEEPFILTERS(FILTER('fact_offer','fact_offer'[referral_to_home_distance_status]="APPROXIMATE_PREFERENCE_CITY" && NOT ISBLANK('fact_offer'[referral_to_home_distance_km]))))
```

<a id="dax-business-oldest-draft-age-days"></a>
### Oldest Draft Age Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 177. Measure container: `_Measures`.

```dax
[Oldest Draft Age Days] =
MAXX (
				FILTER (
					'fact_offer',
					LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) = "draft"
						&& NOT ISBLANK ( 'fact_offer'[offer_age_days] )
				),
				'fact_offer'[offer_age_days]
			)
```

<a id="dax-business-open-on-track-referrals-at-snapshot"></a>
### Open On-Track Referrals at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 810. Measure container: `_Measures`.

```dax
[Open On-Track Referrals at Snapshot] =
CALCULATE (
			    [Snapshot Referrals],
			    'fact_referral_snapshot'[required_placement_date_outcome] = "Open on track"
			)
```

<a id="dax-business-open-overdue-referrals"></a>
### Open Overdue Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 828. Measure container: `_Measures`.

```dax
[Open Overdue Referrals] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open_overdue] = TRUE () )
```

<a id="dax-business-open-overdue-referrals-at-snapshot"></a>
### Open Overdue Referrals at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1000. Measure container: `_Measures`.

```dax
[Open Overdue Referrals at Snapshot] =
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open_overdue] = TRUE () )
```

<a id="dax-business-open-referral-rate-at-snapshot"></a>
### Open Referral Rate at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 833. Measure container: `_Measures`.

```dax
[Open Referral Rate at Snapshot] =
DIVIDE ( [Open Referrals at Snapshot], [Snapshot Referrals] )
```

<a id="dax-business-open-referrals"></a>
### Open Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 878. Measure container: `_Measures`.

```dax
[Open Referrals] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )
```

<a id="dax-business-open-referrals-stalled-7-days"></a>
### Open Referrals Stalled 7+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 955. Measure container: `_Measures`.

```dax
[Open Referrals Stalled 7+ Days] =
CALCULATE (
			    [Total Referrals],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[days_without_activity] >= 7 )
			)
```

<a id="dax-business-open-referrals-at-snapshot"></a>
### Open Referrals at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 705. Measure container: `_Measures`.

```dax
[Open Referrals at Snapshot] =
CALCULATE ( [Snapshot Referrals], 'fact_referral_snapshot'[is_open] = TRUE () )
```

<a id="dax-business-other-gender-referrals"></a>
### Other Gender Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 79. Measure container: `_Measures`.

```dax
[Other Gender Referrals] =
CALCULATE ( [Total Referrals], 'dim_person'[gender_clean] = "Other" )
```

<a id="dax-business-pending-offers"></a>
### Pending Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1059. Measure container: `_Measures`.

```dax
[Pending Offers] =
CALCULATE (
			    [Offers Submitted],
			    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } ) )
			)
```

<a id="dax-business-pending-offers-under-offer-referrals"></a>
### Pending Offers (Under Offer Referrals)

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 60. Measure container: `_Measures`.

```dax
[Pending Offers (Under Offer Referrals)] =
CALCULATE (
			    [Pending Offers],
			    FILTER ( 'fact_referral', 'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER" )
			)
```

<a id="dax-business-pending-offers-0-7-days"></a>
### Pending Offers 0-7 Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 289. Measure container: `_Measures`.

```dax
[Pending Offers 0-7 Days] =
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 0 && 'fact_offer'[offer_age_days] <= 7 ) )
			)
```

<a id="dax-business-pending-offers-15-29-days"></a>
### Pending Offers 15-29 Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 271. Measure container: `_Measures`.

```dax
[Pending Offers 15-29 Days] =
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 15 && 'fact_offer'[offer_age_days] <= 29 ) )
			)
```

<a id="dax-business-pending-offers-15-30-days"></a>
### Pending Offers 15–30 Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1627. Measure container: `_Measures`.

```dax
[Pending Offers 15–30 Days] =
CALCULATE ( [Pending Offers], KEEPFILTERS ( FILTER ( 'fact_offer', 'fact_offer'[offer_age_days] >= 15 && 'fact_offer'[offer_age_days] <= 30 ) ) )
```

<a id="dax-business-pending-offers-30-days"></a>
### Pending Offers 30+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 280. Measure container: `_Measures`.

```dax
[Pending Offers 30+ Days] =
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 30 ) )
			)
```

<a id="dax-business-pending-offers-8-14-days"></a>
### Pending Offers 8-14 Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 298. Measure container: `_Measures`.

```dax
[Pending Offers 8-14 Days] =
CALCULATE (
			    [Pending Offers],
			    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[offer_age_days] ) && 'fact_offer'[offer_age_days] >= 8 && 'fact_offer'[offer_age_days] <= 14 ) )
			)
```

<a id="dax-business-placement-rate-at-snapshot"></a>
### Placement Rate at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 839. Measure container: `_Measures`.

```dax
[Placement Rate at Snapshot] =
DIVIDE ( [Referrals with IPA at Snapshot], [Snapshot Referrals] )
```

<a id="dax-business-placement-target-hit-rate"></a>
### Placement Target Hit Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 912. Measure container: `_Measures`.

```dax
[Placement Target Hit Rate] =
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

<a id="dax-business-planned-referrals"></a>
### Planned Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1038. Measure container: `_Measures`.

```dax
[Planned Referrals] =
CALCULATE (
			    [Total Referrals], KEEPFILTERS ( 'fact_referral'[current_status] IN { "OPEN", "UNDER_OFFER" } ),
			    KEEPFILTERS ( FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[referral_created_date] ) && NOT ISBLANK ( 'fact_referral'[required_placement_date] ) && 'fact_referral'[is_emergency_placement] = FALSE () ) )
			)
```

<a id="dax-business-preferred-city-distance-coverage"></a>
### Preferred-city distance coverage

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explore Measures.tmdl`, line 77. Measure container: `_Explore Measures`.

```dax
[Preferred-city distance coverage] =
DIVIDE([Offers with preferred-city distance],[Offers Submitted])
```

<a id="dax-business-provider-assignments"></a>
### Provider Assignments

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1594. Measure container: `_Measures`.

```dax
[Provider Assignments] =
DISTINCTCOUNT ( 'fact_referral_provider'[referral_provider_id] )
```

<a id="dax-business-provider-average-response-hours"></a>
### Provider Average Response Hours

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1680. Measure container: `_Measures`.

```dax
[Provider Average Response Hours] =
DIVIDE (
				SUMX (
					'fact_provider_kpi_monthly',
					'fact_provider_kpi_monthly'[average_response_minutes]
						* 'fact_provider_kpi_monthly'[qualifying_response_count]
				),
				[Provider Qualifying Responses] * 60
			)
```

<a id="dax-business-provider-decline-rate"></a>
### Provider Decline Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1602. Measure container: `_Measures`.

```dax
[Provider Decline Rate] =
DIVIDE ( [Provider Declines], [Provider Assignments] )
```

<a id="dax-business-provider-declines"></a>
### Provider Declines

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1598. Measure container: `_Measures`.

```dax
[Provider Declines] =
CALCULATE ( [Provider Assignments], 'fact_referral_provider'[is_declined] = TRUE () )
```

<a id="dax-business-provider-homes-registered"></a>
### Provider Homes Registered

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 89. Measure container: `_Measures`.

```dax
[Provider Homes Registered] =
IF ( ISFILTERED ( 'dim_provider' ),
			    CALCULATE ( DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] ), KEEPFILTERS ( TREATAS ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider_home'[provider_id] ) ) ),
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_home_id] )
			)
```

<a id="dax-business-provider-homes-with-expired-documents"></a>
### Provider Homes With Expired Documents

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1502. Measure container: `_Measures`.

```dax
[Provider Homes With Expired Documents] =
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_submission_document'[home_id] ),
			    FILTER (
			        'dim_provider_submission_document',
			        NOT ISBLANK ( 'dim_provider_submission_document'[expiry_date] )
			            && 'dim_provider_submission_document'[expiry_date] < TODAY ()
			    )
			)
```

<a id="dax-business-provider-messages-sent"></a>
### Provider Messages Sent

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1527. Measure container: `_Measures`.

```dax
[Provider Messages Sent] =
CALCULATE (
			    [Referral Lifecycle Events],
			    'fact_referral_lifecycle_event'[event_type] = "ProviderMessageSent"
			)
```

<a id="dax-business-provider-offer-conversion-rate"></a>
### Provider Offer Conversion Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1662. Measure container: `_Measures`.

```dax
[Provider Offer Conversion Rate] =
DIVIDE (
				SUM ( 'fact_provider_kpi_monthly'[accepted_offer_count] ),
				SUM ( 'fact_provider_kpi_monthly'[offers_submitted_count] )
			)
```

<a id="dax-business-provider-onboarding-success-rate"></a>
### Provider Onboarding Success Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1162. Measure container: `_Measures`.

```dax
[Provider Onboarding Success Rate] =
DIVIDE ( [Providers Approved], [Providers Registered] )
```

<a id="dax-business-provider-qualifying-responses"></a>
### Provider Qualifying Responses

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1652. Measure container: `_Measures`.

```dax
[Provider Qualifying Responses] =
SUM ( 'fact_provider_kpi_monthly'[qualifying_response_count] )
```

<a id="dax-business-provider-response-opportunities"></a>
### Provider Response Opportunities

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1647. Measure container: `_Measures`.

```dax
[Provider Response Opportunities] =
SUM ( 'fact_provider_kpi_monthly'[response_opportunity_count] )
```

<a id="dax-business-provider-response-rate"></a>
### Provider Response Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1657. Measure container: `_Measures`.

```dax
[Provider Response Rate] =
DIVIDE ( [Provider Qualifying Responses], [Provider Response Opportunities] )
```

<a id="dax-business-provider-submission-documents"></a>
### Provider Submission Documents

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1473. Measure container: `_Measures`.

```dax
[Provider Submission Documents] =
DISTINCTCOUNT ( 'dim_provider_submission_document'[document_id] )
```

<a id="dax-business-provider-target-placement-rate"></a>
### Provider Target Placement Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1671. Measure container: `_Measures`.

```dax
[Provider Target Placement Rate] =
DIVIDE (
				SUM ( 'fact_provider_kpi_monthly'[placed_by_target_count] ),
				SUM ( 'fact_provider_kpi_monthly'[successful_referral_count] )
			)
```

<a id="dax-business-provider-matches-offer-status"></a>
### Provider matches offer status

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Explorer KPI Measures.tmdl`, line 853. Measure container: `_Explorer KPI Measures`.

```dax
[Provider matches offer status] =
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

<a id="dax-business-providers-fostering"></a>
### Providers - Fostering

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 199. Measure container: `_Measures`.

```dax
[Providers - Fostering] =
VAR framework_providers = CALCULATETABLE ( VALUES ( 'bridge_provider_framework'[provider_id] ), FILTER ( 'dim_framework', LOWER ( 'dim_framework'[placement_type] ) IN { "fostering", "plcm-fost" } ) )
			VAR home_providers = CALCULATETABLE ( VALUES ( 'dim_provider_home'[provider_id] ), FILTER ( 'dim_provider_home', LOWER ( 'dim_provider_home'[service_type] ) IN { "fostering", "plcm-fost" } ) )
			RETURN CALCULATE ( [Providers Registered], KEEPFILTERS ( TREATAS ( DISTINCT ( UNION ( framework_providers, home_providers ) ), 'dim_provider'[provider_id] ) ) )
```

<a id="dax-business-providers-residential"></a>
### Providers - Residential

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 207. Measure container: `_Measures`.

```dax
[Providers - Residential] =
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
			    'dim_provider_home'[service_type] = "Residential"
			)
```

<a id="dax-business-providers-supported-accommodation"></a>
### Providers - Supported Accommodation

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 216. Measure container: `_Measures`.

```dax
[Providers - Supported Accommodation] =
CALCULATE (
			    DISTINCTCOUNT ( 'dim_provider_home'[provider_id] ),
			    'dim_provider_home'[service_type] = "Supported Accommodation"
			)
```

<a id="dax-business-providers-approved"></a>
### Providers Approved

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1154. Measure container: `_Measures`.

```dax
[Providers Approved] =
CALCULATE (
			    [Providers Registered],
			    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "approved" )
			)
```

<a id="dax-business-providers-pending-onboarding"></a>
### Providers Pending Onboarding

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1146. Measure container: `_Measures`.

```dax
[Providers Pending Onboarding] =
CALCULATE (
			    [Providers Registered],
			    FILTER ( 'dim_provider', LOWER ( COALESCE ( 'dim_provider'[provider_status], "" ) ) = "pending" )
			)
```

<a id="dax-business-providers-registered"></a>
### Providers Registered

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 98. Measure container: `_Measures`.

```dax
[Providers Registered] =
DISTINCTCOUNT(dim_provider[provider_id])
```

<a id="dax-business-providers-who-made-offers"></a>
### Providers Who Made Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1078. Measure container: `_Measures`.

```dax
[Providers Who Made Offers] =
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

<a id="dax-business-providers-with-pending-offers-30-days"></a>
### Providers With Pending Offers 30+ Days

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1465. Measure container: `_Measures`.

```dax
[Providers With Pending Offers 30+ Days] =
CALCULATE (
			    DISTINCTCOUNT ( 'fact_offer'[provider_id] ),
			    KEEPFILTERS ( FILTER ( 'fact_offer', LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) ) IN { "pending", "offer_made" } && 'fact_offer'[offer_age_days] >= 30 ) )
			)
```

<a id="dax-business-providers-with-qa-flags"></a>
### Providers With QA Flags

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1130. Measure container: `_Measures`.

```dax
[Providers With QA Flags] =
CALCULATE ( [Providers Registered], KEEPFILTERS ( 'dim_provider'[qa_flag] = TRUE () ) )
```

<a id="dax-business-qa-flagged-homes"></a>
### QA Flagged Homes

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1134. Measure container: `_Measures`.

```dax
[QA Flagged Homes] =
VAR flagged_providers = CALCULATETABLE ( VALUES ( 'dim_provider'[provider_id] ), 'dim_provider'[qa_flag] = TRUE () )
			VAR selected_providers = VALUES ( 'dim_provider'[provider_id] )
			RETURN
			    CALCULATE (
			        [Provider Homes Registered],
			        KEEPFILTERS ( TREATAS ( selected_providers, 'dim_provider_home'[provider_id] ) ),
			        KEEPFILTERS ( FILTER ( 'dim_provider_home', 'dim_provider_home'[qa_flag] = TRUE () || 'dim_provider_home'[provider_id] IN flagged_providers ) )
			    )
```

<a id="dax-business-referral-lifecycle-events"></a>
### Referral Lifecycle Events

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1514. Measure container: `_Measures`.

```dax
[Referral Lifecycle Events] =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[event_id] )
```

<a id="dax-business-referral-volume-month-on-month"></a>
### Referral Volume Month on Month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1014. Measure container: `_Measures`.

```dax
[Referral Volume Month on Month] =
[Total Referrals] - [Referrals Created Previous Month]
```

<a id="dax-business-referral-volume-month-on-month-percent"></a>
### Referral Volume Month on Month %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1018. Measure container: `_Measures`.

```dax
[Referral Volume Month on Month %] =
DIVIDE ( [Referral Volume Month on Month], [Referrals Created Previous Month] )
```

<a id="dax-business-referrals-awaiting-offer"></a>
### Referrals Awaiting Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 9. Measure container: `_Measures`.

```dax
[Referrals Awaiting Offer] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_awaiting_offer] = TRUE () )
```

<a id="dax-business-referrals-created-previous-month"></a>
### Referrals Created Previous Month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1010. Measure container: `_Measures`.

```dax
[Referrals Created Previous Month] =
CALCULATE ( [Total Referrals], DATEADD ( 'dim_date'[date], -1, MONTH ) )
```

<a id="dax-business-referrals-created-this-financial-year"></a>
### Referrals Created This Financial Year

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1023. Measure container: `_Measures`.

```dax
[Referrals Created This Financial Year] =
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
			VAR year_start = DATE ( YEAR ( as_of ) - IF ( MONTH ( as_of ) < 4, 1, 0 ), 4, 1 )
			RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], year_start, as_of ) ) )
```

<a id="dax-business-referrals-created-this-month"></a>
### Referrals Created This Month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1004. Measure container: `_Measures`.

```dax
[Referrals Created This Month] =
VAR as_of = MAX ( 'fact_referral'[as_of_date] )
			RETURN IF ( NOT ISBLANK ( as_of ), CALCULATE ( [Total Referrals], DATESBETWEEN ( 'dim_date'[date], DATE ( YEAR ( as_of ), MONTH ( as_of ), 1 ), as_of ) ) )
```

<a id="dax-business-referrals-currently-active"></a>
### Referrals Currently Active

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 103. Measure container: `_Measures`.

```dax
[Referrals Currently Active] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_open] = TRUE () )
```

<a id="dax-business-referrals-placed-by-required-date"></a>
### Referrals Placed by Required Date

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 908. Measure container: `_Measures`.

```dax
[Referrals Placed by Required Date] =
CALCULATE ( [Total Referrals], 'fact_referral'[placed_by_required_date] = TRUE () )
```

<a id="dax-business-referrals-under-offer"></a>
### Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1030. Measure container: `_Measures`.

```dax
[Referrals Under Offer] =
CALCULATE ( [Total Referrals], KEEPFILTERS ( 'fact_referral'[is_open] = TRUE () ), KEEPFILTERS ( 'fact_referral'[current_status] = "UNDER_OFFER" ) )
```

<a id="dax-business-referrals-with-fully-signed-ipa"></a>
### Referrals With Fully Signed IPA

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1204. Measure container: `_Measures`.

```dax
[Referrals With Fully Signed IPA] =
CALCULATE ( DISTINCTCOUNT ( 'fact_ipa'[referral_id] ), KEEPFILTERS ( 'fact_ipa'[is_ipa_completed] = TRUE () ) )
```

<a id="dax-business-referrals-with-lifecycle-activity"></a>
### Referrals With Lifecycle Activity

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1518. Measure container: `_Measures`.

```dax
[Referrals With Lifecycle Activity] =
DISTINCTCOUNT ( 'fact_referral_lifecycle_event'[referral_id] )
```

<a id="dax-business-referrals-with-multiple-provider-assignments"></a>
### Referrals With Multiple Provider Assignments

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1428. Measure container: `_Measures`.

```dax
[Referrals With Multiple Provider Assignments] =
CALCULATE ( [Total Referrals], 'fact_referral'[provider_assignment_count] > 1 )
```

<a id="dax-business-referrals-with-an-offer"></a>
### Referrals With an Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 900. Measure container: `_Measures`.

```dax
[Referrals With an Offer] =
CALCULATE ( [Total Referrals], 'fact_referral'[has_offer] = TRUE () )
```

<a id="dax-business-referrals-without-provider-assignment"></a>
### Referrals Without Provider Assignment

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 904. Measure container: `_Measures`.

```dax
[Referrals Without Provider Assignment] =
CALCULATE ( [Total Referrals], 'fact_referral'[is_not_seen_by_providers] = TRUE () )
```

<a id="dax-business-referrals-closed-during-month"></a>
### Referrals closed during month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl`, line 19. Measure container: `_Story Measures`.

```dax
[Referrals closed during month] =
CALCULATE(DISTINCTCOUNT('fact_referral'[referral_id]), USERELATIONSHIP('fact_referral'[referral_closed_date],'dim_date'[date]), CROSSFILTER('fact_referral'[referral_created_date],'dim_date'[date],NONE), KEEPFILTERS(NOT ISBLANK('fact_referral'[referral_closed_date])))
```

<a id="dax-business-referrals-with-ipa-at-snapshot"></a>
### Referrals with IPA at Snapshot

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 883. Measure container: `_Measures`.

```dax
[Referrals with IPA at Snapshot] =
CALCULATE (
			    [Snapshot Referrals],
			    FILTER (
			        'fact_referral_snapshot',
			        NOT ISBLANK ( 'fact_referral_snapshot'[ipa_issued_date] )
			            && 'fact_referral_snapshot'[ipa_issued_date] < 'fact_referral_snapshot'[snapshot_date] + 1
			    )
			)
```

<a id="dax-business-residential-homes"></a>
### Residential Homes

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 257. Measure container: `_Measures`.

```dax
[Residential Homes] =
CALCULATE ( [Provider Homes Registered], 'dim_provider_home'[service_type] = "Residential" )
```

<a id="dax-business-snapshot-referrals"></a>
### Snapshot Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 700. Measure container: `_Measures`.

```dax
[Snapshot Referrals] =
DISTINCTCOUNT ( 'fact_referral_snapshot'[referral_id] )
```

<a id="dax-business-snapshot-referrals-mom-change"></a>
### Snapshot referrals MoM change

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl`, line 31. Measure container: `_Story Measures`.

```dax
[Snapshot referrals MoM change] =
VAR currentTotal = [Snapshot Referrals]
			VAR previousTotal = [Snapshot referrals previous month]
			RETURN IF(NOT ISBLANK(currentTotal) && NOT ISBLANK(previousTotal), currentTotal - previousTotal)
```

<a id="dax-business-snapshot-referrals-mom-percent"></a>
### Snapshot referrals MoM percent

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl`, line 39. Measure container: `_Story Measures`.

```dax
[Snapshot referrals MoM percent] =
DIVIDE([Snapshot referrals MoM change],[Snapshot referrals previous month])
```

<a id="dax-business-snapshot-referrals-previous-month"></a>
### Snapshot referrals previous month

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl`, line 24. Measure container: `_Story Measures`.

```dax
[Snapshot referrals previous month] =
VAR currentMonth = SELECTEDVALUE('dim_snapshot_month'[month_start])
			RETURN IF(NOT ISBLANK(currentMonth), CALCULATE([Snapshot Referrals], REMOVEFILTERS('dim_snapshot_month'), 'dim_snapshot_month'[month_start] = EDATE(currentMonth,-1)))
```

<a id="dax-business-spot-offer-rate"></a>
### Spot Offer Rate

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1439. Measure container: `_Measures`.

```dax
[Spot Offer Rate] =
DIVIDE ( [Spot Offers], [Non-Draft Offers] )
```

<a id="dax-business-spot-offers"></a>
### Spot Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 370. Measure container: `_Measures`.

```dax
[Spot Offers] =
CALCULATE ( [Non-Draft Offers], 'dim_provider_home (offer)'[is_spot] = TRUE () )
```

<a id="dax-business-spot-offers-on-referrals-under-offer"></a>
### Spot Offers on Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1350. Measure container: `_Measures`.

```dax
[Spot Offers on Referrals Under Offer] =
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

<a id="dax-business-successful-offers-on-referrals-under-offer"></a>
### Successful Offers on Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 34. Measure container: `_Measures`.

```dax
[Successful Offers on Referrals Under Offer] =
CALCULATE (
			    [Accepted Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```

<a id="dax-business-successful-offers-to-ipa-completed-percent"></a>
### Successful Offers to IPA Completed %

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 459. Measure container: `_Measures`.

```dax
[Successful Offers to IPA Completed %] =
DIVIDE ( [IPA Completed], [Accepted Offers] )
```

<a id="dax-business-supported-accommodation-homes"></a>
### Supported Accommodation Homes

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 262. Measure container: `_Measures`.

```dax
[Supported Accommodation Homes] =
CALCULATE (
			    [Provider Homes Registered],
			    'dim_provider_home'[service_type] = "Supported Accommodation"
			)
```

<a id="dax-business-total-gendered-referrals"></a>
### Total Gendered Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 84. Measure container: `_Measures`.

```dax
[Total Gendered Referrals] =
CALCULATE ( [Total Referrals], KEEPFILTERS ( FILTER ( 'dim_person', NOT ISBLANK ( 'dim_person'[gender_clean] ) && 'dim_person'[gender_clean] <> "Unknown" ) ) )
```

<a id="dax-business-total-ipa-weekly-cost"></a>
### Total IPA Weekly Cost

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1188. Measure container: `_Measures`.

```dax
[Total IPA Weekly Cost] =
SUM ( 'fact_ipa'[estimated_weekly_cost] )
```

<a id="dax-business-total-referrals"></a>
### Total Referrals

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 4. Measure container: `_Measures`.

```dax
[Total Referrals] =
DISTINCTCOUNT ( 'fact_referral'[referral_id] )
```

<a id="dax-business-unsuccessful-offers"></a>
### Unsuccessful Offers

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1578. Measure container: `_Measures`.

```dax
[Unsuccessful Offers] =
CALCULATE (
			    [Offers Submitted],
			    FILTER (
			        'fact_offer',
			        LOWER ( COALESCE ( 'fact_offer'[offer_status], "" ) )
			            IN { "declined", "rejected", "withdrawn", "offer_unsuccessful", "offer_withdrawn" }
			    )
			)
```

<a id="dax-business-unsuccessful-offers-on-referrals-under-offer"></a>
### Unsuccessful Offers on Referrals Under Offer

Source ZIP member: `SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition/tables/_Measures.tmdl`, line 1067. Measure container: `_Measures`.

```dax
[Unsuccessful Offers on Referrals Under Offer] =
CALCULATE (
			    [Unsuccessful Offers],
			    FILTER (
			        'fact_referral',
			        'fact_referral'[is_open] = TRUE () && 'fact_referral'[current_status] = "UNDER_OFFER"
			    )
			)
```


## Exact saved DAX — mission

<a id="dax-mission-active-dq-rules"></a>
### Active DQ Rules

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 473. Measure container: `_MissionControl_Measures`.

```dax
[Active DQ Rules] =
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:133`](#python-03-silver-business-rules-py-133)

<a id="dax-mission-archive-export-rows"></a>
### Archive Export Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 329. Measure container: `_MissionControl_Measures`.

```dax
[Archive Export Rows] =
SUM ( 'cfg_archive_table_export_load'[row_count] )
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-archive-file-failures"></a>
### Archive File Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 266. Measure container: `_MissionControl_Measures`.

```dax
[Archive File Failures] =
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-archive-file-rows-read"></a>
### Archive File Rows Read

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 284. Measure container: `_MissionControl_Measures`.

```dax
[Archive File Rows Read] =
SUM ( 'cfg_archive_file_load'[rows_read] )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-archive-file-rows-written"></a>
### Archive File Rows Written

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 293. Measure container: `_MissionControl_Measures`.

```dax
[Archive File Rows Written] =
SUM ( 'cfg_archive_file_load'[rows_written] )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-archive-files-awaiting-reload"></a>
### Archive Files Awaiting Reload

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 275. Measure container: `_MissionControl_Measures`.

```dax
[Archive Files Awaiting Reload] =
CALCULATE ( [Archive Files Processed], 'cfg_archive_file_load'[reload] = TRUE () )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-archive-files-processed"></a>
### Archive Files Processed

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 248. Measure container: `_MissionControl_Measures`.

```dax
[Archive Files Processed] =
COUNTROWS ( 'cfg_archive_file_load' )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-archive-pipeline-failures"></a>
### Archive Pipeline Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 85. Measure container: `_MissionControl_Measures`.

```dax
[Archive Pipeline Failures] =
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-archive-pipeline-runs"></a>
### Archive Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 67. Measure container: `_MissionControl_Measures`.

```dax
[Archive Pipeline Runs] =
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_archive_pipeline" )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-archive-table-exports"></a>
### Archive Table Exports

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 302. Measure container: `_MissionControl_Measures`.

```dax
[Archive Table Exports] =
COUNTROWS ( 'cfg_archive_table_export_load' )
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-archive-table-exports-awaiting-reload"></a>
### Archive Table Exports Awaiting Reload

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 320. Measure container: `_MissionControl_Measures`.

```dax
[Archive Table Exports Awaiting Reload] =
CALCULATE ( [Archive Table Exports], 'cfg_archive_table_export_load'[reload] = TRUE () )
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-archive-zip-batches"></a>
### Archive ZIP Batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 194. Measure container: `_MissionControl_Measures`.

```dax
[Archive ZIP Batches] =
COUNTROWS ( 'cfg_archive_zip_load' )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-archive-zip-batches-awaiting-reload"></a>
### Archive ZIP Batches Awaiting Reload

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 221. Measure container: `_MissionControl_Measures`.

```dax
[Archive ZIP Batches Awaiting Reload] =
CALCULATE ( [Archive ZIP Batches], 'cfg_archive_zip_load'[reload] = TRUE () )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-archive-zip-files-declared"></a>
### Archive ZIP Files Declared

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 230. Measure container: `_MissionControl_Measures`.

```dax
[Archive ZIP Files Declared] =
SUM ( 'cfg_archive_zip_load'[file_count] )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-archived-nullable-columns"></a>
### Archived Nullable Columns

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 554. Measure container: `_MissionControl_Measures`.

```dax
[Archived Nullable Columns] =
COUNTROWS ( FILTER ( 'cfg_archived_schema_live', UPPER ( COALESCE ( 'cfg_archived_schema_live'[is_nullable], "" ) ) IN { "TRUE", "YES", "Y", "1" } ) )
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-archived-schema-columns"></a>
### Archived Schema Columns

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 527. Measure container: `_MissionControl_Measures`.

```dax
[Archived Schema Columns] =
COUNTROWS ( 'cfg_archived_schema_live' )
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-archived-schema-data-types"></a>
### Archived Schema Data Types

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 563. Measure container: `_MissionControl_Measures`.

```dax
[Archived Schema Data Types] =
DISTINCTCOUNT ( 'cfg_archived_schema_live'[data_type] )
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-archived-schema-tables"></a>
### Archived Schema Tables

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 536. Measure container: `_MissionControl_Measures`.

```dax
[Archived Schema Tables] =
COUNTROWS ( SUMMARIZE ( 'cfg_archived_schema_live', 'cfg_archived_schema_live'[schema_name], 'cfg_archived_schema_live'[table_name] ) )
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-average-archive-zip-duration-min"></a>
### Average Archive ZIP Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 239. Measure container: `_MissionControl_Measures`.

```dax
[Average Archive ZIP Duration (min)] =
AVERAGEX ( FILTER ( 'cfg_archive_zip_load', NOT ISBLANK ( 'cfg_archive_zip_load'[started_at] ) && NOT ISBLANK ( 'cfg_archive_zip_load'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_archive_zip_load'[started_at], 'cfg_archive_zip_load'[ended_at], SECOND ), 60.0 ) )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-average-pipeline-duration-min"></a>
### Average Pipeline Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 139. Measure container: `_MissionControl_Measures`.

```dax
[Average Pipeline Duration (min)] =
AVERAGEX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-calendar-day-failures"></a>
### Calendar Day Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 913. Measure container: `_MissionControl_Measures`.

```dax
[Calendar Day Failures] =
COALESCE([Failed Job Runs], 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-calendar-day-in-window"></a>
### Calendar Day In Window

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 923. Measure container: `_MissionControl_Measures`.

```dax
[Calendar Day In Window] =
VAR d = SELECTEDVALUE('Load Calendar'[Date])
			RETURN IF(NOT ISBLANK(d) && d >= TODAY() - 364 && d <= TODAY(), 1, 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-calendar-day-other"></a>
### Calendar Day Other

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 918. Measure container: `_MissionControl_Measures`.

```dax
[Calendar Day Other] =
COALESCE(CALCULATE([Job Runs], KEEPFILTERS(rpt_job_run_summary[Outcome] IN {"Running", "Other"})), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-calendar-day-runs"></a>
### Calendar Day Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 908. Measure container: `_MissionControl_Measures`.

```dax
[Calendar Day Runs] =
COALESCE([Job Runs], 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-completed-pipeline-runs"></a>
### Completed Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 40. Measure container: `_MissionControl_Measures`.

```dax
[Completed Pipeline Runs] =
[Successful Pipeline Runs] + [Failed Pipeline Runs]
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-control-failures"></a>
### Control Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 581. Measure container: `_MissionControl_Measures`.

```dax
[Control Failures] =
[Failed Pipeline Runs] + [Failed Archive ZIP Batches] + [Archive File Failures] + [Failed Archive Table Exports] + [Failed Gold Snapshots]
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119); [`00_archive_load.py:653`](#python-00-archive-load-py-653); [`00_archive_load.py:798`](#python-00-archive-load-py-798); [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-critical-active-dq-rules"></a>
### Critical Active DQ Rules

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 482. Measure container: `_MissionControl_Measures`.

```dax
[Critical Active DQ Rules] =
COUNTROWS ( FILTER ( 'cfg_data_quality_rule', UPPER ( COALESCE ( 'cfg_data_quality_rule'[active], "" ) ) IN { "TRUE", "Y", "1" } && UPPER ( COALESCE ( 'cfg_data_quality_rule'[severity], "" ) ) = "CRITICAL" ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:133`](#python-03-silver-business-rules-py-133)

<a id="dax-mission-critical-rules-failing"></a>
### Critical Rules Failing

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 446. Measure container: `_MissionControl_Measures`.

```dax
[Critical Rules Failing] =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) = "CRITICAL" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-checked-rows"></a>
### DQ Checked Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 419. Measure container: `_MissionControl_Measures`.

```dax
[DQ Checked Rows] =
SUM ( 'cfg_data_quality_result'[checked_row_count] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-checks"></a>
### DQ Checks

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 383. Measure container: `_MissionControl_Measures`.

```dax
[DQ Checks] =
COUNTROWS ( 'cfg_data_quality_result' )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-evaluated-checks"></a>
### DQ Evaluated Checks

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 392. Measure container: `_MissionControl_Measures`.

```dax
[DQ Evaluated Checks] =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "PASS", "SUCCESS", "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-failed-checks"></a>
### DQ Failed Checks

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 401. Measure container: `_MissionControl_Measures`.

```dax
[DQ Failed Checks] =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-failed-rows"></a>
### DQ Failed Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 428. Measure container: `_MissionControl_Measures`.

```dax
[DQ Failed Rows] =
SUM ( 'cfg_data_quality_result'[failed_row_count] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-failure-rate"></a>
### DQ Failure Rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 410. Measure container: `_MissionControl_Measures`.

```dax
[DQ Failure Rate] =
DIVIDE ( [DQ Failed Checks], [DQ Evaluated Checks] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dq-failures-with-sample-keys"></a>
### DQ Failures With Sample Keys

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 464. Measure container: `_MissionControl_Measures`.

```dax
[DQ Failures With Sample Keys] =
COUNTROWS ( FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } && NOT ISBLANK ( 'cfg_data_quality_result'[sample_key_json] ) ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-dashboard-last-refreshed"></a>
### Dashboard Last Refreshed

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 599. Measure container: `_MissionControl_Measures`.

```dax
[Dashboard Last Refreshed] =
FORMAT ( UTCNOW (), "dd mmm yyyy HH:mm" )
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-day-explorer-job-visible"></a>
### Day Explorer Job Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 930. Measure container: `_MissionControl_Measures`.

```dax
[Day Explorer Job Visible] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_run_summary),
			    CALCULATE(COUNTROWS(rpt_job_run_summary), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(ISFILTERED('Load Calendar'[Date]) && NOT HASONEVALUE('Load Calendar'[Date]), 0, IF(n > 0, 1, 0))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-day-colour"></a>
### Day colour

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 46. Measure container: `_Load Experience`.

```dax
[Day colour] =
SWITCH(TRUE(),[Failures]>0,"#A43C49",[In progress or other]>0,"#66512B",[Successful]>=10,"#4C854F",[Successful]>0,"#345B3D","#242F28")
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-day-text-colour"></a>
### Day text colour

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 50. Measure container: `_Load Experience`.

```dax
[Day text colour] =
"#F3F7EF"
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-day-tile"></a>
### Day tile

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 39. Measure container: `_Load Experience`.

```dax
[Day tile] =
VAR d=SELECTEDVALUE('Load Calendar'[Date])
			VAR n=COALESCE([Runs],0)
			RETURN IF(NOT ISBLANK(d), FORMAT(d,"d") & UNICHAR(10) & IF(d>TODAY(),"Future",SWITCH(TRUE(),[Failures]>0,"! " & FORMAT([Failures],"0") & " failed",[In progress or other]>0,"~ " & FORMAT(n,"0") & " runs",n>0,FORMAT(n,"0") & " OK","No loads")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-calendar-failures"></a>
### Discovery calendar failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1956. Measure container: `_MissionControl_Measures`.

```dax
[Discovery calendar failures] =
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
			    FILTER('Discovery Job Runs', UPPER('Discovery Job Runs'[status]) IN {"FAILED", "FAILURE", "ERROR"}
			        || 'Discovery Job Runs'[steps_failed] > 0)), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-calendar-jobs"></a>
### Discovery calendar jobs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1949. Measure container: `_MissionControl_Measures`.

```dax
[Discovery calendar jobs] =
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-calendar-other"></a>
### Discovery calendar other

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1965. Measure container: `_MissionControl_Measures`.

```dax
[Discovery calendar other] =
COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
			    FILTER('Discovery Job Runs', NOT(UPPER('Discovery Job Runs'[status]) IN {"SUCCESS", "SUCCESSFUL", "SUCCEEDED", "FAILED", "FAILURE", "ERROR"})
			        && COALESCE('Discovery Job Runs'[steps_failed], 0) = 0)), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-archive-zip-load-latest-key"></a>
### Discovery cfg_archive_zip_load Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1864. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_archive_zip_load, cfg_archive_zip_load[run_id], "DiscoveryTime", MAX(cfg_archive_zip_load[started_at])), ALLSELECTED(cfg_archive_zip_load))
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])), [DiscoveryTime], DESC, cfg_archive_zip_load[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_archive_zip_load[run_id])
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-discovery-cfg-archive-zip-load-latest-time"></a>
### Discovery cfg_archive_zip_load Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1859. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load Latest time] =
CALCULATE(MAX(cfg_archive_zip_load[started_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-discovery-cfg-archive-zip-load-rows"></a>
### Discovery cfg_archive_zip_load Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1871. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_archive_zip_load), KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id]))), 0)
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-discovery-cfg-archive-zip-load-selected-time"></a>
### Discovery cfg_archive_zip_load Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1881. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load Selected time] =
CALCULATE(MAX(cfg_archive_zip_load[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-discovery-cfg-archive-zip-load-state"></a>
### Discovery cfg_archive_zip_load State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1886. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load State] =
VAR n = [Discovery cfg_archive_zip_load Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-archive-zip-load-visible"></a>
### Discovery cfg_archive_zip_load Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1876. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archive_zip_load Visible] =
IF([Discovery cfg_archive_zip_load Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-discovery-cfg-archived-schema-live-latest-time"></a>
### Discovery cfg_archived_schema_live Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1831. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archived_schema_live Latest time] =
CALCULATE(MAX(cfg_archived_schema_live[contract_loaded_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-discovery-cfg-archived-schema-live-rows"></a>
### Discovery cfg_archived_schema_live Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1836. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archived_schema_live Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_archived_schema_live), KEEPFILTERS(TREATAS({[Discovery cfg_archived_schema_live Latest time]}, cfg_archived_schema_live[contract_loaded_at]))), 0)
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-discovery-cfg-archived-schema-live-selected-time"></a>
### Discovery cfg_archived_schema_live Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1846. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archived_schema_live Selected time] =
CALCULATE(MAX(cfg_archived_schema_live[contract_loaded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_archived_schema_live Latest time]}, cfg_archived_schema_live[contract_loaded_at])))
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-discovery-cfg-archived-schema-live-state"></a>
### Discovery cfg_archived_schema_live State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1851. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archived_schema_live State] =
VAR n = [Discovery cfg_archived_schema_live Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-archived-schema-live-visible"></a>
### Discovery cfg_archived_schema_live Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1841. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_archived_schema_live Visible] =
IF([Discovery cfg_archived_schema_live Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-discovery-cfg-bronze-schema-live-context"></a>
### Discovery cfg_bronze_schema_live Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1634. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery cfg_bronze_schema_live Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-discovery-batches"></a>
### Discovery cfg_bronze_schema_live Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1658. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_bronze_schema_live[job_run_id]))), IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]), CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time]}, cfg_bronze_schema_live[captured_at]))), CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-distinct-objects"></a>
### Discovery cfg_bronze_schema_live Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1651. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[table_name]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_bronze_schema_live[job_run_id]))), IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]), CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[table_name]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time]}, cfg_bronze_schema_live[captured_at]))), CALCULATE(DISTINCTCOUNT(cfg_bronze_schema_live[table_name]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-latest-key"></a>
### Discovery cfg_bronze_schema_live Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1166. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_bronze_schema_live, cfg_bronze_schema_live[run_id],
			    "DiscoveryTime", MAX(cfg_bronze_schema_live[captured_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_bronze_schema_live[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_bronze_schema_live[run_id])
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-latest-time"></a>
### Discovery cfg_bronze_schema_live Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1161. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Latest time] =
CALCULATE(MAX(cfg_bronze_schema_live[captured_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-rows"></a>
### Discovery cfg_bronze_schema_live Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1175. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_bronze_schema_live), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_bronze_schema_live[job_run_id]))), IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]), CALCULATE(COUNTROWS(cfg_bronze_schema_live), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time]}, cfg_bronze_schema_live[captured_at]))), CALCULATE(COUNTROWS(cfg_bronze_schema_live), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-scope-count"></a>
### Discovery cfg_bronze_schema_live Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1644. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(cfg_bronze_schema_live,cfg_bronze_schema_live[table_name],cfg_bronze_schema_live[column_name])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_bronze_schema_live[job_run_id]))), IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(cfg_bronze_schema_live,cfg_bronze_schema_live[table_name],cfg_bronze_schema_live[column_name])), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time]}, cfg_bronze_schema_live[captured_at]))), CALCULATE(COUNTROWS(SUMMARIZE(cfg_bronze_schema_live,cfg_bronze_schema_live[table_name],cfg_bronze_schema_live[column_name])), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-selected-time"></a>
### Discovery cfg_bronze_schema_live Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1187. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_bronze_schema_live[captured_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_bronze_schema_live[job_run_id]))), IF(ISBLANK([Discovery cfg_bronze_schema_live Latest key]), CALCULATE(MAX(cfg_bronze_schema_live[captured_at]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest time]}, cfg_bronze_schema_live[captured_at]))), CALCULATE(MAX(cfg_bronze_schema_live[captured_at]), KEEPFILTERS(TREATAS({[Discovery cfg_bronze_schema_live Latest key]}, cfg_bronze_schema_live[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-state"></a>
### Discovery cfg_bronze_schema_live State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1194. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live State] =
VAR n = [Discovery cfg_bronze_schema_live Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-bronze-schema-live-visible"></a>
### Discovery cfg_bronze_schema_live Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1182. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_bronze_schema_live Visible] =
IF([Discovery cfg_bronze_schema_live Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-data-domain-context"></a>
### Discovery cfg_data_domain Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1572. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery cfg_data_domain Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-discovery-batches"></a>
### Discovery cfg_data_domain Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1596. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_data_domain[job_run_id]))), IF(ISBLANK([Discovery cfg_data_domain Latest key]), CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest time]}, cfg_data_domain[profiled_at]))), CALCULATE(DISTINCTCOUNT(cfg_data_domain[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest key]}, cfg_data_domain[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-distinct-objects"></a>
### Discovery cfg_data_domain Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1589. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_data_domain[job_run_id]))), IF(ISBLANK([Discovery cfg_data_domain Latest key]), CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest time]}, cfg_data_domain[profiled_at]))), CALCULATE(DISTINCTCOUNT(cfg_data_domain[source_table]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest key]}, cfg_data_domain[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-latest-key"></a>
### Discovery cfg_data_domain Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 979. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_data_domain, cfg_data_domain[run_id],
			    "DiscoveryTime", MAX(cfg_data_domain[profiled_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_data_domain[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_data_domain[run_id])
```

Python/Spark SQL evidence: [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-latest-time"></a>
### Discovery cfg_data_domain Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 974. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Latest time] =
CALCULATE(MAX(cfg_data_domain[profiled_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-rows"></a>
### Discovery cfg_data_domain Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 988. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_data_domain), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_data_domain[job_run_id]))), IF(ISBLANK([Discovery cfg_data_domain Latest key]), CALCULATE(COUNTROWS(cfg_data_domain), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest time]}, cfg_data_domain[profiled_at]))), CALCULATE(COUNTROWS(cfg_data_domain), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest key]}, cfg_data_domain[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-scope-count"></a>
### Discovery cfg_data_domain Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1582. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(cfg_data_domain,cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_data_domain[job_run_id]))), IF(ISBLANK([Discovery cfg_data_domain Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(cfg_data_domain,cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest time]}, cfg_data_domain[profiled_at]))), CALCULATE(COUNTROWS(SUMMARIZE(cfg_data_domain,cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name])), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest key]}, cfg_data_domain[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-selected-time"></a>
### Discovery cfg_data_domain Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1000. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_data_domain[profiled_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_data_domain[job_run_id]))), IF(ISBLANK([Discovery cfg_data_domain Latest key]), CALCULATE(MAX(cfg_data_domain[profiled_at]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest time]}, cfg_data_domain[profiled_at]))), CALCULATE(MAX(cfg_data_domain[profiled_at]), KEEPFILTERS(TREATAS({[Discovery cfg_data_domain Latest key]}, cfg_data_domain[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-state"></a>
### Discovery cfg_data_domain State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1007. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain State] =
VAR n = [Discovery cfg_data_domain Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-data-domain-visible"></a>
### Discovery cfg_data_domain Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 995. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_data_domain Visible] =
IF([Discovery cfg_data_domain Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`99_data_domain.py:110`](#python-99-data-domain-py-110); [`99_common_library.py:462`](#python-99-common-library-py-462)

<a id="dax-mission-discovery-cfg-gold-lineage-mapping-rows"></a>
### Discovery cfg_gold_lineage_mapping Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1554. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_gold_lineage_mapping Rows] =
COALESCE(COUNTROWS(cfg_gold_lineage_mapping), 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-gold-lineage-mapping-state"></a>
### Discovery cfg_gold_lineage_mapping State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1564. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_gold_lineage_mapping State] =
VAR n = [Discovery cfg_gold_lineage_mapping Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-gold-lineage-mapping-visible"></a>
### Discovery cfg_gold_lineage_mapping Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1559. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_gold_lineage_mapping Visible] =
IF([Discovery cfg_gold_lineage_mapping Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-location-coordinate-rows"></a>
### Discovery cfg_location_coordinate Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1015. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_location_coordinate Rows] =
COALESCE(COUNTROWS(cfg_location_coordinate), 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-location-coordinate-state"></a>
### Discovery cfg_location_coordinate State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1025. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_location_coordinate State] =
VAR n = [Discovery cfg_location_coordinate Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-location-coordinate-visible"></a>
### Discovery cfg_location_coordinate Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1020. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_location_coordinate Visible] =
IF([Discovery cfg_location_coordinate Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-month-end-gold-run-latest-key"></a>
### Discovery cfg_month_end_gold_run Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1899. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_month_end_gold_run, cfg_month_end_gold_run[run_id], "DiscoveryTime", MAX(cfg_month_end_gold_run[started_at])), ALLSELECTED(cfg_month_end_gold_run))
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])), [DiscoveryTime], DESC, cfg_month_end_gold_run[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_month_end_gold_run[run_id])
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-discovery-cfg-month-end-gold-run-latest-time"></a>
### Discovery cfg_month_end_gold_run Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1894. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run Latest time] =
CALCULATE(MAX(cfg_month_end_gold_run[started_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-discovery-cfg-month-end-gold-run-rows"></a>
### Discovery cfg_month_end_gold_run Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1906. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_month_end_gold_run), KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id]))), 0)
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-discovery-cfg-month-end-gold-run-selected-time"></a>
### Discovery cfg_month_end_gold_run Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1916. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run Selected time] =
CALCULATE(MAX(cfg_month_end_gold_run[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id])))
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-discovery-cfg-month-end-gold-run-state"></a>
### Discovery cfg_month_end_gold_run State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1921. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run State] =
VAR n = [Discovery cfg_month_end_gold_run Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-month-end-gold-run-visible"></a>
### Discovery cfg_month_end_gold_run Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1911. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_month_end_gold_run Visible] =
IF([Discovery cfg_month_end_gold_run Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-discovery-cfg-referential-exception-latest-key"></a>
### Discovery cfg_referential_exception Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1317. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_referential_exception, cfg_referential_exception[run_id],
			    "DiscoveryTime", MAX(cfg_referential_exception[detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_referential_exception[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_referential_exception[run_id])
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-referential-exception-latest-time"></a>
### Discovery cfg_referential_exception Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1312. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception Latest time] =
CALCULATE(MAX(cfg_referential_exception[detected_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-referential-exception-rows"></a>
### Discovery cfg_referential_exception Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1326. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_referential_exception), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_referential_exception[job_run_id]))), IF(ISBLANK([Discovery cfg_referential_exception Latest key]), CALCULATE(COUNTROWS(cfg_referential_exception), KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest time]}, cfg_referential_exception[detected_at]))), CALCULATE(COUNTROWS(cfg_referential_exception), KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest key]}, cfg_referential_exception[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-referential-exception-selected-time"></a>
### Discovery cfg_referential_exception Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1338. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_referential_exception[detected_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_referential_exception[job_run_id]))), IF(ISBLANK([Discovery cfg_referential_exception Latest key]), CALCULATE(MAX(cfg_referential_exception[detected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest time]}, cfg_referential_exception[detected_at]))), CALCULATE(MAX(cfg_referential_exception[detected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_referential_exception Latest key]}, cfg_referential_exception[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-referential-exception-state"></a>
### Discovery cfg_referential_exception State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1345. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception State] =
VAR n = [Discovery cfg_referential_exception Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-referential-exception-visible"></a>
### Discovery cfg_referential_exception Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1333. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_referential_exception Visible] =
IF([Discovery cfg_referential_exception Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-latest-key"></a>
### Discovery cfg_rejected_row Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1276. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_rejected_row, cfg_rejected_row[run_id],
			    "DiscoveryTime", MAX(cfg_rejected_row[rejected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_rejected_row[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_rejected_row[run_id])
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-latest-time"></a>
### Discovery cfg_rejected_row Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1271. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row Latest time] =
CALCULATE(MAX(cfg_rejected_row[rejected_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-rows"></a>
### Discovery cfg_rejected_row Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1285. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_rejected_row), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_rejected_row[job_run_id]))), IF(ISBLANK([Discovery cfg_rejected_row Latest key]), CALCULATE(COUNTROWS(cfg_rejected_row), KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest time]}, cfg_rejected_row[rejected_at]))), CALCULATE(COUNTROWS(cfg_rejected_row), KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest key]}, cfg_rejected_row[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-selected-time"></a>
### Discovery cfg_rejected_row Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1297. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_rejected_row[rejected_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_rejected_row[job_run_id]))), IF(ISBLANK([Discovery cfg_rejected_row Latest key]), CALCULATE(MAX(cfg_rejected_row[rejected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest time]}, cfg_rejected_row[rejected_at]))), CALCULATE(MAX(cfg_rejected_row[rejected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_rejected_row Latest key]}, cfg_rejected_row[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-state"></a>
### Discovery cfg_rejected_row State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1304. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row State] =
VAR n = [Discovery cfg_rejected_row Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-rejected-row-visible"></a>
### Discovery cfg_rejected_row Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1292. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_rejected_row Visible] =
IF([Discovery cfg_rejected_row Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-discovery-cfg-schema-contract-column-latest-time"></a>
### Discovery cfg_schema_contract_column Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1202. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_contract_column Latest time] =
CALCULATE(MAX(cfg_schema_contract_column[contract_loaded_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-schema-contract-column-rows"></a>
### Discovery cfg_schema_contract_column Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1207. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_contract_column Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_schema_contract_column), KEEPFILTERS(TREATAS({[Discovery cfg_schema_contract_column Latest time]}, cfg_schema_contract_column[contract_loaded_at]))), 0)
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-schema-contract-column-selected-time"></a>
### Discovery cfg_schema_contract_column Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1217. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_contract_column Selected time] =
CALCULATE(MAX(cfg_schema_contract_column[contract_loaded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_contract_column Latest time]}, cfg_schema_contract_column[contract_loaded_at])))
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-schema-contract-column-state"></a>
### Discovery cfg_schema_contract_column State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1222. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_contract_column State] =
VAR n = [Discovery cfg_schema_contract_column Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-schema-contract-column-visible"></a>
### Discovery cfg_schema_contract_column Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1212. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_contract_column Visible] =
IF([Discovery cfg_schema_contract_column Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-schema-definition-candidate-rows"></a>
### Discovery cfg_schema_definition_candidate Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1143. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_definition_candidate Rows] =
COALESCE(COUNTROWS(cfg_schema_definition_candidate), 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-schema-definition-candidate-state"></a>
### Discovery cfg_schema_definition_candidate State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1153. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_definition_candidate State] =
VAR n = [Discovery cfg_schema_definition_candidate Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-schema-definition-candidate-visible"></a>
### Discovery cfg_schema_definition_candidate Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1148. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_definition_candidate Visible] =
IF([Discovery cfg_schema_definition_candidate Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-schema-drift-definition-latest-time"></a>
### Discovery cfg_schema_drift_definition Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1115. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_definition Latest time] =
CALCULATE(MAX(cfg_schema_drift_definition[definition_loaded_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:120`](#python-01a-cfg-schema-capture-live-py-120)

<a id="dax-mission-discovery-cfg-schema-drift-definition-rows"></a>
### Discovery cfg_schema_drift_definition Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1120. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_definition Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_schema_drift_definition), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_definition Latest time]}, cfg_schema_drift_definition[definition_loaded_at]))), 0)
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:120`](#python-01a-cfg-schema-capture-live-py-120)

<a id="dax-mission-discovery-cfg-schema-drift-definition-selected-time"></a>
### Discovery cfg_schema_drift_definition Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1130. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_definition Selected time] =
CALCULATE(MAX(cfg_schema_drift_definition[definition_loaded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_definition Latest time]}, cfg_schema_drift_definition[definition_loaded_at])))
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:120`](#python-01a-cfg-schema-capture-live-py-120)

<a id="dax-mission-discovery-cfg-schema-drift-definition-state"></a>
### Discovery cfg_schema_drift_definition State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1135. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_definition State] =
VAR n = [Discovery cfg_schema_drift_definition Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:120`](#python-01a-cfg-schema-capture-live-py-120); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-schema-drift-definition-visible"></a>
### Discovery cfg_schema_drift_definition Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1125. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_definition Visible] =
IF([Discovery cfg_schema_drift_definition Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:120`](#python-01a-cfg-schema-capture-live-py-120)

<a id="dax-mission-discovery-cfg-schema-drift-event-context"></a>
### Discovery cfg_schema_drift_event Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1603. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery cfg_schema_drift_event Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-discovery-batches"></a>
### Discovery cfg_schema_drift_event Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1627. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_schema_drift_event[job_run_id]))), IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]), CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time]}, cfg_schema_drift_event[detected_at]))), CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-distinct-objects"></a>
### Discovery cfg_schema_drift_event Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1620. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[target_table]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_schema_drift_event[job_run_id]))), IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]), CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[target_table]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time]}, cfg_schema_drift_event[detected_at]))), CALCULATE(DISTINCTCOUNT(cfg_schema_drift_event[target_table]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-latest-key"></a>
### Discovery cfg_schema_drift_event Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1038. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_schema_drift_event, cfg_schema_drift_event[run_id],
			    "DiscoveryTime", MAX(cfg_schema_drift_event[detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_schema_drift_event[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_schema_drift_event[run_id])
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-latest-time"></a>
### Discovery cfg_schema_drift_event Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1033. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Latest time] =
CALCULATE(MAX(cfg_schema_drift_event[detected_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-rows"></a>
### Discovery cfg_schema_drift_event Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1047. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_schema_drift_event), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_schema_drift_event[job_run_id]))), IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]), CALCULATE(COUNTROWS(cfg_schema_drift_event), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time]}, cfg_schema_drift_event[detected_at]))), CALCULATE(COUNTROWS(cfg_schema_drift_event), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-scope-count"></a>
### Discovery cfg_schema_drift_event Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1613. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(cfg_schema_drift_event,cfg_schema_drift_event[drift_key])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_schema_drift_event[job_run_id]))), IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(cfg_schema_drift_event,cfg_schema_drift_event[drift_key])), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time]}, cfg_schema_drift_event[detected_at]))), CALCULATE(COUNTROWS(SUMMARIZE(cfg_schema_drift_event,cfg_schema_drift_event[drift_key])), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-selected-time"></a>
### Discovery cfg_schema_drift_event Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1059. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_schema_drift_event[detected_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_schema_drift_event[job_run_id]))), IF(ISBLANK([Discovery cfg_schema_drift_event Latest key]), CALCULATE(MAX(cfg_schema_drift_event[detected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest time]}, cfg_schema_drift_event[detected_at]))), CALCULATE(MAX(cfg_schema_drift_event[detected_at]), KEEPFILTERS(TREATAS({[Discovery cfg_schema_drift_event Latest key]}, cfg_schema_drift_event[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-state"></a>
### Discovery cfg_schema_drift_event State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1066. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event State] =
VAR n = [Discovery cfg_schema_drift_event Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-schema-drift-event-visible"></a>
### Discovery cfg_schema_drift_event Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1054. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_schema_drift_event Visible] =
IF([Discovery cfg_schema_drift_event Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`01a_cfg_schema_capture_live.py:308`](#python-01a-cfg-schema-capture-live-py-308)

<a id="dax-mission-discovery-cfg-silver-export-load-latest-key"></a>
### Discovery cfg_silver_export_load Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1399. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_silver_export_load, cfg_silver_export_load[run_id],
			    "DiscoveryTime", MAX(cfg_silver_export_load[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_silver_export_load[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_silver_export_load[run_id])
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-export-load-latest-time"></a>
### Discovery cfg_silver_export_load Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1394. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load Latest time] =
CALCULATE(MAX(cfg_silver_export_load[started_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-export-load-rows"></a>
### Discovery cfg_silver_export_load Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1408. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_silver_export_load), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_silver_export_load[job_run_id]))), IF(ISBLANK([Discovery cfg_silver_export_load Latest key]), CALCULATE(COUNTROWS(cfg_silver_export_load), KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest time]}, cfg_silver_export_load[started_at]))), CALCULATE(COUNTROWS(cfg_silver_export_load), KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest key]}, cfg_silver_export_load[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-export-load-selected-time"></a>
### Discovery cfg_silver_export_load Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1420. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_silver_export_load[started_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_silver_export_load[job_run_id]))), IF(ISBLANK([Discovery cfg_silver_export_load Latest key]), CALCULATE(MAX(cfg_silver_export_load[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest time]}, cfg_silver_export_load[started_at]))), CALCULATE(MAX(cfg_silver_export_load[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_silver_export_load Latest key]}, cfg_silver_export_load[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-export-load-state"></a>
### Discovery cfg_silver_export_load State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1427. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load State] =
VAR n = [Discovery cfg_silver_export_load Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-export-load-visible"></a>
### Discovery cfg_silver_export_load Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1415. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_export_load Visible] =
IF([Discovery cfg_silver_export_load Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`00_setup_cfg.py:96`](#python-00-setup-cfg-py-96)

<a id="dax-mission-discovery-cfg-silver-load-control-latest-key"></a>
### Discovery cfg_silver_load_control Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1440. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_silver_load_control, cfg_silver_load_control[run_id],
			    "DiscoveryTime", MAX(cfg_silver_load_control[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_silver_load_control[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_silver_load_control[run_id])
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-silver-load-control-latest-time"></a>
### Discovery cfg_silver_load_control Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1435. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control Latest time] =
CALCULATE(MAX(cfg_silver_load_control[started_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-silver-load-control-rows"></a>
### Discovery cfg_silver_load_control Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1449. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control Rows] =
COALESCE(CALCULATE(COUNTROWS(cfg_silver_load_control), KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest key]}, cfg_silver_load_control[run_id]))), 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-silver-load-control-selected-time"></a>
### Discovery cfg_silver_load_control Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1459. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control Selected time] =
CALCULATE(MAX(cfg_silver_load_control[started_at]), KEEPFILTERS(TREATAS({[Discovery cfg_silver_load_control Latest key]}, cfg_silver_load_control[run_id])))
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-silver-load-control-state"></a>
### Discovery cfg_silver_load_control State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1464. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control State] =
VAR n = [Discovery cfg_silver_load_control Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-silver-load-control-visible"></a>
### Discovery cfg_silver_load_control Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1454. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_silver_load_control Visible] =
IF([Discovery cfg_silver_load_control Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-table-load-metric-context"></a>
### Discovery cfg_table_load_metric Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1696. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery cfg_table_load_metric Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-discovery-batches"></a>
### Discovery cfg_table_load_metric Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1720. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_table_load_metric[job_run_id]))), IF(ISBLANK([Discovery cfg_table_load_metric Latest key]), CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time]}, cfg_table_load_metric[recorded_at]))), CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[run_id]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-distinct-objects"></a>
### Discovery cfg_table_load_metric Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1713. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[source_object]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_table_load_metric[job_run_id]))), IF(ISBLANK([Discovery cfg_table_load_metric Latest key]), CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[source_object]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time]}, cfg_table_load_metric[recorded_at]))), CALCULATE(DISTINCTCOUNT(cfg_table_load_metric[source_object]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-latest-key"></a>
### Discovery cfg_table_load_metric Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1358. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(cfg_table_load_metric, cfg_table_load_metric[run_id],
			    "DiscoveryTime", MAX(cfg_table_load_metric[recorded_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, cfg_table_load_metric[run_id], DESC)
			RETURN MAXX(LatestBatch, cfg_table_load_metric[run_id])
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-table-load-metric-latest-time"></a>
### Discovery cfg_table_load_metric Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1353. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Latest time] =
CALCULATE(MAX(cfg_table_load_metric[recorded_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-discovery-cfg-table-load-metric-rows"></a>
### Discovery cfg_table_load_metric Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1367. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(cfg_table_load_metric), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_table_load_metric[job_run_id]))), IF(ISBLANK([Discovery cfg_table_load_metric Latest key]), CALCULATE(COUNTROWS(cfg_table_load_metric), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time]}, cfg_table_load_metric[recorded_at]))), CALCULATE(COUNTROWS(cfg_table_load_metric), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-scope-count"></a>
### Discovery cfg_table_load_metric Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1706. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(cfg_table_load_metric,cfg_table_load_metric[target_object])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_table_load_metric[job_run_id]))), IF(ISBLANK([Discovery cfg_table_load_metric Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(cfg_table_load_metric,cfg_table_load_metric[target_object])), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time]}, cfg_table_load_metric[recorded_at]))), CALCULATE(COUNTROWS(SUMMARIZE(cfg_table_load_metric,cfg_table_load_metric[target_object])), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-selected-time"></a>
### Discovery cfg_table_load_metric Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1379. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(cfg_table_load_metric[recorded_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), cfg_table_load_metric[job_run_id]))), IF(ISBLANK([Discovery cfg_table_load_metric Latest key]), CALCULATE(MAX(cfg_table_load_metric[recorded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest time]}, cfg_table_load_metric[recorded_at]))), CALCULATE(MAX(cfg_table_load_metric[recorded_at]), KEEPFILTERS(TREATAS({[Discovery cfg_table_load_metric Latest key]}, cfg_table_load_metric[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-state"></a>
### Discovery cfg_table_load_metric State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1386. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric State] =
VAR n = [Discovery cfg_table_load_metric Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-cfg-table-load-metric-visible"></a>
### Discovery cfg_table_load_metric Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1374. Measure container: `_MissionControl_Measures`.

```dax
[Discovery cfg_table_load_metric Visible] =
IF([Discovery cfg_table_load_metric Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-history-selected"></a>
### Discovery history selected

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 969. Measure container: `_MissionControl_Measures`.

```dax
[Discovery history selected] =
IF(ISFILTERED('Load Calendar'[Date]) || ISFILTERED('Discovery Job Runs'[job_run_id]), 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-job-picker-visible"></a>
### Discovery job picker visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1974. Measure container: `_MissionControl_Measures`.

```dax
[Discovery job picker visible] =
IF(CALCULATE(COUNTROWS('Discovery Job Runs'),
			    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))) > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-discovery-rpt-job-data-quality-context"></a>
### Discovery rpt_job_data_quality Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1665. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery rpt_job_data_quality Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-discovery-batches"></a>
### Discovery rpt_job_data_quality Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1689. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_data_quality[job_run_id]))), IF(ISBLANK([Discovery rpt_job_data_quality Latest key]), CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[run_id]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time]}, rpt_job_data_quality[checked_at]))), CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[run_id]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-distinct-objects"></a>
### Discovery rpt_job_data_quality Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1682. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[source_table]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_data_quality[job_run_id]))), IF(ISBLANK([Discovery rpt_job_data_quality Latest key]), CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[source_table]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time]}, rpt_job_data_quality[checked_at]))), CALCULATE(DISTINCTCOUNT(rpt_job_data_quality[source_table]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-latest-key"></a>
### Discovery rpt_job_data_quality Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1235. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_data_quality, rpt_job_data_quality[run_id],
			    "DiscoveryTime", MAX(rpt_job_data_quality[checked_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_data_quality[run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_data_quality[run_id])
```

Python/Spark SQL evidence: [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-latest-time"></a>
### Discovery rpt_job_data_quality Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1230. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Latest time] =
CALCULATE(MAX(rpt_job_data_quality[checked_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-rows"></a>
### Discovery rpt_job_data_quality Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1244. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(rpt_job_data_quality), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_data_quality[job_run_id]))), IF(ISBLANK([Discovery rpt_job_data_quality Latest key]), CALCULATE(COUNTROWS(rpt_job_data_quality), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time]}, rpt_job_data_quality[checked_at]))), CALCULATE(COUNTROWS(rpt_job_data_quality), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-scope-count"></a>
### Discovery rpt_job_data_quality Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1675. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_data_quality,rpt_job_data_quality[rule_id])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_data_quality[job_run_id]))), IF(ISBLANK([Discovery rpt_job_data_quality Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_data_quality,rpt_job_data_quality[rule_id])), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time]}, rpt_job_data_quality[checked_at]))), CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_data_quality,rpt_job_data_quality[rule_id])), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-selected-time"></a>
### Discovery rpt_job_data_quality Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1256. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(rpt_job_data_quality[checked_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_data_quality[job_run_id]))), IF(ISBLANK([Discovery rpt_job_data_quality Latest key]), CALCULATE(MAX(rpt_job_data_quality[checked_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest time]}, rpt_job_data_quality[checked_at]))), CALCULATE(MAX(rpt_job_data_quality[checked_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_data_quality Latest key]}, rpt_job_data_quality[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-state"></a>
### Discovery rpt_job_data_quality State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1263. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality State] =
VAR n = [Discovery rpt_job_data_quality Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-data-quality-visible"></a>
### Discovery rpt_job_data_quality Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1251. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_data_quality Visible] =
IF([Discovery rpt_job_data_quality Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:202`](#python-06-reports-py-202)

<a id="dax-mission-discovery-rpt-job-layer-lineage-context"></a>
### Discovery rpt_job_layer_lineage Context

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1727. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Context] =
VAR History = [Discovery history selected] = 1
			VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
			VAR LatestTime = [Discovery rpt_job_layer_lineage Latest time]
			RETURN IF(History,
			    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
			    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-discovery-batches"></a>
### Discovery rpt_job_layer_lineage Discovery batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1751. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Discovery batches] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[job_run_id]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_layer_lineage[job_run_id]))), IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]), CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[job_run_id]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time]}, rpt_job_layer_lineage[observed_at]))), CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[job_run_id]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-distinct-objects"></a>
### Discovery rpt_job_layer_lineage Distinct objects

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1744. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Distinct objects] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[source_object]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_layer_lineage[job_run_id]))), IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]), CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[source_object]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time]}, rpt_job_layer_lineage[observed_at]))), CALCULATE(DISTINCTCOUNT(rpt_job_layer_lineage[source_object]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-latest-key"></a>
### Discovery rpt_job_layer_lineage Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1477. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_layer_lineage, rpt_job_layer_lineage[job_run_id],
			    "DiscoveryTime", MAX(rpt_job_layer_lineage[observed_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_layer_lineage[job_run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_layer_lineage[job_run_id])
```

Python/Spark SQL evidence: [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-latest-time"></a>
### Discovery rpt_job_layer_lineage Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1472. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Latest time] =
CALCULATE(MAX(rpt_job_layer_lineage[observed_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-rows"></a>
### Discovery rpt_job_layer_lineage Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1486. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(rpt_job_layer_lineage), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_layer_lineage[job_run_id]))), IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]), CALCULATE(COUNTROWS(rpt_job_layer_lineage), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time]}, rpt_job_layer_lineage[observed_at]))), CALCULATE(COUNTROWS(rpt_job_layer_lineage), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-scope-count"></a>
### Discovery rpt_job_layer_lineage Scope count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1737. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Scope count] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_layer_lineage,rpt_job_layer_lineage[target_layer],rpt_job_layer_lineage[target_object])), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_layer_lineage[job_run_id]))), IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]), CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_layer_lineage,rpt_job_layer_lineage[target_layer],rpt_job_layer_lineage[target_object])), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time]}, rpt_job_layer_lineage[observed_at]))), CALCULATE(COUNTROWS(SUMMARIZE(rpt_job_layer_lineage,rpt_job_layer_lineage[target_layer],rpt_job_layer_lineage[target_object])), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id]))))),0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-selected-time"></a>
### Discovery rpt_job_layer_lineage Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1498. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(rpt_job_layer_lineage[observed_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_layer_lineage[job_run_id]))), IF(ISBLANK([Discovery rpt_job_layer_lineage Latest key]), CALCULATE(MAX(rpt_job_layer_lineage[observed_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest time]}, rpt_job_layer_lineage[observed_at]))), CALCULATE(MAX(rpt_job_layer_lineage[observed_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_layer_lineage Latest key]}, rpt_job_layer_lineage[job_run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-state"></a>
### Discovery rpt_job_layer_lineage State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1505. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage State] =
VAR n = [Discovery rpt_job_layer_lineage Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-layer-lineage-visible"></a>
### Discovery rpt_job_layer_lineage Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1493. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_layer_lineage Visible] =
IF([Discovery rpt_job_layer_lineage Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:235`](#python-06-reports-py-235)

<a id="dax-mission-discovery-rpt-job-schema-drift-latest-key"></a>
### Discovery rpt_job_schema_drift Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1079. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_schema_drift, rpt_job_schema_drift[run_id],
			    "DiscoveryTime", MAX(rpt_job_schema_drift[last_detected_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_schema_drift[run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_schema_drift[run_id])
```

Python/Spark SQL evidence: [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-schema-drift-latest-time"></a>
### Discovery rpt_job_schema_drift Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1074. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift Latest time] =
CALCULATE(MAX(rpt_job_schema_drift[last_detected_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-schema-drift-rows"></a>
### Discovery rpt_job_schema_drift Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1088. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(rpt_job_schema_drift), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_schema_drift[job_run_id]))), IF(ISBLANK([Discovery rpt_job_schema_drift Latest key]), CALCULATE(COUNTROWS(rpt_job_schema_drift), KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest time]}, rpt_job_schema_drift[last_detected_at]))), CALCULATE(COUNTROWS(rpt_job_schema_drift), KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest key]}, rpt_job_schema_drift[run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-schema-drift-selected-time"></a>
### Discovery rpt_job_schema_drift Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1100. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(rpt_job_schema_drift[last_detected_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_schema_drift[job_run_id]))), IF(ISBLANK([Discovery rpt_job_schema_drift Latest key]), CALCULATE(MAX(rpt_job_schema_drift[last_detected_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest time]}, rpt_job_schema_drift[last_detected_at]))), CALCULATE(MAX(rpt_job_schema_drift[last_detected_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_schema_drift Latest key]}, rpt_job_schema_drift[run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-schema-drift-state"></a>
### Discovery rpt_job_schema_drift State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1107. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift State] =
VAR n = [Discovery rpt_job_schema_drift Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-schema-drift-visible"></a>
### Discovery rpt_job_schema_drift Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1095. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_schema_drift Visible] =
IF([Discovery rpt_job_schema_drift Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:177`](#python-06-reports-py-177)

<a id="dax-mission-discovery-rpt-job-step-summary-latest-key"></a>
### Discovery rpt_job_step_summary Latest key

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1518. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary Latest key] =
VAR Batches = CALCULATETABLE(SUMMARIZE(rpt_job_step_summary, rpt_job_step_summary[job_run_id],
			    "DiscoveryTime", MAX(rpt_job_step_summary[started_at])), REMOVEFILTERS())
			VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
			    [DiscoveryTime], DESC, rpt_job_step_summary[job_run_id], DESC)
			RETURN MAXX(LatestBatch, rpt_job_step_summary[job_run_id])
```

Python/Spark SQL evidence: [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-discovery-rpt-job-step-summary-latest-time"></a>
### Discovery rpt_job_step_summary Latest time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1513. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary Latest time] =
CALCULATE(MAX(rpt_job_step_summary[started_at]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-discovery-rpt-job-step-summary-rows"></a>
### Discovery rpt_job_step_summary Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1527. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary Rows] =
COALESCE(IF([Discovery history selected] = 1, CALCULATE(COUNTROWS(rpt_job_step_summary), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_step_summary[job_run_id]))), IF(ISBLANK([Discovery rpt_job_step_summary Latest key]), CALCULATE(COUNTROWS(rpt_job_step_summary), KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest time]}, rpt_job_step_summary[started_at]))), CALCULATE(COUNTROWS(rpt_job_step_summary), KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest key]}, rpt_job_step_summary[job_run_id]))))), 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-discovery-rpt-job-step-summary-selected-time"></a>
### Discovery rpt_job_step_summary Selected time

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1539. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary Selected time] =
IF([Discovery history selected] = 1, CALCULATE(MAX(rpt_job_step_summary[started_at]), KEEPFILTERS(TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
			            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), rpt_job_step_summary[job_run_id]))), IF(ISBLANK([Discovery rpt_job_step_summary Latest key]), CALCULATE(MAX(rpt_job_step_summary[started_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest time]}, rpt_job_step_summary[started_at]))), CALCULATE(MAX(rpt_job_step_summary[started_at]), KEEPFILTERS(TREATAS({[Discovery rpt_job_step_summary Latest key]}, rpt_job_step_summary[job_run_id])))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-discovery-rpt-job-step-summary-state"></a>
### Discovery rpt_job_step_summary State

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1546. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary State] =
VAR n = [Discovery rpt_job_step_summary Rows]
			RETURN IF(n = 0,
			    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
			    "Retained records: " & FORMAT(n, "#,0"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-discovery-rpt-job-step-summary-visible"></a>
### Discovery rpt_job_step_summary Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1534. Measure container: `_MissionControl_Measures`.

```dax
[Discovery rpt_job_step_summary Visible] =
IF([Discovery rpt_job_step_summary Rows] > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:74`](#python-06-reports-py-74)

<a id="dax-mission-failed-archive-table-exports"></a>
### Failed Archive Table Exports

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 311. Measure container: `_MissionControl_Measures`.

```dax
[Failed Archive Table Exports] =
COUNTROWS ( FILTER ( 'cfg_archive_table_export_load', UPPER ( COALESCE ( 'cfg_archive_table_export_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-failed-archive-zip-batches"></a>
### Failed Archive ZIP Batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 212. Measure container: `_MissionControl_Measures`.

```dax
[Failed Archive ZIP Batches] =
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-failed-gold-snapshots"></a>
### Failed Gold Snapshots

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 356. Measure container: `_MissionControl_Measures`.

```dax
[Failed Gold Snapshots] =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-failed-job-runs"></a>
### Failed Job Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 625. Measure container: `_MissionControl_Measures`.

```dax
[Failed Job Runs] =
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-failed-job-steps"></a>
### Failed Job Steps

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 734. Measure container: `_MissionControl_Measures`.

```dax
[Failed Job Steps] =
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-failed-pipeline-runs"></a>
### Failed Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 22. Measure container: `_MissionControl_Measures`.

```dax
[Failed Pipeline Runs] =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-failures"></a>
### Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 14. Measure container: `_Load Experience`.

```dax
[Failures] =
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome]="Failed"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-gold-snapshot-dq-failures"></a>
### Gold Snapshot DQ Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 374. Measure container: `_MissionControl_Measures`.

```dax
[Gold Snapshot DQ Failures] =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[dq_result], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-gold-snapshot-runs"></a>
### Gold Snapshot Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 338. Measure container: `_MissionControl_Measures`.

```dax
[Gold Snapshot Runs] =
COUNTROWS ( 'cfg_month_end_gold_run' )
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-gold-snapshots-awaiting-replay"></a>
### Gold Snapshots Awaiting Replay

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 365. Measure container: `_MissionControl_Measures`.

```dax
[Gold Snapshots Awaiting Replay] =
CALCULATE ( [Gold Snapshot Runs], 'cfg_month_end_gold_run'[reload] = TRUE () )
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-high-or-critical-rules-failing"></a>
### High or Critical Rules Failing

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 455. Measure container: `_MissionControl_Measures`.

```dax
[High or Critical Rules Failing] =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[severity], "" ) ) IN { "CRITICAL", "HIGH" } && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-in-progress-or-other"></a>
### In progress or other

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 19. Measure container: `_Load Experience`.

```dax
[In progress or other] =
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome] IN {"Running","Other"}))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-runs"></a>
### Job Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 607. Measure container: `_MissionControl_Measures`.

```dax
[Job Runs] =
DISTINCTCOUNT ( 'rpt_job_run_summary'[job_run_id] )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-steps"></a>
### Job Steps

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 716. Measure container: `_MissionControl_Measures`.

```dax
[Job Steps] =
COUNTROWS ( 'rpt_job_step_timing' )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-job-steps-with-error"></a>
### Job Steps With Error

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 743. Measure container: `_MissionControl_Measures`.

```dax
[Job Steps With Error] =
COUNTROWS ( FILTER ( 'rpt_job_step_timing', NOT ISBLANK ( 'rpt_job_step_timing'[error_message] ) && 'rpt_job_step_timing'[error_message] <> "" ) )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-job-success-rate"></a>
### Job Success Rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 634. Measure container: `_MissionControl_Measures`.

```dax
[Job Success Rate] =
DIVIDE ( [Successful Job Runs], [Successful Job Runs] + [Failed Job Runs] )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-actual-min"></a>
### Job actual min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 79. Measure container: `_Run Benchmarks`.

```dax
[Job actual min] =
DIVIDE(SELECTEDVALUE('rpt_job_run_summary'[job_duration_seconds]),60)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-baseline-n"></a>
### Job baseline n

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 4. Measure container: `_Run Benchmarks`.

```dax
[Job baseline n] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-comparison"></a>
### Job comparison

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 84. Measure container: `_Run Benchmarks`.

```dax
[Job comparison] =
VAR n=[Job baseline n]
			VAR actual=[Job actual min]
			RETURN SWITCH(TRUE(),ISBLANK(n),"Select one job",n<5,"Insufficient history",ISBLANK(actual),"No duration recorded",actual<[Job prior p25 min],"Below prior P25",actual>[Job prior p75 min],"Above prior P75","Within prior IQR")
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-prior-mean-min"></a>
### Job prior mean min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 19. Measure container: `_Run Benchmarks`.

```dax
[Job prior mean min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-prior-median-min"></a>
### Job prior median min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 34. Measure container: `_Run Benchmarks`.

```dax
[Job prior median min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-prior-p25-min"></a>
### Job prior p25 min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 49. Measure container: `_Run Benchmarks`.

```dax
[Job prior p25 min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-job-prior-p75-min"></a>
### Job prior p75 min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 64. Measure container: `_Run Benchmarks`.

```dax
[Job prior p75 min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-archived-schema-capture"></a>
### Latest Archived Schema Capture

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 545. Measure container: `_MissionControl_Measures`.

```dax
[Latest Archived Schema Capture] =
MAX ( 'cfg_archived_schema_live'[contract_loaded_at] )
```

Python/Spark SQL evidence: [`01a_cfg_schema_capture_archive.py:107`](#python-01a-cfg-schema-capture-archive-py-107)

<a id="dax-mission-latest-job-run-id"></a>
### Latest Job Run ID

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 652. Measure container: `_MissionControl_Measures`.

```dax
[Latest Job Run ID] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-job-run-started"></a>
### Latest Job Run Started

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 643. Measure container: `_MissionControl_Measures`.

```dax
[Latest Job Run Started] =
MAXX ( FILTER ( ALLSELECTED ( 'rpt_job_run_summary' ), NOT ISBLANK ( 'rpt_job_run_summary'[started_at] ) ), 'rpt_job_run_summary'[started_at] )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-critical-rules"></a>
### Latest Load Critical Rules

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 882. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Critical Rules] =
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([Critical Rules Failing], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-evaluated-checks"></a>
### Latest Load Evaluated Checks

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 858. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Evaluated Checks] =
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Evaluated Checks], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-failed-checks"></a>
### Latest Load Failed Checks

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 866. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Failed Checks] =
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Failed Checks], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-failed-rows"></a>
### Latest Load Failed Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 874. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Failed Rows] =
VAR _id = [Latest Load Run ID]
			RETURN IF([Latest Load Quality Records] > 0,
			    COALESCE(CALCULATE([DQ Failed Rows], KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))), 0))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-quality-records"></a>
### Latest Load Quality Records

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 851. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Quality Records] =
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id), COALESCE(CALCULATE(COUNTROWS(cfg_data_quality_result), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = _id), 0))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-quality-report"></a>
### Latest Load Quality Report

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 898. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Quality Report] =
VAR _id = [Latest Load Run ID]
			VAR lastCheck = CALCULATE(MAX(cfg_data_quality_result[checked_at]), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = _id)
			RETURN IF(ISBLANK(_id), "No load recorded in this model",
			    "Load started " & FORMAT([Latest Load Started], "dd MMM yyyy HH:mm") & " | " &
			    IF([Latest Load Quality Records] = 0, "No quality report for this load yet",
			       "Quality checked " & FORMAT(lastCheck, "dd MMM yyyy HH:mm")))
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-run-id"></a>
### Latest Load Run ID

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 830. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Run ID] =
VAR latest = TOPN(1,
			    FILTER(CALCULATETABLE(rpt_job_run_summary, REMOVEFILTERS()), NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC)
			RETURN CALCULATE(MAXX(latest, rpt_job_run_summary[job_run_id]), REMOVEFILTERS())
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-started"></a>
### Latest Load Started

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 838. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Started] =
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id), CALCULATE(MAX(rpt_job_run_summary[started_at]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = _id))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-load-status"></a>
### Latest Load Status

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 845. Measure container: `_MissionControl_Measures`.

```dax
[Latest Load Status] =
VAR _id = [Latest Load Run ID]
			RETURN IF(ISBLANK(_id), "No loads", CALCULATE(SELECTEDVALUE(rpt_job_run_summary[status]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = _id))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-pipeline-end"></a>
### Latest Pipeline End

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 175. Measure container: `_MissionControl_Measures`.

```dax
[Latest Pipeline End] =
MAX ( 'cfg_pipeline_run'[ended_at] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-latest-pipeline-row-visible"></a>
### Latest Pipeline Row Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1758. Measure container: `_MissionControl_Measures`.

```dax
[Latest Pipeline Row Visible] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(cfg_pipeline_run),
			    CALCULATE(COUNTROWS(cfg_pipeline_run), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-pipeline-status"></a>
### Latest Pipeline Status

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 184. Measure container: `_MissionControl_Measures`.

```dax
[Latest Pipeline Status] =
VAR latest_end = [Latest Pipeline End]
			RETURN
			    CALCULATE ( CONCATENATEX ( VALUES ( 'cfg_pipeline_run'[status] ), 'cfg_pipeline_run'[status], ", " ), 'cfg_pipeline_run'[ended_at] = latest_end )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-latest-matching-archive-zip-batches"></a>
### Latest matching Archive ZIP Batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1929. Measure container: `_MissionControl_Measures`.

```dax
[Latest matching Archive ZIP Batches] =
CALCULATE([Archive ZIP Batches], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-latest-matching-archive-zip-batches-awaiting-reload"></a>
### Latest matching Archive ZIP Batches Awaiting Reload

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1934. Measure container: `_MissionControl_Measures`.

```dax
[Latest matching Archive ZIP Batches Awaiting Reload] =
CALCULATE([Archive ZIP Batches Awaiting Reload], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-latest-matching-failed-archive-zip-batches"></a>
### Latest matching Failed Archive ZIP Batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1939. Measure container: `_MissionControl_Measures`.

```dax
[Latest matching Failed Archive ZIP Batches] =
CALCULATE([Failed Archive ZIP Batches], KEEPFILTERS(TREATAS({[Discovery cfg_archive_zip_load Latest key]}, cfg_archive_zip_load[run_id])))
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-latest-matching-failed-gold-snapshots"></a>
### Latest matching Failed Gold Snapshots

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1944. Measure container: `_MissionControl_Measures`.

```dax
[Latest matching Failed Gold Snapshots] =
CALCULATE([Failed Gold Snapshots], KEEPFILTERS(TREATAS({[Discovery cfg_month_end_gold_run Latest key]}, cfg_month_end_gold_run[run_id])))
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-latest-or-selected-failures"></a>
### Latest or selected Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1795. Measure container: `_MissionControl_Measures`.

```dax
[Latest or selected Failures] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Failures],
			    CALCULATE([Failures], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-or-selected-p95-duration-min"></a>
### Latest or selected P95 duration min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1807. Measure container: `_MissionControl_Measures`.

```dax
[Latest or selected P95 duration min] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [P95 duration min],
			    CALCULATE([P95 duration min], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-or-selected-rows-written"></a>
### Latest or selected Rows written

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1819. Measure container: `_MissionControl_Measures`.

```dax
[Latest or selected Rows written] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Rows written],
			    CALCULATE([Rows written], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-or-selected-runs"></a>
### Latest or selected Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1771. Measure container: `_MissionControl_Measures`.

```dax
[Latest or selected Runs] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Runs],
			    CALCULATE([Runs], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-latest-or-selected-success-rate"></a>
### Latest or selected Success rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 1783. Measure container: `_MissionControl_Measures`.

```dax
[Latest or selected Success rate] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			RETURN IF(ISFILTERED('Load Calendar'[Date]), [Success rate],
			    CALCULATE([Success rate], KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-live-pipeline-failures"></a>
### Live Pipeline Failures

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 76. Measure container: `_MissionControl_Measures`.

```dax
[Live Pipeline Failures] =
CALCULATE ( [Failed Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-live-pipeline-runs"></a>
### Live Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 58. Measure container: `_MissionControl_Measures`.

```dax
[Live Pipeline Runs] =
CALCULATE ( [Pipeline Runs], 'cfg_pipeline_run'[pipeline_name] = "90_run_live_pipeline" )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-longest-job-step-duration-min"></a>
### Longest Job Step Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 789. Measure container: `_MissionControl_Measures`.

```dax
[Longest Job Step Duration (min)] =
DIVIDE ( MAX ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-operational-exception-count"></a>
### Operational Exception Count

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 590. Measure container: `_MissionControl_Measures`.

```dax
[Operational Exception Count] =
[Control Failures] + [DQ Failed Checks]
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119); [`00_archive_load.py:653`](#python-00-archive-load-py-653); [`00_archive_load.py:798`](#python-00-archive-load-py-798); [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611); [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-p95-pipeline-duration-min"></a>
### P95 Pipeline Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 148. Measure container: `_MissionControl_Measures`.

```dax
[P95 Pipeline Duration (min)] =
PERCENTILEX.INC ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ), 0.95 )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-p95-duration-min"></a>
### P95 duration min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 29. Measure container: `_Load Experience`.

```dax
[P95 duration min] =
PERCENTILEX.INC(FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[ended_at]) && rpt_job_run_summary[job_duration_seconds]>=0), DIVIDE(rpt_job_run_summary[job_duration_seconds],60),0.95)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-pipeline-rows-read"></a>
### Pipeline Rows Read

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 112. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Rows Read] =
SUM ( 'cfg_pipeline_run'[rows_read] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-rows-written"></a>
### Pipeline Rows Written

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 121. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Rows Written] =
SUM ( 'cfg_pipeline_run'[rows_written] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-rows-per-minute"></a>
### Pipeline Rows per Minute

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 166. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Rows per Minute] =
DIVIDE ( [Pipeline Rows Written], [Total Pipeline Duration (min)] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-runs"></a>
### Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 4. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Runs] =
DISTINCTCOUNT ( 'cfg_pipeline_run'[run_id] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-runs-with-error"></a>
### Pipeline Runs With Error

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 130. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Runs With Error] =
COUNTROWS ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[error_message] ) ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-success-rate"></a>
### Pipeline Success Rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 49. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Success Rate] =
DIVIDE ( [Successful Pipeline Runs], [Completed Pipeline Runs] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-tables-failed"></a>
### Pipeline Tables Failed

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 103. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Tables Failed] =
SUM ( 'cfg_pipeline_run'[tables_failed] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-pipeline-tables-succeeded"></a>
### Pipeline Tables Succeeded

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 94. Measure container: `_MissionControl_Measures`.

```dax
[Pipeline Tables Succeeded] =
SUM ( 'cfg_pipeline_run'[tables_succeeded] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-ri-checked-rows"></a>
### RI Checked Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 500. Measure container: `_MissionControl_Measures`.

```dax
[RI Checked Rows] =
CALCULATE ( [DQ Checked Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-ri-failed-rows"></a>
### RI Failed Rows

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 509. Measure container: `_MissionControl_Measures`.

```dax
[RI Failed Rows] =
CALCULATE ( [DQ Failed Rows], FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-ri-failure-rate"></a>
### RI Failure Rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 518. Measure container: `_MissionControl_Measures`.

```dax
[RI Failure Rate] =
DIVIDE ( [RI Failed Rows], [RI Checked Rows] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-ri-rules-failing"></a>
### RI Rules Failing

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 491. Measure container: `_MissionControl_Measures`.

```dax
[RI Rules Failing] =
CALCULATE ( DISTINCTCOUNT ( 'cfg_data_quality_result'[rule_id] ), FILTER ( 'cfg_data_quality_result', UPPER ( COALESCE ( 'cfg_data_quality_result'[rule_type], "" ) ) = "REFERENTIAL_INTEGRITY" && UPPER ( COALESCE ( 'cfg_data_quality_result'[status], "" ) ) IN { "FAILED", "FAIL", "ERROR" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

<a id="dax-mission-reload-requests"></a>
### Reload Requests

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 572. Measure container: `_MissionControl_Measures`.

```dax
[Reload Requests] =
[Archive ZIP Batches Awaiting Reload] + [Archive Files Awaiting Reload] + [Archive Table Exports Awaiting Reload] + [Gold Snapshots Awaiting Replay]
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653); [`00_archive_load.py:798`](#python-00-archive-load-py-798); [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-rows-written"></a>
### Rows written

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 34. Measure container: `_Load Experience`.

```dax
[Rows written] =
SUM(rpt_job_run_summary[rows_written])
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-running-pipeline-runs"></a>
### Running Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 31. Measure container: `_MissionControl_Measures`.

```dax
[Running Pipeline Runs] =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "RUNNING", "IN_PROGRESS", "STARTED" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-runs"></a>
### Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 4. Measure container: `_Load Experience`.

```dax
[Runs] =
DISTINCTCOUNT(rpt_job_run_summary[job_run_id])
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-step-error-detail"></a>
### Selected Step Error Detail

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 814. Measure container: `_MissionControl_Measures`.

```dax
[Selected Step Error Detail] =
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

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-selected-or-latest-failed-steps"></a>
### Selected or Latest Failed Steps

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 766. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Failed Steps] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					[Failed Job Steps],
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-or-latest-job-duration-min"></a>
### Selected or Latest Job Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 702. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Job Duration (min)] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					DIVIDE ( MAX ( 'rpt_job_run_summary'[job_duration_seconds] ), 60.0 ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-or-latest-job-error"></a>
### Selected or Latest Job Error

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 689. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Job Error] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					SELECTEDVALUE ( 'rpt_job_run_summary'[error_message] ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-or-latest-job-run-id"></a>
### Selected or Latest Job Run ID

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 668. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Job Run ID] =
COALESCE ( SELECTEDVALUE ( 'rpt_job_run_summary'[job_run_id] ), [Latest Job Run ID] )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-or-latest-job-status"></a>
### Selected or Latest Job Status

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 676. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Job Status] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					SELECTEDVALUE ( 'rpt_job_run_summary'[status] ),
					'rpt_job_run_summary'[job_run_id] = selected_job_run_id
				)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-selected-or-latest-job-steps"></a>
### Selected or Latest Job Steps

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 752. Measure container: `_MissionControl_Measures`.

```dax
[Selected or Latest Job Steps] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			RETURN
				CALCULATE (
					[Job Steps],
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-show-latest-load-quality"></a>
### Show Latest Load Quality

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 890. Measure container: `_MissionControl_Measures`.

```dax
[Show Latest Load Quality] =
VAR _id = [Latest Load Run ID]
			RETURN IF(NOT ISBLANK(_id) && CALCULATE(COUNTROWS(cfg_data_quality_result),
			    KEEPFILTERS(TREATAS({_id}, cfg_data_quality_result[job_run_id]))) > 0, 1, 0)
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-show-step-for-selected-or-latest-job-run"></a>
### Show Step for Selected or Latest Job Run

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 798. Measure container: `_MissionControl_Measures`.

```dax
[Show Step for Selected or Latest Job Run] =
VAR selected_job_run_id = [Selected or Latest Job Run ID]
			VAR matching_steps =
				CALCULATE (
					COUNTROWS ( 'rpt_job_step_timing' ),
					KEEPFILTERS ( 'rpt_job_step_timing'[job_run_id] = selected_job_run_id )
				)
			RETURN
				IF ( NOT ISBLANK ( selected_job_run_id ) && matching_steps > 0, 1, 0 )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45); [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-single-calendar-day"></a>
### Single calendar day

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 188. Measure container: `_Run Benchmarks`.

```dax
[Single calendar day] =
IF(HASONEVALUE('Load Calendar'[Date]),1,0)
```

Python/Spark SQL evidence: Local semantic calculation; see its referenced measures/tables.

<a id="dax-mission-step-actual-min"></a>
### Step actual min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 176. Measure container: `_Run Benchmarks`.

```dax
[Step actual min] =
DIVIDE(SELECTEDVALUE('rpt_job_step_timing'[step_duration_seconds]),60)
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-baseline-n"></a>
### Step baseline n

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 91. Measure container: `_Run Benchmarks`.

```dax
[Step baseline n] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-comparison"></a>
### Step comparison

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 181. Measure container: `_Run Benchmarks`.

```dax
[Step comparison] =
VAR n=[Step baseline n]
			VAR actual=[Step actual min]
			RETURN SWITCH(TRUE(),ISBLANK(n),"Select one step",n<5,"Insufficient history",ISBLANK(actual),"No duration recorded",actual<[Step prior p25 min],"Below prior P25",actual>[Step prior p75 min],"Above prior P75","Within prior IQR")
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-prior-mean-min"></a>
### Step prior mean min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 108. Measure container: `_Run Benchmarks`.

```dax
[Step prior mean min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-prior-median-min"></a>
### Step prior median min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 125. Measure container: `_Run Benchmarks`.

```dax
[Step prior median min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-prior-p25-min"></a>
### Step prior p25 min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 142. Measure container: `_Run Benchmarks`.

```dax
[Step prior p25 min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-step-prior-p75-min"></a>
### Step prior p75 min

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Run Benchmarks.tmdl`, line 159. Measure container: `_Run Benchmarks`.

```dax
[Step prior p75 min] =
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

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141); [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-success-rate"></a>
### Success rate

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 24. Measure container: `_Load Experience`.

```dax
[Success rate] =
DIVIDE([Successful],[Successful]+[Failures])
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-successful"></a>
### Successful

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_Load Experience.tmdl`, line 9. Measure container: `_Load Experience`.

```dax
[Successful] =
CALCULATE([Runs], KEEPFILTERS(rpt_job_run_summary[Outcome]="Successful"))
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-successful-archive-files"></a>
### Successful Archive Files

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 257. Measure container: `_MissionControl_Measures`.

```dax
[Successful Archive Files] =
COUNTROWS ( FILTER ( 'cfg_archive_file_load', UPPER ( COALESCE ( 'cfg_archive_file_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`00_archive_load.py:798`](#python-00-archive-load-py-798)

<a id="dax-mission-successful-archive-zip-batches"></a>
### Successful Archive ZIP Batches

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 203. Measure container: `_MissionControl_Measures`.

```dax
[Successful Archive ZIP Batches] =
COUNTROWS ( FILTER ( 'cfg_archive_zip_load', UPPER ( COALESCE ( 'cfg_archive_zip_load'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`00_archive_load.py:653`](#python-00-archive-load-py-653)

<a id="dax-mission-successful-gold-snapshots"></a>
### Successful Gold Snapshots

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 347. Measure container: `_MissionControl_Measures`.

```dax
[Successful Gold Snapshots] =
COUNTROWS ( FILTER ( 'cfg_month_end_gold_run', UPPER ( COALESCE ( 'cfg_month_end_gold_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`02a_archive_silver.py:611`](#python-02a-archive-silver-py-611)

<a id="dax-mission-successful-job-runs"></a>
### Successful Job Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 616. Measure container: `_MissionControl_Measures`.

```dax
[Successful Job Runs] =
CALCULATE ( [Job Runs], FILTER ( 'rpt_job_run_summary', UPPER ( COALESCE ( 'rpt_job_run_summary'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-successful-job-steps"></a>
### Successful Job Steps

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 725. Measure container: `_MissionControl_Measures`.

```dax
[Successful Job Steps] =
CALCULATE ( [Job Steps], FILTER ( 'rpt_job_step_timing', UPPER ( COALESCE ( 'rpt_job_step_timing'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-successful-pipeline-runs"></a>
### Successful Pipeline Runs

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 13. Measure container: `_MissionControl_Measures`.

```dax
[Successful Pipeline Runs] =
CALCULATE ( [Pipeline Runs], FILTER ( 'cfg_pipeline_run', UPPER ( COALESCE ( 'cfg_pipeline_run'[status], "" ) ) IN { "SUCCESS", "SUCCEEDED" } ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-timeline-job-visible"></a>
### Timeline Job Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 943. Measure container: `_MissionControl_Measures`.

```dax
[Timeline Job Visible] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_run_summary),
			    CALCULATE(COUNTROWS(rpt_job_run_summary), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-timeline-step-visible"></a>
### Timeline Step Visible

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 956. Measure container: `_MissionControl_Measures`.

```dax
[Timeline Step Visible] =
VAR LatestJob = CALCULATETABLE(TOPN(1,
			    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
			    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
			    ALLSELECTED(rpt_job_run_summary))
			VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
			VAR n = IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS(rpt_job_step_timing),
			    CALCULATE(COUNTROWS(rpt_job_step_timing), KEEPFILTERS(TREATAS({LatestId}, rpt_job_run_summary[job_run_id]))))
			RETURN IF(n > 0, 1, 0)
```

Python/Spark SQL evidence: [`06_reports.py:141`](#python-06-reports-py-141)

<a id="dax-mission-total-job-step-duration-min"></a>
### Total Job Step Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 780. Measure container: `_MissionControl_Measures`.

```dax
[Total Job Step Duration (min)] =
DIVIDE ( SUM ( 'rpt_job_step_timing'[step_duration_seconds] ), 60.0 )
```

Python/Spark SQL evidence: [`06_reports.py:45`](#python-06-reports-py-45)

<a id="dax-mission-total-pipeline-duration-min"></a>
### Total Pipeline Duration (min)

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 157. Measure container: `_MissionControl_Measures`.

```dax
[Total Pipeline Duration (min)] =
SUMX ( FILTER ( 'cfg_pipeline_run', NOT ISBLANK ( 'cfg_pipeline_run'[started_at] ) && NOT ISBLANK ( 'cfg_pipeline_run'[ended_at] ) ), DIVIDE ( DATEDIFF ( 'cfg_pipeline_run'[started_at], 'cfg_pipeline_run'[ended_at], SECOND ), 60.0 ) )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:119`](#python-03-silver-business-rules-py-119)

<a id="dax-mission-weighted-dq-failure-percentage"></a>
### Weighted DQ Failure Percentage

Source ZIP member: `SM WMPP Mission Control Import/SM WMPP Mission Control.SemanticModel/definition/tables/_MissionControl_Measures.tmdl`, line 437. Measure container: `_MissionControl_Measures`.

```dax
[Weighted DQ Failure Percentage] =
DIVIDE ( [DQ Failed Rows], [DQ Checked Rows] )
```

Python/Spark SQL evidence: [`03_silver_business_rules.py:208`](#python-03-silver-business-rules-py-208)

## Python and Spark SQL implementation definitions

These are verbatim source definitions or notebook cells, extracted without executing Spark. Parameter placeholders remain intact. A configuration table DDL is distinguished from its population logic. Where only setup/control evidence is located, it does not prove a KPI-producing pipeline has run. `latest_dimension` and `copy_bridge` call sites use the helper definitions in `05_gold_dimensions.py`; read those helpers with each mapping.

<a id="python-00-archive-load-py-653"></a>
### 00_archive_load.py:653

Source: [project X/00_archive_load.py:653](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_archive_load.py#L653). Observed physical object: `monitoring.cfg_archive_zip_load`.

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
### 00_archive_load.py:798

Source: [project X/00_archive_load.py:798](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_archive_load.py#L798). Observed physical object: `monitoring.cfg_archive_file_load`.

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
### 00_setup_cfg.py:96

Source: [project X/00_setup_cfg.py:96](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/00_setup_cfg.py#L96). Observed physical object: `monitoring.cfg_silver_export_load`.

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
### 01a_cfg_schema_capture_archive.py:107

Source: [project X/01a_cfg_schema_capture_archive.py:107](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_archive.py#L107). Observed physical object: `monitoring.cfg_archived_schema_live`.

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
### 01a_cfg_schema_capture_live.py:120

Source: [project X/01a_cfg_schema_capture_live.py:120](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_live.py#L120). Observed physical object: `monitoring.cfg_schema_drift_definition`.

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

<a id="python-01a-cfg-schema-capture-live-py-308"></a>
### 01a_cfg_schema_capture_live.py:308

Source: [project X/01a_cfg_schema_capture_live.py:308](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/01a_cfg_schema_capture_live.py#L308). Observed physical object: `monitoring.cfg_schema_drift_event`.

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

<a id="python-02a-archive-silver-py-611"></a>
### 02a_archive_silver.py:611

Source: [project X/02a_archive_silver.py:611](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/02a_archive_silver.py#L611). Observed physical object: `monitoring.cfg_month_end_gold_run`.

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
### 03_silver_business_rules.py:119

Source: [project X/03_silver_business_rules.py:119](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L119). Observed physical object: `monitoring.cfg_pipeline_run`.

```python
append_rows("monitoring.cfg_pipeline_run", [(PIPELINE_RUN_ID, "03_silver_business_rules", "SILVER", f"LATEST_{DQ_RUN_MODE}",
    STARTED_AT, None, "RUNNING", 0, 0, 0, 0, None, JOB_RUN_ID or None)],
    "run_id string,pipeline_name string,layer string,source_kind string,started_at timestamp,ended_at timestamp,status string,tables_succeeded int,tables_failed int,rows_read long,rows_written long,error_message string,job_run_id string")
log_step("Pipeline run row registered")
```

<a id="python-03-silver-business-rules-py-133"></a>
### 03_silver_business_rules.py:133

Source: [project X/03_silver_business_rules.py:133](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L133). Observed physical object: `monitoring.cfg_data_quality_rule`.

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
### 03_silver_business_rules.py:208

Source: [project X/03_silver_business_rules.py:208](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/03_silver_business_rules.py#L208). Observed physical object: `monitoring.cfg_data_quality_result`.

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

<a id="python-04-gold-model-py-232"></a>
### 04_gold_model.py:232

Source: [project X/04_gold_model.py:232](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L232). Observed physical object: `gold.fact_referral`.

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
### 04_gold_model.py:567

Source: [project X/04_gold_model.py:567](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L567). Observed physical object: `gold.fact_referral_snapshot`.

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
### 04_gold_model.py:698

Source: [project X/04_gold_model.py:698](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L698). Observed physical object: `gold.fact_referral_lifecycle_event`.

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
### 04_gold_model.py:712

Source: [project X/04_gold_model.py:712](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L712). Observed physical object: `gold.fact_offer`.

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
### 04_gold_model.py:817

Source: [project X/04_gold_model.py:817](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L817). Observed physical object: `gold.fact_ipa`.

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
### 04_gold_model.py:847

Source: [project X/04_gold_model.py:847](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L847). Observed physical object: `gold.fact_referral_provider`.

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
### 04_gold_model.py:935

Source: [project X/04_gold_model.py:935](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/04_gold_model.py#L935). Observed physical object: `gold.fact_provider_kpi_monthly`.

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
### 05_gold_dimensions.py:128

Source: [project X/05_gold_dimensions.py:128](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L128). Observed physical object: `gold.dim_date`.

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
### 05_gold_dimensions.py:155

Source: [project X/05_gold_dimensions.py:155](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L155). Observed physical object: `gold.dim_provider`.

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
### 05_gold_dimensions.py:163

Source: [project X/05_gold_dimensions.py:163](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L163). Observed physical object: `gold.dim_provider_home`.

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
### 05_gold_dimensions.py:173

Source: [project X/05_gold_dimensions.py:173](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L173). Observed physical object: `gold.dim_framework`.

```python
latest_dimension(
    "silver.framework", "gold.dim_framework", ["framework_code"],
    [("framework_code", "framework_code"), ("framework_name", "framework_name"),
     ("placement_type", "placement_type"), ("start_date", "start_date"),
     ("end_date", "end_date"), ("export_date", "source_export_date")],
)
```

<a id="python-05-gold-dimensions-py-194"></a>
### 05_gold_dimensions.py:194

Source: [project X/05_gold_dimensions.py:194](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L194). Observed physical object: `gold.dim_person`.

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
### 05_gold_dimensions.py:210

Source: [project X/05_gold_dimensions.py:210](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L210). Observed physical object: `gold.bridge_referral_framework_category`.

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
### 05_gold_dimensions.py:239

Source: [project X/05_gold_dimensions.py:239](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L239). Observed physical object: `gold.dim_provider_submission_document`.

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
### 05_gold_dimensions.py:253

Source: [project X/05_gold_dimensions.py:253](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L253). Observed physical object: `gold.dim_referral_provider_message`.

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
### 05_gold_dimensions.py:390

Source: [project X/05_gold_dimensions.py:390](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/05_gold_dimensions.py#L390). Observed physical object: `gold.dim_snapshot_month`.

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
### 06_reports.py:45

Source: [project X/06_reports.py:45](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L45). Observed physical object: `monitoring.rpt_job_step_timing`.

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
### 06_reports.py:74

Source: [project X/06_reports.py:74](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L74). Observed physical object: `monitoring.rpt_job_step_summary`.

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
### 06_reports.py:141

Source: [project X/06_reports.py:141](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L141). Observed physical object: `monitoring.rpt_job_run_summary`.

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
### 06_reports.py:177

Source: [project X/06_reports.py:177](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L177). Observed physical object: `monitoring.rpt_job_schema_drift`.

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
### 06_reports.py:202

Source: [project X/06_reports.py:202](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L202). Observed physical object: `monitoring.rpt_job_data_quality`.

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
### 06_reports.py:235

Source: [project X/06_reports.py:235](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/06_reports.py#L235). Observed physical object: `monitoring.rpt_job_layer_lineage`.

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

<a id="python-99-common-library-py-462"></a>
### 99_common_library.py:462

Source: [project X/99_common_library.py:462](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/99_common_library.py#L462). Observed physical object: `monitoring.cfg_data_domain`.

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
### 99_data_domain.py:110

Source: [project X/99_data_domain.py:110](https://github.com/NewRay99/fabric-csv-bronze-ingestion/blob/0a65e962ff3ab9681ed87d9a0a54df610774b736/project%20X/99_data_domain.py#L110). Observed physical object: `monitoring.cfg_data_domain`.

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

## Runtime acceptance still required

1. Reopen the workbook and verify the consuming query promotes row 1 and selects the intended columns. The RID spacer column J remains blank; select named fields rather than every used cell.
2. The saved business model uses embedded `#table` data for `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage`. Workbook changes alone do not update them. Reconcile their values and stable model column names, including `KPI_s_`, through a separate controlled model update.
3. Rebuild/deploy the relevant Gold and monitoring definitions, then refresh both models. A `CREATE ... IF NOT EXISTS` monitoring definition is not a replacement deployment.
4. Reconcile zero/blank, status/date filters, provider/authority roles, numerator/denominator, duplicate keys, missing periods and IPA versus offer grain against known source records.
5. Test Mission Control selection/latest/history filters, domains, errors, archive/replay and refresh timestamps with known runs. Review access to sample keys/errors.
6. Obtain owner decisions for alternative KPI semantics, proposed operational requirement mappings, monitoring SLA/DR criteria and acceptance. No requirement is signed off by this documentation change.
