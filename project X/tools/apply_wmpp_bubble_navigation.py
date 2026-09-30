"""Apply the approved horizontal bubble menu to the local WMPP delivery only.

Native button fill-image states provide the expansion effect. No animated GIF,
custom visual, external asset request, model change or dataset refresh is used.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET

from apply_report_soft_glow import native_panel
from apply_wmpp_navigation_icons import ICONS
from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, GROUPS, REPORT, ROOT
from use_wmpp_dropdown_navigation import PAGES, POPOVERS, TOP

BRAND = ROOT / "assets/brand-pack"
ASSETS = BRAND / "icons/navigation-bubbles"
RESOURCES = REPORT / "StaticResources/RegisteredResources"
PALETTE = read(BRAND / "WMPP_Palette.json")["colours"]
STATES = ("default", "hover", "selected", "disabled")
PRESET = "WMPP Bubble Navigation"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def svg_asset(short, state):
    """Only the bubble silhouette changes; Lucide path geometry is preserved."""
    source = ET.fromstring(
        (BRAND / "icons" / f"lucide-nav-{ICONS[short][1]}-white.svg").read_text()
    )
    ET.register_namespace("", "http://www.w3.org/2000/svg")
    children = "".join(ET.tostring(child, encoding="unicode") for child in source)
    coral = PALETTE["navigationCoral"]
    backdrop = ""
    if state in ("active", "hover"):
        colour = PALETTE["blushPeach" if state == "active" else "hoverCoral"]
        backdrop = f'<rect x="1" y="3" width="70" height="92" rx="35" fill="{colour}"/>'
    if state == "disabled":
        coral = PALETTE["stone"]
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="72" height="96" viewBox="0 0 72 96">'
        f'{backdrop}<circle cx="36" cy="33" r="27" fill="{coral}"/>'
        '<g transform="translate(22 19) scale(1.166666667)" fill="none" '
        f'stroke="{PALETTE["surface"]}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{children}</g></svg>\n'
    )


def resource_image(filename):
    return {
        "image": {
            "name": L(quoted(filename)),
            "scaling": L("'Fit'"),
            "url": {
                "expr": {
                    "ResourcePackageItem": {
                        "PackageName": "RegisteredResources",
                        "PackageType": 1,
                        "ItemName": filename,
                    }
                }
            },
        }
    }


def main():
    marker = REPORT.parent / "BUBBLE_NAVIGATION.json"
    assert not marker.exists(), "Bubble navigation already applied; inspect before revising"
    backup = BUNDLE / "_review" / ("bubble-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    originals = {p: digest(p) for p in (REPORT / "definition").rglob("*.json")}
    protected = {
        p: digest(p)
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file() and ".pbi" not in p.parts
    }
    protected[BRAND / "WMPP_Theme_v0.json"] = digest(BRAND / "WMPP_Theme_v0.json")
    touched = set()
    planned = {}

    def retain(path):
        if path in touched:
            return
        if path.exists():
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        touched.add(path)

    def write(path, value):
        retain(path)
        save(path, value)

    assets = {}
    for short, _, _ in TOP:
        for state in ("default", "active", "hover", "disabled"):
            filename = f"wmpp-bubble-{short.lower()}-{state}.svg"
            assets[filename] = svg_asset(short, state)
    allowed = set(PALETTE.values())
    assert all(set(re.findall(r"#[0-9A-Fa-f]{6}", s)) <= allowed for s in assets.values())

    for pid in sorted(PAGES):
        folder = REPORT / "definition/pages" / pid
        page = read(folder / "page.json")
        group = next(g for g, members in GROUPS if any(p == pid for _, p in members))
        menu = []
        for i, (short, label, area) in enumerate(TOP):
            path = folder / "visuals" / ident(f"wmpp-dropdown:{pid}:main-{short}") / "visual.json"
            old = read(path)
            d = deepcopy(old)
            active = (
                pid == "ad5ab4aa6928c9178a35"
                if area is None
                else (group == area and pid != "ad5ab4aa6928c9178a35")
            )
            d["position"].update(width=72, height=96, z=100010, tabOrder=i)
            o = d["visual"]["objects"]
            # The outer hit target stays fixed. Transparent SVG regions expose the
            # shared rail; hover expands downward inside this reserved menu slot.
            o["shape"] = obj(tileShape=L("'rectangle'"), roundEdge=L("0L")) + [
                {
                    "selector": {"id": s},
                    "properties": {
                        "tileShape": L("'rectangle'"),
                        "roundEdge": L("0L"),
                    },
                }
                for s in STATES
            ]
            o["fill"] = obj(show=L("true")) + [
                {
                    "selector": {"id": s},
                    "properties": {
                        "show": L("true"),
                        "fillColor": fill(PALETTE["surface"]),
                        "transparency": L("100D"),
                        "image": resource_image(
                            f"wmpp-bubble-{short.lower()}-"
                            + (
                                "hover"
                                if s == "hover"
                                else "disabled"
                                if s == "disabled"
                                else "active"
                                if active or s == "selected"
                                else "default"
                            )
                            + ".svg"
                        ),
                    },
                }
                for s in STATES
            ]
            for key in ("icon", "outline", "shadow", "glow"):
                o[key] = obj(show=L("false")) + [
                    {"selector": {"id": s}, "properties": {"show": L("false")}} for s in STATES
                ]
            # Labels are real text, not raster/SVG text, and remain visible on touch.
            label_text = label + (" ▾" if area in POPOVERS else "")
            o["text"] = obj(show=L("true")) + [
                {
                    "selector": {"id": s},
                    "properties": {
                        "show": L("true"),
                        "text": L(quoted(label_text)),
                        "fontFamily": L("'Segoe UI'"),
                        "fontSize": L("8D" if short in ("PF", "RM") else "9D"),
                        "fontColor": fill(PALETTE["text"]),
                        "bold": L(str(active).lower()),
                        "horizontalAlignment": L("'center'"),
                        "verticalAlignment": L("'middle'"),
                        "leftMargin": L("0L"),
                        "rightMargin": L("0L"),
                        "topMargin": L("62L"),
                        "bottomMargin": L("6L"),
                    },
                }
                for s in STATES
            ]
            c = d["visual"]["visualContainerObjects"]
            c["stylePreset"] = obj(name=L(quoted(PRESET)))
            c["general"] = obj(
                altText=L(
                    quoted(
                        ("Current section: " if active else "Navigation: ")
                        + label
                        + ("; opens subpage menu" if area in POPOVERS else "")
                    )
                )
            )
            assert c["visualLink"] == old["visual"]["visualContainerObjects"]["visualLink"]
            p = d["position"]
            assert 0 <= p["x"] and p["x"] + p["width"] <= page["width"]
            assert p["y"] + p["height"] <= (132 if p["y"] == 34 else 104)
            menu.append(d)
            planned[path] = d
            caption_path = (
                folder
                / "visuals"
                / ident(f"board-annotation:dropdown:{pid}:caption:{short}")
                / "visual.json"
            )
            caption = read(caption_path)
            caption["isHidden"] = True
            planned[caption_path] = caption

        first, last = menu[0]["position"], menu[-1]["position"]
        assert all(a["position"]["x"] + 72 <= b["position"]["x"] for a, b in zip(menu, menu[1:]))
        rail = native_panel(
            pid,
            (first["x"] + 3, first["y"] + 4, last["x"] + 69 - first["x"] - 3, 58),
            color=PALETTE["navigationCoral"],
        )
        rail["name"] = ident(f"wmpp-bubble-rail:{pid}")
        rail["position"].update(z=100003)
        rail["visual"]["objects"]["shape"] = obj(tileShape=L("'rectangle'"), roundEdge=L("29L"))
        for entry in rail["visual"]["objects"]["shadow"]:
            props = entry["properties"]
            if "color" in props:
                props.update(
                    color=fill(PALETTE["shadow"]),
                    shadowBlur=L("12D"),
                    transparency=L("78D"),
                    shadowDistance=L("4D"),
                )
        rail["visual"]["visualContainerObjects"]["general"] = obj(
            altText=L("'Horizontal WMPP navigation rail'")
        )
        planned[folder / "visuals" / rail["name"] / "visual.json"] = rail

        # Keep dropdown content below expanded bubbles; actions and visibility
        # bookmark membership stay unchanged, including the white connected frame.
        for area, members in POPOVERS.items():
            first_path = (
                folder / "visuals" / ident(f"wmpp-dropdown:{pid}:child:{area}:0") / "visual.json"
            )
            first_child = read(first_path)
            shift = max(0, first["y"] + 112 - first_child["position"]["y"])
            for n in range(len(members) + 1):
                child_path = (
                    folder
                    / "visuals"
                    / ident(f"wmpp-dropdown:{pid}:child:{area}:{n}")
                    / "visual.json"
                )
                child = read(child_path)
                child["position"]["y"] += shift
                planned[child_path] = child
            for part in ("panel", "neck", "cap"):
                frame_path = (
                    folder
                    / "visuals"
                    / ident(f"wmpp-dropdown-frame:{pid}:{area}:{part}")
                    / "visual.json"
                )
                frame = read(frame_path)
                if part == "panel":
                    frame["position"]["y"] += shift
                elif part == "neck":
                    frame["position"]["height"] += shift
                assert frame["position"]["y"] + frame["position"]["height"] <= page["height"]
                planned[frame_path] = frame

    # Stage all changes in memory before writing; retain every replaced file.
    for path, d in planned.items():
        write(path, d)
    for name, svg in assets.items():
        for path in (ASSETS / name, RESOURCES / name):
            retain(path)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(svg, encoding="utf-8")
    report_path = REPORT / "definition/report.json"
    report = read(report_path)
    package = next(p for p in report["resourcePackages"] if p["name"] == "RegisteredResources")
    for name in assets:
        assert not any(item["name"] == name for item in package["items"])
        package["items"].append({"name": name, "path": name, "type": "Image"})
    write(report_path, report)

    theme_paths = [
        BRAND / "WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        RESOURCES / "WMPP_Theme.json",
    ]
    for path in theme_paths:
        theme = read(path)
        theme["visualStyles"].setdefault("actionButton", {})[PRESET] = {
            "shape": [{"tileShape": "rectangle", "roundEdge": 0}],
            "fill": [
                {
                    "show": True,
                    "fillColor": {"solid": {"color": PALETTE["surface"]}},
                    "transparency": 100,
                }
            ],
            **{key: [{"show": False}] for key in ("icon", "outline", "shadow", "glow")},
            "text": [
                {
                    "show": True,
                    "fontFamily": "Segoe UI",
                    "fontSize": 9,
                    "fontColor": {"solid": {"color": PALETTE["text"]}},
                    "horizontalAlignment": "center",
                    "verticalAlignment": "middle",
                    "topMargin": 62,
                    "bottomMargin": 6,
                    "leftMargin": 0,
                    "rightMargin": 0,
                }
            ],
        }
        write(path, theme)

    assert all(digest(p) == h for p, h in originals.items() if p not in touched)
    assert all(digest(p) == h for p, h in protected.items())
    for p in touched:
        if p.suffix.lower() in (".json", ".svg"):
            assert (
                set(re.findall(r"#[0-9a-fA-F]{6}", p.read_text(encoding="utf-8-sig"))) <= allowed
            ), p
    result = {
        "pages": len(PAGES),
        "buttons": len(PAGES) * len(TOP),
        "shared_rails": len(PAGES),
        "embedded_state_assets": len(assets),
        "backup": str(backup),
        "actions_bookmarks_models_and_non_navigation_visuals_unchanged": True,
        "current_section_highlight": "blushPeach",
        "hover_highlight": "hoverCoral",
        "effect": "Native fill-image state change, not continuous animation",
        "native_render_verified": False,
        "reference": "https://www.reddit.com/r/PowerBI/comments/1mi4mut/page_navigation_bubble_design/",
        "modified_paths": [str(p.relative_to(ROOT)) for p in sorted(touched)],
    }
    write(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
