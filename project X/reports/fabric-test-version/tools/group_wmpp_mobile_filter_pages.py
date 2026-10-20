"""Reuse the proven phone Filters panel on three additional WMPP pages.

Preview by default. Originals remain on Desktop; only their paired-sync metadata
changes. Native rendering/sync are separate acceptance checks, not schema checks.
"""

import argparse
from copy import deepcopy
import json
import shutil
import subprocess

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import group_wmpp_referral_mobile_filters as referral
import plan_wmpp_mobile_layout as original

CONFIGS = (
    {"page": "1cd52e9c7e4016f342ce", "name": "Offer Locations",
     "searches": ["42512af8cae3f7da924f"], "leading": ["7b4a905dbf7ce68d96a1"],
     "filters": ["0da8828163bf73fd7e40", "dc1856a2578c62cbebd7",
                 "796b6b9c07fad0271ac5", "83ca4687dfc72547bf8c"]},
    {"page": "08ef33dc6a87d1b14392", "name": "Provider Explorer",
     "searches": ["6d0540aac7a79d8d171a"], "leading": [],
     "filters": ["6d0aebfc69f445ce7a03", "1fcc6ba3dff4a32e114e", "5e0b94bb2b350b9ac4b5"]},
    {"page": "1fd2b1f8c98559e99f4d", "name": "Provider Registry Extract",
     "searches": ["8d24832540825ad2bcba", "623e69bcd0767c3c6d77"], "leading": [],
     "filters": ["34a585d144a75095be13", "a3906ac266b432f82462", "60870041c5155963bd65"]},
)
BACKUP = original.ROOT / "reports/_review/mobile-filter-panels-three-pages-before-20261014"
MANIFEST = original.PROJECT / "MOBILE_FILTER_PANELS_DELIVERY.json"


def extend_interactions(interactions, mapping):
    """Copy explicit source and target rules, including rules between two slicers."""
    result = deepcopy(interactions)
    seen = {json.dumps(rule, sort_keys=True) for rule in result}
    for rule in interactions:
        for source in (rule["source"], mapping.get(rule["source"])):
            for target in (rule["target"], mapping.get(rule["target"])):
                if source is None or target is None:
                    continue
                copy = {**deepcopy(rule), "source": source, "target": target}
                signature = json.dumps(copy, sort_keys=True)
                if signature not in seen:
                    result.append(copy)
                    seen.add(signature)
    return result


def search_positions(mobile, searches, leading):
    """Keep search sizes/settings, stacking the primary searches above Filters."""
    y = (max(mobile[v]["position"]["y"] + mobile[v]["position"]["height"] for v in leading) + 8
         if leading else min(mobile[v]["position"]["y"] for v in searches))
    result = {}
    for vid in searches:
        result[vid] = deepcopy(mobile[vid])
        result[vid]["position"]["y"] = round(y, 2)
        y += result[vid]["position"]["height"] + 8
    return result, round(y, 2)


