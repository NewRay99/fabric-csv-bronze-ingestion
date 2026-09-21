# Provider engagement and value scoring implementation guide

## Purpose and boundary

This guide captures the provider-scoring design discussed in the ChatGPT Work
conversation **“Create Provider Scoring System”** and reconciles it to the
client-site `SM_WMPP_v16` package dated 20 September 2026.

The proposed output is a **provider engagement and value score** with separate
home and provider views. It can describe responsiveness, submission quality,
officer experience, handling of referral outcomes and comparable cost. It must
not be presented as a quality-of-care, safeguarding or placement-suitability
rating.

No composite score is currently approved or implemented. Component weights,
thresholds, exclusions and minimum sample sizes require business, procurement,
commissioning and Information Governance approval.

## Repository implementation candidate — 20 September 2026

The repository now implements the evidence layer that can be built without
inventing scoring policy:

- `gold.bridge_provider_home_framework_category` publishes the missing
  home/category bridge;
- `gold.fact_referral_provider` now retains `assigned_at`, offer/reason response
  timestamps, the first qualifying response, elapsed minutes and a rule label;
- `gold.fact_provider_kpi_monthly` publishes security-scope-aware, provider ×
  assignment-month component numerators and denominators;
- the semantic model exposes response rate, offer conversion, target placement
  rate and average response hours; and
- no overall score, ranking, weight or SLA pass/fail has been fabricated.

The response evidence scope is `OFFER_OR_RECORDED_REASON_V1`. Provider messages
remain excluded because `created_by` is not yet classified as provider,
officer or system. The monthly fact is an assignment-cohort view and carries
`security_scope_key` so provider KPIs are not accidentally exposed outside the
user's approved referral scope. Its offer component reads the validated
`gold.fact_offer[referral_provider_id]` assignment key. The Gold offer fact now
publishes that key explicitly and applies the as-of cut-off before the monthly
provider KPI is aggregated (GLD-016).

## Current implementation assessment

| Scoring need | Client-site evidence | Gap before scoring |
| --- | --- | --- |
| Provider and home identity | `dim_provider`, `dim_provider_home`, provider/home IDs on `fact_offer` | Referral assignments are provider-level. Do not attribute an unanswered provider referral to every home. |
| Referral response rate | `fact_referral_provider` has assignment and decline/cancel/closed flags plus `is_engaged` | Define a substantive response. `is_engaged` is a current status rule, not proof of a response event. |
| Response speed | `assigned_at` now uses `referral_provider.created_date` with export date only as a fallback; offer/reason evidence is retained | Business-calendar SLA, approved deadline and provider-message authorship are still unresolved. |
| Submission/document completeness | `dim_provider_submission_document` has type, home ID and validity dates | Required-document rules and denominators do not exist. The schema contract marks document `home_id` as `NO_JOIN`, while the semantic model actively joins it to home; the data owner must resolve this conflict. |
| Decline/closure handling | `dim_referral_provider_reject_reason` and `fact_offer[rejection_reason]` | No governed reason attribution says which outcomes are provider-attributable, neutral, authority-driven or unclassified. |
| Officer feedback/messages | `dim_referral_provider_message` has text, creator and timestamps | `created_by` is not classified as provider/officer/system and there is no structured officer rating. Message sentiment must not directly score a provider. |
| Comparable cost | Estimated weekly costs and the Gold home-to-framework-category bridge now exist | Offer category is not retained in `fact_offer`, and zero can currently represent missing fee components. |
| Historical score | A scoped monthly provider KPI component fact now exists | No approved composite score, score version, restatement policy or home/category score fact exists. |

## Required Gold objects

Build and validate the inputs before creating DAX for a composite score.

| Object | Minimum grain and purpose |
| --- | --- |
| `bridge_provider_home_framework_category` | One row per valid home/category/validity period, sourced from `provider_home_category`. |
| `fact_referral_provider` response fields | Implemented opportunity grain with assignment time, first qualifying offer/reason response, elapsed minutes and evidence rule. SLA deadline and evidence ID remain to add. |
| `dim_provider_response_reason_classification` | Business-owned mapping of decline/cancel/closure reason to neutral, provider-attributable, authority-attributable, capacity, needs mismatch or unclassified treatment. |
| `dim_provider_document_requirement` | Required document type by service/framework category and validity period. |
| `fact_provider_document_compliance` | Home/category/month requirement outcomes: required, supplied, valid, reviewed and exception reason. |
| `fact_placement_officer_feedback` | Structured review with provider/home attribution, rating dimensions, reviewer role, date and moderation status. Do not derive this directly from free text. |
| `fact_provider_cost_comparison` | Comparable offer/home/category/month rate, peer median, peer count, included-cost basis and comparability status. |
| `dim_provider_score_version` | Version, effective dates, approved weights, thresholds, exclusions and owner. |
| `fact_provider_home_score_monthly` | Home × framework category × reporting month × score version. Store component numerators, denominators, coverage, scores and evidence status. |
| `fact_provider_kpi_monthly` | Implemented provider × security scope × assignment month evidence components; not a score. |
| `fact_provider_score_monthly` | Future provider × framework category × reporting month × score version, recalculated from pooled evidence after approval. |

Retain source evidence identifiers and the as-of cut-off used for every monthly
score. A corrected source record may trigger an explicitly versioned
restatement; it must not silently rewrite a published historical ranking.

## Response definition

A qualifying response may be an offer, a reasoned decline or a provider-
authored substantive message. Automated acknowledgements and officer-authored
messages do not count.

