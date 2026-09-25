"""Portable regression coverage for the v16 ZIP reconciliation.

Never execute Fabric notebooks locally. SQL tests use synthetic rows and a
small SQLite dialect translation; they do not certify Fabric runtime execution.
"""

import ast
from pathlib import Path
import re
import sqlite3

from notebook_loader import load_notebook


PROJECT = Path(__file__).resolve().parents[1]


def source(name):
    notebook = load_notebook(PROJECT / f"{name}.py")
    return "\n\n".join(
        "".join(cell["source"]) for cell in notebook["cells"]
        if cell["cell_type"] == "code"
    )


def literal_settings(name):
    settings = {}
    for cell in load_notebook(PROJECT / f"{name}.py")["cells"]:
        code = "".join(cell["source"])
        if cell["cell_type"] != "code" or code.lstrip().startswith("%"):
            continue
        for node in ast.parse(code).body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        settings[target.id] = node.value.value
    return settings


def test_archive_sync_keeps_reset_explicitly_opt_in():
    settings = literal_settings("90_run_archive_pipeline")
    assert settings["PROCESS_ONLY"] == ""
    assert settings["RESET_MONTH_MONITORING"] is False
    assert settings["CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY"] is False
    assert settings["CONFIRM_PROCESS_ONLY_RESET"] == ""
    assert settings["NOTEBOOK_TIMEOUT_SECONDS"] == 9200


def test_live_runner_imports_v16_timeout_and_dq_mode():
    settings = literal_settings("90_run_live_pipeline")
    assert settings["NOTEBOOK_TIMEOUT_SECONDS"] == 7800
    assert settings["RUN_ESSENTIAL_DQ"] is True
    assert settings["FORCE_RERUN"] is False
    assert settings["STOP_ON_ERROR"] is True
    assert 'child_parameters["RUN_ESSENTIAL_DQ"] = str(RUN_ESSENTIAL_DQ).lower()' in source(
        "90_run_live_pipeline"
    )


def test_monitoring_step_summary_uses_object_created_by_reporting_notebook():
    setup = source("00_setup_cfg")
    reports = source("06_reports")
    assert "CREATE OR REPLACE MATERIALIZED LAKE VIEW" not in setup
    assert "CREATE OR REPLACE MATERIALIZED LAKE VIEW monitoring.rpt_job_step_timing AS" in reports
    assert "FROM monitoring.rpt_job_step_timing s" in reports
    assert "FROM monitoring.vw_job_step_timing" not in reports


def test_archive_schema_capture_no_longer_reads_ad_hoc_production_csvs():
    code = source("01a_cfg_schema_capture_archive")
    assert "cfg_archived_schema_live" in code
    assert "FULL OUTER JOIN" in code
    assert "audit/jul26/2026-07-31.csv" not in code
    assert "latest/provider_submission_docs.csv" not in code
    assert "display(df)" not in code


def test_ipa_rollup_qualifies_referral_grouping():
    code = source("03_silver_business_rules")
    assert "GROUP BY c.referral_id" in code


def test_closure_query_resolves_columns_and_sequences_latest_reason():
    code = source("05_gold_dimensions")
    sql = code.split('closure_reasons = spark.sql(f"""', 1)[1].split('""")', 1)[0]
    assert "reject_reason_id" not in sql
    assert "reject_type" not in sql
    # Translate casts/functions only; retain the production CTEs and projections.
    sql = sql.replace("{GOLD_JOB_RUN_ID}", "synthetic-job")
    sql = re.sub(r"CAST\((\w+) AS TIMESTAMP\)", r"datetime(\1)", sql)
    sql = sql.replace(" AS STRING)", " AS TEXT)")
    sql = sql.replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP")
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        connection.create_function("CONCAT", -1, lambda *args: "".join(map(str, args)))
        connection.execute("ATTACH DATABASE ':memory:' AS silver")
        for kind in ("cancel", "decline"):
            connection.execute(f"""CREATE TABLE silver.referral_provider_{kind}_reason (
                {kind}_reason_id TEXT, referral_provider_id TEXT, {kind}_reason TEXT,
                {kind}_reason_other_text TEXT, created_by TEXT, created_date TEXT,
                export_date TEXT)""")
        connection.executemany(
            "INSERT INTO silver.referral_provider_cancel_reason VALUES (?,?,?,?,?,?,?)",
            [
                ("1", "rp1", "old reason", None, "u", "2026-07-01", "2026-07-01"),
                ("1", "rp1", "location unsuitable", None, "u", "2026-07-01", "2026-07-31"),
                ("2", "rp2", "test", None, "u", "2026-07-01", "2026-07-31"),
            ],
        )
        connection.execute(
            "INSERT INTO silver.referral_provider_decline_reason VALUES (?,?,?,?,?,?,?)",
            ("1", "rp1", "placed elsewhere", None, "u", "2026-07-10", "2026-07-31"),
        )
        rows = {row["closure_reason_id"]: dict(row) for row in connection.execute(sql)}
    assert len(rows) == 3  # Repeated snapshots deduplicated; source IDs cannot collide.
    assert rows["cancel:1"]["closure_type"] == "cancel"
    assert rows["cancel:1"]["closure_reason_grouped"] == "Location / Matching issue"
    assert rows["cancel:1"]["sequence_order"] == 2
    assert rows["decline:1"]["closure_type"] == "decline"
    assert rows["decline:1"]["sequence_order"] == 1
    assert rows["decline:1"]["closed_referral_reason_bucket"] == "Placement found elsewhere"
    assert rows["cancel:2"]["closure_reason_clean"] is None
    assert rows["cancel:2"]["closure_reason_grouped"] == "No reason recorded"
    assert all(row["job_run_id"] == "synthetic-job" for row in rows.values())
