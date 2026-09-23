# WMPP reference-design revision — 23 September 2026

Status: **implemented in both report copies; final Power BI visual acceptance is
not complete**. Do not describe schema validation or SVG previews as proof that
the Power BI render matches the supplied images.

Icon sourcing follow-up: see the [implementation guide](../../reports/templates/ICON_IMPLEMENTATION_GUIDE.md)
and [client provenance register](../06_Governance/ICON_RESOURCE_REGISTER.md).
These record six official-source replacement candidates, not verified originals
from the reference images. Sourcing documentation does not mean the current
inline artwork has been replaced or approved.

## What changed

The three `end goal` PNGs were inspected directly. Their common composition is
now implemented on Board Dashboard, Provider & Placement Supply, and Target &
Urgency Performance:

- 1680 × 945 canvases, with the same compact header, score strip and 3 × 2 grid.
- One rounded white scorecard strip with six outlined icons, live KPI values,
  dark labels, understated explanatory captions and fine separators.
- Borderless page/panel headings. All report textboxes explicitly disable
  backgrounds, borders and shadows, rather than inheriting the old boxed theme.
- White panel surfaces, subtle shadows, coral/orange/pale-coral chart accents,
  and teal/amber/coral target-status colours.
- Header navigation buttons to the three dashboards and compact native filters.
- Seventeen native chart/matrix panels with corresponding live data tables;
  34 display-only bookmarks switch each panel without restoring filter values.
- Target page's pale-coral required-date banner, with the **implemented** urgency
  thresholds. No unapproved 14-day planned target has been invented.
- The report opens on Board Dashboard; the three reference pages are first in
  page order, followed by Referral Snapshots. The other pages are retained.

The assets `wmpp-reference-board.svg`, `wmpp-reference-supply.svg` and
`wmpp-reference-target.svg` contain interface chrome, labels and icons only.
They do not contain fake KPI numbers or charts. All values, charts, matrices,
tables and slicers remain native Power BI visuals over the existing model.
Static page decoration is composed as a background image visual; consequently
decorative text is edited through the generator, not as separate PBI textboxes.
Native visuals retain accessible descriptions and buttons retain action tooltips.

## Data differences from the illustrations

The illustrations are design references, not source data. July 2026, provider
names, values and last-month comparisons have not been hard-coded. Weekly cost
is labelled weekly; the model does not provide a lifetime placement-cost total.
Region mapping remains explicitly unavailable. The county breakdown remains a
properly labelled chart instead of a fabricated regional map. Escalations are
unavailable, not zero. Review and shortlist funnel stages remain blank where
there is no reliable event history. Native Power BI bars may differ from the
rounded/gradient illustration geometry; no exact native-render equivalence is
claimed without Desktop inspection.

## Files and maintenance

Local entry point: `reports/current/SM WMPP v16 updated/SM_WMPP_v16.pbip`.
Client-connected copy: `reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.pbip`.
The definition and static-resource files are identical between the attached
local report and the client report. Their own connections and report identities
are preserved. Both have 16 pages and 315 visuals, including hidden table views.

Rebuild the design with:

```powershell
python "project X/tools/redesign_wmpp_reference_style.py"
```

The old version-specific Power BI test scripts have been removed. Resolve the
actual current client project paths before any rebuild; acceptance is a separate
review, not part of the Python/ETL test suite.

`apply_wmpp_end_goal_design.py` now delegates to the revised layout after it has
been installed, so it cannot silently bring back the rejected boxed layout.
The common theme includes `WMPP Reference Clean`, with explicit removal of
both container borders and internal card margins/backgrounds. Do not reassign
the historical boxed presets to these reference visuals.

Recovery copies of the previous report definitions/resources and theme audit
are in `reports/retired/2026-09-23-reference-design-revision/`. No semantic model,
measure, source data, client connection or report page was deleted.

## Verified here

- Authored SVG chrome was rendered and visually inspected against the PNGs.
  `reports/templates/reference-layout-*.png` are **chrome-only layout previews**:
  they intentionally omit the native cards/charts and are not PBI screenshots.
- Eighteen icon-scorecard slots, borderless headings, bounds, navigation targets,
  34 selected-visual/display-only bookmark definitions and opening page pass.
- All report field bindings resolve; snapshot 6/12-month controls and referral/
  provider single-view and drill-through checks pass.
- Both report copies match, and the active model's 53 files remain byte-identical.
- Schema validation covers all report definitions, pages, visuals and bookmarks.
  The existing Requirements Complete card (`0aef383ced90ab2d5c70`) remains a
  schema exception in both copies; it was not redesigned or silently removed.

## Required before design sign-off

Power BI Desktop is not available to this session. The Windows Computer Use
skill was loaded and installed-app discovery found no accessible Power BI
Desktop target. Browser skills do not provide an offline Desktop renderer.

Open the local PBIP and inspect all three reference pages. Supply screenshots
at Fit to page for a final comparison and adjustment pass. Specifically check
the new card values for left alignment/clipping, chart labels and colour rules,
table/chart switching in both directions without slicer reset, SVG text/shadow
rendering, and page navigation. The display-only bookmark structure passes
schema checks but has not been exercised in a running Power BI report here.

**Final design approval remains outstanding.** Client connection, refresh,
publication and deployment remain after user check-in/acceptance as previously
requested. Do not replace missing client access with fabricated live data.
