"""One-time client-delivery layout migration; no semantic-model edits.

Preserves existing queries/selections and uses display-only bookmarks. Backups
and an inventory accompany the migration. Not a persistent report test suite.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT
from fix_wmpp_filter_navigation import (
    BOOKMARKS, CHILDREN, CLOSE, GROUP, OPENERS, REF, filter_bookmark, local_id,
    nav_ids, visual_path,
)
from use_wmpp_dropdown_navigation import TOP, POPOVERS, bm_id
from add_board_dashboard_annotations import text

BOARD = "5038cffdd48af9a80dd1"
OVERVIEW = "b8c7c2636c82c10870b2"
RETIRED = "4be6f15f15a086c98c33"
SINGLE = "f3070e87127b751f89d4"
MAIN = set(OPENERS) | {
    BOARD, OVERVIEW, "510f9f9501ccc5ae8a74", "6ae319c8916a5d63a4ff",
    "b95eb4c0b53cd8c60710", "dd3a58c056d723048dbf",
}
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json"


def pos(x, y, w, h, z=300000):
    return dict(x=x, y=y, width=w, height=h, z=z, tabOrder=z)


def link(value, bookmark, label):
    value["visual"]["visualContainerObjects"]["visualLink"] = obj(
        show=L("true"), type=L("'Bookmark'"), bookmark=L(quoted(bookmark)),
        tooltip=L(quoted(label)),
    )


def signature(value):
    value = deepcopy(value)
    for key in ("name", "position", "isHidden", "howCreated"):
        value.pop(key, None)
    return value


def main():
    marker = REPORT.parent / "NAVIGATION_LAYOUT_DELIVERY.json"
    assert not marker.exists(), "Inspect the prior migration before reapplying."
    pages = {p.parent.name: read(p) for p in (REPORT / "definition/pages").glob("*/page.json")}
    original = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    working = deepcopy(original)
    model_hashes = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()
    }
    backup = BUNDLE / "_review" / ("aligned-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))

    def get(pid, vid):
        return working[visual_path(pid, vid)]

    def put(pid, value):
        working[visual_path(pid, value["name"])] = value
        return value["name"]

    def page_visuals(pid):
        return [v for p, v in working.items() if p.parent.parent.name == "visuals" and p.parents[2].name == pid]

    def state(pid, vid, visible):
        value = {"singleVisual": {"visualType": get(pid, vid)["visual"]["visualType"], "objects": {}}}
        if not visible:
            value["singleVisual"]["display"] = {"mode": "hidden"}
        return value

    def panel(pid, key, rectangle, parent=None):
        value = deepcopy(get(REF, CHILDREN[-1]))
        value["name"] = ident(f"wmpp-layout:{pid}:{key}")
        value["position"] = rectangle
        value.pop("parentGroupName", None)
        if parent:
            value["parentGroupName"] = parent
        value["visual"]["visualContainerObjects"]["border"] = obj(show=L("false"))
        value["visual"]["visualContainerObjects"]["background"] = obj(show=L("false"))
        return value

    def label(pid, key, words, rectangle, parent=None):
        value = text(f"layout:{pid}:{key}", words, (0, 0, 100, 40), size=18, bold=True, color="#2B2B2C")
        value["position"] = rectangle
        if parent:
            value["parentGroupName"] = parent
        return value

    def text_button(pid, key, words, rectangle, bookmark, hidden=False):
        value = deepcopy(get(REF, ident(f"wmpp-dropdown:{REF}:child:Referrals:0")))
        value["$schema"] = SCHEMA
        value["name"] = ident(f"wmpp-layout:{pid}:{key}")
        value["position"] = rectangle
        value["isHidden"] = hidden
        objects = value["visual"]["objects"]
        for entry in objects["text"]:
            props = entry["properties"]
            if "text" in props:
                props.update(text=L(quoted(words)), fontColor=fill("#2B2B2C"), fontSize=L("12D"))
        for entry in objects["fill"]:
            if "fillColor" in entry["properties"]:
                entry["properties"]["fillColor"] = fill("#FEE1DD")
        value["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted(words)))
        link(value, bookmark, words)
        return value

    # Existing stable IDs on normal pages; Desktop assigns new IDs to copied pages.
    navigation = {}
    for pid in pages:
        if visual_path(pid, ident(f"wmpp-dropdown:{pid}:main-HO")) in working:
            navigation[pid] = {vid: vid for ids in nav_ids(pid) for vid in ids}
    copied_map = {}
    for old in set.union(*nav_ids(BOARD)):
        source = get(BOARD, old)
        matches = [v for v in page_visuals(OVERVIEW) if signature(v) == signature(source)]
        if len(matches) > 1:
            matches = [v for v in matches if all(v["position"][k] == source["position"][k] for k in ("x", "y", "tabOrder"))]
        assert len(matches) == 1, (old, len(matches))
        copied_map[old] = matches[0]["name"]
    navigation[OVERVIEW] = copied_map

    def nid(pid, kind):
        basis = BOARD if pid == OVERVIEW else pid
        if kind.startswith("caption:"):
            canonical = ident(f"board-annotation:dropdown:{basis}:caption:{kind.split(':')[1]}")
        elif kind.startswith("frame:"):
            canonical = ident(f"wmpp-dropdown-frame:{basis}:{kind[6:]}")
        elif kind == "rail":
            canonical = ident(f"wmpp-bubble-rail:{basis}")
        else:
            canonical = ident(f"wmpp-dropdown:{basis}:{kind}")
        return navigation[pid][canonical]

    # Keep the number of submenu rows unchanged while replacing a removed-page
    # destination with the new Referral Overview. Other internal IDs stay stable.
    menus = deepcopy(POPOVERS)
    menus["Referrals"][1] = ("Referral Overview", OVERVIEW)
    for area, items in menus.items():
        menus[area] = [(pages[pid]["displayName"], pid) for _, pid in items]
    main_targets = {"HO": "364f2cdd67ba7822850c", "DO": "ad5ab4aa6928c9178a35",
                    "IO": "58d36c775c032a42e01b", "RM": "b95eb4c0b53cd8c60710"}
    for pid in navigation:
        assert pages[pid]["width"] == 1680
        for index, (short, title, area) in enumerate(TOP):
            x = 1072 + index * 74
            value = get(pid, nid(pid, f"main-{short}"))
            value["position"] = pos(x, 8, 66, 66)
            value["isHidden"] = False
            target = bm_id(pid, f"open-{area}") if area in menus else bm_id(main_targets[short], "go")
            link(value, target, f"Open {title} menu" if area in menus else f"Go to {title}")
            caption = get(pid, nid(pid, f"caption:{short}"))
            caption["position"] = pos(x - 7, 77, 80, 22, 300002)
            caption["isHidden"] = False
            link(caption, target, title)
        get(pid, nid(pid, "rail"))["isHidden"] = True
        for area, items in menus.items():
            index = next(i for i, (_, _, a) in enumerate(TOP) if a == area)
            bx = 1072 + index * 74
            x = min(bx, 1346)
            for n in range(len(items) + 1):
                value = get(pid, nid(pid, f"child:{area}:{n}"))
                value["position"] = pos(x, 118 + n * 44, 310, 44, 300020 + n)
                value["isHidden"] = True
                words = items[n][0] if n < len(items) else "Close menu ×"
                target = bm_id(items[n][1], "go") if n < len(items) else bm_id(pid, "close")
                link(value, target, words)
                for entry in value["visual"]["objects"]["text"]:
                    if "text" in entry["properties"]:
                        entry["properties"]["text"] = L(quoted(words))
            rectangles = {
                "panel": pos(x - 12, 106, 334, (len(items) + 1) * 44 + 24, 300005),
                "neck": pos(bx - 8, 41, 82, 87, 300006),
                "cap": pos(bx - 8, 0, 82, 82, 300007),
            }
            for part, rectangle in rectangles.items():
                value = get(pid, nid(pid, f"frame:{area}:{part}"))
                value["position"] = rectangle
                value["isHidden"] = True

    # Display-only drawers; chart parameter controls stay beside their charts.
    drawers = {}
    for pid in sorted(MAIN):
        old_panel = pid in OPENERS
        group_id = local_id(pid, GROUP) if old_panel else ident(f"wmpp-layout:{pid}:filter-group")
        opener_id = OPENERS.get(pid, ident(f"wmpp-layout:{pid}:filter-open"))
        close_id = local_id(pid, CLOSE) if old_panel else ident(f"wmpp-layout:{pid}:filter-close")
        slicers = [v for v in page_visuals(pid) if v.get("visual", {}).get("visualType") == "slicer"
                   and "Snapshot Window" not in json.dumps(v.get("visual", {}).get("query", {}))]
        if not slicers:
            # Requirement Matrix had no on-canvas controls: add the same governed
            # date/type fields as the other original dashboards, initially All.
            for source_id in CHILDREN[:2]:
                value = deepcopy(get(REF, source_id))
                value["name"] = ident(f"wmpp-layout:{pid}:slicer:{source_id}")
                for entry in value["visual"].get("objects", {}).get("general", []):
                    entry.get("properties", {}).pop("filter", None)
                put(pid, value)
                slicers.append(value)
        slicers.sort(key=lambda v: (v["position"]["y"], v["position"]["x"]))
        height = 80 + len(slicers) * 116
        group = deepcopy(get(REF, GROUP))
        group.update(name=group_id, position=pos(650, 112, 398, height, 210000), isHidden=True)
        group["visualGroup"]["displayName"] = pages[pid]["displayName"] + " | Filters drawer"
        put(pid, group)
        background = panel(pid, "filter-background", pos(0, 0, 398, height, 0), group_id)
        if old_panel:
            background["name"] = local_id(pid, CHILDREN[-1])
        children = [put(pid, background)]
        children.append(put(pid, label(pid, "filter-heading", "Filter this dashboard", pos(24, 18, 350, 32, 1), group_id)))
        for n, value in enumerate(slicers):
            value["parentGroupName"] = group_id
            value["isHidden"] = False
            value["position"] = pos(24, 64 + n * 116, 350, 100, 10 + n)
            children.append(value["name"])
        for opened, vid in ((True, opener_id), (False, close_id)):
            value = deepcopy(get(REF, OPENERS[REF] if opened else CLOSE))
            value["name"] = vid
            value["position"] = pos(960, 0, 88, 104, 300010)
            value["isHidden"] = not opened
            value["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted("Open Filters" if opened else "Close Filters")))
            link(value, filter_bookmark(pid, opened), "Open Filters" if opened else "Close Filters")
            put(pid, value)
        drawers[pid] = dict(group=group_id, opener=opener_id, close=close_id, children=children)

    # Duplicate the user's exact native Sankey query; retain the source visual.
    sankey_source = get(OVERVIEW, "9a085d5594727551081c")
    flow_group = ident("wmpp-layout:referrals:journey-group")
    flow_open = ident("wmpp-layout:referrals:journey-open-bookmark")
    flow_close = ident("wmpp-layout:referrals:journey-close-bookmark")
    group = deepcopy(get(REF, GROUP))
    group.update(name=flow_group, position=pos(24, 410, 1632, 640, 180000), isHidden=True)
    group["visualGroup"]["displayName"] = "Referrals | Referral journey overlay"
    put(REF, group)
    flow_children = [put(REF, panel(REF, "journey-background", pos(0, 0, 1632, 640, 0), flow_group))]
    flow_children.append(put(REF, label(REF, "journey-heading", "Referral journey · movement between stages", pos(24, 18, 1100, 36, 1), flow_group)))
    sankey = deepcopy(sankey_source)
    sankey.update(name=ident("wmpp-layout:referrals:journey-chart"), parentGroupName=flow_group,
                  position=pos(24, 70, 1584, 546, 2), isHidden=False)
    sankey["visual"].setdefault("visualContainerObjects", {}).update(
        title=obj(show=L("false")), background=obj(show=L("true"), color=fill("#FFFFFF"), transparency=L("0D")),
        padding=obj(top=L("12D"), bottom=L("12D"), left=L("16D"), right=L("16D")),
    )
    flow_children.append(put(REF, sankey))
    closer = text_button(REF, "journey-close", "Close referral journey ×", pos(1332, 12, 276, 44, 3), flow_close)
    closer["parentGroupName"] = flow_group
    flow_children.append(put(REF, closer))
    flow_opener = put(REF, text_button(REF, "journey-open", "Explore referral journey →", pos(690, 424, 340, 44, 170000), flow_open))

    def section(pid, menu=None, filters=False, journey=False):
        states = {}
        for short, _, _ in TOP:
            for kind in (f"main-{short}", f"caption:{short}"):
                vid = nid(pid, kind)
                states[vid] = state(pid, vid, True)
        states[nid(pid, "rail")] = state(pid, nid(pid, "rail"), False)
        for area, items in menus.items():
            for kind in [f"child:{area}:{n}" for n in range(len(items) + 1)] + [f"frame:{area}:{part}" for part in ("panel", "neck", "cap")]:
                vid = nid(pid, kind)
                states[vid] = state(pid, vid, area == menu)
        groups = {}
        if pid in drawers:
            drawer = drawers[pid]
            states[drawer["opener"]] = state(pid, drawer["opener"], not filters)
            states[drawer["close"]] = state(pid, drawer["close"], filters)
            groups[drawer["group"]] = {"isHidden": not filters}
        if pid == REF:
            states[flow_opener] = state(pid, flow_opener, not journey)
            groups[flow_group] = {"isHidden": not journey}
        return dict(visualContainers=states, visualContainerGroups=groups)

    def bookmark(name, title, pid, sections, navigate=False):
        targets = set()
        for target_pid, value in sections.items():
            targets.update(value["visualContainers"])
            targets.update(value["visualContainerGroups"])
            for visual in page_visuals(target_pid):
                if visual.get("parentGroupName") in value["visualContainerGroups"]:
                    targets.add(visual["name"])
        working[BOOKMARKS / (name + ".bookmark.json")] = {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json",
            "name": name, "displayName": title,
            "options": dict(applyOnlyToTargetVisuals=True, targetVisualNames=sorted(targets),
                            suppressData=True, suppressActiveSection=not navigate),
            "explorationState": dict(version="1.3", activeSection=pid, sections=sections),
        }

    for pid in navigation:
        title = pages[pid]["displayName"]
        bookmark(bm_id(pid, "go"), f"Go to {title}", pid,
                 {p: section(p) for p in navigation}, navigate=True)
        bookmark(bm_id(pid, "close"), f"{title} | Close menus", pid, {pid: section(pid)})
        for area in menus:
            bookmark(bm_id(pid, "open-" + area), f"{title} | {area} menu", pid, {pid: section(pid, menu=area)})
        if pid in drawers:
            for opened in (False, True):
                bookmark(filter_bookmark(pid, opened), f"{title} | {'Open' if opened else 'Close'} filters", pid,
                         {pid: section(pid, filters=opened)})
    for opened, name in ((True, flow_open), (False, flow_close)):
        bookmark(name, "Referrals | " + ("Show" if opened else "Hide") + " referral journey", REF,
                 {REF: section(REF, journey=opened)})
    for alias, opened in (("dbcedff00715c427adb0", True), ("8417bbb65e892523407c", False)):
        bookmark(alias, "Referrals | " + ("Open" if opened else "Close") + " filters (legacy link)", REF,
                 {REF: section(REF, filters=opened)})
    # Preserve old bookmark IDs for any external saved links, without dead pages.
    for p, value in list(working.items()):
        if p.name.endswith(".bookmark.json") and value["displayName"].startswith(f"Navigation / {RETIRED}"):
            bookmark(value["name"], "Go to Referral Single View (legacy link)", SINGLE,
                     {q: section(q) for q in navigation}, navigate=True)
        elif p.name.endswith(".bookmark.json"):
            for prefix, title in (("Board / ", "Board Dashboard | "), ("Supply / ", "Provider & Placement Supply | "),
                                  ("Target / ", "Target & Urgency Performance | ")):
                if value["displayName"].startswith(prefix):
                    value["displayName"] = title + value["displayName"][len(prefix):].replace(" / ", " | ")
    meta = working[BOOKMARKS / "bookmarks.json"]
    known = {item.get("name") for item in meta["items"]}
    for p, value in list(working.items()):
        if p.name.endswith(".bookmark.json") and value["name"] not in known:
            meta["items"].append({"name": value["name"]})
    # Sort the pane by intelligible labels, retaining IDs/actions.
    meta["items"].sort(key=lambda item: working.get(BOOKMARKS / (item.get("name", "") + ".bookmark.json"), {}).get("displayName", "").casefold())

    # One-off delivery checks, deliberately not a permanent semantic/report test.
    for pid in navigation:
        for i, (short, _, _) in enumerate(TOP):
            assert get(pid, nid(pid, f"main-{short}"))["position"] == pos(1072 + i * 74, 8, 66, 66)
        for vid in navigation[pid].values():
            v = get(pid, vid)
            if not v.get("isHidden"):
                assert v["position"]["x"] + v["position"]["width"] <= 1680
    for p, old in original.items():
        if p.name == "visual.json":
            new = working[p]
            assert old.get("visual", {}).get("query") == new.get("visual", {}).get("query"), p
            assert old.get("filterConfig") == new.get("filterConfig"), p
            if old.get("visual", {}).get("visualType") == "slicer":
                assert old["visual"].get("objects") == new["visual"].get("objects"), p
    assert sankey["visual"]["query"] == sankey_source["visual"]["query"]
    for p, value in working.items():
        if not p.name.endswith(".bookmark.json"):
            continue
        for pid, data in value["explorationState"].get("sections", {}).items():
            assert pid in pages, (value["displayName"], pid)
            for key in ("visualContainers", "visualContainerGroups"):
                assert all(visual_path(pid, vid) in working for vid in data.get(key, {})), value["displayName"]

    changed = [p for p, value in working.items() if p not in original or original[p] != value]
    for path in changed:
        if path.exists():
            destination = backup / path.relative_to(ROOT)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
        save(path, working[path])
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in model_hashes.items())
    result = dict(
        backup=str(backup), navigation_pages=[pages[p]["displayName"] for p in navigation],
        filter_drawer_pages=[pages[p]["displayName"] for p in drawers],
        navigation_origin=dict(x=1072, y=8, diameter=66, pitch=74),
        filters_origin=dict(x=960, y=0), source_sankey_retained=True,
        semantic_model_unchanged=True, existing_queries_and_slicer_selections_preserved=True,
        desktop_render_verified=False, modified_paths=[str(p.relative_to(ROOT)) for p in changed],
    )
    save(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))
    print("Modified/new JSON files:", len(changed))


if __name__ == "__main__":
    main()
