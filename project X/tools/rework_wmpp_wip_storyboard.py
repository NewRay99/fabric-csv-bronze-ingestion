"""Scoped, backed-up WIP report storyboard and style consolidation."""

from collections import defaultdict
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re
import shutil

from build_report_design_delivery import L, fill, field, project, obj, ident, quoted, read, save
from build_report_design_delivery import add_columns, measures, table, relation
import rebuild_mission_control_dashboard_v16 as ui

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "reports/client-deliverables/WMPP v16/SM WMPP v16 updated WIP"
REPORT = PROJECT / "SM_WMPP_v16.Report"
MODEL = PROJECT / "SM_WMPP_v16.SemanticModel/definition"
DEFINITION = REPORT / "definition"
HOME = "364f2cdd67ba7822850c"
BOARD = "5038cffdd48af9a80dd1"
REF = "78d576b289e5fe3d2af6"
SINGLE = "f3070e87127b751f89d4"
DETAIL = "4cad3706fca6451c66b8"
GEO = "f028a4be56d03e8404d7"
SNAP = "dd3a58c056d723048dbf"
RETIRED = {GEO, SNAP, "4be6f15f15a086c98c33"}
CONTAINERS = {
    "title",
    "subTitle",
    "background",
    "border",
    "dropShadow",
    "visualHeader",
    "padding",
    "stylePreset",
    "visualLink",
    "tooltip",
}


def scalar(v):
    return v.get("expr", {}).get("Literal", {}).get("Value", "") if isinstance(v, dict) else v


def native(v):
    if isinstance(v, dict):
        return {k: native(x) for k, x in v.items()}
    if isinstance(v, list):
        return [native(x) for x in v]
    if isinstance(v, bool):
        return L(str(v).lower())
    if isinstance(v, (int, float)):
        return L(str(v) + "D")
    return L(quoted(v))


def merge_entries(target, incoming):
    for entry in incoming:
        match = next((e for e in target if e.get("selector") == entry.get("selector")), None)
        if match is None:
            target.append(deepcopy(entry))
        else:
            match["properties"] = {**entry["properties"], **match["properties"]}


