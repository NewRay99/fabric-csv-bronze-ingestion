# WMPP Brand Pack — Power BI Report Design Guide

**Project:** West Midlands Placement Portal (WMPP)  
**Organisation:** Birmingham Children's Trust (BCT)  
**Report:** WMPP PILOT DASHBOARD (V13.1)  
**Date:** 10 July 2026  
**Source:** Extracted from the actual Power BI report theme (CY26SU02.json), visual structure, and KPI Logic Document

---

## 1. Brand Identity

### Organisation
Birmingham Children's Trust is the organisation hosting the WMPP platform on behalf of the 14 West Midlands Local Authorities. The report carries the BCT logo and branding.

### Logo Assets (from report)
The report uses the following image assets:
- **BCT_Logo** — Birmingham Children's Trust logo (transparent PNG, used on page headers)
- **NEW_LOGO** — Secondary logo variant (JPG, used on the homepage)
- **boy icon** — Blue boy silhouette (used for Male Referrals gender card)
- **girl icon** — Pink girl silhouette (used for Female Referrals gender card)
- **Asset_2** — Additional decorative asset
- **Unknown** — Additional icon asset

### Naming Convention
- Report title: `WMPP PILOT DASHBOARD (V13.1)`
- Pages use UPPERCASE display names
- Measures use Title Case with spaces (e.g., `Total Referrals`)

---

## 2. Colour Palette

All colours are extracted from the actual report theme JSON (`CY26SU02.json`).

### Primary Colours

| Colour | Hex | Usage |
|--------|-----|-------|
| 🔵 Primary Blue | `#118DFF` | Table accent, max values, primary data series |
| 🟦 Dark Blue | `#12239E` | Secondary data series, headers |
| 🟠 Orange | `#E66C37` | Tertiary data series, highlights |
| 🟣 Purple | `#6B007B` | Quaternary data series |
| 🩷 Pink | `#E044A7` | Quinary data series |

### Semantic Colours

| Colour | Hex | Usage |
|--------|-----|-------|
| 🟢 Good/Success | `#1AAB40` | Positive KPIs, successful outcomes |
| 🟡 Neutral/Warning | `#D9B300` | At-risk items, aging alerts |
| 🔴 Bad/Error | `#D64554` | Critical alerts, failures, expired docs |
| 🔵 Maximum | `#118DFF` | Heat map maximum |
| 🟡 Centre | `#D9B300` | Heat map midpoint |
| ⚪ Minimum | `#DEEFFF` | Heat map minimum |
| 🟠 Null | `#FF7F48` | Null/missing data |

### UI Colours

| Colour | Hex | Usage |
|--------|-----|-------|
| Background | `#FFFFFF` | Page background |
| Background Light | `#F3F2F1` | Card backgrounds, alternating rows |
| Background Neutral | `#C8C6C4` | Borders, dividers |
| Foreground | `#252423` | Primary text colour |
| Foreground Secondary | `#605E5C` | Secondary text, labels |
| Foreground Tertiary | `#B3B0AD` | Tertiary text, placeholders |
| Hyperlink | `#0078D4` | Links, interactive elements |

### Full Data Colour Sequence (20 colours)
Used in order for charts with many categories:
```
#118DFF, #12239E, #E66C37, #6B007B, #E044A7,
#744EC2, #D9B300, #D64550, #197278, #1AAB40,
#15C6F4, #4092FF, #FFA058, #BE5DC9, #F472D0,
#B5A1FF, #C4A200, #FF8080, #00DBBC, #5BD667
```

---

## 3. Typography

Extracted from `textClasses` in the theme JSON:

| Text Class | Font | Size | Colour | Usage |
|-----------|------|------|--------|-------|
| **Callout** | DIN | 24px | `#252423` | Large KPI numbers on cards |
| **Title** | DIN | 12px | `#252423` | Visual titles |
| **Header** | Segoe UI Semibold | 12px | `#252423` | Column headers, table headers |
| **Label** | Segoe UI | 10px | `#252423` | Axis labels, data labels, small text |

### Font Stack
- Primary font: **DIN** (for KPI values and visual titles)
- Secondary font: **Segoe UI** / **Segoe UI Semibold** (for headers, labels, UI text)
- Fallback: Helvetica, Arial, sans-serif

---

## 4. Page Layout Standards

