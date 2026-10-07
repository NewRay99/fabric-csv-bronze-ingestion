"""Add GLD-023's isolated registry import and restricted extract page to saved WIP.

Preview is default. --apply performs backed-up, hash-guarded definition edits.
Never executes Fabric, publishes, grants service access, enables export policies, changes
existing page visuals/bookmarks/relationships or touches the .pbi data cache.
Contacts are denied by default. --registry-user explicitly approves registry
rows for named sign-in identities within the existing role, not a new role.
--report-group / --registry-group prepare two scoped roles for service group
assignment. They do not create Entra groups or assign live role membership.
"""

import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import uuid


PROJECT = Path(__file__).resolve().parents[1] / "reports/WIP/SM WMPP v16 updated WIP"
MODEL = Path("SM_WMPP_v16.SemanticModel/definition")
REPORT = Path("SM_WMPP_v16.Report/definition")
TABLE = "rpt_provider_registry"
NAMESPACE = uuid.UUID("703a7098-cb6e-4bf6-9919-1fca24a6ae19")
PAGE_ID = uuid.uuid5(NAMESPACE, "provider-registry-extract-page").hex[:20]
EXPORT_FIELDS = (
    "Provider ID", "Home ID", "Provider Name", "Town/City", "Postcode", "Framework Code",
    "Placement Type", "Home Name", "Service Type", "Provider Email", "Provider Phone",
    "Responsible Individual Name", "Responsible Individual Contact Number",
    "Responsible Individual Email Address", "Registrant Name", "Registrant Role",
    "Registrant Email", "Registrant Contact Number", "Provider Status", "County",
    "Country", "Source Export Date",
    "Home Status", "Home Address Line 1",
    "Home Address Line 2", "Home Town/City",
    "Home County", "Home Postcode",
    "Home Country", "Home Phone",
    "Home Email", "Home Registered Beds",
    "Home Spot", "Home Source Export Date",
    "Metrics As Of Date", "Provider Offers",
    "Provider Draft Offers", "Provider Accepted Offers",
    "Provider Rejected Offers", "Provider Offers With Distance",
    "Provider Average Offer Distance km", "Provider IPAs",
    "Provider Active IPAs", "Provider Provider Signed IPAs",
    "Provider Completed IPAs", "Provider Signature Flag",
    "Provider Both Signed Flag", "Provider Estimated Active Weekly Cost",
    "Provider Active IPAs Missing Weekly Cost", "Provider Estimated Lifetime Cost To Date",
    "Provider IPAs Missing Lifetime Cost", "Home Offers",
    "Home Draft Offers", "Home Accepted Offers",
    "Home Rejected Offers", "Home Offers With Distance",
    "Home Average Offer Distance km", "Home IPAs",
    "Home Active IPAs", "Home Provider Signed IPAs",
    "Home Completed IPAs", "Home Signature Flag",
    "Home Both Signed Flag", "Home Estimated Active Weekly Cost",
    "Home Active IPAs Missing Weekly Cost", "Home Estimated Lifetime Cost To Date",
    "Home IPAs Missing Lifetime Cost", "Provider Assignments",
    "Provider Declined Assignments", "Provider Timed Responses",
    "Provider Average Response Minutes", "Provider Messages",
)
REGISTRY_SUBTITLE = (
    "Fostering providers left-joined to homes; providers without homes retained. "
    "One row per Provider ID / Home ID. Provider-wide totals repeat across homes: do not sum them."
)
DENY_RULE = "\ttablePermission rpt_provider_registry = FALSE ()\n"
READER_ROLE = "WMPP Dynamic Detail RLS"
REGISTRY_ROLE = "WMPP Provider Registry RLS"
REGISTRY_ROLE_ID = uuid.uuid5(NAMESPACE, "provider-registry-group-role").hex


def registry_permission(users=None):
    if users is None:
        return DENY_RULE
    identities = sorted({user.strip().lower() for user in users})
    if not identities or any(
        not re.fullmatch(r"[a-z0-9._%+#-]+@[a-z0-9.-]+\.[a-z]{2,}", user)
        for user in identities
    ):
        raise ValueError("Supply at least one valid approved sign-in UPN; no wildcards or DAX")
    values = ", ".join(json.dumps(user) for user in identities)
    return ("\ttablePermission rpt_provider_registry =\n"
            "\t\t\tLOWER ( USERPRINCIPALNAME () ) IN { " + values + " }\n")


def visual_id(name):
    return uuid.uuid5(NAMESPACE, name).hex[:20]


