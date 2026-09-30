"""Finish dropdown colours, white open-state joins and icon baseline.

Open-menu button variants use display-only bookmark visibility, avoiding an
opaque canvas-colour rectangle over the connected white surround.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

from apply_wmpp_owner_bubble_states import BRAND, ASSETS, RESOURCES, PRESET, NS
from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE


def main():
    marker = REPORT.parent / "NAVIGATION_MENU_FINISH.json"
    assert not marker.exists(), "Inspect the saved finish before reapplying."
    backup = BUNDLE / "_review" / ("menu-finish-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    original = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    working = deepcopy(original)
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    bookdir = REPORT / "definition/bookmarks"
    variants = {}
    menu_bookmarks = {}
    row_count = 0
    for page_path in (REPORT / "definition/pages").glob("*/page.json"):
        pid = page_path.parent.name
        for path, value in list(working.items()):
            if path.name != "visual.json" or path.parents[2] != page_path.parent:
                continue
            visual = value.get("visual", {})
            if visual.get("visualType") != "actionButton":
                continue
            containers = visual.get("visualContainerObjects", {})
            if PRESET in json.dumps(containers.get("stylePreset", {})):
                for entry in visual["objects"]["icon"]:
                    entry["properties"]["topMargin"] = L("24L")
                props = containers["visualLink"][0]["properties"]
                bookmark_id = props["bookmark"]["expr"]["Literal"]["Value"].strip("'")
                target = working[bookdir / (bookmark_id + ".bookmark.json")]
                if not target["displayName"].endswith(" menu"):
                    continue
                twin = deepcopy(value)
                twin_id = ident("wmpp-open-menu-button:" + pid + ":" + value["name"])
                twin.update(name=twin_id, isHidden=True)
                twin["position"]["z"] = 400001
                twin["visual"]["visualContainerObjects"]["stylePreset"] = obj(name=L("'WMPP Open Menu Bubble'"))
                for entry in twin["visual"]["objects"]["fill"]:
                    entry["properties"]["fillColor"] = fill("#FFFFFF")
                    if entry.get("selector", {}).get("id") == "default":
                        image = entry["properties"]["image"]["image"]
                        image["name"] = L("'wmpp-bubble-background-active.svg'")
                        image["url"]["expr"]["ResourcePackageItem"]["ItemName"] = "wmpp-bubble-background-active.svg"
                # Clicking an already-open main button closes its submenu.
                close_id = ident(f"wmpp-dropdown-bookmark:{pid}:close")
                twin["visual"]["visualContainerObjects"]["visualLink"][0]["properties"].update(
                    bookmark=L(quoted(close_id)), tooltip=L("'Close menu'"))
                working[path.parent.parent / twin_id / "visual.json"] = twin
                variants.setdefault(pid, {})[value["name"]] = twin_id
                menu_bookmarks[bookmark_id] = (pid, value["name"])
            elif 300020 <= value["position"]["z"] <= 300030:
                # Only dropdown rows, never other visible buttons in bookmarks.
                row_count += 1
                props = containers["visualLink"][0]["properties"]
                target_id = props["bookmark"]["expr"]["Literal"]["Value"].strip("'")
                target = working[bookdir / (target_id + ".bookmark.json")]
                active = target["displayName"].startswith("Go to ") and target["explorationState"]["activeSection"] == pid
                for entry in visual["objects"]["fill"]:
                    state = entry.get("selector", {}).get("id", "default")
                    colour = "#FCA356" if state in ("hover", "selected") or (active and state == "default") else "#FFFFFF"
                    if "fillColor" in entry["properties"]:
                        entry["properties"]["fillColor"] = fill(colour)
                containers["stylePreset"] = obj(name=L("'WMPP Navigation Dropdown'"))

    for path, bookmark in list(working.items()):
        if not path.name.endswith(".bookmark.json"):
            continue
        active = menu_bookmarks.get(bookmark["name"])
        for pid, section in bookmark["explorationState"].get("sections", {}).items():
            states = section.get("visualContainers", {})
            if not any(vid in states for vid in variants.get(pid, {})):
                continue
            for main_id, twin_id in variants[pid].items():
                opened = active == (pid, main_id)
                if main_id in states:
                    if opened:
                        states[main_id]["singleVisual"]["display"] = {"mode": "hidden"}
                    else:
                        states[main_id]["singleVisual"].pop("display", None)
                states[twin_id] = {"singleVisual": {"visualType": "actionButton", "objects": {}}}
                if not opened:
                    states[twin_id]["singleVisual"]["display"] = {"mode": "hidden"}
                if bookmark.get("options", {}).get("applyOnlyToTargetVisuals"):
                    targets = bookmark["options"]["targetVisualNames"]
                    if twin_id not in targets:
                        targets.append(twin_id)

    # Previous spacing migration accidentally included the journey toggle among
    # submenu rows. Restore its pre-migration position, not any data/formatting.
    previous = read(REPORT.parent / "BUBBLE_SPACING_REPAIR.json")
    journey_id = ident("wmpp-layout:78d576b289e5fe3d2af6:journey-open")
    journey_path = REPORT / "definition/pages/78d576b289e5fe3d2af6/visuals" / journey_id / "visual.json"
    prior_path = Path(previous["backup"]) / journey_path.relative_to(ROOT)
    if journey_path in working and working[journey_path]["position"]["x"] == 1346 and working[journey_path]["position"]["y"] == 496:
        working[journey_path]["position"] = read(prior_path)["position"]

    extra = {}
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        styles = theme["visualStyles"]["actionButton"]
        styles[PRESET]["icon"][0]["topMargin"] = 24
        styles["WMPP Open Menu Bubble"] = deepcopy(styles[PRESET])
        styles["WMPP Open Menu Bubble"]["fill"][0]["fillColor"] = {"solid": {"color": "#FFFFFF"}}
        styles["WMPP Navigation Dropdown"] = {
            "fill": [{"show": True, "fillColor": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}],
            "text": [{"show": True, "fontFamily": "Segoe UI", "fontSize": 11,
                      "fontColor": {"solid": {"color": "#2B2B2C"}}}],
            "outline": [{"show": False}],
        }
        extra[path] = theme
    assets = {}
    ET.register_namespace("", NS[1:-1])
    for path in ASSETS.glob("wmpp-bubble-*.svg"):
        root = ET.fromstring(path.read_text())
        group = root.find(NS + "g")
        if group is None:
            continue
        assert group.attrib["transform"] == "translate(32 20) scale(1.333333333)"
        group.set("transform", "translate(32 24) scale(1.333333333)")
        contents = ET.tostring(root, encoding="unicode") + "\n"
        assets[path] = contents
        assets[RESOURCES / path.name] = contents

    assert sum(map(len, variants.values())) == 64
    assert row_count == 272
    planned = {p: v for p, v in working.items() if p not in original or v != original[p]}
    planned.update(extra)
    for path, value in original.items():
        if path.name == "visual.json":
            assert working[path].get("visual", {}).get("query") == value.get("visual", {}).get("query")
            assert working[path].get("filterConfig") == value.get("filterConfig")
            assert working[path].get("visual", {}).get("visualContainerObjects", {}).get("visualLink") == value.get("visual", {}).get("visualContainerObjects", {}).get("visualLink")

    changed = []
    def retain(path):
        if path.exists():
            destination = backup / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        changed.append(str(path.relative_to(ROOT)))
    for path, value in planned.items():
        retain(path)
        save(path, value)
    for path, contents in assets.items():
        retain(path)
        path.write_text(contents, encoding="utf-8")
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in protected.items())
    result = dict(backup=str(backup), dropdown_rows=row_count, open_menu_variants=64,
                  icon_shift_px=4, dropdown_highlight="#FCA356", open_menu_surround="#FFFFFF",
                  semantic_model_unchanged=True, desktop_render_verified=False, modified_paths=changed)
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
