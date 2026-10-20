"""Lightweight journey action/reference checks, not Power BI visual unit tests.

Appearance, layout and rendered interaction acceptance belong in Desktop UAT.
Normal Desktop saves may reformat JSON and omit properties with default values.
"""

import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from add_wmpp_journey_pathways import PROJECT, DEFINITION, SINGLE, DETAIL, PROVIDER, ident


def visual(pid, key):
    vid = ident("journey:" + pid + ":" + key)
    return json.loads(
        (DEFINITION / "pages" / pid / "visuals" / vid / "visual.json").read_text(
            encoding="utf-8-sig"
        )
    )


def literal(value):
    return value.get("expr", {}).get("Literal", {}).get("Value")


class JourneyRailTests(unittest.TestCase):
    def test_explorer_icons_have_filter_actions(self):
        for pid, count in [(SINGLE, 6), (PROVIDER, 5)]:
            for i in range(1, count + 1):
                if pid == PROVIDER and i == 4:
                    continue  # No fabricated provider-confirmation data.
                v = visual(pid, f"icon-{i}")["visual"]
                links = v.get("visualContainerObjects", {}).get("visualLink", [])
                self.assertTrue(
                    any(literal(e["properties"].get("type", {})) == "'Bookmark'" for e in links),
                    (pid, i, "not clickable"),
                )

    def test_bookmarks_only_change_the_stage_selector(self):
        repair = json.loads((PROJECT / "JOURNEY_RAIL_REPAIR.json").read_text(encoding="utf-8-sig"))
        self.assertTrue(repair["new_bookmark_ids"])
        for bid in repair["new_bookmark_ids"]:
            path = DEFINITION / "bookmarks" / f"{bid}.bookmark.json"
            b = json.loads(path.read_text(encoding="utf-8-sig"))
            opts = b["options"]
            self.assertTrue(opts["applyOnlyToTargetVisuals"])
            self.assertTrue(opts["suppressDisplay"])
            self.assertTrue(opts["suppressActiveSection"])
            # Desktop can omit this false default; true would disable stage filtering.
            self.assertFalse(opts.get("suppressData", False))
            sections = b["explorationState"]["sections"]
            self.assertEqual(len(sections), 1)
            for pid, section in sections.items():
                sid = repair["selector_ids"][pid]
                self.assertEqual(opts["targetVisualNames"], [sid])
                self.assertEqual(list(section["visualContainers"]), [sid])
                selector = DEFINITION / "pages" / pid / "visuals" / sid / "visual.json"
                self.assertTrue(selector.is_file(), "Stage selector target is missing")
                self.assertEqual(
                    json.loads(selector.read_text(encoding="utf-8-sig"))["visual"]["visualType"],
                    "slicer",
                )

    def test_all_actions_resolve_and_unavailable_stage_disabled(self):
        repair = json.loads((PROJECT / "JOURNEY_RAIL_REPAIR.json").read_text(encoding="utf-8-sig"))
        bids = set(repair["new_bookmark_ids"])
        for pid, count in [(SINGLE, 6), (DETAIL, 6), (PROVIDER, 5)]:
            for i in range(1, count + 1):
                links = visual(pid, f"icon-{i}")["visual"]["visualContainerObjects"].get(
                    "visualLink", []
                )
                if pid == PROVIDER and i == 4:
                    self.assertFalse(links)
                else:
                    bid = literal(links[0]["properties"]["bookmark"]).strip("'")
                    self.assertIn(bid, bids)
                    self.assertTrue((DEFINITION / "bookmarks" / f"{bid}.bookmark.json").is_file())


if __name__ == "__main__":
    unittest.main()
