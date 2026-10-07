"""GLD-023 data-grain regressions using synthetic contacts, never live data.

Executes the notebook's SQL with SQLite timestamp/type syntax adaptations and
equivalent collect-set/sorted-array functions. Fabric/Delta remains a separate
deployment check. Report checks cover safe file edits, not Power BI rendering.
"""

import ast
from collections import Counter
from datetime import date
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
                   and node.name in {"provider_registry_columns", "provider_registry_sources", "provider_registry_baseline_columns",
                                     "provider_registry_sql", "validate_provider_registry_baseline", "require_columns"}]
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


def fixture_rows(providers, memberships, frameworks, job="synthetic-registry-job", *,
                 homes=(), offers=(), ipas=(), assignments=(), messages=(), by_home=False,
                 dimension_providers=None, dimension_homes=None, with_baseline=False):
    scope = functions()
    fields = scope["provider_registry_columns"]() + ["export_date", "_silver_load_ts"]
    query = scope["provider_registry_sql"]("silver", "gold", job, "2026-10-01")
    query = re.sub(r"CAST\((COALESCE\([^)]*\)|[^()]*) AS DATE\)", r"DATE(\1)", query)
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
        db.create_function("DATEDIFF", 2, lambda end, start: (date.fromisoformat(end[:10]) - date.fromisoformat(start[:10])).days)
        defaults = {"export_date": "2026-10-01", "source_export_date": "2026-10-01",
                    "_silver_load_ts": "2026-10-01 01:00:00", "as_of_date": "2026-10-01"}
        for (source, columns), records in zip(scope["provider_registry_sources"]("silver", "gold").items(),
                                               (homes, offers, ipas, assignments, messages), strict=True):
            db.execute("CREATE TABLE " + source + " (" + ", ".join(columns) + ")")
            for record in records:
                values = {name: defaults[name] for name in columns if name in defaults}
                values.update(record)
                db.execute("INSERT INTO " + source + " (" + ", ".join(values) + ") VALUES (" +
                           ", ".join("?" for _ in values) + ")", tuple(values.values()))
        for provider in providers:
            record = {"export_date": "2026-10-01 00:00:00", "_silver_load_ts": "2026-10-01 01:00:00", **provider}
            db.execute("INSERT INTO silver.provider (" + ", ".join(record) + ") VALUES (" +
                       ", ".join("?" for _ in record) + ")", tuple(record.values()))
        db.executemany("INSERT INTO gold.bridge_provider_framework VALUES (?, ?, ?, ?)", memberships)
        db.executemany("INSERT INTO gold.dim_framework VALUES (?, ?)", frameworks)
        # Independent fixture of the real dimension projection/latest-key rule.
        # Registry contacts and metrics must never define its baseline population.
        provider_fields = fields[:9] + ["export_date", "source_export_date"]
        home_fields = ["provider_home_id", "provider_id", "home_name", "service_type", "town_city", "county", "postcode",
                       "registered_beds", "is_spot", "home_contact_number", "export_date", "source_export_date"]
        for table, columns, records in (("gold.dim_provider", provider_fields, dimension_providers),
                                       ("gold.dim_provider_home", home_fields, dimension_homes)):
            if records is None:
                source = "silver.provider_home" if table.endswith("home") else "silver.provider"
                projection = ", ".join("number_of_registered_beds AS registered_beds" if name == "registered_beds"
                                       else "export_date AS source_export_date" if name == "source_export_date" else name
                                       for name in columns)
                db.execute(f"CREATE TABLE {table} AS SELECT {projection} FROM (SELECT *, ROW_NUMBER() OVER ("
                           f"PARTITION BY {columns[0]} ORDER BY export_date DESC, _silver_load_ts DESC) AS fixture_rank "
                           f"FROM {source}) WHERE fixture_rank = 1")
            else:
                db.execute("CREATE TABLE " + table + " (" + ", ".join(columns) + ")")
                for record in records:
                    values = {name: defaults[name] for name in columns if name in defaults}
                    values.update(record)
                    db.execute("INSERT INTO " + table + " (" + ", ".join(values) + ") VALUES (" +
                               ", ".join("?" for _ in values) + ")", tuple(values.values()))
        baseline = [dict(row) for row in db.execute("SELECT p.provider_id, h.provider_home_id FROM gold.dim_provider p "
                                                   "LEFT JOIN gold.dim_provider_home h ON p.provider_id = h.provider_id")]
        result = [dict(row) for row in db.execute(query)]
        if with_baseline:
            return result, baseline
        return result if by_home else {row["provider_id"]: row for row in result}


