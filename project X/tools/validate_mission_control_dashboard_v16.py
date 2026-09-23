"""Static acceptance checks for the rebuilt Mission Control v16 dashboard."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "reports" / "current" / "SM WMPP Mission Control v16"
REPORT = ROOT / "SM WMPP Mission Control.Report" / "definition"
PAGES = REPORT / "pages"
MODEL = ROOT / "SM WMPP Mission Control.SemanticModel" / "definition"
TABLES = MODEL / "tables"

TIMELINE_PAGE = "ed27e90d06816c7c1eee"


def stable_id(label: str) -> str:
    return hashlib.sha1(f"mission-control-v16:{label}".encode("utf-8")).hexdigest()[:20]


ARCHIVE_PAGE = stable_id("archive-and-replay-page")
DETAIL_PAGE = stable_id("job-step-detail-page")
JOB_GANTT = stable_id("timeline:job-gantt")
STEP_GANTT = stable_id("timeline:step-gantt")
STEP_TABLE = stable_id("timeline:step-table")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def load(path: Path) -> Any:
    return json.loads(read(path))


def semantic_fields() -> tuple[dict[str, set[str]], set[str]]:
    fields: dict[str, set[str]] = {}
    measures: set[str] = set()
    table_pattern = re.compile(r"(?m)^table\s+(?:'((?:''|[^'])+)'|([^\r\n]+))$")
    column_pattern = re.compile(r"(?m)^\tcolumn\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))(?:\s*=|\s*$)")
    measure_pattern = re.compile(r"(?m)^\tmeasure\s+(?:'((?:''|[^'])+)'|([^=\r\n]+?))\s*=")
    for path in TABLES.glob("*.tmdl"):
        text = read(path)
        match = table_pattern.search(text)
        assert match, f"No table declaration: {path.name}"
        table = (match.group(1) or match.group(2)).strip().replace("''", "'")
        names: set[str] = set()
        for pattern in (column_pattern, measure_pattern):
            for item in pattern.finditer(text):
                name = (item.group(1) or item.group(2)).strip().replace("''", "'")
                names.add(name)
                if table == "_MissionControl_Measures" and pattern is measure_pattern:
                    measures.add(name)
        fields[table] = names
    return fields, measures


def field_pairs(value: Any) -> set[tuple[str, str]]:
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


def all_visuals(page_id: str) -> dict[str, Any]:
    return {
        path.parent.name: load(path)
        for path in (PAGES / page_id / "visuals").glob("*/visual.json")
    }


def main() -> None:
    json_paths = list(REPORT.rglob("*.json"))
    for path in json_paths:
        load(path)

    fields, measures = semantic_fields()
    assert len(measures) == 87, f"Expected 87 Mission Control measures, found {len(measures)}"

    referenced_measures: set[str] = set()
    unresolved: set[tuple[str, str]] = set()
    for path in json_paths:
        for entity, prop in field_pairs(load(path)):
            if entity == "_MissionControl_Measures":
                referenced_measures.add(prop)
            if entity not in fields or prop not in fields[entity]:
                unresolved.add((entity, prop))
    assert not unresolved, f"Unresolved report fields: {sorted(unresolved)}"
    assert referenced_measures == measures, (
        f"Every measure must be exposed; missing={sorted(measures - referenced_measures)}, "
        f"unknown={sorted(referenced_measures - measures)}"
    )

    metadata = load(PAGES / "pages.json")
    assert metadata["activePageName"] == TIMELINE_PAGE
    assert ARCHIVE_PAGE in metadata["pageOrder"]
    assert DETAIL_PAGE in metadata["pageOrder"]
    for page_id in metadata["pageOrder"]:
        assert (PAGES / page_id / "page.json").is_file()

    timeline = load(PAGES / TIMELINE_PAGE / "page.json")
    last_14 = timeline["filterConfig"]["filters"][0]
    assert last_14["field"]["Column"]["Property"] == "job_run_window"
    assert last_14["isLockedInViewMode"] is True
    filter_text = json.dumps(last_14)
    assert "Last 14 days" in filter_text

    timeline_visuals = all_visuals(TIMELINE_PAGE)
    assert timeline_visuals[JOB_GANTT]["visual"]["visualType"] == "Gantt1448688115699"
    assert timeline_visuals[STEP_GANTT]["visual"]["visualType"] == "Gantt1448688115699"
    interactions = {
        (item["source"], item["target"], item["type"])
        for item in timeline["visualInteractions"]
    }
    assert (JOB_GANTT, STEP_GANTT, "DataFilter") in interactions
    assert (JOB_GANTT, STEP_TABLE, "DataFilter") in interactions

    job_gantt_text = json.dumps(timeline_visuals[JOB_GANTT])
    step_gantt_text = json.dumps(timeline_visuals[STEP_GANTT])
    assert "rpt_job_run_summary.started_at" in job_gantt_text
    assert "rpt_job_run_summary.ended_at" in job_gantt_text
    assert "rpt_job_run_summary.job_run_id" in job_gantt_text
    assert "rpt_job_step_timing.steps_duration_days" in step_gantt_text
    assert "rpt_job_step_timing.notebook_name" in step_gantt_text

    step_model = read(TABLES / "rpt_job_step_timing.tmdl")
    assert "DIVIDE ( rpt_job_step_timing[step_duration_seconds], 86400.0 )" in step_model
    assert "*0.00" not in step_model.replace(" ", "")
    job_model = read(TABLES / "rpt_job_run_summary.tmdl")
    assert "column job_run_window" in job_model
    assert '"Last 14 days"' in job_model

    detail = load(PAGES / DETAIL_PAGE / "page.json")
    assert detail["visibility"] == "HiddenInViewMode"
    assert detail["pageBinding"]["type"] == "Drillthrough"
    assert detail["filterConfig"]["filters"][0]["howCreated"] == "Drillthrough"

    report_binding = load(ROOT / "SM WMPP Mission Control.Report" / "definition.pbir")
    model_path = report_binding["datasetReference"]["byPath"]["path"]
    assert (ROOT / "SM WMPP Mission Control.Report" / model_path).resolve() == (
        ROOT / "SM WMPP Mission Control.SemanticModel"
    ).resolve()

    print(
        json.dumps(
            {
                "status": "PASS",
                "pages": len(metadata["pageOrder"]),
                "visuals": sum(len(all_visuals(page)) for page in metadata["pageOrder"]),
                "measuresExposed": len(referenced_measures),
                "unresolvedFields": len(unresolved),
                "jobGantt": JOB_GANTT,
                "stepGantt": STEP_GANTT,
                "drillthroughPage": DETAIL_PAGE,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
