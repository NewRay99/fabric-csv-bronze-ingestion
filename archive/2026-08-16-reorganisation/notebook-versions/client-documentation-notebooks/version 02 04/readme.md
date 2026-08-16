# Version 02 03 notebooks

## Shared library and configuration setup

`99_common_library 02 03.ipynb` now owns a safe default
`TIME_PARSER_POLICY = "CORRECTED"`. It can run independently or inherit an
explicit value from a parent notebook.

`00_setup_cfg 02 03.ipynb` also declares the parser policy in its parameter
cell because Fabric child notebooks execute in their own scope. Setup callers
pass resolved parameter values:

```python
cfg_result = mssparkutils.notebook.run(
    CFG_NOTEBOOK_NAME,
    NOTEBOOK_TIMEOUT_SECONDS,
    {"AUDIT_TABLE": AUDIT_TABLE, "TIME_PARSER_POLICY": TIME_PARSER_POLICY},
)
```

The literal `"{AUDIT_TABLE}"` and empty audit-table arguments are not used.
This correction is applied to the latest Silver, archive Silver, archive
rehydration, and Silver-reset notebooks.

## Missing schema contracts

A source table missing completely from `schema_definition.csv` is an auditable
skip, not a failed Silver run. Both Silver formatters:

- write `SKIPPED_NO_CONTRACT` to `monitoring.cfg_silver_export_load` using the
  source table's real export date;
- write `MISSING_TABLE_CONTRACT` to
  `monitoring.cfg_schema_drift_event`;
- print one concise skip message; and
- continue to the next table.

This allows tables such as `archived.archived_provider_sic_codes` to be flagged
without stopping the remaining monthly Silver and Gold processing. When its
contract is later added, the existing non-success audit status allows it to be
loaded normally on the next run.

## Validation

Run:

```text
python validate_version02_03.py
```

The static regression validates notebook JSON/Python, parser-policy ownership,
resolved child-notebook parameters, reset helper ordering, and non-fatal
missing-contract logging. Fabric remains required for the Spark/Delta and
cross-notebook execution test.
