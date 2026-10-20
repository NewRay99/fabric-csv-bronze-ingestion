"""Regression checks for PERF-001 referral-provider scan consolidation."""

from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SILVER_RULES = ROOT / "03_silver_business_rules.py"
def source(path):
    notebook = read_notebook(path)
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def validate_rollup(text, label):
    for expected in (
        'replace_silver_materialisation(referral_provider_rollup, "referral_provider_rollup")',
        "FROM silver.referral_provider rp",
        "GROUP BY rp.referral_id",
        "COUNT(DISTINCT o.offer_id) AS cnt_offer_made",
        "COUNT(DISTINCT rp.provider_id) AS provider_assignment_count",
        "AS has_live_provider",
        "AS has_engaged_provider",
        "silver.referral_provider_rollup pr",
        "COALESCE(pr.provider_assignment_count, 0) AS provider_assignment_count",
        'log_step("Materialised referral_provider_rollup")',
    ):
        assert expected in text, f"{label} is missing PERF-001 rollup contract: {expected}"
    assert "offer_rollup AS" not in text, (
        f"{label} still computes offer rollups inside referral_enrichment"
    )
    assert "provider_seen AS" not in text, (
        f"{label} still rescans provider assignments for first-seen dates"
    )
    assert "live_provider AS" not in text and "engaged_provider AS" not in text, (
        f"{label} still rescans provider assignments for engagement flags"
    )


validate_rollup(source(SILVER_RULES), "03_silver_business_rules")
issue_log = (ROOT / "change tracking" / "ETL_ISSUE_LOG.md").read_text(
    encoding="utf-8"
)
assert "## PERF-001" in issue_log, "PERF-001 is not recorded in the issue log"
print("PASS PERF-001 materialises one referral-provider rollup for enrichment")
