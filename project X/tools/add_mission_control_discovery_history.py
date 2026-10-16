"""Add retained domain versions and per-object load comparisons to the current WIP."""
from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import re
import uuid
import zipfile

import build_mission_control_discovery_pages as build
import refine_mission_control_wip as ui
import reorient_mission_control_change_calendars as calendar

DOMAIN_PAGE = '21e0713419ffecb25e16'
LOAD_PAGE = 'a6e477aeb12bf82f951a'
DOMAIN = 'cfg_data_domain'
METRIC = 'cfg_table_load_metric'
MEASURES = '_MissionControl_Measures'


def save_json(path, value):
    # Keep the current report's compact JSON format and unrelated visuals intact.
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, separators=(',', ':')) + '\n',
                    encoding='utf-8')


def add_columns():
    path = ui.TABLES / 'cfg_data_domain.tmdl'
    text = path.read_text(encoding='utf-8-sig')
    fields = [('previous_run_id', 'string'), ('previous_profiled_at', 'dateTime'),
              ('change_type', 'string'), ('is_present', 'boolean'), ('profile_status', 'string')]
    for name, kind in fields:
        if re.search(r'^\tcolumn ' + name + r'\s*$', text, re.M):
            continue
        block = (f'\tcolumn {name}\n\t\tdataType: {kind}\n\t\tsummarizeBy: none\n'
                 f'\t\tsourceColumn: {name}\n\t\tlineageTag: '
                 f'{uuid.uuid5(uuid.NAMESPACE_URL, "discovery-history:" + name)}\n\n')
        text = text.replace('\tpartition ', block + '\tpartition ', 1)
    if "\tcolumn 'Value change' =" not in text:
        block = '''\tcolumn 'Value change' = COALESCE(cfg_data_domain[change_type], IF(ISBLANK(cfg_data_domain[data_domain]), COALESCE(cfg_data_domain[profile_status], "EMPTY"), "BASELINE"))
\t\tdataType: string
\t\tsummarizeBy: none
\t\tlineageTag: ''' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'discovery-history:value-change')) + '\n\n'
        text = text.replace('\tpartition ', block + '\tpartition ', 1)
    if "\tcolumn 'Present in version' =" not in text:
        block = '''\tcolumn 'Present in version' = COALESCE(cfg_data_domain[is_present], NOT ISBLANK(cfg_data_domain[data_domain]))
\t\tdataType: boolean
\t\tsummarizeBy: none
\t\tlineageTag: ''' + str(uuid.uuid5(uuid.NAMESPACE_URL, 'discovery-history:present')) + '\n\n'
        text = text.replace('\tpartition ', block + '\tpartition ', 1)
    path.write_text(text, encoding='utf-8')
    mode_path = ui.TABLES / 'Domain History View.tmdl'
    if not mode_path.exists():
        mode_path.write_text('''table 'Domain History View'
\tlineageTag: 8c8d3552-bc5c-56d9-9bbd-7a7ad46cc870

\tcolumn Mode
\t\tdataType: string
\t\tsourceColumn: [Mode]
\t\tsummarizeBy: none
\t\tlineageTag: cdd53d99-d443-5323-a5e4-c958cc185f99

\tpartition 'Domain History View' = calculated
\t\tmode: import
\t\tsource = DATATABLE("Mode", STRING, {{"Latest version"}, {"All retained versions"}})
''', encoding='utf-8')
    model_path = ui.TABLES.parent / 'model.tmdl'
    model = model_path.read_text(encoding='utf-8-sig')
    if "ref table 'Domain History View'" not in model:
        model += "\nref table 'Domain History View'\n"
        model_path.write_text(model, encoding='utf-8')
    # Job identity should come from the authoritative log, including standalone profiles.
    job_path = ui.TABLES / 'Discovery Job Runs.tmdl'
    job = job_path.read_text(encoding='utf-8-sig')
    job = job.replace('Item="rpt_job_run_summary"', 'Item="cfg_job_run"')
    job_path.write_text(job, encoding='utf-8')


