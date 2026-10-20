"""Give Referral Explorer an Offers-style phone filter panel.

Desktop slicers stay in place. Phone copies share pair-specific sync groups;
the person-search control and model are not edited.
"""

import argparse
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original

PID = "f3070e87127b751f89d4"
SEARCH = "351ae29accd0f482e860"
REFERENCE = "1f33996970651e846183"
ROOT = original.REPORT / "pages" / PID / "visuals"
REF_ROOT = original.REPORT / "pages" / REFERENCE / "visuals"
BACKUP = original.ROOT / "reports/_review/referral-mobile-filters-before-20261014"
MANIFEST = original.PROJECT / "REFERRAL_MOBILE_FILTERS_DELIVERY.json"
IDS = {role: original.ident(PID + ":phone-filter-panel-v1:" + role)
       for role in ("group", "background", "heading", "open", "close", "open-bookmark", "close-bookmark")}
NAV_OPEN = "9c04003e120ab12e0b01"


def sources():
    return {p.parent.name: original.read(p) for p in ROOT.glob("*/visual.json")}


def candidates(values):
    return [v for v in values.values() if original.vtype(v) == "slicer"
            and not compact.hidden(v["name"], values)]


def panel_ids(page_id):
    return {role: original.ident(page_id + ":phone-filter-panel-v1:" + role)
            for role in IDS}


def paired_slicer(source, index, page_id=PID, group_id=None):
    origin = deepcopy(source)
    prefix = "wmpp_referral_phone_" if page_id == PID else "wmpp_phone_" + page_id + "_"
    sync = {"groupName": prefix + source["name"], "fieldChanges": True, "filterChanges": True}
    assert not origin["visual"].get("syncGroup"), "Preserve and inspect an existing sync group before extending it."
    origin["visual"]["syncGroup"] = sync
    clone = deepcopy(origin)
    clone["name"] = original.ident(page_id + ":phone-filter-panel-v1:slicer:" + source["name"])
    clone["parentGroupName"] = group_id or panel_ids(page_id)["group"]
    clone.pop("isHidden", None)
    clone["position"] = original.position(10, 44 + index * 90, 303, 80, 10 + index, 10 + index)
    return origin, clone


def bookmark(opened, page_id=PID, page_name="Referral Explorer"):
    ids = panel_ids(page_id)
    return {"$schema": original.BASE + "bookmark/2.1.0/schema.json",
        "name": ids["open-bookmark" if opened else "close-bookmark"],
        "displayName": "Mobile | " + page_name + " | " + ("open" if opened else "close") + " filters",
        "options": {"applyOnlyToTargetVisuals": True, "targetVisualNames": [ids["group"], ids["close"]],
                    "suppressActiveSection": True, "suppressData": True},
        "explorationState": {"version": "1.0", "activeSection": page_id, "sections": {page_id: {
            "visualContainers": {ids["close"]: {"singleVisual": {"visualType": "actionButton", "objects": {},
                **({} if opened else {"display": {"mode": "hidden"}})}}},
            "visualContainerGroups": {ids["group"]: {"isHidden": not opened}}}}}}