def encode_json(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def literal(value):
    return {"expr": {"Literal": {"Value": value}}}


def color(value):
    return {"solid": {"color": literal("'" + value + "'")}}


def projection(name):
    return {
        "field": {"Column": {"Expression": {"SourceRef": {"Entity": TABLE}}, "Property": name}},
        "queryRef": TABLE + "." + name, "nativeQueryRef": name, "active": True,
    }


def visual(name, kind, x, y, width, height):
    return {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json",
        "name": visual_id(name),
        "position": {"x": x, "y": y, "z": 1000, "width": width, "height": height, "tabOrder": int(y)},
        "visual": {
            "visualType": kind,
            "visualContainerObjects": {
                "title": [{"properties": {"show": literal("false")}}],
                "background": [{"properties": {"show": literal("false")}}],
                "border": [{"properties": {"show": literal("false")}}],
                "dropShadow": [{"properties": {"show": literal("false")}}],
            },
        },
    }


def textbox(name, text, y, height, size=16):
    result = visual(name, "textbox", 36, y, 1888, height)
    result["visual"]["objects"] = {"general": [{"properties": {"paragraphs": [{
        "textRuns": [{"value": text, "textStyle": {
            "fontFamily": "Segoe UI", "fontSize": f"{size}px", "fontWeight": "normal", "color": "#2B2427",
        }}],
    }]}}]}
    return result


def slicer(name, field, x, width):
    result = visual(name, "slicer", x, 234, width, 100)
    result["visual"]["query"] = {"queryState": {"Values": {"projections": [projection(field)]}}}
    result["visual"]["objects"] = {
        "data": [{"properties": {"mode": literal("'Dropdown'")}}],
        "header": [{"properties": {"show": literal("false")}}],
        "selection": [{"properties": {"singleSelect": literal("false"), "selectAllCheckboxEnabled": literal("true")}}],
        "items": [{"properties": {"fontSize": literal("11D"), "fontColor": color("#2B2427")}}],
    }
    result["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": literal("true"), "text": literal("'" + field + "'"),
                                   "fontSize": literal("12D"), "bold": literal("false")}}],
        "background": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "transparency": literal("0D")}}],
        "border": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "radius": literal("12D")}}],
    })
    return result


def registry_table():
    result = visual("registry-export-table", "tableEx", 36, 354, 1888, 598)
    result["visual"]["query"] = {
        "queryState": {"Values": {"projections": [projection(field) for field in EXPORT_FIELDS]}},
        "sortDefinition": {"sort": [{"field": projection("Provider Name")["field"], "direction": "Ascending"}]},
    }
    result["visual"]["objects"] = {
        "columnHeaders": [{"properties": {"fontColor": color("#2B2427"), "backColor": color("#FFFFFF"),
                                            "fontSize": literal("11D"), "bold": literal("false")}}],
        "values": [{"properties": {"fontColor": color("#2B2427"), "backColorPrimary": color("#FFFFFF"),
                                     "backColorSecondary": color("#F8F5F1"), "fontSize": literal("11D")}}],
        "grid": [{"properties": {"gridVertical": literal("false"), "rowPadding": literal("6D")}}],
        "total": [{"properties": {"totals": literal("false")}}],
    }
    result["visual"]["visualContainerObjects"].update({
        "title": [{"properties": {"show": literal("true"), "text": literal("'Provider registry — Fostering'"),
                                   "fontSize": literal("14D"), "bold": literal("false")}}],
        "background": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "transparency": literal("0D")}}],
        "border": [{"properties": {"show": literal("true"), "color": color("#FFFFFF"), "radius": literal("12D")}}],
        "visualHeader": [{"properties": {"show": literal("true")}}],
        "general": [{"properties": {"altText": literal(
            "'Fostering provider registry with all contact columns. Use the horizontal scrollbar for remaining fields. Export summarized data from this table only when authorized.'"
        )}}],
    })
    return result


