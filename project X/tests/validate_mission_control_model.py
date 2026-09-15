"""Guard the Mission Control measures table's Power BI Import-table structure.

This checks the saved deployment contract, not Power BI's private load validator.
"""

from pathlib import Path
import re
import textwrap


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/current/_MissionControl_Measures.tmdl"
DEFINITION = (
    ROOT
    / "reports/client-deliverables/SM WMPP Mission Control"
    / "SM WMPP Mission Control/SM WMPP Mission Control.SemanticModel/definition"
)
TABLE_NAME = "_MissionControl_Measures"


def comparable_tmdl(text):
    """Ignore Desktop-generated IDs and its observed serialization changes.

    Preserve expression contents, including whitespace inside string literals.
    This is a conservative comparison, not a general TMDL or DAX parser.
    """
    lines = []
    expression = None
    pending_source = None
    for line in text.splitlines():
        if expression is not None:
            if line.strip() == "```":
                while expression and not expression[0].strip():
                    expression.pop(0)
                while expression and not expression[-1].strip():
                    expression.pop()
                lines.append(textwrap.dedent("\n".join(expression)))
                lines.append("```")
                expression = None
            else:
                expression.append(line)
            continue
        if not line.strip() or re.match(r"^\s*lineageTag:", line):
            continue
        if pending_source is not None:
            lines.append(pending_source + " " + line.lstrip())
            pending_source = None
        elif line.rstrip().endswith("= ```"):
            lines.append(line.rstrip())
            expression = []
        elif line.strip() == "source =":
            pending_source = line.rstrip()
        else:
            lines.append(line.rstrip())
    assert expression is None, "Unclosed TMDL expression fence"
    assert pending_source is None, "Partition source expression is missing"
    return "\n".join(lines)


def validate_measures_table(path):
    text = path.read_text(encoding="utf-8-sig")
    partitions = re.findall(r"(?m)^\tpartition .*(?:\n(?!\t(?:partition|annotation) |\S).*)*", text)
    assert len(partitions) == 1, (
        f"{path}: measures table must have one explicit Import partition; "
        "a table declaration and measures alone are not a complete Desktop table"
    )
    partition = partitions[0]
    assert re.search(r"(?m)^\tpartition .+ = m$", partition), path
    assert re.search(r"(?m)^\t\tmode: import$", partition), path
    assert re.search(r"(?m)^\t\tsource\s*=", partition), path
    measures = re.findall(r"(?m)^\tmeasure '((?:[^']|'')+)' =", text)
    assert measures and len(measures) == len(set(measures)), path
    return text, measures


def main():
    source_text, source_measures = validate_measures_table(SOURCE)
    if DEFINITION.exists():
        deployed_text, deployed_measures = validate_measures_table(
            DEFINITION / "tables" / f"{TABLE_NAME}.tmdl"
        )
        assert comparable_tmdl(source_text) == comparable_tmdl(deployed_text), (
            "Deployed Mission Control definitions differ from source after ignoring "
            "Desktop-generated lineage tags and serialization whitespace"
        )
        model = (DEFINITION / "model.tmdl").read_text(encoding="utf-8-sig")
        assert model.splitlines().count(f"ref table {TABLE_NAME}") == 1
        print(f"PASS deployed model registers all {len(deployed_measures)} measures")
    else:
        print("NOTE client-deliverables extraction is absent; checked source table only")

    print(f"PASS {len(source_measures)} Mission Control measures have an explicit Import partition")


if __name__ == "__main__":
    main()
