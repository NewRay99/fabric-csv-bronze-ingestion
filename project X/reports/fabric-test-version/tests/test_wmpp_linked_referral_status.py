"""Contract and preservation checks for the linked referral status column."""

from copy import deepcopy
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "reports/WIP/SM WMPP v16 updated WIP"
BACKUP = ROOT / "reports/_review/linked-referral-status-before-20261019"
TABLE = PROJECT / "SM_WMPP_v16.SemanticModel/definition/tables/Linked Provider Referrals.tmdl"
VISUAL = PROJECT / "SM_WMPP_v16.Report/definition/pages/08ef33dc6a87d1b14392/visuals/586a1ac1befa7498ed75"
NAME = "Linked referral current status"
QUERY_REF = f"Linked Provider Referrals.{NAME}"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def comparable_tmdl_lines(text):
    """Ignore save-time blank-line padding, not tokens or leading indentation."""
    return tuple(
        line.rstrip(" \t")
        for line in text.splitlines()
        if line.strip(" \t")
    )


def test_model_preservation_tolerates_desktop_blank_line_formatting():
    before = "table 'T'\n\n\tmeasure M =\n\t\tRETURN 1\n"
    after = "table 'T'\r\n\t \r\n\tmeasure M =\r\n\t\tRETURN 1  \r\n\r\n"
    assert comparable_tmdl_lines(before) == comparable_tmdl_lines(after)


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("\t\tRETURN 1\n", "\t\tRETURN 0\n"),
        ('\t\tRETURN "Unknown provider"\n', '\t\tRETURN "Unknownprovider"\n'),
        ('\t\tRETURN "A "\n', '\t\tRETURN "A"\n'),
        ("\tmeasure M = 1\n", "\t\tmeasure M = 1\n"),
    ],
)
def test_model_preservation_still_detects_definition_changes(before, after):
    assert comparable_tmdl_lines(before) != comparable_tmdl_lines(after)


def test_measure_matches_visible_pairs_using_referral_uuid():
    text = TABLE.read_text(encoding="utf-8-sig")
    measure = text.split(f"\tmeasure '{NAME}' =", 1)[1].split("\n\t\tdisplayFolder:", 1)[0]
    for required in (
        "CALCULATE([Linked provider row visible]) = 1",
        "'Linked Provider Referrals'[provider_id]",
        "DISTINCT(SELECTCOLUMNS(linkedPairs,",
        '"referral_id", \'Linked Provider Referrals\'[referral_id]',
        "VALUES('fact_referral'[current_status])",
        "REMOVEFILTERS('dim_provider')",
        "KEEPFILTERS(TREATAS(linkedReferralIds,",
        "'fact_referral'[referral_id]",
        "RETURN IF(COUNTROWS(linkedPairs) > 0,",
        "CONCATENATEX(",
        "'fact_referral'[current_status], ASC",
        '"(Unknown status)"',
        '"Referral not found"',
    ):
        assert required in measure
    assert "Source Reference ID" not in measure


def test_existing_model_definitions_are_unchanged():
    before = (BACKUP / "Linked Provider Referrals.tmdl").read_text(encoding="utf-8-sig")
    after = TABLE.read_text(encoding="utf-8-sig")
    without_new_measure, count = re.subn(
        r"\t/// Current referral statuses for visible shared referral/provider pairs\.\n"
        r".*?\t\tlineageTag: 61059267-92a0-4247-9a47-dc66a17ff9de\n\n",
        "", after, count=1, flags=re.DOTALL,
    )
    assert count == 1
    assert comparable_tmdl_lines(without_new_measure) == comparable_tmdl_lines(before)


def test_desktop_adds_only_status_projection_and_width():
    before = read_json(BACKUP / "visual.json")
    after = read_json(VISUAL / "visual.json")
    restored = deepcopy(after)
    projections = restored["visual"]["query"]["queryState"]["Values"]["projections"]
    added = [p for p in projections if p["queryRef"] == QUERY_REF]
    assert len(added) == 1
    assert added[0]["field"]["Measure"]["Property"] == NAME
    assert added[0]["displayName"] == "Referral current status"
    assert projections.index(added[0]) == next(
        i for i, p in enumerate(projections)
        if p["queryRef"] == "Linked Provider Referrals.Linked offer statuses"
    ) + 1
    projections.remove(added[0])
    widths = restored["visual"]["objects"]["columnWidth"]
    new_widths = [w for w in widths if w["selector"]["metadata"] == QUERY_REF]
    assert len(new_widths) == 1
    assert new_widths[0]["properties"]["value"]["expr"]["Literal"]["Value"] == "180D"
    widths.remove(new_widths[0])
    assert restored == before


def test_mobile_preserves_layout_and_fonts():
    before = read_json(BACKUP / "mobile.json")
    restored = read_json(VISUAL / "mobile.json")
    widths = restored["objects"]["columnWidth"]
    new_widths = [w for w in widths if w["selector"]["metadata"] == QUERY_REF]
    assert len(new_widths) == 1
    assert new_widths[0]["properties"]["value"]["expr"]["Literal"]["Value"] == "144D"
    widths.remove(new_widths[0])
    assert restored == before
