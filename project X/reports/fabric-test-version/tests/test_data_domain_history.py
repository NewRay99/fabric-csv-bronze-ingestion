"""Run the production snapshot builder through successive domain discoveries."""

import ast
from datetime import datetime, timedelta, timezone
from pathlib import Path
import re
import sqlite3
from types import SimpleNamespace

from notebook_loader import load_notebook
import pytest


ROOT = Path(__file__).resolve().parents[1]


def snapshot_builder():
    nodes = [node for cell in load_notebook(ROOT / "99_common_library.py")["cells"]
             if cell["cell_type"] == "code"
             for code in ["".join(cell["source"]) ] if not code.lstrip().startswith("%")
             for node in ast.parse(code).body
             if isinstance(node, ast.FunctionDef) and node.name == "build_data_domain_snapshot"]
    assert nodes, "The profiler needs an append-only version builder"
    scope = {}
    exec(compile(ast.Module(nodes, type_ignores=[]), "99_common_library.py", "exec"), scope)
    return scope["build_data_domain_snapshot"]


def build(values, previous=None, status="PROFILED", run_id="second"):
    return snapshot_builder()(
        "bronze", "provider", "status", "varchar(30)", values,
        datetime(2026, 10, 15, tzinfo=timezone.utc), run_id, "job-2", previous, status,
    )


def test_first_discovery_is_a_baseline_not_a_fabricated_change():
    rows = build(["OPEN", "CLOSED", "OPEN"], run_id="first")
    assert [(row["data_domain"], row["change_type"]) for row in rows] == [
        ("CLOSED", "BASELINE"), ("OPEN", "BASELINE"),
    ]
    assert all(row["is_present"] and row["distinct_value_count"] == 2 for row in rows)


def test_later_discovery_retains_old_values_and_marks_added_removed_and_unchanged():
    previous = {"run_id": "first", "profiled_at": datetime(2026, 10, 8, tzinfo=timezone.utc),
                "values": {"OPEN", "CLOSED"}}
    rows = build(["OPEN", "PENDING"], previous)
    assert {(row["data_domain"], row["change_type"], row["is_present"]) for row in rows} == {
        ("CLOSED", "REMOVED", False), ("OPEN", "UNCHANGED", True),
        ("PENDING", "ADDED", True),
    }
    assert previous["values"] == {"OPEN", "CLOSED"}
    assert all(row["previous_run_id"] == "first" and row["job_run_id"] == "job-2"
               and row["distinct_value_count"] == 2 for row in rows)


def test_a_successfully_observed_empty_domain_removes_the_previous_values():
    rows = build([], {"run_id": "first", "profiled_at": None, "values": {"OPEN"}})
    assert len(rows) == 1
    assert rows[0]["change_type"] == "REMOVED"
    assert rows[0]["profile_status"] == "EMPTY"
    assert rows[0]["distinct_value_count"] == 0
    assert rows[0]["is_present"] is False


@pytest.mark.parametrize("status", ["HIGH_CARDINALITY", "SOURCE_MISSING", "EXCLUDED"])
def test_a_skipped_profile_never_claims_that_old_values_were_removed(status):
    rows = build(None, {"run_id": "first", "profiled_at": None, "values": {"OPEN"}}, status)
    assert len(rows) == 1
    assert rows[0]["data_domain"] is None
    assert rows[0]["change_type"] is None
    assert rows[0]["profile_status"] == status
    assert rows[0]["distinct_value_count"] is None


def test_empty_baselines_are_retained_and_new_values_after_empty_are_added():
    baseline = build([])
    assert baseline[0]["profile_status"] == "EMPTY"
    assert baseline[0]["data_domain"] is None
    rows = build(["OPEN"], {"run_id": "empty", "profiled_at": None, "values": set()})
    assert rows[0]["change_type"] == "ADDED"


def test_snapshot_metadata_keeps_a_version_and_comparison_time():
    previous_time = datetime(2026, 10, 15, tzinfo=timezone.utc) - timedelta(days=7)
    rows = build(["OPEN"], {"run_id": "week-1", "profiled_at": previous_time,
                            "values": {"OPEN"}})
    assert rows[0]["previous_profiled_at"] == previous_time
    assert rows[0]["run_id"] == "second"