def membership(provider, framework, key=None, date="2026-10-01"):
    return (key or provider + framework, provider, framework, date)


def test_registry_exactly_preserves_1002_dimension_left_join_rows_without_eligibility_filters():
    providers = [{"provider_id": f"p{index}", "provider_name": f"Synthetic {index}",
                  "provider_status": "CLOSED" if index % 2 else "ACTIVE"} for index in range(1000)]
    rows, baseline = fixture_rows(
        providers, [membership("p0", "F1"), membership("p1", "R1"), membership("p2", "unknown")],
        [("F1", "Fostering"), ("R1", "Residential")],
        homes=[{"provider_id": "p0", "provider_home_id": f"h{index}"} for index in range(3)],
        with_baseline=True,
    )
    assert len(baseline) == 1002
    assert len(rows) == len(baseline), "Registry dropped rows from dim_provider LEFT dim_provider_home"
    assert {(row["provider_id"], row["provider_home_id"]) for row in rows} == {
        (row["provider_id"], row["provider_home_id"]) for row in baseline
    }


def test_registry_keeps_all_providers_and_all_distinct_frameworks_without_eligibility_filters():
    rows = fixture_rows(
        [{"provider_id": "without-offers", "provider_name": "Synthetic Provider"},
         {"provider_id": "mixed", "provider_name": "Mixed Framework Provider"},
         {"provider_id": "non-fostering"}, {"provider_id": "no-membership"}],
        [membership("without-offers", "F2"), membership("without-offers", "F1"),
         membership("without-offers", "F1"), membership("without-offers", "F1", "different-link"),
         membership("mixed", "R1"), membership("mixed", "F1"), membership("non-fostering", "R1")],
        [("F2", "Fostering"), ("F1", " fostering "), ("R1", "Residential")],
    )
    assert set(rows) == {"without-offers", "mixed", "non-fostering", "no-membership"}
    assert rows["without-offers"]["framework_code"] == "F1; F2"
    assert rows["without-offers"]["framework_count"] == 2
    assert rows["mixed"]["framework_code"] == "F1; R1"
    assert {value.strip().lower() for value in rows["mixed"]["placement_type"].split(";")} == {"fostering", "residential"}
    assert rows["non-fostering"]["placement_type"] == "Residential"
    assert rows["no-membership"]["framework_count"] == 0
    assert rows["no-membership"]["framework_code"] is None
    assert all(row["home_name"] is None and row["service_type"] is None for row in rows.values())


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


def test_current_membership_does_not_resurrect_superseded_link_or_remove_unknown_framework_provider():
    rows = fixture_rows(
        [{"provider_id": "changed"}, {"provider_id": "unknown"}],
        [membership("changed", "F1", "link", "2026-09-01"), membership("changed", "R1", "link"),
         membership("unknown", "unrecognised-framework")],
        [("F1", "Fostering"), ("R1", "Residential")],
    )
    assert set(rows) == {"changed", "unknown"}
    assert rows["changed"]["framework_code"] == "R1"
    assert rows["unknown"]["framework_code"] == "unrecognised-framework"
    assert rows["unknown"]["placement_type"] is None


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


def test_registry_never_silently_drops_null_or_blank_ids_already_present_in_dimensions():
    rows = fixture_rows([{ "provider_id": None}, {"provider_id": ""}, {"provider_id": "   "}],
                        [membership("", "F1"), membership("   ", "F1")], [("F1", "Fostering")])
    assert set(rows) == {None, "", "   "}


