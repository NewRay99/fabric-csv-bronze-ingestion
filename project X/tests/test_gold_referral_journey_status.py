"""Execute the notebook's actual referral SQL with small, synthetic fixtures.

SQLite supplies the relational engine; only Spark date/timestamp syntax is
adapted. This does not execute Fabric, Delta writes or Power BI visuals.
"""

import ast
from datetime import date
from pathlib import Path
import re
import sqlite3

import pytest


NOTEBOOK = (Path(__file__).resolve().parents[1] / "04_gold_model.py").read_text(
    encoding="utf-8-sig"
)
TREE = ast.parse(NOTEBOOK)
REQUIREMENTS = next(
    ast.literal_eval(node.value)
    for node in TREE.body
    if isinstance(node, ast.Assign)
    and any(isinstance(t, ast.Name) and t.id == "GOLD_SOURCE_REQUIREMENTS" for t in node.targets)
)
FACT_SQL = NOTEBOOK.split("CREATE OR REPLACE TABLE gold.fact_referral AS", 1)[1].split(
    '""")', 1
)[0]
AS_OF = "2026-09-30"
CREATED = "2026-09-01 09:00:00"
LABELS = {
    1: "Referral created", 2: "Provider search", 3: "Offers received",
    4: "Offer accepted", 5: "IPA created", 6: "IPA signed",
    7: "Closed / cancelled / withdrawn", 8: "Needs review",
}


def portable_sql():
    sql = FACT_SQL.replace("{AS_OF_SQL}", f"'{AS_OF}'").replace("{GOLD_JOB_RUN_ID}", "test-run")
    sql = re.sub(r"CAST\(([^()]+) AS TIMESTAMP\)", r"datetime(\1)", sql)
    sql = sql.replace("AS STRING", "AS TEXT").replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP")
    return sql


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
    values = {
        "referral_id": referral_id, "referral_status": status,
        "referral_created_date": CREATED, "referral_modified_date": CREATED,
        "export_date": CREATED, "required_start_date": "2026-09-10",
    }
    values.update(extra)
    insert(db, "referral", **values)
    insert(db, "referral_enrichment", referral_id=referral_id, is_open=1, is_awaiting_offer=1)


def assignment(db, referral_id="ref-1", assignment_id="assignment-1", provider_id="provider-1",
               created=CREATED):
    insert(db, "referral_provider", referral_id=referral_id, referral_provider_id=assignment_id,
           provider_id=provider_id, created_date=created, modified_date=created, export_date=created)


def offer(db, status, assignment_id="assignment-1", offer_id="offer-1", created=CREATED):
    insert(db, "offer", offer_id=offer_id, referral_provider_id=assignment_id,
           offer_status=status, offer_date=created, export_date=created)


def ipa(db, provider=0, authority=0, closed=0, ipa_id="ipa-1", created=CREATED):
    insert(db, "ipa", referral_id="ref-1", ipa_id=ipa_id, signed_by_provider=provider,
           signed_by_local_authority=authority, closed=closed, created_datetime=created)


def assert_stage(db, stage, raw="OPEN"):
    rows = db.execute(portable_sql()).fetchall()
    assert len(rows) == 1
    row = rows[0]
    assert row["current_status"] == raw
    assert row["journey_stage_order"] == stage
    assert row["journey_stage"] == LABELS[stage]
    assert {"referral_status", "current_status_order", "current_status_rule_version"}.isdisjoint(row.keys())
    return row


@pytest.mark.parametrize("stage", range(1, 9))
def test_all_journey_stages(db, stage):
    raw = "CANCELLED" if stage == 7 else "OPEN"
    referral(db, raw)
    if stage in (2, 3, 4, 5, 6, 8):
        assignment(db)
    if stage == 3:
        offer(db, "OFFER_MADE")
    if stage == 4:
        offer(db, "OFFER_SUCCESSFUL")
    if stage in (5, 6):
        ipa(db, provider=1, authority=int(stage == 6))
    if stage == 8:
        offer(db, "UNRECOGNISED")
    assert_stage(db, stage, raw)


@pytest.mark.parametrize("raw", ["CLOSED", " cancelled ", "canceled", "WITHDRAWN", "completed"])
def test_terminal_status_overrides_signed_ipa_and_unknown_offer(db, raw):
    referral(db, raw)
    assignment(db)
    offer(db, "UNKNOWN")
    ipa(db, 1, 1)
    assert_stage(db, 7, raw)


@pytest.mark.parametrize("raw", ["accepted", "APPROVED", " selected ", "OFFER_SUCCESSFUL"])
def test_accepted_offer_aliases_override_pending_and_unknown(db, raw):
    referral(db)
    assignment(db)
    for ordinal, status in enumerate(["UNKNOWN", "PENDING", raw]):
        offer(db, status, offer_id=f"offer-{ordinal}")
    assert_stage(db, 4)


