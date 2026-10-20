"""Explorer scope/reference checks. Rendered interaction acceptance stays in Desktop."""

from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import repair_wmpp_explorer_scope as repair


def test_master_entity_scopes_do_not_require_offers():
    defs = {name: dax for name, dax, _ in repair.definitions()}
    provider = defs["Explorer provider row visible"]
    assert "'dim_provider'[provider_id]" in provider
    assert "'fact_offer'" not in provider
    assert "NOT homeFilter || matchingHomes > 0" in provider
    referral = repair.referral_scope()
    assert "VALUES('fact_referral'[referral_id])" in referral
    assert "NOT(statusFilter || bandFilter)" in referral
    assert '"(No offers)" IN statuses' in referral
    assert '"(No offers)" IN bands' in referral


def test_counts_are_distinct_and_response_statistics_use_assignment_grain():
    defs = {name: dax for name, dax, _ in repair.definitions()}
    for name in [
        "Explorer provider offers",
        "Explorer provider offers made",
        "Explorer referral offers",
    ]:
        assert "DISTINCTCOUNTNOBLANK('fact_offer'[offer_id])" in defs[name]
    assert (
        "AVERAGE('fact_referral_provider'[response_elapsed_minutes])"
        in defs["Explorer provider average response minutes"]
    )
    assert (
        "MEDIAN('fact_referral_provider'[response_elapsed_minutes])"
        in defs["Explorer provider median response minutes"]
    )
    assert (
        "COUNTROWS('fact_provider_kpi_monthly') = 1"
        in defs["Explorer Gold median response minutes"]
    )


def test_provider_ipa_counts_are_offer_keyed_and_home_scoped():
    defs = {name: dax for name, dax, _ in repair.definitions()}
    for name in [
        "Explorer provider IPAs",
        "Explorer provider signed IPAs",
        "Explorer provider completed IPAs",
    ]:
        assert "TREATAS(offers,'fact_ipa'[accepted_offer_id])" in defs[name]
        assert "'fact_offer'[provider_home_id] IN homes" in defs[name]


def test_kpi_axes_have_existing_unique_metrics():
    defs = repair.definitions()
    names = [name for name, _, _ in defs]
    assert len(names) == len(set(names))
    for rows in [repair.PROVIDER_METRICS, repair.REFERRAL_METRICS]:
        assert len(rows) >= 13
        assert {name for _, _, name, _ in rows} <= set(names)
        assert len({label for _, label, _, _ in rows}) == len(rows)


def test_measure_replacement_preserves_metadata_and_neighbour():
    original = "table 'T'\n\tmeasure 'Old' = ONE()\n\t\tlineageTag: abc\n\tmeasure 'Next' = TWO()\n"
    changed = repair.replace_measure(original, "Old", "VAR n = 3\nRETURN n")
    assert "\tmeasure 'Old' =\n\t\t\tVAR n = 3\n\t\t\tRETURN n\n\t\tlineageTag: abc" in changed
    assert "measure 'Next' = TWO()" in changed
    assert not re.search(r"ONE\(\)", changed)
