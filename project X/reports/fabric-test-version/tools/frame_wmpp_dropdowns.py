"""Add an editable white surround to WMPP dropdowns without changing buttons.

The marked yellow outline in the user's reference denotes a white surround,
not a requested yellow colour. Only local report shapes/bookmarks are changed.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil

from apply_report_soft_glow import native_panel
from build_report_design_delivery import L, ident, obj, quoted, read, save
from use_wmpp_dropdown_navigation import BUNDLE, PAGES, POPOVERS, REPORT, TOP


def backing(pid, area, part, rectangle, radius, z, hidden):
    visual = native_panel(pid, rectangle, color="#FFFFFF")
    visual["name"] = ident(f"wmpp-dropdown-frame:{pid}:{area}:{part}")
    visual["position"]["z"] = z
    visual["isHidden"] = hidden
    visual["visual"]["objects"]["shape"] = obj(
        tileShape=L("'rectangle'"), roundEdge=L(f"{radius}L")
    )
    if part != "panel":
        visual["visual"]["objects"]["shadow"] = obj(show=L("false"))
    visual["visual"]["visualContainerObjects"]["general"] = obj(
        altText=L(quoted(f"White dropdown surround: {area} / {part}"))
    )
    return visual


def main():
    planned = {}
    originals = {}
    for pid in sorted(PAGES):
        folder = REPORT / "definition/pages" / pid
        page = read(folder / "page.json")
        planned[pid] = {}
        for area, items in POPOVERS.items():
            short = next(short for short, _, group in TOP if group == area)
            main_id = ident(f"wmpp-dropdown:{pid}:main-{short}")
            first_id = ident(f"wmpp-dropdown:{pid}:child:{area}:0")
            last_id = ident(f"wmpp-dropdown:{pid}:child:{area}:{len(items)}")
            main = read(folder / "visuals" / main_id / "visual.json")["position"]
            first = read(folder / "visuals" / first_id / "visual.json")
            last = read(folder / "visuals" / last_id / "visual.json")["position"]
            p = first["position"]
            panel_y = p["y"] - 12
            cap_y = max(0, main["y"] - 8)
            neck_y = main["y"] + main["height"] / 2
            shapes = [
                backing(
                    pid,
                    area,
                    "panel",
                    (
                        p["x"] - 12,
                        panel_y,
                        p["width"] + 24,
                        last["y"] + last["height"] + 12 - panel_y,
                    ),
                    18,
                    100005,
                    first.get("isHidden", False),
                ),
                backing(
                    pid,
                    area,
                    "neck",
                    (main["x"] - 8, neck_y, main["width"] + 16, panel_y + 22 - neck_y),
                    0,
                    100006,
                    first.get("isHidden", False),
                ),
                backing(
                    pid,
                    area,
                    "cap",
                    (
                        main["x"] - 8,
                        cap_y,
                        main["width"] + 16,
                        main["y"] + main["height"] + 8 - cap_y,
                    ),
                    41,
                    100007,
                    first.get("isHidden", False),
                ),
            ]
            for shape in shapes:
                pos = shape["position"]
                assert pos["x"] >= 0 and pos["y"] >= 0 and pos["height"] > 0
                assert pos["x"] + pos["width"] <= page["width"]
                assert pos["y"] + pos["height"] <= page["height"]
                assert not (folder / "visuals" / shape["name"]).exists(), "Surround already exists"
            planned[pid][first_id] = shapes
        # Existing buttons, captions, queries, filters and geometry stay byte-identical.
        for path in folder.rglob("*.json"):
            originals[path] = hashlib.sha256(path.read_bytes()).hexdigest()
    backup = BUNDLE / "_review" / ("dropdown-surround-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    shutil.copytree(REPORT / "definition", backup / "definition")
    models = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for m in REPORT.parent.glob("*.SemanticModel")
        for p in m.rglob("*")
        if p.is_file()
    }
    for pid, areas in planned.items():
        for shapes in areas.values():
            for shape in shapes:
                save(
                    REPORT / "definition/pages" / pid / "visuals" / shape["name"] / "visual.json",
                    shape,
                )
    bookmarks = 0
    for path in REPORT.glob("definition/bookmarks/*.bookmark.json"):
        data = read(path)
        changed = False
        for pid, section in data.get("explorationState", {}).get("sections", {}).items():
            states = section.get("visualContainers", {})
            for first_id, shapes in planned.get(pid, {}).items():
                if first_id not in states:
                    continue
                assert (
                    data["options"]["suppressData"] and data["options"]["applyOnlyToTargetVisuals"]
                )
                for shape in shapes:
                    state = deepcopy(states[first_id])
                    state["singleVisual"]["visualType"] = "shape"
                    states[shape["name"]] = state
                    data["options"]["targetVisualNames"].append(shape["name"])
                changed = True
        if changed:
            save(path, data)
            bookmarks += 1
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in originals.items())
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in models.items())
    result = {
        "backup": str(backup),
        "dropdown_surrounds": len(PAGES) * len(POPOVERS),
        "native_shapes_added": len(PAGES) * len(POPOVERS) * 3,
        "bookmarks_updated": bookmarks,
        "existing_page_files_unchanged": True,
        "semantic_models_unchanged": True,
        "native_render_verified": False,
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
