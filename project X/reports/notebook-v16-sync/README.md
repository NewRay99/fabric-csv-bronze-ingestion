# Notebooks v16 ZIP reconciliation — 23 September 2026

## Scope and result

Compared all 17 `Notebooks v16/<name>.Notebook/notebook-content.py` entries in
`../Notebooks v16.zip` with the active `project X/<name>.py` notebooks. Applied
ZIP-to-primary-source changes, including Fabric cell metadata and Markdown.
The 17 numbered primary files had no uncommitted Git changes before this sync.

**15 notebooks match the ZIP after line-ending/terminal-newline normalisation.
Two have the explicit exceptions below.** All 17 output hashes were verified.
There are 16 substantive file diffs; `00_setup_cfg.py` retains its existing
corrected content. No notebook is missing from either set.

The source ZIP is unchanged. Its SHA-256 is
`343182373526a4f5bf60c117eecbe5deac7f08775ddc664fe1a95e532bca536c`.
[comparison.json](comparison.json) records the source entry, pre-sync file hash,
ZIP-entry hash, final LF-normalised hash and comparison flags for every notebook.
Code flags include whitespace differences; they do not all represent logic changes.

## Material changes imported

- `01a_cfg_schema_capture_archive.py`: removed two ad-hoc production CSV preview
  cells (July audit and provider-submission documents), as in the ZIP. Recoverable
  from Git; no production data or CSV files were deleted.
- `03_silver_business_rules.py`: qualifies the IPA rollup grouping as
  `c.referral_id`.
- `04_gold_model.py`: imports the ZIP projection spelling for
  `o.referral_provider_id`; the output column is unchanged.
- `05_gold_dimensions.py`: completes the `closure_reason_id` / `closure_type`
  rename through the source CTE, deduplication and cleaning. Previously the
  primary source produced `reject_*` aliases but consumed `closure_*` columns.
- `90_run_archive_pipeline.py`: child timeout increases from 7,200 to 9,200
  seconds. Nested DQ/Gold calls in `02a_archive_silver.py` remain at 7,200 seconds.
- `90_run_live_pipeline.py`: child timeout increases from 1,800 to 7,800 seconds;
  `RUN_ESSENTIAL_DQ=True` now defaults to critical checks only, as in the ZIP.
  Set it to `False` for a thorough run. `FORCE_RERUN=False` is unchanged.
- Remaining differences are exported cell formatting, whitespace and Markdown.
  Lakehouse/dependency metadata is unchanged across all 17 notebooks.

## Intentional exceptions to an exact copy

1. **Monitoring dependency:** the ZIP creates
   `monitoring.rpt_job_step_timing` but later reads the retired
   `monitoring.vw_job_step_timing`. Retained the existing `rpt_*` reference and
   matching completion message in `00_setup_cfg.py`; importing the ZIP reference
   would reintroduce a missing-object dependency.
2. **Archive reset defaults:** retained `PROCESS_ONLY=""`,
   `RESET_MONTH_MONITORING=False`, and `CONFIRM_PROCESS_ONLY_RESET=""`.
   The ZIP preselects July 2026 and enables/confirms a monitoring reset. These
   run-specific settings were not adopted without explicit user direction.
   `CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY=False` is unchanged. Updated the timeout
   comment to match the imported 9,200-second value.

No `.platform` identities, schedules, `.ipynb` references, older
`reports/current/WMPP/notebooks` snapshot files, Power BI files, or configuration
CSVs were changed. No Fabric notebook, pipeline, reset or cloud deployment ran.

## Pytest results

**Lint follow-up:** obsolete Power BI validators and their two helper test
modules have now been deleted from `tests`, along with its unused pytest
exclusion file. Excluding them from pytest alone did not exclude them from
Ruff's pre-commit file selection. The earlier retention decision below is
historical and no longer applies. Python/ETL tests remain enabled.

