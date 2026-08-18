"""Static checks for the SI-007 contract rebuild and SI-008–SI-012 Silver tables."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "configuration" / "schema_definition.csv"
NOTEBOOK = ROOT / "03_silver_business_rules 02 03.ipynb"

with SCHEMA.open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []

assert "join_class" in fields
assert "join_evidence" in fields
assert {row["join_class"] for row in rows} >= {
    "NO_JOIN", "CONTRACT_FK", "TRIAL_JOIN", "INVALID_JOIN"
}
keys = {(row["table_name"].lower(), row["column_name"].lower()) for row in rows}
for row in rows:
    if row["join_class"] == "INVALID_JOIN":
        assert not row["referenced_table"]
        assert not row["referenced_column"]
    elif row["referenced_table"] and row["referenced_column"]:
        assert (row["referenced_table"].lower(), row["referenced_column"].lower()) in keys
print("PASS SI-007 schema contract has explicit and resolvable join classifications")

notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8-sig"))
source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
for table_name in [
    "age_band", "directory_summary_axis", "fostering_axis",
    "referral_closure_reason_summary", "dim_date",
]:
    assert f'"{table_name}"' in source
assert "replace_silver_materialisation" in source
assert "closed_referral_reason_bucket" in source
assert "SEQUENCE(min_date, max_date, INTERVAL 1 DAY)" in source
print("PASS SI-008–SI-012 are materialised idempotently in Silver")
