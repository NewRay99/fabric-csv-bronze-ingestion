"""Replace the two-row WMPP menu with original-style circles and dropdowns.

Local delivery only. Display-only bookmarks are restricted to menu visuals.
This is a one-time migration, not a reusable whole-report styling pass.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil

from connect_wmpp_report_pages import BUNDLE, GROUPS, REPORT, get_literal
from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from add_board_dashboard_annotations import text

SECTIONS = dict(GROUPS)
TOP = [
    ("HO", "Home", "Home"),
    ("R", "Referrals", "Referrals"),
    ("OO", "Offers", "Offers"),
    ("DO", "Draft offers", None),
    ("IO", "IPAs", "IPAs"),
    ("PR", "Providers", "Providers"),
    ("PF", "Performance", "Performance"),
    ("RM", "Requirements", "Requirements"),
]
POPOVERS = {k: v for k, v in GROUPS if len(v) > 1}
ORIGINAL_HEADERS = {
    "364f2cdd67ba7822850c",
    "78d576b289e5fe3d2af6",
    "1f33996970651e846183",
    "ad5ab4aa6928c9178a35",
    "58d36c775c032a42e01b",
    "b95eb4c0b53cd8c60710",
}
PAGES = {pid for _, items in GROUPS for _, pid in items}
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/"


def button(pid, key, label, position, bookmark, *, active=False, circle=False):
    """Native action button using the original preset and explicit text switch."""
    background = "#FB6540" if active or circle else "#FFFFFF"
    ink = "#1D1D1B"
    size = 18 if circle else 11
    props = {
        "text": L(quoted(label)),
        "fontFamily": L("'Segoe UI'"),
        "fontSize": L(f"{size}D"),
        "bold": L("true"),
        "fontColor": fill(ink),
        "horizontalAlignment": L("'center'" if circle else "'left'"),
        "verticalAlignment": L("'middle'"),
        "leftMargin": L("2D" if circle else "14D"),
        "rightMargin": L("2D" if circle else "14D"),
        "topMargin": L("2D"),
        "bottomMargin": L("2D"),
    }
    states = ("default", "hover", "selected", "disabled")
    return {
        "$schema": SCHEMA + "visualContainer/2.7.0/schema.json",
        "name": ident(f"wmpp-dropdown:{pid}:{key}"),
        "position": dict(zip(("x", "y", "width", "height"), position), z=100010, tabOrder=0),
        "visual": {
            "visualType": "actionButton",
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": {
                **{
                    k: obj(show=L("false"))
                    for k in (
                        "title",
                        "subTitle",
                        "background",
                        "border",
                        "visualHeader",
                        "dropShadow",
                    )
                },
                "padding": obj(top=L("0D"), bottom=L("0D"), left=L("0D"), right=L("0D")),
                "stylePreset": obj(name=L("'WMPP actionButton c54418c8ca'")),
                "general": obj(altText=L(quoted("WMPP navigation: " + label))),
                "visualLink": obj(
                    show=L("true"),
                    type=L("'Bookmark'"),
                    bookmark=L(quoted(bookmark)),
                    tooltip=L(quoted(label)),
                ),
            },
            "objects": {
                "shape": [
                    {
                        "selector": {"id": state},
                        "properties": {"tileShape": L("'oval'"), "roundEdge": L("84L")},
                    }
                    for state in states
                ]
                if circle
                else obj(tileShape=L("'rectangle'"), roundEdge=L("10D")),
                # Enable text at the visual level, as in the original saved preset.
                "text": obj(show=L("true"))
                + [{"selector": {"id": state}, "properties": deepcopy(props)} for state in states],
                "fill": obj(show=L("true"))
                + [
                    {
                        "selector": {"id": state},
                        "properties": {
                            "fillColor": fill(
                                "#F98165"
                                if state == "hover" and circle
                                else "#FFE7DF"
                                if state == "hover" and not active
                                else background
                            ),
                            "transparency": L("0D"),
                        },
                    }
                    for state in states
                ],
                **{k: obj(show=L("false")) for k in ("icon", "shadow", "glow")},
                "outline": obj(show=L("false"))
                + [
                    {
                        "selector": {"id": state},
                        "properties": {
                            "lineColor": fill("#9F341F"),
                            "weight": L("0D"),
                            "transparency": L("100D"),
                        },
                    }
                    for state in states
                ],
            },
        },
    }


def bm_id(pid, state):
    return ident(f"wmpp-dropdown-bookmark:{pid}:{state}")


def state_for(visible):
    state = {"singleVisual": {"visualType": "actionButton", "objects": {}}}
    if not visible:
        state["singleVisual"]["display"] = {"mode": "hidden"}
    return state


def bookmark(pid, label, sections, navigate=False):
    targets = sorted({key for section in sections.values() for key in section["visualContainers"]})
    return {
        "$schema": SCHEMA + "bookmark/2.1.0/schema.json",
        "name": bm_id(pid, label),
        "displayName": f"Navigation / {pid} / {label}",
        "options": {
            "applyOnlyToTargetVisuals": True,
            "targetVisualNames": targets,
            "suppressActiveSection": not navigate,
            "suppressData": True,
        },
        "explorationState": {"version": "1.0", "activeSection": pid, "sections": sections},
    }


def main():
    pages = {pid: read(REPORT / "definition/pages" / pid / "page.json") for pid in PAGES}
    assert all(
        not any(a.get("name") == "wmppDropdownNavigation" for a in p.get("annotations", []))
        for p in pages.values()
    ), "Dropdown navigation is already installed"
    backup = (
        BUNDLE / "_review" / ("dropdown-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    shutil.copytree(REPORT / "definition", backup / "definition")
    models = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for m in REPORT.parent.glob("*.SemanticModel")
        for p in m.rglob("*")
        if p.is_file()
    }
    before_queries = {}
    retired = {}
    popups = {}
    moved = {}
    removed = 0
    for pid, page in pages.items():
        folder = REPORT / "definition/pages" / pid
        retired[pid], popups[pid], moved[pid] = set(), {}, set()
        band = next(
            int(a["value"]) for a in page.get("annotations", []) if a["name"] == "wmppMenuHeight"
        )
        for file in list(folder.glob("visuals/*/visual.json")):
            d = read(file)
            v = d.get("visual", {})
            containers = v.get("visualContainerObjects", {})
            alt = get_literal(
                containers.get("general", [{}])[0].get("properties", {}).get("altText", {})
            )
            if alt.startswith("Navigation: "):
                # Move only the previous migration's known menu visuals into the backup.
                expected = {ident(f"wmpp-menu:{pid}:main-{g}") for g, _ in GROUPS}
                expected |= {ident(f"wmpp-menu:{pid}:sub-{p}") for p in PAGES}
                assert d["name"] in expected and file.resolve().is_relative_to(REPORT.resolve())
                target = backup / "retired-menu" / pid / file.parent.name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file.parent), str(target))
                removed += 1
                continue
            before_queries[str(file)] = (deepcopy(v.get("query")), deepcopy(d.get("filterConfig")))
            if pid in ORIGINAL_HEADERS and not d.get("parentGroupName"):
                d["position"]["y"] -= band
                moved[pid].add(d["name"])
            # Retire the earlier header navigation only; keep original filter toggles.
            texts = {
                get_literal(x.get("properties", {}).get("text", {}))
                for x in v.get("objects", {}).get("text", [])
            }
            if (
                v.get("visualType") == "actionButton"
                and not d.get("parentGroupName")
                and texts & {"HO", "R", "OO", "DO", "IO", "PR", "RM"}
                and d["position"]["y"] < 260
            ):
                d["isHidden"] = True
                retired[pid].add(d["name"])
            save(file, d)
        if pid in ORIGINAL_HEADERS:
            page["height"] -= band
        page["annotations"] = [
            a for a in page.get("annotations", []) if a["name"] != "wmppMenuHeight"
        ]
        page["annotations"].append(
            {"name": "wmppDropdownNavigation", "value": "original-style-circles-v1"}
        )
        save(folder / "page.json", page)
        group = next(g for g, items in GROUPS if any(p == pid for _, p in items))
        # Original branded headers keep their old vertical placement and filter space.
        right = 114 if pid in ORIGINAL_HEADERS and page["width"] >= 1500 else 24
        left = page["width"] - right - (8 * 66 + 7 * 8)
        top = 34 if pid in ORIGINAL_HEADERS else 6
        dropdown_top = 148 if pid in ORIGINAL_HEADERS else 104
        for i, (short, label, area) in enumerate(TOP):
            x = left + i * 74
            dest = "ad5ab4aa6928c9178a35" if area is None else SECTIONS[area][0][1]
            action = bm_id(pid, "open-" + area) if area in POPOVERS else bm_id(dest, "go")
            active = (
                pid == dest if area is None else group == area and pid != "ad5ab4aa6928c9178a35"
            )
            d = button(
                pid, "main-" + short, short, (x, top, 66, 66), action, active=active, circle=True
            )
            d["position"]["tabOrder"] = i * 2
            d["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]["tooltip"] = L(
                quoted(("Show " + label + " pages") if area in POPOVERS else ("Open " + label))
            )
            save(folder / "visuals" / d["name"] / "visual.json", d)
            caption = text(
                f"dropdown:{pid}:caption:{short}",
                label + (" ▾" if area in POPOVERS else ""),
                (x - 7, top + 69, 80, 22),
                size=10,
                bold=active,
            )
            caption["position"]["z"] = 100012
            caption["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0][
                "horizontalTextAlignment"
            ] = "center"
            # Caption is also clickable, keeping the expanded label an effective target.
            caption["visual"]["visualContainerObjects"]["visualLink"] = deepcopy(
                d["visual"]["visualContainerObjects"]["visualLink"]
            )
            save(folder / "visuals" / caption["name"] / "visual.json", caption)
            if area not in POPOVERS:
                continue
            popup_x = min(x, page["width"] - 334)
            members = []
            children = POPOVERS[area] + [("Close menu  ×", None)]
            for n, (child_label, target) in enumerate(children):
                link = bm_id(target, "go") if target else bm_id(pid, "close")
                child = button(
                    pid,
                    f"child:{area}:{n}",
                    child_label,
                    (popup_x, dropdown_top + n * 44, 310, 44),
                    link,
                    active=target == pid,
                )
                child["isHidden"] = True
                child["position"]["z"] = 100020 + n
                child["position"]["tabOrder"] = 20 + i * 10 + n
                child["visual"]["visualContainerObjects"]["background"] = obj(
                    show=L("true"), color=fill("#FFFFFF"), transparency=L("0D")
                )
                save(folder / "visuals" / child["name"] / "visual.json", child)
                members.append(child["name"])
            popups[pid][area] = members

    # Existing data/view bookmarks must not reveal the retired header controls.
    for file in REPORT.glob("definition/bookmarks/*.bookmark.json"):
        d = read(file)
        changed = False
        for pid, section in d.get("explorationState", {}).get("sections", {}).items():
            for vid, state in section.get("visualContainers", {}).items():
                if vid in retired.get(pid, set()):
                    state.setdefault("singleVisual", {}).setdefault("display", {})["mode"] = (
                        "hidden"
                    )
                    changed = True
                if vid in moved.get(pid, set()) and "y" in state.get("position", {}):
                    state["position"]["y"] -= 104
                    changed = True
        if changed:
            save(file, d)
    closed = {
        pid: {
            "visualContainers": {
                vid: state_for(False) for members in groups.values() for vid in members
            }
        }
        for pid, groups in popups.items()
    }
    bookmarks = []
    for pid in PAGES:
        bookmarks.append(bookmark(pid, "go", deepcopy(closed), navigate=True))
        bookmarks.append(bookmark(pid, "close", {pid: deepcopy(closed[pid])}))
        for area, members in popups[pid].items():
            section = deepcopy(closed[pid])
            section["visualContainers"].update({vid: state_for(True) for vid in members})
            bookmarks.append(bookmark(pid, "open-" + area, {pid: section}))
    meta_path = REPORT / "definition/bookmarks/bookmarks.json"
    meta = read(meta_path)
    for d in bookmarks:
        save(REPORT / "definition/bookmarks" / (d["name"] + ".bookmark.json"), d)
        meta["items"].append({"name": d["name"]})
    save(meta_path, meta)

    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in models.items())
    for file, (query, filters) in before_queries.items():
        d = read(Path(file))
        assert query == d.get("visual", {}).get("query") and filters == d.get("filterConfig")
    result = {
        "backup": str(backup),
        "pages": len(PAGES),
        "replaced_menu_visuals": removed,
        "dropdown_bookmarks": len(bookmarks),
        "models_unchanged": True,
        "queries_and_visual_filters_unchanged": True,
        "native_render_verified": False,
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
