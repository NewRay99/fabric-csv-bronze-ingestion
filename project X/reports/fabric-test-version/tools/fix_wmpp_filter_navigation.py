"""Scope Filters display bookmarks and repair their local panel destinations.

--check is a one-off saved-bookmark contract check, not a Desktop render test.
No semantic model, measure, query or existing slicer selection is modified.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil
import sys

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT
from use_wmpp_dropdown_navigation import PAGES, POPOVERS, TOP, bm_id

REF = "78d576b289e5fe3d2af6"
GROUP = "2788173fe42b642d5353"
CLOSE = "e394ddb59056d85d43a4"
CHILDREN = ("096babb2ce05747b020c", "ea000851ec6ed8a869b7", "f6189675911e84688ae6")
OPENERS = {
    REF: "06bb3455853a1e528b3e",
    "1f33996970651e846183": "225c078a903dc639c1d5",
    "ad5ab4aa6928c9178a35": "3c87b8dd2532b26c288a",
    "58d36c775c032a42e01b": "177797b1de47094ab000",
}
BOOKMARKS = REPORT / "definition/bookmarks"


def visual_path(pid, vid):
    return REPORT / "definition/pages" / pid / "visuals" / vid / "visual.json"


def local_id(pid, vid):
    return vid if pid == REF else ident(f"wmpp-local-filter:{pid}:{vid}")


def filter_bookmark(pid, opened):
    if pid == REF:
        return "1677909b4240887766a0" if opened else "f5e9ff962756b577a15b"
    return ident(f"wmpp-local-filter:{pid}:{'open' if opened else 'close'}")


def nav_ids(pid):
    primary = {ident(f"wmpp-dropdown:{pid}:main-{short}") for short, _, _ in TOP}
    primary |= {ident(f"board-annotation:dropdown:{pid}:caption:{short}") for short, _, _ in TOP}
    popups = {
        ident(f"wmpp-dropdown:{pid}:child:{area}:{n}")
        for area, items in POPOVERS.items()
        for n in range(len(items) + 1)
    }
    popups |= {
        ident(f"wmpp-dropdown-frame:{pid}:{area}:{part}")
        for area in POPOVERS
        for part in ("panel", "neck", "cap")
    }
    popups.add(ident(f"wmpp-bubble-rail:{pid}"))
    return primary, popups


def state(pid, vid, visible):
    kind = read(visual_path(pid, vid))["visual"]["visualType"]
    value = {"singleVisual": {"visualType": kind, "objects": {}}}
    if not visible:
        value["singleVisual"]["display"] = {"mode": "hidden"}
    return value


def check():
    errors = []
    for pid, opener in OPENERS.items():
        button = read(visual_path(pid, opener))
        action = button["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        bookmark_id = action["bookmark"]["expr"]["Literal"]["Value"].strip("'")
        opened = read(BOOKMARKS / (bookmark_id + ".bookmark.json"))
        if not opened["options"].get("applyOnlyToTargetVisuals"):
            errors.append((pid, "Filters restores all visual states"))
        if not opened["options"].get("suppressActiveSection"):
            errors.append((pid, "Filters can navigate to another page"))
        primary, popups = nav_ids(pid)
        section = opened["explorationState"]["sections"].get(pid, {})
        states = section.get("visualContainers", {})
        if not all(
            states.get(vid, {}).get("singleVisual", {}).get("display", {}).get("mode") == "hidden"
            for vid in primary | popups
        ):
            errors.append((pid, "Expanded Filters does not isolate navigation visibility"))
        group_path = visual_path(pid, local_id(pid, GROUP))
        if not group_path.exists():
            errors.append((pid, "No local filter panel"))
        elif read(group_path)["position"]["z"] <= 100030:
            errors.append((pid, "Filter panel is behind navigation"))
        close_path = BOOKMARKS / (filter_bookmark(pid, False) + ".bookmark.json")
        if close_path.exists():
            closed = read(close_path)
            restored = (
                closed["explorationState"]["sections"].get(pid, {}).get("visualContainers", {})
            )
            if not all(
                vid in restored and "display" not in restored[vid]["singleVisual"]
                for vid in primary
            ):
                errors.append((pid, "Closing Filters does not restore main navigation"))
    print(
        json.dumps(
            {"bookmark_contract": "FAIL" if errors else "PASS", "failures": errors}, indent=2
        )
    )
    return not errors


def main():
    if "--check" in sys.argv:
        raise SystemExit(0 if check() else 1)
    marker = REPORT.parent / "FILTER_NAVIGATION_REPAIR.json"
    assert not marker.exists(), "Repair already applied; inspect before reapplying"
    backup = BUNDLE / "_review" / ("filter-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    changed = set()
    def digest(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()
    protected = {
        p: digest(p)
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file() and ".pbi" not in p.parts
    }
    existing = {p: read(p) for p in (REPORT / "definition/pages").glob("*/visuals/*/visual.json")}

    def write(path, value):
        if path not in changed and path.exists():
            copy = backup / path.relative_to(ROOT)
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, copy)
        changed.add(path)
        save(path, value)

    templates = {vid: read(visual_path(REF, vid)) for vid in (GROUP, CLOSE, *CHILDREN)}
    meta_path = BOOKMARKS / "bookmarks.json"
    meta = read(meta_path)
    for pid, opener in OPENERS.items():
        page = read(REPORT / "definition/pages" / pid / "page.json")
        for vid, template in templates.items():
            path = visual_path(pid, local_id(pid, vid))
            value = read(path) if path.exists() else deepcopy(template)
            value["name"] = local_id(pid, vid)
            if value.get("parentGroupName") == GROUP:
                value["parentGroupName"] = local_id(pid, GROUP)
            if pid != REF and vid in CHILDREN:
                # A copied date slicer's saved selection must not silently filter
                # Offers/IPAs on initial load. Keep the field/format, start at All.
                for entry in value.get("visual", {}).get("objects", {}).get("general", []):
                    entry.get("properties", {}).pop("filter", None)
            if vid == "f6189675911e84688ae6":
                value["visual"]["objects"]["shape"] = obj(
                    tileShape=L("'rectangle'"), roundEdge=L("16L")
                )
                value["visual"]["objects"]["fill"] = obj(
                    show=L("true"), fillColor=fill("#FFFFFF"), transparency=L("0D")
                )
            if vid == GROUP:
                value["isHidden"] = True
                value["position"]["z"] = 200000
                value["visualGroup"]["displayName"] = page["displayName"] + " - Filters"
            if vid == CLOSE:
                value["isHidden"] = True
                value["position"]["z"] = 200010
                props = value["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
                props["bookmark"] = L(quoted(filter_bookmark(pid, False)))
                props["tooltip"] = L("'Close Filters'")
                props.pop("navigationSection", None)
            write(path, value)
        path = visual_path(pid, opener)
        button = read(path)
        button["isHidden"] = False
        props = button["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
        props["bookmark"] = L(quoted(filter_bookmark(pid, True)))
        props["tooltip"] = L("'Open Filters'")
        props.pop("navigationSection", None)
        write(path, button)

        primary, popups = nav_ids(pid)
        for opened in (True, False):
            visual_states = {vid: state(pid, vid, not opened) for vid in primary}
            visual_states.update({vid: state(pid, vid, False) for vid in popups})
            visual_states[opener] = state(pid, opener, not opened)
            visual_states[local_id(pid, CLOSE)] = state(pid, local_id(pid, CLOSE), opened)
            # Children are shown through the group's visibility. No slicer values,
            # filters, sort order, spotlight or selections are captured here.
            group_states = {local_id(pid, GROUP): {"isHidden": not opened}}
            name = filter_bookmark(pid, opened)
            value = {
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json",
                "name": name,
                "displayName": page["displayName"]
                + (" - Expanded Filter" if opened else " - Collapsed Filter"),
                "options": {
                    "applyOnlyToTargetVisuals": True,
                    "targetVisualNames": sorted(
                        set(visual_states)
                        | set(group_states)
                        | {local_id(pid, child) for child in CHILDREN}
                    ),
                    "suppressData": True,
                    "suppressActiveSection": True,
                },
                "explorationState": {
                    "version": "1.3",
                    "activeSection": pid,
                    "sections": {
                        pid: {
                            "visualContainers": visual_states,
                            "visualContainerGroups": group_states,
                        }
                    },
                },
            }
            write(BOOKMARKS / (name + ".bookmark.json"), value)
            if not any(item.get("name") == name for item in meta["items"]):
                meta["items"].append({"name": name})

    # Retain the old bookmark IDs as scoped aliases, without the obsolete
    # Geography-page snapshot. No active Filters button links to these aliases.
    for old, opened in [("dbcedff00715c427adb0", True), ("8417bbb65e892523407c", False)]:
        value = read(BOOKMARKS / (filter_bookmark(REF, opened) + ".bookmark.json"))
        value["name"] = old
        value["displayName"] += " (Legacy Alias)"
        write(BOOKMARKS / (old + ".bookmark.json"), value)
    write(meta_path, meta)

    # Arriving through navigation closes drawers and restores the header, so a
    # page left with Filters open cannot later arrive with its main menu hidden.
    for pid in PAGES:
        path = BOOKMARKS / (bm_id(pid, "go") + ".bookmark.json")
        bookmark = read(path)
        for target_pid in OPENERS:
            closed = read(BOOKMARKS / (filter_bookmark(target_pid, False) + ".bookmark.json"))
            target = bookmark["explorationState"]["sections"].setdefault(
                target_pid, {"visualContainers": {}}
            )
            source = closed["explorationState"]["sections"][target_pid]
            target["visualContainers"].update(source["visualContainers"])
            target.setdefault("visualContainerGroups", {}).update(source["visualContainerGroups"])
            bookmark["options"]["targetVisualNames"] = sorted(
                set(bookmark["options"]["targetVisualNames"])
                | set(closed["options"]["targetVisualNames"])
            )
        write(path, bookmark)

    for path, old in existing.items():
        now = read(path)
        assert old.get("visual", {}).get("query") == now.get("visual", {}).get("query")
        assert old.get("filterConfig") == now.get("filterConfig")
        if path not in changed:
            assert old == now
    assert all(digest(p) == h for p, h in protected.items())
    assert check()
    result = {
        "backup": str(backup),
        "local_filter_pages": list(OPENERS),
        "new_local_panels": 3,
        "data_and_existing_slicer_definitions_preserved": True,
        "desktop_render_verified": False,
        "modified_paths": [str(p.relative_to(ROOT)) for p in sorted(changed)],
    }
    write(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