def test_gold_dimensions_not_contacts_or_memberships_define_registry_population_and_basic_fields():
    rows, baseline = fixture_rows(
        [{"provider_id": "gold-only", "provider_name": "Stale Silver Name", "postcode": "WRONG",
          "provider_email_address": "contact@example.invalid"}, {"provider_id": "silver-only"}], [], [],
        homes=[{"provider_home_id": "h", "provider_id": "gold-only", "home_name": "Stale Silver Home", "postcode": "WRONG",
                "status": "ACTIVE", "home_email_address": "home@example.invalid"},
               {"provider_home_id": "silver-only-home", "provider_id": "gold-only"}],
        dimension_providers=[{"provider_id": "gold-only", "provider_name": "Authoritative Gold Provider", "postcode": "B1 1AA"},
                             {"provider_id": "no-contact", "provider_name": "No contact record", "provider_status": "SUSPENDED"}],
        dimension_homes=[{"provider_id": "gold-only", "provider_home_id": "h", "home_name": "Authoritative Gold Home", "postcode": "B2 2BB", "registered_beds": 5},
                         {"provider_id": "no-contact", "provider_home_id": "no-home-contact", "home_name": "Gold-only home"}],
        with_baseline=True,
    )
    assert len(rows) == len(baseline) == 2
    keyed = {row["provider_id"]: row for row in rows}
    assert keyed["gold-only"]["provider_name"] == "Authoritative Gold Provider"
    assert keyed["gold-only"]["postcode"] == "B1 1AA"
    assert keyed["gold-only"]["home_name"] == "Authoritative Gold Home"
    assert keyed["gold-only"]["home_postcode"] == "B2 2BB"
    assert keyed["gold-only"]["home_registered_beds"] == 5
    assert keyed["gold-only"]["provider_email_address"] == "contact@example.invalid"
    assert keyed["gold-only"]["home_email_address"] == "home@example.invalid"
    assert keyed["no-contact"]["provider_name"] == "No contact record"
    assert keyed["no-contact"]["provider_status"] == "SUSPENDED"
    assert keyed["no-contact"]["home_name"] == "Gold-only home"
    assert keyed["no-contact"]["provider_email_address"] is None
    assert keyed["no-contact"]["home_offer_count"] == 0


class RegistryKeyFrame:
    """Tiny multiset fixture of the baseline validator's public DataFrame seam."""
    def __init__(self, keys):
        self.keys = list(keys)

    def select(self, *names):
        assert names == ("provider_id", "provider_home_id")
        return self

    def count(self):
        return len(self.keys)

    def exceptAll(self, other):
        remaining = Counter(self.keys) - Counter(other.keys)
        return RegistryKeyFrame(remaining.elements())

    def limit(self, size):
        return RegistryKeyFrame(self.keys[:size])


@pytest.mark.parametrize("actual", [
    [("p", "h1")],  # missing home
    [("p", "h1"), ("p", "h2"), ("p", "h2")],  # multiplied home
    [("p", "h1"), ("different", "h2")],  # same count, wrong provider
    [("p", "h1"), ("p", "h1")],  # same count, one pair duplicated and another lost
])
def test_registry_baseline_guard_rejects_missing_added_or_substituted_rows(actual):
    baseline = RegistryKeyFrame([("p", "h1"), ("p", "h2")])
    captured = []
    scope = functions(spark=SimpleNamespace(sql=lambda query: captured.append(query) or baseline))
    with pytest.raises(ValueError, match="(row count|rows must exactly match)"):
        scope["validate_provider_registry_baseline"](RegistryKeyFrame(actual), "gold")
    assert "FROM gold.dim_provider p" in captured[0]
    assert "LEFT JOIN gold.dim_provider_home" in captured[0]
    assert "framework" not in captured[0] and "WHERE" not in captured[0]


def test_registry_baseline_guard_accepts_the_exact_multiset_including_no_home_rows():
    keys = [("p", "h1"), ("p", "h2"), ("no-home", None), (None, None)]
    scope = functions(spark=SimpleNamespace(sql=lambda query: RegistryKeyFrame(keys)))
    assert scope["validate_provider_registry_baseline"](RegistryKeyFrame(list(reversed(keys))), "gold") == 4


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


def test_left_home_join_keeps_all_homes_no_offer_homes_and_no_home_provider():
    rows = fixture_rows(
        [{"provider_id": "p"}, {"provider_id": "no-home"}],
        [membership("p", "F1"), membership("no-home", "F1")], [("F1", "Fostering")],
        homes=[{"provider_home_id": "h1", "provider_id": "p", "home_name": "First", "postcode": "B1 1AA"},
               {"provider_home_id": "h2", "provider_id": "p", "home_name": "Second", "service_type": "Residential"},
               {"provider_home_id": "h1", "provider_id": "p", "home_name": "Old", "export_date": "2026-09-01"}],
        by_home=True,
    )
    keyed = {(row["provider_id"], row["provider_home_id"]): row for row in rows}
    assert len(rows) == len(keyed) == 3
    assert keyed["p", "h1"]["home_name"] == "First"
    assert keyed["p", "h1"]["home_postcode"] == "B1 1AA"
    assert keyed["p", "h2"]["service_type"] == "Residential"
    assert keyed["no-home", None]["provider_offer_count"] == 0
    assert keyed["no-home", None]["home_ipa_count"] == 0
    assert keyed["no-home", None]["provider_average_response_minutes"] is None
    assert keyed["no-home", None]["provider_average_offer_distance_km"] is None
    assert keyed["no-home", None]["provider_estimated_lifetime_cost_to_date"] == 0


