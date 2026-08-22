"""Regression checks for SI-022 source-schema fields retained into Silver."""

import csv
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "configuration" / "schema_definition.csv"
CANDIDATE = ROOT / "configuration" / "cfg_tables" / "cfg_schema_definition_candidate.csv"
ISSUE_LOG = ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


contract_rows = read_csv(CONTRACT)
candidate_rows = read_csv(CANDIDATE)
contract_columns = {
    (row["table_name"].lower(), row["column_name"].lower())
    for row in contract_rows
}
candidate_columns = {
    (row["table_name"].lower(), row["column_name"].lower())
    for row in candidate_rows
}

missing_from_contract = sorted(candidate_columns - contract_columns)
assert not missing_from_contract, (
    "Supplied source-schema fields would be dropped before Silver: "
    f"{missing_from_contract}"
)

expected_fields = {
    "framework": {"framework_name", "start_date", "end_date", "placement_type"},
    "offer": {"withdraw_reason_other"},
    "provider_education_provision": {"updated_by"},
    "provider_home": {"status"},
    "referral_provider": {"created_date", "modified_date"},
    "referral_provider_message": {"message_read_by", "message_read_timestamp"},
    "referral_spot_category": {"spot_category"},
}
by_table: dict[str, set[str]] = defaultdict(set)
for table_name, column_name in contract_columns:
    by_table[table_name].add(column_name)
for table_name, expected in expected_fields.items():
    assert expected <= by_table[table_name], (
        f"{table_name} is missing source-backed Silver fields: "
        f"{sorted(expected - by_table[table_name])}"
    )

for table_name in expected_fields:
    ordinals = [
        row["ordinal_position"]
        for row in contract_rows
        if row["table_name"].lower() == table_name
    ]
    assert len(ordinals) == len(set(ordinals)), (
        f"{table_name} contract has duplicate ordinal positions"
    )

issue_log = ISSUE_LOG.read_text(encoding="utf-8")
assert "## SI-022" in issue_log
assert "cfg_schema_definition_candidate" in issue_log
assert "LOAD_FILE_CONFIG = True" in issue_log

print("VALIDATION PASSED")
