# WMPP & Mission Control — report design review

Prepared 26 September 2026. **Local review copies, not published or client-certified.**

## Approved-style and calendar revision

The approved pre-revision reports, previews and builder source are frozen in
`_review/approved-baseline-2026-09-26`. The comparison/style specification is
`project X/reports/templates/APPROVED_REPORT_STYLE.md`. The new WMPP pages retain
the approved layout but now use the original v16 rose/pink palette, translucent
frosted surfaces and soft shadows. “Employees model” was interpreted as WMPP;
no separately named employee project was changed.

The calendar's right panel defaults to **Day Gantt**. Select one day to see its
loads; use **Register** to switch back to the native table. The display-only
bookmarks preserve the chosen day/pipeline. In Register mode a day click filters
that register; it does not automatically change the user's chosen view mode.

The day, job and step timelines now use the Deneb visual already declared by
the supplied report. Failure endpoints have layered red halos plus text status.
The grey band is the prior successful-run P25–P75 duration range; the tick is
the mean. Tooltips include median and historical sample count. Steps match
pipeline + notebook + sequence; jobs match pipeline. Only runs ending before
the current start, with starts in the preceding 30 days, are included; at least
five samples are required. Whole-job quantiles are not sums of step quantiles.
Ranges are descriptive, not SLAs, forecasts or failure criteria. See the style
specification for exclusions, RLS/filter context and caveats.

`_review/chart-proofs` contains renders of the exact chart specifications using
**synthetic data only**. They verify chart compilation/appearance outside Power
BI, not client DAX values or interactive behaviour. The regenerated layout
proofs embed these illustrative charts. Deneb 1.9+ is recommended for generated
PBIR; client availability, refresh and bookmark behaviour still need Desktop
acceptance. Prior generated visuals replaced during iteration were moved into
`_review/superseded-generated-visuals` and remain recoverable.

## Open these projects

This bundle now lives at `reports/client-deliverables/WMPP v16`. The longer
`WMPP v16 - Report Design Review` folder name exceeded Desktop's file-path
limit and was shortened without changing project contents or relative links.
Keep the deployment parent path short: every project file must stay below
260 characters and every directory below 248 characters on the affected Desktop.

- `SM WMPP Mission Control v16/SM WMPP Mission Control.pbip`
- `SM WMPP v16 updated/SM_WMPP_v16.pbip`

Each PBIP opens the report attached to its local semantic model. Copy/zip the
**whole corresponding project folder**, including its `.Report` and
`.SemanticModel` folders. Do not deploy `_review`; that folder holds recoverable
original pages and clearly labelled layout proofs, not report assets.

The new category-aware KPI's internal name is `Category-aware open referrals`;
its visible card and metric-selector label remains **Open referrals**. The
original `_Measures[Open Referrals]` is unchanged. This avoids the model-wide,
case-insensitive name collision that prevented WMPP from opening.

The original `reports/current/WMPP v16.zip` and standalone RPT project were not
changed. Existing SQL endpoints, model roles, PBIP entrypoints and local report
bindings were preserved. Both original `.pbi/cache.abf` files are byte-for-byte
unchanged; cached data predates the new fields and is **not** evidence that the
new visuals have refreshed successfully.

Source ZIP SHA-256:
`abb563675523b91d04e083582bf48bcffd88d9b4d4cb173b2afa0e9abc971378`

## What changed

### Mission Control

- **Load Calendar:** compact dark 16:9 page, five KPIs, month/pipeline selectors,
  selectable calendar matrix and a run register. Green = successful loads,
  red = at least one failed job or failed step, amber = running/other outcomes,
  neutral = no loads. Text distinguishes states without relying only on colour.
- **Job & Step Timelines:** last 14 calendar days, searchable job selector,
  cross-filtering Deneb job/step Gantts with prior-duration bands, and native
  detail tables as a fallback when custom visuals are unavailable.
- **Quality & Schema:** four quality KPIs and two focused registers instead of a
  long wall of measures. Quality-result filters do not pretend to filter the
  independent schema inventory.
- **Archive & Replay:** four KPIs with ZIP and snapshot registers; their separate
  filter contexts are labelled. This is read-only reporting, not a replay button.
- Existing drillthrough and tooltip pages and the underlying measure catalogue
  are retained.

Calendar dates use `rpt_job_run_summary.started_at`: a job belongs to its start
day. No timezone conversion has been invented. `Load Calendar` and the existing
last-14-days column update when the model refreshes. The default month is
**This month** at refresh time. Select a single month; clearing the month selection
can combine dates into one week/weekday intersection and leave calendar cells blank.
Success rate excludes running/other outcomes; P95 duration uses ended runs with
non-negative recorded duration. Green intensity changes at ten successful runs.

### WMPP

- **Referral Geography:** city bubbles, framework/category filters and two field
  parameters: grouping (city, category, framework, urgency, placement type,
  status) and metric (referrals, open, awaiting offer, under offer, offers,
  completed IPAs).
- **Offer Locations:** searchable referral/provider selectors, offer-category
  filters, distance distribution, coverage/median KPIs and an offer/home register.
- **Referral Single View:** searchable person initials/ID and referral ID,
  preference-city map, offers/homes, provider referrals and IPA details.
