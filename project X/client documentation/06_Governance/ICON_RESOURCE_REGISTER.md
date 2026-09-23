# WMPP icon resource and provenance register

Record date / source review: **23 September 2026**.
Status: **sources identified; asset acquisition, implementation and approval pending**.

## Purpose and limitations

Client audit record for candidate icons identified for the supplied dashboard
reference images (`reports/current/end goal 1.png`, `end goal 2.png`, and
`end goal 3.png`, relative to Project X). These links identify official resources
that may be used for implementation; they do not establish who created the
reference images or which icon library the images originally used.

**None of the six candidates is verified as the exact original from the images.**
The existing generator has inline vector fragments. No attribution of those
fragments to these libraries is asserted. This documentation change does not
replace icons, download asset files, approve a licence or deploy a report.

Implementation guidance: [Icon implementation guide](../../reports/templates/ICON_IMPLEMENTATION_GUIDE.md).

## Candidate inventory

All rows have status **proposed / not yet incorporated**. Resource IDs are
independent of client project filenames and version numbers.

| ID | Intended dashboard use | Library / icon | Official resource | Licence reference |
|---|---|---|---|---|
| ICON-001 | Active providers / people | Lucide `users-round` | [Icon and Copy SVG](https://lucide.dev/icons/users-round) | LUCIDE below |
| ICON-002 | Offers received / document search | Lucide `file-search` | [Icon and Copy SVG](https://lucide.dev/icons/file-search) | LUCIDE below |
| ICON-003 | Acceptance rate / targets | Tabler `target-arrow` | [Official SVG source](https://github.com/tabler/tabler-icons/blob/main/icons/outline/target-arrow.svg) | TABLER below |
| ICON-004 | Homes offered | Lucide `house` | [Icon and Copy SVG](https://lucide.dev/icons/house) | LUCIDE below |
| ICON-005 | Response time / elapsed time | Lucide `clock` | [Icon and Copy SVG](https://lucide.dev/icons/clock) | LUCIDE; also listed as Feather-derived |
| ICON-006 | Weekly cost (£) | Lucide `pound-sterling` | [Icon and Copy SVG](https://lucide.dev/icons/pound-sterling) | LUCIDE below |

General catalogue: [Lucide icons](https://lucide.dev/icons/).
The links above are discovery references, not pinned asset versions. In
particular, a GitHub `main` URL can change. Pin a release or commit at acquisition.

## Licence and attribution references

- **LUCIDE:** the official [Lucide licence page](https://lucide.dev/license)
  states ISC terms and carries additional Feather MIT notices for specified
  derived icons, including `clock`. Retain the complete applicable copyright and
  permission notices with copied assets, including inherited notices. Review
  the licence bundled with the exact version selected for implementation.
- **TABLER:** the official [Tabler licence](https://github.com/tabler/tabler-icons/blob/main/LICENSE)
  states MIT terms with copyright attribution to Paweł Kuna. Retain the applicable
  copyright and permission notice with copies or substantial portions.

These are implementation compliance notes, not a legal approval or a warranty
of third-party provenance. No full licence files have been archived locally in
this change. A URL and this summary do not replace the upstream licence text.

## Evidence to complete before client implementation sign-off

Maintain one evidence row per icon and derivative; do not fill unknown values
with an assumed version, hash, download date or approval.

| Evidence field | Current state / required action |
|---|---|
| Official source and intended use | Recorded above for six candidates |
| Exact match to image originals | Unverified; label as replacement candidates |
| Upstream release / immutable commit URL | Pending acquisition |
| Original SVG filename, retained local path, SHA-256 | Not downloaded; pending |
| Download date and implementer | Pending |
| Full licence/notice file path and SHA-256 | Not archived; pending |
| Modifications and derivative SVG SHA-256 | Not implemented; record even styling-only changes |
| Actual client project, page and resource usage | Not assigned; record the current project, whatever its name/version |
| Visual/accessibility review evidence | Pending implementation |
| Client/design approver and approval date | Not approved / pending |
| Client delivery package containing assets and notices | Pending |

Other generator icons (alerts, trends, calendar, list/chart controls, clipboard,
pin and grid) remain outside this six-resource register. Add separate records if
they are sourced or replaced. Do not imply this is a complete third-party asset
audit of every current or historic report.

## Change record

| Date | Change | Delivery status |
|---|---|---|
| 2026-09-23 | Recorded official Lucide/Tabler candidates, provenance limitations, implementation link and evidence checklist | Documentation only; no asset replacement or report/model tests |
