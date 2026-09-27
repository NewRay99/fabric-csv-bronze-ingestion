# Approved report layout — comparison reference

The user approved the styling and layout shown on 26 September 2026. Preserve
that approval as a comparison baseline, not as confirmation of live Power BI
rendering or data correctness.

Current delivery override (27 September 2026): at the user's request, the seven
rebuilt pages no longer show the composite background skin (glass panels,
shadows and baked-in icons). They use plain native page colours. Generated
visuals override inherited outer padding to zero and slicer item padding to 2
to address clipped titles/filters. Keep this approved reference unchanged as
a historical comparison; `_review/pre-plain` also preserves the pre-removal pages.
Semantic models and cached data are unchanged. Desktop text rendering still
needs visual confirmation; layout previews are illustrative only.

Theme compatibility repair (27 September 2026): the standalone BCT/Lato theme
was rolled back to the v0 layout-compatible palette, typography and 110 named
presets. The standalone theme omitted styles still referenced by 254 visuals.
The corrected shared template is `assets/brand-pack/WMPP_Theme.json`; the exact
original `WMPP_Theme_v0.json` remains unchanged. Zero outer text/filter padding
and compact slicer item padding are retained. The additional `WMPP Compact KPI`
preset removes inherited outer margins from the generated 50px callout cards.
This repair does not constitute a complete BCT-brand restyle. Both delivery
reports use identical corrected theme files. Native Desktop appearance remains
to be confirmed because screen capture timed out. Before-repair theme and
report definitions are recoverable under `_review/theme-repair-20260927-121933`.

Board Dashboard annotations (27 September 2026): its previously skin-embedded
heading, KPI labels/captions and six chart headings/descriptions are now native
editable textboxes. Thirteen `i` buttons expose explanatory action tooltips and
open the hidden `Board Dashboard - guide` page, which has a return button.
Existing chart/table and page-navigation controls have visible native labels.
The background SVG remains hidden. Chart queries, bookmark/navigation actions
and semantic-model definitions are unchanged. Tooltips and rendering still
require Desktop visual acceptance; file-schema and target-link checks passed.

Frozen reference:
`reports/client-deliverables/WMPP v16/_review/approved-baseline-2026-09-26/`

It contains both complete pre-revision report definitions/resources, the seven
approved PNG/SVG layout proofs, and the builder source at approval time. Do not
overwrite it when regenerating deliverables. No semantic-model data cache was
copied into this styling baseline.

## Current native annotation standard — 27 September 2026

Soft card glow is retained: "no skins" means no composite background artwork,
not removal of panel shadows. Use editable rounded white panels on the warm
canvas, with a rose-grey `#B78D98` shadow, 80% transparency, 14px blur and 4px
downward offset. Mission Control uses its dark panel fill and a black shadow
at 70% transparency. Native shapes carry the shadow behind composite KPI strips
and chart/title groups; do not shadow each inner number, icon or heading.
Standalone data visuals use the same soft container shadow. The theme exposes
`WMPP Soft Glow` visual presets and a `WMPP Soft Panel` shape preset. Headings
remain borderless and the original page background skins remain hidden.

For standalone card/chart containers, keep the visual border enabled with a
14px radius and a 1px line matching the panel fill. Do not disable this container
setting to hide the outline: retain the rounded corners using a matching colour.
Composite native panels keep their existing 18px shape rounding. This corner
treatment does not change chart padding, shadows, data or layout.

Standalone charts and tables use **16px left/right and 12px top/bottom container
padding**, including their native headings and subtitles. Explicit zero-padding
on these outer containers must not override the chart presets. Transparent child
charts inside a separately drawn panel retain their existing geometric inset;
do not double-pad them. This also applies to the legacy named chart presets in
the shared theme. Card callouts, textboxes, filters and report-page headings are
not resized by this chart-spacing rule.

The current light canvas and template wallpaper colour is **`#F8F5F1`** (warm
off-white), replacing `#F8F1F4`. This applies to existing light delivery pages,
guides/tooltips and future pages created with `WMPP_Theme.json`. Mission Control's
dark page backgrounds remain `#101713`; chart palettes and KPI accent colours
are unchanged. The v0 theme and historical comparison assets remain untouched.

This supersedes the decorative-skin instructions below for the delivery projects.
Both reports use plain page colours and editable, borderless Segoe UI annotations;
no composite background skins are visible. Provider & Placement Supply and Target
& Urgency Performance have native page headings, six KPI labels/captions, six
chart explanations and clickable Lucide information icons. Referral Snapshots
has native chart/register explanations without changing its 6/12-month filters.

