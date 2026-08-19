# Sankey Reporting Guidance

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
