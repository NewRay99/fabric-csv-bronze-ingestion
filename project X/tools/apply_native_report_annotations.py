"""Add skin-free native annotations to the two local delivery reports.

No refresh, publication, model changes or report-version-dependent tests.
The before-edit report definitions and resources are retained in _review.
"""

from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import urllib.request
import xml.etree.ElementTree as ET

from build_report_design_delivery import L, fill, ident, obj, quoted, read, save
import rebuild_mission_control_dashboard_v16 as ui


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "reports/client-deliverables/WMPP v16"
REVISION = "66d8f9fc394b8530377e5f6112f0b8908ba01280"
UPSTREAM = f"https://raw.githubusercontent.com/lucide-icons/lucide/{REVISION}/"
ICONS = (
    "info",
    "users",
    "house",
    "handshake",
    "target",
    "calendar-days",
    "clock",
    "pound-sterling",
    "triangle-alert",
    "chart-column",
)
SUPPLY = "510f9f9501ccc5ae8a74"
TARGET = "6ae319c8916a5d63a4ff"
SNAPSHOTS = "dd3a58c056d723048dbf"
BOARD = "5038cffdd48af9a80dd1"

# Titles, concise on-page captions, and fuller click-through explanations.
SUPPLY_KPIS = [
    (
        "Providers Making Offers",
        "Excludes draft / withdrawn offers",
        "Distinct providers with an offer, excluding draft, withdrawn and offer_withdrawn statuses. This is participating supply, not all registered providers.",
    ),
    (
        "Offers Received",
        "Distinct offers in the selection",
        "Distinct offer IDs under the applicable filters. A referral can have several offers, so offers and referrals are different counts.",
    ),
    (
        "Offer Acceptance Rate",
        "Accepted / offers with a decision",
        "Accepted Offers divided by Offers with a Decision. Accepted includes accepted, approved, selected and offer_successful statuses. This is not an IPA completion rate.",
    ),
    (
        "Avg Offers per Referral",
        "Among referrals with an offer",
        "Offers Submitted divided by Referrals With An Offer. Referrals with no offer are not in this denominator.",
    ),
    (
        "Homes Offered",
        "Distinct nonblank home IDs",
        "Distinct provider_home_id values in the filtered offers, excluding missing or empty home identifiers. This is homes offered, not available beds or live vacancies.",
    ),
    (
        "Median Weekly Cost",
        "Estimated offered weekly cost",
        "Median estimated_weekly_cost across filtered offer records. This is a median offer price, not actual expenditure, accepted-placement cost or a sum of weekly costs.",
    ),
]
SUPPLY_CHARTS = [
    (
        "Offers by Provider",
        "Distinct offers received by provider",
        "Compare the volume of distinct offers associated with each provider. The same referral may have offers from multiple providers.",
    ),
    (
        "Accepted Offers by Provider",
        "Offers with an accepted status",
        "Distinct offers in accepted, approved, selected or offer_successful status by provider. Acceptance is not evidence that an IPA has been issued.",
    ),
    (
        "Provider Response Time",
        "Median days to first offer",
        "For each referral within provider context, the earliest submitted offer is compared with referral creation. Valid nonnegative durations are converted from hours to days, then their median is shown. Missing and negative durations are excluded.",
    ),
    (
        "Homes Offered by County",
        "Distinct homes; home county",
        "Distinct offered homes grouped by provider-home county. This is neither a governed region classification nor the referred child's home location.",
    ),
    (
        "Placement Type Mix",
        "Distinct homes offered by type",
        "Distinct offered homes grouped by placement type. A home appearing in multiple types may contribute to more than one segment; do not assume segment totals equal distinct homes overall.",
    ),
    (
        "Offer to IPA Funnel",
        "Recorded stages; gaps stay blank",
        "Shows submitted offers, accepted offers and accepted offers with an IPA. Reviewed and shortlisted stages are deliberately blank because reliable event history is unavailable. It is not an event-timestamp conversion funnel.",
    ),
]
TARGET_KPIS = [
    (
        "Due This Month",
        "Month of source as-of date",
        "Referrals whose required placement date falls in the month of the current source as-of date. The measure removes the reporting-date filter; it is not automatically the computer's current month.",
    ),
    (
        "Due in 3 Days",
        "Open; as-of date through +3 days",
        "Open referrals with a known required date and as-of date, due from the as-of date through three days later, inclusive. Overdue referrals are excluded from this forward-looking bucket.",
    ),
    (
        "Overdue",
        "Open referrals past target",
        "Distinct referrals flagged is_open_overdue in the source/model state. This is recorded overdue status, not a real-time countdown based on the device clock.",
    ),
    (
        "Critical Hit Rate",
        "Eligible critical placements",
        "Placement Target Hit Rate restricted to Critical urgency: placed by required date divided by referrals with both IPA-issued and required-placement dates. Missing dates are not counted as failures.",
    ),
    (
        "Avg Days Early",
        "On-time placements only",
        "Average days between IPA issue and required placement date for referrals flagged placed_by_required_date with both dates known. Late placements are excluded; this is not overall average delay.",
    ),
    (
        "Escalated Cases",
        "Unavailable: no event history",
        "No reliable escalation history is supplied, so this KPI is not calculated. A dash is unavailable data, not zero escalations.",
    ),
]
TARGET_CHARTS = [
    (
        "Required Placement Date Trend",
        "Referrals due by required month",
        "Counts referrals using the required-placement-date relationship to the date table. This is a due-date trend, not a referral-created-date trend.",
    ),
    (
        "Hit Rate by Urgency Over Time",
        "Created-month cohorts by urgency",
        "Placement Target Hit Rate by referral-created month and urgency. Only referrals with both IPA-issued and required-placement dates enter the denominator. Small eligible cohorts can produce volatile rates.",
    ),
    (
        "Open Referrals by Days to Target",
        "Time remaining from source as-of",
        "Open referrals grouped using required placement date minus source as-of date. This is remaining time to target, not age since referral creation; missing dates retain the model's separate bucket.",
    ),
    (
        "Urgency / Target Status Matrix",
        "Open referrals by urgency and status",
        "Combines urgency with target status: overdue, due within three days, later, or missing dates. Missing target dates must not be interpreted as on time.",
    ),
    (
        "Ageing of Open Referrals",
        "Age since referral creation",
        "Open referrals grouped by recorded age: up to 2, 7, 14, 28 days, older, or unknown/invalid. Ageing and time to target answer different questions.",
    ),
    (
        "Cohort Placement Within Window",
        "Only fully observed cohorts qualify",
        "For each observation window, only referrals old enough to complete that window by their source as-of date enter the denominator. The numerator requires IPA issue between creation and the end of that window. This avoids treating immature cohorts as failures.",
    ),
]
SNAPSHOT_ENTRIES = [
    (
        "Snapshot window",
        "Last 6 or 12 available calendar months",
        "The window ends at the latest available snapshot month, not today's date. Last 6 months / Last 12 months filters both the chart and detail table. Missing months remain gaps.",
    ),
    (
        "Referral snapshot trend",
        "Month-end states, not new-referral flows",
        "Each series counts distinct referral IDs in each retained snapshot month. Open, awaiting-offer and under-offer populations overlap; do not add the series together. Closed/cancelled includes closed, cancelled, withdrawn and completed statuses.",
    ),
    (
        "Snapshot detail by month",
        "Compare retained monthly populations",
        "The register shows distinct referrals, open referrals, referrals with IPA and open-overdue referrals at each snapshot. Summing monthly distinct counts does not produce a distinct number of referrals or people across the window.",
    ),
]
INTROS = {
    "Provider & Placement Supply": "Understand provider participation, the offers received and the homes represented. Counts describe filtered records, not a live vacancy register.",
    "Target & Urgency Performance": "See which placements are due, which open referrals are overdue and how eligible cohorts meet their required placement dates. Use the source as-of date when interpreting urgency.",
    "Referral Snapshots": "Compare retained month-end referral states across a 6- or 12-month window. Historical snapshots and the current referral state answer different questions.",
    "PROVIDER SINGLE VIEW": "Search for a provider, then inspect its recorded homes, assignments and offers. Confirm the selection before comparing providers; relationship directions determine which visuals respond.",
    "REFERRAL DETAIL (DRILLTHROUGH)": "Inspect the referral context carried by drillthrough. Search by referral ID or person label and review related offer and IPA records; verify one referral is selected before interpreting individual detail.",
    "OFFERS OVERVIEW": "Review the current offer workload and provider engagement. Referrals, offers and provider assignments are different units; use each metric's definition rather than adding the cards together.",
    "IPA OVERVIEW": "Review the recorded stages between successful offers and IPA completion. Stage counts describe current records, not necessarily one same-period conversion cohort.",
    "DRAFT OFFERS": "Identify draft offers and recorded activity since creation. Age is not a service-level breach by itself; check the selected cohort and supporting records before acting.",
    "REQUIREMENT MATRIX OVERVIEW": "Trace requirements to the documented KPI catalogue. These are catalogue records, not service caseload counts, and a mapping alone does not prove that a requirement has been delivered.",
    "WMPP HOMEPAGE": "Choose a report page to explore referrals, offers, providers and placement performance. Check source refresh/as-of dates before using the figures operationally.",
    "Offer Locations": "Compare the available preferred-city-to-provider-home distances and their coverage. These are not exact child-address distances, road travel distances or journey-time estimates. Missing locations remain unknown.",
    "Referral Geography": "Explore referral preference-city areas, not individual child addresses. Category and framework filters refine the cohort; breakdown and metric selectors change the comparison. Do not infer precise child locations from map circles.",
    "Referral Single View": "Search by person label and referral ID, then inspect offers, provider referrals and IPA records. Check that one referral is selected. The map represents preference-city areas, not the child's home address.",
    "Load Calendar": "Select a calendar day to filter the right-hand view. Switch between Day Gantt and Register without resetting that selection. Green indicates recorded success; red indicates failures, also identified by status text.",
    "Job & Step Timelines": "Choose a job to inspect its steps. Runtime bands describe comparable successful history: previous 30 days, at least five samples, P25–P75 with a mean marker. They are not SLAs or prediction intervals; failed endpoints carry a red halo and status label.",
    "Quality & Schema": "Review evaluated data-quality checks, failed checks and failed-row counts alongside the captured schema. A row can fail several checks, so failed-row totals are not necessarily distinct affected records.",
    "Archive & Replay": "Review archive batches, reload flags, attempts and month-end snapshot results. This is a read-only monitoring page: viewing or selecting a row does not run a replay.",
    "Job Step Detail (Drillthrough)": "Review the selected job and notebook steps with timestamps, durations and recorded errors. Some headline measures fall back to the latest job when no single job is selected; confirm the displayed run ID.",
}

