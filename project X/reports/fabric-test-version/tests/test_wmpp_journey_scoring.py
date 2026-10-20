"""Metric and reference safety checks, not rendered-layout unit tests."""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import improve_wmpp_journeys_scoring as review
from audit_wmpp_report_journeys import inventory


def test_provider_menu_bookmarks_are_not_record_navigation():
    # These share the drillthrough page as activeSection, but only change display.
    for name in ("Offers", "Performance", "Referrals", "Providers", "Close menus"):
        menu = {
            "displayName": "Provider Detail | " + name,
            "explorationState": {"activeSection": review.PD},
            "options": {
                "applyOnlyToTargetVisuals": True,
                "suppressActiveSection": True,
                "suppressData": True,
            },
        }
        assert not review.is_provider_detail_navigation_bookmark(menu), name
    navigation = {
        "explorationState": {"activeSection": review.PD},
        "options": {"suppressActiveSection": False},
    }
    assert review.is_provider_detail_navigation_bookmark(navigation)
    assert not review.is_provider_detail_navigation_bookmark(
        {"explorationState": {"activeSection": review.PROVIDER}}
    )


def test_provider_scoring_does_not_invent_composite_policy():
    defs = {name: dax for name, dax, _ in review.definitions()}
    assert '8, "Not approved"' in defs["Provider scoring result"]
    assert "[Explorer Gold response rate]" in defs["Provider scoring result"]
    assert "[Explorer Gold offer acceptance rate]" in defs["Provider scoring result"]
    assert "[Explorer Gold target placement rate]" in defs["Provider scoring result"]
    assert "Insufficient evidence" in defs["Provider scoring result"]
    assert "0.20" not in defs["Provider scoring result"]
    assert "AVERAGE('fact_provider_kpi_monthly'" not in "\n".join(defs.values())


def test_action_metrics_do_not_treat_missing_response_as_false():
    defs = {name: dax for name, dax, _ in review.definitions()}
    assert "[has_qualifying_response] == FALSE()" in defs["Provider unanswered assignments"]
    assert (
        "NOT ISBLANK('fact_referral_provider'[assigned_at])"
        in defs["Provider unanswered assignments"]
    )
    assert "VALUES('fact_referral'[referral_id])" in defs["Referral open without offers"]
    assert "CALCULATE(COUNTROWS('fact_offer')) = 0" in defs["Referral open without offers"]
    assert "CALCULATE(COUNTROWS('fact_ipa')) = 0" in defs["Referral accepted without IPA"]


def test_detail_summaries_require_one_canonical_key():
    defs = {name: dax for name, dax, _ in review.definitions()}
    for name in [n for n in defs if n.startswith("Provider detail")]:
        assert "HASONEVALUE('dim_provider'[provider_id])" in defs[name]
    for name in [n for n in defs if n.startswith("Referral detail")]:
        assert "HASONEVALUE('fact_referral'[referral_id])" in defs[name]
    drill = review.button(review.PROVIDER, review.PD, "Open detail", 100)
    props = drill["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
    assert props["type"]["expr"]["Literal"]["Value"] == "'Drillthrough'"
    assert "bookmark" not in props


def test_audit_validates_planned_new_fields_and_drill_targets(tmp_path):
    model = tmp_path / "SM_WMPP_v16.SemanticModel/definition/tables"
    pages = tmp_path / "SM_WMPP_v16.Report/definition/pages"
    bookmarks = tmp_path / "SM_WMPP_v16.Report/definition/bookmarks"
    model.mkdir(parents=True)
    pages.mkdir(parents=True)
    bookmarks.mkdir(parents=True)
    pp = pages / "source/page.json"
    pp.parent.mkdir()
    pp.write_text(
        json.dumps({"name": "source", "displayName": "Source", "height": 945, "width": 1680})
    )
    vp = pages / "source/visuals/new/visual.json"
    table = model / "New.tmdl"
    overrides = {
        table: "table 'New'\n\tmeasure 'Count' = 1\n",
        vp: json.dumps(
            {
                "name": "new",
                "position": {},
                "visual": {
                    "query": {
                        "queryState": {
                            "Data": {
                                "projections": [
                                    {
                                        "field": {
                                            "Measure": {
                                                "Expression": {"SourceRef": {"Entity": "New"}},
                                                "Property": "Count",
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    }
                },
            }
        ),
    }
    assert inventory(tmp_path, overrides)["missing_fields"] == []
    overrides[vp] = overrides[vp].replace('"Count"', '"Absent"')
    assert inventory(tmp_path, overrides)["missing_fields"]
    overrides[vp] = json.dumps(review.button("source", "missing-target", "Open", 100))
    assert inventory(tmp_path, overrides)["broken_actions"]
