"""Regression checks for derived referral lifecycle events replacing a missing source audit log."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "project X"
SETUP = PROJECT / "00_setup_cfg 02 03.ipynb"
SILVER_RULES = PROJECT / "03_silver_business_rules 02 03.ipynb"
GOLD = PROJECT / "04_gold_model 02 03.ipynb"


def source(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def main():
    setup = source(SETUP)
    assert "silver.slv_referral_event_log" not in setup, (
        "Setup must not fabricate a Silver event-log source table"
    )
    print("PASS setup does not fabricate a referral event-log source")

    silver = source(SILVER_RULES)
    for token in [
        "referral_lifecycle_event", "ReferralCreated", "ReferralModified",
        "OfferSubmitted", "OfferUpdated", "IPACreated", "IPAUpdated",
        "IPAAdmission", "ProviderMessageSent", "silver.slv_referral_provider",
    ]:
        assert token in silver, f"Silver lifecycle materialisation lacks {token}"
    print("PASS Silver materialises lifecycle events from real sources")

    gold = source(GOLD)
    assert "silver.slv_referral_lifecycle_event" in gold
    assert "gold.fact_referral_lifecycle_event" in gold
    assert "silver.slv_referral_event_log" not in gold
    assert "gold.fact_referral_event_log" not in gold
    print("PASS Gold uses derived lifecycle events, not a nonexistent audit source")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
