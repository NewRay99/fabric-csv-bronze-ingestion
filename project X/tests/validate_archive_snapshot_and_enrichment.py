"""Static regression checks for ARCH-ETL-001/002, LIVE-ETL-001 and SI-018/019."""

import ast
import csv
from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE_RUNNER = ROOT / "90_run_archive_pipeline.py"
ARCHIVE_SILVER = ROOT / "02a_archive_silver.py"
GOLD = ROOT / "04_gold_model.py"
DQ = ROOT / "03_silver_business_rules.py"
DQ_CONFIG = ROOT / "configuration" / "dq_rule_definition.csv"
ARCHITECTURE = (
    ROOT
    / "client documentation"
    / "03_Architecture_and_Design"
    / "Proposed_Solution_Architecture.md"
)
REQUIREMENTS = (
    ROOT
    / "client documentation"
    / "02_Assessment_and_Requirements"
    / "KPI_Enhancement_Requirements.md"
)


def notebook_source(path: Path) -> str:
    notebook = read_notebook(path)
    for index, cell in enumerate(notebook["cells"]):
        code = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and not code.lstrip().startswith("%"):
            ast.parse(code, filename=f"{path.name}:cell-{index}")
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


archive_runner = notebook_source(ARCHIVE_RUNNER)
archive_silver = notebook_source(ARCHIVE_SILVER)
gold = notebook_source(GOLD)
dq = notebook_source(DQ)
print("PASS Fabric notebook cells and Python syntax")

assert "NOTEBOOK_TIMEOUT_SECONDS = 7200" in archive_runner
assert '"spark.synapse.nbs.session.timeout": "7200000"' in ARCHIVE_RUNNER.read_text(
    encoding="utf-8-sig"
)
assert "NOTEBOOK_TIMEOUT_SECONDS = 7200" in archive_silver
assert "DQ_NOTEBOOK_NAME, NOTEBOOK_TIMEOUT_SECONDS" in archive_silver
assert "GOLD_NOTEBOOK_NAME,\n                NOTEBOOK_TIMEOUT_SECONDS" in archive_silver
print("PASS ARCH-ETL-001 archive timeout is two hours through child execution")

assert "month_last_dates" in archive_silver
assert "canonical month-end export" in archive_silver
assert "month_predicate" in gold
assert ".option(\"replaceWhere\", month_predicate)" in gold
assert "replaced active month" in gold
assert "AS_OF_DATE_VALUE = date.today()" in gold
# Gold intentionally reads only conformed Silver sources. Archive ownership
# and the physical archive-to-Silver handoff are verified in Archive Silver.
assert 'source_table = f"{ARCHIVE_SCHEMA}.{physical_table}"' in archive_silver
assert 'target_table = f"{SILVER_SCHEMA}.{contract_table}"' in archive_silver
print("PASS ARCH-ETL-002 and LIVE-ETL-001 replace, rather than accumulate, the active month")

required_fields = {
    "cnt_offer_made",
    "unique_homes_offered",
    "estimated_weekly_cost",
    "first_action_date",
    "first_offer_date",
    "offer_accepted_date",
    "ipa_issued_date",
    "referral_closed_date",
    "last_activity_date",
    "first_provider_seen_date",
    "is_not_seen_by_providers",
    "ipa_placement_admission_date",
    "ipa_2_signatures",
    "ipa_last_signature_date",
    "ipa_due_diligence_min_review_date",
    "is_open",
    "is_awaiting_offer",
    "provider_assignment_count",
}
for field in required_fields:
    assert field in dq, f"Silver enrichment does not materialise {field}"
    assert field in gold, f"Gold does not expose {field}"
assert 'replace_silver_materialisation(referral_enrichment, "referral_enrichment")' in dq
assert "silver.referral_enrichment" in gold
assert "provider_submission_docs" in dq
assert "d.next_review_date > i.placement_admission_date" in dq
assert "activity_type <> 'ReferralCreated'" in dq
assert "'offer_successful'" in dq
assert "x.first_action_date, x.first_offer_date" in gold
assert "x.offer_accepted_date, x.ipa_issued_date" in gold
assert "x.referral_closed_date," in gold
assert "x.last_activity_date," in gold
fact_cell = next(
    cell for cell in read_notebook(GOLD)["cells"]
    if "CREATE OR REPLACE TABLE gold.fact_referral AS" in "".join(cell.get("source", []))
)
fact_source = "".join(fact_cell.get("source", []))
assert "offer_rollup AS" not in fact_source
assert "ipa_rollup AS" not in fact_source
assert "x.unique_homes_offered," in fact_source
assert "x.estimated_weekly_cost," in fact_source
print("PASS SI-018/SI-019 derived Silver enrichment and Gold promotion are present")

