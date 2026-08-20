# WMPP Dashboard — Design System v2.0
## Figma Design Specification

### Brand: Birmingham Children's Trust (BCT) — Expanded Palette

---

## 1. COLOUR SYSTEM

### Core Palette (BCT)

| Token | Hex | CSS Variable | Usage |
|-------|-----|-------------|-------|
| Cream | `#F4EFE4` | `--cream` | Page background, warm neutral |
| Amber | `#E8A020` | `--amber` | Primary CTA, warnings, charts series 2 |
| Pink | `#C82B5E` | `--pink` | Critical alerts, charts series 4 |
| Blue | `#2972C4` | `--blue` | Navigation, links, charts series 1 |
| Charcoal | `#1C1C1A` | `--charcoal` | Primary text, dark surfaces |
| Green | `#3A8B6F` | `--green` | Success, positive deltas |
| Red | `#C0392B` | `--red` | Errors, negative sentiment |

### NEW: Expanded Palette

| Token | Hex | CSS Variable | Usage |
|-------|-----|-------------|-------|
| **Mint** | `#7BD3B8` | `--mint` | New KPI accent, age bucket 0-7 days, "On Track" status |
| **Mint Dark** | `#5DB89A` | `--mint-dark` | Mint text on light bg |
| **Mint Light** | `#B8F0DE` | `--mint-light` | Mint background tint |
| **Pastel Purple** | `#B8A9E8` | `--pastel-purple` | IPA KPI accent, age bucket 8-14 days, "Under Review" status |
| **Pastel Purple Dark** | `#9B8AD4` | `--pastel-purple-dark` | Purple text on light bg |
| **Pastel Purple Light** | `#D8D0F4` | `--pastel-purple-light` | Purple background tint |

### Neutral Tones

| Token | Hex | Usage |
|-------|-----|-------|
| Neutral 50 | `#F8F5F0` | Table alternate rows, subtle surface |
| Neutral 100 | `#F4EFE4` | Page background |
| Neutral 200 | `#E8E4D8` | Borders, dividers |
| Neutral 600 | `#6B6B63` | Secondary text |
| Neutral 700 | `#4A4A42` | Muted text |

### Semantic Colours

| Status | Hex | Badge Text |
|--------|-----|------------|
| Positive / On Track | `#3A8B6F` | White |
| Warning / At Risk | `#E8A020` | Charcoal |
| Negative / Critical | `#C0392B` | White |
| Info | `#2972C4` | White |
| New / Draft | `#7BD3B8` | Charcoal |
| Under Review | `#B8A9E8` | Charcoal |

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

**Figma dimensions:** 336×124px, radius 10px, 18px padding, 1px border `#E8E4D8`

**Accent stripe colour mapping:**
- Referral Volume → Amber `#E8A020`
- Provider Activity → Blue `#2972C4`
- Active Status → Mint `#7BD3B8`
- IPA Tracking → Pastel Purple `#B8A9E8`
- Engagement Rate → Green `#3A8B6F`
- Critical/Pending → Pink `#C82B5E`

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
1. `#2972C4` — Blue (primary, referral counts)
2. `#E8A020` — Amber (secondary, provider metrics)
3. `#3A8B6F` — Green (positive/success)
4. `#C82B5E` — Pink (critical/alert)
5. `#7BD3B8` — Mint (new: age buckets, "on track")
6. `#B8A9E8` — Pastel Purple (new: IPA, "under review")
7. `#1C1C1A` — Charcoal (neutral/dark)
8. `#F4EFE4` — Cream (light contrast)

---

## 5. PAGE-BY-PAGE COLOUR ASSIGNMENT

| Page | Primary Colour | Secondary | Accent |
|------|---------------|-----------|--------|
| Summary Dashboard | Blue `#2972C4` | Amber `#E8A020` | Mint `#7BD3B8` |
| Referral Volume | Amber `#E8A020` | Blue `#2972C4` | Pastel Purple `#B8A9E8` |
| Referral Offers | Blue `#2972C4` | Mint `#7BD3B8` | Pink `#C82B5E` |
| Provider Activity | Green `#3A8B6F` | Amber `#E8A020` | Pastel Purple `#B8A9E8` |
| Provider Registry | Amber `#E8A020` | Blue `#2972C4` | Mint `#7BD3B8` |
| Draft & Pending | Pink `#C82B5E` | Amber `#E8A020` | Mint `#7BD3B8` |
| IPA Tracking | Pastel Purple `#B8A9E8` | Mint `#7BD3B8` | Blue `#2972C4` |
| Spot vs Framework | Blue `#2972C4` | Amber `#E8A020` | Green `#3A8B6F` |

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
