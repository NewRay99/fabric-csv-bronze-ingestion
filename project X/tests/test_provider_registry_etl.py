"""GLD-023 data-grain regressions using synthetic contacts, never live data.

Executes the notebook's SQL with SQLite timestamp/type syntax adaptations and
equivalent collect-set/sorted-array functions. Fabric/Delta remains a separate
deployment check. Report checks cover safe file edits, not Power BI rendering.
"""

import ast
import importlib.util
import json
from pathlib import Path
import re
import sqlite3
from types import SimpleNamespace

import pytest

from notebook_loader import load_notebook


PROJECT = Path(__file__).resolve().parents[1]
NOTEBOOK = PROJECT / "05_gold_dimensions.py"


def notebook_code():
    return "\n\n".join("".join(cell["source"]) for cell in load_notebook(NOTEBOOK)["cells"]
                       if cell["cell_type"] == "code")


def functions(**scope):
    definitions = [node for node in ast.parse(notebook_code()).body if isinstance(node, ast.FunctionDef)
                   and node.name in {"provider_registry_columns", "provider_registry_sql", "require_columns"}]
    exec(compile(ast.Module(body=definitions, type_ignores=[]), str(NOTEBOOK), "exec"), scope)
    return scope


class CollectSet:
    def __init__(self):
        self.values = set()

    def step(self, value):
        if value is not None:
            self.values.add(value)

    def finalize(self):
        return json.dumps(sorted(self.values))


def fixture_rows(providers, memberships, frameworks, job="synthetic-registry-job"):
    scope = functions()
    fields = scope["provider_registry_columns"]() + ["export_date", "_silver_load_ts"]
    query = scope["provider_registry_sql"]("silver", "gold", job)
    query = (query.replace(" AS TIMESTAMP)", " AS TEXT)").replace(" AS STRING)", " AS TEXT)")
             .replace("CURRENT_TIMESTAMP()", "CURRENT_TIMESTAMP"))
    with sqlite3.connect(":memory:") as db:
        db.row_factory = sqlite3.Row
        db.execute("ATTACH DATABASE ':memory:' AS silver")
        db.execute("ATTACH DATABASE ':memory:' AS gold")
        db.execute("CREATE TABLE silver.provider (" + ", ".join(fields) + ")")
        db.execute("CREATE TABLE gold.bridge_provider_framework "
                   "(provider_framework_id, provider_id, framework_code, source_export_date)")
        db.execute("CREATE TABLE gold.dim_framework (framework_code, placement_type)")
        db.create_aggregate("COLLECT_SET", 1, CollectSet)
        db.create_function("SORT_ARRAY", 1, lambda value: json.dumps(sorted(json.loads(value))))
        db.create_function("CONCAT_WS", 2, lambda separator, value: separator.join(json.loads(value)))
        for provider in providers:
            record = {"export_date": "2026-10-01 00:00:00", "_silver_load_ts": "2026-10-01 01:00:00", **provider}
            db.execute("INSERT INTO silver.provider (" + ", ".join(record) + ") VALUES (" +
                       ", ".join("?" for _ in record) + ")", tuple(record.values()))
        db.executemany("INSERT INTO gold.bridge_provider_framework VALUES (?, ?, ?, ?)", memberships)
        db.executemany("INSERT INTO gold.dim_framework VALUES (?, ?)", frameworks)
        return {row["provider_id"]: dict(row) for row in db.execute(query)}


def membership(provider, framework, key=None, date="2026-10-01"):
    return (key or provider + framework, provider, framework, date)


def test_registry_keeps_no_offer_providers_and_all_distinct_fostering_frameworks():
    rows = fixture_rows(
        [{"provider_id": "without-offers", "provider_name": "Synthetic Provider"},
         {"provider_id": "mixed", "provider_name": "Mixed Framework Provider"},
         {"provider_id": "non-fostering"}, {"provider_id": "no-membership"}],
        [membership("without-offers", "F2"), membership("without-offers", "F1"),
         membership("without-offers", "F1"), membership("without-offers", "F1", "different-link"),
         membership("mixed", "R1"), membership("mixed", "F1"), membership("non-fostering", "R1")],
        [("F2", "Fostering"), ("F1", " fostering "), ("R1", "Residential")],
    )
    assert set(rows) == {"without-offers", "mixed"}
    assert rows["without-offers"]["framework_code"] == "F1; F2"
    assert rows["without-offers"]["framework_count"] == 2
    assert rows["mixed"]["framework_code"] == "F1"
    assert all(row["placement_type"] == row["service_type"] == "Fostering" for row in rows.values())
    assert all(row["home_name"] == "N/A" for row in rows.values())


