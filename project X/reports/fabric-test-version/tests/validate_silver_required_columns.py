"""Regression checks for contract columns reaching Silver after a prior success."""

import csv
from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "configuration" / "schema_definition.csv"
NOTEBOOKS = [
    ROOT / "02_silver_formatter.py",
    ROOT / "02a_archive_silver.py",
]
COMMON_LIBRARY = ROOT / "99_common_library.py"
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
    notebook = read_notebook(notebook_path)
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
    # SI-025: the shared contract patch must guarantee export_date reaches
    # Silver even when the deployed contract table pre-dates those rows.
    assert "def ensure_export_date_contract" in common_text, (
        "Common library lacks the SI-025 export_date contract guard"
    )
    assert 'spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")' in common_text, (
        "Common library lacks the Spark 3 Parquet ancient-datetime write policy"
    )

    for notebook in NOTEBOOKS:
        text = source(notebook)
        assert "%run ./99_common_library" in text, (
            f"{notebook.name} does not import the target-schema refresh guard"
        )
        assert "ensure_export_date_contract(" in text, (
            f"{notebook.name} can write Silver without the SI-025 export_date guarantee"
        )
        if notebook.name.startswith("02_silver_formatter"):
            assert "should_skip(" in text and "not target_requires_refresh" in text, (
                f"{notebook.name} can skip a successful load without checking the target schema"
            )
            assert "ensure_export_date_contract(contracts[contract_key])" in text, (
                "Active formatter can drop export_date from a stale control-table contract"
            )
            assert '"yyyy-MM-dd"' in text, (
                "Active formatter cannot parse date-only Bronze export_date values"
            )
        else:
            assert "stale_targets" in text and "not stale_targets" in text, (
                f"{notebook.name} can skip a successful month without checking target schemas"
            )
            assert "complete_framework_schema" in text, (
                f"{notebook.name} can write an incomplete framework target from a stale contract"
            )
            assert "parsed_archive_export_timestamp" in text, (
                "Active archive formatter cannot select legacy export_date values"
            )
        assert "schema_cols" in text and "format_frame" in text, (
            f"{notebook.name} does not project the contract columns through format_frame"
        )
        print(f"PASS {notebook.name} refreshes a stale Silver schema")

    print("PASS active formatters retain and parse referral export_date")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