### Page Dimensions
| Page | Width | Height | Canvas |
|-------|-------|--------|--------|
| WMPP HOMEPAGE | 1284 | 1000 | Landscape 16:9 |
| REFERRALS | 1500 | 1500 | Large landscape |
| OFFERS OVERVIEW | 1500 | 1250 | Landscape |
| DRAFT OFFERS | 1500 | 1100 | Landscape |
| IPA OVERVIEW | 1500 | 1500 | Large landscape |
| PROVIDER REGISTRY | 1500 | 1100 | Landscape |
| Historic | 1280 | 720 | Standard 16:9 |

### Standard Page Structure
```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  WMPP PAGE TITLE                   [NAV BUTTONS]│  ← Header band (80px)
├──────────────────────────────────────────────────────────┤
│ [SLICER]  [SLICER]  [TEXT FILTER]                        │  ← Filter bar (60px)
├──────────────────────────────────────────────────────────┤
│ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐         │
│ │ KPI │ │ KPI │ │ KPI │ │ KPI │ │ KPI │ │ KPI │         │  ← KPI card row(s)
│ │CARD │ │CARD │ │CARD │ │CARD │ │CARD │ │CARD │         │
│ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘ └─────┘         │
├──────────────────────────────────────────────────────────┤
│ ┌────────────────────┐ ┌────────────────────┐            │
│ │                    │ │                    │            │  ← Chart area
│ │   CHART / TABLE    │ │   CHART / TABLE    │            │
│ │                    │ │                    │            │
│ └────────────────────┘ └────────────────────┘            │
├──────────────────────────────────────────────────────────┤
│ [SHAPE DIVIDER]                                          │  ← Visual separator
├──────────────────────────────────────────────────────────┤
│ ┌────────────────────┐ ┌────────────────────┐            │
│ │   CHART / TABLE    │ │   CHART / TABLE    │            │  ← Secondary chart area
│ └────────────────────┘ └────────────────────┘            │
└──────────────────────────────────────────────────────────┘
```

---

## 5. Visual Type Catalogue

The report uses the following visual types (135 total across 7 pages):

| Visual Type | Count | Purpose |
|------------|-------|---------|
| **cardVisual** | 43 | KPI metric cards with large numbers |
| **image** | 18 | Logos, icons (boy/girl), decorative shapes |
| **shape** | 17 | Section dividers, header bars, decorative panels |
| **actionButton** | 12 | Navigation buttons between pages |
| **slicer** | 10 | Date range, placement type, status filters |
| **textbox** | 8 | Page titles, section headers, descriptive text |
| **tableEx** | 5 | Detailed data tables with sorting |
| **clusteredBarChart** | 4 | Provider rankings, category comparisons |
| **donutChart** | 1 | Referral placement type distribution |
| **columnChart** | 1 | Monthly referral activity trends |
| **clusteredColumnChart** | 1 | Draft offer age distribution |
| **hundredPercentStackedColumnChart** | 1 | Spot vs Framework comparison |
| **funnel** | 1 | IPA conversion funnel |
| **textFilter** | 1 | Free-text search filter for provider directory |

---

## 6. Page-by-Page Design Specifications

### Page 1: WMPP HOMEPAGE
**Dimensions:** 1284 x 1000 | **Visuals:** 2

```
┌──────────────────────────────────────────────────┐
│                                                  │
│              [NEW_LOGO - large]                   │
│                                                  │
│         ┌─────────────────────────┐               │
│         │   ENTER DASHBOARD       │  ← actionBtn  │
│         └─────────────────────────┘               │
│                                                  │
└──────────────────────────────────────────────────┘
```
- **image:** Large NEW_LOGO centred on page
- **actionButton:** "Enter Dashboard" — navigates to REFERRALS page
- **Functional ref:** R24 (dashboard for placement officers)

### Page 2: REFERRALS `[R24, R51]`
**Dimensions:** 1500 x 1500 | **Visuals:** 36

