"""Static regression checks for the archive framework fallback."""

import ast
import json
import sys
from pathlib import Path


ROOT = (
    Path(sys.argv[1]).resolve()
    if len(sys.argv) == 2
    else Path(__file__).resolve().parents[1]
)
NOTEBOOK = ROOT / "02a_archive_silver 02 03.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
cells = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
source = "\n".join(cells)

for index, cell in enumerate(notebook["cells"]):
    code = "".join(cell.get("source", []))
    if cell.get("cell_type") == "code" and not code.lstrip().startswith("%"):
        ast.parse(code, filename=f"archive-silver:cell-{index}")
print("PASS notebook JSON and Python syntax")


def require(value, message):
    assert value in source, message


require(
    'FRAMEWORK_FALLBACK_PATH = "Files/deprecated_wmpp_files/framework.csv"',
    "missing controlled framework fallback path",
)
require("def read_framework_fallback(snapshot_date):", "missing fallback reader")
for option in [
    '.option("header", "true")',
    '.option("quote", \'"\')',
    '.option("escape", \'"\')',
    '.option("multiLine", "true")',
]:
    require(option, f"missing CSV option {option}")
require("if frame.rdd.isEmpty():", "empty fallback is not rejected")
require(
    '.withColumn("export_date", F.lit(snapshot_date).cast("timestamp"))',
    "fallback export_date is not the replay snapshot date",
)
for column in [
    '"_source_file"',
    '"_archive_fallback"',
    '"_ingestion_timestamp"',
    '"_ingestion_id"',
]:
    require(column, f"fallback is missing provenance {column}")
print("PASS fallback reader validates input and stamps monthly provenance")

require("framework_archive_present = any(", "missing archive-table detection")
require(
    "archive_logical_name(table) == normalise(FRAMEWORK_FALLBACK_TABLE)",
    "framework detection is not an exact logical-table match",
)
require("if not framework_archive_present:", "missing fallback-only registration")
require('"is_fallback_only": True', "fallback-only source is not marked")
require('"source_schema": "Files"', "fallback audit source is not truthful")
require(
    '"target_table": f"{SILVER_SCHEMA}.slv_{FRAMEWORK_FALLBACK_TABLE}"',
    "fallback target is not silver.slv_framework",
)
require(
    "if contract_key is None and is_framework_table:",
    "archived framework cannot use its temporary local contract",
)
require(
    '"fallback_path": (',
    "archived framework has no per-month fallback route",
)
print("PASS archived framework wins and fallback-only mode covers physical absence")

registration = source.index("if not framework_archive_present:")
ordering = source.index("source_tables = order_tables_by_dependency(source_tables)")
assert registration < ordering, "fallback is added after FK dependency ordering"
require(
    "bool(fallback_path) and archive_source_date is None",
    "fallback is not selected when a framework snapshot is unavailable",
)
require(
    "source_date = snapshot_date if use_fallback else archive_source_date",
    "fallback does not use the current canonical snapshot date",
)
require(
    "read_framework_fallback(snapshot_date)",
    "monthly materialisation does not invoke the fallback reader",
)
require(
    '.withColumn("_archive_fallback", F.lit(True))',
    "Silver output loses fallback provenance",
)
assert "saveAsTable(f\"{ARCHIVE_SCHEMA}.archived_framework\")" not in source
assert "saveAsTable(\"archived.archived_framework\")" not in source
print("PASS fallback enters normal Silver conformance without inventing archive data")

issue_log = (
    ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md"
).read_text(encoding="utf-8", errors="replace")
assert "SI-005" in issue_log, "ETL change log is missing SI-005"
print("PASS ETL change log records the fallback")

print("VALIDATION PASSED")
