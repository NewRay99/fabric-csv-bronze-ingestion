"""Plan narrow WIP identifier edits; emit an apply_patch, never write files.

References belong to people and are not unique referral keys. Every changed
table includes the canonical fact reference AND sequence, so grouping and
compound drillthrough preserve individual referrals. Layout, UUID relationships,
security roles, business measures, connections and bookmarks are not rebuilt.
"""

import argparse
from copy import deepcopy
import difflib
import json
from pathlib import Path
import uuid


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = PROJECT / "reports/WIP/SM WMPP v16 updated WIP"
DETAIL_PAGE = "4cad3706fca6451c66b8"
REFERENCE_FIELDS = (
    ("source_reference_id", "Source reference", "string"),
    ("order_dupe", "Referral sequence", "int64"),
    ("has_multiple_referrals", "Multiple referrals", "boolean"),
    ("source_reference_referral_count", "Referrals for reference", "int64"),
)
REFERRAL_ENTITIES = {"fact_referral", "fact_offer", "fact_ipa", "fact_referral_provider"}


def column(entity, name):
    return {"Column": {"Expression": {"SourceRef": {"Entity": entity}}, "Property": name}}


def is_referral_id(field):
    value = field.get("Column", {})
    return (value.get("Property") == "referral_id"
            and value.get("Expression", {}).get("SourceRef", {}).get("Entity")
            in REFERRAL_ENTITIES)


def projection(name, label):
    return {"field": column("fact_referral", name), "queryRef": f"fact_referral.{name}",
            "nativeQueryRef": label, "displayName": label}


def replace_format_refs(value, old_refs):
    """Rebind only column-format selectors, not actual UUID filters or measures."""
    if isinstance(value, dict):
        return {key: replace_format_refs(item, old_refs) for key, item in value.items()}
    if isinstance(value, list):
        return [replace_format_refs(item, old_refs) for item in value]
    if isinstance(value, str) and value in old_refs:
        return "fact_referral.source_reference_id"
    return value


def table_reference_visual(original):
    result = deepcopy(original)
    visual = result.get("visual", {})
    if visual.get("visualType") != "tableEx":
        return result
    values = visual.get("query", {}).get("queryState", {}).get("Values", {})
    old = values.get("projections", [])
    old_refs = {p["queryRef"] for p in old if is_referral_id(p.get("field", {}))}
    if not old_refs:
        return result
    new = []
    inserted = False
    for item in old:
        if is_referral_id(item.get("field", {})):
            if not inserted:
                new.extend(projection(name, label) for name, label, _ in REFERENCE_FIELDS[:3])
                inserted = True
        elif item.get("queryRef") not in {f"fact_referral.{f[0]}" for f in REFERENCE_FIELDS[:3]}:
            new.append(item)
    values["projections"] = new
    if "objects" in visual:
        visual["objects"] = replace_format_refs(visual["objects"], old_refs)
    for item in visual["query"].get("sortDefinition", {}).get("sort", []):
        if is_referral_id(item.get("field", {})):
            item["field"] = column("fact_referral", "source_reference_id")
    return result


def reference_slicer(original):
    result = deepcopy(original)
    visual = result.get("visual", {})
    if visual.get("visualType") != "slicer" and not visual.get("visualType", "").startswith("textFilter"):
        return result
    changed = False
    for values in visual.get("query", {}).get("queryState", {}).values():
        for item in values.get("projections", []):
            if is_referral_id(item.get("field", {})):
                item.update(projection("source_reference_id", "Source reference"))
                changed = True
    if changed:
        # Refuse to reinterpret any saved UUID selection as a source reference.
        # Current WIP slicers have no such selection; preserve other filters.
        for entry in result.get("filterConfig", {}).get("filters", []):
            if is_referral_id(entry.get("field", {})) and "filter" in entry:
                raise ValueError("Clear saved referral UUID slicer selections before migration")
        for group in (visual.get("objects", {}).get("header", []),
                      visual.get("visualContainerObjects", {}).get("title", [])):
            for entry in group:
                literal = entry.get("properties", {}).get("text", {}).get("expr", {}).get("Literal")
                if literal:
                    literal["Value"] = "'Search / select source references'"
    return result


def identifier_instructions(value):
    """Update navigation/display prose only; keep distinct-UUID KPI explanations."""
    if isinstance(value, dict):
        return {key: identifier_instructions(item) for key, item in value.items()}
    if isinstance(value, list):
        return [identifier_instructions(item) for item in value]
    if isinstance(value, str):
        substitutions = {
            "selected Referral ID": "selected referral (source reference + sequence)",
            "Select one Referral ID row": "Select one source-reference / sequence row",
            "Select a Referral ID row": "Select a source-reference / sequence row",
            "Search by person or Referral ID": "Search by person or source reference",
            "Search by person label and referral ID": "Search by person label and source reference",
            "Search by referral ID or person label": "Search by source reference or person label",
            "right-click a referral ID": "right-click a source-reference / sequence row",
        }
        for old, new in substitutions.items():
            value = value.replace(old, new)
    return value


