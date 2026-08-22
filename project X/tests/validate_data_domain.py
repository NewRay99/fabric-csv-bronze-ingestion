"""Static regression checks for the Bronze data-domain profiler."""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "99_data_domain.ipynb"
SETUP = ROOT / "00_setup_cfg.ipynb"


def notebook_source(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and source.strip():
            ast.parse(source, filename=f"{path.name}:cell-{index}")
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


source = notebook_source(NOTEBOOK)
setup_source = notebook_source(SETUP)

assert "monitoring.cfg_data_domain" in setup_source
for column in (
    "source_schema STRING",
    "source_table STRING",
    "column_name STRING",
    "contract_data_type STRING",
    "data_domain STRING",
    "distinct_value_count BIGINT",
):
    assert column in setup_source

assert 'BRONZE_SCHEMA = "bronze"' in source
assert 'CONTRACT_TABLE = "monitoring.cfg_schema_contract_column"' in source
assert 'DOMAIN_TABLE = "monitoring.cfg_data_domain"' in source
assert "MAX_DISTINCT_VALUES = 40" in source
assert "is_contract_string" in source
assert "limit(MAX_DISTINCT_VALUES + 1)" in source
assert ".distinct().limit(MAX_DISTINCT_VALUES + 1)" in source
assert "if len(values) > MAX_DISTINCT_VALUES" in source
assert ".option(\"replaceWhere\", predicate)" in source
assert "DeltaTable.forName(spark, DOMAIN_TABLE).delete(predicate)" in source
assert "mssparkutils.notebook.run" in source
assert "CFG_NOTEBOOK_NAME = \"00_setup_cfg\"" in source

print("VALIDATION PASSED")
