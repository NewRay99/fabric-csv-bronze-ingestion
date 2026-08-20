"""Static regression checks for linked live-pipeline monitoring."""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def notebook_source(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    cells = []
    for index, cell in enumerate(notebook["cells"]):
        text = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and text.strip() and not text.lstrip().startswith("%"):
            ast.parse(text, filename=f"{name}:cell-{index}")
        cells.append(text)
    return "\n".join(cells)


setup = notebook_source("00_setup_cfg.ipynb")
for table in ("monitoring.cfg_job_run", "monitoring.cfg_job_step_run"):
    assert table in setup, f"setup must create/upgrade {table}"
for table in (
    "cfg_silver_export_load",
    "cfg_pipeline_run",
    "cfg_table_load_metric",
    "cfg_data_quality_result",
    "cfg_rejected_row",
    "cfg_referential_exception",
):
    start = setup.index(f'"monitoring.{table}"')
    end = setup.find("    ],", start)
    assert "job_run_id STRING" in setup[start:end], f"{table} lacks job_run_id"

runner = notebook_source("90_run_live_pipeline.ipynb")
for expected in (
    "JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())",
    "monitoring.cfg_job_run",
    "monitoring.cfg_job_step_run",
    '"JOB_RUN_ID": JOB_RUN_ID',
    "record_step(step_sequence, notebook_name, \"RUNNING\"",
    "JOB_RUN_ID={JOB_RUN_ID}",
):
    assert expected in runner, f"live runner missing {expected}"

common = notebook_source("99_common_library.ipynb")
assert 'JOB_RUN_ID = globals().get("JOB_RUN_ID", "")' in common
assert 'StructField("job_run_id", StringType(), True)' in common
assert '"job_run_id": "s.job_run_id"' in common

silver = notebook_source("02_silver_formatter.ipynb")
assert "job_run_id string" in silver
assert "JOB_RUN_ID or None" in silver

dq = notebook_source("03_silver_business_rules.ipynb")
for table in (
    "monitoring.cfg_data_quality_result",
    "monitoring.cfg_rejected_row",
    "monitoring.cfg_referential_exception",
):
    assert table in dq and "JOB_RUN_ID or None" in dq

for name in (
    "01_bronze_get_latest.ipynb",
    "01a_cfg_schema_capture_live.ipynb",
    "02_silver_formatter.ipynb",
    "03_silver_business_rules.ipynb",
    "04_gold_model.ipynb",
    "05_gold_dimensions.ipynb",
):
    assert 'JOB_RUN_ID = ""' in notebook_source(name), f"{name} cannot receive JOB_RUN_ID"

print("VALIDATION PASSED")
