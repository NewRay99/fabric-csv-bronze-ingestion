# WMPP Power BI brand pack

Updated 28 September 2026. This is the current WMPP reporting style, selected by the project owner. It is not a claim of formal approval of a new Birmingham Children's Trust corporate identity.

## Approved palette — exclusive for report formatting

Use only the following 26 colours for authored WMPP report formatting. The machine-readable source is [WMPP_Palette.json](WMPP_Palette.json); the Power BI implementation is [WMPP_Theme.json](WMPP_Theme.json). Navigation Hover Peach was added from the owner's edited Home hover SVG on 28 September. Filter Charcoal was subsequently selected for the Filters controls across all dashboards.

| Category | Colour | Hex code | Visual role and context |
|---|---|---|---|
| Hero | Main Orange | `#EF7911` | Focal highlights, workload pictograms and headline emphasis |
| Navigation | Signature Coral | `#FB6540` | Circular navigation buttons and primary actions |
| Navigation | Hover Coral | `#F98165` | Hover treatment; no button outline |
| Navigation | Navigation Hover Peach | `#FCA356` | Owner-selected elongated hover capsule, surrounding a Main Orange circle |
| Utility | Filter Charcoal | `#2B2427` | Filters button fill in resting, hover, pressed and disabled states; preserve white filter artwork and white panel |
| Supporting | Balanced Teal | `#4DAAAB` | Contrasting categorical series; Residential placement type |
| Supporting | Deep Teal | `#287C73` | Stronger teal emphasis and supporting icons |
| Supporting | Warm Peach | `#FFB39F` | Additional categorical series where legible |
| Soft accent | Blush Peach | `#FEE1DD` | Selected rows and gentle highlights |
| Saturated accent | Cobalt Blue | `#0D35B8` | Occasional analytical comparison or emphasis |
| Saturated accent | Rich Berry | `#E63496` | Additional categories; never an error indicator |
| Identity accent | BCT Gold | `#FCBF00` | Limited client identity accents, not routine chart segments |
| Identity accent | Pale Gold | `#FFE672` | Limited identity highlights, not routine chart segments |
| RAG — Red | Crimson Jasper | `#C0392B` | Critical, overdue, failed or breached status |
| RAG — Amber | Saffron Gold | `#E69512` | Due soon, warning or pending action requiring attention |
| RAG — Green | Eucalyptus | `#277455` | Successful, completed or on-track status |
| Status tint | Soft Red | `#FBE7E4` | Critical-label background |
| Status tint | Soft Amber | `#FFF1D6` | Warning-label and retained pale information-badge background |
| Status tint | Soft Green | `#E4F1E9` | Success-label background |
| Primary neutral | Charcoal | `#2B2B2C` | Titles, KPI values, body text and comparison marks |
| Secondary neutral | Warm Grey Text | `#625B5B` | Subtitles, annotations and secondary labels |
| Neutral fill | Warm Stone | `#E3DADA` | Unknown categories, dividers and disabled surfaces |
| Light neutral | Warm Mist | `#F0EBE7` | Alternating rows and subdued non-status fills |
| Canvas | Warm Off-white | `#F8F5F1` | All report-page backgrounds |
| Surface | White | `#FFFFFF` | Cards, charts and dropdown surrounds |
| Depth | Warm Shadow | `#C78E7A` | Soft, highly transparent under-card shadows |

## Colour discipline

- Standard categorical sequence: Coral, Charcoal, Teal, Cobalt, Berry, Warm Peach. Use the smallest number needed.
- Placement types: Supported Accommodation → Coral; Residential → Teal; Fostering → Charcoal. Keep these mappings across pages.
- Keep RAG colours for status. Teal is a categorical contrast; Eucalyptus is explicit success.
- Do not introduce automatic tint/shade variants, custom hex colours or continuous colour gradients. Prefer discrete palette colours. Label categories and status; colour alone is insufficient.
- Existing theme index counts are retained for compatibility, but their colour values repeat the approved categorical sequence. Saved theme-colour expressions are resolved to approved literals to avoid inherited shade variants.
- White-on-coral navigation is the owner's requested treatment. Keep dark captions/tooltips; this is not a claim of accessibility compliance. Use dark text on pale fills and check rendered contrast.
- Antialiasing, transparency, selection dimming and map-provider imagery can produce other screen pixels. The restriction is on authored colour values, not a claim that every rendered pixel has one of these exact hex values.
- Supplied client logos and raster artwork retain their original identity. Do not recolour the logo to enforce a report palette. Historical mockups, original upstream SVGs and the immutable fallback theme are reference/archive assets, not current style defaults.
- The current migration applies to the WMPP delivery. Mission Control remains separate and is not silently reskinned.

## Layout, navigation and icons

Preserve the warm canvas, white rounded cards and soft glow. No full-page skin, no border boxes around headings and no outlines around navigation buttons.

