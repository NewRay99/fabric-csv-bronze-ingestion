"""Saved-format compatibility checks against the user's working native rule.

This checks emitted PBIR, not Power BI rendering. The fixture was captured from
the saved WIP after Desktop successfully rendered UNDER_OFFER with an orange icon.
"""

from copy import deepcopy
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import wmpp_status_icons as icons  # noqa: E402
import repair_wmpp_native_status_rules as repair  # noqa: E402


NATIVE = json.loads(
    (Path(__file__).parent / "fixtures/wmpp_native_status_rule.json").read_text(encoding="utf-8")
)
NATIVE_CASE = NATIVE["value"]["expr"]["Conditional"]["Cases"][0]
REFERENCE = NATIVE_CASE["Condition"]["Comparison"]["Left"]


def test_under_offer_uses_the_same_condition_as_the_working_native_rule():
    formatting = icons.icon_format(REFERENCE)
    cases = formatting["value"]["expr"]["Conditional"]["Cases"]
    match = next(
        (case for case in cases if case["Condition"].get("Comparison", {}).get("Right")
         == NATIVE_CASE["Condition"]["Comparison"]["Right"]),
        None,
    )
    assert match is not None, "No native equality rule for UNDER_OFFER"
    assert match["Condition"] == NATIVE_CASE["Condition"]
    assert match["Value"] == icons.literal("wmpp-category-status-under-offer")


def test_all_conditions_have_native_text_metadata_and_no_grouped_in_expression():
    formatting = icons.icon_format(REFERENCE)
    assert set(formatting) == set(NATIVE)
    assert formatting["layout"] == NATIVE["layout"]
    assert formatting["verticalAlignment"] == NATIVE["verticalAlignment"]
    conditional = formatting["value"]["expr"]["Conditional"]
    assert set(conditional) == {"Cases"}
    for case in conditional["Cases"]:
        condition = case["Condition"]
        assert set(condition) == {"Comparison", "Annotations"}
        assert condition["Annotations"] == NATIVE_CASE["Condition"]["Annotations"]
        assert condition["Comparison"]["ComparisonKind"] == 0
        assert condition["Comparison"]["Left"] == REFERENCE
        assert "Literal" in condition["Comparison"]["Right"]


@pytest.mark.parametrize("value,expected", [
    ("UNDER_OFFER", "under-offer"), ("Under offer", "under-offer"),
    ("CANCELLED", "cancelled"), ("Canceled", "cancelled"), ("CLOSED", "closed"),
    ("OPEN", "open"), ("DRAFT", "draft"), ("OFFER_MADE", "offer-made"),
    ("OFFER_SUCCESSFUL", "accepted"), ("OFFER_UNSUCCESSFUL", "declined"),
    ("WITHDRAWN", "withdrawn"), ("Unknown", "unknown"), ("", "unknown"),
])
def test_status_aliases_keep_their_intended_icon(value, expected):
    assert icons.resolve(icons.icon_format(REFERENCE), value) == icons.PREFIX + expected


def test_input_reference_is_not_mutated_or_double_aggregated():
    original = deepcopy(REFERENCE)
    formatting = icons.icon_format(REFERENCE)
    assert REFERENCE == original
    for case in formatting["value"]["expr"]["Conditional"]["Cases"]:
        assert case["Condition"].get("Comparison", {}).get("Left") == REFERENCE


def test_repair_changes_only_the_status_value_not_layout_query_or_other_icons():
    original = {
        "name": "fixture", "position": {"x": 270, "y": 540, "width": 1100, "height": 380},
        "filterConfig": {"filters": [{"name": "keep"}]},
        "visual": {
            "visualType": "tableEx",
            "query": {"queryState": {"Values": {"projections": [{
                "queryRef": "fact_referral.current_status", "field": REFERENCE,
            }]}}},
            "objects": {"values": [
                {"selector": {"metadata": "fact_referral.current_status"},
                 "properties": {"fontSize": 11, "icon": NATIVE}},
                {"selector": {"metadata": "fact_referral.priority"},
                 "properties": {"icon": {"kind": "Icon", "value": {"keep": True}}}},
            ]},
        },
    }
    untouched = deepcopy(original)
    changed, fields = repair.rewrite_visual(original)
    assert original == untouched
    assert fields == ["fact_referral.current_status"]
    repair.assert_only_icon_values_changed(original, changed, fields)
    assert changed["position"] == original["position"]
    assert changed["visual"]["query"] == original["visual"]["query"]
    assert repair.rewrite_visual(changed) == (changed, [])


def test_repair_rejects_unrelated_position_changes():
    original = {"position": {"x": 270}, "visual": {"objects": {"values": []}}}
    changed = deepcopy(original)
    changed["position"]["x"] = 0
    with pytest.raises(AssertionError, match="other than status icon"):
        repair.assert_only_icon_values_changed(original, changed, [])