def test_provider_and_home_metrics_do_not_fan_out_or_attribute_messages_to_homes():
    offers = [
        {"offer_id": "o1", "provider_id": "p", "provider_home_id": "h1", "offer_status": "OFFER_SUCCESSFUL", "referral_to_home_distance_km": 10},
        {"offer_id": "o2", "provider_id": "p", "provider_home_id": "h1", "offer_status": " draft ", "referral_to_home_distance_km": 30},
        {"offer_id": "o3", "provider_id": "p", "provider_home_id": "h2", "offer_status": "OFFER_UNSUCCESSFUL"},
        {"offer_id": "no-home", "provider_id": "p", "offer_status": "OFFER_MADE"},
    ]
    ipa = {"ipa_id": "i1", "accepted_offer_id": "o1", "signed_by_provider": 1, "is_ipa_completed": 1,
           "is_placement_closed": 0, "placement_admission_date": "2026-09-25 12:00:00", "estimated_weekly_cost": 700}
    assignments = [{"referral_provider_id": "a1", "provider_id": "p", "response_elapsed_minutes": 10},
                   {"referral_provider_id": "a2", "provider_id": "p", "response_elapsed_minutes": 30, "is_declined": 1},
                   {"referral_provider_id": "a3", "provider_id": "p", "response_elapsed_minutes": -5}]
    messages = [{"message_id": "m1", "referral_provider_id": "a1"}, {"message_id": "m2", "referral_provider_id": "a1"},
                {"message_id": "future", "referral_provider_id": "a1", "created_timestamp": "2026-10-02"}]
    rows = fixture_rows(
        [{"provider_id": "p"}], [membership("p", "F1")], [("F1", "Fostering")],
        homes=[{"provider_home_id": "h1", "provider_id": "p"}, {"provider_home_id": "h2", "provider_id": "p"}],
        offers=offers + [dict(offers[0]), {**offers[1], "offer_status": "OFFER_MADE", "source_export_date": "2026-09-01"}],
        ipas=[ipa, dict(ipa)], assignments=assignments + [dict(assignments[0])], messages=messages + [dict(messages[0])],
        by_home=True,
    )
    keyed = {row["provider_home_id"]: row for row in rows}
    for row in rows:
        assert row["provider_offer_count"] == 4  # includes drafts; not offers × IPAs × messages
        assert row["provider_draft_offer_count"] == row["provider_rejected_offer_count"] == row["provider_accepted_offer_count"] == 1
        assert row["provider_ipa_count"] == row["provider_completed_ipa_count"] == 1
        assert row["provider_has_provider_signed_ipa"] == row["provider_has_completed_ipa"] == 1
        assert row["provider_assignment_count"] == 3 and row["provider_declined_assignment_count"] == 1
        assert row["provider_message_count"] == 2
        assert row["provider_timed_response_count"] == 2 and row["provider_average_response_minutes"] == 20
        assert row["provider_offers_with_distance_count"] == 2 and row["provider_average_offer_distance_km"] == 20
        assert row["provider_estimated_active_weekly_cost"] == row["provider_estimated_lifetime_cost_to_date"] == 700
        assert row["metrics_as_of_date"] == "2026-10-01"
        assert "home_message_count" not in row  # source has no home key
    assert keyed["h1"]["home_offer_count"] == 2 and keyed["h2"]["home_offer_count"] == 1
    assert keyed["h1"]["home_estimated_lifetime_cost_to_date"] == 700
    assert keyed["h2"]["home_estimated_lifetime_cost_to_date"] == 0


