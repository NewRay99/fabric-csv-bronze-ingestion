"""Regression checks for the desktop homepage shortcut style."""

from copy import deepcopy
import unittest

import compact_wmpp_mobile_layout as compact
import plan_wmpp_mobile_layout as original
import restyle_wmpp_home_provider_shortcut as style


class DesktopProviderStyleTests(unittest.TestCase):
    def reference(self):
        ref = original.new_button("page", "reference", "Referral Explorer",
            original.position(100, 700, 96, 107), "reference-bookmark")
        objects = ref["visual"]["objects"]
        for group, props in {
            "text": {"horizontalAlignment": original.literal("'center'"), "topMargin": compact.literal(74)},
            "icon": {"show": original.literal("true"), "iconSize": compact.literal(32),
                "horizontalAlignment": original.literal("'center'"), "verticalAlignment": original.literal("'top'"),
                "image": {"image": {"name": original.literal("'reference.svg'"), "url": {"expr": {"ResourcePackageItem": {
                    "PackageName": "RegisteredResources", "PackageType": 1, "ItemName": "reference.svg"}}}}}},
            "fill": {"show": original.literal("true"), "transparency": compact.literal(0)}
        }.items():
            for selector in (None,) + tuple({"id": state} for state in style.STATES):
                compact.set_props(objects, group, props, selector)
        return ref

    def provider(self):
        return original.new_button("page", "provider", "Provider Explorer",
            original.position(400, 915, 232, 48), "provider-bookmark")

    def test_original_compact_pill_is_rejected(self):
        with self.assertRaises(AssertionError): style.check_style(self.provider(), self.reference())

    def test_restyled_button_matches_neighbour_and_keeps_destination(self):
        provider, reference = self.provider(), self.reference()
        before = deepcopy(provider)
        result = style.restyle(provider, reference)
        self.assertTrue(style.check_style(result, reference))
        self.assertEqual(result["visual"]["visualContainerObjects"], provider["visual"]["visualContainerObjects"])
        self.assertEqual(original.prop(result, "visualContainerObjects", "visualLink", "bookmark"), "provider-bookmark")
        self.assertEqual(provider, before)

    def test_every_state_retains_correct_provider_label_and_building(self):
        result = style.restyle(self.provider(), self.reference())
        for state in style.STATES:
            text = compact.effective_button_props(result, {}, "text", state)
            self.assertEqual(text["text"], original.literal("'Provider Explorer'"))
            icon = compact.effective_button_props(result, {}, "icon", state)
            self.assertEqual(icon["image"]["image"]["url"]["expr"]["ResourcePackageItem"]["ItemName"], style.BUILDING)

    def test_a_single_wrong_hover_style_is_rejected(self):
        result = style.restyle(self.provider(), self.reference())
        compact.set_props(result["visual"]["objects"], "text", {
            "topMargin": compact.literal(0)}, {"id": "hover"})
        with self.assertRaises(AssertionError): style.check_style(result, self.reference())

    def test_hidden_phone_fill_is_not_mistaken_for_visible_style_change(self):
        provider = self.provider()
        phone = {"objects": {"fill": [{"properties": {"show": original.literal("false")}}]}}
        before = style.rendered_phone_props(provider, phone)
        changed = deepcopy(provider)
        compact.set_props(changed["visual"]["objects"], "fill", {"transparency": compact.literal(80)})
        self.assertEqual(before, style.rendered_phone_props(changed, phone))


if __name__ == "__main__": unittest.main()
