"""Reconcile the WMPP v16 semantic model and add operational report pages.

The script is intentionally deterministic so that the extracted client package can
be rebuilt and reviewed without Power BI Desktop.  It preserves the client live
connection in ``definition.pbir`` and creates ``definition-local.pbir`` for the
repository-local reconciled semantic model.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
import zipfile
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURRENT = PROJECT_ROOT / "reports" / "current"

MODEL_ROOT = CURRENT / "SM WMPP v16 updated" / "SM_WMPP_v16.SemanticModel"
MODEL_DEFINITION = MODEL_ROOT / "definition"
MODEL_TABLES = MODEL_DEFINITION / "tables"
MODEL_MEASURES = MODEL_TABLES / "_Measures.tmdl"
CANONICAL_MEASURES = CURRENT / "_Measures.tmdl"
BASELINE_MEASURES = (
    CURRENT
    / "SM WMPP v16"
    / "SM WMPP v16 updated"
    / "SM_WMPP_v16.SemanticModel"
    / "definition"
    / "tables"
    / "_Measures.tmdl"
)
SOURCE_BUNDLE = CURRENT / "SM WMPP v16 updated.zip"
SOURCE_MEASURE_ENTRY = (
    "SM WMPP v16 updated/SM_WMPP_v16.SemanticModel/"
    "definition/tables/_Measures.tmdl"
)
KPI_SELECTOR = MODEL_TABLES / "KPI Selector.tmdl"
DIM_PERSON = MODEL_TABLES / "dim_person.tmdl"
MODEL_FILE = MODEL_DEFINITION / "model.tmdl"

LOCAL_REPORT = CURRENT / "SM WMPP v16 updated" / "SM_WMPP_v16.Report"
CLIENT_REPORT = CURRENT / "RPT WMPP v16" / "WMPP_DASHBOARD_v16.Report"
CLIENT_DEFINITION = CLIENT_REPORT / "definition"
CLIENT_PAGES = CLIENT_DEFINITION / "pages"


# These are the one-to-one replacements explicitly agreed in the Gold DAX guide.
# Entries are used only when both the legacy and replacement measures exist.
GUIDE_ALIAS_MAP = {
    "Open Referral": "Open Referrals",
    "Referrals This Month": "Referrals Created This Month",
    "Referrals This FY": "Referrals Created This Financial Year",
    "Referrals With Offers": "Referrals With an Offer",
    "Referrals With One or More Offers": "Referrals With an Offer",
    "Active Referrals Awaiting Offers": "Referrals Awaiting Offer",
    "Active Referrals Under Offer": "Referrals Under Offer",
    "Referrals Cancelled/Closed": "Closed or Cancelled Referrals",
    "Closed Referrals (by Reason)": "Closed Referrals",
    "Active Awaiting Offers (Engaged)": "Active Referrals With Provider Engagement",
    "Active Awaiting Offers (No Engagement)": "Active Awaiting Offers Without Engagement",
    "Offer Count": "Offers Submitted",
    "Total Offers Made Historically": "Offers Submitted",
    "(NEW)Total Offers Made": "Offers Submitted",
    "Latest Offer Status Count": "Offers Submitted",
    "Placement Type Totals (Visual)": "Total Referrals",
    "Offers At Risk (8-14 Days)": "Pending Offers 8–14 Days",
    "Offers Outside Timeframe (15-30 Days)": "Pending Offers 15–30 Days",
    "Critical Offers (30+ Days)": "Pending Offers 30+ Days",
    "Provider with Offers over 30+ Days": "Providers With Pending Offers 30+ Days",
    "Draft No Activity 7+ Days": "Draft Offers Stalled 7+ Days",
    "Drafts With No Activity 14+ Days": "Draft Offers Stalled 14+ Days",
    "Draft Offers Updated After Creation": "Draft Offers With Activity Since Creation",
    "Draft With No Activity Since Creation (%)": "Draft Offers With No Activity %",
    "Latest Export per Offer": "Latest Offer Source Export",
    "Dashboard Last Refreshed:": "Gold Model Last Refreshed",
    "Average Active Weekly Cost": "Average Active IPA Weekly Cost",
    "Overlap Referrals": "Referrals With Multiple Provider Assignments",
    "Fostering Providers": "Providers - Fostering",
    "NON Framework Providers": "Non-Framework Providers",
    "Total Offers Made (Active Referrals Under Offer)": "Offers on Referrals Under Offer",
    "Avg Offers per Referral Under Offer": "Average Offers per Referral Under Offer",
    "IPA Created (successful offers with IPA)": "Accepted Offers With IPA",
    "Offers Still to Progress to IPA": "Offers Awaiting IPA Creation",
    "Referrals with Placement at Snapshot": "Referrals with IPA at Snapshot",
}

# Broken legacy visual binding: the misspelled measure never existed in the
# supplied semantic model.  It is the historic equivalent of the period-aware
# referral-with-offer measure.
REPORT_BINDING_FIXES = {
    "Total Referral That Recieved Offers": "Referrals With Offers (Created in Period)",
    # Repair an earlier prefix-based replacement of the plural legacy name.
    "Referrals With an Offer (Created in Period)": "Referrals With Offers (Created in Period)",
}

REPORT_FIELD_FIXES = (
    ("Referral Closure Reason Summary", "Closed Referral Reason Bucket", "fact_referral", "referral_closure_reason"),
    ("fact_referral_offer", "Closure Reason Clean", "fact_referral", "referral_closure_reason"),
    ("dim_referral", "placement_type", "dim_placement_type", "placement_type"),
    ("dim_date", "Date", "dim_date", "date"),
    ("dim_provider", "Service Type (Unified)", "dim_provider_home", "service_type"),
    ("fact_ipa", "provider_name", "dim_provider", "provider_name"),
    ("fact_ipa", "home_name", "dim_provider_home", "home_name"),
    ("fact_ipa", "offer_id", "fact_ipa", "accepted_offer_id"),
    ("fact_ipa", "placement_service_type", "dim_provider_home", "service_type"),
    ("fact_ipa", "placement_framework_or_spot", "fact_referral", "is_spot"),
)

METRIC_SELECTOR_MEASURES = (
    "Total Referrals",
    "Referrals Awaiting Offer",
    "Referrals Under Offer",
    "Offers Submitted",
    "Accepted Offers",
    "Pending Offers",
    "IPAs Created",
    "IPA Completed",
)


MEASURE_BLOCK = re.compile(
    r"(?ms)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*=.*?(?=^\tmeasure\s+|^\tpartition\s+)"
)
MEASURE_HEADER = re.compile(
    r"(?m)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*=\s*"
)
EMPTY_PLACEHOLDER_MEASURE = re.compile(
    r"(?ms)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*$.*?(?=^\tmeasure\s+|^\tpartition\s+)"
)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def measure_name(match: re.Match[str]) -> str:
    raw = match.group(1) if match.group(1) is not None else match.group(2)
    return raw.strip().replace("''", "'")


def measure_blocks(text: str) -> dict[str, str]:
    return {measure_name(match): match.group(0) for match in MEASURE_BLOCK.finditer(text)}


def measure_expression(block: str) -> str:
    header = MEASURE_HEADER.search(block)
    if not header:
        return ""
    tail = block[header.end() :]
    if tail.startswith("```"):
        end = tail.find("```", 3)
        return tail[3:end].strip() if end >= 0 else ""
    return tail.splitlines()[0].strip()


def direct_alias_target(expression: str) -> str | None:
    compact = re.sub(r"\s+", " ", expression).strip()
    match = re.fullmatch(r"(?:'_Measures'\s*)?\[([^\]]+)\]", compact)
    return match.group(1).strip() if match else None


def resolve_alias(name: str, aliases: dict[str, str]) -> str:
    seen: set[str] = set()
    current = name
    while current in aliases and current not in seen:
        seen.add(current)
        current = aliases[current]
    return current


def build_alias_map(text: str) -> dict[str, str]:
    blocks = measure_blocks(text)
    names = set(blocks)
    aliases: dict[str, str] = {}
    for name, block in blocks.items():
        target = direct_alias_target(measure_expression(block))
        if target and target in names and target != name:
            aliases[name] = target
    for legacy, replacement in GUIDE_ALIAS_MAP.items():
        if legacy in names and replacement in names and legacy != replacement:
            aliases[legacy] = replacement
    return {name: resolve_alias(target, aliases) for name, target in aliases.items()}


def replace_measure_tokens(text: str, aliases: dict[str, str]) -> str:
    # Longest first prevents a shorter name from matching a prefix in JSON strings.
    for legacy in sorted(aliases, key=len, reverse=True):
        target = aliases[legacy]
        text = text.replace(f"'_Measures'[{legacy}]", f"'_Measures'[{target}]")
        text = text.replace(f"_Measures[{legacy}]", f"_Measures[{target}]")
        text = text.replace(f"_Measures.{legacy}", f"_Measures.{target}")
        text = text.replace(f"[{legacy}]", f"[{target}]")
    return text


def clean_measure_file(path: Path, aliases: dict[str, str]) -> int:
    text = replace_measure_tokens(read_text(path), aliases)
    removed = 0

    def keep_or_remove(match: re.Match[str]) -> str:
        nonlocal removed
        name = measure_name(match)
        if name in aliases:
            removed += 1
            return ""
        return match.group(0)

    text = MEASURE_BLOCK.sub(keep_or_remove, text)

    def remove_placeholder(match: re.Match[str]) -> str:
        nonlocal removed
        name = (match.group(1) or match.group(2)).strip().replace("''", "'")
        if name in {"Measure", "Measure 2"}:
            removed += 1
            return ""
        return match.group(0)

    text = EMPTY_PLACEHOLDER_MEASURE.sub(remove_placeholder, text)
    write_text(path, text)
    return removed


def update_json_measure_refs(value: Any, aliases: dict[str, str], parent_key: str = "") -> Any:
    if isinstance(value, list):
        return [update_json_measure_refs(item, aliases, parent_key) for item in value]
    if isinstance(value, dict):
        for key, item in list(value.items()):
            if key == "Measure" and isinstance(item, dict):
                source = item.get("Expression", {}).get("SourceRef", {}).get("Entity")
                prop = item.get("Property")
                if source == "_Measures" and prop in aliases:
                    item["Property"] = aliases[prop]
            value[key] = update_json_measure_refs(item, aliases, key)
        return value
    if isinstance(value, str):
        updated = value
        for legacy in sorted(aliases, key=len, reverse=True):
            target = aliases[legacy]
            if updated == f"_Measures.{legacy}":
                updated = f"_Measures.{target}"
            updated = updated.replace(f"'_Measures'[{legacy}]", f"'_Measures'[{target}]")
            if parent_key == "nativeQueryRef" and updated == legacy:
                updated = target
        return updated
    return value


def clean_report_measure_refs(report: Path, aliases: dict[str, str]) -> int:
    changed = 0
    for path in (report / "definition").rglob("*.json"):
        before = path.read_text(encoding="utf-8-sig")
        value = json.loads(before)
        updated = update_json_measure_refs(value, aliases)
        after = json.dumps(updated, indent=2, ensure_ascii=False) + "\n"
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
    return changed


def clean_report_field_refs(report: Path) -> int:
    changed = 0
    for path in (report / "definition").rglob("*.json"):
        before = path.read_text(encoding="utf-8-sig")
        value = json.loads(before)
        for old_entity, old_property, new_entity, new_property in REPORT_FIELD_FIXES:
            value = replace_field(value, old_entity, old_property, new_entity, new_property)
        after = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
    return changed


def reconcile_kpi_selector(aliases: dict[str, str], valid_measures: set[str]) -> int:
    text = read_text(KPI_SELECTOR)
    row_pattern = re.compile(
        r'^\s*\("(?:[^"\\]|\\.)*",\s*NAMEOF\(\'_Measures\'\[([^\]]+)\]\),\s*\d+\),?\s*$',
        re.MULTILINE,
    )
    resolved: list[str] = []
    for match in row_pattern.finditer(text):
        name = resolve_alias(match.group(1), aliases)
        if name in valid_measures and name not in resolved:
            resolved.append(name)
    if not resolved:
        raise RuntimeError("No KPI Selector rows could be parsed")
    rows = "\n".join(
        f'\t\t\t\t    ("{name.replace(chr(34), chr(34) * 2)}", NAMEOF(\'_Measures\'[{name}]), {index}),'
        for index, name in enumerate(resolved)
    )
    source_pattern = re.compile(r"(?ms)(\tpartition 'KPI Selector' = calculated.*?\n\t\tsource =\s*\n)\t\t\t\t\{.*?\n\t\t\t\t\}")
    replacement = r"\1\t\t\t\t{\n" + rows + "\n\t\t\t\t}"
    updated, count = source_pattern.subn(replacement, text, count=1)
    if count != 1:
        raise RuntimeError("KPI Selector calculated partition was not found")
    write_text(KPI_SELECTOR, updated)
    return len(resolved)


def stable_guid(label: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"wmpp-v16:{label}"))


def add_metric_selector(valid_measures: set[str]) -> None:
    missing = [name for name in METRIC_SELECTOR_MEASURES if name not in valid_measures]
    if missing:
        raise RuntimeError(f"Metric selector measures missing: {missing}")
    rows = "\n".join(
        f'\t\t\t\t    ("{name}", NAMEOF(\'_Measures\'[{name}]), {index}),'
        for index, name in enumerate(METRIC_SELECTOR_MEASURES)
    )
    content = f"""table 'Dashboard Metric Selector'
