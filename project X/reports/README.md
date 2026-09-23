# Report packages

## Open this project for local WMPP work

`current/SM WMPP v16 updated/SM_WMPP_v16.pbip` is the latest active local
project. Its attached report now contains all 16 pages / 315 visuals from
`RPT WMPP v16`, including the shared theme, referral/provider detail and
6/12-month snapshot controls. The report connects by relative path to its
sibling `SM_WMPP_v16.SemanticModel`, not to the client-hosted semantic model.
Open the PBIP launcher to load the report and model together.

The three leading dashboard pages use the revised reference-image design:
icon-led scorecards, borderless headings and compact chart/table panels.
Final Power BI rendering acceptance is still pending; see
`client documentation/04_Data_and_Reporting/WMPP_REFERENCE_DESIGN_REVIEW.md`.

The active model has 45 tables; the retired nested `SM WMPP v16` copy had 37.
On 2026-09-23 the retired folder was moved out of `current` to
`retired/2026-09-23-local-report-consolidation/SM WMPP v16`. That archive also
contains the previous attached report, the previous theme manifest and a
consolidation receipt. Nothing was permanently deleted.

The original `current/RPT WMPP v16` client-connected project is retained for
later client deployment. Its default launcher still requires that connection;
use the **SM WMPP v16 updated PBIP** for local review. The report copy does not
provide offline data or change model credentials. Refreshing client-backed
partitions still requires client access; model/render/refresh acceptance in
Desktop remains outstanding.

The historical consolidation validator has been removed with the other
version-specific Power BI tests. Review the actual current client project when
acceptance is requested; the versioned paths above describe the earlier handover.
If either report is subsequently edited, explicitly review/synchronise the
other copy before relying on byte-for-byte parity again.

## Other packages

- `current/` contains the current repository report package.
- `client-deliverables/` contains separately supplied client/report test
  packages whose version numbering is independent of the notebook baseline.
- `retired/` contains recoverable superseded local projects and report backups.

Superseded report ZIPs and extracted report source trees are retained in the
repository archive.
