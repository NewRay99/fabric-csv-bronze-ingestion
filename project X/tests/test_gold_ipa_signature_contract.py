"""Exercise the notebook's signature predicates with multiple IPAs per offer."""

from pathlib import Path
import re
import sqlite3

import pytest


NOTEBOOK = (Path(__file__).resolve().parents[1] / '04_gold_model.py').read_text(encoding='utf-8-sig')
IPA_SQL = NOTEBOOK.split('CREATE OR REPLACE TABLE gold.fact_ipa AS', 1)[1]
SIGNATURE_PROJECTION = IPA_SQL.split('i.offer_id AS accepted_offer_id,', 1)[1].split(
    'CAST(i.created_datetime AS TIMESTAMP)', 1
)[0].strip().rstrip(',')


@pytest.mark.parametrize('provider,authority,closed,completed,pending', [
    (1, 1, 0, 1, 0), (1, 0, 0, 0, 1), (0, 1, 0, 0, 1),
    (0, 0, 0, 0, 1), (None, 1, 0, 0, 1), (1, None, 0, 0, 1),
    (1, 1, 1, 1, 0), (1, 0, 1, 0, 0), (0, 0, 1, 0, 0),
])
def test_gold_ipa_signature_and_closed_state(provider, authority, closed, completed, pending):
    with sqlite3.connect(':memory:') as connection:
        connection.execute('CREATE TABLE ipa (signed_by_provider, signed_by_local_authority, closed)')
        connection.execute('INSERT INTO ipa VALUES (?, ?, ?)', (provider, authority, closed))
        # The projection uses portable COALESCE, boolean CAST, AND and NOT operations.
        row = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchone()
        assert row == (provider or 0, authority or 0, completed, pending)


def test_multiple_ipas_do_not_collapse_signature_counts_to_one_offer():
    with sqlite3.connect(':memory:') as connection:
        connection.execute('CREATE TABLE ipa (offer_id, signed_by_provider, signed_by_local_authority, closed)')
        connection.executemany('INSERT INTO ipa VALUES (?, ?, ?, ?)', [
            ('offer-1', 1, 1, 0), ('offer-1', 0, 1, 0), ('offer-1', 0, 0, 1),
        ])
        rows = connection.execute('SELECT ' + SIGNATURE_PROJECTION + ' FROM ipa i').fetchall()
        assert len(rows) == 3
        assert sum(row[2] for row in rows) == 1
        assert sum(row[3] for row in rows) == 1


@pytest.mark.parametrize('status,created,updated,expected', [
    ('DRAFT', '2026-09-15 08:00:00', '2026-09-15 08:00:00', (0, 1)),
    ('DRAFT', '2026-09-15 08:00:00', '2026-09-15 09:00:00', (0, 0)),
    ('DRAFT', '2026-09-15 08:00:00', None, (1, 0)),
    ('OFFER_MADE', '2026-09-15 08:00:00', '2026-09-15 08:00:00', (0, 0)),
])
def test_same_day_draft_edits_are_activity(status, created, updated, expected):
    start = NOTEBOOK.index("  LOWER(COALESCE(o.offer_status, '')) = 'draft'")
    end = NOTEBOOK.index("  LOWER(COALESCE(o.offer_status, '')) IN", start)
    projection = NOTEBOOK[start:end].strip().rstrip(',')
    # SQLite datetime() stands in for Spark's timestamp cast for these second-precision fixtures.
    projection = re.sub(r'CAST\((o\.\w+) AS TIMESTAMP\)', r'datetime(\1)', projection)
    with sqlite3.connect(':memory:') as connection:
        connection.execute('CREATE TABLE offer (offer_status, offer_date, last_modified_date)')
        connection.execute('INSERT INTO offer VALUES (?, ?, ?)', (status, created, updated))
        assert connection.execute('SELECT ' + projection + ' FROM offer o').fetchone() == expected
