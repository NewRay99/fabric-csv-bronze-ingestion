"""Remove only custom navigation placements from the WIP phone layouts.

Keep native page headings, filters, links, business visuals and Desktop intact.
Off-canvas source definitions/bookmarks remain for recovery and compatibility;
without mobile placements they are not part of the phone canvas.
"""

import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
import shutil
import subprocess

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original

BACKUP = original.ROOT / "reports/_review/native-mobile-navigation-before-20261015"
DELIVERY = original.PROJECT / "MOBILE_NATIVE_NAVIGATION_DELIVERY.json"
QA = original.PROJECT / "MOBILE_NATIVE_NAVIGATION_QA.json"
NAV_KEYS = ("open", "scrim", "panel", "drawer-title", "close", "explorers-heading") + tuple(
    "go:" + target for _, target in original.DESTINATIONS)


def navigation_ids(page_id):
    return {original.ident(page_id + ":" + role): role for role in NAV_KEYS}


def widen_heading(state):
    result = deepcopy(state)
    assert result["position"]["x"] == 0
    result["position"]["width"] = original.WIDTH
    return result


def clashes(sources, mobile):
    visible = [vid for vid in mobile if compact.relevant(sources[vid]) and not compact.hidden(vid, sources)]
    return sorted([a, b] for i, a in enumerate(sorted(visible)) for b in sorted(visible)[i+1:]
                  if compact.overlap(mobile[a]["position"], mobile[b]["position"]))


