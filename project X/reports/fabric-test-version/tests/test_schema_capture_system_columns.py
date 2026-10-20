"""Exercise catalog capture and real drift SQL without a Fabric session."""

import ast
from datetime import datetime, timezone
from pathlib import Path
import sqlite3
from types import SimpleNamespace

from notebook_loader import load_notebook
import pytest


PROJECT = Path(__file__).resolve().parents[1]
LIVE = "01a_cfg_schema_capture_live.py"
ARCHIVE = "01a_cfg_schema_capture_archive.py"
CONTRACT = [
    ("provider", "provider_id", "bigint", None, None),
    ("provider", "business_removed", "string", None, None),
    ("provider", "business_type", "bigint", None, None),
    ("provider", "customer_name", "string", None, None),
    ("provider", "_ingestion_id", "string", None, None),
    ("provider", "_contract_metadata", "string", None, None),
]
CURRENT = [
    ("provider", "provider_id", "bigint"),
    ("provider", "business_added", "string"),
    ("provider", "business_type", "string"),
    ("provider", "customer_name", "string"),
    ("provider", "_ingestion_id", "bigint"),
    ("provider", "_source_file", "string"),
    ("provider", "__future_metadata", "string"),
]


def code_cells(name):
    return ["".join(cell["source"]) for cell in load_notebook(PROJECT / name)["cells"]
            if cell["cell_type"] == "code"]


def python_tree(name):
    return ast.parse("\n".join(code for code in code_cells(name)
                               if not code.lstrip().startswith("%")))


@pytest.mark.parametrize("name", [LIVE, ARCHIVE])
def test_capture_skips_only_columns_with_a_leading_underscore(name):
    columns = [SimpleNamespace(name=column, dataType="string", nullable=True)
               for column in ("_ingestion_id", "provider_id", "_source_file",
                              "customer_name", "__future_metadata", "_FutureMetadata")]
    table = SimpleNamespace(name="provider", isTemporary=False)
    catalog = SimpleNamespace(listTables=lambda _: [table], listColumns=lambda _: columns)
    scope = {
        "spark": SimpleNamespace(catalog=catalog), "BRONZE_SCHEMA": "bronze",
        "COMPARED_SCHEMA": "archived", "tables": [table], "records": [],
        "schema_records": [], "excluded_live_tables": [],
        "is_etl_excluded_table": lambda _: False,
        "etl_logical_table_name": lambda name: name,
        "captured_at": datetime.now(timezone.utc), "RUN_ID": "run", "JOB_RUN_ID": "job",
    }
    loop = next(node for node in python_tree(name).body if isinstance(node, ast.For))
    exec(compile(ast.Module([loop], type_ignores=[]), name, "exec"), scope)
    rows = scope["records"] if name == LIVE else scope["schema_records"]
    assert [row[2] for row in rows] == ["provider_id", "customer_name"]


def live_drift_sql():
    assignment = next(node for node in python_tree(LIVE).body
                      if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == "current_drifts"
                              for target in node.targets))
    sql = eval(compile(ast.Expression(assignment.value.args[0]), LIVE, "eval"), {
        "RUN_ID": "run", "JOB_RUN_ID": "job", "SOURCE_KIND": "LIVE",
        "BRONZE_SCHEMA": "bronze",
    })
    # Translate Spark anti joins to equivalent SQLite NOT EXISTS predicates.
    sql = " ".join(sql.split())
    for left, right, condition in (
        ("live_tables l", "definition_tables d", "l.table_name=d.table_name"),
        ("definition_tables d", "live_tables l", "d.table_name=l.table_name"),
        ("live l", "definition d", "l.table_name=d.table_name AND l.column_name=d.column_name"),
        ("definition d", "live l", "l.table_name=d.table_name AND l.column_name=d.column_name"),
    ):
        original = f"FROM {left} LEFT ANTI JOIN {right} ON {condition}"
        assert original in sql
        sql = sql.replace(original, f"FROM {left} WHERE NOT EXISTS "
                          f"(SELECT 1 FROM {right} WHERE {condition})")
    return sql.replace("current_timestamp()", "CURRENT_TIMESTAMP")


def test_live_drift_ignores_generated_columns_in_contract_current_and_previous():
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        connection.create_function("concat", -1, lambda *items: "".join(map(str, items)))
        connection.create_function("concat_ws", -1, lambda sep, *items: sep.join(
            str(item) for item in items if item is not None))
        connection.create_function("sha2", 2, lambda text, _: text)
        connection.execute("CREATE TABLE _schema_definition "
                           "(table_name, column_name, data_type, referenced_table, referenced_column)")
        for table in ("_schema_live_current", "_schema_live_previous"):
            connection.execute(f"CREATE TABLE {table} (table_name, column_name, live_data_type)")
        connection.executemany("INSERT INTO _schema_definition VALUES (?,?,?,?,?)", CONTRACT)
        connection.executemany("INSERT INTO _schema_live_current VALUES (?,?,?)", CURRENT)
        connection.executemany("INSERT INTO _schema_live_previous VALUES (?,?,?)", [
            ("provider", "business_type", "bigint"),
            ("provider", "_ingestion_id", "string"),
            ("provider", "_source_file", "bigint"),
        ])
        rows = connection.execute(live_drift_sql()).fetchall()
    assert {(row["column_name"], row["drift_type"]) for row in rows} == {
        ("business_added", "COLUMN_ADDED"),
        ("business_removed", "COLUMN_REMOVED"),
        ("business_type", "LIVE_TYPE_CHANGED"),
    }


def test_archive_comparison_ignores_generated_columns_in_contract_and_stored_history():
    sql = next(code for code in code_cells(ARCHIVE) if code.lstrip().startswith("%%sql"))
    sql = sql.split("\n", 1)[1]
    with sqlite3.connect(":memory:") as connection:
        connection.row_factory = sqlite3.Row
        connection.execute("ATTACH DATABASE ':memory:' AS monitoring")
        connection.execute("CREATE TABLE monitoring.cfg_schema_contract_column "
                           "(table_name, column_name, data_type)")
        connection.execute("CREATE TABLE monitoring.cfg_archived_schema_live "
                           "(table_name, column_name, data_type)")
        connection.executemany("INSERT INTO monitoring.cfg_schema_contract_column VALUES (?,?,?)",
                               [row[:3] for row in CONTRACT])
        connection.executemany("INSERT INTO monitoring.cfg_archived_schema_live VALUES (?,?,?)",
                               CURRENT)
        rows = connection.execute(sql).fetchall()
    assert {row["column_name"] for row in rows} == {
        "business_added", "business_removed", "business_type",
    }