METRIC_NOTES = {
    "Total Referrals": "Distinct referral IDs, not distinct people. One person can have more than one referral.",
    "Referrals Currently Active": "Distinct referrals whose recorded is_open flag is true. This is current recorded state within the selected cohort.",
    "Referrals Awaiting Offer": "Distinct referrals flagged is_awaiting_offer. This uses the recorded flag, not a count inferred from the offer table.",
    "Referrals Under Offer": "Distinct referrals that are both open and in UNDER_OFFER status.",
    "Referrals With Multiple Provider Assignments": "Distinct referrals whose recorded provider_assignment_count exceeds one. This is referrals, not the number of assignments.",
    "Active Referral Engagement Rate": "Active Referrals With Provider Engagement divided by Referrals Currently Active. Engagement is not the same as receiving an offer or completing a placement.",
    "Offers Submitted": SUPPLY_KPIS[1][2],
    "Provider Assignments": "Distinct referral_provider_id values. A single referral may have several provider assignments.",
    "Offers on Referrals Under Offer": "Non-draft offers linked to referrals that are open and in UNDER_OFFER status. This is an offer count, not a percentage or a distinct-referral count.",
    "Pending Offers (Under Offer Referrals)": "Offers in pending or offer_made status, restricted to open referrals in UNDER_OFFER status. This is a count, not a percentage.",
    "Offers per Provider (Under Offer Referrals)": "Non-draft offers on open UNDER_OFFER referrals divided by qualifying providers in that context. Read the provider grouping carefully: this is a ratio, not a raw offer total.",
    "Draft Offers With Activity Since Creation": "Draft offers flagged as having activity since creation, excluding records with missing dates. Missing dates must not be interpreted as evidence of inactivity.",
    "Oldest Draft Age Days": "Maximum recorded offer_age_days among draft offers with a known age. A blank age is excluded, not treated as zero days.",
    "Draft Offer Count (Under Offer Referrals)": "Draft offers linked to referrals that are both open and UNDER_OFFER, split by the selected draft-age band. This can be a narrower cohort than the headline draft total.",
    "IPA Completed": "Created IPAs whose is_ipa_completed flag is true. This counts IPA records, not distinct children.",
    "Accepted Offer to IPA Conversion %": "IPAs Created divided by Accepted Offers under the applicable filters. It is a ratio of recorded populations, not a timestamp-tracked same-period conversion rate.",
    "Successful Offers to IPA Completed %": "Completed IPAs divided by accepted offers. Check cohort and date context before treating the ratio as a journey conversion rate.",
    "Gold Model Last Refreshed": "Latest gold_modelled_at timestamp in the filtered referral data. This is a source-model timestamp, not confirmation that Power BI has just refreshed.",
    "Referrals": "Distinct referrals, restricted through the framework-category bridge when categories are selected. A referral can belong to several categories; category counts need not add to the overall distinct total.",
    "Category-aware open referrals": "Open referrals restricted through the framework-category bridge when categories are selected. Multiple category memberships do not represent additional people.",
    "Awaiting offer": "Referrals flagged awaiting an offer, with the selected framework/category cohort applied through the category bridge.",
    "Mapped referrals": "Category-aware referrals with location_match_status CITY_MATCH. Map circles describe preference-city areas, never exact child addresses.",
    "Location review": "Referrals with a missing or non-CITY_MATCH location status. These are not silently assigned to a city or treated as zero-distance placements.",
    "Median preferred-city distance km": "Median nonblank distance for offers marked APPROXIMATE_PREFERENCE_CITY. It is a location approximation, not road distance, travel time or exact child-to-home distance.",
    "Offers without preferred-city distance": "Offers Submitted minus offers with a usable preferred-city distance. Missing distance is unknown, not zero kilometres.",
    "Preferred-city distance coverage": "Offers with preferred-city distance divided by Offers Submitted. Use this coverage percentage alongside the median to see how much of the offer population it represents.",
    "Runs": "Distinct job_run_id values in the selected date and pipeline context. Jobs and notebook steps are different units.",
    "Success rate": "Successful runs divided by successful plus failed runs. Running and other-status jobs are excluded from the denominator, not counted as failures.",
    "Failures": "Distinct job runs classified Failed in the selected context. Red endpoints also have textual status labels; colour is not the sole indication of failure.",
    "P95 duration min": "Inclusive 95th percentile of recorded nonnegative job durations in minutes for ended jobs under the current filters. This includes ended failures; it is different from the successful-history P25–P75 comparison band.",
    "Rows written": "Sum of recorded rows_written for the selected jobs. Retries and repeated writes can count the same logical records more than once; this is not a distinct-row total.",
    "Day tile": "Select a day to filter job detail. Any failure takes red precedence; running/other states are amber; successful days are green; no-load days are neutral. A darker/lighter green reflects successful volume, not an SLA score.",
    "Archive ZIP Batches": "Count of archive ZIP load records under the current filters. This is batches, not contained files or business records.",
    "Failed Archive ZIP Batches": "Archive batch records in FAILED, FAIL or ERROR status. Check the error message and attempt count in the register.",
    "Archive ZIP Batches Awaiting Reload": "Archive batch records with reload set to true. This is a recorded flag, not evidence that a replay is currently executing.",
    "Failed Gold Snapshots": "Month-end Gold run records in FAILED, FAIL or ERROR status. Inspect snapshot date, attempts and errors before interpreting repeated failures.",
    "DQ Evaluated Checks": "Quality-result records with PASS, SUCCESS, FAILED, FAIL or ERROR status. Pending and other statuses are not included in this evaluated population.",
    "DQ Failed Checks": "Quality-result records in FAILED, FAIL or ERROR status. This is check executions, not distinct rules or affected people.",
    "DQ Failed Rows": "Sum of failed_row_count across the selected quality results. The same data row can fail multiple checks, so the sum is not a distinct affected-row count.",
    "Critical Rules Failing": "Distinct rule IDs with CRITICAL severity and FAILED, FAIL or ERROR status. It is distinct failing rules, not all failure occurrences.",
}