def protected_files(targets):
    roots = (original.REPORT, original.PROJECT / "SM_WMPP_v16.SemanticModel/definition",
             original.PROJECT / "SM_WMPP_v16.Report/StaticResources")
    return {str(path.relative_to(original.PROJECT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for root in roots for path in root.rglob("*") if path.is_file() and path not in targets}


def plan():
    assert not DELIVERY.exists(), "Already delivered; use --verify."
    updates, removed, pages = {}, [], []
    initial = original.read(original.PROJECT / "MOBILE_LAYOUT_DELIVERY.json")
    assert len(initial["pages"]) == 31
    for page in initial["pages"]:
        pid = page["id"]
        root = original.REPORT / "pages" / pid / "visuals"
        sources = {p.parent.name: original.read(p) for p in root.glob("*/visual.json")}
        mobile = {p.parent.name: original.read(p) for p in root.glob("*/mobile.json")}
        ids = navigation_ids(pid)
        assert len(ids) == 18 and set(ids) <= set(mobile), (page["name"], "Inspect navigation inventory.")
        for vid in ids:
            assert original.alt(sources[vid]).startswith("Mobile:")
            assert sources[vid]["position"]["x"] >= original.read(root.parent / "page.json")["width"]
            removed.append(root / vid / "mobile.json")
        heading = original.ident(pid + ":header")
        assert heading in mobile and original.vtype(sources[heading]) == "textbox"
        updates[root / heading / "mobile.json"] = widen_heading(mobile[heading])
        pages.append({"id": pid, "name": page["name"], "navigation": ids, "header": heading,
                      "default_overlaps_before": clashes(sources, mobile)})
    return updates, removed, pages


def verify(pages, updates=None, removed=()):
    updates = updates or {}
    removed = set(removed)
    checks, warnings = [], []
    for page in pages:
        pid = page["id"]
        root = original.REPORT / "pages" / pid / "visuals"
        sources = {p.parent.name: original.read(p) for p in root.glob("*/visual.json")}
        mobile = {p.parent.name: updates.get(p, original.read(p)) for p in root.glob("*/mobile.json") if p not in removed}
        assert not (set(page["navigation"]) & set(mobile)), page["name"]
        # The source definitions are deliberately retained, off Desktop's canvas.
        assert set(page["navigation"]) <= set(sources)
        after = clashes(sources, mobile)
        assert not (set(map(tuple, after)) - set(map(tuple, page["default_overlaps_before"]))), (
            page["name"], "New overlap introduced.")
        heading = mobile[page["header"]]
        assert heading["position"]["width"] == original.WIDTH
        if not updates:
            old_heading = original.read(BACKUP / (root / page["header"] / "mobile.json").relative_to(original.PROJECT))
            assert heading == widen_heading(old_heading), "Heading changed beyond width."
        checks.append({"page": page["name"], "custom_navigation_placements": 0,
                       "title_width": original.WIDTH, "new_default_overlaps": 0})
        if after: warnings.append({"page": page["name"], "pre_existing_overlaps_unchanged": after})
    return {"pages": len(pages), "custom_menu_and_drawer_removed": True, "page_titles_kept": True,
        "title_width": original.WIDTH, "new_default_overlaps": 0,
        "unchanged_existing_overlap_warnings": warnings, "page_checks": checks,
        "native_mobile_app_render_verified": False}


def finish_metadata(executable, pages):
    """Finish provenance separately; never repeat removals after unknown outcomes."""
    baseline = protected_files(set())
    manifest = original.read(BACKUP / compact.MANIFEST.relative_to(original.PROJECT))
    previous_reconciliations = len(manifest.get("inventory_reconciliations", []))
    home.reconcile_inventory(manifest)
    if len(manifest.get("inventory_reconciliations", [])) > previous_reconciliations:
        manifest["inventory_reconciliations"][-1].update({"date": "2026-10-15",
            "reason": "Remove custom phone navigation placements; retain the current non-navigation phone inventory."})
    for page in manifest["pages"]:
        root = original.REPORT / "pages" / page["id"] / "visuals"
        page["after_height"] = max(original.read(root / vid / "mobile.json")["position"]["y"] +
                                   original.read(root / vid / "mobile.json")["position"]["height"]
                                   for vid in page["mobile_ids"])
    manifest["custom_mobile_navigation"] = {"enabled": False, "date": "2026-10-15",
        "reason": "Use Power BI mobile app native page navigation; keep filter panels and existing content actions."}
    # Existing saved-source changes can precede this phone-only operation.
    # Reconcile provenance to that preserved current source, never overwrite the
    # user's definitions to make an older historical fingerprint match.
    current_definitions = compact.protected()
    if manifest["protected"] != current_definitions:
        manifest.setdefault("saved_definition_baseline_reconciliations", []).append({"date": "2026-10-15",
            "previous": manifest["protected"], "current": current_definitions,
            "reason": "Adopt the current saved definitions preserved byte-for-byte during navigation removal; no source/model/bookmark edits."})
        manifest["protected"] = current_definitions
    compact.BACKUP = BACKUP
    compact.patch_file(compact.MANIFEST, manifest, executable)
    compact.patch_file(QA, {"scope": "Custom mobile navigation removal only", "checks": verify(pages),
        "desktop_model_bookmarks_and_all_non_navigation_phone_objects_preserved": True,
        "native_app_render_verified": False}, executable)
    assert protected_files(set()) == baseline, "Provenance updates altered report/model/resources."


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--finish-metadata-via")
    args = parser.parse_args()
    if args.verify or args.finish_metadata_via:
        delivery = original.read(DELIVERY)
        assert original.digest_mapping(protected_files(set())) == delivery["saved_report_model_assets_fingerprint"]
        if args.finish_metadata_via:
            finish_metadata(args.finish_metadata_via, delivery["pages"])
        checks = verify(delivery["pages"])
        print(json.dumps({"pages": checks["pages"], "custom_menu_and_drawer_removed": True,
            "new_default_overlaps": checks["new_default_overlaps"],
            "pre_existing_warning_pages": len(checks["unchanged_existing_overlap_warnings"]),
            "native_mobile_app_render_verified": False}))
        return
    updates, removed, pages = plan()
    checks = verify(pages, updates, removed)
    schema = home.published_schema_check(updates) if args.validate else {}
    print(json.dumps({"phone_navigation_placements_to_remove": len(removed), "headings_to_widen": len(updates),
        "pages": checks["pages"], "new_overlaps": checks["new_default_overlaps"],
        "pre_existing_warning_pages": len(checks["unchanged_existing_overlap_warnings"]), "schema": schema}), flush=True)
    if not args.apply_via: return
    assert not BACKUP.exists(), "Inspect existing recovery copy before repeating."
    targets = set(updates) | set(removed)
    baseline = protected_files(targets)
    before = {path: path.read_bytes() for path in targets}
    protected_before = compact.protected()
    BACKUP.mkdir(parents=True)
    for path in list(before) + [compact.MANIFEST]:
        recovery = BACKUP / path.relative_to(original.PROJECT)
        recovery.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, recovery)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert protected_files(targets) == baseline
    for path, value in updates.items():
        assert path.read_bytes() == before[path]
        compact.patch_file(path, value, args.apply_via)
    batches = defaultdict(list)
    for path in removed:
        assert path.name == "mobile.json"
        assert path.parent.parent.name == "visuals"
        assert path.resolve().is_relative_to(original.REPORT.resolve())
        assert path.parent.name in navigation_ids(path.parents[2].name)
        assert path.read_bytes() == before[path]
        assert (BACKUP / path.relative_to(original.PROJECT)).read_bytes() == before[path]
        batches[path.parent.parent].append(path)
    # Each batch names only the 18 verified phone placements on one exact page.
    # No directory deletions, wildcard targets or source-definition removal.
    for root, paths in batches.items():
        assert all(path.read_bytes() == before[path] for path in paths)
        patch = "*** Begin Patch\n" + "".join("*** Delete File: " + path.relative_to(root).as_posix() + "\n"
                                               for path in paths) + "*** End Patch"
        result = subprocess.run([args.apply_via, "--codex-run-as-apply-patch", patch], cwd=root,
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr or result.stdout
        assert all(not path.exists() for path in paths)
    assert protected_files(targets) == baseline, "A non-target visual, filter, model, bookmark or asset changed."
    assert compact.protected() == protected_before, "Desktop/model/bookmark definitions changed."
    checks = verify(pages)
    compact.patch_file(DELIVERY, {"date": "2026-10-15", "pages": pages, "checks": checks, "schema": schema,
        "removed_phone_navigation_placements": len(removed), "backup": str(BACKUP),
        "desktop_model_bookmark_definitions_and_assets_preserved": True,
        "all_other_mobile_filters_buttons_and_data_visuals_preserved": True,
        "off_canvas_source_definitions_retained": True,
        "saved_report_model_assets_fingerprint": original.digest_mapping(protected_files(set()))}, args.apply_via)
    finish_metadata(args.apply_via, pages)
    print(json.dumps({"saved_pages": checks["pages"], "removed_phone_navigation_placements": len(removed),
        "desktop_model_filters_content_and_existing_actions_preserved": True,
        "new_overlaps": 0, "backup": str(BACKUP), "native_app_render_verified": False}), flush=True)


if __name__ == "__main__": main()
