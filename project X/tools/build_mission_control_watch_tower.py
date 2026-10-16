"""Add a latest-only monitoring overview while preserving calendar navigation."""
from __future__ import annotations

import argparse
import copy
import json
import pathlib
import re
import uuid

import refine_mission_control_wip as ui

GROUPS = [
    ('Domains', 'Domains & Reference', 'Profiled columns', 'cfg_data_domain', '21e0713419ffecb25e16'),
    ('Drift', 'Schema & Drift', 'Drift keys', 'cfg_schema_drift_event', 'f6a09fa981fa822fe9d9'),
    ('Contracts', 'Contracts & Schema', 'Captured columns', 'cfg_bronze_schema_live', '1780cfc720f8d4c618ae'),
    ('Quality', 'Quality & Exceptions', 'Quality rules', 'rpt_job_data_quality', '8258238ae0bb40cb8653'),
]

def latest(table, suffix):
    return f'CALCULATE([Discovery {table} {suffix}], REMOVEFILTERS())'

def fmt(expression):
    return f'FORMAT({expression}, "#,0")'

def batch(table, timestamp, predicate):
    # Match the detail page's latest retained batch, including blank run IDs.
    return f'''VAR BatchKey = {latest(table, 'Latest key')}
VAR BatchTime = {latest(table, 'Latest time')}
VAR BatchRows = FILTER(CALCULATETABLE('{table}', REMOVEFILTERS()),
    IF(ISBLANK(BatchKey), '{table}'[{timestamp}] = BatchTime,
       '{table}'[run_id] = BatchKey))
RETURN COALESCE(COUNTROWS(FILTER(BatchRows, {predicate})), 0)'''

def upsert(name, dax, number=False):
    path = ui.TABLES / '_MissionControl_Measures.tmdl'
    source = path.read_text(encoding='utf-8-sig')
    block = "\tmeasure '" + name + "' =\n" + '\n'.join('\t\t\t' + s for s in dax.strip().splitlines()) + '\n'
    if number:
        block += '\t\tformatString: #,0\n'
    block += '\t\tdisplayFolder: Watch Tower\n\t\tlineageTag: ' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'mission-control:' + name)) + '\n\n'
    pattern = r"(?ms)^\tmeasure '" + re.escape(name) + r"' =.*?(?=^\tmeasure |^\tpartition |\Z)"
    if re.search(pattern, source):
        source = re.sub(pattern, lambda _: block, source)
    else:
        at = source.index('\tpartition ')
        source = source[:at] + block + source[at:]
    path.write_text(source, encoding='utf-8')

def rename_display_text(node):
    # Formatting/visible prose only: semantic table names and query refs stay intact.
    changed = False
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, (dict, list)):
                changed = rename_display_text(value) or changed
            elif isinstance(value, str) and key in ('value', 'Value'):
                replacement = value.replace('Load Calendar', 'Watch Tower').replace('Load calendar', 'Watch Tower')
                if replacement != value:
                    node[key] = replacement
                    changed = True
    elif isinstance(node, list):
        for value in node:
            changed = rename_display_text(value) or changed
    return changed

def make_card(label, measure, x, y, width, height, size, ink):
    v = ui.card(ui.CAL, 'watch-tower-' + label, measure, x, y, width, height, size)
    # cardVisual formatting is per-card (default selector), not a global object.
    for entry in v['visual']['objects']['value']:
        entry['properties'].update(fontSize=ui.lit(f'{size}D'), fontColor=ui.color(ink))
    v.pop('filterConfig', None)
    v.pop('isHidden', None)
    return v

