"""Regression check for GLD-016 provider KPI offer-key compatibility."""

from pathlib import Path

from notebook_loader import load_notebook


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "04_gold_model.py"


notebook = load_notebook(NOTEBOOK)
source = "\n".join(
    "".join(cell.get("source", [])) for cell in notebook["cells"]
)
kpi_sql = source.split(
    "CREATE OR REPLACE TABLE gold.fact_provider_kpi_monthly AS", 1
)[1].split(
    "CREATE OR REPLACE MATERIALIZED LAKE VIEW gold.rpt_kpi_referral_board_summary",
    1,
)[0]
offer_component = kpi_sql.split("WITH offer_component AS (", 1)[1].split(
    "), assignment_component AS (", 1
)[0]
fact_offer_sql = source.split(
    "CREATE OR REPLACE TABLE gold.fact_offer AS", 1
)[1].split(
    "CREATE OR REPLACE TABLE gold.fact_ipa AS", 1
)[0]

# Keep the source-grain offer fact reusable: publish the assignment key once,
# then make downstream Gold reporting facts depend on that governed contract.
assert "o.referral_provider_id AS referral_provider_id" in fact_offer_sql, (
    "GLD-016: gold.fact_offer does not publish the assignment key"
)
assert "FROM silver.offer o" in fact_offer_sql
assert "TO_DATE(o.offer_date) <= {AS_OF_SQL}" in fact_offer_sql
assert "FROM gold.fact_offer" in offer_component
assert "SELECT referral_provider_id," in offer_component
assert "GROUP BY referral_provider_id" in offer_component
assert "ON rp.referral_provider_id = o.referral_provider_id" in kpi_sql

issue_log = (ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md").read_text(
    encoding="utf-8"
)
gld016 = issue_log.split("## GLD-016", 1)[1]
assert "### Resolution (2026-09-21)" in gld016
assert "**Status:** resolved in repository source" in gld016

print("PASS GLD-016 publishes and consumes the Gold offer assignment key")