```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  REFERRALS                        [NAV BUTTONS]│
├──────────────────────────────────────────────────────────┤
│ [DATE SLICER]  [PLACEMENT TYPE SLICER]                    │
├──────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│ │Total │ │Active│ │Under │ │Await │ │Closed│ │Offer │   │
│ │Referr│ │Referr│ │Offer │ │Offers│ │Referr│ │Rate %│   │
│ │ 161  │ │  72  │ │   8  │ │  64  │ │  42  │ │ 68%  │   │
│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│                                                          │
│ ┌──────┐ ┌──────┐ ┌──────┐                              │
│ │ Male │ │Female│ │Other │  ← Gender cards with icons   │
│ │ [boy]│ │[girl]│ │      │                              │
│ └──────┘ └──────┘ └──────┘                              │
│                                                          │
│ ┌─────────────────────┐ ┌────────────────────────────┐  │
│ │  DONUT CHART        │ │  COLUMN CHART              │  │
│ │  Placement Type     │ │  Monthly Referral Activity │  │
│ │  Distribution       │ │  (status trends over time) │  │
│ │                     │ │                            │  │
│ │  Residential: 40%  │ │  ████  ██  ████  ██  ████ │  │
│ │  Fostering:  35%   │ │  Open  Closed  Cancelled    │  │
│ │  Supported:  25%   │ │                            │  │
│ └─────────────────────┘ └────────────────────────────┘  │
│                                                          │
│ ┌─────────────────────┐ ┌────────────────────────────┐  │
│ │  CLUSTERED BAR CHART│ │  TABLE                      │  │
│ │  Referral Closure   │ │  Referral detail list       │  │
│ │  Reasons            │ │  (referral_id, status, date) │  │
│ └─────────────────────┘ └────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**KPI Cards (12):**
| Card | Measure | Example Value | Colour |
|------|---------|---------------|--------|
| Total Referrals | `mv_total_referrals` | 161 | Primary Blue `#118DFF` |
| Active Referrals | `mv_referrals_currently_active` | 72 | Green `#1AAB40` |
| Under Offer | `mv_active_under_offer` | 8 | Orange `#E66C37` |
| Awaiting Offers | `mv_active_awaiting_offers` | 64 | Yellow `#D9B300` |
| Closed/Cancelled | `mv_referrals_closed` | 42 | Red `#D64554` |
| Offer Rate % | `mv_referrals_received_offers` | 68% | Primary Blue |
| Male Referrals | `mv_gender_referrals` (M) | — | Blue `#118DFF` |
| Female Referrals | `mv_gender_referrals` (F) | — | Pink `#E044A7` |
| Other Referrals | `mv_gender_referrals` (Other) | — | Purple `#6B007B` |

**Charts:**
- **Donut Chart:** Placement type distribution (Residential / Fostering / Supported Accommodation) — legend on right, labels show "Data value, percent of total"
- **Column Chart:** Monthly referral activity trends — dotted gridlines, axis titles visible
- **Clustered Bar Chart:** Referral closure reasons — horizontal bars sorted by count

**NEW KPIs to add (from functional gaps):**
| Card | Measure | Functional Ref |
|------|---------|---------------|
| Emergency Referrals | `mv_emergency_referrals` | R18, R57 |
| Emergency Rate % | `mv_emergency_placement_rate` | R18 |
| Planned Referrals | `mv_planned_referrals` | R57 |
| Out-of-Region | `mv_out_of_region_referrals` | R22 |

**Functional requirements covered:** R24, R51, R18, R57, R22, R13

---

### Page 3: OFFERS OVERVIEW `[R24-R29, R51]`
**Dimensions:** 1500 x 1250 | **Visuals:** 23

