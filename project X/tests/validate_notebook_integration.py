"""Fast static regressions for the Version 02 03 Fabric notebook fixes."""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "00_archive_load.ipynb",
    "00_setup_cfg.ipynb",
    "00a_rehydrate_archive_cfg.ipynb",
    "00b_reset_silver_cfg.ipynb",
    "01_bronze_get_latest.ipynb",
    "99_common_library.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
    "05_gold_dimensions.ipynb",
]


def load_notebook(name):
    notebook = json.loads((ROOT / name).read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell["cell_type"] == "code" and not source.lstrip().startswith("%"):
            ast.parse(source, filename=f"{name}:cell-{index}")
    return notebook


def source(notebook):
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


notebooks = {name: load_notebook(name) for name in NOTEBOOKS}
print("PASS notebook JSON and Python syntax")

for name in ["00_setup_cfg.ipynb", "99_common_library.ipynb"]:
    text = source(notebooks[name])
    assignment = text.find("TIME_PARSER_POLICY =")
    use = text.find('spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)')
    assert assignment >= 0 and assignment < use, (
        f"{name}: TIME_PARSER_POLICY must have a local default before use"
    )
print("PASS shared/setup parser policy is self-contained")

CFG_CALLERS = [
    "00a_rehydrate_archive_cfg.ipynb",
    "00b_reset_silver_cfg.ipynb",
    "02_silver_formatter.ipynb",
    "02a_archive_silver.ipynb",
    "05_gold_dimensions.ipynb",
]
for name in CFG_CALLERS:
    text = source(notebooks[name])
    assert '"AUDIT_TABLE": AUDIT_TABLE' in text, (
        f"{name}: child-notebook parameter must pass the variable value"
    )
    assert '{"AUDIT_TABLE": "{AUDIT_TABLE}"}' not in text
    assert '"AUDIT_TABLE": ""' not in text
    assert "from notebookutils import mssparkutils" in text
print("PASS cfg notebook receives the resolved audit-table name")

reset_text = source(notebooks["00b_reset_silver_cfg.ipynb"])
assert reset_text.find("def qident") < reset_text.find("cfg_result ="), (
    "00b reset must define qident before the cfg setup cell uses it"
)
print("PASS reset helper execution order")

for name in ["02_silver_formatter.ipynb", "02a_archive_silver.ipynb"]:
    text = source(notebooks[name])
    assert "SKIPPED_NO_CONTRACT" in text, (
        f"{name}: missing contracts must be auditable non-fatal skips"
    )
    assert "MISSING_TABLE_CONTRACT" in text
    assert "monitoring.cfg_schema_drift_event" in text
print("PASS missing table contracts are logged and skipped")
