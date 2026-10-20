"""Restore native Board Dashboard annotations without the decorative SVG skin."""

from datetime import datetime
import hashlib
from pathlib import Path
import shutil

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
import rebuild_mission_control_dashboard_v16 as ui


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "reports/client-deliverables/WMPP v16"
REPORT = BUNDLE / "SM WMPP v16 updated/SM_WMPP_v16.Report"
BOARD = "5038cffdd48af9a80dd1"
GUIDE = ident("board-native-annotation-guide")
INK, MUTED = "#2B2427", "#61575C"

KPIS = [
    (
        "Referrals Created",
        "Selected referral-created cohort",
        "Distinct referral IDs under the current filters. The reporting-period selector filters referral creation dates; this is not a count of all activity occurring during that month.",
    ),
    (
        "Open Referrals",
        "Current status within selection",
        "Distinct referrals where is_open is true, within the selected cohort. This is current recorded status, not a historical month-end snapshot.",
    ),
    (
        "Placed by Target",
        "IPA on or before required date",
        "Referrals flagged placed_by_required_date divided by referrals with both an IPA-issued date and required placement date. It is not a success rate across all referrals; missing dates affect eligibility.",
    ),
    (
        "Critical Overdue",
        "Open critical referrals past target",
        "Referrals flagged is_open_overdue, restricted to the Critical urgency band. This uses the model's overdue flag and recorded reporting state, not a live countdown.",
    ),
    (
        "Median Days to IPA",
        "Nonblank recorded referral durations",
        "Median of nonblank days_to_ipa across the filtered referrals. Missing durations are excluded, not treated as zero. This is the median, not the average.",
    ),
    (
        "Est. Weekly Cost",
        "Active weekly liability; not total spend",
        "Sum of estimated_weekly_cost for IPA records where is_placement_closed is false, under applicable model filters. This is estimated active weekly liability, not invoiced spend or total placement cost.",
    ),
]

CHARTS = [
    (
        "Referrals by Urgency Band",
        "Number of referrals in each urgency band",
        "Distinct referrals grouped by recorded placement urgency within the current selection. Compare caseload distribution, not rates of placement success.",
    ),
    (
        "Target Hit Rate by Urgency",
        "Eligible referrals placed on or before target",
        "The Placement Target Hit Rate measure split by urgency. The denominator requires both IPA-issued and required-placement dates. Compare rates with care where the eligible cohort is small.",
    ),
    (
        "Open Referrals by Target Status",
        "Open referrals against required placement date",
        "Open referrals grouped by the model's target-status classification. The target is the required placement date. Missing target dates are not evidence of an on-time placement.",
    ),
    (
        "Referrals by Region",
        "Unavailable: a governed region source is needed",
        "No governed region field is available for this breakdown. No regional figures or inferred mappings are presented. Referral preference cities on other pages are not a substitute for a governed region classification.",
    ),
    (
        "Referral Outcome Mix",
        "Distribution of recorded referral status",
        "Distinct referrals grouped by current_status in the selected cohort. This shows current recorded outcomes; it is not a transition history or a same-month conversion rate.",
    ),
    (
        "Provider Offers vs Accepted",
        "Offers made and accepted, grouped by provider",
        "Distinct offers by provider, compared with offers whose status is accepted, approved, selected or offer_successful. Accepted offers are not necessarily issued IPAs and are not a same-month conversion of new referrals.",
    ),
]


def shell(key, kind, pos):
    value = ui.visual_shell(ident("board-annotation:" + key), kind, ui.position(*pos, 50000))
    containers = {
        k: obj(show=L("false"))
        for k in ("background", "border", "dropShadow", "title", "subTitle", "visualHeader")
    }
    containers["padding"] = obj(top=L("0D"), bottom=L("0D"), left=L("0D"), right=L("0D"))
    containers["general"] = obj(altText=L(quoted(key)))
    value["visual"]["visualContainerObjects"] = containers
    return value


def text(key, words, pos, size=14, bold=False, color=INK):
    value = shell(key, "textbox", pos)
    value["visual"]["objects"] = {
        "general": obj(
            paragraphs=[
                {
                    "textRuns": [
                        {
                            "value": words,
                            "textStyle": {
                                "fontFamily": "Segoe UI",
                                "fontSize": f"{size}px",
                                "fontWeight": "bold" if bold else "normal",
                                "color": color,
                            },
                        }
                    ]
                }
            ]
        )
    }
    return value


