"""Explicit native button states; preserve placement, action and data context.

Power BI's state selectors are default, hover, selected (on press), and disabled.
Unscoped label properties are not a substitute for labels on these selectors.
"""

from copy import deepcopy

from build_report_design_delivery import fill, L, obj, quoted

STATES = {
    "default": ("#FB6540", "#2B2427"),
    "hover": ("#FCA356", "#2B2427"),
    "selected": ("#EF7911", "#2B2427"),
    "disabled": ("#F0EBE7", "#625B5B"),
}


def state_entry(state, **properties):
    return {"properties": properties, "selector": {"id": state}}


def style_button(value, label, disabled_label):
    value = deepcopy(value)
    visual = value["visual"]
    if visual["visualType"] != "actionButton":
        raise ValueError("Only native action buttons can use this style")
    objects = visual.setdefault("objects", {})
    objects["text"] = obj(show=L("true"))
    objects["fill"] = obj(show=L("true"))
    objects["outline"] = obj(show=L("false"))
    objects["shape"] = obj(tileShape=L("'rectangle'"), roundEdge=L("8D"))
    objects["icon"] = obj(show=L("false"))
    for state, (background, foreground) in STATES.items():
        objects["text"].append(
            state_entry(
                state,
                show=L("true"),
                text=L(quoted(disabled_label if state == "disabled" else label)),
                fontFamily=L("'Segoe UI'"),
                fontSize=L("13D"),
                fontColor=fill(foreground),
                bold=L("false"),
                horizontalAlignment=L("'center'"),
                verticalAlignment=L("'middle'"),
                leftMargin=L("12D"),
                rightMargin=L("12D"),
                topMargin=L("4D"),
                bottomMargin=L("4D"),
            )
        )
        objects["fill"].append(
            state_entry(state, show=L("true"), fillColor=fill(background), transparency=L("0D"))
        )
        objects["outline"].append(state_entry(state, show=L("false")))
        objects["shape"].append(
            state_entry(state, tileShape=L("'rectangle'"), roundEdge=L("8D"))
        )
        objects["icon"].append(state_entry(state, show=L("false")))
    container = visual.setdefault("visualContainerObjects", {})
    container["title"] = obj(show=L("false"))
    container["background"] = obj(show=L("false"))
    container["border"] = obj(show=L("false"))
    container["dropShadow"] = obj(show=L("false"))
    container["padding"] = obj(top=L("0D"), bottom=L("0D"), left=L("0D"), right=L("0D"))
    return value


def missing_state_labels(value):
    entries = value.get("visual", {}).get("objects", {}).get("text", [])
    failures = []
    for state in STATES:
        matches = [x for x in entries if x.get("selector", {}).get("id") == state]
        if len(matches) != 1:
            failures.append(state)
            continue
        props = matches[0].get("properties", {})
        label = props.get("text", {}).get("expr", {}).get("Literal", {}).get("Value", "")
        shown = props.get("show", {}).get("expr", {}).get("Literal", {}).get("Value")
        if not label.strip("' ") or shown != "true":
            failures.append(state)
    return failures
