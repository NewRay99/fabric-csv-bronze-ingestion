# Sankey Reporting Guidance

## Reporting reassessment 30 September 2026

Distinguish the hidden/expandable referral-flow chart from the new journey strips. Referral journey counts assign one refreshed current stage; provider counts assign one furthest evidenced stage per provider in the current cohort. Neither strip is a time-to-stage or transition-conversion Sankey. Detail step clicks focus related event families; acceptance/signature are not explicit lifecycle event types.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


Use one board-level Sankey to explain the referral journey:

`Urgency → Offer availability → Match decision → Required-placement-date outcome`

Recommended terminal states:

- IPA issued by target
- IPA issued late
- Open on track
- Open overdue
- Closed without placement
- Withdrawn or cancelled

Useful explanatory fields include `PlacementUrgencyBand`, offer-count band, `DelayReason`, and `ReferralClosureReason`. Controlled values might include no provider response, no suitable home, location constraint, education constraint, sibling requirement, complex needs, funding approval, officer review delay, provider withdrawal, and changed circumstances.

Do not mix referral counts and offer counts. A single referral can generate many offers. Use `DISTINCTCOUNT(ReferralID)` for referral lifecycle flows and `COUNTROWS(FactOffer)` or distinct `OfferID` for provider/home analysis.
