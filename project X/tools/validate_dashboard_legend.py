"""Read-only validation of the fixed Dashboard Legend v1 import contract.

This is an explicit workbook release check, not part of the routine notebook
pytest suite and not a Power BI refresh or DAX-engine validation.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
V1_SHA256 = "c8d98a31ca5baa336355ec78180d3849d34d1d58f1173fde2452fedb8273ee83"


def read_workbook(path: Path) -> tuple[list[str], dict, dict]:
    with zipfile.ZipFile(path) as archive:
        strings = []
        if "xl/sharedStrings.xml" in archive.namelist():
            for si in ET.fromstring(archive.read("xl/sharedStrings.xml")):
                strings.append("".join(t.text or "" for t in si.findall(".//s:t", NS)))
        relationships = {
            r.attrib["Id"]: r.attrib["Target"]
            for r in ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        }
        names, sheets, tables = [], {}, {}
        for sheet in ET.fromstring(archive.read("xl/workbook.xml")).find("s:sheets", NS):
            name = sheet.attrib["name"]
            target = relationships[sheet.attrib[f"{{{REL}}}id"]]
            target = target.lstrip("/") if target.startswith("/") else "xl/" + target
            cells = {}
            for cell in ET.fromstring(archive.read(target)).findall("s:sheetData/s:row/s:c", NS):
                value_node, formula = cell.find("s:v", NS), cell.find("s:f", NS)
                value = value_node.text if value_node is not None else None
                if cell.attrib.get("t") == "s" and value is not None:
                    value = strings[int(value)]
                elif cell.attrib.get("t") == "inlineStr":
                    value = "".join(t.text or "" for t in cell.findall(".//s:t", NS))
                cells[cell.attrib["r"]] = {
                    "value": value,
                    "formula": formula.text if formula is not None else None,
                    "type": cell.attrib.get("t"),
                }
            names.append(name)
            sheets[name] = cells
        for name in archive.namelist():
            if name.startswith("xl/tables/") and name.endswith(".xml"):
                table = ET.fromstring(archive.read(name))
                tables[table.attrib["name"]] = {
                    "range": table.attrib["ref"],
                    "columns": [c.attrib["name"] for c in table.find("s:tableColumns", NS)],
                }
        return names, sheets, tables


def field(cells: dict, address: str):
    cell = cells.get(address, {})
    return cell.get("formula") or cell.get("value")


def validate(reference: Path, workbook: Path) -> dict:
    original_names, original, _ = read_workbook(reference)
    names, actual, tables = read_workbook(workbook)
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    check(hashlib.sha256(reference.read_bytes()).hexdigest() == V1_SHA256, "The immutable v1 reference file has changed")

    check(names == original_names + ["Gold Source Coverage"], "Sheet names/order must be v1 plus Gold Source Coverage only")
    extents = {"RID": 11, "Table Definition": 4, "KPI Definition": 9}
    counts = {"RID": 81, "Table Definition": 18, "KPI Definition": 118}
    for name, width in extents.items():
        if name not in actual:
            errors.append(f"Missing original sheet: {name}")
            continue
        original_width = 8 if name == "KPI Definition" else width
        for column in range(original_width):
            address = chr(65 + column) + "1"
            check(field(actual[name], address) == field(original[name], address), f"Changed header: {name}!{address}")
        for address, cell in actual[name].items():
            letters = address.rstrip("0123456789")
            row = int(address[len(letters):])
            populated = cell["formula"] is not None or cell["value"] not in (None, "")
            if populated:
                check(len(letters) == 1 and ord(letters) - 64 <= width, f"Extra import column: {name}!{address}")
                check(row <= counts[name], f"Extra import row: {name}!{address}")
            check(cell["type"] != "e", f"Excel formula error: {name}!{address} = {cell['value']}")
    # User-approved append-only extension. The original A:H contract remains fixed.
    check(field(actual.get("KPI Definition", {}), "I1") == "Date Added", "Column I must be Date Added")
    first_recorded = (datetime.date(2026, 8, 26) - datetime.date(1899, 12, 30)).days
    for row in range(2, 119):
        cell = actual.get("KPI Definition", {}).get(f"I{row}", {})
        try:
            date_matches = float(cell.get("value")) == first_recorded
        except (ValueError, TypeError):
            date_matches = False
        check(date_matches and cell.get("type") not in ("s", "str", "inlineStr")
              and cell.get("formula") is None, f"Missing/incorrect typed first-recorded date: KPI Definition!I{row}")
    immutable = {"RID": "ABCDEFJK", "KPI Definition": "ABCDH", "Table Definition": "A"}
    for name, columns in immutable.items():
        if name not in actual:
            continue
        for row in range(2, counts[name] + 1):
            for column in columns:
                address = f"{column}{row}"
                check(field(actual[name], address) == field(original[name], address), f"Changed immutable field/formula: {name}!{address}")
    for name, column, expected in [("RID", "B", 80), ("KPI Definition", "A", 117)]:
        identifiers = [field(actual.get(name, {}), f"{column}{r}") for r in range(2, counts[name] + 1)]
        check(len(set(identifiers)) == expected and None not in identifiers, f"Missing/duplicate IDs in {name}")
    expected_tables = {"LegendSourceCoverage": (16, 9), "LegendRequirements": (80, 9),
                       "LegendGoldCatalogue": (144, 9), "LegendMissionControl": (276, 9),
                       "LegendModelInventory": (71, 9), "LegendPriorGaps": (10, 7)}
    for name, (rows, columns) in expected_tables.items():
        table = tables.get(name)
        check(table is not None, f"Missing coverage table: {name}")
        if table:
            first, last = table["range"].split(":")
            first_row = int(first.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            last_row = int(last.lstrip("ABCDEFGHIJKLMNOPQRSTUVWXYZ"))
            check(last_row - first_row == rows and len(table["columns"]) == columns, f"Coverage extent mismatch: {name}")
    result = {"status": "PASS" if not errors else "FAIL", "errors": errors,
              "reference_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
              "workbook_sha256": hashlib.sha256(workbook.read_bytes()).hexdigest(),
              "requirements": 80, "legacy_kpi_rows": 117, "catalogue_entries": 144,
              "date_added": "2026-08-26; first recorded in repository, not business creation date",
              "scope": "Static workbook contract and formula-error check; no Fabric/Power BI runtime validation"}
    return result


def main() -> int:
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, default=root / "project X/configuration/Dashboard Legend.xlsx")
    args = parser.parse_args()
    result = validate(root / "project X/configuration/Dashboard Legend v1.xlsx", args.workbook)
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return int(result["status"] != "PASS")


if __name__ == "__main__":
    raise SystemExit(main())
