"""Static acceptance checks for the WMPP v16 report/model enhancements."""

from __future__ import annotations

import json
import re
import hashlib
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURRENT = PROJECT_ROOT / "reports" / "current"
MODEL = CURRENT / "SM WMPP v16 updated" / "SM_WMPP_v16.SemanticModel" / "definition"
TABLES = MODEL / "tables"
REPORT = CURRENT / "RPT WMPP v16" / "WMPP_DASHBOARD_v16.Report"
PAGES = REPORT / "definition" / "pages"
LOCAL_REPORT = CURRENT / "SM WMPP v16 updated" / "SM_WMPP_v16.Report"
MISSION_ROOT = CURRENT / "SM WMPP Mission Control v16"


LEGACY_NAMES = {
    "Open Referral",
    "Referrals This Month",
    "Referrals This FY",
    "Referrals With Offers",
    "Referrals With One or More Offers",
    "Active Referrals Awaiting Offers",
    "Active Referrals Under Offer",
    "Referrals Cancelled/Closed",
    "Offer Count",
    "Total Offers Made Historically",
    "(NEW)Total Offers Made",
    "Latest Offer Status Count",
    "Dashboard Last Refreshed:",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load(path: Path):
    return json.loads(read(path))


def measure_names(text: str) -> set[str]:
    pattern = re.compile(r"(?m)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*=")
    return {
        (match.group(1) if match.group(1) is not None else match.group(2)).strip().replace("''", "'")
        for match in pattern.finditer(text)
    }


def semantic_fields(tables_dir: Path) -> dict[str, set[str]]:
    fields: dict[str, set[str]] = {}
    table_pattern = re.compile(r"(?m)^table\s+(?:'((?:''|[^'])+)'|([^\r\n]+))$")
    column_pattern = re.compile(r"(?m)^\tcolumn\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))(?:\s*=|\s*$)")
    measure_pattern = re.compile(r"(?m)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*=")
    for path in tables_dir.glob("*.tmdl"):
        text = read(path)
        table_match = table_pattern.search(text)
        assert table_match, f"No table declaration in {path}"
        table = (table_match.group(1) or table_match.group(2)).strip().replace("''", "'")
        names: set[str] = set()
        for pattern in (column_pattern, measure_pattern):
            for match in pattern.finditer(text):
                names.add((match.group(1) or match.group(2)).strip().replace("''", "'"))
        fields[table] = names
    return fields


def field_pairs(value) -> set[tuple[str, str]]:
    pairs: set[tuple[str, str]] = set()
    if isinstance(value, list):
        for item in value:
            pairs.update(field_pairs(item))
    elif isinstance(value, dict):
        for kind in ("Column", "Measure"):
            field = value.get(kind)
            if isinstance(field, dict):
                entity = field.get("Expression", {}).get("SourceRef", {}).get("Entity")
                prop = field.get("Property")
                if entity and prop:
                    pairs.add((entity, prop))
        for item in value.values():
            pairs.update(field_pairs(item))
    return pairs


def deterministic_hex(label: str) -> str:
    return hashlib.sha1(f"wmpp-v16:{label}".encode("utf-8")).hexdigest()[:20]


def assert_page_fields(page_id: str, required: set[tuple[str, str]]) -> None:
    found: set[tuple[str, str]] = set()
    for visual in (PAGES / page_id / "visuals").glob("*/visual.json"):
        found.update(field_pairs(load(visual)))
    missing = required - found
    assert not missing, f"Page {page_id} is missing fields: {sorted(missing)}"


def main() -> None:
    # Every JSON document in the enhanced report must parse.
    for path in (REPORT / "definition").rglob("*.json"):
        load(path)

    model_fields = semantic_fields(TABLES)
    measures = measure_names(read(TABLES / "_Measures.tmdl"))
    stale = LEGACY_NAMES & measures
    assert not stale, f"Legacy duplicate measures still present: {sorted(stale)}"

    for report_root in (REPORT, LOCAL_REPORT):
        report_measure_refs: set[str] = set()
        report_column_refs: set[tuple[str, str]] = set()
        for path in (report_root / "definition").rglob("*.json"):
            for entity, prop in field_pairs(load(path)):
                if entity == "_Measures":
                    report_measure_refs.add(prop)
                else:
                    report_column_refs.add((entity, prop))
        missing_report_measures = report_measure_refs - measures
        assert not missing_report_measures, (
            f"{report_root.name} references removed or missing measures: "
            f"{sorted(missing_report_measures)}"
        )
        missing_report_columns = {
            (entity, prop)
            for entity, prop in report_column_refs
            if entity not in model_fields or prop not in model_fields[entity]
        }
        assert not missing_report_columns, (
            f"{report_root.name} references removed or missing columns: "
            f"{sorted(missing_report_columns)}"
        )

    selector = read(TABLES / "KPI Selector.tmdl")
    selector_refs = set(re.findall(r"NAMEOF\('_Measures'\[([^\]]+)\]\)", selector))
    assert selector_refs <= measures, f"KPI Selector has missing measures: {sorted(selector_refs - measures)}"

    metric_selector = read(TABLES / "Dashboard Metric Selector.tmdl")
    metric_refs = set(re.findall(r"NAMEOF\('_Measures'\[([^\]]+)\]\)", metric_selector))
    assert metric_refs and metric_refs <= measures
    assert "ref table 'Dashboard Metric Selector'" in read(MODEL / "model.tmdl")
    assert "column person_search_label" in read(TABLES / "dim_person.tmdl")

    client_binding = load(REPORT / "definition.pbir")
    assert "byConnection" in client_binding["datasetReference"], "Client binding must be preserved"
    local_binding = load(REPORT / "definition-local.pbir")
    local_path = local_binding["datasetReference"]["byPath"]["path"]
    assert local_path.endswith("SM_WMPP_v16.SemanticModel")
    assert (REPORT / local_path).resolve() == MODEL.parent.resolve()

    pages = load(PAGES / "pages.json")["pageOrder"]
    single = deterministic_hex("referral-single-view-page")
    drill = deterministic_hex("referral-drillthrough-page")
    assert single in pages and drill in pages
    assert load(PAGES / "08ef33dc6a87d1b14392" / "page.json")["displayName"] == "PROVIDER SINGLE VIEW"

    drill_page = load(PAGES / drill / "page.json")
    assert drill_page["pageBinding"]["type"] == "Drillthrough"
    assert drill_page["visibility"] == "HiddenInViewMode"
    assert drill_page["filterConfig"]["filters"][0]["howCreated"] == "Drillthrough"

    required_common = {
        ("fact_referral", "referral_id"),
        ("dim_person", "person_search_label"),
        ("fact_offer", "offer_id"),
        ("fact_ipa", "accepted_offer_id"),
        ("fact_referral_provider", "is_closed"),
    }
    assert_page_fields(single, required_common | {("Dashboard Metric Selector", "Dashboard Metric Selector")})
    assert_page_fields(drill, required_common)

    # Removed measure names must not remain as semantic references in report JSON.
    all_report_text = "\n".join(read(path) for path in (REPORT / "definition").rglob("*.json"))
    stale_refs = [name for name in LEGACY_NAMES if f'"_Measures.{name}"' in all_report_text]
    assert not stale_refs, f"Report still references removed measures: {stale_refs}"

    mission_model = MISSION_ROOT / "SM WMPP Mission Control.SemanticModel" / "definition"
    mission_report = MISSION_ROOT / "SM WMPP Mission Control.Report"
    mission_tables = semantic_fields(mission_model / "tables")
    mission_measures = measure_names(
        read(mission_model / "tables" / "_MissionControl_Measures.tmdl")
    )
    assert len(mission_measures) == 87
    for path in (mission_model / "tables").glob("*.tmdl"):
        assert re.search(r"(?m)^\tpartition\s+", read(path)), f"Table has no partition: {path.name}"
    for path in (mission_report / "definition").rglob("*.json"):
        load(path)
    mission_binding = load(mission_report / "definition.pbir")
    mission_path = mission_binding["datasetReference"]["byPath"]["path"]
    assert (mission_report / mission_path).resolve() == mission_model.parent.resolve()
    mission_refs: set[str] = set()
    for path in (mission_report / "definition").rglob("*.json"):
        mission_refs.update(
            prop
            for entity, prop in field_pairs(load(path))
            if entity == "_MissionControl_Measures"
        )
    assert mission_refs <= mission_measures
    model_refs = set(re.findall(r"(?m)^ref table (?:'((?:''|[^'])+)'|([^\r\n]+))$", read(mission_model / "model.tmdl")))
    flattened_refs = {(quoted or bare).replace("''", "'") for quoted, bare in model_refs}
    assert flattened_refs <= mission_tables.keys()

    print(
        json.dumps(
            {
                "status": "PASS",
                "measureCount": len(measures),
                "kpiSelectorCount": len(selector_refs),
                "metricSelectorCount": len(metric_refs),
                "pageCount": len(pages),
                "referralSingleView": single,
                "referralDrillthrough": drill,
                "providerSingleView": "08ef33dc6a87d1b14392",
                "missionControlMeasures": len(mission_measures),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