def main():
    marker = PROJECT / "STORYBOARD_DELIVERY.json"
    assert not marker.exists(), "Inspect the existing delivery before reapplying."
    backup = (
        PROJECT.parent / "_review" / ("wip-storyboard-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    initial_backup = PROJECT.parent / "_review/wip-storyboard-20260929-233007"
    if initial_backup.exists():
        backup = initial_backup
    else:
        shutil.copytree(PROJECT, backup, ignore=shutil.ignore_patterns(".pbi", ".git"))
    docs = {p: read(p) for p in DEFINITION.rglob("*.json")}
    original = deepcopy(docs)

    def page(pid):
        return docs[DEFINITION / "pages" / pid / "page.json"]

    def visuals(pid):
        return [
            (p, v) for p, v in docs.items() if p.name == "visual.json" and p.parents[2].name == pid
        ]

    def put(pid, v):
        docs[DEFINITION / "pages" / pid / "visuals" / v["name"] / "visual.json"] = v
        return v

    def new(pid, key, kind, x, y, w, h, title=None):
        v = ui.visual_shell(
            ident("wmpp-story:" + pid + ":" + key), kind, ui.position(x, y, w, h, 90000)
        )
        v["visual"]["visualContainerObjects"] = {
            "title": obj(
                show=L("true" if title else "false"),
                text=L(quoted(title or "")),
                fontSize=L("13D"),
                bold=L("false"),
                fontFamily=L("'Segoe UI'"),
            ),
            "background": obj(show=L("true"), color=fill("#FFFFFF"), transparency=L("0D")),
            "border": obj(show=L("true"), color=fill("#FFFFFF"), radius=L("14D")),
            "padding": obj(top=L("16D"), bottom=L("16D"), left=L("16D"), right=L("16D")),
        }
        return put(pid, v)

    def text(pid, key, label, x, y, w, h, size=18):
        v = ui.textbox(
            ident("wmpp-story:" + pid + ":" + key),
            label,
            ui.position(x, y, w, h, 91000),
            size,
            False,
        )
        return put(pid, v)

    def query(v, roles):
        v["visual"]["query"] = {"queryState": {k: {"projections": ps} for k, ps in roles.items()}}

    def tab(pid, key, title, cols, x, y, w, h, measure_name=None):
        v = new(pid, key, "tableEx", x, y, w, h, title)
        ps = [project(t, c, label=label) for t, c, label in cols]
        if measure_name:
            ps.append(project("_Story Measures", measure_name, True))
        query(v, {"Values": ps})
        v["visual"]["objects"] = {
            "columnHeaders": obj(fontSize=L("11D"), bold=L("false")),
            "values": obj(fontSize=L("11D")),
        }
        return v

    def chart(pid, key, title, kind, category, metrics, x, y, w, h):
        v = new(pid, key, kind, x, y, w, h, title)
        query(v, {"Category": [project(*category)], "Y": [project(t, n, True) for t, n in metrics]})
        return v

    def slicer(pid, key, title, t, c, x, y, w=390):
        v = new(pid, key, "slicer", x, y, w, 92, title)
        query(v, {"Values": [dict(project(t, c), active=True)]})
        v["visual"]["objects"] = {
            "data": obj(mode=L("'Dropdown'")),
            "selection": obj(singleSelect=L("false"), selectAllCheckboxEnabled=L("true")),
        }
        return v

    # Preserve IDs and display-only bookmark behaviour while moving full menus.
    order = [
        "Home",
        "Performance",
        "Referrals",
        "Offers",
        "Draft offers",
        "IPAs",
        "Providers",
        "Requirements",
    ]
    moved = 0
    retired_visuals = set()
    for pp in list(docs):
        if pp.name != "page.json":
            continue
        pid = pp.parent.name
        mains = []
        for p, v in visuals(pid):
            style = json.dumps(
                v.get("visual", {}).get("visualContainerObjects", {}).get("stylePreset", {})
            )
            if "WMPP Owner Bubble Navigation" in style:
                label = next(
                    scalar(e["properties"]["text"]).strip("'").replace(" ▾", "")
                    for e in v["visual"]["objects"]["text"]
                    if "text" in e["properties"]
                )
                mains.append((p, v, label))
        old_positions = {
            v["position"]["x"]: 860
            + 100 * next(i for i, n in enumerate(order) if n.lower() == label.lower())
            for _, v, label in mains
        }
        for p, v in visuals(pid):
            pos = v["position"]
            if pos["y"] <= 116 and pos["z"] >= 300000:
                for oldx, newx in old_positions.items():
                    if pos["x"] in (oldx, oldx - 4) and pos["width"] in (96, 104):
                        pos["x"] += newx - oldx
                        moved += 1
                        break
        for _, main, label in mains:
            props = main["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]
            target = scalar(props.get("bookmark", {})).strip("'")
            bp = DEFINITION / "bookmarks" / (target + ".bookmark.json")
            if bp not in docs or not docs[bp]["displayName"].endswith(" menu"):
                continue
            states = docs[bp]["explorationState"]["sections"][pid]["visualContainers"]
            active = [
                (p, v)
                for p, v in visuals(pid)
                if v["name"] in states
                and states[v["name"]]["singleVisual"].get("display", {}).get("mode") != "hidden"
            ]
            rows = sorted(
                [(p, v) for p, v in active if 300020 <= v["position"]["z"] <= 300030],
                key=lambda x: x[1]["position"]["y"],
            )
            kept = []
            for p, v in rows:
                rowtext = next(
                    (
                        scalar(e["properties"]["text"]).strip("'")
                        for e in v["visual"]["objects"].get("text", [])
                        if "text" in e["properties"]
                    ),
                    "",
                )
                if label == "Referrals" and any(
                    s in rowtext.lower() for s in ("geography", "snapshot", "overview", "detail")
                ):
                    retired_visuals.add(v["name"])
                    v["isHidden"] = True
                    continue
                kept.append((p, v))
            px = min(main["position"]["x"], 1346) - 12
            for i, (_, v) in enumerate(kept):
                v["position"].update(x=px + 12, y=136 + i * 44)
            for _, v in active:
                if v["position"]["z"] == 300005:
                    v["position"].update(x=px, height=24 + 44 * len(kept))
                elif v["position"]["z"] == 300006:
                    v["position"]["x"] = main["position"]["x"] - 4
        if pid in RETIRED:
            page(pid)["visibility"] = "HiddenInViewMode"
    # Remove decommissioned menu entries from every stored display state.
    for p, b in docs.items():
        if not p.name.endswith(".bookmark.json"):
            continue
        for pid, sec in b.get("explorationState", {}).get("sections", {}).items():
            for vid, state in sec.get("visualContainers", {}).items():
                if vid in retired_visuals:
                    state["singleVisual"]["display"] = {"mode": "hidden"}
    page(BOARD)["displayName"] = "Overall Performance"
    metadata = docs[DEFINITION / "pages/pages.json"]
    metadata["activePageName"] = HOME
    preferred = [HOME, BOARD, REF, SINGLE, DETAIL]
    metadata["pageOrder"] = (
        preferred
        + [p for p in metadata["pageOrder"] if p not in preferred and p not in RETIRED]
        + [p for p in RETIRED if p in metadata["pageOrder"]]
    )

    # Source fields remain intact; only add report-specific calculations.
    add_columns(
        MODEL,
        "fact_offer",
        [
            (
                "Offer activity band",
                "string",
                'VAR d = \'fact_offer\'[days_since_offer_activity] RETURN SWITCH(TRUE(), ISBLANK(d), "Unknown", d < 0, "Review", d <= 3, "0-3 days", d <= 7, "4-7 days", d <= 14, "8-14 days", "15+ days")',
                "\t\tsortByColumn: 'Offer activity band order'\n",
            ),
            (
                "Offer activity band order",
                "int64",
                "VAR d = 'fact_offer'[days_since_offer_activity] RETURN SWITCH(TRUE(), ISBLANK(d), 99, d < 0, 98, d <= 3, 1, d <= 7, 2, d <= 14, 3, 4)",
                "",
            ),
        ],
    )
    relation(
        MODEL,
        "dim_referral_provider_message",
        "referral_provider_id",
        "fact_referral_provider",
        "referral_provider_id",
    )
    provider_rows = """SELECTCOLUMNS('fact_referral_provider',
        "Referral", [referral_id], "Point ID", "P:" & [referral_provider_id], "Location type", "Assigned provider",
        "Provider", RELATED('dim_provider'[provider_name]), "Home", BLANK(), "Offer", BLANK(),
        "Address", RELATED('dim_provider'[town_city]) & ", " & RELATED('dim_provider'[county]) & ", " & RELATED('dim_provider'[postcode]),
        "Map location", IF(NOT ISBLANK(RELATED('dim_provider'[postcode])), RELATED('dim_provider'[postcode]) & ", United Kingdom"))"""
    offer_rows = """SELECTCOLUMNS('fact_offer',
        "Referral", [referral_id], "Point ID", "O:" & [offer_id], "Location type", "Offer home",
        "Provider", RELATED('dim_provider'[provider_name]), "Home", RELATED('dim_provider_home'[home_name]), "Offer", [offer_id],
        "Address", RELATED('dim_provider_home'[town_city]) & ", " & RELATED('dim_provider_home'[county]) & ", " & RELATED('dim_provider_home'[postcode]),
        "Map location", IF(NOT ISBLANK(RELATED('dim_provider_home'[postcode])), RELATED('dim_provider_home'[postcode]) & ", United Kingdom"))"""
    table(
        MODEL,
        "Referral Map Points",
        [
            (c, "string", "")
            for c in [
                "Referral",
                "Point ID",
                "Location type",
                "Provider",
                "Home",
                "Offer",
                "Address",
                "Map location",
            ]
        ],
        f"UNION({provider_rows}, {offer_rows})",
    )
    relation(MODEL, "Referral Map Points", "Referral", "fact_referral", "referral_id")
    matching = """VAR offerFilter = ISFILTERED('fact_offer'[offer_status]) || ISFILTERED('fact_offer'[Offer activity band])
VAR offerRefs = VALUES('fact_offer'[referral_id])
RETURN IF(offerFilter, CALCULATE([Referrals], KEEPFILTERS(TREATAS(offerRefs,'fact_referral'[referral_id]))), [Referrals])"""
    measures(
        MODEL,
        "_Story Measures",
        [
            ("Matching referrals", matching, "#,0"),
            (
                "Detail referral selected",
                "IF(COUNTROWS(ALLSELECTED('fact_referral')) = 1, 1, BLANK())",
                "0",
            ),
            (
                "Detail map points",
                "IF([Detail referral selected] = 1, COUNTROWS('Referral Map Points'), BLANK())",
                "#,0",
            ),
            (
                "Referrals closed during month",
                "CALCULATE(DISTINCTCOUNT('fact_referral'[referral_id]), USERELATIONSHIP('fact_referral'[referral_closed_date],'dim_date'[date]), CROSSFILTER('fact_referral'[referral_created_date],'dim_date'[date],NONE), KEEPFILTERS(NOT ISBLANK('fact_referral'[referral_closed_date])))",
                "#,0",
            ),
            (
                "Snapshot referrals previous month",
                "VAR currentMonth = SELECTEDVALUE('dim_snapshot_month'[month_start]) RETURN IF(NOT ISBLANK(currentMonth), CALCULATE([Snapshot Referrals], REMOVEFILTERS('dim_snapshot_month'), 'dim_snapshot_month'[month_start] = EDATE(currentMonth,-1)))",
                "#,0",
            ),
            (
                "Snapshot referrals MoM change",
                "VAR currentTotal = [Snapshot Referrals] VAR previousTotal = [Snapshot referrals previous month] RETURN IF(NOT ISBLANK(currentTotal) && NOT ISBLANK(previousTotal), currentTotal - previousTotal)",
                "#,0",
            ),
            (
                "Snapshot referrals MoM percent",
                "DIVIDE([Snapshot referrals MoM change],[Snapshot referrals previous month])",
                "0.0%",
            ),
        ],
    )

    # Replace only detail-page body visuals; retain header and menu IDs.
    for pid in (SINGLE, DETAIL):
        for p, v in visuals(pid):
            if v["position"]["y"] >= 120 and v["position"]["z"] < 170000:
                v["isHidden"] = True
                retired_visuals.add(v["name"])
        page(pid)["height"] = 2160 if pid == DETAIL else 1540
    text(SINGLE, "heading", "Referral Single View", 36, 150, 1500, 44, 28)
    text(
        SINGLE,
        "intro",
        "Filter the cohort, compare the breakdowns, then right-click a referral ID to drill through to Referral Detail.",
        36,
        202,
        1580,
        38,
        16,
    )
    filters = [
        ("Priority", "fact_referral", "priority"),
        ("Framework category", "Referral Category", "Category"),
        ("Current status", "fact_referral", "current_status"),
        ("Placement urgency band (under review)", "fact_referral", "placement_urgency_band"),
        ("Open referral", "fact_referral", "is_open"),
        ("Open and overdue", "fact_referral", "is_open_overdue"),
        ("Offer status", "fact_offer", "offer_status"),
        ("Days since offer activity", "fact_offer", "Offer activity band"),
    ]
    for i, (label, t, c) in enumerate(filters):
        slicer(SINGLE, "filter-" + str(i), label, t, c, 36 + (i % 4) * 408, 252 + (i // 4) * 108)
    chart(
        SINGLE,
        "priority",
        "Referrals by priority",
        "clusteredBarChart",
        ("fact_referral", "priority"),
        [("_Story Measures", "Matching referrals")],
        36,
        480,
        520,
        280,
    )
    chart(
        SINGLE,
        "status",
        "Referrals by current status",
        "clusteredBarChart",
        ("fact_referral", "current_status"),
        [("_Story Measures", "Matching referrals")],
        580,
        480,
        520,
        280,
    )
    chart(
        SINGLE,
        "category",
        "Referrals by framework category",
        "clusteredBarChart",
        ("Referral Category", "Category"),
        [("_Story Measures", "Matching referrals")],
        1124,
        480,
        520,
        280,
    )
    text(
        SINGLE,
        "category-note",
        "A referral can belong to several framework categories; category totals are not additive. Offer filters return referrals with at least one matching offer.",
        36,
        775,
        1590,
        42,
        14,
    )
    tab(
        SINGLE,
        "referrals",
        "Referral results — right-click Referral ID → Drill through → Referral Detail",
        [
            ("fact_referral", "referral_id", "Referral ID"),
            ("fact_referral", "priority", "Priority"),
            ("fact_referral", "current_status", "Current status"),
            ("fact_referral", "placement_urgency_band", "Urgency band"),
            ("fact_referral", "is_open", "Open"),
            ("fact_referral", "is_open_overdue", "Overdue"),
            ("fact_referral", "referral_created_date", "Created"),
            ("fact_referral", "required_placement_date", "Required placement"),
        ],
        36,
        832,
        1608,
        520,
        "Matching referrals",
    )
    text(
        SINGLE,
        "band-note",
        "Activity bands: 0–3, 4–7, 8–14, 15+ days. Missing values stay Unknown; negative values are flagged Review. Priority and urgency remain separate until agreed.",
        36,
        1370,
        1608,
        60,
        14,
    )

    text(DETAIL, "heading", "Referral Detail", 36, 150, 1300, 44, 28)
    text(
        DETAIL,
        "intro",
        "One referral: details → provider messages → lifecycle → offers and homes → provider and offer locations. Use Back to return to your filtered results.",
        36,
        202,
        1608,
        42,
        16,
    )
    # Existing native drillthrough binding to fact_referral.referral_id is retained.
    slicer(DETAIL, "referral", "Referral ID", "fact_referral", "referral_id", 36, 250, 520)
    docs[
        DEFINITION
        / "pages"
        / DETAIL
        / "visuals"
        / ident("wmpp-story:" + DETAIL + ":referral")
        / "visual.json"
    ]["visual"]["objects"]["selection"] = obj(singleSelect=L("true"))
    tab(
        DETAIL,
        "summary",
        "Referral details",
        [
            ("fact_referral", c, l)
            for c, l in [
                ("referral_id", "Referral ID"),
                ("priority", "Priority"),
                ("placement_urgency_band", "Urgency"),
                ("current_status", "Status"),
                ("referral_created_date", "Created"),
                ("required_placement_date", "Required placement"),
                ("referral_closed_date", "Closed"),
                ("referral_closure_reason", "Closure reason"),
            ]
        ],
        36,
        370,
        1608,
        180,
        "Detail referral selected",
    )
    tab(
        DETAIL,
        "messages",
        "Provider messages",
        [
            ("dim_referral_provider_message", c, l)
            for c, l in [
                ("created_timestamp", "Sent"),
                ("created_by", "Sender"),
                ("referral_provider_id", "Provider assignment"),
                ("message_text", "Message"),
                ("message_read_timestamp", "Read at"),
            ]
        ],
        36,
        574,
        960,
        310,
        "Detail referral selected",
    )
    tab(
        DETAIL,
        "lifecycle",
        "Referral lifecycle events",
        [
            ("fact_referral_lifecycle_event", c, l)
            for c, l in [
                ("sequence_number", "Sequence"),
                ("event_timestamp", "Time"),
                ("event_type", "Event"),
                ("created_by", "Actor"),
            ]
        ],
        1020,
        574,
        624,
        310,
        "Detail referral selected",
    )
    tab(
        DETAIL,
        "offers",
        "Offers and proposed provider homes",
        [
            ("fact_offer", "offer_id", "Offer ID"),
            ("dim_provider", "provider_name", "Provider"),
            ("dim_provider_home", "home_name", "Home"),
            ("dim_provider_home", "postcode", "Home postcode"),
            ("fact_offer", "offer_status", "Status"),
            ("fact_offer", "estimated_weekly_cost", "Estimated weekly cost"),
            ("fact_offer", "Offer activity band", "Activity band"),
        ],
        36,
        908,
        1608,
        320,
        "Detail referral selected",
    )
    mp = new(
        DETAIL,
        "map",
        "azureMap",
        36,
        1252,
        1040,
        510,
        "Assigned providers and offer homes — postcode locations",
    )
    query(
        mp,
        {
            "Category": [project("Referral Map Points", "Location type")],
            "Location": [project("Referral Map Points", "Map location")],
            "Size": [project("_Story Measures", "Detail map points", True)],
            "Tooltips": [
                project("Referral Map Points", c) for c in ["Provider", "Home", "Offer", "Address"]
            ],
        },
    )
    mp["visual"]["objects"] = {
        "legend": obj(show=L("true")),
        "bubbleLayer": obj(show=L("true")),
        "dataPoint": [
            {
                "properties": {"fill": fill(colour)},
                "selector": {
                    "data": [
                        {
                            "scopeId": {
                                "Comparison": {
                                    "ComparisonKind": 0,
                                    "Left": field("Referral Map Points", "Location type"),
                                    "Right": {"Literal": {"Value": quoted(label)}},
                                }
                            }
                        }
                    ]
                },
            }
            for label, colour in [("Assigned provider", "#4DAAAB"), ("Offer home", "#EF7911")]
        ],
    }
    tab(
        DETAIL,
        "addresses",
        "Provider / offer location directory",
        [
            ("Referral Map Points", c, c)
            for c in ["Location type", "Provider", "Home", "Offer", "Address"]
        ],
        1100,
        1252,
        544,
        510,
        "Detail map points",
    )
    text(
        DETAIL,
        "map-note",
        "Teal: assigned provider office. Orange: offered home. Postcode-level locations are approximate; missing postcodes remain in the directory but cannot be plotted. Markers may overlap.",
        36,
        1780,
        1608,
        62,
        14,
    )
    tab(
        DETAIL,
        "assignments",
        "Referral-provider assignments",
        [
            ("fact_referral_provider", "referral_provider_id", "Assignment ID"),
            ("dim_provider", "provider_name", "Provider"),
            ("dim_provider", "town_city", "Town"),
            ("dim_provider", "postcode", "Postcode"),
            ("fact_referral_provider", "provider_response_status", "Response"),
            ("fact_referral_provider", "is_declined", "Declined"),
        ],
        36,
        1860,
        1608,
        260,
        "Detail referral selected",
    )

    # Add performance progress and cost panels below the existing executive view.
    page(BOARD)["height"] = 1950
    text(BOARD, "progress-heading", "Monthly progress and cost breakdown", 36, 1090, 1550, 40, 26)
    chart(
        BOARD,
        "snapshots",
        "Month-end snapshot: total referrals and closed states",
        "lineChart",
        ("dim_snapshot_month", "month_start"),
        [
            ("_Measures", "Snapshot Referrals"),
            ("_Measures", "Closed or Cancelled Referrals at Snapshot"),
        ],
        36,
        1150,
        1020,
        330,
    )
    chart(
        BOARD,
        "cost",
        "Estimated active weekly cost by placement type",
        "clusteredBarChart",
        ("fact_referral", "placement_type_required"),
        [("_Measures", "Estimated Active Weekly Cost")],
        1080,
        1150,
        564,
        330,
    )
    tab(
        BOARD,
        "mom",
        "Monthly snapshot comparison",
        [("dim_snapshot_month", "year_month", "Snapshot month")],
        36,
        1540,
        1020,
        290,
    )
    mom = docs[
        DEFINITION
        / "pages"
        / BOARD
        / "visuals"
        / ident("wmpp-story:" + BOARD + ":mom")
        / "visual.json"
    ]
    mom["visual"]["query"]["queryState"]["Values"]["projections"] += [
        project(t, n, True)
        for t, n in [
            ("_Measures", "Snapshot Referrals"),
            ("_Measures", "Closed or Cancelled Referrals at Snapshot"),
            ("_Story Measures", "Snapshot referrals MoM change"),
            ("_Story Measures", "Snapshot referrals MoM percent"),
        ]
    ]
    chart(
        BOARD,
        "closed-flow",
        "Referrals closed during each month",
        "lineChart",
        ("dim_date", "year_month"),
        [("_Story Measures", "Referrals closed during month")],
        1080,
        1540,
        564,
        290,
    )
    text(
        BOARD,
        "definitions",
        "Snapshot closed states include closed, cancelled, withdrawn and completed. Closure flow uses the recorded closure date. Costs are estimated weekly liability, not total spend. Missing snapshots are not fabricated.",
        36,
        1850,
        1608,
        70,
        14,
    )
    # Landing-page storyboard with native page-navigation buttons.
    for i, (title, description, destination) in enumerate(
        [
            (
                "1 · Overall Performance",
                "Start with outcomes, estimated weekly costs and month-on-month referral progress.",
                BOARD,
            ),
            (
                "2 · Referrals",
                "Review current demand, open referrals, offer engagement and overdue work.",
                REF,
            ),
            (
                "3 · Referral Single View",
                "Filter the cohort and drill into one referral, its messages, events, offers and locations.",
                SINGLE,
            ),
        ]
    ):
        x = 60 + i * 540
        b = new(HOME, "start-" + str(i), "actionButton", x, 570, 500, 86)
        b["visual"]["objects"] = {
            "text": obj(show=L("true"), text=L(quoted(title)), bold=L("false"), fontSize=L("16D")),
            "fill": obj(show=L("true"), fillColor=fill("#FFFFFF")),
        }
        b["visual"]["visualContainerObjects"]["visualLink"] = obj(
            show=L("true"), type=L("'PageNavigation'"), navigationSection=L(quoted(destination))
        )
        text(HOME, "start-description-" + str(i), description, x + 16, 680, 468, 118, 18)

    # Retired body content stays recoverable but cannot be reopened by bookmarks.
    for p, b in docs.items():
        if not p.name.endswith(".bookmark.json"):
            continue
        for sec in b.get("explorationState", {}).get("sections", {}).values():
            for vid, state in sec.get("visualContainers", {}).items():
                if vid in retired_visuals:
                    state["singleVisual"]["display"] = {"mode": "hidden"}

    # Consolidate common properties into one named style per visual family.
    theme_path = REPORT / "StaticResources/RegisteredResources/WMPP_Theme.json"
    theme = read(theme_path)
    styles = theme["visualStyles"]
    used = defaultdict(set)
    for p, v in docs.items():
        vis = v.get("visual", {}) if p.name == "visual.json" else {}
        entries = vis.get("visualContainerObjects", {}).get("stylePreset", [])
        if entries:
            used[vis["visualType"]].add(scalar(entries[0]["properties"]["name"]).strip("'"))
    mapping = {}
    canonical = {}
    before = sum(len(x) - int("*" in x) for x in styles.values())
    readable = {
        "cardVisual": "KPI Card",
        "tableEx": "Detail Table",
        "pivotTable": "Matrix",
        "textbox": "Text",
        "actionButton": "Navigation Button",
        "azureMap": "Location Map",
        "slicer": "Filter",
        "clusteredBarChart": "Bar Chart",
        "clusteredColumnChart": "Column Chart",
        "lineChart": "Trend Chart",
        "donutChart": "Donut Chart",
        "image": "Icon",
        "shape": "Panel",
    }
    for kind, names in used.items():
        valid = [n for n in sorted(names) if n in styles.get(kind, {})]
        if not valid:
            continue
        common = deepcopy(styles[kind][valid[0]])
        for object_name, entries in list(common.items()):
            kept = []
            for e in entries:
                matchers = [
                    next(
                        (
                            z
                            for z in styles[kind][name].get(object_name, [])
                            if z.get("$id") == e.get("$id")
                        ),
                        {},
                    )
                    for name in valid
                ]
                props = {
                    k: x
                    for k, x in e.items()
                    if k != "$id" and all(z.get(k) == x for z in matchers)
                }
                if props:
                    if "$id" in e:
                        props["$id"] = e["$id"]
                    kept.append(props)
            if kept:
                common[object_name] = kept
            else:
                common.pop(object_name)
        name = "WMPP " + readable.get(kind, re.sub(r"([a-z])([A-Z])", r"\1 \2", kind).title())
        canonical[kind] = (name, common)
        for old in valid:
            mapping[(kind, old)] = name
    for p, v in docs.items():
        if p.name != "visual.json":
            continue
        vis = v.get("visual", {})
        kind = vis.get("visualType")
        containers = vis.get("visualContainerObjects", {})
        entries = containers.get("stylePreset", [])
        if not entries:
            continue
        old = scalar(entries[0]["properties"]["name"]).strip("'")
        if (kind, old) not in mapping:
            continue
        # Retain only differences from the shared family; local overrides win.
        for role, theme_entries in styles[kind][old].items():
            target = containers if role in CONTAINERS else vis.setdefault("objects", {})
            incoming = []
            for e in theme_entries:
                common_entry = next(
                    (z for z in canonical[kind][1].get(role, []) if z.get("$id") == e.get("$id")),
                    {},
                )
                entry = {
                    "properties": {
                        k: native(x)
                        for k, x in e.items()
                        if k != "$id" and (k not in common_entry or common_entry[k] != x)
                    }
                }
                if not entry["properties"]:
                    continue
                if "$id" in e:
                    entry["selector"] = {"id": e["$id"]}
                incoming.append(entry)
            merge_entries(target.setdefault(role, []), incoming)
        containers["stylePreset"] = obj(name=L(quoted(mapping[(kind, old)])))
    # Do not retain unused hash-named choices in the style picker.
    for kind in list(styles):
        base = {"*": styles[kind]["*"]} if "*" in styles[kind] else {}
        if kind in canonical:
            name, common = canonical[kind]
            base[name] = common
        styles[kind] = base
    theme["name"] = "WMPP WIP — Shared Styles"
    save(theme_path, theme)
    save(PROJECT / "WMPP_Theme.json", theme)
    for p, v in docs.items():
        if v != original.get(p):
            save(p, v)
    save(
        PROJECT / "STYLE_MIGRATION.json",
        {
            "before": before,
            "after": len(canonical),
            "mappings": [
                {"visualType": k, "old": n, "new": new} for (k, n), new in mapping.items()
            ],
            "strategy": "Common shared family style; differing formatting retained as explicit per-visual overrides.",
        },
    )
    result = {
        "backup": str(backup),
        "style_presets_before": before,
        "style_presets_after": len(canonical),
        "moved_navigation_visuals": moved,
        "retired_visuals": len(retired_visuals),
        "new_visuals": sum(p not in original for p in docs),
        "changed_definition_files": sum(v != original.get(p) for p, v in docs.items()),
        "desktop_render_verified": False,
        "data_refresh_performed": False,
    }
    save(marker, result)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
