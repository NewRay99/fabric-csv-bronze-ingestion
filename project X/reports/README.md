# Report packages

## 18 October 2026 — Provider documents and missing requirement KPI visibility (SEM-004)

Both provider pages now show home-level document metadata, recorded expiry dates and a document-level `expired_docs` flag (1 expired, 0 dated/not expired, blank unknown). Removed the unrelated monthly-performance row filter. Four scoped document summaries extend the provider KPI list; 33 already implemented requirement-linked calculations are now surfaced on Requirement Matrix with explicit proxy labels.

The saved business model now has 73 tables/501 definitions/35 pages; relationships and roles remain 54/two. KPI Definition preserves all preceding 567 records and its column contract, appends GOLD-KPI-327–330 dated 18 October, and contains 571 dictionary records. Mission Control remains 34 tables/351 definitions/17 pages. These counts include helpers and historical dispositions; they do not establish accepted KPI scope.

Saved model and catalogue checks have passed. Refreshed results, report and mobile review, access checks and client acceptance remain pending. The data owner must confirm how documents are assigned to homes; the model link and schema contract currently differ. Document compliance, reminder delivery and referral blocking still require separate rules and evidence.

[Implementation, exact calculations, gaps and acceptance](../client%20documentation/04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

## Current reporting project

WMPP_v16 is the current reporting model, opened through `SM_WMPP_v16.pbip` together with its report and semantic-model folders. It contains the provider document registers, expiry flags and additional requirement-linked KPI results described in the current reporting update. Earlier delivery links are retained as v15 or earlier. The project must be reopened and refreshed in Power BI before completing the acceptance checks.

## Previous delivery baseline — v15 or earlier

`current/v15 or earlier/SM_WMPP_v16.pbip` was used for the earlier delivery baseline. Its attached report now contains all 16 pages / 315 visuals from `RPT WMPP_v16`, including the shared theme, referral/provider detail and 6/12-month snapshot controls. The report connects by relative path to its sibling `SM_WMPP_v16.SemanticModel`, not to the client-hosted semantic model. Open the PBIP launcher to load the report and model together.

The three leading dashboard pages use the revised reference-image design: icon-led scorecards, borderless headings and compact chart/table panels. Final Power BI rendering acceptance is still pending; see `client documentation/04_Data_and_Reporting/WMPP_REFERENCE_DESIGN_REVIEW.md`.

The active model has 45 tables; the retired nested `SM WMPP_v16` copy had 37. On 2026-09-23 the retired folder was moved out of `current` to `retired/2026-09-23-local-report-consolidation/SM WMPP_v16`. That archive also contains the previous attached report, the previous theme manifest and a consolidation receipt. Nothing was permanently deleted.

The original `current/RPT WMPP_v16` client-connected project is retained for later client deployment. Its default launcher still requires that connection; use the **v15 or earlier PBIP** for local review. The report copy does not provide offline data or change model credentials. Refreshing client-backed partitions still requires client access; model/render/refresh acceptance in Desktop remains outstanding.

The historical consolidation validator has been removed with the other version-specific Power BI tests. Review the actual current client project when acceptance is requested; the versioned paths above describe the earlier handover. If either report is subsequently edited, explicitly review/synchronise the other copy before relying on byte-for-byte parity again.

## Other packages

- `current/` contains the current repository report package.
- `client-deliverables/` contains separately supplied client/report test packages whose version numbering is independent of the notebook baseline.
- `retired/` contains recoverable superseded local projects and report backups.

Superseded report ZIPs and extracted report source trees are retained in the repository archive.
