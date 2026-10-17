# WMPP data platform — Birmingham Children's Trust

## 17 October 2026 — Legend v1 compatibility and verified coverage

`configuration/Dashboard Legend.xlsx` now follows the exact three-sheet import contract in `Dashboard Legend v1.xlsx`: same first three sheet names/order, exact row-1 headers (including `Oiriginal ID`), original RID formulas/IDs/wording/dated notes and original 117 KPI IDs/order/descriptions/Section values. RID column J remains an empty spacer. The v1 file is unchanged. Gold Source Coverage is the only additional sheet; it holds source coverage, the 80-requirement assessment, the separate 144-entry catalogue, current Mission Control calculations and model inventory. The `Calculation` field retains the original specification and adds verified DAX plus notebook evidence. Long expressions have explicitly labelled excerpts linked to the full traceability document.

See [current requirement assessment](client%20documentation/04_Data_and_Reporting/WMPP_REQUIREMENT_REASSESSMENT.md), [exact calculations](client%20documentation/04_Data_and_Reporting/KPI_CALCULATION_TRACEABILITY.md) and [workbook release procedure](client%20documentation/05_Operations_and_Runbooks/DASHBOARD_LEGEND_RUNBOOK.md).

This folder is the active BCT implementation. The numbered `.py` files are the
primary notebooks, stored in Microsoft Fabric source format as of 11 September
2026. Edit these files for future changes. The adjacent `.ipynb` files are retained
as pre-conversion migration references and are no longer maintained.
Superseded notebook trees are retained under the repository `archive` folder.

The Python files preserve Fabric cell/parameter markers, Markdown, language
metadata, `%run` commands, and dependency bindings. They are notebook source
files, not standalone scripts to execute with `python`.

On 23 September 2026 the 17 active notebooks were reconciled against
`reports/Notebooks v16.zip`. See the [v16 sync record](reports/notebook-v16-sync/README.md)
for imported changes, the two intentional safety/correctness exceptions and
the original sync's pytest results. The routine test scope was subsequently
restricted to Python/notebook checks as described below.

For Git integration, the content of `<name>.py` belongs in
`<name>.Notebook/notebook-content.py` alongside the destination item's existing
`.platform` and optional resources/settings. The supplied client snapshot is
under `reports/current/WMPP/notebooks`; it was used for comparison and has not
been overwritten. Keep destination item identities and bindings under review
when promoting source changes.

See the [conversion findings](reports/notebook-comparison/README.md) and
[full comparison](reports/notebook-comparison/comparison.md). To regenerate the
comparison from the repository root:

```powershell
python "project X/tools/fabric_notebooks.py" compare
python -m pytest
```

Routine pytest runs cover Python notebooks, ETL/configuration contracts and
pipeline logic. They do **not** validate semantic models, DAX guide/model
coverage, report layouts, themes, PBIP projects or client project versions.
Client Power BI projects can be added, removed or renamed without being a test
requirement. Obsolete Power BI test/validator files and their helper tests have
been removed from `tests`, not merely excluded from pytest; this also removes
them from test-folder Ruff checks. Python validators are
explicitly listed in `tests/test_validation_scripts.py`, rather than auto-added
from every `validate_*.py` file. They validate the active numbered notebooks,
not historical client notebook snapshots. Regression tests verify the affected
validators work with no `reports` directory and still reject missing active inputs.
Latest Python-only run (23 September 2026): **73 passed, 0 failed**.

`tools/fabric_notebooks.py convert <path.ipynb>` supports migration of an additional
notebook and refuses to overwrite an existing primary `.py` file. Do not regenerate
the primary notebooks from the retained originals after editing them.

## Start here

- [Notebook runbook](client%20documentation/05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md)
- [High-Level Design](client%20documentation/03_Architecture_and_Design/HLD.md)
- [Technical/Functional Design](client%20documentation/03_Architecture_and_Design/TFD.md)
- [Client documentation index](client%20documentation/README.md)
- [ETL issue log](change%20tracking/ETL_ISSUE_LOG.md)
- [ETL change log](change%20tracking/ETL_CHANGE_LOG.md)

## Active notebook set

| Notebook | Purpose |
|---|---|
| `99_common_library.py` | Consolidated exclusions, schema-conformance, audit, and Silver helpers |
| `00_setup_cfg.py` | Creates/upgrades all monitoring and configuration tables |
| `00c_load_location_coordinates.py` | Preview/merge uploaded OS city/postcode reference data locally; deliberate maintenance step, no external lookups |
| `00_archive_load.py` | Loads dated archive ZIP/file extracts into source-named `archived` Delta tables |
| `00a_rehydrate_archive_cfg.py` | Reconstructs archive controls for an existing deployment |
| `00b_reset_silver_cfg.py` | Guarded administrative reset for Silver replay |
| `01_bronze_get_latest.py` | Loads the latest source extracts into Bronze |
| `01a_cfg_schema_capture_live.py` | Captures live Bronze schema and records drift |
| `01a_cfg_schema_capture_archive.py` | Captures/compares the archive catalogue schema |
| `02_silver_formatter.py` | Formats the current Bronze batch into Silver |
| `02a_archive_silver.py` | Replays canonical historical month-end states into Silver/Gold |
| `03_silver_business_rules.py` | Runs schema-driven DQ and referential-integrity checks |
| `04_gold_model.py` | Builds the current/historical referral Gold model and snapshots |
| `05_gold_dimensions.py` | Builds Gold reporting dimensions and provider bridges from Silver |
| `06_reports.py` | Creates missing monitoring materialized lake views; runners refresh all six after the final job status is written |
| `90_run_live_pipeline.py` | Runs the standard live Bronze-to-Gold notebook sequence |
| `90_run_archive_pipeline.py` | Runs the monitored archive hydration and historical replay sequence |
| `99_data_domain.py` | Profiles data domains against the configuration contract |
| `99_data_extracts.py` | Produces supporting data extracts |

## Supporting folders

| Folder | Contents |
|---|---|
| `configuration/` | `schema_definition.csv`, DQ rules, and schema-drift review workbook |
| `client documentation/` | Controlled client documentation and operational runbooks |
| `change tracking/` | ETL issue/change history and semantic-model changelog |
| `assets/` | Brand material, screenshots, and design previews |
| `reports/` | Current/client report packages |
| `tests/` | Static Fabric-source validators and Gold Spark simulation |
| `tools/` | Fabric notebook conversion, parsing, and client comparison |

Do not create new `version NN` notebook folders. Update the active notebooks in
this root, record material changes in the ETL issue/change log, and use Git tags
or the repository archive for immutable milestones.
