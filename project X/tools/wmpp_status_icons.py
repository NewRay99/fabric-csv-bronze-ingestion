"""Filled status tiles for native table formatting, without changing source values.

These are status codes, not calculated journey milestones. Explicit case and
separator aliases avoid relying on a visual formatting evaluator's collation.
"""

from copy import deepcopy


TARGET_COLUMNS = {
    "current_status", "offer_status", "provider_response_status",
    "provider_status", "placement_status",
}
PREFIX = "wmpp-category-status-"
INK = "#2B2427"
COLOURS = {
    "draft": "#E69512", "open": "#4DAAAB", "assigned": "#0D35B8",
    "pending": "#E69512", "offer-made": "#EF7911", "under-offer": "#EF7911",
    "accepted": "#277455", "closed": INK, "cancelled": "#C0392B",
    "withdrawn": "#E69512", "declined": "#C0392B", "excluded": "#757075",
    "inactive": "#757075", "unknown": "#757075",
}
STATUS_GROUPS = {
    "draft": ("Draft", "Not started"),
    "open": ("Open", "Active"),
    "assigned": ("Assigned", "First contact"),
    "pending": ("Pending", "Offer pending", "Under review", "Awaiting", "Awaiting decision", "On hold", "In progress"),
    "offer-made": ("Offer made", "Offered", "Submitted"),
    "under-offer": ("Under offer",),
    "accepted": ("Accepted", "Offer accepted", "Approved", "Selected", "Successful", "Offer successful", "Completed", "Complete", "Signed"),
    "closed": ("Closed",),
    "cancelled": ("Cancelled", "Canceled"),
    "withdrawn": ("Withdrawn",),
    "declined": ("Declined", "Rejected", "Unsuccessful", "Offer unsuccessful"),
    "excluded": ("Excluded",),
    "inactive": ("Inactive",),
    "unknown": ("Unknown", "Unspecified", "Not known", "", " "),
}
DESCRIPTIONS = {
    "draft": "Draft — one amber tile",
    "open": "Open / active — one teal tile",
    "assigned": "Assigned — two blue tiles across the top",
    "pending": "Pending / awaiting — upper-right amber tile",
    "offer-made": "Offer made / submitted — two orange tiles down the left",
    "under-offer": "Under offer — three orange tiles",
    "accepted": "Accepted / completed / signed — green tiles with a final check",
    "closed": "Closed — four solid dark tiles; does not imply success",
    "cancelled": "Cancelled — three red tiles and a solid final dot",
    "withdrawn": "Withdrawn — three amber tiles and a final minus",
    "declined": "Declined / rejected — three red tiles and a final cross",
    "excluded": "Excluded — three grey tiles and a final cross",
    "inactive": "Inactive — three grey tiles and a solid final dot",
    "unknown": "Missing / unrecognised — grey question mark; original text retained",
}


def aliases(labels):
    """Cover the observed uppercase codes and existing readable labels."""
    values = set()
    for label in labels:
        for separated in (label, label.replace(" ", "_"), label.replace(" ", "-")):
            values.update((separated, separated.upper(), separated.lower(), separated.title(), separated.capitalize()))
    return sorted(values)


def literal(value):
    return {"Literal": {"Value": "'" + value.replace("'", "''") + "'"}}


def scalar_reference(reference):
    """Native conditional formatting needs a measure or aggregated column.

    Function 3 matches the user's working Desktop-authored text rule. Status is
    already a grouping column in each table row, so this reads that row's single
    status without changing the visible projection or any model calculation.
    """
    if "Column" in reference:
        return {"Aggregation": {"Expression": deepcopy(reference), "Function": 3}}
    if "Aggregation" in reference or "Measure" in reference:
        return deepcopy(reference)
    raise ValueError("Status icon input must be a column, aggregation or measure.")


