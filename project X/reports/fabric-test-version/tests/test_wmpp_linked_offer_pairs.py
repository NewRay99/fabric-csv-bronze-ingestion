"""Saved-DAX contract checks; live expression execution is verified separately."""

from pathlib import Path
import re


MODEL = Path(__file__).resolve().parents[1] / "reports/WIP/SM WMPP v16 updated WIP/SM_WMPP_v16.SemanticModel/definition"
TABLE = MODEL / "tables/Linked Provider Referrals.tmdl"


def source_parts():
    text = TABLE.read_text(encoding="utf-8-sig")
    partition = text.split("\tpartition 'Linked Provider Referrals' = calculated", 1)[1]
    source = partition.split("\t\tsource =", 1)[1].split("\n\tannotation", 1)[0]
    return text, source.split("\t\t\t\tRETURN", 1)


def test_pair_candidates_come_only_from_filtered_offers():
    _, (pairs, _) = source_parts()
    assert "UNION(" not in pairs
    assert "'fact_referral_provider'" not in pairs
    assert re.search(r"FILTER\s*\(\s*'fact_offer'\s*,", pairs)
    assert "'fact_offer'[offer_status]" in pairs and "IN {" in pairs
    assert set(re.findall(r'"(OFFER_[A-Z]+)"', pairs)) == {
        "OFFER_MADE", "OFFER_SUCCESSFUL", "OFFER_UNSUCCESSFUL"
    }


def test_pair_grain_and_reference_lookups_are_retained():
    text, (pairs, enrich) = source_parts()
    assert "DISTINCT(" in pairs
    assert '"referral_id", \'fact_offer\'[referral_id]' in pairs
    assert '"provider_id", \'fact_offer\'[provider_id]' in pairs
    assert "NOT ISBLANK([referral_id]) && NOT ISBLANK([provider_id])" in enrich
    for field in ("'dim_provider'[provider_name]", "'fact_referral'[person_id]", "'dim_person'[Source Reference ID]"):
        assert field in enrich
    for field in ("provider_id", "referral_id", "provider_name", "'Source Reference ID'"):
        assert f"\tcolumn {field}\n" in text


def test_existing_cancellation_and_search_safeguards_remain():
    text, _ = source_parts()
    assert "UPPER(TRIM(COALESCE('fact_referral'[current_status], \"\"))) = \"CANCELLED\"" in text
    assert "UPPER(TRIM(COALESCE('fact_referral_provider'[provider_response_status], \"\"))) = \"CANCELLED\"" in text
    assert "NOT (linkedProviderId IN searchedProviderIds)" in text
    assert "hasProviderSearch" in text
