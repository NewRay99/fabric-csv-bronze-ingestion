"""Keep primary buttons visible and add headroom above the complete icon disc."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET

from apply_wmpp_owner_bubble_states import BRAND, ASSETS, RESOURCES, PRESET, NS
from build_report_design_delivery import L, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE


def main():
    marker = REPORT.parent / "CAPSULE_HEADROOM_CORRECTION.json"
    assert not marker.exists(), "Inspect the prior correction before reapplying."
    backup = BUNDLE / "_review" / ("capsule-headroom-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    original = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    working = deepcopy(original)
    model_hashes = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    mains = set()
    retired = set()
    adjusted = 0
    for path, value in working.items():
        if path.name != "visual.json":
            continue
        visual = value.get("visual", {})
        preset = json.dumps(visual.get("visualContainerObjects", {}).get("stylePreset", {}))
        if PRESET not in preset and "WMPP Open Menu Bubble" not in preset:
            continue
        if PRESET in preset:
            mains.add(value["name"])
            value["isHidden"] = False
        else:
            retired.add(value["name"])
            value["isHidden"] = True
        # Match glyph centre to the circle centre in each fill-image state.
        fills = {}
        for entry in visual["objects"]["fill"]:
            if "image" in entry["properties"]:
                fills[entry.get("selector", {}).get("id", "default")] = entry["properties"]["image"]["image"]["url"]["expr"]["ResourcePackageItem"]["ItemName"]
        for entry in visual["objects"]["icon"]:
            state = entry.get("selector", {}).get("id", "default")
            capsule = any(fills.get(state, "").endswith(f"-{s}.svg") for s in ("active", "hover"))
            entry["properties"]["topMargin"] = L("26L" if capsule else "20L")
        adjusted += 1
    assert len(mains) == 128 and adjusted == 192

    repaired_states = 0
    for path, value in working.items():
        if not path.name.endswith(".bookmark.json"):
            continue
        for section in value["explorationState"].get("sections", {}).values():
            for vid, state in section.get("visualContainers", {}).items():
                if vid in mains and state["singleVisual"].get("display", {}).get("mode") == "hidden":
                    state["singleVisual"].pop("display")
                    repaired_states += 1
                if vid in retired:
                    state["singleVisual"]["display"] = {"mode": "hidden"}
    assert repaired_states == 64

    assets = {}
    ET.register_namespace("", NS[1:-1])
    for path in ASSETS.glob("wmpp-bubble-*.svg"):
        root = ET.fromstring(path.read_text())
        circle = root.find(NS + "circle")
        if circle is None:
            continue
        capsule = root.find(NS + "rect") is not None
        circle.set("cy", "42" if capsule else "36")
        group = root.find(NS + "g")
        if group is not None:
            group.set("transform", f"translate(32 {26 if capsule else 20}) scale(1.333333333)")
        contents = ET.tostring(root, encoding="unicode") + "\n"
        assets[path] = contents
        assets[RESOURCES / path.name] = contents

    planned = {p: value for p, value in working.items() if value != original[p]}
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        styles = theme["visualStyles"]["actionButton"]
        styles[PRESET]["icon"][0]["topMargin"] = 20
        styles["WMPP Open Menu Bubble"]["icon"][0]["topMargin"] = 26
        planned[path] = theme
    for path, value in original.items():
        if path.name == "visual.json":
            updated = working[path]
            assert updated["position"] == value["position"]
            assert updated.get("visual", {}).get("query") == value.get("visual", {}).get("query")
            assert updated.get("filterConfig") == value.get("filterConfig")
            assert updated.get("visual", {}).get("visualContainerObjects", {}).get("visualLink") == value.get("visual", {}).get("visualContainerObjects", {}).get("visualLink")
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
    for path, contents in assets.items():
        retain(path)
        path.write_text(contents, encoding="utf-8")
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in model_hashes.items())
    result = dict(backup=str(backup), always_visible_primary_buttons=128,
                  removed_primary_hide_states=repaired_states, capsule_top_gap_px=9,
                  capsule_circle_centre_y=42, capsule_glyph_top=26,
                  resting_circle_centre_y=36, resting_glyph_top=20,
                  open_menu_replacement_variants_retired=64,
                  semantic_model_unchanged=True, desktop_render_verified=False, modified_paths=changed)
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


def retire_open_variants():
    """Finish an already-saved correction without rerunning the migration."""
    marker = REPORT.parent / "CAPSULE_HEADROOM_CORRECTION.json"
    inventory = read(marker)
    retired = set()
    for path in (REPORT / "definition/pages").glob("*/visuals/*/visual.json"):
        value = read(path)
        if "WMPP Open Menu Bubble" in json.dumps(value.get("visual", {}).get("visualContainerObjects", {}).get("stylePreset", {})):
            assert value.get("isHidden")
            retired.add(value["name"])
    count = 0
    for path in (REPORT / "definition/bookmarks").glob("*.bookmark.json"):
        value = read(path)
        changed = False
        for section in value["explorationState"].get("sections", {}).values():
            for vid, state in section.get("visualContainers", {}).items():
                if vid in retired and state["singleVisual"].get("display", {}).get("mode") != "hidden":
                    state["singleVisual"]["display"] = {"mode": "hidden"}
                    changed = True
                    count += 1
        if changed:
            assert str(path.relative_to(ROOT)) in inventory["modified_paths"]
            save(path, value)
    inventory["open_menu_replacement_variants_retired"] = len(retired)
    save(marker, inventory)
    print(json.dumps({"retired_open_variants": len(retired), "show_states_removed": count}))


if __name__ == "__main__":
    main()
