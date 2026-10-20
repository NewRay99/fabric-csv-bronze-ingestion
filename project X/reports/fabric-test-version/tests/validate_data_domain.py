"""Static regression checks for the Bronze data-domain profiler."""

import ast
from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "99_data_domain.py"
COMMON_LIBRARY = ROOT / "99_common_library.py"
SETUP = ROOT / "00_setup_cfg.py"


def notebook_source(path: Path) -> str:
    notebook = read_notebook(path)
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if (
            cell.get("cell_type") == "code"
            and source.strip()
            and not source.lstrip().startswith("%")
        ):
            ast.parse(source, filename=f"{path.name}:cell-{index}")
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


source = notebook_source(NOTEBOOK)
common_source = notebook_source(COMMON_LIBRARY)
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
assert "CLEAR_TARGET_TABLE" not in source
assert "%run ./99_common_library" in source
assert "collect_low_cardinality_domain_values" in source
assert "data_domain_exclusion_reason(column_name, contract_data_type)" in source
assert "skipped_unsuitable" in source
assert "if values is None" in source
assert "remove_data_domain(DOMAIN_TABLE" not in source
assert "clear_data_domain_table(DOMAIN_TABLE)" not in source
assert "replace_data_domain(" not in source
assert "append_data_domain_snapshots(DOMAIN_TABLE, snapshots)" in source
assert "latest_data_domain_profiles(DOMAIN_TABLE)" in source
assert "JOB_RUN_ID = JOB_RUN_ID or RUN_ID" in source
assert "def record_domain_job" in source
for field in ("previous_run_id STRING", "previous_profiled_at TIMESTAMP",
              "change_type STRING", "is_present BOOLEAN", "profile_status STRING"):
    assert field in setup_source
assert "def build_data_domain_snapshot" in common_source
assert "def append_data_domain_snapshots" in common_source
assert 'mode("append").saveAsTable(domain_table)' in common_source
assert "def is_contract_string" not in source
assert "mssparkutils.notebook.run" in source
assert "CFG_NOTEBOOK_NAME = \"00_setup_cfg\"" in source

assert "def is_contract_string" in common_source
assert "def data_domain_exclusion_reason" in common_source
assert "identifier_type" in common_source
assert "email_address" in common_source
assert "audit_user" in common_source
assert "free_text" in common_source
assert "def collect_low_cardinality_domain_values" in common_source
assert "max_distinct_values + 1" in common_source
assert "if len(values) > max_distinct_values" in common_source
assert "def clear_data_domain_table" in common_source
assert "def replace_data_domain" in common_source
assert ".option(\"replaceWhere\", predicate)" in common_source

print("VALIDATION PASSED")
