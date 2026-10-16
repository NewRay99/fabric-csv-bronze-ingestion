"""Add the homepage Provider Explorer shortcut without changing the model.

Preview by default; saved edits and metadata updates use apply_patch.
"""

import argparse
from copy import deepcopy
import hashlib
import json
import shutil

import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original

PAGE = compact.HOME_PAGE
NEW_ID = compact.HOME_PROVIDER_SHORTCUT
REF_ID = "a214f7d8c8a55d927cd1"
DESC_ID = "e28633552744aa54558a"
SIDEBAR_ID = "ed614ceffe457e1d1571"
FOOTERS = ("42dbc746800031d00ea0", "c66a58c9a2a2d0a9a04d")
BOOKMARK = "5d2360e07f9eb62f82a7"
DESTINATION = "08ef33dc6a87d1b14392"
ROOT = original.REPORT / "pages" / PAGE / "visuals"
BACKUP = original.ROOT / "reports/_review/home-provider-shortcut-before-20261014"


def button(source_template, ref_source, ref_phone, description):
    source = deepcopy(source_template)
    source["name"] = NEW_ID
    source.pop("isHidden", None)
    source.pop("parentGroupName", None)
    pos = ref_source["position"]
    source["position"] = original.position(pos["x"] + pos["width"] / 2 - 116,
        description["position"]["y"] + 72 + 12, 232, 48, 94000, 90010)
    compact.set_props(source["visual"]["visualContainerObjects"], "general", {
        "altText": original.literal("'Homepage shortcut: Provider Explorer'")})
    phone = deepcopy(ref_phone)
    phone["position"] = original.position(0, 0, 323, 52, 180, 180)
    for entry in phone.setdefault("objects", {}).get("text", []):
        entry["properties"]["text"] = original.literal("'Provider Explorer'")
    compact.phone_home_button_format(source, phone)
    return source, phone


def plans():
    assert not (ROOT / NEW_ID / "visual.json").exists(), "Already added; use --verify."
    ref = original.read(ROOT / REF_ID / "visual.json")
    ref_phone = original.read(ROOT / REF_ID / "mobile.json")
    description = original.read(ROOT / DESC_ID / "visual.json")
    desc_phone = original.read(ROOT / DESC_ID / "mobile.json")
    template = original.read(ROOT / SIDEBAR_ID / "visual.json")
    source, phone = button(template, ref, ref_phone, description)
    phone["position"]["y"] = desc_phone["position"]["y"] + desc_phone["position"]["height"] + 8
    changes = {ROOT / NEW_ID / "visual.json": source, ROOT / NEW_ID / "mobile.json": phone}
    shortened = deepcopy(description)
    shortened["position"]["height"] = 72  # Existing 18px paragraph retains room for three lines.
    changes[ROOT / DESC_ID / "visual.json"] = shortened
    for vid in FOOTERS:
        path = ROOT / vid / "mobile.json"
        state = original.read(path)
        state["position"]["y"] += 60
        state["position"]["z"] += 10
        state["position"]["tabOrder"] += 10
        changes[path] = state
    return changes


def preserved(changes):
    roots = (original.REPORT, original.PROJECT / "SM_WMPP_v16.SemanticModel/definition",
             original.PROJECT / "SM_WMPP_v16.Report/StaticResources")
    return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
            for root in roots for p in root.rglob("*") if p.is_file() and p not in changes}


def published_schema_check(changes):
    # Desktop has saved newer schema references whose public URLs return 404.
    # Preserve those references in the actual report; validate copies against
    # Microsoft's published compatible contracts, without claiming exact-version
    # or native-render verification.
    aliases = {"visualContainer/2.13.0/": "visualContainer/2.7.0/",
               "visualContainerMobileState/2.8.0/": "visualContainerMobileState/2.4.0/"}
    documents = []
    used = {}
    for path, value in changes.items():
        copy = deepcopy(value)
        for new, published in aliases.items():
            if new in copy["$schema"]:
                used[new] = published
                copy["$schema"] = copy["$schema"].replace(new, published)
        documents.append((str(path), copy))
    return {**original.validate_documents(documents), "compatible_contracts": used,
            "saved_schema_references_preserved": True}


def reconcile_inventory(manifest):
    """Record the current saved inventory, without restoring user-removed phone visuals."""
    adjustments = []
    for page in manifest["pages"]:
        actual = {p.parent.name for p in (original.REPORT / "pages" / page["id"] / "visuals").glob("*/mobile.json")}
        expected = set(page["mobile_ids"])
        if expected != actual:
            adjustments.append({"page": page["name"], "missing_from_saved_report": sorted(expected - actual),
                                "present_in_saved_report": sorted(actual - expected)})
            page["mobile_ids"] = sorted(actual)
    if adjustments:
        manifest.setdefault("inventory_reconciliations", []).append({"date": "2026-10-14",
            "reason": "Use the current Desktop-saved inventory; do not restore earlier removed mobile objects.",
            "pages": adjustments})


def delivery_checks(manifest):
    try:
        return compact.check_saved(manifest)
    except AssertionError as error:
        detail = error.args[0] if error.args else None
        # Report an unchanged other-page warning; never conceal a homepage,
        # preservation, or unidentifiable validation failure.
        assert isinstance(detail, tuple) and detail[0] not in {PAGE, "WMPP Homepage"}, error
        sources = {p.parent.name: original.read(p) for p in ROOT.glob("*/visual.json")}
        mobile = {p.parent.name: original.read(p) for p in ROOT.glob("*/mobile.json")}
        states = compact.check_bookmark_table_tiles(sources, mobile,
            [original.read(p) for p in (original.REPORT / "bookmarks").glob("*.bookmark.json")], PAGE)
        return {"scope": "Homepage Provider Explorer shortcut", "homepage": check(),
            "mobile_visuals": len(list(original.REPORT.rglob("mobile.json"))),
            "definitions_match_authorised_baseline": compact.protected() == manifest["protected"],
            "semantic_model_preserved": True, "global_mobile_layout_check_passed": False,
            "unchanged_other_page_validation_warning": repr(detail),
            "bookmark_page_states_checked": states, "phone_render_verified": False}


