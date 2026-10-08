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

The source-status/journey migration below is the 6 October change. The separate
7 October identifier migration is documented at the end of this guide.

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

## Source person reference and multiple referrals (7 October 2026)

Use `source_reference_id` (the actual source spelling) as the user-facing person
reference. It originates on `silver.referral_person` and is published as text
on `gold.dim_person`; leading zeros are retained. It is not a unique referral
identifier. Relationships, distinct referral counts and RLS still use UUIDs.

| Referral fact field | Meaning |
| --- | --- |
| `source_reference_id` | Latest eligible source reference for the referral's selected person. Surrounding spaces removed, blank becomes NULL; display case preserved. |
| `has_multiple_referrals` | True when more than one as-of fact referral shares the same nonblank reference, including closed referrals. Case-insensitive comparison. |
| `source_reference_referral_count` | Number of those referrals, not source-person/history/offer rows. Zero when reference is missing. |
| `order_dupe` | Sequence starting at 1 within a reference, earliest referral creation first, UUID ascending for tied timestamps. Missing-reference referrals have a separate stable sequence for navigation but are not duplicate people. |

Source-person history versions are ranked by export/load timestamps before
joining. Future exports are excluded from historical as-of reference selection.
For multi-person referrals, the existing lowest-person-ID selection is retained;
the fact is not exploded into one row per person. No referral is deleted or
merged. Repeated references may reflect legitimate repeat referrals or reused
codes; review the underlying records before deciding they are data errors.

The count and flag describe the Gold as-of population, not the current report
selection. Report filtering does not renumber referrals or hide the flag when
only one sibling referral is selected. These annotations can indicate another
referral exists outside a restricted viewer's scope; approve that diagnostic
disclosure for intended audiences. They do not grant access to other rows.
Sequence values can change after an earlier creation/correction is loaded;
they must not replace the persistent UUID in external integrations.

New `fact_referral_snapshot` writes copy all four fields at that month's as-of
date. Retained old months remain NULL until replay of the corresponding export;
do not copy today's references, flag, count or sequence into historic rows.

### Report usage and deployment

The saved project is `reports/WIP/SM WMPP v16 updated WIP`. Thirteen tables use
Source reference, Referral sequence and Multiple referrals instead of the UUID.
All six referral-identifier searches now use source references; selecting a
reference can intentionally show several referrals. Select a specific directory
row to drill through. Referral Detail has compound filters on the canonical
fact reference plus sequence, preserving separate rows for duplicate references.
This follows [Microsoft's multiple-field drillthrough guidance](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-drillthrough).
Visual positions/sizes, existing colours/icons, UUID relationships, counts,
status logic, bookmarks and security roles remain unchanged.

1. Preserve unsaved Desktop work separately; do not save an older open session
   over the edited project definitions.
2. Deploy/run the revised root `04_gold_model.py` and `05_gold_dimensions.py`
   against the development Lakehouse. The live runner already uses that order.
3. Check the SQL endpoint exposes the new fact/snapshot/person columns. Compare
   the total/distinct referral UUID counts with the prior population. Check a
   singleton reference, repeated reference, tied creation time and missing ref.
4. Reopen the saved WIP and refresh its model only after the endpoint is ready.
   Search a duplicate reference; confirm separate sequence rows, then select
   each row and use View referral details/right-click Drill through. Verify
   only the intended UUID's offers, messages, IPAs and journey appear. Repeat
   with a blank reference. Check both ordinary viewer and restricted RLS users.
5. Check unchanged headline counts and that extra table columns scroll without
   covering adjacent visuals. Native rendering/drillthrough and Spark/Delta
   acceptance remain pending; local file checks do not establish publication.

Local verification: 358 tests and 158 subtests pass, including 29 new portable
source-reference/migration checks; schema/dimension validators pass. All 27
changed visuals retain positions/sizes; all 2,704 unlisted WIP files are
hash-identical (excluding `.pbi`). The migration preview is idempotent.
All 32 touched WIP files are backed up under
`reports/WIP/_review/source-reference-identifiers-20261007-734c16`.
