"""Repair entity-first WIP explorers and add context-aware KPI lists.

Explicit project argument; plans changes before applying; backs up touched files.
Never changes caches, credentials, roles, source queries or other report pages.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil

from build_report_design_delivery import field, fill, guid, ident, L, obj, project, quoted
from add_wmpp_table_icons_provider_detail import icon_format
import rebuild_mission_control_dashboard_v16 as ui

PROVIDER = "08ef33dc6a87d1b14392"
REFERRAL = "f3070e87127b751f89d4"
PROVIDER_DETAIL = "b8f53cbc2c75ffd952be"
REFERRAL_DETAIL = "4cad3706fca6451c66b8"
MT = "_Explorer KPI Measures"
ACCEPTED = '{"accepted", "approved", "selected", "offer_successful"}'
PENDING = '{"pending", "submitted", "offered", "offer_made", "offer_pending", "under_review", "under review", "awaiting", "awaiting_decision", "awaiting decision"}'


def measure_text(table, definitions):
    result = f"table {quoted(table)}\n\tlineageTag: {guid(table)}\n"
    for name, dax, fmt in definitions:
        result += f"\n\tmeasure {quoted(name)} =\n"
        result += "\n".join("\t\t\t" + line for line in dax.splitlines()) + "\n"
        result += f"\t\tlineageTag: {guid(table + name)}\n\t\tdisplayFolder: Explorer KPIs\n"
        if fmt:
            result += f"\t\tformatString: {fmt}\n"
    result += f"\n\tpartition {quoted(table)} = m\n\t\tmode: import\n\t\tsource = #table(type table [], {{}})\n"
    return result


def calculated_table(name, columns, expression):
    result = f"table {quoted(name)}\n\tlineageTag: {guid(name)}\n"
    for col, dtype in columns:
        result += f"\n\tcolumn {quoted(col)}\n\t\tdataType: {dtype}\n\t\tlineageTag: {guid(name + col)}\n\t\tsummarizeBy: none\n\t\tsourceColumn: [{col}]\n"
        if col == "Metric":
            result += "\t\tsortByColumn: Ordinal\n"
        if col == "Ordinal":
            result += "\t\tisHidden\n"
    result += f"\n\tpartition {quoted(name)} = calculated\n\t\tmode: import\n\t\tsource =\n"
    return result + "\n".join("\t\t\t" + line for line in expression.splitlines()) + "\n"


def replace_measure(text, name, dax):
    pattern = r"(?m)(^\tmeasure " + re.escape(quoted(name)) + r" =)[^\n]*\n(?:\t\t\t[^\n]*\n|\n)*"
    replacement = "\n" + "\n".join("\t\t\t" + line for line in dax.splitlines()) + "\n"
    result, n = re.subn(pattern, lambda m: m[1] + replacement, text, count=1)
    if n != 1:
        raise ValueError(f"Expected measure {name}")
    return result


def scope_provider(expression, fmt="#,0"):
    return (
        "VAR eligible = FILTER(VALUES('dim_provider'[provider_id]), CALCULATE([Explorer provider row visible]) = 1)\n"
        f"RETURN CALCULATE({expression}, KEEPFILTERS(eligible))",
        fmt,
    )


def provider_offer(expression):
    return scope_provider(
        "VAR homeFilter = ISFILTERED('dim_provider_home')\n"
        "VAR homes = VALUES('dim_provider_home'[provider_home_id])\n"
        f"RETURN CALCULATE({expression}, KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes)))"
    )[0]


def referral_scope():
    # No activity filter => all master referrals, including no offers. Independent
    # disconnected slicers do not silently trim one another's choices.
    return """VAR categories = VALUES('Referral Category'[Category ID])
VAR categoryRefs = CALCULATETABLE(VALUES('bridge_referral_framework_category'[referral_id]), TREATAS(categories,'bridge_referral_framework_category'[framework_category_id]))
VAR statuses = VALUES('Explorer Offer Status'[Status])
VAR bands = VALUES('Explorer Offer Activity'[Band])
VAR statusFilter = ISFILTERED('Explorer Offer Status'[Status])
VAR bandFilter = ISFILTERED('Explorer Offer Activity'[Band])
VAR offerRows = FILTER('fact_offer', (NOT statusFilter || COALESCE('fact_offer'[offer_status],"(Unknown status)") IN statuses) && (NOT bandFilter || COALESCE('fact_offer'[Offer activity band],"(Unknown activity)") IN bands))
VAR offeredRefs = SELECTCOLUMNS(offerRows,"Referral",'fact_offer'[referral_id])
VAR anyOfferedRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), REMOVEFILTERS('fact_offer'[offer_status], 'fact_offer'[Offer activity band]))
VAR noOfferChoice = (NOT statusFilter || "(No offers)" IN statuses) && (NOT bandFilter || "(No offers)" IN bands)
VAR eligible = FILTER(VALUES('fact_referral'[referral_id]), NOT ISBLANK('fact_referral'[referral_id]) &&
    (NOT ISCROSSFILTERED('Referral Category') || 'fact_referral'[referral_id] IN categoryRefs) &&
    (NOT(statusFilter || bandFilter) || 'fact_referral'[referral_id] IN offeredRefs || (noOfferChoice && NOT('fact_referral'[referral_id] IN anyOfferedRefs))))
"""


def scope_referral(expression, fmt="#,0"):
    return referral_scope() + f"RETURN CALCULATE({expression}, KEEPFILTERS(eligible))", fmt


def definitions():
    defs = []

    def add(name, value, fmt="#,0"):
        if isinstance(value, tuple):
            value, fmt = value
        defs.append((name, value, fmt))

    add(
        "Explorer provider row visible",
        """VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
