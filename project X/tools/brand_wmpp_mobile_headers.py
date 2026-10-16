"""Reuse the user's saved BCT logo/title header on every existing phone page.

Only header phone states and missing, off-Desktop-canvas image sources change.
The saved Target & Urgency example, other phone content and cache are immutable.
"""

import argparse
from copy import deepcopy
import hashlib
import json
import shutil

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original
import use_wmpp_native_mobile_navigation as native

PAGE = "6ae319c8916a5d63a4ff"
LOGO = "2588cb7adc78557320a6"
BACKUP = original.ROOT / "reports/_review/mobile-logo-headers-before-20261015"
DELIVERY = original.PROJECT / "MOBILE_LOGO_HEADERS_DELIVERY.json"


def resource(source):
    return next((e.get("properties", {}).get("sourceFile", {}).get("image", {})
                 .get("url", {}).get("expr", {}).get("ResourcePackageItem", {}).get("ItemName")
                 for e in source.get("visual", {}).get("objects", {}).get("image", [])
                 if e.get("properties", {}).get("sourceFile")), None)


def title_runs(state):
    return [run for entry in state.get("objects", {}).get("general", [])
            for para in entry.get("properties", {}).get("paragraphs", [])
            for run in para.get("textRuns", [])]


def branded_title(state, template):
    result = deepcopy(state)
    for key in ("x", "y", "height", "width"):
        result["position"][key] = template["position"][key]
    runs = title_runs(result)
    assert runs, "Inspect a header without text runs."
    for run in runs:
        run.setdefault("textStyle", {})["fontSize"] = "9pt"
    return result


