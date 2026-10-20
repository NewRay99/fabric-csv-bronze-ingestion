"""Saved-definition checks only; no assertion of Desktop/DAX execution."""

from pathlib import Path
import re
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import add_wmpp_provider_offer_status as status


def test_status_cohort_has_clear_no_offer_unknown_and_external_filter_paths():
    dax = status.status_match()
    assert "ISFILTERED('Provider Offer Status'[Status])" in dax
    assert "IF(NOT limited, 1," in dax
    assert '"(No offers)" IN statuses && COUNTROWS(providerOffers) = 0' in dax
    assert "COALESCE('fact_offer'[offer_status], \"(Unknown status)\") IN statuses" in dax
    assert "'fact_offer'[provider_id] == providerKey" in dax
    assert "'fact_offer'[provider_home_id] IN homes" in dax
    assert "ALLSELECTED()" in dax
    assert "REMOVEFILTERS()" not in dax


@pytest.mark.parametrize(
    ("name", "rejected", "replacement"),
    [
        ("Provider matches offer status", "key", "providerKey"),
        ("Explorer provider row visible", "key", "providerKey"),
        ("Provider scoring result", "row", "scoringOrdinal"),
        ("Provider scoring evidence status", "row", "scoringOrdinal"),
    ],
)
def test_generated_variables_avoid_confirmed_desktop_parser_errors(
    name, rejected, replacement
):
    definitions = {
        metric: dax
        for metric, dax, _ in [
            *status.core.definitions(),
            *status.review.definitions(),
        ]
    }
    definitions[status.MATCH] = status.status_match()
    dax = definitions[name]
    assert not re.search(rf"\bVAR\s+{rejected}\s*=", dax, re.IGNORECASE)
    assert f"VAR {replacement} =" in dax


def test_dropdown_uses_a_detached_provider_selector_and_clears_old_state():
    template = {
        "name": "old",
        "position": {},
        "filterConfig": {"old": True},
        "isHidden": True,
        "visual": {"query": {}, "objects": {"general": [{"filter": "old"}]}},
    }
    v = status.dropdown(template)
    assert v["name"] == status.SELECTOR
    assert "filterConfig" not in v
    assert "isHidden" not in v
    field = v["visual"]["query"]["queryState"]["Values"]["projections"][0]["field"]["Column"]
    assert field["Expression"]["SourceRef"]["Entity"] == status.TABLE
    assert field["Property"] == "Status"
    assert "general" not in v["visual"]["objects"]
    assert template["isHidden"] is True  # Original template is preserved.


def test_measure_extraction_retains_multi_line_formula_not_metadata():
    source = "table 'T'\n\tmeasure 'First' = ONE()\n\t\tformatString: 0\n\tmeasure 'Second' =\n\t\t\tVAR n = 1\n\t\t\tRETURN n\n\t\tlineageTag: abc\n"
    assert status.get_measure(source, "First") == "ONE()"
    assert status.get_measure(source, "Second") == "VAR n = 1\nRETURN n"
