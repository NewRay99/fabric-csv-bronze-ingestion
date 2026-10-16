"""Portable lossless-compaction checks: never conflate formatting with cleanup."""

import unittest

import compact_wmpp_report_json as formatter


class JsonCompactionTests(unittest.TestCase):
    def test_only_insignificant_whitespace_and_encoding_change(self):
        raw = b'{\n  "name": "page",\n  "position": {"x": 2.5},\n  "visible": false\n}\n'
        result = formatter.minified(raw)
        self.assertEqual(formatter.load_json(result), formatter.load_json(raw))
        self.assertLess(len(result), len(raw))
        self.assertEqual(formatter.minified(result), result)

    def test_embedded_dax_and_text_whitespace_is_preserved(self):
        import json
        value = {"expr": 'IF ( [Value] > 1, "A  B", BLANK () )', "text": "Line 1\n  Line 2"}
        raw = json.dumps(value, indent=2).encode()
        self.assertEqual(formatter.load_json(formatter.minified(raw)), value)

    def test_utf8_and_escaped_characters_are_semantically_identical(self):
        raw = b'{ "label": "\\u2630 Menu", "path": "C:\\\\reports" }'
        self.assertEqual(formatter.load_json(formatter.minified(raw)), formatter.load_json(raw))

    def test_duplicate_keys_are_rejected_instead_of_dropping_data(self):
        with self.assertRaises(ValueError): formatter.minified(b'{"same":1,"same":2}')

    def test_non_json_numbers_are_rejected(self):
        for raw in (b'{"x":NaN}', b'{"x":Infinity}', b'{"x":-Infinity}'):
            with self.assertRaises(ValueError): formatter.minified(raw)

    def test_bom_and_line_endings_do_not_change_values(self):
        raw = b'\xef\xbb\xbf{\r\n  "version": "0.20"\r\n}\r\n'
        self.assertEqual(formatter.load_json(formatter.minified(raw)), {"version": "0.20"})


if __name__ == "__main__": unittest.main()
