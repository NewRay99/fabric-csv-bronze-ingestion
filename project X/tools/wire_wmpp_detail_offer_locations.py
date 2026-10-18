"""Wire only Referral Detail's offers -> location-directory interaction."""

import argparse
from copy import deepcopy
import hashlib
import json
import shutil

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original

PAGE = "4cad3706fca6451c66b8"
SOURCE = "79a53defabe24e19d2e1"
TARGET = "df60c76f07c5702701ed"
NAME = "Detail location matches offer"
TABLE = "_Story Measures"
ROOT = original.REPORT / "pages" / PAGE
MODEL = original.PROJECT / "SM_WMPP_v16.SemanticModel/definition/tables/_Story Measures.tmdl"
PAGE_FILE = ROOT / "page.json"
VISUAL = ROOT / "visuals" / TARGET / "visual.json"
TARGETS = (MODEL, PAGE_FILE, VISUAL)
BACKUP = original.ROOT / "reports/_review/detail-offer-location-filter-before-20261017"
RECORD = BACKUP / "delivery.json"
DAX = """VAR offerSelected = ISFILTERED('fact_offer'[offer_id])
VAR matchingLocations =
    CALCULATE(
        COUNTROWS('Referral Map Points'),
        KEEPFILTERS(TREATAS(
            VALUES('fact_offer'[offer_id]),
            'Referral Map Points'[Offer]))
    )
RETURN IF([Detail referral selected] <> 1, BLANK(),
    IF(NOT offerSelected,
        IF(COUNTROWS('Referral Map Points') > 0, 1, BLANK()),
        IF(matchingLocations > 0, 1, BLANK())))"""


def field(source=False):
    return {"Measure": {"Expression": {"SourceRef": {"Source" if source else "Entity": "m" if source else TABLE}},
                        "Property": NAME}}


def filter_rule():
    return {"name": original.ident("detail-offer-location-filter"), "field": field(),
        "type": "Advanced", "filter": {"Version": 2, "From": [{"Name": "m", "Entity": TABLE, "Type": 0}],
        "Where": [{"Condition": {"Comparison": {"ComparisonKind": 0, "Left": field(True),
                    "Right": {"Literal": {"Value": "1L"}}}}}]}, "howCreated": "User"}


def plans(model, page, visual):
    assert "\tmeasure '" + NAME + "'" not in model
    marker = "\tpartition '_Story Measures' = m"
    assert model.count(marker) == 1
    entry = ("\t/// Offer selection filters the location directory only; keep single-referral scope.\n"
        f"\tmeasure '{NAME}' =\n" + "\n".join("\t\t\t" + line for line in DAX.splitlines())
        + "\n\t\tformatString: 0\n\t\tdisplayFolder: Report experience\n"
        + "\t\tlineageTag: 7282694e-5d5e-53f1-8332-1a109436a9a3\n\n")
    page, visual = deepcopy(page), deepcopy(visual)
    interactions = page.setdefault("visualInteractions", [])
    interactions[:] = [i for i in interactions if (i["source"], i["target"]) != (SOURCE, TARGET)]
    interactions.append({"source": SOURCE, "target": TARGET, "type": "DataFilter"})
    filters = visual.setdefault("filterConfig", {}).setdefault("filters", [])
    assert not any(f.get("field") == field() for f in filters)
    filters.append(filter_rule())
    assert any(p.get("field", {}).get("Column", {}).get("Property") == "offer_id"
               for p in original.read(ROOT / "visuals" / SOURCE / "visual.json")["visual"]["query"]["queryState"]["Values"]["projections"])
    return {MODEL: model.replace(marker, entry + marker), PAGE_FILE: page, VISUAL: visual}


def preserved():
    values = {str(p.relative_to(original.PROJECT)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in original.PROJECT.rglob("*") if p.is_file() and p not in TARGETS}
    caches = {str(p.relative_to(original.PROJECT)): [p.stat().st_size, p.stat().st_mtime_ns,
               hashlib.sha256(p.read_bytes()).hexdigest()] for p in original.PROJECT.rglob("*")
               if p.is_file() and p.suffix.lower() in {".abf", ".adb"}}
    assert caches
    return {"non_target_files": len(values), "fingerprint": original.digest_mapping(values), "caches": caches}


def expected_from_backup():
    return plans((BACKUP / MODEL.relative_to(original.PROJECT)).read_text(encoding="utf-8-sig"),
                 original.read(BACKUP / PAGE_FILE.relative_to(original.PROJECT)),
                 original.read(BACKUP / VISUAL.relative_to(original.PROJECT)))


def verify(record):
    for path, value in expected_from_backup().items():
        actual = path.read_text(encoding="utf-8-sig") if isinstance(value, str) else original.read(path)
        assert actual == value, path
    assert preserved() == record["preserved"], "A non-target file or cache changed."
    return {"source_to_target_filter": True, "filter_measure_added_not_displayed": True,
            "single_referral_guard_kept": True, "other_files_and_cache_unchanged": True,
            "native_render_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply-via")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    if args.verify:
        print(json.dumps(verify(original.read(RECORD))))
        return
    updates = plans(MODEL.read_text(encoding="utf-8-sig"), original.read(PAGE_FILE), original.read(VISUAL))
    schemas = home.published_schema_check({p: v for p, v in updates.items() if p.suffix == ".json"}) if args.validate else {}
    print(json.dumps({"target_files": len(updates), "schema": schemas}), flush=True)
    if not args.apply_via: return
    assert not BACKUP.exists(), "Inspect recovery copy before repeating."
    baseline = preserved()
    before = {p: p.read_bytes() for p in TARGETS}
    BACKUP.mkdir(parents=True)
    for path in TARGETS:
        saved = BACKUP / path.relative_to(original.PROJECT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, saved)
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", args.apply_via)
    assert preserved() == baseline
    for path, value in updates.items():
        assert path.read_bytes() == before[path], "A target changed after backup."
        compact.patch_file(path, value, args.apply_via)
    record = {"date": "2026-10-17", "preserved": baseline, "schema": schemas,
              "targets": [str(p.relative_to(original.PROJECT)) for p in TARGETS],
              "behaviour": "Selected offer homes only; clearing selection restores all referral locations; no referral selection stays blank."}
    compact.patch_file(RECORD, record, args.apply_via)
    print(json.dumps(verify(record)), flush=True)


if __name__ == "__main__": main()
