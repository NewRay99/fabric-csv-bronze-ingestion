"""Reuse the working menu-cap visibility to render a white-backed open button."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

from apply_wmpp_owner_bubble_states import ASSETS, BRAND, NS, PRESET, RESOURCES, image_ref
from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT


def main():
    marker = REPORT.parent / "WHITE_MENU_JOIN_REPAIR.json"
    assert not marker.exists(), "Inspect the saved repair before reapplying."
    backup = BUNDLE / "_review" / ("white-menu-join-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    original = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    working = deepcopy(original)
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    caps = {}
    mains = set()
    for path, value in original.items():
        if path.name != "visual.json":
            continue
        visual = value.get("visual", {})
        if PRESET not in json.dumps(visual.get("visualContainerObjects", {}).get("stylePreset", {})):
            continue
        mains.add(value["name"])
        pid = path.parents[2].name
        target_id = visual["visualContainerObjects"]["visualLink"][0]["properties"]["bookmark"]["expr"]["Literal"]["Value"].strip("'")
        target = original[REPORT / "definition/bookmarks" / (target_id + ".bookmark.json")]
        if not target["displayName"].endswith(" menu"):
            continue
        candidates = [(p, v) for p, v in original.items() if p.name == "visual.json"
                      and p.parents[2] == path.parents[2] and v["position"]["z"] == 300007
                      and v["position"]["x"] == value["position"]["x"] - 4]
        assert len(candidates) == 1
        cap_path, old_cap = candidates[0]
        cap = deepcopy(value)
        cap["name"] = old_cap["name"]
        cap["position"] = deepcopy(old_cap["position"])
        cap["position"]["z"] = 400010
        # Preserve the already-working cap's initial visibility and bookmark ID.
        cap.pop("isHidden", None)
        if "isHidden" in old_cap:
            cap["isHidden"] = old_cap["isHidden"]
        objects = cap["visual"]["objects"]
        for entry in objects["shape"]:
            entry["properties"].update(tileShape=L("'rectangle'"), roundEdge=L("41L"))
        for entry in objects["fill"]:
            props = entry["properties"]
            props.update(fillColor=fill("#FFFFFF"), transparency=L("0D"))
            if "image" in props:
                old_name = props["image"]["image"]["url"]["expr"]["ResourcePackageItem"]["ItemName"]
                props["image"] = image_ref(old_name.replace("background-", "connected-"))
        for entry in objects["icon"]:
            props = entry["properties"]
            top = int(props["topMargin"]["expr"]["Literal"]["Value"].rstrip("LD"))
            props["topMargin"] = L(f"{top + 8}L")
        for entry in objects["text"]:
            props = entry["properties"]
            for key, delta in (("topMargin", 8), ("leftMargin", 4), ("rightMargin", 4)):
                if key in props:
                    n = int(props[key]["expr"]["Literal"]["Value"].rstrip("LD"))
                    props[key] = L(f"{n + delta}L")
        containers = cap["visual"]["visualContainerObjects"]
        containers["stylePreset"] = obj(name=L("'WMPP Connected Open Menu'"))
        containers["general"] = obj(altText=L(quoted("Open navigation menu: " + target["displayName"])))
        containers["visualLink"][0]["properties"].update(
            bookmark=L(quoted(ident(f"wmpp-dropdown-bookmark:{pid}:close"))), tooltip=L("'Close menu'"))
        working[cap_path] = cap
        caps[cap["name"]] = (pid, target_id, value["name"])
    assert len(caps) == 64 and len(mains) == 128
    state_count = 0
    for path, bookmark in working.items():
        if not path.name.endswith(".bookmark.json"):
            continue
        for section in bookmark["explorationState"].get("sections", {}).values():
            for vid, state in section.get("visualContainers", {}).items():
                if vid in caps:
                    state["singleVisual"]["visualType"] = "actionButton"
                    state_count += 1
                if vid in mains:
                    assert state["singleVisual"].get("display", {}).get("mode") != "hidden"
    # Preserve cap visibility verbatim: only its visual type changes in bookmarks.
    for cap_id, (pid, bookmark_id, main_id) in caps.items():
        b = working[REPORT / "definition/bookmarks" / (bookmark_id + ".bookmark.json")]
        states = b["explorationState"]["sections"][pid]["visualContainers"]
        assert states[cap_id]["singleVisual"].get("display", {}).get("mode") != "hidden"
        assert states[main_id]["singleVisual"].get("display", {}).get("mode") != "hidden"
        assert cap_id in b["options"]["targetVisualNames"]

    assets = {}
    ET.register_namespace("", NS[1:-1])
    for state in ("default", "active", "hover", "disabled"):
        source = ET.fromstring((ASSETS / f"wmpp-bubble-background-{state}.svg").read_text())
        root = ET.Element(NS + "svg", {"width": "104", "height": "116", "viewBox": "0 0 104 116"})
        group = ET.SubElement(root, NS + "g", {"transform": "translate(4 8)"})
        for child in source:
            group.append(deepcopy(child))
        name = f"wmpp-bubble-connected-{state}.svg"
        contents = ET.tostring(root, encoding="unicode") + "\n"
        assets[ASSETS / name] = contents
        assets[RESOURCES / name] = contents
    report = working[REPORT / "definition/report.json"]
    package = next(p for p in report["resourcePackages"] if p["name"] == "RegisteredResources")
    names = {i["name"] for i in package["items"]}
    for path in assets:
        if path.parent == RESOURCES and path.name not in names:
            package["items"].append(dict(name=path.name, path=path.name, type="Image"))
    planned = {p: v for p, v in working.items() if v != original[p]}
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        style = deepcopy(theme["visualStyles"]["actionButton"][PRESET])
        style["fill"][0].update(fillColor={"solid": {"color": "#FFFFFF"}}, transparency=0)
        style["shape"][0]["roundEdge"] = 41
        style["icon"][0]["topMargin"] = 28
        style["text"][0].update(topMargin=82, leftMargin=10, rightMargin=10)
        theme["visualStyles"]["actionButton"]["WMPP Connected Open Menu"] = style
        planned[path] = theme
    for path, value in original.items():
        if path.name == "visual.json" and value["name"] not in caps:
            assert working[path] == value, "Do not alter original buttons or report data visuals."
    changed = []
    for path in list(planned) + list(assets):
        if path.exists():
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        changed.append(str(path.relative_to(ROOT)))
        if path in planned:
            save(path, planned[path])
        else:
            path.write_text(assets[path], encoding="utf-8")
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = dict(backup=str(backup), connected_white_buttons=64, primary_buttons_unchanged=128,
                  bookmark_cap_states_preserved=state_count, native_icon_and_label_positions_preserved=True,
                  semantic_model_unchanged=True, desktop_render_verified=False, modified_paths=changed)
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
