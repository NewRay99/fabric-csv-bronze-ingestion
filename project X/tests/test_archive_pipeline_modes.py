"""Exercise the archive runner with fake children; never run Spark or delete data."""

import ast
from pathlib import Path
import sys
from types import SimpleNamespace

from notebook_loader import load_notebook
import pytest


PROJECT = Path(__file__).resolve().parents[1]
NIGHTLY_STEPS = [
    "00_setup_cfg", "00_archive_load", "01a_cfg_schema_capture_archive", "06_reports",
]
REPLAY_STEPS = NIGHTLY_STEPS[:-1] + [
    "02a_archive_silver", "05_gold_dimensions", "06_reports",
]


def code_cells(name):
    return [cell for cell in load_notebook(PROJECT / f"{name}.py")["cells"]
            if cell["cell_type"] == "code"]


def execute_parameters(name, overrides=None):
    cell = next(cell for cell in code_cells(name)
                if "parameters" in cell["metadata"].get("tags", []))
    scope = {}
    exec("".join(cell["source"]), scope)
    scope.update(overrides or {})
    return scope


def run_runner(monkeypatch, overrides=None, fail_at=None):
    calls = []
    records = []

    def run_child(name, timeout, parameters):
        calls.append((name, timeout, parameters))
        if name == fail_at:
            raise RuntimeError("synthetic child failure")
        return "synthetic success"

    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        mssparkutils=SimpleNamespace(notebook=SimpleNamespace(run=run_child)),
    ))
    scope = execute_parameters("90_run_archive_pipeline", overrides)
    scope["merge_monitor_row"] = lambda *args: records.append(args)

    def execute():
        for cell in code_cells("90_run_archive_pipeline"):
            source = "".join(cell["source"])
            if "parameters" not in cell["metadata"].get("tags", []) and not source.lstrip().startswith("%"):
                exec(source, scope)

    return execute, scope, calls, records


@pytest.mark.parametrize("mode, expected", [
    ("ARCHIVE_ONLY", NIGHTLY_STEPS), ("REPLAY", REPLAY_STEPS),
])
def test_selected_route_dispatches_and_records_one_job(monkeypatch, mode, expected):
    execute, scope, calls, records = run_runner(monkeypatch, {
        "ARCHIVE_RUN_MODE": mode, "JOB_RUN_ID": "synthetic-parent",
    })
    execute()
    assert [name for name, _, _ in calls] == expected
    assert all(timeout == 9200 for _, timeout, _ in calls)
    assert all(parameters["JOB_RUN_ID"] == "synthetic-parent" for _, _, parameters in calls)
    assert calls[2][2]["COMPARED_SCHEMA"] == "archived"
    assert scope["status"] == "SUCCESS"
    jobs = [row for table, row, _, _ in records if table == "monitoring.cfg_job_run"]
    assert jobs[-1][0] == "synthetic-parent"
    assert jobs[-1][4:7] == ("SUCCESS", len(expected), 0)
    steps = [row for table, row, _, _ in records
             if table == "monitoring.cfg_job_step_run" and row[5] == "SUCCESS"]
    assert [row[1] for row in steps] == list(range(1, len(expected) + 1))
    assert [row[2] for row in steps] == expected


def test_nightly_is_default_and_never_runs_business_rebuilds(monkeypatch):
    execute, _, calls, _ = run_runner(monkeypatch)
    execute()
    assert [name for name, _, _ in calls] == NIGHTLY_STEPS
    assert execute_parameters("00_archive_load")["RESET_ARCHIVE_TABLES"] is False


@pytest.mark.parametrize("overrides", [
    {"ARCHIVE_RUN_MODE": "incorrect"},
    {"PROCESS_ONLY": "2026-05"},
    {"RESET_MONTH_MONITORING": True},
    {"CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY": True},
    {"CONFIRM_PROCESS_ONLY_RESET": "RESET ALL"},
    {"RESET_MONTH_MONITORING": "maybe"},
    {"ARCHIVE_RUN_MODE": "REPLAY", "PROCESS_ONLY": "2026-5"},
    {"ARCHIVE_RUN_MODE": "REPLAY", "PROCESS_ONLY": "2026-13"},
    {"ARCHIVE_RUN_MODE": "REPLAY", "RESET_MONTH_MONITORING": True},
    {"ARCHIVE_RUN_MODE": "REPLAY", "CONFIRM_PROCESS_ONLY_RESET": "RESET ALL"},
    {"ARCHIVE_RUN_MODE": "REPLAY", "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY": True,
     "CONFIRM_PROCESS_ONLY_RESET": "RESET ALL"},
    {"ARCHIVE_RUN_MODE": "REPLAY", "PROCESS_ONLY": "2026-05",
     "RESET_MONTH_MONITORING": True, "CONFIRM_PROCESS_ONLY_RESET": "RESET ALL"},
])
def test_invalid_or_conflicting_controls_fail_before_any_child(monkeypatch, overrides):
    execute, _, calls, records = run_runner(monkeypatch, overrides)
    with pytest.raises(ValueError):
        execute()
    assert calls == []
    assert records == []


