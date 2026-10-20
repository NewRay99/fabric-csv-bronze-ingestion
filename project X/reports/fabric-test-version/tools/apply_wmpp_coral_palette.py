"""Apply the user-approved coral navigation accent without changing layout/data."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil

from build_report_design_delivery import fill, ident, read, save
from connect_wmpp_report_pages import BUNDLE, GROUPS, REPORT, ROOT
from use_wmpp_dropdown_navigation import PAGES, POPOVERS, TOP, button

COLOURS = {
    "#A33B61": "#FB6540",
    "#FBE2EB": "#FFE7DF",
    "#74334C": "#1D1D1B",
    "#EEDCE3": "#FFE7DF",
    "#E96B7D": "#FB6540",
    "#FCE8ED": "#FFE7DF",
    "#F092A5": "#FF8C42",
    "#F7BDC9": "#FFD8D1",
    "#F2ECEF": "#EEE8E2",
    "#DDD3D8": "#D8D0C8",
    "#C84758": "#F34E43",
    "#C9BEC3": "#D8D0C8",
}


def recolour(value):
    if isinstance(value, str):
        if value.upper() in COLOURS:
            return COLOURS[value.upper()]
        if value.startswith("'") and value.endswith("'") and value[1:-1].upper() in COLOURS:
            return "'" + COLOURS[value[1:-1].upper()] + "'"
        return value
    if isinstance(value, list):
        return [recolour(v) for v in value]
    if isinstance(value, dict):
        return {k: recolour(v) for k, v in value.items()}
    return value


def theme_update(value):
    theme = deepcopy(value)
    theme["name"] = "WMPP — Coral and warm neutrals"
    # Preserve indices and length: original presets refer to ThemeDataColor IDs.
    theme["dataColors"] = recolour(theme["dataColors"])
    theme["dataColors"][:8] = [
        "#FB6540",
        "#2B2427",
        "#3DAFA5",
        "#FF8C42",
        "#FFD8D1",
        "#FCBF00",
        "#287C73",
        "#F34E43",
    ]
    theme.update(
        tableAccent="#FB6540",
        good="#3DAFA5",
        neutral="#FFB20C",
        bad="#F34E43",
        maximum="#3DAFA5",
        center="#FFD8D1",
        minimum="#F34E43",
    )
    for name, preset in theme["visualStyles"].get("actionButton", {}).items():
        # Keep preset typography/shape/layout, but replace all button colour states.
        updated = recolour(preset)
        for key, field in [
            ("fill", "fillColor"),
            ("text", "fontColor"),
            ("icon", "lineColor"),
            ("outline", "lineColor"),
            ("shadow", "color"),
            ("glow", "color"),
        ]:
            for item in updated.get(key, []):
                if field not in item:
                    continue
                state = item.get("$id", "default")
                colour = (
                    (
                        "#FB6540"
                        if state in ("default", "selected")
                        else "#F98165"
                        if state == "hover"
                        else "#EEE8E2"
                    )
                    if key == "fill"
                    else (
                        "#1D1D1B"
                        if key in ("text", "icon")
                        else "#9F341F"
                        if key == "outline"
                        else "#C78E7A"
                    )
                )
                item[field] = {"solid": {"color": colour}}
        theme["visualStyles"]["actionButton"][name] = updated
    return theme


def main():
    backup = BUNDLE / "_review" / ("coral-palette-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    themes = [
        ROOT / "assets/brand-pack/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        REPORT / "StaticResources/RegisteredResources/WMPP_Theme.json",
    ]
    protected = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file()
    }
    v0 = ROOT / "assets/brand-pack/WMPP_Theme_v0.json"
    protected[v0] = hashlib.sha256(v0.read_bytes()).hexdigest()
    for path in themes:
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        save(path, theme_update(read(path)))
    count = 0
    main_ids = {
        ident(f"wmpp-dropdown:{pid}:main-{short}"): (pid, short, area)
        for pid in PAGES
        for short, _, area in TOP
    }
    child_ids = {
        ident(f"wmpp-dropdown:{pid}:child:{area}:{n}")
        for pid in PAGES
        for area, children in POPOVERS.items()
        for n in range(len(children) + 1)
    }
    for path in REPORT.glob("definition/pages/*/visuals/*/visual.json"):
        old = read(path)
        if old.get("visual", {}).get("visualType") != "actionButton":
            continue
        new = recolour(old)
        if old["name"] in main_ids:
            pid, short, area = main_ids[old["name"]]
            group = next(g for g, items in GROUPS if any(p == pid for _, p in items))
            active = (
                pid == "ad5ab4aa6928c9178a35"
                if area is None
                else (group == area and pid != "ad5ab4aa6928c9178a35")
            )
            style = button(
                pid, "unused", short, (0, 0, 66, 66), "unused", active=active, circle=True
            )
            for key in ("fill", "text", "outline"):
                if key == "text" and any(
                    "image" in entry.get("properties", {})
                    for entry in old["visual"]["objects"].get("icon", [])
                ):
                    continue  # Preserve the later Lucide icon-only navigation.
                new["visual"]["objects"][key] = style["visual"]["objects"][key]
        elif old["name"] in child_ids:
            # White text on the new coral is too weak for small submenu labels.
            objects = new["visual"].get("objects", {})
            for entry in objects.get("text", []):
                if "fontColor" in entry.get("properties", {}):
                    entry["properties"]["fontColor"] = fill("#1D1D1B")
        if new != old:
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            save(path, new)
            assert new["position"] == old["position"]
            assert new["visual"].get("query") == old["visual"].get("query")
            assert new.get("filterConfig") == old.get("filterConfig")
            assert new["visual"].get("objects", {}).get("shape") == old["visual"].get(
                "objects", {}
            ).get("shape")
            assert new["visual"]["visualContainerObjects"].get("visualLink") == old["visual"][
                "visualContainerObjects"
            ].get("visualLink")
            count += 1
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = {
        "button_visuals_updated": count,
        "main_buttons": len(main_ids),
        "themes_updated": len(themes),
        "geometry_actions_models_and_v0_preserved": True,
        "native_render_verified": False,
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
