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
| `common_util.ipynb` | Shared `ref_*` and internal-table exclusion policy |
| `00_setup_cfg 02 03.ipynb` | Creates/upgrades all monitoring and configuration tables |
| `00_archive_load 02 03.ipynb` | Loads dated archive ZIP/file extracts into `archived` Delta tables |
| `00a_rehydrate_archive_cfg 02 03.ipynb` | Reconstructs archive controls for an existing deployment |
| `00b_reset_silver_cfg 02 03.ipynb` | Guarded administrative reset for Silver replay |
| `01_bronze_get_latest 02 03.ipynb` | Loads the latest source extracts into Bronze |
| `01a_cfg_schema_capture_live 02 03.ipynb` | Captures live Bronze schema and records drift |
| `01a_cfg_schema_capture_archive 02 03.ipynb` | Captures/compares the archive catalogue schema |
| `02_silver_formatter 02 03.ipynb` | Formats the current Bronze batch into Silver |
| `02a_archive_silver 02 03.ipynb` | Replays canonical historical month-end states into Silver/Gold |
| `03_silver_business_rules 02 03.ipynb` | Runs schema-driven DQ and referential-integrity checks |
| `04_gold_model 02 03.ipynb` | Builds the current/historical referral Gold model and snapshots |
| `99_common_library 02 03.ipynb` | Legacy/shared parsing helpers retained for compatibility |

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
