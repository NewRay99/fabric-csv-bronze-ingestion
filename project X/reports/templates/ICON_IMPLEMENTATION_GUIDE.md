# WMPP icon resources — implementation guide

Recorded: 23 September 2026. Scope: icon sourcing and future implementation.

## Status and source of truth

The [client icon resource register](../../client%20documentation/06_Governance/ICON_RESOURCE_REGISTER.md)
contains the six sourced icon candidates, official links, licence references and
audit requirements. They are suggested replacements, **not verified originals**
from the `end goal 1.png`, `end goal 2.png` and `end goal 3.png` references.
No upstream SVG files have been downloaded, incorporated or approved through
this documentation change. Do not describe the existing report artwork as
verified Lucide/Tabler assets on the strength of this register.

## Existing implementation seam

The current [reference-layout generator](../../tools/redesign_wmpp_reference_style.py)
defines inline vector fragments in `ICONS`, with sizing/colour in `icon()`.
Candidate replacements map to these existing keys:

| Generator key | Client register ID | Intended use |
|---|---|---|
| `people` | ICON-001 | Active providers / people |
| `document` | ICON-002 | Offers received / document search |
| `target` | ICON-003 | Acceptance rate / targets |
| `home` | ICON-004 | Homes offered |
| `clock` | ICON-005 | Response time / elapsed time |
| `pound` | ICON-006 | Weekly cost in GBP |

The generator also contains `alert`, `trend`, `calendar`, `list`, `chart`,
`clipboard`, `pin` and `grid`. Those are **not covered by this sourcing register**;
record their provenance separately before claiming a fully sourced icon set.

The common theme controls visual styling; it is not an SVG asset bundle. Merely
importing `WMPP_Common_Theme.json` does not replace the inline icon fragments.
The generator composes them into `wmpp-reference-board.svg`,
`wmpp-reference-supply.svg` and `wmpp-reference-target.svg`.

## Implementation procedure (not yet performed)

1. Confirm the selected candidates against the reference images with the design
   owner. Use official source pages from the register, not a third-party mirror.
2. Select and record an immutable upstream release/commit for each library.
   Save the exact original SVGs and complete applicable licence/notice files in
   a shared version-neutral asset directory, for example
   `project X/assets/icons/upstream/<library>/<release>/`. This is a proposed
   location, not a claim that files already exist there.
3. Record download date, source URL, release/commit and SHA-256 for every original.
   Retain originals unchanged. Keep any styled derivatives separately and record
   their hashes and changes (stroke, colour, dimensions, circular surround).
4. Replace the relevant generator fragments or load the approved local assets
   there. Preserve the upstream coordinate system and aspect ratio. If converting
   a complete SVG into fragments, retain required geometry/transforms and resolve
   inherited styles explicitly. Do not blindly nest full SVG markup.
5. Use the reference design as the styling target: thin near-black line art,
   consistent optical size, rounded line ends/joins and a separate fine circular
   badge. The existing renderer uses a 24-unit coordinate space, stroke width
   `1.3`, round caps/joins, and default colour `#161616`; these are local styling
   choices, not claims about the upstream artwork. Keep page/panel titles
   borderless. Do not modify KPI logic or bake values into the icon artwork.
6. Inspect external SVGs before embedding: retain only required vector markup;
   reject scripts, event handlers and external resource references. Package assets
   locally so viewing the report does not rely on live icon-site URLs.
7. Resolve the **actual current client project paths** before running any report
   generator. Existing scripts contain historical v16 paths; do not assume these
   exist or recreate retired projects. Preserve project identities and bindings.
8. As part of a separately requested implementation review, visually inspect the
   target report at normal viewing size for clipping, line weight, contrast and
   alignment. Keep meaningful text labels/tooltips; do not rely on icons alone
   for status or action meaning. Capture implementation evidence and obtain
   client/design acceptance. No semantic-model or report-project pytest checks
   are required by this guide.

## Handover evidence

Complete the client register with original/derivative hashes, pinned source
versions, retained licence files, actual target project/page/resource locations,
screenshots and approver/date. Include notices in the client handover package,
not only in a developer checkout. Website links alone are not a licence archive.

Project names can change from v16 to v17/v20 without changing the resource IDs
above. Record each deployment separately; a new project name is not a new icon.
