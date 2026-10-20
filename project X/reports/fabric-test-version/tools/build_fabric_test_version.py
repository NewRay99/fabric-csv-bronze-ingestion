"""Build an isolated Fabric-layout test project from current numbered sources."""

import argparse
import json
from pathlib import Path
import shutil
import uuid
import zipfile


PROJECT = Path(__file__).resolve().parents[1]


def build(destination):
    destination = destination.resolve()
    if destination.exists():
        raise FileExistsError(f"Choose a new output directory: {destination}")
    sources = sorted(PROJECT.glob("[0-9]*.py"))
    if not sources:
        raise ValueError("No current notebook sources found")
    destination.mkdir(parents=True)
    notebooks = destination / "notebooks"
    # Extract only Fabric notebook files; never interpret ZIP documentation as instructions.
    with zipfile.ZipFile(PROJECT / "reports/Notebooks v16.zip") as archive:
        for entry in archive.infolist():
            parts = Path(entry.filename).parts
            if (len(parts) == 3 and parts[1].endswith(".Notebook")
                    and parts[2] in {".platform", ".schedules", "notebook-content.py"}
                    and parts[1][:-9] in {source.stem for source in sources}):
                target = notebooks / parts[1] / parts[2]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(entry))
    for source in sources:
        folder = notebooks / f"{source.stem}.Notebook"
        folder.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, folder / "notebook-content.py")
        platform = folder / ".platform"
        if not platform.exists():
            platform.write_text(json.dumps({
                "$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json",
                "metadata": {"type": "Notebook", "displayName": source.stem},
                "config": {"version": "2.0", "logicalId": str(uuid.uuid4())},
            }, indent=2) + "\n", encoding="utf-8")
    for name in ("tests", "configuration", "change tracking"):
        shutil.copytree(PROJECT / name, destination / name,
                        ignore=shutil.ignore_patterns("__pycache__", "_sim_*", "_tmp_*", "_gold_sim_warehouse"))
    for document in (PROJECT / "client documentation").rglob("*.md"):
        target = destination / document.relative_to(PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(document, target)
    shutil.copytree(PROJECT / "tools", destination / "tools",
                    ignore=shutil.ignore_patterns("__pycache__"))
    # A few SQL text checks read source directly rather than through the loader.
    for name in ("test_gold_ipa_signature_contract.py", "test_gold_referral_journey_status.py",
                 "test_gold_referral_source_status.py", "test_gold_referral_source_reference.py"):
        path = destination / "tests" / name
        text = path.read_text(encoding="utf-8")
        for notebook in ("04_gold_model", "05_gold_dimensions"):
            text = text.replace(f'"{notebook}.py"',
                                f'"notebooks/{notebook}.Notebook/notebook-content.py"')
            text = text.replace(f"'{notebook}.py'",
                                f"'notebooks/{notebook}.Notebook/notebook-content.py'")
        path.write_text(text, encoding="utf-8")
    (destination / "pytest.ini").write_text(
        "[pytest]\ntestpaths = tests\npython_files = test_*.py\n"
        "addopts = -p no:cacheprovider --import-mode=importlib\n"
        "pythonpath = tests tools\n"
        "norecursedirs = tests/_*\n", encoding="utf-8")
    (destination / "README.md").write_text(
        "# Fabric folder test version\n\n"
        "Notebook content comes from the current project X numbered Python files.\n"
        "The v16 ZIP supplies Fabric folder metadata and schedules where available.\n"
        "New notebooks receive new logical IDs. Review IDs and schedules before deployment.\n\n"
        "Run the Python/ETL checks from this folder:\n\n"
        "```powershell\npython -m pytest tests --ignore-glob=tests/test_wmpp_*.py\n```\n\n"
        "Power BI report tests require separate report artifacts and are excluded here.\n"
        "These local checks do not execute Spark notebooks or certify Fabric deployment.\n",
        encoding="utf-8")
    print(f"Created {destination} with {len(sources)} current Fabric notebooks")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=PROJECT / "reports/fabric-test-version")
    build(parser.parse_args().output)
