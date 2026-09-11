"""Static checks for job-level monitoring, lineage, drift and DQ views."""

import ast
from notebook_loader import load_notebook as read_notebook
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


def source(name):
    notebook = read_notebook(PROJECT / name)
    text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    for index, cell in enumerate(notebook["cells"]):
        code = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and code.strip() and not code.lstrip().startswith("%"):
            ast.parse(code, filename=f"{name}:cell-{index}")
    return text


setup = source("00_setup_cfg.py")
for expected in (
    "monitoring.cfg_gold_lineage_mapping",
    "monitoring.vw_job_step_timing",
    "monitoring.vw_job_step_summary",
    "monitoring.vw_job_run_summary",
    "monitoring.vw_job_schema_drift",
    "monitoring.vw_job_data_quality",
    "monitoring.vw_job_layer_lineage",
    "cfg_schema_drift_event",
    "job_run_id STRING",
):
    assert expected in setup, f"setup is missing {expected}"

for notebook in (
    "01a_cfg_schema_capture_live.py",
    "02_silver_formatter.py",
    "02a_archive_silver.py",
):
    text = source(notebook)
    assert "job_run_id string" in text, f"{notebook} does not write job-linked drift"
    assert "JOB_RUN_ID" in text, f"{notebook} cannot associate drift with a job"

print("VALIDATION PASSED")
