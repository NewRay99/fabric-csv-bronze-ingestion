> Current authority: [WMPP_Brand_Pack.md](WMPP_Brand_Pack.md) and `WMPP_Palette.json` supersede earlier palette/design instructions below. Only the approved 24 colours may be authored. No automatic shades or chart gradients; retain warm canvas, rounded white cards, small transparent KPI icons, pale information badges, and borderless circular navigation. Older proposal/approval statements are historical, not evidence of client sign-off.

# WMPP Dashboard — Design System v2.0
## Figma Design Specification

### Brand: Birmingham Children's Trust (BCT) — Expanded Palette

---

## 1. COLOUR SYSTEM

### Core Palette (BCT)

| Token | Hex | CSS Variable | Usage |
|-------|-----|-------------|-------|
| Cream | `#F0EBE7` | `--cream` | Page background, warm neutral |
| Amber | `#E69512` | `--amber` | Primary CTA, warnings, charts series 2 |
| Pink | `#C0392B` | `--pink` | Critical alerts, charts series 4 |
| Blue | `#0D35B8` | `--blue` | Navigation, links, charts series 1 |
| Charcoal | `#2B2B2C` | `--charcoal` | Primary text, dark surfaces |
| Green | `#277455` | `--green` | Success, positive deltas |
| Red | `#C0392B` | `--red` | Errors, negative sentiment |

### NEW: Expanded Palette

| Token | Hex | CSS Variable | Usage |
|-------|-----|-------------|-------|
| **Mint** | `#4DAAAB` | `--mint` | New KPI accent, age bucket 0-7 days, "On Track" status |
| **Mint Dark** | `#4DAAAB` | `--mint-dark` | Mint text on light bg |
| **Mint Light** | `#E4F1E9` | `--mint-light` | Mint background tint |
| **Pastel Purple** | `#E3DADA` | `--pastel-purple` | IPA KPI accent, age bucket 8-14 days, "Under Review" status |
| **Pastel Purple Dark** | `#4DAAAB` | `--pastel-purple-dark` | Purple text on light bg |
| **Pastel Purple Light** | `#F0EBE7` | `--pastel-purple-light` | Purple background tint |

### Neutral Tones

| Token | Hex | Usage |
|-------|-----|-------|
| Neutral 50 | `#FFFFFF` | Table alternate rows, subtle surface |
| Neutral 100 | `#F0EBE7` | Page background |
| Neutral 200 | `#F0EBE7` | Borders, dividers |
| Neutral 600 | `#625B5B` | Secondary text |
| Neutral 700 | `#2B2B2C` | Muted text |

### Semantic Colours

| Status | Hex | Badge Text |
|--------|-----|------------|
| Positive / On Track | `#277455` | White |
| Warning / At Risk | `#E69512` | Charcoal |
| Negative / Critical | `#C0392B` | White |
| Info | `#0D35B8` | White |
| New / Draft | `#4DAAAB` | Charcoal |
| Under Review | `#E3DADA` | Charcoal |

---

## 2. TYPOGRAPHY

| Element | Font | Weight | Size | Line Height |
|---------|------|--------|------|-------------|
| Page Title | Lato | 700 | 22px | 1.3 |
| Chart Title | Lato | 600 | 13px | 1.3 |
| KPI Value | Lato | 700 | 34px | 1.0 |
| Table Header | Lato | 600 | 10px | 1.4 |
| Body / Labels | Lato | 400/500 | 10-11px | 1.5 |
| Badges | Lato | 700 | 9.5px | 1.0 |

> **Power BI equivalent:** Set visual-level font to "Lato" for titles and card values; "Lato" for data labels and axis text. Fallback: Segoe UI, Arial, sans-serif.

---

## 3. COMPONENT LIBRARY (Figma-Ready)

### 3.1 KPI Card

```
┌─────────────────────────┐
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  │ ← Accent stripe (3px, colour-coded per metric)
│                         │
│  TOTAL REFERRALS        │ ← Label: Lato 10.5px, 600, uppercase, text-secondary
│  2,847                  │ ← Value: Lato 34px, 700, charcoal
│  +8.3%  vs prev. qtr   │ ← Delta: badge + comparison text
│                         │
└─────────────────────────┘
```

**Figma dimensions:** 336×124px, radius 10px, 18px padding, 1px border `#F0EBE7`

**Accent stripe colour mapping:**
- Referral Volume → Amber `#E69512`
- Provider Activity → Blue `#0D35B8`
- Active Status → Mint `#4DAAAB`
- IPA Tracking → Pastel Purple `#E3DADA`
- Engagement Rate → Green `#277455`
- Critical/Pending → Pink `#C0392B`

### 3.2 Chart Card

