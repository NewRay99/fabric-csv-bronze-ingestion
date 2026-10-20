"""Check the narrow identifier migration, not Power BI visual rendering."""

from copy import deepcopy
import importlib.util
import json
from pathlib import Path

import pytest


PROJECT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "source_reference_migration", PROJECT / "tools/use_wmpp_source_reference_ids.py")
migration = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(migration)


def visual(fields, kind="tableEx"):
    return {"name": "test", "position": {"x": 316, "y": 900, "width": 1608, "height": 330},
            "visual": {"visualType": kind, "query": {"queryState": {"Values": {"projections": fields}}},
                       "objects": {"columnWidth": [{"selector": {"metadata": "fact_offer.referral_id"},
                                    "properties": {"value": {"expr": {"Literal": {"Value": "257D"}}}}}]},
                       "visualContainerObjects": {"background": [{"custom": "preserve"}]}},
            "filterConfig": {"filters": [{"field": migration.column("fact_referral", "referral_id"),
                              "filter": {"Version": 2, "test": "UUID-filter-remains"}}]}}


def old_projection(entity):
    return {"field": migration.column(entity, "referral_id"), "queryRef": f"{entity}.referral_id"}


@pytest.mark.parametrize("entity", sorted(migration.REFERRAL_ENTITIES))
def test_table_uses_canonical_reference_and_sequence_without_moving_or_rekeying_filters(entity):
    original = visual([old_projection(entity), migration.projection("current_status", "Status")])
    frozen = deepcopy(original)
    result = migration.table_reference_visual(original)
    assert original == frozen
    assert result["position"] == original["position"]
    assert result["filterConfig"] == original["filterConfig"]
    assert result["visual"]["visualContainerObjects"] == original["visual"]["visualContainerObjects"]
    refs = [p["queryRef"] for p in result["visual"]["query"]["queryState"]["Values"]["projections"]]
    assert refs == ["fact_referral.source_reference_id", "fact_referral.order_dupe",
                    "fact_referral.has_multiple_referrals", "fact_referral.current_status"]
    assert migration.table_reference_visual(result) == result


def test_two_uuid_projections_do_not_add_reference_columns_twice():
    original = visual([old_projection("fact_referral"), old_projection("fact_referral_provider")])
    fields = migration.table_reference_visual(original)["visual"]["query"]["queryState"]["Values"]["projections"]
    assert len(fields) == 3
    assert len({p["queryRef"] for p in fields}) == 3


def test_column_width_selector_follows_reference_but_keeps_existing_width():
    result = migration.table_reference_visual(visual([old_projection("fact_offer")]))
    width = result["visual"]["objects"]["columnWidth"][0]
    assert width["selector"]["metadata"] == "fact_referral.source_reference_id"
    assert width["properties"]["value"]["expr"]["Literal"]["Value"] == "257D"


def test_non_referral_table_and_journey_count_not_changed():
    original = visual([migration.projection("current_status", "Status")])
    assert migration.table_reference_visual(original) == original
    original = visual([old_projection("fact_referral")], "card")
    assert migration.table_reference_visual(original) == original


def test_selection_label_uses_reference_but_single_referral_guard_still_uses_uuid():
    original = ('HASONEVALUE(\'fact_referral\'[referral_id]),'
                '"Selected referral: " & SELECTEDVALUE(\'fact_referral\'[referral_id])')
    result = migration.reference_selection_label(original)
    assert "HASONEVALUE('fact_referral'[referral_id])" in result
    assert "SELECTEDVALUE('fact_referral'[source_reference_id])" in result
    assert "SELECTEDVALUE('fact_referral'[order_dupe])" in result
    assert "SELECTEDVALUE('fact_referral'[referral_id])" not in result
    assert migration.reference_selection_label(result) == result


def test_slicer_refuses_to_migrate_saved_uuid_selections():
    with pytest.raises(ValueError, match="Clear saved referral UUID"):
        migration.reference_slicer(visual([old_projection("fact_referral")], "slicer"))


def test_compound_drillthrough_fields_match_table_and_preserve_binding_identity():
    original = {"width": 1960, "height": 3100,
                "filterConfig": {"filters": [{"name": "old-filter", "type": "Categorical",
                   "howCreated": "Drillthrough", "field": migration.column("fact_referral", "referral_id")}]},
                "pageBinding": {"name": "binding", "type": "Drillthrough", "acceptsFilterContext": "None",
                   "parameters": [{"name": "old-param", "boundFilter": "old-filter",
                        "fieldExpr": migration.column("fact_referral", "referral_id")}]}}
    result = migration.detail_reference_binding(original)
    assert result["width"] == original["width"] and result["height"] == original["height"]
    binding = result["pageBinding"]
    assert binding["name"] == "binding" and binding["acceptsFilterContext"] == "None"
    assert binding["parameters"][0]["name"] == "old-param"
    assert {p["fieldExpr"]["Column"]["Property"] for p in binding["parameters"]} == {
        "source_reference_id", "order_dupe"}
    filters = {f["name"]: f["field"] for f in result["filterConfig"]["filters"]}
    assert all(filters[p["boundFilter"]] == p["fieldExpr"] for p in binding["parameters"])
    assert migration.detail_reference_binding(result) == result


@pytest.mark.parametrize("entity", ["dim_person", "fact_referral", "fact_referral_snapshot"])
def test_model_fields_are_direct_gold_imports_not_new_keys_or_dax_derivations(entity):
    source = (f"table {entity}\n\tcolumn referral_id\n\t\tlineageTag: keep-me\n"
              f"\t\tsourceColumn: referral_id\n\n\tpartition {entity} = m\n"
              "\t\tmode: import\n\t\tsource =\n\t\t\tKEEP_CONNECTION\n")
    result = migration.reference_model(source, entity)
    assert "lineageTag: keep-me" in result and "KEEP_CONNECTION" in result
    assert "\t\tsummarizeBy: sum" not in result
    assert migration.reference_model(result, entity) == result
    assert "sourceColumn: source_reference_id" in result
    if entity != "dim_person":
        assert "sourceColumn: order_dupe" in result
        assert "sourceColumn: has_multiple_referrals" in result


def test_current_wip_migration_plan_does_not_touch_roles_relationships_or_bookmarks():
    root = migration.DEFAULT_ROOT
    if not root.exists():
        pytest.skip("User's gitignored WIP is absent on this checkout")
    changes = migration.plan(root)
    assert not any("roles" in p.parts or "bookmarks" in p.parts or p.name == "relationships.tmdl"
                   for p in changes)
    for path, value in changes.items():
        if path.name == "visual.json":
            before = json.loads(path.read_text(encoding="utf-8-sig"))
            after = json.loads(value)
            assert after["position"] == before["position"]


def test_saved_referral_tables_have_no_exposed_uuid_and_detail_has_both_filter_fields():
    root = migration.DEFAULT_ROOT
    if not root.exists():
        pytest.skip("User's gitignored WIP is absent on this checkout")
    # Validate the effective plan both before and after it is applied.
    planned = migration.plan(root)
    for path in (root / "SM_WMPP_v16.Report/definition/pages").glob("*/visuals/*/visual.json"):
        data = json.loads(planned.get(path, path.read_text(encoding="utf-8-sig")))
        if data.get("visual", {}).get("visualType") == "tableEx":
            fields = data["visual"]["query"]["queryState"]["Values"]["projections"]
            assert not any(migration.is_referral_id(p.get("field", {})) for p in fields)
            refs = {p["queryRef"] for p in fields}
            if "fact_referral.source_reference_id" in refs:
                assert "fact_referral.order_dupe" in refs