Implement these timestamps in Gold:

```text
opportunity_started_at = actual referral-provider assignment/creation time
first_qualifying_response_at = earliest approved provider response event
response_due_at = SLA deadline after urgency and business-calendar rules
response_minutes = qualifying business minutes between start and response
responded_in_sla = response exists and response time <= due time
```

An opportunity still within its deadline is pending, not a failure. An overdue
unanswered opportunity is a non-response. Archive export dates are evidence
cut-offs, not response timestamps.

## Proposed pilot components

These weights came from the mobile discussion and remain an unapproved pilot:

| Component | Proposed weight | Score basis |
| --- | ---: | --- |
| Referral response rate | 20% | Qualifying responses / eligible opportunities |
| Response speed | 15% | In-SLA responses, supported by median and 90th-percentile response time |
| Submission/document completeness | 15% | Valid required documents / required documents |
| Placement-officer feedback | 25% | Moderated structured ratings, with review coverage shown |
| Decline/closure handling | 10% | Timely, documented, appropriately classified handling; not raw decline volume |
| Cost competitiveness | 15% | Like-for-like cost position within framework category and service cohort |

The pilot formula is:

```text
overall score =
    0.20 × response
  + 0.15 × speed
  + 0.15 × completeness
  + 0.25 × feedback
  + 0.10 × handling
  + 0.15 × cost
```

Do not convert a missing component to zero. Apply a governed “insufficient
evidence” result when an essential component or minimum denominator is absent.
Publish the component coverage beside every score.

## Home and provider aggregation

Produce these views:

| View | Grain | Use |
| --- | --- | --- |
| Home score | Home × framework category × month × version | Assess a service in its comparable category. |
| Provider/category score | Provider × framework category × month × version | Compare providers delivering similar services. |
| Provider overall | Provider × month × version | Portfolio summary with category mix, lowest home and spread visible. |

Recalculate provider components from pooled numerators and denominators. Do not
take a simple average of home percentages. If one home responds to 8 of 10
opportunities and another to 45 of 90, the provider result is 53/100 = 53%,
not the average of 80% and 50%.

Attribute evidence at the lowest grain supported by the source:

- provider-level referrals and feedback stay provider-level unless a home is
  explicitly identified;
- home documents stay home-level only after the `home_id` contract is approved;
- costs stay offer/home/category-level and use comparable service cohorts; and
- centrally handled provider activity must not be duplicated across homes.

## Component rules

### Documents

Score completeness, not upload count. A home with all five required and valid
documents must outperform a home with fifteen files that omits a mandatory
document. Separate missing source extraction from genuine provider omission.

### Decline and closure reasons

Business owners must classify every reason. Needs mismatch, no vacancy,
authority withdrawal and planned endings should not automatically harm a
provider score. A confirmed provider withdrawal or service failure can be
adverse only after attribution and review. Prevent the same incident being
penalised again through handling, feedback and response components.

### Messages and feedback

Classify `created_by` to provider, placement officer, system or unknown before
using messages as response evidence. Keep message text restricted under RLS.
Free-text classification may identify records for human review, but raw
sentiment must not directly alter a score: negative wording may describe a
child's circumstances rather than provider performance.

### Cost

Compare equivalent services within framework category, placement/service type,
support intensity, geography, urgency and pricing period. Standardise the fee
unit and treatment of extras. Distinguish missing cost from a genuine zero.
Show the home cost, peer median, percentage difference and peer sample size;
return “insufficient comparable data” for a small or non-comparable cohort.
A low cost must not outweigh suitability or a serious service concern.

## Power BI model

Calculate governed components and monthly scores in Gold. Power BI should
present them rather than reconstructing the scoring algorithm from raw events.

Recommended relationships are single-direction dimensions to monthly score
facts. Use `dim_provider`, `dim_provider_home`, `dim_framework_category`,
`dim_snapshot_month` and `dim_provider_score_version`. Keep message text and
case-level drill-through on the secured detail path described in
[RLS and partial aggregate access guide](RLS_AND_PARTIAL_AGGREGATE_ACCESS_GUIDE.md).

Display at least:

- overall and component scores;
- numerators, denominators and evidence coverage;
- score version and as-of month;
- peer group and peer sample size;
- six-month trend;
- lowest-scoring home and home-score spread; and
- “insufficient evidence”, “under review” or “disputed” status.

## Delivery sequence

1. Confirm real referral-assignment timestamp and response-event taxonomy.
2. Classify message authors and automate only evidence extraction, not scoring
   sentiment.
3. Validate the implemented home/category bridge against refreshed Gold data.
4. Resolve document `home_id` ownership and define required-document rules.
5. Approve reason attribution, comparable-cost rules and structured feedback.
6. Build versioned Gold evidence and monthly score facts.
7. Run sensitivity analysis on weights and minimum samples.
8. Pilot with a limited period and a human dispute/review process.
9. Approve RLS, message-text access and aggregate disclosure controls.
10. Publish only after reconciliation, fairness review and business UAT.

## Acceptance criteria

- Every component is reproducible from versioned evidence and a documented
  denominator.
- No provider/home is penalised for missing extraction data.
- Provider totals use pooled evidence and do not duplicate home activity.
- Score comparisons use compatible framework/service cohorts.
- Historical scores retain their as-of month and score version.
- Sensitive feedback/message text is not exposed by aggregate score access.
- The dashboard never labels the composite as quality of care or suitability.
