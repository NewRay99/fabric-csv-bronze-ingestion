# Power BI Dashboard Mockup Generator — Master Prompt

## Purpose

Use this prompt to generate stunning, production-quality HTML mockups of Power BI dashboard pages. The AI has full creative freedom to make the report visually striking while adhering to the corporate brand system and KPI specifications provided.

---

## The Prompt

```
You are an expert UX/UI designer specializing in data visualization and Power BI dashboard design. You have been commissioned to create a stunning, high-fidelity HTML mockup of a Power BI dashboard page for a corporate reporting suite.

## Corporate Brand System

The following brand colours are MANDATORY — use them as the foundation of every visual decision:

Primary Palette:
- Primary Navy: #002060 (headers, table headers, primary chart series, KPI accent borders for primary metrics)
- Secondary Gold: #f0a010 (accents, R-tag badges, active nav indicators, highlight series)
- Navy Dark: #001A45 (gradient depth, hover states)
- Navy Light: #1a4080 (secondary chart series, tertiary elements)
- Gold Light: #f5c050 (hover highlights, subtle accents)
- Gold Dark: #c08000 (text on light backgrounds, emphasis)

Surface & Text:
- Background: #f0f2f5 (page canvas — calm, professional)
- Surface: #ffffff (cards, charts, tables)
- Ink: #1a1a1a (primary text, KPI values)
- Ink Secondary: #555555 (labels, descriptions)
- Ink Tertiary: #999999 (metadata, axis labels)
- Border: #e0e0e0 (subtle dividers)

Semantic Colours (use purposefully, not decoratively):
- Success Green: #2E8B2E (positive KPIs, completed, active status)
- Warning Yellow: #D4A017 (at-risk, ageing, draft status)
- Alert Red: #C0392B (critical, expired, closed, over-budget)
- Each semantic colour has a tinted background variant for badges: green-tint #e8f5e8, yellow-tint #fff9e6, red-tint #fcebe9

Typography:
- Primary font: Inter (Google Fonts) — use weights 300, 400, 500, 600, 700
- KPI values: 28px, weight 700, font-variant-numeric: tabular-nums
- Chart titles: 13px, weight 600
- Table headers: 11px, weight 600, uppercase, letter-spacing 0.3px
- Labels: 11px, weight 500
- Metadata: 11px, weight 400, ink-tertiary

Logo: Use the provided logo image (bct_logo.png) in the header at 36px height.

## Design System Components

### Header Bar
- Navy gradient: linear-gradient(135deg, #002060, #001A45)
- Height: 64px
- Logo on left, page title in white (18px, 600), nav links on right
- Active nav: white text with 2px gold (#f0a010) bottom border
- Inactive nav: rgba(255,255,255,0.65), hover to white with subtle bg

### Filter Bar
- White surface with subtle shadow
- Pill-shaped filters (border-radius: 20px) with label + value + dropdown caret
- Refresh button: navy bg, white text, 4px radius

### KPI Cards
- White surface, 6px border-radius, subtle shadow (0 1px 3px rgba(0,0,0,0.08))
- 3px coloured left accent bar (navy/gold/green/yellow/red based on metric type)
- Label: 11px uppercase, ink-secondary
- Value: 28px bold, tabular-nums
- Sub-text: 11px, ink-tertiary, with ▲ (green) / ▼ (red) trend indicators
- Hover: lift with shadow-lg (0 4px 16px rgba(0,32,96,0.1))

### Chart Cards
- White surface, same shadow and radius as KPI cards
- Title row: 13px bold ink + 11px ink-tertiary metadata on right
- Charts built with pure CSS — no JavaScript charting libraries
- Dotted gridlines (1px dashed #e0e0e0)
- Legends with coloured dots/squares

### Tables
- Navy (#002060) header row with white text
- Alternating row colours (#ffffff / #fafafa)
- Hover: navy-tint (#e8edf5) row background
- Status badges: pill-shaped (border-radius: 10px) with tinted bg + semantic colour text
- 1px solid #e0e0e0 bottom borders on rows

### R-Tag Badges (Functional Requirement References)
- Gold (#f0a010) background, navy (#002060) text
- 9px, weight 700, 3px radius, padding 2px 6px
- Placed above the KPI label

### Navigation Buttons / Slide Navigation
- Include a horizontal slide/button nav at the bottom of each page
- Each button: navy-tint background, navy text, 4px radius, 12px font, 8px 16px padding
- Active button: navy background, white text, gold left border (3px)
- Buttons link to the other dashboard pages
- Include arrow indicators (← Previous | Next →)

## Creative Freedom

Within the brand system above, you have FULL creative freedom to:

1. **Choose the best chart type** for each data set — donut, bar, column, line, funnel, heatmap, treemap, gauge, or any CSS-constructable visual. Pick what communicates the data most effectively.

2. **Design the layout** — you decide the grid structure. Use CSS Grid with whatever column spans make sense for the data. Break the grid when a visual needs more or less space. Asymmetric layouts are encouraged when they serve the data.

3. **Add micro-interactions** — hover states, transitions, animated bar fills, tooltip-style info popovers. Make it feel alive. Use CSS transitions and transforms. Respect prefers-reduced-motion.

4. **Enhance with visual flourishes** — gradient accents, subtle texture, depth via shadows, glassmorphism on overlay elements (used sparingly and purposefully, not as default decoration).

5. **Invent data visualizations** — if a standard chart doesn't serve the data, create a custom CSS visual. Think: progress rings, funnel drops, sankey-style flows, calendar heatmaps, bullet charts.

6. **Use iconography** — Unicode symbols, CSS-drawn icons, or inline SVG for visual anchors. Keep them minimal and purposeful.

7. **Tell a story** — arrange the page so the eye flows from summary KPIs → trends → detail. Use visual hierarchy (size, colour, spacing) to guide attention.

## What NOT to Do

- Do NOT use emoji as data icons (unless the brand specifically uses them)
- Do NOT use generic stock-photo placeholders
- Do NOT create fake metrics that aren't in the KPI spec
- Do NOT use rainbow palettes — stick to navy/gold + semantic colours
- Do NOT make every section a card grid — vary the layout
- Do NOT add decorative elements that don't serve comprehension
- Do NOT use Lorem Ipsum — all text should be real, meaningful labels

## Technical Requirements

- Single self-contained HTML file with inline CSS
- Inter font loaded from Google Fonts
- Mobile responsive (grid collapses gracefully on small screens)
- CSS variables for all brand tokens
- All charts constructed with pure CSS (no JS charting libraries)
- File must open directly in a browser with no build step

## Page Specification

For each page, you will receive:
1. Page name and purpose
2. KPI cards list (label, value, sub-text, accent colour, optional R-tag)
3. Charts list (type, title, data series, colours)
4. Tables list (columns, sample rows)
5. Any NEW measures with functional requirement tags [R##]

Interpret these as a guide, not a constraint. If you see a better way to visualize the data, do it. If a KPI would be more impactful as a progress ring instead of a card, transform it. If two charts would work better combined, merge them.

The goal is a dashboard that a senior designer would be proud to put in their portfolio.

## Output

Produce a single HTML file. Before returning it, verify:
- File is complete and valid HTML
- All CSS variables reference the brand system
- Logo image path is correct (bct_logo.png, relative)
- All nav links point to valid pages
- No JavaScript errors (if any JS is used for interactions)
- Mobile breakpoint works
```

