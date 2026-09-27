> Current authority: [WMPP_Brand_Pack.md](../WMPP_Brand_Pack.md) and `../WMPP_Palette.json` supersede earlier palette/design instructions below. Only the approved 24 colours may be authored. No automatic shades or chart gradients; retain warm canvas, rounded white cards, small transparent KPI icons, pale information badges, and borderless circular navigation. Older proposal/approval statements are historical, not evidence of client sign-off.

# WMPP KPI and guide icons

Updated 27 September 2026. Applies to the WMPP delivery, not the dark Mission
Control report. Navigation remains white-on-coral and borderless.

## Icon meanings

| KPI / section | Lucide pictogram | Stroke colour |
|---|---|---|
| Referrals and current caseload | Users | Hero orange `#EF7911` |
| Offers and referrals under offer | Handshake | Hero orange `#EF7911` |
| Successful/accepted offers | Handshake | Deep teal `#287C73` |
| Waiting / pending / elapsed age | Clock | Saffron gold `#E69512` |
| Engagement / activity | Activity | Deep teal `#287C73` |
| Multiple provider assignments | Network | Hero orange `#EF7911` |
| Draft offers | File pen line | Hero orange `#EF7911` |
| Drafts with no activity | Hourglass | Saffron gold `#E69512` |
| IPAs created | File plus | Hero orange `#EF7911` |
| IPA completion / conversion | File check corner | Deep teal `#287C73` |
| Requirements / KPI catalogue | Clipboard list | Hero orange `#EF7911` |
| Requirements completion card | Clipboard check | Deep teal `#287C73` |
| Distance | Route | Hero orange `#EF7911` |
| Location coverage / review | Map pin | Teal / amber respectively |
| Targets | Target | Deep teal `#287C73` |
| Overdue / escalation | Triangle alert | Crimson jasper `#C0392B` |
| Cost | Pound sterling | Deep teal `#287C73` |
| Snapshots / due month | Calendar days | Hero orange `#EF7911` |
| Homes / providers | House / building complex | Hero orange `#EF7911` |

The complete per-visual mapping is in `LUCIDE_KPI_SOURCES.json`, including exact
source links, a pinned Lucide revision, original and coloured-variant hashes.
Unmodified downloads remain in `lucide-originals/`; transparent coloured SVGs
are alongside this document. Retain `LUCIDE_LICENSE.txt` with every distribution.

## Implementation rules

- Size revision: the new KPI/guide pictograms are **25% smaller**, centred inside
  their original slots by expanding the SVG viewBox to `-4 -4 32 32`. Card and
  heading positions are unchanged. Navigation icons and information badges are
  unchanged. Do not reset the viewBox when reusing these compact variants.

- Colour the strokes, not a circle behind the icon. No background disc is added
  to KPI pictograms. Native white cards and their existing soft shadows remain.
- **Exception requested by the owner:** the small information/help icons keep
  their existing pale background. Do not replace or recolour these badges.
- Existing native card-image slots are reused. Narrow Board/Supply/Target value
  cards retain their separate icons to avoid reducing the number's space.
- Added subpages use icons beside appropriate titles/sections and within KPI
  cards. Guide headings use the same semantic icon selection; text is inset to
  leave a 12px icon-to-heading gap. Body explanations stay unchanged, except new
  explanatory entries for requirement scorecards missing from the earlier guide.
- An icon does not validate a KPI calculation or certify delivery. In particular,
  a requirements-linkage count is not evidence of client acceptance.
- Icons are embedded in the report's registered resources; no external image
  URL or API key is needed when viewing the deployed report.

## Chart colours

The Offers per Qualifying Provider chart uses uniform `#FB6540` bars and dark
labels: bar length already represents the quantity, so the old rose gradient is
removed. Continuous chart gradients are removed; only discrete approved colours are used.
Other updated marks follow coral/orange/peach and teal, with the existing semantic
red and amber meanings retained. No measure, denominator, filter or chart type
is changed by this visual refresh.

Keep full labels/tooltips alongside icons and colours. Guide icons are visual
aids, not new navigation controls. Desktop rendering still requires inspection.
