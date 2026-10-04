"""Backed-up local WIP journey improvements and provider scoring evidence.

No composite policy, RAG thresholds, refresh, publication or source-data changes.
"""

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil

import repair_wmpp_explorer_scope as core
from build_report_design_delivery import field, ident, L, obj, project, quoted
import rebuild_mission_control_dashboard_v16 as ui
from audit_wmpp_report_journeys import inventory, scalar
from wmpp_drillthrough_button_style import style_button

MT = "_Report Journey Measures"
SCORING = "Provider Scoring Evidence"
PROVIDER = core.PROVIDER
REFERRAL = core.REFERRAL
PD = core.PROVIDER_DETAIL
RD = core.REFERRAL_DETAIL
SCORE_ROWS = [
    (
        "Response",
        "Qualifying response rate",
        "Qualifying responses / assignment-cohort opportunities; offers or recorded reasons, not message volume",
    ),
    (
        "Conversion",
        "Accepted offer share",
        "Accepted / offer records attributed to assignment cohorts; Gold includes draft records in its offer component",
    ),
    (
        "Target",
        "Placed by target share",
        "Placed by target / referrals with an accepted offer; recorded target outcome, not independently confirmed admission",
    ),
    (
        "Speed",
        "Median response hours",
        "Assignment-level median elapsed minutes / 60; not a business-calendar SLA score",
    ),
    (
        "Documents",
        "Required document compliance",
        "Not scored: required-document rules and home-ID contract approval are missing",
    ),
    (
        "Feedback",
        "Officer feedback",
        "Not scored: structured moderated ratings are unavailable; message sentiment is excluded",
    ),
    (
        "Handling",
        "Decline and closure handling",
        "Not scored: business-owned reason attribution is not approved",
    ),
    (
        "Cost",
        "Comparable cost",
        "Not scored: comparable service cohorts, fee completeness and minimum samples are not approved",
    ),
    (
        "Overall",
        "Overall provider score",
        "Not approved: no composite weights, minimum samples, version or quality-of-care rating",
    ),
]


def is_provider_detail_navigation_bookmark(bookmark):
    """Identify a record navigation target, not a page-local display menu."""
    return (
        bookmark.get("explorationState", {}).get("activeSection") == PD
        and not bookmark.get("options", {}).get("suppressActiveSection", False)
    )


