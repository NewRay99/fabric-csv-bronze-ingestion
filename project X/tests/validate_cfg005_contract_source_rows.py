"""Regression checks for CFG-005 contract CSV row retention."""

import ast
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_CSV = ROOT / "configuration" / "schema_definition.csv"
DQ_RULE_CSV = ROOT / "configuration" / "dq_rule_definition.csv"
SETUP_NOTEBOOK = ROOT / "00_setup_cfg.ipynb"

with CONTRACT_CSV.open(encoding="utf-8-sig", newline="") as handle:
    raw_rows = list(csv.reader(handle))

assert raw_rows, "schema_definition.csv is empty"
header = raw_rows[0]
assert {"table_name", "ordinal_position", "column_name", "data_type"} <= set(header)
assert all(len(row) == len(header) for row in raw_rows[1:]), (
    "schema_definition.csv contains a malformed row that a CSV reader could drop or shift"
)

with CONTRACT_CSV.open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert len(rows) == len(raw_rows) - 1, "CSV records were lost while parsing"
print(f"PASS schema-contract source contains {len(rows):,} rows")

with DQ_RULE_CSV.open(encoding="utf-8-sig", newline="") as handle:
    dq_raw_rows = list(csv.reader(handle))
assert dq_raw_rows, "dq_rule_definition.csv is empty"
dq_header = dq_raw_rows[0]
assert {"rule_id", "active", "severity", "rule_type"} <= set(dq_header)
assert all(len(row) == len(dq_header) for row in dq_raw_rows[1:]), (
    "dq_rule_definition.csv contains a malformed row that a CSV reader could drop or shift"
)
with DQ_RULE_CSV.open(encoding="utf-8-sig", newline="") as handle:
    dq_rows = list(csv.DictReader(handle))
assert len(dq_rows) == len(dq_raw_rows) - 1, "DQ CSV records were lost while parsing"
print(f"PASS DQ-rule source contains {len(dq_rows):,} rows")

notebook = json.loads(SETUP_NOTEBOOK.read_text(encoding="utf-8-sig"))
sources = [
    "".join(cell.get("source", []))
    for cell in notebook["cells"]
    if cell.get("cell_type") == "code"
]
for index, source in enumerate(sources):
    if source.strip() and not source.lstrip().startswith("%"):
        ast.parse(source, filename=f"00_setup_cfg.ipynb:cell-{index}")

bootstrap_source = next(
    source for source in sources if "def bootstrap_csv_table(" in source
)
assert "frame = (spark.read.format(\"csv\")" in bootstrap_source
assert ".option(\"header\", \"true\")" in bootstrap_source
assert ".option(\"quote\", '\"')" in bootstrap_source
assert ".option(\"escape\", '\"')" in bootstrap_source
assert ".option(\"multiLine\", \"true\")" in bootstrap_source
assert '.option("lineSep", "\\n")' in bootstrap_source, (
    "00_setup_cfg does not pin LF for mixed-line-ending contract CSV files"
)
assert ".where(" not in bootstrap_source and ".filter(" not in bootstrap_source, (
    "00_setup_cfg filters CSV rows before writing the contract"
)
assert ".mode(\"overwrite\")" in bootstrap_source
assert ".saveAsTable(target_table)" in bootstrap_source
assert "def validate_csv_target_parity(csv_path, target_table, required_columns):" in bootstrap_source
assert "source_count = source.count()" in bootstrap_source
assert "target_count = target.count()" in bootstrap_source
assert "if source_count != target_count" in bootstrap_source
assert "if LOAD_FILE_CONFIG:" in bootstrap_source
assert "validate_csv_target_parity(\n        SCHEMA_CONTRACT_CSV_PATH,\n        \"monitoring.cfg_schema_contract_column\"" in bootstrap_source
assert "validate_csv_target_parity(\n        DQ_RULE_CSV_PATH,\n        \"monitoring.cfg_data_quality_rule\"" in bootstrap_source
print("PASS setup compares each source CSV row count with its target table")

# Reproduce the exact Spark reader used by setup when PySpark is available.
# This catches the mixed-line-ending regression that a Python CSV parser alone
# cannot reveal.
try:
    from pyspark.sql import SparkSession
except ImportError:
    print("SKIP Spark parser regression check: PySpark is unavailable")
else:
    spark = SparkSession.builder.master("local[1]").appName(
        "validate-cfg005-contract-rows"
    ).getOrCreate()
    try:
        spark_rows = (
            spark.read.format("csv").option("header", "true")
            .option("quote", '"').option("escape", '"')
            .option("multiLine", "true").option("lineSep", "\n")
            .load(str(CONTRACT_CSV))
        )
        assert spark_rows.count() == len(rows), (
            "Spark CSV reader excluded or created contract rows"
        )
        spark_dq_rows = (
            spark.read.format("csv").option("header", "true")
            .option("quote", '"').option("escape", '"')
            .option("multiLine", "true").option("lineSep", "\n")
            .load(str(DQ_RULE_CSV))
        )
        assert spark_dq_rows.count() == len(dq_rows), (
            "Spark CSV reader excluded or created DQ-rule rows"
        )
    finally:
        spark.stop()
    print("PASS Spark CSV parser retains every schema-contract and DQ-rule row")

print("VALIDATION PASSED")