def project_hashes(excluded=()):
    excluded = {original.PROJECT / p if isinstance(p, str) else p for p in excluded} | {DELIVERY}
    return {str(p.relative_to(original.PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in original.PROJECT.rglob("*") if p.is_file() and p not in excluded}


def cache_state():
    return {str(p.relative_to(original.PROJECT)): (p.stat().st_size,
            p.stat().st_mtime_ns, hashlib.sha256(p.read_bytes()).hexdigest())
            for p in original.PROJECT.rglob("*") if p.is_file() and p.suffix.lower() in {".abf", ".adb"}}


def plan(use_recovery=False):
    def read(path):
        recovery = BACKUP / path.relative_to(original.PROJECT)
        return original.read(recovery if use_recovery and recovery.exists() else path)

    template_root = original.REPORT / "pages" / PAGE / "visuals"
    template_logo = read(template_root / LOGO / "visual.json")
    phone_logo = read(template_root / LOGO / "mobile.json")
    template_title = read(template_root / original.ident(PAGE + ":header") / "mobile.json")
    assert all(r["textStyle"]["fontSize"] == "9pt" for r in title_runs(template_title))
    assert phone_logo["position"] == {"x": 0, "y": 9, "z": 55001, "height": 25, "width": 111}
    asset = resource(template_logo)
    assert asset and (original.PROJECT / "SM_WMPP_v16.Report/StaticResources/RegisteredResources" / asset).is_file()
    updates, pages = {}, []
    for page in original.read(original.PROJECT / "MOBILE_LAYOUT_DELIVERY.json")["pages"]:
        pid = page["id"]
        root = original.REPORT / "pages" / pid / "visuals"
        # A resume reconstructs the original plan, not a second branding pass.
        # A partially added deterministic logo is checked against that plan
        # before overwriting; it must not change the calculated original z-order.
        added_logo = original.ident(pid + ":brand-logo")
        sources = {p.parent.name: read(p) for p in root.glob("*/visual.json")
                   if not (use_recovery and p.parent.name == added_logo and
                           not (BACKUP / p.relative_to(original.PROJECT)).exists())}
        mobile = {p.parent.name: read(p) for p in root.glob("*/mobile.json")
                  if not (use_recovery and not (BACKUP / p.relative_to(original.PROJECT)).exists()
                          and p.parent.name == added_logo)}
        header = original.ident(pid + ":header")
        assert header in mobile
        after = branded_title(mobile[header], template_title)
        if after != mobile[header]: updates[root / header / "mobile.json"] = after
        candidates = [vid for vid, v in sources.items() if resource(v) == asset
                      and not compact.hidden(vid, sources) and not v.get("parentGroupName")]
        assert len(candidates) <= 1, (page["name"], "Ambiguous logo")
        new_source = not candidates
        logo = candidates[0] if candidates else original.ident(pid + ":brand-logo")
        if new_source:
            assert logo not in sources
            source = deepcopy(template_logo)
            source["name"] = logo
            desktop = original.read(root.parent / "page.json")
            source["position"].update(x=desktop["width"] + 80, y=120,
                z=max(v["position"].get("z", 0) for v in sources.values()) + 1000)
            source["visual"]["visualContainerObjects"]["general"] = original.obj(
                altText=original.literal("'Mobile: Birmingham Children’s Trust logo'"))
            updates[root / logo / "visual.json"] = source
        if logo not in mobile: updates[root / logo / "mobile.json"] = deepcopy(phone_logo)
        else: assert mobile[logo] == phone_logo, "Preserve the user's saved logo placement."
        pages.append({"id": pid, "name": page["name"], "header": header, "logo": logo,
            "new_off_canvas_source": new_source,
            "title_text_before": [r.get("value") for r in title_runs(mobile[header])],
            "overlaps_before": native.clashes(sources, mobile)})
    return updates, pages, asset


def verify(pages, asset, updates=None):
    updates = updates or {}
    for page in pages:
        root = original.REPORT / "pages" / page["id"] / "visuals"
        sources = {p.parent.name: original.read(p) for p in root.glob("*/visual.json")}
        mobile = {p.parent.name: original.read(p) for p in root.glob("*/mobile.json")}
        for path, value in updates.items():
            if path.parent.parent == root:
                (mobile if path.name == "mobile.json" else sources)[path.parent.name] = value
        logo, title = mobile[page["logo"]], mobile[page["header"]]
        assert resource(sources[page["logo"]]) == asset
        assert not compact.hidden(page["logo"], sources)
        assert {k: logo["position"][k] for k in ("x", "y", "height", "width")} == {
            "x": 0, "y": 9, "height": 25, "width": 111}
        assert {k: title["position"][k] for k in ("x", "y", "height", "width")} == {
            "x": 120, "y": 9, "height": 25, "width": 203}
        assert [r.get("value") for r in title_runs(title)] == page["title_text_before"]
        assert all(r["textStyle"]["fontSize"] == "9pt" for r in title_runs(title))
        assert not compact.overlap(logo["position"], title["position"])
        assert not (set(map(tuple, native.clashes(sources, mobile))) - set(map(tuple, page["overlaps_before"])))
        assert not (set(native.navigation_ids(page["id"])) & set(mobile))
        if page["new_off_canvas_source"]:
            assert sources[page["logo"]]["position"]["x"] >= original.read(root.parent / "page.json")["width"]
    return {"pages": len(pages), "title_font_points": 9, "logo_title_overlaps": 0,
            "new_content_overlaps": 0, "native_render_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.verify:
        d = original.read(DELIVERY)
        assert original.digest_mapping(project_hashes(d["targets"])) == d["protected_files_fingerprint"]
        assert cache_state() == {k: tuple(v) for k, v in d["cache_before"].items()}
        for name, digest in d["target_hashes"].items():
            assert hashlib.sha256((original.PROJECT / name).read_bytes()).hexdigest() == digest
        print(json.dumps(verify(d["pages"], d["asset"])))
        return
    updates, pages, asset = plan(args.resume)
    if args.check:
        print(json.dumps(verify(pages, asset)))
        return
    checks = verify(pages, asset, updates)
    schemas = home.published_schema_check(updates) if args.validate else {}
    print(json.dumps({"changed_files": len(updates), "new_logo_sources": sum(p["new_off_canvas_source"] for p in pages),
                      "checks": checks, "schema": schemas}), flush=True)
    if not args.apply_via: return
    assert not DELIVERY.exists(), "Already delivered; verify rather than repeat."
    assert BACKUP.exists() if args.resume else not BACKUP.exists(), "Inspect recovery files before repeating."
    baseline, caches = project_hashes(updates), cache_state()
    assert caches
    if args.resume:
        before = {p: (BACKUP / p.relative_to(original.PROJECT)).read_bytes() for p in updates
                  if (BACKUP / p.relative_to(original.PROJECT)).exists()}
        for path, value in updates.items():
            if path.exists():
                assert path.read_bytes() == before.get(path) or original.read(path) == value, "Unexpected target edit during resume."
    else:
        before = {p: p.read_bytes() for p in updates if p.exists()}
        BACKUP.mkdir(parents=True)
        for path in before:
            saved = BACKUP / path.relative_to(original.PROJECT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
    current = {p: p.read_bytes() for p in updates if p.exists()}
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert project_hashes(updates) == baseline and cache_state() == caches
    for path, value in updates.items():
        if path in current:
            assert path.read_bytes() == current[path]
        else:
            assert not path.exists()
        path.parent.mkdir(parents=True, exist_ok=True)
        # Keep report definitions compact; only this requested branding changes.
        compact.patch_file(path, json.dumps(value, ensure_ascii=True, separators=(",", ":")) + "\n", args.apply_via)
    assert project_hashes(updates) == baseline and cache_state() == caches
    checks = verify(pages, asset)
    record = {"date": "2026-10-15", "scope": "Existing mobile pages only", "pages": pages,
        "asset": asset, "checks": checks, "schema": schemas, "backup": str(BACKUP),
        "targets": [str(p.relative_to(original.PROJECT)) for p in updates],
        "target_hashes": {str(p.relative_to(original.PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in updates},
        "protected_files_fingerprint": original.digest_mapping(baseline),
        "protected_file_count": len(baseline), "cache_before": {k: list(v) for k, v in caches.items()},
        "resumed_after_utf8_verification_failure": args.resume,
        "note": "Baseline includes the user's latest Desktop save. Legacy deliveries remain historical; no model/assets/existing desktop visual definitions altered."}
    compact.patch_file(DELIVERY, record, args.apply_via)
    print(json.dumps({"saved": checks, "cached_database_and_non_target_files_unchanged": True,
                      "backup": str(BACKUP)}), flush=True)


if __name__ == "__main__": main()
