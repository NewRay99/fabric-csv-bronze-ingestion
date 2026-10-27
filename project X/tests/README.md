# Notebook regression checks

## GLD-026 — Referral creator regression

Run from the repository root:

```powershell
python -m pytest "project X/tests/test_gold_referral_created_by.py" "project X/tests/test_gold_referral_source_status.py" "project X/tests/test_gold_referral_source_reference.py" "project X/tests/test_gold_referral_journey_status.py"
python -m pytest "project X/tests/test_validation_scripts.py"
```

These checks execute complete production referral SQL against synthetic Silver data with SQLite date/timestamp adaptations, test exact creator/NULL preservation and current-row ordering, exercise the production preflight and assert snapshot exclusion. Existing coverage also requires the SQL fixture to match production. The Spark simulation asserts a known creator and NULL each month; it remains a separate Spark/Delta runtime check, not part of portable pytest or Fabric acceptance.

To build a separate test project in the Fabric Git folder format used by
`reports/Notebooks v16.zip`, run from the repository root:

```powershell
python "project X/tools/build_fabric_test_version.py"
```

The output is `project X/reports/fabric-test-version`, with current numbered
Python source copied into `notebooks/<name>.Notebook/notebook-content.py` and
its own `tests` folder. ZIP notebook metadata is retained; current source
replaces the ZIP code. The builder refuses to overwrite an existing output;
use `--output` with a new directory for another snapshot. See the output README
for the test command and runtime limits.

The numbered `.py` notebooks in `project X` are the primary source. Every
notebook validator and the Gold SQL extractor reads that source through
`notebook_loader.py`, which uses the shared Fabric parser in
`../tools/fabric_notebooks.py`. No validator falls back to the retained `.ipynb`
migration references.

The parser preserves cell boundaries, parameter tags, Markdown, `%run`, SQL
magic and metadata so the existing business checks still inspect notebook
semantics. Python syntax checks run on decoded Python cells, not on the whole
Fabric file containing notebook magic commands.

From the repository root:

```powershell
python -m pytest
python "project X/tests/validate_table_naming_and_archive_runner.py"
```

`test_validation_scripts.py` runs an explicit allowlist of active Python/ETL
validators as subprocesses. Obsolete semantic-model, DAX, report-project and
associated helper tests have been removed from this folder, so neither pytest
nor the test-folder Ruff pre-commit hook checks them. No ignore list is needed.
`test_fabric_notebooks.py` covers the format boundary and every primary notebook.
Tests do not require the supplied client snapshot; the comparison is generated
separately with `python "project X/tools/fabric_notebooks.py" compare`.

`_extract_gold_sql.py` extracts SQL from primary `04_gold_model.py` for the
simulation fixture. `_gold_sim_test.py` requires PySpark/Delta dependencies and
may need a compatible Spark environment. End-to-end notebook orchestration and
Fabric import/deployment remain Fabric acceptance tests.