def domain_scope(expression):
    return f'''VAR DateChosen=ISFILTERED('Load Calendar'[Date])
VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
VAR Days=VALUES('Load Calendar'[Date])
VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
VAR LatestKey=[Discovery cfg_data_domain Latest key]
VAR LatestTime=[Discovery cfg_data_domain Latest time]
RETURN IF(DateChosen || JobChosen || AllVersions,
    CALCULATE({expression},KEEPFILTERS(FILTER(cfg_data_domain,
        (NOT DateChosen || INT(cfg_data_domain[profiled_at]) IN Days)
        && (NOT JobChosen || cfg_data_domain[job_run_id] IN Jobs)))),
    IF(ISBLANK(LatestKey),
        CALCULATE({expression},KEEPFILTERS(TREATAS({{LatestTime}},cfg_data_domain[profiled_at]))),
        CALCULATE({expression},KEEPFILTERS(TREATAS({{LatestKey}},cfg_data_domain[run_id])))))'''


def domain_measures():
    expressions = {
        'Rows': 'COUNTROWS(cfg_data_domain)',
        'Scope count': 'COUNTROWS(SUMMARIZE(FILTER(cfg_data_domain,COALESCE(cfg_data_domain[profile_status],"PROFILED") IN {"PROFILED","EMPTY"}),cfg_data_domain[source_schema],cfg_data_domain[source_table],cfg_data_domain[column_name]))',
        'Distinct objects': 'DISTINCTCOUNT(cfg_data_domain[source_table])',
        'Discovery batches': 'DISTINCTCOUNT(cfg_data_domain[run_id])',
        'Selected time': 'MAX(cfg_data_domain[profiled_at])',
    }
    for suffix, expression in expressions.items():
        scoped = domain_scope(expression)
        if suffix != 'Selected time':
            scoped = 'COALESCE((' + scoped + '),0)'
        build.measure(build.name(DOMAIN, suffix), scoped,
                      'dd MMM yyyy HH:mm' if suffix == 'Selected time' else '#,0')
    for label, change in [('Added', 'ADDED'), ('Removed', 'REMOVED')]:
        scoped = domain_scope(f'COUNTROWS(FILTER(cfg_data_domain,cfg_data_domain[change_type]="{change}"))')
        build.measure('Domain values ' + label, 'COALESCE((' + scoped + '),0)', '#,0')
    build.measure('Domain value changes',
                  '"Added " & FORMAT(COALESCE([Domain values Added],0),"#,0") & " · Removed " & FORMAT(COALESCE([Domain values Removed],0),"#,0")')
    build.measure('Discovery cfg_data_domain Visible',
                  'IF([Discovery cfg_data_domain Rows]>0,1,0)', '0')
    build.measure('Discovery domains calendar changes', calendar.activity_dax([
        calendar.source(DOMAIN, ['profiled_at'], 'cfg_data_domain[change_type] IN {"ADDED","REMOVED"}')
    ]), '#,0')
    build.measure('Discovery cfg_data_domain Context', '''VAR Historical=[Discovery history selected]=1
VAR AllVersions=SELECTEDVALUE('Domain History View'[Mode],"Latest version")="All retained versions"
RETURN IF(Historical,"Selected discovery history",IF(AllVersions,"All retained discovery versions",
    "Latest discovery · " & FORMAT([Discovery cfg_data_domain Latest time],"dd MMM yyyy HH:mm")))''')


def metric_context():
    return f'''VAR ThisTime=SELECTEDVALUE({METRIC}[recorded_at])
VAR ThisRun=SELECTEDVALUE({METRIC}[run_id])
VAR ThisLayer=SELECTEDVALUE({METRIC}[layer])
VAR ThisKind=SELECTEDVALUE({METRIC}[source_kind])
VAR ThisSource=SELECTEDVALUE({METRIC}[source_object])
VAR ThisTarget=SELECTEDVALUE({METRIC}[target_object])
VAR History=FILTER(ALL({METRIC}),
    {METRIC}[layer]=ThisLayer && {METRIC}[source_kind]=ThisKind
    && {METRIC}[source_object]=ThisSource && {METRIC}[target_object]=ThisTarget)
'''