def make_plan(config):
    pid, name = config["page"], config["name"]
    root = original.REPORT / "pages" / pid / "visuals"
    ids = referral.panel_ids(pid)
    assert not (root / ids["group"] / "visual.json").exists(), "Already grouped; use --verify."
    page_path = root.parent / "page.json"
    page = original.read(page_path)
    assert page["displayName"] == name
    values = {p.parent.name: original.read(p) for p in root.glob("*/visual.json")}
    mobile = {p.parent.name: original.read(p) for p in root.glob("*/mobile.json")}
    assert {v["name"] for v in referral.candidates(values)} == set(config["filters"])
    additions, deletes, pairs = {}, [], []
    searches, top = search_positions(mobile, config["searches"], config["leading"])
    for vid, state in searches.items():
        if state != mobile[vid]: additions[root / vid / "mobile.json"] = state
    excluded = set(config["filters"] + config["searches"] + config["leading"])
    body = {vid: state for vid, state in mobile.items() if vid not in excluded
            and not original.alt(values[vid]).startswith("Mobile:")}
    base = max(state["position"]["z"] for state in body.values()) + 10
    chrome_z = min(state["position"]["z"] for vid, state in mobile.items()
                   if original.alt(values[vid]).startswith("Mobile:"))
    assert base + 50 < chrome_z, "Filters must remain below navigation."
    park_x = page["width"] + 80
    panel_top, height = round(top + 47, 2), 56 + len(config["filters"]) * 90
    group = original.read(referral.REF_ROOT / "1c58e933994fd21e7496/visual.json")
    group["name"] = ids["group"]
    group["position"] = original.position(park_x, 20, 323, height, base, 99000)
    group["visualGroup"]["displayName"] = name + " | Mobile Filters drawer"
    group["isHidden"] = True
    additions[root / ids["group"] / "visual.json"] = group
    # No group mobile.json: this follows the working Desktop-normalized template.
    for role, template in (("background", "ef5d33a4ad5ff21c1029"), ("heading", "03e8287a57b1a615f63d")):
        source = original.read(referral.REF_ROOT / template / "visual.json")
        phone = original.read(referral.REF_ROOT / template / "mobile.json")
        source["name"], source["parentGroupName"] = ids[role], ids["group"]
        source["position"] = original.position(0 if role == "background" else 10,
            0 if role == "background" else 8, 323 if role == "background" else 210,
            height if role == "background" else 30, 0 if role == "background" else 1)
        phone["position"] = original.position(source["position"]["x"], panel_top + source["position"]["y"],
            source["position"]["width"], source["position"]["height"], base if role == "background" else base + 1)
        additions[root / ids[role] / "visual.json"] = source
        additions[root / ids[role] / "mobile.json"] = phone
    for role, template in (("open", "8ea73a405f7ef268214c"), ("close", "8fde89f83526ca1ffa03")):
        source = original.read(referral.REF_ROOT / template / "visual.json")
        phone = original.read(referral.REF_ROOT / template / "mobile.json")
        source["name"] = ids[role]
        source["position"] = original.position(park_x, 20, 323, 48, base + 40, 99010)
        source.pop("parentGroupName", None)
        if role == "close": source["isHidden"] = True
        else: source.pop("isHidden", None)
        compact.set_props(source["visual"]["visualContainerObjects"], "visualLink", {
            "bookmark": original.literal(original.quote(ids[role + "-bookmark"]))})
        compact.set_props(source["visual"]["visualContainerObjects"], "general", {
            "altText": original.literal(original.quote("Mobile: " + name + " " + role + " filters"))})
        phone["position"] = original.position(0 if role == "open" else 235,
            top if role == "open" else panel_top + 6, 323 if role == "open" else 76,
            39 if role == "open" else 36, base + 50 if role == "open" else base + 40,
            160 if role == "open" else 170)
        phone["objects"]["text"] = compact.complete_button_text(source["visual"]["objects"]["text"], phone["objects"]["text"])
        additions[root / ids[role] / "visual.json"] = source
        additions[root / ids[role] / "mobile.json"] = phone
    for index, vid in enumerate(config["filters"]):
        origin, clone = referral.paired_slicer(values[vid], index, pid)
        stripped = deepcopy(origin)
        stripped["visual"].pop("syncGroup")
        assert stripped == values[vid], "Original may only gain sync metadata."
        phone = deepcopy(mobile[vid])
        phone["position"] = original.position(10, panel_top + 44 + index * 90, 303, 80, base + 2 + index, 180 + index)
        additions[root / vid / "visual.json"] = origin
        additions[root / clone["name"] / "visual.json"] = clone
        additions[root / clone["name"] / "mobile.json"] = phone
        deletes.append(root / vid / "mobile.json")
        pairs.append({"original": vid, "phone": clone["name"], "title": original.title(values[vid])})
    delta = round(min(state["position"]["y"] for state in body.values()) - (top + 48), 2)
    for vid, state in body.items():
        phone = deepcopy(state)
        phone["position"]["y"] = round(phone["position"]["y"] - delta, 2)
        additions[root / vid / "mobile.json"] = phone
    mapping = {p["original"]: p["phone"] for p in pairs}
    old_interactions = deepcopy(page.get("visualInteractions", []))
    page["visualInteractions"] = extend_interactions(old_interactions, mapping)
    additions[page_path] = page
    for opened in (False, True):
        b = referral.bookmark(opened, pid, name)
        additions[original.REPORT / "bookmarks" / (b["name"] + ".bookmark.json")] = b
    nav_path = next(p for p in (original.REPORT / "bookmarks").glob("*.bookmark.json")
                    if original.read(p).get("displayName") == "Mobile | " + name + " | open")
    nav = original.read(nav_path)
    assert nav["options"]["suppressData"] and nav["options"]["suppressActiveSection"]
    section = nav["explorationState"]["sections"][pid]
    section.setdefault("visualContainerGroups", {})[ids["group"]] = {"isHidden": True}
    section["visualContainers"][ids["close"]] = {"singleVisual": {
        "visualType": "actionButton", "objects": {}, "display": {"mode": "hidden"}}}
    nav["options"]["targetVisualNames"] += [ids["group"], ids["close"]]
    additions[nav_path] = nav
    return additions, deletes, {**config, "ids": ids, "nav_open": nav["name"],
        "filter_pairs": pairs, "panel_top": panel_top, "panel_height": height, "layer_base": base,
        "navigation_layer_min": chrome_z, "body_shift_up": delta, "body_count": len(body),
        "original_interactions": old_interactions,
        "interaction_rules_added": len(page["visualInteractions"]) - len(old_interactions),
        "source_mobile_placements_removed": [str(p.relative_to(original.PROJECT)) for p in deletes]}


