# WMPP Brand Pack — Power BI Report Design Guide

**Project:** West Midlands Placement Portal (WMPP)  
**Organisation:** Birmingham Children's Trust (BCT)  
**Report:** WMPP PILOT DASHBOARD V13 (v0.1 project)
**Semantic model:** `SM_WMPP` — 79 tables, 850 columns, 48 relationships, 95 measures
**Source:** BCT Brand Guidelines v1 PDF, the supplied `brand pack/ideas` imagery, and the v01 PBIP report project

---

## 1. Brand Identity

### Organisation
Birmingham Children's Trust is the organisation hosting the WMPP platform on behalf of the 14 West Midlands Local Authorities. The report carries the BCT logo and branding.

### Brand Source
The colour system is anchored to the official **BCT Brand Guidelines v1** supplied in this repository. The mandala specifies four primary colours: gold `#FCBF00`, orange `#F59E00`, deep orange `#EF7911`, and pale yellow `#FFE672`. The `brand pack/ideas` images add a deep navy `#2E3E71`, sky blue `#AFD9FF`, illustration tint `#F1F8FF`, and a warm orange highlight `#F9B234`. These colours are used for the report theme and the v01 visual overrides.

### Logo Assets (from report)
The report uses the following image assets:
- **BCT_Logo** — Birmingham Children's Trust logo (transparent PNG, used on page headers)
- **NEW_LOGO** — Secondary logo variant (JPG, used on the homepage)
- **boy icon** — Blue boy silhouette (used for Male Referrals gender card)
- **girl icon** — Pink girl silhouette (used for Female Referrals gender card)
- **Asset_2** — Additional decorative asset
- **Unknown** — Additional icon asset

### Logo Description (from website)
The BCT logo features a flower/mandala shape in warm amber and gold tones with a yellow centre. The wordmark "BIRMINGHAM CHILDREN'S TRUST" appears in dark charcoal caps. The logo conveys warmth, growth, and child-centred care.

### Naming Convention
- Report title: `WMPP PILOT DASHBOARD (V13.1)`
- Pages use UPPERCASE display names
- Measures use Title Case with spaces (e.g., `Total Referrals`)

---

## 2. Colour Palette

The palette below combines the four official mandala colours from BCT003 Brand Guidelines v1 with the blue/navy accents sampled from the supplied WMPP systems illustration. The first four colours must remain the dominant BCT identity colours; the supporting colours provide readable data series and status states.

### Official BCT colours

| Colour | Hex | Usage |
|--------|-----|-------|
| Mandala gold | `#FCBF00` | Primary navigation, headline accents, main data series |
| Mandala orange | `#F59E00` | Secondary data series, active selections, warm emphasis |
| Mandala deep orange | `#EF7911` | Tertiary series, hover/pressed states, escalation accent |
| Mandala pale yellow | `#FFE672` | Soft highlights, low-severity bands, background tint |

### Idea-image supporting colours

| Colour | Hex | Usage |
|--------|-----|-------|
| Systems navy | `#2E3E71` | KPI values, headings on light surfaces, hyperlinks |
| Sky blue | `#AFD9FF` | Informational series, illustration accents |
| Illustration tint | `#F1F8FF` | Light blue surfaces and information badges |
| Warm orange highlight | `#F9B234` | Decorative bands inspired by `wmcpp-background.jpg` |
| Charcoal | `#1C1C1A` | Body text, labels, high-contrast values |
| White | `#FFFFFF` | Report canvas and card surfaces |

### Semantic colours

| Colour | Hex | Usage |
|--------|-----|-------|
| Success green | `#3A8B6F` | Positive/completed outcomes |
| Warning gold | `#FCBF00` | At-risk or ageing items |
| Critical red | `#C0392B` | Critical alerts and failed outcomes |
| Border neutral | `#E6E1D7` | Dividers and visual outlines |
| Secondary text | `#5C5A56` | Labels and supporting text |

### Full data colour sequence

Use this sequence for visuals with multiple categories:

