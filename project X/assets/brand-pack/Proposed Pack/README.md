# WMPP Brand Pack — Proposed Pack (v1.0)

**Project:** West Midlands Placement Portal (WMPP)
**Prepared for:** Birmingham Children's Trust
**Date:** 29 July 2026
**Status:** 🟡 Proposed — awaiting client sign-off
**Design reference:** SupplySense Supply Chain Dashboard (pastel pink / coral aesthetic)

---

## What is this?

The **Proposed Pack** is a complete restyle proposal for the WMPP Pilot Dashboard. It replaces the current stock theme (CY26SU02 blue/orange) with a soft, modern **pastel coral** design language — warm, approachable, and consistent with a children's-services context — modelled directly on the reference dashboard the client approved as the target look.

Everything in this folder is new. Nothing in the existing `brand pack/` has been modified.

---

## What's in this folder

```
Proposed Pack/
├── README.md                     ← this file
├── design-system/
│   ├── tokens.css                ← all colours, fonts, radii, spacing as variables
│   └── components.css            ← KPI cards, circular buttons, chips, bars
├── icons/                        ← 20 SVG assets (see below)
│   ├── referral-open.svg         referral-closed.svg
│   ├── referral-engaged.svg      referral-success.svg
│   ├── provider-home.svg         authority.svg
│   ├── child-placement.svg       offer.svg
│   ├── clock-pending.svg         caseload.svg
│   ├── map-pin.svg               trend-up.svg
│   ├── filter.svg                calendar.svg
│   ├── compare.svg               grid.svg
│   └── arrow-squiggly-*.svg      ← 4 rounded hand-drawn style arrows
└── mockups/
    ├── brand-preview.html        ← every token & component on one page
    └── referrals-performance.html← full dashboard page in the new style
```

---

## Added (new in this pack)

| Item | Detail |
|------|--------|
| **Pastel coral colour system** | Full ramp from `#E0603F` coral through 5 tints to `#FEEDE8`, plus teal `#78B8C0` comparison ramp and ink `#282828` neutral. Extracted pixel-by-pixel from the approved reference. |
| **Referral status colour mapping** | Open → coral, With Engagement → teal, Successful → green, Closed → ink. One glance tells the reader where a referral sits in the lifecycle. |
| **KPI card component** | Rounded tile + circular icon badge + large DIN numeral + delta vs previous period + data provenance label (LOCKED / DERIVED / USER INPUT). Four colour variants. |
| **Circular buttons** | 46px pill buttons for page navigation (coral = primary action, ink = secondary, white = utility) plus 26px mini action buttons on card headers — matching the reference dashboard exactly. |
| **20 SVG icons** | Purpose-drawn for WMPP: open / closed / engaged / successful referrals, provider homes, local authority, child placement, offers, caseload, pending clock — plus 4 rounded squiggly arrows (right, teal-right, down, loop) for annotations and callouts. All stroke-based so they recolour with one CSS change. |
| **Status chips** | Pill badges for the four referral lifecycle states. |
| **Two HTML mockups** | `brand-preview.html` (component catalogue) and `referrals-performance.html` (a complete report page in the proposed style). Both viewable on any phone or desktop browser. |

## Revised (changes vs current V13.1 theme)

| Element | Current (CY26SU02) | Proposed |
|---------|-------------------|----------|
| Page background | White `#FFFFFF` | Pastel peach wash `#FDF0EB` |
| Primary data series | Blue `#118DFF` | Coral `#E0603F` with 5-step tint ramp for ranked categories |
| Comparison series | Dark blue `#12239E` | Teal `#78B8C0` |
| Neutral series | — | Ink `#282828` (near-black, used for "closed" states) |
| Card corners | Square / default | 18px radius, soft coral-tinted shadow |
| Success colour | Bright green `#1AAB40` | Softer `#3A9E75` (harmonises with coral) |
| Navigation | Text buttons | Circular icon buttons, top-right |
| Ranked bar charts | Single flat colour | Coral ramp — darkest = highest rank, fades with rank |

**Unchanged:** typography (DIN for numerals/titles, Segoe UI for labels — already in the current theme), page structure, all measures and KPI logic. This is a pure restyle — zero impact on the semantic model.

---

## How to review

1. **Open `mockups/referrals-performance.html`** — a full report page in the proposed style (KPI strip, ranked bar charts, grouped comparisons, donut, map). Works on mobile.
2. **Open `mockups/brand-preview.html`** — every colour, font, button, chip, icon and arrow in the system.
3. Feedback welcome on: coral vs a pinker tint, teal as the secondary colour, icon style, and whether the pastel canvas should extend to every page or just the homepage.

## Path to Power BI (if approved)

- `design-system/tokens.css` maps 1:1 to a Power BI theme JSON — the data colour sequence, semantic colours and text classes drop straight into a new `.json` theme file.
- The 20 SVGs can be uploaded as report image assets; KPI cards build as standard card visuals with the mapped status colours.
- No changes required to the semantic model, measures, or page logic.

---

*Sample figures in the mockups are illustrative only and will be replaced by live WMPP measures on implementation.*
