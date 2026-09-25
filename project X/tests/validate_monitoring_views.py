"""Static checks for job-level monitoring, lineage, drift and DQ objects."""

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
reports = source("06_reports.py")
for expected in (
    "monitoring.rpt_job_step_timing",
    "monitoring.rpt_job_step_summary",
    "monitoring.rpt_job_run_summary",
    "monitoring.rpt_job_schema_drift",
    "monitoring.rpt_job_data_quality",
    "monitoring.rpt_job_layer_lineage",
):
    assert reports.count(f"CREATE OR REPLACE MATERIALIZED LAKE VIEW {expected} AS") == 1, (
        f"06_reports is missing or duplicates {expected}"
    )

assert "monitoring.cfg_gold_lineage_mapping" in setup
assert "cfg_schema_drift_event" in setup
assert "job_run_id STRING" in setup
assert "CREATE OR REPLACE MATERIALIZED LAKE VIEW" not in setup, (
    "00_setup_cfg must not define reporting views before the ETL runs"
)
assert "FROM monitoring.rpt_job_step_timing s" in reports, (
    "rpt_job_step_summary still depends on a retired vw_* object"
)
assert "CREATE OR REPLACE VIEW monitoring.vw_job_" not in reports, (
    "06_reports must not recreate retired monitoring vw_* objects"
)
for runner in ("90_run_live_pipeline.py", "90_run_archive_pipeline.py"):
    steps = source(runner)
    assert steps.index('("05_gold_dimensions", {})') < steps.index('("06_reports", {})')
    assert steps.count('("06_reports", {})') == 1

for notebook in (
    "01a_cfg_schema_capture_live.py",
    "02_silver_formatter.py",
    "02a_archive_silver.py",
):
    text = source(notebook)
    assert "job_run_id string" in text, f"{notebook} does not write job-linked drift"
    assert "JOB_RUN_ID" in text, f"{notebook} cannot associate drift with a job"

print("VALIDATION PASSED")