def load_measures():
    names = []
    for label, column in [('Read', 'rows_read'), ('Written', 'rows_written')]:
        prefix = 'Load Rows ' + label
        previous = prefix + ' Previous'
        delta = prefix + ' Delta'
        pct = prefix + ' Delta %'
        spark = prefix + ' Sparkline'
        build.measure(previous, metric_context() + f'''
VAR Prior=TOPN(1,FILTER(History,({METRIC}[recorded_at]<ThisTime || ({METRIC}[recorded_at]=ThisTime && {METRIC}[run_id]<ThisRun))),
    {METRIC}[recorded_at],DESC,{METRIC}[run_id],DESC)
RETURN IF(NOT ISBLANK(ThisTime),MAXX(Prior,{METRIC}[{column}]))''', '#,0')
        build.measure(delta, f'''VAR CurrentCount=SELECTEDVALUE({METRIC}[{column}])
VAR PreviousCount=[{previous}]
RETURN IF(NOT ISBLANK(CurrentCount) && NOT ISBLANK(PreviousCount),CurrentCount-PreviousCount)''', '+#,0;-#,0;0')
        build.measure(pct, f'DIVIDE([{delta}],[{previous}])', '+0.0%;-0.0%;0.0%')
        build.measure(spark, metric_context() + f'''
VAR Points=SUMMARIZE(FILTER(History,NOT ISBLANK({METRIC}[{column}])
    && ({METRIC}[recorded_at]<ThisTime || ({METRIC}[recorded_at]=ThisTime && {METRIC}[run_id]<=ThisRun))),
    {METRIC}[recorded_at],{METRIC}[run_id],"LoadValue",MAX({METRIC}[{column}]))
VAR TrendWindow=TOPN(12,Points,{METRIC}[recorded_at],DESC,{METRIC}[run_id],DESC)
VAR N=COUNTROWS(TrendWindow)
VAR Low=MINX(TrendWindow,[LoadValue])
VAR High=MAXX(TrendWindow,[LoadValue])
VAR Indexed=ADDCOLUMNS(TrendWindow,"PointIndex",
    VAR T={METRIC}[recorded_at] VAR R={METRIC}[run_id]
    RETURN COUNTROWS(FILTER(TrendWindow,{METRIC}[recorded_at]<T
        || ({METRIC}[recorded_at]=T && {METRIC}[run_id]<R))))
VAR XY=CONCATENATEX(Indexed,
    FORMAT(4+112*DIVIDE([PointIndex],MAX(1,N-1)),"0.0","en-US") & "," &
    FORMAT(IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)),"0.0","en-US"),
    " ",[PointIndex],ASC)
VAR LastPoint=TOPN(1,Indexed,[PointIndex],DESC)
VAR EndX=IF(N=1,4,116)
VAR EndY=MAXX(LastPoint,IF(High=Low,14,25-22*DIVIDE([LoadValue]-Low,High-Low)))
RETURN IF(N>0 && NOT ISBLANK(ThisTime),
    "data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='120' height='28' viewBox='0 0 120 28'><polyline fill='none' stroke='%23CBF576' stroke-width='2' points='" & XY & "'/><circle fill='%23CBF576' r='2.5' cx='" & FORMAT(EndX,"0.0","en-US") & "' cy='" & FORMAT(EndY,"0.0","en-US") & "'/></svg>")''')
        names += [previous, delta, pct, spark]
    path = ui.TABLES / (MEASURES + '.tmdl')
    text = path.read_text(encoding='utf-8-sig')
    for name in (n for n in names if n.endswith('Sparkline')):
        pattern = r"(?ms)(^\tmeasure '" + re.escape(name) + r"' =.*?)(?=^\tmeasure |^\tpartition |\Z)"
        text = re.sub(pattern, lambda m: m.group(1).replace(
            '\t\tdisplayFolder:', '\t\tdataCategory: ImageUrl\n\t\tdisplayFolder:'), text)
    path.write_text(text, encoding='utf-8')
    return names


