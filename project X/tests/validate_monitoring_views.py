"""Static checks for job-level monitoring, lineage, drift and DQ views."""

import ast
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]


def source(name):
    notebook = json.loads((PROJECT / name).read_text(encoding="utf-8"))
    text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    for index, cell in enumerate(notebook["cells"]):
        code = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and code.strip() and not code.lstrip().startswith("%"):
            ast.parse(code, filename=f"{name}:cell-{index}")
    return text


setup = source("00_setup_cfg.ipynb")
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
    "01a_cfg_schema_capture_live.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
):
    text = source(notebook)
    assert "job_run_id string" in text, f"{notebook} does not write job-linked drift"
    assert "JOB_RUN_ID" in text, f"{notebook} cannot associate drift with a job"

print("VALIDATION PASSED")
