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

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
