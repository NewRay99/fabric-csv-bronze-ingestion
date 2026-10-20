"""Exercise the real notebook clock expressions without a live Lakehouse."""

import ast
import calendar
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
import warnings

import pytest

from notebook_loader import load_notebook


ROOT = Path(__file__).resolve().parents[1]
CLOCK_NOTEBOOKS = (
    "00_archive_load.py", "00a_rehydrate_archive_cfg.py",
    "01a_cfg_schema_capture_live.py", "01a_cfg_schema_capture_archive.py",
    "02_silver_formatter.py", "02a_archive_silver.py", "03_silver_business_rules.py",
    "05_gold_dimensions.py", "90_run_live_pipeline.py", "90_run_archive_pipeline.py",
    "99_common_library.py",
)


def notebook_tree(name):
    body = []
    for cell in load_notebook(ROOT / name)["cells"]:
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and not source.lstrip().startswith("%"):
            body.extend(ast.parse(source, filename=name).body)
    return ast.Module(body=body, type_ignores=[])


def clock_scope(tree):
    # 02_silver_formatter receives datetime imports from its isolated %run.
    scope = {}
    for source in (notebook_tree("99_common_library.py"), tree):
        for node in source.body:
            if isinstance(node, ast.ImportFrom) and node.module == "datetime":
                exec(compile(ast.Module([node], type_ignores=[]), "imports", "exec"), scope)
    scope["os"] = SimpleNamespace(path=SimpleNamespace(getmtime=lambda _: 1_700_000_000))
    scope["full_path"] = "synthetic-file-metadata"
    return scope


def clock_values(name):
    tree = notebook_tree(name)
    scope = clock_scope(tree)
    calls = [node for node in ast.walk(tree)
             if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
             and isinstance(node.func.value, ast.Name) and node.func.value.id == "datetime"
             and node.func.attr in {"utcnow", "now", "utcfromtimestamp", "fromtimestamp"}]
    assert calls, f"No monitoring clocks exercised in {name}"
    with warnings.catch_warnings():
        warnings.simplefilter("error", DeprecationWarning)
        return [eval(compile(ast.Expression(call), name, "eval"), scope) for call in calls]


@pytest.mark.parametrize("name", CLOCK_NOTEBOOKS)
def test_notebook_clocks_are_warning_free_and_explicit_utc(name):
    for value in clock_values(name):
        assert value.tzinfo is not None
        assert value.utcoffset() == timedelta(0)


def test_pyspark_timestamp_serialization_keeps_the_exact_utc_instant():
    timestamp_type = pytest.importorskip("pyspark.sql.types").TimestampType()
    for name in CLOCK_NOTEBOOKS:
        for value in clock_values(name):
            expected = calendar.timegm(value.utctimetuple()) * 1_000_000 + value.microsecond
            assert timestamp_type.toInternal(value) == expected


def load_function(name, function_name, scope):
    node = next(node for node in notebook_tree(name).body
                if isinstance(node, ast.FunctionDef) and node.name == function_name)
    exec(compile(ast.Module([node], type_ignores=[]), name, "exec"), scope)
    return scope[function_name]


class FrozenClock:
    @staticmethod
    def now(tz):
        assert tz is timezone.utc
        return datetime(2026, 10, 7, 12, 0, 5, tzinfo=timezone.utc)


@pytest.mark.parametrize("name", ("90_run_live_pipeline.py", "90_run_archive_pipeline.py"))
def test_runner_step_records_keep_status_keys_and_aware_timestamps(name):
    rows = []
    scope = {"datetime": FrozenClock, "timezone": timezone, "JOB_RUN_ID": "synthetic-job",
             "merge_monitor_row": lambda *args: rows.append(args)}
    record_step = load_function(name, "record_step", scope)
    started = datetime(2026, 10, 7, 12, tzinfo=timezone.utc)
    for status in ("RUNNING", "SUCCESS", "FAILED"):
        record_step(2, "synthetic-child", status, started, "done", "failure" if status == "FAILED" else None)
    for table, row, schema, condition in rows:
        assert table == "monitoring.cfg_job_step_run"
        assert row[:4] == ("synthetic-job", 2, "synthetic-child", started)
        assert "started_at timestamp,ended_at timestamp" in schema
        assert condition == "target.job_run_id = source.job_run_id AND target.step_sequence = source.step_sequence"
        assert row[-1].tzinfo is timezone.utc
        if row[5] == "RUNNING":
            assert row[4] is None
        else:
            assert (row[4] - row[3]).total_seconds() == 5
            assert row[4].tzinfo is timezone.utc
    assert [row[1][5] for row in rows] == ["RUNNING", "SUCCESS", "FAILED"]


def test_shared_step_elapsed_time_uses_compatible_utc_objects(capsys):
    scope = {"datetime": FrozenClock, "timezone": timezone, "_LOG_STEP_STATE": {}}
    log_step = load_function("99_common_library.py", "log_step", scope)
    log_step("first")
    log_step("second")
    assert "+0.0s step" in capsys.readouterr().out
    assert all(value.tzinfo is timezone.utc for value in scope["_LOG_STEP_STATE"].values())


def test_rule_elapsed_time_uses_compatible_utc_objects(capsys):
    scope = {"datetime": FrozenClock, "timezone": timezone}
    log_rule = load_function("03_silver_business_rules.py", "log_rule", scope)
    log_rule("synthetic-rule", "PASS", "checked", datetime(2026, 10, 7, 12, tzinfo=timezone.utc))
    assert "(+5.0s)" in capsys.readouterr().out