def make_plan():
    assert not (ROOT / IDS["group"] / "visual.json").exists(), "Already grouped; use --verify."
    values = sources()
    mobile = {p.parent.name: original.read(p) for p in ROOT.glob("*/mobile.json")}
    filters = candidates(values)
    assert len(filters) == 11 and SEARCH not in {v["name"] for v in filters}
    # Retain the current phone order; the Desktop-only referral-ID selector is last.
    filters.sort(key=lambda v: mobile.get(v["name"], {}).get("position", {}).get("y", 1e9))
    top = mobile[SEARCH]["position"]["y"] + mobile[SEARCH]["position"]["height"] + 8
    panel_top, height = top + 39 + 8, 56 + len(filters) * 90
    additions, deletes, pairs = {}, [], []
    group = original.read(REF_ROOT / "1c58e933994fd21e7496/visual.json")
    group["name"] = IDS["group"]
    group["position"] = original.position(2040, 20, 323, height, 50010, 99000)
    group["visualGroup"]["displayName"] = "Referral Explorer | Mobile Filters drawer"
    group["isHidden"] = True
    additions[ROOT / IDS["group"] / "visual.json"] = group
    for role, template in (("background", "ef5d33a4ad5ff21c1029"), ("heading", "03e8287a57b1a615f63d")):
        source = original.read(REF_ROOT / template / "visual.json")
        phone = original.read(REF_ROOT / template / "mobile.json")
        source["name"], source["parentGroupName"] = IDS[role], IDS["group"]
        source["position"] = original.position(0 if role == "background" else 10,
            0 if role == "background" else 8, 323 if role == "background" else 210,
            height if role == "background" else 30, 0 if role == "background" else 1)
        phone["position"] = original.position(source["position"]["x"], panel_top + source["position"]["y"],
            source["position"]["width"], source["position"]["height"], 50010 if role == "background" else 50011)
        additions[ROOT / IDS[role] / "visual.json"] = source
        additions[ROOT / IDS[role] / "mobile.json"] = phone
    for role, template in (("open", "8ea73a405f7ef268214c"), ("close", "8fde89f83526ca1ffa03")):
        source = original.read(REF_ROOT / template / "visual.json")
        phone = original.read(REF_ROOT / template / "mobile.json")
        source["name"] = IDS[role]
        source["position"] = original.position(2040, 20, 323, 48, 50050, 99010)
        source.pop("parentGroupName", None)
        if role == "close": source["isHidden"] = True
        else: source.pop("isHidden", None)
        compact.set_props(source["visual"]["visualContainerObjects"], "visualLink", {
            "bookmark": original.literal(original.quote(IDS[role + "-bookmark"]))})
        compact.set_props(source["visual"]["visualContainerObjects"], "general", {
            "altText": original.literal(original.quote("Mobile: Referral Explorer " + role + " filters"))})
        phone["position"] = original.position(0 if role == "open" else 235,
            top if role == "open" else panel_top + 6, 323 if role == "open" else 76,
            39 if role == "open" else 36, 50060 if role == "open" else 50050, 110 if role == "open" else 120)
        phone["objects"]["text"] = compact.complete_button_text(source["visual"]["objects"]["text"], phone["objects"]["text"])
        additions[ROOT / IDS[role] / "visual.json"] = source
        additions[ROOT / IDS[role] / "mobile.json"] = phone
    sample_phone = mobile[filters[0]["name"]]
    for index, source in enumerate(filters):
        origin, clone = paired_slicer(source, index)
        phone = deepcopy(mobile.get(source["name"], sample_phone))
        phone["position"] = original.position(10, panel_top + 44 + index * 90, 303, 80, 50012 + index, 130 + index)
        additions[ROOT / source["name"] / "visual.json"] = origin
        additions[ROOT / clone["name"] / "visual.json"] = clone
        additions[ROOT / clone["name"] / "mobile.json"] = phone
        if source["name"] in mobile: deletes.append(ROOT / source["name"] / "mobile.json")
        pairs.append({"original": source["name"], "phone": clone["name"], "title": original.title(source)})
    filter_ids = {v["name"] for v in filters}
    body = {vid: state for vid, state in mobile.items() if vid not in filter_ids and vid != SEARCH
            and not original.alt(values[vid]).startswith("Mobile:")}
    first = min(state["position"]["y"] for state in body.values())
    delta = first - (top + 39 + 9)
    for vid, state in body.items():
        phone = deepcopy(state)
        phone["position"]["y"] = round(phone["position"]["y"] - delta, 2)
        additions[ROOT / vid / "mobile.json"] = phone
    for opened in (False, True):
        b = bookmark(opened)
        additions[original.REPORT / "bookmarks" / (b["name"] + ".bookmark.json")] = b
    # Close this panel when opening the navigation drawer; keep all selections.
    path = original.REPORT / "bookmarks" / (NAV_OPEN + ".bookmark.json")
    nav = original.read(path)
    section = nav["explorationState"]["sections"][PID]
    section.setdefault("visualContainerGroups", {})[IDS["group"]] = {"isHidden": True}
    section["visualContainers"][IDS["close"]] = {"singleVisual": {"visualType": "actionButton", "objects": {}, "display": {"mode": "hidden"}}}
    nav["options"]["targetVisualNames"] += [IDS["group"], IDS["close"]]
    additions[path] = nav
    index_path = original.REPORT / "bookmarks/bookmarks.json"
    index = original.read(index_path)
    next(item for item in index["items"] if item.get("displayName") == "Mobile navigation")["children"] += [IDS["open-bookmark"], IDS["close-bookmark"]]
    additions[index_path] = index
    delivery = {"date": "2026-10-14", "page": PID, "group": IDS["group"], "person_search": SEARCH,
        "filter_pairs": pairs, "source_mobile_placements_removed": [str(p.relative_to(original.PROJECT)) for p in deletes],
        "body_shift_up": delta, "panel_top": panel_top, "panel_height": height, "backup": str(BACKUP),
        "native_render_verified": False}
    return additions, deletes, delivery