@pytest.mark.parametrize("raw", [
    "pending", "submitted", "offered", "offer_made", "offer_pending", "under_review",
    "under review", "awaiting", "awaiting_decision", "awaiting decision",
])
def test_pending_offer_aliases_override_unknown(db, raw):
    referral(db)
    assignment(db)
    offer(db, raw.upper(), offer_id="pending")
    offer(db, None, offer_id="unknown")
    assert_stage(db, 3)


@pytest.mark.parametrize("raw", [
    "draft", "declined", "rejected", "withdrawn", "closed", "cancelled", "canceled",
    "offer_unsuccessful", "unsuccessful",
])
def test_draft_and_terminal_offers_do_not_imply_offers_received(db, raw):
    referral(db)
    assignment(db)
    offer(db, raw)
    assert_stage(db, 2)


@pytest.mark.parametrize("raw", [None, "", "  "])
def test_missing_source_status_requires_review_without_stronger_evidence(db, raw):
    referral(db, raw)
    assignment(db)
    assert_stage(db, 8, raw)
    offer(db, "accepted")
    assert_stage(db, 4, raw)


@pytest.mark.parametrize("provider,authority,closed,stage", [
    (1, 1, 0, 6), (1, 1, None, 6), (1, 0, 0, 5), (0, 1, 0, 5),
    (None, 1, 0, 5), (1, None, 0, 5), (None, None, None, 5), (1, 1, 1, 4),
])
def test_active_ipa_and_signature_precedence(db, provider, authority, closed, stage):
    referral(db)
    assignment(db)
    offer(db, "accepted")
    ipa(db, provider, authority, closed)
    assert_stage(db, stage)


def test_signatures_on_different_ipas_are_not_combined(db):
    referral(db)
    ipa(db, 1, 0, ipa_id="one")
    ipa(db, 0, 1, ipa_id="two")
    ipa(db, 1, 1, closed=1, ipa_id="closed")
    assert_stage(db, 5)


def test_multiple_assignments_offers_and_ipas_keep_one_referral_row(db):
    referral(db)
    for ordinal in range(3):
        assignment_id = f"assignment-{ordinal}"
        assignment(db, assignment_id=assignment_id, provider_id=f"provider-{ordinal}")
        offer(db, "OFFER_MADE", assignment_id, f"offer-{ordinal}")
        ipa(db, ipa_id=f"ipa-{ordinal}")
    row = assert_stage(db, 5)
    assert row["provider_assignment_count"] == 3


def test_assignment_with_missing_provider_key_still_evidences_search(db):
    referral(db)
    assignment(db, provider_id=None)
    row = assert_stage(db, 2)
    assert row["provider_assignment_count"] == 0


def test_as_of_excludes_future_evidence_and_referrals(db):
    referral(db)
    assignment(db)
    offer(db, "accepted", created="2026-10-01 00:00:00")
    ipa(db, 1, 1, created="2026-10-01 00:00:00")
    assignment(db, assignment_id="future", created="2026-10-01 00:00:00")
    offer(db, "accepted", assignment_id="future", offer_id="future-assignment", created=None)
    referral(db, referral_id="future-referral", referral_created_date="2026-10-01 00:00:00")
    assert_stage(db, 2)


def test_unknown_offer_with_missing_date_requires_review(db):
    referral(db)
    assignment(db)
    offer(db, None, created=None)
    assert_stage(db, 8)


def test_current_source_status_is_preserved_and_not_used_as_journey_label(db):
    referral(db, "UNDER_OFFER")
    insert(db, "referral", referral_id="ref-1", referral_status="OPEN",
           referral_created_date=CREATED, referral_modified_date="2026-08-01 00:00:00",
           export_date="2026-08-01 00:00:00")
    row = assert_stage(db, 1, "UNDER_OFFER")
    assert row["required_placement_date_outcome"] == "Open overdue"


def test_snapshot_preserves_source_status_and_adds_separate_journey_columns():
    select = next(
        node.value for node in ast.walk(TREE)
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "snapshot" for t in node.targets)
    )
    columns = {arg.value for arg in select.args if isinstance(arg, ast.Constant)}
    assert {"current_status", "journey_stage", "journey_stage_order"} <= columns
    assert {"referral_status", "journey_status", "journey_status_order"}.isdisjoint(columns)
    snapshot_source = NOTEBOOK.split('snapshot = spark.table("gold.fact_referral")', 1)[1]
    assert '.option("replaceWhere", month_predicate)' in snapshot_source
    assert '.option("mergeSchema", "true")' in snapshot_source
    historic_update = snapshot_source.split("UPDATE {SNAPSHOT_TABLE}", 1)[1].split('""")', 1)[0]
    assert "journey_stage" not in historic_update