def shell(key, kind, position):
    result = ui.visual_shell(ident("native-style:" + key), kind, ui.position(*position, 55000))
    result["visual"]["visualContainerObjects"] = {
        name: obj(show=L("false"))
        for name in ("background", "border", "dropShadow", "title", "subTitle", "visualHeader")
    }
    result["visual"]["visualContainerObjects"]["padding"] = obj(
        **{k: L("0D") for k in ("top", "bottom", "left", "right")}
    )
    result["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted(key)))
    return result


def text(key, words, pos, size=14, bold=False, dark=False):
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
                                "color": "#F3F7EF" if dark else "#2B2427",
                            },
                        }
                    ]
                }
            ]
        )
    }
    return value


def image(key, icon, pos, dark=False):
    value = shell(key, "image", pos)
    name = f"lc-{icon}-{'light' if dark else 'ink'}.svg"
    value["visual"]["objects"] = {
        "image": obj(
            sourceFile={
                "image": {
                    "name": L(quoted(name)),
                    "url": {
                        "expr": {
                            "ResourcePackageItem": {
                                "PackageName": "RegisteredResources",
                                "PackageType": 1,
                                "ItemName": name,
                            }
                        }
                    },
                    "scaling": L("'Fit'"),
                }
            }
        )
    }
    return value