def load_functions(filename, names, scope):
    nodes = [node for cell in load_notebook(ROOT / filename)["cells"]
             if cell["cell_type"] == "code"
             for code in ["".join(cell["source"]) ] if not code.lstrip().startswith("%")
             for node in ast.parse(code).body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    assert len(nodes) == len(names)
    exec(compile(ast.Module(nodes, type_ignores=[]), filename, "exec"), scope)


def test_latest_comparable_snapshot_skips_unobserved_profiles_and_keeps_empty_baselines():
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("ATTACH DATABASE ':memory:' AS monitoring")
        connection.execute('''CREATE TABLE monitoring.cfg_data_domain (
            source_schema, source_table, column_name, run_id, profiled_at,
            data_domain, is_present, profile_status)''')
        connection.executemany("INSERT INTO monitoring.cfg_data_domain VALUES (?,?,?,?,?,?,?,?)", [
            ("bronze", "provider", "status", "first", "2026-10-01", "OPEN", None, None),
            ("bronze", "provider", "status", "skip", "2026-10-08", None, 0, "HIGH_CARDINALITY"),
            ("bronze", "provider", "empty", "first", "2026-10-01", "OLD", 1, "PROFILED"),
            ("bronze", "provider", "empty", "empty", "2026-10-08", "OLD", 0, "EMPTY"),
        ])

        def execute(query):
            result = connection.execute(query.replace("<=>", "IS")).fetchall()
            values = [{**dict(row), "is_present": None if row["is_present"] is None
                       else bool(row["is_present"])} for row in result]
            return SimpleNamespace(collect=lambda: [SimpleNamespace(**row) for row in values])

        scope = {"spark": SimpleNamespace(sql=execute), "qident": lambda name: f'`{name}`'}
        load_functions("99_common_library.py", {"latest_data_domain_profiles"}, scope)
        profiles = scope["latest_data_domain_profiles"]("monitoring.cfg_data_domain")
    assert profiles[("bronze", "provider", "status")]["run_id"] == "first"
    assert profiles[("bronze", "provider", "status")]["values"] == {"OPEN"}
    assert profiles[("bronze", "provider", "empty")]["values"] == set()


@pytest.mark.parametrize("fail_scan", [False, True])
def test_profiler_appends_one_complete_batch_and_never_publishes_partial_scans(fail_scan):
    stored = [{"run_id": "retained-week-1"}]
    appends = []
    contract = [SimpleNamespace(table_name="provider", column_name=name, data_type="varchar(20)")
                for name in ("kind", "status")]
    frame = SimpleNamespace(schema=SimpleNamespace(fields=[SimpleNamespace(name=row.column_name)
                                                          for row in contract]))
    contract_frame = SimpleNamespace(select=lambda *args: SimpleNamespace(collect=lambda: contract))
    spark = SimpleNamespace(
        catalog=SimpleNamespace(tableExists=lambda _: True),
        table=lambda name: contract_frame if name == "contract" else frame,
        sql=lambda query: SimpleNamespace(collect=lambda: [SimpleNamespace(
            isTemporary=False, tableName="provider")]),
    )

    def collect_values(frame, column, maximum, include_empty):
        if fail_scan and column == "status":
            raise RuntimeError("scan failed")
        return ["NEW"]

    def append(table, rows):
        appends.append(rows)
        stored.extend(rows)

    scope = {"spark": spark, "CONTRACT_TABLE": "contract", "DOMAIN_TABLE": "domains",
             "BRONZE_SCHEMA": "bronze", "MAX_DISTINCT_VALUES": 40, "INCLUDE_EMPTY_STRING": False,
             "RUN_ID": "week-2", "JOB_RUN_ID": "job-2", "PROFILED_AT": datetime.now(timezone.utc),
             "latest_data_domain_profiles": lambda _: {}, "re": re,
             "qident": lambda name: f'`{name}`',
             "collect_low_cardinality_domain_values": collect_values,
             "append_data_domain_snapshots": append,
             "build_data_domain_snapshot": snapshot_builder()}
    load_functions("99_common_library.py", {"normalise", "is_contract_string",
                                           "data_domain_exclusion_reason"}, scope)
    load_functions("99_data_domain.py", {"profile_data_domains"}, scope)
    if fail_scan:
        with pytest.raises(RuntimeError, match="scan failed"):
            scope["profile_data_domains"]()
        assert appends == []
        assert stored == [{"run_id": "retained-week-1"}]
    else:
        result = scope["profile_data_domains"]()
        assert len(appends) == 1 and len(appends[0]) == 2
        assert stored[0] == {"run_id": "retained-week-1"}
        assert result["job_run_id"] == "job-2"


@pytest.mark.parametrize("orchestrated", [False, True])
def test_standalone_profiles_have_job_history_and_parent_jobs_are_not_overwritten(orchestrated):
    rows = []
    scope = {"IS_ORCHESTRATED_RUN": orchestrated, "JOB_RUN_ID": "job", "datetime": datetime,
             "timezone": timezone, "PROFILED_AT": datetime.now(timezone.utc),
             "merge_monitor_row": lambda *args: rows.append(args)}
    load_functions("99_data_domain.py", {"record_domain_job"}, scope)
    scope["record_domain_job"]("RUNNING")
    scope["record_domain_job"]("SUCCESS")
    if orchestrated:
        assert rows == []
    else:
        jobs = [row for table, row, *_ in rows if table == "monitoring.cfg_job_run"]
        assert jobs[0][3:5] == (None, "RUNNING")
        assert jobs[1][3] is not None and jobs[1][4] == "SUCCESS"
