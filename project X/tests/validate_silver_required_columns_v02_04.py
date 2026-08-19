"""Regression checks for contract columns reaching Silver after a prior success."""

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "project X" / "configuration" / "schema_definition.csv"
NOTEBOOKS = [
    ROOT / "project X" / "02_silver_formatter 02 03.ipynb",
    ROOT / "project X" / "02a_archive_silver 02 03.ipynb",
]
COMMON_LIBRARY = ROOT / "project X" / "99_common_library 02 03.ipynb"
REQUIRED_REFERRAL = {
    "referral_id",
    "placement_type",
    "required_start_date",
    "response_required_by_date",
    "referral_created_date",
    "referral_modified_date",
    "referral_status",
    "export_date",
}


def source(notebook_path):
    notebook = json.loads(notebook_path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def main():
    with CONTRACT.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    referral = {row["column_name"] for row in rows if row["table_name"].lower() == "referral"}
    missing_contract = REQUIRED_REFERRAL - referral
    assert not missing_contract, f"Referral contract lost Gold-required columns: {sorted(missing_contract)}"
    print("PASS schema contract retains all Gold-required referral columns")

    common_text = source(COMMON_LIBRARY)
    assert "def target_requires_refresh" in common_text, (
        "Common library lacks the target-schema refresh guard"
    )

    for notebook in NOTEBOOKS:
        text = source(notebook)
        assert "%run ./99_common_library 02 03" in text, (
            f"{notebook.name} does not import the target-schema refresh guard"
        )
        if notebook.name.startswith("02_silver_formatter"):
            assert "if should_skip(" in text and "not target_requires_refresh" in text, (
                f"{notebook.name} can skip a successful load without checking the target schema"
            )
        else:
            assert "stale_targets" in text and "not stale_targets" in text, (
                f"{notebook.name} can skip a successful month without checking target schemas"
            )
        assert "schema_cols" in text and "format_frame" in text, (
            f"{notebook.name} does not project the contract columns through format_frame"
        )
        print(f"PASS {notebook.name} refreshes a stale Silver schema")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