```
┌─────────────────────────────────────┐
│ CHART TITLE                          │
│ ┌─────────────────────────────────┐  │
│ │ ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓ │  │
│ │ ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓ │  │
│ │ ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓  ▓▓▓▓ │  │
│ │ Jan   Feb   Mar   Apr   May   │  │ ← Axis labels: Lato 9px
│ └─────────────────────────────────┘  │
└─────────────────────────────────────┘
```

**Figma dimensions:** 884×320px, radius 10px, 24px padding

### 3.3 Status Badge

```
┌─────────────┐  ┌──────────────┐  ┌────────┐
│  OPEN       │  │ UNDER OFFER  │  │ DRAFT  │
│  mint bg    │  │ purple bg    │  │ grey    │
└─────────────┘  └──────────────┘  └────────┘
```

**Figma dimensions:** Auto width, 24px height, radius 100px, padding 3px 10px
**Font:** Lato 9.5px, 700, uppercase

### 3.4 Mini Donut Card

```
┌──────────────────────────────────┐
│ [donut]  OFFERS UNDER ACTIVE     │
│  chart   382                     │
│          Active referrals        │
│          ● 0-7 days: 187         │
│          ● 8-14 days: 124        │
│          ● 15+ days: 71          │
└──────────────────────────────────┘
```

**Figma dimensions:** 573×140px, radius 10px, 20px padding, horizontal layout

### 3.5 Sidebar Navigation

```
┌─────────────────────┐
│ OVERVIEW            │ ← Section header: Lato 9px, 700, uppercase
│ ● Summary Dashboard │ ← Active: weight 600, blue left border
│                     │
│ REFERRALS           │
│ ○ Referral Volume   │ ← Inactive: weight 500, grey
│ ○ Referral Offers   │
│                     │
│ PROVIDERS           │
│ ○ Provider Activity │
│ ○ Provider Registry │
└─────────────────────┘
```

**Figma dimensions:** 220px wide, full height, bg white

---

## 4. POWER BI THEME APPLICATION

The file `WMPP_BCT_Expanded_Theme.json` contains the complete Power BI theme JSON with all tokens mapped. Import via:
```
Power BI Desktop → View → Themes → Browse → Select WMPP_BCT_Expanded_Theme.json
```

### Chart Colour Assignments (dataColors array order)
1. `#0D35B8` — Blue (primary, referral counts)
2. `#E69512` — Amber (secondary, provider metrics)
3. `#277455` — Green (positive/success)
4. `#C0392B` — Pink (critical/alert)
5. `#4DAAAB` — Mint (new: age buckets, "on track")
6. `#E3DADA` — Pastel Purple (new: IPA, "under review")
7. `#2B2B2C` — Charcoal (neutral/dark)
8. `#F0EBE7` — Cream (light contrast)

---

## 5. PAGE-BY-PAGE COLOUR ASSIGNMENT

| Page | Primary Colour | Secondary | Accent |
|------|---------------|-----------|--------|
| Summary Dashboard | Blue `#0D35B8` | Amber `#E69512` | Mint `#4DAAAB` |
| Referral Volume | Amber `#E69512` | Blue `#0D35B8` | Pastel Purple `#E3DADA` |
| Referral Offers | Blue `#0D35B8` | Mint `#4DAAAB` | Pink `#C0392B` |
| Provider Activity | Green `#277455` | Amber `#E69512` | Pastel Purple `#E3DADA` |
| Provider Registry | Amber `#E69512` | Blue `#0D35B8` | Mint `#4DAAAB` |
| Draft & Pending | Pink `#C0392B` | Amber `#E69512` | Mint `#4DAAAB` |
| IPA Tracking | Pastel Purple `#E3DADA` | Mint `#4DAAAB` | Blue `#0D35B8` |
| Spot vs Framework | Blue `#0D35B8` | Amber `#E69512` | Green `#277455` |

---

## 6. FIGMA HANDOFF NOTES

- **Canvas size:** 1920×1080px (fixed, no scrolling)
- **Grid:** 12-column, 20px gutter, 24px margin
- **Component variants:** KPI cards have 5 colour variants (amber, blue, mint, purple, green) controlled via the accent-stripe property
- **Auto-layout:** KPI row uses horizontal auto-layout with 16px gap and "fill container" resizing
- **Latoactive states:** Hover (shadow), active (selected), focus (ring)
- **Data binding:** Use Figma's "Text" and "Instance swap" properties for data-driven variants
- **Typography styles:** 6 text styles pre-defined (Page Title, Chart Title, KPI Value, Table Header, Body, Badge)

---

## 7. MOCKUP FILES

| File | Description |
|------|------------|
| `WMPP_Summary_Dashboard.html` | Latoactive summary dashboard with KPIs, charts, tables |
| `WMPP_BCT_Expanded_Theme.json` | Power BI theme JSON for direct import |

*Additional page mockups can be generated on request.*
