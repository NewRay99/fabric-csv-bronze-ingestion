"""Source-status checks against the actual Gold notebook SQL and synthetic data.

SQLite adapts Spark date/timestamp syntax. No Fabric/Delta or Power BI execution.
Gold journey stages are separate from the untouched source current_status.
"""

import ast
from datetime import date
from pathlib import Path
import re
import sqlite3

import pytest


PROJECT = Path(__file__).resolve().parents[1]
NOTEBOOK = (PROJECT / "04_gold_model.py").read_text(encoding="utf-8-sig")
TREE = ast.parse(NOTEBOOK)
REQUIREMENTS = next(
    ast.literal_eval(node.value) for node in TREE.body
    if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "GOLD_SOURCE_REQUIREMENTS" for t in node.targets)
)
FACT_SQL = NOTEBOOK.split("CREATE OR REPLACE TABLE gold.fact_referral AS", 1)[1].split('""")', 1)[0]
AS_OF = "2026-09-30"
CREATED = "2026-09-01 09:00:00"
REMOVED_FIELDS = {"referral_status", "current_status_order", "current_status_rule_version",
                  "journey_status", "journey_status_order", "journey_status_rule_version"}


def portable_sql():
    sql = FACT_SQL.replace("{AS_OF_SQL}", f"'{AS_OF}'").replace("{GOLD_JOB_RUN_ID}", "test-run")
    sql = re.sub(r"CAST\(([^()]+) AS TIMESTAMP\)", r"datetime(\1)", sql)
    return sql.replace("AS STRING", "AS TEXT").replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP")


def to_date(value):
    return None if value is None else str(value)[:10]


def date_diff(end, start):
    if end is None or start is None:
        return None
    return (date.fromisoformat(to_date(end)) - date.fromisoformat(to_date(start))).days


@pytest.fixture
def db():
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        connection.create_function("TO_DATE", 1, to_date)
        connection.create_function("DATEDIFF", 2, date_diff)
        connection.create_function("LEAST", 2, min)
        connection.execute("ATTACH DATABASE ':memory:' AS silver")
        for table, columns in REQUIREMENTS.items():
            fields = ", ".join(f'"{column}"' for column in sorted(columns))
            connection.execute(f"CREATE TABLE {table} ({fields})")
        yield connection


def insert(db, table, **values):
    columns = ", ".join(f'"{column}"' for column in values)
    placeholders = ", ".join("?" for _ in values)
    db.execute(f"INSERT INTO silver.{table} ({columns}) VALUES ({placeholders})", tuple(values.values()))


def referral(db, status="OPEN", referral_id="ref-1", **extra):
    values = {"referral_id": referral_id, "referral_status": status,
              "referral_created_date": CREATED, "referral_modified_date": CREATED,
              "export_date": CREATED, "required_start_date": "2026-09-10", **extra}
    insert(db, "referral", **values)
    insert(db, "referral_enrichment", referral_id=referral_id, is_open=1, is_awaiting_offer=1)


def assignment(db, ordinal=1, created=CREATED):
    insert(db, "referral_provider", referral_id="ref-1", referral_provider_id=f"assignment-{ordinal}",
           provider_id=f"provider-{ordinal}", created_date=created, modified_date=created, export_date=created)


def assert_source_status(db, raw):
    rows = db.execute(portable_sql()).fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row["current_status"] == raw
    assert REMOVED_FIELDS.isdisjoint(row.keys())
    return row


@pytest.mark.parametrize("raw", ["OPEN", "UNDER_OFFER", "CLOSED", "CANCELLED", "WITHDRAWN",
                                 "COMPLETED", "open", " Closed ", "future_status", None, "", "  "])
def test_current_status_preserves_source_value_without_relabeling(db, raw):
    referral(db, raw)
    assert_source_status(db, raw)


