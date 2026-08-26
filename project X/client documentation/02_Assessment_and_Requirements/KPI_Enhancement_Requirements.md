# Referral and placement KPI enhancements

## Purpose

The reporting model must expose reusable referral, offer, IPA-signature and
provider-document indicators so placement teams can measure responsiveness,
matching progress and due-diligence readiness at a reporting snapshot.

## Implemented analytical fields

| Gold field | Definition | Source limitation / rule |
|---|---|---|
| `CntOfferMade` | Distinct offers linked to the referral. | Defaults to zero. |
| `FirstOfferDate` | Earliest linked offer date. | Cannot predate referral creation. |
| `FirstProviderSeenDate` | Earliest export date on a referral-provider row. | This is first observed provider assignment, not a provider UI-view timestamp; the source does not deliver one. |
| `IsNotSeenByProviders` | No referral-provider row exists for the referral. | A true value means no provider assignment was delivered. |
| `IPAPlacementAdmissionDate` | Earliest IPA placement-admission date for the referral. | Cannot predate referral creation. |
| `IPA2Signatures` | At least one linked IPA has source status `SIGNED`. | `SIGNED` is the supplied indication that both bodies have completed signing. |
| `IPALastSignatureDate` | Latest of local-authority signature, provider signature and can-sign dates across linked IPAs. | Null when no signature timestamps are delivered. |
| `IPADueDiligenceMinReviewDate` | Earliest `provider_submission_docs.next_review_date` linked through the IPA offer/home and later than admission. | Null when no eligible delivered document exists. |
| `ResponseRequiredDate` | Delivered referral response target date. | Retained separately from the required placement date. |
| `PlacedByRequiredDate` | IPA issue date exists on or before the delivered required placement date. | Null target dates are excluded from a target-hit denominator. |
| `RequiredPlacementDateOutcome` | Target outcome: placed by target, placed after target, open overdue, open on track or closed without placement. | Derived as at the Gold `AsOfDate`; it is not a source status. |
| `DaysToFirstAction` / `DaysToFirstOffer` / `DaysToIPA` | Derived duration from referral creation to the stated event. | Null when the event has not been delivered. |
| `DaysPastRequiredDate` / `DaysWithoutActivity` | Target overrun and inactivity age as at the Gold `AsOfDate`. | Use only for open referral escalation. |

## Layering and snapshot policy

The calculations are held in `silver.referral_enrichment`, a one-row-per-
referral derived relation. `gold.fact_referral` exposes them using business
names, and `gold.fact_referral_snapshot` includes them for point-in-time
reporting. The raw `silver.referral` contract is not changed because it remains
the source-conformed replayable relation.

All referral-grain calculations, including offer count, unique homes offered,
estimated weekly IPA cost and lifecycle dates, are calculated once in this
Silver relation. Gold projects these fields and does not repeat offer or IPA
rollups for the referral fact. The separate Offer and Placement facts still
retain their own source grain by design.

### Derived-date lineage

The following dates are calculated in `03_silver_business_rules.ipynb` and
stored in `silver.referral_enrichment`; `04_gold_model.ipynb` only promotes
them to `gold.fact_referral` and `gold.fact_referral_snapshot`.

| Gold field | Silver derivation |
|---|---|
| `FirstActionDate` | Earliest delivered action after referral creation: referral modification, offer submission/update, IPA creation/update, or IPA admission. The creation event is deliberately excluded. |
| `OfferAcceptedDate` | Earliest offer update/date for statuses `accepted`, `approved`, `selected`, or `offer_successful`. |
| `IPAIssuedDate` | Earliest linked IPA `created_datetime`. |
| `ReferralClosedDate` | For a delivered terminal referral status, its modification timestamp, falling back to export timestamp. The source has no dedicated close timestamp. |
| `LastActivityDate` | Latest delivered referral, offer or IPA timestamp. |

Every live or archive run replaces the snapshot rows for the active calendar
month with its latest extract. It therefore retains one current-month snapshot
instead of a separate row set for every daily archive export.

## Gold fact coverage

The analytics layer now exposes the following source-grain facts in addition to
the referral fact and its snapshot:

- `gold.fact_offer`: one row per offer, including referral, provider and home
  keys, submitted/reviewed/decision dates, status, proposed start, weekly cost
  and delivered rejection reason.
- `gold.fact_placement`: one row per IPA, including referral, IPA offer,
  issuance, admission, supplied status, closure and estimated weekly cost.
- `gold.fact_referral_provider`: one row per provider assignment, including
  supplied exclusion/decline/cancellation/closure flags.

The notebook also publishes `gold.vw_kpi_referral_board_summary`,
`gold.vw_kpi_referral_monthly` and `gold.vw_provider_offer_performance` for
board, monthly and provider comparison visuals. The detailed field rules and
DAX measures are in the active Gold v02 measure library in
[KPI Reference Guide](../04_Data_and_Reporting/KPI_Reference_Guide.md).

Where the source does not provide actual placement dates, actual cost, duration,
end reason, region or complexity classification, the Gold views expose a
nullable field. This keeps the published table shape stable and makes the data
gap visible without inventing a business value.

## Quality controls

The configuration-driven DQ suite checks the enrichment key, offer-count
presence and non-negativity, provider-observation flag, and the applicable
chronological rules. Values that cannot be supported by the delivered source
remain null rather than being fabricated.

It also records warnings, rather than blocking a run, when IPA admission is
before IPA issue, an IPA signature is before issue or after the planned
admission date, an accepted offer predates the first offer, or an admitted
placement has no eligible due-diligence review date. Derived-field DQ runs only
after the current `silver.referral_enrichment` table is written, so it never
validates a prior run's enrichment state.

## Reporting outcomes

These fields support KPI views for offer responsiveness, referrals with no
provider assignment, IPA completion/signing, and provider document review
readiness. They support requirements for referral status visibility, IPA
signing/auditability, provider due-diligence, and accurate commissioner
reporting (R24, R35, R47–R49, R51–R54 and R69).

### Confirmed-placement cost KPI

The active Gold v02 measure library adds `Average Estimated Weekly Cost —
Confirmed Referrals` for R51 and R62. It averages the referral-level delivered
`EstimatedWeeklyCost` for referrals with an issued IPA (`IPAIssuedDate` is not
blank). This is suitable for placement value analysis and finance reporting;
it is explicitly an estimate, not an actual cost, payment or invoice value.
The copy-ready DAX and the full active-measure requirement mapping are held in
[KPI Reference Guide](../04_Data_and_Reporting/KPI_Reference_Guide.md).