def test_latest_contact_record_uses_export_date_then_load_timestamp():
    rows = fixture_rows(
        [{"provider_id": "p", "provider_email_address": "old@example.invalid", "export_date": "2026-09-30"},
         {"provider_id": "p", "provider_email_address": "early@example.invalid", "_silver_load_ts": "2026-10-01 00:01:00"},
         {"provider_id": "p", "provider_email_address": "latest@example.invalid"}],
        [membership("p", "F1")], [("F1", "Fostering")],
    )
    assert rows["p"]["provider_email_address"] == "latest@example.invalid"
    assert rows["p"]["source_export_date"] == "2026-10-01 00:00:00"


def test_exact_timestamp_ties_are_deterministic_in_both_input_orders():
    providers = [{"provider_id": "p", "provider_email_address": f"{suffix}@example.invalid"} for suffix in ("a", "z")]
    forward = fixture_rows(providers, [membership("p", "F1")], [("F1", "Fostering")])
    reverse = fixture_rows(list(reversed(providers)), [membership("p", "F1")], [("F1", "Fostering")])
    assert forward["p"]["provider_email_address"] == reverse["p"]["provider_email_address"] == "z@example.invalid"


def test_current_membership_does_not_resurrect_superseded_fostering_link():
    rows = fixture_rows(
        [{"provider_id": "changed"}, {"provider_id": "unknown"}],
        [membership("changed", "F1", "link", "2026-09-01"), membership("changed", "R1", "link"),
         membership("unknown", "unrecognised-framework")],
        [("F1", "Fostering"), ("R1", "Residential")],
    )
    assert rows == {}


def test_nullable_contacts_and_phone_leading_zeros_are_preserved():
    rows = fixture_rows(
        [{"provider_id": "p", "provider_phone_number": "01234567890",
          "responsible_individual_contact_number": "+44 01234 567890",
          "registrant_contact_number": "00123", "postcode": "B01 1AA"}],
        [membership("p", "F1")], [("F1", "Fostering")], job="synthetic'quoted-job",
    )
    record = rows["p"]
    assert record["provider_phone_number"] == "01234567890"
    assert record["responsible_individual_contact_number"] == "+44 01234 567890"
    assert record["registrant_contact_number"] == "00123"
    assert record["postcode"] == "B01 1AA"
    assert record["provider_email_address"] is None
    assert record["responsible_individual_name"] is None
    assert record["registrant_name"] is None
    assert record["job_run_id"] == "synthetic'quoted-job"


def test_newest_missing_contact_is_not_filled_with_outdated_contact():
    rows = fixture_rows(
        [{"provider_id": "p", "provider_email_address": "outdated@example.invalid", "export_date": "2026-09-30"},
         {"provider_id": "p", "provider_email_address": None}],
        [membership("p", "F1")], [("F1", "Fostering")],
    )
    assert rows["p"]["provider_email_address"] is None


def test_null_or_blank_provider_ids_cannot_create_registry_rows():
    rows = fixture_rows([{ "provider_id": None}, {"provider_id": ""}, {"provider_id": "   "}],
                        [membership("", "F1"), membership("   ", "F1")], [("F1", "Fostering")])
    assert rows == {}


def test_registry_required_column_preflight_fails_for_missing_contact_column():
    scope = functions()
    columns = scope["provider_registry_columns"]()
    fields = [SimpleNamespace(name=name) for name in columns if name != "provider_email_address"]
    scope["spark"] = SimpleNamespace(catalog=SimpleNamespace(tableExists=lambda name: True),
                                     table=lambda name: SimpleNamespace(schema=SimpleNamespace(fields=fields)))
    with pytest.raises(ValueError, match="provider_email_address"):
        scope["require_columns"]("silver.provider", columns)


def test_registry_import_contract_matches_sql_output_and_keeps_phone_columns_as_text():
    registry = fixture_rows([{"provider_id": "p"}], [membership("p", "F1")], [("F1", "Fostering")])["p"]
    template = (PROJECT / "tools/templates/provider_registry.tmdl").read_text(encoding="utf-8")
    source_columns = set(re.findall(r"sourceColumn: (\w+)", template))
    assert source_columns == set(registry)
    for column in ("Provider Phone", "Responsible Individual Contact Number", "Registrant Contact Number"):
        block = template.split("\tcolumn '" + column + "'", 1)[1].split("\tcolumn ", 1)[0]
        assert "dataType: string" in block and "summarizeBy: none" in block
    assert 'Item="rpt_provider_registry"' in template
    assert "MissingField.UseNull" not in template
    assert "rpt_provider_fostering" not in template