@pytest.mark.parametrize("offer_status,provider_signed,authority_signed,closed", [
    ("OFFER_MADE", 0, 0, 0), ("OFFER_SUCCESSFUL", 0, 0, 0),
    ("UNKNOWN", 1, 1, 0), (None, None, None, None),
    ("DRAFT", 1, 0, 0), ("OFFER_SUCCESSFUL", 1, 1, 0),
    ("OFFER_SUCCESSFUL", 1, 1, 1), ("OFFER_WITHDRAWN", 0, 1, 0),
])
def test_offer_or_ipa_evidence_cannot_replace_source_status(db, offer_status, provider_signed,
                                                         authority_signed, closed):
    referral(db, "UNDER_OFFER")
    assignment(db)
    insert(db, "offer", offer_id="offer-1", referral_provider_id="assignment-1",
           offer_status=offer_status, offer_date=CREATED)
    insert(db, "ipa", ipa_id="ipa-1", referral_id="ref-1", signed_by_provider=provider_signed,
           signed_by_local_authority=authority_signed, closed=closed, created_datetime=CREATED)
    assert_source_status(db, "UNDER_OFFER")


@pytest.mark.parametrize("raw,outcome", [("OPEN", "Open overdue"), ("UNDER_OFFER", "Open overdue"),
                                       ("CLOSED", "Closed without placement"), ("CANCELLED", "Closed without placement"),
                                       ("WITHDRAWN", "Closed without placement"), ("COMPLETED", "Closed without placement")])
def test_outcome_rules_use_original_source_status(db, raw, outcome):
    referral(db, raw)
    assert assert_source_status(db, raw)["required_placement_date_outcome"] == outcome


def test_latest_referral_record_supplies_current_status(db):
    referral(db, "UNDER_OFFER")
    insert(db, "referral", referral_id="ref-1", referral_status="OPEN",
           referral_created_date=CREATED, referral_modified_date="2026-08-01 00:00:00",
           export_date="2026-08-01 00:00:00")
    assert_source_status(db, "UNDER_OFFER")


def test_multiple_assignments_offers_and_ipas_keep_one_referral_row(db):
    referral(db)
    for ordinal in range(3):
        assignment(db, ordinal)
        insert(db, "offer", offer_id=f"offer-{ordinal}", referral_provider_id=f"assignment-{ordinal}",
               offer_status="OFFER_SUCCESSFUL", offer_date=CREATED)
        insert(db, "ipa", ipa_id=f"ipa-{ordinal}", referral_id="ref-1", signed_by_provider=1,
               signed_by_local_authority=1, closed=0, created_datetime=CREATED)
    assert assert_source_status(db, "OPEN")["provider_assignment_count"] == 3


def test_future_referrals_and_provider_response_evidence_remain_excluded(db):
    referral(db)
    assignment(db)
    assignment(db, 2, created="2026-10-01 00:00:00")
    referral(db, referral_id="future", referral_created_date="2026-10-01 00:00:00")
    assert assert_source_status(db, "OPEN")["provider_assignment_count"] == 1


def test_snapshot_selects_source_status_and_separate_journey_fields():
    select = next(node.value for node in ast.walk(TREE) if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "snapshot" for t in node.targets))
    direct_columns = {arg.value for arg in select.args if isinstance(arg, ast.Constant)}
    assert "current_status" in direct_columns
    assert {"journey_stage", "journey_stage_order"} <= direct_columns
    assert REMOVED_FIELDS.isdisjoint(direct_columns)
    assert not any("journey_status" in ast.unparse(arg) for arg in select.args)
    snapshot_source = NOTEBOOK.split('snapshot = spark.table("gold.fact_referral")', 1)[1]
    assert '.option("replaceWhere", month_predicate)' in snapshot_source
    assert '.option("mergeSchema", "true")' in snapshot_source
    historic_update = snapshot_source.split("UPDATE {SNAPSHOT_TABLE}", 1)[1].split('""")', 1)[0]
    assert "current_status" not in historic_update and "journey_stage" not in historic_update


def test_separate_gold_journey_classifier_and_fixture_matches_production():
    assert "r.referral_status AS current_status" in FACT_SQL
    assert "END AS journey_stage_order" in FACT_SQL
    assert "END AS journey_stage," in FACT_SQL
    assert ("CREATE OR REPLACE TABLE gold.fact_referral AS" + FACT_SQL).strip() == (
        PROJECT / "tests/_gold_fact_sql.sql"
    ).read_text(encoding="utf-8").strip()
