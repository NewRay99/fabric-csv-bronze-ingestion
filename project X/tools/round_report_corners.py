"""Enable rounded visual containers; leave shadows, spacing and data untouched."""

from copy import deepcopy
from datetime import datetime
import shutil

from apply_report_soft_glow import BUNDLE, ROOT, DATA_KINDS, fill, lit, props, read, save


def main():
    reports = list(BUNDLE.glob("*/*.Report"))
    backup = BUNDLE / "_review" / ("rounded-corners-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True)
    count = 0
    for report in reports:
        for path in report.glob("definition/pages/*/visuals/*/visual.json"):
            value = read(path)
            visual = value["visual"]
            if visual["visualType"] not in DATA_KINDS:
                continue
            containers = visual.get("visualContainerObjects", {})
            background = containers.get("background", [{}])[0].get("properties", {})
            if background.get("show", {}).get("expr", {}).get("Literal", {}).get("Value") != "true":
                continue  # Inner charts and labels use their existing rounded parent panel.
            if value["position"]["height"] < 70 or value["position"]["width"] < 100:
                continue
            before = deepcopy(value)
            target = backup / report.name / path.relative_to(report)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            containers["border"] = props(
                show=lit("true"), radius=lit("14D"), width=lit("1D"),
                color=deepcopy(background.get("color", fill("#FFFFFF"))),
            )
            save(path, value)
            expected = deepcopy(before)
            expected["visual"]["visualContainerObjects"]["border"] = containers["border"]
            assert read(path) == expected
            count += 1
    themes = [ROOT / "assets/brand-pack/WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json", ROOT / "reports/templates/WMPP_Common_Theme.json"]
    themes += [r / "StaticResources/RegisteredResources/WMPP_Theme.json" for r in reports]
    for i, path in enumerate(themes):
        shutil.copy2(path, backup / f"theme-{i}.json")
        theme = read(path)
        for kind in DATA_KINDS:
            styles = theme["visualStyles"].setdefault(kind, {})
            for name in ("*", "WMPP Soft Glow"):
                style = styles.setdefault(name, {})
                style["border"] = [{"show": True, "radius": 14, "width": 1, "color": {"solid": {"color": "#FFFFFF"}}}]
        save(path, theme)
    print(f"Rounded {count} standalone visual containers; updated {len(themes)} theme copies.")
    print("Only corner/border properties changed; shadows, padding, queries and positions preserved.")
    print("Backup:", backup)


if __name__ == "__main__":
    main()
