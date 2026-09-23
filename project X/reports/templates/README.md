# WMPP common report theme

`WMPP_Common_Theme.json` is the reusable Power BI **report theme**, not a PBIT
with a semantic model or credentials. It is the central editable source for
the current WMPP report projects. No semantic-model schema or DAX is changed.

Icon sourcing and future implementation are documented in the
[icon implementation guide](ICON_IMPLEMENTATION_GUIDE.md), with official source
links and licence/provenance evidence in the
[client audit register](../../client%20documentation/06_Governance/ICON_RESOURCE_REGISTER.md).
The six candidates are not verified originals and have not yet replaced the
inline artwork. SVG assets are separate from the theme JSON.

## Latest design revision

The three leading WMPP dashboards now use the image-reference design and the
`WMPP Reference Clean` preset. The common theme now has 110 presets; 554
historical visual assignments remain in the migration manifest, while the new
reference visuals select their clean presets directly. The generator owns the
three SVG interface assets and mirrors both report copies. Chrome-only PNG
previews in this folder are not Power BI renders. See
`client documentation/04_Data_and_Reporting/WMPP_REFERENCE_DESIGN_REVIEW.md` for
the update and the still-outstanding rendered acceptance.

The older counts and migration notes below document the original theme capture.

## Captured design

The main source is `reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report`.
Compatible styles from the other current reports are included as variants so
that Mission Control and the existing layouts keep their purposeful differences.

- Coral `#FC6547`, pastel pink `#E96B7D`, teal `#72AEB5`, dark text
  `#2B2427` / `#202124`, white cards, and the light dashboard canvas `#F7F8FA`.
- Segoe UI / Segoe UI Semibold typography; KPI values, labels and headings.
- Borders, rounded corners, padding, shadows, headers, slicers, buttons,
  chart formatting, table/matrix styling and supported state-specific settings.
- 97 deduplicated, type-specific named presets, selected by 698 active saved visuals
  after the local-report consolidation (810 at the original five-report rollout).
  Preset names contain stable style identifiers; the manifest maps each preset
  to its report/page/visual. A shared preset change affects every assigned visual.
- The existing palette ordering is preserved because `ThemeDataColor` references
  use numeric indices. Newly encountered colours are appended, not reordered.
  The 504-colour palette includes the original extended palette, not 504 new
  recommended categorical series colours.

Default card/column-chart/slicer styling comes from the new Board Dashboard.
Existing special variants select their named presets rather than being flattened
to one style. The five original built-in Minimal table/matrix selections are
superseded by their captured common-theme presets, intentionally adopting the
common table defaults for previously inherited formatting.

## Applied current projects

1. `current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report`
2. `current/SM WMPP v16 updated/SM_WMPP_v16.Report`
3. `current/SM WMPP Mission Control v16/SM WMPP Mission Control.Report`
4. `current/WMPP/SM_WMPP.Report`

The retired `current/SM WMPP v16` tree was moved to
`retired/2026-09-23-local-report-consolidation/SM WMPP v16` and is excluded from
active theme sync. The latest local project is **SM WMPP v16 updated**; its
attached report now has all 16 pages from the RPT dashboard. The pre-copy report
and theme manifest are recoverable in the same retirement archive.

Source ZIPs and `reports/client-deliverables` are unchanged. Previous theme
resource files are retained, but each report registers only one active custom
theme. The shared theme is copied byte-for-byte into each report's registered
resources using a content-hash filename to avoid stale theme caching.

## Maintain and reuse

1. Edit `WMPP_Common_Theme.json`. Use `visualStyles.<type>.*` for defaults or a
   named preset for an existing visual family. Do not rename a used preset
   without also updating its manifest assignment.
2. From the repository root run:

   ```powershell
   python "project X/tools/sync_wmpp_report_theme.py"
   ```

3. Resolve the current client project paths before running the sync script;
   historical v16 paths may no longer exist. The old report test scripts have
   been removed. Reopen the reports in Power BI Desktop and check representative
   pages, hover/selected button states, tables, slicers and tooltips.
4. On an additional/new report, import the common JSON as a custom report theme.
   Applying it sets defaults; existing explicit formatting can still override
   the theme. Review that report before removing its overrides. The sync script
   deliberately targets only the four projects above.

Run the sync command after any report-page generator. Captured inline values
reintroduced by those generators are moved back to the shared preset; later
different local overrides are preserved. Newly created visual IDs require an
explicit mapping review. `--capture` is a one-time bootstrap and is blocked
after rollout to avoid accidentally overwriting the maintained common theme.

`WMPP_Common_Theme.manifest.json` is migration/audit metadata, **not** a second
importable Power BI theme. It records original values, assignments, 21 rich-text
style variants, 11 page-background variants and safety fingerprints. It contains
no row-level report data. The initial migration check also supports `--baseline`
to compare captured values against their original appearance. That comparison
is intentionally not required after an approved theme design change.

## Deliberately report-local

Themes cannot safely replace every PBIR property. Rich-text content and its
inline text-run styles, page-specific backgrounds, logos/SVGs, field/series
selectors, conditional formatting and unsupported/custom-visual settings remain
local. Navigation actions, tooltip destinations, slicer state, axis ranges,
queries, filters, layouts and interactions are preserved. Their static colours
are included in the palette where applicable; this does not make artwork or
custom-visual formatting centrally editable through a Power BI theme.

## Verification and outstanding acceptance

Completed 2026-09-23: identical active theme copies across all four reports;
all 97 presets resolve; 698 visual assignments; 841 non-style JSON safety
fingerprints and 165 active model/connection file hashes checked. The prior
five-project migration audit is retained in the retirement archive. Re-running sync
updates zero visual files. Existing WMPP bindings, referral/provider detail,
6/12-month snapshot and Mission Control job/step checks pass.

The common theme passes Microsoft's `reportThemeSchema-2.154.json`. PBIR file
validation is a static check, not proof of rendering or data access.

Re-run the official-schema check with
`& "project X/tools/validate_wmpp_theme_schemas.ps1"` from PowerShell at the
repository root. It fetches the public Microsoft schemas once, bundles their
references in memory and validates the saved files. It currently exits with
code 1 for the known card exception below; it does not silently waive failures.

Before consolidation, the 816-file schema sweep passed the theme, all five report definitions and
809 of the 810 changed visual definitions. One existing `Requirements Complete`
card on page `b95eb4c0b53cd8c60710`, visual `0aef383ced90ab2d5c70`, does not pass
the published PBIR schema. Both the untouched ZIP version and an in-memory
reconstruction of its pre-theme formatting also fail validation. Its non-style
safety fingerprint is unchanged. Investigate/re-save this existing card in
Desktop; it was not silently removed or rebuilt during a theme-only update.
The unchanged card was also copied into the local model's report when all pages
were transferred, so the same exception now exists in both report copies.

Outstanding: open/reopen in Power BI Desktop, check the visual appearance and
named presets (particularly tables formerly using Minimal), and obtain user
acceptance; resolve the existing Requirements Complete card schema exception.
No Desktop rendering, refresh, client connection or publication is
claimed here. Keep client-environment reconnection/deployment as the final
workstatement after the user has checked in and accepted the other work.

References: [Microsoft custom theme and preset documentation](https://learn.microsoft.com/en-us/power-bi/create-reports/report-themes-create-custom)
and [Microsoft PBIR theme/preset selection reference](https://github.com/microsoft/skills-for-fabric/blob/main/skills/powerbi-report-authoring/references/theming.md).