def page_definitions(approved=False):
    access_note = (
        "Restricted provider contacts. Only approved viewer identities can see registry rows. "
        "Export remains disabled until the administrator enables the approved export policy."
        if approved else
        "Contact extract for report owners pending audience approval. The existing reader role returns no registry rows. This page is hidden in reading view; hiding is not a security control."
    )
    documents = [
        textbox("registry-title", "Provider Registry Extract", 32, 48, 28),
        textbox("registry-subtitle", REGISTRY_SUBTITLE, 92, 36),
        textbox("registry-access-note", access_note, 144, 60),
        slicer("registry-provider-filter", "Provider Name", 36, 928),
        slicer("registry-status-filter", "Provider Status", 984, 450),
        slicer("registry-town-filter", "Town/City", 1454, 470),
        registry_table(),
        textbox("registry-export-help", "Filter this page, then use the table menu (…) → Export data → Summarized data. Scroll sideways to view all fields. Framework Code retains every distinct Fostering membership.", 968, 30, 14),
    ]
    table_id = visual_id("registry-export-table")
    page = {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json",
        "name": PAGE_ID, "displayName": "Provider Registry Extract", "displayOption": "FitToWidth",
        "width": 1960, "height": 1020, "visibility": "HiddenInViewMode",
        "objects": {"background": [{"properties": {"color": color("#F8F5F1"), "transparency": literal("0D")}}]},
        "visualInteractions": [{"source": visual_id(key), "target": table_id, "type": "DataFilter"} for key in (
            "registry-provider-filter", "registry-status-filter", "registry-town-filter",
        )],
    }
    if approved:
        # Page navigation is shared. RLS protects the rows, not the page tab.
        page.pop("visibility")
    result = {REPORT / "pages" / PAGE_ID / "page.json": encode_json(page)}
    for document in documents:
        result[REPORT / "pages" / PAGE_ID / "visuals" / document["name"] / "visual.json"] = encode_json(document)
    return result