def verify(delivery, additions=None, deletes=()):
    additions = additions or {}
    def read(path): return additions[path] if path in additions else original.read(path)
    all_sources = {p.parent.name: read(p) for p in ROOT.glob("*/visual.json")}
    all_sources.update({p.parent.name: value for p, value in additions.items() if p.name == "visual.json" and p.parent.parent == ROOT})
    all_mobile = {p.parent.name: read(p) for p in ROOT.glob("*/mobile.json") if p not in deletes}
    all_mobile.update({p.parent.name: value for p, value in additions.items() if p.name == "mobile.json" and p.parent.parent == ROOT})
    assert read(ROOT / IDS["group"] / "visual.json")["isHidden"] is True
    assert SEARCH in all_mobile and not all_sources[SEARCH].get("parentGroupName")
    assert {p["original"] for p in delivery["filter_pairs"]} == {v["name"] for v in candidates(all_sources) if v["name"] not in {p["phone"] for p in delivery["filter_pairs"]}}
    for pair in delivery["filter_pairs"]:
        original_visual, clone = all_sources[pair["original"]], all_sources[pair["phone"]]
        assert clone["parentGroupName"] == IDS["group"]
        assert clone["visual"]["syncGroup"] == original_visual["visual"]["syncGroup"]
        for key in ("query", "objects", "visualContainerObjects"):
            assert clone["visual"].get(key) == original_visual["visual"].get(key), (pair["title"], key)
        assert clone.get("filterConfig") == original_visual.get("filterConfig")
        assert pair["original"] not in all_mobile
    visible = [vid for vid in all_mobile if compact.relevant(all_sources[vid]) and not compact.hidden(vid, all_sources)]
    clashes = [(a,b) for i,a in enumerate(visible) for b in visible[i+1:]
               if compact.overlap(all_mobile[a]["position"], all_mobile[b]["position"])]
    assert not clashes, clashes
    content = [IDS["heading"], IDS["close"]] + [p["phone"] for p in delivery["filter_pairs"]]
    for i,a in enumerate(content):
        rect = all_mobile[a]["position"]
        assert 0 <= rect["x"] and rect["x"] + rect["width"] <= 323
        assert delivery["panel_top"] <= rect["y"] and rect["y"] + rect["height"] <= delivery["panel_top"] + delivery["panel_height"]
        for b in content[i+1:]: assert not compact.overlap(rect, all_mobile[b]["position"]), (a,b)
    for opened in (False, True):
        b = read(original.REPORT / "bookmarks" / (IDS["open-bookmark" if opened else "close-bookmark"] + ".bookmark.json"))
        assert b["options"]["suppressData"] and b["options"]["suppressActiveSection"]
        assert b["explorationState"]["sections"][PID]["visualContainerGroups"][IDS["group"]]["isHidden"] is not opened
    return {"grouped_filters": len(delivery["filter_pairs"]), "person_search_outside": True,
        "default_overlaps": 0, "filter_panel_content_overlaps": 0, "display_only_open_close": True,
        "paired_sync_configured": True, "native_render_and_selection_sync_verified": False}


def preserved(targets):
    roots = (original.REPORT, original.PROJECT / "SM_WMPP_v16.SemanticModel/definition",
             original.PROJECT / "SM_WMPP_v16.Report/StaticResources")
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for root in roots for p in root.rglob("*")
            if p.is_file() and p not in targets}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(original.read(MANIFEST))))
        return
    additions, deletes, delivery = make_plan()
    result = verify(delivery, additions, deletes)
    schema = home.published_schema_check(additions) if args.validate else {}
    print(json.dumps({"planned_updates_and_additions": len(additions), "phone_placements_to_remove": len(deletes), "checks": result, "schema": schema}), flush=True)
    if not args.apply_via: return
    assert not BACKUP.exists(), "Backup exists; inspect before repeating."
    targets = set(additions) | set(deletes)
    baseline = preserved(targets)
    before = {p: p.read_bytes() for p in targets if p.exists()}
    manifest = original.read(compact.MANIFEST)
    BACKUP.mkdir(parents=True)
    for path in list(before) + [compact.MANIFEST, compact.QA]:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert preserved(targets) == baseline
    for path, value in additions.items():
        if path in before: assert path.read_bytes() == before[path]
        path.parent.mkdir(parents=True, exist_ok=True)
        compact.patch_file(path, value, args.apply_via)
    for path in deletes:
        assert path.resolve().is_relative_to(ROOT.resolve()) and path.name == "mobile.json"
        assert path.read_bytes() == before[path]
        patch = "*** Begin Patch\n*** Delete File: mobile.json\n*** End Patch"
        done = subprocess.run([args.apply_via, "--codex-run-as-apply-patch", patch], cwd=path.parent,
                              capture_output=True, text=True)
        assert done.returncode == 0, done.stderr or done.stdout
    assert preserved(targets) == baseline, "Unrelated report/model/resources changed."
    compact.patch_file(MANIFEST, {**delivery, "checks": verify(delivery), "schema": schema}, args.apply_via)
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-14",
        "reason": "Phone-only Referral Explorer filter panel and paired slicer sync; Desktop appearance preserved.",
        "files": [str(p.relative_to(original.PROJECT)) for p in additions if p.name != "mobile.json"]})
    home.reconcile_inventory(manifest)
    page = next(p for p in manifest["pages"] if p["id"] == PID)
    page["after_height"] = max(original.read(ROOT/vid/"mobile.json")["position"]["y"] + original.read(ROOT/vid/"mobile.json")["position"]["height"]
                                for vid in page["mobile_ids"])
    compact.patch_file(compact.MANIFEST, manifest, args.apply_via)
    compact.patch_file(compact.QA, {"scope": "Referral Explorer mobile filters", "checks": verify(delivery),
        "unrelated_report_model_and_assets_preserved": True, "phone_render_verified": False}, args.apply_via)
    print(json.dumps({"saved": verify(delivery), "unrelated_report_model_and_assets_preserved": True, "backup": str(BACKUP)}), flush=True)


if __name__ == "__main__": main()
