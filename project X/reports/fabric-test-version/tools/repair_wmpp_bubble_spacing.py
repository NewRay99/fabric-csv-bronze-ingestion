"""Correct bubble colours, text space and dropdown occlusion in client delivery."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

from apply_wmpp_owner_bubble_states import BRAND, ASSETS, RESOURCES, PRESET, NS
from apply_wmpp_navigation_icons import ICONS
from build_report_design_delivery import L, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE
from use_wmpp_dropdown_navigation import TOP, POPOVERS


def main():
    marker = REPORT.parent / "BUBBLE_SPACING_REPAIR.json"
    assert not marker.exists(), "Inspect previous repair before reapplying."
    backup = BUNDLE / "_review" / ("bubble-spacing-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    old = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    planned = {}
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    buttons = []
    pages = []
    for page_path in (REPORT / "definition/pages").glob("*/page.json"):
        page = read(page_path)
        visuals = {p: deepcopy(v) for p, v in old.items() if p.name == "visual.json" and p.parents[2] == page_path.parent}
        main_buttons = [(p, v) for p, v in visuals.items() if PRESET in json.dumps(v.get("visual", {}).get("visualContainerObjects", {}).get("stylePreset", {}))]
        if not main_buttons:
            continue
        assert len(main_buttons) == 8
        assert page["width"] == 1680
        pages.append(page["displayName"])
        # Captures the old group centres before moving them; handles copied IDs.
        frame_groups = {}
        for path, value in main_buttons:
            serialized = json.dumps(value["visual"]["objects"]["icon"])
            short = next(short for short, (_, name) in ICONS.items() if f"lucide-nav-{name}-white.svg" in serialized)
            index = next(i for i, item in enumerate(TOP) if item[0] == short)
            area = TOP[index][2]
            if area in POPOVERS:
                frame_groups[area] = (value["position"]["x"] + 36, 860 + index * 100)
            value["position"].update(x=860 + index * 100, y=8, width=96, height=108, z=400000, tabOrder=index)
            for entry in value["visual"]["objects"]["icon"]:
                entry["properties"].update(iconSize=L("32D"), topMargin=L("20L"))
            for entry in value["visual"]["objects"]["text"]:
                if "text" in entry["properties"]:
                    entry["properties"].update(fontSize=L("8D"), topMargin=L("74L"), bottomMargin=L("8L"),
                                               leftMargin=L("6L"), rightMargin=L("6L"))
            planned[path] = value
            buttons.append(value)

        for path, value in visuals.items():
            position = value["position"]
            if value.get("visual", {}).get("visualType") == "shape" and position["z"] in (300005, 300006, 300007):
                if position["z"] in (300006, 300007):
                    centre = position["x"] + position["width"] / 2
                    matches = [(area, new_x) for area, (old_centre, new_x) in frame_groups.items() if abs(centre - old_centre) < .1]
                    assert len(matches) == 1
                    _, new_x = matches[0]
                    if position["z"] == 300007:
                        position.update(x=new_x - 4, y=0, width=104, height=116)
                    else:
                        position.update(x=new_x - 4, y=54, width=104, height=92)
                    planned[path] = value
            # Identify submenu row/frame membership through the saved bookmark,
            # rather than assuming Desktop preserved hashed visual identifiers.
        for area, (_, new_x) in frame_groups.items():
            corresponding = next(v for _, v in main_buttons if f"Open {area} menu" in json.dumps(v))
            bid = corresponding["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]["bookmark"]["expr"]["Literal"]["Value"].strip("'")
            bookmark = old[REPORT / "definition/bookmarks" / (bid + ".bookmark.json")]
            section = bookmark["explorationState"]["sections"][page["name"]]
            for vid, state in section["visualContainers"].items():
                if state["singleVisual"].get("display", {}).get("mode") == "hidden":
                    continue
                path = page_path.parent / "visuals" / vid / "visual.json"
                value = visuals[path]
                position = value["position"]
                if value.get("visual", {}).get("visualType") == "actionButton" and 300020 <= position["z"] <= 300030:
                    position.update(x=min(new_x, 1346), y=position["y"] + 18)
                    planned[path] = value
                elif value.get("visual", {}).get("visualType") == "shape" and position["z"] == 300005:
                    position.update(x=min(new_x, 1346) - 12, y=124)
                    planned[path] = value

        for path, value in visuals.items():
            position = value["position"]
            if "visualGroup" in value and value["visualGroup"].get("displayName", "").endswith("| Filters drawer"):
                position.update(x=438, y=124)
                planned[path] = value
            elif value.get("visual", {}).get("visualType") == "actionButton" and position["x"] == 960 and position["y"] == 0 and position["width"] == 88:
                position.update(x=748, z=400020)
                planned[path] = value

    ET.register_namespace("", NS[1:-1])
    assets = {}
    for state in ("default", "active", "hover", "disabled"):
        colour = "#E3DADA" if state == "disabled" else "#EF7911"
        root = ET.Element(NS + "svg", dict(width="96", height="108", viewBox="0 0 96 108"))
        if state in ("active", "hover"):
            ET.SubElement(root, NS + "rect", dict(x="2", y="2", width="92", height="104", rx="32", fill="#FCA356"))
        ET.SubElement(root, NS + "circle", dict(cx="48", cy="36", r="31", fill=colour))
        assets[f"wmpp-bubble-background-{state}.svg"] = ET.tostring(root, encoding="unicode") + "\n"
        for short, (_, name) in ICONS.items():
            full = deepcopy(root)
            icon = ET.fromstring((BRAND / "icons" / f"lucide-nav-{name}-white.svg").read_text())
            group = ET.SubElement(full, NS + "g", {
                "transform": "translate(32 20) scale(1.333333333)", "fill": "none", "stroke": "#FFFFFF",
                "stroke-width": "2", "stroke-linecap": "round", "stroke-linejoin": "round"})
            for child in icon:
                group.append(deepcopy(child))
            assets[f"wmpp-bubble-{short.lower()}-{state}.svg"] = ET.tostring(full, encoding="unicode") + "\n"
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        preset = theme["visualStyles"]["actionButton"][PRESET]
        preset["icon"][0].update(iconSize=32, topMargin=20)
        preset["text"][0].update(fontSize=8, topMargin=74, bottomMargin=8, leftMargin=6, rightMargin=6)
        planned[path] = theme

    changed = []
    def retain(path):
        if path.exists():
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        changed.append(str(path.relative_to(ROOT)))
    assert len(buttons) == 128
    for path, value in planned.items():
        if path in old:
            assert value.get("visual", {}).get("query") == old[path].get("visual", {}).get("query")
            assert value.get("filterConfig") == old[path].get("filterConfig")
            assert value.get("visual", {}).get("visualContainerObjects", {}).get("visualLink") == old[path].get("visual", {}).get("visualContainerObjects", {}).get("visualLink")
        retain(path)
        save(path, value)
    for name, contents in assets.items():
        for path in (ASSETS / name, RESOURCES / name):
            retain(path)
            path.write_text(contents, encoding="utf-8")
    assert all(read(path) == value for path, value in old.items() if path not in planned)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = dict(backup=str(backup), pages=pages, buttons=128, button_size=[96, 108],
                  navigation_origin=[860, 8], pitch=100, filter_origin=[748, 0],
                  filter_drawer_origin=[438, 124], main_button_z=400000,
                  active_and_hover_colours=["#EF7911", "#FCA356"],
                  bookmark_actions_queries_and_model_unchanged=True,
                  native_render_verified=False, modified_paths=changed)
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
