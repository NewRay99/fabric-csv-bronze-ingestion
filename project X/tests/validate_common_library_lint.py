"""Static lint guard for the standalone common Fabric notebook."""

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "project X" / "99_common_library.ipynb"


def main():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert notebook["nbformat"] == 4

    code_cells = [cell for cell in notebook["cells"] if cell.get("cell_type") == "code"]
    for index, cell in enumerate(code_cells):
        source = "".join(cell.get("source", []))
        ast.parse(source, filename=f"99_common_library:code-cell-{index}")
        assert "##Silver Layer functions" not in source, (
            "Use a Markdown cell rather than a Markdown heading in code"
        )
    print("PASS common-library JSON and code-cell syntax")

    source = "\n".join("".join(cell.get("source", [])) for cell in code_cells)
    for setting in [
        "TIME_PARSER_POLICY", "DATE_FORMATS", "TIMESTAMP_FORMATS",
        "VERBOSE_DIAGNOSTICS", "DIAGNOSTIC_KEY_SAMPLE_SIZE",
        "SILVER_SCHEMA", "AUDIT_TABLE", "contracts_by_table",
    ]:
        assert f'{setting} = globals().get(' in source, (
            f"Common library lacks a standalone default for {setting}"
        )
    print("PASS common-library caller settings have standalone defaults")

    for function_name in (
        "qident",
        "append_rows",
        "merge_monitor_row",
        "drift_event_row",
    ):
        assert f"def {function_name}" in source, (
            f"Common library is missing shared utility {function_name}"
        )

    shared_callers = {
        "00_archive_load.ipynb": {"qident", "append_rows"},
        "01a_cfg_schema_capture_archive.ipynb": {"qident", "append_rows"},
        "02_silver_formatter.ipynb": {"drift_event_row"},
        "02a_archive_silver.ipynb": {"drift_event_row"},
        "90_run_live_pipeline.ipynb": {"merge_monitor_row"},
        "90_run_archive_pipeline.ipynb": {"merge_monitor_row"},
    }
    project = ROOT / "project X"
    for notebook_name, function_names in shared_callers.items():
        child = json.loads((project / notebook_name).read_text(encoding="utf-8"))
        child_source = "\n".join(
            "".join(cell.get("source", [])) for cell in child["cells"]
        )
        assert "%run ./99_common_library" in child_source, (
            f"{notebook_name} does not load the shared utility seam"
        )
        for function_name in function_names:
            assert f"def {function_name}" not in child_source, (
                f"{notebook_name} still duplicates common utility {function_name}"
            )
    print("PASS duplicate cross-notebook utilities are owned by the common library")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
