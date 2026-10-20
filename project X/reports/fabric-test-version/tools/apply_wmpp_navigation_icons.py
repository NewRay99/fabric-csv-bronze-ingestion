"""Embed audited Lucide SVGs in existing navigation; preserve actions and layout."""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import shutil
import urllib.request
import xml.etree.ElementTree as ET

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT
from use_wmpp_dropdown_navigation import PAGES

REVISION = "66d8f9fc394b8530377e5f6112f0b8908ba01280"
ICONS = {
    "HO": ("Home", "house"),
    "R": ("Referrals", "user-round-plus"),
    "OO": ("Offers", "handshake"),
    "DO": ("Draft offers", "file-pen-line"),
    "IO": ("IPAs", "file-check-corner"),
    "PR": ("Providers", "building-complex"),
    "PF": ("Performance", "chart-no-axes-combined"),
    "RM": ("Requirements", "clipboard-list"),
}
STATES = ("default", "hover", "selected", "disabled")


def fetch(path):
    url = f"https://raw.githubusercontent.com/lucide-icons/lucide/{REVISION}/{path}"
    return urllib.request.urlopen(url, timeout=30).read(), url


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    # Fetch/parse all assets before modifying the report.
    assets = {}
    for short, (label, name) in ICONS.items():
        source, url = fetch(f"icons/{name}.svg")
        root = ET.fromstring(source)
        assert root.tag == "{http://www.w3.org/2000/svg}svg"
        assert root.attrib.get("viewBox") == "0 0 24 24"
        assert b"currentColor" in source
        white = source.replace(b"currentColor", b"#FFFFFF")
        assets[short] = (label, name, source, white, url)
    licence, licence_url = fetch("LICENSE")
    backup = BUNDLE / "_review" / ("lucide-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    protected = {p: digest(p) for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    protected.update({p: digest(p) for p in (REPORT / "definition/bookmarks").glob("*.json")})

    def retain(path):
        if path.exists():
            target = backup / path.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)

    icon_root = ROOT / "assets/brand-pack/icons"
    upstream = icon_root / "lucide-originals"
    upstream.mkdir(parents=True, exist_ok=True)
    registered = REPORT / "StaticResources/RegisteredResources"
    definition_path = REPORT / "definition/report.json"
    definition = read(definition_path)
    package = next(p for p in definition["resourcePackages"] if p["name"] == "RegisteredResources")
    provenance = []
    for short, (label, name, source, white, url) in assets.items():
        filename = f"lucide-nav-{name}-white.svg"
        for path, content in [
            (upstream / f"{name}.svg", source),
            (icon_root / filename, white),
            (registered / filename, white),
        ]:
            retain(path)
            path.write_bytes(content)
        if not any(i["name"] == filename for i in package["items"]):
            package["items"].append({"name": filename, "path": filename, "type": "Image"})
        provenance.append(
            {
                "navigation": label,
                "icon": name,
                "page": f"https://lucide.dev/icons/{name}",
                "source": url,
                "revision": REVISION,
                "file": filename,
                "source_sha256": hashlib.sha256(source).hexdigest(),
                "white_sha256": hashlib.sha256(white).hexdigest(),
                "modification": "stroke currentColor replaced by #FFFFFF; paths unchanged",
            }
        )
        for pid in PAGES:
            path = (
                REPORT
                / "definition/pages"
                / pid
                / "visuals"
                / ident(f"wmpp-dropdown:{pid}:main-{short}")
                / "visual.json"
            )
            old = read(path)
            new = deepcopy(old)
            objects = new["visual"]["objects"]
            objects["text"] = obj(show=L("false")) + [
                {"selector": {"id": state}, "properties": {"show": L("false"), "text": L("''")}}
                for state in STATES
            ]
            properties = {
                "show": L("true"),
                "shapeType": L("'custom'"),
                "placement": L("'custom'"),
                "horizontalAlignment": L("'center'"),
                "verticalAlignment": L("'middle'"),
                "iconSize": L("32D"),
                "leftMargin": L("0L"),
                "rightMargin": L("0L"),
                "topMargin": L("0L"),
                "bottomMargin": L("0L"),
                "lineColor": fill("#FFFFFF"),
                "lineTransparency": L("0D"),
                "image": {
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
                },
            }
            objects["icon"] = obj(**deepcopy(properties)) + [
                {"selector": {"id": state}, "properties": deepcopy(properties)} for state in STATES
            ]
            objects["outline"] = obj(show=L("false")) + [
                {
                    "selector": {"id": state},
                    "properties": {
                        "show": L("false"),
                        "weight": L("0D"),
                        "transparency": L("100D"),
                    },
                }
                for state in STATES
            ]
            new["visual"]["visualContainerObjects"]["border"] = obj(show=L("false"))
            assert new["position"] == old["position"]
            assert objects["shape"] == old["visual"]["objects"]["shape"]
            assert objects["fill"] == old["visual"]["objects"]["fill"]
            assert (
                new["visual"]["visualContainerObjects"]["visualLink"]
                == old["visual"]["visualContainerObjects"]["visualLink"]
            )
            retain(path)
            save(path, new)
    retain(definition_path)
    save(definition_path, definition)
    for path in [icon_root / "LUCIDE_LICENSE.txt", REPORT.parent / "LUCIDE_LICENSE.txt"]:
        retain(path)
        path.write_bytes(licence)
    manifest = {
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "licence_source": licence_url,
        "icons": provenance,
    }
    for path in [
        icon_root / "LUCIDE_NAVIGATION_SOURCES.json",
        REPORT.parent / "LUCIDE_NAVIGATION_SOURCES.json",
    ]:
        retain(path)
        save(path, manifest)
    for path in [
        ROOT / "assets/brand-pack/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        registered / "WMPP_Theme.json",
    ]:
        theme = read(path)
        for preset in theme["visualStyles"].get("actionButton", {}).values():
            for entry in preset.get("outline", []):
                entry["show"] = False
            for entry in preset.get("icon", []):
                if "lineColor" in entry:
                    entry["lineColor"] = {"solid": {"color": "#FFFFFF"}}
        retain(path)
        save(path, theme)
    assert all(digest(p) == h for p, h in protected.items())
    result = {
        "icons": 8,
        "navigation_buttons": 128,
        "white_icons": True,
        "button_outlines": False,
        "actions_geometry_fills_bookmarks_models_preserved": True,
        "native_render_verified": False,
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
