"""Static regression checks for Bronze drift contracts, Gold dimensions and runbooks."""

from __future__ import annotations

import ast
import csv
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "project X"

EXPECTED_CONTRACTS = {
    "mlv_additional_fee": {
        "additional_fee_id", "offer_id", "fee_title", "number_of_hours",
        "other_fee_title", "fee_frequency", "rate", "export_date",
    },
    "provider_sic_codes": {"provider_id", "sic_code", "export_date"},
    "provider_submission_docs": {
        "document_id", "submission_id", "s3_file_metadata_id", "document_name",
        "document_type", "expiry_date", "last_updated", "next_review_date",
        "service_type", "home_id", "start_date", "export_date",
    },
    "ref_kpi_definition": {
        "KPI ID", "KPI Description", "Calculation", "PBI Measure", "Section",
        "Tables", "ref FR IDs", "ref FR IDs Description", "export_date",
    },
    "ref_kpi_rid_linkage": {"KPI ID", "Req ID", "export_date"},
    "ref_rid": {
        "Req ID", "Oiriginal ID", "Priority", "Requirement", "Stakeholder",
        "Status", "KPI_s_", "export_date",
    },
    "ref_table_lineage": {
        "Schema Definition Table", "Silver Source", "Gold Table", "Functional Area",
        "export_date",
    },
    "referral_person_support_needs": {"person_id", "support_need", "export_date"},
}


def notebook_source(path: Path) -> str:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4, f"{path.name} is not Notebook 4"
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        source = "".join(cell.get("source", []))
        if source.lstrip().startswith(("%run", "%%sql")):
            continue
        ast.parse(source)
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


with (PROJECT / "configuration" / "schema_definition.csv").open(
    newline="", encoding="utf-8-sig"
) as handle:
    contract_rows = list(csv.DictReader(handle))

by_table: dict[str, list[dict[str, str]]] = {}
for row in contract_rows:
    by_table.setdefault(row["table_name"], []).append(row)

for table_name, expected_columns in EXPECTED_CONTRACTS.items():
    rows = by_table.get(table_name, [])
    assert rows, f"Missing Bronze drift contract for {table_name}"
    actual_columns = {row["column_name"] for row in rows}
    assert actual_columns == expected_columns, (
        f"{table_name} contract mismatch: expected={expected_columns}, actual={actual_columns}"
    )
    export_row = next(row for row in rows if row["column_name"] == "export_date")
    assert export_row["data_type"] == "timestamp without time zone"

assert next(
    row for row in by_table["provider_submission_docs"] if row["column_name"] == "document_id"
)["is_primary_key"] == "YES"
assert next(
    row for row in by_table["provider_sic_codes"] if row["column_name"] == "provider_id"
)["referenced_table"] == "provider"

archive_loader = PROJECT / "00_archive_load.ipynb"
assert archive_loader.exists(), "Renamed archive loader is missing"
assert not (PROJECT / "00_archive_load 02 03.ipynb").exists(), "Retired archive loader remains active"
archive_source = notebook_source(archive_loader)
assert "TABLE_PREFIX" not in archive_source
assert 'return safe_name' in archive_source
assert 'target_object = f"{ARCHIVE_SCHEMA}.{physical_table}"' in archive_source

archive_silver_source = notebook_source(PROJECT / "02a_archive_silver.ipynb")
assert "ARCHIVE_PREFIXES" not in archive_silver_source
assert 'EXCLUDED_ARCHIVE_TABLES = {"audit"}' in archive_silver_source
assert 'resolve_contract(archive_logical_name(physical_table), ())' in archive_silver_source
assert "source_named_logicals" in archive_silver_source
assert "legacy_shadowed_tables" in archive_silver_source
assert "RUN_GOLD_DIMENSIONS_AT_MONTH_END = True" in archive_silver_source
assert 'GOLD_DIMENSIONS_NOTEBOOK_NAME = "05_gold_dimensions"' in archive_silver_source

dimension_source = notebook_source(PROJECT / "05_gold_dimensions.ipynb")
for required in (
    ".dim_date", ".dim_provider", ".dim_provider_home",
    ".dim_framework", ".dim_framework_category",
    ".dim_provider_submission_document", ".bridge_provider_sic_code",
):
    assert required in dimension_source, f"Missing Gold dimension target: {required}"
assert "silver.slv_provider_submission_docs" in dimension_source
assert "silver.slv_provider_sic_codes" in dimension_source

live_source = notebook_source(PROJECT / "90_run_live_pipeline.ipynb")
expected_live_order = [
    "00_setup_cfg", "01_bronze_get_latest",
    "01a_cfg_schema_capture_live", "02_silver_formatter",
    "03_silver_business_rules", "04_gold_model", "05_gold_dimensions",
]
positions = [live_source.index(name) for name in expected_live_order]
assert positions == sorted(positions), "Live runner order is incorrect"

archive_runbook = PROJECT / "client documentation" / "05_Operations_and_Runbooks" / "ARCHIVE_PIPELINE_RUNBOOK.md"
assert archive_runbook.exists(), "Archive runbook is missing"
assert "00_archive_load.ipynb" in archive_runbook.read_text(encoding="utf-8")

field_status = PROJECT / "client documentation" / "Supplementary" / "ETL_FIELD_IMPLEMENTATION_STATUS.md"
assert field_status.exists(), "Supplementary field implementation status is missing"
assert "Not source-backed yet" in field_status.read_text(encoding="utf-8")

print("Schema drift contracts, Gold dimensions, archive rename and runbook checks passed.")