```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  OFFERS OVERVIEW                  [NAV BUTTONS]│
├──────────────────────────────────────────────────────────┤
│ [DATE SLICER]  [PLACEMENT TYPE SLICER]                    │
├──────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Active│ │With  │ │Await │ │Offer │                     │
│ │Referr│ │Offers│ │First │ │Rate %│                     │
│ │ 106  │ │  55  │ │  51  │ │ 52%  │                     │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Total │ │Avg   │ │Providers│ │Avg  │                    │
│ │Offers│ │Offers│ │Who Made │ │Offers│                    │
│ │ 427  │ │/Ref  │ │ Offers  │ │/Prov │                    │
│ │      │ │ 2.74 │ │   86   │ │ 4.97 │                    │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Succes│ │Unsuc │ │Draft │ │Pendin│                     │
│ │Offers│ │Offers│ │Offers│ │Offers│                     │
│ │  10  │ │  40  │ │ 162  │ │ 377  │                     │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐  │
│ │  100% STACKED COLUMN CHART                          │  │
│ │  Spot vs Framework Offers                           │  │
│ │  ████  ████  ████  ████  ████                       │  │
│ │  Spot (orange) vs Framework (blue)                  │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐  │
│ │  CLUSTERED BAR CHART                                │  │
│ │  Provider Ranking (top providers by offer count)    │  │
│ │  Provider A ████████████████  15                    │  │
│ │  Provider B ███████████       11                    │  │
│ │  Provider C ████████          8                     │  │
│ └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**KPI Cards (8):**
| Card | Measure | Example Value | Colour |
|------|---------|---------------|--------|
| Active Referrals | `mv_referrals_currently_active` | 106 | Green |
| Referrals With Offers | `mv_referrals_with_offers` | 55 | Primary Blue |
| Awaiting First Offer | `mv_active_awaiting_offers` | 51 | Yellow |
| Offer Rate % | — | 52% | Primary Blue |
| Total Offers Made | `mv_total_offers_made` | 427 | Primary Blue |
| Avg Offers/Referral | `mv_avg_offers_per_referral` | 2.74 | Orange |
| Providers Who Made Offers | `mv_providers_who_made_offers` | 86 | Purple |
| Avg Offers/Provider | `mv_avg_offers_per_provider` | 4.97 | Orange |
| Successful Offers | `mv_offer_status_counts` (ACCEPTED) | 10 | Green `#1AAB40` |
| Unsuccessful Offers | `mv_offer_status_counts` (DECLINED) | 40 | Red `#D64554` |
| Draft Offers | `mv_offer_status_counts` (DRAFT) | 162 | Yellow `#D9B300` |
| Pending Offers | `mv_offer_status_counts` (PENDING) | 377 | Orange `#E66C37` |

**Charts:**
- **100% Stacked Column Chart:** Spot vs Framework comparison — uses `mv_spot_vs_framework`
- **Clustered Bar Chart:** Provider ranking by offer count — uses `mv_offers_per_provider`

**Functional requirements covered:** R24, R25, R26, R27, R28, R29, R51, R67, R68

---

### Page 4: DRAFT OFFERS `[R24]`
**Dimensions:** 1500 x 1100 | **Visuals:** 24

```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  DRAFT OFFERS                     [NAV BUTTONS]│
├──────────────────────────────────────────────────────────┤
│ [DATE SLICER]  [PLACEMENT TYPE SLICER]                    │
├──────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐   │
│ │Draft │ │No    │ │With  │ │No    │ │14+   │ │No    │   │
│ │Count │ │Activ.│ │Activ.│ │Activ.│ │Days  │ │Activ.%│  │
│ │ 166  │ │ 165  │ │   1  │ │ 114  │ │ 114  │ │ 99%  │   │
│ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘ └──────┘   │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐  │
│ │  CLUSTERED COLUMN CHART                             │  │
│ │  Draft Offer Age Distribution                       │  │
│ │                                                      │  │
│ │  ████  ████  ████  ████                             │  │
│ │  0-7d  8-14d 15-30d 30+d                            │  │
│ │  (green)(yellow)(orange)(red)                       │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐  │
│ │  TEXT BOX: "Average Days in Draft: X | Oldest: Y"   │  │
│ └─────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**KPI Cards (6):**
| Card | Measure | Example Value | Colour |
|------|---------|---------------|--------|
| Draft Offer Count | `mv_draft_offers.draft_offer_count` | 166 | Yellow |
| No Activity Since Creation | `mv_draft_offers.draft_no_activity` | 165 | Red |
| With Activity Since Creation | `mv_draft_offers.draft_with_activity` | 1 | Green |
| No Activity 14+ Days | `mv_draft_offers.draft_14plus_days` | 114 | Red `#D64554` |
| Average Days in Draft | `mv_draft_offers.avg_days_in_draft` | — | Orange |
| No Activity % | `mv_draft_offers.draft_no_activity_pct` | 99% | Red |

**Colour Coding for Age Bands:**
| Age Band | Colour | Semantic |
|----------|--------|----------|
| 0–7 Days | Green `#1AAB40` | Healthy pipeline |
| 8–14 Days | Yellow `#D9B300` | At risk |
| 15–30 Days | Orange `#E66C37` | Outside timeframe |
| 30+ Days | Red `#D64554` | Critical pipeline |

**Functional requirements covered:** R24

---

### Page 5: IPA OVERVIEW `[R35, R28]`
**Dimensions:** 1500 x 1500 | **Visuals:** 27

