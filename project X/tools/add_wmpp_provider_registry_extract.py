"""Add GLD-023's isolated registry import and owner-only export page to saved WIP.

Preview is default. --apply performs backed-up, hash-guarded definition edits.
Never executes Fabric, publishes, grants access, enables export policies, changes
existing page visuals/bookmarks/relationships or touches the .pbi data cache.
"""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import uuid


PROJECT = Path(__file__).resolve().parents[1] / "reports/WIP/SM WMPP v16 updated WIP"
MODEL = Path("SM_WMPP_v16.SemanticModel/definition")
REPORT = Path("SM_WMPP_v16.Report/definition")
TABLE = "rpt_provider_registry"
NAMESPACE = uuid.UUID("703a7098-cb6e-4bf6-9919-1fca24a6ae19")
PAGE_ID = uuid.uuid5(NAMESPACE, "provider-registry-extract-page").hex[:20]
EXPORT_FIELDS = (
    "Provider ID", "Provider Name", "Town/City", "Postcode", "Framework Code",
    "Placement Type", "Home Name", "Service Type", "Provider Email", "Provider Phone",
    "Responsible Individual Name", "Responsible Individual Contact Number",
    "Responsible Individual Email Address", "Registrant Name", "Registrant Role",
    "Registrant Email", "Registrant Contact Number", "Provider Status", "County",
    "Country", "Source Export Date",
)
DENY_RULE = "\ttablePermission rpt_provider_registry = FALSE ()\n"


def visual_id(name):
    return uuid.uuid5(NAMESPACE, name).hex[:20]


def encode_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def color(value):
    return {"solid": {"color": literal("'" + value + "'")}}


def projection(name):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": TABLE}}, "Property": name}},
        "queryRef": TABLE + "." + name, "nativeQueryRef": name, "active": True,
    }


def visual(name, kind, x, y, width, height):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": visual_id(name),
        "position": {"x": x, "y": y, "z": 1000, "width": width, "height": height, "tabOrder": int(y)},
        "visual": {
            "visualType": kind,
            "visualContainerObjects": {
                "title": [{"properties": {"show": literal("false")}}],
                "background": [{"properties": {"show": literal("false")}}],
                "border": [{"properties": {"show": literal("false")}}],
                "dropShadow": [{"properties": {"show": literal("false")}}],
            },
        },
    }


def textbox(name, text, y, height, size=16):
    result = visual(name, "textbox", 36, y, 1888, height)
    result["visual"]["objects"] = {"general": [{"properties": {"paragraphs": [{
        "textRuns": [{"value": text, "textStyle": {
            "fontFamily": "Segoe UI", "fontSize": f"{size}px", "fontWeight": "normal", "color": "#2B2427",
        }}],
    }]}}]}
    return result


def slicer(name, field, x, width):
    result = visual(name, "slicer", x, 234, width, 100)
    result["visual"]["query"] = {"queryState": {"Values": {"projections": [projection(field)]}}}
    result["visual"]["objects"] = {
        "data": [{"properties": {"mode": literal("'Dropdown'")}}],
        "header": [{"properties": {"show": literal("false")}}],
        "selection": [{"properties": {"singleSelect": literal("false"), "selectAllCheckboxEnabled": literal("true")}}],
        "items": [{"properties": {"fontSize": literal("11D"), "fontColor": color("#2B2427")}}],
    }
    result["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": literal("true"), "text": literal("'" + field + "'"),
                                   "fontSize": literal("12D"), "bold": literal("false")}}],
        "background": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "transparency": literal("0D")}}],
        "border": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "radius": literal("12D")}}],
    })
    return result


def registry_table():
    result = visual("registry-export-table", "tableEx", 36, 354, 1888, 598)
    result["visual"]["query"] = {
        "queryState": {"Values": {"projections": [projection(field) for field in EXPORT_FIELDS]}},
        "sortDefinition": {"sort": [{"field": projection("Provider Name")["field"], "direction": "Ascending"}]},
    }
    result["visual"]["objects"] = {
        "columnHeaders": [{"properties": {"fontColor": color("#2B2427"), "backColor": color("#FFFFFF"),
                                            "fontSize": literal("11D"), "bold": literal("false")}}],
        "values": [{"properties": {"fontColor": color("#2B2427"), "backColorPrimary": color("#FFFFFF"),
                                     "backColorSecondary": color("#F8F5F1"), "fontSize": literal("11D")}}],
        "grid": [{"properties": {"gridVertical": literal("false"), "rowPadding": literal("6D")}}],
        "total": [{"properties": {"totals": literal("false")}}],
    }
    result["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": literal("true"), "text": literal("'Provider registry — Fostering'"),
                                   "fontSize": literal("14D"), "bold": literal("false")}}],
        "background": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "transparency": literal("0D")}}],
        "border": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "radius": literal("12D")}}],
        "visualHeader": [{"properties": {"show": literal("true")}}],
        "general": [{"properties": {"altText": literal(
            "'Fostering provider registry with all contact columns. Use the horizontal scrollbar for remaining fields. Export summarized data from this table only when authorized.'"
        )}}],
    })
    return result


