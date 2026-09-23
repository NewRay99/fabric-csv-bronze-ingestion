"""Rebuild the Mission Control v16 PBIR dashboard around monitoring use cases.

The supplied report mixed monitoring fields with bindings copied from the WMPP
business report.  This deterministic rebuild keeps the local semantic-model
binding, exposes every Mission Control measure, and creates a focused 14-day
job/step timeline with explicit cross-filter interactions.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parents[1]
ROOT = PROJECT_ROOT / "reports" / "current" / "SM WMPP Mission Control v16"
REPORT = ROOT / "SM WMPP Mission Control.Report"
PAGES = REPORT / "definition" / "pages"
TABLES = ROOT / "SM WMPP Mission Control.SemanticModel" / "definition" / "tables"

EXECUTIVE_PAGE = "803165f7d2f5aaccd8ac"
TIMELINE_PAGE = "ed27e90d06816c7c1eee"
QUALITY_PAGE = "d807778066085fbd96dc"
TOOLTIP_PAGE = "2af45662f5a13e0c063b"


MEASURE_GROUPS: dict[str, list[str]] = {
    "Control health": [
        "Reload Requests",
        "Control Failures",
        "Operational Exception Count",
        "Dashboard Last Refreshed",
    ],
    "Job runs": [
        "Job Runs",
        "Successful Job Runs",
        "Failed Job Runs",
        "Job Success Rate",
    ],
    "Pipeline execution": [
        "Pipeline Runs",
        "Successful Pipeline Runs",
        "Failed Pipeline Runs",
        "Running Pipeline Runs",
        "Completed Pipeline Runs",
        "Pipeline Success Rate",
        "Live Pipeline Runs",
        "Archive Pipeline Runs",
        "Live Pipeline Failures",
        "Archive Pipeline Failures",
        "Pipeline Tables Succeeded",
        "Pipeline Tables Failed",
        "Pipeline Rows Read",
        "Pipeline Rows Written",
        "Pipeline Runs With Error",
        "Average Pipeline Duration (min)",
        "P95 Pipeline Duration (min)",
        "Total Pipeline Duration (min)",
        "Pipeline Rows per Minute",
        "Latest Pipeline End",
        "Latest Pipeline Status",
    ],
    "Job selection": [
        "Latest Job Run Started",
        "Latest Job Run ID",
        "Selected or Latest Job Run ID",
        "Selected or Latest Job Status",
        "Selected or Latest Job Error",
        "Selected or Latest Job Duration (min)",
        "Selected or Latest Job Steps",
        "Selected or Latest Failed Steps",
        "Show Step for Selected or Latest Job Run",
        "Selected Step Error Detail",
    ],
    "Job steps": [
        "Job Steps",
        "Successful Job Steps",
        "Failed Job Steps",
        "Job Steps With Error",
        "Total Job Step Duration (min)",
        "Longest Job Step Duration (min)",
    ],
    "Data quality": [
        "DQ Checks",
        "DQ Evaluated Checks",
        "DQ Failed Checks",
        "DQ Failure Rate",
        "DQ Checked Rows",
        "DQ Failed Rows",
        "Weighted DQ Failure Percentage",
        "Critical Rules Failing",
        "High or Critical Rules Failing",
        "DQ Failures With Sample Keys",
        "Active DQ Rules",
        "Critical Active DQ Rules",
        "RI Rules Failing",
        "RI Checked Rows",
        "RI Failed Rows",
        "RI Failure Rate",
    ],
    "Schema inventory": [
        "Archived Schema Columns",
        "Archived Schema Tables",
        "Latest Archived Schema Capture",
        "Archived Nullable Columns",
        "Archived Schema Data Types",
    ],
    "Archive control": [
        "Archive ZIP Batches",
        "Successful Archive ZIP Batches",
        "Failed Archive ZIP Batches",
        "Archive ZIP Batches Awaiting Reload",
        "Archive ZIP Files Declared",
        "Average Archive ZIP Duration (min)",
        "Archive Files Processed",
        "Successful Archive Files",
        "Archive File Failures",
        "Archive Files Awaiting Reload",
        "Archive File Rows Read",
        "Archive File Rows Written",
        "Archive Table Exports",
        "Failed Archive Table Exports",
        "Archive Table Exports Awaiting Reload",
        "Archive Export Rows",
        "Gold Snapshot Runs",
        "Successful Gold Snapshots",
        "Failed Gold Snapshots",
        "Gold Snapshots Awaiting Replay",
        "Gold Snapshot DQ Failures",
    ],
}


def stable_id(label: str) -> str:
    return hashlib.sha1(f"mission-control-v16:{label}".encode("utf-8")).hexdigest()[:20]


ARCHIVE_PAGE = stable_id("archive-and-replay-page")
DETAIL_PAGE = stable_id("job-step-detail-page")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def literal(value: str) -> dict[str, Any]:
    return {"expr": {"Literal": {"Value": value}}}


def column_field(table: str, column: str) -> dict[str, Any]:
    return {
        "Column": {
            "Expression": {"SourceRef": {"Entity": table}},
            "Property": column,
        }
    }


def measure_field(measure: str) -> dict[str, Any]:
    return {
        "Measure": {
            "Expression": {"SourceRef": {"Entity": "_MissionControl_Measures"}},
            "Property": measure,
        }
    }


def aggregation_field(table: str, column: str, function: int) -> dict[str, Any]:
    return {
        "Aggregation": {
            "Expression": column_field(table, column),
            "Function": function,
        }
    }


def projection(field: dict[str, Any], query_ref: str, native_ref: str) -> dict[str, Any]:
    return {"field": field, "queryRef": query_ref, "nativeQueryRef": native_ref}


def position(x: float, y: float, width: float, height: float, z: int) -> dict[str, Any]:
    return {
        "x": x,
        "y": y,
        "z": z,
        "height": height,
        "width": width,
        "tabOrder": z,
    }


def container_objects(title: str | None = None, tooltip: bool = False) -> dict[str, Any]:
    objects: dict[str, Any] = {
        "background": [
            {
                "properties": {
                    "show": literal("true"),
                    "color": {"solid": {"color": literal("'#FFFFFF'")}},
                    "transparency": literal("0D"),
                }
            }
        ],
        "border": [
            {
                "properties": {
                    "show": literal("true"),
                    "color": {"solid": {"color": literal("'#E8DCE1'")}},
                    "radius": literal("12D"),
                    "width": literal("1D"),
                }
            }
        ],
        "dropShadow": [
            {
                "properties": {
                    "show": literal("true"),
                    "preset": literal("'BottomRight'"),
                    "transparency": literal("90D"),
                    "shadowBlur": literal("8D"),
                    "shadowDistance": literal("2D"),
                }
            }
        ],
        "visualHeader": [
            {
                "properties": {
                    "show": literal("true"),
                    "showFilterRestatementButton": literal("true"),
                    "showFocusModeButton": literal("true"),
                    "showOptionsMenu": literal("true"),
                }
            }
        ],
        "padding": [
            {
                "properties": {
                    "top": literal("8D"),
                    "bottom": literal("8D"),
                    "left": literal("8D"),
                    "right": literal("8D"),
                }
            }
        ],
    }
    if title is not None:
        objects["title"] = [
            {
                "properties": {
                    "show": literal("true"),
                    "text": literal(repr(title)),
                    "titleWrap": literal("true"),
                    "fontColor": {"solid": {"color": literal("'#2B2427'")}},
                    "fontSize": literal("13D"),
                    "bold": literal("true"),
                    "fontFamily": literal("'Segoe UI Semibold'"),
                }
            }
        ]
    if tooltip:
        objects["visualTooltip"] = [
            {
                "properties": {
                    "show": literal("true"),
                    "section": literal(repr(TOOLTIP_PAGE)),
                    "type": literal("'ReportPage'"),
                }
            }
        ]
    return objects


def visual_shell(name: str, kind: str, pos: dict[str, Any]) -> dict[str, Any]:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json",
        "name": name,
        "position": pos,
        "visual": {"visualType": kind, "drillFilterOtherVisuals": True},
    }


def textbox(name: str, text: str, pos: dict[str, Any], size: int = 18, bold: bool = True) -> dict[str, Any]:
    value = visual_shell(name, "textbox", pos)
    value["visual"]["objects"] = {
        "general": [
            {
                "properties": {
                    "paragraphs": [
                        {
                            "textRuns": [
                                {
                                    "value": text,
                                    "textStyle": {
                                        "fontWeight": "bold" if bold else "normal",
                                        "fontFamily": "Segoe UI",
                                        "fontSize": f"{size}px",
                                        "color": "#2B2427",
                                    },
                                }
                            ]
                        }
                    ]
                }
            }
        ]
    }
    value["visual"]["visualContainerObjects"] = {
        "visualHeader": [{"properties": {"show": literal("false")}}],
        "background": [{"properties": {"show": literal("false")}}],
    }
    return value


def card(name: str, measure: str, pos: dict[str, Any]) -> dict[str, Any]:
    field = measure_field(measure)
    value = visual_shell(name, "cardVisual", pos)
    value["visual"]["query"] = {
        "queryState": {
            "Data": {
                "projections": [
                    projection(field, f"_MissionControl_Measures.{measure}", measure)
                ]
            }
        }
    }
    value["visual"]["objects"] = {
        "value": [
            {
                "properties": {
                    "fontSize": literal("24D"),
                    "bold": literal("true"),
                    "fontColor": {"solid": {"color": literal("'#C5526B'")}},
                    "horizontalAlignment": literal("'left'"),
                    "textWrap": literal("true"),
                },
                "selector": {"id": "default"},
            }
        ],
        "label": [
            {
                "properties": {
                    "show": literal("true"),
                    "fontSize": literal("10D"),
                    "bold": literal("true"),
                    "textWrap": literal("true"),
                    "position": literal("'aboveValue'"),
                },
                "selector": {"id": "default"},
            }
        ],
        "layout": [
            {
                "properties": {
                    "alignment": literal("'top'"),
                    "autoGrid": literal("true"),
                    "orientation": literal("2D"),
                    "rowCount": literal("1L"),
                }
            }
        ],
    }
    value["visual"]["visualContainerObjects"] = container_objects()
    value["filterConfig"] = {
        "filters": [
            {
                "name": stable_id(f"filter:measure:{measure}"),
                "field": field,
                "type": "Advanced",
            }
        ]
    }
    return value


def table_visual(
    name: str,
    fields: Iterable[tuple[str, str]],
    title: str,
    pos: dict[str, Any],
    sort: tuple[str, str, str] | None = None,
) -> dict[str, Any]:
    projections: list[dict[str, Any]] = []
    filters: list[dict[str, Any]] = []
    for table, column in fields:
        field = column_field(table, column)
        projections.append(projection(field, f"{table}.{column}", column))
        filters.append(
            {
                "name": stable_id(f"filter:{name}:{table}:{column}"),
                "field": field,
                "type": "Categorical",
            }
        )
    query: dict[str, Any] = {
        "queryState": {"Values": {"projections": projections}},
        "sortDefinition": {"isDefaultSort": True},
    }
    if sort:
        table, column, direction = sort
        query["sortDefinition"]["sort"] = [
            {"field": column_field(table, column), "direction": direction}
        ]
    value = visual_shell(name, "tableEx", pos)
    value["visual"]["query"] = query
    value["visual"]["visualContainerObjects"] = container_objects(title, tooltip=True)
    value["filterConfig"] = {"filters": filters, "filterSortOrder": "Custom"}
    return value


def slicer(name: str, table: str, column: str, title: str, pos: dict[str, Any]) -> dict[str, Any]:
    field = column_field(table, column)
    value = visual_shell(name, "slicer", pos)
    value["visual"]["query"] = {
        "queryState": {
            "Values": {
                "projections": [
                    {
                        **projection(field, f"{table}.{column}", column),
                        "active": True,
                    }
                ]
            }
        },
        "sortDefinition": {
            "sort": [{"field": field, "direction": "Ascending"}],
            "isDefaultSort": True,
        },
    }
    value["visual"]["objects"] = {
        "selection": [
            {
                "properties": {
                    "singleSelect": literal("false"),
                    "selectAllCheckboxEnabled": literal("true"),
                }
            }
        ]
    }
    value["visual"]["visualContainerObjects"] = container_objects(title)
    value["filterConfig"] = {
        "filters": [
            {
                "name": stable_id(f"filter:{name}"),
                "field": field,
                "type": "Categorical",
            }
        ]
    }
    return value


def donut(name: str, table: str, category: str, count_column: str, title: str, pos: dict[str, Any]) -> dict[str, Any]:
    category_field = column_field(table, category)
    count_field = aggregation_field(table, count_column, 5)
    value = visual_shell(name, "donutChart", pos)
    value["visual"]["query"] = {
        "queryState": {
            "Category": {
                "projections": [
                    {**projection(category_field, f"{table}.{category}", category), "active": True}
                ]
            },
            "Y": {
                "projections": [
                    projection(
                        count_field,
                        f"CountNonNull({table}.{count_column})",
                        f"Count of {count_column}",
                    )
                ]
            },
        }
    }
    value["visual"]["objects"] = {
        "labels": [{"properties": {"show": literal("true"), "bold": literal("true")}}],
        "legend": [{"properties": {"position": literal("'Bottom'"), "bold": literal("true")}}],
    }
    value["visual"]["visualContainerObjects"] = container_objects(title)
    value["filterConfig"] = {
        "filters": [
            {
                "name": stable_id(f"filter:{name}:category"),
                "field": category_field,
                "type": "Categorical",
            },
            {
                "name": stable_id(f"filter:{name}:count"),
                "field": count_field,
                "type": "Advanced",
            },
        ]
    }
    return value


def gantt_filter(name: str, fields: Iterable[dict[str, Any]]) -> dict[str, Any]:
    return {
        "filters": [
            {
                "name": stable_id(f"filter:{name}:{index}"),
                "field": field,
                "type": "Categorical" if "Column" in field else "Advanced",
            }
            for index, field in enumerate(fields)
        ],
        "filterSortOrder": "Custom",
    }


def set_title(value: dict[str, Any], title: str) -> None:
    value["visual"]["visualContainerObjects"] = container_objects(title, tooltip=True)


def job_gantt(template: dict[str, Any], name: str, pos: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(template)
    value["name"] = name
    value["position"] = pos
    state = value["visual"]["query"]["queryState"]
    start = column_field("rpt_job_run_summary", "started_at")
    end = aggregation_field("rpt_job_run_summary", "ended_at", 3)
    status = column_field("rpt_job_run_summary", "status")
    job = column_field("rpt_job_run_summary", "job_run_id")
    pipeline = column_field("rpt_job_run_summary", "pipeline_name")
    state.clear()
    state.update(
        {
            "StartDate": {"projections": [projection(start, "rpt_job_run_summary.started_at", "started_at")]},
            "EndDate": {"projections": [projection(end, "Min(rpt_job_run_summary.ended_at)", "ended_at")]},
            "Parent": {"projections": [projection(pipeline, "rpt_job_run_summary.pipeline_name", "pipeline_name")]},
            "Legend": {"projections": [projection(status, "rpt_job_run_summary.status", "status")]},
            "Task": {"projections": [projection(job, "rpt_job_run_summary.job_run_id", "job_run_id")]},
            "ExtraInformation": {
                "projections": [
                    projection(pipeline, "rpt_job_run_summary.pipeline_name", "pipeline_name"),
                    projection(status, "rpt_job_run_summary.status", "status"),
                ]
            },
            "Completion": {"projections": []},
        }
    )
    value["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": start, "direction": "Descending"}],
        "isDefaultSort": True,
    }
    value["visual"]["objects"] = {
        "legend": [{"properties": {"position": literal("'Bottom'"), "bold": literal("true")}}],
        "dateType": [{"properties": {"type": literal("'Hour'")}}],
        "daysOff": [{"properties": {"show": literal("false")}}],
    }
    set_title(value, "Job runs — last 14 days (select a bar to filter job steps)")
    value["visual"]["drillFilterOtherVisuals"] = True
    value["filterConfig"] = gantt_filter(name, [start, end, pipeline, status, job])
    return value


def step_gantt(template: dict[str, Any], name: str, pos: dict[str, Any]) -> dict[str, Any]:
    value = deepcopy(template)
    value["name"] = name
    value["position"] = pos
    state = value["visual"]["query"]["queryState"]
    start = column_field("rpt_job_step_timing", "started_at")
    duration = aggregation_field("rpt_job_step_timing", "steps_duration_days", 3)
    status = column_field("rpt_job_step_timing", "status")
    job = column_field("rpt_job_step_timing", "job_run_id")
    notebook = column_field("rpt_job_step_timing", "notebook_name")
    state.clear()
    state.update(
        {
            "StartDate": {"projections": [projection(start, "rpt_job_step_timing.started_at", "started_at")]},
            "Duration": {"projections": [projection(duration, "Min(rpt_job_step_timing.steps_duration_days)", "step duration (days)")]},
            "Parent": {"projections": [projection(job, "rpt_job_step_timing.job_run_id", "job_run_id")]},
            "Legend": {"projections": [projection(status, "rpt_job_step_timing.status", "status")]},
            "Task": {"projections": [projection(notebook, "rpt_job_step_timing.notebook_name", "notebook_name")]},
            "ExtraInformation": {
                "projections": [
                    projection(job, "rpt_job_step_timing.job_run_id", "job_run_id"),
                    projection(status, "rpt_job_step_timing.status", "status"),
                ]
            },
        }
    )
    value["visual"]["query"]["sortDefinition"] = {
        "sort": [{"field": start, "direction": "Ascending"}],
        "isDefaultSort": True,
    }
    value["visual"]["objects"] = {
        "legend": [{"properties": {"position": literal("'Bottom'"), "bold": literal("true")}}],
        "dateType": [{"properties": {"type": literal("'Hour'")}}],
        "daysOff": [{"properties": {"show": literal("false")}}],
    }
    set_title(value, "Steps for selected job run")
    value["visual"]["drillFilterOtherVisuals"] = True
    value["filterConfig"] = gantt_filter(name, [start, duration, status, job, notebook])
    return value


def page_filter_last_14_days() -> dict[str, Any]:
    field = column_field("rpt_job_run_summary", "job_run_window")
    return {
        "name": stable_id("filter:last-14-days"),
        "field": field,
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": "j", "Entity": "rpt_job_run_summary", "Type": 0}],
            "Where": [
                {
                    "Condition": {
                        "In": {
                            "Expressions": [
                                {
                                    "Column": {
                                        "Expression": {"SourceRef": {"Source": "j"}},
                                        "Property": "job_run_window",
                                    }
                                }
                            ],
                            "Values": [[{"Literal": {"Value": "'Last 14 days'"}}]],
                        }
                    }
                }
            ],
        },
        "howCreated": "User",
        "isLockedInViewMode": True,
    }


def page_json(name: str, display_name: str, height: int, width: int = 1500) -> dict[str, Any]:
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": name,
        "displayName": display_name,
        "displayOption": "FitToPage",
        "height": height,
        "width": width,
        "objects": {
            "background": [
                {
                    "properties": {
                        "color": {"solid": {"color": literal("'#FAF7F8'")}},
                        "transparency": literal("0D"),
                    }
                }
            ]
        },
    }


def write_visual(page_id: str, value: dict[str, Any]) -> None:
    write_json(PAGES / page_id / "visuals" / value["name"] / "visual.json", value)


def reset_page(page_id: str) -> None:
    visual_dir = PAGES / page_id / "visuals"
    if visual_dir.exists():
        shutil.rmtree(visual_dir)
    visual_dir.mkdir(parents=True, exist_ok=True)


def add_heading(page_id: str, label: str, text: str, y: int, z: int) -> None:
    write_visual(
        page_id,
        textbox(stable_id(f"{page_id}:{label}"), text, position(30, y, 1440, 46, z), 18, True),
    )


def add_cards(
    page_id: str,
    label: str,
    measures: list[str],
    start_y: int,
    z_start: int,
    columns: int = 5,
) -> int:
    gap = 12
    card_width = (1440 - gap * (columns - 1)) / columns
    card_height = 112
    for index, measure in enumerate(measures):
        row, column = divmod(index, columns)
        x = 30 + column * (card_width + gap)
        y = start_y + row * (card_height + gap)
        name = stable_id(f"{page_id}:{label}:{measure}")
        write_visual(page_id, card(name, measure, position(x, y, card_width, card_height, z_start + index)))
    rows = (len(measures) + columns - 1) // columns
    return start_y + rows * (card_height + gap)


def build_executive_page() -> None:
    reset_page(EXECUTIVE_PAGE)
    page = page_json(EXECUTIVE_PAGE, "Mission Control Overview", 2100)
    write_json(PAGES / EXECUTIVE_PAGE / "page.json", page)
    write_visual(
        EXECUTIVE_PAGE,
        textbox(
            stable_id("executive:title"),
            "MISSION CONTROL | Operational overview",
            position(30, 20, 1440, 55, 1),
            26,
        ),
    )
    write_visual(
        EXECUTIVE_PAGE,
        textbox(
            stable_id("executive:subtitle"),
            "Health, job and pipeline measures. Use the Job Runs & Steps page for the linked 14-day Gantt view.",
            position(30, 72, 1440, 36, 2),
            12,
            False,
        ),
    )
    add_heading(EXECUTIVE_PAGE, "health-heading", "Control health", 120, 3)
    y = add_cards(EXECUTIVE_PAGE, "Control health", MEASURE_GROUPS["Control health"], 170, 10)
    add_heading(EXECUTIVE_PAGE, "job-heading", "Job run health", y + 4, 30)
    y = add_cards(EXECUTIVE_PAGE, "Job runs", MEASURE_GROUPS["Job runs"], y + 54, 40)
    write_visual(
        EXECUTIVE_PAGE,
        donut(
            stable_id("executive:job-status"),
            "rpt_job_run_summary",
            "status",
            "job_run_id",
            "Job runs by status",
            position(30, y + 18, 430, 330, 60),
        ),
    )
    write_visual(
        EXECUTIVE_PAGE,
        table_visual(
            stable_id("executive:recent-jobs"),
            [
                ("rpt_job_run_summary", "job_run_id"),
                ("rpt_job_run_summary", "pipeline_name"),
                ("rpt_job_run_summary", "status"),
                ("rpt_job_run_summary", "started_at"),
                ("rpt_job_run_summary", "ended_at"),
                ("rpt_job_run_summary", "job_duration_seconds"),
                ("rpt_job_run_summary", "steps_failed"),
                ("rpt_job_run_summary", "dq_failures"),
                ("rpt_job_run_summary", "active_drift_events"),
                ("rpt_job_run_summary", "error_message"),
            ],
            "Recent job runs and exceptions",
            position(480, y + 18, 990, 330, 61),
            ("rpt_job_run_summary", "started_at", "Descending"),
        ),
    )
    pipeline_y = y + 372
    add_heading(EXECUTIVE_PAGE, "pipeline-heading", "Pipeline execution measures", pipeline_y, 70)
    add_cards(
        EXECUTIVE_PAGE,
        "Pipeline execution",
        MEASURE_GROUPS["Pipeline execution"],
        pipeline_y + 50,
        80,
    )


def build_timeline_page(job_template: dict[str, Any], step_template: dict[str, Any]) -> None:
    reset_page(TIMELINE_PAGE)
    page = page_json(TIMELINE_PAGE, "Job Runs & Steps | Last 14 Days", 2350)
    page["filterConfig"] = {"filters": [page_filter_last_14_days()]}
    job_gantt_id = stable_id("timeline:job-gantt")
    step_gantt_id = stable_id("timeline:step-gantt")
    job_table_id = stable_id("timeline:job-table")
    step_table_id = stable_id("timeline:step-table")
    page["visualInteractions"] = [
        {"source": job_gantt_id, "target": step_gantt_id, "type": "DataFilter"},
        {"source": job_gantt_id, "target": step_table_id, "type": "DataFilter"},
        {"source": job_table_id, "target": step_gantt_id, "type": "DataFilter"},
        {"source": job_table_id, "target": step_table_id, "type": "DataFilter"},
    ]
    write_json(PAGES / TIMELINE_PAGE / "page.json", page)
    write_visual(
        TIMELINE_PAGE,
        textbox(
            stable_id("timeline:title"),
            "JOB RUNS & STEPS | Last 14 days",
            position(30, 20, 1440, 55, 1),
            26,
        ),
    )
    write_visual(
        TIMELINE_PAGE,
        textbox(
            stable_id("timeline:instructions"),
            "Select a job bar or a job-table row to cross-filter its notebook steps. Right-click a job to drill through to the full step detail page.",
            position(30, 72, 1440, 36, 2),
            12,
            False,
        ),
    )
    write_visual(
        TIMELINE_PAGE,
        slicer(stable_id("timeline:pipeline-slicer"), "rpt_job_run_summary", "pipeline_name", "Pipeline", position(30, 120, 300, 120, 3)),
    )
    write_visual(
        TIMELINE_PAGE,
        slicer(stable_id("timeline:status-slicer"), "rpt_job_run_summary", "status", "Job status", position(345, 120, 250, 120, 4)),
    )
    write_visual(
        TIMELINE_PAGE,
        slicer(stable_id("timeline:job-slicer"), "rpt_job_run_summary", "job_run_id", "Job run ID (search)", position(610, 120, 500, 120, 5)),
    )
    for index, measure in enumerate(
        [
            "Selected or Latest Job Status",
            "Selected or Latest Job Duration (min)",
            "Selected or Latest Job Steps",
            "Selected or Latest Failed Steps",
        ]
    ):
        write_visual(
            TIMELINE_PAGE,
            card(
                stable_id(f"timeline:selected:{measure}"),
                measure,
                position(1125, 120 + index * 118, 345, 106, 10 + index),
            ),
        )
    write_visual(TIMELINE_PAGE, job_gantt(job_template, job_gantt_id, position(30, 260, 1065, 420, 20)))
    write_visual(TIMELINE_PAGE, step_gantt(step_template, step_gantt_id, position(30, 700, 1440, 430, 21)))
    write_visual(
        TIMELINE_PAGE,
        table_visual(
            job_table_id,
            [
                ("rpt_job_run_summary", "job_run_id"),
                ("rpt_job_run_summary", "pipeline_name"),
                ("rpt_job_run_summary", "status"),
                ("rpt_job_run_summary", "started_at"),
                ("rpt_job_run_summary", "ended_at"),
                ("rpt_job_run_summary", "job_duration_seconds"),
                ("rpt_job_run_summary", "rows_read"),
                ("rpt_job_run_summary", "rows_written"),
                ("rpt_job_run_summary", "dq_failures"),
                ("rpt_job_run_summary", "error_message"),
            ],
            "Job runs (selection source)",
            position(30, 1150, 710, 390, 30),
            ("rpt_job_run_summary", "started_at", "Descending"),
        ),
    )
    write_visual(
        TIMELINE_PAGE,
        table_visual(
            step_table_id,
            [
                ("rpt_job_step_timing", "job_run_id"),
                ("rpt_job_step_timing", "step_sequence"),
                ("rpt_job_step_timing", "notebook_name"),
                ("rpt_job_step_timing", "status"),
                ("rpt_job_step_timing", "started_at"),
                ("rpt_job_step_timing", "ended_at"),
                ("rpt_job_step_timing", "step_duration_seconds"),
                ("rpt_job_step_timing", "gap_from_previous_step_seconds"),
                ("rpt_job_step_timing", "error_message"),
            ],
            "Job step detail (cross-filter target)",
            position(760, 1150, 710, 390, 31),
            ("rpt_job_step_timing", "step_sequence", "Ascending"),
        ),
    )
    add_heading(TIMELINE_PAGE, "selection-heading", "Job selection measures", 1570, 50)
    y = add_cards(TIMELINE_PAGE, "Job selection", MEASURE_GROUPS["Job selection"], 1620, 60)
    add_heading(TIMELINE_PAGE, "steps-heading", "Job step measures", y + 2, 80)
    add_cards(TIMELINE_PAGE, "Job steps", MEASURE_GROUPS["Job steps"], y + 52, 90)


def build_quality_page() -> None:
    reset_page(QUALITY_PAGE)
    page = page_json(QUALITY_PAGE, "Data Quality & Schema", 2050)
    write_json(PAGES / QUALITY_PAGE / "page.json", page)
    write_visual(
        QUALITY_PAGE,
        textbox(stable_id("quality:title"), "DATA QUALITY & SCHEMA", position(30, 20, 1440, 55, 1), 26),
    )
    write_visual(
        QUALITY_PAGE,
        slicer(stable_id("quality:severity"), "cfg_data_quality_result", "severity", "Severity", position(30, 90, 280, 120, 2)),
    )
    write_visual(
        QUALITY_PAGE,
        slicer(stable_id("quality:status"), "cfg_data_quality_result", "status", "Check status", position(325, 90, 280, 120, 3)),
    )
    write_visual(
        QUALITY_PAGE,
        slicer(stable_id("quality:rule-type"), "cfg_data_quality_result", "rule_type", "Rule type", position(620, 90, 320, 120, 4)),
    )
    write_visual(
        QUALITY_PAGE,
        donut(stable_id("quality:status-donut"), "cfg_data_quality_result", "status", "rule_id", "Quality checks by status", position(960, 90, 510, 300, 5)),
    )
    add_heading(QUALITY_PAGE, "dq-heading", "Data quality measures", 410, 10)
    y = add_cards(QUALITY_PAGE, "Data quality", MEASURE_GROUPS["Data quality"], 460, 20)
    write_visual(
        QUALITY_PAGE,
        table_visual(
            stable_id("quality:results"),
            [
                ("cfg_data_quality_result", "job_run_id"),
                ("cfg_data_quality_result", "rule_id"),
                ("cfg_data_quality_result", "severity"),
                ("cfg_data_quality_result", "rule_type"),
                ("cfg_data_quality_result", "source_table"),
                ("cfg_data_quality_result", "column_name"),
                ("cfg_data_quality_result", "status"),
                ("cfg_data_quality_result", "checked_row_count"),
                ("cfg_data_quality_result", "failed_row_count"),
                ("cfg_data_quality_result", "failure_percentage"),
                ("cfg_data_quality_result", "sample_key_json"),
                ("cfg_data_quality_result", "checked_at"),
                ("cfg_data_quality_result", "message"),
            ],
            "Data quality result detail",
            position(30, y + 15, 1440, 420, 60),
            ("cfg_data_quality_result", "checked_at", "Descending"),
        ),
    )
    schema_y = y + 465
    add_heading(QUALITY_PAGE, "schema-heading", "Archived schema inventory", schema_y, 70)
    schema_bottom = add_cards(QUALITY_PAGE, "Schema inventory", MEASURE_GROUPS["Schema inventory"], schema_y + 50, 80)
    write_visual(
        QUALITY_PAGE,
        table_visual(
            stable_id("quality:schema-table"),
            [
                ("cfg_archived_schema_live", "schema_name"),
                ("cfg_archived_schema_live", "table_name"),
                ("cfg_archived_schema_live", "ordinal_position"),
                ("cfg_archived_schema_live", "column_name"),
                ("cfg_archived_schema_live", "data_type"),
                ("cfg_archived_schema_live", "is_nullable"),
                ("cfg_archived_schema_live", "contract_loaded_at"),
            ],
            "Archived schema columns",
            position(30, schema_bottom + 15, 1440, 380, 100),
            ("cfg_archived_schema_live", "contract_loaded_at", "Descending"),
        ),
    )


def build_archive_page() -> None:
    reset_page(ARCHIVE_PAGE)
    page = page_json(ARCHIVE_PAGE, "Archive & Replay", 2200)
    write_json(PAGES / ARCHIVE_PAGE / "page.json", page)
    write_visual(
        ARCHIVE_PAGE,
        textbox(stable_id("archive:title"), "ARCHIVE & REPLAY CONTROL", position(30, 20, 1440, 55, 1), 26),
    )
    write_visual(
        ARCHIVE_PAGE,
        textbox(
            stable_id("archive:subtitle"),
            "Monitor reload queues, archive processing, table exports and month-end Gold snapshots.",
            position(30, 72, 1440, 36, 2),
            12,
            False,
        ),
    )
    add_heading(ARCHIVE_PAGE, "archive-heading", "Archive control measures", 115, 3)
    y = add_cards(ARCHIVE_PAGE, "Archive control", MEASURE_GROUPS["Archive control"], 165, 10)
    write_visual(
        ARCHIVE_PAGE,
        table_visual(
            stable_id("archive:zip-table"),
            [
                ("cfg_archive_zip_load", "zip_path"),
                ("cfg_archive_zip_load", "export_date"),
                ("cfg_archive_zip_load", "status"),
                ("cfg_archive_zip_load", "reload"),
                ("cfg_archive_zip_load", "attempt_count"),
                ("cfg_archive_zip_load", "file_count"),
                ("cfg_archive_zip_load", "started_at"),
                ("cfg_archive_zip_load", "ended_at"),
                ("cfg_archive_zip_load", "error_message"),
            ],
            "Archive ZIP batches",
            position(30, y + 15, 700, 380, 50),
            ("cfg_archive_zip_load", "started_at", "Descending"),
        ),
    )
    write_visual(
        ARCHIVE_PAGE,
        table_visual(
            stable_id("archive:file-table"),
            [
                ("cfg_archive_file_load", "filename"),
                ("cfg_archive_file_load", "source_zip"),
                ("cfg_archive_file_load", "target_object"),
                ("cfg_archive_file_load", "status"),
                ("cfg_archive_file_load", "reload"),
                ("cfg_archive_file_load", "rows_read"),
                ("cfg_archive_file_load", "rows_written"),
                ("cfg_archive_file_load", "started_at"),
                ("cfg_archive_file_load", "ended_at"),
                ("cfg_archive_file_load", "error_message"),
            ],
            "Archive file loads",
            position(750, y + 15, 720, 380, 51),
            ("cfg_archive_file_load", "started_at", "Descending"),
        ),
    )
    write_visual(
        ARCHIVE_PAGE,
        table_visual(
            stable_id("archive:gold-table"),
            [
                ("cfg_month_end_gold_run", "snapshot_date"),
                ("cfg_month_end_gold_run", "status"),
                ("cfg_month_end_gold_run", "reload"),
                ("cfg_month_end_gold_run", "attempt_count"),
                ("cfg_month_end_gold_run", "dq_result"),
                ("cfg_month_end_gold_run", "gold_result"),
                ("cfg_month_end_gold_run", "started_at"),
                ("cfg_month_end_gold_run", "ended_at"),
                ("cfg_month_end_gold_run", "error_message"),
            ],
            "Month-end Gold snapshot runs",
            position(30, y + 420, 1440, 390, 52),
            ("cfg_month_end_gold_run", "started_at", "Descending"),
        ),
    )


def build_detail_page() -> None:
    reset_page(DETAIL_PAGE)
    drill_filter = stable_id("detail:drill-filter")
    field = column_field("rpt_job_run_summary", "job_run_id")
    page = page_json(DETAIL_PAGE, "Job Step Detail (Drillthrough)", 1450)
    page["filterConfig"] = {
        "filters": [
            {
                "name": drill_filter,
                "field": field,
                "type": "Categorical",
                "howCreated": "Drillthrough",
                "isLockedInViewMode": True,
            }
        ]
    }
    page["pageBinding"] = {
        "name": "PodMissionControlJobDetail",
        "type": "Drillthrough",
        "parameters": [
            {
                "name": f"Param_{drill_filter}",
                "boundFilter": drill_filter,
                "qnaSingleSelectRequired": True,
                "fieldExpr": field,
            }
        ],
    }
    page["visibility"] = "HiddenInViewMode"
    write_json(PAGES / DETAIL_PAGE / "page.json", page)
    write_visual(
        DETAIL_PAGE,
        textbox(stable_id("detail:title"), "JOB RUN DETAIL", position(30, 20, 1440, 55, 1), 26),
    )
    selected = [
        "Selected or Latest Job Run ID",
        "Selected or Latest Job Status",
        "Selected or Latest Job Duration (min)",
        "Selected or Latest Job Steps",
        "Selected or Latest Failed Steps",
    ]
    for index, measure in enumerate(selected):
        write_visual(
            DETAIL_PAGE,
            card(
                stable_id(f"detail:{measure}"),
                measure,
                position(30 + index * 288, 90, 276, 120, 10 + index),
            ),
        )
    write_visual(
        DETAIL_PAGE,
        table_visual(
            stable_id("detail:job"),
            [
                ("rpt_job_run_summary", "job_run_id"),
                ("rpt_job_run_summary", "pipeline_name"),
                ("rpt_job_run_summary", "status"),
                ("rpt_job_run_summary", "started_at"),
                ("rpt_job_run_summary", "ended_at"),
                ("rpt_job_run_summary", "job_duration_seconds"),
                ("rpt_job_run_summary", "steps_succeeded"),
                ("rpt_job_run_summary", "steps_failed"),
                ("rpt_job_run_summary", "rows_read"),
                ("rpt_job_run_summary", "rows_written"),
                ("rpt_job_run_summary", "duplicate_rows"),
                ("rpt_job_run_summary", "dq_checks"),
                ("rpt_job_run_summary", "dq_failures"),
                ("rpt_job_run_summary", "drift_events"),
                ("rpt_job_run_summary", "active_drift_events"),
                ("rpt_job_run_summary", "error_message"),
            ],
            "Job summary",
            position(30, 235, 1440, 300, 20),
        ),
    )
    write_visual(
        DETAIL_PAGE,
        table_visual(
            stable_id("detail:steps"),
            [
                ("rpt_job_step_timing", "step_sequence"),
                ("rpt_job_step_timing", "notebook_name"),
                ("rpt_job_step_timing", "status"),
                ("rpt_job_step_timing", "started_at"),
                ("rpt_job_step_timing", "ended_at"),
                ("rpt_job_step_timing", "step_duration_seconds"),
                ("rpt_job_step_timing", "gap_from_previous_step_seconds"),
                ("rpt_job_step_timing", "child_result"),
                ("rpt_job_step_timing", "error_message"),
            ],
            "Notebook steps",
            position(30, 555, 1440, 430, 21),
            ("rpt_job_step_timing", "step_sequence", "Ascending"),
        ),
    )
    write_visual(
        DETAIL_PAGE,
        table_visual(
            stable_id("detail:pipeline"),
            [
                ("cfg_pipeline_run", "run_id"),
                ("cfg_pipeline_run", "pipeline_name"),
                ("cfg_pipeline_run", "layer"),
                ("cfg_pipeline_run", "source_kind"),
                ("cfg_pipeline_run", "started_at"),
                ("cfg_pipeline_run", "ended_at"),
                ("cfg_pipeline_run", "status"),
                ("cfg_pipeline_run", "tables_succeeded"),
                ("cfg_pipeline_run", "tables_failed"),
                ("cfg_pipeline_run", "rows_read"),
                ("cfg_pipeline_run", "rows_written"),
                ("cfg_pipeline_run", "error_message"),
            ],
            "Pipeline execution detail",
            position(30, 1005, 1440, 390, 22),
            ("cfg_pipeline_run", "started_at", "Descending"),
        ),
    )


def build_tooltip_page() -> None:
    reset_page(TOOLTIP_PAGE)
    page = page_json(TOOLTIP_PAGE, "Job Run Tooltip", 300, 650)
    page["visibility"] = "HiddenInViewMode"
    write_json(PAGES / TOOLTIP_PAGE / "page.json", page)
    for index, measure in enumerate(
        [
            "Selected or Latest Job Run ID",
            "Selected or Latest Job Status",
            "Selected or Latest Job Duration (min)",
            "Selected or Latest Failed Steps",
        ]
    ):
        row, column = divmod(index, 2)
        write_visual(
            TOOLTIP_PAGE,
            card(
                stable_id(f"tooltip:{measure}"),
                measure,
                position(15 + column * 315, 15 + row * 138, 300, 123, 1 + index),
            ),
        )


def update_model() -> None:
    step_path = TABLES / "rpt_job_step_timing.tmdl"
    step_text = step_path.read_text(encoding="utf-8-sig")
    step_text = re.sub(
        r"column steps_duration_days\s*=.*",
        "column steps_duration_days = DIVIDE ( rpt_job_step_timing[step_duration_seconds], 86400.0 )",
        step_text,
        count=1,
    )
    step_text = step_text.replace(
        "\t\tformatString: 0.000E+000\n\t\tlineageTag: 68fed6b5-53d2-4327-ade2-39ef16f4a6fd",
        "\t\tformatString: 0.000000\n\t\tlineageTag: 68fed6b5-53d2-4327-ade2-39ef16f4a6fd",
    )
    step_path.write_text(step_text, encoding="utf-8", newline="\n")

    job_path = TABLES / "rpt_job_run_summary.tmdl"
    job_text = job_path.read_text(encoding="utf-8-sig")
    if "\tcolumn job_run_window =" not in job_text:
        block = (
            "\n\tcolumn job_run_window = IF ( NOT ISBLANK ( rpt_job_run_summary[started_at] ) "
            "&& rpt_job_run_summary[started_at] >= TODAY () - 13 "
            "&& rpt_job_run_summary[started_at] < TODAY () + 1, \"Last 14 days\", \"Older\" )\n"
            "\t\tdataType: string\n"
            "\t\tlineageTag: 6749b413-3a79-4de2-87d5-4e30d31d40aa\n"
            "\t\tsummarizeBy: none\n\n"
            "\t\tannotation SummarizationSetBy = Automatic\n"
        )
        job_text = job_text.replace("\n\tpartition rpt_job_run_summary = m", block + "\n\tpartition rpt_job_run_summary = m")
        job_path.write_text(job_text, encoding="utf-8", newline="\n")


def load_gantt_template(preferred_id: str, entity: str) -> dict[str, Any]:
    """Load the supplied Gantt once, then the generated equivalent on reruns."""
    preferred = PAGES / TIMELINE_PAGE / "visuals" / preferred_id / "visual.json"
    if preferred.is_file():
        return read_json(preferred)
    for path in (PAGES / TIMELINE_PAGE / "visuals").glob("*/visual.json"):
        value = read_json(path)
        if value.get("visual", {}).get("visualType") != "Gantt1448688115699":
            continue
        if entity in json.dumps(value):
            return value
    raise FileNotFoundError(f"No Gantt template found for {entity}")


def main() -> None:
    job_template = load_gantt_template("83ec31be9e6708cc6e52", "rpt_job_run_summary")
    step_template = load_gantt_template("08efdb0d3bb8d6feaeda", "rpt_job_step_timing")
    update_model()
    build_executive_page()
    build_timeline_page(job_template, step_template)
    build_quality_page()
    build_archive_page()
    build_detail_page()
    build_tooltip_page()
    write_json(
        PAGES / "pages.json",
        {
            "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
            "pageOrder": [
                EXECUTIVE_PAGE,
                TIMELINE_PAGE,
                QUALITY_PAGE,
                ARCHIVE_PAGE,
                DETAIL_PAGE,
                TOOLTIP_PAGE,
            ],
            "activePageName": TIMELINE_PAGE,
        },
    )
    print(
        json.dumps(
            {
                "status": "rebuilt",
                "pages": 6,
                "archivePage": ARCHIVE_PAGE,
                "detailPage": DETAIL_PAGE,
                "measuresExposed": sum(len(values) for values in MEASURE_GROUPS.values()),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