def detail_reference_binding(original):
    result = deepcopy(original)
    binding = result.get("pageBinding", {})
    params = binding.get("parameters", [])
    filters = result.get("filterConfig", {}).get("filters", [])
    for param in params:
        if is_referral_id(param.get("fieldExpr", {})):
            param["fieldExpr"] = column("fact_referral", "source_reference_id")
            bound = next(f for f in filters if f["name"] == param["boundFilter"])
            bound["field"] = column("fact_referral", "source_reference_id")
    sequence = column("fact_referral", "order_dupe")
    if not any(p.get("fieldExpr") == sequence for p in params):
        filter_name = uuid.uuid5(uuid.NAMESPACE_URL, "wmpp/source-reference/sequence-filter").hex[:20]
        params.append({"name": uuid.uuid5(uuid.NAMESPACE_URL,
                       "wmpp/source-reference/sequence-parameter").hex[:20],
                       "boundFilter": filter_name, "fieldExpr": sequence})
        filters.append({"name": filter_name, "field": sequence,
                        "type": "Categorical", "howCreated": "Drillthrough"})
    return result


def reference_model(source, entity):
    result = source
    fields = REFERENCE_FIELDS[:1] if entity == "dim_person" else REFERENCE_FIELDS
    for name, _, datatype in fields:
        if f"\tcolumn {name}\n" in result:
            continue
        lineage = uuid.uuid5(uuid.NAMESPACE_URL, f"wmpp/gold-source-reference/{entity}/{name}")
        description = {
            "source_reference_id": "Source person reference (text), not a unique referral key.",
            "order_dupe": "Oldest-first sequence within a trimmed case-insensitive reference; UUID breaks ties. Missing references have a separate sequence for navigation.",
            "has_multiple_referrals": "Review flag: more than one as-of referral shares a nonblank source reference, including closed referrals. Not a deletion rule.",
            "source_reference_referral_count": "As-of referral count for a nonblank reference; zero for missing references. Not recomputed by report filters.",
        }[name]
        block = (f"\tcolumn {name}\n\t\tdescription: {description}\n"
                 f"\t\tdataType: {datatype}\n\t\tlineageTag: {lineage}\n"
                 f"\t\tsummarizeBy: none\n\t\tsourceColumn: {name}\n\n"
                 "\t\tannotation SummarizationSetBy = Automatic\n\n")
        marker = f"\tpartition {entity} = m"
        if marker not in result:
            raise ValueError(f"Expected the current Gold import partition for {entity}")
        result = result.replace(marker, block + marker, 1)
    if entity == "dim_person":
        result = result.replace("RETURN person_initials & \" | \" & 'dim_person'[person_id]",
                                "RETURN person_initials & \" | \" & COALESCE ( 'dim_person'[source_reference_id], \"Reference missing\" )")
    return result


def reference_selection_label(source):
    # Keep UUID-based single-record detection; change only the displayed label.
    return source.replace(
        '"Selected referral: " & SELECTEDVALUE(\'fact_referral\'[referral_id])',
        '"Selected referral: " & COALESCE(SELECTEDVALUE(\'fact_referral\'[source_reference_id]),'
        '"Reference missing") & " | Sequence: " & FORMAT(SELECTEDVALUE(\'fact_referral\'[order_dupe]),"0")',
    )


def plan(root):
    root = Path(root)
    updates = {}
    report = root / "SM_WMPP_v16.Report/definition"
    model = root / "SM_WMPP_v16.SemanticModel/definition/tables"
    for entity in ("dim_person", "fact_referral", "fact_referral_snapshot"):
        path = model / f"{entity}.tmdl"
        old = path.read_text(encoding="utf-8-sig")
        new = reference_model(old, entity)
        if new != old:
            updates[path] = new
    path = model / "_Report Journey Measures.tmdl"
    old = path.read_text(encoding="utf-8-sig")
    new = reference_selection_label(old)
    if new != old:
        updates[path] = new
    for path in sorted((report / "pages").glob("*/visuals/*/visual.json")):
        old = json.loads(path.read_text(encoding="utf-8-sig"))
        new = table_reference_visual(old)
        new = identifier_instructions(reference_slicer(new))
        if old != new:
            assert old["position"] == new["position"], "Never move/resize an identifier change"
            updates[path] = json.dumps(new, ensure_ascii=False, indent=2) + "\n"
    path = report / f"pages/{DETAIL_PAGE}/page.json"
    old = json.loads(path.read_text(encoding="utf-8-sig"))
    new = detail_reference_binding(old)
    if old != new:
        updates[path] = json.dumps(new, ensure_ascii=False, indent=2) + "\n"
    return updates


def patch_for(updates):
    parts = ["*** Begin Patch"]
    for path, content in updates.items():
        old = path.read_text(encoding="utf-8-sig").splitlines()
        new = content.splitlines()
        diff = list(difflib.unified_diff(old, new, n=3))
        parts.append(f"*** Update File: {path.as_posix()}")
        parts.extend("@@" if line.startswith("@@") else line for line in diff[2:])
    return "\n".join(parts + ["*** End Patch"])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--print-patch", action="store_true")
    args = parser.parse_args()
    updates = plan(args.root)
    if args.print_patch:
        print(patch_for(updates))
    else:
        print(json.dumps({"changes": len(updates), "files": [str(p.relative_to(args.root))
                         for p in updates]}, indent=2))


if __name__ == "__main__":
    main()
