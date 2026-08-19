# Page Blueprints

## 1. Executive Overview

- Header: title, refresh date, reporting period and urgency slicer.
- KPI row: New referrals; Open referrals; Placed by target; Critical overdue; IPAs issued; committed cost.
- Main left visual: 12-month created referrals vs IPAs issued by required date.
- Main right visual: open referrals by target status — On track, Due soon, Overdue.
- Lower row: target hit rate by urgency, referral-to-IPA funnel, board attention table.

## 2. Target & Urgency

- KPI row: target hit rate, overdue count, median days to IPA, critical overdue.
- Main visual: target hit rate by `PlacementUrgencyBand` with required-placement-date target line.
- Supporting visual: ageing bands for open referrals.
- Exception table: referral ID, urgency, required date, days overdue, last activity, barrier reason.
- Use conditional formatting plus text labels; never rely on red/green alone.

## 3. Provider Performance

- KPI row: unique providers responding, offer coverage, median offer review time, accepted offers.
- Main visual: offers, acceptance rate and placed-by-target rate by provider.
- Supporting visual: provider response time distribution.
- Detail table: provider, unique homes offered, offers, accepted, acceptance rate, target hit rate, median cost.
- Add a drill-through to home-level analysis only for authorised operational users.

## 4. Referral Journey / Sankey

- KPI row: referrals created, referrals with at least one offer, accepted match, IPAs issued, placed by target, overdue.
- Sankey flow: Urgency → Offer availability → Match decision → Required-placement-date outcome.
- Outcome nodes: IPA by target, IPA late, Open on track, Open overdue, Closed without placement.
- Add three narrative callouts with denominators and a visible “illustrative / synthetic” label in prototypes.
- Count distinct `ReferralID` at referral stages; use `OfferID` only for offer-level analysis.

## 5. Data Quality

- KPI row: completeness, valid target dates, duplicate referrals, orphan offers, stale open referrals.
- Main visual: quality score by field/table.
- Supporting visual: issue trend by month and severity.
- Detail table: issue type, affected records, owner, ageing, remediation status.
- Treat safeguarding/privacy issues as high-severity exceptions and keep case-level details restricted.