```text
#FCBF00, #F59E00, #EF7911, #FFE672, #2E3E71, #AFD9FF,
#C82B5E, #3A8B6F, #C0392B, #1C1C1A, #F9B234, #F1F8FF
```

### Accessibility note

Use charcoal or systems navy for small text. Do not use white text on `#FCBF00` or `#F59E00` for small labels; use charcoal instead. Never rely on colour alone—retain text labels, icons, and status descriptions.

---

## 3. Typography

### Font System

The BCT website uses bold, rounded sans-serif fonts. For Power BI (which has limited font support), we map to the closest available alternatives.

| Text Class | Web Font | PBI Font | Size | Weight | Colour | Usage |
|------------|----------|----------|------|--------|--------|-------|
| **Callout** | Poppins | Poppins (or DIN fallback) | 28px | 700 | `#1C1C1A` | Large KPI numbers on cards |
| **Heading** | Poppins | Poppins Semibold (or DIN fallback) | 18px | 600 | `#1C1C1A` | Page titles, section headers |
| **Title** | Poppins | Poppins (or DIN fallback) | 13px | 600 | `#1C1C1A` | Visual titles, chart titles |
| **Header** | Inter | Segoe UI Semibold | 12px | 600 | `#1C1C1A` | Column headers, table headers |
| **Label** | Inter | Segoe UI | 11px | 500 | `#6B6862` | Axis labels, data labels |
| **Metadata** | Inter | Segoe UI | 11px | 400 | `#A09D97` | Sub-text, timestamps, counts |

### Font Stack
- Primary font: **Poppins** (for KPI values, headings, visual titles) — bold, rounded, warm
- Secondary font: **Inter** (for body text, labels, UI elements) — clean, highly legible
- Power BI fallback: **DIN** → **Segoe UI** → Helvetica, Arial, sans-serif
- Google Fonts import: `https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap`

---

## 4. Design Language

### Visual Character
The BCT brand is warm, approachable, and child-focused. The design language reflects this:

- **Rounded corners** — 8px radius on cards, 20px (pill) on buttons and badges
- **Warm backgrounds** — cream `#F4EFE4` instead of cold grey/white
- **White cards** — clean white surfaces float on the warm cream background
- **Soft shadows** — `0 2px 8px rgba(28,28,26,0.06)` for cards, `0 4px 16px rgba(200,43,94,0.12)` on hover
- **Pill-shaped buttons** — `border-radius: 24px`, amber background, white text
- **Chevron nav rows** — amber `#E8A020` background strips with chevron arrows (matching BCT website)
- **Flower mandala accents** — subtle decorative elements in headers using amber/gold tones

### Page Layout Standards

#### Page Dimensions

The v01 report contains ten pages. Power BI stores the canvas dimensions in the page definition; use those page definitions as the source of truth when editing layout.

| Page | Page ID |
|------|---------|
| PROVIDER REGISTRY | `08ef33dc6a87d1b14392` |
| Duplicate of REFERRALS | `0b9ca7bdee6979c44204` |
| OFFERS OVERVIEW | `1f33996970651e846183` |
| Duplicate of REFERRALS | `285db1ac6285737d2d5b` |
| WMPP HOMEPAGE | `364f2cdd67ba7822850c` |
| IPA OVERVIEW | `58d36c775c032a42e01b` |
| Historic | `7b4c90309550bd42911c` |
| DRAFT OFFERS | `ad5ab4aa6928c9178a35` |
| Page 1 | `ea102595f4e9d503f186` |
| REFERRALS | `f028a4be56d03e8404d7` |

