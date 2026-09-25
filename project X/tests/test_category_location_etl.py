"""ETL-only regressions: synthetic records, no client/report/model dependencies."""

import ast
import math
from pathlib import Path
import re
import sqlite3

import pytest

from notebook_loader import load_notebook


PROJECT = Path(__file__).resolve().parents[1]


def code(name):
    return "\n\n".join(
        "".join(cell["source"])
        for cell in load_notebook(PROJECT / f"{name}.py")["cells"]
        if cell["cell_type"] == "code"
        and not "".join(cell["source"]).lstrip().startswith("%")
    )


def function(name, notebook):
    tree = ast.parse(code(notebook))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name)
    scope = {}
    exec(compile(ast.Module(body=[node], type_ignores=[]), notebook, "exec"), scope)
    return scope[name]


@pytest.mark.parametrize("text,city,status,review", [
    (None, "Birmingham", "DEFAULT_MISSING", False),
    ("  ", "Birmingham", "DEFAULT_MISSING", False),
    ("BIRMINGHAM area preferred", "Birmingham", "CITY_MATCH", False),
    ("Bham", "Birmingham", "CITY_MATCH", False),
    ("Coventry", "Coventry", "CITY_MATCH", False),
    ("Outside Birmingham", "Birmingham", "DEFAULT_REVIEW_EXCLUSION", True),
    ("Not Birmingham", "Birmingham", "DEFAULT_REVIEW_EXCLUSION", True),
    ("Avoid Coventry; Birmingham preferred", "Birmingham", "DEFAULT_REVIEW_EXCLUSION", True),
    ("Birmingham or Coventry", "Birmingham", "DEFAULT_REVIEW_MULTIPLE", True),
    ("somewhere rural", "Birmingham", "DEFAULT_REVIEW_UNRECOGNISED", True),
    ("Nottingham", "Nottingham", "CITY_MATCH", False),
])
def test_location_classification(text, city, status, review):
    classify = function("classify_referral_location", "03_silver_business_rules")
    result = classify(text, "Birmingham", ["Coventry", "Nottingham"])
    assert result == (city, status, status != "CITY_MATCH", review)


def test_configurable_default_and_literal_city_names():
    classify = function("classify_referral_location", "03_silver_business_rules")
    assert classify(None, "Coventry")[0] == "Coventry"
    assert classify("New Town", "Birmingham", ["New Town"])[0] == "New Town"
    assert classify("Birminghamshire", "Birmingham")[1] == "DEFAULT_REVIEW_UNRECOGNISED"
    with pytest.raises(ValueError):
        classify(None, " ")


@pytest.mark.parametrize("table,key,cte", [
    ("referral_category", "referral_id", "referral_framework_category"),
    ("provider_home_category", "provider_home_id", "home_framework_category"),
])
def test_category_rollups_preserve_grain_and_ambiguity(table, key, cte):
    source = code("04_gold_model")
    query = re.search(rf"{cte} AS \(\s*(SELECT.*?)\n\)", source, re.S).group(1)
    with sqlite3.connect(":memory:") as db:
        db.execute("ATTACH DATABASE ':memory:' AS silver")
        db.execute(f"CREATE TABLE silver.{table} ({key} TEXT, framework_category_id INT)")
        db.executemany(f"INSERT INTO silver.{table} VALUES (?, ?)", [
            ("single", 7), ("single", 7), ("multi", 7), ("multi", 8),
            ("unknown", 999), ("null", None),
        ])
        rows = {row[0]: row[1:] for row in db.execute(query)}
    assert rows == {"single": (7, 1), "multi": (None, 2), "unknown": (999, 1), "null": (None, 0)}


def test_offer_contract_keeps_proposed_and_home_categories_distinct():
    source = code("04_gold_model")
    offer = source.split("CREATE OR REPLACE TABLE gold.fact_offer AS", 1)[1].split('""")', 1)[0]
    assert "o.category AS framework_category_id" in offer
    assert "AS provider_home_framework_category_id" in offer
    assert "o.provider_home_id AS provider_home_id" in offer
    assert "AS home_id" not in offer
    assert "LEFT JOIN home_framework_category" in offer
    assert "framework_category_count" in source.split("snapshot =", 1)[1].split("month_start =", 1)[0]


def test_new_bridges_preserve_source_column_names():
    source = code("05_gold_dimensions")
    for table, columns in {
        "referral_framework_category": ("referral_id", "framework_category_id"),
        "provider_home_spot_category": ("provider_home_id", "spot_category_code"),
        "referral_spot_category": ("referral_id", "spot_category"),
    }.items():
        block = source.split(f'"gold.bridge_{table}"', 1)[1].split("\n)", 1)[0]
        assert all(f'("{name}", "{name}")' in block for name in columns)
        assert f"gold.bridge_{table}" in code("00_setup_cfg")


@pytest.mark.parametrize("coords,expected", [
    ((0, 0, 0, 0), 0),
    ((0, 0, 0, 90), math.pi * 6371.0088 / 2),
    ((0, 0, 0, 180), math.pi * 6371.0088),
    ((None, 0, 0, 90), None),
    ((91, 0, 0, 90), None),
    ((0, 181, 0, 90), None),
])
def test_distance_expression_uses_km_and_rejects_missing_or_invalid_coordinates(coords, expected):
    expression = function("distance_km_sql", "04_gold_model")("a", "b", "c", "d")
    with sqlite3.connect(":memory:") as db:
        db.create_function("LEAST", -1, min)
        db.create_function("GREATEST", -1, max)
        result = db.execute(f"SELECT {expression} FROM (SELECT ? a, ? b, ? c, ? d)", coords).fetchone()[0]
    if expected is None:
        assert result is None
    else:
        assert result == pytest.approx(expected, abs=0.001)


