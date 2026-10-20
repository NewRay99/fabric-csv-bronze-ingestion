"""Restore explicit native-state mobile drawer button labels.

This is a saved-configuration repair. It does not prove native rendering.
"""

import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil

import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original


def plans(page_id=None):
    delivery = original.read(original.PROJECT / "MOBILE_LAYOUT_DELIVERY.json")
    result = []
    for page in delivery["pages"]:
        if page_id and page["id"] != page_id:
            continue
        for vid in page["new_visual_ids"]:
            folder = original.REPORT / "pages" / page["id"] / "visuals" / vid
            source = original.read(folder / "visual.json")
            if original.vtype(source) != "actionButton" or not original.label(source).strip():
                continue  # The empty scrim is intentionally not a labelled control.
            path = folder / "mobile.json"
            mobile = original.read(path)
            fixed = deepcopy(mobile)
            fixed.setdefault("objects", {})["text"] = compact.complete_button_text(
                source["visual"]["objects"]["text"], mobile.get("objects", {}).get("text", []))
            result.append((page, path, mobile, fixed))
    assert result, "No matching mobile drawer controls."
    return result


def check(items):
    errors = []
    for page, path, mobile, expected in items:
        entries = mobile.get("objects", {}).get("text", [])
        state_errors = []
        for name in ("default", "hover", "selected", "disabled"):
            props = next((e.get("properties", {}) for e in entries
                          if e.get("selector") == {"id": name}), {})
            if (not original.decode(props.get("text", {})).strip()
                    or original.decode(props.get("show", {})) != "true"
                    or compact.number(props.get("fontSize", {})) is None
                    or compact.number(props["fontSize"]) > 10):
                state_errors.append(name)
        if state_errors or entries != expected["objects"]["text"]:
            errors.append((page["name"], path.parent.name))
    return errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--page")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--apply-via")
    args = parser.parse_args()
    items = plans(args.page)
    errors = check(items)
    if args.check:
        print(json.dumps({"labelled_controls": len(items), "invalid_state_specific_labels": len(errors),
                          "examples": errors[:3]}))
        raise SystemExit(1 if errors else 0)
    documents = [(str(path), fixed) for _, path, _, fixed in items]
    schemas = original.validate_documents(documents) if args.validate else {}
    print(json.dumps({"planned_controls": len(errors), "pages": len({page["id"] for page, *_ in items}),
                      "schema": schemas}), flush=True)
    if not args.apply_via:
        return
    backup = original.ROOT / "reports/_review" / ("mobile-drawer-text-states-20261013-" + (args.page or "all"))
    assert not backup.exists(), "Backup exists; inspect before repeating the repair."
    baseline = compact.protected()
    changed = [(page, path, mobile, fixed) for page, path, mobile, fixed in items if mobile != fixed]
    backup.mkdir(parents=True)
    for _, path, _, _ in changed:
        saved = backup / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = backup
    compact.patch_file(backup / ".gitignore", "*\n", args.apply_via)
    assert compact.protected() == baseline, "Definitions changed before applying."
    for index, (_, path, mobile, fixed) in enumerate(changed, 1):
        assert original.read(path) == mobile, "Mobile state changed during diagnosis."
        compact.patch_file(path, fixed, args.apply_via)
        if index % 50 == 0:
            print(json.dumps({"saved_controls": index}), flush=True)
    assert compact.protected() == baseline, "Non-mobile definitions changed."
    assert not check(plans(args.page)), "Drawer label repair did not persist."
    print(json.dumps({"saved_controls": len(changed), "protected_definitions": baseline["files"],
                      "non_mobile_files_unchanged": True, "backup": str(backup),
                      "native_render_verified": False}), flush=True)


if __name__ == "__main__":
    main()