#### Standard Page Structure
```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  WMPP PAGE TITLE                   [NAV PILLS]│  ← Header bar (white, 72px)
├──────────────────────────────────────────────────────────┤
│ [AMBER STRIP] ▸ Here for children...                     │  ← BCT-style nav strip (optional)
├──────────────────────────────────────────────────────────┤
│ [SLICER PILL]  [SLICER PILL]  [TEXT FILTER]   [REFRESH]  │  ← Filter bar (white, 56px)
├──────────────────────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐         │
│ │ KPI │ │ KPI │ │ KPI │ │ KPI │ │ KPI │ │ KPI │         │  ← KPI card row(s)
│ │CARD │ │CARD │ │CARD │ │CARD │ │CARD │ │CARD │         │  (white, 8px radius, amber left border)
│ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘         │
├──────────────────────────────────────────────────────────┤
│ ┌────────────────────┐ ┌────────────────────┐            │
│ │                    │ │                    │            │  ← Chart area
│ │   CHART / TABLE    │ │   CHART / TABLE    │            │  (white cards on cream bg)
│ │                    │ │                    │            │
│ └────────────────────┘ └────────────────────┘            │
├──────────────────────────────────────────────────────────┤
│ [SLIDE NAV: ← Previous | Next →]                         │  ← Bottom navigation
└──────────────────────────────────────────────────────────┘
```

---

## 5. Visual Type Catalogue

The v01 report contains **184 visuals across 10 pages**:

| Visual Type | Count | Purpose |
|------------|------:|---------|
| **cardVisual** | 61 | KPI metric cards |
| **image** | 24 | Logos, people icons, and decorative assets |
| **shape** | 22 | Header bars, dividers, and layout panels |
| **actionButton** | 14 | Navigation and report actions |
| **slicer** | 16 | Date, status, placement, and operational filters |
| **textbox** | 11 | Titles, explanations, and narrative text |
| **tableEx** | 7 | Detail tables |
| **clusteredBarChart** | 5 | Provider/category comparisons |
| **columnChart** | 3 | Activity and engagement trends |
| **donutChart** | 2 | Composition and distribution |
| **clusteredColumnChart** | 1 | Age-band distribution |
| **hundredPercentStackedColumnChart** | 1 | Spot vs framework comparison |
| **funnel** | 1 | IPA conversion workflow |
| **textFilter** | 1 | Provider directory search |
| **Other/legacy containers** | 15 | Containers retained in the v01 PBIR definition |

---

## 6. KPI Card Design Specification

### Standard KPI Card (cardVisual)
```
┌───────────────────────────────────┐
│ ▌                                 │  ← 3px amber left accent bar
│   KPI LABEL                       │  ← 11px Inter, #6B6862, uppercase
│   (e.g., "Total Referrals")       │
│                                   │
│   161                             │  ← 28px Poppins bold, #1C1C1A
│                                   │
│   ▲ 12% vs last period            │  ← 11px Inter, green/red trend
│                                   │
│ ┌─────────────────────────────┐   │  ← Reference label
│ │ Reference label             │   │  (white bg, 8px radius bottom)
│ └─────────────────────────────┘   │
└───────────────────────────────────┘
```

**Specifications:**
- Background: White `#FFFFFF`
- Border: 1px solid `#E0DDD5`
- Border radius: 8px (rounded)
- Cell padding: 14px
- Left accent bar: 3px wide, colour varies by metric type
- Shadow: `0 2px 8px rgba(28,28,26,0.06)`
- Hover shadow: `0 4px 16px rgba(200,43,94,0.12)` (pink-tinted hover glow)
- Reference label background: `#F4EFE4` (cream)

### Accent Bar Colours by Metric Type
| Metric Type | Accent Colour | Hex |
|-------------|---------------|-----|
| Primary volume | Amber/Gold | `#E8A020` |
| Active/positive | Green | `#3A8B6F` |
| Warning/at-risk | Amber | `#E8A020` |
| Critical/alert | Red | `#C0392B` |
| CTA/interactive | Pink/Magenta | `#C82B5E` |
| Informational | Blue | `#2972C4` |

### Gender Cards (special)
- **Male:** Blue circle icon + blue accent `#2972C4`
- **Female:** Pink circle icon + pink accent `#C82B5E`
- **Other:** Amber accent `#E8A020`, no icon

---

## 7. Chart Style Standards

### Bar/Column Charts
- Gridline style: **dotted** (1px dashed `#E0DDD5`)
- Axis titles: **visible** (show = true)
- Bar fill: Primary `#E8A020`, secondary `#C82B5E`, tertiary `#2972C4`
- Bar radius: 4px top corners
- Line stroke width: 3px
- Background: visible, transparent

