"""Portable tests for the compact mobile formatter's preservation contract."""

from copy import deepcopy
import unittest

import compact_wmpp_mobile_layout as compact


class MobileCompactTests(unittest.TestCase):
    def source(self, kind):
        return {"name": "test", "visual": {"visualType": kind, "objects": {},
                "visualContainerObjects": {}}}

    def state(self):
        return {"position": {"x": 0, "y": 100, "width": 323, "height": 100, "z": 100}}

    def test_table_mobile_fonts_without_desktop_edits(self):
        source = self.source("tableEx")
        source["visual"]["objects"] = {"values": [{"properties": {"fontSize": compact.literal(12),
            "fontColor": {"solid": {"color": {"expr": {"Literal": {"Value": "'#FF0000'"}}}}}}}]}
        original = deepcopy(source)
        state = self.state()
        compact.phone_format(source, state, {})
        self.assertEqual(source, original)
        self.assertEqual(compact.number(state["objects"]["values"][0]["properties"]["fontSize"]), 9)
        self.assertNotIn("fontColor", state["objects"]["values"][0]["properties"])

    def test_dynamic_title_not_replaced_by_static_caption(self):
        source = self.source("tableEx")
        source["visual"]["visualContainerObjects"]["title"] = [{"properties": {
            "text": {"expr": {"Measure": {"Property": "selection warning"}}}}}]
        state = self.state()
        compact.phone_format(source, state, {"test": "Wrong static caption"})
        self.assertNotIn("text", state["visualContainerObjects"]["title"][0]["properties"])

    def test_selector_preserved(self):
        source = self.source("actionButton")
        source["visual"]["objects"]["text"] = [{"selector": {"id": "hover"},
            "properties": {"fontSize": compact.literal(12)}}]
        state = self.state()
        compact.phone_format(source, state, {})
        self.assertEqual(state["objects"]["text"][0]["selector"], {"id": "hover"})
        self.assertEqual(compact.number(state["objects"]["text"][0]["properties"]["fontSize"]), 10)

    def test_text_uses_points_and_preserves_words(self):
        source = self.source("textbox")
        source["visual"]["objects"]["general"] = [{"properties": {"paragraphs": [
            {"textRuns": [{"value": "Body text", "textStyle": {"fontSize": "12pt"}}]}]}}]
        state = self.state()
        compact.phone_format(source, state, {})
        run = state["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
        self.assertEqual(run["value"], "Body text")
        self.assertEqual(run["textStyle"]["fontSize"], "9pt")

    def test_non_numeric_expressions_are_not_rewritten(self):
        self.assertIsNone(compact.number([]))
        self.assertIsNone(compact.number({"expr": {"Measure": {"Property": "font"}}}))

    def test_overlap_and_gap(self):
        a = {"x": 0, "y": 0, "width": 323, "height": 100}
        self.assertTrue(compact.overlap(a, {**a, "y": 50}))
        self.assertFalse(compact.overlap(a, {**a, "y": 108}))

    def test_group_hidden_state_inherited(self):
        sources = {"parent": {"isHidden": True}, "child": {"parentGroupName": "parent"}}
        self.assertTrue(compact.hidden("child", sources))
        self.assertFalse(compact.hidden("child", sources, {"parent": False}))

    def test_column_width_zero_is_not_unhidden(self):
        source = self.source("tableEx")
        source["visual"]["objects"]["columnWidth"] = [{"properties": {"value": compact.literal(0)},
            "selector": {"metadata": "technical id"}}]
        state = self.state()
        compact.phone_format(source, state, {})
        self.assertEqual(compact.number(state["objects"]["columnWidth"][0]["properties"]["value"]), 0)

    def test_smaller_card_does_not_get_larger_font(self):
        source = self.source("cardVisual")
        source["visual"]["objects"]["value"] = [{"properties": {"fontSize": compact.literal(14)}}]
        state = self.state()
        compact.phone_format(source, state, {})
        self.assertEqual(compact.number(state["objects"]["value"][0]["properties"]["fontSize"]), 12)

    def test_button_label_survives_font_override(self):
        source = self.source("actionButton")
        source["visual"]["objects"]["text"] = [{"properties": {
            "fontSize": compact.literal(12), "show": compact.original.literal("true"),
            "text": compact.original.literal("'Home'")}}]
        state = self.state()
        compact.phone_format(source, state, {})
        props = state["objects"]["text"][0]["properties"]
        self.assertEqual(props.get("show"), compact.original.literal("true"))
        self.assertEqual(props.get("text"), compact.original.literal("'Home'"))

    def test_legacy_drawer_default_state_has_label(self):
        # The native formatting pane reads the selected Default-state object,
        # not a font-only/unscoped mobile entry.
        source = compact.original.new_button(
            "page", "nav-performance", "Overall performance",
            compact.original.position(2040, 20, 323, 48), "bookmark", hidden=True)
        # Match the saved legacy button: its source has only unscoped text.
        source["visual"]["objects"]["text"] = [source["visual"]["objects"]["text"][0]]
        before = deepcopy(source)
        state = self.state()
        state["objects"] = {"text": [{"properties": {"fontSize": compact.literal(10),
            "leftMargin": compact.literal(8)}}]}
        compact.phone_format(source, state, {})
        for name in ("default", "hover", "selected", "disabled"):
            entry = next((e for e in state["objects"]["text"]
                          if e.get("selector") == {"id": name}), {})
            props = entry.get("properties", {})
            self.assertEqual(props.get("show"), compact.original.literal("true"), name)
            self.assertEqual(props.get("text"), compact.original.literal("'Overall performance'"), name)
            self.assertLessEqual(compact.number(props["fontSize"]), 10)
        self.assertEqual(source, before)

    def test_state_label_and_phone_font_are_both_preserved(self):
        source = [{"properties": {"text": compact.original.literal("'Performance'"),
            "show": compact.original.literal("true"), "fontSize": compact.literal(12)}},
            {"selector": {"id": "disabled"}, "properties": {
                "text": compact.original.literal("'Performance expanded'")}}]
        phone = [{"properties": {"text": compact.original.literal("'Performance'"),
            "fontSize": compact.literal(9)}}]
        entries = compact.complete_button_text(source, phone)
        disabled = next(e["properties"] for e in entries if e.get("selector") == {"id": "disabled"})
        self.assertEqual(disabled["text"], compact.original.literal("'Performance expanded'"))
        self.assertEqual(compact.number(disabled["fontSize"]), 9)
        self.assertEqual(compact.complete_button_text(source, entries), entries)

    def test_new_drawer_generator_populates_default_text(self):
        source = compact.original.new_button("page", "nav-home", "Home",
            compact.original.position(2040, 20, 323, 48), "bookmark")
        objects, _ = compact.original.formatting(source)
        entry = next(e for e in objects["text"] if e.get("selector") == {"id": "default"})
        self.assertEqual(entry["properties"]["text"], compact.original.literal("'Home'"))
        self.assertEqual(entry["properties"]["show"], compact.original.literal("true"))

    def test_homepage_phone_button_reserves_space_for_its_icon(self):
        # Minimise the saved pattern: centred desktop image, zero phone title
        # top margin, and a 52-point phone button. No local report is required.
        source = self.source("actionButton")
        source["name"] = compact.HOME_BUTTONS[0]
        text = {"show": compact.original.literal("true"),
                "text": compact.original.literal("'Performance'"), "fontSize": compact.literal(11),
                "horizontalAlignment": compact.original.literal("'center'"),
                "verticalAlignment": compact.original.literal("'middle'"), "topMargin": compact.literal(74)}
        icon = {"show": compact.original.literal("true"), "placement": compact.original.literal("'custom'"),
                "iconSize": compact.literal(32), "horizontalAlignment": compact.original.literal("'center'"),
                "verticalAlignment": compact.original.literal("'top'"), "topMargin": compact.literal(20),
                "image": {"image": {"url": {"expr": {"ResourcePackageItem": {
                    "PackageName": "RegisteredResources", "PackageType": 1, "ItemName": "existing-icon.svg"}}}}}}
        source["visual"]["objects"] = {"text": [{"properties": text}], "icon": [{"properties": icon}]}
        state = self.state()
        state["position"]["height"] = 52
        state["objects"] = {"text": [{"properties": {"fontSize": compact.literal(9),
            "topMargin": compact.literal(0), "bottomMargin": compact.literal(0),
            "leftMargin": compact.literal(8), "rightMargin": compact.literal(8)}}],
            "icon": [{"properties": {"iconSize": compact.literal(25.6), "topMargin": compact.literal(16)}}]}
        self.assertEqual(compact.button_icon_text_collisions(source, state),
                         ["default", "hover", "selected", "disabled"])
        before = deepcopy(source)
        compact.phone_format(source, state, {})
        self.assertEqual(compact.button_icon_text_collisions(source, state), [])
        self.assertEqual(source, before)
        for name in ("default", "hover", "selected", "disabled"):
            icon = compact.effective_button_props(source, state, "icon", name)
            asset = icon["image"]["image"]["url"]["expr"]["ResourcePackageItem"]["ItemName"]
            self.assertEqual(asset, compact.HOME_BADGES[source["name"]])
            self.assertEqual(compact.number(icon["iconSize"]), 32)

    def test_home_badge_symbol_and_background_stay_together(self):
        source = self.source("actionButton")
        source["name"] = compact.HOME_BUTTONS[0]
        source["visual"]["objects"] = {
            "text": [{"properties": {"show": compact.original.literal("true"),
                "text": compact.original.literal("'Performance'"), "fontSize": compact.literal(9)}}],
            "icon": [{"properties": {"show": compact.original.literal("true"),
                "image": {"image": {"url": {"expr": {"ResourcePackageItem": {
                    "PackageName": "RegisteredResources", "PackageType": 1,
                    "ItemName": "lucide-nav-chart-no-axes-combined-white.svg"}}}}}}}],
            "fill": [{"selector": {"id": name}, "properties": {"show": compact.original.literal("true"),
                "image": {"image": {"url": {"expr": {"ResourcePackageItem": {
                    "PackageName": "RegisteredResources", "PackageType": 1,
                    "ItemName": "wmpp-bubble-background-default.svg"}}}}}}}
                for name in ("default", "hover", "selected", "disabled")]}
        state = self.state()
        state["position"]["height"] = 52
        self.assertTrue(compact.home_badge_errors(source, state))
        before = deepcopy(source)
        compact.phone_home_button_format(source, state)
        self.assertEqual(compact.home_badge_errors(source, state), [])
        self.assertEqual(compact.button_icon_text_collisions(source, state), [])
        self.assertEqual(source, before)

    def test_provider_home_shortcut_reuses_link_and_complete_badge(self):
        import add_wmpp_home_provider_shortcut as shortcut
        template = self.source("actionButton")
        template["visual"]["objects"]["text"] = [{"properties": {
            "show": compact.original.literal("true"), "text": compact.original.literal("'Provider Explorer'"),
            "fontSize": compact.literal(11)}}]
        template["visual"]["visualContainerObjects"]["visualLink"] = [{"properties": {
            "bookmark": compact.original.literal(compact.original.quote(shortcut.BOOKMARK))}}]
        before = deepcopy(template)
        ref = {"position": compact.original.position(1606, 709, 96, 107)}
        source, phone = shortcut.button(template, ref, self.state(),
            {"position": compact.original.position(1421, 831, 468, 118)})
        self.assertEqual(source["name"], compact.HOME_PROVIDER_SHORTCUT)
        self.assertEqual(compact.original.label(source), "Provider Explorer")
        self.assertEqual(compact.original.prop(source, "visualContainerObjects", "visualLink", "bookmark"),
                         shortcut.BOOKMARK)
        self.assertEqual(source["position"]["y"], 915)
        self.assertEqual(compact.home_badge_errors(source, phone), [])
        self.assertEqual(compact.button_icon_text_collisions(source, phone), [])
        self.assertEqual(template, before)

    def test_phone_filter_copy_keeps_query_and_desktop_position(self):
        import group_wmpp_referral_mobile_filters as filters
        source = self.source("slicer")
        source["name"] = "current-status"
        source["position"] = compact.original.position(1180, 300, 232, 92)
        source["visual"]["query"] = {"field": "fact_referral.current_status"}
        before = deepcopy(source)
        original, phone = filters.paired_slicer(source, 2)
        self.assertEqual(source, before)
        self.assertEqual(original["position"], before["position"])
        self.assertEqual(phone["visual"]["query"], before["visual"]["query"])
        self.assertEqual(original["visual"]["syncGroup"], phone["visual"]["syncGroup"])
        self.assertEqual(phone["parentGroupName"], filters.IDS["group"])
        self.assertNotIn("parentGroupName", original)

    def test_phone_filter_bookmarks_never_reset_data_or_person_search(self):
        import group_wmpp_referral_mobile_filters as filters
        for opened in (False, True):
            b = filters.bookmark(opened)
            self.assertTrue(b["options"]["suppressData"])
            self.assertTrue(b["options"]["suppressActiveSection"])
            self.assertNotIn(filters.SEARCH, b["options"]["targetVisualNames"])
            state = b["explorationState"]["sections"][filters.PID]
            self.assertEqual(state["visualContainerGroups"][filters.IDS["group"]]["isHidden"], not opened)

    def test_phone_filter_pairs_are_namespaced_by_page(self):
        import group_wmpp_referral_mobile_filters as filters
        source = self.source("slicer")
        source["position"] = compact.original.position(100, 200, 232, 92)
        source["filterConfig"] = {"filters": [{"name": "status", "selection": "OFFER_MADE"}]}
        before = deepcopy(source)
        pairs = [filters.paired_slicer(source, 0, pid) for pid in ("page-a", "page-b")]
        self.assertNotEqual(pairs[0][1]["name"], pairs[1][1]["name"])
        self.assertNotEqual(pairs[0][0]["visual"]["syncGroup"]["groupName"],
                            pairs[1][0]["visual"]["syncGroup"]["groupName"])
        for pid, (origin, clone) in zip(("page-a", "page-b"), pairs):
            self.assertEqual(clone["parentGroupName"], filters.panel_ids(pid)["group"])
            self.assertEqual(clone["filterConfig"], before["filterConfig"])
            self.assertEqual(origin["position"], before["position"])
            origin["visual"].pop("syncGroup")
            self.assertEqual(origin, before)
        self.assertEqual(source, before)

    def test_additional_page_filter_bookmarks_only_change_display(self):
        import group_wmpp_mobile_filter_pages as pages
        import group_wmpp_referral_mobile_filters as filters
        for config in pages.CONFIGS:
            for opened in (False, True):
                b = filters.bookmark(opened, config["page"], config["name"])
                self.assertTrue(b["options"]["suppressData"])
                self.assertTrue(b["options"]["suppressActiveSection"])
                self.assertFalse(set(config["searches"]) & set(b["options"]["targetVisualNames"]))
                ids = filters.panel_ids(config["page"])
                self.assertEqual(b["options"]["targetVisualNames"], [ids["group"], ids["close"]])

    def test_two_registry_searches_stack_without_resizing_or_reformatting(self):
        import group_wmpp_mobile_filter_pages as pages
        mobile = {"provider": self.state(), "home": self.state()}
        mobile["provider"]["position"].update(y=59, height=66)
        mobile["home"]["position"].update(y=243, height=66)
        mobile["home"]["objects"] = {"existing": "search-format"}
        before = deepcopy(mobile)
        states, button_y = pages.search_positions(mobile, ["provider", "home"], [])
        self.assertEqual(states["provider"], before["provider"])
        self.assertEqual(states["home"]["position"]["y"], 133)
        self.assertEqual(button_y, 207)
        states["home"]["position"]["y"] = before["home"]["position"]["y"]
        self.assertEqual(states["home"], before["home"])
        self.assertEqual(mobile, before)

    def test_offer_person_search_follows_unchanged_location_warning(self):
        import group_wmpp_mobile_filter_pages as pages
        mobile = {"note": self.state(), "person": self.state()}
        mobile["note"]["position"].update(y=59.4, height=63)
        mobile["person"]["position"].update(y=500.8, height=84)
        before = deepcopy(mobile)
        states, button_y = pages.search_positions(mobile, ["person"], ["note"])
        self.assertEqual(states["person"]["position"]["y"], 130.4)
        self.assertEqual(button_y, 222.4)
        self.assertEqual(mobile, before)

    def test_filter_interaction_copies_cover_incoming_outgoing_and_both_sides(self):
        import group_wmpp_mobile_filter_pages as pages
        rules = [{"source": "a", "target": "map", "type": "DataFilter"},
                 {"source": "table", "target": "b", "type": "NoFilter"},
                 {"source": "a", "target": "b", "type": "DataFilter"}]
        before = deepcopy(rules)
        actual = pages.extend_interactions(rules, {"a": "phone-a", "b": "phone-b"})
        self.assertEqual(actual[:3], rules)
        for source, target, kind in (("phone-a", "map", "DataFilter"),
                                     ("table", "phone-b", "NoFilter"),
                                     ("phone-a", "b", "DataFilter"),
                                     ("a", "phone-b", "DataFilter"),
                                     ("phone-a", "phone-b", "DataFilter")):
            self.assertIn({"source": source, "target": target, "type": kind}, actual)
        self.assertEqual(rules, before)
        self.assertEqual(pages.extend_interactions(actual, {"a": "phone-a", "b": "phone-b"}), actual)


if __name__ == "__main__":
    unittest.main()