def plan_changes(project, registry_users=None, access_only=False):
    planned = {}
    permission_rule = registry_permission(registry_users)
    if access_only and registry_users is None:
        raise ValueError("Access-only changes require explicitly approved --registry-user accounts")

    def read(relative):
        return (project / relative).read_text(encoding="utf-8-sig")

    def put(relative, contents, new_only=False):
        path = project / relative
        if path.exists() and read(relative) == contents:
            return
        if path.exists() and new_only:
            raise RuntimeError(f"Registry definition has user edits; preserve it: {relative}")
        planned[path] = contents

    # A separate, unrelated contact table cannot silently inherit referral RLS.
    # Protect its rows explicitly, without granting anyone a new model role.
    role_files = list((project / MODEL / "roles").glob("*.tmdl"))
    role_path = MODEL / "roles/WMPP Dynamic Detail RLS.tmdl"
    if {p.name for p in role_files} != {role_path.name}:
        raise RuntimeError("Unrecognised RLS roles: review each role's registry access before adding contacts")
    role = read(role_path)
    permission = re.search(r"\ttablePermission rpt_provider_registry\s*=([^\n]*(?:\n\t{2,}[^\n]*)*)", role)
    if permission:
        if permission.group(0) == permission_rule.rstrip("\n"):
            pass
        elif registry_users is not None and permission.group(1).strip() == "FALSE ()":
            role = role[:permission.start()] + permission_rule.rstrip("\n") + role[permission.end():]
            put(role_path, role)
        else:
            raise RuntimeError("Existing registry access rule needs an explicit audience decision; do not overwrite")
    else:
        marker = "\tannotation PBI_Id = "
        if role.count(marker) != 1:
            raise RuntimeError("Unexpected role format; no edits made")
        role = role.replace(marker, permission_rule + "\n" + marker, 1)
        put(role_path, role)

    if access_only:
        # A saved import/table can have legitimate Desktop edits. Do not revisit
        # it, the model metadata, table visuals or any other page for access edits.
        page_path = REPORT / "pages" / PAGE_ID / "page.json"
        note_path = page_path.parent / "visuals" / visual_id("registry-access-note") / "visual.json"
        if not (project / MODEL / "tables/rpt_provider_registry.tmdl").is_file():
            raise RuntimeError("Install the registry import before configuring its audience")
        page = json.loads(read(page_path))
        if page.get("name") != PAGE_ID:
            raise RuntimeError("Unrecognised registry page; no access edits made")
        page.pop("visibility", None)
        put(page_path, encode_json(page))
        note = json.loads(read(note_path))
        run = note["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
        previous = json.loads(page_definitions()[note_path])
        approved = json.loads(page_definitions(approved=True)[note_path])
        previous_text = previous["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"]
        approved_text = approved["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"]
        if run["value"] not in {previous_text, approved_text}:
            raise RuntimeError("Registry access note has user edits; preserve it")
        run["value"] = approved_text
        put(note_path, encode_json(note))
        return planned

    template = Path(__file__).with_name("templates") / "provider_registry.tmdl"
    put(MODEL / "tables/rpt_provider_registry.tmdl", template.read_text(encoding="utf-8"), new_only=True)
    model = read(MODEL / "model.tmdl")
    if "ref table rpt_provider_registry\n" not in model:
        model += "\nref table rpt_provider_registry\n"
    order_pattern = r"(?m)^annotation PBI_QueryOrder = (\[.*\])$"
    match = re.search(order_pattern, model)
    if not match:
        raise RuntimeError("Missing model query order; no edits made")
    order = json.loads(match.group(1))
    if TABLE not in order:
        order.append(TABLE)
        model = model[:match.start(1)] + json.dumps(order, ensure_ascii=False, separators=(",", ":")) + model[match.end(1):]
    put(MODEL / "model.tmdl", model)

    metadata_path = REPORT / "pages/pages.json"
    metadata = json.loads(read(metadata_path))
    if PAGE_ID not in metadata["pageOrder"]:
        metadata["pageOrder"].append(PAGE_ID)
        put(metadata_path, encode_json(metadata))
    original_page = page_definitions()
    for relative, contents in page_definitions(approved=registry_users is not None).items():
        path = project / relative
        # Upgrade only our unchanged, deny-by-default page. Preserve user edits.
        known_original = registry_users is not None and path.exists() and read(relative) == original_page[relative]
        put(relative, contents, new_only=not known_original)
    return planned


def plan_group_access(project, report_group, registry_group):
    """Only the registry predicate differs between these roles' table filters.

    Group names in annotations are handover metadata, not membership checks.
    Service RLS membership is authoritative and must be configured separately.
    """
    groups = [group.strip() for group in (report_group, registry_group)]
    if any(not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_. -]{0,127}", group) for group in groups):
        raise ValueError("Supply valid, explicitly approved security-group names")
    if groups[0].lower() == groups[1].lower():
        raise ValueError("Report and registry groups must be different")
    report_group, registry_group = groups
    reader_path = project / MODEL / "roles" / (READER_ROLE + ".tmdl")
    registry_path = project / MODEL / "roles" / (REGISTRY_ROLE + ".tmdl")
    known_roles = {reader_path.name, registry_path.name}
    present_roles = {path.name for path in reader_path.parent.glob("*.tmdl")}
    if reader_path.name not in present_roles or not present_roles <= known_roles:
        raise RuntimeError("Unrecognised RLS roles: review all role permissions before group access")
    if not (project / MODEL / "tables/rpt_provider_registry.tmdl").is_file():
        raise RuntimeError("Install the registry import before configuring its groups")
    reader = reader_path.read_text(encoding="utf-8-sig")
    if not reader.startswith("role '" + READER_ROLE + "'\n") or "\tmodelPermission: read\n" not in reader:
        raise RuntimeError("Unexpected reader role definition; preserve it")
    permissions = list(re.finditer(
        r"(?m)^\ttablePermission rpt_provider_registry\s*=([^\n]*(?:\n\t{2,}[^\n]*)*)", reader,
    ))
    if len(permissions) != 1:
        raise RuntimeError("Expected one explicit registry reader predicate")
    permission = permissions[0]
    existing = permission.group(0)
    if existing != DENY_RULE.rstrip("\n"):
        old_users = re.fullmatch(r"\s*LOWER \( USERPRINCIPALNAME \(\) \) IN \{ (.*) \}", permission.group(1))
        if old_users is None:
            raise RuntimeError("Unknown registry reader predicate; preserve it for review")
        users = json.loads("[" + old_users.group(1) + "]")
        if existing != registry_permission(users).rstrip("\n"):
            raise RuntimeError("Unknown registry identity expression; preserve it for review")
    reader = reader[:permission.start()] + DENY_RULE.rstrip("\n") + reader[permission.end():]
    group_marker = "\tannotation WMPP_ServiceGroup = "
    group_annotations = re.findall(r"(?m)^\tannotation WMPP_ServiceGroup = ([^\n]+)$", reader)
    if group_annotations and group_annotations != [report_group]:
        raise RuntimeError("Existing report-group annotation differs; explicit review required")
    id_marker = "\tannotation PBI_Id = "
    if reader.count(id_marker) != 1:
        raise RuntimeError("Unexpected reader role identifier; preserve it")
    if not group_annotations:
        reader = reader.replace(id_marker, group_marker + report_group + "\n\n" + id_marker, 1)
    # Never add a registry-only role with no filters on the other tables: role
    # permissions are additive. Copy every existing scoped table predicate.
    registry = reader.replace("role '" + READER_ROLE + "'", "role '" + REGISTRY_ROLE + "'", 1)
    registry = registry.replace(DENY_RULE, "\ttablePermission rpt_provider_registry = TRUE ()\n", 1)
    registry = registry.replace(group_marker + report_group, group_marker + registry_group, 1)
    registry = re.sub(r"(?m)^\tannotation PBI_Id = [^\n]+$", id_marker + REGISTRY_ROLE_ID, registry)
    if registry_path.exists() and registry_path.read_text(encoding="utf-8-sig").rstrip("\n") != registry.rstrip("\n"):
        raise RuntimeError("Registry group role differs from current scoped rules; review role drift")
    model_path = project / MODEL / "model.tmdl"
    model = model_path.read_text(encoding="utf-8-sig")
    reader_ref = "ref role '" + READER_ROLE + "'"
    registry_ref = "ref role '" + REGISTRY_ROLE + "'"
    if model.count(reader_ref) != 1 or model.count(registry_ref) > 1:
        raise RuntimeError("Unexpected model role references; preserve them")
    if registry_ref not in model:
        model = model.replace(reader_ref, reader_ref + "\n\n" + registry_ref, 1)
    return {path: contents for path, contents in (
        (reader_path, reader), (registry_path, registry), (model_path, model),
    ) if not path.exists() or path.read_text(encoding="utf-8-sig").rstrip("\n") != contents.rstrip("\n")}


def plan_registry_expansion(project):
    """Only add registry fields; preserve connection, lineage, layout and access."""
    template = (Path(__file__).parent / "templates/provider_registry.tmdl").read_text(encoding="utf-8")
    model_path = project / MODEL / "tables/rpt_provider_registry.tmdl"
    contents = model_path.read_text(encoding="utf-8-sig")
    if contents.count("\tpartition rpt_provider_registry = m") != 1:
        raise RuntimeError("Unexpected registry partition; preserve the user-edited import")
    blocks = re.findall(r"(?ms)^\tcolumn [^\n]+\n.*?(?=^\tcolumn |^\tpartition |\Z)", template)
    existing = set(re.findall(r"sourceColumn: (\w+)", contents))
    if len(existing) != len(re.findall(r"sourceColumn:", contents)):
        raise RuntimeError("Duplicate registry source columns; preserve the user-edited import")
    additions = []
    sources = []
    for block in blocks:
        source = re.search(r"sourceColumn: (\w+)", block).group(1)
        if source not in existing:
            name = block.splitlines()[0].removeprefix("\tcolumn ").strip("'")
            if re.search(r"(?m)^\tcolumn '?" + re.escape(name) + r"'?\s*$", contents):
                raise RuntimeError("Existing registry field name has a different source; preserve it: " + name)
            # Keep all existing user-generated lineage tags; deterministic tags
            # apply only to additions and survive repeated/recovered upgrades.
            tag = str(uuid.uuid5(NAMESPACE, "registry-column:" + source))
            block = block.replace("\t\tsummarizeBy:", "\t\tlineageTag: " + tag + "\n\t\tsummarizeBy:", 1)
            additions.append(block)
            sources.append(source)
    if additions:
        selection = re.search(r"Selected = Table.SelectColumns\(Registry, \{(.*?)\}\)", contents, re.S)
        if not selection or len(re.findall(r"Selected = Table.SelectColumns", contents)) != 1:
            raise RuntimeError("Unexpected registry column selection; preserve the user-edited import")
        selected = re.findall(r'"(\w+)"', selection.group(1))
        if set(selected) != existing or len(selected) != len(existing):
            raise RuntimeError("Registry import selection differs from declared columns; preserve it")
        if re.sub(r'"\w+"|[\s,]', "", selection.group(1)):
            raise RuntimeError("Registry selection has custom expressions; preserve them")
        extra = ",\n" + "\n".join("\t\t\t\t        \"" + source + "\"" + ("," if index < len(sources) - 1 else "")
                                     for index, source in enumerate(sources))
        updated = selection.group(1).rstrip() + extra + "\n\t\t\t\t    "
        contents = contents[:selection.start(1)] + updated + contents[selection.end(1):]
        contents = contents.replace("\tpartition rpt_provider_registry = m", "".join(additions) + "\tpartition rpt_provider_registry = m", 1)

    table_path = project / REPORT / "pages" / PAGE_ID / "visuals" / visual_id("registry-export-table") / "visual.json"
    table = json.loads(table_path.read_text(encoding="utf-8-sig"))
    if table["visual"]["visualType"] != "tableEx":
        raise RuntimeError("Registry export is no longer a native table; preserve user edits")
    projections = table["visual"]["query"]["queryState"]["Values"]["projections"]
    fields = []
    for item in projections:
        column = item.get("field", {}).get("Column", {})
        if column.get("Expression", {}).get("SourceRef", {}).get("Entity") != TABLE:
            raise RuntimeError("Registry table has a custom/aggregated field; preserve it")
        fields.append(column["Property"])
    if len(fields) != len(set(fields)):
        raise RuntimeError("Registry table contains duplicate fields; preserve it")
    for name in EXPORT_FIELDS:
        if name not in fields:
            if name == "Home ID":
                projections.insert(fields.index("Provider ID") + 1, projection(name))
                fields.insert(fields.index("Provider ID") + 1, name)
            else:
                projections.append(projection(name))
                fields.append(name)
    subtitle_path = project / REPORT / "pages" / PAGE_ID / "visuals" / visual_id("registry-subtitle") / "visual.json"
    subtitle = subtitle_path.read_text(encoding="utf-8-sig")
    old = "Fostering providers with framework membership, including providers without offers. One row per Provider ID."
    subtitle = subtitle.replace(old, REGISTRY_SUBTITLE)
    # Only query projections and the known subtitle change. No role, report
    # setting, page coordinate, table style or user connection is replaced.
    return {path: value for path, value in (
        (model_path, contents), (table_path, encode_json(table)), (subtitle_path, subtitle),
    ) if path.read_text(encoding="utf-8-sig") != value}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--access-only", action="store_true",
                        help="Configure an installed registry without revisiting its import or table visuals.")
    parser.add_argument("--expand-registry", action="store_true",
                        help="Add home keys and metrics without replacing existing import, layout or security.")
    parser.add_argument("--registry-user", action="append", default=None, metavar="UPN",
                        help="Explicitly approved registry viewer; repeat for each account. Does not enable export.")
    parser.add_argument("--report-group", metavar="GROUP",
                        help="Ordinary report-reader service group; requires --registry-group and --access-only.")
    parser.add_argument("--registry-group", metavar="GROUP",
                        help="Registry viewer/export service group; membership and exports remain unconfigured.")
    args = parser.parse_args()
    project = PROJECT.resolve(strict=True)
    if args.expand_registry and (args.access_only or args.registry_user or args.report_group or args.registry_group):
        parser.error("Registry expansion is independent of access changes; use --expand-registry alone")
    if args.report_group or args.registry_group:
        if not args.access_only or args.registry_user is not None or not (args.report_group and args.registry_group):
            parser.error("Group access requires both group names and --access-only, without --registry-user")

    def plan():
        if args.expand_registry:
            return plan_registry_expansion(project)
        if args.report_group:
            return plan_group_access(project, args.report_group, args.registry_group)
        return plan_changes(project, args.registry_user, args.access_only)

    planned = plan()
    result = {"project": str(project), "files": [str(p.relative_to(project)) for p in planned], "apply": args.apply}
    if args.apply and planned:
        original = {p: digest(p) for p in project.rglob("*") if p.is_file() and ".pbi" not in p.relative_to(project).parts}
        backup = project.parent / "_review" / ("gld023-registry-" + datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:8])
        backup.mkdir(parents=True)
        for path in planned:
            if path in original:
                destination = backup / path.relative_to(project)
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, destination)
                if digest(destination) != original[path]:
                    raise RuntimeError("Concurrent save during backup; no report writes attempted")
        for path, expected in original.items():
            if digest(path) != expected:
                raise RuntimeError("Concurrent save before apply; no report writes attempted")
        manifest = {**result, "before_sha256": {str(p.relative_to(project)): original.get(p) for p in planned}}
        manifest_path = backup / "registry-manifest.json"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        for path, contents in planned.items():
            if path.exists() and digest(path) != original.get(path):
                raise RuntimeError(f"Concurrent edit; preserve it: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")
        for path, expected in original.items():
            if path not in planned and digest(path) != expected:
                raise RuntimeError(f"Unrelated file changed during apply: {path}")
        if plan():
            raise RuntimeError("Apply did not produce an idempotent result")
        manifest["verified"] = "All unlisted model/report file hashes unchanged, excluding .pbi cache"
        manifest_path.write_text(encode_json(manifest), encoding="utf-8")
        result.update({"backup": str(backup), "verified": manifest["verified"]})
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
