"""Add only the Offer Locations path map to the confirmed saved WIP.

Default: preview. --apply: backed-up, hash-guarded mechanical definition edits.
No publishing, cache editing, notebook execution, layout rebuild or RLS changes.
Azure Maps bindings verified against Desktop 2.158's installed capabilities:
PathID + PointOrder + unaggregated X/Y, with no Category or endpoint Legend.
"""

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import uuid


PROJECT = Path(__file__).resolve().parents[1] / "reports/WIP/SM WMPP v16 updated WIP"
PAGE_ID = "1cd52e9c7e4016f342ce"
REPORT = Path("SM_WMPP_v16.Report/definition")
MODEL = Path("SM_WMPP_v16.SemanticModel/definition")
TABLE = "Offer Location Paths"
COORDINATES = ("referral_latitude", "referral_longitude", "provider_home_latitude", "provider_home_longitude")
NAMESPACE = uuid.UUID("a80dd9aa-1c2a-442d-ab59-283493245480")


def uid(name):
    return str(uuid.uuid5(NAMESPACE, name))


def visual_id(name):
    return uuid.uuid5(NAMESPACE, name).hex[:20]


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def encode_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def color(value):
    return {"solid": {"color": literal("'" + value + "'")}}


def projection(name, measure=False):
    return {
        "field": {"Measure" if measure else "Column": {
            "Expression": {"SourceRef": {"Entity": TABLE}}, "Property": name,
        }},
        "queryRef": TABLE + "." + name, "nativeQueryRef": name, "active": True,
    }


def clone_visual(original, name, x, y, width, height):
    result = deepcopy(original)
    result["name"] = visual_id(name)
    result["position"] = {"x": x, "y": y, "z": 90000, "width": width, "height": height, "tabOrder": 90000}
    result.pop("isHidden", None)
    result.pop("parentGroupName", None)
    return result


def map_visual():
    data = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": visual_id("offer-connections-map"),
        "position": {"x": 334, "y": 1272, "z": 92000, "height": 522, "width": 1572, "tabOrder": 92000},
        "visual": {
            "visualType": "azureMap",
            "query": {"queryState": {
                "PathID": {"projections": [projection("Offer ID")]},
                "PointOrder": {"projections": [projection("Point order")]},
                "Y": {"projections": [projection("Latitude")]},
                "X": {"projections": [projection("Longitude")]},
                "Tooltips": {"projections": [projection(name, True) for name in (
                    "Connection referral", "Connection city", "Connection postcode", "Connection provider",
                    "Connection home", "Connection offer status", "Connection endpoint", "Connection quality",
                    "Connection straight-line km",
                )]},
            }},
            "objects": {
                "mapControls": [{"properties": {
                    "autoZoom": literal("true"), "defaultStyle": literal("'grayscale_light'"),
                    "showNavigationControls": literal("true"), "showStylePicker": literal("false"),
                }}],
                "pathLayer": [{"properties": {
                    "show": literal("true"), "color": color("#FB6540"),
                    "strokeWidth": literal("3L"), "strokeTransparency": literal("15D"),
                }}],
                "bubbleLayer": [{"properties": {
                    "show": literal("true"), "fillColor": color("#49ACB0"),
                    "bubbleRadius": literal("7L"), "clusteringEnabled": literal("false"),
                    "strokeColor": color("#FFFFFF"), "bubbleStrokeWidth": literal("2L"),
                }}],
                "legend": [{"properties": {"show": literal("false")}}],
            },
            "visualContainerObjects": {
                "title": [{"properties": {"show": literal("false")}}],
                "background": [{"properties": {"show": literal("false")}}],
                "border": [{"properties": {"show": literal("false")}}],
                "dropShadow": [{"properties": {"show": literal("false")}}],
                "general": [{"properties": {"altText": literal(
                    "'Approximate city-to-postcode connections for the selected referral. One line per offer, not a driving route. Hover for endpoint and offer details.'"
                )}}],
            },
            "drillFilterOtherVisuals": True,
        },
        "filterConfig": {"filters": [{
            "name": visual_id("offer-connection-filter"),
            "field": projection("Map connection visible", True)["field"], "type": "Advanced",
            "filter": {"Version": 2, "From": [{"Name": "m", "Entity": TABLE, "Type": 0}],
                       "Where": [{"Condition": {"Comparison": {
                           "ComparisonKind": 0,
                           "Left": {"Measure": {"Expression": {"SourceRef": {"Source": "m"}}, "Property": "Map connection visible"}},
                           "Right": {"Literal": {"Value": "1L"}},
                       }}}]}, "howCreated": "User",
        }]},
    }
    return data


