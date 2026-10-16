"""Checks for phone-only logo/title branding; not a native render assertion."""

from copy import deepcopy
import unittest

import brand_wmpp_mobile_headers as branding


class MobileHeaderTests(unittest.TestCase):
    def test_title_keeps_words_style_and_stacking_but_matches_saved_geometry(self):
        state = {"position": {"x": 0, "y": 6, "width": 323, "height": 55, "z": 12000, "tabOrder": 0},
                 "objects": {"general": [{"properties": {"paragraphs": [{"textRuns": [
                     {"value": "Provider Explorer", "textStyle": {"fontSize": "14pt", "color": "#123456"}}
                 ]}]}}]}}
        before = deepcopy(state)
        result = branding.branded_title(state, {"position": {"x": 120, "y": 9, "width": 203, "height": 25}})
        self.assertEqual(state, before)
        self.assertEqual(result["position"], {"x": 120, "y": 9, "width": 203, "height": 25, "z": 12000, "tabOrder": 0})
        self.assertEqual(branding.title_runs(result)[0], {"value": "Provider Explorer", "textStyle": {
            "fontSize": "9pt", "color": "#123456"}})

    def test_header_without_text_runs_is_not_silently_overwritten(self):
        with self.assertRaises(AssertionError):
            branding.branded_title({"position": {}}, {"position": {"x": 120, "y": 9, "width": 203, "height": 25}})

    def test_non_logo_images_are_not_candidates(self):
        self.assertIsNone(branding.resource({"visual": {"objects": {"image": []}}}))

    def test_saved_header_coverage(self):
        updates, pages, asset = branding.plan()
        self.assertEqual(len(pages), 31)
        self.assertEqual(branding.verify(pages, asset, updates)["new_content_overlaps"], 0)


if __name__ == "__main__": unittest.main()