def check(values=None):
    values = values or {}
    def read(path):
        return values[path] if path in values else original.read(path)
    source, phone = read(ROOT / NEW_ID / "visual.json"), read(ROOT / NEW_ID / "mobile.json")
    assert original.label(source) == "Provider Explorer" and not source.get("isHidden")
    assert original.prop(source, "visualContainerObjects", "visualLink", "bookmark") == BOOKMARK
    bookmark = original.read(original.REPORT / "bookmarks" / (BOOKMARK + ".bookmark.json"))
    assert bookmark["explorationState"]["activeSection"] == DESTINATION
    assert bookmark["options"].get("suppressData") is True
    description = read(ROOT / DESC_ID / "visual.json")
    if (original.PROJECT / "HOMEPAGE_DESKTOP_SHORTCUTS_DELIVERY.json").exists():
        # The approved desktop revision places all four shortcuts in one row;
        # the phone shortcut deliberately remains below the referral paragraph.
        reference = read(ROOT / REF_ID / "visual.json")
        assert source["position"]["y"] == reference["position"]["y"]
        assert source["position"]["x"] > reference["position"]["x"]
        for dimension in ("width", "height"):
            assert source["position"][dimension] == reference["position"][dimension]
    else:
        assert source["position"]["y"] >= description["position"]["y"] + description["position"]["height"] + 12
    desc_phone = read(ROOT / DESC_ID / "mobile.json")
    assert phone["position"]["y"] >= desc_phone["position"]["y"] + desc_phone["position"]["height"] + 8
    assert not compact.button_icon_text_collisions(source, phone)
    assert not compact.home_badge_errors(source, phone)
    sources = {p.parent.name: read(p) for p in ROOT.glob("*/visual.json")}
    sources[NEW_ID] = source
    for vid, other in sources.items():
        if vid == NEW_ID or compact.hidden(vid, sources) or not compact.relevant(other):
            continue
        if other["position"]["x"] < 1960:
            assert not compact.overlap(source["position"], other["position"]), ("Desktop overlap", vid)
        path = ROOT / vid / "mobile.json"
        if path.exists():
            assert not compact.overlap(phone["position"], read(path)["position"]), ("Phone overlap", vid)
    compact.validate_home_badge_assets()
    return {"label": "Provider Explorer", "destination": "Provider Explorer",
            "desktop_and_mobile": True, "button_overlaps": 0, "icon_title_collisions": 0,
            "native_render_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--finish-metadata-via")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(check()))
        return
    if args.finish_metadata_via:
        assert BACKUP.exists(), "Missing pre-change backup."
        check()
        baseline = preserved({})
        manifest = original.read(compact.MANIFEST)
        assert manifest["protected"] == compact.protected(), "Definition baseline changed since application."
        reconcile_inventory(manifest)
        result = delivery_checks(manifest)
        compact.BACKUP = BACKUP
        compact.patch_file(compact.MANIFEST, manifest, args.finish_metadata_via)
        compact.patch_file(compact.QA, result, args.finish_metadata_via)
        assert preserved({}) == baseline, "Metadata finishing changed report/model content."
        print(json.dumps({"saved": check(), "mobile_visuals": result["mobile_visuals"],
            "bookmark_states_checked": result["bookmark_page_states_checked"],
            "report_model_and_assets_unchanged_by_metadata_finish": True}), flush=True)
        return
    changes = plans()
    checks = check(changes)
    schemas = published_schema_check(changes) if args.validate else {}
    print(json.dumps({"planned_files": len(changes), "checks": checks, "schemas": schemas}), flush=True)
    if not args.apply_via:
        return
    assert not BACKUP.exists(), "Backup exists; inspect before repeating."
    existing = {p: p.read_bytes() for p in changes if p.exists()}
    baseline = preserved(changes)
    protected_before = compact.protected()
    manifest = original.read(compact.MANIFEST)
    BACKUP.mkdir(parents=True)
    for path in list(existing) + [compact.MANIFEST, compact.QA]:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert preserved(changes) == baseline, "Unrelated report/model files changed before application."
    for path, value in changes.items():
        if path in existing:
            assert path.read_bytes() == existing[path], "A target changed before application."
        path.parent.mkdir(parents=True, exist_ok=True)
        compact.patch_file(path, value, args.apply_via)
    assert preserved(changes) == baseline, "Unrelated report/model/resources changed."
    manifest["protected_before_home_provider_shortcut"] = protected_before
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-14",
        "reason": "Homepage Provider Explorer shortcut; fit below the unchanged referral paragraph.",
        "files": [str(p.relative_to(original.PROJECT)) for p in changes if p.name == "visual.json"]})
    page = next(p for p in manifest["pages"] if p["id"] == PAGE)
    page["mobile_ids"] = sorted(page["mobile_ids"] + [NEW_ID])
    page["after_height"] += 60
    reconcile_inventory(manifest)
    compact.patch_file(compact.MANIFEST, manifest, args.apply_via)
    result = delivery_checks(manifest)
    compact.patch_file(compact.QA, result, args.apply_via)
    print(json.dumps({"saved": check(), "other_report_model_and_assets_preserved": True,
        "mobile_visuals": result["mobile_visuals"], "bookmark_states_checked": result["bookmark_page_states_checked"],
        "backup": str(BACKUP)}), flush=True)


if __name__ == "__main__":
    main()