def replace_text(pid, label, value):
    visual = ui.visual(pid, ui.sid(pid + ':' + label))
    ui.texts(visual)[0]['value'] = value
    save_json(ui.path(pid, visual['name']), visual)


def update_visuals():
    replace_text(DOMAIN_PAGE, 'intro', 'Each discovery retains a version. Compare added and removed values, or choose All retained versions to inspect the full history.')
    replace_text(DOMAIN_PAGE, 'table-note:' + DOMAIN, 'BASELINE = first retained observation · ADDED / REMOVED compare the previous complete profile · skipped scans do not imply removals.')
    domain = ui.visual(DOMAIN_PAGE, ui.sid(DOMAIN_PAGE + ':register:' + DOMAIN))
    order = ['source_schema', 'source_table', 'column_name', 'data_domain', 'Value change',
             'Present in version', 'distinct_value_count', 'profile_status', 'profiled_at',
             'previous_profiled_at', 'run_id', 'previous_run_id', 'job_run_id', 'contract_data_type']
    domain['visual']['query']['queryState']['Values']['projections'] = [
        ui.projection(DOMAIN, name, 'Column') for name in order]
    save_json(ui.path(DOMAIN_PAGE, domain['name']), domain)
    for path in (ui.PAGES / DOMAIN_PAGE / 'visuals').glob('*/visual.json'):
        visual = ui.load(path)
        if visual['visual']['visualType'] != 'slicer':
            continue
        items = visual['visual'].get('query', {}).get('queryState', {}).get('Values', {}).get('projections', [])
        for item in items:
            field = item['field'].get('Column', {})
            if field.get('Expression', {}).get('SourceRef', {}).get('Entity') == DOMAIN:
                name = field['Property']
                if name in ['source_schema', 'source_table', 'column_name']:
                    i = ['source_schema', 'source_table', 'column_name'].index(name)
                    ui.pos(visual, 36 + i * 408, 594, 384, 63)
                    save_json(path, visual)
    change = build.slicer(DOMAIN_PAGE, 'Value change · Data domains', DOMAIN, 'Value change',
                          1260, 594, 384, 63)
    save_json(ui.path(DOMAIN_PAGE, change['name']), change)
    job = ui.visual(DOMAIN_PAGE, ui.sid(DOMAIN_PAGE + ':filter:Job ID · historical selection'))
    ui.pos(job, 1120, 339, 502, 54)
    save_json(ui.path(DOMAIN_PAGE, job['name']), job)
    mode = build.slicer(DOMAIN_PAGE, 'Version view', 'Domain History View', 'Mode',
                        1120, 395, 502, 52)
    ui.props(mode['visual']['objects'], 'selection')['singleSelect'] = ui.lit('true')
    save_json(ui.path(DOMAIN_PAGE, mode['name']), mode)
    changes = ui.card(DOMAIN_PAGE, 'value-changes', 'Domain value changes', 869, 549, 350, 23, 12)
    save_json(ui.path(DOMAIN_PAGE, changes['name']), changes)
    for path in (ui.PAGES / DOMAIN_PAGE / 'visuals').glob('*/visual.json'):
        visual = ui.load(path)
        items = visual['visual'].get('query', {}).get('queryState', {}).get('Data', {}).get('projections', [])
        if any(item['field'].get('Measure', {}).get('Property') == 'Discovery cfg_data_domain Rows'
               for item in items):
            visual['position']['height'] = 36
            save_json(path, visual)
    # Keep the new domain controls out of the coordinate-reference tab.
    for path in (ui.DEF / 'bookmarks').glob('*.bookmark.json'):
        bookmark = ui.load(path)
        section = bookmark.get('explorationState', {}).get('sections', {}).get(DOMAIN_PAGE)
        if not section or domain['name'] not in section.get('visualContainers', {}):
            continue
        hidden = section['visualContainers'][domain['name']]['singleVisual'].get('display', {}).get('mode') == 'hidden'
        for visual in (changes, mode, change):
            targets = bookmark['options']['targetVisualNames']
            if visual['name'] not in targets:
                targets.append(visual['name'])
            single = {'visualType': visual['visual']['visualType'], 'objects': {}}
            if hidden:
                single['display'] = {'mode': 'hidden'}
            section['visualContainers'][visual['name']] = {'singleVisual': single}
        save_json(path, bookmark)
    return changes, mode, change