def page_definitions():
    documents = [
        textbox("registry-title", "Provider Registry Extract", 32, 48, 28),
        textbox("registry-subtitle", "Fostering providers with framework membership, including providers without offers. One row per Provider ID.", 92, 36),
        textbox("registry-access-note", "Contact extract for report owners pending audience approval. The existing reader role returns no registry rows. This page is hidden in reading view; hiding is not a security control.", 144, 60),
        slicer("registry-provider-filter", "Provider Name", 36, 928),
        slicer("registry-status-filter", "Provider Status", 984, 450),
        slicer("registry-town-filter", "Town/City", 1454, 470),
        registry_table(),
        textbox("registry-export-help", "Filter this page, then use the table menu (…) → Export data → Summarized data. Scroll sideways to view all fields. Framework Code retains every distinct Fostering membership.", 968, 30, 14),
    ]
    table_id = visual_id("registry-export-table")
    page = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": PAGE_ID, "displayName": "Provider Registry Extract", "displayOption": "FitToWidth",
        "width": 1960, "height": 1020, "visibility": "HiddenInViewMode",
        "objects": {"background": [{"properties": {"color": color("#F8F5F1"), "transparency": literal("0D")}}]},
        "visualInteractions": [{"source": visual_id(key), "target": table_id, "type": "DataFilter"} for key in (
            "registry-provider-filter", "registry-status-filter", "registry-town-filter",
        )],
    }
    result = {REPORT / "pages" / PAGE_ID / "page.json": encode_json(page)}
    for document in documents:
        result[REPORT / "pages" / PAGE_ID / "visuals" / document["name"] / "visual.json"] = encode_json(document)
    return result


def plan_changes(project):
    planned = {}

    def read(relative):
        return (project / relative).read_text(encoding="utf-8-sig")

    def put(relative, contents, new_only=False):
        path = project / relative
        if path.exists() and read(relative) == contents:
            return
        if path.exists() and new_only:
            raise RuntimeError(f"Registry definition has user edits; preserve it: {relative}")
        planned[path] = contents

    # A separate, unrelated contact table cannot silently inherit referral RLS.
    # Protect its rows explicitly, without granting anyone a new model role.
    role_files = list((project / MODEL / "roles").glob("*.tmdl"))
    role_path = MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
    if {p.name for p in role_files} != {role_path.name}:
        raise RuntimeError("Unrecognised RLS roles: review each role's registry access before adding contacts")
    role = read(role_path)
    permission = re.search(r"\ttablePermission rpt_provider_registry\s*=([^\n]*(?:\n\t{2,}[^\n]*)*)", role)
    if permission:
        if permission.group(1).strip() != "FALSE ()":
            raise RuntimeError("Existing registry access rule needs an explicit audience decision; do not overwrite")
    else:
        marker = "\tannotation PBI_Id = "
        if role.count(marker) != 1:
            raise RuntimeError("Unexpected role format; no edits made")
        role = role.replace(marker, DENY_RULE + "\n" + marker, 1)
        put(role_path, role)

    template = Path(__file__).with_name("templates") / "provider_registry.tmdl"
    put(MODEL / "tables/rpt_provider_registry.tmdl", template.read_text(encoding="utf-8"), new_only=True)
    model = read(MODEL / "model.tmdl")
    if "ref table rpt_provider_registry\n" not in model:
        model += "\nref table rpt_provider_registry\n"
    order_pattern = r"(?m)^annotation PBI_QueryOrder = (\[.*\])$"
    match = re.search(order_pattern, model)
    if not match:
        raise RuntimeError("Missing model query order; no edits made")
    order = json.loads(match.group(1))
    if TABLE not in order:
        order.append(TABLE)
        model = model[:match.start(1)] + json.dumps(order, ensure_ascii=False, separators=(",", ":")) + model[match.end(1):]
    put(MODEL / "model.tmdl", model)

    metadata_path = REPORT / "pages/pages.json"
    metadata = json.loads(read(metadata_path))
    if PAGE_ID not in metadata["pageOrder"]:
        metadata["pageOrder"].append(PAGE_ID)
        put(metadata_path, encode_json(metadata))
    for relative, contents in page_definitions().items():
        put(relative, contents, new_only=True)
    return planned


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    project = PROJECT.resolve(strict=True)
    planned = plan_changes(project)
    result = {"project": str(project), "files": [str(p.relative_to(project)) for p in planned], "apply": args.apply}
    if args.apply and planned:
        original = {p: digest(p) for p in project.rglob("*") if p.is_file() and ".pbi" not in p.relative_to(project).parts}
        backup = project.parent / "_review" / ("gld023-registry-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
        backup.mkdir(parents=True)
        for path in planned:
            if path in original:
                destination = backup / path.relative_to(project)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
                if digest(destination) != original[path]:
                    raise RuntimeError("Concurrent save during backup; no report writes attempted")
        for path, expected in original.items():
            if digest(path) != expected:
                raise RuntimeError("Concurrent save before apply; no report writes attempted")
        manifest = {**result, "before_sha256": {str(p.relative_to(project)): original.get(p) for p in planned}}
        manifest_path = backup / "registry-manifest.json"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        for path, contents in planned.items():
            if path.exists() and digest(path) != original.get(path):
                raise RuntimeError(f"Concurrent edit; preserve it: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        for path, expected in original.items():
            if path not in planned and digest(path) != expected:
                raise RuntimeError(f"Unrelated file changed during apply: {path}")
        if plan_changes(project):
            raise RuntimeError("Apply did not produce an idempotent result")
        manifest["verified"] = "All unlisted model/report file hashes unchanged, excluding .pbi cache"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        result.update({"backup": str(backup), "verified": manifest["verified"]})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
