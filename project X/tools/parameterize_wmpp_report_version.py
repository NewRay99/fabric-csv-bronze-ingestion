"""Bind every existing WIP version footer to one Power Query text parameter.

Preview is read-only. Apply through the normal patch tool, retaining a backup.
No running Power BI model, external data source, relationship or RLS changes.
"""

import argparse
from copy import deepcopy
import json
import re
import shutil
import uuid

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import group_wmpp_referral_mobile_filters as preservation
import plan_wmpp_mobile_layout as original

MODEL = original.PROJECT / "SM_WMPP_v16.SemanticModel/definition"
BACKUP = original.ROOT / "reports/_review/report-version-parameter-before-20261015"
DELIVERY = original.PROJECT / "REPORT_VERSION_PARAMETER_DELIVERY.json"
PARAMETER = "ReportVersion"
TABLE = "Report Settings"
MEASURE = "Report Version Label"
VALUE_ID = "ReportVersionLabel"
OLD_LABEL = "Version: 0.16"
UPDATE_INSTRUCTIONS = (
    "Power BI Desktop: Home > Transform data > Manage Parameters > ReportVersion. "
    "Change Current Value (text), then Close & Apply. Refresh Report Settings if "
    "prompted; publish the updated report/model for service users."
)


def lineage(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "wmpp:report-version:" + name))


def parameter_definition():
    return f'''/// Display version used by every report version footer. Edit in Manage Parameters.
expression {PARAMETER} = "0.16" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
\tlineageTag: {lineage("parameter")}

\tannotation PBI_ResultType = Text
'''


def table_definition():
    return f'''/// Local one-row report metadata; disconnected from all business and security tables.
table '{TABLE}'
\tlineageTag: {lineage("table")}

\t/// Shared footer label. Its version comes only from the Power Query parameter.
\tmeasure '{MEASURE}' =
\t\t\tVAR versionText =
\t\t\t    CALCULATE (
\t\t\t        SELECTEDVALUE ( '{TABLE}'[{PARAMETER}] ),
\t\t\t        REMOVEFILTERS ( '{TABLE}' )
\t\t\t    )
\t\t\tRETURN IF ( NOT ISBLANK ( versionText ), "Version: " & versionText )
\t\tdisplayFolder: Report information
\t\tlineageTag: {lineage("measure")}

\tcolumn {PARAMETER}
\t\tdataType: string
\t\tisHidden
\t\tlineageTag: {lineage("column")}
\t\tsummarizeBy: none
\t\tsourceColumn: {PARAMETER}

\tpartition '{TABLE}' = m
\t\tmode: import
\t\tsource =
\t\t\t\tlet
\t\t\t\t    VersionText = Text.Trim({PARAMETER}),
\t\t\t\t    ValidatedVersion = if Text.Length(VersionText) = 0
\t\t\t\t        then error "ReportVersion must not be blank."
\t\t\t\t        else VersionText
\t\t\t\tin
\t\t\t\t    #table(type table [{PARAMETER} = text], {{{{ValidatedVersion}}}})

\tannotation PBI_NavigationStepName = Navigation

\tannotation PBI_ResultType = Table
'''


def dynamic_reference():
    return {"propertyIdentifier": {"objectName": "values", "propertyName": "expr"},
            "selector": {"id": VALUE_ID}}


def settings_definition_matches(text):
    # Desktop can append a blank line when saving TMDL. Do not mistake that
    # serialization-only change for a changed query or measure definition.
    return text.rstrip() == table_definition().rstrip()


def measure_expression():
    return {"Measure": {"Expression": {"SourceRef": {"Entity": TABLE}}, "Property": MEASURE}}


def replace_label(source):
    """Change the text payload only; preserve the textbox, geometry and all styles."""
    result = deepcopy(source)
    assert original.vtype(source) == "textbox"
    objects = result["visual"]["objects"]
    assert "values" not in objects, "Inspect existing dynamic values before extending."
    replaced = 0
    for entry in objects["general"]:
        for paragraph in entry["properties"]["paragraphs"]:
            for run in paragraph["textRuns"]:
                if run["value"] == OLD_LABEL:
                    run["value"] = dynamic_reference()
                    replaced += 1
    assert replaced == 1, "Expected exactly one existing version label."
    objects["values"] = [{"properties": {"expr": {"expr": measure_expression()}},
                          "selector": {"id": VALUE_ID}}]
    return result


def extend_model(model):
    assert f"ref table '{TABLE}'" not in model
    match = re.search(r"(?m)^annotation PBI_QueryOrder = (.+)$", model)
    assert match
    order = json.loads(match.group(1))
    assert PARAMETER not in order and TABLE not in order
    order += [PARAMETER, TABLE]
    model = model[:match.start(1)] + json.dumps(order, separators=(",", ":")) + model[match.end(1):]
    # Preserve all existing references and their ordering.
    marker = "ref role 'WMPP Dynamic Detail RLS'"
    assert model.count(marker) == 1
    return model.replace(marker, f"ref table '{TABLE}'\n\n" + marker)