def button(key, label, description, pos, destination=GUIDE):
    value = shell(key, "actionButton", pos)
    value["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted(description)))
    value["visual"]["visualContainerObjects"]["visualLink"] = obj(
        show=L("true"),
        type=L("'PageNavigation'"),
        navigationSection=L(quoted(destination)),
        tooltip=L(quoted(description)),
    )
    value["visual"]["objects"] = {
        k: obj(show=L("false")) for k in ("fill", "outline", "icon", "shadow", "glow")
    }
    value["visual"]["objects"]["text"] = [
        {
            "selector": {"id": "default"},
            "properties": {
                "show": L("true"),
                "text": L(quoted(label)),
                "fontFamily": L("'Segoe UI'"),
                "fontSize": L("11D"),
                "bold": L("true"),
                "fontColor": fill(INK),
                "horizontalAlignment": L("'center'"),
                "verticalAlignment": L("'middle'"),
            },
        }
    ]
    return value


def put(page_id, value):
    save(REPORT / "definition/pages" / page_id / "visuals" / value["name"] / "visual.json", value)


def main():
    board = REPORT / "definition/pages" / BOARD
    backup = BUNDLE / "_review" / ("board-annotations-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True, exist_ok=False)
    shutil.copytree(board, backup / "board")
    shutil.copy2(REPORT / "definition/pages/pages.json", backup / "pages.json")
    model = REPORT.parent / "SM_WMPP_v16.SemanticModel"
    hashes = {
        p: hashlib.sha256(p.read_bytes()).hexdigest() for p in model.rglob("*") if p.is_file()
    }

    for key, words, pos, size, bold in [
        ("heading", "FOSTER PLACEMENT PERFORMANCE", (96, 24, 660, 38), 28, True),
        ("page-title", "Board Dashboard", (96, 65, 660, 30), 20, True),
        ("as-of", "Data as of", (96, 99, 64, 22), 12, False),
    ]:
        put(BOARD, text(key, words, pos, size, bold))
    intro = "Board overview of the selected referral-created cohort and current recorded outcomes. Hover the i buttons for definitions, or select one to open the full guide."
    put(BOARD, button("overview-info", "i", intro, (780, 35, 32, 32)))
    for i, (title, caption, detail) in enumerate(KPIS):
        x = 24 + i * 272
        put(BOARD, text("kpi-label-" + str(i), title, (x + 98, 200, 166, 27), 14, True))
        put(BOARD, text("kpi-caption-" + str(i), caption, (x + 98, 229, 166, 38), 11, False, MUTED))
        put(BOARD, button("kpi-info-" + str(i), "i", detail, (x + 39, 201, 28, 28)))
    for i, (title, caption, detail) in enumerate(CHARTS):
        x, y = 24 + i % 3 * 552, 276 if i < 3 else 592
        put(BOARD, text("chart-title-" + str(i), title, (x + 20, y + 10, 350, 30), 18, True))
        put(
            BOARD,
            text("chart-caption-" + str(i), caption, (x + 20, y + 43, 488, 32), 12, False, MUTED),
        )
        put(BOARD, button("chart-info-" + str(i), "i", detail, (x + 390, y + 10, 28, 28)))
    put(
        BOARD,
        text(
            "region-unavailable",
            "Region breakdown not yet available",
            (85, 738, 400, 32),
            18,
            True,
            MUTED,
        ),
    )
    put(
        BOARD,
        text(
            "region-explanation",
            "A governed region field is needed; no sample or inferred regional counts are shown.",
            (85, 778, 400, 60),
            14,
            False,
            MUTED,
        ),
    )

    # The hidden skin also carried labels for existing transparent controls.
    # Restore visible labels without changing their navigation/bookmark actions.
    for path in board.glob("visuals/*/visual.json"):
        value = read(path)
        visual = value["visual"]
        if visual["visualType"] != "actionButton":
            continue
        label = (
            visual.get("visualContainerObjects", {})
            .get("general", [{}])[0]
            .get("properties", {})
            .get("altText", {})
            .get("expr", {})
            .get("Literal", {})
            .get("Value", "")
            .strip("'")
        )
        visible = (
            "Chart"
            if label.startswith("Show chart for ")
            else "Table"
            if label.startswith("Show table for ")
            else {"Go to Board": "Board", "Go to Supply": "Supply", "Go to Target": "Targets"}.get(
                label
            )
        )
        if visible:
            visual.setdefault("objects", {})["text"] = [
                {
                    "selector": {"id": "default"},
                    "properties": {
                        "show": L("true"),
                        "text": L(quoted(visible)),
                        "fontFamily": L("'Segoe UI'"),
                        "fontSize": L("8D" if visible in ("Chart", "Table") else "10D"),
                        "fontColor": fill(INK),
                        "horizontalAlignment": L("'center'"),
                        "verticalAlignment": L("'middle'"),
                    },
                }
            ]
            save(path, value)

    guide = ui.page_json(GUIDE, "Board Dashboard - guide", 945, 1680)
    guide["visibility"] = "HiddenInViewMode"
    guide["objects"] = {"background": obj(color=fill("#F8F5F1"), transparency=L("0D"))}
    save(REPORT / "definition/pages" / GUIDE / "page.json", guide)
    put(
        GUIDE,
        text(
            "guide-title", "Board Dashboard | how to read this page", (36, 24, 1350, 44), 28, True
        ),
    )
    put(
        GUIDE,
        text(
            "guide-intro",
            intro
            + " The definitions describe the saved measures, not a new calculation or a refresh confirmation.",
            (36, 76, 1590, 48),
            15,
            False,
            MUTED,
        ),
    )
    for i, (left, right) in enumerate(zip(KPIS, CHARTS)):
        for column, (title, _, detail) in enumerate((left, right)):
            x, y = 36 + column * 820, 148 + i * 120
            put(GUIDE, text(f"guide-title-{column}-{i}", title, (x, y, 776, 30), 19, True))
            put(
                GUIDE,
                text(f"guide-body-{column}-{i}", detail, (x, y + 35, 776, 77), 15, False, MUTED),
            )
    put(
        GUIDE,
        button(
            "guide-back",
            "Back to Board Dashboard",
            "Return to the Board Dashboard",
            (36, 896, 260, 36),
            BOARD,
        ),
    )
    metadata_path = REPORT / "definition/pages/pages.json"
    metadata = read(metadata_path)
    if GUIDE not in metadata["pageOrder"]:
        metadata["pageOrder"].append(GUIDE)
    save(metadata_path, metadata)
    assert all(hashlib.sha256(p.read_bytes()).hexdigest() == h for p, h in hashes.items())
    print("Added native Board headings/captions, 13 explanatory buttons and a hidden guide page.")
    print("Semantic model unchanged. Before-edit page backup:", backup)


if __name__ == "__main__":
    main()
