"""GLD-026: run production referral SQL with synthetic creator values.

SQLite adapts Spark date/timestamp syntax; Fabric/Delta acceptance is separate.
"""

import ast
from types import SimpleNamespace

import pytest

import test_gold_referral_source_status as source_status
from test_gold_referral_source_status import (
    CREATED, NOTEBOOK, REQUIREMENTS, TREE, insert, portable_sql, referral,
)


db = source_status.db


@pytest.mark.parametrize("creator", [
    "synthetic-placement-officer-001", "00001234", "Officer Élodie", "x" * 100,
    None, "", "  officer-001  ",
])
def test_creator_survives_complete_gold_projection(db, creator):
    db.execute("ALTER TABLE silver.referral ADD COLUMN referral_updated_by")
    referral(db, referral_created_by=creator, referral_updated_by="different-updater")
    rows = db.execute(portable_sql()).fetchall()
    assert len(rows) == 1
    assert rows[0]["referral_created_by"] == creator


@pytest.mark.parametrize("latest_creator", ["latest-synthetic-creator", None])
@pytest.mark.parametrize("same_modified", [False, True])
def test_creator_follows_current_referral_version(db, latest_creator, same_modified):
    referral(db, referral_created_by="older-synthetic-creator")
    insert(db, "referral", referral_id="ref-1", referral_status="OPEN",
           referral_created_date=CREATED,
           referral_modified_date=CREATED if same_modified else "2026-09-20 09:00:00",
           export_date="2026-09-20 10:00:00", referral_created_by=latest_creator)
    rows = db.execute(portable_sql()).fetchall()
    assert len(rows) == 1
    assert rows[0]["referral_created_by"] == latest_creator


def test_empty_sources_return_no_referrals(db):
    assert db.execute(portable_sql()).fetchall() == []


@pytest.mark.parametrize("missing_creator", [False, True])
def test_production_preflight_requires_creator_column(missing_creator):
    def table(name):
        columns = REQUIREMENTS[name] - (
            {"referral_created_by"} if missing_creator and name == "silver.referral" else set()
        )
        return SimpleNamespace(schema=SimpleNamespace(
            fields=[SimpleNamespace(name=column) for column in columns]))

    spark = SimpleNamespace(catalog=SimpleNamespace(tableExists=lambda name: True), table=table)
    preflight = NOTEBOOK.split("gold_input_issues = []", 1)[1].split(
        'print("Gold source validation passed")', 1)[0]
    context = {"spark": spark, "GOLD_SOURCE_REQUIREMENTS": REQUIREMENTS}
    code = "gold_input_issues = []" + preflight
    if missing_creator:
        with pytest.raises(RuntimeError, match="silver.referral: missing .*referral_created_by"):
            exec(code, context)
    else:
        exec(code, context)
        assert context["gold_input_issues"] == []


def test_creator_is_excluded_from_snapshot():
    select = next(node.value for node in ast.walk(TREE) if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "snapshot" for t in node.targets))
    assert "referral_created_by" not in ast.unparse(select)
