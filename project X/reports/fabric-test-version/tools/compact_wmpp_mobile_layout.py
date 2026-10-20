"""Compact current phone layouts; never edit Desktop/model/bookmark definitions.

Preview by default. Backups are copies; all edits go through apply_patch.
The published 2.4 mobile schema supports independent phone formatting.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import difflib
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import xml.etree.ElementTree as ET

import plan_wmpp_mobile_layout as original

PROJECT = original.PROJECT
REPORT = original.REPORT
SCHEMA = original.MOBILE_SCHEMA
WIDTH = 323
SCALE = 0.8
GAP = 8
MANIFEST = PROJECT / "MOBILE_COMPACT_LAYOUT_DELIVERY.json"
QA = PROJECT / "MOBILE_COMPACT_LAYOUT_QA.json"
BACKUP = original.ROOT / "reports/_review/mobile-compact-before-20261013"
CARDS = original.CARDS
TABLES = original.TABLES
HOME_PAGE = "364f2cdd67ba7822850c"
HOME_PROVIDER_SHORTCUT = "a786374f5b2d40d37613"
HOME_BUTTONS = ("88abb8e9012a51c31712", "feac96019202c65a5eca", "a214f7d8c8a55d927cd1", HOME_PROVIDER_SHORTCUT)
HOME_BADGES = {HOME_BUTTONS[0]: "wmpp-sidebar-chart-no-axes-combined.svg",
               HOME_BUTTONS[1]: "wmpp-sidebar-user-round-plus.svg",
               HOME_BUTTONS[2]: "wmpp-sidebar-user-round-plus.svg",
               HOME_PROVIDER_SHORTCUT: "wmpp-sidebar-building-complex.svg"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def kind(source):
    return source.get("visual", {}).get("visualType", "group")


def literal(number):
    return original.literal(f"{number:g}D")


def number(value):
    if not isinstance(value, dict):
        return None
    match = re.fullmatch(r"(-?\d+(?:\.\d+)?)[DL]?", original.decode(value))
    return float(match[1]) if match else None


def set_props(objects, group, values, selector=None):
    entries = objects.setdefault(group, [])
    entry = next((e for e in entries if e.get("selector") == selector), None)
    if entry is None:
        entry = {"properties": {}}
        if selector is not None:
            entry["selector"] = deepcopy(selector)
        entries.append(entry)
    entry.setdefault("properties", {}).update(values)


def smaller_font(objects, group, target, selector=None):
    entry = next((e for e in objects.get(group, []) if e.get("selector") == selector), {})
    current = number(entry.get("properties", {}).get("fontSize", {}))
    return {"fontSize": literal(min(target, current) if current is not None else target)}


def complete_button_text(source_entries, mobile_entries):
    """Keep phone sizing while supplying each native button state's label.

    An unscoped label alone does not populate the native Default-state field.
    Intentionally unlabelled/icon-only controls remain unlabelled.
    """
    def props(entries, selector):
        return next((e.get("properties", {}) for e in entries
                     if e.get("selector") == selector), {})

    def has_text(value):
        return bool(value) and ("Literal" not in value.get("expr", {})
                                or bool(original.decode(value).strip()))

    fallback = next((e.get("properties", {}) for e in source_entries
                     if has_text(e.get("properties", {}).get("text"))), None)
    if fallback is None:
        return deepcopy(mobile_entries)
    source_base = props(source_entries, None)
    mobile_base = props(mobile_entries, None)
    result = []
    for name in (None, "default", "hover", "selected", "disabled"):
        selector = {"id": name} if name else None
        source_state = props(source_entries, selector)
        combined = deepcopy(fallback)
        combined.update(deepcopy(source_base))
        combined.update(deepcopy(source_state))
        phone_base = deepcopy(mobile_base)
        # A general phone label must not erase a state's distinct label.
        if name and has_text(source_state.get("text")):
            phone_base.pop("text", None)
        combined.update(phone_base)
        combined.update(deepcopy(props(mobile_entries, selector)))
        if not has_text(combined.get("text")):
            combined["text"] = deepcopy(source_state.get("text") or fallback["text"])
        entry = {"properties": combined}
        if selector:
            entry["selector"] = selector
        result.append(entry)
    # Preserve any non-standard selector rather than discarding custom states.
    result.extend(deepcopy(e) for e in mobile_entries
                  if e.get("selector") not in [None] + [{"id": n} for n in
                      ("default", "hover", "selected", "disabled")])
    return result


def phone_home_button_format(source, state):
    """Use a single existing orange/white badge beside the homepage title."""
    objects = state.setdefault("objects", {})
    src = source["visual"]["objects"]
    objects["text"] = complete_button_text(src.get("text", []), objects.get("text", []))
    original_icons = src.get("icon", [])
    default_icon = next((e.get("properties", {}) for e in original_icons
                         if e.get("selector") is None), {})
    phone_icons = deepcopy(objects.get("icon", []))
    objects["icon"] = []
    for name in (None, "default", "hover", "selected", "disabled"):
        selector = {"id": name} if name else None
        icon = deepcopy(default_icon)
        for entry in original_icons:
            if entry.get("selector") == selector:
                icon.update(deepcopy(entry.get("properties", {})))
        for entry in phone_icons:
            if entry.get("selector") == selector:
                icon.update(deepcopy(entry.get("properties", {})))
        asset = HOME_BADGES[source["name"]]
        icon.update(show=original.literal("true"), placement=original.literal("'custom'"), iconSize=literal(32),
                    horizontalAlignment=original.literal("'left'"),
                    verticalAlignment=original.literal("'middle'"),
                    leftMargin=literal(12), rightMargin=literal(0),
                    topMargin=literal(0), bottomMargin=literal(0))
        icon["image"] = {"image": {"name": original.literal(original.quote(asset)),
            "url": {"expr": {"ResourcePackageItem": {"PackageName": "RegisteredResources",
                "PackageType": 1, "ItemName": asset}}}, "scaling": original.literal("'Fit'")}}
        set_props(objects, "icon", icon, selector)
        # The Desktop button's orange circle is a separate fill image. Hide
        # that layer on phone, where the icon image now includes the circle.
        set_props(objects, "fill", {"show": original.literal("false")}, selector)
        set_props(objects, "text", {"horizontalAlignment": original.literal("'left'"),
                  "verticalAlignment": original.literal("'middle'"), "leftMargin": literal(52),
                  "rightMargin": literal(8), "topMargin": literal(0), "bottomMargin": literal(0)}, selector)
    assert not button_icon_text_collisions(source, state), "Homepage icon/title areas still collide."
    assert not home_badge_errors(source, state), "Homepage badge and symbol are separated."


def hidden(vid, sources, override=None):
    override = override or {}
    source = sources[vid]
    own = override.get(vid, bool(source.get("isHidden")))
    parent = source.get("parentGroupName")
    return own or (hidden(parent, sources, override) if parent else False)


def filter_group(vid, sources):
    parent = sources[vid].get("parentGroupName")
    while parent:
        if "Filters drawer" in sources[parent].get("visualGroup", {}).get("displayName", ""):
            return parent
        parent = sources[parent].get("parentGroupName")
    return None


def relevant(source):
    return kind(source) not in {"group", "shape"} and not (
        kind(source) == "textbox" and not original.plain(source).strip()
    )


def overlap(a, b):
    return (min(a["x"] + a["width"], b["x"] + b["width"]) - max(a["x"], b["x"]) > 0.1
            and min(a["y"] + a["height"], b["y"] + b["height"]) - max(a["y"], b["y"]) > 0.1)


def effective_button_props(source, mobile, group, name):
    values = {}
    for objects in (source.get("visual", {}).get("objects", {}), mobile.get("objects", {})):
        for selector in (None, {"id": name}):
            for entry in objects.get(group, []):
                if entry.get("selector") == selector:
                    values.update(deepcopy(entry.get("properties", {})))
    return values


def button_icon_text_collisions(source, mobile):
    """Check reserved icon/text areas, including state-specific inheritance.

    This guards content geometry inside one visual; it is not a native render.
    """
    errors = []
    rect = mobile["position"]
    for name in ("default", "hover", "selected", "disabled"):
        icon = effective_button_props(source, mobile, "icon", name)
        text = effective_button_props(source, mobile, "text", name)
        if original.decode(icon.get("show", {})) != "true" or original.decode(text.get("show", {})) != "true":
            continue
        if original.decode(icon.get("placement", {})) != "custom":
            continue
        def margins(properties):
            return [number(properties.get(key, {})) or 0 for key in
                    ("leftMargin", "topMargin", "rightMargin", "bottomMargin")]
        il, it, ir, ib = margins(icon)
        tl, tt, tr, tb = margins(text)
        size = number(icon.get("iconSize", {}))
        assert size is not None, "Custom icon must have an explicit size."
        width, height = rect["width"], rect["height"]
        align_x = original.decode(icon.get("horizontalAlignment", {}))
        align_y = original.decode(icon.get("verticalAlignment", {}))
        icon_rect = {"x": il if align_x == "left" else width - ir - size if align_x == "right" else
                     il + (width - il - ir - size) / 2,
                     "y": it if align_y == "top" else height - ib - size if align_y == "bottom" else
                     it + (height - it - ib - size) / 2,
                     "width": size, "height": size}
        text_rect = {"x": tl, "y": tt, "width": width - tl - tr, "height": height - tt - tb}
        if overlap(icon_rect, text_rect):
            errors.append(name)
    return errors


def check_home_buttons():
    root = REPORT / "pages" / HOME_PAGE / "visuals"
    return {vid: button_icon_text_collisions(read(root / vid / "visual.json"), read(root / vid / "mobile.json"))
            for vid in HOME_BUTTONS}


def home_badge_errors(source, mobile):
    """Ensure the white symbol moves together with its orange backdrop."""
    errors = []
    for name in ("default", "hover", "selected", "disabled"):
        icon = effective_button_props(source, mobile, "icon", name)
        fill = effective_button_props(source, mobile, "fill", name)
        asset = icon.get("image", {}).get("image", {}).get("url", {}).get("expr", {}).get("ResourcePackageItem", {}).get("ItemName")
        if asset != HOME_BADGES[source["name"]] or original.decode(icon.get("show", {})) != "true":
            errors.append((name, "Icon does not contain its orange badge"))
        if original.decode(fill.get("show", {})) != "false":
            errors.append((name, "Separate centred background badge is still enabled"))
    return errors


def check_home_badges():
    root = REPORT / "pages" / HOME_PAGE / "visuals"
    return {vid: home_badge_errors(read(root / vid / "visual.json"), read(root / vid / "mobile.json"))
            for vid in HOME_BUTTONS}


def phone_format(source, state, captions):
    objects = state.setdefault("objects", {})
    src = source.get("visual", {}).get("objects", {})
    vt = kind(source)
    refs = original.references(source)
    rect = state["position"]
    journey = any(re.search(r"(Journey providers|Rail referrals|Journey detail label) \d$", r) for r in refs)
    context = any("context" in r.lower() or "summary" in r.lower() or "As Of" in r
                  or "Gold Model Last Refreshed" in r for r in refs)
    value_size = 9 if context or any("Journey detail label" in r or r.endswith("Journey providers 4") for r in refs) else 14 if journey else 20
    for group, entries in src.items():
        for entry in entries:
            updates = {}
            for key, value in entry.get("properties", {}).items():
                numeric = number(value)
                if numeric is None:
                    continue
                if key in {"fontSize", "textSize", "labelFontSize"}:
                    target = value_size if group in {"value", "calloutValue", "dataLabels"} and vt in CARDS else 9
                    if vt == "actionButton":
                        target = 10
                    updates[key] = literal(max(8, min(target, math.ceil(numeric * SCALE))))
                elif key in {"leftMargin", "rightMargin", "topMargin", "bottomMargin", "cellPadding",
                             "leftOuterMargin", "rightOuterMargin", "topOuterMargin", "bottomOuterMargin",
                             "roundEdge", "rectangleRoundedCurve", "imageSize", "iconSize"}:
                    updates[key] = literal(round(numeric * SCALE, 2))
            if updates:
                set_props(objects, group, updates, entry.get("selector"))
    if vt in CARDS:
        set_props(objects, "value", smaller_font(objects, "value", value_size))
        set_props(objects, "label", smaller_font(objects, "label", 9))
        for group in ("referenceLabelValue", "referenceLabelTitle"):
            if group in src:
                for entry in src[group]:
                    selector = entry.get("selector")
                    set_props(objects, group, smaller_font(objects, group, 9, selector), selector)
    if vt in TABLES:
        set_props(objects, "columnHeaders", smaller_font(objects, "columnHeaders", 9))
        set_props(objects, "values", smaller_font(objects, "values", 9))
        if vt == "pivotTable":
            set_props(objects, "rowHeaders", {"fontSize": literal(9)})
        set_props(objects, "grid", {"rowPadding": literal(3)})
        for entry in src.get("columnWidth", []):
            width = number(entry.get("properties", {}).get("value", {}))
            if width is not None:
                set_props(objects, "columnWidth", {"value": literal(0 if width == 0 else max(36, round(width * SCALE, 2)))}, entry.get("selector"))
    if vt == "actionButton":
        for entry in src.get("text", [{}]):
            selector = entry.get("selector")
            existing = next((e for e in objects.get("text", []) if e.get("selector") == selector), {})
            complete_text = deepcopy(entry.get("properties", {}))
            complete_text.update(deepcopy(existing.get("properties", {})))
            set_props(objects, "text", complete_text, selector)
            set_props(objects, "text", {**smaller_font(objects, "text", 10, entry.get("selector")), "leftMargin": literal(8),
                      "rightMargin": literal(8), "topMargin": literal(0), "bottomMargin": literal(0)}, entry.get("selector"))
        objects["text"] = complete_button_text(src.get("text", []), objects.get("text", []))
        if source["name"] in HOME_BUTTONS:
            phone_home_button_format(source, state)
    if vt == "slicer":
        for group in ("items", "header"):
            set_props(objects, group, {"fontSize": literal(9)})
    if vt == "textbox":
        entries = objects.get("general", src.get("general", []))
        for entry in entries:
            paragraphs = entry.get("properties", {}).get("paragraphs")
            if paragraphs is None:
                continue
            paragraphs = deepcopy(paragraphs)
            alt = original.alt(source)
            main_heading = alt.startswith("Mobile:") and rect["z"] == 500000
            for para in paragraphs:
                for run in para.get("textRuns", []):
                    style = run.setdefault("textStyle", {})
                    current = re.match(r"([0-9.]+)", str(style.get("fontSize", "12pt")))
                    short_heading = len(original.plain(source)) < 60 and current and float(current[1]) >= 14
                    size = 14 if main_heading else 13 if original.plain(source) == "WMPP" else 12 if short_heading else 9
                    style["fontSize"] = f"{max(8, min(size, math.ceil(float(current[1]) * SCALE) if current else size))}pt"
            set_props(objects, "general", {"paragraphs": paragraphs}, entry.get("selector"))
    container = state.setdefault("visualContainerObjects", {})
    set_props(container, "title", {"fontSize": literal(10), "titleWrap": original.literal("true")})
    set_props(container, "subTitle", {"fontSize": literal(9)})
    # Retain mobile captions that replaced separate Desktop-only headings.
    dynamic_title = any("text" in entry.get("properties", {})
                        and "Literal" not in entry["properties"]["text"].get("expr", {})
                        for entry in source.get("visual", {}).get("visualContainerObjects", {}).get("title", []))
    if source["name"] in captions and not original.title(source) and not dynamic_title:
        set_props(container, "title", {"show": original.literal("true"),
                  "text": original.literal(original.quote(captions[source["name"]]))})
    if journey:
        set_props(container, "title", {"show": original.literal("false")})
    state["$schema"] = SCHEMA


def compact_page(folder):
    sources = {p.parent.name: read(p) for p in folder.glob("*/visual.json")}
    before = {p.parent.name: read(p) for p in folder.glob("*/mobile.json")}
    mobile = deepcopy(before)
    captions = {}
    page_path = folder.parent / "page.json"
    # Reuse the existing layout builder's label matching, not its geometry.
    rebuilt = original.PhonePage(folder.parent.name, read(page_path), sources).plan()
    for vid, state in rebuilt.mobile.items():
        entries = state.get("visualContainerObjects", {}).get("title", [])
        if entries and "text" in entries[0].get("properties", {}):
            captions[vid] = original.decode(entries[0]["properties"]["text"])
    for vid, state in mobile.items():
        rect = state["position"]
        rect["y"] = round(rect["y"] * SCALE, 2)
        rect["height"] = math.ceil(rect["height"] * SCALE)
        if kind(sources[vid]) == "actionButton":
            rect["height"] = max(36, rect["height"])
        if kind(sources[vid]) == "image" and abs(rect["width"] - before[vid]["position"]["height"]) < 1:
            rect["width"] = rect["height"] = max(36, rect["height"])
        phone_format(sources[vid], state, captions)
    # Saved mobile positions are independent of Desktop group coordinates.
    # Normalise the old filter panel's local positions into explicit phone rows.
    group_ids = {filter_group(vid, sources) for vid in mobile} - {None}
    for gid in group_ids:
        children = [vid for vid in mobile if filter_group(vid, sources) == gid]
        fields = sorted([vid for vid in children if kind(sources[vid]) == "slicer" or "Filter" in kind(sources[vid])],
                        key=lambda vid: sources[vid]["position"]["y"])
        top = 109
        for index, vid in enumerate(fields):
            mobile[vid]["position"].update(x=10, y=top + 44 + index * 90, width=303, height=80, z=700010 + index)
        for vid in children:
            if kind(sources[vid]) == "shape":
                mobile[vid]["position"].update(x=0, y=top, width=WIDTH, height=56 + len(fields) * 90, z=700000)
            elif kind(sources[vid]) == "textbox":
                mobile[vid]["position"].update(x=10, y=top + 8, width=210, height=30, z=700005)
    visible = [vid for vid in mobile if not hidden(vid, sources) and relevant(sources[vid])
               and not filter_group(vid, sources)]
    rows = []
    body = [vid for vid in visible if mobile[vid]["position"]["z"] < 500000]
    for vid in sorted(body, key=lambda key: (before[key]["position"]["y"], before[key]["position"]["x"])):
        rect = mobile[vid]["position"]
        row = next((row for row in rows if abs(row["original_y"] - before[vid]["position"]["y"]) < 2
                    and all(rect["x"] + rect["width"] <= mobile[other]["position"]["x"] + 0.1
                            or rect["x"] >= mobile[other]["position"]["x"] + mobile[other]["position"]["width"] - 0.1
                            for other in row["ids"])), None)
        if row is None:
            row = {"original_y": before[vid]["position"]["y"], "ids": []}
            rows.append(row)
        row["ids"].append(vid)
    cursor = max((mobile[vid]["position"]["y"] + mobile[vid]["position"]["height"]
                  for vid in visible if mobile[vid]["position"]["z"] >= 500000), default=48) + GAP
    for row in rows:
        y = max(cursor, round(row["original_y"] * SCALE, 2))
        for vid in row["ids"]:
            mobile[vid]["position"]["y"] = y
        cursor = y + max(mobile[vid]["position"]["height"] for vid in row["ids"]) + GAP
    # Hidden chart/table alternatives retain exactly their visible counterpart's slot.
    for vid in mobile:
        if not hidden(vid, sources) or filter_group(vid, sources) or kind(sources[vid]) in {"textbox", "image", "shape", "actionButton", "group"}:
            continue
        old = before[vid]["position"]
        anchors = [other for other in body if kind(sources[other]) not in CARDS and
                   all(abs(old[key] - before[other]["position"][key]) < 1 for key in ("x", "y", "width", "height"))]
        if anchors:
            mobile[vid]["position"].update({key: mobile[anchors[0]]["position"][key] for key in ("x", "y", "width", "height")})
    assert not [(a, b) for i, a in enumerate(visible) for b in visible[i + 1:]
                if overlap(mobile[a]["position"], mobile[b]["position"])], folder.parent.name
    return before, mobile, sources


def protected():
    files = {p.relative_to(PROJECT).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for root in (PROJECT / "SM_WMPP_v16.Report/definition", PROJECT / "SM_WMPP_v16.SemanticModel/definition")
             for p in root.rglob("*") if p.is_file() and p.name != "mobile.json"}
    return {"files": len(files), "fingerprint": original.digest_mapping(files)}


def check_bookmark_table_tiles(sources, mobile, bookmarks, pid):
    checked = 0
    for bookmark in bookmarks:
        section = bookmark.get("explorationState", {}).get("sections", {}).get(pid)
        if section is None:
            continue
        overrides = {}
        targets = bookmark.get("options", {}).get("targetVisualNames")
        scoped = bookmark.get("options", {}).get("applyOnlyToTargetVisuals")
        for vid, entry in section.get("visualContainers", {}).items():
            if vid in sources and (not scoped or not targets or vid in targets):
                single = entry.get("singleVisual", {})
                overrides[vid] = single.get("display", {}).get("mode") == "hidden"
        for vid, entry in section.get("visualContainerGroups", {}).items():
            if vid in sources and (not scoped or not targets or vid in targets):
                overrides[vid] = bool(entry.get("isHidden"))
        visible = [vid for vid in mobile if not hidden(vid, sources, overrides)
                   and not filter_group(vid, sources) and kind(sources[vid]) in CARDS | TABLES]
        collisions = [(a, b) for a in visible if kind(sources[a]) in TABLES
                      for b in visible if kind(sources[b]) in CARDS
                      and overlap(mobile[a]["position"], mobile[b]["position"])]
        assert not collisions, (pid, bookmark.get("displayName"), collisions)
        checked += 1
    return checked


def patch_file(path, value, executable):
    assert path.resolve().is_relative_to(PROJECT.resolve()) or path.resolve().is_relative_to(BACKUP.resolve())
    old = path.read_text(encoding="utf-8-sig") if path.exists() else None
    new = original.json_text(value) if not isinstance(value, str) else value
    if old is not None and old.replace("\r\n", "\n") == new:
        return
    header = ("*** Update File: " if old is not None else "*** Add File: ") + path.name + "\n"
    body = ("@@\n" + "\n".join("-" + line for line in old.splitlines()) + "\n" if old is not None else "")
    body += "\n".join("+" + line for line in new.splitlines()) + "\n"

    def invoke(payload):
        command = [executable, "--codex-run-as-apply-patch", payload]
        assert len(subprocess.list2cmdline(command)) < 30000, path
        result = subprocess.run(command, cwd=path.parent, capture_output=True, encoding="utf-8", errors="replace")
        assert result.returncode == 0, result.stderr or result.stdout

    payload = "*** Begin Patch\n" + header + body + "*** End Patch"
    if len(subprocess.list2cmdline([executable, "--codex-run-as-apply-patch", payload])) < 28000:
        invoke(payload)
    elif old is not None:
        # Prefer exact changed hunks to repeating both whole documents, keeping
        # one context-checked edit whenever it fits Windows' argument limit.
        diff = list(difflib.unified_diff(old.splitlines(), new.splitlines(), n=3))[2:]
        body = "\n".join("@@" if line.startswith("@@") else line for line in diff) + "\n"
        smaller = "*** Begin Patch\n" + header + body + "*** End Patch"
        if len(subprocess.list2cmdline([executable, "--codex-run-as-apply-patch", smaller])) < 28000:
            invoke(smaller)
        else:
            # Complete button replacements or bulk delivery-inventory changes
            # can exceed Windows' argument limit even as minimal diffs. Rebuild
            # only an exact backed-up visual or this root delivery manifest via
            # bounded apply_patch additions. Never allow models/mobile states.
            if path.name == "visual.json":
                assert path.resolve().is_relative_to((PROJECT / "SM_WMPP_v16.Report/definition/pages").resolve())
            else:
                assert path.resolve() == MANIFEST.resolve()
            recovery = BACKUP / path.relative_to(PROJECT)
            assert recovery.is_file() and recovery.read_bytes() == path.read_bytes(), "Missing exact pre-edit recovery copy."
            invoke("*** Begin Patch\n*** Delete File: " + path.name + "\n*** End Patch")
            patch_file(path, value, executable)
    else:
        lines = new.splitlines()
        cursor = 0
        while cursor < len(lines):
            first = cursor == 0
            prefix = "*** Begin Patch\n" + ("*** Add File: " + path.name + "\n" if first else
                     "*** Update File: " + path.name + "\n@@\n" + "\n".join(" " + line for line in lines[max(0, cursor - 3):cursor]) + "\n")
            tail = ("" if first else "*** End of File\n") + "*** End Patch"
            end = cursor
            body = ""
            while end < len(lines):
                candidate = body + "+" + lines[end] + "\n"
                if len(subprocess.list2cmdline([executable, "--codex-run-as-apply-patch", prefix + candidate + tail])) > 22000:
                    break
                body = candidate
                end += 1
            assert end > cursor
            invoke(prefix + body + tail)
            cursor = end
    if isinstance(value, str):
        assert path.read_text().strip() == value.strip()
    else:
        assert read(path) == value


def check_saved(manifest, schema=False):
    assert protected() == manifest["protected"], "Desktop, model or bookmarks changed"
    checks, pages, state_checks = [], [], 0
    bookmarks = [read(p) for p in (REPORT / "bookmarks").glob("*.bookmark.json")]
    for page in manifest["pages"]:
        folder = REPORT / "pages" / page["id"] / "visuals"
        sources = {p.parent.name: read(p) for p in folder.glob("*/visual.json")}
        mobile = {p.parent.name: read(p) for p in folder.glob("*/mobile.json")}
        assert set(mobile) == set(page["mobile_ids"]), page["name"]
        visible = [vid for vid in mobile if relevant(sources[vid]) and not hidden(vid, sources)
                   and not filter_group(vid, sources)]
        for vid, value in mobile.items():
            rect = value["position"]
            assert 0 <= rect["x"] and rect["x"] + rect["width"] <= WIDTH + 0.1, (page["name"], vid, rect)
            assert rect["y"] >= 0 and rect["height"] > 0
            if kind(sources[vid]) == "actionButton":
                assert rect["height"] >= 36, (page["name"], vid, "Small button")
            checks.append((str(folder / vid / "mobile.json"), value))
        overlaps = [(a, b) for i, a in enumerate(visible) for b in visible[i + 1:]
                    if overlap(mobile[a]["position"], mobile[b]["position"])]
        assert not overlaps, (page["name"], overlaps)
        state_checks += check_bookmark_table_tiles(sources, mobile, bookmarks, page["id"])
        pages.append({"name": page["name"], "mobile_visuals": len(mobile), "visible_overlaps": 0,
                      "height": max((mobile[v]["position"]["y"] + mobile[v]["position"]["height"] for v in visible), default=0)})
    return {"pages": len(pages), "mobile_visuals": sum(p["mobile_visuals"] for p in pages),
            "desktop_and_model_preserved": not bool(manifest.get("authorised_definition_updates")),
            "definitions_match_authorised_baseline": True, "semantic_model_preserved": True, "visible_overlaps": 0,
            "bookmark_page_states_checked": state_checks, "bookmark_table_tile_overlaps": 0,
            "phone_render_verified": False, "schema": original.validate_documents(checks) if schema else {},
            "page_inventory": pages}


def validate_home_badge_assets():
    packages = read(REPORT / "report.json")["resourcePackages"]
    registered = next(p for p in packages if p["name"] == "RegisteredResources")
    resources = PROJECT / "SM_WMPP_v16.Report/StaticResources/RegisteredResources"
    names = {item["name"] for item in registered["items"]}
    for asset in set(HOME_BADGES.values()):
        assert asset in names, (asset, "Existing badge is not registered.")
        tree = ET.parse(resources / asset)
        circle = tree.find("{http://www.w3.org/2000/svg}circle")
        glyph = tree.find("{http://www.w3.org/2000/svg}g")
        assert circle is not None and circle.get("fill") == "#EF7911", asset
        assert glyph is not None and glyph.get("stroke") == "#FFFFFF" and len(glyph), asset


def repair_home_buttons(executable, validate=False, backup_name="mobile-home-button-spacing-20261013"):
    validate_home_badge_assets()
    root = REPORT / "pages" / HOME_PAGE / "visuals"
    baseline = protected()
    changes = []
    for vid in HOME_BUTTONS:
        path = root / vid / "mobile.json"
        source, before = read(path.with_name("visual.json")), read(path)
        after = deepcopy(before)
        phone_home_button_format(source, after)
        assert after["position"] == before["position"], "Do not resize or move homepage rows."
        assert after.get("visualContainerObjects") == before.get("visualContainerObjects")
        assert {k: v for k, v in after["objects"].items() if k not in {"icon", "text", "fill"}} == {
            k: v for k, v in before["objects"].items() if k not in {"icon", "text", "fill"}}
        changes.append((path, before, after))
    schemas = original.validate_documents([(str(path), after) for path, _, after in changes]) if validate else {}
    print(json.dumps({"homepage_buttons": len(changes), "schema": schemas}), flush=True)
    backup = original.ROOT / "reports/_review" / backup_name
    if backup.exists():
        # A prior attempt stopped before any report edits. Never replace its
        # backup or resume if even one target has changed since that snapshot.
        assert all(path.read_bytes() == (backup / path.relative_to(PROJECT)).read_bytes()
                   for path, _, _ in changes), "Inspect changes against the existing backup before repeating."
    else:
        backup.mkdir(parents=True)
        for path, _, _ in changes:
            saved = backup / path.relative_to(PROJECT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
    global BACKUP
    BACKUP = backup
    patch_file(backup / ".gitignore", "*\n", executable)
    assert protected() == baseline, "Definitions changed before applying."
    for path, before, after in changes:
        assert read(path) == before, "Phone settings changed before applying."
        patch_file(path, after, executable)
    assert protected() == baseline, "Non-mobile definitions changed."
    assert not any(check_home_buttons().values()), "Saved homepage spacing check failed."
    assert not any(check_home_badges().values()), "Saved homepage badge check failed."
    print(json.dumps({"saved_buttons": len(changes), "icon_title_collisions": 0,
                      "non_mobile_files_unchanged": True, "backup": str(backup),
                      "native_render_verified": False}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--check-home-buttons", action="store_true")
    parser.add_argument("--repair-home-buttons-via")
    parser.add_argument("--check-home-badges", action="store_true")
    parser.add_argument("--repair-home-badges-via")
    args = parser.parse_args()
    if args.check_home_buttons:
        failures = {vid: states for vid, states in check_home_buttons().items() if states}
        print(json.dumps({"homepage_buttons": len(HOME_BUTTONS), "icon_title_collisions": failures}))
        raise SystemExit(1 if failures else 0)
    if args.check_home_badges:
        failures = {vid: states for vid, states in check_home_badges().items() if states}
        print(json.dumps({"homepage_buttons": len(HOME_BUTTONS), "badge_failures": failures}))
        raise SystemExit(1 if failures else 0)
    if args.repair_home_buttons_via:
        repair_home_buttons(args.repair_home_buttons_via, args.validate)
        return
    if args.repair_home_badges_via:
        repair_home_buttons(args.repair_home_badges_via, args.validate, "mobile-home-badges-20261013")
        return
    if args.verify:
        print(json.dumps(check_saved(read(MANIFEST), args.validate)))
        return
    assert not MANIFEST.exists(), "Already compacted; use --verify, do not shrink twice."
    baseline = protected()
    plans, pages, documents = {}, [], []
    delivery = read(PROJECT / "MOBILE_LAYOUT_DELIVERY.json")
    bookmarks = [read(p) for p in (REPORT / "bookmarks").glob("*.bookmark.json")]
    for page in delivery["pages"]:
        folder = REPORT / "pages" / page["id"] / "visuals"
        before, after, sources = compact_page(folder)
        check_bookmark_table_tiles(sources, after, bookmarks, page["id"])
        visible = [vid for vid in after if relevant(sources[vid]) and not hidden(vid, sources) and not filter_group(vid, sources)]
        pages.append({"id": page["id"], "name": page["name"], "mobile_ids": sorted(after),
                      "before_height": max((before[v]["position"]["y"] + before[v]["position"]["height"] for v in visible), default=0),
                      "after_height": max((after[v]["position"]["y"] + after[v]["position"]["height"] for v in visible), default=0)})
        for vid, value in after.items():
            path = folder / vid / "mobile.json"
            if value != before[vid]:
                plans[path] = value
            documents.append((str(path), value))
    manifest = {"version": 1, "date": "2026-10-13", "project": str(PROJECT), "vertical_scale": SCALE,
                "canvas_width": WIDTH, "body_font_points": 9, "button_font_points": 10,
                "table_font_points": 9, "table_row_padding": 3, "minimum_button_height": 36,
                "protected": baseline, "backup": str(BACKUP), "pages": pages,
                "phone_render_verified": False}
    schema_check = original.validate_documents(documents) if args.validate else {}
    print(json.dumps({"planned_mobile_files": len(plans), "pages": len(pages), "schema": schema_check,
                      "page_heights": [{"name": p["name"], "before": p["before_height"], "after": p["after_height"]} for p in pages]}), flush=True)
    if not args.apply_via:
        return
    assert not BACKUP.exists(), "Backup exists; inspect interrupted application before retrying."
    BACKUP.mkdir(parents=True)
    for path in plans:
        backup = BACKUP / path.relative_to(PROJECT)
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, backup)
    patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert protected() == baseline, "Definitions changed before applying; no edits performed."
    for index, (path, value) in enumerate(plans.items(), 1):
        assert path.read_bytes() == (BACKUP / path.relative_to(PROJECT)).read_bytes(), f"File changed during patch: {path}"
        patch_file(path, value, args.apply_via)
        if index % 50 == 0:
            print(json.dumps({"applied_mobile_files": index}), flush=True)
    patch_file(MANIFEST, manifest, args.apply_via)
    qa = check_saved(manifest, args.validate)
    patch_file(QA, qa, args.apply_via)
    print(json.dumps({"complete": True, "checks": qa}), flush=True)


if __name__ == "__main__":
    main()
