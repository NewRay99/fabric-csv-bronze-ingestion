"""Inset standalone chart content without moving visuals or restyling cards."""

from copy import deepcopy
from datetime import datetime
import shutil

from apply_report_soft_glow import (
    BUNDLE,
    ROOT,
    CHART_KINDS,
    CHART_PADDING,
    lit,
    props,
    read,
    save,
)


def apply_padding():
    backup = BUNDLE / "_review" / ("chart-padding-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True)
    reports = list(BUNDLE.glob("*/*.Report"))
    summary = {}
    for report in reports:
        changed = []
        for path in report.glob("definition/pages/*/visuals/*/visual.json"):
            value = read(path)
            visual = value["visual"]
            if visual["visualType"] not in CHART_KINDS:
                continue
            containers = visual.get("visualContainerObjects", {})
            background = containers.get("background", [{}])[0].get("properties", {})
            if background.get("show", {}).get("expr", {}).get("Literal", {}).get("Value") != "true":
                continue  # Transparent child visuals already sit inside an inset parent panel.
            if value["position"]["height"] < 100 or value["position"]["width"] < 100:
                continue
            before = deepcopy(value)
            copy = backup / report.name / path.relative_to(report)
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, copy)
            containers["padding"] = props(
                **{key: lit(str(pixels) + "D") for key, pixels in CHART_PADDING.items()}
            )
            save(path, value)
            expected = deepcopy(before)
            expected["visual"]["visualContainerObjects"]["padding"] = containers["padding"]
            assert read(path) == expected, path
            changed.append(str(path.relative_to(report)))
        summary[report.name] = changed
    theme_paths = [
        ROOT / "assets/brand-pack/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
    ]
    theme_paths += [
        report / "StaticResources/RegisteredResources/WMPP_Theme.json" for report in reports
    ]
    for i, path in enumerate(theme_paths):
        shutil.copy2(path, backup / f"theme-{i}.json")
        theme = read(path)
        for kind in CHART_KINDS:
            for preset in theme["visualStyles"].get(kind, {}).values():
                # Named legacy presets otherwise override the corrected chart defaults.
                preset["padding"] = [dict(CHART_PADDING)]
        save(path, theme)
    save(
        backup / "verification.json",
        {
            "changed_visuals": summary,
            "padding": CHART_PADDING,
            "only_visual_padding_changed": True,
            "native_render_verified": False,
        },
    )
    for name, files in summary.items():
        print(f"{name}: padded {len(files)} standalone charts/tables")
    print("Templates updated; data, layout, corners and shadows unchanged.")
    print("Backup:", backup)


if __name__ == "__main__":
    apply_padding()