def apply(root):
    calendar.configure(root)
    ui.TEXT_TEMPLATE = ui.visual(ui.CAL, '8335a1c4e82d9ae351c3')
    ui.PANEL_TEMPLATE = ui.visual(ui.CAL, 'fa3abf7e2ce8b2d29b4d')
    ui.CARD_TEMPLATE = ui.visual(ui.CAL, '43756e2036440b35a2a4')
    ui.BUTTON_TEMPLATE = ui.visual(ui.CAL, '89bfad1ebbda3675c1c3')
    backup = root.parent / '_backups' / ('discovery-history-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.zip')
    backup.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as archive:
        for directory in (ui.DEF, ui.TABLES.parent):
            for path in directory.rglob('*'):
                if path.is_file():
                    archive.write(path, path.relative_to(root))
    add_columns()
    domain_measures()
    load_names = load_measures()
    measure_path = ui.TABLES / (MEASURES + '.tmdl')
    measure_path.write_text(measure_path.read_text(encoding='utf-8-sig').replace(
        ' retained values"', ' snapshot records"'), encoding='utf-8')
    update_visuals()
    metric = ui.visual(LOAD_PAGE, ui.sid(LOAD_PAGE + ':register:' + METRIC))
    projections = []
    for projection in metric['visual']['query']['queryState']['Values']['projections']:
        if 'Column' not in projection['field']:
            continue
        projections.append(projection)
        name = projection['field']['Column']['Property']
        if name in {'rows_read', 'rows_written'}:
            label = 'Read' if name == 'rows_read' else 'Written'
            for suffix, title in [('Delta', 'Δ ' + label.lower()), ('Delta %', 'Δ ' + label.lower() + ' %'),
                                  ('Sparkline', label + ' · last 12 loads')]:
                projections.append(ui.projection(MEASURES, 'Load Rows ' + label + ' ' + suffix,
                                                  label=title))
    metric['visual']['query']['queryState']['Values']['projections'] = projections
    ui.props(metric['visual']['objects'], 'grid')['imageHeight'] = ui.lit('28D')
    save_json(ui.path(LOAD_PAGE, metric['name']), metric)
    replace_text(LOAD_PAGE, 'intro', 'Compare each load with the preceding load of the same layer, source kind and object. Sparklines show up to 12 retained loads.')
    replace_text(LOAD_PAGE, 'table-note:' + METRIC, 'Δ compares the preceding retained load for this object, even when viewing a historical day. Blank = no prior load; % is blank when the prior count is zero. Each sparkline has its own scale.')
    save_json(root / 'Discovery history revision.json', {
        'project': str(root), 'backup': str(backup), 'domainHistory': 'Append-only snapshots; no fabricated history',
        'domainVersionSelector': ['Latest version', 'All retained versions'],
        'loadMeasures': load_names, 'sparklinePoints': 12, 'sourceRefresh': 'Not performed',
        'deployment': ['00_setup_cfg', '99_common_library', '99_data_domain', 'Refresh the updated semantic model'],
    })
    print(json.dumps({'project': str(root), 'backup': str(backup), 'loadMeasures': len(load_names)}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--project-root', type=Path, required=True)
    args = parser.parse_args()
    apply(args.project_root.resolve())
