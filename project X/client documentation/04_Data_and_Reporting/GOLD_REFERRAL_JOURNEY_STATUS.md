# Gold referral status and journey stages

Updated 6 October 2026. Keep the original referral source status and the overall
journey stage as separate fields. Gold calculates the journey once per referral;
Power BI imports the result instead of independently classifying the referral
in DAX. This supersedes both the 4 October status replacement and the earlier
6 October full journey rollback.

## Field definitions

| Object and field | Meaning |
| --- | --- |
| `gold.fact_referral.current_status` | Original `silver.referral.referral_status`, preserving casing, whitespace and NULLs. |
| `gold.fact_referral.journey_stage` | Derived overall journey label at the Gold as-of date. |
| `gold.fact_referral.journey_stage_order` | Integer 1–8 for sorting and journey filters, not an additive measure. |
| `gold.fact_referral_snapshot` | Copies all three fields for the active reporting month. |
| `gold.fact_referral_global_summary.current_status` | Source-status grouping, unchanged. |

There is no additional Gold `referral_status`, `current_status_order` or
`current_status_rule_version` output. Silver's source column is unchanged.
Offer statuses and IPA signatures remain in their own detailed facts; the
lifecycle-event table remains a timestamp-derived activity history, not a
source-system audit log.

For example, a source status of `UNDER_OFFER` can coexist with journey stage
`IPA signed`. Neither field replaces the other. One referral may have several
offers with different statuses, but it has one overall journey stage.

## Journey rules

| Order | Label | Evidence |
| --- | --- | --- |
| 1 | Referral created | Creation date exists, with no higher-priority evidence. |
| 2 | Provider search | Provider assignment exists; drafts and terminal offers alone do not advance this stage. |
| 3 | Offers received | At least one pending or submitted offer. |
| 4 | Offer accepted | At least one accepted, approved, selected or successful offer. |
| 5 | IPA created | At least one active IPA, without both signatures on the same IPA. |
| 6 | IPA signed | Both provider and local-authority signatures on the same active IPA. |
| 7 | Closed / cancelled / withdrawn | Terminal source status: closed, cancelled, canceled, withdrawn or completed. This overrides milestones. |
| 8 | Needs review | Missing source status or an unrecognised offer status, without stronger milestone evidence. |

Evaluation precedence is 7, 6, 5, 4, 3, 8, 2, 1. Journey comparisons normalise
case and whitespace without changing the published source value. A closed IPA
does not count as an active agreement. Signatures on separate IPAs cannot be
combined. An IPA signed stage is not proof that admission occurred.

Offer and IPA evidence is aggregated to referral grain before joining, so
multiple offers, assignments or IPAs do not multiply referral rows. Referrals
without offers remain in the population. Future-dated creations are excluded
using the notebook's as-of date. Historical runs must use the corresponding
Silver export; these checks do not reconstruct past status/signature changes
from today's source records.

The existing source-status required-placement-date outcome rules, provider
response metrics, category links, coordinates, detailed facts and registry
extracts are unchanged.

## Saved WIP model

The updated project is `project X/reports/WIP/SM WMPP v16 updated WIP`.

| Semantic table | Existing field name | Gold source column |
| --- | --- | --- |
| `fact_referral` | `Journey stage` | `journey_stage` |
| `fact_referral` | `Journey stage order` | `journey_stage_order` |
| `fact_referral_snapshot` | `Journey stage` | `journey_stage` |
| `fact_referral_snapshot` | `Journey stage order` | `journey_stage_order` |

The current-referral fields retain their names, lineage identifiers and sort
relationship. Existing journey measures, click-to-filter bookmarks and detail
navigation continue to reference those same fields. Source-status filters and
icons still use `current_status`. No report page, visual layout, relationship,
role, icon asset or report ZIP is changed by this migration.

The two previous semantic files are backed up under
`reports/WIP/_review/source-journey-split-20261006-085714`.

## Deployment sequence

1. Preserve any unsaved Power BI work separately. Do not save an older open
   session over the edited project definitions.
2. Import and run the revised `04_gold_model.py` in the development Fabric
   workspace attached to `LH_BCT_WMPP`, with current Silver business-rule
   outputs available. Do this before refreshing the updated model.
3. Verify one row per referral and all three columns through the SQL endpoint.
   Check a referral without offers, a pending offer, an accepted offer, an active
   signed IPA, a closed referral, and missing/unrecognised evidence. Compare
   `current_status` directly with the latest Silver source value.
4. Once the endpoint exposes the new columns, open/reload the saved WIP and
   refresh the model. Verify the Referral Explorer stage counts reconcile to
   the matching referral population, stage clicks filter the directory, and
   Referral Detail shows the selected referral's overall stage.
5. Check source-status counts and snapshot trends separately. Models manually
   migrated to the earlier GLD-022 raw `referral_status` alias must rebind to
   `current_status`; their journey fields should import the new stage columns.

Local file changes do not deploy a Lakehouse, refresh cached data or publish a
report. Fabric/Delta execution and Power BI rendering remain deployment checks.

## Retained snapshots

Only the active month is replaced. New writes include source status and journey
stage separately, while the existing snapshot rule stays `WMPP_SNAPSHOT_V2`.
Older months are not relabelled from live evidence. Additive schema merging
leaves their new stage fields NULL until the corresponding historical exports
are replayed. NULL means unavailable history, not stage 1 or zero referrals.

If the earlier GLD-022 version ran in Fabric, extra physical snapshot columns
may remain. The current projection does not use them; do not drop historic
columns or copy old classifications into the new fields automatically.

## Verification

The portable SQL checks execute the actual notebook query with synthetic data.
They cover raw status preservation, all eight journey stages, alias/precedence
rules, same-IPA signatures, closed-IPAs, referral grain, as-of cutoffs and the
monthly snapshot projection. SQLite adapts Spark date/timestamp syntax; it does
not execute Fabric or the Power BI engine.

Local validation passed 85 focused source-status/journey SQL checks and the full
suite of 279 tests plus 158 subtests. Notebook syntax/schema and test lint checks
passed. Model bindings and retained journey identifiers were checked; hashes
confirmed all 2,536 report-definition files, 74 unrelated model files and the
user's modified report ZIP were unchanged.

Semantic definitions are Git-ignored in this repository. Retain the edited WIP
folder and its backup with the delivery; a commit of the notebook alone does
not carry these semantic changes.
