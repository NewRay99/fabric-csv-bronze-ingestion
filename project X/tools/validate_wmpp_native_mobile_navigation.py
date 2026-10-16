"""Checks for precise mobile navigation removal without losing filters/actions."""

from copy import deepcopy
import unittest

import plan_wmpp_mobile_layout as original
import use_wmpp_native_mobile_navigation as native


class NativeNavigationTests(unittest.TestCase):
    def test_only_exact_navigation_roles_are_selected(self):
        page = "test-page"
        selected = native.navigation_ids(page)
        self.assertEqual(len(selected), 18)
        for role in ("open", "close", "scrim", "panel", "drawer-title", "explorers-heading"):
            self.assertIn(original.ident(page + ":" + role), selected)
        for role in ("header", "filter-open", "filter-close", "phone-filter-panel-v1:open",
                     "phone-filter-panel-v1:close", "back", "drillthrough"):
            self.assertNotIn(original.ident(page + ":" + role), selected)

    def test_navigation_keys_are_page_specific(self):
        self.assertFalse(set(native.navigation_ids("a")) & set(native.navigation_ids("b")))

    def test_all_twelve_drawer_links_are_removed_but_not_content_shortcuts(self):
        page = "test-page"
        selected = native.navigation_ids(page)
        for _, target in original.DESTINATIONS:
            self.assertIn(original.ident(page + ":go:" + target), selected)
        self.assertNotIn("a786374f5b2d40d37613", selected)  # Provider homepage shortcut.
        self.assertNotIn("a214f7d8c8a55d927cd1", selected)  # Referral homepage shortcut.

    def test_header_uses_freed_width_without_moving_or_reformatting(self):
        state = {"position": original.position(0, 6.4, 243, 45, 1000, 10),
                 "objects": {"general": [{"properties": {"paragraphs": ["existing title"]}}]}}
        before = deepcopy(state)
        result = native.widen_heading(state)
        self.assertEqual(result["position"]["width"], 323)
        result["position"]["width"] = 243
        self.assertEqual(result, before)
        self.assertEqual(state, before)

    def test_misaligned_header_requires_inspection(self):
        with self.assertRaises(AssertionError):
            native.widen_heading({"position": original.position(10, 0, 243, 45)})


if __name__ == "__main__": unittest.main()
