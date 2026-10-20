"""Reconcile the 20 September 2026 client PBIP export with repo-owned Gold changes.

The source ZIP remains immutable. Run this tool against the version-controlled
``reports/current/SM WMPP v16 updated`` copy after refreshing that copy from the
client export. It removes generated auto-date artifacts, applies the governed
relationship design, installs current measures, adds Gold/RLS tables and repairs
known stale report bindings.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
DEFAULT_ROOT = PROJECT / "reports" / "current" / "SM WMPP v16 updated"
SERVER = (
    "m7hju2pe2lguxmyd2k56fon36e-qo2p37tm2lmuxgspbra4y6dhoa."
    "datawarehouse.fabric.microsoft.com"
)
DATABASE = "LH_BCT_WMPP"


def strip_variations(text: str) -> str:
    """Remove auto-date variation blocks from a table declaration."""
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.lstrip().startswith("variation Variation"):
            base_indent = len(line) - len(line.lstrip())
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip():
                    index += 1
                    continue
                indent = len(candidate) - len(candidate.lstrip())
                if indent <= base_indent:
                    break
                index += 1
            continue
        output.append(line)
        index += 1
    return "".join(output)


def column_block(name: str, data_type: str, *, hidden: bool = False) -> str:
    properties = [f"\tcolumn {name}", f"\t\tdataType: {data_type}"]
    if data_type == "dateTime":
        properties.append("\t\tformatString: General Date")
    if data_type == "boolean":
        properties.append('\t\tformatString: """TRUE"";""TRUE"";""FALSE"""')
    if hidden:
        properties.append("\t\tisHidden")
    properties.extend(("\t\tsummarizeBy: none", f"\t\tsourceColumn: {name}"))
    return "\n".join(properties) + "\n\n"


def add_columns(table_path: Path, columns: list[tuple[str, str, bool]]) -> None:
    text = table_path.read_text(encoding="utf-8-sig")
    additions = []
    for name, data_type, hidden in columns:
        if re.search(rf"^\tcolumn {re.escape(name)}$", text, flags=re.MULTILINE):
            continue
        additions.append(column_block(name, data_type, hidden=hidden))
    if additions:
        marker = "\tpartition "
        position = text.find(marker)
        if position < 0:
            raise ValueError(f"No partition declaration found in {table_path}")
        text = text[:position] + "".join(additions) + text[position:]
        table_path.write_text(text, encoding="utf-8", newline="\n")


def imported_table(
    table_name: str,
    columns: list[tuple[str, str, bool]],
    *,
    hidden: bool = False,
) -> str:
    table_lines = [f"table {table_name}"]
    if hidden:
        table_lines.append("\tisHidden")
    table_lines.append("")
    body = "".join(column_block(*column[:2], hidden=column[2]) for column in columns)
    partition = f"""\tpartition {table_name} = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    Source = Sql.Database(\"{SERVER}\", \"{DATABASE}\"),
\t\t\t\t    GoldTable = Source{{[Schema=\"gold\",Item=\"{table_name}\"]}}[Data]
\t\t\t\tin
\t\t\t\t    GoldTable

\tannotation PBI_NavigationStepName = Navigation

\tannotation PBI_ResultType = Table
"""
    return "\n".join(table_lines) + body + partition


NEW_TABLES: dict[str, tuple[bool, list[tuple[str, str, bool]]]] = {
    "dim_snapshot_month": (False, [
        ("month_start", "dateTime", False), ("month_end", "dateTime", False),
        ("calendar_year", "int64", False), ("calendar_month_number", "int64", False),
        ("calendar_month_name", "string", False), ("year_month", "string", False),
        ("export_date", "dateTime", True), ("job_run_id", "string", True),
        ("gold_modelled_at", "dateTime", True),
    ]),
    "bridge_provider_home_framework_category": (False, [
        ("provider_home_category_id", "int64", True),
        ("provider_home_id", "string", False),
        ("framework_category_id", "int64", False),
        ("source_export_date", "dateTime", True), ("export_date", "dateTime", True),
        ("job_run_id", "string", True),
    ]),
    "fact_provider_kpi_monthly": (False, [
        ("provider_id", "string", False), ("assignment_month", "dateTime", False),
        ("security_scope_key", "string", True),
        ("response_opportunity_count", "int64", False),
        ("qualifying_response_count", "int64", False),
        ("offers_submitted_count", "int64", False),
        ("accepted_offer_count", "int64", False),
        ("successful_referral_count", "int64", False),
        ("placed_by_target_count", "int64", False),
        ("average_response_minutes", "double", False),
        ("median_response_minutes", "double", False),
        ("kpi_rule_version", "string", True), ("job_run_id", "string", True),
        ("gold_modelled_at", "dateTime", True),
    ]),
    "fact_referral_global_summary": (True, [
        ("snapshot_month_start", "dateTime", False),
        ("snapshot_month_end", "dateTime", False),
        ("current_status", "string", False),
        ("placement_type_required", "string", False), ("priority", "string", False),
        ("placement_urgency_band", "string", False),
        ("required_placement_date_outcome", "string", False),
        ("referral_count", "int64", False), ("open_referral_count", "int64", False),
        ("closed_referral_count", "int64", False),
        ("awaiting_offer_count", "int64", False),
        ("referrals_with_offer_count", "int64", False),
        ("offer_count", "int64", False),
        ("provider_response_referral_count", "int64", False),
        ("placed_by_required_date_count", "int64", False),
        ("snapshot_rule_version", "string", True), ("job_run_id", "string", True),
        ("gold_modelled_at", "dateTime", True),
    ]),
    "dim_security_scope": (True, [
        ("security_scope_key", "string", True), ("scope_type", "string", True),
        ("scope_code", "string", True), ("scope_name", "string", True),
        ("allows_global_summary", "boolean", True), ("valid_from", "dateTime", True),
        ("valid_to", "dateTime", True), ("approved_by", "string", True),
        ("updated_at", "dateTime", True), ("job_run_id", "string", True),
        ("gold_modelled_at", "dateTime", True),
    ]),
    "sec_user_scope_access": (True, [
        ("user_principal_name", "string", True),
        ("security_scope_key", "string", True), ("valid_from", "dateTime", True),
        ("valid_to", "dateTime", True), ("approved_by", "string", True),
        ("access_reason", "string", True), ("updated_at", "dateTime", True),
        ("job_run_id", "string", True), ("gold_modelled_at", "dateTime", True),
    ]),
    "bridge_referral_scope": (True, [
        ("referral_id", "string", True), ("security_scope_key", "string", True),
        ("valid_from", "dateTime", True), ("valid_to", "dateTime", True),
        ("assigned_by", "string", True), ("assignment_reason", "string", True),
        ("updated_at", "dateTime", True), ("job_run_id", "string", True),
        ("gold_modelled_at", "dateTime", True),
    ]),
}


NEW_RELATIONSHIPS = """
relationship 646434aa-f282-58a0-a37c-0e51d581d9b1
	joinOnDateBehavior: datePartOnly
	fromColumn: fact_referral_snapshot.snapshot_month_start
	toColumn: dim_snapshot_month.month_start

relationship 152ea9d6-37bf-5208-8268-b14137eaee01
	fromColumn: fact_referral.placement_type_required
	toColumn: dim_placement_type.placement_type

relationship 68d7a7f4-8bec-5b5b-ac0c-d95c918f3465
	fromColumn: fact_referral_snapshot.placement_type_required
	toColumn: dim_placement_type.placement_type

relationship 62bfe3d1-0a71-5a79-ac32-83ca68453d5c
	fromColumn: bridge_provider_home_framework_category.provider_home_id
	toColumn: dim_provider_home.provider_home_id

relationship 4bc46202-2630-54ec-8bbd-56a758360e67
	fromColumn: bridge_provider_home_framework_category.framework_category_id
	toColumn: dim_framework_category.framework_category_id

relationship 0ba59342-c67c-56cd-bf11-7ab0541ca52d
	fromColumn: fact_provider_kpi_monthly.provider_id
	toColumn: dim_provider.provider_id

relationship 1db7587c-c61c-50d4-a7ee-bb5104929953
	joinOnDateBehavior: datePartOnly
	fromColumn: fact_provider_kpi_monthly.assignment_month
	toColumn: dim_snapshot_month.month_start

relationship d12e31cc-9515-57bd-aea0-e4fb56035491
	joinOnDateBehavior: datePartOnly
	fromColumn: fact_referral_global_summary.snapshot_month_start
	toColumn: dim_snapshot_month.month_start

relationship 8cde0318-ce19-590f-acbf-e365796889b9
	fromColumn: fact_referral_global_summary.placement_type_required
	toColumn: dim_placement_type.placement_type
""".lstrip()
NEW_RELATIONSHIP_NAMES = set(
    re.findall(r"^relationship (\S+)", NEW_RELATIONSHIPS, flags=re.MULTILINE)
)


ROLE = """role 'WMPP Dynamic Detail RLS'
	modelPermission: read

	tablePermission sec_user_scope_access = ```
			LOWER ( 'sec_user_scope_access'[user_principal_name] )
				= LOWER ( USERPRINCIPALNAME () )
			```

	tablePermission dim_security_scope = ```
			VAR current_upn = LOWER ( USERPRINCIPALNAME () )
			VAR allowed_scopes =
				CALCULATETABLE (
					VALUES ( 'sec_user_scope_access'[security_scope_key] ),
					FILTER (
						ALL ( 'sec_user_scope_access' ),
						LOWER ( 'sec_user_scope_access'[user_principal_name] ) = current_upn
					)
				)
			RETURN 'dim_security_scope'[security_scope_key] IN allowed_scopes
			```

	tablePermission bridge_referral_scope = ```
			VAR current_upn = LOWER ( USERPRINCIPALNAME () )
			VAR allowed_scopes =
				CALCULATETABLE (
					VALUES ( 'sec_user_scope_access'[security_scope_key] ),
					FILTER (
						ALL ( 'sec_user_scope_access' ),
						LOWER ( 'sec_user_scope_access'[user_principal_name] ) = current_upn
					)
				)
			RETURN 'bridge_referral_scope'[security_scope_key] IN allowed_scopes
			```

	tablePermission fact_referral = ```
			VAR current_referral = 'fact_referral'[referral_id]
			VAR current_upn = LOWER ( USERPRINCIPALNAME () )
			VAR allowed_scopes =
				CALCULATETABLE (
					VALUES ( 'sec_user_scope_access'[security_scope_key] ),
					FILTER (
						ALL ( 'sec_user_scope_access' ),
						LOWER ( 'sec_user_scope_access'[user_principal_name] ) = current_upn
					)
				)
			RETURN
				COUNTROWS (
					FILTER (
						ALL ( 'bridge_referral_scope' ),
						'bridge_referral_scope'[referral_id] = current_referral
							&& 'bridge_referral_scope'[security_scope_key] IN allowed_scopes
					)
				) > 0
			```

	tablePermission fact_referral_snapshot = ```
			VAR current_referral = 'fact_referral_snapshot'[referral_id]
			VAR current_upn = LOWER ( USERPRINCIPALNAME () )
			VAR allowed_scopes =
				CALCULATETABLE (
					VALUES ( 'sec_user_scope_access'[security_scope_key] ),
					FILTER (
						ALL ( 'sec_user_scope_access' ),
						LOWER ( 'sec_user_scope_access'[user_principal_name] ) = current_upn
					)
				)
			RETURN
				COUNTROWS (
					FILTER (
						ALL ( 'bridge_referral_scope' ),
						'bridge_referral_scope'[referral_id] = current_referral
							&& 'bridge_referral_scope'[security_scope_key] IN allowed_scopes
					)
				) > 0
			```

	tablePermission fact_provider_kpi_monthly = ```
			VAR current_upn = LOWER ( USERPRINCIPALNAME () )
			VAR allowed_scopes =
				CALCULATETABLE (
					VALUES ( 'sec_user_scope_access'[security_scope_key] ),
					FILTER (
						ALL ( 'sec_user_scope_access' ),
						LOWER ( 'sec_user_scope_access'[user_principal_name] ) = current_upn
					)
				)
			RETURN 'fact_provider_kpi_monthly'[security_scope_key] IN allowed_scopes
			```
"""


def update_model(definition: Path) -> None:
    tables = definition / "tables"
    model_path = definition / "model.tmdl"
    model = model_path.read_text(encoding="utf-8-sig")
    model = model.replace("annotation __PBI_TimeIntelligenceEnabled = 1",
                          "annotation __PBI_TimeIntelligenceEnabled = 0")
    model = re.sub(r"^ref table (?:LocalDateTable_|DateTableTemplate_).+\r?\n", "", model,
                   flags=re.MULTILINE)
    model = re.sub(r"^ref cultureInfo .+\r?\n", "", model, flags=re.MULTILINE)

    query_order_match = re.search(r"annotation PBI_QueryOrder = (\[[^\n]+\])", model)
    if not query_order_match:
        raise ValueError("PBI_QueryOrder annotation not found")
    query_order = json.loads(query_order_match.group(1))
    for table_name in NEW_TABLES:
        if table_name not in query_order:
            query_order.append(table_name)
    if "KPI Selector" not in query_order:
        query_order.append("KPI Selector")
    model = model[:query_order_match.start(1)] + json.dumps(
        query_order, separators=(",", ":")
    ) + model[query_order_match.end(1):]

    for table_name in NEW_TABLES:
        ref = f"ref table {table_name}"
        if ref not in model:
            model = model.rstrip() + f"\n{ref}\n"
    if "ref table 'KPI Selector'" not in model:
        model = model.rstrip() + "\nref table 'KPI Selector'\n"
    role_ref = "ref role 'WMPP Dynamic Detail RLS'"
    if role_ref not in model:
        model = model.rstrip() + f"\n{role_ref}\n"
    model_path.write_text(model, encoding="utf-8", newline="\n")

    for generated in list(tables.glob("LocalDateTable_*.tmdl")) + list(
        tables.glob("DateTableTemplate_*.tmdl")
    ):
        generated.unlink()
    for table_path in tables.glob("*.tmdl"):
        table_text = strip_variations(table_path.read_text(encoding="utf-8-sig"))
        # Keep one predictable storage mode; the two report-generated
        # DirectQuery tables in the client export are small reporting objects
        # and do not justify a composite-model boundary here.
        table_text = table_text.replace("\t\tmode: directQuery", "\t\tmode: import")
        table_path.write_text(
            table_text,
            encoding="utf-8", newline="\n",
        )
    cultures = definition / "cultures"
    if cultures.exists():
        for culture in cultures.glob("*.tmdl"):
            culture.unlink()
        try:
            cultures.rmdir()
        except OSError:
            pass

    add_columns(tables / "fact_referral.tmdl", [
        ("provider_responded_count", "int64", False),
        ("has_provider_response", "boolean", False),
        ("first_provider_response_date", "dateTime", False),
    ])
    add_columns(tables / "fact_referral_snapshot.tmdl", [
        ("snapshot_month_start", "dateTime", False),
        ("snapshot_month_end", "dateTime", False),
        ("snapshot_rule_version", "string", True),
        ("provider_responded_count", "int64", False),
        ("has_provider_response", "boolean", False),
        ("first_provider_response_date", "dateTime", False),
    ])
    add_columns(tables / "fact_referral_provider.tmdl", [
        ("assigned_at", "dateTime", False),
        ("first_offer_response_at", "dateTime", False),
        ("first_reason_response_at", "dateTime", False),
        ("first_qualifying_response_at", "dateTime", False),
        ("has_qualifying_response", "boolean", False),
        ("response_elapsed_minutes", "int64", False),
        ("response_evidence_scope", "string", True),
    ])
    for table_name, (hidden, columns) in NEW_TABLES.items():
        (tables / f"{table_name}.tmdl").write_text(
            imported_table(table_name, columns, hidden=hidden),
            encoding="utf-8", newline="\n",
        )

    relationships_path = definition / "relationships.tmdl"
    relationship_text = relationships_path.read_text(encoding="utf-8-sig")
    blocks = re.split(r"(?=^relationship )", relationship_text, flags=re.MULTILINE)
    kept: list[str] = []
    for block in blocks:
        if not block.strip():
            continue
        relationship_name = re.match(r"relationship (\S+)", block)
        if relationship_name and relationship_name.group(1) in NEW_RELATIONSHIP_NAMES:
            continue
        if "LocalDateTable_" in block or "DateTableTemplate_" in block:
            continue
        if ("fromColumn: fact_referral_snapshot.referral_id" in block
                and "toColumn: fact_referral.referral_id" in block):
            continue
        if ("fromColumn: fact_referral_snapshot.snapshot_date" in block
                and "toColumn: dim_date.date" in block):
            continue
        block = re.sub(r"^\tcrossFilteringBehavior: bothDirections\r?\n", "", block,
                       flags=re.MULTILINE)
        block = re.sub(r"^\tsecurityFilteringBehavior: bothDirections\r?\n", "", block,
                       flags=re.MULTILINE)
        kept.append(block.rstrip() + "\n\n")
    relationships_path.write_text(
        "".join(kept).rstrip() + "\n\n" + NEW_RELATIONSHIPS,
        encoding="utf-8", newline="\n",
    )

    canonical_measures = PROJECT / "reports" / "current" / "_Measures.tmdl"
    (tables / "_Measures.tmdl").write_text(
        canonical_measures.read_text(encoding="utf-8-sig"),
        encoding="utf-8", newline="\n",
    )
    kpi_selector = (
        PROJECT / "reports" / "current" / "WMPP" / "SM_WMPP.SemanticModel"
        / "definition" / "tables" / "KPI Selector.tmdl"
    )
    (tables / "KPI Selector.tmdl").write_text(
        kpi_selector.read_text(encoding="utf-8-sig"),
        encoding="utf-8", newline="\n",
    )
    roles = definition / "roles"
    roles.mkdir(exist_ok=True)
    (roles / "WMPP Dynamic Detail RLS.tmdl").write_text(
        ROLE, encoding="utf-8", newline="\n"
    )


def update_report(report_definition: Path) -> int:
    replacements = {
        '"Entity": "dim_referral"': '"Entity": "dim_placement_type"',
    }
    closure_binding = re.compile(
        r'("Entity":\s*)"(?:Referral Closure Reason Summary_old|'
        r'dim_referral_provider_reject_reason)"'
        r'(\s*\}\s*\},\s*"Property":\s*)'
        r'"(?:Closed Referral Reason Bucket|closed_referral_reason_bucket)"'
    )
    changed = 0
    for json_path in report_definition.rglob("*.json"):
        text = json_path.read_text(encoding="utf-8-sig")
        updated = text
        updated = closure_binding.sub(
            r'\1"fact_referral"\2"referral_closure_reason"', updated
        )
        for old, new in replacements.items():
            updated = updated.replace(old, new)
        if updated != text:
            json.loads(updated)
            json_path.write_text(updated, encoding="utf-8", newline="\n")
            changed += 1
    return changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    model_definition = root / "SM_WMPP_v16.SemanticModel" / "definition"
    report_definition = root / "SM_WMPP_v16.Report" / "definition"
    if not model_definition.is_dir() or not report_definition.is_dir():
        raise FileNotFoundError(f"Expected SM_WMPP_v16 PBIP project below {root}")
    update_model(model_definition)
    changed_report_files = update_report(report_definition)
    print(
        f"Reconciled {root}: {len(NEW_TABLES)} Gold tables, one RLS role, "
        f"{changed_report_files} report JSON files repaired"
    )


if __name__ == "__main__":
    main()