---

## Usage Examples

### Example 1: Generating a Single Page

```
[Paste the master prompt above]

## Page Specification: REFERRALS

Purpose: Referral demand monitoring and lifecycle overview

KPI Cards:
- Total Referrals: 161 (navy accent, ▲ 12% vs last period)
- Active: 72 (green accent, ▲ 8%)
- Under Offer: 8 (gold accent, 2 new this week)
- Awaiting Offers: 64 (yellow accent, ▼ 5%)
- Closed/Cancelled: 42 (red accent, 17 placed · 25 withdrawn)
- Offer Rate: 68% (navy accent, ▲ 3pp)

Gender Cards:
- Male: 89 (navy circle icon, 55.3%)
- Female: 66 (gold circle icon, 41.0%)
- Other: 6 (navy-light circle, 3.7%)

NEW KPIs (with R-tags):
- Emergency Referrals: 12 [R18, R57] (red accent)
- Emergency Rate: 7.5% [R57] (navy-light accent, target ≤10%)
- Planned Referrals: 149 [R57] (navy accent)
- Out-of-Region: 3 [R22] (gold accent)

Charts:
- Donut: Placement Type (Residential 40%, Fostering 35%, Supported 25%)
- Column: Monthly Activity (Jan-Apr, 3 series: Open/Closed/Cancelled)
- Bar: Closure Reasons (No capacity 15, Too far 8, Wrong specialism 6, Other 4)

Table: Recent Referrals (8 rows, columns: ID, Type, Status, Date, Region)
```

### Example 2: Generating All Pages at Once

```
[Paste the master prompt above]

Generate all 5 dashboard pages as separate HTML files:

1. referrals.html — 6 KPI cards + 3 gender cards + 4 R-tag cards + donut + column + bar + table
2. offers_overview.html — 12 KPI cards (3 rows) + 100% stacked column + top-10 bar chart
3. ipa_overview.html — 12 KPI cards + funnel chart + IPA detail table + conversion rates table
4. draft_offers.html — 9 KPI cards + clustered column (age bands) + legend cards
5. provider_registry.html — 11 KPI cards + bar chart + directory table + QA flag breakdown

[Include KPI values and chart data for each page — see KPI Reference Guide]
```

### Example 3: Iterating on a Design

```
[Paste the master prompt above]

## Iteration Request

Take the existing referrals.html and make these improvements:
- Replace the donut chart with a more visually striking radial progress visualization
- Add a sparkline to each KPI card showing 7-day trend
- Make the table collapsible with a "Show All" button
- Add a gradient accent strip at the top of the page
- Include a "last refreshed" timestamp with a subtle pulse animation
```

---

## Notes for the User

- **Model choice:** This prompt works best with a model that has strong visual design capabilities. Claude Sonnet/Opus produce the best HTML artifacts. GLM-5.2 will produce functional but less polished results.
- **Iterating:** The prompt is designed to be reusable. Paste it again with revised specs to iterate on any page.
- **Brand colours:** The navy (#002060) and gold (#f0a010) were extracted from pixel analysis of the actual BCT logo. If the brand changes, update the CSS variables in the prompt.
- **Logo file:** Ensure `bct_logo.png` exists in the same directory as the generated HTML files.
