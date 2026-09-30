"""Offline generation and business-rule fixtures; not a substitute for DAX-engine QA."""

import json
from pathlib import Path
import re
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import add_wmpp_journey_pathways as j


def referral_stage(status="open", offers=(), ipas=(), assignments=1, created=True):
    active = [i for i in ipas if not i.get("closed")]
    if status.lower() in j.CLOSED:
        return 7
    if any(i.get("provider") and i.get("authority") for i in active):
        return 6
    if active:
        return 5
    if any(o in j.ACCEPTED for o in offers):
        return 4
    if any(o in j.PENDING for o in offers):
        return 3
    if not status or any(
        o not in j.ACCEPTED + j.PENDING + j.TERMINAL_OFFER + ["draft"] for o in offers
    ):
        return 8
    if assignments:
        return 2
    return 1 if created else 8


class JourneyTests(unittest.TestCase):
    def test_referral_states(self):
        self.assertEqual(referral_stage(assignments=0), 1)
        self.assertEqual(referral_stage(offers=["draft"]), 2)
        self.assertEqual(referral_stage(offers=["withdrawn"]), 2)
        self.assertEqual(referral_stage(offers=["pending", "draft", "declined"]), 3)
        self.assertEqual(referral_stage(offers=["pending", "accepted"]), 4)
        self.assertEqual(referral_stage(ipas=[{}]), 5)
        self.assertEqual(referral_stage(ipas=[{"provider": True, "authority": True}]), 6)
        self.assertEqual(
            referral_stage(status="closed", ipas=[{"provider": True, "authority": True}]), 7
        )
        self.assertEqual(referral_stage(offers=["unmapped"]), 8)
        self.assertEqual(referral_stage(ipas=[{"provider": True}, {"authority": True}]), 5)
        self.assertEqual(
            referral_stage(ipas=[{"provider": True, "authority": True, "closed": True}]), 2
        )

    def test_provider_signature_is_offer_scoped(self):
        defs = {n: d for n, d, _ in j.definitions()}
        self.assertIn(
            "TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])", defs["Journey provider stage"]
        )
        self.assertIn(
            "TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])",
            defs["Journey providers both signed"],
        )
        self.assertEqual(defs["Journey providers 4"], '"Not captured"')
        self.assertIn(" == 0", defs["Journey providers 0"])

    def test_model_references_and_names(self):
        defs = j.definitions()
        self.assertEqual(len(defs), len({n.casefold() for n, _, _ in defs}))
        columns = {}
        for f in (j.MODEL / "tables").glob("*.tmdl"):
            columns[f.stem] = set(
                (a or b).replace("''", "'")
                for a, b in re.findall(
                    r"(?m)^\tcolumn (?:'((?:[^']|'')+)'|([^\s=]+))",
                    f.read_text(encoding="utf-8-sig"),
                )
            )
        columns["fact_referral"].update(c[0] for c in j.column_definitions())
        for _, dax, _ in defs:
            for table, col in re.findall(r"'([^']+)'\[([^\]]+)\]", dax):
                self.assertIn(col, columns[table], (table, col))
        for _, _, dax, _ in j.column_definitions():
            for table, col in re.findall(r"'([^']+)'\[([^\]]+)\]", dax):
                self.assertIn(col, columns[table], (table, col))

    def test_registered_bookmarks_resolve(self):
        """Check current references, not formatting or a historical layout backup."""
        folder = j.DEFINITION / "bookmarks"
        index = json.loads((folder / "bookmarks.json").read_text(encoding="utf-8-sig"))

        def names(items):
            for item in items:
                if "children" in item:
                    yield from names(item["children"])
                else:
                    yield item["name"]

        registered = list(names(index["items"]))
        self.assertTrue(registered)
        self.assertEqual(len(registered), len(set(registered)))
        for bid in registered:
            with self.subTest(bookmark=bid):
                path = folder / f"{bid}.bookmark.json"
                self.assertTrue(path.is_file(), "Missing registered bookmark")
                bookmark = json.loads(path.read_text(encoding="utf-8-sig"))
                self.assertEqual(bookmark["name"], bid)


if __name__ == "__main__":
    unittest.main()