def test_normalises_fabric_string_flags_before_selecting_route(monkeypatch):
    execute, scope, calls, _ = run_runner(monkeypatch, {
        "ARCHIVE_RUN_MODE": " archive_only ", "STOP_ON_ERROR": "true",
        "RESET_MONTH_MONITORING": "false", "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY": "0",
    })
    execute()
    assert [name for name, _, _ in calls] == NIGHTLY_STEPS
    assert scope["RESET_MONTH_MONITORING"] is False
    assert scope["CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY"] is False


@pytest.mark.parametrize("month, confirmation", [("", "RESET ALL"), ("2026-05", "RESET 2026-05")])
def test_confirmed_replay_forwards_controls_without_resetting_raw_archive(monkeypatch, month, confirmation):
    execute, _, calls, _ = run_runner(monkeypatch, {
        "ARCHIVE_RUN_MODE": "REPLAY", "PROCESS_ONLY": month,
        "RESET_MONTH_MONITORING": "true", "CONFIRM_PROCESS_ONLY_RESET": confirmation,
        "DEFAULT_LOCATION_CITY": "Coventry",
    })
    execute()
    parameters = next(parameters for name, _, parameters in calls if name == "02a_archive_silver")
    assert parameters["RESET_MONTH_MONITORING"] is True
    assert parameters["PROCESS_ONLY"] == month
    assert parameters["CONFIRM_PROCESS_ONLY_RESET"] == confirmation
    assert parameters["RUN_GOLD_DIMENSIONS_AT_MONTH_END"] is False
    assert parameters["DEFAULT_LOCATION_CITY"] == "Coventry"
    archive_parameters = next(parameters for name, _, parameters in calls if name == "00_archive_load")
    assert "RESET_ARCHIVE_TABLES" not in archive_parameters


@pytest.mark.parametrize("mode, fail_at", [
    ("ARCHIVE_ONLY", "00_archive_load"), ("REPLAY", "02a_archive_silver"),
])
def test_child_failure_stops_and_marks_parent_failed(monkeypatch, mode, fail_at):
    execute, _, calls, records = run_runner(monkeypatch, {"ARCHIVE_RUN_MODE": mode}, fail_at)
    with pytest.raises(RuntimeError, match="synthetic child failure"):
        execute()
    assert calls[-1][0] == fail_at
    assert "06_reports" not in [name for name, _, _ in calls]
    jobs = [row for table, row, _, _ in records if table == "monitoring.cfg_job_run"]
    assert jobs[-1][4:7] == ("FAILED", len(calls) - 1, 1)


def test_continue_on_error_still_fails_the_completed_job(monkeypatch):
    execute, _, calls, records = run_runner(monkeypatch, {"STOP_ON_ERROR": "false"}, "00_archive_load")
    with pytest.raises(RuntimeError, match="Archive pipeline failed"):
        execute()
    assert [name for name, _, _ in calls] == NIGHTLY_STEPS
    jobs = [row for table, row, _, _ in records if table == "monitoring.cfg_job_run"]
    assert jobs[-1][4:7] == ("FAILED", 3, 1)


def test_replay_derived_reset_is_calculated_after_parameter_injection():
    scope = execute_parameters("02a_archive_silver", {
        "JOB_RUN_ID": "synthetic-parent", "RESET_MONTH_MONITORING": True,
        "CONFIRM_PROCESS_ONLY_RESET": "RESET ALL",
    })
    assert "RESET_ALL_ARCHIVE_PROCESSING" not in scope
    guard = next(cell for cell in code_cells("02a_archive_silver")
                 if "Derived controls must be evaluated" in "".join(cell["source"]))
    exec("".join(guard["source"]), scope)
    assert scope["RESET_ALL_ARCHIVE_PROCESSING"] is True
    assert scope["IS_ORCHESTRATED_RUN"] is True


@pytest.mark.parametrize("name", ["00_archive_load", "01a_cfg_schema_capture_archive"])
def test_archive_children_do_not_repeat_setup_with_injected_parent(monkeypatch, name):
    calls = []
    monkeypatch.setitem(sys.modules, "notebookutils", SimpleNamespace(
        mssparkutils=SimpleNamespace(notebook=SimpleNamespace(run=lambda *args: calls.append(args))),
    ))
    scope = execute_parameters(name, {"JOB_RUN_ID": "synthetic-parent"})
    assert "IS_ORCHESTRATED_RUN" not in scope
    bootstrap = next(cell for cell in code_cells(name)
                     if "if not IS_ORCHESTRATED_RUN:" in "".join(cell["source"]))
    exec("".join(bootstrap["source"]), scope)
    assert scope["IS_ORCHESTRATED_RUN"] is True
    assert calls == []


def test_pipeline_controls_are_discoverable_in_fabric_parameter_cell():
    scope = execute_parameters("90_run_archive_pipeline")
    assert {"ARCHIVE_RUN_MODE", "JOB_RUN_ID", "PROCESS_ONLY", "RESET_MONTH_MONITORING",
            "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY", "CONFIRM_PROCESS_ONLY_RESET"} <= scope.keys()
    assert execute_parameters("01a_cfg_schema_capture_archive")["COMPARED_SCHEMA"] == "archived"
    reports = "\n".join("".join(cell["source"]) for cell in code_cells("06_reports"))
    tree = ast.parse(reports)
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "sql":
            assert isinstance(node.args[0], ast.Constant)
            sql = node.args[0].value
            assert "CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring." in sql
            assert "FROM gold." not in sql
