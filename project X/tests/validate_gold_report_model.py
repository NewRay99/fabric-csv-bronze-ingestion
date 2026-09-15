"""Validate the deployed Gold report's sources, graph and expression references.

Static model checks complement, rather than replace, a Fabric refresh and DAX UAT.
"""

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "reports/client-deliverables/SM WMPP v15"
MODEL = PROJECT / "SM_WMPP.SemanticModel/definition"


def object_names(text, kind):
    return {
        (a.replace("''", "'") if a else b).strip().casefold()
        for a, b in re.findall(
            rf"^\t{kind} (?:'((?:[^']|'')+)'|([^\n=]+?))(?=\s*=|\s*$)",
            text, re.MULTILINE,
        )
    }


def measure_expressions(text):
    result = {}
    for match in re.finditer(r"^\tmeasure '((?:[^']|'')+)'\s*=([\s\S]*?)(?=^\t(?:measure|partition)|\Z)", text, re.M):
        expression = re.split(r'^\t\t(?:formatString|displayFolder|lineageTag|annotation|description|isHidden)\b', match[2], maxsplit=1, flags=re.M)[0]
        expression = expression.replace('```', '').strip()
        result[match[1].replace("''", "'")] = expression
    return result


def check_model():
    if not MODEL.exists():
        print("NOTE extracted Gold report absent; skipping saved-model checks")
        return
    tables = {p.stem.casefold(): p.read_text(encoding="utf-8-sig")
              for p in (MODEL / "tables").glob("*.tmdl")}
    columns = {name: object_names(text, "column") for name, text in tables.items()}
    measures = {name: object_names(text, "measure") for name, text in tables.items()}
    source_expressions = measure_expressions((ROOT / 'reports/current/_Measures.tmdl').read_text(encoding='utf-8-sig'))
    for name, expression in measure_expressions(tables['_measures']).items():
        assert name in source_expressions, f'Missing maintained measure: {name}'
        assert re.sub(r'\s+', '', expression) == re.sub(r'\s+', '', source_expressions[name]), (
            f'Source and deployed expression differ: {name}'
        )
        # This is a delimiter check, not a substitute for compiling DAX.
        tokens = re.sub(r'"(?:[^"]|"")*"|\x27(?:[^\x27]|\x27\x27)*\x27|\[[^\]]+\]', '', expression)
        depth = 0
        for token in tokens:
            depth += (token == '(') - (token == ')')
            assert depth >= 0, f'Unbalanced expression: {name}'
        assert depth == 0, f'Unbalanced expression: {name}'
    for name, text in tables.items():
        assert not re.search(r'Schema\s*=\s*"(?:bronze|silver)"', text, re.I), name
        assert 'mode: directQuery' not in text, f"Unexpected mixed storage: {name}"
        # Remove quoted strings and comments before inspecting DAX references.
        expressions = re.sub(r'"(?:[^"]|"")*"', '""', text)
        for quoted, bare, column in re.findall(
            r"(?:'([^'\n]+)'|\b([A-Za-z_]\w*))\[([^\]\n]+)\]", expressions
        ):
            table = (quoted or bare).casefold()
            # M field access has no table qualifier; all matches here are DAX.
            assert table in tables, f"{name}: missing table {table}"
            assert column.casefold() in columns[table] | measures[table], (
                f"{name}: missing field {table}[{column}]"
            )
    required_gold = {
        "dim_person": "dim_person", "dim_offer_status": "dim_offer_status",
        "fact_referral": "fact_referral", "fact_offer": "fact_offer",
        "fact_ipa": "fact_ipa", "fact_referral_snapshot": "fact_referral_snapshot",
    }
    for name, physical in required_gold.items():
        assert f'Schema="gold",Item="{physical}"' in tables[name], name
    relationships = (MODEL / 'relationships.tmdl').read_text(encoding='utf-8-sig')
    edges = {}
    for block in re.split(r'(?=^relationship )', relationships, flags=re.M):
        if not block.strip():
            continue
        endpoints = []
        for end in ('from', 'to'):
            match = re.search(rf'{end}Column: (?:\x27([^\x27]+)\x27|([^\.]+))\.(?:\x27([^\x27]+)\x27|([^\n]+))', block)
            assert match, block
            table, column = (match[1] or match[2]).casefold(), (match[3] or match[4]).casefold()
            assert table in columns and column in columns[table], block
            endpoints.append(table)
        if 'isActive: false' not in block:
            assert 'bothDirections' not in block, 'Business graph must be single direction'
            edges.setdefault(endpoints[1], []).append(endpoints[0])
    # An active dimension must not reach a fact by multiple paths (ambiguous filters).
    for origin in edges:
        visited = set()
        def visit(node):
            assert node not in visited, f'Cycle or ambiguous paths from {origin} to {node}'
            visited.add(node)
            for child in edges.get(node, []):
                visit(child)
        visit(origin)
    assert 'gender_clean' in columns['dim_person']
    assert {'signed_by_provider', 'signed_by_local_authority', 'is_ipa_completed',
            'is_ipa_pending'} <= columns['fact_ipa']
    for path in (PROJECT / "SM_WMPP.Report/definition").rglob("*.json"):
        def walk(value):
            if isinstance(value, dict):
                for kind, inventory in (("Column", columns), ("Measure", measures)):
                    field = value.get(kind, {})
                    entity = field.get("Expression", {}).get("SourceRef", {}).get("Entity")
                    if entity:
                        assert entity.casefold() in inventory, f"{path}: {entity}"
                        assert field['Property'].casefold() in inventory[entity.casefold()], (
                            f"{path}: {entity}[{field['Property']}]"
                        )
                for child in value.values():
                    walk(child)
            elif isinstance(value, list):
                for child in value:
                    walk(child)
        walk(json.loads(path.read_text(encoding="utf-8-sig")))
    print(f"PASS {len(tables)} Gold/report tables, expressions and report field bindings")


if __name__ == "__main__":
    check_model()
