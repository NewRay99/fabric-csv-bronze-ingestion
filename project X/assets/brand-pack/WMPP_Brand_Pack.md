# WMPP Power BI brand pack

This folder is the implementation source for a Birmingham Children's Trust-branded WMPP report. The live BCT website is the primary reference, followed by the supplied official logo, brand-guideline PDF and PowerPoint template.

## Brand principles

- Warm, direct and public-service focused.
- Use the four official mandala colours as accents, not as large fields behind small white text.
- Use charcoal text and white report surfaces on the BCT light-grey canvas.
- Keep cards nearly square: 4px corner radius, a fine grey border and a restrained shadow.
- Do not use glassmorphism, radiant glow, decorative gradients, navy/blue/magenta brand colours or pill-shaped navigation.
- Never use colour as the only indication of status.

## Colour system

| Token | Hex | Power BI use |
|---|---|---|
| BCT gold | `#FCBF00` | Primary accent, selected state, first data series |
| BCT orange | `#F59E00` | Secondary accent and second data series |
| BCT deep orange | `#EF7911` | Strong emphasis and third data series |
| BCT pale yellow | `#FFE672` | Soft highlight and fourth data series |
| Charcoal | `#1D1D1B` | Primary text and high-contrast marks |
| Mid grey | `#575756` | Secondary text |
| Canvas grey | `#EDEDED` | Report-page background |
| Border grey | `#D6D6D4` | Dividers and visual borders |
| White | `#FFFFFF` | Cards, tables and chart surfaces |
| Success green | `#3A8B6F` | Positive status only |
| Critical red | `#C0392B` | Critical status only |

The multi-series chart sequence is:

`#FCBF00`, `#F59E00`, `#EF7911`, `#FFE672`, `#575756`, `#1D1D1B`, `#3A8B6F`, `#C0392B`.

## Typography

Use **Lato** throughout the report, matching the current BCT website. If Lato is unavailable in a controlled Power BI environment, use **Arial** as the approved fallback.

| Role | Font | Weight | Suggested size |
|---|---|---:|---:|
| Page title | Lato | 700 | 24–30px |
| Section title | Lato | 700 | 16–20px |
| Visual title | Lato | 700 | 12–14px |
| KPI value | Lato | 700 | 28–36px |
| Body / labels | Lato | 400 | 11–13px |
| Metadata | Lato | 400 | 10–11px |

Power BI cannot guarantee font availability in every export or service environment. Test the report on the deployment tenant; use Arial when a portable system-font fallback is required.

## KPI scorecard terminology

The SVG scorecard family uses:

- **Current period**
- **Previous month**
- **Month-on-month change**
- **Change rate**

For percentage-point metrics, state the absolute change as `+2.6 pp`; do not label it as a percentage change. The SVG examples contain illustrative values and are design references, not report data.

## Layout

- Page canvas: `#EDEDED`
- Visual surface: white with `#D6D6D4` 1px border
- Corner radius: 4px
- Base spacing: 8px; common gaps 16px and 24px
- Page margins: 24–32px
- KPI accent rail: 8px, using an official BCT warm colour
- Charts: visible titles and axis labels, dotted neutral gridlines
- Tables: gold header with charcoal text; white rows with subtle grey dividers

## Files

- `BCT_LOGO_P_COLOUR.tif` — supplied official logo master
- `BCT003__Brand_Guidelines_v1.pdf` — supplied official guidelines
- `BCT_PPT_4_3_WITH_TEXT_GUIDE.pptx` — supplied official presentation template
- `WMPP_Brand_Theme.json` — importable Power BI theme
- `BCT_PowerBI_Brand_Swatch.svg` — colour and type swatch
- `BCT_PowerBI_Font_Guide.md` — font implementation notes
- `ideas/` — SVG KPI scorecards and design references

## Power BI use

1. Import `WMPP_Brand_Theme.json` from **View → Themes → Browse for themes**.
2. Add the supplied BCT logo as an image resource; preserve its clear space and aspect ratio.
3. Use the SVG files in `ideas/` as design references or convert their markup to data-URI measures for Image URL visuals.
4. Verify contrast, text alternatives, keyboard order and export behaviour before publishing.

The operational measure catalogue remains at `../WMPP_Semantic_Model_Measures.md`; it is deliberately outside the visual brand pack.
