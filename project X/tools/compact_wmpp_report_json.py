"""Shrink PBIR disk size by lossless JSON formatting only; never touch cache.abf.

The bulk formatting pass is deliberately separate from semantic edits. Strictly
parsed values must be identical before/after each atomic file replacement.
Recovery copies are outside the WIP project. Cached/local-state/model/media files
are protected by full byte hashes and are not rewritten or copied into the WIP.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original
import use_wmpp_native_mobile_navigation as native

BACKUP = original.ROOT / "reports/_review/report-json-format-before-20261015"
DELIVERY = original.PROJECT / "REPORT_JSON_COMPACTION_DELIVERY.json"
NATIVE_DELIVERY = native.DELIVERY
METADATA = {compact.MANIFEST, NATIVE_DELIVERY, DELIVERY}


def unique_pairs(items):
    result = {}
    for key, value in items:
        if key in result: raise ValueError("Duplicate JSON property: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Non-JSON numeric constant: " + value)


def load_json(raw):
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_pairs, parse_constant=reject_constant)


def minified(raw):
    value = load_json(raw)
    result = (json.dumps(value, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")
    assert load_json(result) == value
    return result


def project_size():
    return sum(path.stat().st_size for path in original.PROJECT.rglob("*") if path.is_file())


def byte_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def semantic_report_fingerprint():
    return original.digest_mapping({path.relative_to(original.PROJECT).as_posix(): hashlib.sha256(
        minified(path.read_bytes())).hexdigest() for path in original.REPORT.rglob("*.json")})


def protected_files(targets):
    return {str(path.relative_to(original.PROJECT)): byte_hash(path) for path in original.PROJECT.rglob("*")
            if path.is_file() and path not in targets and path not in METADATA}


def caches():
    result = {}
    for path in original.PROJECT.rglob("*"):
        if path.is_file() and (path.suffix.lower() in {".abf", ".adb"} or
                               path.name.lower() in {"cache.abf", "cache.adb", "cach.adb"}):
            result[str(path.relative_to(original.PROJECT))] = {"bytes": path.stat().st_size,
                "sha256": byte_hash(path), "modified_ns": path.stat().st_mtime_ns}
    assert result, "Locate and protect the cache before applying."
    return result


def plan():
    values, before, after = {}, 0, 0
    for path in original.REPORT.rglob("*.json"):
        raw = path.read_bytes()
        value = minified(raw)
        before += len(raw)
        after += min(len(raw), len(value))
        if len(value) < len(raw): values[path] = value
    return values, {"report_json_bytes_before": before, "report_json_bytes_after": after,
                    "potential_bytes_saved": before - after, "files_to_compact": len(values)}


def replace_formatting(path, data):
    assert path.resolve().is_relative_to(original.REPORT.resolve()) and path.suffix == ".json"
    # Only lexical JSON whitespace/escaping may change. Cache/model/local-state
    # paths are not valid formatting targets.
    assert ".pbi" not in path.parts and "StaticResources" not in path.parts
    assert load_json(path.read_bytes()) == load_json(data)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".wmpp-compact-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(data)
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            assert temporary.parent.resolve() == path.parent.resolve() and temporary.name.startswith(".wmpp-compact-")
            temporary.unlink()
    assert path.read_bytes() == data


def verify(delivery):
    assert caches() == delivery["cache_files"], "Cached database bytes/timestamp changed."
    assert semantic_report_fingerprint() == delivery["semantic_report_fingerprint"], "Report JSON values changed."
    remaining, projection = plan()
    assert not remaining, projection
    checked = 0
    for source in (BACKUP / "SM_WMPP_v16.Report/definition").rglob("*.json"):
        path = original.PROJECT / source.relative_to(BACKUP)
        assert load_json(path.read_bytes()) == load_json(source.read_bytes())
        checked += 1
    assert checked == delivery["compacted_files"]
    targets = set(original.REPORT.rglob("*.json"))
    assert original.digest_mapping(protected_files(targets)) == delivery["protected_other_files_fingerprint"]
    assert compact.protected() == original.read(compact.MANIFEST)["protected"]
    return {"compacted_files": checked, "all_parsed_report_values_identical": True,
        "cached_database_bytes_and_timestamp_unchanged": True, "model_media_and_other_files_unchanged": True,
        "project_bytes_now": project_size(), "native_desktop_reopen_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-compact", action="store_true")
    parser.add_argument("--apply-formatting-via")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(original.read(DELIVERY))))
        return
    updates, projection = plan()
    print(json.dumps({"project_bytes_now": project_size(), **projection}), flush=True)
    if args.check_compact:
        assert not updates, "Lossless whitespace-only size reduction is still available."
        return
    if not args.apply_formatting_via: return
    assert not BACKUP.exists() and not DELIVERY.exists(), "Inspect existing recovery copy before repeating."
    assert updates
    original_size = project_size()
    cache_before = caches()
    protected = protected_files(set(updates))
    protected_fingerprint = original.digest_mapping(protected)
    semantic_fingerprint = semantic_report_fingerprint()
    before_hashes = {path: byte_hash(path) for path in updates}
    BACKUP.mkdir(parents=True)
    for path in list(updates) + [compact.MANIFEST, NATIVE_DELIVERY]:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_formatting_via)
    assert caches() == cache_before
    assert protected_files(set(updates)) == protected
    for path, data in updates.items():
        assert byte_hash(path) == before_hashes[path], "File changed after the formatting plan."
        assert (BACKUP / path.relative_to(original.PROJECT)).read_bytes() == path.read_bytes()
        replace_formatting(path, data)
    assert semantic_report_fingerprint() == semantic_fingerprint
    assert protected_files(set(updates)) == protected
    assert caches() == cache_before
    manifest = original.read(compact.MANIFEST)
    previous = manifest["protected"]
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-15",
        "reason": "Lossless report-definition JSON minification only; all parsed values and cached database preserved.",
        "compacted_files": len(updates), "previous_byte_fingerprint": previous,
        "semantic_report_fingerprint": semantic_fingerprint})
    compact.patch_file(compact.MANIFEST, manifest, args.apply_formatting_via)
    nav = original.read(NATIVE_DELIVERY)
    nav.setdefault("authorised_formatting_updates", []).append({"date": "2026-10-15",
        "previous_byte_fingerprint": nav["saved_report_model_assets_fingerprint"],
        "reason": "Report JSON minification; values/layout/navigation unchanged."})
    nav["saved_report_model_assets_fingerprint"] = original.digest_mapping(native.protected_files(set()))
    compact.patch_file(NATIVE_DELIVERY, nav, args.apply_formatting_via)
    delivery = {"date": "2026-10-15", "project_bytes_before": original_size,
        "compacted_files": len(updates), **projection, "cache_files": cache_before,
        "semantic_report_fingerprint": semantic_fingerprint,
        "protected_other_files_fingerprint": protected_fingerprint, "backup": str(BACKUP),
        "all_parsed_report_values_identical": True, "native_desktop_reopen_verified": False,
        "existing_zip_unchanged": True,
        "note": "Folder-size reduction, not data/model compression. Desktop may re-expand JSON formatting on a later save."}
    # Include this small delivery record in the final folder-size prediction.
    for _ in range(5):
        predicted = project_size() + len(original.json_text(delivery).encode("utf-8"))
        if delivery.get("project_bytes_after") == predicted: break
        delivery["project_bytes_after"] = predicted
    compact.patch_file(DELIVERY, delivery, args.apply_formatting_via)
    result = verify(delivery)
    print(json.dumps({"project_bytes_before": original_size, "project_bytes_after": project_size(),
        "actual_bytes_saved": original_size - project_size(), "checks": result, "backup": str(BACKUP)}), flush=True)


if __name__ == "__main__": main()
