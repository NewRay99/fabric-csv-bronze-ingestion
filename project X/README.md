# WMPP data platform — Birmingham Children's Trust

This folder is the active, deployable BCT implementation. The `.ipynb` files
in this folder are the current notebook set promoted from version 02 04 on
16 August 2026. Superseded notebook trees are retained under the repository
`archive` folder.

## Start here

- [Notebook runbook](client%20documentation/05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md)
- [High-Level Design](client%20documentation/03_Architecture_and_Design/HLD.md)
- [Technical/Functional Design](client%20documentation/03_Architecture_and_Design/TFD.md)
- [Client documentation index](client%20documentation/README.md)
- [ETL issue and change log](change%20tracking/ETL_ISSUE_AND_CHANGE_LOG.md)

## Active notebook set

| Notebook | Purpose |
|---|---|
| `99_common_library.ipynb` | Consolidated exclusions, schema-conformance, audit, and Silver helpers |
| `00_setup_cfg.ipynb` | Creates/upgrades all monitoring and configuration tables |
| `00_archive_load.ipynb` | Loads dated archive ZIP/file extracts into source-named `archived` Delta tables |
| `00a_rehydrate_archive_cfg.ipynb` | Reconstructs archive controls for an existing deployment |
| `00b_reset_silver_cfg.ipynb` | Guarded administrative reset for Silver replay |
| `01_bronze_get_latest.ipynb` | Loads the latest source extracts into Bronze |
| `01a_cfg_schema_capture_live.ipynb` | Captures live Bronze schema and records drift |
| `01a_cfg_schema_capture_archive.ipynb` | Captures/compares the archive catalogue schema |
| `02_silver_formatter.ipynb` | Formats the current Bronze batch into Silver |
| `02a_archive_silver.ipynb` | Replays canonical historical month-end states into Silver/Gold |
| `03_silver_business_rules.ipynb` | Runs schema-driven DQ and referential-integrity checks |
| `04_gold_model.ipynb` | Builds the current/historical referral Gold model and snapshots |
| `05_gold_dimensions.ipynb` | Builds Gold reporting dimensions and provider bridges from Silver |
| `90_run_live_pipeline.ipynb` | Runs the standard live Bronze-to-Gold notebook sequence |

## Supporting folders

| Folder | Contents |
|---|---|
| `configuration/` | `schema_definition.csv`, DQ rules, and schema-drift review workbook |
| `client documentation/` | Controlled client documentation and operational runbooks |
| `change tracking/` | ETL issue/change history and semantic-model changelog |
| `assets/` | Brand material, screenshots, and design previews |
| `reports/` | Current/client report packages |
| `tests/` | Static notebook validators and Gold Spark simulation |

Do not create new `version NN` notebook folders. Update the active notebooks in
this root, record material changes in the ETL issue/change log, and use Git tags
or the repository archive for immutable milestones.
