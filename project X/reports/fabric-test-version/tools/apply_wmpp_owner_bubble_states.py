"""Apply owner-provided bubble colours without restoring the withdrawn rail.

Native icons remain enabled. Separate icon-free fill images draw the silhouette;
fill opacity is explicit. Labels are inside the button so they share its hover.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

from apply_wmpp_navigation_icons import ICONS
from build_report_design_delivery import L, fill, obj, quoted, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE
from use_wmpp_dropdown_navigation import TOP, POPOVERS

BRAND = ROOT / "assets/brand-pack"
ASSETS = BRAND / "icons/navigation-bubbles"
RESOURCES = REPORT / "StaticResources/RegisteredResources"
PRESET = "WMPP Owner Bubble Navigation"
STATES = ("default", "hover", "selected", "disabled")
NS = "{http://www.w3.org/2000/svg}"


def image_ref(name):
    return {"image": {"name": L(quoted(name)), "scaling": L("'Fit'"),
                      "url": {"expr": {"ResourcePackageItem": {
                          "PackageName": "RegisteredResources", "PackageType": 1, "ItemName": name}}}}}


def main():
    marker = REPORT.parent / "OWNER_BUBBLE_NAVIGATION.json"
    assert not marker.exists(), "Inspect the existing migration before reapplying."
    backup = BUNDLE / "_review" / ("owner-bubble-states-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    sources = {s: (ASSETS / f"wmpp-bubble-ho-{s}.svg").read_text(encoding="utf-8") for s in ("active", "hover")}
    svg = {s: ET.fromstring(value) for s, value in sources.items()}
    hover_peach = svg["hover"].find(NS + "rect").attrib["fill"].upper()
    resting = svg["hover"].find(NS + "circle").attrib["fill"].upper()
    active_peach = svg["active"].find(NS + "rect").attrib["fill"].upper()
    active_circle = svg["active"].find(NS + "circle").attrib["fill"].upper()
    assert all(root.attrib["viewBox"] == "0 0 72 96" for root in svg.values())
    ET.register_namespace("", NS[1:-1])
    planned = {}
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    definitions = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    asset_text = {}
    for state in ("default", "active", "hover", "disabled"):
        background = deepcopy(svg["hover" if state == "hover" else "active"])
        for child in list(background):
            if child.tag == NS + "g" or (state in ("default", "disabled") and child.tag == NS + "rect"):
                background.remove(child)
        if state in ("default", "disabled"):
            background.find(NS + "circle").set("fill", resting if state == "default" else "#E3DADA")
        asset_text[f"wmpp-bubble-background-{state}.svg"] = ET.tostring(background, encoding="unicode") + "\n"
        for short in ICONS:
            name = f"wmpp-bubble-{short.lower()}-{state}.svg"
            if short == "HO" and state in sources:
                asset_text[name] = sources[state]
                continue
            full = deepcopy(background)
            source = ET.fromstring((BRAND / "icons" / f"lucide-nav-{ICONS[short][1]}-white.svg").read_text())
            group = deepcopy(svg["hover"].find(NS + "g"))
            for child in list(group):
                group.remove(child)
            for child in source:
                group.append(deepcopy(child))
            full.append(group)
            asset_text[name] = ET.tostring(full, encoding="unicode") + "\n"

    captions = set()
    count = 0
    affected = []
    active_by_name = {
        "WMPP Homepage": "HO", "Draft Offers": "DO", "IPA Overview": "IO",
        "Requirement Matrix Overview": "RM", "Board Dashboard": "PF",
        "Target & Urgency Performance": "PF", "Provider & Placement Supply": "PR",
        "Provider Single View": "PR", "Offers Overview": "OO", "Offer Locations": "OO",
    }
    for page_path in (REPORT / "definition/pages").glob("*/page.json"):
        page = read(page_path)
        values = {p: d for p, d in definitions.items() if p.name == "visual.json" and p.parents[2] == page_path.parent}
        buttons = []
        for p, value in values.items():
            if value.get("isHidden") or value.get("visual", {}).get("visualType") != "actionButton" or value["position"]["y"] >= 100:
                continue
            contents = json.dumps(value["visual"].get("objects", {}).get("icon", {}))
            matches = [short for short, (_, icon) in ICONS.items() if f"lucide-nav-{icon}-white.svg" in contents]
            if matches:
                assert len(matches) == 1
                buttons.append((p, value, matches[0]))
        if not buttons:
            continue
        assert len(buttons) == 8, (page["displayName"], len(buttons))
        active_short = active_by_name.get(page["displayName"], "R")
        affected.append(page["displayName"])
        for path, old, short in buttons:
            index = next(i for i, item in enumerate(TOP) if item[0] == short)
            label = ICONS[short][0] + (" ▾" if TOP[index][2] in POPOVERS else "")
            active = short == active_short
            value = deepcopy(old)
            value["position"].update(x=1069 + index * 74, y=8, width=72, height=96, tabOrder=index)
            objects = value["visual"]["objects"]
            objects["shape"] = obj(tileShape=L("'rectangle'"), roundEdge=L("0L")) + [
                {"selector": {"id": s}, "properties": {"tileShape": L("'rectangle'"), "roundEdge": L("0L")}} for s in STATES]
            objects["fill"] = obj(show=L("true")) + [
                {"selector": {"id": s}, "properties": {
                    "show": L("true"), "fillColor": fill("#F8F5F1"), "transparency": L("0D"),
                    "image": image_ref("wmpp-bubble-background-" + (
                        "hover" if s == "hover" else "disabled" if s == "disabled" else "active" if active or s == "selected" else "default"
                    ) + ".svg"),
                }} for s in STATES]
            # Keep a separate, directly configured icon visible in every state.
            icon = deepcopy(objects["icon"][0]["properties"])
            icon.update(show=L("true"), shapeType=L("'custom'"), placement=L("'custom'"),
                        horizontalAlignment=L("'center'"), verticalAlignment=L("'top'"), iconSize=L("28D"),
                        topMargin=L("19L"), bottomMargin=L("0L"), leftMargin=L("0L"), rightMargin=L("0L"))
            objects["icon"] = [{"properties": deepcopy(icon)}] + [
                {"selector": {"id": s}, "properties": deepcopy(icon)} for s in STATES]
            text_props = dict(show=L("true"), text=L(quoted(label)), fontFamily=L("'Segoe UI'"),
                              fontSize=L("8D"), fontColor=fill("#2B2B2C"), bold=L(str(active).lower()),
                              horizontalAlignment=L("'center'"), verticalAlignment=L("'middle'"),
                              leftMargin=L("0L"), rightMargin=L("0L"), topMargin=L("62L"), bottomMargin=L("6L"))
            objects["text"] = obj(show=L("true")) + [
                {"selector": {"id": s}, "properties": deepcopy(text_props)} for s in STATES]
            for key in ("outline", "shadow", "glow"):
                objects[key] = obj(show=L("false")) + [
                    {"selector": {"id": s}, "properties": {"show": L("false")}} for s in STATES]
            containers = value["visual"]["visualContainerObjects"]
            containers["stylePreset"] = obj(name=L(quoted(PRESET)))
            containers["general"] = obj(altText=L(quoted(("Current section: " if active else "Navigation: ") + ICONS[short][0])))
            assert containers["visualLink"] == old["visual"]["visualContainerObjects"]["visualLink"]
            planned[path] = value
            # Identify captions from the saved page, including Desktop-copied IDs.
            candidates = [(p, d) for p, d in values.items() if d.get("visual", {}).get("visualType") == "textbox"
                          and d["position"]["y"] == 77 and abs(d["position"]["x"] - (old["position"]["x"] - 7)) < .1]
            assert len(candidates) == 1, (page["displayName"], short)
            cp, caption = candidates[0]
            caption = deepcopy(caption)
            caption["isHidden"] = True
            planned[cp] = caption
            captions.add(caption["name"])
            count += 1

    assert count == 128 and len(affected) == 16
    for path, original in definitions.items():
        if path.name.endswith(".bookmark.json"):
            value = deepcopy(original)
            for section in value["explorationState"].get("sections", {}).values():
                for vid, state in section.get("visualContainers", {}).items():
                    if vid in captions:
                        state["singleVisual"]["display"] = {"mode": "hidden"}
            if value != original:
                planned[path] = value
    report_path = REPORT / "definition/report.json"
    report = deepcopy(definitions[report_path])
    package = next(p for p in report["resourcePackages"] if p["name"] == "RegisteredResources")
    existing_resources = {item["name"] for item in package["items"]}
    for name in asset_text:
        if name not in existing_resources:
            package["items"].append(dict(name=name, path=name, type="Image"))
    planned[report_path] = report
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        theme["visualStyles"]["actionButton"][PRESET] = {
            "shape": [{"tileShape": "rectangle", "roundEdge": 0}],
            "fill": [{"show": True, "fillColor": {"solid": {"color": "#F8F5F1"}}, "transparency": 0}],
            "icon": [{"show": True, "shapeType": "custom", "placement": "custom", "iconSize": 28,
                      "horizontalAlignment": "center", "verticalAlignment": "top", "topMargin": 19,
                      "bottomMargin": 0, "leftMargin": 0, "rightMargin": 0}],
            "text": [{"show": True, "fontFamily": "Segoe UI", "fontSize": 8, "fontColor": {"solid": {"color": "#2B2B2C"}},
                      "horizontalAlignment": "center", "verticalAlignment": "middle", "topMargin": 62,
                      "bottomMargin": 6, "leftMargin": 0, "rightMargin": 0}],
            **{key: [{"show": False}] for key in ("outline", "shadow", "glow")},
        }
        planned[path] = theme
    palette_path = BRAND / "WMPP_Palette.json"
    palette = read(palette_path)
    palette["version"] = "2026-09-28"
    palette["colours"]["navigationHoverPeach"] = hover_peach
    planned[palette_path] = palette

    changed = []
    def retain(path):
        if path.exists():
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        changed.append(str(path.relative_to(ROOT)))

    for path, value in planned.items():
        retain(path)
        save(path, value)
    for name, contents in asset_text.items():
        for path in (ASSETS / name, RESOURCES / name):
            if path.exists() and path.read_text(encoding="utf-8") == contents:
                continue
            retain(path)
            path.write_text(contents, encoding="utf-8")
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == digest for p, digest in protected.items())
    assert all(read(p) == d for p, d in definitions.items() if p not in planned)
    assert all((ASSETS / f"wmpp-bubble-ho-{s}.svg").read_text(encoding="utf-8") == source for s, source in sources.items())
    result = dict(backup=str(backup), pages=affected, buttons=count, resting_circle=resting,
                  hover_capsule=hover_peach, active_capsule=active_peach, active_circle=active_circle,
                  effect="Fixed 72x96 hit target; native hover-state capsule, not continuous animation",
                  native_icons_enabled=True, fill_transparency=0, orange_rail_restored=False,
                  semantic_model_unchanged=True, native_render_verified=False, modified_paths=changed)
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
