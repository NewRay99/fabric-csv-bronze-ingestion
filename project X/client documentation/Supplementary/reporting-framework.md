# Foster Referral Reporting Framework

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
