"""Check WIP measure inventory and completeness of requirement audit rows.

Name coverage is deliberately separate from DAX correctness and business sign-off.
"""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "client documentation/04_Data_and_Reporting"


def guide_measure_names(text):
    names = []
    for block in re.findall(r"```DAX\s*\n(.*?)```", text, re.DOTALL | re.IGNORECASE):
        for match in re.finditer(r"^([^\n=]+?)[ \t]*=[ \t]*", block, re.MULTILINE):
            candidate = match[1]
            if candidate[0].isspace() or candidate.upper().startswith("VAR "):
                continue
            if any(char in candidate for char in "[]'\""):
                continue
            name = candidate.strip()
            if name.startswith(("<Base>", "--", "//")):
                continue
            names.append(name)
    assert names, "No concrete WIP measure definitions found"
    assert len(names) == len({name.casefold() for name in names}), "Duplicate guide measures"
    return set(names)


def model_measure_names(paths):
    return {
        name.replace("''", "'").casefold()
        for path in paths
        for name in re.findall(
            r"^\tmeasure '((?:[^']|'')+)'\s*=",
            path.read_text(encoding="utf-8-sig"),
            re.MULTILINE,
        )
    }


def ids(text, prefix):
    return set(re.findall(rf"^\| ({prefix}\d+) \|", text, re.MULTILINE))


def main():
    guide = (DOCS / "GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE WIP.md").read_text(encoding="utf-8-sig")
    required = {name.casefold() for name in guide_measure_names(guide)}
    source = model_measure_names([ROOT / "reports/current/_Measures.tmdl"])
    assert not required - source, f"Source missing WIP measures: {sorted(required - source)}"
    deployed = ROOT / "reports/client-deliverables/SM WMPP v15/SM_WMPP.SemanticModel/definition/tables"
    if deployed.exists():
        present = model_measure_names(deployed.glob("*.tmdl"))
        assert not required - present, f"v15 missing WIP measures: {sorted(required - present)}"
        print(f"PASS all {len(required)} concrete WIP measures present in extracted v15")
    else:
        print("NOTE extracted v15 is absent; checked maintained source only")
    audit = (DOCS / "GOLD_MEASURE_REQUIREMENT_COVERAGE_AUDIT.md").read_text(encoding="utf-8-sig")
    reference = (DOCS / "KPI_Reference_Guide.md").read_text(encoding="utf-8-sig")
    assessment = (ROOT / "client documentation/02_Assessment_and_Requirements/As_Is_Assessment_Report.md").read_text(encoding="utf-8-sig")
    for prefix, original in (("KPI-", reference), ("R", assessment)):
        expected = ids(original, prefix)
        assert expected and ids(audit, prefix) == expected, f"Audit {prefix} coverage differs"
        print(f"PASS audit accounts for all {len(expected)} {prefix} IDs")
    print(f"PASS source contains {len(required)} concrete WIP measures; no correctness claim")


if __name__ == "__main__":
    main()
