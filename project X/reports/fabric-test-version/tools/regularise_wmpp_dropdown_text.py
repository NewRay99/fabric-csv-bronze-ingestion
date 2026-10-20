"""Remove bold only from the existing dropdown rows and their theme preset."""

from copy import deepcopy
from datetime import datetime
import json
import shutil

from apply_wmpp_owner_bubble_states import BRAND, RESOURCES
from build_report_design_delivery import L, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE


def main():
    marker = REPORT.parent / "DROPDOWN_REGULAR_TEXT.json"
    assert not marker.exists(), "Inspect prior update before reapplying."
    backup = BUNDLE / "_review" / ("dropdown-regular-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    planned = {}
    pages = set()
    states = 0
    for path in (REPORT / "definition/pages").glob("*/visuals/*/visual.json"):
        original = read(path)
        visual = original.get("visual", {})
        if visual.get("visualType") != "actionButton" or not 300020 <= original["position"]["z"] <= 300030:
            continue
        assert "WMPP Navigation Dropdown" in json.dumps(visual["visualContainerObjects"]["stylePreset"])
        value = deepcopy(original)
        for entry in value["visual"]["objects"]["text"]:
            entry["properties"]["bold"] = L("false")
            states += 1
        comparison = deepcopy(value)
        comparison["visual"]["objects"]["text"] = original["visual"]["objects"]["text"]
        assert comparison == original
        pages.add(path.parents[2].name)
        planned[path] = value
    rows = len(planned)
    assert rows == 272 and len(pages) == 16
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        for entry in theme["visualStyles"]["actionButton"]["WMPP Navigation Dropdown"]["text"]:
            entry["bold"] = False
        planned[path] = theme
    for path, value in planned.items():
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        save(path, value)
        assert read(path) == value
    result = dict(backup=str(backup), dropdown_rows=rows, pages=len(pages), text_states=states,
                  desktop_render_verified=False, modified_paths=[str(p.relative_to(ROOT)) for p in planned])
    save(marker, result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