def plan():
    assert not DELIVERY.exists(), "Already parameterized; use --verify."
    expression_path, model_path = MODEL / "expressions.tmdl", MODEL / "model.tmdl"
    expressions = expression_path.read_text(encoding="utf-8-sig")
    assert not re.search(r"(?m)^expression ReportVersion\s*=", expressions)
    assert not (MODEL / "tables" / (TABLE + ".tmdl")).exists()
    updates = {expression_path: expressions.rstrip() + "\n\n" + parameter_definition(),
               model_path: extend_model(model_path.read_text(encoding="utf-8-sig")),
               MODEL / "tables" / (TABLE + ".tmdl"): table_definition()}
    labels = []
    for path in sorted(original.REPORT.glob("pages/*/visuals/*/visual.json")):
        value = original.read(path)
        if OLD_LABEL not in original.plain(value): continue
        updated = replace_label(value)
        assert updated["position"] == value["position"]
        updates[path] = updated
        labels.append({"page": path.parents[2].name,
            "page_name": original.read(path.parents[2] / "page.json")["displayName"],
            "visual": value["name"], "file": str(path.relative_to(original.PROJECT))})
    assert len(labels) == 14, "Inspect changed version-label inventory before applying."
    return updates, {"date": "2026-10-15", "parameter": PARAMETER, "initial_value": "0.16",
        "table": TABLE, "measure": MEASURE, "labels": labels, "backup": str(BACKUP),
        "update_instructions": UPDATE_INSTRUCTIONS, "refresh_required": True,
        "native_render_and_refresh_verified": False}


def verify(delivery, updates=None):
    updates = updates or {}
    def read(path): return updates[path] if path in updates else original.read(path)
    def source_text(path): return updates[path] if path in updates else path.read_text(encoding="utf-8-sig")
    assert "IsParameterQuery=true" in source_text(MODEL / "expressions.tmdl")
    assert source_text(MODEL / "expressions.tmdl").count("expression ReportVersion =") == 1
    assert f"ref table '{TABLE}'" in source_text(MODEL / "model.tmdl")
    assert settings_definition_matches(source_text(MODEL / "tables" / (TABLE + ".tmdl")))
    expected = {v["visual"] for v in delivery["labels"]}
    actual = set()
    for path in original.REPORT.glob("pages/*/visuals/*/visual.json"):
        value = read(path)
        assert OLD_LABEL not in original.plain(value), "Static version label remains."
        values = value.get("visual", {}).get("objects", {}).get("values", [])
        bound = [v for v in values if v.get("selector") == {"id": VALUE_ID}]
        if not bound: continue
        assert len(bound) == 1 and bound[0]["properties"]["expr"]["expr"] == measure_expression()
        refs = [run["value"] for entry in value["visual"]["objects"]["general"]
                for para in entry["properties"]["paragraphs"] for run in para["textRuns"]]
        assert refs.count(dynamic_reference()) == 1
        actual.add(value["name"])
        if not updates:
            before = original.read(BACKUP / path.relative_to(original.PROJECT))
            assert value == replace_label(before), "Unexpected visual/style/layout change."
    assert actual == expected and len(actual) == 14
    return {"labels_bound_to_one_parameter": len(actual), "static_version_labels_remaining": 0,
        "textbox_type_layout_and_formatting_preserved": True, "text_parameter": True,
        "refresh_required": True, "native_render_and_refresh_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(original.read(DELIVERY))))
        return
    updates, delivery = plan()
    checks = verify(delivery, updates)
    schema = home.published_schema_check({p: v for p, v in updates.items() if p.suffix == ".json"}) if args.validate else {}
    print(json.dumps({"files": len(updates), "checks": checks, "schema": schema}), flush=True)
    if not args.apply_via: return
    assert not BACKUP.exists(), "Inspect backup before repeating."
    baseline = preservation.preserved(set(updates))
    before = {p: p.read_bytes() for p in updates if p.exists()}
    BACKUP.mkdir(parents=True)
    for path in list(before) + [compact.MANIFEST]:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert preservation.preserved(set(updates)) == baseline
    for path, value in updates.items():
        if path in before: assert path.read_bytes() == before[path], "Report changed during edit."
        path.parent.mkdir(parents=True, exist_ok=True)
        compact.patch_file(path, value, args.apply_via)
    assert preservation.preserved(set(updates)) == baseline, "Unrelated report/model/resources changed."
    checks = verify(delivery)
    compact.patch_file(DELIVERY, {**delivery, "checks": checks, "schema": schema,
        "unrelated_definitions_mobile_layouts_and_assets_preserved": True}, args.apply_via)
    manifest = original.read(compact.MANIFEST)
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-15",
        "reason": "One ReportVersion text parameter, local settings table/measure and 14 existing footer bindings; geometry unchanged.",
        "files": [str(p.relative_to(original.PROJECT)) for p in updates]})
    compact.patch_file(compact.MANIFEST, manifest, args.apply_via)
    print(json.dumps({"saved": checks, "backup": str(BACKUP),
        "unrelated_definitions_mobile_layouts_and_assets_preserved": True}), flush=True)


if __name__ == "__main__": main()
