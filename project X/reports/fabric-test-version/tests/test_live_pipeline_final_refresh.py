"""Exercise final monitoring publication with fake Spark and child notebooks."""

from pathlib import Path
import sys
from types import SimpleNamespace

from notebook_loader import load_notebook
import pytest


PROJECT = Path(__file__).resolve().parents[1]
REFRESH_VIEWS = (
    "monitoring.rpt_job_step_timing",
    "monitoring.rpt_job_step_summary",
    "monitoring.rpt_job_run_summary",
    "monitoring.rpt_job_schema_drift",
    "monitoring.rpt_job_data_quality",
    "monitoring.rpt_job_layer_lineage",
)


def execute_notebook(name, scope):
    for cell in load_notebook(PROJECT / f"{name}.py")["cells"]:
        code = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and not code.lstrip().startswith("%"):
            exec(compile(code, f"{name}.py", "exec"), scope)


@pytest.mark.parametrize("runner, failed_child, views_exist", [
    ("90_run_live_pipeline", None, False),
    ("90_run_live_pipeline", None, True),
    ("90_run_live_pipeline", "04_gold_model", True),
    ("90_run_live_pipeline", "06_reports", True),
    ("90_run_archive_pipeline", None, False),
    ("90_run_archive_pipeline", None, True),
    ("90_run_archive_pipeline", "00_archive_load", True),
    ("90_run_archive_pipeline", "06_reports", True),
])
@pytest.mark.parametrize("refresh_fails", [False, True])
def test_final_refresh_captures_closed_job_and_preserves_etl_outcome(
    monkeypatch, capsys, runner, failed_child, views_exist, refresh_fails,
):
    jobs = []
    steps = {}
    materialized = {view: None for view in REFRESH_VIEWS} if views_exist else {}
    creations = []
    refreshes = []

    def merge_monitor_row(table, row, schema, condition):
        record = dict(zip((field.split()[0] for field in schema.split(",")), row))
        if table == "monitoring.cfg_job_run":
            jobs.append(record)
        else:
            steps[record["step_sequence"]] = record

    class Spark:
        def sql(self, query):
            if query.startswith("REFRESH MATERIALIZED LAKE VIEW"):
                refreshes.append((query, dict(jobs[-1])))
                if refresh_fails:
                    raise RuntimeError("synthetic refresh failure")
                view = query.split()[4]
                if view not in materialized:
                    raise RuntimeError(f"View does not exist: {view}")
            else:
                tokens = query.split()
                view = tokens[tokens.index("AS") - 1]
                if "IF NOT EXISTS" in query and view in materialized:
                    return
                creations.append(view)
            if view == REFRESH_VIEWS[0]:
                materialized[view] = [dict(step) for step in steps.values()]
            elif view == REFRESH_VIEWS[1]:
                materialized[view] = [dict(step) for step in materialized[REFRESH_VIEWS[0]]]
            else:
                materialized[view] = dict(jobs[-1])

    spark = Spark()

    def run_child(name, timeout, parameters):
        if name == "06_reports":
            execute_notebook(name, {"spark": spark})
        if name == failed_child:
            raise RuntimeError("synthetic child failure")
        return "synthetic success"

    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        mssparkutils=SimpleNamespace(notebook=SimpleNamespace(run=run_child)),
    ))
    scope = {"merge_monitor_row": merge_monitor_row, "spark": spark}
    if failed_child:
        with pytest.raises(RuntimeError, match="^synthetic child failure$"):
            execute_notebook(runner, scope)
    else:
        execute_notebook(runner, scope)

    expected_status = "FAILED" if failed_child else "SUCCESS"
    assert jobs[-1]["status"] == expected_status
    assert jobs[-1]["ended_at"] is not None
    assert creations == ([] if views_exist else list(REFRESH_VIEWS))
    expected_views = REFRESH_VIEWS[:1] if refresh_fails else REFRESH_VIEWS
    assert [query for query, _ in refreshes] == [
        f"REFRESH MATERIALIZED LAKE VIEW {view} FULL" for view in expected_views
    ]
    assert all(job == jobs[-1] for _, job in refreshes)
    if refresh_fails:
        assert "WARNING: Monitoring refresh failed: synthetic refresh failure" in (
            capsys.readouterr().out
        )
    else:
        assert materialized[REFRESH_VIEWS[2]] == jobs[-1]
        for view in REFRESH_VIEWS[:2]:
            assert materialized[view] == list(steps.values())
            assert all(step["ended_at"] is not None for step in materialized[view])
