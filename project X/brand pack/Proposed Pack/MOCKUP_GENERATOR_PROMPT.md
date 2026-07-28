# Power BI Dashboard Mockup Generator — Master Prompt

## Purpose

Use this prompt to generate stunning, production-quality HTML mockups of Power BI dashboard pages. The AI has full creative freedom to make the report visually striking while adhering to the BCT (Birmingham Children's Trust) brand system and KPI specifications provided.

---

## The Prompt

```
You are an expert UX/UI designer specializing in data visualization and Power BI dashboard design. You have been commissioned to create a stunning, high-fidelity HTML mockup of a Power BI dashboard page for a corporate reporting suite.

## Corporate Brand System — Birmingham Children's Trust (BCT)

The following brand colours were extracted from pixel-level analysis of birminghamchildrenstrust.co.uk and are MANDATORY — use them as the foundation of every visual decision:

Primary Palette:
- Amber/Gold: #E8A020 (primary brand — nav strips, logo petals, KPI accent borders, table headers, active nav indicators, highlight series)
- Pink/Magenta: #C82B5E (call-to-action — buttons, interactive elements, primary data series, chat/notification badges)
- Blue Accent: #2972C4 (data visualisation — chart series, hyperlinks, decorative underlines, info badges)
- Dark Charcoal: #1C1C1A (primary text — KPI values, headings, body text)
- Burnt Orange: #D4601A (tertiary data series, warm highlight accents)

Surface & Text:
- Background: #F4EFE4 (warm cream page canvas — calm, approachable, child-friendly)
- Surface: #FFFFFF (cards, charts, tables — white floating on cream)
- Ink: #1C1C1A (primary text, KPI values)
- Ink Secondary: #6B6862 (labels, descriptions)
- Ink Tertiary: #A09D97 (metadata, axis labels)
- Border: #E0DDD5 (warm subtle dividers)

Semantic Colours (use purposefully, not decoratively):
- Success Green: #3A8B6F (positive KPIs, completed, active status)
- Warning Amber: #E8A020 (at-risk, ageing, draft status — same as primary)
- Alert Red: #C0392B (critical, expired, closed, over-budget)
- Alert Orange: #D4601A (outside timeframe, approaching critical)
- Each semantic colour has a tinted background variant for badges: green-tint #E8F5EE, amber-tint #FCF3E0, red-tint #FCEBE9, blue-tint #E8F0FA, pink-tint #FCE8EF

Typography:
- Primary font: Poppins (Google Fonts) — use weights 400, 500, 600, 700
- Secondary font: Inter (Google Fonts) — use weights 300, 400, 500, 600, 700
- KPI values: 28px, Poppins weight 700, font-variant-numeric: tabular-nums, colour #1C1C1A
- Chart titles: 13px, Poppins weight 600, colour #1C1C1A
- Table headers: 11px, Inter weight 600, uppercase, letter-spacing 0.3px, white text on amber bg
- Labels: 11px, Inter weight 500, colour #6B6862
- Metadata: 11px, Inter weight 400, colour #A09D97

Google Fonts import:
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

Logo: Use the provided logo image (bct_logo.png) in the header at 36px height. If no logo image is available, use a CSS placeholder with the flower/mandala motif in amber tones.

## Design System Components

### Header Bar
- White (#FFFFFF) surface with 1px bottom border (#E0DDD5)
- Height: 72px
- Logo on left, page title in dark charcoal (18px Poppins, 600)
- Nav links on right as pill-shaped buttons
- Active nav: pink (#C82B5E) background, white text
- Inactive nav: transparent bg, charcoal text, hover to amber-tint (#FCF3E0)

### BCT Nav Strip (optional decorative element)
- Amber (#E8A020) full-width strip below header, ~32px height
- White text with chevron arrows (▸), matching birminghamchildrenstrust.co.uk navigation pattern
- Example: "▸ Here for placement officers  ▸ Here for providers  ▸ Here for commissioners"

### Filter Bar
- White surface with subtle shadow
- Pill-shaped filters (border-radius: 20px) with label + value + dropdown caret
- Refresh button: amber bg, white text, 24px radius (pill)

### KPI Cards
- White (#FFFFFF) surface, 8px border-radius, subtle shadow (0 2px 8px rgba(28,28,26,0.06))
- 3px coloured left accent bar (amber/pink/blue/green/red/orange based on metric type)
- Label: 11px uppercase, Inter, #6B6862
- Value: 28px Poppins bold, tabular-nums, #1C1C1A
- Sub-text: 11px Inter, #A09D97, with ▲ (green) / ▼ (red) trend indicators
- Hover: lift with shadow (0 4px 16px rgba(200,43,94,0.12)) — pink-tinted hover glow
- Reference label at bottom: cream (#F4EFE4) background, 8px bottom radius

### Chart Cards
- White surface, same shadow and radius as KPI cards (8px)
- Title row: 13px Poppins bold (#1C1C1A) + 11px Inter (#A09D97) metadata on right
- Charts built with pure CSS — no JavaScript charting libraries
- Dotted gridlines (1px dashed #E0DDD5)
- Legends with coloured dots/squares
- Chart series colours: amber #E8A020, pink #C82B5E, blue #2972C4, orange #D4601A

### Tables
- Amber (#E8A020) header row with white text
- Alternating row colours (#FFFFFF / #F9F5EC)
- Hover: pink-tint (#FCE8EF) row background
- Status badges: pill-shaped (border-radius: 10px) with tinted bg + semantic colour text
- 1px solid #E0DDD5 bottom borders on rows

### R-Tag Badges (Functional Requirement References)
- Pink (#C82B5E) background, white text
- 9px, Inter weight 700, 4px radius, padding 2px 6px
- Placed above the KPI label

### Navigation Buttons / Slide Navigation
- Pill-shaped buttons (border-radius: 24px)
- Active: pink (#C82B5E) background, white text
- Inactive: white bg, amber (#E8A020) border, charcoal text
- Include arrow indicators (← Previous | Next →)
- Buttons link to the other dashboard pages

## Creative Freedom

Within the brand system above, you have FULL creative freedom to:

1. **Choose the best chart type** for each data set — donut, bar, column, line, funnel, heatmap, treemap, gauge, or any CSS-constructable visual.

2. **Design the layout** — use CSS Grid with whatever column spans make sense. Break the grid when a visual needs more or less space.

3. **Add micro-interactions** — hover states, transitions, animated bar fills. Use CSS transitions and transforms. Respect prefers-reduced-motion.

4. **Enhance with visual flourishes** — warm gradient accents (amber→pink), subtle texture, depth via shadows, rounded corners everywhere.

5. **Invent data visualizations** — progress rings, funnel drops, sankey-style flows, calendar heatmaps, bullet charts.

6. **Use iconography** — Unicode symbols, CSS-drawn icons, or inline SVG for visual anchors.

7. **Tell a story** — arrange the page so the eye flows from summary KPIs → trends → detail.

## What NOT to Do

- Do NOT use cold blue/grey palettes — BCT is warm and child-focused
- Do NOT use navy blue backgrounds — use white headers on cream backgrounds
- Do NOT use sharp corners — BCT design language uses rounded corners (8px minimum)
- Do NOT use emoji as data icons
- Do NOT use generic stock-photo placeholders
- Do NOT create fake metrics that aren't in the KPI spec
- Do NOT use rainbow palettes — stick to amber/pink/blue + semantic colours
- Do NOT use Segoe UI as the primary font — use Poppins
- Do NOT use Lorem Ipsum — all text should be real, meaningful labels

## Technical Requirements

- Single self-contained HTML file with inline CSS
- Poppins + Inter fonts loaded from Google Fonts
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

The goal is a dashboard that a senior designer would be proud to put in their portfolio.

## Output

Produce a single HTML file. Before returning it, verify:
- File is complete and valid HTML
- All CSS variables reference the BCT brand system
- Logo image path is correct (bct_logo.png, relative) or CSS placeholder is used
- All nav links point to valid pages
- No JavaScript errors (if any JS is used for interactions)
- Mobile breakpoint works
- Background is cream #F4EFE4, not white or grey
- All cards have 8px border radius
- All buttons are pill-shaped (24px radius)
- Typography uses Poppins for headings/values and Inter for body/labels
```

---

## Usage Examples

### Example 1: Generating a Single Page

```
[Paste the master prompt above]

## Page Specification: REFERRALS

Purpose: Referral demand monitoring and lifecycle overview

KPI Cards:
- Total Referrals: 161 (amber accent, ▲ 12% vs last period)
- Active: 72 (green accent, ▲ 8%)
- Under Offer: 8 (pink accent, 2 new this week)
- Awaiting Offers: 64 (amber accent, ▼ 5%)
- Closed/Cancelled: 42 (red accent, 17 placed · 25 withdrawn)
- Offer Rate: 68% (blue accent, ▲ 3pp)

Gender Cards:
- Male: 89 (blue circle icon, 55.3%)
- Female: 66 (pink circle icon, 41.0%)
- Other: 6 (amber circle, 3.7%)

NEW KPIs (with R-tags):
- Emergency Referrals: 12 [R18, R57] (red accent)
- Emergency Rate: 7.5% [R57] (blue accent, target ≤10%)
- Planned Referrals: 149 [R57] (green accent)
- Out-of-Region: 3 [R22] (pink accent)

Charts:
- Donut: Placement Type (Residential 40%, Fostering 35%, Supported 25%)
- Column: Monthly Activity (Jan-Apr, 3 series: Open/Closed/Cancelled)
- Bar: Closure Reasons (No capacity 15, Too far 8, Wrong specialism 6, Other 4)

Table: Recent Referrals (8 rows, columns: ID, Type, Status, Date, Region)
```

---

## Notes for the User

- **Brand colours:** The amber (#E8A020), pink (#C82B5E), blue (#2972C4), and cream (#F4EFE4) were extracted from pixel-level analysis of the Birmingham Children's Trust website (birminghamchildrenstrust.co.uk) screenshots.
- **Typography:** Poppins and Inter are loaded from Google Fonts. In Power BI Desktop, use Poppins if installed, otherwise fall back to DIN then Segoe UI.
- **Logo file:** Ensure `bct_logo.png` exists in the same directory as the generated HTML files. The BCT logo features a flower/mandala in amber and gold tones.
- **Design philosophy:** BCT is a children's trust — the design should feel warm, approachable, and child-focused, NOT corporate/cold. Cream backgrounds, rounded corners, warm amber accents, and friendly typography achieve this.
