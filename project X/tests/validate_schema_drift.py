import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def notebook_source(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


with (ROOT / "configuration" / "schema_definition.csv").open(encoding="utf-8-sig", newline="") as handle:
    reader = csv.DictReader(handle)
    rows = list(reader)
    fields = reader.fieldnames or []

check("schema_name" not in fields, "schema_definition.csv still contains schema_name")
check(len(rows) > 0, "schema_definition.csv has no rows")
check(
    len({(row["table_name"].lower(), row["column_name"].lower()) for row in rows}) == len(rows),
    "schema_definition.csv contains duplicate table/column definitions",
)

contract_consumers = [
    "01a_cfg_schema_capture_live.ipynb",
    "01a_cfg_schema_capture_archive.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
    "03_silver_business_rules.ipynb",
]
for name in contract_consumers:
    source = notebook_source(name)
    check('row["schema_name"]' not in source, f"{name} still indexes schema_name")
    check('row.get("schema_name")' not in source, f"{name} still reads schema_name")

live_source = notebook_source("01a_cfg_schema_capture_live.ipynb")
common_source = notebook_source("99_common_library.ipynb")
check(
    "def etl_logical_table_name" in common_source,
    "common library does not define etl_logical_table_name",
)
check(
    "logical_table = etl_logical_table_name(table.name)" in live_source,
    "live schema capture does not call the common etl_logical_table_name helper",
)
check(
    "logical_table = logical_table_name(table.name)" not in live_source,
    "live schema capture still calls the retired logical_table_name helper",
)
for required in [
    "monitoring.cfg_schema_drift_definition",
    "monitoring.cfg_schema_drift_event",
    "monitoring.cfg_schema_definition_candidate",
    "COLUMN_ADDED",
    "COLUMN_REMOVED",
    "TABLE_ADDED",
    "TABLE_REMOVED",
    "FK_TARGET_TABLE_MISSING",
    "FK_TARGET_COLUMN_MISSING",
    "whenMatchedUpdate",
]:
    check(required in live_source, f"daily live capture is missing {required}")

setup_source = notebook_source("00_setup_cfg.ipynb")
check(
    "monitoring.cfg_schema_drift_definition" in setup_source,
    "00_setup_cfg does not deploy cfg_schema_drift_definition",
)

dq_source = notebook_source("03_silver_business_rules.ipynb")
for guard in [
    "Missing Silver source table",
    "Missing Silver column(s)",
    "Missing Silver parent table",
    "Missing Silver parent column",
]:
    check(guard in dq_source, f"03_silver_business_rules lost SKIPPED guard: {guard}")

archive_source = notebook_source("01a_cfg_schema_capture_archive.ipynb")
check('COMPARED_SCHEMA = "Bronze"' in archive_source, "archive capture was not restored")
check("ARCHIVE_TABLE_PREFIX" not in archive_source, "archive capture still has the unwanted rewrite")
check('StructField("schema_name"' not in archive_source, "archive capture still stores schema_name")

for name in ["02_silver_formatter.ipynb", "02a_archive_silver.ipynb"]:
    source = notebook_source(name)
    check("actual_type string" in source, f"{name} still writes the legacy drift-event shape")
    check("drift_event_row" in source, f"{name} has no expanded drift-event row builder")

if failures:
    print("VALIDATION FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("VALIDATION PASSED")
