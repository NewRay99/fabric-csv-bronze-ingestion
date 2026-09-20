# Snapshot Month-on-Month KPI guide

## Decision

Use `gold.fact_referral_snapshot` for Month-on-Month comparisons of referral
**state**. Continue to use event facts for activity that occurred **during** a
month.

This distinction prevents a historical chart from recalculating old months
using today's referral status. It also prevents the current active
`dim_date[date]` to `fact_referral[referral_created_date]` relationship from
turning an “open last month” card into “currently open referrals that were
created last month”.

## Client-site status — 20 September 2026

The reviewed `SM_WMPP_v16` model already imports
`fact_referral_snapshot`. It contains one referral row per snapshot with
`snapshot_date`, status, offer, IPA, overdue, provider-assignment and target
fields. The Gold notebook replaces the active calendar-month slice on rerun,
which is consistent with keeping one effective snapshot per month.

The semantic implementation is not yet suitable for governed monthly trends:

- `dim_date` actively filters `fact_referral[referral_created_date]`;
- its relationship to `fact_referral_snapshot[snapshot_date]` is inactive;
- current and snapshot facts are joined directly and bidirectionally by
  `referral_id`;
- snapshot dates are not guaranteed to be the same day number each month;
- no `snapshot_month_start` key is present;
- the current snapshot does not retain enough provider-engagement detail to
  reproduce `Active Referral Engagement Rate` historically; and
- the legacy MoM family is calculated from current `fact_referral` state.

## Repository implementation candidate — 20 September 2026

The repository now contains a reconciled candidate at
`reports/current/SM WMPP v16 updated` plus repeatable transformation tooling at
`tools/reconcile_semantic_model_v16.py`. It is not yet the client-deployed
model. The candidate:

- adds `snapshot_month_start`, `snapshot_month_end` and
  `snapshot_rule_version` to the physical snapshot contract;
- adds conservative response evidence fields `has_provider_response`,
  `provider_responded_count` and `first_provider_response_date`;
- adds and actively relates `dim_snapshot_month`;
- removes the current-referral-to-snapshot relationship and all general
  bidirectional relationships;
- disables Auto date/time and removes the generated date tables;
- moves the legacy stock/variance stacks to snapshot-backed measures; and
- repairs the known report field bindings and compatibility aliases.

The response flag currently means evidence of an offer or a recorded
decline/cancel reason after assignment. Messages are excluded until their
authors can be classified reliably. This rule is recorded as
`WMPP_SNAPSHOT_V2`; it is deliberately narrower than an ungoverned
“engagement” label.

Existing retained snapshot rows receive deterministic month keys and the rule
label `LEGACY_PRE_V2`; their response fields remain null. Response-rate DAX
uses only rows with non-null response evidence and therefore returns blank,
not a misleading zero, for a wholly legacy month.

## KPI classification

Classify every KPI before changing DAX.

| Question | Type | Correct source |
| --- | --- | --- |
| How many referrals were open at the September snapshot? | Stock/state | `fact_referral_snapshot` |
| How many referrals were under offer at the September snapshot? | Stock/state | `fact_referral_snapshot` |
| How many new referrals arrived during September? | Flow/event | `fact_referral[referral_created_date]` |
| How many referrals closed during September? | Flow/event | A closure event or `referral_closed_date` |
| Of referrals created in September, how many have ever received an offer? | Cohort outcome | `fact_referral` plus an explicit outcome cut-off |
| What percentage of the open September caseload had provider engagement then? | Stock/state | Snapshot, after adding engagement-at-snapshot fields |

Do not mix stock and flow measures under the same generic label. For example,
use “Closed referrals at snapshot” for cumulative closed state and “Referrals
closed during month” for closure flow.

## Gold changes

The repository implementation adds these physical fields to
`gold.fact_referral_snapshot`:

| Field | Rule |
| --- | --- |
| `snapshot_month_start` | First day of `snapshot_date`'s calendar month. |
| `snapshot_month_end` | Calendar month end; useful for labels and quality checks. |
| `has_provider_response` | True where an offer or recorded decline/cancel reason provides response evidence after assignment. It is not inferred from assignment alone. |
| `provider_responded_count` | Number of referral-provider opportunities with that qualifying response evidence. |
| `first_provider_response_date` | Earliest qualifying response timestamp for the referral. |
| `snapshot_rule_version` | Version of the status/engagement derivation used for reproducibility. |

Retain exactly one effective snapshot per referral and month. For closed
months, the effective date should be the agreed month-end export. For the open
month, a latest-live snapshot is acceptable only when visuals label it as
“month to date”. If a month has no snapshot, return blank and show a data-
quality warning; do not silently compare with an older month.

Quality tests must prove:

1. uniqueness of `(snapshot_month_start, referral_id)`;
2. one physical `snapshot_date` per `snapshot_month_start`, unless an explicit
   intramonth design replaces this contract;
3. no future-dated events are reflected in an historical snapshot;
4. closed-period snapshots are not changed by a live-pipeline rerun;
5. snapshot counts reconcile to the archive replay for the same as-of date;
6. every status/engagement rule version is retained; and
7. required conformed dimension keys are non-null or mapped to a governed
   Unknown member.

## Semantic-model relationships

Create a one-row-per-month `dim_snapshot_month` and an active, single-direction
relationship:

```text
dim_snapshot_month[month_start]
    1 ─────── * fact_referral_snapshot[snapshot_month_start]
```

Keep `dim_date` for event dates. Remove the direct current-fact-to-snapshot-
fact relationship. Relate the snapshot directly to conformed dimensions such
as person and placement type. This keeps a creation-date filter from leaking
into as-of measures.

