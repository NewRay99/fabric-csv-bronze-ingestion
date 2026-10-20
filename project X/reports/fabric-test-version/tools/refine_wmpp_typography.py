"""Reduce 32pt headings and regularise small headings and card labels."""

from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
import re
import shutil

from apply_wmpp_owner_bubble_states import BRAND, RESOURCES
from build_report_design_delivery import L, read, save
from connect_wmpp_report_pages import ROOT, REPORT, BUNDLE


def scalar(value):
    if isinstance(value, dict):
        return value.get("expr", {}).get("Literal", {}).get("Value")
    return value


def size(value, default=13):
    value = scalar(value)
    if value is None:
        return default
    match = re.fullmatch(r"(\d+(?:\.\d+)?)(pt|px|D|L)?", str(value))
    if not match:
        return default
    return float(match[1]) * (0.75 if match[2] == "px" else 1)


def format_props(props, native, label=False):
    def put(key, value):
        props[key] = L(value) if native else value
    heading4 = str(scalar(props.get("heading", ""))).strip("'").lower() == "heading4"
    if not label and size(props.get("fontSize")) == 32:
        put("fontSize", "24D" if native else 24)
    if label or heading4 or size(props.get("fontSize")) <= 13:
        put("bold", "false" if native else False)
        for key in ("fontFamily", "fontFace"):
            if key in props and any(word in str(scalar(props[key])).lower() for word in ("semibold", "bold")):
                put(key, "'Segoe UI'" if native else "Segoe UI")


def main():
    marker = REPORT.parent / "TYPOGRAPHY_REFINEMENT.json"
    assert not marker.exists(), "Inspect prior typography update before reapplying."
    backup = BUNDLE / "_review" / ("typography-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    original = {p: read(p) for p in (REPORT / "definition").rglob("*.json")}
    protected = {p: hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in REPORT.parent.glob("*.SemanticModel/**/*") if p.is_file()}
    planned = {}
    counts = Counter()
    titles = []
    for path, old in original.items():
        if path.name != "visual.json":
            continue
        value = deepcopy(old)
        visual = value.get("visual", {})
        kind = visual.get("visualType")
        # Navigation/menu labels intentionally retain their established states.
        if kind == "actionButton":
            continue
        for role in ("title", "subTitle"):
            for entry in visual.get("visualContainerObjects", {}).get(role, []):
                props = entry.get("properties", {})
                if any(k in props for k in ("fontSize", "bold", "fontFamily", "heading")):
                    format_props(props, True)
        if kind == "cardVisual":
            for entry in visual.get("objects", {}).get("label", []):
                format_props(entry["properties"], True, label=True)
        if kind == "textbox":
            for entry in visual.get("objects", {}).get("general", []):
                for para in entry.get("properties", {}).get("paragraphs", []):
                    for run in para.get("textRuns", []):
                        style = run.get("textStyle", {})
                        if size(style.get("fontSize"), 0) == 32:
                            style["fontSize"] = "24pt"
                            titles.append(run.get("value", ""))
                        if 0 < size(style.get("fontSize"), 0) <= 13:
                            if "fontWeight" in style:
                                style["fontWeight"] = "normal"
                            if "bold" in style:
                                style["bold"] = False
                            for key in ("fontFamily", "fontFace"):
                                if any(w in str(style.get(key, "")).lower() for w in ("bold", "semibold")):
                                    style[key] = "Segoe UI"
        if value != old:
            for key in ("position", "filterConfig", "parentGroupName", "isHidden"):
                assert value.get(key) == old.get(key)
            for key in ("query", "filterConfig"):
                assert visual.get(key) == old.get("visual", {}).get(key)
            for key in ("callout", "value", "referenceLabelValue"):
                assert visual.get("objects", {}).get(key) == old.get("visual", {}).get("objects", {}).get(key)
            planned[path] = value
            counts[kind] += 1
    for path in (BRAND / "WMPP_Theme.json", ROOT / "reports/templates/WMPP_Theme.json",
                 ROOT / "reports/templates/WMPP_Common_Theme.json", RESOURCES / "WMPP_Theme.json"):
        theme = read(path)
        for role in ("title", "header", "label"):
            props = theme.get("textClasses", {}).get(role, {})
            if size(props.get("fontSize")) <= 13:
                props["fontFace"] = "Segoe UI"
        for kind, presets in theme["visualStyles"].items():
            if kind == "actionButton":
                continue
            for style in presets.values():
                for role in ("title", "subTitle"):
                    for props in style.get(role, []):
                        format_props(props, False)
                if kind == "cardVisual":
                    for props in style.get("label", []):
                        format_props(props, False, label=True)
        planned[path] = theme
    for path, value in planned.items():
        target = backup / path.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        save(path, value)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in protected.items())
    result = dict(backup=str(backup), section_titles_32_to_24=titles, changed_visuals_by_type=dict(counts),
                  card_labels_regular=True, small_titles_regular=True, semantic_model_unchanged=True,
                  desktop_render_verified=False, modified_paths=[str(p.relative_to(ROOT)) for p in planned])
    save(marker, result)
    print(json.dumps({k: v for k, v in result.items() if k != "modified_paths"}, indent=2))


if __name__ == "__main__":
    main()