def button(key, label, detail, pos, destination, dark=False):
    value = shell(key, "actionButton", pos)
    value["position"]["z"] = 55001
    c = value["visual"]["visualContainerObjects"]
    c["general"] = obj(altText=L(quoted(detail)))
    c["visualLink"] = obj(
        show=L("true"),
        type=L("'PageNavigation'"),
        navigationSection=L(quoted(destination)),
        tooltip=L(quoted(detail)),
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
                "fontSize": L("10D"),
                "fontColor": fill("#F3F7EF" if dark else "#2B2427"),
                "horizontalAlignment": L("'center'"),
                "verticalAlignment": L("'middle'"),
            },
        }
    ]
    return value


def put(report, page, value):
    save(report / "definition/pages" / page / "visuals" / value["name"] / "visual.json", value)


def info(report, page, key, detail, pos, destination, dark=False):
    put(report, page, image(key + "-icon", "info", pos, dark))
    put(report, page, button(key, "", detail, pos, destination, dark))


def literal(value):
    return value.get("expr", {}).get("Literal", {}).get("Value", "").strip("'").replace("''", "'")


def refs(visual):
    found = []

    def walk(value):
        if isinstance(value, dict):
            if "queryRef" in value and value["queryRef"] not in found:
                found.append(value["queryRef"])
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(visual.get("query", {}))
    return found


def get_title(visual):
    return literal(
        visual.get("visualContainerObjects", {})
        .get("title", [{}])[0]
        .get("properties", {})
        .get("text", {})
    )


def install_icons(report):
    """Retain upstream originals and the exact rendered variants beside the PBIP."""
    sources = []
    registry = read(report / "definition/report.json")
    items = next(
        p["items"] for p in registry["resourcePackages"] if p["name"] == "RegisteredResources"
    )
    for icon in ICONS:
        original = report.parent / f"lucide-{icon}.svg"
        if not original.exists():
            original.write_bytes(
                urllib.request.urlopen(UPSTREAM + f"icons/{icon}.svg", timeout=30).read()
            )
        raw = original.read_text(encoding="utf-8")
        element = ET.fromstring(raw)
        assert element.tag.endswith("svg") and "<script" not in raw and "href=" not in raw
        sources.append(
            {
                "icon": icon,
                "catalogue": f"https://lucide.dev/icons/{icon}",
                "source": UPSTREAM + f"icons/{icon}.svg",
                "sha256": hashlib.sha256(original.read_bytes()).hexdigest(),
            }
        )
        for suffix, color in (("ink", "#2B2427"), ("light", "#F3F7EF")):
            filename = f"lc-{icon}-{suffix}.svg"
            variant = raw.replace('stroke="currentColor"', f'stroke="{color}"')
            (report.parent / filename).write_text(variant, encoding="utf-8")
            (report / "StaticResources/RegisteredResources" / filename).write_text(
                variant, encoding="utf-8"
            )
            if not any(i["name"] == filename for i in items):
                items.append({"name": filename, "path": filename, "type": "Image"})
    license_path = report.parent / "Lucide-LICENSE.txt"
    if not license_path.exists():
        license_path.write_bytes(urllib.request.urlopen(UPSTREAM + "LICENSE", timeout=30).read())
    save(
        report.parent / "Lucide-provenance.json",
        {
            "revision": REVISION,
            "retrieved": "2026-09-27",
            "modifications": "lc-* variants replace currentColor with explicit report ink/light stroke only. Upstream geometry is unchanged. Originals and license are beside this file.",
            "icons": sources,
        },
    )
    save(report / "definition/report.json", registry)


