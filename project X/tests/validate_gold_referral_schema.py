"""Static regression checks for SI-006 Gold referral schema alignment."""

import ast
import csv
import json
import re
import sys
from pathlib import Path


ROOT = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2
    else Path(__file__).resolve().parents[1]
)
NOTEBOOK = ROOT / "04_gold_model.ipynb"
SCHEMA = ROOT / "configuration" / "schema_definition.csv"


notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8-sig"))
cells = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
source = "\n".join(cells)
for index, cell in enumerate(notebook["cells"]):
    code = "".join(cell.get("source", []))
    if cell.get("cell_type") == "code" and not code.lstrip().startswith("%"):
        ast.parse(code, filename=f"gold-model:cell-{index}")
print("PASS notebook JSON and Python syntax")


with SCHEMA.open("r", encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))
referral = {
    row["column_name"].lower(): row
    for row in rows
    if row["table_name"].lower() == "referral"
}

required_contract = {
    "placement_type": "2",
    "referral_created_date": "13",
    "referral_modified_date": "14",
    "referral_created_by": "16",
    "referral_updated_by": "17",
    "referral_status": "18",
    "export_date": "19",
}
for column, ordinal in required_contract.items():
    assert column in referral, f"referral contract is missing {column}"
    assert referral[column]["ordinal_position"] == ordinal, (
        f"{column} has ordinal {referral[column]['ordinal_position']}, expected {ordinal}"
    )
assert referral["referral_created_date"]["data_type"] == "timestamp without time zone"
assert referral["referral_modified_date"]["data_type"] == "timestamp without time zone"
print("PASS referral contract retains the six captured live fields with approved ordinals")


fact_cell = next(cell for cell in cells if "CREATE OR REPLACE VIEW gold.fact_referral AS" in cell)
for required_name in [
    "referral_created_date",
    "referral_modified_date",
    "referral_status",
    "placement_type",
]:
    assert required_name in fact_cell, f"Gold mapping does not use {required_name}"

stale_patterns = {
    "old history ordering": r"ORDER\s+BY\s+COALESCE\s*\(\s*modified_timestamp\s*,\s*created_timestamp",
    "old referral creation field": r"MIN\s*\(\s*created_timestamp\s*\)\s+AS\s+ReferralCreatedDate",
    "old referral modification field": r"\br\.modified_timestamp\b",
    "old referral status field": r"\br\.status\b",
    "old referral placement field": r"\br\.placement_type_code\b",
    "audit revision field on current referral": r"\brev\s+DESC",
}
for label, pattern in stale_patterns.items():
    assert not re.search(pattern, fact_cell, re.IGNORECASE), label
print("PASS fact_referral uses current referral extract names, not audit-table names")


assert "GOLD_SOURCE_REQUIREMENTS" in source, "missing Gold source preflight"
for source_table in [
    "silver.referral",
    "silver.offer",
    "silver.referral_provider",
    "silver.ipa",
    "silver.referral_lifecycle_event",
]:
    assert source_table in source, f"preflight does not cover {source_table}"
assert "Gold source validation failed" in source
print("PASS Gold fails early with one actionable source-schema message")

assert 'EVENT_ROLLUP_SOURCE = "silver.referral_lifecycle_event"' in source
assert "source-system referral-event audit log" in source
assert "referral_event_log" not in source
assert "FROM {EVENT_ROLLUP_SOURCE}" in source
assert "SELECT * FROM silver.referral_enrichment" in fact_cell
assert "x.first_action_date AS FirstActionDate" in fact_cell
print("PASS Gold exposes lifecycle events separately and promotes derived referral dates from Silver")


issue_log = (
    ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md"
).read_text(encoding="utf-8", errors="replace")
assert "## SI-006" in issue_log
assert "referral_modified_date" in issue_log
assert "validate_gold_referral_schema.py" in issue_log
print("PASS change log records SI-006 and its validation")


simulation = (ROOT / "tests" / "_gold_sim_test.py").read_text(encoding="utf-8")
ast.parse(simulation, filename="_gold_sim_test.py")
fixture_sql = (ROOT / "tests" / "_gold_fact_sql.sql").read_text(encoding="utf-8")
assert not any(line.startswith("+") for line in fixture_sql.splitlines()), (
    "simulation SQL contains a patch-marker character"
)
assert 'write(mkdf(referrals), "referral")' in simulation
assert "referral_aud" not in simulation
for required_name in [
    "referral_created_date",
    "referral_modified_date",
    "referral_status",
    "placement_type",
]:
    assert required_name in simulation, f"simulation does not fabricate {required_name}"
    assert required_name in fixture_sql, f"simulation SQL does not use {required_name}"
for label, pattern in stale_patterns.items():
    assert not re.search(pattern, fixture_sql, re.IGNORECASE), f"simulation SQL: {label}"
assert "FROM silver.referral" in fixture_sql
assert "FROM silver.referral_aud" not in fixture_sql
print("PASS Spark simulation fixture mirrors the production flattened referral model")

print("VALIDATION PASSED")
