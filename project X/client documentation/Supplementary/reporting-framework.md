# Foster Referral Reporting Framework

## Reporting reassessment 30 September 2026

The current WIP implements the separation of creation flow, month-end snapshot state and closure-date flow. Overall Performance hosts the snapshot comparisons; the standalone snapshot page is hidden. Referral stages are current state at refresh, and provider stages are current-cohort evidence. Preserve these population distinctions and keep priority/urgency separately until approved.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


## Lifecycle separation

Treat referrals as demand and placements as outcomes. Do not use estimated placement duration or estimated placement end as a referral end date.

## Recommended dates

| Field | Meaning | Reporting use |
|---|---|---|
| `ReferralCreatedDate` | Referral entered the system | Demand trend |
| `RequiredPlacementDate` | Date placement is needed | Target and urgency |
| `FirstActionDate` | First meaningful team action | Responsiveness |
| `FirstOfferDate` | First provider offer received | Supply response |
| `OfferAcceptedDate` | Preferred offer selected | Matching throughput |
| `IPAIssuedDate` | Formal assignment issued | Confirmed placement |
| `ReferralClosedDate` | Referral process ended | Completion |
| `ReferralClosureReason` | Why it ended | Outcome mix |
| `LastActivityDate` | Most recent activity | Stalled cases |

Placement dates such as planned start, actual start, planned end, actual end, cost, and duration belong in the placement/IPA fact table.

## Suggested model

- `FactReferral`: one row per referral.
- `FactOffer`: one row per provider-home offer.
- `FactPlacement`: one row per accepted placement/IPA.
- `FactReferralStatusHistory`: one row per status interval.
- `FactReferralSnapshot`: daily or month-end point-in-time workload.
- `DimDate`: conformed calendar dimension.

## Point-in-time rule

Created-date counts answer “how many arrived?”. Snapshot or status-history counts answer “how many were open at month end?”. These are different measures and should be labelled separately.

## Urgency field

Add a controlled field such as `PlacementUrgencyBand` with values `Critical`, `High`, `Medium`, and `Planned`. It should influence default target intervals and escalation windows, but the stored `RequiredPlacementDate` remains the formal target. Criticality should be agreed by safeguarding and placement leads, not inferred from free text.