def plan_changes(project):
    planned = {}

    def read(relative):
        return (project / relative).read_text(encoding="utf-8-sig")

    def put(relative, text):
        path = project / relative
        if not path.exists() or read(relative) != text:
            planned[path] = text

    fact = read(MODEL / "tables/fact_offer.tmdl")
    present = [f"\tcolumn {name}\n" in fact for name in COORDINATES]
    if any(present) and not all(present):
        raise RuntimeError("Partial endpoint columns already exist; preserve user edits and inspect first")
    if not all(present):
        columns = ""
        for name in COORDINATES:
            category = "Latitude" if name.endswith("latitude") else "Longitude"
            columns += (f"\tcolumn {name}\n\t\tdataType: double\n\t\tformatString: 0.000000\n"
                        f"\t\tdataCategory: {category}\n\t\tlineageTag: {uid(name)}\n"
                        f"\t\tsummarizeBy: none\n\t\tsourceColumn: {name}\n\n")
        marker = "\tpartition fact_offer = m"
        if fact.count(marker) != 1:
            raise RuntimeError("Expected exactly one offer import partition")
        fact = fact.replace(marker, columns + marker, 1)
    if "CoordinateColumns =" not in fact:
        old = ('\t\t\t\t    gold_fact_offer = Source{[Schema="gold",Item="fact_offer"]}[Data]\n'
               '\t\t\t\tin\n\t\t\t\t    gold_fact_offer')
        names = ", ".join('"' + name + '"' for name in COORDINATES)
        types = ", ".join('{"' + name + '", type number}' for name in COORDINATES)
        new = ('\t\t\t\t    gold_fact_offer = Source{[Schema="gold",Item="fact_offer"]}[Data],\n'
               f'\t\t\t\t    CoordinateColumns = {{{names}}},\n'
               '\t\t\t\t    WithOptionalCoordinates = Table.SelectColumns(gold_fact_offer,\n'
               '\t\t\t\t        List.Union({Table.ColumnNames(gold_fact_offer), CoordinateColumns}), MissingField.UseNull),\n'
               f'\t\t\t\t    TypedCoordinates = Table.TransformColumnTypes(WithOptionalCoordinates, {{{types}}})\n'
               '\t\t\t\tin\n\t\t\t\t    TypedCoordinates')
        if fact.count(old) != 1:
            raise RuntimeError("Offer source differs from expected saved query; do not overwrite")
        fact = fact.replace(old, new, 1)
    put(MODEL / "tables/fact_offer.tmdl", fact)

    template = Path(__file__).with_name("templates") / "offer_location_paths.tmdl"
    table_path = MODEL / "tables/Offer Location Paths.tmdl"
    table = template.read_text(encoding="utf-8")
    if (project / table_path).exists() and read(table_path) != table:
        raise RuntimeError("Map table was edited since creation; preserve it and inspect")
    put(table_path, table)
    model = read(MODEL / "model.tmdl")
    reference = "ref table 'Offer Location Paths'"
    if reference not in model:
        model = model.replace("ref role 'WMPP Dynamic Detail RLS'", reference + "\n\nref role 'WMPP Dynamic Detail RLS'", 1)
        if reference not in model:
            raise RuntimeError("Expected saved model role marker")
    put(MODEL / "model.tmdl", model)
    relationships = read(MODEL / "relationships.tmdl")
    relation_id = uid("map-offer-relationship")
    if relation_id not in relationships:
        relationships = relationships.rstrip() + (
            f"\n\nrelationship {relation_id}\n\tfromColumn: 'Offer Location Paths'.'Offer ID'\n"
            "\ttoColumn: fact_offer.offer_id\n\n"
        )
    put(MODEL / "relationships.tmdl", relationships)

    page_path = REPORT / "pages" / PAGE_ID
    page = json.loads(read(page_path / "page.json"))
    if page["displayName"] != "Offer Locations":
        raise RuntimeError("The target page is not Offer Locations")
    page["height"] = max(page["height"], 1870)

    def existing(identifier):
        return json.loads(read(page_path / "visuals" / identifier / "visual.json"))

    panel = clone_visual(existing("b2af12eb67f89f3c4c93"), "offer-connections-panel", 316, 1144, 1608, 702)
    panel["position"]["z"] = 4000
    title = clone_visual(existing("976592b5dc39f1d9aa12"), "offer-connections-title", 334, 1162, 1572, 34)
    title["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"] = "Referral city → offered provider homes"
    summary = clone_visual(existing("343f9b5f6dca3cde85c0"), "offer-connections-summary", 334, 1202, 1572, 62)
    summary["visual"]["query"] = {"queryState": {"Data": {"projections": [projection("Map connection summary", True)]}}}
    for entry in summary["visual"]["objects"].get("value", []):
        entry["properties"].update({"fontSize": literal("13D"), "fontFamily": literal("'Segoe UI'"), "fontColor": color("#625B5B")})
    summary["visual"]["visualContainerObjects"]["general"] = [{"properties": {
        "altText": literal("'Map selection guidance and distinct mapped-offer coverage. Missing coordinates and reviewed locations are not mapped.'")
    }}]
    note = clone_visual(existing("7b4a905dbf7ce68d96a1"), "offer-connections-note", 334, 1804, 1572, 32)
    note["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"] = (
        "Orange lines join city and postcode representative points; teal markers are endpoints. Approximate straight-line connections, not driving routes or exact addresses."
    )
    additions = [panel, title, summary, map_visual(), note]
    for document in additions:
        relative = page_path / "visuals" / document["name"] / "visual.json"
        if (project / relative).exists() and json.loads(read(relative)) != document:
            raise RuntimeError(f"New map visual has user edits; do not overwrite: {relative}")
        put(relative, encode_json(document))
    sidebar = existing("96f992b34676b9b26e3e")
    sidebar["position"]["height"] = page["height"] - 24
    put(page_path / "visuals/96f992b34676b9b26e3e/visual.json", encode_json(sidebar))
    interactions = page.setdefault("visualInteractions", [])
    map_id = visual_id("offer-connections-map")
    summary_id = summary["name"]
    for source in ("0da8828163bf73fd7e40", "dc1856a2578c62cbebd7", "796b6b9c07fad0271ac5",
                   "83ca4687dfc72547bf8c", "6687223bfdc5772d4688", "715b4ecf86089373c4b3", "9a14a01785aa833d2865"):
        for target in (map_id, summary_id):
            interaction = {"source": source, "target": target, "type": "DataFilter"}
            if interaction not in interactions:
                interactions.append(interaction)
    for target in ("715b4ecf86089373c4b3", "9a14a01785aa833d2865", summary_id):
        interaction = {"source": map_id, "target": target, "type": "NoFilter"}
        if interaction not in interactions:
            interactions.append(interaction)
    put(page_path / "page.json", encode_json(page))
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
        backup = project.parent / "_review" / ("offer-location-map-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
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
        manifest_path = backup / "map-manifest.json"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        for path, text in planned.items():
            if path.exists() and digest(path) != original.get(path):
                raise RuntimeError(f"Concurrent edit; preserve it: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        for path, expected in original.items():
            if path not in planned and digest(path) != expected:
                raise RuntimeError(f"Unrelated file changed during apply: {path}")
        assert not plan_changes(project), "Apply did not produce an idempotent result"
        manifest["verified"] = "Only listed map definitions changed; all other report/model file hashes unchanged (excluding .pbi cache)"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        result.update({"backup": str(backup), "verified": manifest["verified"]})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