### Donut/Pie Charts
- Legend: **visible**, position **RightCenter**
- Labels: **"Data value, percent of total"**
- Segment colours: `#E8A020`, `#C82B5E`, `#2972C4`

### Funnel Chart
- Used for IPA conversion workflow
- 3 stages: Successful Offers → IPA Created → IPA Completed
- Decreasing width shows drop-off
- Colour: Amber gradient `#E8A020` → `#D4601A` → `#C0392B`

### Tables (tableEx)
- Header row: Amber `#E8A020` background, white text
- Alternating rows: White `#FFFFFF` / cream `#F9F5EC`
- Hover row: Pink tint `#FCE8EF`
- Status badges: pill-shaped (border-radius: 10px) with tinted bg + semantic colour text
- Expand/collapse buttons: visible
- Row headers with sorting

---

## 8. Navigation

### Action Buttons
Each page has navigation buttons for:
- Previous page / Next page
- Back to Homepage
- Specific page jumps

### Button Style
- **Pill-shaped** — `border-radius: 24px`
- Background: Amber `#E8A020`
- Text: White `#FFFFFF`, 12px Poppins Semibold
- Padding: 8px 20px
- Hover: Darken to `#D4601A`
- Active: Pink `#C82B5E` background
- Positioned in top-right area of each page

### BCT-Style Nav Strips (optional decorative element)
Amber `#E8A020` background strips with chevron arrows, matching the BCT website navigation pattern:
```
▸ Here for children...  ▸ Here for families...  ▸ Here for providers...
```

---

## 9. Slicers / Filters

### Standard Slicers (16 total across report)
| Slicer Type | Pages Used On | Purpose |
|------------|---------------|---------|
| Date range | All data pages | Filter by referral/offer date period |
| Placement type | Referrals, Offers, Draft, IPA | Filter by Residential/Fostering/Supported |
| Status | Offers, Draft | Filter by offer status |

### Slicer Style
- **Pill-shaped** — `border-radius: 20px`
- Background: White `#FFFFFF`
- Border: 1px solid `#E0DDD5`
- Label: 10px Inter, `#A09D97`, uppercase
- Value: 11px Inter, `#1C1C1A`
- Dropdown arrow: `#6B6862`

### Text Filter (custom visual)
- Used on Provider Registry page
- Free-text search for provider names

---

## 10. Shape Elements

### Header Bar (shape)
- Full-width white bar at top of each page
- Contains BCT logo (left) and page title (centre/left)
- Navigation buttons positioned right
- Bottom border: 1px solid `#E0DDD5`

### Section Dividers (shape)
- Horizontal lines separating KPI cards from chart areas
- Thin, subtle colour (`#E0DDD5`)

### Amber Nav Strip (decorative)
- Optional amber `#E8A020` strip below header
- Matches BCT website navigation pattern
- Contains contextual links (e.g., "Here for placement officers...")

---

## 11. Accessibility `[R81]`

### Compliance
- **WCAG 2.0 / 2.1** (consideration for 2.2) — required by R81
- Government accessibility requirements (GDS assessment)

### Colour Contrast
| Text on Background | Ratio | Status |
|-------------------|-------|--------|
| Dark Charcoal `#1C1C1A` on White `#FFFFFF` | 16.2:1 | ✅ AAA |
| Dark Charcoal `#1C1C1A` on Cream `#F4EFE4` | 14.8:1 | ✅ AAA |
| Mid Grey `#6B6862` on White | 5.4:1 | ✅ AA |
| Mid Grey `#6B6862` on Cream | 4.9:1 | ✅ AA |
| White on Amber `#E8A020` | 2.1:1 | ⚠️ Large text only |
| White on Pink `#C82B5E` | 4.6:1 | ✅ AA |
| White on Blue `#2972C4` | 4.8:1 | ✅ AA |
| White on Green `#3A8B6F` | 4.5:1 | ✅ AA |
| White on Red `#C0392B` | 5.2:1 | ✅ AA |