```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  IPA OVERVIEW                     [NAV BUTTONS]│
├──────────────────────────────────────────────────────────┤
│ [DATE SLICER]  [PLACEMENT TYPE SLICER]                    │
├──────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Succes│ │IPA   │ │IPA   │ │IPAs  │                     │
│ │Offers│ │Created│ │Compl.│ │Pendin│                    │
│ │  10  │ │   6  │ │   1  │ │   5  │                     │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Offers│ │Accept│ │Offers│ │IPA   │                     │
│ │Await.│ │to IPA│ │Still │ │Cread │                     │
│ │IPA   │ │Create│ │to Pro│ │to Com│                     │
│ │  4   │ │ 60%  │ │ 40%  │ │ 17%  │                     │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌─────────────────────────────────────────────────────┐  │
│ │  FUNNEL CHART                                        │  │
│ │                                                      │  │
│ │  ████████████████████████████  Successful Offers (10)│  │
│ │     ███████████████         IPA Created (6)         │  │
│ │        ███                   IPA Completed (1)      │  │
│ └─────────────────────────────────────────────────────┘  │
│                                                          │
│ ┌─────────────────────┐ ┌────────────────────────────┐  │
│ │  TABLE              │ │  TABLE                     │  │
│ │  IPA Detail List    │ │  Conversion Rates          │  │
│ │  (ipa_id, status,   │ │  (Accepted→Created: 60%,  │  │
│ │   signatures)       │ │   Created→Completed: 17%, │  │
│ │                     │ │   Successful→Completed: 10%)│  │
│ └─────────────────────┘ └────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**KPI Cards (9):**
| Card | Measure | Example Value | Colour |
|------|---------|---------------|--------|
| Successful Offers | `mv_ipa_funnel.successful_offers` | 10 | Green |
| IPA Created | `mv_ipa_funnel.ipa_created` | 6 | Primary Blue |
| IPA Completed | `mv_ipa_funnel.ipa_completed` | 1 | Green |
| IPAs Pending Completion | `mv_ipa_funnel.ipa_pending_completion` | 5 | Yellow |
| Offers Awaiting IPA Creation | `mv_ipa_funnel.offers_awaiting_ipa_creation` | 4 | Orange |
| Accepted to IPA Created % | `mv_ipa_conversion_rates.accepted_to_ipa_created_pct` | 60% | Primary Blue |
| Offers Still to Progress % | `mv_ipa_conversion_rates.offers_still_to_progress_pct` | 40% | Orange |
| IPA Created to Completion % | `mv_ipa_conversion_rates.ipa_created_to_completion_pct` | 17% | Yellow |
| Successful to Completed % | `mv_ipa_conversion_rates.successful_to_completed_pct` | 10% | Red |

**Charts:**
- **Funnel Chart:** IPA workflow funnel — Successful Offers → IPA Created → IPA Completed
- **Tables:** IPA detail list and conversion rate breakdown

**NEW KPIs to add (from functional gaps):**
| Card | Measure | Functional Ref |
|------|---------|---------------|
| Weekly Fee Liability | `mv_weekly_fee_liability` | R62 |
| Payment Method Breakdown | `mv_payment_method_breakdown` | R62 |
| IPA Signature Status | `mv_ipa_signature_status` | R20, R35 |

**Functional requirements covered:** R28, R35, R62, R20

---

### Page 6: PROVIDER REGISTRY `[R91, R93, R95, R96]`
**Dimensions:** 1500 x 1100 | **Visuals:** 19

```
┌──────────────────────────────────────────────────────────┐
│ [BCT LOGO]  PROVIDER REGISTRY               [NAV BUTTONS]│
├──────────────────────────────────────────────────────────┤
│ [TEXT FILTER: Search providers...]  [SERVICE TYPE SLICER]  │
├──────────────────────────────────────────────────────────┤
│ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐                     │
│ │Provi-│ │Homes │ │Foster│ │Resid.│                     │
│ │ders  │ │Regist│ │Provi-│ │Homes │                     │
│ │Regist│ │      │ │ders │ │      │                     │
│ └──────┘ └──────┘ └──────┘ └──────┘                     │
│                                                          │
│ ┌──────┐ ┌──────┐ ┌──────┐                               │
│ │Supp. │ │Frame-│ │Non-  │                               │
│ │Accom.│ │work  │ │Frame.│                               │
│ │Homes │ │Provi.│ │Provi.│                               │
│ └──────┘ └──────┘ └──────┘                               │
│                                                          │
│ ┌─────────────────────┐ ┌────────────────────────────┐  │
│ │  CLUSTERED BAR CHART│ │  TABLE                     │  │
│ │  Providers by       │ │  Provider Directory        │  │
│ │  Service Type       │ │  (name, status, type, homes)│  │
│ │                     │ │  [Text filter for search]   │  │
│ │  Fostering ████  12 │ │                            │  │
│ │  Residenti ███   8  │ │  Sortable columns:         │  │
│ │  Supported ██    5  │ │  - Provider Name           │  │
│ │                     │ │  - Status (Approved/Pending)│  │
│ └─────────────────────┘ └────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