def verify(delivery, additions=None, deletes=()):
    additions = additions or {}
    pid, ids = delivery["page"], delivery["ids"]
    root = original.REPORT / "pages" / pid / "visuals"
    def read(path): return additions[path] if path in additions else original.read(path)
    values = {p.parent.name: read(p) for p in root.glob("*/visual.json")}
    values.update({p.parent.name: v for p, v in additions.items() if p.name == "visual.json" and p.parent.parent == root})
    mobile = {p.parent.name: read(p) for p in root.glob("*/mobile.json") if p not in deletes}
    mobile.update({p.parent.name: v for p, v in additions.items() if p.name == "mobile.json" and p.parent.parent == root})
    assert values[ids["group"]]["isHidden"] is True
    assert values[ids["group"]]["position"]["x"] >= read(root.parent / "page.json")["width"]
    assert {v["name"] for v in referral.candidates(values)} == set(delivery["filters"])
    for vid in delivery["searches"] + delivery["leading"]:
        assert vid in mobile and not values[vid].get("parentGroupName")
    for pair in delivery["filter_pairs"]:
        origin, clone = values[pair["original"]], values[pair["phone"]]
        assert clone["parentGroupName"] == ids["group"]
        assert origin["visual"]["syncGroup"] == clone["visual"]["syncGroup"]
        for key in ("query", "objects", "visualContainerObjects"):
            assert origin["visual"].get(key) == clone["visual"].get(key), (pair["title"], key)
        assert origin.get("filterConfig") == clone.get("filterConfig")
        assert pair["original"] not in mobile
    visible = [vid for vid in mobile if compact.relevant(values[vid]) and not compact.hidden(vid, values)]
    clashes = [(a, b) for i, a in enumerate(visible) for b in visible[i + 1:]
               if compact.overlap(mobile[a]["position"], mobile[b]["position"])]
    assert not clashes, (delivery["name"], clashes)
    content = [ids["heading"], ids["close"]] + [p["phone"] for p in delivery["filter_pairs"]]
    for i, vid in enumerate(content):
        pos = mobile[vid]["position"]
        assert not compact.hidden(vid, values, {ids["group"]: False, ids["close"]: False})
        assert 0 <= pos["x"] and pos["x"] + pos["width"] <= 323
        assert delivery["panel_top"] <= pos["y"] and pos["y"] + pos["height"] <= delivery["panel_top"] + delivery["panel_height"]
        assert pos["z"] < delivery["navigation_layer_min"]
        for other in content[i + 1:]: assert not compact.overlap(pos, mobile[other]["position"])
    for opened in (False, True):
        b = read(original.REPORT / "bookmarks" / (ids["open-bookmark" if opened else "close-bookmark"] + ".bookmark.json"))
        assert b["options"]["suppressData"] and b["options"]["suppressActiveSection"]
        assert b["options"]["targetVisualNames"] == [ids["group"], ids["close"]]
        assert b["explorationState"]["sections"][pid]["visualContainerGroups"][ids["group"]]["isHidden"] is not opened
    mapping = {p["original"]: p["phone"] for p in delivery["filter_pairs"]}
    assert read(root.parent / "page.json")["visualInteractions"] == extend_interactions(delivery["original_interactions"], mapping)
    nav = read(original.REPORT / "bookmarks" / (delivery["nav_open"] + ".bookmark.json"))
    assert nav["options"]["suppressData"] and nav["options"]["suppressActiveSection"]
    assert nav["explorationState"]["sections"][pid]["visualContainerGroups"][ids["group"]]["isHidden"]
    index = read(original.REPORT / "bookmarks/bookmarks.json")
    children = next(v for v in index["items"] if v.get("displayName") == "Mobile navigation")["children"]
    assert children.count(ids["open-bookmark"]) == children.count(ids["close-bookmark"]) == 1
    return {"page": delivery["name"], "grouped_filters": len(mapping), "searches_outside": len(delivery["searches"]),
        "default_overlaps": 0, "panel_content_overlaps": 0, "display_only_bookmarks": True,
        "paired_query_selection_sync_configured": True, "explicit_interactions_preserved": True,
        "native_render_and_selection_sync_verified": False}


