"""Saved-definition safety checks, not Power BI rendering or DAX execution."""

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("offer_map", ROOT / "tools/add_wmpp_offer_location_map.py")
MAP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MAP)
TEMPLATE = (ROOT / "tools/templates/offer_location_paths.tmdl").read_text(encoding="utf-8")


def test_path_binding_matches_installed_azure_map_capabilities():
    visual = MAP.map_visual()
    query = visual["visual"]["query"]["queryState"]
    assert set(query) == {"PathID", "PointOrder", "X", "Y", "Tooltips"}
    assert query["PathID"]["projections"][0]["field"]["Column"]["Property"] == "Offer ID"
    assert query["PointOrder"]["projections"][0]["field"]["Column"]["Property"] == "Point order"
    assert query["X"]["projections"][0]["field"]["Column"]["Property"] == "Longitude"
    assert query["Y"]["projections"][0]["field"]["Column"]["Property"] == "Latitude"
    assert "Category" not in query  # No text geocoding.
    assert "Series" not in query  # Endpoint type must not split each line into two paths.


def test_two_endpoint_rows_per_offer_not_two_offer_counts():
    assert TEMPLATE.count('SELECTCOLUMNS ( eligibleOffers,') == 2
    assert '"Point order", 0' in TEMPLATE and '"Point order", 1' in TEMPLATE
    assert '"Latitude", \'fact_offer\'[referral_latitude]' in TEMPLATE
    assert '"Latitude", \'fact_offer\'[provider_home_latitude]' in TEMPLATE
    assert 'DISTINCTCOUNTNOBLANK ( \'Offer Location Paths\'[Offer ID] )' in TEMPLATE
    assert "COUNTROWS ( 'Offer Location Paths' )" not in TEMPLATE


@pytest.mark.parametrize("column", MAP.COORDINATES)
def test_all_four_coordinates_must_be_present(column):
    assert f"NOT ISBLANK ( 'fact_offer'[{column}] )" in TEMPLATE


def test_review_and_incomplete_paths_cannot_be_drawn():
    assert "NOT ( 'fact_offer'[location_requires_review] == TRUE () )" in TEMPLATE
    assert '"APPROXIMATE_PREFERENCE_CITY", "APPROXIMATE_DEFAULT_CITY"' in TEMPLATE
    assert "'fact_offer'[referral_latitude] >= -90" in TEMPLATE
    assert "'fact_offer'[provider_home_longitude] <= 180" in TEMPLATE
    assert "HASONEVALUE ( 'fact_offer'[referral_id] )" in TEMPLATE
    assert "No connection available" in TEMPLATE
    assert "Default-city estimate" in TEMPLATE


def test_map_does_not_overlap_the_existing_offer_register():
    map_position = MAP.map_visual()["position"]
    assert map_position["x"] >= 316
    assert map_position["y"] > 1093  # Lowest pre-existing visible footer edge.
    assert map_position["x"] + map_position["width"] <= 1960
    assert map_position["y"] + map_position["height"] < 1870


def test_template_has_no_unsecured_or_bidirectional_filter_bypass():
    assert "REMOVEFILTERS" not in TEMPLATE
    assert "CROSSFILTER" not in TEMPLATE
    assert "ALL (" not in TEMPLATE
    source = Path(MAP.__file__).read_text(encoding="utf-8")
    assert "toColumn: fact_offer.offer_id" in source
    assert "crossFilteringBehavior: bothDirections" not in source


def test_generated_visual_is_json_serializable():
    assert json.loads(json.dumps(MAP.map_visual())) == MAP.map_visual()