**KPI Cards (4):**
| Card | Measure | Colour |
|------|---------|--------|
| Providers Registered | `mv_provider_registry.providers_registered` | Primary Blue |
| Homes Registered | `mv_provider_homes` (sum) | Primary Blue |
| Fostering Providers | `mv_provider_homes` (Fostering) | Purple `#6B007B` |
| Residential Homes | `mv_provider_homes` (Residential) | Orange `#E66C37` |

**Charts:**
- **Clustered Bar Chart:** Providers by service type
- **Table:** Provider directory with text filter — name, status, service type, homes count

**NEW KPIs to add (from functional gaps):**
| Card | Measure | Functional Ref |
|------|---------|---------------|
| Providers with QA Flags | `mv_providers_with_qa_flags` | R41 |
| QA Flag Type Breakdown | `mv_qa_flag_type_breakdown` | R41 |
| Due Diligence Status | `mv_provider_due_diligence` | R49 |
| Onboarding Pipeline | `mv_provider_onboarding_pipeline` | R59 |

**Functional requirements covered:** R41, R46, R49, R59, R91, R93, R95, R96

---

### Page 7: Historic
**Dimensions:** 1280 x 720 | **Visuals:** 4

Simple summary page with 4 KPI cards showing historical totals.

---

## 7. KPI Card Design Specification

### Standard KPI Card (cardVisual)
```
┌───────────────────────────┐
│  ┌───┐                    │
│  │IMG│  KPI LABEL         │  ← 10px Segoe UI, foreground
│  └───┘  (e.g., "Total Referrals") │
│                           │
│         161               │  ← 24px DIN, foreground (#252423)
│                           │
│  ┌───────────────────┐    │
│  │ Reference label   │    │  ← backgroundLight (#F3F2F1)
│  │ "vs. last month"  │    │  ← rounded bottom corners (4px)
│  └───────────────────┘    │
└───────────────────────────┘
```

**Specifications:**
- Cell padding: 12px
- Image position: Left
- Image area size: 20px
- Background: Show (true)
- Rounded corners: 4px
- Reference label background: `#F3F2F1` (backgroundLight)
- Reference label detail background: `#252423` (foreground)
- Reference label detail font: `#FFFFFF` (background/inverted)

### Gender Cards (special)
- **Male:** Blue boy icon (`boy7123444918221673.png`) + blue accent
- **Female:** Pink girl icon (`girl5491708265852747.png`) + pink accent
- **Other:** Purple accent, no icon

---

## 8. Chart Style Standards

### Bar/Column Charts
- Gridline style: **dotted**
- Axis titles: **visible** (show = true)
- Category axis: concatenate labels = **false**
- Line stroke width: **3px**
- Background: visible, transparent
- Border: 1px

### Donut/Pie Charts
- Legend: **visible**, position **RightCenter**
- Labels: **"Data value, percent of total"**

### Funnel Chart
- Used for IPA conversion workflow
- 3 stages: Successful Offers → IPA Created → IPA Completed
- Decreasing width shows drop-off

### Tables (tableEx)
- Expand/collapse buttons: visible
- Legacy style: disabled
- Row headers with sorting

---

## 9. Navigation

### Action Buttons
Each page has navigation buttons (typically 2 per page) for:
- Previous page / Next page
- Back to Homepage
- Specific page jumps

### Button Style
- Standard Power BI action button
- Positioned in top-right area of each page
- Uses hyperlink colour `#0078D4`

---

## 10. Slicers / Filters