VAR homeFilter = ISFILTERED('dim_provider_home')
VAR matchingHomes = CALCULATE(COUNTROWS('dim_provider_home'))
VAR stage = SELECTEDVALUE('Journey Provider Selection'[Stage], -1)
RETURN IF(NOT ISBLANK(providerKey) && (NOT homeFilter || matchingHomes > 0) && (stage = -1 || [Journey provider stage] == stage), 1, BLANK())""",
        "0",
    )
    add(
        "Explorer providers",
        scope_provider("COALESCE(DISTINCTCOUNTNOBLANK('dim_provider'[provider_id]),0)"),
    )
    add(
        "Explorer providers without offers",
        scope_provider(
            "COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), CALCULATE(COUNTROWS('fact_offer')) = 0))"
        ),
    )
    for suffix, fact in [
        ("assignment", "fact_referral_provider"),
        ("offer", "fact_offer"),
        ("message", "dim_referral_provider_message"),
        ("monthly", "fact_provider_kpi_monthly"),
    ]:
        add(
            f"Explorer provider {suffix} row visible",
            f"IF([Explorer provider row visible] = 1 && COUNTROWS('{fact}') > 0, 1, BLANK())",
            "0",
        )
    add(
        "Explorer provider homes",
        scope_provider("COALESCE(DISTINCTCOUNTNOBLANK('dim_provider_home'[provider_home_id]),0)"),
    )
    add("Explorer provider beds", scope_provider("SUM('dim_provider_home'[registered_beds])"))
    add(
        "Explorer provider offers",
        provider_offer("COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0)"),
    )
    add(
        "Explorer provider offers made",
        provider_offer(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', NOT ISBLANK('fact_offer'[offer_status]) && LOWER(TRIM('fact_offer'[offer_status])) <> \"draft\")))"
        ),
    )
    add(
        "Explorer provider drafts",
        provider_offer(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) = \"draft\")))"
        ),
    )
    add(
        "Explorer provider accepted offers",
        provider_offer(
            f"CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {ACCEPTED})))"
        ),
    )
    add(
        "Explorer provider pending offers",
        provider_offer(
            f"CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0), KEEPFILTERS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN {PENDING})))"
        ),
    )
    add(
        "Explorer provider assignments",
        scope_provider(
            "COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0)"
        ),
    )
    add(
        "Explorer provider assigned referrals",
        scope_provider("COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_id]),0)"),
    )
    add(
        "Explorer provider messages",
        scope_provider(
            "COALESCE(DISTINCTCOUNTNOBLANK('dim_referral_provider_message'[message_id]),0)"
        ),
    )
    add(
        "Explorer provider qualifying responses",
        scope_provider(
            "CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id]),0), KEEPFILTERS('fact_referral_provider'[has_qualifying_response] == TRUE()))"
        ),
    )
    add(
        "Explorer provider response rate",
        "DIVIDE([Explorer provider qualifying responses],[Explorer provider assignments])",
        "0.0%",
    )
    add(
        "Explorer provider offer acceptance rate",
        "DIVIDE([Explorer provider accepted offers],[Explorer provider offers made])",
        "0.0%",
    )
    add(
        "Explorer provider average response minutes",
        scope_provider("AVERAGE('fact_referral_provider'[response_elapsed_minutes])", "0.0"),
    )
    add(
        "Explorer provider median response minutes",
        scope_provider("MEDIAN('fact_referral_provider'[response_elapsed_minutes])", "0.0"),
    )
    for suffix, ipa_filter in [
        ("IPAs", "TRUE()"),
        ("signed IPAs", "'fact_ipa'[signed_by_provider] == TRUE()"),
        ("completed IPAs", "'fact_ipa'[is_ipa_completed] == TRUE()"),
    ]:
        add(
            "Explorer provider " + suffix,
            scope_provider(
                f"VAR homeFilter = ISFILTERED('dim_provider_home') VAR homes = VALUES('dim_provider_home'[provider_home_id]) VAR offers = CALCULATETABLE(VALUES('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer', NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))) RETURN CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]),0), KEEPFILTERS(TREATAS(offers,'fact_ipa'[accepted_offer_id])), KEEPFILTERS(FILTER('fact_ipa', {ipa_filter})))"
            ),
        )
    for col, label in [
        ("response_opportunity_count", "opportunities"),
        ("qualifying_response_count", "responses"),
        ("offers_submitted_count", "offers"),
        ("accepted_offer_count", "accepted offers"),
        ("successful_referral_count", "successful referrals"),
        ("placed_by_target_count", "placed by target"),
    ]:
        add("Explorer Gold " + label, scope_provider(f"SUM('fact_provider_kpi_monthly'[{col}])"))
    add(
        "Explorer Gold response rate",
        "DIVIDE([Explorer Gold responses],[Explorer Gold opportunities])",
        "0.0%",
    )
    add(
        "Explorer Gold offer acceptance rate",
        "DIVIDE([Explorer Gold accepted offers],[Explorer Gold offers])",
        "0.0%",
    )
    add(
        "Explorer Gold target placement rate",
        "DIVIDE([Explorer Gold placed by target],[Explorer Gold successful referrals])",
        "0.0%",
    )
    for stat_name in ["average", "median"]:
        add(
            f"Explorer Gold {stat_name} response minutes",
            scope_provider(
                f"IF(COUNTROWS('fact_provider_kpi_monthly') = 1, MAX('fact_provider_kpi_monthly'[{stat_name}_response_minutes]))",
                "0.0",
            ),
        )
    add(
        "Explorer referral row visible",
        referral_scope() + "RETURN IF(COUNTROWS(eligible) > 0, 1, BLANK())",
        "0",
    )
    add(
        "Explorer referrals",
        scope_referral("COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0)"),
    )
    for suffix, condition in [
        ("open", "'fact_referral'[is_open] == TRUE()"),
        ("open overdue", "'fact_referral'[is_open_overdue] == TRUE()"),
        (
            "closed",
            'LOWER(TRIM(\'fact_referral\'[current_status])) IN {"closed","cancelled","canceled","withdrawn","completed"}',
        ),
    ]:
        add(
            "Explorer referrals " + suffix,
            scope_referral(
                f"CALCULATE(COALESCE(DISTINCTCOUNTNOBLANK('fact_referral'[referral_id]),0), KEEPFILTERS(FILTER('fact_referral',{condition})))"
            ),
        )
    add(
        "Explorer referral offers",
        scope_referral("COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]),0)"),
    )
    add(
        "Explorer referrals with offers",
        scope_referral("COALESCE(DISTINCTCOUNTNOBLANK('fact_offer'[referral_id]),0)"),
    )
    add(
        "Explorer referrals without offers",
        "[Explorer referrals] - [Explorer referrals with offers]",
    )
    for suffix, expression in [
        ("assignments", "DISTINCTCOUNTNOBLANK('fact_referral_provider'[referral_provider_id])"),
        ("messages", "DISTINCTCOUNTNOBLANK('dim_referral_provider_message'[message_id])"),
        ("IPAs", "DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id])"),
        (
            "completed IPAs",
            "CALCULATE(DISTINCTCOUNTNOBLANK('fact_ipa'[ipa_id]), KEEPFILTERS('fact_ipa'[is_ipa_completed] == TRUE()))",
        ),
        (
            "accepted offers",
            f"CALCULATE(DISTINCTCOUNTNOBLANK('fact_offer'[offer_id]), KEEPFILTERS(FILTER('fact_offer',LOWER(TRIM('fact_offer'[offer_status])) IN {ACCEPTED})))",
        ),
    ]:
        add("Explorer referral " + suffix, scope_referral(f"COALESCE({expression},0)"))
    add(
        "Explorer referral offer coverage",
        "DIVIDE([Explorer referrals with offers],[Explorer referrals])",
        "0.0%",
    )
    return defs


PROVIDER_METRICS = [
    (
        "Directory",
        "Providers without any offers",
        "Explorer providers without offers",
        "No offer record, including no draft records",
    ),
    (
        "Directory",
        "Providers in selection",
        "Explorer providers",
        "Distinct provider IDs, including providers without offers",
    ),
    (
        "Directory",
        "Provider homes",
        "Explorer provider homes",
        "All matching registered homes; no offer required",
    ),
    (
        "Directory",
        "Registered beds",
        "Explorer provider beds",
        "Recorded capacity, not vacancies; missing values remain unknown",
    ),
    (
        "Activity",
        "Distinct offer records",
        "Explorer provider offers",
        "Distinct offer IDs, including drafts",
    ),
    (
        "Activity",
        "Distinct offers made",
        "Explorer provider offers made",
        "Non-draft records with a recorded status",
    ),
    ("Activity", "Draft offers", "Explorer provider drafts", "Distinct draft offer IDs"),
    (
        "Activity",
        "Accepted offers",
        "Explorer provider accepted offers",
        "Distinct accepted/approved/selected/successful offers",
    ),
    (
        "Activity",
        "Pending offers",
        "Explorer provider pending offers",
        "Distinct awaiting-decision offer IDs",
    ),
    (
        "Activity",
        "Offer acceptance rate",
        "Explorer provider offer acceptance rate",
        "Accepted offers / non-draft offers made",
    ),
    (
        "Engagement",
        "Assigned referrals",
        "Explorer provider assigned referrals",
        "Distinct referrals assigned to matching providers",
    ),
    (
        "Engagement",
        "Referral assignments",
        "Explorer provider assignments",
        "Distinct referral-provider assignment IDs",
    ),
    (
        "Engagement",
        "Recorded messages",
        "Explorer provider messages",
        "Messages in either direction; browsing is not captured",
    ),
    (
        "Engagement",
        "Qualifying responses",
        "Explorer provider qualifying responses",
        "Offer/reason response evidence, not every message",
    ),
    (
        "Engagement",
        "Qualifying response rate",
        "Explorer provider response rate",
        "Qualifying response assignments / assignments",
    ),
    (
        "Engagement",
        "Average response minutes",
        "Explorer provider average response minutes",
        "From assignment-level observations; excludes missing durations",
    ),
    (
        "Engagement",
        "Median response minutes",
        "Explorer provider median response minutes",
        "Recomputed from assignment-level observations",
    ),
    (
        "Placement",
        "IPAs linked to offers",
        "Explorer provider IPAs",
        "Linked by accepted offer ID, not all IPAs on a shared referral",
    ),
    (
        "Placement",
        "Provider-signed IPAs",
        "Explorer provider signed IPAs",
        "Provider signature evidence only",
    ),
    ("Placement", "Completed IPAs", "Explorer provider completed IPAs", "Recorded completion flag"),
]
REFERRAL_METRICS = [
    (
        "Referrals",
        "Referrals in selection",
        "Explorer referrals",
        "Master referral list; an offer is not required",
    ),
    ("Referrals", "Open referrals", "Explorer referrals open", "Recorded open flag"),
    ("Referrals", "Open and overdue", "Explorer referrals open overdue", "Recorded overdue flag"),
    (
        "Referrals",
        "Closed / cancelled / withdrawn",
        "Explorer referrals closed",
        "Recorded closed/terminal referral status",
    ),
    (
        "Offers",
        "Referrals with offers",
        "Explorer referrals with offers",
        "At least one offer record, including drafts",
    ),
    (
        "Offers",
        "Referrals without offers",
        "Explorer referrals without offers",
        "No offer record in the current source context",
    ),
    (
        "Offers",
        "Offer coverage",
        "Explorer referral offer coverage",
        "Referrals with offers / matching referrals",
    ),
    (
        "Offers",
        "Distinct offer records",
        "Explorer referral offers",
        "Distinct offer IDs linked to matching referrals",
    ),
    (
        "Offers",
        "Accepted offers",
        "Explorer referral accepted offers",
        "Distinct accepted/approved/selected/successful offers",
    ),
    (
        "Engagement",
        "Provider assignments",
        "Explorer referral assignments",
        "Distinct referral-provider assignment IDs",
    ),
    (
        "Engagement",
        "Recorded messages",
        "Explorer referral messages",
        "Message count in either direction, not browsing events",
    ),
    (
        "Placement",
        "IPAs",
        "Explorer referral IPAs",
        "Distinct IPA IDs linked to matching referrals",
    ),
    ("Placement", "Completed IPAs", "Explorer referral completed IPAs", "Recorded completion flag"),
]


def metric_axis(name, rows):
    data = [[group, label, i, note] for i, (group, label, _, note) in enumerate(rows)]
    encoded = ",\n".join("{" + ",".join(json.dumps(x) for x in row) + "}" for row in data)
    return calculated_table(
        name,
        [("Group", "string"), ("Metric", "string"), ("Ordinal", "int64"), ("Definition", "string")],
        'DATATABLE("Group",STRING,"Metric",STRING,"Ordinal",INTEGER,"Definition",STRING,{\n'
        + encoded
        + "\n})",
    )


def metric_value(axis, rows, defs, single=None):
    formats = {name: fmt for name, _, fmt in defs}
    cases = ",\n".join(
        f'{i}, IF(ISBLANK([{measure}]), "—", FORMAT([{measure}], "{formats[measure]}"))'
        for i, (_, _, measure, _) in enumerate(rows)
    )
    dax = f"SWITCH(SELECTEDVALUE({quoted(axis)}[Ordinal]),\n{cases}, BLANK())"
    return f"IF(HASONEVALUE({single}), {dax})" if single else dax


def swap_entities(node, mapping):
    if isinstance(node, list):
        return [swap_entities(x, mapping) for x in node]
    if isinstance(node, dict):
        return {k: swap_entities(v, mapping) for k, v in node.items()}
    if isinstance(node, str):
        if node in mapping:
            return mapping[node]
        for old, new in mapping.items():
            node = node.replace(old + ".", new + ".")
        return node
    return node


def new_table(name, title, columns, x, y, w, h):
    v = ui.visual_shell(name, "tableEx", ui.position(x, y, w, h, 170000))
    projections = []
    for table, col, label, measure in columns:
        pr = project(table, col, measure, label)
        pr["displayName"] = label
        projections.append(pr)
    v["visual"]["query"] = {"queryState": {"Values": {"projections": projections}}}
    v["visual"]["objects"] = {
        "columnHeaders": obj(fontSize=L("11D"), bold=L("false")),
        "values": obj(fontSize=L("11D")),
        "total": obj(totals=L("false")),
    }
    for t, c, _, measure in columns:
        if measure:
            continue
        kind = None
        if c in {"is_open", "is_open_overdue", "is_spot", "qa_flag"}:
            kind = "boolean"
        elif "status" in c:
            kind = "status"
        elif c in {"priority", "placement_urgency_band"}:
            kind = "priority"
        elif c == "service_type":
            kind = "placement"
        if kind:
            v["visual"]["objects"]["values"].append(
                {
                    "properties": {"icon": icon_format(t, c, kind)},
                    "selector": {
                        "data": [{"dataViewWildcard": {"matchingOption": 1}}],
                        "metadata": t + "." + c,
                    },
                }
            )
    v["visual"]["visualContainerObjects"] = {
        "title": obj(show=L("true"), text=L(quoted(title)), fontSize=L("13D"), bold=L("false")),
        "background": obj(show=L("true"), color=fill("#FFFFFF"), transparency=L("0D")),
        "border": obj(show=L("true"), color=fill("#FFFFFF"), radius=L("14D")),
    }
    return v


def gate(v, table, measure):
    v["filterConfig"] = {
        "filters": [
            {
                "name": ident(v["name"] + measure),
                "field": field(table, measure, True),
                "type": "Advanced",
                "howCreated": "User",
                "filter": {
                    "Version": 2,
                    "From": [{"Name": "m", "Entity": table, "Type": 0}],
                    "Where": [
                        {
                            "Condition": {
                                "Comparison": {
                                    "ComparisonKind": 2,
                                    "Left": {
                                        "Measure": {
                                            "Expression": {"SourceRef": {"Source": "m"}},
                                            "Property": measure,
                                        }
                                    },
                                    "Right": {"Literal": {"Value": "1L"}},
                                }
                            }
                        }
                    ],
                },
            }
        ]
    }


def build(bundle):
    model = bundle / "SM_WMPP_v16.SemanticModel/definition"
    definition = bundle / "SM_WMPP_v16.Report/definition"
    changes = {}
    docs = {}

    def read(path):
        return path.read_text(encoding="utf-8-sig")

    def json_doc(path):
        if path not in docs:
            docs[path] = json.loads(read(path))
        return docs[path]

    def put(page, v):
        docs[definition / "pages" / page / "visuals" / v["name"] / "visual.json"] = v

    def existing(page, name):
        return json_doc(definition / "pages" / page / "visuals" / name / "visual.json")

    # One canonical provider -> offer relationship, preserving the separate role
    # dimensions for offer-only reports. No bidirectional propagation is introduced.
    rel_path = model / "relationships.tmdl"
    rels = read(rel_path)
    if not re.search(
        r"fromColumn: fact_offer.provider_id\s+toColumn: dim_provider.provider_id", rels
    ):
        rels += f"\nrelationship {guid('explorer-provider-offer')}\n\tfromColumn: fact_offer.provider_id\n\ttoColumn: dim_provider.provider_id\n"
    changes[rel_path] = rels
    journey_path = model / "tables/_Journey Measures.tmdl"
    journey = (
        read(journey_path)
        .replace("'dim_provider (offer)'", "'dim_provider'")
        .replace("'dim_provider_home (offer)'", "'dim_provider_home'")
    )
    journey = journey.replace(
        "VAR homeScope = ISCROSSFILTERED('dim_provider_home')",
        "VAR homeScope = ISFILTERED('dim_provider_home')",
    )
    changes[journey_path] = journey
    interaction_path = model / "tables/_Journey Interaction.tmdl"
    interaction = (
        read(interaction_path)
        .replace("'dim_provider (offer)'", "'dim_provider'")
        .replace("'dim_provider_home (offer)'", "'dim_provider_home'")
    )
    interaction = replace_measure(
        interaction, "Rail provider row visible", "[Explorer provider row visible]"
    )
    # The previous chart used whole-model referrals when no journey stage was selected.
    interaction = replace_measure(
        interaction,
        "Rail provider selected metric",
        """VAR metric = IF(NOT ISCROSSFILTERED('Dashboard Metric Selector'), 3, SELECTEDVALUE('Dashboard Metric Selector'[Dashboard Metric Selector Order]))