def icon_format(reference):
    """Match the working native text-rule shape, not generic SQ 'In' conditions.

    Desktop's rule editor stores one equality comparison per text value, with
    both text-evaluation annotations. Keep its Cases-only conditional shape;
    unmapped codes are not silently labelled with a misleading question mark.
    """
    reference = scalar_reference(reference)
    cases = []
    for key, labels in STATUS_GROUPS.items():
        for label in aliases(labels):
            cases.append({
                "Condition": {
                    "Comparison": {
                        "ComparisonKind": 0,
                        "Left": deepcopy(reference),
                        "Right": literal(label),
                    },
                    "Annotations": {
                        "PowerBI.SQExprEvaluationKind": 1,
                        "PowerBI.SQExprTextOperatorOption": 2,
                    },
                },
                "Value": literal(PREFIX + key),
            })
    return {
        "kind": "Icon", "layout": {"expr": literal("Before")},
        "verticalAlignment": {"expr": literal("Middle")},
        "value": {"expr": {"Conditional": {"Cases": cases}}},
    }


def icons():
    """Original, compact 24px SVG geometry; text remains the authoritative status."""
    patterns = {
        "draft": ({0}, None), "open": ({0}, None), "assigned": ({0, 1}, None),
        "pending": ({1}, None), "offer-made": ({0, 2}, None),
        "under-offer": ({0, 1, 2}, None), "accepted": ({0, 1, 2, 3}, "check"),
        "closed": ({0, 1, 2, 3}, None), "cancelled": ({0, 1, 2}, "dot"),
        "withdrawn": ({0, 1, 2}, "minus"), "declined": ({0, 1, 2}, "cross"),
        "excluded": ({0, 1, 2}, "cross"), "inactive": ({0, 1, 2}, "dot"),
    }
    result = {}
    for key, (filled, terminal) in patterns.items():
        colour = COLOURS[key]
        pieces = []
        for ordinal, (x, y) in enumerate(((3, 3), (14, 3), (3, 14), (14, 14))):
            if ordinal == 3 and terminal in {"dot", "minus", "cross"}:
                continue
            fill = colour if ordinal in filled else "none"
            stroke = colour if ordinal in filled else "#8C8589"
            pieces.append(f'<rect x="{x}" y="{y}" width="7" height="7" rx="1" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
        if terminal == "dot":
            pieces.append(f'<circle cx="17.5" cy="17.5" r="3.5" fill="{colour}"/>')
        elif terminal == "minus":
            pieces.append(f'<path d="M14.5 17.5h6" fill="none" stroke="{colour}" stroke-width="2" stroke-linecap="round"/>')
        elif terminal == "cross":
            pieces.append(f'<path d="m14.5 14.5 6 6m0-6-6 6" fill="none" stroke="{colour}" stroke-width="2" stroke-linecap="round"/>')
        elif terminal == "check":
            pieces.append('<path d="m15.3 17.5 1.5 1.5 3-3" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>')
        result["status-" + key] = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">' + "".join(pieces) + "</svg>"
    result["status-unknown"] = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#757075" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M9 9a3 3 0 0 1 6 0c0 2-3 2-3 4M12 17h.01"/></svg>'
    return result


def resolve(formatting, value):
    """Read the saved literals for a deterministic, exact-code coverage check."""
    conditional = formatting["value"]["expr"]["Conditional"]
    probe = "null" if value is None else literal(value)["Literal"]["Value"]
    for case in conditional["Cases"]:
        condition = case["Condition"]
        inside = condition.get("In", {})
        comparison = condition.get("Comparison", {})
        labels = [entry[0].get("Literal", {}).get("Value") for entry in inside.get("Values", [])]
        if comparison:
            labels.append(comparison.get("Right", {}).get("Literal", {}).get("Value"))
        if probe in labels:
            return case["Value"]["Literal"]["Value"].strip("'")
    default = conditional.get("DefaultValue", {}).get("Literal", {}).get("Value")
    return default.strip("'") if default else None