def test_costs_are_estimated_inclusive_prorated_bounded_and_missing_evidence_is_visible():
    def ipa(key, **values):
        return {"ipa_id": key, "accepted_offer_id": "o", "is_placement_closed": 0,
                "estimated_weekly_cost": 700, "placement_admission_date": "2026-09-25", **values}
    base = dict(providers=[{"provider_id": "p"}], memberships=[membership("p", "F1")], frameworks=[("F1", "Fostering")],
                offers=[{"offer_id": "o", "provider_id": "p"}])
    row = fixture_rows(**base, ipas=[
        ipa("active"), ipa("closed", is_placement_closed=1, placement_ended_date="2026-09-26"),
        ipa("future", placement_admission_date="2026-10-02"),
        ipa("future-end", is_placement_closed=1, placement_ended_date="2026-10-03"),
        ipa("missing-fee", estimated_weekly_cost=None), ipa("missing-start", placement_admission_date=None),
        ipa("missing-end", is_placement_closed=1),
        ipa("reversed", is_placement_closed=1, placement_ended_date="2026-09-20"),
        ipa("negative-fee", estimated_weekly_cost=-1),
        {"ipa_id": "unlinked", "accepted_offer_id": "missing-offer", "estimated_weekly_cost": 999},
    ])["p"]
    assert row["provider_ipa_count"] == 9  # no provider ownership can be inferred for unlinked IPA
    assert row["provider_active_ipa_count"] == 5
    assert row["provider_estimated_active_weekly_cost"] == 2100  # non-closed, incl future/pending, as report defines it
    assert row["provider_active_ipas_missing_weekly_cost_count"] == 2
    assert row["provider_estimated_lifetime_cost_to_date"] == 1600  # 7 + 2 + 0 + 7 days at £100/day
    assert row["provider_ipas_missing_lifetime_cost_count"] == 5
    missing = fixture_rows(**base, ipas=[ipa("missing", estimated_weekly_cost=None)])["p"]
    assert missing["provider_estimated_active_weekly_cost"] is None
    assert missing["provider_estimated_lifetime_cost_to_date"] is None
    assert missing["provider_active_ipas_missing_weekly_cost_count"] == 1


def test_home_ownership_mismatch_never_credits_another_providers_home():
    rows = fixture_rows(
        [{"provider_id": "p"}, {"provider_id": "other"}], [membership("p", "F1"), membership("other", "F1")], [("F1", "Fostering")],
        homes=[{"provider_home_id": "h", "provider_id": "other"}],
        offers=[{"offer_id": "o", "provider_id": "p", "provider_home_id": "h"}], by_home=True,
    )
    keyed = {row["provider_id"]: row for row in rows}
    assert keyed["p"]["provider_offer_count"] == 1 and keyed["p"]["home_offer_count"] == 0
    assert keyed["other"]["provider_offer_count"] == keyed["other"]["home_offer_count"] == 0


@pytest.mark.parametrize("as_of", ["2026-13-01", "2026-10-01' OR true", ""])
def test_registry_rejects_invalid_metrics_dates(as_of):
    with pytest.raises(ValueError):
        functions()["provider_registry_sql"]("silver", "gold", "job", as_of)


def test_new_metrics_and_home_keys_are_unaggregated_semantic_columns():
    tool = load_report_tool()
    template = (PROJECT / "tools/templates/provider_registry.tmdl").read_text(encoding="utf-8")
    for name in tool.EXPORT_FIELDS:
        block = re.search(r"(?ms)^\tcolumn '?" + re.escape(name) + r"'?\n.*?(?=^\tcolumn |^\tpartition )", template)
        assert block, name
        assert "summarizeBy: none" in block.group(0)
    assert "dataType: boolean" in template.split("column 'Provider Signature Flag'", 1)[1].split("\tcolumn ", 1)[0]


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
    assert len(tool.EXPORT_FIELDS) == len(set(tool.EXPORT_FIELDS)) == 72
    assert tool.EXPORT_FIELDS[:2] == ("Provider ID", "Home ID")
    assert all(item["field"]["Column"]["Expression"]["SourceRef"]["Entity"] == tool.TABLE for item in projections)


def older_registry_fixture(tmp_path):
    tool, _ = report_fixture(tmp_path)
    for path, contents in tool.plan_changes(tmp_path).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    old_fields = ("Provider ID", "Provider Name", "Town/City", "Postcode", "Framework Code",
                  "Placement Type", "Home Name", "Service Type", "Provider Email", "Provider Phone",
                  "Responsible Individual Name", "Responsible Individual Contact Number", "Responsible Individual Email Address",
                  "Registrant Name", "Registrant Role", "Registrant Email", "Registrant Contact Number", "Provider Status",
                  "County", "Country", "Source Export Date", "Holding Company ID", "QA Flag", "Framework Count",
                  "Export Date", "Job Run ID", "Gold Modelled At")
    model = tmp_path / tool.MODEL / "tables/rpt_provider_registry.tmdl"
    contents = model.read_text(encoding="utf-8")
    for block in re.findall(r"(?ms)^\tcolumn [^\n]+\n.*?(?=^\tcolumn |^\tpartition |\Z)", contents):
        if block.splitlines()[0].removeprefix("\tcolumn ").strip("'") not in old_fields:
            contents = contents.replace(block, "")
    sources = re.findall(r"sourceColumn: (\w+)", contents)
    contents = re.sub(r"Selected = Table.SelectColumns\(Registry, \{.*?\}\)",
                      "Selected = Table.SelectColumns(Registry, {" + ", ".join('"' + source + '"' for source in sources) + "})",
                      contents, flags=re.S)
    contents = contents.replace("LH_BCT_WMPP", "UserEditedConnection")
    contents = contents.replace("\tcolumn 'Provider ID'\n", "\tcolumn 'Provider ID'\n\t\tlineageTag: existing-user-lineage\n")
    model.write_text(contents, encoding="utf-8")
    table_path = tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "visuals" / tool.visual_id("registry-export-table") / "visual.json"
    table = json.loads(table_path.read_text(encoding="utf-8"))
    table["position"]["z"] = 37
    table["visual"]["objects"]["values"][0]["properties"]["fontSize"] = tool.literal("13D")
    table["visual"]["query"]["queryState"]["Values"]["projections"] = [item for item in
        table["visual"]["query"]["queryState"]["Values"]["projections"] if item["nativeQueryRef"] in old_fields]
    table_path.write_text(tool.encode_json(table), encoding="utf-8")
    subtitle = tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "visuals" / tool.visual_id("registry-subtitle") / "visual.json"
    subtitle.write_text(subtitle.read_text(encoding="utf-8").replace(tool.REGISTRY_SUBTITLE,
        "Fostering providers with framework membership, including providers without offers. One row per Provider ID."), encoding="utf-8")
    return tool, model, table_path, subtitle


