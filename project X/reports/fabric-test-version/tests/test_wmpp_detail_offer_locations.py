"""Saved wiring contracts; native query behaviour is checked separately."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import wire_wmpp_detail_offer_locations as wire


def test_measure_preserves_referral_guard_and_matches_offer_ids():
    text = wire.MODEL.read_text(encoding="utf-8-sig")
    assert f"\tmeasure '{wire.NAME}' =" in text
    assert "IF([Detail referral selected] <> 1, BLANK()," in text
    assert "KEEPFILTERS(TREATAS(" in text
    assert "VALUES('fact_offer'[offer_id])" in text
    assert "'Referral Map Points'[Offer]" in text
    assert "IF(NOT offerSelected, 1," not in text
    assert "IF(COUNTROWS('Referral Map Points') > 0, 1, BLANK())" in text


def test_source_filters_directory_and_not_a_displayed_measure():
    page, visual = wire.original.read(wire.PAGE_FILE), wire.original.read(wire.VISUAL)
    assert {"source": wire.SOURCE, "target": wire.TARGET, "type": "DataFilter"} in page.get("visualInteractions", [])
    assert wire.filter_rule() in visual.get("filterConfig", {}).get("filters", [])
    assert not any(p.get("field") == wire.field()
                   for p in visual["visual"]["query"]["queryState"]["Values"]["projections"])


def test_filter_uses_semantic_query_literal_not_formatting_expression():
    comparison = wire.filter_rule()["filter"]["Where"][0]["Condition"]["Comparison"]
    assert comparison["Right"] == {"Literal": {"Value": "1L"}}
    assert comparison["Left"]["Measure"]["Expression"]["SourceRef"] == {"Source": "m"}
