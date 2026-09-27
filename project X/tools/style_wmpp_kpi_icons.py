"""Add transparent, meaning-matched Lucide icons and refresh WMPP chart colours.

One-time delivery styling; no model, query, filter, navigation or refresh changes.
"""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import shutil
import sys
import urllib.request
import xml.etree.ElementTree as ET

from build_report_design_delivery import L, fill, obj, quoted, read, save
from connect_wmpp_report_pages import BUNDLE, REPORT, ROOT
from apply_native_report_annotations import image as image_visual
from add_board_dashboard_annotations import text as text_visual
from apply_wmpp_navigation_icons import REVISION

CORAL, TEAL, AMBER, RED, INK = "#D94D2B", "#287C73", "#A86612", "#C13F35", "#575756"
PALETTE = {
    "#F9CAD4": "#FFD8C7",
    "#963542": "#D94D2B",
    "#E96B7D": "#FB6540",
    "#F092A5": "#FF8C42",
    "#F7BDC9": "#FFD8D1",
    "#A33B61": "#D94D2B",
    "#FF5D43": "#FB6540",
    "#FFB49F": "#FFB39F",
    "#39AEA5": "#3DAFA5",
    "#45AEAF": "#3DAFA5",
    "#E94D3E": "#F34E43",
    "#CAFD3C": "#3DAFA5",
}
EXTERNAL_KPIS = {"5038cffdd48af9a80dd1", "510f9f9501ccc5ae8a74", "6ae319c8916a5d63a4ff"}
SKIP_METRICS = {"Gold Model Last Refreshed", "Current Referral As Of", "Snapshot Window Anchor"}


def values(value, key):
    result = []
    if isinstance(value, dict):
        if key in value:
            result.append(value[key])
        for child in value.values():
            result.extend(values(child, key))
    elif isinstance(value, list):
        for child in value:
            result.extend(values(child, key))
    return result


def words(value):
    return " ".join(
        str(v)
        for v in values(value.get("visual", {}).get("objects", {}).get("general", []), "value")
    )


def metric(value):
    projections = (
        value.get("visual", {})
        .get("query", {})
        .get("queryState", {})
        .get("Data", {})
        .get("projections", [])
    )
    if not projections:
        return ""
    projection = projections[0]
    fields = values(projection.get("field", {}), "Property")
    return (
        fields[0]
        if fields and fields[0] not in ("Req ID", "KPI ID")
        else projection.get("displayName", projection.get("nativeQueryRef", ""))
    )


def choose(label):
    """Shared mapping for cards, guide headings and section headings."""
    s = label.casefold().replace("new", "").replace("'", "")
    if "refreshed" in s or "as of" in s:
        return "clock", INK
    if "requirement" in s or s == "kpi id" or "kpis" in s:
        return ("clipboard-check", TEAL) if "complete" in s else ("clipboard-list", CORAL)
    if "weekly cost" in s or "liability" in s:
        return "pound-sterling", TEAL
    if "multiple provider" in s or "assignments" in s or "provider referrals" in s:
        return "network", CORAL
    if "no activity" in s or "inactive" in s:
        return "hourglass", AMBER
    if "activity" in s or "engagement" in s or "engaged" in s or "provider contact" in s:
        return "activity", TEAL
    if "overdue" in s or "escalat" in s:
        return "triangle-alert", RED
    if "location review" in s or "without preferred-city" in s or "needs location" in s:
        return "map-pin", AMBER
    if "distance" in s:
        return ("map-pin", TEAL) if "coverage" in s else ("route", CORAL)
    if (
        "geography" in s
        or "city" in s
        or "region" in s
        or "county" in s
        or "location" in s
        or "preference map" in s
    ):
        return "map-pin", CORAL
    if "snapshot" in s or "due this" in s:
        return "calendar-days", CORAL
    if "draft" in s:
        return ("clock", AMBER) if "age" in s or "days" in s else ("file-pen-line", CORAL)
    if "pending" in s or "awaiting" in s or "not entered" in s or "due in" in s:
        return "clock", AMBER
    if "ipa" in s or "agreement" in s:
        if "days" in s:
            return "clock", AMBER
        if "complet" in s or "conversion" in s:
            return "file-check-corner", TEAL
        return "file-plus", CORAL
    if "target" in s or "hit rate" in s or "placed by" in s:
        return "target", TEAL
    if "days early" in s or "response time" in s:
        return "clock", TEAL
    if "accept" in s or "successful" in s:
        return "handshake", TEAL
    if "homes" in s:
        return "house", CORAL
    if "provider" in s and "offer" not in s:
        return "building-complex", CORAL
    if "offer" in s:
        return "handshake", CORAL
    if "not yet closed" in s:
        return "users", CORAL
    if "closed" in s or "cancelled" in s:
        return "clipboard-check", INK
    if "referral" in s:
        return "users", CORAL
    if "performance" in s or "board" in s or "breakdown" in s:
        return "chart-no-axes-combined", CORAL
    if "home" in s:
        return "house", CORAL
    return "chart-column", CORAL


