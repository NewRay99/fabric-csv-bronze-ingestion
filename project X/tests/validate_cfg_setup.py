import ast
import json
import re
import sys
from pathlib import Path


sys.stdout.reconfigure(encoding="utf-8")
PROJECT = Path(__file__).resolve().parents[1]
SETUP = "00_setup_cfg.ipynb"
CONSUMERS = [
    "00_archive_load.ipynb",
    "00a_rehydrate_archive_cfg.ipynb",
    "00b_reset_silver_cfg.ipynb",
    "01_bronze_get_latest.ipynb",
    "01a_cfg_schema_capture_live.ipynb",
    "01a_cfg_schema_capture_archive.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
    "03_silver_business_rules.ipynb",
    "04_gold_model.ipynb",
    "05_gold_dimensions.ipynb",
]
REQUIRED_TABLES = {
    "monitoring.cfg_silver_export_load",
    "monitoring.cfg_pipeline_run",
    "monitoring.cfg_table_load_metric",
    "monitoring.cfg_job_run",
    "monitoring.cfg_job_step_run",
    "monitoring.cfg_schema_drift_definition",
    "monitoring.cfg_schema_drift_event",
    "monitoring.cfg_month_end_gold_run",
    "monitoring.cfg_archive_zip_load",
    "monitoring.cfg_archive_file_load",
    "monitoring.cfg_archive_table_export_load",
    "monitoring.cfg_schema_contract_column",
    "monitoring.cfg_bronze_schema_live",
    "monitoring.cfg_archived_schema_live",
    "monitoring.cfg_schema_definition_candidate",
    "monitoring.cfg_data_quality_result",
    "monitoring.cfg_rejected_row",
    "monitoring.cfg_referential_exception",
    "monitoring.cfg_data_quality_rule",
    "gold.cfg_placement_urgency_rule",
}


def load(name):
    path = PROJECT / name
    notebook = json.loads(path.read_text(encoding="utf-8"))
    sources = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
    return notebook, sources, "\n".join(sources)


errors = []
setup_notebook, setup_cells, setup_source = load(SETUP)

parameter_cells = [
    cell for cell in setup_notebook["cells"]
    if cell.get("cell_type") == "code"
    and "parameters" in cell.get("metadata", {}).get("tags", [])
]
if len(parameter_cells) != 1:
    errors.append(f"{SETUP}: expected one Fabric parameters cell")

for table_name in sorted(REQUIRED_TABLES):
    if table_name.lower() not in setup_source.lower():
        errors.append(f"{SETUP}: missing {table_name}")
if "CONFIG_TABLE_DEFINITIONS" not in setup_source:
    errors.append(f"{SETUP}: missing central CONFIG_TABLE_DEFINITIONS registry")
if "ensure_delta_table" not in setup_source:
    errors.append(f"{SETUP}: missing idempotent ensure_delta_table helper")

ddl_pattern = re.compile(
    r"(?:CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS|ALTER\s+TABLE|MERGE\s+INTO)"
    r"[^\n]*(?:monitoring|gold)\.cfg_",
    re.IGNORECASE,
)

for name in CONSUMERS:
    notebook, cells, source = load(name)
    parameter_source = next(
        "".join(cell.get("source", []))
        for cell in notebook["cells"]
        if cell.get("cell_type") == "code"
        and "".join(cell.get("source", [])).strip()
        and not "".join(cell.get("source", [])).lstrip().startswith("%")
    )
    for setting in (
        "CFG_NOTEBOOK_NAME", "AUDIT_TABLE", "TIME_PARSER_POLICY",
        "NOTEBOOK_TIMEOUT_SECONDS",
    ):
        if setting not in parameter_source:
            errors.append(f"{name}: parameters cell missing {setting}")
    call_cells = [
        index for index, cell in enumerate(cells)
        if "mssparkutils.notebook.run" in cell and "CFG_NOTEBOOK_NAME" in cell
    ]
    if not call_cells:
        errors.append(f"{name}: missing 00_setup_cfg invocation")
    else:
        call_index = call_cells[0]
        operation_cells = [
            index for index, cell in enumerate(cells)
            if re.search(
                r"(?:spark\.table|saveAsTable|append_rows|DeltaTable\.forName|"
                r"DELETE\s+FROM|UPDATE\s+monitoring\.|MERGE\s+INTO)"
                r"[\s\S]{0,250}(?:monitoring|gold)\.cfg_",
                cell,
                re.IGNORECASE,
            )
        ]
        if operation_cells and call_index > min(operation_cells):
            errors.append(
                f"{name}: setup call cell {call_index} follows config operation "
                f"cell {min(operation_cells)}"
            )
    if ddl_pattern.search(source):
        errors.append(f"{name}: config DDL/seed logic remains outside {SETUP}")

for path in [PROJECT / SETUP] + [PROJECT / name for name in CONSUMERS]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    for index, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") != "code":
            continue
        source = "".join(cell.get("source", []))
        if not source.strip() or source.lstrip().startswith("%"):
            continue
        try:
            ast.parse(source)
        except SyntaxError as exc:
            errors.append(f"{path.name} cell {index}: {exc}")

issue_log = (PROJECT / "change tracking" / "ETL_ISSUE_AND_CHANGE_LOG.md").read_text(encoding="utf-8")
if "SI-002" not in issue_log:
    errors.append("issue_log.md: missing SI-002")

if errors:
    print("VALIDATION FAILED")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("VALIDATION PASSED")