# GLD-009/GLD-011: the open and awaiting-offer flags implement the original
# business rules in Silver and are propagated, not recalculated, in Gold.
assert "latest_export AS" in dq
assert "MAX(TO_DATE(export_date)) AS latest_export_date" in dq
assert "live_provider AS" in dq
assert "engaged_provider AS" in dq
assert "'UNDER_OFFER'" in dq
assert "TO_DATE(r.response_required_by_date) >= le.latest_export_date" in dq
assert "is_open boolean, is_awaiting_offer boolean" in dq
assert "CROSS JOIN latest_export le" in dq
assert "COALESCE(is_open, false) AS is_open" in fact_source
assert "COALESCE(is_awaiting_offer, false) AS is_awaiting_offer" in fact_source
assert "x.is_open, x.is_awaiting_offer," in fact_source
# GLD-010: is_spot is restored to gold.fact_referral from silver.referral.
assert "CAST(r.is_spot AS BOOLEAN) AS is_spot" in fact_source
assert '"is_spot", "has_offer"' in gold
# GLD-012: is_engaged flags provider referrals that are not cancelled,
# closed or excluded.
provider_cell = next(
    cell for cell in read_notebook(GOLD)["cells"]
    if "CREATE OR REPLACE TABLE gold.fact_referral_provider AS" in "".join(cell.get("source", []))
)
provider_source = "".join(provider_cell.get("source", []))
assert "AS is_engaged" in provider_source
assert "NOT COALESCE(CAST(rp.is_cancelled AS BOOLEAN), false)" in provider_source
assert "NOT COALESCE(CAST(rp.is_closed AS BOOLEAN), false)" in provider_source
assert "NOT COALESCE(CAST(rp.is_excluded AS BOOLEAN), false)" in provider_source
print("PASS GLD-009/010/011/012 open, awaiting-offer, is_spot and is_engaged logic is present")

# GLD-013: semantic-model push-downs mined from SM WMPP v15. Referral-grain
# columns ride the Silver enrichment relation; offer-grain flags are computed
# in Gold with an IPA rollup join.
assert "COUNT(DISTINCT rp.provider_id) AS provider_assignment_count" in dq
assert "COALESCE(o.provider_assignment_count, 0) AS provider_assignment_count" in dq
assert "provider_assignment_count long" in dq
assert "x.provider_assignment_count," in fact_source
assert "COALESCE(provider_assignment_count, 0) AS provider_assignment_count" in fact_source
assert "AS is_emergency_placement" in fact_source
assert (
    "DATEDIFF(TO_DATE(required_placement_date), TO_DATE(referral_created_date)) = 0"
    in fact_source
)
assert "AS is_open_overdue" in fact_source
assert '"provider_assignment_count", "is_emergency_placement", "is_open_overdue",' in gold
assert '"signed_by_provider", "signed_by_local_authority",' in gold
offer_cell = next(
    cell for cell in read_notebook(GOLD)["cells"]
    if "CREATE OR REPLACE TABLE gold.fact_offer AS" in "".join(cell.get("source", []))
)
offer_source = "".join(offer_cell.get("source", []))
for offer_field in [
    "AS offer_age_days",
    "AS days_since_offer_activity",
    "AS is_draft_missing_dates",
    "AS is_draft_no_activity",
    "AS is_awaiting_ipa_creation",
    "AS is_ipa_pending",
    "AS is_ipa_completed",
    "has_completed_ipa",
    "signed_by_provider",
    "signed_by_local_authority",
]:
    assert offer_field in offer_source, f"gold.fact_offer does not publish {offer_field}"
print("PASS GLD-013 provider-count, emergency, overdue, draft-age and IPA flags are present")

for field in {
    "person_id",
    "referral_created_date",
    "required_placement_date",
    "first_action_date",
    "first_offer_date",
    "offer_accepted_date",
    "ipa_issued_date",
    "referral_closed_date",
    "referral_closure_reason",
    "current_status",
    "last_activity_date",
    "placement_type_required",
    "region",
    "priority",
    "complexity_band",
}:
    assert field in gold, f"Gold referral model does not expose {field}"
for gold_fact in [
    "CREATE OR REPLACE TABLE gold.fact_offer AS",
    "CREATE OR REPLACE TABLE gold.fct_ipa AS",
    "CREATE OR REPLACE TABLE gold.fact_referral_provider AS",
]:
    assert gold_fact in gold, f"missing source-grain Gold fact: {gold_fact}"
assert "actual_placement_start_date" in gold
assert "estimated_duration_weeks" in gold
print("PASS full fact_referral shape, snapshot promotion and Offer/IPA facts are present")

with DQ_CONFIG.open(encoding="utf-8-sig", newline="") as handle:
    dq_rules = list(csv.DictReader(handle))
enrichment_rules = [
    row for row in dq_rules if row["rule_id"].startswith("REFERRAL_ENRICHMENT_")
]
assert len(enrichment_rules) >= 7
assert {row["rule_type"] for row in enrichment_rules} >= {
    "UNIQUE", "NOT_NULL", "NON_NEGATIVE", "DATE_ORDER", "CONDITIONAL_NOT_NULL"
}
assert 'operator == ">="' in dq
assert "derived_dq_rules" in dq
assert "CONDITIONAL_NOT_NULL" in dq
assert "SIGNATURE_ON_OR_BEFORE_ADMISSION" in "\n".join(
    row["rule_id"] for row in enrichment_rules
)
assert "IPA_ADMISSION_ON_OR_AFTER_ISSUE" in "\n".join(
    row["rule_id"] for row in enrichment_rules
)
print("PASS enrichment DQ rules and bidirectional date-order support are configured")

for document in [ARCHITECTURE, REQUIREMENTS]:
    text = document.read_text(encoding="utf-8")
    assert "referral_enrichment" in text
    assert "snapshot" in text.lower()
assert "not a provider UI-view timestamp" in REQUIREMENTS.read_text(encoding="utf-8")
print("PASS architecture and requirements document the implemented contract and caveat")

print("VALIDATION PASSED")