- Main navigation: isolated circular icons at rest, with downward capsules on hover/current section. All enabled circles use Main Orange `#EF7911`; hover, current-section and pressed capsules use Navigation Hover Peach `#FCA356`. Do not use coral or blush pink for these button states. Direct white Lucide icons remain enabled. No connecting rail or outlines. Dropdowns retain connected white surrounds and readable title-case labels.
- On 1680px report pages, use 96×108px navigation targets at x=860, y=8 with 100px horizontal pitch. The SVG circle is 62px across and the white native icon is 32px. Resting/disabled circles have centre y=36 and icon top margin 20px. Active/hover capsules have circle centre y=42 and icon top margin 26px: circle and glyph move together, leaving 9px of peach headroom above the circle. Labels use an independent lower area (top margin 74px, bottom 8px, side margins 6px), with native 8pt text. Reserve x=748, y=0, 88×104px for Filters on overview dashboards. The filter drawer opens below/left of the navigation (x=438, y=124, width=398px), with 24px content insets. Guide/tooltip return controls are separate.
- Dropdown rows use White at rest and Navigation Hover Peach `#FCA356` for the current page, hover and pressed highlights, with Charcoal text; no coral/pink row overrides. Keep original primary buttons visible. The existing menu-cap IDs render white-backed native buttons above them at z=400010, retaining their original bookmark visibility. Use `WMPP Connected Open Menu` with 104×116 connected background SVGs; icon/text top offsets increase by 8px and text side offsets by 4px to preserve absolute placement. Clicking an open cap or the Close menu row closes the menu. The retired replacement variants stay hidden. Preserve data selections; verify the white join in Desktop after reopening.
- Keep primary buttons above dropdown cap/neck/panel shapes: the current delivery uses z=400000 for buttons, versus z=300005–300007 for surrounds. Dropdown rows start at y=136. Opening a submenu must not cover its parent icon or label. Maintain the same geometry on all 16 navigable report pages.
- Use the `WMPP Owner Bubble Navigation` preset plus the registered `wmpp-bubble-background-*.svg` fill assets, with fill transparency explicitly **0%**. Keep icons separate from these icon-free backgrounds. Use the owner's full `wmpp-bubble-*-active.svg` and `*-hover.svg` assets as visual/audit references. State swaps create the elongated-hover effect; this is not continuous animation and does not move adjacent buttons. Theme import alone cannot install resources or actions.
- Main dashboard filters may collapse into display-only bookmark drawers. Keep detail-page search/filter controls visible and chart-specific parameters beside their charts. Opening a drawer or submenu closes competing overlays without restoring data selections. Use readable bookmark labels such as `Referrals | Open filters`, never page hashes in user-visible names.
- Canvas and surrounding wallpaper must both use Warm Off-white `#F8F5F1`, including explicit per-page `outspace` overrides; the theme alone does not override previously saved page colours. Never use coral for the surrounding wallpaper.
- Page names and guide-page suffixes use title case, preserving WMPP and IPA acronyms. Preserve internal page IDs and action targets when renaming. Distinguish `Referral Single View (Original)` from the newer `Referral Single View`.
- KPI and guide pictograms: transparent, meaning-matched Lucide outlines. Keep the 25% smaller artwork inside its original slots; do not move cards or headings.
- Information badges: retain their small pale-background treatment, now expressed with Soft Amber and Charcoal from this palette. Do not remove their backgrounds.
- Typical panel corners 14–18px; spacing on an 8px rhythm, usually 16–24px between panels. Inset chart headings/content 12–16px where practical.
- Keep grouped visual coordinates, padding, click targets, bookmarks and data bindings unchanged during palette edits.
- Fonts remain Segoe UI in the delivered report. Lato/Arial are historical brand references, not instructions to migrate working report typography.
- Section titles previously set to 32pt now use 24pt. Heading 4/KPI labels use regular weight, including refresh labels; small chart titles and supporting headings at 13pt or below also use regular Segoe UI, not bold or Semibold. Preserve large numeric KPI callouts and the navigation's established active-state emphasis. Apply both theme defaults and local visual overrides; browser zoom still scales the entire report.
- Dropdown menu rows, including their section entries and Close menu, use regular Segoe UI in every state. Do not bold dropdown text on hover or selection. This does not change the main navigation buttons' active-state emphasis.
- Starting sizes: page titles 24–30px, section titles 16–20px, chart titles 12–14px, KPI values 28–36px, body labels 11–13px. Check Power BI's property units and actual rendering before changing them.

## KPI language

Use Current period, Previous month, Month-on-month change and Change rate consistently. Percentage-point differences use “pp”, not percentage change. Separate current snapshots, period activity and cohorts. Mockup values are illustrative, never report data. Styling does not certify requirement delivery or KPI calculation correctness.

## Implementation and audit files

All reusable report SVG icons are consolidated under `icons/`; see
[`icons/README.md`](icons/README.md) for the folder guide and migration manifest.
Loose report-root/category/journey files have moved there. Power BI's embedded
resource copies remain in their report packages to preserve working visuals.

- `WMPP_Palette.json` — permitted colours and placement-category mapping.
- `WMPP_Theme.json` — active theme; aligned copies are in `reports/templates` and the delivery's registered resources.
- `WMPP_Theme_v0.json` — immutable historical fallback; never import it as the current palette.
- `design-system/tokens.css` and `components.css` — active UI tokens/components.
- `icons/LUCIDE_KPI_ICONS.md` and `LUCIDE_NAVIGATION.md` — icon implementation.
- `icons/LUCIDE_KPI_SOURCES.json` — source URLs, pinned revision, current variant colours/hashes and visual mapping.
- `icons/lucide-originals/` — unmodified upstream evidence, not directly deployed assets.
- `icons/LUCIDE_LICENSE.txt` — retain with client delivery.
- `icons/navigation-bubbles/` — current owner-selected bubble state references and icon-free backgrounds; see its README. The previous connecting rail remains withdrawn. Direct white `lucide-nav-*-white.svg` icons are still used alongside these backgrounds.
- `Mockups/` and `Proposed Pack/` — historical reference material only. Their colours do not override this guide.
- Supplied logo/guidelines/template remain under `Mockups/`; preserve their aspect ratio, clear space and identity.

Import the current theme for new work, then inspect saved visual overrides. Before delivery, review each page in Desktop, including navigation, clipped labels, small icons, status colours and exports. File/schema validation does not prove rendered acceptance. No refresh or publication is implied by a styling edit.

The operational catalogue is [WMPP_Semantic_Model_Measures.md](../../client%20documentation/04_Data_and_Reporting/WMPP_Semantic_Model_Measures.md).
