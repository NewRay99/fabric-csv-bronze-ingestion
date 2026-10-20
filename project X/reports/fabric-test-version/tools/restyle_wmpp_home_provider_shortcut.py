"""Match the desktop Provider Explorer shortcut to its homepage neighbours.

Desktop-only, four-column revision. Phone files and effective phone styles are
preserved. Preview by default; apply through apply_patch with recovery copies.
"""

import argparse
from copy import deepcopy
import json
import shutil

import add_wmpp_home_provider_shortcut as home
import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original

ROOT = home.ROOT
BUTTONS = compact.HOME_BUTTONS
DESCRIPTIONS = ("ac6f421a5c6b48600c2e", "16015cc037165e0e1c30", home.DESC_ID,
                original.ident(home.PAGE + ":desktop-provider-description-v1"))
DIVIDERS = ("a5c0320779641d172438", "2eb9812020c54e388502",
            original.ident(home.PAGE + ":desktop-provider-divider-v1"))
BUILDING = "lucide-nav-building-complex-white.svg"
BACKUP = original.ROOT / "reports/_review/home-desktop-provider-style-before-20261015"
DELIVERY = original.PROJECT / "HOMEPAGE_DESKTOP_SHORTCUTS_DELIVERY.json"
STATES = ("default", "hover", "selected", "disabled")
GROUPS = ("shape", "text", "icon", "fill", "outline", "shadow", "glow")


def restyle(provider, reference):
    result = deepcopy(provider)
    result["visual"]["objects"] = deepcopy(reference["visual"]["objects"])
    for entry in result["visual"]["objects"]["text"]:
        entry["properties"]["text"] = original.literal("'Provider Explorer'")
    for entry in result["visual"]["objects"]["icon"]:
        image = entry["properties"].get("image", {}).get("image")
        if image:
            image["name"] = original.literal(original.quote(BUILDING))
            image["url"]["expr"]["ResourcePackageItem"]["ItemName"] = BUILDING
    for dimension in ("width", "height"):
        result["position"][dimension] = reference["position"][dimension]
    # Keep the original bookmark, accessible name and container styling. These
    # are already identical to the neighbour's non-style-preset container values.
    assert result["visual"]["visualContainerObjects"] == provider["visual"]["visualContainerObjects"]
    return result


def check_style(provider, reference):
    assert (provider["position"]["width"], provider["position"]["height"]) == (
        reference["position"]["width"], reference["position"]["height"]), "Provider shortcut is not the matching desktop icon/label size."
    for state in STATES:
        for group in GROUPS:
            actual = compact.effective_button_props(provider, {}, group, state)
            expected = compact.effective_button_props(reference, {}, group, state)
            if group == "text":
                assert actual.pop("text") == original.literal("'Provider Explorer'")
                expected.pop("text", None)
            if group == "icon":
                image = actual.pop("image")
                assert image["image"]["url"]["expr"]["ResourcePackageItem"]["ItemName"] == BUILDING
                expected.pop("image", None)
            assert actual == expected, (state, group, "Desktop style differs from its neighbour.")
    return True


def rendered_phone_props(source, phone):
    result = {}
    for state in STATES:
        for group in GROUPS:
            props = compact.effective_button_props(source, phone, group, state)
            if props.get("show") == original.literal("false"):
                props = {"show": original.literal("false")}
            result[state, group] = props
    return result


def plans(source_overrides=None):
    assert not DELIVERY.exists(), "Already delivered; use --verify."
    sources = {p.parent.name: original.read(p) for p in ROOT.glob("*/visual.json")}
    sources.update(source_overrides or {})
    reference = sources[home.REF_ID]
    # The current row's left/right edges stay fixed. Four equal columns replace
    # three, with a neutral divider in each gap; no page-height/footer changes.
    left = sources[DESCRIPTIONS[0]]["position"]["x"]
    right = sources[home.DESC_ID]["position"]["x"] + sources[home.DESC_ID]["position"]["width"]
    gap = 32
    width = (right - left - 3 * gap) / 4
    updates = {}
    for index, vid in enumerate(BUTTONS):
        value = restyle(sources[vid], reference) if vid == home.NEW_ID else deepcopy(sources[vid])
        value["position"]["x"] = left + index * (width + gap) + (width - value["position"]["width"]) / 2
        value["position"]["y"] = reference["position"]["y"]
        updates[ROOT / vid / "visual.json"] = value
        description = deepcopy(sources.get(DESCRIPTIONS[index], sources[home.DESC_ID]))
        description["name"] = DESCRIPTIONS[index]
        description["position"]["x"] = left + index * (width + gap)
        description["position"]["width"] = width
        description["position"]["height"] = 118
        if index == 3:
            description["position"]["z"] = 94010
            description["position"]["tabOrder"] = 90020
            runs = description["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"]
            assert len(runs) == 1
            runs[0]["value"] = "Search providers and homes, and explore their linked referrals, offers and messages."
        updates[ROOT / DESCRIPTIONS[index] / "visual.json"] = description
    for index, vid in enumerate(DIVIDERS):
        divider = deepcopy(sources.get(vid, sources[DIVIDERS[1]]))
        divider["name"] = vid
        divider["position"]["x"] = left + (index + 1) * (width + gap) - gap / 2 - divider["position"]["width"] / 2
        if index == 2:
            divider["position"]["z"] = 57010
            divider["position"]["tabOrder"] = 93010
        updates[ROOT / vid / "visual.json"] = divider
    phone = original.read(ROOT / home.NEW_ID / "mobile.json")
    assert rendered_phone_props(sources[home.NEW_ID], phone) == rendered_phone_props(
        updates[ROOT / home.NEW_ID / "visual.json"], phone), "Phone appearance must remain unchanged."
    return updates


