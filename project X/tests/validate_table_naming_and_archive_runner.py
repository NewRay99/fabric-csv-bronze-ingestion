"""Regression checks for source-named tables and archive orchestration."""

import ast
import json
import sys
from pathlib import Path


ROOT = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2
    else Path(__file__).resolve().parents[1]
)


def notebook_source(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    cells = []
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and not source.lstrip().startswith("%"):
            ast.parse(source, filename=f"{name}:cell-{index}")
        cells.append(source)
    return "\n".join(cells)


bronze = notebook_source("01_bronze_get_latest.ipynb")
live_capture = notebook_source("01a_cfg_schema_capture_live.ipynb")
silver = notebook_source("02_silver_formatter.ipynb")
archive_silver = notebook_source("02a_archive_silver.ipynb")
reset = notebook_source("00b_reset_silver_cfg.ipynb")
common = notebook_source("99_common_library.ipynb")
archive_capture = notebook_source("01a_cfg_schema_capture_archive.ipynb")
archive_runner = notebook_source("90_run_archive_pipeline.ipynb")

assert 'TABLE_PREFIX     = ""' in bronze
assert "TABLE_PREFIXES = ()" in live_capture
assert "LATEST_PREFIXES = ()" in silver
assert 'SILVER_TABLE_PREFIX = ""' in reset
assert "ETL_PHYSICAL_PREFIXES = ()" in common
assert "silver.slv_" not in silver + archive_silver + common
assert "brz_" not in bronze + live_capture + silver
assert "replace(c.table_name,'archived_','')" not in archive_capture
assert "ON c.table_name = l.table_name" in archive_capture
assert 'target_table = f"{SILVER_SCHEMA}.{contract_table}"' in silver
assert 'target_table = f"{SILVER_SCHEMA}.{contract_table}"' in archive_silver
assert 'normalise(entry["target_table"].split(".")[-1])' in archive_silver
assert 'startswith("archived_")' not in archive_silver
print("PASS active Bronze, Archive, and Silver targets use source names")


assert 'PIPELINE_NAME = "90_run_archive_pipeline"' in archive_runner
for notebook_name in [
    '"00_setup_cfg"',
    '"00_archive_load"',
    '"01a_cfg_schema_capture_archive"',
    '"02a_archive_silver"',
    '"05_gold_dimensions"',
]:
    assert notebook_name in archive_runner, f"archive runner missing {notebook_name}"
assert '"RUN_GOLD_DIMENSIONS_AT_MONTH_END": False' in archive_runner
for required in [
    "JOB_RUN_ID",
    "monitoring.cfg_job_run",
    "monitoring.cfg_job_step_run",
    "mssparkutils.notebook.run",
]:
    assert required in archive_runner, f"archive runner missing {required}"
print("PASS archive runner records and passes one JOB_RUN_ID across its steps")

print("VALIDATION PASSED")