Apply the common typography, padding and border treatment across all existing
pages, including helper/tooltips. Other business/operational pages have a native
“How to read this page” footer and a hidden explanatory guide. The footer uses
52 pixels of extra canvas below the existing content, preserving chart/filter
positions; the two snapshot panels reserve space within their existing bounds
for native annotations. Board retains its established guide controls.

Lucide source SVGs, ink/light variants, full licence and a pinned-revision source
manifest are saved **beside each PBIP in its project root**, with resource copies
embedded in each report. Catalogue: https://lucide.dev/icons/. Source revision:
`66d8f9fc394b8530377e5f6112f0b8908ba01280`. Only stroke colours are changed.
No API key is needed. Keep the licence/provenance files in the client delivery.

Recoverable before-edit definitions/resources are under
`_review/native-style-20260927-124938`. Semantic models, original ZIP, saved data
queries, filters, bookmark actions and drillthrough bindings are unchanged.
Do not treat older layout previews as renders of this revision. Native Desktop
appearance and interactions still require inspection; schema validation does
not substitute for that visual acceptance.

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

## WMPP navigation assembly

The client-deliverable WMPP report is trialling original-style circular navigation
across 16 main pages. Referrals, Offers, Providers and Performance reveal dropdowns
under the buttons; Home, Draft offers, IPAs and Requirements are direct links.
Preserve full captions, the active-area highlight and capitalised original page
names. Retain original REFERRALS and REFERRAL SINGLE VIEW separately from the newer
geography and referral explorer pages. Dropdown bookmarks affect only menu visuals,
with Data disabled. Navigation does not pass a selected record: keep drillthrough
and destination search controls available.

Open dropdowns use a connected white surround behind both the circular trigger
and submenu panel. Keep 12 pixels of panel padding outside the submenu rows,
rounded outside corners and a subtle rose-grey shadow. The yellow outline in the
user's reference is annotation only, never a palette choice. The surround is made
from editable native shapes, shown/hidden with its own dropdown bookmark; do not
change the main buttons into rectangular tabs or add a full-page background skin.

Preserve the original branded header placement where it exists. Elsewhere, keep
the dedicated navigation band to avoid covering headings while menus are closed.
Move only root visual containers; group child coordinates are relative. No
full-page skin is needed. Explicitly enable native action-button text at visual
level as well as defining its state-specific labels. Desktop label rendering and
interaction acceptance remain outstanding; schema validation alone is not enough.
Existing whole-page builders must not be rerun over the final navigation assembly
without adapting their offsets and group handling. See `REPORT_NAVIGATION.md` in
the delivery for the restoration audit, menu behaviour and backups.

## WMPP coral palette — 27 September 2026

Use `assets/brand-pack/WMPP_Brand_Pack.md` for the current reporting extension.
The primary navigation colour is `#FB6540`, with white Lucide icons,
lighter coral `#F98165` hover and no button outline. Keep charcoal captions below
the circles. White text on primary coral is insufficient for small labels. Preserve circular
main buttons, white dropdown surrounds, `#F8F5F1` canvas, rounded panels and the
existing soft card glow. Saved button overrides must be updated along with the
theme; a theme import alone does not replace their old rose fills.

The master theme, both template copies and the WMPP delivery's embedded theme
now share the new palette. Existing presets, theme colour indices and typography
are retained. This is a WMPP colour change, not a reskin of dark Mission Control.
Reference-inspired urgency/status colours are documented separately from client
identity colours; they are not a claim of formal BCT brand approval.

## Mission Control interaction revision

WMPP-only KPI icon follow-up: use the transparent, coloured Lucide strokes in
`assets/brand-pack/icons/LUCIDE_KPI_ICONS.md` on cards and matching guide headings.
Do not add pink/coloured discs behind KPI pictograms. The owner explicitly
retains the small information badges and their pale backgrounds. Keep white
navigation icons, coral circle fills and borderless navigation unchanged.

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
# Current colour authority — 27 September 2026

The exclusive 24-colour list in `assets/brand-pack/WMPP_Palette.json` and
`WMPP_Brand_Pack.md` supersedes historical palette guidance below. Use only those
authored colours in WMPP. No automatic theme shades or continuous chart colour
gradients. Preserve the smaller transparent KPI icons and pale information
badges; the badges now use approved Soft Amber and Charcoal. Logos/raster
artwork and historical originals are exempt; Mission Control is separate.