def asset_name(icon, colour):
    return f"lucide-kpi-{icon}-{colour[1:].lower()}.svg"


def picture(filename):
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


def recolour(value):
    if isinstance(value, str):
        raw = value.strip("'").upper()
        if raw in PALETTE:
            return "'" + PALETTE[raw] + "'" if value.startswith("'") else PALETTE[raw]
        return value
    if isinstance(value, list):
        return [recolour(v) for v in value]
    if isinstance(value, dict):
        return {k: recolour(v) for k, v in value.items()}
    return value


def main():
    pages_root = REPORT / "definition/pages"
    pages = {p.parent.name: read(p) for p in pages_root.glob("*/page.json")}
    assert not any(
        a.get("name") == "wmppKpiIconRevision"
        for p in pages.values()
        for a in p.get("annotations", [])
    ), "Already applied; review existing changes instead of rerunning."
    originals = {p: read(p) for p in pages_root.glob("*/visuals/*/visual.json")}
    modified = deepcopy(originals)
    additions, mappings, assets = {}, [], set()
    counters = {
        "native_kpi_icons": 0,
        "existing_image_icons": 0,
        "guide_icons": 0,
        "subpage_icons": 0,
        "chart_visuals_recoloured": 0,
    }

    def track(label, pair, pid, vid, kind):
        assets.add(pair)
        mappings.append(
            {
                "page": pages[pid]["displayName"],
                "visual": vid,
                "label": label,
                "icon": pair[0],
                "colour": pair[1],
                "kind": kind,
            }
        )
        return asset_name(*pair)

    def add_icon(pid, text_value, pair, kind):
        pos = text_value["position"]
        size = 28 if pos["height"] <= 30 else 34
        filename = track(words(text_value), pair, pid, text_value["name"], kind)
        icon = image_visual(
            "kpi-icon:" + pid + ":" + text_value["name"],
            "info",
            (pos["x"], pos["y"] + max(0, (min(pos["height"], 44) - size) / 2), size, size),
        )
        icon["visual"]["objects"]["image"] = obj(sourceFile=picture(filename))
        icon["visual"]["visualContainerObjects"]["general"] = obj(
            altText=L(quoted(words(text_value) + " icon"))
        )
        icon["position"]["z"] = pos["z"] + 1
        additions[pages_root / pid / "visuals" / icon["name"] / "visual.json"] = icon
        pos["x"] += size + 12
        pos["width"] -= size + 12

    for path, value in modified.items():
        pid = path.parents[2].name
        page = pages[pid]
        name = page["displayName"]
        visual = value.get("visual", {})
        kind = visual.get("visualType", "")
        objects = visual.setdefault("objects", {}) if visual else {}
        label = metric(value)
        if kind == "cardVisual" and label and label not in SKIP_METRICS:
            # Small KPI-ID info widgets are explanations, not business scorecards.
            if value["position"]["width"] < 85:
                continue  # Preserve the owner's pale-background information badges.
            elif pid in EXTERNAL_KPIS:
                continue  # Reuse the existing separate icon without crowding narrow value cards.
            else:
                pair = choose(label)
            filename = track(label, pair, pid, value["name"], "card")
            current = deepcopy(
                objects.get("image", [{"selector": {"id": "default"}, "properties": {}}])
            )
            for entry in current:
                props = entry.setdefault("properties", {})
                props.update(
                    show=L("true"),
                    imageType=L("'image'"),
                    image=picture(filename),
                    fit=L("'Fit'"),
                    imageEffects=L("false"),
                )
                if "imageAreaSize" not in props:
                    props.update(
                        imageAreaSize=L("20L"), padding=L("2L"), verticalAlignment=L("'middle'")
                    )
            objects["image"] = current
            for entry in objects.get("cardImage", []):
                if "image" in entry.get("properties", {}):
                    entry["properties"]["image"] = picture(filename)
            counters["native_kpi_icons"] += 1

        if kind == "image":
            refs = values(objects, "ResourcePackageItem")
            filenames = [r["ItemName"] for r in refs]
            if any(f.startswith("lc-") or "info-" in f or f.startswith("bulb") for f in filenames):
                if any("info" in f for f in filenames):
                    continue  # Information icon backgrounds are explicitly retained.
                elif any(f.startswith("bulb") for f in filenames):
                    pair, label = ("lightbulb", AMBER), "Interpretation note"
                else:
                    candidates = [
                        v
                        for p, v in originals.items()
                        if p.parents[2].name == pid
                        and v.get("visual", {}).get("visualType") == "cardVisual"
                        and abs(v["position"]["y"] - value["position"]["y"]) < 12
                        and 0 < v["position"]["x"] - value["position"]["x"] < 100
                    ]
                    label = metric(candidates[0]) if candidates else name
                    pair = choose(label)
                filename = track(label, pair, pid, value["name"], "existing image")
                for ref in refs:
                    ref["ItemName"] = filename
                for image in values(objects, "image"):
                    if isinstance(image, dict) and "url" in image:
                        image["name"] = L(quoted(filename))
                counters["existing_image_icons"] += 1

        if kind == "textbox" and not value.get("isHidden"):
            pos = value["position"]
            if name.endswith(" - guide") and pos["height"] in (30, 44):
                add_icon(pid, value, choose(words(value)), "guide")
                counters["guide_icons"] += 1
            elif not name.endswith(" - guide") and pid not in EXTERNAL_KPIS and pos["z"] != 100012:
                # Headings on the added detail/explorer pages; leave long prose/captions alone.
                heading = words(value)
                explorer_heading = (
                    pid in {"1cd52e9c7e4016f342ce", "f028a4be56d03e8404d7", "f3070e87127b751f89d4"}
                    and pos["y"] == 157
                    and pos["height"] == 44
                )
                section_heading = (
                    pid in {"1cd52e9c7e4016f342ce", "f028a4be56d03e8404d7", "f3070e87127b751f89d4"}
                    and pos["height"] == 28
                    and pos["y"] in (521, 767)
                )
                simple_heading = (
                    pid in {"08ef33dc6a87d1b14392", "4cad3706fca6451c66b8", "4be6f15f15a086c98c33"}
                    and pos["y"] == 124
                )
                snapshot_heading = pid == "dd3a58c056d723048dbf" and pos["height"] in (28, 55)
                if explorer_heading or section_heading or simple_heading or snapshot_heading:
                    add_icon(pid, value, choose(name if explorer_heading else heading), "subpage")
                    counters["subpage_icons"] += 1

        if kind not in {"actionButton", "textbox", "image", "shape", "cardVisual", "", "slicer"}:
            updated = recolour(objects)
            if updated != objects:
                visual["objects"] = updated
                counters["chart_visuals_recoloured"] += 1
            # The annotated provider chart: length carries magnitude, not a second colour scale.
            if pid == "1f33996970651e846183" and value["name"] == "feef8d204a260a0060c7":
                visual["objects"]["dataPoint"] = obj(
                    defaultColor=fill("#FB6540"), fill=fill("#FB6540")
                )
                for entry in visual["objects"].get("labels", []):
                    entry["properties"]["color"] = fill("#1D1D1B")
                visual["objects"]["labels"].append({"properties": {"color": fill("#1D1D1B")}})

    # Requirement scorecards were absent from the existing guide: add explanations
    # without certifying the underlying aggregation as a delivered requirement count.
    pid = "260af7ad894430df8e65"
    for i, (title, detail) in enumerate(
        [
            (
                "Original Requirements",
                "Catalogue requirement-ID card. Read its saved aggregation and current filters; this styling update does not certify it as a distinct requirement count.",
            ),
            (
                "Requirements Complete",
                "Existing linkage-based card. A linked requirement is not proof of delivered functionality; consult the requirement status and client acceptance evidence.",
            ),
            (
                "KPIs",
                "KPI catalogue card under the current report filters. Catalogue entries are not service caseload or placement totals.",
            ),
        ]
    ):
        x, y = 36 + (i % 2) * 820, 430 + (i // 2) * 132
        title_value = text_visual("kpi-guide:" + title, title, (x, y, 776, 30), 18, True)
        detail_value = text_visual(
            "kpi-guide-description:" + title, detail, (x, y + 34, 776, 90), 13
        )
        add_icon(pid, title_value, choose(title), "guide")
        for v in (title_value, detail_value):
            additions[pages_root / pid / "visuals" / v["name"] / "visual.json"] = v
        counters["guide_icons"] += 1

    # Download complete icon set before writing any report files.
    sources = {}
    for icon in sorted({icon for icon, _ in assets}):
        url = f"https://raw.githubusercontent.com/lucide-icons/lucide/{REVISION}/icons/{icon}.svg"
        data = urllib.request.urlopen(url, timeout=30).read()
        svg = ET.fromstring(data)
        assert svg.tag == "{http://www.w3.org/2000/svg}svg" and b"currentColor" in data
        sources[icon] = (data, url)

    backup = BUNDLE / "_review" / ("kpi-icons-colours-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    protected = {
        p: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in REPORT.parent.glob("*.SemanticModel/**/*")
        if p.is_file()
    }
    protected.update(
        {
            p: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (REPORT / "definition/bookmarks").glob("*.json")
        }
    )

    def retain(path):
        if path.exists():
            dest = backup / path.relative_to(ROOT)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, dest)

    icon_root = ROOT / "assets/brand-pack/icons"
    registered = REPORT / "StaticResources/RegisteredResources"
    definition_path = REPORT / "definition/report.json"
    definition = read(definition_path)
    items = next(
        p["items"] for p in definition["resourcePackages"] if p["name"] == "RegisteredResources"
    )
    manifest = []
    for icon, colour in sorted(assets):
        data, url = sources[icon]
        variant = data.replace(b"currentColor", colour.encode())
        filename = asset_name(icon, colour)
        for p, content in [
            (icon_root / "lucide-originals" / (icon + ".svg"), data),
            (icon_root / filename, variant),
            (registered / filename, variant),
        ]:
            retain(p)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(content)
        if not any(i["name"] == filename for i in items):
            items.append({"name": filename, "path": filename, "type": "Image"})
        manifest.append(
            {
                "icon": icon,
                "colour": colour,
                "source": url,
                "page": f"https://lucide.dev/icons/{icon}",
                "file": filename,
                "source_sha256": hashlib.sha256(data).hexdigest(),
                "variant_sha256": hashlib.sha256(variant).hexdigest(),
            }
        )
    retain(definition_path)
    save(definition_path, definition)

    changed = []
    for p, new in modified.items():
        old = originals[p]
        if new == old:
            continue
        ov, nv = old.get("visual", {}), new.get("visual", {})
        assert ov.get("query") == nv.get("query")
        assert old.get("filterConfig") == new.get("filterConfig")
        assert ov.get("visualContainerObjects", {}).get("visualLink") == nv.get(
            "visualContainerObjects", {}
        ).get("visualLink")
        if ov.get("visualType") != "textbox":
            assert old["position"] == new["position"]
        assert values(ov.get("objects", {}).get("referenceLabel", []), "Measure") == values(
            nv.get("objects", {}).get("referenceLabel", []), "Measure"
        )
        retain(p)
        save(p, new)
        changed.append(str(p.relative_to(REPORT)))
    for p, new in additions.items():
        assert not p.exists(), str(p)
        save(p, new)
    for pid, page in pages.items():
        if page["displayName"].endswith(" - guide") or any(
            m["page"] == page["displayName"] for m in mappings
        ):
            p = pages_root / pid / "page.json"
            retain(p)
            page.setdefault("annotations", []).append(
                {"name": "wmppKpiIconRevision", "value": "transparent-lucide-20260927"}
            )
            save(p, page)
    for p in [
        ROOT / "assets/brand-pack/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Theme.json",
        ROOT / "reports/templates/WMPP_Common_Theme.json",
        registered / "WMPP_Theme.json",
    ]:
        theme = read(p)
        # Only colour defaults/preset literals, not typography or geometry.
        theme = recolour(theme)
        retain(p)
        save(p, theme)
    audit = {
        "revision": REVISION,
        "downloaded_utc": datetime.now(timezone.utc).isoformat(),
        "modification": "stroke currentColor replaced; no background shapes added; original paths retained",
        "assets": manifest,
        "visual_mapping": mappings,
    }
    for p in [icon_root / "LUCIDE_KPI_SOURCES.json", REPORT.parent / "LUCIDE_KPI_SOURCES.json"]:
        retain(p)
        save(p, audit)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = {
        **counters,
        "svg_variants": len(assets),
        "changed_visuals": len(changed),
        "added_icon_and_guide_visuals": len(additions),
        "model_bookmarks_queries_filters_actions_preserved": True,
        "native_render_verified": False,
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    save(backup / "changed_visuals.json", changed)
    print(json.dumps(result, indent=2))


def repair_open_referral_icon():
    """Correct the not-yet-closed pictogram without rerunning the layout migration."""
    path = REPORT / "definition/pages/78d576b289e5fe3d2af6/visuals/96620a62474172e2400e/visual.json"
    value = read(path)
    pair = choose("Referrals Not Yet Closed (Created in Period)")
    filename = asset_name(*pair)
    assert (REPORT / "StaticResources/RegisteredResources" / filename).is_file()
    for key in ("image", "cardImage"):
        for entry in value["visual"]["objects"].get(key, []):
            if "image" in entry.get("properties", {}):
                entry["properties"]["image"] = picture(filename)
    save(path, value)
    for path in (
        ROOT / "assets/brand-pack/icons/LUCIDE_KPI_SOURCES.json",
        REPORT.parent / "LUCIDE_KPI_SOURCES.json",
    ):
        audit = read(path)
        for item in audit["visual_mapping"]:
            if item["label"] == "Referrals Not Yet Closed (Created in Period)":
                item["icon"], item["colour"] = pair
        save(path, audit)
    print("Not-yet-closed referrals use the caseload icon; no data or geometry changed.")


if __name__ == "__main__":
    if "--repair-open-icon" in sys.argv:
        repair_open_referral_icon()
    else:
        main()