def build(root, backup=True):
    ui.ROOT = root
    ui.REPORT = root / 'SM WMPP Mission Control.Report'
    ui.DEF = ui.REPORT / 'definition'
    ui.PAGES = ui.DEF / 'pages'
    ui.TABLES = root / 'SM WMPP Mission Control.SemanticModel/definition/tables'
    ui.TEXT_TEMPLATE = ui.visual(ui.CAL, '8335a1c4e82d9ae351c3')
    ui.PANEL_TEMPLATE = ui.visual(ui.CAL, 'fa3abf7e2ce8b2d29b4d')
    ui.CARD_TEMPLATE = ui.visual(ui.CAL, '43756e2036440b35a2a4')
    ui.BUTTON_TEMPLATE = ui.visual(ui.CAL, '89bfad1ebbda3675c1c3')
    if backup:
        ui.backup()

    manifest_path = root / 'Watch Tower revision.json'
    previous = ui.load(manifest_path) if manifest_path.exists() else None
    page_path = ui.PAGES / ui.CAL / 'page.json'
    page = ui.load(page_path)
    original_positions = previous['originalPositions'] if previous else {
        p.parent.name: ui.load(p)['position'] for p in (ui.PAGES / ui.CAL / 'visuals').glob('*/visual.json')}
    original_height = previous['originalHeight'] if previous else page['height']
    offset = 244
    for vid, position in original_positions.items():
        v = ui.visual(ui.CAL, vid)
        v['position'] = copy.deepcopy(position)
        if position['y'] >= 147:
            v['position']['y'] += offset
        ui.put(ui.CAL, v)
    page['displayName'] = 'Watch Tower'
    page['height'] = original_height + offset

    expressions = {
        'Watch Tower Drift Active': batch('cfg_schema_drift_event', 'detected_at', 'UPPER(cfg_schema_drift_event[status]) IN {"ACTIVE", "OPEN", "NEW", "DETECTED", "PENDING"}'),
        'Watch Tower Quality Failed Checks': batch('rpt_job_data_quality', 'checked_at', 'rpt_job_data_quality[failed_row_count] > 0 || UPPER(rpt_job_data_quality[status]) IN {"FAIL", "FAILED", "ERROR"}'),
    }
    details = {
        'Domains': fmt(latest('cfg_data_domain', 'Distinct objects')) + ' & " tables · " & ' + fmt(latest('cfg_data_domain', 'Rows')) + ' & " retained values"',
        'Drift': fmt(latest('cfg_schema_drift_event', 'Distinct objects')) + ' & " target tables · " & ' + fmt('[Watch Tower Drift Active]') + ' & " active keys"',
        'Contracts': fmt(latest('cfg_bronze_schema_live', 'Distinct objects')) + ' & " captured tables · " & ' + fmt(latest('cfg_schema_contract_column', 'Rows')) + ' & " contract columns"',
        'Quality': fmt(latest('rpt_job_data_quality', 'Rows')) + ' & " checks · " & ' + fmt('[Watch Tower Quality Failed Checks]') + ' & " failed"',
    }
    extras = {
        'Domains': fmt('CALCULATE(COUNTROWS(cfg_location_coordinate), REMOVEFILTERS())') + ' & " coordinate references · current"',
        'Drift': fmt(latest('cfg_schema_drift_definition', 'Rows')) + ' & " definitions · " & ' + fmt(latest('cfg_schema_definition_candidate', 'Rows')) + ' & " current candidates"',
        'Contracts': 'VAR t = ' + latest('cfg_schema_contract_column', 'Latest time') + '\nRETURN IF(ISBLANK(t), "No dated contract capture", "Contract: " & FORMAT(t, "dd MMM yyyy HH:mm"))',
        'Quality': fmt(latest('cfg_rejected_row', 'Rows')) + ' & " rejected (" & FORMAT(' + latest('cfg_rejected_row', 'Latest time') + ', "dd MMM") & ") · " & ' + fmt(latest('cfg_referential_exception', 'Rows')) + ' & " FK exceptions (" & FORMAT(' + latest('cfg_referential_exception', 'Latest time') + ', "dd MMM") & ")"',
    }
    captions = {'Domains': 'Profiled', 'Drift': 'Detected', 'Contracts': 'Schema captured', 'Quality': 'Quality checked'}
    for key, title, unit, table, target in GROUPS:
        expressions[f'Watch Tower {key} Count'] = latest(table, 'Scope count')
        expressions[f'Watch Tower {key} Detail'] = details[key]
        expressions[f'Watch Tower {key} Reference'] = extras[key]
        expressions[f'Watch Tower {key} Date'] = 'VAR t = ' + latest(table, 'Latest time') + '\nRETURN IF(ISBLANK(t), "No retained discovery", "' + captions[key] + ': " & FORMAT(t, "dd MMM yyyy HH:mm"))'
    for name, expression in expressions.items():
        upsert(name, expression, name.endswith('Count') or name.endswith('Active') or name.endswith('Checks'))

    new_cards = []
    navigation = []
    for i, (key, title, unit, table, target) in enumerate(GROUPS):
        x = 36 + i * 408
        panel = ui.panel(ui.CAL, 'watch-tower-' + key + '-panel', x, 147, 384, 222)
        panel['position']['z'] = 6000
        panel['position']['tabOrder'] = 6000
        ui.put(ui.CAL, panel)
        ui.put(ui.CAL, ui.textbox(ui.CAL, 'watch-tower-' + key + '-title', title, x + 18, 162, 309, 28, 17, ui.TEXT, True))
        for suffix, y, h, size, ink in [('Count', 198, 55, 32, ui.TEXT), ('Detail', 275, 24, 11, ui.TEXT), ('Reference', 301, 24, 10, ui.MUTED), ('Date', 339, 21, 10, ui.MUTED)]:
            v = make_card(key + '-' + suffix, f'Watch Tower {key} {suffix}', x + 18, y, 348, h, size, ink)
            ui.put(ui.CAL, v)
            new_cards.append(v['name'])
        ui.put(ui.CAL, ui.textbox(ui.CAL, 'watch-tower-' + key + '-unit', unit, x + 18, 255, 348, 19, 12, ui.MUTED))
        button = ui.button(ui.CAL, 'watch-tower-' + key + '-open', '→', x + 335, 159, 36, 32, 'PageNavigation', target)
        ui.props(button['visual']['visualContainerObjects'], 'visualLink')['tooltip'] = ui.string('Open ' + title)
        ui.put(ui.CAL, button)
        navigation.append({'page': title, 'target': target, 'visual': button['name']})

    # Latest summaries deliberately ignore all slicers, calendars and row selections.
    sources = ['e263e453f96be0512a19', '52b0db0e9f2a1ebfb85e', '3b28a42eb9ca129a560e', 'fe821948e1b3b2425852', '5c55c8df64c46f54fa93', '91a7abd13be1fc90f248']
    pairs = {(s, t) for s in sources for t in new_cards}
    page['visualInteractions'] = [v for v in page.get('visualInteractions', []) if (v['source'], v['target']) not in pairs]
    page['visualInteractions'] += [{'source': s, 'target': t, 'type': 'NoFilter'} for s, t in sorted(pairs)]
    ui.save(page_path, page)
    v = ui.visual(ui.CAL, '8335a1c4e82d9ae351c3')
    ui.texts(v)[0]['value'] = 'Watch Tower'
    ui.put(ui.CAL, v)
    v = ui.visual(ui.CAL, 'eccc8b5a690c7caffdfb')
    ui.texts(v)[0]['value'] = 'Latest discoveries across the four monitoring areas. Choose a calendar day below to inspect loads and open its job timelines.'
    ui.put(ui.CAL, v)
    for p in (ui.PAGES / ui.CAL / 'visuals').glob('*/visual.json'):
        v = ui.load(p)
        if v['position']['y'] == 22 and v['visual']['visualType'] == 'textbox':
            ui.texts(v)[0]['value'] = 'MISSION CONTROL / WATCH TOWER'
            ui.save(p, v)
    # Update visible return links and guides, preserving semantic identities.
    renamed_visuals = []
    for p in ui.PAGES.glob('*/visuals/*/visual.json'):
        v = ui.load(p)
        changed = rename_display_text(v['visual'].get('objects', {}))
        changed = rename_display_text(v['visual'].get('visualContainerObjects', {})) or changed
        if changed:
            ui.save(p, v)
            renamed_visuals.append(str(p.relative_to(root)))
    guide_path = ui.PAGES / 'faff55cdb2ebf5436d8d' / 'page.json'
    guide = ui.load(guide_path)
    guide['displayName'] = 'Watch Tower - guide'
    ui.save(guide_path, guide)
    v = ui.visual('faff55cdb2ebf5436d8d', 'a7aedc610c28e34762c9')
    ui.texts(v)[0]['value'] = 'Overview cards use the latest retained discovery per source; dates can differ. Arrows open detail pages. Below, select a calendar day, then Open day timelines to carry the day and pipeline into Job & Step Timelines.'
    ui.put('faff55cdb2ebf5436d8d', v)
    # The calendar section retains its name as an activity widget.
    v = ui.visual(ui.CAL, '489e984aa0a980a7e8cd')
    ui.texts(v)[0]['value'] = 'Load activity'
    ui.put(ui.CAL, v)
    ui.save(manifest_path, {'pageId': ui.CAL, 'displayName': 'Watch Tower', 'writtenMeasures': list(expressions),
        'originalPositions': original_positions, 'originalHeight': original_height, 'offset': offset,
        'summaryCardIds': new_cards, 'navigation': navigation, 'renamedVisuals': renamed_visuals,
        'latestScope': 'Latest cached cohort per source, independent of calendar or slicer context',
        'sourceRefresh': 'None'})
    # DEFINE lets the prepared formulas be verified against the existing cache before deployment.
    query = 'DEFINE\n' + '\n'.join("MEASURE '_MissionControl_Measures'[" + name + '] = ' + dax for name, dax in expressions.items())
    checks = []
    for key, title, unit, table, target in GROUPS:
        name = f'Watch Tower {key} Count'
        expected = latest(table, 'Scope count')
        # Probe both a retained historical day and an empty day, plus conflicting field filters.
        for label, filters in [('Default', ''), ('Historical', ", TREATAS({DATE(2026, 8, 24)}, 'Load Calendar'[Date])"), ('Empty', ", TREATAS({DATE(2026, 1, 1)}, 'Load Calendar'[Date])"), ('Conflicting table', f", TREATAS({{\"__no_such_value__\"}}, '{table}'[" + ('table_name' if key == 'Contracts' else 'source_table') + '])'), ('Unknown job', ", TREATAS({\"__no_such_job__\"}, 'Discovery Job Runs'[job_run_id])")]:
            actual = '[' + name + ']' if not filters else 'CALCULATE([' + name + ']' + filters + ')'
            checks.append('ROW("Area", "' + title + '", "Case", "' + label + '", "Actual", ' + actual + ', "Expected", ' + expected + ', "Pass", ' + actual + ' = ' + expected + ')')
    query += '\nEVALUATE UNION(\n' + ',\n'.join(checks) + '\n)\n'
    (root / 'Watch Tower prepared checks.dax').write_text(query, encoding='utf-8')
    print('Prepared Watch Tower: 4 latest summaries, 18 measures, preserved calendar/drillthrough IDs and interactions.')

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--project-root', type=pathlib.Path, required=True)
    args.add_argument('--no-backup', action='store_true')
    options = args.parse_args()
    build(options.project_root, not options.no_backup)
