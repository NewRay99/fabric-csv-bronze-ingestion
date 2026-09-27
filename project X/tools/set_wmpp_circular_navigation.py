"""Apply the original native circular shape definition to main navigation only."""

from copy import deepcopy
from datetime import datetime
import json
import shutil

from build_report_design_delivery import ident, read, save
from connect_wmpp_report_pages import BUNDLE, SOURCE
from use_wmpp_dropdown_navigation import PAGES, REPORT, TOP


def main():
    original = read(
        SOURCE / "definition/pages/f028a4be56d03e8404d7/visuals/616e2a09e791dbc9044d/visual.json"
    )["visual"]["objects"]["shape"][0]
    assert original["selector"] == {"id": "default"}
    assert original["properties"]["tileShape"]["expr"]["Literal"]["Value"] == "'oval'"
    states = ("default", "hover", "selected", "disabled")
    shape = [dict(deepcopy(original), selector={"id": state}) for state in states]
    paths = [
        REPORT
        / "definition/pages"
        / pid
        / "visuals"
        / ident(f"wmpp-dropdown:{pid}:main-{short}")
        / "visual.json"
        for pid in sorted(PAGES)
        for short, _, _ in TOP
    ]
    before = {path: read(path) for path in paths}
    assert len(paths) == 128
    assert all(v["position"]["width"] == v["position"]["height"] == 66 for v in before.values())
    backup = (
        BUNDLE / "_review" / ("circular-navigation-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    for path, value in before.items():
        target = backup / path.relative_to(REPORT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        revised = deepcopy(value)
        revised["visual"]["objects"]["shape"] = deepcopy(shape)
        save(path, revised)
    for path, old in before.items():
        new = read(path)
        assert new["visual"]["objects"]["shape"] == shape
        new["visual"]["objects"]["shape"] = old["visual"]["objects"]["shape"]
        assert new == old, "Only the shape definition may change"
    result = {
        "main_buttons_updated": len(paths),
        "pages": len(PAGES),
        "shape": "Original oval, equal width and height, explicit state selectors",
        "only_main_button_shape_changed": True,
        "native_render_verified": False,
        "backup": str(backup),
    }
    save(backup / "verification.json", result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
