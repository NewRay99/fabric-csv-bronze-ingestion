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
DEPLOYED_NOTEBOOK = ROOT / "reports" / "current" / "WMPP" / "notebooks" / "02_silver_formatter.Notebook" / "notebook-content.py"
DEPLOYED_ARCHIVE_NOTEBOOK = ROOT / "reports" / "current" / "WMPP" / "notebooks" / "02a_archive_silver.Notebook" / "notebook-content.py"
DEPLOYED_COMMON_LIBRARY = ROOT / "reports" / "current" / "WMPP" / "notebooks" / "99_common_library.Notebook" / "notebook-content.py"
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
        else:
            assert "stale_targets" in text and "not stale_targets" in text, (
                f"{notebook.name} can skip a successful month without checking target schemas"
            )
            assert "complete_framework_schema" in text, (
                f"{notebook.name} can write an incomplete framework target from a stale contract"
            )
        assert "schema_cols" in text and "format_frame" in text, (
            f"{notebook.name} does not project the contract columns through format_frame"
        )
        print(f"PASS {notebook.name} refreshes a stale Silver schema")

    deployed_text = source(DEPLOYED_NOTEBOOK)
    deployed_archive_text = source(DEPLOYED_ARCHIVE_NOTEBOOK)
    deployed_common_text = source(DEPLOYED_COMMON_LIBRARY)
    assert "def ensure_export_date_contract" in deployed_common_text, (
        "Deployed WMPP common library lacks the SI-025 export_date contract guard"
    )
    assert 'spark.conf.set("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")' in deployed_common_text, (
        "Deployed WMPP common library lacks the Spark 3 Parquet ancient-datetime write policy"
    )
    assert "ensure_export_date_contract(contracts[contract_key])" in deployed_text, (
        "Deployed WMPP formatter can drop export_date from a stale control-table contract"
    )
    assert '"yyyy-MM-dd"' in deployed_text, (
        "Deployed WMPP formatter cannot parse date-only Bronze export_date values"
    )
    assert "ensure_export_date_contract(" in deployed_archive_text, (
        "Deployed WMPP archive formatter can drop export_date from a stale control-table contract"
    )
    assert "parsed_archive_export_timestamp" in deployed_archive_text, (
        "Deployed WMPP archive formatter cannot select legacy export_date values"
    )
    print("PASS deployed WMPP formatter retains and parses referral export_date")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