### Notes
- Never rely on colour alone — always include text labels
- Gender cards use icons (boy/girl silhouettes) in addition to colour
- KPI semantic colours (green/amber/red) should have text labels ("Healthy", "At Risk", "Critical")
- Ensure all visuals have titles and axis labels
- White text on amber `#E8A020` fails AA for small text — use dark charcoal `#1C1C1A` text on amber backgrounds instead

---

## 12. Power BI Theme File

A ready-to-import Power BI theme file is provided at:
`brand pack/WMPP_Brand_Theme.json`

**To import:**
1. Open Power BI Desktop
2. View → Themes → Browse for themes
3. Select `WMPP_Brand_Theme.json`
4. Click Apply

This will apply all colours, fonts, and visual styles defined in this brand pack.

---

## 13. Page-by-Page Design Specifications

### Page 1: WMPP HOMEPAGE
**Dimensions:** 1284 x 1000 | **Visuals:** 2
- Large BCT logo centred on cream background
- "Enter Dashboard" pill button (pink `#C82B5E`)
- Functional ref: R24

### Page 2: REFERRALS `[R24, R51]`
**Dimensions:** 1500 x 1500 | **Visuals:** 36

**KPI Cards (9):**
| Card | Example Value | Accent Colour |
|------|---------------|---------------|
| Total Referrals | 161 | Amber `#E8A020` |
| Active | 72 | Green `#3A8B6F` |
| Under Offer | 8 | Pink `#C82B5E` |
| Awaiting Offers | 64 | Amber `#E8A020` |
| Closed/Cancelled | 42 | Red `#C0392B` |
| Offer Rate % | 68% | Blue `#2972C4` |
| Male Referrals | — | Blue `#2972C4` |
| Female Referrals | — | Pink `#C82B5E` |
| Other Referrals | — | Amber `#E8A020` |

**NEW KPIs (from functional gaps):**
| Card | Functional Ref | Accent |
|------|---------------|--------|
| Emergency Referrals | R18, R57 | Red `#C0392B` |
| Emergency Rate % | R18 | Blue `#2972C4` |
| Planned Referrals | R57 | Green `#3A8B6F` |
| Out-of-Region | R22 | Pink `#C82B5E` |

**Charts:**
- Donut: Placement type distribution (amber/pink/blue segments)
- Column: Monthly activity trends
- Bar: Referral closure reasons

### Page 3: OFFERS OVERVIEW `[R24-R29, R51]`
**Dimensions:** 1500 x 1250 | **Visuals:** 23

**KPI Cards (12):** Active Referrals (106), With Offers (55), Awaiting (51), Offer Rate (52%), Total Offers (427), Avg/Ref (2.74), Providers (86), Avg/Provider (4.97), Successful (10), Unsuccessful (40), Draft (162), Pending (377)

**Charts:**
- 100% Stacked Column: Spot vs Framework (amber vs pink)
- Clustered Bar: Provider ranking

### Page 4: DRAFT OFFERS `[R24]`
**Dimensions:** 1500 x 1100 | **Visuals:** 24

**KPI Cards (6):** Draft Count (166), No Activity (165), With Activity (1), 14+ Days (114), Avg Days (—), No Activity % (99%)

**Colour Coding for Age Bands:**
| Age Band | Colour | Hex |
|----------|--------|-----|
| 0–7 Days | Green | `#3A8B6F` |
| 8–14 Days | Amber | `#E8A020` |
| 15–30 Days | Orange | `#D4601A` |
| 30+ Days | Red | `#C0392B` |

### Page 5: IPA OVERVIEW `[R35, R28]`
**Dimensions:** 1500 x 1500 | **Visuals:** 27

**KPI Cards (9):** Successful (10), IPA Created (6), IPA Completed (1), Pending (5), Awaiting IPA (4), Accepted→IPA (60%), Still to Progress (40%), Created→Completed (17%), Successful→Completed (10%)

**Charts:**
- Funnel: Successful Offers → IPA Created → IPA Completed (amber gradient)

**NEW KPIs:** Weekly Fee Liability [R62], Payment Method [R62], Signature Status [R20, R35]

