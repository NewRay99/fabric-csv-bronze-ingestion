# Dashboard Legend release runbook

## 17 October 2026 — KPI Definition reconciled to latest saved WIP

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

Import KPI Definition row 1 as headers and include all 567 records (through row 568), selecting named A:I fields. Preserve KPI IDs as text across legacy KPI-xx, Gold and MC namespaces; do not interpret different namespaces or aliases as accepted-scope additions. Do not import helper inventories as additional KPI records.

Date Added means first catalogue registration. Original dates and evidenced dates of older Gold catalogue IDs remain intact; 366 newly registered current definitions are dated 17 October 2026. The 49 older Gold IDs newly surfaced in this sheet retain 26 August dates. No implementation/approval date is invented from file timestamps.

Run `python "project X/tools/validate_dashboard_legend.py"`. The current release JSON fixes row identities/content hashes, date values, source inventories and helper classification. Keep it with the workbook and current calculation snapshot.

Static verification covers the v1 hash/import schema, original IDs/specifications, native dates, complete current measure classification/coverage, exact current DAX snapshots, transitive calculated-table dependencies and notebook spans. The preceding 152-record workbook is a negative control and must fail the new release check. These checks do not rerun Fabric or Power BI native queries or certify client acceptance.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](../04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

## 17 October 2026 — New catalogue entries in KPI Definition

Appended `GOLD-KPI-110`–`GOLD-KPI-144` to **KPI Definition rows 119–153** using the existing A:I fields. The sheet now contains 152 records: the unchanged 117 legacy records plus 35 later catalogue entries. Stable Gold identifiers are retained. These are existing WIP measures newly included in this import sheet; no calculation was implemented by this workbook change. The overlapping 144-entry Gold catalogue is unchanged, and 152 is a workbook record count, not an accepted KPI scope baseline.

The 35 rows carry **30 September 2026** as `Date Added`, their first evidenced appearance anywhere in the version-controlled Dashboard Legend, commit [`70b71eb`](https://github.com/NewRay99/fabric-csv-bronze-ingestion/commit/70b71eb95648eaea487830bdcd8f9931b527a05e). The four earlier workbook revisions contain no `GOLD-KPI-110`–`GOLD-KPI-144`. This date predates their move into KPI Definition on 17 October. The original 117 dates remain 26 August 2026. This field records catalogue provenance, not business creation, model implementation or approval.

Each appended row includes the exact saved measure name/DAX, existing source-table and Python/Spark SQL locators, full calculation-trace reference, existing Section classification and proposed requirement links. Requirement descriptions explicitly retain owner approval pending; implementation status remains Built; UAT pending. The original rows, headers, v1 reference and all other workbook cells are unchanged. Embedded Power BI reference tables still need separate synchronisation and refreshed-model/UAT checks.

The release validator requires all 35 appended IDs in order, exact catalogue measure/source/calculation matches, proposed requirement status, existing Section values and typed dates. Preserve rows 2–118 and their original identifiers; include rows 119–153 when importing KPI Definition. Do not generate replacement KPI-118-style identifiers or add these same records a second time from Gold Source Coverage.

## 17 October 2026 — KPI Date Added metadata

The user-approved `Date Added` column is appended as **column I** on `KPI Definition`; the original eight columns A:H retain their names, order and definitions. All 117 existing KPI rows are dated **26 August 2026**, because every one was already present in the first workbook upload, commit [`b372181`](https://github.com/NewRay99/fabric-csv-bronze-ingestion/commit/b372181ac72ce43ac274b2928ca8473f32921891). The untouched v1 workbook is the same original content.

`Date Added` means **first recorded in the version-controlled Dashboard Legend**, not the KPI's original business creation, approval, implementation, deployment or latest modification date. Values are typed Excel dates displayed as `dd mmm yyyy`. Future additions must use evidenced first-appearance dates; do not infer them from a last-modified timestamp. Existing model import fields remain unchanged; the embedded model reference tables were not modified.

The explicit release validator permits only this approved column-I extension, verifies the original 117 numeric date values (the later appended 35 are checked separately) and still protects every original import header/identity/formula. Consumers should select named A:H fields unless they deliberately import the new date metadata.

Reviewed 17 October 2026; inspected source commit `0a65e962ff3ab9681ed87d9a0a54df610774b736`.

## Fixed workbook contract

`configuration/Dashboard Legend.xlsx` now follows the exact three-sheet import contract in `Dashboard Legend v1.xlsx`: same first three sheet names/order, exact row-1 headers (including `Oiriginal ID`), original RID formulas/IDs/wording/dated notes and original 117 KPI IDs/order/descriptions/Section values. RID column J remains an empty spacer. The v1 file is unchanged. Gold Source Coverage is the only additional sheet; it holds source coverage, the 80-requirement assessment, the separate 144-entry catalogue, current Mission Control calculations and model inventory. The `Calculation` field retains the original specification and adds verified DAX plus notebook evidence. Long expressions have explicitly labelled excerpts linked to the full traceability document.

This restores a workbook contract, not a refreshed semantic model. The saved `ref_RID`, `ref_KPI` and `ref_KPI_RID_Linkage` remain embedded M data; their values, relationships and stable model column names have not been rewritten. Owner approval and refreshed-model reconciliation remain required.

| Sheet | Header row | Header extent | Row identity |
|---|---:|---|---|
| RID | 1 | A:K; J empty | 80 original Req ID values, original order and column-A formulas |
| Table Definition | 1 | A:D | Original 17 table rows retained; unsupported historical targets explicitly labelled |
| KPI Definition | 1 | A:I; A:H original, I approved metadata | 117 original KPI IDs/rows retained; 35 existing Gold catalogue IDs appended in rows 119–153 |
| Gold Source Coverage | Separate section headers | A:I | Additional source, requirement, catalogue and monitoring evidence |

Exact headers are verified against the untouched v1 workbook, not a handwritten approximation. `KPI(s)` remains the workbook field; the saved model's `KPI_s_` is a separate model column. Neither is silently renamed. Original `Oiriginal ID` spelling is intentional compatibility.

## Static release checks

1. Run `python "project X/tools/validate_dashboard_legend.py"` from the repository root.
2. Confirm v1 file SHA-256 is unchanged, original header text/order/blank spacer match, all 80 RIDs and original 117 KPI IDs remain in order, all 35 appended Gold IDs match the catalogue, original formulas/requirement text/notes/Section fields are retained, and no original sheet has extra columns.
3. Inspect the first rows and representative long calculation/requirement cells in Excel. The original white/yellow header convention remains; text wrapping/row height accommodates calculation detail. New evidence sections are separate from import ranges.
4. Verify every named measure and source locator against the inspected archives/notebooks; retain gaps explicitly. Do not interpret a reference-table label as proof that a measure currently exists.

## Model update and runtime checks

The current business model uses embedded `#table` reference data. Publishing Excel alone will not update Requirement Matrix Overview. Preserve model table identities, column names, relationships and existing KPI-to-RID links when preparing a separate controlled reference-data update. For an external Excel query, inspect its navigation and header-promotion steps; use row 1 of the three original sheets, select named fields, and do not ingest Gold Source Coverage as the legacy KPI table.

Do not automatically coerce a KPI count into a ratio, an offer cohort into referral-grain counts, or a retired helper into a new business measure. Compare the original calculation against current DAX and obtain the owner decision where they differ. Refresh both models only after relevant physical sources are available. Reconcile known data, date/provider/authority contexts, blank/zero/missing periods, signatures, statuses, duplicate/unknown keys, role access and operational latest/history selection. Run Desktop visual/interaction checks and obtain client acceptance before publication.

## Recovery

`Dashboard Legend v1.xlsx` is the immutable import reference. The pre-repair expanded workbook is recoverable at `0a65e962ff3ab9681ed87d9a0a54df610774b736`. Restore an explicitly selected workbook version without reverting unrelated notebooks or reports. Keep the dated requirement assessment and source-of-truth decisions alongside the selected import version.
