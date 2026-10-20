"""Restrict authored WMPP colours to the approved palette, preserving layout/data."""

from copy import deepcopy
from datetime import datetime
import colorsys
import hashlib
import json
import re
import shutil
import sys

from build_report_design_delivery import fill, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT

BRAND = ROOT / "assets/brand-pack"
PALETTE = read(BRAND / "WMPP_Palette.json")
ALLOWED = set(PALETTE["colours"].values())
HEX = re.compile(r"#[0-9a-fA-F]{8}\b|#[0-9a-fA-F]{6}\b|#[0-9a-fA-F]{3}\b")
EXPLICIT = {
    "#1D1D1B": "#2B2B2C",
    "#2B2427": "#2B2B2C",
    "#000000": "#2B2B2C",
    "#61575C": "#625B5B",
    "#575756": "#625B5B",
    "#756A70": "#625B5B",
    "#B78D98": "#C78E7A",
    "#E96B7D": "#FB6540",
    "#D94D2B": "#EF7911",
    "#A86612": "#E69512",
    "#C13F35": "#C0392B",
    "#F34E43": "#C0392B",
    "#C84758": "#C0392B",
    "#FF8C42": "#EF7911",
    "#FFB51B": "#E69512",
    "#FFB20C": "#E69512",
    "#F8B421": "#E69512",
    "#F59E00": "#E69512",
    "#FFAD45": "#E69512",
    "#E0603F": "#FB6540",
    "#3DAFA5": "#4DAAAB",
    "#72AEB5": "#4DAAAB",
    "#78B8C0": "#4DAAAB",
    "#3A9E75": "#277455",
    "#438B70": "#277455",
    "#3A8B6F": "#277455",
    "#FFE7DF": "#FEE1DD",
    "#F8F1F4": "#F8F5F1",
    "#FFF9FB": "#F8F5F1",
    "#FFF9F7": "#F8F5F1",
    "#FFF1EC": "#FEE1DD",
    "#FFDAD4": "#FEE1DD",
    "#FFD8D1": "#FEE1DD",
    "#FFD8C7": "#FEE1DD",
    "#EEDCE3": "#E3DADA",
    "#FFF6D8": "#FFF1D6",
    "#FFF5C7": "#FFF1D6",
    "#FFEBBC": "#FFF1D6",
    "#FADCE4": "#FEE1DD",
    "#FDF0EB": "#F8F5F1",
    "#F0D9D1": "#E3DADA",
    "#E1F0E9": "#E4F1E9",
    "#FBE7DF": "#FEE1DD",
    "#C84E2E": "#EF7911",
}


def rgb(colour):
    return tuple(int(colour[i : i + 2], 16) for i in (1, 3, 5))


def mapped(colour):
    colour = colour.upper()
    if len(colour) == 4:
        colour = "#" + "".join(c * 2 for c in colour[1:])
    if len(colour) == 9:
        colour = colour[:7]
    if colour in ALLOWED:
        return colour
    if colour in EXPLICIT:
        return EXPLICIT[colour]
    r, g, b = rgb(colour)
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if s < 0.16:
        if v < 0.32:
            return "#2B2B2C"
        if v < 0.68:
            return "#625B5B"
        if v < 0.9:
            return "#E3DADA"
        return "#F0EBE7" if v < 0.97 else "#FFFFFF"
    return min(ALLOWED, key=lambda c: sum((a - b) ** 2 for a, b in zip(rgb(colour), rgb(c))))


def colour_text(text):
    text = HEX.sub(lambda m: mapped(m.group()), text)

    def replace_rgb(m):
        colour = "#" + "".join(f"{min(255, max(0, round(float(v)))):02X}" for v in m.group(2, 3, 4))
        components = rgb(mapped(colour))
        alpha = m.group(5)
        return (
            ("rgba(" + ",".join(map(str, components)) + "," + alpha + ")")
            if alpha is not None
            else "rgb(" + ",".join(map(str, components)) + ")"
        )

    return re.sub(
        r"\b(rgb|rgba)\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)",
        replace_rgb,
        text,
    )


def transform(value, data_colours):
    if isinstance(value, str):
        return colour_text(value)
    if isinstance(value, list):
        return [transform(v, data_colours) for v in value]
    if isinstance(value, dict):
        if set(value) == {"ThemeDataColor"}:
            index = value["ThemeDataColor"]["ColorId"]
            # No implicit tint/shade arithmetic: use a declared palette colour.
            return {"Literal": {"Value": repr(data_colours[index % len(data_colours)])}}
        if set(value) == {"FillRule"}:
            rule = value["FillRule"].get("FillRule", {})
            for key in ("linearGradient2", "linearGradient3"):
                if key in rule:
                    endpoint = rule[key].get("max", {}).get("color", {})
                    return (
                        transform(endpoint, data_colours)
                        if endpoint
                        else {"Literal": {"Value": "'#FB6540'"}}
                    )
        return {k: transform(v, data_colours) for k, v in value.items()}
    return value