def test_geography_is_local_and_reviewed_locations_cannot_produce_distance():
    silver = code("03_silver_business_rules")
    gold = code("04_gold_model")
    assert '"monitoring.cfg_location_coordinate"' in code("00_setup_cfg")
    assert "location_requires_review" in silver
    assert '"referral_location"' in silver
    assert '"provider_home_location"' in silver
    assert "WHEN loc.location_requires_review THEN NULL" in gold
    assert "APPROXIMATE_DEFAULT_CITY" in gold
    assert "APPROXIMATE_PREFERENCE_CITY" in gold
    assert "CITY_CENTROID_TO_POSTCODE_STRAIGHT_LINE" in gold


def test_referral_etl_simulation_sql_matches_current_notebook():
    source = code("04_gold_model")
    marker = "CREATE OR REPLACE TABLE gold.fact_referral AS"
    query = marker + source.split(marker, 1)[1].split('""")', 1)[0]
    assert query.strip() == (PROJECT / "tests/_gold_fact_sql.sql").read_text(encoding="utf-8").strip()


def test_location_default_reaches_live_and_archive_silver_child():
    assert 'child_parameters["DEFAULT_LOCATION_CITY"] = DEFAULT_LOCATION_CITY' in code("90_run_live_pipeline")
    assert '"DEFAULT_LOCATION_CITY": DEFAULT_LOCATION_CITY' in code("90_run_archive_pipeline")
    assert '"DEFAULT_LOCATION_CITY": DEFAULT_LOCATION_CITY' in code("02a_archive_silver")


def test_offer_sql_joins_without_fanout_and_with_explicit_distance_status():
    source = code("04_gold_model")
    requirements = next(ast.literal_eval(node.value) for node in ast.parse(source).body
                        if isinstance(node, ast.Assign)
                        and any(isinstance(t, ast.Name) and t.id == "GOLD_SOURCE_REQUIREMENTS"
                                for t in node.targets))
    distance = function("distance_km_sql", "04_gold_model")(
        "loc.location_latitude", "loc.location_longitude", "home.home_latitude", "home.home_longitude",
    )
    query = source.split("CREATE OR REPLACE TABLE gold.fact_offer AS", 1)[1].split('""")', 1)[0]
    query = (query.replace("{AS_OF_SQL}", "'2026-09-25'")
             .replace("{GOLD_JOB_RUN_ID}", "synthetic-job").replace("{OFFER_DISTANCE_KM_SQL}", distance)
             .replace(" AS TIMESTAMP)", " AS TEXT)").replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP"))
    with sqlite3.connect(":memory:") as db:
        db.row_factory = sqlite3.Row
        db.create_function("LEAST", -1, min)
        db.create_function("GREATEST", -1, max)
        db.create_function("TO_DATE", 1, lambda value: value)
        db.create_function("DATEDIFF", 2, lambda a, b: None)
        db.execute("ATTACH DATABASE ':memory:' AS silver")
        for table, columns in requirements.items():
            db.execute(f"CREATE TABLE {table} ({', '.join(sorted(columns))})")

        def insert(table, **values):
            db.execute(f"INSERT INTO silver.{table} ({', '.join(values)}) "
                       f"VALUES ({', '.join('?' for _ in values)})", tuple(values.values()))

        for n in range(1, 6):
            insert("offer", offer_id=f"o{n}", referral_provider_id=f"rp{n}", category=99, provider_home_id="h")
            insert("referral_provider", referral_provider_id=f"rp{n}", referral_id=f"r{n}", provider_id="p")
        for category in (7, 7, 8):
            insert("provider_home_category", provider_home_id="h", framework_category_id=category)
        insert("provider_home_location", provider_home_id="h", home_latitude=0, home_longitude=90)
        for n, review, default, lat in ((1, 0, 0, 0), (2, 1, 1, 0), (3, 0, 1, 0), (4, 0, 0, None)):
            insert("referral_location", referral_id=f"r{n}", location="Synthetic city",
                   location_requires_review=review, location_is_default=default,
                   location_latitude=lat, location_longitude=0)
        rows = {row["offer_id"]: dict(row) for row in db.execute(query)}
    assert len(rows) == 5
    assert all(row["framework_category_id"] == 99 for row in rows.values())
    assert all(row["provider_home_framework_category_id"] is None for row in rows.values())
    assert all(row["provider_home_framework_category_count"] == 2 for row in rows.values())
    assert rows["o1"]["referral_to_home_distance_km"] == pytest.approx(10007.5572, abs=0.001)
    assert rows["o1"]["referral_to_home_distance_status"] == "APPROXIMATE_PREFERENCE_CITY"
    assert rows["o2"]["referral_to_home_distance_km"] is None
    assert rows["o2"]["referral_to_home_distance_status"] == "LOCATION_REQUIRES_REVIEW"
    assert rows["o3"]["referral_to_home_distance_status"] == "APPROXIMATE_DEFAULT_CITY"
    assert rows["o4"]["referral_to_home_distance_status"] == "MISSING_CITY_COORDINATES"
    assert rows["o5"]["referral_to_home_distance_status"] == "MISSING_REFERRAL_LOCATION"
