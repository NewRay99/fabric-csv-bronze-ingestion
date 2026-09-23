"""Capture reusable PBIR formatting once, then sync the shared Power BI theme.

Default execution is offline and only writes report formatting/theme resources.
--capture is a one-time bootstrap requiring Microsoft's public theme schema.
Edit templates/WMPP_Common_Theme.json afterwards, then run this script again.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
CURRENT = ROOT / 'reports/current'
TEMPLATES = ROOT / 'reports/templates'
THEME = TEMPLATES / 'WMPP_Common_Theme.json'
MANIFEST = TEMPLATES / 'WMPP_Common_Theme.manifest.json'
SCHEMA = 'https://raw.githubusercontent.com/microsoft/powerbi-desktop-samples/main/Report%20Theme%20JSON%20Schema/reportThemeSchema-2.154.json'
SOURCE = CURRENT / 'RPT WMPP v16/WMPP_DASHBOARD_v16.Report'
# Only explicitly enumerated current projects; never archives/client-deliverables.
REPORTS = [SOURCE,
    CURRENT / 'SM WMPP v16 updated/SM_WMPP_v16.Report',
    CURRENT / 'SM WMPP Mission Control v16/SM WMPP Mission Control.Report',
    CURRENT / 'WMPP/SM_WMPP.Report']
SKIP_GROUPS = {'general', 'data', 'selection', 'date', 'dateRange', 'columnWidth',
    'visualLink', 'visualTooltip', 'stylePreset', 'image', 'cardImage', 'imageScaling',
    'query', 'zoom', 'rotation', 'shape', 'layout', 'referenceLabelLayout'}
SKIP_PROPERTIES = {'text', 'altText', 'url', 'webUrl', 'section', 'navigationSection',
    'drillthroughSection', 'bookmark', 'image', 'imageUrl', 'titleText', 'name',
    'start', 'end', 'minimum', 'maximum', 'axisType', 'axisScale', 'invertAxis',
    'labelDisplayUnits', 'labelPrecision', 'decimalPlaces', 'formatString'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def packed(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def invariant(data, spec=None, report=False, original_preset=None):
    """Remove only authorized theme deltas for before/after safety comparison."""
    data = deepcopy(data)
    if spec:
        visual = data['visual']
        for slot in spec['slots']:
            for entry in visual.get(slot['location'], {}).get(slot['group'], []):
                if entry.get('selector', {}) == slot['selector']:
                    entry.get('properties', {}).pop(slot['property'], None)
        visual.get('objects', {}).pop('stylePreset', None)
        container = visual.get('visualContainerObjects', {})
        preset = container.get('stylePreset', [{}])[0].get('properties', {}).get('name', {})
        if preset.get('expr', {}).get('Literal', {}).get('Value', '').startswith("'WMPP "):
            container.pop('stylePreset', None)
        if original_preset is not None:
            visual.setdefault('visualContainerObjects', {})['stylePreset'] = deepcopy(original_preset)
        for location in ('objects', 'visualContainerObjects'):
            groups = visual.get(location, {})
            for group in list(groups):
                groups[group] = [e for e in groups[group] if e.get('properties')]
                if not groups[group]:
                    del groups[group]
            if not groups:
                visual.pop(location, None)
    if report:
        data['themeCollection'].pop('customTheme', None)
        for package in data.get('resourcePackages', []):
            package['items'] = [i for i in package['items'] if i.get('type') != 'CustomTheme']
        data['resourcePackages'] = [p for p in data.get('resourcePackages', []) if p['items']]
    return hashlib.sha256(packed(data).encode()).hexdigest()


def save(path, value):
    text = json.dumps(value, indent=2, ensure_ascii=False) + '\n'
    if not path.exists() or path.read_text(encoding='utf-8') != text:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')


def plain(value):
    """Translate only literal/static PBIR values, never data-bound expressions."""
    if isinstance(value, dict):
        if 'expr' in value:
            expr = value['expr']
            if set(expr) == {'ThemeDataColor'}:
                return deepcopy(value)
            if set(expr) != {'Literal'}:
                raise ValueError('data-bound expression')
            literal = expr['Literal']['Value']
            if literal.startswith("'") and literal.endswith("'"):
                return literal[1:-1].replace("''", "'")
            if literal in ('true', 'false'):
                return literal == 'true'
            if re.fullmatch(r'-?\d+(?:\.\d+)?[DLM]?', literal):
                number = float(literal.rstrip('DLM'))
                return int(number) if number.is_integer() else number
            raise ValueError('non-style literal')
        if any(k in value for k in ('ResourcePackageItem', 'filter', 'Rule', 'FillRule')):
            raise ValueError('resource or conditional expression')
        return {k: plain(v) for k, v in value.items()}
    if isinstance(value, list):
        return [plain(v) for v in value]
    return value


def properties(schema, root):
    if '$ref' in schema:
        result = root
        for part in schema['$ref'].removeprefix('#/').split('/'):
            result = result[part]
        return properties(result, root)
    result = dict(schema.get('properties', {}))
    for part in schema.get('allOf', []):
        result.update(properties(part, root))
    return result


def resolved(schema, root):
    if '$ref' not in schema:
        return schema
    value = root
    for part in schema['$ref'].removeprefix('#/').split('/'):
        value = value[part]
    return resolved(value, root)


def compatible(value, schema, root):
    """Conservative preflight for extracted property schemas; full Test-Json follows."""
    schema = resolved(schema, root)
    kinds = {'object': lambda x: isinstance(x, dict),
             'array': lambda x: isinstance(x, list),
             'string': lambda x: isinstance(x, str),
             'boolean': lambda x: isinstance(x, bool),
             'number': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
             'integer': lambda x: isinstance(x, int) and not isinstance(x, bool),
             'null': lambda x: x is None}
    if 'type' in schema:
        types = schema['type'] if isinstance(schema['type'], list) else [schema['type']]
        if not any(kinds[t](value) for t in types):
            return False
    if 'const' in schema and value != schema['const']:
        return False
    if 'enum' in schema and value not in schema['enum']:
        return False
    if 'oneOf' in schema and sum(compatible(value, s, root) for s in schema['oneOf']) != 1:
        return False
    if 'anyOf' in schema and not any(compatible(value, s, root) for s in schema['anyOf']):
        return False
    if not all(compatible(value, s, root) for s in schema.get('allOf', [])):
        return False
    if 'not' in schema and compatible(value, schema['not'], root):
        return False
    if isinstance(value, dict):
        if not all(k in value for k in schema.get('required', [])):
            return False
        props = schema.get('properties', {})
        for key, child in value.items():
            if key in props and not compatible(child, props[key], root):
                return False
            if key not in props and schema.get('additionalProperties') is False:
                return False
    if isinstance(value, list) and 'items' in schema:
        if not all(compatible(v, schema['items'], root) for v in value):
            return False
    if isinstance(value, str) and 'pattern' in schema and not re.search(schema['pattern'], value):
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if value < schema.get('minimum', float('-inf')) or value > schema.get('maximum', float('inf')):
            return False
    return True


def extract(visual, schema):
    kind = visual['visualType']
    definition = schema['definitions'].get('visual-' + kind)
    if not definition:  # Third-party visuals keep their explicit formatting.
        return {}, []
    supported = properties(definition, schema)
    style, slots = {}, []
    objects = visual.get('objects', {})
    containers = visual.get('visualContainerObjects', {})
    for location, groups in [('objects', objects), ('visualContainerObjects', containers)]:
        for group, entries in groups.items():
            if group in SKIP_GROUPS or group not in supported:
                continue
            # The theme has one namespace; avoid ambiguous object/container collisions.
            if group in objects and group in containers:
                continue
            allowed = properties(supported[group].get('items', {}), schema)
            for index, entry in enumerate(entries):
                selector = entry.get('selector', {})
                if selector and set(selector) != {'id'}:
                    continue  # A field/series selector is not a reusable style.
                target = {'$id': selector['id']} if selector else {}
                for prop, value in entry.get('properties', {}).items():
                    if prop in SKIP_PROPERTIES or prop not in allowed:
                        continue
                    try:
                        converted = plain(value)
                    except ValueError:
                        continue
                    prop_schema = resolved(allowed[prop], schema)
                    if prop_schema.get('type') in ('number', 'integer') and isinstance(converted, str):
                        if re.fullmatch(r'-?\d+(?:\.\d+)?', converted):
                            converted = float(converted)
                            if converted.is_integer():
                                converted = int(converted)
                    if not compatible(converted, prop_schema, schema):
                        continue
                    target[prop] = converted
                    slots.append({'location': location, 'group': group,
                        'index': index, 'property': prop,
                        'selector': selector, 'original': value})
                if set(target) - {'$id'}:
                    style.setdefault(group, []).append(target)
    return style, slots


def capture():
    if any(read(p / 'definition/report.json')['themeCollection'].get('customTheme', {}).get('name', '').startswith('WMPP_Common_Theme-') for p in REPORTS):
        raise SystemExit('Theme already applied. Edit the common theme and run without --capture.')
    with urllib.request.urlopen(SCHEMA, timeout=30) as response:
        schema = json.load(response)
    report = read(SOURCE / 'definition/report.json')
    old_name = report['themeCollection']['customTheme']['name']
    theme = read(SOURCE / 'StaticResources/RegisteredResources' / old_name)
    theme['name'] = 'WMPP Common'
    theme['$schema'] = SCHEMA
    # Preserve original palette indices: existing ThemeDataColor bindings rely on them.
    palette = theme['dataColors']
    theme['textClasses'] = {
        'title': {'fontFace': 'Segoe UI Semibold', 'fontSize': 13, 'color': '#2B2427'},
        'header': {'fontFace': 'Segoe UI Semibold', 'fontSize': 12, 'color': '#2B2427'},
        'label': {'fontFace': 'Segoe UI', 'fontSize': 10, 'color': '#61575C'},
        'callout': {'fontFace': 'Segoe UI Semibold', 'fontSize': 24, 'color': '#202124'}}
    # Latest dashboard canvas. Existing page-specific backgrounds stay explicit.
    theme['visualStyles']['page']['*']['background'] = [
        {'color': {'solid': {'color': '#F7F8FA'}}, 'transparency': 0}]
    manifest = {'version': 1, 'source': str(SOURCE.relative_to(ROOT)).replace('\\', '/'),
        'reports': [str(p.relative_to(ROOT)).replace('\\', '/') for p in REPORTS],
        'visuals': {}, 'styles': {}, 'inlineTextStyles': [], 'pageStyles': [],
        'safetyFingerprints': {}, 'protectedFileHashes': {}, 'originalPresets': {},
        'notes': ['Conditional formatting, data/field selectors, visual content, images, '
                  'navigation, slicer state and custom-visual settings remain report-local.']}
    typography = set()
    for folder in REPORTS:
        for path in sorted((folder / 'definition/pages').rglob('*.json')):
            data = read(path)
            for color in re.findall(r'#[0-9A-Fa-f]{6}\b', json.dumps(data)):
                if color.upper() not in {p.upper() for p in palette}:
                    palette.append(color.upper())
            if path.name == 'page.json' and data.get('objects'):
                style = {k: v for k, v in data['objects'].items() if k in ('background', 'outspace')}
                if style and style not in manifest['pageStyles']:
                    manifest['pageStyles'].append(style)
            visual = data.get('visual')
            if not visual:
                continue
            # Rich-text paragraphs cannot safely be moved to a theme without their content.
            for entry in visual.get('objects', {}).get('general', []):
                for paragraph in entry.get('properties', {}).get('paragraphs', []):
                    for run in paragraph.get('textRuns', []):
                        if run.get('textStyle'):
                            typography.add(packed(run['textStyle']))
            style, slots = extract(visual, schema)
            if not style:
                continue
            kind = visual['visualType']
            preset = 'WMPP ' + kind + ' ' + hashlib.sha256(packed(style).encode()).hexdigest()[:10]
            theme['visualStyles'].setdefault(kind, {})[preset] = style
            spec = {'type': kind, 'preset': preset, 'slots': slots}
            existing = visual.get('visualContainerObjects', {}).get('stylePreset')
            if existing:
                manifest['originalPresets'][str(path.relative_to(ROOT)).replace('\\', '/')] = existing
            style_id = hashlib.sha256(packed(spec).encode()).hexdigest()[:16]
            manifest['styles'][style_id] = spec
            manifest['visuals'][str(path.relative_to(ROOT)).replace('\\', '/')] = style_id
    manifest['inlineTextStyles'] = [json.loads(t) for t in sorted(typography)]
    for folder in REPORTS:
        for path in (folder / 'definition').rglob('*.json'):
            relative = str(path.relative_to(ROOT)).replace('\\', '/')
            spec = manifest['styles'].get(manifest['visuals'].get(relative))
            manifest['safetyFingerprints'][relative] = invariant(read(path), spec, path.name == 'report.json')
        for path in folder.glob('*.pbir'):
            manifest['protectedFileHashes'][str(path.relative_to(ROOT)).replace('\\', '/')] = hashlib.sha256(path.read_bytes()).hexdigest()
    for path in CURRENT.rglob('*.tmdl'):
        manifest['protectedFileHashes'][str(path.relative_to(ROOT)).replace('\\', '/')] = hashlib.sha256(path.read_bytes()).hexdigest()
    # Make the new dashboard style the default for newly-created cards/charts.
    # Existing special variants select their own preset, preserving their formatting.
    board = SOURCE / 'definition/pages/5038cffdd48af9a80dd1'
    seen = set()
    for path in sorted(board.rglob('visual.json')):
        v = read(path).get('visual', {})
        kind = v.get('visualType')
        if kind not in ('cardVisual', 'clusteredColumnChart', 'clusteredBarChart', 'slicer') or kind in seen:
            continue
        style, _ = extract(v, schema)
        theme['visualStyles'].setdefault(kind, {}).setdefault('*', {}).update(style)
        seen.add(kind)
    save(THEME, theme)
    save(MANIFEST, manifest)
    print(f'Captured {len(manifest["visuals"])} visual style assignments; {len(palette)} palette colours.')


def sync():
    theme, manifest = read(THEME), read(MANIFEST)
    content_hash = hashlib.sha256(THEME.read_bytes()).hexdigest()[:32]
    resource = f'WMPP_Common_Theme-{content_hash}.json'
    changed = 0
    pending = []
    for relative, style_id in manifest['visuals'].items():
        spec = manifest['styles'][style_id]
        path = ROOT / relative
        if not path.exists():
            raise ValueError(f'Missing expected visual: {relative}')
        data = read(path)
        original = deepcopy(data)
        visual = data['visual']
        if visual['visualType'] != spec['type']:
            raise ValueError(f'Visual type changed; review style mapping: {relative}')
        if spec['preset'] not in theme['visualStyles'][spec['type']]:
            raise ValueError(f'Missing shared preset: {spec["preset"]}')
        for slot in spec['slots']:
            entries = visual.get(slot['location'], {}).get(slot['group'], [])
            # Match selector, not array offset: other saved entries may have shifted.
            candidates = [e for e in entries if e.get('selector', {}) == slot['selector']]
            if len(candidates) > 1:
                raise ValueError(f'Ambiguous style selector: {relative} {slot["group"]}')
            for entry in candidates:
                props = entry.get('properties', {})
                # Only strip the captured value. Preserve later local edits.
                if props.get(slot['property']) == slot['original']:
                    del props[slot['property']]
        for location in ('objects', 'visualContainerObjects'):
            groups = visual.get(location, {})
            for group in list(groups):
                groups[group] = [e for e in groups[group] if e.get('properties')]
                if not groups[group]:
                    del groups[group]
        visual.get('objects', {}).pop('stylePreset', None)
        visual.setdefault('visualContainerObjects', {})['stylePreset'] = [{'properties': {
            'name': {'expr': {'Literal': {'Value': "'" + spec['preset'] + "'"}}}}}]
        if data != original:
            original_preset = manifest.get('originalPresets', {}).get(relative)
            if invariant(data, spec, original_preset=original_preset) != invariant(original, spec, original_preset=original_preset):
                raise ValueError(f'Non-style content changed: {relative}')
            pending.append((path, data))
            changed += 1
    for relative in manifest['reports']:
        folder = ROOT / relative
        path = folder / 'definition/report.json'
        report = read(path)
        version = report['themeCollection'].get('customTheme', report['themeCollection']['baseTheme'])['reportVersionAtImport']
        report['themeCollection']['customTheme'] = {
            'name': resource, 'reportVersionAtImport': version, 'type': 'RegisteredResources'}
        packages = report.setdefault('resourcePackages', [])
        package = next((p for p in packages if p['name'] == 'RegisteredResources'), None)
        if package is None:
            package = {'name': 'RegisteredResources', 'type': 'RegisteredResources', 'items': []}
            packages.append(package)
        package['items'] = [i for i in package['items'] if i.get('type') != 'CustomTheme']
        package['items'].append({'name': resource, 'path': resource, 'type': 'CustomTheme'})
        pending.append((folder / 'StaticResources/RegisteredResources' / resource, theme))
        pending.append((path, report))
    for path, data in pending:
        save(path, data)
    print(f'Synced {resource} to {len(manifest["reports"])} current reports; {changed} visual files updated.')


def adopt_local_dashboard():
    """Rebase style assignments after the authorized report copy/retirement."""
    archive = ROOT / 'reports/retired/2026-09-23-local-report-consolidation'
    if not (archive / 'consolidation-receipt.json').exists():
        raise ValueError('Complete the recoverable local-report consolidation first.')
    local = 'reports/current/SM WMPP v16 updated/SM_WMPP_v16.Report'
    source = str(SOURCE.relative_to(ROOT)).replace('\\', '/')
    retired = 'reports/current/SM WMPP v16/'
    # Always derive the migration from the archived pre-copy manifest.
    manifest = read(archive / 'WMPP_Common_Theme.manifest.before.json')
    manifest['reports'] = [r for r in manifest['reports'] if not r.startswith(retired)]
    for key in ('visuals', 'safetyFingerprints', 'originalPresets'):
        existing = manifest.get(key, {})
        replacement = {p: v for p, v in existing.items()
                       if not p.startswith(retired) and not p.startswith(local + '/')}
        replacement.update({local + p[len(source):]: deepcopy(v)
                            for p, v in existing.items() if p.startswith(source + '/')})
        manifest[key] = replacement
    manifest['protectedFileHashes'] = {p: v for p, v in manifest['protectedFileHashes'].items()
                                       if not p.startswith(retired)}
    manifest['notes'].append('2026-09-23: dashboard authoring files copied into the active local report; '
                             'retired SM WMPP v16 removed from active sync scope. Prior audit manifest archived.')
    # Verify the copied content against source before updating the safety baseline.
    for path in (SOURCE / 'definition').rglob('*'):
        if path.is_file():
            target = ROOT / local / path.relative_to(SOURCE)
            if path.read_bytes() != target.read_bytes():
                raise ValueError(f'Local dashboard differs from source: {target}')
    save(MANIFEST, manifest)
    print('Theme assignments rebased to the copied local dashboard; retired project excluded.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture', action='store_true')
    parser.add_argument('--adopt-local-dashboard', action='store_true')
    args = parser.parse_args()
    if args.adopt_local_dashboard:
        adopt_local_dashboard()
    elif args.capture:
        capture()
    else:
        sync()
