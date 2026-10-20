"""Regression checks for LIVE-ETL-002 (schema guard) and LIVE-ETL-003 (logging/performance)."""

import ast
from notebook_loader import load_notebook as read_notebook
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures = []


def check(condition, message):
    if not condition:
        failures.append(message)


def notebook_source(name):
    notebook = read_notebook(ROOT / name)
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell.get("source", []))
        if cell.get("cell_type") == "code" and not source.lstrip().startswith("%"):
            try:
                ast.parse(source, filename=f"{name}:cell-{index}")
            except SyntaxError as exc:
                failures.append(f"{name}:cell-{index} syntax error: {exc}")
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


common = notebook_source("99_common_library.py")
check("def log_step(" in common, "99_common_library is missing the log_step timing helper")
check("_LOG_STEP_STATE" in common, "99_common_library log_step has no shared timing state")

rules = notebook_source("03_silver_business_rules.py")

# LIVE-ETL-002: fail-fast schema guard instead of slow resolver fallback.
check("SHOW SCHEMAS" in rules, "03 is missing the schema visibility probe")
check("CREATE SCHEMA IF NOT EXISTS" in rules, "03 is missing CREATE SCHEMA IF NOT EXISTS guard")
check("LIVE-ETL-002" in rules, "03 guard does not reference LIVE-ETL-002")

# LIVE-ETL-003: per-cell and per-rule observability.
check(rules.count("log_step(") >= 6, "03 has too few log_step calls between cells")
check("def log_rule(" in rules, "03 DQ loop is missing per-rule timing logs")

# LIVE-ETL-003: one scan per Silver table per run.
check("checked_counts" in rules, "03 DQ loop does not reuse per-table row counts")
check("cached_frames" in rules, "03 DQ loop does not cache multi-rule tables")
check("unpersist" in rules, "03 DQ loop does not unpersist cached tables")

issue_log = (ROOT / "change tracking" / "ETL_ISSUE_LOG.md").read_text(
    encoding="utf-8", errors="replace"
)
check("LIVE-ETL-002" in issue_log, "issue log does not record LIVE-ETL-002")
check("LIVE-ETL-003" in issue_log, "issue log does not record LIVE-ETL-003")

if failures:
    print("VALIDATION FAILED")
    for failure in failures:
        print(f"- {failure}")
    raise SystemExit(1)

print("PASS LIVE-ETL-002 schema guard is in place")
print("PASS LIVE-ETL-003 logging and single-scan DQ loop are in place")
print("VALIDATION PASSED")