**Latest result, 23 September 2026: 73 passed, 0 failed.** The four stale-snapshot
failures were resolved by removing duplicate historical checks and retargeting
unique spot-logic and export-date assertions to the active notebooks. All four
validators remain enabled. The Gold snapshot check now inspects actual select
arguments rather than requiring columns to occur adjacently. Four new regression
cases confirm these validators pass without a `reports` directory and still fail
when a required active notebook is missing. No production notebook changed in
this follow-up. Results: [pytest-python-only-results.xml](pytest-python-only-results.xml).

```powershell
python -m pytest "project X/tests" --basetemp="_tmp_active_notebook_full_20260923" -o addopts= -p no:cacheprovider -q --tb=short --junitxml="project X/reports/notebook-v16-sync/pytest-python-only-results.xml"
```

**Earlier scope change, requested 23 September 2026:** routine pytest now
excludes all semantic-model, DAX and report-project checks, including their
helper unit tests. That intermediate Python-only run was **65 passed, 4 failed** (69
tests). The four failures are the older WMPP notebook-snapshot comparisons
listed below, not Power BI projects. The original results and XML below are
retained as historical evidence of the sync; model/report asset absence is no
longer a routine test failure or a Python-sync completion requirement.

Before editing: **73 passed, 9 failed** (82 tests).

After syncing and adding six regression tests: **79 passed, 9 failed** (88 tests).
No new failing test remains. Existing assertions were updated for the ZIP's
closure naming, timeout, essential-DQ default and equivalent implicit SQL alias;
no tests were skipped or removed to hide the remaining failures.

```powershell
python -m pytest "project X/tests" --basetemp="_tmp_notebooks_v16_final_20260923" -o addopts= -p no:cacheprovider -q --tb=no --junitxml="project X/reports/notebook-v16-sync/pytest-results.xml"
```

Full machine-readable results: [pytest-results.xml](pytest-results.xml).

Focused Fabric-source/parser/syntax and new v16 regressions: **30 passed**.

```powershell
python -m pytest "project X/tests/test_fabric_notebooks.py" "project X/tests/test_notebooks_v16_contract.py" --basetemp="_tmp_notebooks_v16_focused_20260923" -o addopts= -p no:cacheprovider -q
```

The new closure SQL test executes the notebook's CTEs against synthetic SQLite
fixtures, translating timestamp/string casts and the current-timestamp function.
It covers column resolution, snapshot deduplication, non-colliding cancel/decline
IDs, latest-reason ordering, cleaning/grouping and job lineage. This is not a
Spark/Fabric execution test.

## Historical failures at sync time (superseded by the resolution above)

| Validator | Current cause |
|---|---|
| `validate_gld015_reject_reason_dimension` | Primary closure checks now pass; older WMPP snapshot lacks closure cleaning. |
| `validate_gold_referral_schema` | Primary checks now pass; older WMPP Gold snapshot lacks job-run lineage. |
| `validate_job_run_lineage` | Older WMPP live runner lacks `FORCE_RERUN` control. |
| `validate_silver_required_columns` | Older WMPP common library lacks the export-date contract guard. |
| `validate_wmpp_end_goal_design` | Expected active semantic model `_Design Measures.tmdl` is absent. |
| `validate_wmpp_local_project` | Expected `SM WMPP v16 updated/SM_WMPP_v16.pbip` is absent. |
| `validate_wmpp_reference_design` | Expected `RPT WMPP v16` dashboard page files are absent. |
| `validate_wmpp_report_theme` | Expected `RPT WMPP v16` report definition is absent. |
| `validate_wmpp_v16_enhancements` | Expected active semantic model `_Measures.tmdl` is absent. |

At sync time the first two failures moved past repaired primary-source assertions
and exposed older snapshot mismatches. These historical-snapshot checks have now
been removed or retargeted; Power BI tests are excluded per user direction.
The historical snapshot remains unchanged. Fabric runtime and full DQ acceptance
remain unverified until a client/development Lakehouse is available.
