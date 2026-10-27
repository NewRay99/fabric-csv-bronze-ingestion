# WMPP data platform — Birmingham Children's Trust

## 27 October 2026 — Referral creator in Gold (GLD-026)

`04_gold_model.py` now requires `silver.referral.referral_created_by` in source preflight and publishes it unchanged as `gold.fact_referral.referral_created_by`, using the selected current referral row. NULLs remain NULL. The monthly snapshot projection is unchanged. This is a local source change; Fabric deployment and consuming-model refresh remain pending. See the [TFD](client%20documentation/03_Architecture_and_Design/TFD.md#27-october-2026--referral-creator-gld-026) and [ETL issue](change%20tracking/ETL_ISSUE_LOG.md#gld-026--referral-creator-missing-from-current-referral-fact).

## 19 October 2026 — WMPP_v16 linked referral status

Provider Explorer now shows Referral current status immediately after Offer statuses in the linked-provider results. The value uses referral UUIDs from the visible linked pairs and the current referral status; source reference IDs remain display labels. The current WMPP_v16 model contains 73 tables, 502 measure definitions and 35 report pages. This adds a display helper, not an additional business KPI. Refresh and visual acceptance remain pending.

## 18 October 2026 — Provider documents and missing requirement KPI visibility (SEM-004)

Both provider pages now show home-level document metadata, recorded expiry dates and a document-level `expired_docs` flag (1 expired, 0 dated/not expired, blank unknown). Removed the unrelated monthly-performance row filter. Four scoped document summaries extend the provider KPI list; 33 already implemented requirement-linked calculations are now surfaced on Requirement Matrix with explicit proxy labels.

The saved business model now has 73 tables/501 definitions/35 pages; relationships and roles remain 54/two. KPI Definition preserves all preceding 567 records and its column contract, appends GOLD-KPI-327–330 dated 18 October, and contains 571 dictionary records. Mission Control remains 34 tables/351 definitions/17 pages. These counts include helpers and historical dispositions; they do not establish accepted KPI scope.

Saved model and catalogue checks have passed. Refreshed results, report and mobile review, access checks and client acceptance remain pending. The data owner must confirm how documents are assigned to homes; the model link and schema contract currently differ. Document compliance, reminder delivery and referral blocking still require separate rules and evidence.

[Implementation, exact calculations, gaps and acceptance](client%20documentation/04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

## 17 October 2026 — KPI Definition reconciled to latest saved WMPP_v16

KPI Definition is now reconciled to the latest saved local WMPP_v16, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. The calculation reference records these changes; production refresh and acceptance remain pending.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

[Current DAX, Python/Spark SQL and source evidence](client%20documentation/04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

This folder is the active BCT implementation. The numbered `.py` files are the primary notebooks, stored in Microsoft Fabric source format as of 11 September 2026. Edit these files for future changes. The adjacent `.ipynb` files are retained as pre-conversion migration references and are no longer maintained. Superseded notebook trees are retained under the repository `archive` folder.

The Python files preserve Fabric cell/parameter markers, Markdown, language metadata, `%run` commands, and dependency bindings. They are notebook source files, not standalone scripts to execute with `python`.

On 23 September 2026 the 17 active notebooks were reconciled against `reports/Notebooks v16.zip`. See the [v16 sync record](reports/notebook-v16-sync/README.md) for imported changes, the two intentional safety/correctness exceptions and the original sync's pytest results. The routine test scope was subsequently restricted to Python/notebook checks as described below.

For Git integration, the content of `<name>.py` belongs in `<name>.Notebook/notebook-content.py` alongside the destination item's existing `.platform` and optional resources/settings. The supplied client snapshot is under `reports/current/WMPP/notebooks`; it was used for comparison and has not been overwritten. Keep destination item identities and bindings under review when promoting source changes.

See the [conversion findings](reports/notebook-comparison/README.md) and [full comparison](reports/notebook-comparison/comparison.md). To regenerate the comparison from the repository root:

```powershell
python "project X/tools/fabric_notebooks.py" compare
python -m pytest
```

Routine pytest runs cover Python notebooks, ETL/configuration contracts and pipeline logic. They do **not** validate semantic models, DAX guide/model coverage, report layouts, themes, PBIP projects or client project versions. Client Power BI projects can be added, removed or renamed without being a test requirement. Obsolete Power BI test/validator files and their helper tests have been removed from `tests`, not merely excluded from pytest; this also removes them from test-folder Ruff checks. Python validators are explicitly listed in `tests/test_validation_scripts.py`, rather than auto-added from every `validate_*.py` file. They validate the active numbered notebooks, not historical client notebook snapshots. Regression tests verify the affected validators work with no `reports` directory and still reject missing active inputs. Latest Python-only run (23 September 2026): **73 passed, 0 failed**.

`tools/fabric_notebooks.py convert <path.ipynb>` supports migration of an additional notebook and refuses to overwrite an existing primary `.py` file. Do not regenerate the primary notebooks from the retained originals after editing them.

## Start here

- [Notebook runbook](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md?d=wb6a632cd16734785903b5fb8e4a6513c&csf=1&web=1&e=PmCZlN)
- [High-Level Design](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/03_Architecture_and_Design/HLD.md?d=we715265df69c49798eb4779afbf52e61&csf=1&web=1&e=u6iSxc)
- [Technical/Functional Design](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/03_Architecture_and_Design/TFD.md?d=w90ef1687119842da970f1db64dfa8dcc&csf=1&web=1&e=RzksV1)
- [Client documentation index](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/README.md?d=wc9130c0e20ae4b39ad0d234465ae83be&csf=1&web=1&e=qOT68x)
- **Live Link: [ETL issue log](change%20tracking/ETL_ISSUE_LOG.md) **Sharepoint Link: [ETL issue log](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/99_Change_Tracking/ETL_CHANGE_LOG.md?d=w07ab4b5821014b0c89dc509a89efd845&csf=1&web=1&e=otX4wg)
- **Live Link: [ETL change log](change%20tracking/ETL_CHANGE_LOG.md) **Sharepoint Link: [ETL change log](https://birminghamcitycouncil.sharepoint.com/:t:/r/sites/PRJ0048180-WMPPProject/Shared%20Documents/General/Phase%202/Dashboard%20%26%20Reporting%20Documents/Phase%202/99_Change_Tracking/ETL_CHANGE_LOG.md?d=w07ab4b5821014b0c89dc509a89efd845&csf=1&web=1&e=hHkEwC)

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
| `tests/` | Static Fabric-source validators and Gold Spark simulation |
| `tools/` | Fabric notebook conversion, parsing, and client comparison |

Do not create new `version NN` notebook folders. Update the active notebooks in this root, record material changes in the ETL issue/change log, and use Git tags or the repository archive for immutable milestones.
