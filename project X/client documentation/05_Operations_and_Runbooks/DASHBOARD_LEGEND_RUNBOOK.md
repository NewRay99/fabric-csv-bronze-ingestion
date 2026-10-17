# Dashboard Legend release runbook

Reviewed 17 October 2026; inspected source commit `0a65e962ff3ab9681ed87d9a0a54df610774b736`.

## Fixed workbook contract

`configuration/Dashboard Legend.xlsx` now follows the exact three-sheet import contract in `Dashboard Legend v1.xlsx`: same first three sheet names/order, exact row-1 headers (including `Oiriginal ID`), original RID formulas/IDs/wording/dated notes and original 117 KPI IDs/order/descriptions/Section values. RID column J remains an empty spacer. The v1 file is unchanged. Gold Source Coverage is the only additional sheet; it holds source coverage, the 80-requirement assessment, the separate 144-entry catalogue, current Mission Control calculations and model inventory. The `Calculation` field retains the original specification and adds verified DAX plus notebook evidence. Long expressions have explicitly labelled excerpts linked to the full traceability document.

This restores a workbook contract, not a refreshed semantic model. The saved `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage` remain embedded M data; their values, relationships and stable model column names have not been rewritten. Owner approval and refreshed-model reconciliation remain required.

| Sheet | Header row | Header extent | Row identity |
|---|---:|---|---|
| RID | 1 | A:K; J empty | 80 original Req ID values, original order and column-A formulas |
| Table Definition | 1 | A:D | Original 17 table rows retained; unsupported historical targets explicitly labelled |
| KPI Definition | 1 | A:H | 117 original KPI IDs, original order and descriptions/Section values |
| Gold Source Coverage | Separate section headers | A:I | Additional source, requirement, catalogue and monitoring evidence |

Exact headers are verified against the untouched v1 workbook, not a handwritten approximation. `KPI(s)` remains the workbook field; the saved model's `KPI_s_` is a separate model column. Neither is silently renamed. Original `Oiriginal ID` spelling is intentional compatibility.

## Static release checks

1. Run `python "project X/tools/validate_dashboard_legend.py"` from the repository root.
2. Confirm v1 file SHA-256 is unchanged, original header text/order/blank spacer match, all 80 RIDs and 117 KPI IDs remain in order, original formulas/requirement text/notes/Section fields are retained, and no original sheet has extra columns.
3. Inspect the first rows and representative long calculation/requirement cells in Excel. The original white/yellow header convention remains; text wrapping/row height accommodates calculation detail. New evidence sections are separate from import ranges.
4. Verify every named measure and source locator against the inspected archives/notebooks; retain gaps explicitly. Do not interpret a reference-table label as proof that a measure currently exists.

## Model update and runtime checks

The current business model uses embedded `#table` reference data. Publishing Excel alone will not update Requirement Matrix Overview. Preserve model table identities, column names, relationships and existing KPI-to-RID links when preparing a separate controlled reference-data update. For an external Excel query, inspect its navigation and header-promotion steps; use row 1 of the three original sheets, select named fields, and do not ingest Gold Source Coverage as the legacy KPI table.

Do not automatically coerce a KPI count into a ratio, an offer cohort into referral-grain counts, or a retired helper into a new business measure. Compare the original calculation against current DAX and obtain the owner decision where they differ. Refresh both models only after relevant physical sources are available. Reconcile known data, date/provider/authority contexts, blank/zero/missing periods, signatures, statuses, duplicate/unknown keys, role access and operational latest/history selection. Run Desktop visual/interaction checks and obtain client acceptance before publication.

## Recovery

`Dashboard Legend v1.xlsx` is the immutable import reference. The pre-repair expanded workbook is recoverable at `0a65e962ff3ab9681ed87d9a0a54df610774b736`. Restore an explicitly selected workbook version without reverting unrelated notebooks or reports. Keep the dated requirement assessment and source-of-truth decisions alongside the selected import version.
