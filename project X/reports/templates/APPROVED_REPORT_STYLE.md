# Approved report layout — comparison reference

The user approved the styling and layout shown on 26 September 2026. Preserve
that approval as a comparison baseline, not as confirmation of live Power BI
rendering or data correctness.

Frozen reference:
`reports/client-deliverables/WMPP v16/_review/approved-baseline-2026-09-26/`

It contains both complete pre-revision report definitions/resources, the seven
approved PNG/SVG layout proofs, and the builder source at approval time. Do not
overwrite it when regenerating deliverables. No semantic-model data cache was
copied into this styling baseline.

## Keep stable

- 1680 × 945 canvas, 36 px outer margin, approximately 22 px panel gutters.
- Borderless page/section headings, Segoe UI, spacious icon scorecards.
- Four or five headline KPIs; focused lower panels, details on dedicated pages.
- 18 px rounded panels; no heavy chart borders or decorative clutter.
- WMPP business pages remain light; Mission Control remains dark green/charcoal.
- Native data-bound report visuals; no fake numbers inside deployable reports.

## Requested WMPP colour/effect revision

“Employees model” is assumed to mean the WMPP semantic-model attached report.
No separate employee project has been identified or changed.

Use the original v16 referral report's `#F8F1F4` canvas and `#EEDCE3` surface
family. Its shared theme supplies rose `#E96B7D`, ink `#2B2427`, muted
`#61575C`, pink `#F7BDC9` and supporting teal `#72AEB5`. Existing legacy
referral-series colours (`#CAFD3C`, `#FFEBBC`, `#EF7911`) remain on preserved
original visuals; do not reinterpret them as success/failure colours.

The revised new WMPP pages use frosted translucent white surfaces, soft rose/teal
background gradients and restrained shadows. SVG panel artwork approximates
glassmorphism; it does not perform browser-style live backdrop blur. Data labels
remain opaque and readable. Keep approved geometry unchanged for comparison.

## Mission Control interaction revision

- Calendar selection filters both right-panel views; **Day Gantt** is the default.
- **Day Gantt / Register** are display-only, selected-visual bookmarks. They must
  not restore/reset calendar or pipeline data selections.
- No selected day: choose-day guidance; multiple days: switch to Register or
  choose one day. A calendar click does not forcibly leave Register mode.
- Muted P25–P75 bands, a mean tick, status-coloured actual bars, and concentric
  translucent red circles around failed-job endpoints. Failure is also named in
  the row label/tooltip. No blinking animation.
- Reuse Deneb, already declared in the supplied Mission Control report. Its
  client version/tenant availability still needs checking; native registers are
  retained as fallback. Prefer Deneb 1.9+ for generated PBIR.

## Duration reference definition

Use the previous 30 days relative to **each displayed run/step's start time**.
Only previous, ended successful records qualify. A record must have started in
the lookback window and ended strictly before the current start; the current job
is excluded. Negative/missing durations and inverted timestamps are excluded.
Successful steps from failed parent jobs are excluded from the healthy baseline.

Match jobs by pipeline, steps by pipeline + notebook + sequence. Report sample
count, mean, median, inclusive P25 and P75. Require five samples to display a
band; below that report insufficient history. This small minimum is a display
guard, not a guarantee of stable estimates. Historical extremes are retained.
The comparison uses raw durations, not percentiles of averaged steps. Whole-job
quantiles are independent of step quantiles: sums would be misleading with
parallelism, retries, gaps and dependencies.

The statistical-analysis skill informed the mean/median pairing, IQR band and
sample-count disclosure. These are descriptive reference ranges, not confidence
intervals, SLAs, anomaly thresholds or predicted completion guarantees. Being
above P75 does not make a successful load failed. The cohort is intentionally
successful-run-only; it does not estimate failure-inclusive runtime. Changes in
volume, hardware, notebook versions or scheduling may reduce comparability.

History ignores the display date/job/status filters so the selected day does not
erase its baseline. RLS remains enforced by the model. Client refresh and DAX
execution remain acceptance checks; local renders use explicitly synthetic data.

References: [Deneb PBIR configuration](https://deneb.guide/docs/pbir-guide),
[Deneb cross-filtering](https://deneb.guide/docs/interactivity-selection),
[Power BI bookmark options](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-bookmarks).
