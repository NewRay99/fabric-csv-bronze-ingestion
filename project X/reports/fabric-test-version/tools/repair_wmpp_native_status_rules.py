"""Narrow WIP repair: only status icon expressions, with a recoverable backup.

Default is read-only preview. --apply performs a bulk mechanical JSON rewrite,
not report generation, and checks that layout, model and other files stay intact.
"""

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil
import uuid

from wmpp_status_icons import TARGET_COLUMNS, icon_format


PROJECT = Path(__file__).resolve().parents[1] / "reports/WIP/SM WMPP v16 updated WIP"
REPORT_NAME = "SM_WMPP_v16.Report"


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def rewrite_visual(original):
    """Return a copy changing only existing status icon value expressions."""
    result = deepcopy(original)
    visual = result.get("visual", {})
    if visual.get("visualType") not in {"tableEx", "pivotTable"}:
        return result, []
    projections = {}
    for group in visual.get("query", {}).get("queryState", {}).values():
        for projection in group.get("projections", []):
            reference = projection.get("field", {})
            column = reference.get("Column") or reference.get("Aggregation", {}).get(
                "Expression", {}
            ).get("Column")
            if column and column.get("Property") in TARGET_COLUMNS:
                projections[projection["queryRef"]] = reference
    changed = []
    for entry in visual.get("objects", {}).get("values", []):
        metadata = entry.get("selector", {}).get("metadata")
        icon = entry.get("properties", {}).get("icon")
        if metadata not in projections or not icon or icon.get("kind") != "Icon":
            continue
        desired = icon_format(projections[metadata])["value"]
        if icon.get("value") != desired:
            icon["value"] = desired
            changed.append(metadata)
    return result, changed


def assert_only_icon_values_changed(before, after, metadata):
    stripped = deepcopy(after)
    old_entries = before["visual"]["objects"]["values"]
    new_entries = stripped["visual"]["objects"]["values"]
    for old, new in zip(old_entries, new_entries, strict=True):
        if old.get("selector", {}).get("metadata") in metadata:
            new["properties"]["icon"]["value"] = deepcopy(old["properties"]["icon"]["value"])
    if stripped != before:
        raise AssertionError("Repair changed something other than status icon values")


def native_evidence(definition):
    """Require the user's saved working rule, not a guessed generic template."""
    path = definition / "pages/f3070e87127b751f89d4/visuals/4a70f5c5a98aea85ed0a/visual.json"
    document = read_json(path)
    for entry in document["visual"]["objects"]["values"]:
        if entry.get("selector", {}).get("metadata") != "fact_referral.current_status":
            continue
        cases = entry.get("properties", {}).get("icon", {}).get("value", {}).get(
            "expr", {}
        ).get("Conditional", {}).get("Cases", [])
        for case in cases:
            condition = case.get("Condition", {})
            comparison = condition.get("Comparison", {})
            if comparison.get("Right", {}).get("Literal", {}).get("Value") != "'UNDER_OFFER'":
                continue
            expected = {
                "PowerBI.SQExprEvaluationKind": 1,
                "PowerBI.SQExprTextOperatorOption": 2,
            }
            if comparison.get("ComparisonKind") == 0 and condition.get("Annotations") == expected:
                return {"path": str(path), "sha256": digest(path), "condition": condition}
    raise RuntimeError("The saved working native UNDER_OFFER rule was not found; no files changed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    project = PROJECT.resolve(strict=True)
    definition = project / REPORT_NAME / "definition"
    evidence = native_evidence(definition)
    original_hashes = {
        path: digest(path) for path in project.rglob("*")
        if path.is_file() and ".pbi" not in path.relative_to(project).parts
    }
    planned = []
    for path in sorted((definition / "pages").glob("*/visuals/*/visual.json")):
        before = read_json(path)
        after, metadata = rewrite_visual(before)
        if not metadata:
            continue
        assert_only_icon_values_changed(before, after, metadata)
        planned.append((path, before, after, metadata))
    summary = {
        "project": str(project), "apply": args.apply, "visuals": len(planned),
        "status_columns": sum(len(item[3]) for item in planned),
        "pages": len({item[0].parents[2].name for item in planned}),
    }
    if not args.apply or not planned:
        print(json.dumps(summary, indent=2))
        return
    backup = project.parent / "_review" / (
        "native-status-rules-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8]
    )
    backup.mkdir(parents=True, exist_ok=False)
    manifest = {**summary, "native_evidence": evidence, "files": []}
    for path, _, _, metadata in planned:
        relative = path.relative_to(project)
        target = backup / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        if digest(target) != original_hashes[path]:
            raise RuntimeError(f"File changed while taking backup: {relative}")
        manifest["files"].append({
            "path": str(relative), "before_sha256": original_hashes[path], "status_columns": metadata,
        })
    manifest_path = backup / "repair-manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    for path, _, after, _ in planned:
        if digest(path) != original_hashes[path]:
            raise RuntimeError(f"File changed since preview; stop to preserve new user edits: {path}")
        path.write_text(json.dumps(after, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    changed_paths = {item[0] for item in planned}
    for path, original_hash in original_hashes.items():
        if path not in changed_paths and digest(path) != original_hash:
            raise RuntimeError(f"Unrelated file changed during repair; inspect before proceeding: {path}")
    for path, before, _, metadata in planned:
        assert_only_icon_values_changed(before, read_json(path), metadata)
    manifest["verified"] = "Only status icon value expressions changed; all other file hashes unchanged"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({**summary, "backup": str(backup), "verified": manifest["verified"]}, indent=2))


if __name__ == "__main__":
    main()