### Standard Slicers (10 total across report)
| Slicer Type | Pages Used On | Purpose |
|------------|---------------|---------|
| Date range | All data pages | Filter by referral/offer date period |
| Placement type | Referrals, Offers, Draft, IPA | Filter by Residential/Fostering/Supported |
| Status | Offers, Draft | Filter by offer status |

### Text Filter (custom visual)
- Used on Provider Registry page
- Free-text search for provider names
- Custom visual: `textFilter25A4896A83E0487089E2B90C9AE57C8A`

---

## 11. Shape Elements

### Header Bar (shape)
- Full-width coloured bar at top of each page
- Contains BCT logo (left) and page title (centre/left)
- Navigation buttons positioned right

### Section Dividers (shape)
- Horizontal lines separating KPI cards from chart areas
- Thin, subtle colour (`#C8C6C4` backgroundNeutral)

---

## 12. Accessibility `[R81]`

### Compliance
- **WCAG 2.0 / 2.1** (consideration for 2.2) — required by R81
- Government accessibility requirements (GDS assessment)

### Colour Contrast
| Text on Background | Ratio | Status |
|-------------------|-------|--------|
| Foreground `#252423` on White `#FFFFFF` | 14.5:1 | ✅ AAA |
| Foreground `#252423` on Light `#F3F2F1` | 13.1:1 | ✅ AAA |
| Secondary `#605E5C` on White | 5.9:1 | ✅ AA |
| Tertiary `#B3B0AD` on White | 2.2:1 | ⚠️ Large text only |
| White on Primary Blue `#118DFF` | 3.6:1 | ✅ AA (large) |
| White on Green `#1AAB40` | 2.8:1 | ⚠️ Large text only |
| White on Red `#D64554` | 3.4:1 | ✅ AA (large) |

### Notes
- Never rely on colour alone — always include text labels
- Gender cards use icons (boy/girl silhouettes) in addition to colour
- KPI semantic colours (green/yellow/red) should have text labels ("Healthy", "At Risk", "Critical")
- Ensure all visuals have titles and axis labels

---

## 13. Power BI Theme File

A ready-to-import Power BI theme file is provided at:
`brand pack/WMPP_Brand_Theme.json`

**To import:**
1. Open Power BI Desktop
2. View → Themes → Browse for themes
3. Select `WMPP_Brand_Theme.json`
4. Click Apply

This will apply all colours, fonts, and visual styles defined in this brand pack.

---

## 14. Requirements Coverage by Page

| Page | Requirements Covered | New Requirements to Add |
|------|---------------------|------------------------|
| WMPP HOMEPAGE | R24 | — |
| REFERRALS | R24, R51, R13 | R18, R57, R22 (emergency/out-of-region) |
| OFFERS OVERVIEW | R24-R29, R51, R67, R68 | R14 (messaging KPIs) |
| DRAFT OFFERS | R24 | — |
| IPA OVERVIEW | R28, R35 | R62, R20 (finance, audit) |
| PROVIDER REGISTRY | R91, R93, R95, R96 | R41, R49, R59 (QA, diligence, onboarding) |
| Historic | — | R47, R48 (document compliance) |

---

## 15. Implementation Checklist

- [ ] Import `WMPP_Brand_Theme.json` into Power BI Desktop
- [ ] Upload BCT logo to report as image resource
- [ ] Upload boy/girl icons for gender cards
- [ ] Create 7 pages with correct dimensions from Section 4
- [ ] Add header bar shape with BCT logo on each page
- [ ] Add navigation action buttons on each page
- [ ] Create KPI cards per page specifications in Section 6
- [ ] Apply semantic colours (green/yellow/red) to status-based cards
- [ ] Add slicers (date, placement type) to all data pages
- [ ] Create charts per page specifications
- [ ] Verify colour contrast meets WCAG AA standards
- [ ] Add text labels to all colour-coded visuals
- [ ] Test text filter on Provider Registry page
- [ ] Add new KPIs for functional gaps (emergency, QA, finance, docs)
- [ ] Verify all 117 gold layer measures have corresponding visuals
- [ ] Publish to Fabric workspace and connect to gold lakehouse tables

---

*Brand pack extracted from WMPP PILOT DASHBOARD (V13.1) report files — theme JSON (CY26SU02.json), visual definitions, and KPI Logic Document. The BCT website (birminghamchildrenstrust.co.uk) was referenced but was inaccessible (403 Forbidden) during creation; all branding data was sourced from the actual report files.*
