"""Add a backed-up provider-cohort offer-status selector to the saved WIP.

The selector finds providers, not just offer rows. Other activity remains visible
for those providers; the existing provider/home/stage filters still intersect.
Saved definitions can be checked here, but Desktop DAX/runtime acceptance cannot.
"""

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil

from audit_wmpp_report_journeys import inventory
from build_report_design_delivery import ident, L, obj, project
import improve_wmpp_journeys_scoring as review
import repair_wmpp_explorer_scope as core

TABLE = "Provider Offer Status"
MATCH = "Provider matches offer status"
SELECTOR = ident("provider-explorer:with-offer-status")
MARKER = "PROVIDER_OFFER_STATUS_UPDATE.json"
SEARCH = "6d0540aac7a79d8d171a"
SERVICE = "6d0aebfc69f445ce7a03"
MONTH = ident("journey-review:scoring-period:" + core.PROVIDER)


def status_match():
    # ALLSELECTED restores external selections before testing membership. A row
    # in the offer/message/assignment evidence list must not redefine the whole
    # provider cohort. Reapply the canonical key explicitly after restoration.
    return """VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
VAR limited = ISFILTERED('Provider Offer Status'[Status])
VAR statuses = VALUES('Provider Offer Status'[Status])
VAR homeFilter = CALCULATE(ISFILTERED('dim_provider_home'), ALLSELECTED())
VAR homes = CALCULATETABLE(VALUES('dim_provider_home'[provider_home_id]), ALLSELECTED())
VAR offerEvidence = CALCULATETABLE(
    SUMMARIZE('fact_offer', 'fact_offer'[provider_id], 'fact_offer'[provider_home_id], 'fact_offer'[offer_status]),
    ALLSELECTED())
VAR providerOffers = FILTER(offerEvidence,
    'fact_offer'[provider_id] == providerKey && (NOT homeFilter || 'fact_offer'[provider_home_id] IN homes))
VAR matchingOffers = COUNTROWS(FILTER(providerOffers,
    COALESCE('fact_offer'[offer_status], "(Unknown status)") IN statuses))
RETURN IF(ISBLANK(providerKey), BLANK(),
    IF(NOT limited, 1,
        IF(matchingOffers > 0 || ("(No offers)" IN statuses && COUNTROWS(providerOffers) = 0), 1, BLANK())))"""


def dropdown(template):
    v = deepcopy(template)
    v["name"] = SELECTOR
    v.pop("isHidden", None)
    v.pop("filterConfig", None)
    v.pop("parentGroupName", None)
    v["position"].update(x=852, y=219, width=388, height=110, z=110000, tabOrder=17500)
    v["visual"]["query"] = {
        "queryState": {"Values": {"projections": [dict(project(TABLE, "Status"), active=True)]}}
    }
    v["visual"]["objects"] = {
        "data": obj(mode=L("'Dropdown'")),
        "header": obj(show=L("false")),
        "selection": obj(singleSelect=L("false"), selectAllCheckboxEnabled=L("true")),
    }
    review.title(v, "with Offer Status")
    return v


def get_measure(text, name):
    pattern = (
        r"(?ms)^\tmeasure "
        + re.escape(core.quoted(name))
        + r" =(.*?)(?=^\t\t(?!\t)|^\tmeasure |^\tpartition |\Z)"
    )
    result = re.search(pattern, text)
    if not result:
        raise ValueError(f"Missing existing measure: {name}")
    return "\n".join(line.strip() for line in result[1].strip().splitlines())


