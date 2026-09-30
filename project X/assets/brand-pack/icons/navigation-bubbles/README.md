# WMPP horizontal bubble navigation

## Current implementation — 28 September 2026

### White connected open-menu caps

The 64 existing white menu-cap IDs now render native buttons, retaining their working bookmark visibility and displaying above the unchanged primary buttons. Use `WMPP Connected Open Menu`, white fill, and `wmpp-bubble-connected-*.svg` backgrounds (104×116 with the original artwork translated by 4px right and 8px down). Add 8px to native icon/text top margins and 4px to text side margins; this preserves their absolute positions. The cap closes its menu when clicked. Do not hide the original main button or revive the retired replacement variants. These cap visuals provide the white join missing from the prior correction; Desktop render acceptance remains outstanding.

### Current correction: capsule headroom and persistent main buttons

Active/hover capsules have 9px of peach headroom above the orange circle: capsule top y=2, circle centre y=42 and radius 31. Move the circle and glyph together. Complete capsule SVG glyphs use `translate(32 26) scale(1.333333333)`; resting/disabled glyphs use `translate(32 20) scale(1.333333333)` with circle centre y=36. Native icon top margins match each state (26px capsule, 20px circle), keeping the 32px glyph centred inside its circle.

Dropdown highlights use `#FCA356` with dark text instead of coral/pink. All 128 original main buttons remain visible in navigation/filter bookmarks; the 64 replacement open-menu variants are retired and hidden in every bookmark. Do not swap the primary button out on menu opening. Use the Close menu row to close a dropdown. This supersedes the prior white-fill replacement approach; a seamless white join has not been confirmed in Desktop. Retain opaque fill images and separate native icons. No full-page background, data, or model change is involved.

### Spacing and layering correction

The owner rejected the remaining coral/pink active state. Current assets now use orange `#EF7911` circles and peach `#FCA356` active/hover capsules; disabled circles remain stone. All 36 SVGs (32 complete icon variants and four icon-free backgrounds) use a 96×108 viewBox. These updated assets supersede the original 72×96 Home samples, retained in the delivery backup.

Use 96×108px targets at x=860 + 100×index, y=8. Icons are 32px, inset 20px for circle states and 26px for capsule states. Native 8pt labels have 6px left/right margins and a dedicated lower area beginning 74px from the top, with 8px bottom margin. Keep native icons enabled, background fills at 0% transparency, and separate caption layers hidden. Primary buttons render above dropdown surrounds (z=400000 versus 300005–300007). Dropdown rows begin at y=136. Filters sits at x=748; its drawer starts at x=438, y=124.

The colour and geometry details below describe the prior iteration and are superseded by this correction.

The owner selected the edited Home hover and active SVGs in this folder. Their exact Home source files are retained unchanged. Equivalent full SVGs are available for all eight navigation destinations, using the existing audited Lucide paths.

- Resting: Main Orange `#EF7911` circle.
- Hover: Navigation Hover Peach `#FCA356` capsule around Main Orange.
- Active/current section and pressed: Blush Peach `#FEE1DD` capsule around Signature Coral `#FB6540`.
- Disabled: Warm Stone `#E3DADA` circle.
- White 28px Lucide icons; charcoal native text; no outline or connecting rail.

The report deliberately renders the four **icon-free** `wmpp-bubble-background-*.svg` files as native button fills, and retains a separate native Lucide icon in every state. Set fill transparency to **0%**, not 100%. Full combined SVG variants are implementation/audit references; do not apply them as fills while also enabling a duplicate native icon.

Use `WMPP Owner Bubble Navigation` from the current theme. Targets are 72×96px, spaced every 74px, starting at x=1069, y=8 on a 1680px page. Native icons are centred horizontally and placed 19px from the top; native captions use top margin 62px and bottom margin 6px. Labels share the button's hover target. The old separate caption visuals remain hidden in all navigation/filter bookmarks.

Hover is a native state swap, not continuous animated motion. Current-section styling is configured per page, not inferred from the transient pressed state. Touch users retain visible labels and the current-section capsule. Existing click actions, dropdowns, Filters and referral-journey bookmarks are retained. No hover-triggered navigation is introduced. Microsoft documents [button states and fill images](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons).

The theme does not package SVGs or navigation actions: register the background assets and direct white icons in each report. The 128 buttons across 16 pages have been updated in the WMPP client delivery. Mission Control is unchanged. Backup and changed-file inventory are recorded in `OWNER_BUBBLE_NAVIGATION.json` alongside the client PBIP. File/schema checks are not Desktop-render acceptance.

## Superseded experiment — 27 September 2026

The description below is historical only. Its connecting rail, disabled native icons and transparent fill configuration must **not** be reapplied.

The horizontal adaptation of the [supplied bubble-menu reference](https://www.reddit.com/r/PowerBI/comments/1mi4mut/page_navigation_bubble_design/) is installed in the client-delivery WMPP report. The reference is inspiration, not redistributed artwork.

The 32 SVG files combine existing audited white Lucide paths with new WMPP bubble silhouettes. Existing Lucide provenance and licence files in the parent directory remain applicable; upstream icon paths are unchanged.

- Shared rail: Signature Coral `#FB6540`, rounded ends and Warm Shadow `#C78E7A` at high transparency.
- Resting icon: 54px coral circle; 28px white Lucide artwork.
- Current section: Blush Peach `#FEE1DD` capsule behind the coral circle.
- Hover: Hover Coral `#F98165` capsule, extending down around the native label.
- Disabled: Warm Stone `#E3DADA` circle.
- Labels: native Segoe UI in Charcoal `#2B2B2C`, always visible, not baked into SVGs.

Use the `WMPP Bubble Navigation` action-button preset from `WMPP_Theme.json`. Assign each image to the native button's Fill image for the corresponding state; retain a transparent fill colour and disable the separate native Icon, Outline, Glow and Shadow settings. The rail supplies the shadow. The fixed button target is 72 × 96px, on a 74px horizontal pitch, with labels below the icon and no overlap between button targets.

Expansion is a native state swap, not continuous animated motion. It does not trigger bookmarks on hover. Clicking grouped areas opens the existing submenu; direct destinations and filter-preserving bookmarks are retained. Keep dropdown rows below the expanded image. Power BI supports [button fill images and state formatting](https://learn.microsoft.com/en-us/power-bi/create-reports/desktop-buttons).

The theme does not carry resource files or navigation actions. New reports require these SVG resources, the rail, button actions and menu bookmark definitions as well as the preset. Do not use theme import alone as a migration.

The small information badges, KPI icons, cards, source logo and report measures are outside this change. Desktop visual/interaction acceptance remains required; schema validation is not a rendering guarantee.