def reference_page(report, page, name, kpis, charts):
    guide = ident("native-guide:" + page)
    put(
        report,
        page,
        text(page + "-heading", "FOSTER PLACEMENT PERFORMANCE", (96, 22, 660, 42), 28, True),
    )
    put(report, page, text(page + "-page-title", name, (96, 65, 710, 30), 20, True))
    put(report, page, text(page + "-asof", "Data as of", (96, 99, 64, 22), 12))
    put(
        report,
        page,
        image(page + "-page-icon", "house" if page == SUPPLY else "target", (36, 33, 42, 42)),
    )
    info(report, page, page + "-intro", INTROS[name], (790, 35, 28, 28), guide)
    top = 124 if page == SUPPLY else 120
    icons = (
        ("users", "handshake", "target", "chart-column", "house", "pound-sterling")
        if page == SUPPLY
        else ("calendar-days", "clock", "triangle-alert", "target", "clock", "triangle-alert")
    )
    for i, (title, caption, detail) in enumerate(kpis):
        x = 24 + 272 * i
        put(report, page, image(page + f"-kpi-{i}", icons[i], (x + 33, top + 16, 34, 34)))
        put(
            report,
            page,
            text(page + f"-kpi-label-{i}", title, (x + 98, top + 58, 166, 42), 14, True),
        )
        put(
            report,
            page,
            text(page + f"-kpi-caption-{i}", caption, (x + 98, top + 102, 166, 32), 11),
        )
        info(report, page, page + f"-kpi-info-{i}", detail, (x + 39, top + 72, 24, 24), guide)
    for i, (title, caption, detail) in enumerate(charts):
        x = 24 + i % 3 * 552
        y = (260 if i < 3 else 572) if page == SUPPLY else (256 if i < 3 else 544)
        put(
            report,
            page,
            text(page + f"-chart-title-{i}", title, (x + 20, y + 9, 350, 30), 18, True),
        )
        put(
            report, page, text(page + f"-chart-caption-{i}", caption, (x + 20, y + 43, 488, 30), 12)
        )
        info(report, page, page + f"-chart-info-{i}", detail, (x + 390, y + 9, 26, 26), guide)
    if page == TARGET:
        put(
            report,
            page,
            text(
                page + "-target-note",
                "Required Placement Date is the core target.",
                (36, 851, 700, 32),
                18,
                True,
            ),
        )
        put(
            report,
            page,
            text(
                page + "-target-note-2",
                "Interpret urgency using the recorded source as-of date; missing targets stay separate.",
                (36, 885, 1520, 24),
                13,
            ),
        )


def snapshots(report):
    page = SNAPSHOTS
    folder = report / "definition/pages" / page
    path = folder / "visuals/f38eef183da0ff549194/visual.json"
    value = read(path)
    value["position"]["width"] = 1000
    save(path, value)
    for visual_id, old_y, y, height, title, caption in (
        (
            "25d0c5fe446cdbcb2cf3",
            260,
            312,
            348,
            "Referral snapshot trend",
            "Distinct referrals at each month end • Series overlap; do not sum • Missing months remain gaps",
        ),
        (
            "e5f0b8f9afa923fcf3e2",
            680,
            732,
            228,
            "Snapshot detail by month",
            "Retained monthly state • The selected 6 / 12 month window applies to this table too",
        ),
    ):
        path = folder / "visuals" / visual_id / "visual.json"
        value = read(path)
        value["position"].update(y=y, height=height)
        value["visual"].setdefault("visualContainerObjects", {})["title"] = obj(show=L("false"))
        save(path, value)
        put(report, page, text(visual_id + "-title", title, (26, old_y, 1430, 28), 20, True))
        put(report, page, text(visual_id + "-caption", caption, (26, old_y + 29, 1550, 23), 13))
        info(
            report,
            page,
            visual_id + "-info",
            SNAPSHOT_ENTRIES[1 if "25d" in visual_id else 2][2],
            (1614, old_y, 26, 26),
            ident("native-guide:" + page),
        )