def test_registry_expansion_preserves_user_import_lineage_layout_security_and_exports(tmp_path):
    tool, model, table_path, subtitle = older_registry_fixture(tmp_path)
    model_definition = tmp_path / tool.MODEL / "model.tmdl"
    model_definition.write_text(model_definition.read_text(encoding="utf-8") + "ref role 'WMPP Dynamic Detail RLS'\n", encoding="utf-8")
    report_path = tmp_path / tool.REPORT / "report.json"
    report_path.write_text('{"settings":{"exportDataMode":"None"}}\n', encoding="utf-8")
    for path, value in tool.plan_group_access(tmp_path, "wmpp_report_users", "wmpp_provider_registry_users").items():
        path.write_text(value, encoding="utf-8")
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    table = json.loads(table_path.read_text(encoding="utf-8"))
    planned = tool.plan_registry_expansion(tmp_path)
    assert set(planned) == {model, table_path, subtitle}
    assert "UserEditedConnection" in planned[model] and "existing-user-lineage" in planned[model]
    updated_table = json.loads(planned[table_path])
    assert updated_table["position"] == table["position"]
    assert updated_table["visual"]["objects"] == table["visual"]["objects"]
    assert updated_table["visual"]["visualContainerObjects"] == table["visual"]["visualContainerObjects"]
    assert updated_table["visual"]["query"]["sortDefinition"] == table["visual"]["query"]["sortDefinition"]
    assert "Provider ID / Home ID" in planned[subtitle] and "do not sum" in planned[subtitle]
    for path, value in planned.items():
        path.write_text(value, encoding="utf-8")
    assert not tool.plan_registry_expansion(tmp_path)
    for path, value in before.items():
        if path not in planned:
            assert path.read_bytes() == value
    assert json.loads(report_path.read_text(encoding="utf-8"))["settings"]["exportDataMode"] == "None"


def test_registry_expansion_refuses_custom_import_selection_without_writing(tmp_path):
    tool, model, _, _ = older_registry_fixture(tmp_path)
    model.write_text(model.read_text(encoding="utf-8").replace("Selected = Table.SelectColumns", "CustomSelected = Table.RemoveColumns"), encoding="utf-8")
    before = model.read_bytes()
    with pytest.raises(RuntimeError, match="Unexpected registry column selection"):
        tool.plan_registry_expansion(tmp_path)
    assert model.read_bytes() == before


