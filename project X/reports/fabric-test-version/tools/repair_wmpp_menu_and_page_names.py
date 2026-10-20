"""Restore native navigation icons, neutral wallpaper and readable page labels.

This is a scoped corrective migration, not a semantic/report-version test suite.
Use --check for one-off inspection of the reported configuration regression.
"""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
import shutil
import sys

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT
from use_wmpp_dropdown_navigation import PAGES, TOP

BRAND = ROOT / "assets/brand-pack"
CANVAS = "#F8F5F1"


def title_case(value):
    value = value.title()
    for pattern, replacement in [(r"\bWmpp\b", "WMPP"), (r"\bIpa\b", "IPA"), (r"\bIpas\b", "IPAs")]:
        value = re.sub(pattern, replacement, value)
    return value


def fingerprint(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect():
    faults = []
    for pid in PAGES:
        base = REPORT / "definition/pages" / pid / "visuals"
        rail = read(base / ident(f"wmpp-bubble-rail:{pid}") / "visual.json")
        if not rail.get("isHidden", False):
            faults.append("visible orange rail")
        for short, _, _ in TOP:
            button = read(base / ident(f"wmpp-dropdown:{pid}:main-{short}") / "visual.json")
            icons = button["visual"]["objects"].get("icon", [])
            if not icons or any(e["properties"].get("show") != L("true") for e in icons):
                faults.append("native navigation icon disabled")
            for entry in icons:
                resource = (
                    entry["properties"]
                    .get("image", {})
                    .get("image", {})
                    .get("url", {})
                    .get("expr", {})
                    .get("ResourcePackageItem", {})
                )
                if (
                    resource
                    and not (
                        REPORT / "StaticResources/RegisteredResources" / resource["ItemName"]
                    ).is_file()
                ):
                    faults.append("missing icon asset")
    for path in (REPORT / "definition/pages").glob("*/page.json"):
        page = read(path)
        if page.get("objects", {}).get("outspace") != obj(color=fill(CANVAS), transparency=L("0D")):
            faults.append("wallpaper override is not neutral")
        if page["displayName"] != title_case(page["displayName"]):
            faults.append("page name not title case")
    counts = {name: faults.count(name) for name in sorted(set(faults))}
    print(json.dumps({"configuration_check": "FAIL" if faults else "PASS", "faults": counts}))
    return not faults


def main():
    if "--check" in sys.argv:
        raise SystemExit(0 if inspect() else 1)
    marker = REPORT.parent / "MENU_CORRECTION.json"
    assert not marker.exists(), "Correction already applied; inspect before changing again"
    bubble = read(REPORT.parent / "BUBBLE_NAVIGATION.json")
    from pathlib import Path

    source_backup = Path(bubble["backup"])
    backup = BUNDLE / "_review" / ("menu-correction-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    protected = {
        p: fingerprint(p)
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file() and ".pbi" not in p.parts
    }
    protected.update({p: fingerprint(p) for p in (REPORT / "definition/bookmarks").glob("*.json")})
    touched = set()
    queries = {}
    for path in (REPORT / "definition/pages").glob("*/visuals/*/visual.json"):
        d = read(path)
        queries[path] = (
            deepcopy(d.get("visual", {}).get("query")),
            deepcopy(d.get("filterConfig")),
        )

    def write(path, data):
        if path not in touched and path.exists():
            copy = backup / path.relative_to(ROOT)
            copy.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, copy)
        touched.add(path)
        save(path, data)

    def prior(path):
        return read(source_backup / path.relative_to(ROOT))

    for pid in PAGES:
        folder = REPORT / "definition/pages" / pid / "visuals"
        for short, _, _ in TOP:
            path = folder / ident(f"wmpp-dropdown:{pid}:main-{short}") / "visual.json"
            old, current = prior(path), read(path)
            # Restore direct native custom icons; no fill-image dependency.
            current["visual"]["objects"] = old["visual"]["objects"]
            current["visual"]["visualContainerObjects"]["stylePreset"] = old["visual"][
                "visualContainerObjects"
            ]["stylePreset"]
            current["position"].update(width=66, height=66)
            write(path, current)
            path = (
                folder / ident(f"board-annotation:dropdown:{pid}:caption:{short}") / "visual.json"
            )
            caption = read(path)
            caption["isHidden"] = False
            for paragraph in caption["visual"]["objects"]["general"][0]["properties"]["paragraphs"]:
                for run in paragraph["textRuns"]:
                    run["value"] = title_case(run["value"])
            write(path, caption)
        path = folder / ident(f"wmpp-bubble-rail:{pid}") / "visual.json"
        rail = read(path)
        rail["isHidden"] = True
        write(path, rail)

    renamed = {}
    for path in (REPORT / "definition/pages").glob("*/page.json"):
        page = read(path)
        old_name = page["displayName"]
        new_name = title_case(old_name)
        if page["name"] == "4be6f15f15a086c98c33":
            new_name = "Referral Single View (Original)"
        page["displayName"] = new_name
        page.setdefault("objects", {})["outspace"] = obj(color=fill(CANVAS), transparency=L("0D"))
        if old_name != new_name:
            renamed[old_name] = new_name
        write(path, page)

    # Update UI labels only. Never rename fields, measures, internal IDs or actions.
    nav_ids = {
        ident(f"wmpp-dropdown:{pid}:child:{area}:{n}")
        for pid in PAGES
        for area in ("Referrals", "Offers", "Providers", "Performance")
        for n in range(8)
    }

    def labels(value, nav=False):
        if isinstance(value, dict):
            for key, child in value.items():
                if (
                    key == "Value"
                    and isinstance(child, str)
                    and child.startswith("'")
                    and child.endswith("'")
                ):
                    plain = child[1:-1].replace("''", "'")
                    if plain in renamed:
                        value[key] = quoted(renamed[plain])
                elif key == "value" and isinstance(child, str) and child in renamed:
                    value[key] = renamed[child]
                else:
                    labels(child, nav)
        elif isinstance(value, list):
            for child in value:
                labels(child, nav)

    for path in queries:
        d = read(path)
        before = deepcopy(d)
        visual = d.get("visual", {})
        # Text boxes and button text are presentation, not semantic expressions.
        if visual.get("visualType") in ("textbox", "actionButton"):
            labels(visual.get("objects", {}))
        if d["name"] in nav_ids:
            for entry in visual.get("objects", {}).get("text", []):
                prop = entry["properties"].get("text", {})
                literal = prop.get("expr", {}).get("Literal", {})
                if "Value" in literal:
                    plain = literal["Value"][1:-1].replace("''", "'")
                    literal["Value"] = quoted(title_case(plain))
        if d != before:
            write(path, d)

    for path in [
        BRAND / "WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        REPORT / "StaticResources/RegisteredResources/WMPP_Theme.json",
    ]:
        theme = read(path)
        theme["visualStyles"].get("actionButton", {}).pop("WMPP Bubble Navigation", None)
        theme["visualStyles"].setdefault("page", {}).setdefault("*", {})["outspace"] = [
            {"color": {"solid": {"color": CANVAS}}, "transparency": 0}
        ]
        write(path, theme)
    assert all(fingerprint(p) == h for p, h in protected.items())
    for path, expected in queries.items():
        d = read(path)
        assert (d.get("visual", {}).get("query"), d.get("filterConfig")) == expected
    assert inspect()
    names = [read(p)["displayName"] for p in (REPORT / "definition/pages").glob("*/page.json")]
    assert len(names) == len(set(names))
    result = {
        "backup": str(backup),
        "restored_native_icons": 128,
        "hidden_orange_rails": 16,
        "neutral_wallpaper_pages": len(names),
        "renamed_pages": renamed,
        "semantic_files_bookmarks_queries_filters_unchanged": True,
        "desktop_render_verified": False,
        "modified_paths": [str(p.relative_to(ROOT)) for p in sorted(touched)],
    }
    write(marker, result)
    save(backup / "verification.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
