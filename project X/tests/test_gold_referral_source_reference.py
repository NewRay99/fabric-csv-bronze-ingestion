"""Execute production referral SQL with synthetic source-person histories.

SQLite date/timestamp adaptation is portable relational verification, not a
Fabric/Delta deployment test. References are person attributes, never join keys.
"""

import ast
from pathlib import Path

import pytest

import test_gold_referral_source_status as source_status
from test_gold_referral_source_status import (
    CREATED, NOTEBOOK, TREE, insert, portable_sql, referral,
)


# Register the existing fixture without an unused import named like test parameters.
db = source_status.db


def person(connection, referral_id, reference, person_id="person-1", **extra):
    insert(connection, "referral_person", referral_id=referral_id, person_id=person_id,
           source_reference_id=reference, child_index=1, export_date=CREATED,
           _silver_load_ts=CREATED, **extra)


def rows(connection):
    return {row["referral_id"]: row for row in connection.execute(portable_sql()).fetchall()}


def test_multiple_referrals_flagged_without_removing_closed_or_open_rows(db):
    referral(db, "CLOSED", "older", referral_created_date="2026-08-01 09:00:00")
    referral(db, "UNDER_OFFER", "newer")
    person(db, "older", "001234")
    person(db, "newer", "001234")
    result = rows(db)
    assert set(result) == {"older", "newer"}
    for row in result.values():
        assert row["source_reference_id"] == "001234"
        assert row["has_multiple_referrals"] == 1
        assert row["source_reference_referral_count"] == 2
    assert result["older"]["order_dupe"] == 1
    assert result["newer"]["order_dupe"] == 2
    assert result["older"]["current_status"] == "CLOSED"


def test_same_creation_time_uses_stable_referral_id_tie_break(db):
    for identifier in ("ref-c", "ref-a", "ref-b"):
        referral(db, referral_id=identifier)
        person(db, identifier, "shared")
    assert [(key, rows(db)[key]["order_dupe"]) for key in sorted(rows(db))] == [
        ("ref-a", 1), ("ref-b", 2), ("ref-c", 3),
    ]


@pytest.mark.parametrize("references", [("ABC", " abc "), ("00123", " 00123 ")])
def test_reference_matching_ignores_casing_and_surrounding_spaces(db, references):
    for identifier, reference in zip(("a", "b"), references):
        referral(db, referral_id=identifier)
        person(db, identifier, reference)
    result = rows(db)
    assert all(row["source_reference_referral_count"] == 2 for row in result.values())
    assert result["a"]["source_reference_id"] == references[0].strip()
    assert result["b"]["source_reference_id"] == references[1].strip()


def test_leading_zeros_are_not_removed_or_matched_to_another_reference(db):
    for identifier, reference in (("a", "00123"), ("b", "123")):
        referral(db, referral_id=identifier)
        person(db, identifier, reference)
    assert all(row["source_reference_referral_count"] == 1 for row in rows(db).values())


@pytest.mark.parametrize("blank", [None, "", "   "])
def test_blank_references_not_flagged_but_remain_separately_navigable(db, blank):
    for identifier in ("a", "b"):
        referral(db, referral_id=identifier)
        person(db, identifier, blank)
    result = rows(db)
    assert len(result) == 2
    assert all(row["source_reference_id"] is None for row in result.values())
    assert all(row["has_multiple_referrals"] == 0 for row in result.values())
    assert all(row["source_reference_referral_count"] == 0 for row in result.values())
    assert {row["order_dupe"] for row in result.values()} == {1, 2}


def test_person_history_versions_do_not_multiply_or_flag_a_single_referral(db):
    referral(db)
    person(db, "ref-1", "old-reference")
    for exported, reference in (("2026-09-20", "new-reference"),
                                ("2026-10-01", "future-reference")):
        insert(db, "referral_person", referral_id="ref-1", person_id="person-1",
               source_reference_id=reference, child_index=1, export_date=exported,
               _silver_load_ts=exported)
    row = rows(db)["ref-1"]
    assert row["source_reference_id"] == "new-reference"
    assert row["has_multiple_referrals"] == 0
    assert row["source_reference_referral_count"] == 1
    assert row["order_dupe"] == 1


def test_future_referrals_cannot_inflate_as_of_counts_or_sequence(db):
    referral(db)
    referral(db, referral_id="future", referral_created_date="2026-10-01 00:00:00")
    person(db, "ref-1", "shared")
    person(db, "future", "shared")
    result = rows(db)
    assert set(result) == {"ref-1"}
    assert result["ref-1"]["source_reference_referral_count"] == 1
    assert result["ref-1"]["order_dupe"] == 1


def test_multi_person_referral_preserves_existing_min_person_selection(db):
    referral(db)
    person(db, "ref-1", "secondary", "person-z")
    person(db, "ref-1", "selected", "person-a")
    row = rows(db)["ref-1"]
    assert row["person_id"] == "person-a"
    assert row["source_reference_id"] == "selected"
    assert row["source_reference_referral_count"] == 1


def test_no_person_does_not_remove_referral_or_create_duplicate_flag(db):
    referral(db)
    row = rows(db)["ref-1"]
    assert row["person_id"] is None and row["source_reference_id"] is None
    assert row["has_multiple_referrals"] == 0 and row["order_dupe"] == 1


def test_snapshot_carries_as_of_annotations_without_backfilling_retained_months():
    select = next(node.value for node in ast.walk(TREE) if isinstance(node, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "snapshot" for t in node.targets))
    fields = {arg.value for arg in select.args if isinstance(arg, ast.Constant)}
    expected = {"source_reference_id", "source_reference_referral_count",
                "has_multiple_referrals", "order_dupe"}
    assert expected <= fields
    update = NOTEBOOK.split("UPDATE {SNAPSHOT_TABLE}", 1)[1].split('""")', 1)[0]
    assert not any(field in update for field in expected)


def test_person_dimension_publishes_a_text_reference_and_keeps_person_key():
    source = (Path(__file__).resolve().parents[1] / "05_gold_dimensions.py").read_text(
        encoding="utf-8-sig")
    person_source = source.split('"silver.referral_person",', 1)[1].split("# GLD-008", 1)[0]
    assert '"source_reference_id"' in person_source
    assert 'F.col("source_reference_id").cast("string")' in person_source
    assert 'F.col("person_id").alias("person_id")' in person_source
    assert 'Window.partitionBy("person_id")' in person_source
