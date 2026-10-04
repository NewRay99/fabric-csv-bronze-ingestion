# Gold referral journey status

Updated 4 October 2026. Implemented in the active `project X/04_gold_model.py`
notebook source; deployment and execution in Fabric remain to be verified.
The semantic model and report files have not been modified for this change.

## Fields on gold.fact_referral

| Field | Meaning |
| --- | --- |
| `referral_status` | Original `silver.referral.referral_status`, unchanged, including casing and NULLs. Replaces the former source-status meaning of `current_status`. |
| `current_status` | Current referral journey label, materialised in Gold rather than calculated in DAX. |
| `current_status_order` | Integer 1–8, for stage selectors and sorting. |
| `current_status_rule_version` | `WMPP_REFERRAL_JOURNEY_V1`, identifying the classification rules. |

The grain remains one row per referral. Offer and IPA evidence is aggregated at
referral grain before joining, so a referral with several offers, assignments
or IPAs is not counted repeatedly.

## Stage values and precedence

Evaluate rules from the highest precedence down, not in numeric order:

| Sort order | current_status | Evidence |
| ---: | --- | --- |
| 7 | Closed / cancelled / withdrawn | Source status is closed, cancelled, canceled, withdrawn or completed. Overrides offer and IPA evidence. The label preserves the existing DAX grouping, including completed. |
| 6 | IPA signed | At least one active IPA has both provider and local-authority signatures on that same IPA. |
| 5 | IPA created | At least one active IPA exists, without qualifying for stage 6. |
| 4 | Offer accepted | At least one accepted, approved, selected or offer_successful offer. |
| 3 | Offers received | At least one pending, submitted, offered, offer_made, offer_pending, under_review, under review, awaiting, awaiting_decision or awaiting decision offer. |
| 8 | Needs review | No stronger evidence above, and an unrecognised/missing offer status or a blank/missing referral source status. |
| 2 | Provider search | At least one referral-provider assignment, without qualifying for the rules above. An assignment with a missing provider key still evidences search. |
| 1 | Referral created | Creation date exists, without qualifying for the rules above. |
| 8 | Needs review | Fallback if none of the conditions applies. |

Status comparisons ignore casing and surrounding spaces; the raw
`referral_status` does not change. This intentionally matches the existing
referral Journey stage/order calculation, not the provider journey.

An IPA with NULL `closed` is treated as active, matching the existing DAX.
NULL signature flags are not signatures. A closed signed IPA does not imply a
currently signed stage, and signatures on two different IPAs cannot be combined.
Draft or declined/rejected/withdrawn/closed/cancelled/canceled/offer_unsuccessful/
unsuccessful offers alone do not establish stage 3. Accepted or pending evidence
takes precedence over an unrelated unknown offer, as in the existing DAX.

These are current evidenced stages, not cumulative milestone counts or an audit
of every step ever reached. Assignment alone does not prove browsing, and IPA
creation/signature does not prove admission to a placement.

## Historical snapshots

`gold.fact_referral_snapshot.current_status` and
`gold.fact_referral_global_summary.current_status` retain their existing **source
status** meaning. This protects retained-month KPI counts and their existing
OPEN/UNDER_OFFER/CLOSED filters from silently changing meaning.

New snapshot writes additionally retain:

- `referral_status`: the raw source value.
- `journey_status`: the current fact's `current_status`.
- `journey_status_order`: the current fact's `current_status_order`.
- `journey_status_rule_version`: the current fact's rule version.

Only the active calendar month is replaced. Existing older months receive NULLs
for these new columns through additive Delta schema merging; their existing
source-status `current_status` stays intact. They are not backfilled with live
offer/IPA evidence. Historical journey reporting requires replaying the relevant
archive month through Silver and this Gold notebook. Do not treat unavailable
historic journey values as zero or "Referral created".

`AS_OF_DATE` excludes future-created referrals, assignments, offers and IPAs.
It does not reconstruct older offer/signature states from today's Silver data:
archive replay must load that month's Silver export first. The existing snapshot
population/KPI rule version remains `WMPP_SNAPSHOT_V2`; the journey calculation
has its own independent version column.

## Semantic model migration

Prepare these changes together before refreshing the model against the changed
Gold table. The existing import reads the entire table, so a refresh will change
the meaning of its current `current_status` binding even without a new query.

1. Import `referral_status`, `current_status_order` and
   `current_status_rule_version` from `gold.fact_referral`. Use `current_status`
   for journey labels and sort it by `current_status_order`.
2. Replace the existing DAX-calculated `Journey stage` and `Journey stage order`
   with source-backed columns mapped to `current_status` and
   `current_status_order`. Keeping the existing display names and lineage
   preserves report/selector references. Do not leave the old derivation running
   against the newly defined `current_status`.
3. Change **source-code** comparisons on `fact_referral[current_status]` to
   `fact_referral[referral_status]`. In the inspected WIP these occur in
   `_Measures` (under-offer, emergency/planned, cost and closure measures) and
   `_Explorer KPI Measures` (terminal-referral count). Journey-based displays and
   selectors should instead use the new stage fields. Do not blindly replace all
   status references, and leave snapshot source-status comparisons unchanged.
4. Point any source-status relationship/filter to `referral_status`.
   `gold.dim_referral_status` still contains source statuses, not journey labels;
   it must not be joined to the new journey `current_status`. Use a separate stage
   dimension if a journey relationship is needed.
5. Update table icon rules and labels to recognise the new journey values.
   Existing rules for UNDER_OFFER/OPEN/CLOSED do not recognise the new labels.
   This Gold change does not itself repair the native Power BI icon formatting.
6. For monthly journey visuals, import the separate snapshot `journey_status`
   fields, with explicit handling for older unavailable months.

Deploy the revised `04_gold_model.py` to Fabric and run it after the current
Silver business rules. Existing source requirements already cover all fields
needed; no new external lookup, package or source schema is required.

Before accepting the model migration, compare total referrals, open/under-offer
source counts, all eight journey counts, signed-IPA examples, terminal referrals
with offers/IPAs, explorer stage filtering and referral drillthrough. Check that
the stage counts reconcile to the same referral cohort and that historical source
KPI trends remain unchanged.

## Verification

The actual notebook referral SQL is executed against synthetic fixtures in
`tests/test_gold_referral_journey_status.py`, with SQLite adapting only Spark
date/timestamp syntax. Its 54 checks cover all stages, status aliases and raw
preservation, precedence, missing values, same-IPA signatures, row grain,
creation-date cutoffs and snapshot bindings. The full local suite passes
203 tests and 158 subtests. These are data-layer checks, not proof of Fabric/Delta
execution or Power BI rendering; those still require deployment validation.
