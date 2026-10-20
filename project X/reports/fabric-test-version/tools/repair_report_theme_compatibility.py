"""Restore v0 report style compatibility without rebuilding models or layouts.

Run only against the local delivery copy. Keep the failed theme and report
definitions in _review; never modify the immutable WMPP_Theme_v0.json backup.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BRAND = ROOT / "assets/brand-pack"
BUNDLE = ROOT / "reports/client-deliverables/WMPP v16"
COMPACT = "WMPP Compact KPI"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def referenced_presets(report):
    for path in report.glob("definition/pages/*/visuals/*/visual.json"):
        visual = read(path)["visual"]
        for group in ("objects", "visualContainerObjects"):
            for setting in visual.get(group, {}).get("stylePreset", []):
                name = setting["properties"]["name"]["expr"]["Literal"]["Value"].strip("'")
                yield visual["visualType"], name, path


def main():
    baseline_path = BRAND / "WMPP_Theme_v0.json"
    baseline_bytes = baseline_path.read_bytes()
    old = read(baseline_path)
    current = read(BRAND / "WMPP_Theme.json")
    reports = sorted(BUNDLE.glob("*/*.Report"))
    if len(reports) != 2:
        raise ValueError("Expected exactly the two local delivery reports")
    # This is a targeted preflight, not a semantic-model or versioned test suite.
    missing = 0
    for report in reports:
        for kind, name, path in referenced_presets(report):
            if not name.startswith("WMPP") or name == COMPACT:
                continue  # Built-in presets, e.g. Tile, belong to the base theme.
            if name not in old["visualStyles"].get(kind, {}):
                raise ValueError(f"Rollback theme lacks {name}: {path}")
            missing += name not in current["visualStyles"].get(kind, {})
    print("Before repair: missing named-style references:", missing)

    backup = BUNDLE / "_review" / ("theme-repair-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copy2(BRAND / "WMPP_Theme.json", backup / "theme-before.json")
    for i, report in enumerate(reports):
        target = backup / str(i)
        target.mkdir()
        shutil.copytree(report / "definition", target / "definition")
        shutil.copy2(
            report / "StaticResources/RegisteredResources/WMPP_Theme.json", target / "theme.json"
        )
    model_hashes = {
        path: hashlib.sha256(path.read_bytes()).hexdigest()
        for model in BUNDLE.glob("*/*.SemanticModel")
        for path in model.rglob("*")
        if path.is_file()
    }

    theme = deepcopy(old)
    theme["name"] = "WMPP — layout-compatible"
    # Preserve v0 sizes, fonts, palette ordering and every named preset. Do not
    # mix the standalone brand defaults with layout-specific inherited styles.
    styles = theme["visualStyles"]
    # Retain the current approved canvas when restoring legacy visual presets.
    for surface in ("background", "outspace"):
        styles["page"]["*"][surface][0]["color"]["solid"]["color"] = "#F8F5F1"
    zero = {"top": 0, "bottom": 0, "left": 0, "right": 0}
    styles["*"]["*"]["padding"] = [dict(zero)]
    textbox = styles.setdefault("textbox", {}).setdefault("*", {})
    textbox.update(
        {key: [{"show": False}] for key in ("background", "border", "dropShadow", "title")}
    )
    textbox["padding"] = [dict(zero)]
    slicer = styles["slicer"]["*"]
    slicer["padding"] = [dict(zero)]
    slicer["items"][0]["padding"] = 2

    compact = {
        "padding": [
            {
                "$id": "default",
                "paddingSelection": "Custom",
                "paddingIndividual": True,
                "leftMargin": 0,
                "rightMargin": 0,
                "topMargin": 0,
                "bottomMargin": 0,
            }
        ],
        "layout": [
            {
                "$id": "default",
                "autoGrid": True,
                "rowCount": 1,
                "columnCount": 1,
                "cellPadding": 0,
                "leftOuterMargin": 0,
                "rightOuterMargin": 0,
                "topOuterMargin": 0,
                "bottomOuterMargin": 0,
                "backgroundShow": False,
            }
        ],
        "value": [
            {
                "$id": "default",
                "fontFamily": "Segoe UI Semibold",
                "fontSize": 29,
                "horizontalAlignment": "left",
            }
        ],
    }
    for key in (
        "label",
        "fillCustom",
        "outline",
        "shadowCustom",
        "accentBar",
        "divider",
        "image",
        "cardImage",
    ):
        compact[key] = [{"$id": "default", "show": False}]
    for key in ("background", "border", "dropShadow", "title", "subTitle"):
        compact[key] = [{"show": False}]
    styles["cardVisual"][COMPACT] = compact
    from apply_report_soft_glow import apply_theme_glow

    apply_theme_glow(theme)
    save(BRAND / "WMPP_Theme.json", theme)

    count = 0
    for report in reports:
        shutil.copy2(
            BRAND / "WMPP_Theme.json",
            report / "StaticResources/RegisteredResources/WMPP_Theme.json",
        )
        for path in report.glob("definition/pages/*/visuals/*/visual.json"):
            value = read(path)
            visual = value["visual"]
            if visual["visualType"] != "cardVisual":
                continue
            # Recognize only this generator's compact callout cards; legacy
            # visual presets and manually sized report objects remain untouched.
            if value["position"]["height"] != 50:
                continue
            padding = visual.get("objects", {}).get("padding", [])
            if not padding or padding[0].get("selector", {}).get("id") != "default":
                continue
            visual["visualContainerObjects"]["stylePreset"] = [
                {"properties": {"name": literal("'" + COMPACT + "'")}}
            ]
            layout = compact["layout"][0]
            visual["objects"]["layout"] = [
                {
                    "selector": {"id": "default"},
                    "properties": {
                        k: literal(str(v).lower() if isinstance(v, bool) else str(v) + "L")
                        for k, v in layout.items()
                        if k != "$id"
                    },
                }
            ]
            save(path, value)
            count += 1
        missing_after = [
            name
            for kind, name, _ in referenced_presets(report)
            if name.startswith("WMPP") and name not in styles.get(kind, {})
        ]
        if missing_after:
            raise AssertionError(missing_after)
    if baseline_path.read_bytes() != baseline_bytes:
        raise AssertionError("Rollback backup changed")
    if any(hashlib.sha256(p.read_bytes()).hexdigest() != h for p, h in model_hashes.items()):
        raise AssertionError("Semantic-model content changed")
    print("After repair: missing named-style references: 0")
    print("Compact KPI card margin corrections:", count)
    print("Saved corrected shared theme; v0 and semantic models unchanged.")
    print("Before-repair backup:", backup)


if __name__ == "__main__":
    main()
