# Notebook regression checks

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
