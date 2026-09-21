"""Validate the Mission Control job-run to job-step semantic contract."""

from pathlib import Path
from zipfile import ZipFile

from validate_mission_control_model import comparable_tmdl, validate_measures_table


ROOT = Path(__file__).resolve().parents[1]
WORK_PROJECT = (
    ROOT
    / "reports/client-deliverables/_mission_control_align_work"
    / "SM WMPP Mission Control - SEM-02 repaired"
)
ALIGNED_ZIP = (
    ROOT
    / "reports/client-deliverables"
    / "SM WMPP Mission Control - SEM-02 repaired - job drill aligned.zip"
)
ZIP_PREFIX = "SM WMPP Mission Control - SEM-02 repaired/"
DEFINITION = "SM WMPP Mission Control.SemanticModel/definition/"


def read_project_file(relative_path):
    """Read from the temporary project during build or the checked-in ZIP."""
    unpacked = WORK_PROJECT / relative_path
    if unpacked.exists():
        return unpacked.read_text(encoding="utf-8-sig")
    assert ALIGNED_ZIP.exists(), f"Aligned Mission Control package is missing: {ALIGNED_ZIP}"
    with ZipFile(ALIGNED_ZIP) as archive:
        return archive.read(ZIP_PREFIX + relative_path).decode("utf-8-sig")


model = read_project_file(DEFINITION + "model.tmdl")
relationships = read_project_file(DEFINITION + "relationships.tmdl")
job_runs = read_project_file(DEFINITION + "tables/rpt_job_run_summary.tmdl")
job_steps = read_project_file(DEFINITION + "tables/rpt_job_step_timing.tmdl")
pipeline_runs = read_project_file(DEFINITION + "tables/cfg_pipeline_run.tmdl")
deployed_measures_text = read_project_file(
    DEFINITION + "tables/_MissionControl_Measures.tmdl"
)
source_measures_path = ROOT / "reports/current/_MissionControl_Measures.tmdl"
source_measures_text, source_measures = validate_measures_table(source_measures_path)

assert len(source_measures) == 87, "Expected 67 original plus 20 job drill measures"
assert comparable_tmdl(source_measures_text) == comparable_tmdl(deployed_measures_text)

for table_name in ("rpt_job_run_summary", "rpt_job_step_timing"):
    assert model.splitlines().count(f"ref table {table_name}") == 1
    assert table_name in model.split("annotation PBI_QueryOrder = ", 1)[1].splitlines()[0]

assert "fromColumn: rpt_job_step_timing.job_run_id" in relationships
assert "toColumn: rpt_job_run_summary.job_run_id" in relationships
assert "fromColumn: cfg_pipeline_run.job_run_id" in relationships
assert relationships.count("toColumn: rpt_job_run_summary.job_run_id") == 2
assert "crossFilteringBehavior: bothDirections" not in relationships

for field in (
    "job_run_id", "pipeline_name", "started_at", "ended_at", "status",
    "steps_succeeded", "steps_failed", "error_message",
    "job_duration_seconds",
):
    assert f"column {field}" in job_runs, f"Job summary is missing {field}"

for field in (
    "job_run_id", "step_sequence", "notebook_name", "status", "started_at",
    "ended_at", "step_duration_seconds", "gap_from_previous_step_seconds",
    "child_result", "error_message",
):
    assert f"column {field}" in job_steps, f"Job step timing is missing {field}"

assert "column job_run_id" in pipeline_runs
for required_measure in (
    "Latest Job Run ID",
    "Selected or Latest Job Run ID",
    "Selected or Latest Job Error",
    "Selected or Latest Failed Steps",
    "Show Step for Selected or Latest Job Run",
    "Selected Step Error Detail",
):
    assert required_measure in source_measures

semantic_text = "\n".join((model, relationships, job_runs, job_steps, pipeline_runs))
for forbidden in ("LocalDateTable_", "DateTableTemplate_", "variation Variation"):
    assert forbidden not in semantic_text

guide = (
    ROOT
    / "client documentation/04_Data_and_Reporting"
    / "MISSION_CONTROL_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md"
).read_text(encoding="utf-8")
for expected in (
    "Same-page latest job, historical Gantt and step detail",
    "Show Step for Selected or Latest Job Run",
    "set its interaction",
    "with the step table to **Filter**",
    "error_message",
):
    assert expected in guide

print("PASS Mission Control latest-job, Gantt selection, step and error contract")
