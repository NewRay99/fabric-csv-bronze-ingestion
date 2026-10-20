"""Restore source referral pages alongside enhanced pages and add native navigation.

Only the client-deliverable report is edited. Original report/model sources stay
untouched. Source pages get distinct IDs so enhanced views are not overwritten.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from apply_report_soft_glow import DATA_KINDS, CHART_KINDS, CHART_PADDING, shadow_properties

ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "reports/client-deliverables/WMPP v16"
SOURCE = ROOT / "reports/current/WMPP v16/RPT WMPP v16/WMPP_DASHBOARD_v16.Report"
REPORT = BUNDLE / "SM WMPP v16 updated/SM_WMPP_v16.Report"
RESTORED = {
    "f028a4be56d03e8404d7": ident("wmpp-original-referrals"),
    "f3070e87127b751f89d4": ident("wmpp-original-referral-single"),
}
MENU_HEIGHT = 104
GROUPS = [
    ("Home", [("Home", "364f2cdd67ba7822850c")]),
    (
        "Referrals",
        [
            ("REFERRALS", RESTORED["f028a4be56d03e8404d7"]),
            ("Single referral · original", RESTORED["f3070e87127b751f89d4"]),
            ("Referral explorer", "f3070e87127b751f89d4"),
            ("Geography", "f028a4be56d03e8404d7"),
            ("Snapshots", "dd3a58c056d723048dbf"),
            ("Referral detail", "4cad3706fca6451c66b8"),
        ],
    ),
    (
        "Offers",
        [
            ("OFFERS OVERVIEW", "1f33996970651e846183"),
            ("DRAFT OFFERS", "ad5ab4aa6928c9178a35"),
            ("Offer locations", "1cd52e9c7e4016f342ce"),
        ],
    ),
    (
        "Providers",
        [
            ("PROVIDER SINGLE VIEW", "08ef33dc6a87d1b14392"),
            ("Provider & placement supply", "510f9f9501ccc5ae8a74"),
        ],
    ),
    ("IPAs", [("IPA OVERVIEW", "58d36c775c032a42e01b")]),
    (
        "Performance",
        [("Board dashboard", "5038cffdd48af9a80dd1"), ("Target & urgency", "6ae319c8916a5d63a4ff")],
    ),
    ("Requirements", [("REQUIREMENT MATRIX", "b95eb4c0b53cd8c60710")]),
]


def replace_ids(value, mapping):
    if isinstance(value, str):
        if value in mapping:
            return mapping[value]
        if value.startswith("'") and value.endswith("'") and value[1:-1] in mapping:
            return quoted(mapping[value[1:-1]])
        return value
    if isinstance(value, dict):
        return {mapping.get(k, k): replace_ids(v, mapping) for k, v in value.items()}
    if isinstance(value, list):
        return [replace_ids(v, mapping) for v in value]
    return value


def get_literal(value):
    return value.get("expr", {}).get("Literal", {}).get("Value", "").strip("'")


def walk(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def restore_pages():
    report_data = read(REPORT / "definition/report.json")
    source_report = read(SOURCE / "definition/report.json")
    source_packages = {p["name"]: p for p in source_report["resourcePackages"]}
    packages = {p["name"]: p for p in report_data["resourcePackages"]}
    theme_path = REPORT / "StaticResources/RegisteredResources/WMPP_Theme.json"
    theme = read(theme_path)
    source_theme = source_report["themeCollection"]["customTheme"]
    source_theme_item = next(
        i
        for i in source_packages[source_theme["type"]]["items"]
        if i["name"] == source_theme["name"]
    )
    original_theme = read(
        SOURCE / "StaticResources" / source_theme["type"] / source_theme_item["path"]
    )
    source_bookmarks = {}
    docs = []
    for old_id, new_id in RESTORED.items():
        destination = REPORT / "definition/pages" / new_id
        if destination.exists():
            raise ValueError(
                "Restored page already exists; preserve it and update the menu separately"
            )
        for path in (SOURCE / "definition/pages" / old_id).rglob("*.json"):
            data = read(path)
            for node in walk(data):
                if "bookmark" in node and get_literal(node.get("type", {})) == "Bookmark":
                    bid = get_literal(node["bookmark"])
                    source_bookmarks[bid] = ident("restored-bookmark:" + bid)
            docs.append(
                (destination / path.relative_to(SOURCE / "definition/pages" / old_id), data)
            )
    mapping = RESTORED | source_bookmarks
    for path, original in docs:
        value = replace_ids(original, mapping)
        if path.name == "page.json":
            value.setdefault("objects", {})["background"] = obj(
                color=fill("#F8F5F1"), transparency=L("0D")
            )
            value["objects"]["outspace"] = obj(color=fill("#F8F5F1"), transparency=L("0D"))
            value.setdefault("annotations", []).append(
                {"name": "wmppSourceReport", "value": str(SOURCE.relative_to(ROOT))}
            )
        visual = value.get("visual")
        if visual:
            containers = visual.setdefault("visualContainerObjects", {})
            kind = visual["visualType"]
            for style in containers.get("stylePreset", []):
                name = get_literal(style["properties"]["name"])
                if name.startswith("WMPP") and name not in theme["visualStyles"].get(kind, {}):
                    theme["visualStyles"].setdefault(kind, {})[name] = deepcopy(
                        original_theme["visualStyles"][kind][name]
                    )
            position = value["position"]
            if kind in DATA_KINDS and position["width"] >= 100 and position["height"] >= 70:
                containers["background"] = obj(
                    show=L("true"), color=fill("#FFFFFF"), transparency=L("0D")
                )
                containers["border"] = obj(
                    show=L("true"), radius=L("14D"), width=L("1D"), color=fill("#FFFFFF")
                )
                containers["dropShadow"] = shadow_properties()
                if kind in CHART_KINDS:
                    containers["padding"] = obj(
                        **{k: L(str(v) + "D") for k, v in CHART_PADDING.items()}
                    )
            if kind == "textbox":
                containers["border"] = obj(show=L("false"))
                containers["dropShadow"] = obj(show=L("false"))
        # Copy only referenced resources, remapping filename collisions safely.
        for node in walk(value):
            ref = node.get("ResourcePackageItem")
            if not ref:
                continue
            package_name, name = ref["PackageName"], ref["ItemName"]
            source_package = source_packages[package_name]
            item = next(i for i in source_package["items"] if i["name"] == name)
            source_file = SOURCE / "StaticResources" / package_name / item["path"]
            package = packages.setdefault(
                package_name, {"name": package_name, "type": source_package["type"], "items": []}
            )
            existing = next((i for i in package["items"] if i["name"] == name), None)
            if existing:
                existing_file = REPORT / "StaticResources" / package_name / existing["path"]
                if (
                    existing_file.exists()
                    and existing_file.read_bytes() == source_file.read_bytes()
                ):
                    continue
                new_name = "original-" + ident(name) + source_file.suffix
                item = dict(item, name=new_name, path=new_name)
                ref["ItemName"] = new_name
            else:
                item = dict(item)
            target = REPORT / "StaticResources" / package_name / item["path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_file, target)
            if not any(i["name"] == item["name"] for i in package["items"]):
                package["items"].append(item)
        save(path, value)
    report_data["resourcePackages"] = list(packages.values())
    report_data["publicCustomVisuals"] = list(
        dict.fromkeys(
            report_data.get("publicCustomVisuals", [])
            + source_report.get("publicCustomVisuals", [])
        )
    )
    save(REPORT / "definition/report.json", report_data)
    save(theme_path, theme)
    metadata_path = REPORT / "definition/bookmarks/bookmarks.json"
    metadata = read(metadata_path)
    for old_id, new_id in source_bookmarks.items():
        value = replace_ids(
            read(SOURCE / "definition/bookmarks" / (old_id + ".bookmark.json")), mapping
        )
        value["name"] = new_id
        save(REPORT / "definition/bookmarks" / (new_id + ".bookmark.json"), value)
        metadata["items"].append({"name": new_id})
    save(metadata_path, metadata)
    return source_bookmarks


def menu_button(page_id, key, label, destination, x, y, width, active=False, secondary=False):
    background = "#EEDCE3" if active and secondary else "#A33B61" if active else "#FFFFFF"
    ink = "#FFFFFF" if active and not secondary else "#2B2427"
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": ident("wmpp-menu:" + page_id + ":" + key),
        "position": {
            "x": x,
            "y": y,
            "width": width,
            "height": 36,
            "z": 90000,
            "tabOrder": 0 if not secondary else 10,
        },
        "visual": {
            "visualType": "actionButton",
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": {
                **{
                    k: obj(show=L("false"))
                    for k in ("title", "subTitle", "visualHeader", "dropShadow")
                },
                "general": obj(altText=L(quoted("Navigation: " + label))),
                "background": obj(show=L("true"), color=fill(background), transparency=L("0D")),
                "border": obj(
                    show=L("true"), radius=L("8D"), width=L("1D"), color=fill(background)
                ),
                "padding": obj(top=L("4D"), bottom=L("4D"), left=L("8D"), right=L("8D")),
                "visualLink": obj(
                    show=L("true"),
                    type=L("'PageNavigation'"),
                    navigationSection=L(quoted(destination)),
                    tooltip=L(
                        quoted(
                            "Open "
                            + label
                            + ". Use referral drillthrough to carry a selected record; menu navigation does not select a referral."
                        )
                    ),
                ),
            },
            "objects": {
                **{k: obj(show=L("false")) for k in ("fill", "outline", "icon", "shadow", "glow")},
                "text": [
                    {
                        "selector": {"id": "default"},
                        "properties": {
                            "show": L("true"),
                            "text": L(quoted(label)),
                            "fontFamily": L("'Segoe UI'"),
                            "fontSize": L("10D"),
                            "bold": L("true"),
                            "fontColor": fill(ink),
                            "horizontalAlignment": L("'center'"),
                            "verticalAlignment": L("'middle'"),
                        },
                    }
                ],
            },
        },
    }


def add_menu():
    pages = {p.parent.name: read(p) for p in REPORT.glob("definition/pages/*/page.json")}
    content_ids = {page_id for _, items in GROUPS for _, page_id in items}
    assert content_ids <= set(pages)
    shifted = {}
    retired = {}
    for page_id in content_ids:
        page = pages[page_id]
        path = REPORT / "definition/pages" / page_id
        assert not any(a.get("name") == "wmppMenuHeight" for a in page.get("annotations", [])), (
            "Menu already installed"
        )
        originals = list(path.glob("visuals/*/visual.json"))
        shifted[page_id] = set()
        retired[page_id] = set()
        for file in originals:
            value = read(file)
            if not value.get("parentGroupName"):
                value["position"]["y"] += MENU_HEIGHT
                shifted[page_id].add(value["name"])
            visual = value.get("visual", {})
            containers = visual.get("visualContainerObjects", {})
            alt = get_literal(
                containers.get("general", [{}])[0].get("properties", {}).get("altText", {})
            )
            for link in containers.get("visualLink", []):
                prop = link.get("properties", {})
                if (
                    get_literal(prop.get("type", {})) == "PageNavigation"
                    and get_literal(prop.get("navigationSection", {})) in content_ids
                ):
                    value["isHidden"] = True
                    retired[page_id].add(value["name"])
            if alt.startswith("navlabel-"):
                value["isHidden"] = True
                retired[page_id].add(value["name"])
            save(file, value)
        page["height"] += MENU_HEIGHT
        page.setdefault("annotations", []).append(
            {"name": "wmppMenuHeight", "value": str(MENU_HEIGHT)}
        )
        save(path / "page.json", page)
        active_group, children = next(
            (name, items) for name, items in GROUPS if page_id in {i for _, i in items}
        )
        gap, margin = 8, 24
        width = (page["width"] - 2 * margin - (len(GROUPS) - 1) * gap) / len(GROUPS)
        for index, (label, items) in enumerate(GROUPS):
            value = menu_button(
                page_id,
                "main-" + label,
                label,
                items[0][1],
                margin + index * (width + gap),
                8,
                width,
                label == active_group,
            )
            value["position"]["tabOrder"] = index
            save(path / "visuals" / value["name"] / "visual.json", value)
        width = min(300, (page["width"] - 2 * margin - (len(children) - 1) * gap) / len(children))
        for index, (label, destination) in enumerate(children):
            value = menu_button(
                page_id,
                "sub-" + destination,
                label,
                destination,
                margin + index * (width + gap),
                52,
                width,
                page_id == destination,
                True,
            )
            value["position"]["tabOrder"] = len(GROUPS) + index
            save(path / "visuals" / value["name"] / "visual.json", value)
    # Saved display bookmarks must not put content back under the menu or reveal
    # obsolete navigation controls. Selection/filter payloads remain unchanged.
    for file in REPORT.glob("definition/bookmarks/*.bookmark.json"):
        bookmark = read(file)
        changed = False
        for page_id, section in bookmark.get("explorationState", {}).get("sections", {}).items():
            if page_id not in shifted:
                continue
            for visual_id, state in section.get("visualContainers", {}).items():
                if (
                    visual_id in shifted[page_id]
                    and isinstance(state.get("position"), dict)
                    and "y" in state["position"]
                ):
                    state["position"]["y"] += MENU_HEIGHT
                    changed = True
                if visual_id in retired[page_id]:
                    state.setdefault("singleVisual", {}).setdefault("display", {})["mode"] = (
                        "hidden"
                    )
                    changed = True
        if changed:
            save(file, bookmark)
    metadata_path = REPORT / "definition/pages/pages.json"
    metadata = read(metadata_path)
    order = [page_id for _, items in GROUPS for _, page_id in items]
    metadata["pageOrder"] = order + [
        page_id for page_id in metadata["pageOrder"] if page_id not in content_ids
    ]
    save(metadata_path, metadata)
    return len(content_ids)


def main():
    backup = BUNDLE / "_review" / ("navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copytree(REPORT / "definition", backup / "definition")
    shutil.copytree(REPORT / "StaticResources", backup / "resources")
    models = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for m in REPORT.parent.glob("*.SemanticModel")
        for p in m.rglob("*")
        if p.is_file()
    }
    bookmarks = restore_pages()
    pages = add_menu()
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in models.items())
    for old_id, new_id in RESTORED.items():
        for path in (SOURCE / "definition/pages" / old_id).glob("visuals/*/visual.json"):
            old = read(path)
            new = read(
                REPORT / "definition/pages" / new_id / "visuals" / path.parent.name / "visual.json"
            )
            assert old.get("visual", {}).get("query") == new.get("visual", {}).get("query")
            assert old.get("filterConfig") == new.get("filterConfig")
    save(
        backup / "verification.json",
        {
            "restored_pages": RESTORED,
            "cloned_bookmarks": bookmarks,
            "menu_pages": pages,
            "source_queries_preserved": True,
            "models_unchanged": True,
            "native_render_verified": False,
        },
    )
    print(
        json.dumps(
            {
                "backup": str(backup),
                "restored_pages": RESTORED,
                "cloned_bookmarks": bookmarks,
                "menu_pages": pages,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
