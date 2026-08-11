# Version 01 validation

Validated locally on 4 August 2026:

- All seven `.ipynb` files parse as valid Notebook 4 JSON.
- All Python code cells compile successfully after excluding Fabric `%%sql` cells.
- The schema contract contains 57 tables and exactly one `export_date` column per table.
- Every `export_date` contract column is nullable `timestamp without time zone`.
- Gold-layer Silver references resolve to the `silver.slv_<table>` naming convention.
- Resumable-load static checks confirm export auditing, reload control, failed-month retry, canonical month-end materialisation, and the `AS_OF_DATE` hand-off are present.
- Archive-ingestion static checks confirm global table/export, ZIP, and file controls; row-level `export_date`; source-file replacement where file lineage exists; export-date-only rehydration for older tables; and exclusion of the non-contract `archived_audit` table.
- Date-only `2026-07-26` and fractional timestamp values `2026-05-19 08:51:41.0` and `2026-06-05 09:28:43.959135` are covered by the corrected Spark parser configuration in both Silver notebooks.
- Archive replay statically confirms one canonical batch per calendar month, exact selected-export filtering, primary-key `row_number()` deduplication, verbose identifier/date diagnostics, and a hard null-`export_date` gate before Gold.
- `framework_category` and `ipa_child_support_needs` now have complete contracts, and duplicate ordinal rows were removed from `provider_document` and `submission_documents`.
- No retired secondary-Silver-schema or pre-rename notebook references remain in version 01.
- The DQ rule catalogue contains five rules, and every referenced table and column exists in the schema contract.

The notebooks were not executed end-to-end locally because they require a
Microsoft Fabric Spark session, Lakehouse tables, Delta Lake, `notebookutils`,
and the configured `Files/cfg_files` path. End-to-end execution should be run
in Fabric in this order:

1. `01_bronze_get_latest 02 03.ipynb`
2. `02_silver_formatter 02 03.ipynb`
3. `03_silver_business_rules 02 03.ipynb`
4. `04_gold_model 02 03.ipynb`

Historical replay should be tested separately with `02a_archive_silver 02 03.ipynb`
after running `00_archive_load 02 03.ipynb` and confirming the archive tables contain
valid row-level `export_date` values. `_archive_source_path` is optional for
Silver/Gold replay. For an existing deployment, run
`00a_rehydrate_archive_cfg 02 03.ipynb` first; only tables reported as genuinely
missing `export_date` require correction before replay.

The first Fabric run should confirm that the latest Bronze source contains the
expected contract tables and that `export_date` is populated from the source
or, when absent, stamped at Bronze load time.

Run the portable static regression locally with:

```text
python validate_version01.py
```