Disable Power BI Auto date/time and remove the generated `LocalDateTable_*`
objects. The client-site model currently has 87 of them, which obscures which
date role a visual is using.

## Base snapshot measures

The page or visual must supply one snapshot month. If no month is selected,
the following pattern deliberately uses the latest available month.

```DAX
Selected Snapshot Month =
COALESCE (
    SELECTEDVALUE ( 'dim_snapshot_month'[month_start] ),
    CALCULATE (
        MAX ( 'fact_referral_snapshot'[snapshot_month_start] ),
        REMOVEFILTERS ()
    )
)

Snapshot Referrals As Of =
VAR snapshot_month = [Selected Snapshot Month]
RETURN
CALCULATE (
    DISTINCTCOUNT ( 'fact_referral_snapshot'[referral_id] ),
    REMOVEFILTERS ( 'dim_snapshot_month' ),
    TREATAS ( { snapshot_month }, 'dim_snapshot_month'[month_start] )
)

Open Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals As Of],
    KEEPFILTERS ( 'fact_referral_snapshot'[is_open] = TRUE () )
)

Closed Referrals at Snapshot =
CALCULATE (
    [Snapshot Referrals As Of],
    KEEPFILTERS ( 'fact_referral_snapshot'[is_open] = FALSE () )
)

Referrals With an Offer at Snapshot =
CALCULATE (
    [Snapshot Referrals As Of],
    KEEPFILTERS ( 'fact_referral_snapshot'[has_offer] = TRUE () )
)

Referrals Awaiting Offer at Snapshot =
CALCULATE (
    [Snapshot Referrals As Of],
    KEEPFILTERS ( 'fact_referral_snapshot'[is_awaiting_offer] = TRUE () )
)

Referrals Under Offer at Snapshot =
CALCULATE (
    [Snapshot Referrals As Of],
    KEEPFILTERS ( 'fact_referral_snapshot'[is_open] = TRUE () ),
    KEEPFILTERS ( 'fact_referral_snapshot'[current_status] = "UNDER_OFFER" )
)

Active Provider Response Rate at Snapshot =
DIVIDE (
    CALCULATE (
        [Snapshot Referrals As Of],
        KEEPFILTERS ( 'fact_referral_snapshot'[is_open] = TRUE () ),
        KEEPFILTERS ( 'fact_referral_snapshot'[has_provider_response] = TRUE () )
    ),
    [Open Referrals at Snapshot]
)
```

Do not substitute `provider_assignment_count > 0`; an assignment is not proof
of provider response. Extend the qualifying evidence only after the event
taxonomy and message authorship rules are approved and version the change.

## Previous-month and variance pattern

Use the exact preceding calendar month. This makes a missing monthly snapshot
visible as blank instead of silently comparing September with July.

```DAX
Open Referrals at Snapshot Previous Month =
VAR previous_month = EDATE ( [Selected Snapshot Month], -1 )
RETURN
CALCULATE (
    [Open Referrals at Snapshot],
    REMOVEFILTERS ( 'dim_snapshot_month' ),
    TREATAS ( { previous_month }, 'dim_snapshot_month'[month_start] )
)

Open Referrals at Snapshot Variance =
[Open Referrals at Snapshot] - [Open Referrals at Snapshot Previous Month]

Open Referrals at Snapshot MoM % =
DIVIDE (
    [Open Referrals at Snapshot Variance],
    [Open Referrals at Snapshot Previous Month]
)

Open Referrals at Snapshot Variance Indicator =
VAR variance = [Open Referrals at Snapshot Variance]
RETURN IF ( ISBLANK ( variance ), BLANK (), IF ( variance > 0, "▲", IF ( variance < 0, "▼", "–" ) ) )

Open Referrals at Snapshot Variance Indicator Color =
VAR variance = [Open Referrals at Snapshot Variance]
RETURN IF ( ISBLANK ( variance ), "grey", IF ( variance > 0, "green", IF ( variance < 0, "red", "grey" ) ) )
```

Repeat this five-measure stack for approved snapshot bases. Directional colour
is a business rule, not a universal rule: more open/overdue referrals may be
adverse, while a higher placement rate may be favourable. Store the preferred
direction in the KPI catalogue rather than assuming every increase is green.

## Flow measures that remain event-based

Keep these on their event facts and label them explicitly:

- referrals created during month;
- offers submitted during month;
- IPAs issued during month;
- placements started or ended during month; and
- referrals closed during month.

The event date must be the date named by the KPI. Do not reuse referral
creation date for offer, IPA or closure flows.

## Report migration

1. Add a visible snapshot-month slicer or a clearly displayed “As at” label.
2. The repository candidate restores `_Measures[Open Referral Previous Month]`
   as a snapshot-backed compatibility measure; verify all 34 dependent
   references visually in Desktop.
3. Keep cohort measures on separate visuals with labels such as “referrals
   created in month”.
4. Hide or remove legacy creation-date state stacks after dependent visuals
   have moved.
5. Test latest month, a prior closed month, a missing month and a zero-
   denominator month.
6. Reconcile card values to direct Gold queries for at least three months.

## Acceptance criteria

- Selecting September returns the state stored for September, unaffected by
  a referral's status in October.
- Previous month always means the exact prior calendar month.
- Missing snapshot months are obvious and do not produce a misleading trend.
- All stock cards display the effective snapshot date and rule version.
- Event and cohort visuals state their date basis in the title or tooltip.
- No snapshot measure depends on the current `fact_referral` table or a
  bidirectional fact-to-fact relationship.
