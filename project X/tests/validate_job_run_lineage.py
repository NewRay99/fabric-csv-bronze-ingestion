"""Static regression checks for linked live-pipeline monitoring."""

import ast
from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def notebook_source(name):
    notebook = read_notebook(ROOT / name)
    cells = []
    for index, cell in enumerate(notebook["cells"]):
        text = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and text.strip() and not text.lstrip().startswith("%"):
            ast.parse(text, filename=f"{name}:cell-{index}")
        cells.append(text)
    return "\n".join(cells)


setup = notebook_source("00_setup_cfg.py")
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

runner = notebook_source("90_run_live_pipeline.py")
for expected in (
    "JOB_RUN_ID = JOB_RUN_ID or str(uuid.uuid4())",
    "FORCE_RERUN = False",
    'child_parameters["FORCE_RERUN"] = str(FORCE_RERUN).lower()',
    "RUN_ESSENTIAL_DQ = True",
    'child_parameters["RUN_ESSENTIAL_DQ"] = str(RUN_ESSENTIAL_DQ).lower()',
    "monitoring.cfg_job_run",
    "monitoring.cfg_job_step_run",
    '"JOB_RUN_ID": JOB_RUN_ID',
    "record_step(step_sequence, notebook_name, \"RUNNING\"",
    "JOB_RUN_ID={JOB_RUN_ID}",
):
    assert expected in runner, f"live runner missing {expected}"

common = notebook_source("99_common_library.py")
assert 'JOB_RUN_ID = globals().get("JOB_RUN_ID", "")' in common
assert 'StructField("job_run_id", StringType(), True)' in common
assert '"job_run_id": "s.job_run_id"' in common
assert '.withColumn("job_run_id", F.lit(JOB_RUN_ID).cast("string"))' in common

silver = notebook_source("02_silver_formatter.py")
assert "job_run_id string" in silver
assert "JOB_RUN_ID or None" in silver
assert "FORCE_RERUN = False" in silver
assert "if (not FORCE_RERUN" in silver
assert "FORCE RERUN" in silver

dq = notebook_source("03_silver_business_rules.py")
assert 'frame.withColumn("job_run_id", F.lit(JOB_RUN_ID).cast("string"))' in dq
for expected in (
    "RUN_ESSENTIAL_DQ = False",
    'DQ_RUN_MODE = "ESSENTIAL" if RUN_ESSENTIAL_DQ else "THOROUGH"',
    'if RUN_ESSENTIAL_DQ:',
    'if (rule.get("severity") or "").upper() == "CRITICAL"',
    'f"LATEST_{DQ_RUN_MODE}"',
):
    assert expected in dq, f"Silver DQ mode control missing {expected}"

issue_log = (ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md").read_text(
    encoding="utf-8"
)
assert "## DQ-004" in issue_log
assert "RUN_ESSENTIAL_DQ" in issue_log
for table in (
    "monitoring.cfg_data_quality_result",
    "monitoring.cfg_rejected_row",
    "monitoring.cfg_referential_exception",
):
    assert table in dq and "JOB_RUN_ID or None" in dq

pipeline_children = {
    "00_archive_load.py": "00_archive_load",
    "02_silver_formatter.py": "02_silver_formatter",
    "02a_archive_silver.py": "02a_archive_silver",
    "03_silver_business_rules.py": "03_silver_business_rules",
}
for name, pipeline_name in pipeline_children.items():
    child = notebook_source(name)
    assert "PIPELINE_RUN_ID = JOB_RUN_ID or RUN_ID" in child, (
        f"{name} does not prefer the parent JOB_RUN_ID for its pipeline run"
    )
    assert "[(PIPELINE_RUN_ID," in child, (
        f"{name} writes cfg_pipeline_run with local RUN_ID instead of PIPELINE_RUN_ID"
    )
    pipeline_updates = [
        line for line in child.splitlines()
        if "WHERE run_id" in line and "cfg_pipeline_run" in child
    ]
    assert pipeline_updates and all("PIPELINE_RUN_ID" in line for line in pipeline_updates), (
        f"{name} does not update its shared pipeline run by PIPELINE_RUN_ID"
    )
    assert pipeline_name in child

print("PASS child pipeline records prefer JOB_RUN_ID and preserve local RUN_ID telemetry")

for name in (
    "01_bronze_get_latest.py",
    "01a_cfg_schema_capture_live.py",
    "02_silver_formatter.py",
    "03_silver_business_rules.py",
    "04_gold_model.py",
    "05_gold_dimensions.py",
):
    assert 'JOB_RUN_ID = ""' in notebook_source(name), f"{name} cannot receive JOB_RUN_ID"

print("VALIDATION PASSED")
