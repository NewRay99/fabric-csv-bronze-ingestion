"""Saved button-state and preservation contracts, not rendered pixel tests."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import wmpp_drillthrough_button_style as style


def test_detects_the_original_unscoped_text_pattern():
    original = {
        "visual": {
            "objects": {
                "text": [{"properties": {"text": {"expr": {"Literal": {"Value": "'Open'"}}}}}]
            }
        }
    }
    assert style.missing_state_labels(original) == list(style.STATES)


def test_styles_each_real_native_state_without_moving_or_rebinding():
    original = {
        "name": "original",
        "position": {"x": 123.45, "y": 456.78, "width": 354, "height": 42, "z": 166000},
        "parentGroupName": "existing-group",
        "visual": {
            "visualType": "actionButton",
            "visualContainerObjects": {
                "visualLink": [{"properties": {"drillthroughSection": "keep"}}]
            },
        },
    }
    result = style.style_button(original, "View referral details →", "Select a referral first")
    assert style.missing_state_labels(result) == []
    assert result["position"] == original["position"]
    assert result["parentGroupName"] == original["parentGroupName"]
    assert (
        result["visual"]["visualContainerObjects"]["visualLink"]
        == original["visual"]["visualContainerObjects"]["visualLink"]
    )
    assert "objects" not in original["visual"]
    states = {
        x["selector"]["id"]: x["properties"]
        for x in result["visual"]["objects"]["text"]
        if "selector" in x
    }
    assert states["default"]["text"]["expr"]["Literal"]["Value"] == "'View referral details →'"
    assert states["disabled"]["text"]["expr"]["Literal"]["Value"] == "'Select a referral first'"
    for properties in states.values():
        assert properties["bold"]["expr"]["Literal"]["Value"] == "false"