\tlineageTag: {stable_guid('dashboard-metric-selector-table')}

\tcolumn 'Dashboard Metric Selector'
\t\tlineageTag: {stable_guid('dashboard-metric-selector-label')}
\t\tsummarizeBy: none
\t\tsourceColumn: [Value1]
\t\tsortByColumn: 'Dashboard Metric Selector Order'

\t\trelatedColumnDetails
\t\t\tgroupByColumn: 'Dashboard Metric Selector Fields'

\t\tannotation SummarizationSetBy = Automatic

\tcolumn 'Dashboard Metric Selector Fields'
\t\tisHidden
\t\tlineageTag: {stable_guid('dashboard-metric-selector-fields')}
\t\tsummarizeBy: none
\t\tsourceColumn: [Value2]
\t\tsortByColumn: 'Dashboard Metric Selector Order'

\t\textendedProperty ParameterMetadata =
\t\t\t\t{{
\t\t\t\t  "version": 3,
\t\t\t\t  "kind": 2
\t\t\t\t}}

\t\tannotation SummarizationSetBy = Automatic

\tcolumn 'Dashboard Metric Selector Order'
\t\tisHidden
\t\tformatString: 0
\t\tlineageTag: {stable_guid('dashboard-metric-selector-order')}
\t\tsummarizeBy: sum
\t\tsourceColumn: [Value3]