def verify(updates=None):
    updates = updates or {}
    def read(path): return updates[path] if path in updates else original.read(path)
    sources = {p.parent.name: read(p) for p in ROOT.glob("*/visual.json")}
    sources.update({p.parent.name: value for p, value in updates.items()})
    provider, reference = sources[home.NEW_ID], sources[home.REF_ID]
    check_style(provider, reference)
    assert original.prop(provider, "visualContainerObjects", "visualLink", "bookmark") == home.BOOKMARK
    bookmark = original.read(original.REPORT / "bookmarks" / (home.BOOKMARK + ".bookmark.json"))
    assert bookmark["explorationState"]["activeSection"] == home.DESTINATION
    row = [sources[vid]["position"] for vid in BUTTONS]
    assert len({pos["y"] for pos in row}) == 1
    centres = [pos["x"] + pos["width"] / 2 for pos in row]
    gaps = [b-a for a, b in zip(centres, centres[1:])]
    assert max(gaps) - min(gaps) < 0.01
    footer_y = min(sources[vid]["position"]["y"] for vid in home.FOOTERS)
    for vid, desc_id in zip(BUTTONS, DESCRIPTIONS):
        pos, desc = sources[vid]["position"], sources[desc_id]["position"]
        assert pos["y"] + pos["height"] + 8 <= desc["y"]
        assert desc["y"] + desc["height"] + 16 < footer_y
    for vid in BUTTONS + DESCRIPTIONS:
        source = sources[vid]
        for other_id, other in sources.items():
            if other_id == vid or compact.hidden(other_id, sources) or not compact.relevant(other): continue
            assert not compact.overlap(source["position"], other["position"]), (vid, other_id, "Desktop overlap")
    phone = read(ROOT / home.NEW_ID / "mobile.json")
    assert not compact.button_icon_text_collisions(provider, phone)
    assert not compact.home_badge_errors(provider, phone)
    if not updates:
        before = original.read(BACKUP / (ROOT / home.NEW_ID / "visual.json").relative_to(original.PROJECT))
        assert rendered_phone_props(before, phone) == rendered_phone_props(provider, phone)
    return {"four_desktop_shortcuts_aligned": True, "provider_matches_neighbour_style_all_states": True,
        "button_description_and_footer_overlaps": 0, "provider_destination_preserved": True,
        "phone_appearance_preserved": True, "native_render_verified": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-style", action="store_true")
    parser.add_argument("--verify", action="store_true")
    parser.add_argument("--validate", action="store_true")
    parser.add_argument("--apply-via")
    parser.add_argument("--resume-via")
    args = parser.parse_args()
    if args.check_style:
        print(json.dumps({"desktop_style_matches": check_style(original.read(ROOT / home.NEW_ID / "visual.json"),
            original.read(ROOT / home.REF_ID / "visual.json"))}))
        return
    if args.verify:
        print(json.dumps(verify()))
        return
    overrides = {}
    if args.resume_via:
        assert BACKUP.exists() and not DELIVERY.exists()
        overrides = {p.parent.name: original.read(p) for p in
                     (BACKUP / ROOT.relative_to(original.PROJECT)).glob("*/visual.json")}
        assert len(overrides) == 9, "Inspect original backup inventory before resuming."
    updates = plans(overrides)
    checks = verify(updates)
    schema = home.published_schema_check(updates) if args.validate else {}
    print(json.dumps({"planned_desktop_files": len(updates), "checks": checks, "schema": schema}), flush=True)
    executable = args.resume_via or args.apply_via
    if not executable: return
    if not args.resume_via: assert not BACKUP.exists(), "Inspect backup before repeating."
    baseline = home.preserved(set(updates))
    before = {p: p.read_bytes() for p in updates if p.exists()}
    if not args.resume_via:
        BACKUP.mkdir(parents=True)
        for path in list(before) + [compact.MANIFEST]:
            saved = BACKUP / path.relative_to(original.PROJECT)
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
    else:
        for path in before:
            recovery = BACKUP / path.relative_to(original.PROJECT)
            assert original.read(path) == updates[path] or (
                recovery.exists() and path.read_bytes() == recovery.read_bytes()), "Unexpected external edit; do not overwrite."
    compact.BACKUP = BACKUP
    compact.patch_file(BACKUP / ".gitignore", "*\n", executable)
    assert home.preserved(set(updates)) == baseline
    for path, value in updates.items():
        if path in before: assert path.read_bytes() == before[path]
        path.parent.mkdir(parents=True, exist_ok=True)
        compact.patch_file(path, value, executable)
    assert home.preserved(set(updates)) == baseline, "Unrelated report/model/phone/resources changed."
    compact.patch_file(DELIVERY, {"date": "2026-10-15", "checks": verify(), "schema": schema,
        "backup": str(BACKUP), "files": [str(p.relative_to(original.PROJECT)) for p in updates],
        "model_bookmarks_assets_and_mobile_files_preserved": True}, executable)
    manifest = original.read(compact.MANIFEST)
    manifest["protected"] = compact.protected()
    manifest.setdefault("authorised_definition_updates", []).append({"date": "2026-10-15",
        "reason": "Four-column homepage desktop shortcuts; Provider Explorer matches circular neighbour style; phone unchanged.",
        "files": [str(p.relative_to(original.PROJECT)) for p in updates]})
    compact.patch_file(compact.MANIFEST, manifest, executable)
    print(json.dumps({"saved": verify(), "backup": str(BACKUP),
                      "all_mobile_files_model_bookmarks_assets_preserved": True}), flush=True)


if __name__ == "__main__": main()
