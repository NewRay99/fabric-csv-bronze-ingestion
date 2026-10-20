"""Read-only saved-report journey inventory; not a Desktop rendering test."""

import argparse
from collections import defaultdict
import json
from pathlib import Path
import re


def scalar(value):
    return value.get("expr", {}).get("Literal", {}).get("Value", "").strip("'")


def field_refs(node):
    if isinstance(node, dict):
        for kind in ("Column", "Measure"):
            item = node.get(kind, {})
            entity = item.get("Expression", {}).get("SourceRef", {}).get("Entity")
            if entity and item.get("Property"):
                yield kind, entity, item["Property"]
        for child in node.values():
            yield from field_refs(child)
    elif isinstance(node, list):
        for child in node:
            yield from field_refs(child)


def unquote(name):
    return name.strip("'").replace("''", "'")


def inventory(bundle, overrides=None):
    overrides = overrides or {}

    def read(path):
        return overrides[path] if path in overrides else path.read_text(encoding="utf-8-sig")

    definition = bundle / "SM_WMPP_v16.Report/definition"
    tables = {}
    table_root = bundle / "SM_WMPP_v16.SemanticModel/definition/tables"
    for path in sorted(
        set(table_root.glob("*.tmdl")) | {p for p in overrides if p.parent == table_root}
    ):
        text = read(path)
        table = unquote(re.search(r"^table (.+)$", text, re.M)[1])
        tables[table] = {
            kind: set(
                unquote(x) for x in re.findall(r"^\t" + kind + r" (.+?)(?: =.*)?$", text, re.M)
            )
            for kind in ("column", "measure")
        }
    bookmarks = {
        path.name.split(".")[0]: json.loads(read(path))
        for path in (definition / "bookmarks").glob("*.bookmark.json")
    }
    pages = {}
    missing = []
    for pp in (definition / "pages").glob("*/page.json"):
        p = json.loads(read(pp))
        entries = []
        visual_paths = set((pp.parent / "visuals").glob("*/visual.json")) | {
            path
            for path in overrides
            if path.name == "visual.json" and path.parents[2] == pp.parent
        }
        for path in sorted(visual_paths):
            v = json.loads(read(path))
            visual = v.get("visual", {})
            refs = sorted(set(field_refs(v)))
            for kind, entity, prop in refs:
                if prop not in tables.get(entity, {}).get(kind.lower(), set()):
                    missing.append([p["displayName"], v["name"], kind, entity, prop])
            props = visual.get("visualContainerObjects", {})
            labels = [
                scalar(x["properties"].get("text", {}))
                for x in visual.get("objects", {}).get("text", [])
            ]
            actions = []
            for entry in props.get("visualLink", []):
                properties = entry["properties"]
                action = {
                    k: scalar(val)
                    for k, val in properties.items()
                    if k
                    in {"type", "bookmark", "navigationSection", "drillthroughSection", "tooltip"}
                }
                if action.get("bookmark") in bookmarks:
                    bm = bookmarks[action["bookmark"]]
                    action["target_page"] = bm.get("explorationState", {}).get("activeSection")
                actions.append(action)
            entries.append(
                {
                    "id": v["name"],
                    "type": visual.get("visualType", "group"),
                    "title": next(
                        (scalar(x["properties"].get("text", {})) for x in props.get("title", [])),
                        "",
                    ),
                    "label": next((x for x in labels if x), ""),
                    "position": v.get("position", {}),
                    "hidden": v.get("isHidden", False),
                    "parent": v.get("parentGroupName"),
                    "fields": refs,
                    "query_fields": sorted(set(field_refs(visual.get("query", {})))),
                    "actions": actions,
                }
            )
        duplicates = defaultdict(list)
        for v in entries:
            if v["query_fields"]:
                duplicates[tuple(map(tuple, v["query_fields"]))].append(v["id"])
        pages[p["name"]] = {
            "name": p["displayName"],
            "visibility": p.get("visibility", "Visible"),
            "width": p["width"],
            "height": p["height"],
            "binding": p.get("pageBinding"),
            "visuals": entries,
            "repeated_query_fields": [ids for ids in duplicates.values() if len(ids) > 1],
        }
    action_errors = []
    for p in pages.values():
        for v in p["visuals"]:
            for a in v["actions"]:
                if a.get("bookmark") and a["bookmark"] not in bookmarks:
                    action_errors.append([p["name"], v["id"], "bookmark", a["bookmark"]])
                if a.get("navigationSection") and a["navigationSection"] not in pages:
                    action_errors.append([p["name"], v["id"], "page", a["navigationSection"]])
                if a.get("drillthroughSection") and a["drillthroughSection"] not in pages:
                    action_errors.append(
                        [p["name"], v["id"], "drillthrough", a["drillthroughSection"]]
                    )
    return {
        "project": str(bundle),
        "pages": pages,
        "missing_fields": missing,
        "broken_actions": action_errors,
        "table_count": len(tables),
        "measure_count": sum(len(t["measure"]) for t in tables.values()),
        "bookmark_count": len(bookmarks),
        "runtime_verified": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--page")
    args = parser.parse_args()
    audit = inventory(args.project.resolve())
    if args.page:
        pages = [p for p in audit["pages"].values() if args.page.lower() in p["name"].lower()]
        for p in pages:
            print(p["name"], p["visibility"], p["width"], p["height"])
            for v in p["visuals"]:
                if v["query_fields"] or (v["actions"] and v["position"].get("y", 0) > 500):
                    print(json.dumps(v, ensure_ascii=False))
    else:
        print(json.dumps({k: v for k, v in audit.items() if k != "pages"}, indent=2))
        for p in audit["pages"].values():
            print(
                p["name"],
                p["visibility"],
                "visuals",
                len(p["visuals"]),
                "repeated query groups",
                len(p["repeated_query_fields"]),
            )


if __name__ == "__main__":
    main()