\t\tannotation SummarizationSetBy = Automatic

\tpartition 'Dashboard Metric Selector' = calculated
\t\tmode: import
\t\tsource =
\t\t\t\t{{
{rows}
\t\t\t\t}}
"""
    write_text(MODEL_TABLES / "Dashboard Metric Selector.tmdl", content)
    model = read_text(MODEL_FILE)
    ref = "ref table 'Dashboard Metric Selector'"
    if ref not in model:
        model = model.rstrip() + "\n" + ref + "\n"
        write_text(MODEL_FILE, model)


def add_person_search_label() -> None:
    text = read_text(DIM_PERSON)
    if re.search(r"(?m)^\tcolumn person_search_label\b", text):
        return
    marker = "\n\tpartition dim_person = m"
    if marker not in text:
        raise RuntimeError("dim_person partition marker not found")
    column = f"""

\tcolumn person_search_label =
\t\t\tVAR person_initials = COALESCE ( 'dim_person'[initials], "Unknown initials" )
\t\t\tRETURN person_initials & " | " & 'dim_person'[person_id]
\t\tdataType: string
\t\tlineageTag: {stable_guid('dim-person-search-label')}
\t\tsummarizeBy: none

\t\tannotation SummarizationSetBy = Automatic
"""
    write_text(DIM_PERSON, text.replace(marker, column + marker, 1))


def add_local_report_binding() -> None:
    client_binding = json.loads(read_text(CLIENT_REPORT / "definition.pbir"))
    local_binding = {
        "$schema": client_binding["$schema"],
        "version": client_binding["version"],
        "datasetReference": {
            "byPath": {"path": "../../SM WMPP v16 updated/SM_WMPP_v16.SemanticModel"}
        },
    }
    write_json(CLIENT_REPORT / "definition-local.pbir", local_binding)


def deterministic_hex(label: str) -> str:
    return hashlib.sha1(f"wmpp-v16:{label}".encode("utf-8")).hexdigest()[:20]


def get_source_entity(field: dict[str, Any]) -> str | None:
    return field.get("Expression", {}).get("SourceRef", {}).get("Entity")


def replace_field(
    value: Any,
    old_entity: str,
    old_property: str,
    new_entity: str,
    new_property: str,
    *,
    new_kind: str | None = None,
    parent_key: str = "",
) -> Any:
    if isinstance(value, list):
        return [
            replace_field(item, old_entity, old_property, new_entity, new_property, new_kind=new_kind, parent_key=parent_key)
            for item in value
        ]
    if isinstance(value, dict):
        for kind in ("Column", "Measure"):
            field = value.get(kind)
            if isinstance(field, dict) and get_source_entity(field) == old_entity and field.get("Property") == old_property:
                field["Expression"]["SourceRef"]["Entity"] = new_entity
                field["Property"] = new_property
                if new_kind and new_kind != kind:
                    del value[kind]
                    value[new_kind] = field
                break
        for key, item in list(value.items()):
            value[key] = replace_field(
                item,
                old_entity,
                old_property,
                new_entity,
                new_property,
                new_kind=new_kind,
                parent_key=key,
            )
        return value
    if isinstance(value, str):
        old_ref = f"{old_entity}.{old_property}"
        if value == old_ref or value.startswith(old_ref + "."):
            return f"{new_entity}.{new_property}" + value[len(old_ref) :]
        if parent_key == "nativeQueryRef" and value == old_property:
            return new_property
    return value


def clone_visual(
    source: Path,
    destination_page: Path,
    role: str,
    position: tuple[float, float, float, float],
    transform: Any | None = None,
) -> str:
    value = json.loads(read_text(source / "visual.json"))
    visual_id = deterministic_hex(role)
    value["name"] = visual_id
    x, y, width, height = position
    value["position"] = {
        "x": x,
        "y": y,
        "z": 1000 + len(list((destination_page / "visuals").glob("*/visual.json"))) * 1000,
        "height": height,
        "width": width,
        "tabOrder": 1000 + len(list((destination_page / "visuals").glob("*/visual.json"))) * 1000,
    }
    value.pop("parentGroupName", None)
    if transform:
        value = transform(value)
    write_json(destination_page / "visuals" / visual_id / "visual.json", value)
    return visual_id


def column_field(entity: str, prop: str) -> dict[str, Any]:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Entity": entity}},
            "Property": prop,
        }
    }


def projection(entity: str, prop: str) -> dict[str, Any]:
    return {
        "field": column_field(entity, prop),
        "queryRef": f"{entity}.{prop}",
        "nativeQueryRef": prop,
    }


def write_visual(page: Path, role: str, value: dict[str, Any]) -> str:
    visual_id = deterministic_hex(role)
    value["name"] = visual_id
    write_json(page / "visuals" / visual_id / "visual.json", value)
    return visual_id


def visual_position(page: Path, x: float, y: float, width: float, height: float) -> dict[str, float]:
    sequence = len(list((page / "visuals").glob("*/visual.json")))
    return {
        "x": x,
        "y": y,
        "z": 1000 + sequence * 1000,
        "height": height,
        "width": width,
        "tabOrder": 1000 + sequence * 1000,
    }


def add_title(page: Path, role: str, title: str, position: tuple[float, float, float, float]) -> str:
    x, y, width, height = position
    value = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": "placeholder",
        "position": visual_position(page, x, y, width, height),
        "visual": {
            "visualType": "textbox",
            "objects": {
                "general": [
                    {
                        "properties": {
                            "paragraphs": [
                                {
                                    "textRuns": [
                                        {
                                            "value": title,
                                            "textStyle": {
                                                "fontWeight": "bold",
                                                "fontFamily": "Segoe UI Semibold",
                                                "fontSize": "30pt",
                                                "color": "#2B2427",
                                            },
                                        }
                                    ]
                                }
                            ]
                        }
                    }
                ]
            },
            "drillFilterOtherVisuals": True,
        },
    }
    return write_visual(page, role, value)


def add_slicer(
    page: Path,
    role: str,
    entity: str,
    prop: str,
    position: tuple[float, float, float, float],
) -> str:
    x, y, width, height = position
    value = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": "placeholder",
        "position": visual_position(page, x, y, width, height),
        "visual": {
            "visualType": "slicer",
            "query": {"queryState": {"Values": {"projections": [projection(entity, prop)]}}},
            "drillFilterOtherVisuals": True,
        },
    }
    return write_visual(page, role, value)


def add_table(
    page: Path,
    role: str,
    fields: tuple[tuple[str, str], ...],
    position: tuple[float, float, float, float],
) -> str:
    x, y, width, height = position
    value = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": "placeholder",
        "position": visual_position(page, x, y, width, height),
        "visual": {
            "visualType": "tableEx",
            "query": {
                "queryState": {
                    "Values": {
                        "projections": [projection(entity, prop) for entity, prop in fields]
                    }
                }
            },
            "drillFilterOtherVisuals": True,
        },
    }
    return write_visual(page, role, value)


def title_transform(title: str):
    def transform(value: dict[str, Any]) -> dict[str, Any]:
        text_runs = value["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"]
        text_runs[0]["value"] = title
        return value

    return transform


def compose_transforms(*transforms):
    def transform(value: dict[str, Any]) -> dict[str, Any]:
        for item in transforms:
            value = item(value)
        return value

    return transform


def field_transform(old_entity: str, old_property: str, new_entity: str, new_property: str, new_kind: str | None = None):
    def transform(value: dict[str, Any]) -> dict[str, Any]:
        return replace_field(
            value,
            old_entity,
            old_property,
            new_entity,
            new_property,
            new_kind=new_kind,
        )

    return transform


def make_page(page_id: str, display_name: str, *, drillthrough: bool) -> Path:
    page = CLIENT_PAGES / page_id
    if page.exists():
        shutil.rmtree(page)
    (page / "visuals").mkdir(parents=True)
    value: dict[str, Any] = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": page_id,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": 1500,
        "width": 1500,
        "annotations": [
            {"name": "wmppPurpose", "value": "Referral journey, offers, provider responses and IPA detail"}
        ],
    }
    if drillthrough:
        filter_id = "Filter" + deterministic_hex("referral-drillthrough-filter") + "aa55"
        field = {
            "Column": {
                "Expression": {"SourceRef": {"Entity": "fact_referral"}},
                "Property": "referral_id",
            }
        }
        value["filterConfig"] = {
            "filters": [
                {
                    "name": filter_id,
                    "field": field,
                    "type": "Categorical",
                    "howCreated": "Drillthrough",
                    "isLockedInViewMode": True,
                }
            ]
        }
        value["pageBinding"] = {
            "name": "PodReferralDetail",
            "type": "Drillthrough",
            "parameters": [
                {
                    "name": "Param_" + filter_id,
                    "boundFilter": filter_id,
                    "qnaSingleSelectRequired": True,
                    "fieldExpr": field,
                }
            ],
        }
        value["visibility"] = "HiddenInViewMode"
    write_json(page / "page.json", value)
    return page


def add_referral_pages() -> None:
    provider_page = CLIENT_PAGES / "08ef33dc6a87d1b14392" / "visuals"
    local_detail = LOCAL_REPORT / "definition" / "pages" / "08ef33dc6a87d1b14392" / "visuals"
    ipa_page = CLIENT_PAGES / "58d36c775c032a42e01b" / "visuals"
    referral_page = CLIENT_PAGES / "f028a4be56d03e8404d7" / "visuals"

    original_search = provider_page / "810da240382d7a408e53"
    generated_search = provider_page / deterministic_hex("provider-single-search")
    sources = {
        "search": original_search if (original_search / "visual.json").exists() else generated_search,
        "journey": local_detail / "3d0f43d6a03170416ad7",
        "offer": ipa_page / "5df5024e8ac262339a06",
        "ipa": ipa_page / "33bbc8c0008d696692c0",
        "chart": referral_page / "817356520703d95da2d8",
    }
    for name, path in sources.items():
        if not (path / "visual.json").exists():
            raise FileNotFoundError(f"Missing {name} visual template: {path}")

    single_id = deterministic_hex("referral-single-view-page")
    drill_id = deterministic_hex("referral-drillthrough-page")
    single = make_page(single_id, "REFERRAL SINGLE VIEW", drillthrough=False)
    drill = make_page(drill_id, "REFERRAL DETAIL (DRILLTHROUGH)", drillthrough=True)

    def populate(page: Path, title: str, include_metric_switch: bool) -> None:
        add_title(page, f"{page.name}-title", title, (35, 20, 900, 80))
        clone_visual(
            sources["search"],
            page,
            f"{page.name}-referral-search",
            (35, 115, 690, 110),
            field_transform("dim_provider", "provider_name", "fact_referral", "referral_id"),
        )
        clone_visual(
            sources["search"],
            page,
            f"{page.name}-person-search",
            (760, 115, 690, 110),
            field_transform("dim_provider", "provider_name", "dim_person", "person_search_label"),
        )
        top_y = 370 if include_metric_switch else 245
        if include_metric_switch:
            add_slicer(
                page,
                f"{page.name}-metric-selector",
                "Dashboard Metric Selector",
                "Dashboard Metric Selector",
                (35, 245, 390, 110),
            )
            clone_visual(
                sources["chart"],
                page,
                f"{page.name}-metric-chart",
                (455, 245, 995, 350),
                compose_transforms(
                    field_transform(
                        "dim_referral",
                        "placement_type",
                        "dim_placement_type",
                        "placement_type",
                    ),
                    field_transform(
                        "_Measures",
                        "Referrals Currently Active",
                        "Dashboard Metric Selector",
                        "Dashboard Metric Selector",
                        new_kind="Column",
                    ),
                ),
            )
            top_y = 615
        clone_visual(sources["journey"], page, f"{page.name}-journey", (35, top_y, 1415, 300))
        clone_visual(sources["offer"], page, f"{page.name}-offers", (35, top_y + 330, 690, 430))
        clone_visual(sources["ipa"], page, f"{page.name}-ipa", (760, top_y + 330, 690, 430))

    populate(single, "Referral single view", include_metric_switch=True)
    populate(drill, "Referral detail", include_metric_switch=False)

    pages_file = CLIENT_PAGES / "pages.json"
    pages = json.loads(read_text(pages_file))
    order = [page for page in pages.get("pageOrder", []) if page not in (single_id, drill_id)]
    # Visible single-view page sits beside the provider page. The hidden drillthrough
    # page is retained in the order so Desktop preserves it during round trips.
    provider_id = "08ef33dc6a87d1b14392"
    insert_at = order.index(provider_id) + 1 if provider_id in order else len(order)
    order[insert_at:insert_at] = [single_id, drill_id]
    pages["pageOrder"] = order
    write_json(pages_file, pages)


def rebuild_provider_page() -> None:
    path = CLIENT_PAGES / "08ef33dc6a87d1b14392" / "page.json"
    page = json.loads(read_text(path))
    page_dir = path.parent
    original_search = page_dir / "visuals" / "810da240382d7a408e53" / "visual.json"
    generated_search = page_dir / "visuals" / deterministic_hex("provider-single-search") / "visual.json"
    search_template = load_path = original_search if original_search.exists() else generated_search
    if not load_path.exists():
        raise FileNotFoundError("Provider text-search visual template is missing")
    search_value = json.loads(read_text(search_template))
    shutil.rmtree(page_dir / "visuals")
    (page_dir / "visuals").mkdir()
    page["displayName"] = "PROVIDER SINGLE VIEW"
    page["height"] = 1500
    page["width"] = 1500
    annotations = [item for item in page.get("annotations", []) if item.get("name") != "wmppPurpose"]
    annotations.append(
        {
            "name": "wmppPurpose",
            "value": "Provider search, provider/home register, offers, placement supply and chart/list bookmark views",
        }
    )
    page["annotations"] = annotations
    write_json(path, page)
    add_title(page_dir, "provider-single-title", "Provider single view", (35, 20, 900, 80))
    search_value["name"] = deterministic_hex("provider-single-search")
    search_value["position"] = visual_position(page_dir, 35, 115, 690, 110)
    search_value = replace_field(search_value, "dim_provider", "provider_name", "dim_provider", "provider_name")
    write_json(generated_search, search_value)
    add_slicer(page_dir, "provider-service-slicer", "dim_provider_home", "service_type", (760, 115, 330, 110))
    add_slicer(
        page_dir,
        "provider-metric-slicer",
        "Dashboard Metric Selector",
        "Dashboard Metric Selector",
        (1120, 115, 330, 110),
    )

    chart_source = CLIENT_PAGES / "f028a4be56d03e8404d7" / "visuals" / "817356520703d95da2d8"
    clone_visual(
        chart_source,
        page_dir,
        "provider-metric-chart",
        (35, 250, 1415, 350),
        compose_transforms(
            field_transform(
                "dim_referral", "placement_type", "dim_provider_home", "service_type"
            ),
            field_transform(
                "_Measures",
                "Referrals Currently Active",
                "Dashboard Metric Selector",
                "Dashboard Metric Selector",
                new_kind="Column",
            ),
        ),
    )
    add_table(
        page_dir,
        "provider-home-detail",
        (
            ("dim_provider", "provider_name"),
            ("dim_provider", "provider_status"),
            ("dim_provider", "town_city"),
            ("dim_provider", "postcode"),
            ("dim_provider", "qa_flag"),
            ("dim_provider_home", "home_name"),
            ("dim_provider_home", "service_type"),
            ("dim_provider_home", "town_city"),
            ("dim_provider_home", "postcode"),
            ("dim_provider_home", "registered_beds"),
            ("dim_provider_home", "qa_flag"),
        ),
        (35, 630, 1415, 260),
    )
    add_table(
        page_dir,
        "provider-referral-assignments",
        (
            ("dim_provider", "provider_name"),
            ("fact_referral_provider", "referral_id"),
            ("fact_referral_provider", "provider_response_status"),
            ("fact_referral_provider", "assigned_at"),
            ("fact_referral_provider", "first_qualifying_response_at"),
            ("fact_referral_provider", "response_elapsed_minutes"),
            ("fact_referral_provider", "is_engaged"),
        ),
        (35, 920, 690, 480),
    )
    add_table(
        page_dir,
        "provider-offers",
        (
            ("dim_provider", "provider_name"),
            ("fact_offer", "referral_id"),
            ("fact_offer", "offer_id"),
            ("fact_offer", "offer_status"),
            ("fact_offer", "offer_submitted_date"),
            ("fact_offer", "offer_decision_date"),
            ("fact_offer", "estimated_weekly_cost"),
        ),
        (760, 920, 690, 480),
    )


def remove_stale_provider_bookmarks() -> None:
    bookmarks = CLIENT_DEFINITION / "bookmarks"
    metadata_path = bookmarks / "bookmarks.json"
    if not metadata_path.exists():
        return
    stale = {"6ea266472800b205d205", "8222659d22a927bd30a5"}
    metadata = json.loads(read_text(metadata_path))
    metadata["items"] = [item for item in metadata.get("items", []) if item.get("name") not in stale]
    write_json(metadata_path, metadata)
    for bookmark_id in stale:
        path = bookmarks / f"{bookmark_id}.bookmark.json"
        if path.exists():
            path.unlink()


def main() -> None:
    for path in (MODEL_MEASURES, CANONICAL_MEASURES, KPI_SELECTOR, DIM_PERSON, MODEL_FILE):
        if not path.exists():
            raise FileNotFoundError(path)

    if SOURCE_BUNDLE.exists():
        with zipfile.ZipFile(SOURCE_BUNDLE) as bundle:
            alias_source_text = bundle.read(SOURCE_MEASURE_ENTRY).decode("utf-8-sig")
    else:
        alias_source = BASELINE_MEASURES if BASELINE_MEASURES.exists() else MODEL_MEASURES
        alias_source_text = read_text(alias_source)
    aliases = build_alias_map(alias_source_text)
    if not aliases:
        raise RuntimeError("No legacy aliases were detected")

    removed_model = clean_measure_file(MODEL_MEASURES, aliases)
    removed_canonical = clean_measure_file(CANONICAL_MEASURES, aliases)
    remaining = set(measure_blocks(read_text(MODEL_MEASURES)))
    selector_count = reconcile_kpi_selector(aliases, remaining)
    add_metric_selector(remaining)
    add_person_search_label()
    add_local_report_binding()
    add_referral_pages()
    rebuild_provider_page()
    remove_stale_provider_bookmarks()

    clean_report_field_refs(LOCAL_REPORT)
    clean_report_field_refs(CLIENT_REPORT)

    report_aliases = {**aliases, **REPORT_BINDING_FIXES}
    changed_reports = {
        str(LOCAL_REPORT.relative_to(PROJECT_ROOT)): clean_report_measure_refs(LOCAL_REPORT, report_aliases),
        str(CLIENT_REPORT.relative_to(PROJECT_ROOT)): clean_report_measure_refs(CLIENT_REPORT, report_aliases),
    }
    result = {
        "legacyMeasuresRemoved": len(aliases),
        "deployedMeasureBlocksRemoved": removed_model,
        "canonicalMeasureBlocksRemoved": removed_canonical,
        "remainingMeasures": len(remaining),
        "kpiSelectorEntries": selector_count,
        "reportJsonFilesUpdated": changed_reports,
        "localReportBinding": str((CLIENT_REPORT / "definition-local.pbir").relative_to(PROJECT_ROOT)),
        "referralSingleViewPage": deterministic_hex("referral-single-view-page"),
        "referralDrillthroughPage": deterministic_hex("referral-drillthrough-page"),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
