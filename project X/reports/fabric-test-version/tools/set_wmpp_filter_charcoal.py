"""Apply the owner's charcoal choice only to the shared Filters controls."""

from copy import deepcopy
from datetime import datetime
import hashlib
import json
import shutil

from apply_wmpp_owner_bubble_states import BRAND, RESOURCES
from build_report_design_delivery import read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE


def main():
    colour = "#2B2427"
    marker = REPORT.parent / "FILTER_CHARCOAL_UPDATE.json"
    assert not marker.exists(), "Inspect the previous update before reapplying."
    backup = BUNDLE / "_review" / ("filter-charcoal-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    presets = set()
    pages = set()
    controls = 0
    definitions = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (REPORT / "definition").rglob("*.json")}
    for path in (REPORT / "definition/pages").glob("*/visuals/*/visual.json"):
        value = read(path)
        visual = value.get("visual", {})
        general = json.dumps(visual.get("visualContainerObjects", {}).get("general", {}))
        if "Open Filters" not in general and "Close Filters" not in general:
            continue
        preset = visual["visualContainerObjects"]["stylePreset"][0]["properties"]["name"]["expr"]["Literal"]["Value"].strip("'")
        presets.add(preset)
        pages.add(path.parents[2].name)
        controls += 1
        assert all("fillColor" not in e["properties"] for e in visual["objects"]["fill"])
        assert "filter_w6879838832520849.svg" in json.dumps(visual["objects"]["fill"])
    assert controls == 20 and len(pages) == 10
    # Do not change a preset shared by unrelated visuals.
    for path in (REPORT / "definition/pages").glob("*/visuals/*/visual.json"):
        value = read(path)
        containers = value.get("visual", {}).get("visualContainerObjects", {})
        selected = json.dumps(containers.get("stylePreset", {}))
        if any(preset in selected for preset in presets):
            assert "Filters" in json.dumps(containers.get("general", {}))
    planned = {}
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        original = deepcopy(theme)
        for preset in presets:
            entries = theme["visualStyles"]["actionButton"][preset]["fill"]
            for state in ("default", "hover", "selected", "disabled"):
                entry = next((e for e in entries if e.get("$id") == state), None)
                if entry is None:
                    entry = {"$id": state}
                    entries.append(entry)
                entry.update(fillColor={"solid": {"color": colour}}, transparency=0)
            for entry in entries:
                if "fillColor" in entry:
                    entry["fillColor"] = {"solid": {"color": colour}}
        # Only fill settings of the two filter-specific presets are changed.
        comparison = deepcopy(theme)
        for preset in presets:
            comparison["visualStyles"]["actionButton"][preset]["fill"] = original["visualStyles"]["actionButton"][preset]["fill"]
        assert comparison == original
        planned[path] = theme
    palette_path = BRAND / "WMPP_Palette.json"
    palette = read(palette_path)
    palette["colours"]["filterCharcoal"] = colour
    planned[palette_path] = palette
    for path, value in planned.items():
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        save(path, value)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in definitions.items())
    result = dict(colour=colour, dashboards=len(pages), open_close_controls=controls,
                  presets=sorted(presets), backup=str(backup), report_definitions_unchanged=True,
                  desktop_render_verified=False, modified_paths=[str(p.relative_to(ROOT)) for p in planned])
    save(marker, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