@pytest.mark.parametrize("schema", ["gold;DROP TABLE provider", "a.b", "gold'", ""])
def test_registry_query_rejects_unsafe_schema_identifiers(schema):
    with pytest.raises(ValueError, match="SQL identifiers"):
        functions()["provider_registry_sql"]("silver", schema, "test-job")


def load_report_tool():
    path = PROJECT / "tools/add_wmpp_provider_registry_extract.py"
    spec = importlib.util.spec_from_file_location("registry_report_tool", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def report_fixture(tmp_path):
    tool = load_report_tool()
    originals = {
        tool.MODEL / "model.tmdl": 'model Model\nannotation PBI_QueryOrder = ["dim_provider"]\nref table dim_provider\n',
        tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl":
            "role 'WMPP Dynamic Detail RLS'\n\tmodelPermission: read\n\ttablePermission fact_referral = TRUE ()\n\n\tannotation PBI_Id = synthetic\n",
        tool.REPORT / "pages/pages.json": '{"pageOrder":["existing"],"activePageName":"existing"}\n',
        tool.REPORT / "pages/existing/visuals/user-layout/visual.json": '{"userLayout":"must remain unchanged"}\n',
        tool.MODEL / "relationships.tmdl": "relationship existing\n\tfromColumn: fact_offer.provider_id\n\ttoColumn: dim_provider.provider_id\n",
        tool.REPORT / "bookmarks/user-bookmark.bookmark.json": '{"userBookmark":"must remain unchanged"}\n',
    }
    for relative, contents in originals.items():
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    return tool, originals


def test_report_plan_preserves_existing_visuals_bookmarks_and_relationships(tmp_path):
    tool, originals = report_fixture(tmp_path)
    planned = tool.plan_changes(tmp_path)
    new_page = tool.REPORT / "pages" / tool.PAGE_ID
    allowed_existing = {tool.MODEL / "model.tmdl", tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl",
                        tool.REPORT / "pages/pages.json"}
    for path in planned:
        relative = path.relative_to(tmp_path)
        assert relative in allowed_existing or relative == tool.MODEL / "tables/rpt_provider_registry.tmdl" or relative.is_relative_to(new_page)
    role = planned[tmp_path / tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"]
    assert role.replace(tool.DENY_RULE + "\n", "") == originals[tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"]
    metadata = json.loads(planned[tmp_path / tool.REPORT / "pages/pages.json"])
    assert metadata["activePageName"] == "existing" and metadata["pageOrder"] == ["existing", tool.PAGE_ID]
    for path, contents in planned.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    assert not tool.plan_changes(tmp_path)


def test_report_plan_refuses_unknown_roles_or_modified_contact_access(tmp_path):
    tool, _ = report_fixture(tmp_path)
    path = tmp_path / tool.MODEL / "roles/Unapproved Other Role.tmdl"
    path.write_text("role 'Unapproved Other Role'\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unrecognised RLS roles"):
        tool.plan_changes(tmp_path)
    path.unlink()
    role_path = tmp_path / tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
    role_path.write_text(role_path.read_text(encoding="utf-8").replace(
        "\tannotation PBI_Id", "\ttablePermission rpt_provider_registry = TRUE ()\n\tannotation PBI_Id"), encoding="utf-8")
    with pytest.raises(RuntimeError, match="audience decision"):
        tool.plan_changes(tmp_path)


def test_report_plan_never_overwrites_user_edited_registry_definitions(tmp_path):
    tool, _ = report_fixture(tmp_path)
    path = tmp_path / tool.MODEL / "tables/rpt_provider_registry.tmdl"
    path.parent.mkdir(parents=True)
    path.write_text("table rpt_provider_registry\n\tannotation UserChanges = true\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="user edits"):
        tool.plan_changes(tmp_path)
    assert "UserChanges" in path.read_text(encoding="utf-8")


def test_export_table_includes_the_requested_columns_and_unique_provider_key():
    tool = load_report_tool()
    projections = tool.registry_table()["visual"]["query"]["queryState"]["Values"]["projections"]
    assert tuple(item["nativeQueryRef"] for item in projections) == tool.EXPORT_FIELDS
    assert len(tool.EXPORT_FIELDS) == len(set(tool.EXPORT_FIELDS)) == 21
    assert tool.EXPORT_FIELDS[0] == "Provider ID"
    assert all(item["field"]["Column"]["Expression"]["SourceRef"]["Entity"] == tool.TABLE for item in projections)
