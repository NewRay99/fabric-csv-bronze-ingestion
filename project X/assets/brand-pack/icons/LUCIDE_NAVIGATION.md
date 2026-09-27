> Current authority: [WMPP_Brand_Pack.md](../WMPP_Brand_Pack.md) and `../WMPP_Palette.json` supersede earlier palette/design instructions below. Only the approved 24 colours may be authored. No automatic shades or chart gradients; retain warm canvas, rounded white cards, small transparent KPI icons, pale information badges, and borderless circular navigation. Older proposal/approval statements are historical, not evidence of client sign-off.

# WMPP navigation icons

Downloaded from the official Lucide repository on 27 September 2026. SVG paths
are original Lucide artwork; only `currentColor` is replaced by `#FFFFFF` in the
white deployment variants. Unmodified sources are retained in `lucide-originals/`.

| Navigation | Lucide icon | White SVG |
|---|---|---|
| Home | [house](https://lucide.dev/icons/house) | `lucide-nav-house-white.svg` |
| Referrals | [user-round-plus](https://lucide.dev/icons/user-round-plus) | `lucide-nav-user-round-plus-white.svg` |
| Offers | [handshake](https://lucide.dev/icons/handshake) | `lucide-nav-handshake-white.svg` |
| Draft offers | [file-pen-line](https://lucide.dev/icons/file-pen-line) | `lucide-nav-file-pen-line-white.svg` |
| IPAs | [file-check-corner](https://lucide.dev/icons/file-check-corner) | `lucide-nav-file-check-corner-white.svg` |
| Providers | [building-complex](https://lucide.dev/icons/building-complex) | `lucide-nav-building-complex-white.svg` |
| Performance | [chart-no-axes-combined](https://lucide.dev/icons/chart-no-axes-combined) | `lucide-nav-chart-no-axes-combined-white.svg` |
| Requirements | [clipboard-list](https://lucide.dev/icons/clipboard-list) | `lucide-nav-clipboard-list-white.svg` |

Use native Power BI button custom icons, not separate overlaid image visuals.
The saved WMPP delivery embeds these resources and uses them in all four states
of its 128 main navigation buttons. Initials are disabled; captions, tooltips,
actions, circular geometry and coral fills are retained. Button outlines and
container borders are disabled. The separate Filters control is unchanged.

Native icon size is 32 within a 66-square circular button. Keep the SVG aspect
ratio and original 2-unit stroke. These are white on transparent backgrounds;
they can look blank on a white image preview.

See `LUCIDE_NAVIGATION_SOURCES.json` for the exact upstream revision and hashes.
Retain `LUCIDE_LICENSE.txt` with copies of the assets, including client packages.
The project root of the WMPP delivery contains the same source manifest and
licence; registered report resources make the icons available without a live
web connection. [Lucide licensing](https://lucide.dev/license).

The white-on-coral pair is the requested visual treatment, not a verified
accessibility pass. Keep dark captions below it. Power BI Desktop rendering and
interaction acceptance remain required; file checks cannot prove rendering.
