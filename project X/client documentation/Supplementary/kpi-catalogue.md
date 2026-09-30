# Board KPI Catalogue

## Reporting reassessment 30 September 2026

The current Dashboard Legend has 144 curated measure entries, including 35 newly catalogued WIP measures for demographics/signatures, snapshot change, closure flow, journey stages, provider components and location coverage. The full model has 366 measures including helpers. Estimates, derived activity and current-cohort stages retain their limits; new requirement mappings await owner approval.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


The active Gold v02 definitions and DAX expressions are in
[Measures Comparison Checklist](Measures_Comparison_Checklist.md).
Use `RequiredPlacementDateOutcome` and `PlacedByRequiredDate` from
`gold.fact_referral` for target reporting rather than recreating target logic
against `Fact Placement`.

## Headline KPIs

| KPI | Definition |
|---|---|
| New referrals | Distinct referrals created in the selected period |
| Open referrals | Referrals open at the selected as-of date |
| Placed by target | Percentage of completed placements with IPA issued on or before `RequiredPlacementDate` |
| Critical overdue | Open Critical referrals beyond `RequiredPlacementDate` |
| IPAs issued | IPAs issued during the period, regardless of referral cohort |
| Median days to IPA | Median days from referral creation to IPA issuance |
| Estimated committed cost | Accepted-offer or placement cost only; never sum every offer |

## Supporting measures

- Referrals created month-to-date versus same-day prior month.
- Open referrals by age band: 0–2, 3–7, 8–14, 15–28, and 29+ days.
- Percentage receiving at least one offer.
- Percentage receiving first offer within SLA.
- Median days to first action, first offer, accepted offer, and IPA.
- Placement outcomes: matched, withdrawn, cancelled, no suitable placement, and transferred.
- Target hit rate by urgency band.
- Overdue referrals by delay/barrier reason.

## Board interpretation

Use throughput measures for work completed in the period and cohort measures for the experience of referrals created in a period. Do not divide IPAs issued this month by referrals created this month and call it a conversion rate; the cohorts are not aligned.
