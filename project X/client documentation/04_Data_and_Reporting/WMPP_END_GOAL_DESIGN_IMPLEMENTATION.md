# WMPP end-goal report implementation — 23 September 2026

## Reference-style correction

The initial boxed implementation described below was superseded after design
feedback. See `WMPP_REFERENCE_DESIGN_REVIEW.md` for the icon-led score strips,
borderless headings, compact reference layouts, live chart/table switching and
verification limits. Both report copies now contain 16 pages / 315 visuals.
Final Power BI rendered comparison and acceptance are still outstanding.

## Initial KPI implementation record

The candidate is `reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report`.
For local review without the client-hosted report connection, open
`reports/current/SM WMPP v16 updated/SM_WMPP_v16.pbip`. On 23 September 2026
all report definition files, pages, bookmarks and resources were copied into
its attached report, preserving the local semantic-model binding. The older
`reports/current/SM WMPP v16` extraction is now in `reports/retired/`.
Three new pages implement the KPI layouts in the supplied `end goal 1.png`,
`end goal 2.png` and `end goal 3.png`. Existing pages remain available; the
report now has 16 pages, including hidden pages and a new snapshot page.

## Design mapping

| Design / report page | Implemented content | Definition or source difference |
| --- | --- | --- |
| End goal 2 / Board Dashboard | Referral volume, open referrals, target hit rate, critical overdue, median days to IPA, estimated active weekly cost; urgency volume, target rate, target status, outcome mix, provider offers versus accepted | Cost is labelled weekly, matching the existing measure. Outcome mix uses recorded statuses. Region panel states that Gold region is null. |
| End goal 1 / Provider & Placement Supply | Providers making offers, offers received, acceptance, offers per referral with an offer, distinct homes, median offered weekly cost; provider volumes, accepted offers, median first-offer time, county distribution, placement mix and evidenced offer-to-IPA stages | Active-provider label is narrowed to providers making offers. County is labelled county. Reviewed and shortlisted stages remain blank without reliable history. |
| End goal 3 / Target & Urgency Performance | Due in the data-as-of month, due within three days, overdue, critical hit rate, average days early; required-date trend, created-month cohort hit rate by urgency, target-day bands, urgency/status matrix, open age and cohort observation windows | Escalated cases are explicitly unavailable. Required-date trend uses the inactive required-date relationship via `USERELATIONSHIP`. |
| Referral Snapshots | Monthly total/open/awaiting-offer/under-offer/closed-or-cancelled trend and detail table | Uses retained `fact_referral_snapshot` state and `dim_snapshot_month[month_start]`. |

Board and Supply pages have referral-created-period and urgency slicers. The
Target page has urgency filtering; its required-date trend is not restricted
by referral-created-month selection. Canonical measures are reused where
their meaning matches. Screenshot values and July 2026 dates are not report
data. Previous-month comparison annotations are not hard-coded: the separate
snapshot page provides actual month-end state comparisons.

## Snapshot x-axis

The visible **X-axis window** dropdown offers **Last 6 months** and **Last 12
months**, with 12 selected by default. The window ends at the latest available
snapshot month in the current access and placement-type context, displayed
above the graph. September 2026 would give April–September 2026 for six months
or October 2025–September 2026 for twelve months, inclusive. Missing source
months remain gaps; months after the anchor are excluded.

`Snapshot Window` is disconnected. `[Snapshot Month In Window]` uses
`EDATE(anchor, 1 - months)` and is applied as a visual-level `= 1` filter to
both the graph and detail table. Both sort `month_start` ascending. The anchor
removes snapshot-calendar context while retaining other filters and RLS.

## Calculation choices

The local model adds six disconnected control/axis tables and
`_Design Measures`, an Import measure container with 18 measures. The 258
canonical measures are preserved, with no duplicate names added.

- Due soon: known required date zero to three calendar days after the row's
  `as_of_date`. Overdue: required date before that date. Missing dates retain
  a **No target** category. Due this month uses the data-as-of month.
- Open-age bands: 0–2, 3–7, 8–14, 15–28 and 29+ days, plus unknown.
- Days early: calendar days between IPA issue and required date, for referrals
  classified as placed by target.
- Provider first-offer response: earliest submitted offer per referral within
  the provider filter, then median elapsed days from referral creation.
- Cohort windows: 1/3/7/14 days from creation to IPA issue. Only referrals old
  enough to complete each window enter that window's denominator. Different
  windows have different eligible cohorts, so rates need not be monotonic.
- Acceptance retains the existing decided-offers denominator. Offers per
  referral retains the existing referrals-with-an-offer denominator.

## Verification

Rebuild: `python "project X/tools/apply_wmpp_end_goal_design.py"`.
The former version-specific acceptance script has been removed. Resolve the
current client project paths before rebuilding; report acceptance is reviewed
separately and is not part of the Python/ETL test suite.

Completed: 61 generated page/visual definitions passed Microsoft's PBIR
schemas; every report field and supporting DAX column reference resolves;
new visual rectangles fit their canvases without overlaps; the saved window
choices, filters, sorting, interactions and client/local bindings pass checks.
The existing WMPP enhancement and model-reconciliation validators also pass.
The model now has 45 tables. These are static checks, not DAX execution or
Power BI Desktop rendering against client data.

## What's outstanding

1. Open `WMPP_DASHBOARD_v16.Report/definition-local.pbir`, refresh the local
   model and exercise all four pages in Desktop: both windows, year boundaries,
   missing months, no-data selections, card clipping, chart labels and RLS.
2. Confirm cohort definitions, weekly cost and denominator choices with the
   business owner. Add prior-month KPI-strip comparisons only with agreed
   period/cohort semantics.
3. Supply governed referral/home regions and actual escalation, review and
   shortlist events. Gold currently sets `region` to null and derives
   `offer_reviewed_date` from `last_modified_date`, which is not review proof.
4. **After the user reviews and checks in the repository work**, deploy the
   additional model tables/measures to the client semantic model and test the
   preserved client-connected report. The existing `definition.pbir` does not
   deploy local model changes; an older client model can show missing-field
   errors. Resolve this during the already-deferred final client connection,
   refresh and publish task.

References: Microsoft's [PBIR project format](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-report)
and [disconnected tables for slicer input](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-relationships-understand).
