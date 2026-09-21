"""Guard the Mission Control model's Power BI project structure.

This checks the saved deployment contract, not Power BI's private load validator.
"""

from pathlib import Path
import re
import textwrap
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "reports/current/_MissionControl_Measures.tmdl"
DEPLOYED_PROJECT = (
    ROOT
    / "reports/client-deliverables/SM WMPP Mission Control - SEM-02 repaired"
)
DEFINITION = DEPLOYED_PROJECT / "SM WMPP Mission Control.SemanticModel/definition"
TABLE_NAME = "_MissionControl_Measures"
REPORT_DEFINITION = (
    DEPLOYED_PROJECT / "SM WMPP Mission Control.Report/definition"
)
ALIGNED_ZIP = (
    ROOT
    / "reports/client-deliverables"
    / "SM WMPP Mission Control - SEM-02 repaired - job drill aligned.zip"
)
ALIGNED_PREFIX = "SM WMPP Mission Control - SEM-02 repaired/"


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


def validate_no_automatic_date_metadata():
    """Reject the generated date paths that March 2026 Desktop cannot resolve."""
    date_tables = sorted((DEFINITION / "tables").glob("LocalDateTable_*.tmdl"))
    assert not date_tables, (
        "SEM-02: generated LocalDateTable definitions reproduce the client's "
        "unresolved DefaultHierarchy/ToColumn load failure"
    )

    semantic_text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in DEFINITION.rglob("*.tmdl")
    )
    report_text = "\n".join(
        path.read_text(encoding="utf-8-sig")
        for path in REPORT_DEFINITION.rglob("*.json")
    )
    for forbidden in (
        "LocalDateTable_",
        "DateTableTemplate_",
        "variation Variation",
        "PropertyVariationSource",
        ".Variation.Date Hierarchy",
    ):
        assert forbidden not in semantic_text
        assert forbidden not in report_text

    private_cache_dirs = list(DEPLOYED_PROJECT.rglob(".pbi"))
    assert not private_cache_dirs, (
        "Client package must not contain Desktop-local .pbi caches"
    )


def main():
    source_text, source_measures = validate_measures_table(SOURCE)
    if ALIGNED_ZIP.exists():
        with ZipFile(ALIGNED_ZIP) as archive:
            names = archive.namelist()
            deployed_text = archive.read(
                ALIGNED_PREFIX
                + "SM WMPP Mission Control.SemanticModel/definition/tables/"
                + f"{TABLE_NAME}.tmdl"
            ).decode("utf-8-sig")
            model = archive.read(
                ALIGNED_PREFIX
                + "SM WMPP Mission Control.SemanticModel/definition/model.tmdl"
            ).decode("utf-8-sig")
            database = archive.read(
                ALIGNED_PREFIX
                + "SM WMPP Mission Control.SemanticModel/definition/database.tmdl"
            ).decode("utf-8-sig")
            model_text = "\n".join(
                archive.read(name).decode("utf-8-sig")
                for name in names
                if name.endswith((".tmdl", ".json"))
            )
        deployed_measures = re.findall(
            r"(?m)^\tmeasure '((?:[^']|'')+)' =", deployed_text
        )
        assert comparable_tmdl(source_text) == comparable_tmdl(deployed_text)
        for forbidden in (
            "LocalDateTable_", "DateTableTemplate_", "variation Variation",
            "PropertyVariationSource", ".Variation.Date Hierarchy",
        ):
            assert forbidden not in model_text
        assert not any("/.pbi/" in name for name in names)
        assert model.splitlines().count(f"ref table {TABLE_NAME}") == 1
        assert "compatibilityLevel: 1600" in database
        assert "compatibilityLevel: 1606" not in database
        print(f"PASS aligned ZIP registers all {len(deployed_measures)} measures")
    elif DEFINITION.exists():
        validate_no_automatic_date_metadata()
        deployed_text, deployed_measures = validate_measures_table(
            DEFINITION / "tables" / f"{TABLE_NAME}.tmdl"
        )
        assert comparable_tmdl(source_text) == comparable_tmdl(deployed_text), (
            "Deployed Mission Control definitions differ from source after ignoring "
            "Desktop-generated lineage tags and serialization whitespace"
        )
        model = (DEFINITION / "model.tmdl").read_text(encoding="utf-8-sig")
        assert model.splitlines().count(f"ref table {TABLE_NAME}") == 1
        database = (DEFINITION / "database.tmdl").read_text(encoding="utf-8-sig")
        # Keep the repaired copy at the compatibility level used by the client.
        assert "compatibilityLevel: 1600" in database
        assert "compatibilityLevel: 1606" not in database
        print(f"PASS deployed model registers all {len(deployed_measures)} measures")
    else:
        print("NOTE client-deliverables extraction is absent; checked source table only")

    print(f"PASS {len(source_measures)} Mission Control measures have an explicit Import partition")


if __name__ == "__main__":
    main()