def build(bundle):
    model = bundle / "SM_WMPP_v16.SemanticModel/definition"
    root = bundle / "SM_WMPP_v16.Report/definition"
    page_root = root / "pages" / core.PROVIDER
    changes = {}

    def read(path):
        return path.read_text(encoding="utf-8-sig")

    def save(path, doc):
        changes[path] = json.dumps(doc, ensure_ascii=False, indent=2) + "\n"

    changes[model / "tables" / (TABLE + ".tmdl")] = core.calculated_table(
        TABLE,
        [("Status", "string")],
        'DISTINCT(UNION(ROW("Status","(No offers)"), '
        "SELECTCOLUMNS('fact_offer',\"Status\",COALESCE('fact_offer'[offer_status],\"(Unknown status)\"))))",
    )
    path = model / "model.tmdl"
    model_text = read(path)
    if "ref table " + core.quoted(TABLE) in model_text:
        raise ValueError("Status table already registered; review before reapplying")
    changes[path] = model_text.replace(
        "\nref role ", "\nref table " + core.quoted(TABLE) + "\n\nref role ", 1
    )
    if changes[path] == model_text:
        raise ValueError("Expected model table/role reference boundary")

    path = model / "tables" / (core.MT + ".tmdl")
    text = read(path)
    if "measure " + core.quoted(MATCH) + " =" in text:
        raise ValueError("Status measure already exists; review before reapplying")
    block = core.measure_text(core.MT, [(MATCH, status_match(), "0")])
    block = block[block.index("\n\tmeasure ") : block.index("\n\tpartition ")]
    text = text.replace("\n\tpartition ", block + "\n\tpartition ", 1)
    dax = get_measure(text, "Explorer provider row visible")
    old = "(NOT homeFilter || matchingHomes > 0) &&"
    if old not in dax:
        raise ValueError("Provider visibility definition changed; inspect before applying")
    dax = dax.replace(old, old + " [" + MATCH + "] = 1 &&", 1)
    text = core.replace_measure(text, "Explorer provider row visible", dax)
    # A provider can have offers elsewhere but none for the selected home type.
    text = core.replace_measure(
        text,
        "Explorer providers without offers",
        core.scope_provider(
            "COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), CALCULATE([Explorer provider offers]) = 0))"
        )[0],
    )
    changes[path] = text

    # Stage counters describe the same status-selected cohort. The stage selector
    # itself still affects the result list, rather than hiding the other steps.
    path = model / "tables/_Journey Measures.tmdl"
    text = read(path)
    for name in [
        *(f"Journey providers {n}" for n in [0, 1, 2, 3, 5]),
        "Journey providers both signed",
    ]:
        dax = get_measure(text, name)
        old = "NOT ISBLANK('dim_provider'[provider_id]) &&"
        if old not in dax:
            raise ValueError(f"Journey definition changed: {name}")
        dax = dax.replace(old, old + " CALCULATE([" + MATCH + "]) = 1 &&", 1)
        text = core.replace_measure(text, name, dax)
    changes[path] = text

    path = model / "tables/_Report Journey Measures.tmdl"
    text = read(path)
    context = get_measure(text, "Provider selection context")
    context = (
        "VAR message = (\n"
        + context
        + ")\nVAR statuses = VALUES('Provider Offer Status'[Status])\n"
        + "VAR sample = TOPN(3, statuses, 'Provider Offer Status'[Status], ASC)\n"
        + "VAR label = CONCATENATEX(sample, 'Provider Offer Status'[Status], \", \", 'Provider Offer Status'[Status], ASC)\n"
        + 'RETURN message & IF(ISFILTERED(\'Provider Offer Status\'[Status]), " | With offer status: " & label & IF(COUNTROWS(statuses) > 3, " + " & FORMAT(COUNTROWS(statuses) - 3, "0") & " more", ""), "")'
    )
    changes[path] = core.replace_measure(text, "Provider selection context", context)

    # Four equal-width controls on the existing row, with the navigation and
    # journey strip untouched. Keep the full-width provider result list.
    for vid, x in [(SEARCH, 36), (SERVICE, 444), (MONTH, 1260)]:
        path = page_root / "visuals" / vid / "visual.json"
        v = json.loads(read(path))
        v["position"].update(x=x, width=384, y=219)
        save(path, v)
    template = json.loads(read(page_root / "visuals" / SERVICE / "visual.json"))
    selector = dropdown(template)
    selector["position"].update(x=852, width=384)
    save(page_root / "visuals" / SELECTOR / "visual.json", selector)

    path = page_root / "page.json"
    p = json.loads(read(path))
    interactions = p.setdefault("visualInteractions", [])
    for vp in (page_root / "visuals").glob("*/visual.json"):
        v = json.loads(read(vp))
        if not v.get("visual", {}).get("query"):
            continue
        if v["visual"]["visualType"] in {"slicer", "textFilter25A4896A83E0487089E2B90C9AE57C8A"}:
            continue
        if v["name"] == "cfe6facac7ed85d46c46":  # Refresh timestamp, not cohort data.
            continue
        interactions.append({"source": SELECTOR, "target": v["name"], "type": "DataFilter"})
    save(path, p)

    # Existing navigation/filter bookmarks suppress data; stage bookmarks target
    # only the hidden stage selector. Do not let a new control become a target.
    for bp in (root / "bookmarks").glob("*.bookmark.json"):
        b = json.loads(read(bp))
        if core.PROVIDER not in b.get("explorationState", {}).get("sections", {}):
            continue
        options = b.get("options", {})
        if not options.get("suppressData") and not options.get("applyOnlyToTargetVisuals"):
            raise ValueError(f"Unscoped data bookmark could reset status selection: {bp.name}")

    path = root / "pages/5d4291498d7574ae92b3/visuals/2c493d2eb660b6f228a0/visual.json"
    v = json.loads(read(path))
    runs = v["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"]
    runs[0]["value"] = (
        "Search all providers. With Offer Status finds providers with a matching offer under the selected service type. Clear it to include zero-offer providers; (No offers) finds those without offers in that selection. KPIs and activity remain about matching providers, not only matching-status offer rows."
    )
    for run in runs[1:]:
        run["value"] = ""
    save(path, v)
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    bundle = args.project.resolve()
    if not (bundle / "JOURNEY_SCORING_REVIEW.json").exists():
        raise ValueError("Expected the reviewed entity-first WIP project")
    if (bundle / MARKER).exists():
        raise ValueError("Already applied; inspect the saved manifest before reapplying")
    if (bundle / "SM_WMPP_v16.SemanticModel/unappliedChanges.json").exists():
        raise ValueError("Resolve pending Desktop model changes first")
    before = inventory(bundle)
    if before["missing_fields"] or before["broken_actions"]:
        raise ValueError("Resolve baseline saved-reference errors first")
    changes = build(bundle)
    planned = inventory(bundle, changes)
    if planned["missing_fields"] or planned["broken_actions"]:
        raise ValueError("Planned saved-reference check failed")
    print(json.dumps({"project": str(bundle), "files": len(changes), "apply": args.apply}))
    if not args.apply:
        return
    backup = (
        bundle.parent
        / "_review"
        / ("provider-offer-status-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    )
    backup.mkdir(parents=True, exist_ok=False)
    hashes = {}
    for path in changes:
        if path.exists():
            target = backup / path.relative_to(bundle)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
            hashes[str(path.relative_to(bundle))] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path in changes:
        relative = str(path.relative_to(bundle))
        if relative in hashes and hashlib.sha256(path.read_bytes()).hexdigest() != hashes[relative]:
            raise ValueError(f"Concurrent file change; no edits applied: {relative}")
    for path, content in changes.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    after = inventory(bundle)
    manifest = {
        "project": str(bundle),
        "backup": str(backup),
        "files": [str(p.relative_to(bundle)) for p in changes],
        "original_hashes": hashes,
        "missing_fields": after["missing_fields"],
        "broken_actions": after["broken_actions"],
        "selection_semantics": "Provider cohort, OR within statuses, AND with other explorer filters; current activity is not restricted to those offer-status rows",
        "runtime_verified": False,
        "published": False,
        "cache_sources_roles_relationships_unchanged": True,
    }
    (bundle / MARKER).write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {k: v for k, v in manifest.items() if k not in {"files", "original_hashes"}}, indent=2
        )
    )
    if after["missing_fields"] or after["broken_actions"]:
        raise ValueError("Saved-reference check failed; inspect manifest and backup")


if __name__ == "__main__":
    main()