def batch_plan():
    additions, deletes, pages = {}, [], []
    for config in CONFIGS:
        updates, removed, delivery = make_plan(config)
        assert not (set(additions) & set(updates)), "Unexpected shared target."
        additions.update(updates)
        deletes.extend(removed)
        pages.append(delivery)
    index_path = original.REPORT / "bookmarks/bookmarks.json"
    index = original.read(index_path)
    children = next(v for v in index["items"] if v.get("displayName") == "Mobile navigation")["children"]
    for delivery in pages: children.extend(delivery["ids"][r] for r in ("open-bookmark", "close-bookmark"))
    assert len(children) == len(set(children))
    additions[index_path] = index
    return additions, deletes, pages


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps([verify(d) for d in original.read(MANIFEST)["pages"]]))
        return
    additions, deletes, pages = batch_plan()
    checks = [verify(d, additions, deletes) for d in pages]
    schema = home.published_schema_check(additions) if args.validate else {}
    print(json.dumps({"updates_and_additions": len(additions), "old_phone_placements": len(deletes),
                      "checks": checks, "schema": schema}), flush=True)
    if not args.apply_via: return
    assert not BACKUP.exists(), "Inspect existing backup before repeating."
    assert not MANIFEST.exists(), "Already delivered; use --verify."
    targets = set(additions) | set(deletes)
    baseline = referral.preserved(targets)
    before = {p: p.read_bytes() for p in targets if p.exists()}
    manifest = original.read(compact.MANIFEST)
    BACKUP.mkdir(parents=True)
    for path in list(before) + [compact.MANIFEST, compact.QA]:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert referral.preserved(targets) == baseline
    for path, value in additions.items():
        if path in before: assert path.read_bytes() == before[path], "Report changed during edit."
        path.parent.mkdir(parents=True, exist_ok=True)
        compact.patch_file(path, value, args.apply_via)
    for path in deletes:
        assert path.name == "mobile.json" and any(path.resolve().is_relative_to(
            (original.REPORT / "pages" / d["page"] / "visuals").resolve()) for d in pages)
        assert path.read_bytes() == before[path]
        assert (BACKUP / path.relative_to(original.PROJECT)).read_bytes() == before[path]
        patch = "*** Begin Patch\n*** Delete File: mobile.json\n*** End Patch"
        done = subprocess.run([args.apply_via, "--codex-run-as-apply-patch", patch], cwd=path.parent,
                              capture_output=True, text=True)
        assert done.returncode == 0, done.stderr or done.stdout
    assert referral.preserved(targets) == baseline, "Unrelated report/model/assets changed."
    # Existing definitions may differ only as described by the plan.
    for d in pages:
        root = original.REPORT / "pages" / d["page"] / "visuals"
        for pair in d["filter_pairs"]:
            path = root / pair["original"] / "visual.json"
            saved = original.read(path)
            saved["visual"].pop("syncGroup")
            assert saved == json.loads(before[path].decode("utf-8-sig"))
        for vid in d["searches"] + d["leading"]:
            assert root / vid / "visual.json" not in targets
    checks = [verify(d) for d in pages]
    compact.patch_file(MANIFEST, {"date": "2026-10-14", "pages": pages, "checks": checks,
        "schema": schema, "backup": str(BACKUP), "native_render_verified": False,
        "unrelated_report_model_and_assets_preserved": True}, args.apply_via)
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-14",
        "reason": "Mobile Filters panels for Offer Locations, Provider Explorer and Provider Registry Extract; Desktop geometry unchanged.",
        "files": [str(p.relative_to(original.PROJECT)) for p in additions if p.name != "mobile.json"]})
    home.reconcile_inventory(manifest)
    for d in pages:
        page = next(p for p in manifest["pages"] if p["id"] == d["page"])
        root = original.REPORT / "pages" / d["page"] / "visuals"
        page["after_height"] = max(original.read(root / vid / "mobile.json")["position"]["y"] +
                                   original.read(root / vid / "mobile.json")["position"]["height"] for vid in page["mobile_ids"])
    compact.patch_file(compact.MANIFEST, manifest, args.apply_via)
    compact.patch_file(compact.QA, {"scope": "Three additional mobile filter panels", "checks": checks,
        "unrelated_report_model_and_assets_preserved": True, "phone_render_verified": False}, args.apply_via)
    print(json.dumps({"saved": checks, "backup": str(BACKUP), "other_report_pages_model_assets_preserved": True}), flush=True)


if __name__ == "__main__": main()