- Board, supply, target, provider single view, snapshots (including the existing
  6/12-month selector), other business pages and existing referral drillthrough
  were retained. A legacy tooltip flag unsupported by its declared PBIR schema
  was removed in this delivery copy only.

Native text, cards, slicers, tables, charts, maps and navigation sit above local
SVG panel/icon artwork. No sample numbers were embedded in the reports. Icons
are project-authored line artwork; no claim is made that they are original
third-party/Lucide artwork. No new paid/custom visual was introduced.

## Location accuracy and privacy

The current Gold contract contains **preferred placement city**, not a child's
residential address. The map therefore represents referrals' recognised city
preferences, not exact child locations. Only `CITY_MATCH` locations are mapped;
defaulted, ambiguous and missing locations remain in the review KPI.

Distance is the ETL-provided **city-centroid to provider-home-postcode straight-line
estimate**, not driving distance. Median and coverage KPIs use only
`APPROXIMATE_PREFERENCE_CITY` rows with a numeric distance. Default-city estimates
are separate. Missing distances remain blank, never zero. The distance register
shows the source status, and distance bands retain unavailable/review rows.

Azure Maps receives city + `United Kingdom` location labels for geocoding, not
child names, person IDs or precise child addresses. Its availability depends on
the client's Power BI tenant and supported environment. No tenant/privacy setting
was changed. See [Microsoft's Azure Maps visual guidance](https://learn.microsoft.com/en-us/azure/azure-maps/power-bi-visual-get-started).

The model has initials and person IDs, not full child names. Full-name search is
therefore not claimed or fabricated.

## Category semantics

`Referral Category` is a disconnected selector. Category-aware measures use
`gold.bridge_referral_framework_category` and distinct referral IDs to respect
multi-category referral membership, existing referral filters and RLS. No
bidirectional relationships were added. Referrals can appear in several category
bars: **do not add those bars to derive the distinct total**. Uncategorised
referrals are included with no category filter, but not when a category is selected.

`Offer Category` filters the proposed offer's `framework_category_id`, not the
referral requirement or all categories registered against a provider home.
Provider-home category columns are imported for later analysis but are not
mislabelled as offer categories. Current category memberships do not filter the
historical snapshot page.

## Refresh prerequisites — important

The ZIP's model did not yet expose the location/category fields already defined
by the current repository's Gold notebooks. The delivery adds those bindings,
the referral/category bridge, two category roles and the field parameters.
It also aligns `fact_offer.home_id` with the current Gold column
`provider_home_id`, preserving the existing column lineage and relationship.

Before reviewing live values, the target client Lakehouse must expose the current
Gold outputs from `04_gold_model.py` / `05_gold_dimensions.py`, including:

- `gold.bridge_referral_framework_category` (`referral_id`, `framework_category_id`);
- referral location/match/default/review fields and framework category fields;
- offer `provider_home_id`, category, postcode, distance/basis/status fields.

Approved city/postcode reference data must be populated for ETL distances to be
available. A city can geocode in Azure Maps while its ETL distance is still blank;
those are separate services/data paths. Do not interpret that as a zero distance.

No source notebook, Lakehouse object, credential or client data was changed by
this delivery. Refresh requires normal authorised access to the existing client
source. The new imported fields/tables may be unavailable until that refresh;
offline opening/rendering of the modified models has not been verified.

## Verification and inspection

Completed locally:

- JSON parsing, visual field-reference and rebuilt-page bounds checks;
- report/model local binding and unchanged cache/entrypoint comparisons;
- PBIR JSON structure checked against Microsoft's public schemas;
- layout-only SVG/PNG proofs inspected for spacing and typography;
- new Python builder linted. No semantic-model/report pytest tests added or run.

**Power BI Desktop was not available to this agent.** Layout proofs are not
Power BI screenshots and contain illustrative calendar states, no client data.
They cannot prove native visual rendering, DAX evaluation, refresh, RLS or
cross-filter behaviour. These remain client-side acceptance checks:

1. Open each PBIP in a compatible Desktop release and refresh with client access.
2. Check a success-only day, a mixed success/failure day, a running day and a
   no-load day; reconcile against the job register. Confirm the source timezone.
3. Select a day and verify cards/register filter together. Clear it, switch month
   and pipeline, and check a six-week calendar month for clipping/scrollbars.
4. Select a job bar/table row and verify only its steps remain; check drillthrough.
   Switch Day Gantt/Register after choosing a calendar day: the day/pipeline
   filters must remain selected. Confirm no day / multiple-day empty guidance.
   Reconcile five historical observations against the mean, median and quartiles;
   confirm current/future/failed records do not enter the healthy baseline. Check
   insufficient-history rows, a failed run's halo and successful runs above P75.
5. Check map availability, circles and tooltips; verify default locations are
   excluded and no precise child data is geocoded.
6. Change both WMPP field parameters, then framework/category filters. Reconcile
   a multi-category referral and uncategorised total against the bridge/source.
7. Search one person/referral and verify its offers, provider assignments and IPAs.
   Inspect distance blanks, default estimates and median coverage separately.
8. Check existing snapshots, provider single view and RLS as the intended client
   viewer; confirm map/custom-visual tenant approval before deployment.

A reproducible builder is retained in `project X/tools/build_report_design_delivery.py`.
It only targets a dedicated directory beneath `reports/client-deliverables`.
Original replaced pages are in `_review/original-pages` for recovery/comparison.
