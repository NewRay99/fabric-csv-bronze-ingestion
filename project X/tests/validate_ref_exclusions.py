import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def notebook_source(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and not source.lstrip().startswith("%"):
            try:
                ast.parse(source, filename=f"{name}:cell-{index}")
            except SyntaxError as exc:
                failures.append(f"{name}:cell-{index} syntax error: {exc}")
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


common_path = ROOT / "common_util.ipynb"
check(common_path.exists(), "common_util.ipynb does not exist")
common_source = notebook_source("common_util.ipynb") if common_path.exists() else ""

for table in [
    "ref_KPI_Definition",
    "ref_KPI_RID_linkage",
    "ref_RID",
    "ref_Table_Lineage",
]:
    check(table in common_source, f"common_util is missing explicit exclusion {table}")
check('ETL_EXCLUDED_TABLE_PREFIXES = ["ref_"]' in common_source, "common_util is missing ref_ prefix exclusion")
check("def is_etl_excluded_table" in common_source, "common_util is missing exclusion helper")

consumers = [
    "00_archive_load.ipynb",
    "01_bronze_get_latest.ipynb",
    "01a_cfg_schema_capture_live.ipynb",
    "01a_cfg_schema_capture_archive.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
]
for name in consumers:
    source = notebook_source(name)
    check(
        "%run ./99_common_library" in source,
        f"{name} does not reference the shared common library",
    )
    check("is_etl_excluded_table" in source, f"{name} does not apply the shared exclusion")

latest_source = notebook_source("02_silver_formatter.ipynb")
check(
    latest_source.find("is_etl_excluded_table") < latest_source.find("for physical_table in physical_tables"),
    "latest Silver exclusion is not applied before the processing loop",
)
check("Excluded internal/reference Bronze tables" in latest_source, "latest Silver does not report exclusions")

archive_source = notebook_source("02a_archive_silver.ipynb")
check("Excluded internal/reference archive tables" in archive_source, "archive Silver does not report exclusions")

issue_log = (ROOT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md").read_text(encoding="utf-8", errors="replace")
check("SI-001" in issue_log, "issue_log.md does not record the ref_* export_date failure")

if failures:
    print("VALIDATION FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("VALIDATION PASSED")
