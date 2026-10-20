"""Check/reapply SEM-004 to its exact saved-WIP baseline; no model refresh."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import uuid


def digest(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else None


def within(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Path outside intended directory: {relative}")
    return path


def install(project: Path, package: Path, apply: bool, backup: Path) -> dict:
    manifest = json.loads((package / "manifest.json").read_text(encoding="utf-8"))
    changes = []
    # Verify the entire plan before writing any target.
    for entry in manifest["files"]:
        target = within(project, entry["target"])
        payload = within(package, entry["payload"])
        if digest(payload) != entry["after_sha256"]:
            raise ValueError(f"Altered source payload: {entry['payload']}")
        current = digest(target)
        if current not in (entry["before_sha256"], entry["after_sha256"]):
            raise ValueError(f"Unexpected baseline; no files changed: {entry['target']}")
        if current != entry["after_sha256"]:
            changes.append((entry, target, payload))
    if apply:
        for entry, target, payload in changes:
            saved = within(backup, entry["target"])
            if target.exists():
                saved.parent.mkdir(parents=True, exist_ok=True)
                if saved.exists() and digest(saved) != entry["before_sha256"]:
                    raise ValueError(f"Existing backup differs: {saved}")
                shutil.copy2(target, saved)
        for entry, target, payload in changes:
            # Refuse a concurrent edit after the initial preflight/backup.
            if digest(target) != entry["before_sha256"]:
                raise ValueError(f"Concurrent target edit: {target}")
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(target.name + ".sem004-" + uuid.uuid4().hex + ".tmp")
            try:
                shutil.copyfile(payload, temporary)
                os.replace(temporary, target)
            finally:
                if temporary.exists():
                    temporary.unlink()
    return {"change": manifest["change_id"], "status": "applied" if apply else "checked",
            "files_to_change": len(changes), "already_applied": len(manifest["files"]) - len(changes),
            "refresh_or_live_model_write": False}


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path,
                        default=root / "reports/WIP/SM WMPP v16 updated WIP")
    parser.add_argument("--package", type=Path,
                        default=root / "reports/change-records/2026-10-18-requirement-kpis")
    parser.add_argument("--backup", type=Path,
                        default=root / "reports/_review/requirement-kpis-before-20261018")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    print(json.dumps(install(args.project, args.package, args.apply, args.backup), indent=2))


if __name__ == "__main__":
    main()