def test_explicit_registry_audience_preserves_other_security_and_does_not_enable_exports(tmp_path):
    tool, originals = report_fixture(tmp_path)
    report_path = tmp_path / tool.REPORT / "report.json"
    report_path.write_text('{"settings":{"exportDataMode":"None"}}\n', encoding="utf-8")
    # Install the original deny-by-default extract, then approve two identities.
    for path, contents in tool.plan_changes(tmp_path).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    users = ["second@example.invalid", "first@example.invalid"]
    planned = tool.plan_changes(tmp_path, users)
    role_path = tmp_path / tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
    role = planned[role_path]
    rule = tool.registry_permission(users)
    assert role.replace(rule + "\n", "") == originals[tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"]
    assert 'LOWER ( USERPRINCIPALNAME () ) IN { "first@example.invalid", "second@example.invalid" }' in role
    expected_paths = {
        role_path,
        tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "page.json",
        tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "visuals" / tool.visual_id("registry-access-note") / "visual.json",
    }
    assert set(planned) == expected_paths
    assert "visibility" not in json.loads(planned[tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "page.json"])
    assert report_path not in planned
    for path, contents in planned.items():
        path.write_text(contents, encoding="utf-8")
    assert not tool.plan_changes(tmp_path, users)
    assert json.loads(report_path.read_text(encoding="utf-8"))["settings"]["exportDataMode"] == "None"
    with pytest.raises(RuntimeError, match="audience decision"):
        tool.plan_changes(tmp_path)
    with pytest.raises(RuntimeError, match="audience decision"):
        tool.plan_changes(tmp_path, ["unapproved@example.invalid"])


@pytest.mark.parametrize("users", [[], [""], ["*"], ["example.invalid"], ['a@example.invalid" } || TRUE ()']])
def test_registry_audience_rejects_empty_wildcard_and_dax_inputs(users):
    with pytest.raises(ValueError, match="valid approved sign-in UPN"):
        load_report_tool().registry_permission(users)


def test_registry_audience_normalizes_and_deduplicates_exact_identities():
    tool = load_report_tool()
    assert tool.registry_permission([" FIRST@EXAMPLE.INVALID ", "first@example.invalid"]) == (
        '\ttablePermission rpt_provider_registry =\n'
        '\t\t\tLOWER ( USERPRINCIPALNAME () ) IN { "first@example.invalid" }\n'
    )
    assert tool.registry_permission() == tool.DENY_RULE


def test_registry_audience_preserves_user_edited_page_and_unknown_roles(tmp_path):
    tool, _ = report_fixture(tmp_path)
    for path, contents in tool.plan_changes(tmp_path).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    page_path = tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "page.json"
    page_path.write_text(page_path.read_text(encoding="utf-8").replace('"width": 1960', '"width": 2000'), encoding="utf-8")
    with pytest.raises(RuntimeError, match="user edits"):
        tool.plan_changes(tmp_path, ["first@example.invalid"])
    role_path = tmp_path / tool.MODEL / "roles/Other Role.tmdl"
    role_path.write_text("role 'Other Role'\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unrecognised RLS roles"):
        tool.plan_changes(tmp_path, ["first@example.invalid"])


def test_access_only_preserves_edited_import_and_page_layout(tmp_path):
    tool, _ = report_fixture(tmp_path)
    for path, contents in tool.plan_changes(tmp_path).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    table_path = tmp_path / tool.MODEL / "tables/rpt_provider_registry.tmdl"
    edited_import = table_path.read_text(encoding="utf-8") + "\n\tannotation UserChange = preserve\n"
    table_path.write_text(edited_import, encoding="utf-8")
    page_path = tmp_path / tool.REPORT / "pages" / tool.PAGE_ID / "page.json"
    page = json.loads(page_path.read_text(encoding="utf-8"))
    page["width"] = 2200
    page_path.write_text(tool.encode_json(page), encoding="utf-8")
    users = ["first@example.invalid", "second@example.invalid"]
    planned = tool.plan_changes(tmp_path, users, access_only=True)
    assert table_path not in planned
    assert json.loads(planned[page_path])["width"] == 2200
    assert len(planned) == 3
    for path, contents in planned.items():
        path.write_text(contents, encoding="utf-8")
    assert not tool.plan_changes(tmp_path, users, access_only=True)
    assert table_path.read_text(encoding="utf-8") == edited_import
    with pytest.raises(ValueError, match="explicitly approved"):
        tool.plan_changes(tmp_path, access_only=True)


def group_fixture(tmp_path):
    tool, _ = report_fixture(tmp_path)
    for path, contents in tool.plan_changes(tmp_path, ["first@example.invalid"]).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    model_path = tmp_path / tool.MODEL / "model.tmdl"
    model_path.write_text(model_path.read_text(encoding="utf-8") + "\nref role 'WMPP Dynamic Detail RLS'\n", encoding="utf-8")
    # Synthetic scoped detail predicates; these must exist in BOTH roles.
    reader_path = tmp_path / tool.MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
    reader = reader_path.read_text(encoding="utf-8").replace(
        "\ttablePermission fact_referral = TRUE ()",
        "\ttablePermission fact_referral = 'fact_referral'[scope] = USERPRINCIPALNAME ()\n"
        "\ttablePermission fact_referral_snapshot = 'fact_referral_snapshot'[scope] = USERPRINCIPALNAME ()\n"
        "\ttablePermission fact_provider_kpi_monthly = 'fact_provider_kpi_monthly'[scope] = USERPRINCIPALNAME ()",
    )
    reader_path.write_text(reader, encoding="utf-8")
    return tool


def table_predicates(role):
    role = role.replace("\r\n", "\n")
    return dict(re.findall(r"(?m)^\ttablePermission (\w+)\s*=([^\n]*(?:\n\t{2,}[^\n]*)*)", role))


def test_registry_group_keeps_all_other_scoped_predicates_and_has_no_email_allowlist(tmp_path):
    tool = group_fixture(tmp_path)
    before = {path: path.read_bytes() for path in tmp_path.rglob("*") if path.is_file()}
    planned = tool.plan_group_access(tmp_path, "wmpp_report_users", "wmpp_provider_registry_users")
    reader_path = tmp_path / tool.MODEL / "roles" / (tool.READER_ROLE + ".tmdl")
    registry_path = tmp_path / tool.MODEL / "roles" / (tool.REGISTRY_ROLE + ".tmdl")
    assert set(planned) == {reader_path, registry_path, tmp_path / tool.MODEL / "model.tmdl"}
    reader_filters = table_predicates(planned[reader_path])
    registry_filters = table_predicates(planned[registry_path])
    original_filters = table_predicates(before[reader_path].decode("utf-8"))
    assert reader_filters.pop(tool.TABLE).strip() == "FALSE ()"
    assert registry_filters.pop(tool.TABLE).strip() == "TRUE ()"
    original_filters.pop(tool.TABLE)
    assert reader_filters == registry_filters == original_filters
    assert "first@example.invalid" not in planned[reader_path] + planned[registry_path]
    assert "WMPP_ServiceGroup = wmpp_report_users" in planned[reader_path]
    assert "WMPP_ServiceGroup = wmpp_provider_registry_users" in planned[registry_path]
    # Overlapping membership unions identical detail filters, not an open role.
    assert all(value.strip() != "TRUE ()" for value in registry_filters.values())
    for path, contents in planned.items():
        path.write_text(contents, encoding="utf-8")
    assert not tool.plan_group_access(tmp_path, "wmpp_report_users", "wmpp_provider_registry_users")
    registry_path.write_text(registry_path.read_text(encoding="utf-8").rstrip("\n") + "\n\n", encoding="utf-8")
    assert not tool.plan_group_access(tmp_path, "wmpp_report_users", "wmpp_provider_registry_users")
    for path, contents in before.items():
        if path not in planned:
            assert path.read_bytes() == contents


@pytest.mark.parametrize("report_group,registry_group", [
    ("", "registry"), ("report", "*"), ("report", "report"), ("report", "REPORT"),
    ("report", 'registry\n\ttablePermission fact_referral = TRUE ()'),
])
def test_registry_groups_reject_invalid_or_shared_group_names(tmp_path, report_group, registry_group):
    tool = load_report_tool()
    with pytest.raises(ValueError):
        tool.plan_group_access(tmp_path, report_group, registry_group)


def test_registry_group_refuses_unknown_role_and_security_rule_drift(tmp_path):
    tool = group_fixture(tmp_path)
    unknown_path = tmp_path / tool.MODEL / "roles/Unexpected Role.tmdl"
    unknown_path.write_text("role 'Unexpected Role'\n", encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unrecognised RLS roles"):
        tool.plan_group_access(tmp_path, "report", "registry")
    unknown_path.unlink()
    for path, contents in tool.plan_group_access(tmp_path, "report", "registry").items():
        path.write_text(contents, encoding="utf-8")
    registry_path = tmp_path / tool.MODEL / "roles" / (tool.REGISTRY_ROLE + ".tmdl")
    registry_path.write_text(registry_path.read_text(encoding="utf-8").replace(
        "'fact_referral'[scope] = USERPRINCIPALNAME ()", "TRUE ()"), encoding="utf-8")
    with pytest.raises(RuntimeError, match="role drift"):
        tool.plan_group_access(tmp_path, "report", "registry")


def test_registry_group_refuses_unrecognised_current_contact_predicate(tmp_path):
    tool = group_fixture(tmp_path)
    reader_path = tmp_path / tool.MODEL / "roles" / (tool.READER_ROLE + ".tmdl")
    role = reader_path.read_text(encoding="utf-8").replace(
        tool.registry_permission(["first@example.invalid"]).rstrip("\n"),
        "\ttablePermission rpt_provider_registry = TRUE ()",
    )
    reader_path.write_text(role, encoding="utf-8")
    with pytest.raises(RuntimeError, match="Unknown registry reader predicate"):
        tool.plan_group_access(tmp_path, "report", "registry")
