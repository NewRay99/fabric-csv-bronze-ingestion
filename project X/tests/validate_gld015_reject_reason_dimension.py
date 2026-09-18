"""Regression checks for GLD-015 closure-reason cleaning and sequencing."""

from notebook_loader import load_notebook as read_notebook
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = (
    ROOT / "05_gold_dimensions.py",
    ROOT / "reports" / "current" / "WMPP" / "notebooks"
    / "05_gold_dimensions.Notebook" / "notebook-content.py",
)


def source(path):
    notebook = read_notebook(path)
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


for notebook in NOTEBOOKS:
    text = source(notebook)
    assert "rejection" not in text.lower(), (
        f"{notebook.name} still uses rejection terminology internally"
    )
    for expected in (
        "closure_reason_clean",
        "closure_reason_grouped",
        "closed_referral_reason_bucket",
        "sequence_order",
        "PARTITION BY referral_provider_id",
        "ORDER BY created_date DESC NULLS LAST,",
        "source_export_date DESC NULLS LAST,",
        "reject_reason_id DESC",
        "= 'test'",
        "THEN CAST(NULL AS STRING)",
        "CONTAINSSTRING",
    ):
        # SQL uses LIKE rather than DAX CONTAINSSTRING; the exception below
        # makes that translation explicit while still rejecting copied DAX.
        if expected == "CONTAINSSTRING":
            assert expected not in text, f"{notebook.name} contains untranslatable DAX"
            continue
        assert expected in text, f"{notebook.name} is missing GLD-015 contract: {expected}"
    for expected in (
        "LIKE '%location%'",
        "LIKE '%off portal%'",
        "LIKE '%not on the portal%'",
        "LIKE '%doesn''t have access%'",
        "LIKE '%placed%'",
        "LIKE '%moved%'",
        "LIKE '%case closed%'",
        "LIKE '%remove%'",
        "LIKE '%update%'",
        "LIKE '%email%'",
        "LIKE '%portal not working%'",
    ):
        assert expected in text, f"{notebook.name} is missing GLD-015 grouping: {expected}"
    assert "PARTITION BY reject_reason_id" in text, (
        f"{notebook.name} no longer deduplicates repeated source snapshots"
    )

issue_log = (ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md").read_text(
    encoding="utf-8"
)
assert "## GLD-015" in issue_log
assert "**Status:** resolved" in issue_log.split("## GLD-015", 1)[1]
print("PASS GLD-015 cleans, groups and sequences provider closure reasons")
