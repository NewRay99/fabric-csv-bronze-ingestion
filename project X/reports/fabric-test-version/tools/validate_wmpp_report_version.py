"""Portable tests for the shared WMPP report-version parameter."""

from copy import deepcopy
import unittest

import parameterize_wmpp_report_version as version


class ReportVersionTests(unittest.TestCase):
    def sample(self):
        return {"name": "existing", "position": {"x": 50, "y": 40, "width": 92, "height": 27},
            "visual": {"visualType": "textbox", "objects": {"general": [{"properties": {
                "paragraphs": [{"textRuns": [{"value": version.OLD_LABEL,
                    "textStyle": {"fontFamily": "Segoe UI", "fontSize": "8pt", "color": "#333333"}}],
                    "horizontalTextAlignment": "right"}]}}]},
                "visualContainerObjects": {"background": [{"properties": {"show": False}}]}}}

    def test_native_textbox_reference_matches_its_value_selector(self):
        source = self.sample()
        value = version.replace_label(source)
        text = value["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]
        self.assertEqual(text["value"]["propertyIdentifier"], {"objectName": "values", "propertyName": "expr"})
        bound = value["visual"]["objects"]["values"][0]
        self.assertEqual(text["value"]["selector"], bound["selector"])
        self.assertEqual(bound["properties"]["expr"]["expr"], version.measure_expression())

    def test_geometry_style_alignment_and_source_are_preserved(self):
        source = self.sample()
        before = deepcopy(source)
        result = version.replace_label(source)
        result["visual"]["objects"].pop("values")
        result["visual"]["objects"]["general"][0]["properties"]["paragraphs"][0]["textRuns"][0]["value"] = version.OLD_LABEL
        self.assertEqual(result, before)
        self.assertEqual(source, before)

    def test_existing_values_are_not_silently_overwritten(self):
        source = self.sample()
        source["visual"]["objects"]["values"] = []
        with self.assertRaises(AssertionError): version.replace_label(source)

    def test_parameter_is_text_and_single_source_of_version_number(self):
        parameter, table = version.parameter_definition(), version.table_definition()
        self.assertIn('"0.16" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]', parameter)
        self.assertNotIn("0.16", table)
        self.assertIn("Text.Trim(ReportVersion)", table)
        self.assertIn('#table(type table [ReportVersion = text], {{ValidatedVersion}})', table)
        self.assertIn('then error "ReportVersion must not be blank."', table)

    def test_label_is_disconnected_and_ignores_settings_filter_context(self):
        table = version.table_definition()
        self.assertIn("REMOVEFILTERS ( 'Report Settings' )", table)
        self.assertIn('"Version: " & versionText', table)
        self.assertNotIn("relationship", table)
        self.assertNotIn("Sql.Database", table)
        self.assertNotIn("Web.Contents", table)

    def test_desktop_trailing_blank_line_does_not_mask_real_definition_changes(self):
        self.assertTrue(version.settings_definition_matches(version.table_definition() + "\n"))
        self.assertFalse(version.settings_definition_matches(version.table_definition().replace("REMOVEFILTERS", "KEEPFILTERS")))

    def test_model_extension_preserves_existing_refs_and_query_order(self):
        text = 'model Model\n\tculture: en-GB\n\nannotation PBI_QueryOrder = ["one","two"]\n\nref table one\nref table two\n\nref role \'WMPP Dynamic Detail RLS\'\n'
        actual = version.extend_model(text)
        self.assertIn('["one","two","ReportVersion","Report Settings"]', actual)
        self.assertIn("ref table one\nref table two\n", actual)
        self.assertIn("ref table 'Report Settings'\n\nref role", actual)
        with self.assertRaises(AssertionError): version.extend_model(actual)


if __name__ == "__main__": unittest.main()