def category_colour(label):
    label = label.strip("'").casefold().replace("_", " ")
    if label in {"residential"}:
        return "#4DAAAB"
    if label in {"supported accommodation"}:
        return "#FB6540"
    if label in {"fostering", "standard foster"}:
        return "#2B2B2C"
    if label in {"critical", "overdue", "failed", "failure", "error", "high"}:
        return "#C0392B"
    if label in {"due soon", "pending", "warning", "medium"}:
        return "#E69512"
    if label in {
        "on track",
        "success",
        "successful",
        "complete",
        "completed",
        "implemented",
        "ready",
    }:
        return "#277455"
    if label in {"planned", "low"}:
        return "#FEE1DD"
    return None


def normalise_theme(value):
    """Theme colour fields use strings, unlike PBIR visual expression literals."""
    if isinstance(value, dict):
        literal = value.get("expr", {}).get("Literal", {}).get("Value")
        if set(value) == {"expr"} and isinstance(literal, str) and literal.strip("'") in ALLOWED:
            return literal.strip("'")
        return {k: normalise_theme(v) for k, v in value.items()}
    if isinstance(value, list):
        return [normalise_theme(v) for v in value]
    return value


def finish_themes():
    backup = (
        BUNDLE
        / "_review"
        / ("palette-theme-normalisation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    paths = [
        BRAND / "WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
    ]
    paths += list((REPORT / "StaticResources").rglob("*.json"))
    for p in paths:
        theme = read(p)
        if "dataColors" not in theme:
            continue
        sequence = PALETTE["categorical"]
        colours = [sequence[i % len(sequence)] for i in range(len(theme["dataColors"]))]
        new = normalise_theme(transform(theme, colours))
        new["dataColors"] = colours
        new.update(good="#277455", neutral="#E69512", bad="#C0392B", tableAccent="#EF7911")
        target = backup / p.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
        save(p, new)
    for p in [BRAND / "icons/LUCIDE_KPI_SOURCES.json", REPORT.parent / "LUCIDE_KPI_SOURCES.json"]:
        audit = read(p)
        for asset in audit["assets"]:
            asset["variant_sha256"] = hashlib.sha256(
                (BRAND / "icons" / asset["file"]).read_bytes()
            ).hexdigest()
        save(p, audit)
    print(json.dumps({"theme_paths_processed": len(paths), "backup": str(backup)}))


def main():
    backup = BUNDLE / "_review" / ("approved-palette-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    plan = {}
    changes = {}
    protected = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file()
    }
    protected[BRAND / "WMPP_Theme_v0.json"] = hashlib.sha256(
        (BRAND / "WMPP_Theme_v0.json").read_bytes()
    ).hexdigest()
    master = read(BRAND / "WMPP_Theme.json")
    # Retain index count and first-three meanings used by existing visuals.
    sequence = PALETTE["categorical"]
    colours = [sequence[i % len(sequence)] for i in range(len(master["dataColors"]))]
    themes = [
        BRAND / "WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        REPORT / "StaticResources/RegisteredResources/WMPP_Theme.json",
    ]
    themes += list((REPORT / "StaticResources/SharedResources").rglob("*.json"))
    for p in themes:
        d = transform(read(p), colours)
        d["dataColors"] = colours
        if p in themes[:4]:
            d["name"] = "WMPP — approved 24-colour palette"
        d.update(
            tableAccent="#EF7911",
            good="#277455",
            neutral="#E69512",
            bad="#C0392B",
            maximum="#277455",
            center="#FEE1DD",
            minimum="#C0392B",
            null="#E3DADA",
        )
        plan[p] = d
    definitions = list((REPORT / "definition").rglob("*.json"))
    for p in definitions:
        old = read(p)
        new = transform(old, colours)
        v = new.get("visual", {})
        for entry in v.get("objects", {}).get("dataPoint", []):
            labels = []

            def scope(o):
                if isinstance(o, dict):
                    if "Comparison" in o:
                        labels.append(
                            o["Comparison"].get("Right", {}).get("Literal", {}).get("Value", "")
                        )
                    for x in o.values():
                        scope(x)
                elif isinstance(o, list):
                    for x in o:
                        scope(x)

            scope(entry.get("selector", {}))
            chosen = next((category_colour(s) for s in labels if category_colour(s)), None)
            if chosen:
                entry.setdefault("properties", {})["fill"] = fill(chosen)
        # Explicitly fix placement-type categories in every donut, not only the pictured one.
        if v.get("visualType") == "donutChart":
            categories = (
                v.get("query", {}).get("queryState", {}).get("Category", {}).get("projections", [])
            )
            if (
                categories
                and categories[0].get("field", {}).get("Column", {}).get("Property")
                == "placement_type"
            ):
                column = categories[0]["field"]
                points = v.setdefault("objects", {}).setdefault("dataPoint", [])
                for label, colour in PALETTE["placementTypes"].items():
                    points.append(
                        {
                            "selector": {
                                "data": [
                                    {
                                        "scopeId": {
                                            "Comparison": {
                                                "ComparisonKind": 0,
                                                "Left": deepcopy(column),
                                                "Right": {"Literal": {"Value": repr(label)}},
                                            }
                                        }
                                    }
                                ]
                            },
                            "properties": {"fill": fill(colour)},
                        }
                    )
        if old != new:
            if "visual" in old:
                assert old["visual"].get("query") == new["visual"].get("query")
                assert old.get("filterConfig") == new.get("filterConfig")
                assert old["position"] == new["position"]
                assert old["visual"].get("visualContainerObjects", {}).get("visualLink") == v.get(
                    "visualContainerObjects", {}
                ).get("visualLink")
            plan[p] = new
    # SVG source variants, not raster logo/media or unmodified upstream originals.
    svgs = (
        list((REPORT / "StaticResources/RegisteredResources").glob("*.svg"))
        + list((BRAND / "icons").glob("*.svg"))
        + list(REPORT.parent.glob("*.svg"))
    )
    for p in svgs:
        old = p.read_text(encoding="utf-8-sig")
        new = colour_text(old)
        for token, colour in [
            ("black", "#2B2B2C"),
            ("white", "#FFFFFF"),
            ("red", "#C0392B"),
            ("orange", "#EF7911"),
            ("yellow", "#FFE672"),
            ("green", "#277455"),
        ]:
            new = re.sub(
                r'(\b(?:fill|stroke|stop-color)=["\'])' + token + r'(["\'])',
                lambda m: m.group(1) + colour + m.group(2),
                new,
                flags=re.I,
            )
        if old != new:
            plan[p] = new
    # Keep active design tokens/components in sync; archives retain historical evidence.
    for p in (BRAND / "design-system").glob("*.css"):
        old = p.read_text(encoding="utf-8-sig")
        new = colour_text(old)
        if p.name == "tokens.css":
            overrides = {
                "bg-canvas": "#F8F5F1",
                "bg-canvas-soft": "#F0EBE7",
                "bg-card-hover": "#F0EBE7",
                "coral": "#FB6540",
                "coral-deep": "#EF7911",
                "coral-mid": "#F98165",
                "coral-soft": "#FFB39F",
                "coral-tint": "#FEE1DD",
                "coral-faint": "#FEE1DD",
                "teal": "#4DAAAB",
                "teal-deep": "#287C73",
                "teal-soft": "#E3DADA",
                "teal-tint": "#F0EBE7",
                "good": "#277455",
                "good-tint": "#E4F1E9",
                "warn": "#E69512",
                "warn-tint": "#FFF1D6",
                "bad": "#C0392B",
                "bad-tint": "#FBE7E4",
            }
            for key, value in overrides.items():
                new = re.sub(r"(--" + key + r":\s*)#[0-9A-F]{6}", lambda m: m.group(1) + value, new)
        plan[p] = new
    # Audit records are updated without changing source hashes or upstream originals.
    for p in [BRAND / "icons/LUCIDE_KPI_SOURCES.json", REPORT.parent / "LUCIDE_KPI_SOURCES.json"]:
        d = read(p)
        for a in d["assets"]:
            a["colour"] = mapped(a["colour"])
            asset = BRAND / "icons" / a["file"]
            content = plan.get(asset, asset.read_text(encoding="utf-8-sig"))
            a["variant_sha256"] = hashlib.sha256(content.encode("utf-8")).hexdigest()
        for m in d["visual_mapping"]:
            m["colour"] = mapped(m["colour"])
        d["palette_version"] = PALETTE["version"]
        d["filename_note"] = (
            "Filename colour suffixes are stable identifiers; use colour and hash fields for current values."
        )
        plan[p] = d
    for p, new in plan.items():
        if p.exists():
            target = backup / p.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, target)
        if isinstance(new, str):
            p.write_text(new, encoding="utf-8")
        else:
            save(p, new)
        changes[str(p.relative_to(ROOT))] = True
    # Exhaustive authored-literal check; referenced raster imagery is separately disclosed.
    violations = []
    for p in definitions + themes + svgs + list((BRAND / "design-system").glob("*.css")):
        literals = {m.group().upper() for m in HEX.finditer(p.read_text(encoding="utf-8-sig"))}
        outside = literals - ALLOWED
        if outside:
            violations.append({"file": str(p), "colours": sorted(outside)})
    assert not violations, violations
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = {
        "palette_colours": len(ALLOWED),
        "files_changed": len(plan),
        "outside_palette_authored_hex_literals": violations,
        "layout_queries_filters_actions_models_and_v0_preserved": True,
        "native_render_verified": False,
        "scope": "WMPP delivery and active brand assets; original client raster/logo imagery, upstream originals, historical mockups and Mission Control excluded",
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    save(backup / "changed_files.json", list(changes))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if "--finish-themes" in sys.argv:
        finish_themes()
    else:
        main()
