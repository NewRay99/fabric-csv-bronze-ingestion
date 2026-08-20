"""Static regression checks for the Version 01 Fabric notebooks and contracts."""

import ast
import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_NAMES = [
    "00_archive_load.ipynb",
    "00a_rehydrate_archive_cfg.ipynb",
    "01_bronze_get_latest.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
    "03_silver_business_rules.ipynb",
    "04_gold_model.ipynb",
]
SILVER_NOTEBOOKS = [
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
]
REQUIRED_FRACTIONAL_FORMATS = {
    "yyyy-MM-dd",
    "yyyy-MM-dd HH:mm:ss.S",
    "yyyy-MM-dd HH:mm:ss.SSS",
    "yyyy-MM-dd HH:mm:ss.SSSSSS",
}


def notebook_source(notebook):
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def parameter_assignments(notebook):
    tree = ast.parse("".join(notebook["cells"][1]["source"]))
    result = {}
    for node in tree.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                pass
    return result


notebooks = {}
for name in NOTEBOOK_NAMES:
    path = ROOT / name
    notebook = json.loads(path.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4, f"{name}: expected Notebook format 4"
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and not source.lstrip().startswith("%"):
            ast.parse(source, filename=f"{name}:cell-{index}")
    notebooks[name] = notebook
    print(f"PASS notebook JSON/Python: {name}")

for name in SILVER_NOTEBOOKS:
    notebook = notebooks[name]
    parameters = parameter_assignments(notebook)
    formats = (set(parameters.get("TIMESTAMP_FORMATS", []))
               | set(parameters.get("DATE_FORMATS", [])))
    assert parameters.get("TIME_PARSER_POLICY") == "CORRECTED", (
        f"{name}: Spark corrected time parser policy is required"
    )
    assert REQUIRED_FRACTIONAL_FORMATS.issubset(formats), (
        f"{name}: missing fractional timestamp formats"
    )
    assert 'spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)' in notebook_source(notebook)
    print(f"PASS fractional timestamp regression: {name}")

archive_source = notebook_source(notebooks["02a_archive_silver.ipynb"])
assert "month_end_dates = sorted(month_last_dates.values())" in archive_source
assert "for snapshot_date in month_end_dates:" in archive_source
assert "for batch_date in batch_dates:" not in archive_source
assert "spark.table(source_table).where(" in archive_source
assert 'F.to_date("export_date") == F.lit(source_date)' in archive_source
common_notebook = json.loads(
    (ROOT / "99_common_library.ipynb").read_text(encoding="utf-8")
)
common_source = notebook_source(common_notebook)
assert "deduplicate_frame(raw_frame, schema_cols)" in archive_source
assert "F.row_number().over(window)" in common_source
assert "latest_table_export(" in archive_source
assert "formatted_export_non_null != written" in archive_source
assert 'GOLD_NOTEBOOK_NAME' in archive_source and '"AS_OF_DATE": snapshot_date.isoformat()' in archive_source
assert 'SOURCE_KIND = "ARCHIVE_MONTH_END"' in archive_source
assert "VERBOSE_DIAGNOSTICS = True" in archive_source
assert "Primary-key sample" in common_source
assert "Silver export_date" in common_source
assert "TARGET CHECK" in archive_source
print(
    "PASS archive strategy: month-end-only batches, PK deduplication, "
    "date gate, diagnostics, and Gold hand-off"
)

with (ROOT / "configuration" / "schema_definition.csv").open(encoding="utf-8-sig", newline="") as handle:
    rows = list(csv.DictReader(handle))

tables = {}
for row in rows:
    tables.setdefault(row["table_name"], []).append(row)

assert len(tables) == 39, f"Expected 39 observed table contracts, found {len(tables)}"
assert {row["join_class"] for row in rows} >= {"NO_JOIN", "CONTRACT_FK", "TRIAL_JOIN", "INVALID_JOIN"}
for table_name, definitions in tables.items():
    ordinals = [int(row["ordinal_position"]) for row in definitions]
    assert len(ordinals) == len(set(ordinals)), f"{table_name}: duplicate ordinal"
    export_rows = [row for row in definitions if row["column_name"] == "export_date"]
    assert len(export_rows) == 1, f"{table_name}: expected one export_date"
    assert export_rows[0]["data_type"].lower() == "timestamp without time zone"

expected_columns = {
    "framework_category": {
        "framework_category_id", "category_name", "framework_code", "export_date",
    },
    "ipa_child_support_needs": {"ipa_child_id", "support_need", "export_date"},
}
for table_name, columns in expected_columns.items():
    assert table_name in tables, f"Missing contract: {table_name}"
    assert {row["column_name"] for row in tables[table_name]} == columns

support_key = {
    row["column_name"] for row in tables["ipa_child_support_needs"]
    if row["is_primary_key"].upper() == "YES"
}
assert support_key == {"ipa_child_id", "support_need"}

print("PASS schema contracts: observed tables, unique ordinals, one export_date each")
print("PASS archive regression contracts: framework_category, ipa_child_support_needs")