### Page 6: PROVIDER REGISTRY `[R91, R93, R95, R96]`
**Dimensions:** 1500 x 1100 | **Visuals:** 19

**KPI Cards (7):** Providers Registered, Homes Registered, Fostering, Residential, Supported Accommodation, Framework, Non-Framework

**Charts:**
- Clustered Bar: Providers by service type
- Table: Provider directory with text filter

**NEW KPIs:** QA Flags [R41], Due Diligence [R49], Onboarding Pipeline [R59]

---

## 14. Requirements Coverage by Page

| Page | Requirements Covered | New Requirements to Add |
|------|---------------------|------------------------|
| WMPP HOMEPAGE | R24 | — |
| REFERRALS | R24, R51, R13 | R18, R57, R22 (emergency/out-of-region) |
| Duplicate of REFERRALS (0b9c…) | Same as REFERRALS | Confirm whether retained for authoring only |
| Duplicate of REFERRALS (285d…) | Same as REFERRALS | Confirm whether retained for authoring only |
| OFFERS OVERVIEW | R24-R29, R51, R67, R68 | R14 (messaging KPIs) |
| DRAFT OFFERS | R24 | — |
| IPA OVERVIEW | R28, R35 | R62, R20 (finance, audit) |
| PROVIDER REGISTRY | R91, R93, R95, R96 | R41, R49, R59 (QA, diligence, onboarding) |
| Historic | — | R47, R48 (document compliance) |
| Page 1 | — | Confirm whether retained as a working page |

---

## 15. Implementation Checklist

- [ ] Import `WMPP_Brand_Theme.json` into Power BI Desktop
- [ ] Upload BCT logo to report as image resource
- [ ] Upload boy/girl icons for gender cards
- [ ] Validate the 10 v01 pages and their page IDs from Section 4
- [ ] Add header bar with BCT logo on each page (white/cream surface)
- [ ] Add pill-shaped navigation buttons (gold/orange background, charcoal text)
- [ ] Create KPI cards per page specifications (8px radius, 3px accent bar)
- [ ] Apply semantic colours (green/gold/red) to status-based cards
- [ ] Add pill-shaped slicers to all data pages
- [ ] Create charts using the BCT gold/orange/deep-orange and idea-image navy/blue sequence
- [ ] Set table headers to gold/orange background with charcoal text
- [ ] Verify colour contrast meets WCAG AA standards
- [ ] Add text labels to all colour-coded visuals
- [ ] Test text filter on Provider Registry page
- [ ] Add new KPIs for functional gaps (emergency, QA, finance, docs)
- [ ] Verify all 95 v01 semantic-model measures are documented in `WMPP_Semantic_Model_Measures.md`
- [ ] Validate `Closed_Date` remains blank when no related `has_offer = TRUE()` row exists
- [ ] Publish to Fabric workspace and connect to gold lakehouse tables

---

## 16. Brand Colour Reference Card

```
┌──────────────────────────────────────────────┐
│  BCT BRAND PALETTE                            │
│                                               │
│  ████████  Mandala Gold      #FCBF00  Primary │
│  ████████  Mandala Orange    #F59E00  Warm    │
│  ████████  Deep Orange       #EF7911  Accent  │
│  ████████  Pale Yellow       #FFE672  Soft    │
│  ████████  Systems Navy      #2E3E71  KPI     │
│  ████████  Sky Blue          #AFD9FF  Info    │
│  ████████  Charcoal          #1C1C1A  Text    │
│  ████████  Success Green     #3A8B6F  Positive│
│  ████████  Critical Red      #C0392B  Alert   │
│  ████████  White             #FFFFFF  Canvas  │
│                                               │
│  Typography: Poppins (headings) / Inter (body)│
└──────────────────────────────────────────────┘
```

The complete current measure catalogue and `Closed_Date` implementation note are in [`WMPP_Semantic_Model_Measures.md`](WMPP_Semantic_Model_Measures.md). The importable theme is [`WMPP_Brand_Theme.json`](WMPP_Brand_Theme.json), and the report project contains the same palette in its embedded base theme.