def definitions():
    result = []

    def add(name, dax, fmt="#,0"):
        if isinstance(dax, tuple):
            dax, fmt = dax
        result.append((name, dax, fmt))

    add(
        "Provider unanswered assignments",
        core.scope_provider(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == FALSE() && NOT ISBLANK('fact_referral_provider'[assigned_at]))))"
        ),
    )
    add(
        "Provider response durations recorded",
        core.scope_provider(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[response_elapsed_minutes]))))"
        ),
    )
    add(
        "Provider response timing coverage",
        "DIVIDE([Provider response durations recorded],[Explorer provider qualifying responses])",
        "0.0%",
    )
    add(
        "Provider QA flagged homes",
        core.scope_provider(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('dim_provider_home'[provider_home_id]),0), KEEPFILTERS('dim_provider_home'[qa_flag] == TRUE()))"
        ),
    )
    add(
        "Provider no recorded activity",
        core.scope_provider(
            "COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), CALCULATE(COUNTROWS('fact_referral_provider')) = 0 && CALCULATE(COUNTROWS('fact_offer')) = 0 && CALCULATE(COUNTROWS('dim_referral_provider_message')) = 0))"
        ),
    )
    for name, predicate in [
        (
            "Referral open without offers",
            "'fact_referral'[is_open] == TRUE() && CALCULATE(COUNTROWS('fact_offer')) = 0",
        ),
        (
            "Referral open without assignments",
            "'fact_referral'[is_open] == TRUE() && CALCULATE(COUNTROWS('fact_referral_provider')) = 0",
        ),
        (
            "Referral accepted without IPA",
            f"CALCULATE(COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {core.ACCEPTED}))) > 0 && CALCULATE(COUNTROWS('fact_ipa')) = 0",
        ),
    ]:
        add(
            name,
            core.scope_referral(
                f"COUNTROWS(FILTER(VALUES('fact_referral'[referral_id]), CALCULATE(COUNTROWS(FILTER('fact_referral', {predicate}))) > 0))"
            ),
        )
    add(
        "Referral open overdue share",
        "DIVIDE([Explorer referrals open overdue],[Explorer referrals open])",
        "0.0%",
    )
    add(
        "Referral IPAs awaiting signatures",
        core.scope_referral(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(FILTER('fact_ipa', NOT('fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE()))))"
        ),
    )
    add(
        "Provider scoring cohort months",
        core.scope_provider("DISTINCTCOUNTNOBLANK('fact_provider_kpi_monthly'[assignment_month])"),
    )
    add(
        "Provider scoring median response hours",
        "DIVIDE([Explorer provider median response minutes],60)",
        "0.0",
    )
    add(
        "Provider scoring result",
        """VAR scoringOrdinal = SELECTEDVALUE('Provider Scoring Evidence'[Ordinal])
VAR opportunities = [Explorer Gold opportunities]
VAR offers = [Explorer Gold offers]
VAR successes = [Explorer Gold successful referrals]
RETURN SWITCH(scoringOrdinal,
0, IF(opportunities > 0, FORMAT([Explorer Gold response rate],"0.0%"), "Insufficient evidence"),
1, IF(offers > 0, FORMAT([Explorer Gold offer acceptance rate],"0.0%"), "Insufficient evidence"),
2, IF(successes > 0, FORMAT([Explorer Gold target placement rate],"0.0%"), "Insufficient evidence"),
3, IF(ISBLANK([Provider scoring median response hours]), "Insufficient evidence", FORMAT([Provider scoring median response hours],"0.0") & " h"),
8, "Not approved", "Not scored")""",
        "",
    )
    add(
        "Provider scoring numerator",
        """SWITCH(SELECTEDVALUE('Provider Scoring Evidence'[Ordinal]),
0,[Explorer Gold responses],1,[Explorer Gold accepted offers],2,[Explorer Gold placed by target],3,[Provider response durations recorded],BLANK())""",
    )
    add(
        "Provider scoring denominator",
        """SWITCH(SELECTEDVALUE('Provider Scoring Evidence'[Ordinal]),
0,[Explorer Gold opportunities],1,[Explorer Gold offers],2,[Explorer Gold successful referrals],3,[Explorer provider qualifying responses],BLANK())""",
    )
    add(
        "Provider scoring evidence status",
        """VAR scoringOrdinal = SELECTEDVALUE('Provider Scoring Evidence'[Ordinal])
VAR denominator = [Provider scoring denominator]
VAR versions = CONCATENATEX(VALUES('fact_provider_kpi_monthly'[kpi_rule_version]),'fact_provider_kpi_monthly'[kpi_rule_version],", ")
RETURN SWITCH(TRUE(), scoringOrdinal = 8, "Policy approval required", scoringOrdinal > 3, "Evidence or policy missing",
scoringOrdinal = 3, "Activity-level timing; no SLA threshold",
ISBLANK(denominator) || denominator = 0, "No eligible cohort evidence",
"Assignment cohort | " & FORMAT([Provider scoring cohort months],"0") & " month(s) | " & COALESCE(versions,"Rule unknown"))""",
        "",
    )
    for name, key, text in [
        ("Provider selection context", "'dim_provider'[provider_id]", "provider"),
        ("Referral selection context", "'fact_referral'[referral_id]", "referral"),
    ]:
        count = "[Explorer providers]" if text == "provider" else "[Explorer referrals]"
        add(
            name,
            f'VAR n = {count} RETURN IF(n = 0,"No matching {text}s - clear a filter or stage", IF(HASONEVALUE({key}),"Selected {text}: " & SELECTEDVALUE({key}),FORMAT(n,"#,0") & " matching {text}s - select a row to open detail"))',
            "",
        )
    for prefix, key, measures in [
        (
            "Provider",
            "'dim_provider'[provider_id]",
            [
                "Explorer provider homes",
                "Explorer provider offers made",
                "Explorer provider messages",
                "Provider unanswered assignments",
            ],
        ),
        (
            "Referral",
            "'fact_referral'[referral_id]",
            [
                "Explorer referral offers",
                "Explorer referral assignments",
                "Explorer referral messages",
                "Referral IPAs awaiting signatures",
            ],
        ),
    ]:
        for measure in measures:
            add(prefix + " detail headline " + measure, f"IF(HASONEVALUE({key}),[{measure}])")
    for suffix in ["result", "numerator", "denominator", "evidence status"]:
        fmt = "#,0" if suffix in {"numerator", "denominator"} else ""
        add(
            "Provider detail scoring " + suffix,
            f"IF(HASONEVALUE('dim_provider'[provider_id]),[Provider scoring {suffix}])",
            fmt,
        )
    add("Requirements catalogued", "DISTINCTCOUNTNOBLANK('ref_RID'[Req ID])")
    add(
        "Requirements linked to KPIs",
        "COUNTROWS(INTERSECT(VALUES('ref_RID'[Req ID]), VALUES('ref_KPI_RID_Linkage'[Req ID])))",
    )
    add("KPIs catalogued", "DISTINCTCOUNTNOBLANK('ref_KPI'[KPI ID])")
    return result


PROVIDER_EXTRA = [
    (
        "Action",
        "Assignments without qualifying response",
        "Provider unanswered assignments",
        "Recorded no-response assignments with a start time; not an SLA failure count",
    ),
    (
        "Evidence",
        "Response timing coverage",
        "Provider response timing coverage",
        "Qualifying responses with an elapsed duration / qualifying responses",
    ),
    (
        "Directory",
        "QA flagged homes",
        "Provider QA flagged homes",
        "Current home QA flag only; not a quality-of-care score",
    ),
    (
        "Directory",
        "Providers without recorded activity",
        "Provider no recorded activity",
        "No assignment, offer or message records in the current context",
    ),
]
REFERRAL_EXTRA = [
    (
        "Action",
        "Open referrals without offers",
        "Referral open without offers",
        "Open referrals with no offer records, including no drafts",
    ),
    (
        "Action",
        "Open referrals without assignments",
        "Referral open without assignments",
        "Open referrals with no referral-provider assignment records",
    ),
    (
        "Action",
        "Accepted offer but no IPA",
        "Referral accepted without IPA",
        "Referrals with accepted offer evidence and no IPA record",
    ),
    (
        "Action",
        "IPAs awaiting either signature",
        "Referral IPAs awaiting signatures",
        "Distinct IPAs without both signatures on the same IPA; missing signature evidence is included",
    ),
    (
        "Action",
        "Open overdue share",
        "Referral open overdue share",
        "Open overdue referrals / open referrals in the same selection",
    ),
]


def title(v, text):
    v["visual"].setdefault("visualContainerObjects", {})["title"] = obj(
        show=L("true"), text=L(quoted(text)), fontSize=L("13D"), bold=L("false")
    )


def headline(pid, measures, y, detail=False):
    cols = []
    for measure, label in measures:
        table = MT if measure.startswith(("Provider ", "Referral ")) else core.MT
        if detail:
            prefix = "Provider" if pid == PD else "Referral"
            measure = prefix + " detail headline " + measure
            table = MT
        cols.append((table, measure, label, True))
    v = core.new_table(
        ident("journey-review:headline:" + pid),
        "Headline KPIs for the current selection",
        cols,
        36,
        y,
        1608,
        105,
    )
    v["visual"]["objects"]["values"] = obj(fontSize=L("20D"))
    return v


def score_table(pid, y, detail=False):
    prefix = "Provider detail scoring " if detail else "Provider scoring "
    return core.new_table(
        ident("journey-review:scoring:" + pid),
        "Provider scoring evidence - components only, not an overall rating",
        [
            (SCORING, "Metric", "Component", False),
            (MT, prefix + "result", "Result", True),
            (MT, prefix + "numerator", "Numerator / timed responses", True),
            (MT, prefix + "denominator", "Denominator / responses", True),
            (MT, prefix + "evidence status", "Evidence status", True),
            (SCORING, "Definition", "Basis and limitation", False),
        ],
        36,
        y,
        1608,
        370,
    )


def button(pid, target, label, y):
    v = ui.visual_shell(
        ident("journey-review:drill:" + pid + target),
        "actionButton",
        ui.position(1290, y, 354, 42, 180000),
    )
    v["visual"]["visualContainerObjects"] = {
        "visualLink": obj(
            show=L("true"),
            type=L("'Drillthrough'"),
            drillthroughSection=L(quoted(target)),
            enabledTooltip=L("'Open detail for the selected record'"),
            disabledTooltip=L("'Select one ID in the results table first'"),
        )
    }
    return style_button(v, label, "Select one record first")


def build(bundle):
    root = bundle / "SM_WMPP_v16.Report/definition"
    model = bundle / "SM_WMPP_v16.SemanticModel/definition"
    docs = {}
    changes = {}

    def get(path):
        if path not in docs:
            docs[path] = json.loads(path.read_text(encoding="utf-8-sig"))
        return docs[path]

    def visual(pid, vid):
        return get(root / "pages" / pid / "visuals" / vid / "visual.json")

    def put(pid, v):
        docs[root / "pages" / pid / "visuals" / v["name"] / "visual.json"] = v

    def place(pid, vid, y, h=None, x=None, w=None):
        pos = visual(pid, vid)["position"]
        pos["y"] = y
        for k, val in [("height", h), ("x", x), ("width", w)]:
            if val is not None:
                pos[k] = val

    defs = definitions()
    changes[model / "tables" / (MT + ".tmdl")] = core.measure_text(MT, defs)
    changes[model / "tables" / (SCORING + ".tmdl")] = core.metric_axis(
        SCORING, [(group, label, "", note) for group, label, note in SCORE_ROWS]
    )
    all_defs = core.definitions() + defs
    kpi_path = model / "tables/_Explorer KPI Measures.tmdl"
    kpi_text = kpi_path.read_text(encoding="utf-8-sig")
    for prefix, axis, rows, extra, key in [
        (
            "Provider",
            "Provider Explorer KPI",
            core.PROVIDER_METRICS,
            PROVIDER_EXTRA,
            "'dim_provider'[provider_id]",
        ),
        (
            "Referral",
            "Referral Explorer KPI",
            core.REFERRAL_METRICS,
            REFERRAL_EXTRA,
            "'fact_referral'[referral_id]",
        ),
    ]:
        combined = rows + extra
        changes[model / "tables" / (axis + ".tmdl")] = core.metric_axis(axis, combined)
        for scope, single in [("explorer", None), ("detail", key)]:
            kpi_text = core.replace_measure(
                kpi_text,
                prefix + " " + scope + " KPI value",
                core.metric_value(axis, combined, all_defs, single),
            )
    changes[kpi_path] = kpi_text
    mpath = model / "model.tmdl"
    mtext = mpath.read_text(encoding="utf-8-sig")
    for table in [MT, SCORING]:
        mtext += "\nref table " + quoted(table) + "\n"
    changes[mpath] = mtext

    # Keep the existing journey icon/count group together. Main menu IDs/positions
    # and selector-only bookmark data are never moved or widened.
    for pid, low, high, shift in [(PROVIDER, 350, 646, 120), (REFERRAL, 550, 772, 110)]:
        for path in (root / "pages" / pid / "visuals").glob("*/visual.json"):
            v = get(path)
            if (
                low <= v["position"]["y"] <= high
                and v["position"]["z"] < 200000
                and v["name"] != "d55d271a06ed4dcd1ad1"
            ):
                v["position"]["y"] += shift

    ph = [
        ("Explorer providers", "Providers in selection"),
        ("Explorer provider offers made", "Distinct offers made"),
        ("Explorer provider messages", "Recorded messages"),
        ("Provider unanswered assignments", "Unanswered assignments"),
    ]
    rh = [
        ("Explorer referrals", "Referrals in selection"),
        ("Explorer referrals open overdue", "Open and overdue"),
        ("Referral open without offers", "Open without offers"),
        ("Referral accepted without IPA", "Accepted but no IPA"),
    ]
    put(PROVIDER, headline(PROVIDER, ph, 350))
    put(REFERRAL, headline(REFERRAL, rh, 550))
    put(
        PD,
        headline(
            PD,
            [
                ("Explorer provider homes", "Registered homes"),
                ("Explorer provider offers made", "Distinct offers made"),
                ("Explorer provider messages", "Recorded messages"),
                ("Provider unanswered assignments", "Unanswered assignments"),
            ],
            479,
            True,
        ),
    )
    put(
        RD,
        headline(
            RD,
            [
                ("Explorer referral offers", "Offer records"),
                ("Explorer referral assignments", "Provider assignments"),
                ("Explorer referral messages", "Recorded messages"),
                ("Referral IPAs awaiting signatures", "IPAs awaiting signatures"),
            ],
            884,
            True,
        ),
    )

    # Results precede the detailed KPI catalogue and activity evidence.
    place(PROVIDER, "23150d16760f289f4166", 800, 370)
    place(PROVIDER, "d55d271a06ed4dcd1ad1", 1240, 580, 36, 1608)
    p_kpi = visual(PROVIDER, "d55d271a06ed4dcd1ad1")
    p_kpi["visual"]["query"]["queryState"]["Values"]["projections"] = [
        project("Provider Explorer KPI", "Group", label="Area"),
        project("Provider Explorer KPI", "Metric", label="KPI"),
        project(core.MT, "Provider explorer KPI value", True, "Value"),
        project("Provider Explorer KPI", "Definition", label="Definition"),
    ]
    put(PROVIDER, score_table(PROVIDER, 1860))
    for vid, y in [
        ("b1c7e6028b7b1c565017", 2270),
        ("3a3d0319cf091735159b", 2270),
        ("bc985532f5d7fafc4ada", 2700),
        ("1623de849a96563dac1f", 3080),
        ("7c33a25a2d56dbbbfa5d", 3540),
        ("d2bf8cf3bfb4b834b9b9", 4080),
    ]:
        place(PROVIDER, vid, y)
    title(visual(PROVIDER, "b1c7e6028b7b1c565017"), "Referral assignment and response evidence")
    title(visual(PROVIDER, "3a3d0319cf091735159b"), "Offer records and proposed homes")
    title(
        visual(PROVIDER, "d2bf8cf3bfb4b834b9b9"),
        "Accepted offer share by assignment month - Gold cohort denominator",
    )
    place(PROVIDER, "252dfe03e93fe044b74b", 4470)
    place(PROVIDER, "2b0650a84c3da66c301b", 4476)
    place(PROVIDER, "d1a2b1f6a79a871ec771", 1180, 48, 36, 1210)
    put(PROVIDER, button(PROVIDER, PD, "Open selected provider detail", 1180))
    directory = visual(PROVIDER, "23150d16760f289f4166")
    # Rates carry a denominator in the scorecard, not an unexplained overall score.
    directory["visual"]["query"]["queryState"]["Values"]["projections"] += [
        project(core.MT, "Explorer Gold response rate", True, "Cohort response rate"),
        project(core.MT, "Explorer Gold offer acceptance rate", True, "Cohort accepted share"),
        project(core.MT, "Explorer Gold opportunities", True, "Cohort opportunities"),
    ]
    # Remove a duplicate activity response-rate column so the directory stays leaner.
    directory["visual"]["query"]["queryState"]["Values"]["projections"] = [
        p
        for p in directory["visual"]["query"]["queryState"]["Values"]["projections"]
        if p["queryRef"]
        not in {
            core.MT + ".Explorer provider response rate",
            core.MT + ".Explorer provider assignments",
            core.MT + ".Explorer provider accepted offers",
        }
    ]

    place(REFERRAL, "4a70f5c5a98aea85ed0a", 920, 420)
    place(REFERRAL, "2fb19244b155fb828fb5", 1400, 500)
    visual(REFERRAL, "2fb19244b155fb828fb5")["visual"]["query"]["queryState"]["Values"][
        "projections"
    ].insert(0, project("Referral Explorer KPI", "Group", label="Area"))
    for vid in ["8e8c4f2fddf1da23cdcd", "9d92d9b18d55fbad4ea7", "fc2ed197e11fecee79e0"]:
        place(REFERRAL, vid, 1960, 300)
    put(REFERRAL, button(REFERRAL, RD, "Open selected referral detail", 1350))
    put(
        REFERRAL,
        ui.textbox(
            ident("journey-review:referral-tip"),
            "Select a Referral ID row to open detail. Search includes referrals with no offers. Clear stage changes only the journey filter.",
            ui.position(36, 1350, 1210, 44, 180000),
            12,
            False,
        ),
    )
    for pid, axis, vid in [
        (PROVIDER, "Provider Explorer KPI", "d55d271a06ed4dcd1ad1"),
        (REFERRAL, "Referral Explorer KPI", "2fb19244b155fb828fb5"),
    ]:
        visual(pid, vid)["visual"]["query"]["sortDefinition"] = {
            "sort": [{"field": field(axis, "Metric"), "direction": "Ascending"}],
            "isDefaultSort": False,
        }

    # Detail profile/pathway remains first. Put summary and component evidence
    # ahead of raw activity, preserving existing Back actions.
    for path in (root / "pages" / PD / "visuals").glob("*/visual.json"):
        v = get(path)
        if v["position"]["y"] >= 1149 and v["position"]["z"] < 200000:
            v["position"]["y"] += 450
    pdkpi = ident("explorer-scope:provider-detail-kpi")
    place(PD, pdkpi, 620, 520)
    put(PD, score_table(PD, 1180, True))
    for path in (root / "pages" / RD / "visuals").glob("*/visual.json"):
        v = get(path)
        if 884 <= v["position"]["y"] < 2500 and v["position"]["z"] < 200000:
            v["position"]["y"] += 660
    place(RD, "deb457ea94bd7dde565e", 1020, 500)

    # Canonical ID fields enable cross-entity drillthrough from real activity rows.
    for pid, vid in [(RD, "79a53defabe24e19d2e1"), (RD, "9816e3d56d3423ba6ec7")]:
        v = visual(pid, vid)
        projections = v["visual"]["query"]["queryState"]["Values"]["projections"]
        projections.insert(0, project("dim_provider", "provider_id", label="Provider ID"))
    for pid, vids in [
        (PROVIDER, ["3a3d0319cf091735159b", "b1c7e6028b7b1c565017", "1623de849a96563dac1f"]),
        (PD, ["a6749ca9664490c2ea5d", "82ffb63ae00ca52bdfb5", "ec75285f156b37b56d67"]),
    ]:
        for vid in vids:
            v = visual(pid, vid)
            ps = v["visual"]["query"]["queryState"]["Values"]["projections"]
            if not any(p["queryRef"] == "fact_referral.referral_id" for p in ps):
                ps.insert(0, project("fact_referral", "referral_id", label="Referral ID"))

    archived = {
        "4cf4bd622bcd0f3317ca",
        "7ecbf97386432be48354",
        "0201737d8a9e36dd43a5",
        "488fb30362073b3e218d",
    }
    for vid in archived:
        visual(PROVIDER, vid)["isHidden"] = True
    # All existing visibility snapshots must keep the retired explorer charts
    # hidden, including chart/list toggles. Data-bearing stage bookmarks stay intact.
    for path in (root / "bookmarks").glob("*.bookmark.json"):
        original = json.loads(path.read_text(encoding="utf-8-sig"))
        b = deepcopy(original)
        for vid, state in (
            b.get("explorationState", {})
            .get("sections", {})
            .get(PROVIDER, {})
            .get("visualContainers", {})
            .items()
        ):
            if vid in archived:
                state.setdefault("singleVisual", {})["display"] = {"mode": "hidden"}
        if b != original:
            docs[path] = b

    # True record drillthrough replaces unfiltered menu jumps to detail pages.
    for path in (root / "pages").glob("*/visuals/*/visual.json"):
        v = get(path)
        container = v.get("visual", {}).get("visualContainerObjects", {})
        for entry in container.get("visualLink", []):
            prop = entry["properties"]
            bm = scalar(prop.get("bookmark", {}))
            destination = RD if bm == "f9213b97760541335978" else None
            if destination:
                prop.pop("bookmark", None)
                prop["type"] = L("'Drillthrough'")
                prop["drillthroughSection"] = L(quoted(destination))
                prop["disabledTooltip"] = L(
                    "'Select one matching record ID in a table before opening detail'"
                )
    # Find provider detail navigation by actual bookmark target, not a guessed ID.
    detail_bookmarks = {
        path.name.split(".")[0]
        for path in (root / "bookmarks").glob("*.bookmark.json")
        if is_provider_detail_navigation_bookmark(
            json.loads(path.read_text(encoding="utf-8-sig"))
        )
    }
    for path, v in docs.items():
        if path.name != "visual.json":
            continue
        for entry in v.get("visual", {}).get("visualContainerObjects", {}).get("visualLink", []):
            prop = entry["properties"]
            if scalar(prop.get("bookmark", {})) in detail_bookmarks:
                prop.pop("bookmark", None)
                prop.update(
                    type=L("'Drillthrough'"),
                    drillthroughSection=L(quoted(PD)),
                    disabledTooltip=L("'Select one Provider ID row first'"),
                )

    # Correct misleading labels and identifier-as-count cards outside explorers.
    title(
        visual("78d576b289e5fe3d2af6", "dfcfe27539d41e80730c"),
        "Active referrals by placement type and recorded engagement",
    )
    for vid, measure, label in [
        ("b7db015d6153289ce2d7", "KPIs catalogued", "KPIs catalogued"),
        ("058b102ca09b988287a5", "Requirements catalogued", "Requirements catalogued"),
        (
            "0aef383ced90ab2d5c70",
            "Requirements linked to KPIs",
            "Requirements linked to KPIs - not delivery complete",
        ),
    ]:
        v = visual("b95eb4c0b53cd8c60710", vid)
        v["visual"]["query"] = {
            "queryState": {"Data": {"projections": [project(MT, measure, True, label)]}}
        }
        v.pop("filterConfig", None)
        title(v, label)

    for pid, height in [(PROVIDER, 4550), (REFERRAL, 2420), (PD, 3900), (RD, 3100)]:
        page = get(root / "pages" / pid / "page.json")
        page["height"] = height
        page["width"] = 1680
        if pid in [PROVIDER, REFERRAL]:
            source = "23150d16760f289f4166" if pid == PROVIDER else "4a70f5c5a98aea85ed0a"
            interactions = page.setdefault("visualInteractions", [])
            for path, v in docs.items():
                if (
                    path.name == "visual.json"
                    and path.parents[2].name == pid
                    and v.get("visual", {}).get("query")
                    and v["name"] != source
                    and not v.get("isHidden")
                    and v["visual"]["visualType"] not in {"slicer"}
                    and not v["visual"]["visualType"].startswith("textFilter")
                ):
                    interactions[:] = [
                        i
                        for i in interactions
                        if not (i["source"] == source and i["target"] == v["name"])
                    ]
                    interactions.append(
                        {"source": source, "target": v["name"], "type": "DataFilter"}
                    )
    for pid, key in [
        (PROVIDER, "Provider selection context"),
        (REFERRAL, "Referral selection context"),
    ]:
        y = 770 if pid == PROVIDER else 885
        v = ui.visual_shell(
            ident("journey-review:context:" + pid),
            "cardVisual",
            ui.position(36, y, 1608, 28, 180000),
        )
        v["visual"]["query"] = {"queryState": {"Data": {"projections": [project(MT, key, True)]}}}
        v["visual"]["objects"] = {
            "value": obj(fontSize=L("12D"), bold=L("false")),
            "label": obj(show=L("false")),
        }
        v["visual"]["visualContainerObjects"] = {"background": obj(show=L("false"))}
        put(pid, v)
        page = get(root / "pages" / pid / "page.json")
        source = "23150d16760f289f4166" if pid == PROVIDER else "4a70f5c5a98aea85ed0a"
        page.setdefault("visualInteractions", []).append(
            {"source": source, "target": v["name"], "type": "DataFilter"}
        )

    # Summary tables and score evidence should not filter each other through the
    # row selected in their disconnected catalogue axes. Keep ordering stable.
    for pid, axis, vid in [
        (PD, "Provider Explorer KPI", pdkpi),
        (RD, "Referral Explorer KPI", "deb457ea94bd7dde565e"),
    ]:
        visual(pid, vid)["visual"]["query"]["sortDefinition"] = {
            "sort": [{"field": field(axis, "Metric"), "direction": "Ascending"}],
            "isDefaultSort": False,
        }
    for pid in [PROVIDER, PD]:
        score = docs[
            root
            / "pages"
            / pid
            / "visuals"
            / ident("journey-review:scoring:" + pid)
            / "visual.json"
        ]
        score["visual"]["query"]["sortDefinition"] = {
            "sort": [{"field": field(SCORING, "Metric"), "direction": "Ascending"}],
            "isDefaultSort": False,
        }

    for path, doc in docs.items():
        if not path.exists() or json.loads(path.read_text(encoding="utf-8-sig")) != doc:
            changes[path] = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
    return changes


def scoring_period_changes(bundle):
    """Add an explicit scoring period without changing activity-table time scope."""
    root = bundle / "SM_WMPP_v16.Report/definition"
    model = bundle / "SM_WMPP_v16.SemanticModel/definition"
    changes = {}

    def save(path, doc):
        changes[path] = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"

    def scoped_response(expression, require_timing=False):
        timing = (
            " && NOT ISBLANK('fact_referral_provider'[response_elapsed_minutes])"
            if require_timing
            else ""
        )
        return core.scope_provider(
            "VAR months = VALUES('dim_snapshot_month'[month_start]) VAR limited = ISFILTERED('dim_snapshot_month') RETURN CALCULATE("
            + expression
            + ", KEEPFILTERS(FILTER('fact_referral_provider', 'fact_referral_provider'[has_qualifying_response] == TRUE() && NOT ISBLANK('fact_referral_provider'[assigned_at])"
            + timing
            + " && (NOT limited || DATE(YEAR('fact_referral_provider'[assigned_at]),MONTH('fact_referral_provider'[assigned_at]),1) IN months))))"
        )[0]

    path = model / "tables" / (MT + ".tmdl")
    text = path.read_text(encoding="utf-8-sig")
    text = core.replace_measure(
        text,
        "Provider scoring median response hours",
        scoped_response(
            "DIVIDE(MEDIAN('fact_referral_provider'[response_elapsed_minutes]),60)", True
        ),
    )
    for name, timing in [
        ("Provider scoring timed responses", True),
        ("Provider scoring qualifying responses", False),
    ]:
        dax = scoped_response(
            "DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id])", timing
        )
        fragment = core.measure_text(MT, [(name, dax, "#,0")])
        block = fragment[fragment.index("\n\tmeasure ") : fragment.index("\n\tpartition ")]
        text = text.replace("\n\tpartition ", block + "\n\tpartition ", 1)
    text = text.replace(
        "3,[Provider response durations recorded]", "3,[Provider scoring timed responses]"
    )
    text = text.replace(
        "3,[Explorer provider qualifying responses]", "3,[Provider scoring qualifying responses]"
    )
    changes[path] = text
    for pid, y in [(PROVIDER, 219), (PD, 590)]:
        v = ui.visual_shell(
            ident("journey-review:scoring-period:" + pid),
            "slicer",
            ui.position(1268, y, 376, 92, 180000),
        )
        v["visual"]["query"] = {
            "queryState": {
                "Values": {
                    "projections": [dict(project("dim_snapshot_month", "year_month"), active=True)]
                }
            }
        }
        v["visual"]["objects"] = {
            "data": obj(mode=L("'Dropdown'")),
            "header": obj(show=L("false")),
            "selection": obj(singleSelect=L("false"), selectAllCheckboxEnabled=L("true")),
        }
        title(v, "Scoring assignment month")
        save(root / "pages" / pid / "visuals" / v["name"] / "visual.json", v)
    for path in (root / "pages" / PD / "visuals").glob("*/visual.json"):
        v = json.loads(path.read_text(encoding="utf-8-sig"))
        if v["name"] in {"249faf528a7281564965", "65a18b5e0a8121030050"}:
            v["isHidden"] = True
        elif v["name"] == "274ce3025b6e834ef74c":
            v["position"].update(x=36, width=1608)
        elif v["position"]["y"] >= 620 and v["position"]["z"] < 200000:
            v["position"]["y"] += 100
        else:
            continue
        save(path, v)
    note = ui.textbox(
        ident("journey-review:score-period-note:" + PD),
        "Scoring uses assignment cohorts. Select month(s) here; current activity totals above use their own context. No overall provider score is approved.",
        ui.position(36, 599, 1200, 76, 180000),
        12,
        False,
    )
    save(root / "pages" / PD / "visuals" / note["name"] / "visual.json", note)
    for path in (root / "bookmarks").glob("*.bookmark.json"):
        b = json.loads(path.read_text(encoding="utf-8-sig"))
        old = deepcopy(b)
        for vid, state in (
            b.get("explorationState", {})
            .get("sections", {})
            .get(PD, {})
            .get("visualContainers", {})
            .items()
        ):
            if vid in {"249faf528a7281564965", "65a18b5e0a8121030050"}:
                state.setdefault("singleVisual", {})["display"] = {"mode": "hidden"}
        if b != old:
            save(path, b)
    path = root / "pages" / PD / "page.json"
    p = json.loads(path.read_text(encoding="utf-8-sig"))
    p["height"] = 4000
    save(path, p)
    return changes


def guide_changes(bundle):
    root = bundle / "SM_WMPP_v16.Report/definition/pages"
    edits = {
        "5d4291498d7574ae92b3": {
            "24decefb2b52237183bc": "Search providers, including those with no offers or homes. Select a Provider ID row and open detail; Back returns to the originating results. Scoring evidence is separate from current activity totals.",
            "0ff7edba9c005a01334f": "Provider directory",
            "2c493d2eb660b6f228a0": "The canonical provider directory includes zero-offer providers. Home service filters narrow provider eligibility. Result columns show activity and cohort evidence; home filters do not create a home-level response score.",
            "78c140fadcb6194b5582": "Offer and home evidence",
            "c233b2d1c915c251bc08": "Distinct offers made excludes drafts and missing statuses. Total offer records includes drafts. Detail lists all registered homes and attributes home offers using the actual offer home ID.",
            "1e9d1bc5b2e1a46bec9f": "Response and action KPIs",
            "1b61fdf6bf6e1bd4132d": "Unanswered assignments require recorded assignment time and no qualifying response. Qualifying evidence is an offer or recorded reason; message volume is not a response SLA. Timing coverage exposes missing durations.",
            "ee37c1fd645f71177fc4": "Provider scoring evidence",
            "364ca2a4e44d2ddc9892": "Select assignment month(s) for response, accepted-offer share, target outcome and median response hours. Read numerator and denominator. Missing evidence is not zero. An overall score, weights and ranking policy are not approved.",
        },
        "ab109d96fb506aaf8fba": {
            "9407b120d7c2993b9668": "Search by person or Referral ID, including referrals without offers. Headline KPIs show the current selection; select a result row to open Referral Detail. Use Back to return to the source results.",
            "ad9234b59477f2674b0d": "Referral directory",
            "223fc5dc24e7701e322e": "Starts from all master referrals, not the offer table. Counts are distinct referral IDs, not distinct people. One person can have several referrals. Empty results mean the current filters have no matching records.",
            "105056458708505c763a": "Action KPIs",
            "cd6f571377787eec5164": "Check open overdue cases, open cases without offers or assignments, accepted offers without an IPA and IPAs awaiting either signature. These identify evidence to investigate, not proven officer or provider failures.",
            "21376314cd762c6720b3": "Current journey stage",
            "485ec1a415d2fa20efcd": "Click a stage to narrow the results; Clear stage removes only that filter. The rail classifies current evidence, not historical conversion. Closure can happen at any point. Signed paperwork does not confirm admission.",
            "8c2c41ee95b76dd266e3": "Offer activity filters",
            "754ad85a5b14ab786675": "Status and activity-band filters are optional. Choose (No offers) to find referrals without any offer record. A draft is an offer record, but not an offer made. Missing status or activity has its own unknown label.",
            "dca99469bdcfa7ba034f": "Selected record detail",
            "34d33b9e77496ae2e18a": "Select a Referral ID row, then use Open selected referral detail or right-click Drill through. The detail page contains lifecycle events, messages, offers and locations; Provider IDs support related provider drillthrough.",
            "ba573e5fbbeeb5f85a45": "KPI population",
            "ad59a187b6a0128ca977": "The KPI list describes matching or selected referrals under the same filters. Offers, assignments and IPA records have different keys and grains; their counts are not interchangeable.",
            "1d19c812ff3f7d3fe66d": "IPA chase evidence",
            "5a9ca06d8a5fdf991133": "An accepted offer without an IPA is different from an issued IPA awaiting signatures. Completion uses recorded evidence. Missing signature flags are included as awaiting evidence, not assumed complete.",
        },
    }
    changes = {}
    for pid, items in edits.items():
        for vid, label in items.items():
            path = root / pid / "visuals" / vid / "visual.json"
            v = json.loads(path.read_text(encoding="utf-8-sig"))
            runs = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"]
            runs[0]["value"] = label
            runs[0].setdefault("textStyle", {})["fontWeight"] = "normal"
            for run in runs[1:]:
                run["value"] = ""
            changes[path] = json.dumps(v, ensure_ascii=False, indent=2) + "\n"
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--scoring-period", action="store_true")
    parser.add_argument("--guides", action="store_true")
    args = parser.parse_args()
    bundle = args.project.resolve()
    if not (bundle / "EXPLORER_SCOPE_REPAIR.json").exists():
        raise ValueError("Apply and inspect the entity-scope repair first")
    if args.scoring_period and args.guides:
        raise ValueError("Apply one reviewed follow-up at a time")
    marker = (
        "EXPLORER_GUIDE_UPDATE.json"
        if args.guides
        else "SCORING_PERIOD_UPDATE.json"
        if args.scoring_period
        else "JOURNEY_SCORING_REVIEW.json"
    )
    if (bundle / marker).exists():
        raise ValueError("Review already applied; inspect the manifest before reapplying")
    if (args.scoring_period or args.guides) and not (
        bundle / "JOURNEY_SCORING_REVIEW.json"
    ).exists():
        raise ValueError("Apply the journey review before the period selector")
    if (bundle / "SM_WMPP_v16.SemanticModel/unappliedChanges.json").exists():
        raise ValueError("Pending Desktop model changes must be resolved first")
    before = inventory(bundle)
    if before["missing_fields"] or before["broken_actions"]:
        raise ValueError("Resolve saved baseline reference errors before applying")
    changes = (
        guide_changes(bundle)
        if args.guides
        else scoring_period_changes(bundle)
        if args.scoring_period
        else build(bundle)
    )
    planned = inventory(bundle, changes)
    if planned["missing_fields"] or planned["broken_actions"]:
        raise ValueError(
            json.dumps(
                {
                    "missing_fields": planned["missing_fields"],
                    "broken_actions": planned["broken_actions"],
                }
            )
        )
    print(json.dumps({"project": str(bundle), "files": len(changes), "apply": args.apply}))
    if not args.apply:
        return
    backup = (
        bundle.parent / "_review" / ("journey-scoring-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    backup.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for path in changes:
        if path.exists():
            destination = backup / path.relative_to(bundle)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            hashes[str(path.relative_to(bundle))] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path, content in changes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    after = inventory(bundle)
    manifest = {
        "project": str(bundle),
        "backup": str(backup),
        "files": [str(p.relative_to(bundle)) for p in changes],
        "original_hashes": hashes,
        "missing_fields": after["missing_fields"],
        "broken_actions": after["broken_actions"],
        "runtime_verified": False,
        "published": False,
        "overall_provider_score_approved": False,
        "cache_sources_roles_unchanged": True,
    }
    (bundle / marker).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in manifest.items() if k not in {"files", "original_hashes"}}, indent=2
        )
    )
    if after["missing_fields"] or after["broken_actions"]:
        raise ValueError("Saved reference check failed; inspect the manifest and backup")


if __name__ == "__main__":
    main()