def common_style(report, pagefile):
    page = read(pagefile)
    dark = report.name.startswith("SM WMPP Mission") and page["name"] not in (
        "112fda69b94ad2ed064c",
        "2af45662f5a13e0c063b",
    )
    for key in ("background", "outspace"):
        for block in page.get("objects", {}).get(key, []):
            block.get("properties", {}).pop("image", None)
    page.setdefault("objects", {})["background"] = obj(
        color=fill("#101713" if dark else "#F8F5F1"), transparency=L("0D")
    )
    save(pagefile, page)
    for path in pagefile.parent.glob("visuals/*/visual.json"):
        value = read(path)
        visual = value.get("visual", {})
        kind = visual.get("visualType", "")
        c = visual.setdefault("visualContainerObjects", {})
        c["border"] = obj(show=L("false"))
        if kind in ("textbox", "image", "actionButton", "slicer"):
            c["dropShadow"] = obj(show=L("false"))
        c["padding"] = obj(**{k: L("0D") for k in ("top", "bottom", "left", "right")})
        if kind == "image" and "wmpp-reference-" in json.dumps(visual):
            value["isHidden"] = True
        if value["name"] == "0674b93d00a0a2360e81":
            # Keep the helper screenshot inside its existing tooltip canvas.
            value["position"]["height"] = 162.5
            visual["objects"]["image"][0]["properties"]["sourceFile"]["image"]["scaling"] = L(
                "'Fit'"
            )
        if kind == "textbox":
            for key in ("title", "subTitle", "background"):
                c[key] = obj(show=L("false"))
            for group in visual.get("objects", {}).get("general", []):
                for para in group.get("properties", {}).get("paragraphs", []):
                    for run in para.get("textRuns", []):
                        run.setdefault("textStyle", {})["fontFamily"] = "Segoe UI"
        if kind == "slicer":
            # Do not change selection, slicer kind, orientation or parameter binding.
            for block in visual.get("objects", {}).get("items", []):
                block.setdefault("properties", {})["padding"] = L("2D")
        for title in c.get("title", []):
            title.setdefault("properties", {}).update(
                fontFamily=L("'Segoe UI'"), fontColor=fill("#F3F7EF" if dark else "#2B2427")
            )
        # Keep headings faithful to the existing bindings, without changing queries.
        corrected_titles = {
            "4cf4bd622bcd0f3317ca": "Referrals by Placement Type",
            "bd4f7880ccae3a031056": "Offers on Referrals Under Offer",
            "e293464320d09d1cb511": "Pending Offers on Referrals Under Offer",
            "feef8d204a260a0060c7": "Offers per Qualifying Provider",
        }
        if value["name"] in corrected_titles:
            c.setdefault("title", obj())[0].setdefault("properties", {})["text"] = L(
                quoted(corrected_titles[value["name"]])
            )
        if kind == "actionButton":
            alt = literal(c.get("general", [{}])[0].get("properties", {}).get("altText", {}))
            label = (
                "Chart"
                if alt.startswith("Show chart for ")
                else "Table"
                if alt.startswith("Show table for ")
                else {
                    "Go to Board": "Board",
                    "Go to Supply": "Supply",
                    "Go to Target": "Targets",
                }.get(alt)
            )
            if label:
                visual.setdefault("objects", {})["text"] = [
                    {
                        "selector": {"id": "default"},
                        "properties": {
                            "show": L("true"),
                            "text": L(quoted(label)),
                            "fontFamily": L("'Segoe UI'"),
                            "fontSize": L("8D" if label in ("Chart", "Table") else "10D"),
                            "fontColor": fill("#2B2427"),
                            "horizontalAlignment": L("'center'"),
                            "verticalAlignment": L("'middle'"),
                        },
                    }
                ]
        # Decorative legacy help glyphs are replaced with licensed Lucide artwork.
        if kind == "image" and re.search(r"bulb|info-black|info-peach", json.dumps(visual)):
            visual["objects"]["image"] = image("replacement", "info", (0, 0, 24, 24), dark)[
                "visual"
            ]["objects"]["image"]
        save(path, value)
    return page, dark


def guide_entries(pagefile):
    entries = []
    for path in pagefile.parent.glob("visuals/*/visual.json"):
        value = read(path)
        visual = value.get("visual", {})
        fields = refs(visual)
        if (
            value.get("isHidden")
            or not fields
            or visual.get("visualType") in ("slicer", "shape")
            or "textFilter" in visual.get("visualType", "")
        ):
            continue
        if all("Min(ref_" in f for f in fields):
            continue
        title = get_title(visual) or fields[0].split(".", 1)[-1]
        readable = [f.split(".", 1)[-1].replace("_", " ") for f in fields]
        if "card" in visual.get("visualType", "").lower():
            detail = (
                "Headline metric: "
                + "; ".join(readable)
                + ". Read it under the current selection and displayed as-of context. Blank values are not necessarily zero."
            )
        else:
            detail = (
                "Displays "
                + "; ".join(readable[:7])
                + ("; additional fields are available in the visual" if len(readable) > 7 else "")
                + ". Use the selected cohort and displayed units when comparing values."
            )
        metric_names = [f.split(".", 1)[-1] for f in fields if f.startswith("_")]
        notes = [METRIC_NOTES[n] for n in metric_names if n in METRIC_NOTES]
        if notes:
            detail = " ".join(notes[:2])
            if not get_title(visual):
                title = " / ".join(metric_names[:2])
        if any(n.startswith("Selected or Latest") for n in metric_names):
            detail = (
                "Shows "
                + ", ".join(metric_names)
                + ". A single selected run takes priority; otherwise the measure falls back to the latest job. Confirm the displayed run ID before interpreting the value."
            )
        if any(f.startswith("_Run Benchmarks.") for f in fields):
            title = (
                "Job runtime and prior history"
                if any(f.startswith("rpt_job_run_summary.") for f in fields)
                else "Step runtime and prior history"
            )
            detail = "Compare actual duration with the previous 30 days of comparable successful history. At least five completed samples are required for the P25–P75 band. The mean is a separate tick. These are descriptive ranges, not SLAs. Failed endpoints use red halos and status text."
        entries.append((title, "", detail))
        visual.setdefault("visualContainerObjects", {}).setdefault("general", obj())[0].setdefault(
            "properties", {}
        )["altText"] = L(quoted(title + ". " + detail))
        save(path, value)
    return entries