RETURN SWITCH(metric, 0,[Explorer provider assigned referrals],3,[Explorer provider offers],4,[Explorer provider accepted offers],5,[Explorer provider pending offers],6,[Explorer provider IPAs],7,[Explorer provider completed IPAs],BLANK())""",
    )
    changes[interaction_path] = interaction
    defs = definitions()
    axes = {"Provider Explorer KPI": PROVIDER_METRICS, "Referral Explorer KPI": REFERRAL_METRICS}
    for axis, rows in axes.items():
        changes[model / "tables" / (axis + ".tmdl")] = metric_axis(axis, rows)
        prefix = "Provider" if axis.startswith("Provider") else "Referral"
        key = (
            "'dim_provider'[provider_id]"
            if prefix == "Provider"
            else "'fact_referral'[referral_id]"
        )
        defs += [
            (prefix + " explorer KPI value", metric_value(axis, rows, defs), ""),
            (prefix + " detail KPI value", metric_value(axis, rows, defs, key), ""),
        ]
    changes[model / "tables/Explorer Offer Status.tmdl"] = calculated_table(
        "Explorer Offer Status",
        [("Status", "string")],
        'DISTINCT(UNION(ROW("Status","(No offers)"), SELECTCOLUMNS(\'fact_offer\',"Status",COALESCE(\'fact_offer\'[offer_status],"(Unknown status)"))))',
    )
    changes[model / "tables/Explorer Offer Activity.tmdl"] = calculated_table(
        "Explorer Offer Activity",
        [("Band", "string")],
        'DISTINCT(UNION(ROW("Band","(No offers)"), SELECTCOLUMNS(\'fact_offer\',"Band",COALESCE(\'fact_offer\'[Offer activity band],"(Unknown activity)"))))',
    )
    changes[model / "tables" / (MT + ".tmdl")] = measure_text(MT, defs)
    model_text = read(model / "model.tmdl")
    for table in [MT, *axes, "Explorer Offer Status", "Explorer Offer Activity"]:
        ref = "ref table " + quoted(table)
        if ref not in model_text:
            model_text += "\n" + ref + "\n"
    changes[model / "model.tmdl"] = model_text
    story_path = model / "tables/_Story Measures.tmdl"
    changes[story_path] = replace_measure(
        read(story_path), "Matching referrals", "[Explorer referrals]"
    )
    # Both drillthrough pages remain entity-keyed, not offer- or home-keyed.
    for page, table, col in [
        (PROVIDER_DETAIL, "dim_provider", "provider_id"),
        (REFERRAL_DETAIL, "fact_referral", "referral_id"),
    ]:
        p = json_doc(definition / "pages" / page / "page.json")
        fid = ident(page + ":entity-drillthrough")
        p["filterConfig"] = {
            "filters": [
                {
                    "name": fid,
                    "field": field(table, col),
                    "type": "Categorical",
                    "howCreated": "Drillthrough",
                }
            ]
        }
        p["pageBinding"] = {
            "name": ident(page + ":entity-binding"),
            "type": "Drillthrough",
            "parameters": [
                {
                    "name": ident(page + ":entity-parameter"),
                    "boundFilter": fid,
                    "fieldExpr": field(table, col),
                }
            ],
            "acceptsFilterContext": "None",
        }
    for page in [PROVIDER, PROVIDER_DETAIL]:
        for path in (definition / "pages" / page / "visuals").glob("*/visual.json"):
            docs[path] = swap_entities(
                json_doc(path),
                {
                    "dim_provider (offer)": "dim_provider",
                    "dim_provider_home (offer)": "dim_provider_home",
                },
            )
    # Master provider list never groups on home/offer/message facts.
    v = existing(PROVIDER, "23150d16760f289f4166")
    cols = [
        ("dim_provider", c, label, False)
        for c, label in [
            ("provider_id", "Provider ID"),
            ("provider_name", "Provider"),
            ("provider_status", "Status"),
            ("town_city", "Town / city"),
            ("postcode", "Postcode"),
        ]
    ]
    cols += [
        (MT, m, label, True)
        for m, label in [
            ("Explorer provider homes", "Homes"),
            ("Explorer provider offers made", "Offers made"),
            ("Explorer provider accepted offers", "Accepted"),
            ("Explorer provider messages", "Messages"),
            ("Explorer provider assignments", "Assignments"),
            ("Explorer provider response rate", "Response rate"),
            ("Explorer provider completed IPAs", "Completed IPAs"),
        ]
    ]
    new = new_table(
        v["name"],
        "Provider directory — includes providers without offers",
        cols,
        36,
        1044,
        1608,
        330,
    )
    gate(new, MT, "Explorer provider row visible")
    put(PROVIDER, new)
    v = existing(PROVIDER, "d55d271a06ed4dcd1ad1")
    cols = [
        ("Provider Explorer KPI", "Metric", "KPI", False),
        (MT, "Provider explorer KPI value", "Value", True),
    ]
    put(
        PROVIDER,
        new_table(v["name"], "KPIs for matching / selected providers", cols, 1024, 354, 620, 660),
    )
    for name in ["b1c7e6028b7b1c565017", "3a3d0319cf091735159b"]:
        v = existing(PROVIDER, name)
        v["position"]["y"] = 1404
        v["position"]["height"] = 400
        gate(
            v,
            MT,
            "Explorer provider assignment row visible"
            if name.startswith("b1c")
            else "Explorer provider offer row visible",
        )
        if name.startswith("3a3"):
            v["visual"]["query"]["queryState"]["Values"]["projections"] += [
                project("dim_provider_home (offer)", "home_name", label="Proposed home")
            ]
    for path in (definition / "pages" / PROVIDER / "visuals").glob("*/visual.json"):
        v = json_doc(path)
        if not v.get("visual", {}).get("query") and v["position"]["y"] >= 1830:
            v["position"]["y"] += 1800
    v = existing(PROVIDER, "d2bf8cf3bfb4b834b9b9")
    v["position"].update(x=36, y=3260, width=1608, height=330)
    for well in v["visual"]["query"]["queryState"].values():
        for pr in well.get("projections", []):
            if pr.get("field", {}).get("Measure"):
                pr.update(project(MT, "Explorer Gold offer acceptance rate", True))
    v["visual"]["query"].pop("sortDefinition", None)
    # Conversion by provider must also follow provider journey/home search scope.
    v = existing(PROVIDER, "7ecbf97386432be48354")
    for well in v["visual"]["query"]["queryState"].values():
        for pr in well.get("projections", []):
            if pr.get("field", {}).get("Measure"):
                pr.update(project(MT, "Explorer provider offer acceptance rate", True))
    v["visual"]["query"].pop("sortDefinition", None)
    homecols = [
        ("dim_provider_home", c, label, False)
        for c, label in [
            ("provider_home_id", "Home ID"),
            ("home_name", "Home"),
            ("service_type", "Placement type"),
            ("town_city", "Town / city"),
            ("postcode", "Postcode"),
            ("registered_beds", "Registered beds"),
            ("is_spot", "Spot"),
            ("qa_flag", "QA flag"),
        ]
    ]
    homecols += [
        (MT, "Explorer provider offers", "Offer records", True),
        (MT, "Explorer provider offers made", "Offers made", True),
        (MT, "Explorer provider accepted offers", "Accepted offers", True),
    ]
    home_v = new_table(
        ident("explorer-scope:provider-homes"),
        "Provider homes — including homes with no offers",
        [
            ("dim_provider", "provider_id", "Provider ID", False),
            ("dim_provider", "provider_name", "Provider", False),
        ]
        + homecols,
        36,
        1834,
        1608,
        350,
    )
    gate(home_v, MT, "Explorer provider row visible")
    put(PROVIDER, home_v)
    messages = [("fact_referral_provider", "referral_id", "Referral ID", False)] + [
        ("dim_referral_provider_message", c, label, False)
        for c, label in [
            ("message_id", "Message ID"),
            ("created_timestamp", "Created"),
            ("created_by", "Created by"),
            ("message_text", "Message"),
            ("message_read_timestamp", "Read"),
        ]
    ]
    mv = new_table(
        ident("explorer-scope:provider-messages"),
        "Recorded messages for matching providers",
        [
            ("dim_provider", "provider_id", "Provider ID", False),
            ("dim_provider", "provider_name", "Provider", False),
        ]
        + messages,
        36,
        2220,
        1608,
        400,
    )
    gate(mv, MT, "Explorer provider message row visible")
    put(PROVIDER, mv)
    monthly_cols = [
        ("dim_provider", "provider_id", "Provider ID", False),
        ("dim_provider", "provider_name", "Provider", False),
    ]
    monthly_cols += [
        ("fact_provider_kpi_monthly", c, label, False)
        for c, label in [
            ("assignment_month", "Assignment cohort month"),
            ("security_scope_key", "Scope"),
            ("response_opportunity_count", "Response opportunities"),
            ("qualifying_response_count", "Qualifying responses"),
            ("offers_submitted_count", "Offer records"),
            ("accepted_offer_count", "Accepted offers"),
            ("successful_referral_count", "Successful referrals"),
            ("placed_by_target_count", "Placed by target"),
            ("average_response_minutes", "Average response minutes"),
            ("median_response_minutes", "Median response minutes"),
        ]
    ]
    monthly = new_table(
        ident("explorer-scope:monthly-provider"),
        "Gold provider KPIs — recorded provider / assignment-month / scope rows",
        monthly_cols,
        36,
        2670,
        1608,
        480,
    )
    gate(monthly, MT, "Explorer provider monthly row visible")
    put(PROVIDER, monthly)
    # Detail: preserve all existing activity sections and add a KPI list above homes.
    for path in (definition / "pages" / PROVIDER_DETAIL / "visuals").glob("*/visual.json"):
        v = json_doc(path)
        if v["position"]["y"] >= 479:
            v["position"]["y"] += 670
    put(
        PROVIDER_DETAIL,
        new_table(
            ident("explorer-scope:provider-detail-kpi"),
            "Selected provider KPIs",
            [
                ("Provider Explorer KPI", "Group", "Area", False),
                ("Provider Explorer KPI", "Metric", "KPI", False),
                (MT, "Provider detail KPI value", "Value", True),
                ("Provider Explorer KPI", "Definition", "Definition", False),
            ],
            36,
            479,
            1608,
            620,
        ),
    )
    v = existing(PROVIDER_DETAIL, "ebc5fdd0bf864b3d221f")
    v["visual"]["query"]["queryState"]["Values"]["projections"] = [
        dict(project(t, c, m, label), displayName=label) for t, c, label, m in homecols
    ]
    gate(v, "_Provider Detail Measures", "Provider detail home rows")
    # Use role-specific offer homes in offer-detail rows, avoiding an unrelated
    # crossjoin to every home registered to that provider.
    v = existing(PROVIDER_DETAIL, "a6749ca9664490c2ea5d")
    for pr in v["visual"]["query"]["queryState"]["Values"]["projections"]:
        if (
            pr["field"].get("Column", {}).get("Expression", {}).get("SourceRef", {}).get("Entity")
            == "dim_provider_home"
        ):
            pr.update(swap_entities(pr, {"dim_provider_home": "dim_provider_home (offer)"}))
    gate(v, "_Provider Detail Measures", "Provider detail offer rows")
    detail_monthly = deepcopy(monthly)
    detail_monthly["name"] = ident("explorer-scope:monthly-provider-detail")
    detail_monthly["position"].update(y=2840, height=480)
    gate(detail_monthly, MT, "Explorer provider monthly row visible")
    put(PROVIDER_DETAIL, detail_monthly)
    for name in ["249faf528a7281564965", "65a18b5e0a8121030050"]:
        v = existing(PROVIDER_DETAIL, name)
        metric = (
            "Explorer provider homes" if name.startswith("249") else "Explorer provider offers made"
        )
        v["visual"]["query"] = {
            "queryState": {"Data": {"projections": [project(MT, metric, True)]}}
        }
        gate(v, "_Provider Detail Measures", "Provider detail profile rows")
    # Referral directory: no raw offer fields in the base list, and explicit
    # detached activity selections support a No offers choice.
    for visual, table, col in [
        ("166b5d2a167216361c67", "Explorer Offer Status", "Status"),
        ("1d6a221eb0795ab5916a", "Explorer Offer Activity", "Band"),
    ]:
        v = existing(REFERRAL, visual)
        v["visual"]["query"] = {
            "queryState": {"Values": {"projections": [dict(project(table, col), active=True)]}}
        }
        v["visual"].setdefault("objects", {}).pop("general", None)
        v.pop("filterConfig", None)
    # The archived search slicers were hidden; supply an always-visible entity key search.
    v = deepcopy(existing(REFERRAL, "caecb1a99d366a8efa12"))
    v["name"] = ident("explorer-scope:referral-search")
    v.pop("isHidden", None)
    v["position"].update(x=36, y=470, width=800, height=64, z=170000, tabOrder=170000)
    v["visual"].setdefault("objects", {}).pop("general", None)
    v["visual"]["visualContainerObjects"]["title"] = obj(
        show=L("true"), text=L("'Search / select referral IDs'"), fontSize=L("12D"), bold=L("false")
    )
    put(REFERRAL, v)
    v = deepcopy(existing(REFERRAL, "b38106da2fdc38f7c64b"))
    v["name"] = ident("explorer-scope:person-search")
    v.pop("isHidden", None)
    v["position"].update(x=852, y=470, width=792, height=64, z=170000, tabOrder=171000)
    v["visual"].setdefault("objects", {}).pop("general", None)
    v["visual"]["visualContainerObjects"]["title"] = obj(
        show=L("true"), text=L("'Search / select person'"), fontSize=L("12D"), bold=L("false")
    )
    put(REFERRAL, v)
    directory = existing(REFERRAL, "4a70f5c5a98aea85ed0a")
    columns = [
        ("fact_referral", c, label, False)
        for c, label in [
            ("referral_id", "Referral ID"),
            ("priority", "Priority"),
            ("placement_urgency_band", "Urgency"),
            ("current_status", "Status"),
            ("is_open", "Open"),
            ("is_open_overdue", "Open overdue"),
            ("referral_created_date", "Created"),
            ("required_placement_date", "Required date"),
        ]
    ]
    columns += [
        (MT, m, label, True)
        for m, label in [
            ("Explorer referral offers", "Offers"),
            ("Explorer referral assignments", "Assignments"),
            ("Explorer referral messages", "Messages"),
            ("Explorer referral completed IPAs", "Completed IPAs"),
        ]
    ]
    new = new_table(
        directory["name"],
        "Referral directory — includes referrals without offers",
        columns,
        36,
        1710,
        1608,
        530,
    )
    gate(new, MT, "Explorer referral row visible")
    put(REFERRAL, new)
    put(
        REFERRAL,
        new_table(
            ident("explorer-scope:referral-kpi"),
            "KPIs for matching / selected referrals",
            [
                ("Referral Explorer KPI", "Metric", "KPI", False),
                (MT, "Referral explorer KPI value", "Value", True),
                ("Referral Explorer KPI", "Definition", "Definition", False),
            ],
            36,
            1240,
            1608,
            420,
        ),
    )
    put(
        REFERRAL_DETAIL,
        new_table(
            ident("explorer-scope:referral-detail-kpi"),
            "Selected referral KPIs",
            [
                ("Referral Explorer KPI", "Metric", "KPI", False),
                (MT, "Referral detail KPI value", "Value", True),
                ("Referral Explorer KPI", "Definition", "Definition", False),
            ],
            36,
            2500,
            1608,
            420,
        ),
    )
    # Correct the pre-existing missing home entity on this detail page.
    for path in (definition / "pages" / REFERRAL_DETAIL / "visuals").glob("*/visual.json"):
        docs[path] = swap_entities(
            json_doc(path), {"dim_provider_home_offer": "dim_provider_home (offer)"}
        )
    provider_detail_measures = model / "tables/_Provider Detail Measures.tmdl"
    text = read(provider_detail_measures)
    text = replace_measure(
        text,
        "Provider detail offer rows",
        "VAR n = CALCULATE(COUNTROWS('fact_offer'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]), 'fact_offer'[provider_id]))) RETURN IF(HASONEVALUE('dim_provider'[provider_id]) && n > 0,n)",
    )
    changes[provider_detail_measures] = text
    # Tall pages retain their navigation/menu IDs and bookmark-only visibility.
    for page, height in [
        (PROVIDER, 3830),
        (REFERRAL, 2310),
        (PROVIDER_DETAIL, 3430),
        (REFERRAL_DETAIL, 2990),
    ]:
        json_doc(definition / "pages" / page / "page.json")["height"] = height
    for page, source in [(PROVIDER, "23150d16760f289f4166"), (REFERRAL, "4a70f5c5a98aea85ed0a")]:
        p = json_doc(definition / "pages" / page / "page.json")
        interactions = p.setdefault("visualInteractions", [])
        for path, v in docs.items():
            if (
                path.name != "visual.json"
                or path.parents[2].name != page
                or v["name"] == source
                or not v.get("visual", {}).get("query")
                or v.get("isHidden")
            ):
                continue
            kind = v["visual"]["visualType"]
            if kind == "slicer" or kind.startswith("textFilter"):
                continue
            interactions[:] = [
                entry
                for entry in interactions
                if not (entry["source"] == source and entry["target"] == v["name"])
            ]
            interactions.append({"source": source, "target": v["name"], "type": "DataFilter"})
    # New KPI visuals must not be included in old filter/menu visibility snapshots.
    # Only rebind activity slicer snapshots if a bookmark actually names them.
    for path in (definition / "bookmarks").glob("*.bookmark.json"):
        b = json.loads(read(path))
        sections = b.get("explorationState", {}).get("sections", {})
        if REFERRAL in sections:
            section = sections[REFERRAL]
            containers = section.get("visualContainers", {})
            for visual in ["166b5d2a167216361c67", "1d6a221eb0795ab5916a"]:
                if visual in containers:
                    # Display state is retained; old offer slicer filter state is removed.
                    for key in ["singleVisual", "filters", "query", "dataTransforms"]:
                        containers[visual].pop(key, None)
            if b != json.loads(read(path)):
                docs[path] = b
    for path, doc in docs.items():
        content = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"
        if not path.exists() or json.loads(read(path)) != doc:
            changes[path] = content
    # Drop no-op changes; retain untouched disk files exactly.
    return {p: content for p, content in changes.items() if not p.exists() or read(p) != content}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    bundle = args.project.resolve()
    if not (bundle / "SM_WMPP_v16.pbip").is_file():
        raise ValueError("Expected the explicit saved WMPP PBIP project folder")
    if args.apply and (bundle / "EXPLORER_SCOPE_REPAIR.json").exists():
        raise ValueError("Repair already applied; inspect its backup/manifest before reapplying")
    if (bundle / "SM_WMPP_v16.SemanticModel/unappliedChanges.json").exists():
        raise ValueError("Apply pending model query changes in Desktop first")
    changes = build(bundle)
    print(f"Prepared {len(changes)} changed/new files in {bundle}; apply={args.apply}")
    if not args.apply:
        return
    backup = (
        bundle.parent / "_review" / ("explorer-scope-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    backup.mkdir(parents=True, exist_ok=False)
    originals = {}
    for path in changes:
        if path.exists():
            relative = path.relative_to(bundle)
            destination = backup / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)
            originals[str(relative)] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path, content in changes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = {
        "project": str(bundle),
        "backup": str(backup),
        "changed_files": [str(p.relative_to(bundle)) for p in changes],
        "original_hashes": originals,
        "desktop_render_verified": False,
        "published": False,
        "cache_untouched": True,
    }
    (bundle / "EXPLORER_SCOPE_REPAIR.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {k: v for k, v in manifest.items() if k not in {"original_hashes", "changed_files"}},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
