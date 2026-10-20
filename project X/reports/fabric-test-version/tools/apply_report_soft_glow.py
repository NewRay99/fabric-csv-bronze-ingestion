"""Restore native panel shadows without composite image backgrounds or data edits."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "reports/client-deliverables/WMPP v16"
DATA_KINDS = {
    "cardVisual",
    "card",
    "multiRowCard",
    "tableEx",
    "pivotTable",
    "azureMap",
    "map",
    "funnel",
    "donutChart",
    "pieChart",
    "lineChart",
    "areaChart",
    "clusteredBarChart",
    "clusteredColumnChart",
    "barChart",
    "columnChart",
    "hundredPercentStackedColumnChart",
}
CHART_KINDS = DATA_KINDS - {"cardVisual", "card", "multiRowCard"}
CHART_PADDING = {"top": 12, "bottom": 12, "left": 16, "right": 16}
REFERENCE = {
    "5038cffdd48af9a80dd1": [(24, 136, 1632, 134)]
    + [(24 + i % 3 * 552, 276 if i < 3 else 592, 528, 300 if i < 3 else 306) for i in range(6)],
    "510f9f9501ccc5ae8a74": [(24, 124, 1632, 134)]
    + [(24 + i % 3 * 552, 260 if i < 3 else 572, 528, 294 if i < 3 else 310) for i in range(6)],
    "6ae319c8916a5d63a4ff": [(24, 120, 1632, 134)]
    + [(24 + i % 3 * 552, 256 if i < 3 else 544, 528, 272 if i < 3 else 282) for i in range(6)],
    "dd3a58c056d723048dbf": [(16, 250, 1648, 420), (16, 674, 1648, 296)],
}
GENERATED = {
    "1cd52e9c7e4016f342ce": [(36, 400, 574, 474), (632, 400, 1012, 474)],
    "f028a4be56d03e8404d7": [(36, 400, 790, 474), (848, 400, 796, 474)],
    "f3070e87127b751f89d4": [
        (36, 400, 488, 474),
        (543, 400, 1101, 224),
        (543, 646, 540, 228),
        (1105, 646, 539, 228),
    ],
    "803165f7d2f5aaccd8ac": [(36, 400, 696, 474), (754, 400, 890, 474)],
    "ed27e90d06816c7c1eee": [
        (36, 230, 792, 370),
        (851, 230, 792, 370),
        (36, 620, 792, 254),
        (851, 620, 792, 254),
    ],
    "d807778066085fbd96dc": [(36, 400, 1020, 474), (1078, 400, 566, 474)],
    "5133b9c7cfcf12cf7f74": [(36, 400, 790, 474), (848, 400, 796, 474)],
}


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def lit(value):
    return {"expr": {"Literal": {"Value": value}}}


def fill(color):
    return {"solid": {"color": lit("'" + color + "'")}}


def props(**values):
    return [{"properties": values}]


def shadow_style(dark=False):
    return {
        "show": True,
        "preset": "Custom",
        "position": "Outer",
        "color": {"solid": {"color": "#000000" if dark else "#B78D98"}},
        "transparency": 70 if dark else 80,
        "shadowSpread": 0,
        "shadowBlur": 14,
        "angle": 90,
        "shadowDistance": 4,
    }


def shadow_properties(dark=False):
    result = {}
    for key, value in shadow_style(dark).items():
        result[key] = (
            fill(value["solid"]["color"])
            if isinstance(value, dict)
            else lit(
                str(value).lower()
                if isinstance(value, bool)
                else str(value) + "D"
                if isinstance(value, (int, float))
                else "'" + value + "'"
            )
        )
    return props(**result)


def native_panel(page_id, rectangle, dark=False, color=None):
    """A separate editable rounded panel below data/text, never a page skin."""
    x, y, width, height = rectangle
    name = hashlib.sha256(
        ("soft-panel:" + page_id + repr(tuple(float(v) for v in rectangle))).encode()
    ).hexdigest()[:20]
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": name,
        "position": {"x": x, "y": y, "width": width, "height": height, "z": 0, "tabOrder": 60000},
        "visual": {
            "visualType": "shape",
            "drillFilterOtherVisuals": True,
            "visualContainerObjects": {
                **{
                    key: props(show=lit("false"))
                    for key in (
                        "background",
                        "border",
                        "dropShadow",
                        "title",
                        "subTitle",
                        "visualHeader",
                    )
                },
                "padding": props(**{key: lit("0D") for key in ("top", "bottom", "left", "right")}),
                "general": props(altText=lit("'Decorative native soft-glow panel'")),
            },
            "objects": {
                "shape": props(tileShape=lit("'rectangle'"), roundEdge=lit("18L")),
                "fill": [
                    {"properties": {"show": lit("true")}},
                    {
                        "selector": {"id": "default"},
                        "properties": {
                            "fillColor": fill(color or ("#1B241E" if dark else "#FFFFFF")),
                            "transparency": lit("0D"),
                        },
                    },
                ],
                "outline": props(show=lit("false")),
                "text": props(show=lit("false")),
                "glow": props(show=lit("false")),
                "shadow": [
                    {"properties": {"show": lit("true")}},
                    {
                        "selector": {"id": "default"},
                        "properties": {
                            "color": fill("#000000" if dark else "#B78D98"),
                            "transparency": lit("70D" if dark else "80D"),
                            "shadowBlur": lit("14D"),
                            "shadowPositionPreset": lit("'custom'"),
                            "angle": lit("90D"),
                            "shadowDistance": lit("4D"),
                        },
                    },
                ],
            },
        },
    }


def apply_theme_glow(theme):
    styles = theme["visualStyles"]
    for kind in DATA_KINDS:
        style = styles.setdefault(kind, {}).setdefault("*", {})
        style["dropShadow"] = [shadow_style()]
        styles[kind]["WMPP Soft Glow"] = {
            "dropShadow": [shadow_style()],
            "background": [
                {"show": True, "color": {"solid": {"color": "#FFFFFF"}}, "transparency": 0}
            ],
            "border": [
                {"show": True, "radius": 14, "width": 1, "color": {"solid": {"color": "#FFFFFF"}}}
            ],
        }
        style["border"] = deepcopy(styles[kind]["WMPP Soft Glow"]["border"])
        if kind in CHART_KINDS:
            for preset in styles[kind].values():
                preset["padding"] = [dict(CHART_PADDING)]
    # Labels, icons and controls never acquire their own floating shadow.
    for kind in ("textbox", "image", "actionButton", "slicer"):
        styles.setdefault(kind, {}).setdefault("*", {})["dropShadow"] = [{"show": False}]
    panel = native_panel("template", (0, 0, 100, 100))["visual"]["objects"]

    def unwrap(value):
        if isinstance(value, dict):
            if set(value) == {"expr"} and "Literal" in value["expr"]:
                raw = value["expr"]["Literal"]["Value"]
                if raw in ("true", "false"):
                    return raw == "true"
                if raw.endswith(("D", "L")):
                    return float(raw[:-1])
                return raw.strip("'")
            return {k: unwrap(v) for k, v in value.items()}
        if isinstance(value, list):
            return [unwrap(v) for v in value]
        return value

    preset = {}
    for key, blocks in panel.items():
        preset[key] = []
        for block in blocks:
            item = unwrap(block["properties"])
            if "selector" in block:
                item["$id"] = block["selector"]["id"]
            preset[key].append(item)
    preset.update(
        {key: [{"show": False}] for key in ("background", "border", "dropShadow", "title")}
    )
    styles.setdefault("shape", {})["WMPP Soft Panel"] = preset


def apply_report_glow(report):
    counts = {"panels": 0, "standalone_visuals": 0}
    for pagefile in report.glob("definition/pages/*/page.json"):
        page = read(pagefile)
        if page["displayName"].endswith(" - guide") or page.get("height", 0) < 400:
            continue
        page_id = page["name"]
        dark = "#101713" in json.dumps(page.get("objects", {}).get("background", []))
        visuals = [(path, read(path)) for path in pagefile.parent.glob("visuals/*/visual.json")]
        rectangles = list(REFERENCE.get(page_id, GENERATED.get(page_id, [])))
        if page_id in GENERATED:
            for _, value in visuals:
                p = value["position"]
                if value["visual"]["visualType"] == "cardVisual" and p["height"] == 50:
                    rectangles.append((p["x"] - 17, p["y"] - 48, p["width"] + 36, 146))
        for rectangle in rectangles:
            panel = native_panel(page_id, rectangle, dark)
            save(pagefile.parent / "visuals" / panel["name"] / "visual.json", panel)
            counts["panels"] += 1
        for path, value in visuals:
            visual, position = value["visual"], value["position"]
            if visual["visualType"] not in DATA_KINDS and not visual["visualType"].startswith(
                "deneb"
            ):
                continue
            if position["width"] < 100 or position["height"] < 70:
                continue  # Tiny KPI IDs, refresh stamps and compact calls stay transparent.
            containers = visual.setdefault("visualContainerObjects", {})
            covered = any(
                position["x"] >= x - 2
                and position["y"] >= y - 2
                and position["x"] + position["width"] <= x + w + 2
                and position["y"] + position["height"] <= y + h + 2
                for x, y, w, h in rectangles
            )
            if covered:
                containers["dropShadow"] = props(show=lit("false"))
                containers["background"] = props(show=lit("false"))
            else:
                containers["dropShadow"] = shadow_properties(dark)
                containers["background"] = props(
                    show=lit("true"),
                    color=fill("#1B241E" if dark else "#FFFFFF"),
                    transparency=lit("0D"),
                )
                containers["border"] = props(
                    show=lit("true"),
                    radius=lit("14D"),
                    width=lit("1D"),
                    color=fill("#1B241E" if dark else "#FFFFFF"),
                )
                if visual["visualType"] in CHART_KINDS:
                    containers["padding"] = props(
                        **{key: lit(str(pixels) + "D") for key, pixels in CHART_PADDING.items()}
                    )
                counts["standalone_visuals"] += 1
            save(path, value)
    return counts


def main():
    reports = list(BUNDLE.glob("*/*.Report"))
    backup = BUNDLE / "_review" / ("soft-glow-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True)
    models = {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for m in BUNDLE.glob("*/*.SemanticModel")
        for p in m.rglob("*")
        if p.is_file()
    }
    theme_paths = [
        ROOT / "assets/brand-pack/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
    ] + [r / "StaticResources/RegisteredResources/WMPP_Theme.json" for r in reports]
    for i, path in enumerate(theme_paths):
        shutil.copy2(path, backup / f"theme-{i}.json")
        theme = read(path)
        apply_theme_glow(theme)
        save(path, theme)
    summary = {}
    for report in reports:
        shutil.copytree(report / "definition", backup / report.name)
        summary[report.name] = apply_report_glow(report)
        # Confirm semantic bindings and interactions have not moved with the styling.
        for old in (backup / report.name).rglob("*.json"):
            current = read(report / "definition" / old.relative_to(backup / report.name))
            before = read(old)
            if old.name == "visual.json":
                expected = deepcopy(before)
                expected["visual"]["visualContainerObjects"] = current["visual"].get(
                    "visualContainerObjects", {}
                )
                assert expected == current, old
            else:
                assert before == current, old
    assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in models.items())
    save(
        backup / "verification.json",
        {"reports": summary, "models_unchanged": True, "desktop_render_verified": False},
    )
    print(json.dumps({"backup": str(backup), "reports": summary}, indent=2))


if __name__ == "__main__":
    main()