def add_guide(report, pagefile, page, dark, entries):
    page_id, name = page["name"], page["displayName"]
    guide_id = ident("native-guide:" + page_id)
    intro = INTROS.get(
        name,
        "Read the selected report context and the source metric definitions before comparing values.",
    )
    rows = max(1, (len(entries) + 1) // 2)
    height = max(945, 200 + rows * 132)
    guide = ui.page_json(guide_id, name + " - guide", height, 1680)
    guide["visibility"] = "HiddenInViewMode"
    guide["objects"] = {
        "background": obj(color=fill("#101713" if dark else "#F8F5F1"), transparency=L("0D"))
    }
    save(report / "definition/pages" / guide_id / "page.json", guide)
    put(
        report,
        guide_id,
        text(
            guide_id + "-heading",
            name + " | how to read this page",
            (36, 24, 1580, 44),
            28,
            True,
            dark,
        ),
    )
    put(report, guide_id, text(guide_id + "-intro", intro, (36, 78, 1590, 58), 15, dark=dark))
    for i, (title, _, detail) in enumerate(entries):
        x, y = 36 + (i % 2) * 820, 150 + (i // 2) * 132
        put(
            report, guide_id, text(guide_id + f"-title-{i}", title, (x, y, 776, 30), 19, True, dark)
        )
        put(
            report,
            guide_id,
            text(guide_id + f"-body-{i}", detail, (x, y + 34, 776, 90), 15, dark=dark),
        )
    put(
        report,
        guide_id,
        button(
            guide_id + "-back",
            "Return to report page",
            "Return to " + name,
            (36, height - 48, 300, 36),
            page_id,
            dark,
        ),
    )
    meta_path = report / "definition/pages/pages.json"
    metadata = read(meta_path)
    if guide_id not in metadata["pageOrder"]:
        metadata["pageOrder"].append(guide_id)
    save(meta_path, metadata)
    # Add a dedicated footer outside existing visuals, never over a chart/filter.
    footer_key = ident("native-style:" + page_id + "-read-guide")
    existing = pagefile.parent / "visuals" / footer_key / "visual.json"
    if existing.exists():
        footer_y = read(existing)["position"]["y"]
    else:
        footer_y = page["height"] + 8
        page["height"] += 52
        save(pagefile, page)
    put(report, page_id, image(page_id + "-footer-info", "info", (36, footer_y + 6, 24, 24), dark))
    put(
        report,
        page_id,
        button(
            page_id + "-read-guide",
            "How to read this page • definitions & context",
            intro,
            (72, footer_y, 430, 36),
            guide_id,
            dark,
        ),
    )


def hashes(paths):
    return {
        str(p): hashlib.sha256(p.read_bytes()).hexdigest()
        for root in paths
        for p in root.rglob("*")
        if p.is_file()
    }


def board_icons(report):
    put(report, BOARD, image("board-heading-icon", "users", (36, 33, 42, 42)))
    for i, icon in enumerate(
        ("users", "house", "target", "triangle-alert", "clock", "pound-sterling")
    ):
        put(report, BOARD, image(f"board-kpi-icon-{i}", icon, (57 + 272 * i, 158, 34, 34)))
    # The user has replaced the old region placeholder with an actual status chart.
    # Do not leave the previous unavailable-region text covering that visual.
    folder = report / "definition/pages" / BOARD / "visuals"
    heading_path = folder / ident("board-annotation:heading") / "visual.json"
    heading = read(heading_path)
    heading["position"].update(y=22, height=42)
    save(heading_path, heading)
    for key in ("region-unavailable", "region-explanation"):
        path = folder / ident("board-annotation:" + key) / "visual.json"
        if path.exists():
            value = read(path)
            value["isHidden"] = True
            save(path, value)
    replacements = {
        "chart-title-3": "Referral Status Mix",
        "chart-caption-3": "Current status within the selected cohort",
    }
    for key, words in replacements.items():
        path = folder / ident("board-annotation:" + key) / "visual.json"
        value = read(path)
        value["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0][
            "value"
        ] = words
        save(path, value)
    detail = "Distinct referrals grouped by current recorded status in the selected cohort. This is a status distribution, not a geographical region breakdown or a historical transition flow."
    path = folder / ident("board-annotation:chart-info-3") / "visual.json"
    value = read(path)
    value["visual"]["visualContainerObjects"]["visualLink"][0]["properties"]["tooltip"] = L(
        quoted(detail)
    )
    value["visual"]["visualContainerObjects"]["general"] = obj(altText=L(quoted(detail)))
    save(path, value)
    guide_folder = report / "definition/pages" / ident("board-native-annotation-guide") / "visuals"
    for key, words in (("guide-title-1-3", "Referral Status Mix"), ("guide-body-1-3", detail)):
        path = guide_folder / ident("board-annotation:" + key) / "visual.json"
        value = read(path)
        value["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0][
            "value"
        ] = words
        save(path, value)


def main():
    reports = sorted(BUNDLE.glob("*/*.Report"))
    assert len(reports) == 2
    models = list(BUNDLE.glob("*/*.SemanticModel"))
    model_before = hashes(models)
    backup = BUNDLE / "_review" / ("native-style-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    backup.mkdir(parents=True, exist_ok=False)
    for report in reports:
        shutil.copytree(report / "definition", backup / report.name / "definition")
        shutil.copytree(report / "StaticResources", backup / report.name / "StaticResources")
    save(backup / "model-hashes.json", model_before)
    counts = {}
    for report in reports:
        install_icons(report)
        pages = list((report / "definition/pages").glob("*/page.json"))
        counts[report.name] = 0
        for pagefile in pages:
            page, dark = common_style(report, pagefile)
            if page["displayName"].endswith(" - guide"):
                continue
            page_id = page["name"]
            if page_id == SUPPLY:
                reference_page(report, page_id, page["displayName"], SUPPLY_KPIS, SUPPLY_CHARTS)
                entries = SUPPLY_KPIS + SUPPLY_CHARTS
            elif page_id == TARGET:
                reference_page(report, page_id, page["displayName"], TARGET_KPIS, TARGET_CHARTS)
                entries = TARGET_KPIS + TARGET_CHARTS
            elif page_id == SNAPSHOTS:
                snapshots(report)
                entries = SNAPSHOT_ENTRIES
            else:
                entries = guide_entries(pagefile)
            if page_id == BOARD:
                # Existing Board guide remains authoritative; do not duplicate it.
                board_icons(report)
                continue
            if not page.get("visibility") or page.get("pageBinding"):
                add_guide(report, pagefile, page, dark, entries)
            counts[report.name] += 1
        notes = [
            "# Native report annotations and icon audit",
            "",
            "Updated 27 September 2026. Changes are local to the semantic-model-attached delivery report; no publication or model edits.",
            "",
            "## Styling",
            "",
            "Cards and chart panels retain a native soft glow: light panels use #B78D98 at 80% transparency, 14px blur and 4px downward offset; dark panels use black at 70% transparency. The light canvas stays #F8F5F1. Headings/icons remain shadow-free. Reuse the WMPP Soft Glow / WMPP Soft Panel theme presets.",
            "",
            "Plain page colours; no visible composite skin. Editable Segoe UI headings and captions, borderless annotations, zero outer padding. Existing chart colours, filters, measures, bookmarks and drillthrough bindings are retained. The light WMPP and dark Mission Control palettes remain distinct.",
            "",
            "Visible pages and the job drillthrough page have a How to read this page footer linking to a hidden native guide. The Board retains its existing header/section guide buttons. Footer space is added below existing visuals, not over them. Compact tooltip/helper pages are styled in place.",
            "",
            "## Icons",
            "",
            f"Source: https://lucide.dev/icons/ — official lucide-icons/lucide revision `{REVISION}`.",
            "",
            "`lucide-*.svg` files in this project root are upstream originals. `lc-*-ink.svg` / `lc-*-light.svg` are report variants with only the stroke colour changed. The exact variants used by Power BI are also embedded as registered report resources. No API key is required.",
            "",
            "See `Lucide-provenance.json` for each source URL and SHA-256; retain `Lucide-LICENSE.txt` with client deliveries, including the ISC and applicable Feather/MIT notices.",
            "",
            "## Verification and acceptance",
            "",
            "One-off JSON/schema, layout bounds and preservation checks are used; no report-version-specific or semantic-model test suite is added. Native Power BI Desktop rendering, interaction and client refresh still require inspection. Older layout renders do not show this revision.",
            "",
            "## Page context",
            "",
        ]
        for pagefile in pages:
            page = read(pagefile)
            if page["displayName"] in INTROS:
                notes.extend(["### " + page["displayName"], "", INTROS[page["displayName"]], ""])
        (report.parent / "REPORT_ANNOTATIONS.md").write_text("\n".join(notes), encoding="utf-8")
    # Skin-free is not shadow-free: retain the current native card treatment.
    from apply_report_soft_glow import apply_report_glow

    for report in reports:
        apply_report_glow(report)
    assert hashes(models) == model_before, "A semantic-model file changed unexpectedly"
    save(
        backup / "summary.json",
        {
            "styled_original_pages": counts,
            "models_unchanged": True,
            "native_desktop_render_verified": False,
        },
    )
    print(
        json.dumps(
            {"backup": str(backup), "styled_original_pages": counts, "models_unchanged": True},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
