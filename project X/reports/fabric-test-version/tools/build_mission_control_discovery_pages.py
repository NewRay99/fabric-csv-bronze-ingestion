"""Group newly added monitoring tables into latest-first discovery pages."""
from __future__ import annotations

import copy
import json
import pathlib
import re
import uuid

import refine_mission_control_wip as ui

GROUPS = [
    dict(key='domains', title='Domains & Reference', headline='Discover the values. Understand the scope.',
         intro='Latest retained data-domain discovery, with current coordinate reference data. Choose a historical day and job to inspect retained results.',
         tables=['cfg_data_domain', 'cfg_location_coordinate'],
         labels=['Data domains', 'Coordinate reference'],
         filters=['source_schema', 'source_table', 'column_name'],
         metric=('Profiled columns', ['source_schema', 'source_table', 'column_name']),
         distinct=('Source tables', 'source_table')),
    dict(key='drift', title='Schema & Drift', headline='Find the change. Trace its impact.',
         intro='Latest drift discovery and job context, alongside current definitions and candidates. Calendar selection follows retained job-run evidence.',
         tables=['cfg_schema_drift_event', 'rpt_job_schema_drift', 'cfg_schema_drift_definition', 'cfg_schema_definition_candidate'],
         labels=['Drift events', 'Job drift context', 'Drift definitions', 'Schema candidates'],
         filters=['source_table', 'drift_type', 'status'],
         metric=('Drift keys', ['drift_key']), distinct=('Target tables', 'target_table')),
    dict(key='contracts', title='Contracts & Schema', headline='See the structure. Check the contract.',
         intro='Latest captured Bronze schema and current schema contract. Contract snapshots without job lineage remain explicitly separate from historical job selections.',
         tables=['cfg_bronze_schema_live', 'cfg_schema_contract_column'],
         labels=['Bronze schema', 'Schema contract'],
         filters=['table_name', 'column_name', 'live_data_type'],
         metric=('Captured columns', ['table_name', 'column_name']), distinct=('Captured tables', 'table_name')),
    dict(key='quality', title='Quality & Exceptions', headline='Inspect the finding. Follow the exception.',
         intro='Latest quality discovery, rejected keys and referential exceptions. Historical selections show only retained records belonging to the chosen jobs.',
         tables=['rpt_job_data_quality', 'cfg_rejected_row', 'cfg_referential_exception'],
         labels=['Quality findings', 'Rejected rows', 'Referential exceptions'],
         filters=['source_table', 'severity', 'status'],
         metric=('Quality rules', ['rule_id']), distinct=('Source tables', 'source_table')),
    dict(key='loads', title='Load Metrics & Control', headline='Count the rows. Inspect the load.',
         intro='Latest table metrics, Silver exports and load control. Select a historical day and job to follow recorded volumes and load outcomes.',
         tables=['cfg_table_load_metric', 'cfg_silver_export_load', 'cfg_silver_load_control'],
         labels=['Table load metrics', 'Silver export loads', 'Silver load control'],
         filters=['layer', 'source_object', 'target_object'],
         metric=('Target objects', ['target_object']), distinct=('Source objects', 'source_object')),
    dict(key='lineage', title='Lineage & Step Summary', headline='Follow the lineage. Review the steps.',
         intro='Latest observed layer lineage and step summary, with the current Gold mapping. Current mappings do not record historical job snapshots.',
         tables=['rpt_job_layer_lineage', 'rpt_job_step_summary', 'cfg_gold_lineage_mapping'],
         labels=['Layer lineage', 'Job step summary', 'Gold lineage mapping'],
         filters=['source_layer', 'target_layer', 'target_object'],
         metric=('Target objects', ['target_layer', 'target_object']), distinct=('Source objects', 'source_object')),
]

DATES = {
    'cfg_data_domain': 'profiled_at', 'cfg_schema_drift_event': 'detected_at',
    'rpt_job_schema_drift': 'last_detected_at', 'cfg_schema_drift_definition': 'definition_loaded_at',
    'cfg_bronze_schema_live': 'captured_at', 'cfg_schema_contract_column': 'contract_loaded_at',
    'rpt_job_data_quality': 'checked_at', 'cfg_rejected_row': 'rejected_at',
    'cfg_referential_exception': 'detected_at', 'cfg_table_load_metric': 'recorded_at',
    'cfg_silver_export_load': 'started_at', 'cfg_silver_load_control': 'started_at',
    'rpt_job_layer_lineage': 'observed_at', 'rpt_job_step_summary': 'started_at',
}

# Put identifiers after the operational columns; every source field remains
# available in the register, including the discovery and job/run provenance.
PRIORITY = {
    'cfg_data_domain': ['source_schema', 'source_table', 'column_name', 'contract_data_type', 'data_domain', 'distinct_value_count', 'profiled_at'],
    'cfg_location_coordinate': ['location_type', 'location_key', 'latitude', 'longitude', 'reference_source', 'reference_version'],
    'cfg_schema_drift_event': ['source_table', 'target_table', 'column_name', 'drift_type', 'expected_type', 'actual_type', 'status', 'detected_at', 'occurrence_count'],
    'rpt_job_schema_drift': ['source_table', 'target_table', 'column_name', 'drift_type', 'status', 'expected_type', 'actual_type', 'last_detected_at', 'definition_match_found'],
    'cfg_schema_drift_definition': ['table_name', 'column_name', 'data_type', 'is_nullable', 'join_class', 'definition_loaded_at', 'definition_hash'],
    'cfg_schema_definition_candidate': ['table_name', 'column_name', 'data_type', 'is_nullable', 'is_primary_key', 'referenced_table', 'referenced_column'],
    'cfg_bronze_schema_live': ['table_name', 'column_name', 'ordinal_position', 'live_data_type', 'is_nullable', 'captured_at'],
    'cfg_schema_contract_column': ['table_name', 'column_name', 'data_type', 'is_nullable', 'is_primary_key', 'referenced_table', 'referenced_column', 'contract_loaded_at'],
    'rpt_job_data_quality': ['source_table', 'column_name', 'rule_id', 'severity', 'status', 'checked_row_count', 'failed_row_count', 'failure_percentage', 'rejected_key_count', 'referential_exception_count', 'checked_at', 'message'],
    'cfg_rejected_row': ['source_table', 'rule_id', 'rejection_reason', 'business_key_json', 'rejected_at'],
    'cfg_referential_exception': ['child_table', 'child_column', 'child_key', 'parent_table', 'parent_column', 'rule_id', 'detected_at'],
    'cfg_table_load_metric': ['layer', 'source_object', 'target_object', 'rows_read', 'rows_written', 'duplicate_key_count', 'null_primary_key_count', 'recorded_at'],
    'cfg_silver_export_load': ['source_table', 'target_table', 'status', 'rows_read', 'rows_written', 'duplicate_key_count', 'started_at', 'ended_at', 'error_message'],
    'cfg_silver_load_control': ['source_table', 'target_table', 'status', 'rows_read', 'rows_written', 'missing_column_count', 'extra_column_count', 'started_at', 'ended_at', 'error_message'],
    'rpt_job_layer_lineage': ['source_layer', 'source_object', 'target_layer', 'target_object', 'lineage_stage', 'lineage_status', 'rows_read', 'rows_written', 'observed_at', 'relationship_role'],
    'rpt_job_step_summary': ['notebook_name', 'step_sequence', 'status', 'started_at', 'ended_at', 'step_duration_seconds', 'gap_from_previous_step_seconds', 'pipeline_rows_read', 'pipeline_rows_written', 'dq_checks_failed', 'active_drift_count', 'error_message'],
    'cfg_gold_lineage_mapping': ['gold_object', 'source_object', 'source_layer', 'transformation_notebook', 'relationship_role', 'is_required', 'description'],
}

def name(table, suffix):
    return f'Discovery {table} {suffix}'

def columns(table):
    source = (ui.TABLES/(table+'.tmdl')).read_text(encoding='utf-8-sig')
    return {m.group(1).strip("'"): m.group(2) for m in re.finditer(r'^\tcolumn (.+)\n\t\tdataType: (\w+)', source, re.M)}

def measure(measure_name, dax, fmt=None):
    # Reapplying only this builder preserves user table additions and report
    # edits; updates replace only these measures' expression blocks.
    path = ui.TABLES/'_MissionControl_Measures.tmdl'
    text = path.read_text(encoding='utf-8-sig')
    pattern = r"(?ms)^\tmeasure '"+re.escape(measure_name)+r"' =.*?(?=^\tmeasure |^\tpartition |\Z)"
    block = "\tmeasure '"+measure_name+"' =\n"+'\n'.join('\t\t\t'+line for line in dax.strip().splitlines())+'\n'
    if fmt:
        block += '\t\tformatString: '+fmt+'\n'
    block += '\t\tdisplayFolder: Discovery monitoring\n\t\tlineageTag: '+str(uuid.uuid5(uuid.NAMESPACE_URL, 'mission-control:'+measure_name))+'\n\n'
    if re.search(pattern, text):
        text = re.sub(pattern, lambda _:block, text)
    else:
        at = text.index('\tpartition ')
        text = text[:at]+block+text[at:]
    path.write_text(text, encoding='utf-8')

def history_filter(table):
    c = columns(table)
    if 'job_run_id' in c:
        return f'''TREATAS(CALCULATETABLE(VALUES('Discovery Job Runs'[job_run_id]),
            KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), {table}[job_run_id])'''
    return None

def latest_filter(table):
    c = columns(table)
    timestamp = DATES.get(table)
    if not timestamp:
        return None
    key = 'run_id' if 'run_id' in c else 'job_run_id' if 'job_run_id' in c else None
    measure(name(table, 'Latest time'), f'CALCULATE(MAX({table}[{timestamp}]), REMOVEFILTERS())', 'dd MMM yyyy HH:mm')
    if key:
        measure(name(table, 'Latest key'), f'''
VAR Batches = CALCULATETABLE(SUMMARIZE({table}, {table}[{key}],
    "DiscoveryTime", MAX({table}[{timestamp}])), REMOVEFILTERS())
VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])),
    [DiscoveryTime], DESC, {table}[{key}], DESC)
RETURN MAXX(LatestBatch, {table}[{key}])''')
        return f'TREATAS({{[{name(table, "Latest key")}]}}, {table}[{key}])'
    return f'TREATAS({{[{name(table, "Latest time")}]}}, {table}[{timestamp}])'

def scoped_expression(table, expression):
    historic = history_filter(table)
    latest = latest_filter(table)
    latest_expression = f'CALCULATE({expression}, KEEPFILTERS({latest}))' if latest else expression
    if latest and ('run_id' in columns(table) or 'job_run_id' in columns(table)):
        time_filter = f'TREATAS({{[{name(table, "Latest time")}]}}, {table}[{DATES[table]}])'
        latest_expression = f'IF(ISBLANK([{name(table, "Latest key")}]), CALCULATE({expression}, KEEPFILTERS({time_filter})), {latest_expression})'
    if historic and latest:
        return f'IF([Discovery history selected] = 1, CALCULATE({expression}, KEEPFILTERS({historic})), {latest_expression})'
    if latest:
        return f'CALCULATE({expression}, KEEPFILTERS({latest}))'
    return expression

def table_measures(table):
    measure(name(table, 'Rows'), 'COALESCE('+scoped_expression(table, f'COUNTROWS({table})')+', 0)', '#,0')
    measure(name(table, 'Visible'), f'IF([{name(table, "Rows")}] > 0, 1, 0)', '0')
    dated = DATES.get(table)
    if dated:
        measure(name(table, 'Selected time'), scoped_expression(table, f'MAX({table}[{dated}])'), 'dd MMM yyyy HH:mm')
    measure(name(table, 'State'), f'''
VAR n = [{name(table, 'Rows')}]
RETURN IF(n = 0,
    IF([Discovery history selected] = 1, "No retained discovery for this selection", "No discovery records available"),
    "Retained records: " & FORMAT(n, "#,0"))''')

def page_id(group):
    return ui.sid('discovery-page:'+group['key'])

def shell(pid, label, kind, x, y, w, h):
    return {'$schema': 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.7.0/schema.json',
            'name': ui.sid(pid+':'+label), 'position': {'x':x, 'y':y, 'width':w, 'height':h, 'z':60000, 'tabOrder':60000},
            'visual': {'visualType':kind, 'drillFilterOtherVisuals':True}}

def register(pid, table, x, y, w, h):
    v = copy.deepcopy(ui.visual(ui.CAL, 'fe821948e1b3b2425852'))
    v['name'] = ui.sid(pid+':register:'+table)
    v.pop('isHidden', None);v.pop('filterConfig', None)
    fields = columns(table)
    order = PRIORITY[table]+[col for col in fields if col not in PRIORITY[table]]
    v['visual']['query'] = {'queryState': {'Values': {'projections': [ui.projection(table, col, 'Column') for col in order]}}}
    timestamp = DATES.get(table)
    if timestamp:
        v['visual']['query']['sortDefinition'] = {'sort': [{'field':ui.field(table, timestamp, 'Column'), 'direction':'Descending'}]}
    for key, entries in v['visual'].get('objects', {}).items():
        v['visual']['objects'][key] = [entry for entry in entries if 'selector' not in entry]
    ui.table_style(v);ui.add_filter(v, name(table, 'Visible'))
    ui.props(v['visual']['objects'], 'total')['show'] = ui.lit('false')
    ui.props(v['visual']['objects'], 'values')['fontSize'] = ui.lit('11D')
    ui.props(v['visual']['visualContainerObjects'], 'general')['altText'] = ui.string('Discovery register for '+table)
    return ui.pos(v, x, y, w, h, 65000)

def slicer(pid, label, table, field_name, x, y, w, h):
    v = copy.deepcopy(ui.visual(ui.CAL, '91a7abd13be1fc90f248'))
    v['name'] = ui.sid(pid+':filter:'+label)
    v.pop('filterConfig', None);v.pop('isHidden', None)
    v['visual']['query'] = {'queryState': {'Values': {'projections':[ui.projection(table, field_name, 'Column')]}}}
    for entry in v['visual'].get('objects', {}).get('general', []):
        entry.get('properties', {}).pop('filter', None)
    ui.props(v['visual']['objects'], 'header')['text'] = ui.string(label)
    ui.props(v['visual']['objects'], 'selection')['singleSelect'] = ui.lit('false')
    ui.props(v['visual']['objects'], 'selection')['selectAllCheckboxEnabled'] = ui.lit('true')
    return ui.pos(v, x, y, w, h, 65000)

def data_bookmark(pid, label, targets, visible):
    bid = ui.sid(pid+':tab:'+label)
    containers = {}
    for v in targets:
        sv = {'visualType':v['visual']['visualType'], 'objects':{}}
        if v['name'] not in visible:
            sv['display'] = {'mode':'hidden'}
        containers[v['name']] = {'singleVisual':sv}
    b = {'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json',
         'name':bid, 'displayName':label+' · '+pid, 'options':{'applyOnlyToTargetVisuals':True,
         'targetVisualNames':[v['name'] for v in targets], 'suppressActiveSection':True, 'suppressData':True},
         'explorationState':{'version':'1.0', 'activeSection':pid, 'sections':{pid:{'visualContainers':containers}}}}
    ui.save(ui.DEF/'bookmarks'/f'{bid}.bookmark.json', b)
    meta = ui.load(ui.DEF/'bookmarks/bookmarks.json')
    if not any(item.get('name') == bid for item in meta['items']):
        meta['items'].append({'name':bid});ui.save(ui.DEF/'bookmarks/bookmarks.json', meta)
    return bid

def create_page(group):
    pid = page_id(group);primary = group['tables'][0]
    p = copy.deepcopy(ui.load(ui.PAGES/ui.CAL/'page.json'))
    p.update(name=pid, displayName=group['title'], height=1128, width=1680)
    p.pop('pageBinding', None);p.pop('filterConfig', None);p.pop('visibility', None)
    p['visualInteractions'] = []
    ui.save(ui.PAGES/pid/'page.json', p)
    put = lambda v:ui.put(pid, v)
    put(ui.textbox(pid, 'overline', 'OPERATIONS / MISSION CONTROL / DISCOVERY', 36,22,1500,22,12,ui.ACCENT,True))
    put(ui.textbox(pid, 'title', group['headline'], 36,53,1580,44,30,ui.TEXT,True))
    put(ui.textbox(pid, 'intro', group['intro'], 36,102,1608,33,13,ui.MUTED))
    for i, other in enumerate(GROUPS):
        b = ui.button(pid, 'group-nav:'+other['key'], other['title'],36+i*270,148,258,34,'PageNavigation',page_id(other))
        if other['key'] == group['key']:
            ui.props(b['visual']['objects'], 'fill')['show'] = ui.lit('true')
            b['visual']['objects']['fill'][1]['properties']['fillColor'] = ui.color('#34463A')
        put(b)
    put(ui.panel(pid,'calendar-panel',36,205,1038,248))
    put(ui.textbox(pid,'calendar-heading','Job-run history · last 365 days',58,222,990,28,18,ui.TEXT,True))
    put(ui.textbox(pid,'calendar-note','Select a day, then choose a Job ID if that day has several runs. Clear both to return to latest.',58,253,990,28,11,ui.MUTED))
    heat = copy.deepcopy(ui.visual(ui.CAL, ui.sid('github-load-calendar')))
    heat['name'] = ui.sid(pid+':calendar');heat.pop('isHidden',None)
    projections=heat['visual']['query']['queryState']['dataset']['projections']
    for projection in projections:
        if projection.get('field',{}).get('Measure'):
            old=projection['nativeQueryRef']
            replacement={'Calendar Day Runs':'Discovery calendar jobs',
                         'Calendar Day Failures':'Discovery calendar failures',
                         'Calendar Day Other':'Discovery calendar other'}[old]
            projection.update(ui.projection('_MissionControl_Measures',replacement,label=old))
    props = ui.props(heat['visual']['objects'], 'vega')
    raw = props['jsonSpec']['expr']['Literal']['Value']
    spec = json.loads(raw[1:-1].replace("''", "'"));spec.update(width=938, height=112)
    props['jsonSpec'] = ui.string(json.dumps(spec, ensure_ascii=False))
    props.update(enableSelection=ui.lit('true'), selectionMode=ui.string('simple'))
    ui.props(heat['visual']['objects'], 'stateManagement').update(viewportWidth=ui.lit('990D'),viewportHeight=ui.lit('144D'))
    put(ui.pos(heat,58,281,990,144,65000))
    put(ui.textbox(pid,'calendar-legend','Green intensity = jobs · Red = failed job · Amber = running / other · Empty square = no recorded job run',58,428,990,22,10,ui.MUTED))
    put(ui.panel(pid,'selection-panel',1098,205,546,248))
    put(ui.textbox(pid,'selection-heading','Discovery context · '+group['labels'][0],1120,222,502,26,16,ui.TEXT,True))
    context = name(primary, 'Context')
    measure(context, f'''
VAR History = [Discovery history selected] = 1
VAR DateChosen = SELECTEDVALUE('Load Calendar'[Date])
VAR LatestTime = [{name(primary, 'Latest time')}]
RETURN IF(History,
    "Historical selection" & IF(NOT ISBLANK(DateChosen), " · " & FORMAT(DateChosen, "dd MMM yyyy"), " · chosen job"),
    IF(ISBLANK(LatestTime), "No latest discovery available", "Latest discovery · " & FORMAT(LatestTime, "dd MMM yyyy HH:mm")))''')
    put(ui.card(pid,'scope-card',context,1114,254,514,56,18))
    put(ui.card(pid,'state-card',name(primary,'State'),1114,309,514,31,12))
    job = slicer(pid,'Job ID · historical selection','Discovery Job Runs','job_run_id',1120,351,502,62)
    ui.add_filter(job,'Discovery job picker visible')
    put(job)
    metric_name = name(primary, 'Scope count')
    dims = ','.join(f'{primary}[{col}]' for col in group['metric'][1])
    measure(metric_name, 'COALESCE('+scoped_expression(primary,f'COUNTROWS(SUMMARIZE({primary},{dims}))')+',0)', '#,0')
    distinct_name = name(primary, 'Distinct objects')
    measure(distinct_name,'COALESCE('+scoped_expression(primary,f'DISTINCTCOUNT({primary}[{group["distinct"][1]}])')+',0)', '#,0')
    batch_name = name(primary, 'Discovery batches')
    key = 'run_id' if 'run_id' in columns(primary) else 'job_run_id'
    measure(batch_name,'COALESCE('+scoped_expression(primary,f'DISTINCTCOUNT({primary}[{key}])')+',0)', '#,0')
    kpis = [(group['metric'][0],metric_name), (group['distinct'][0],distinct_name), ('Retained records',name(primary,'Rows')), ('Discovery batches',batch_name)]
    for i, (label, m) in enumerate(kpis):
        x=36+i*408
        put(ui.panel(pid,'kpi-panel:'+label,x,458,384,118))
        put(ui.textbox(pid,'kpi-label:'+label,label,x+20,474,344,24,12,ui.MUTED,True))
        put(ui.card(pid,'kpi-value:'+label,m,x+17,503,350,52,29))
    selectors = []
    for i, col in enumerate(group['filters']):
        s = slicer(pid,col.replace('_',' ').capitalize()+' · '+group['labels'][0],primary,col,36+i*544,594,520,63)
        ui.add_filter(s,name(primary,'Visible'))
        put(s);selectors.append(s)
    put(ui.panel(pid,'register-panel',36,679,1608,365))
    put(ui.textbox(pid,'register-heading',group['title']+' register',58,696,1540,28,18,ui.TEXT,True))
    tables=[];captions=[]
    for i, table in enumerate(group['tables']):
        v=register(pid,table,58,802,1564,216)
        linked=bool(history_filter(table));dated=bool(DATES.get(table))
        note = ('Latest retained discovery by default; selected day / job filters retained records. An empty register means no retained result for that selection.' if linked else
                'Current snapshot; this source has no confirmed job-run lineage. Calendar selection does not reconstruct past values.')
        if not dated:
            note += ' No discovery timestamp is recorded.'
        caption=ui.textbox(pid,'table-note:'+table,note,58,769,1560,30,11,ui.MUTED)
        ui.hide(v,i>0);ui.hide(caption,i>0)
        tables.append(v);captions.append(caption);put(v);put(caption)
    for i, (table,label) in enumerate(zip(group['tables'],group['labels'])):
        bid=data_bookmark(pid,label,tables+captions,{tables[i]['name'],captions[i]['name']})
        put(ui.button(pid,'table-tab:'+table,label,58+i*350,731,338,30,'Bookmark',bid))
    # The independent calendar and selectors do not receive register selections.
    # They keep the date identity stable as display-only tabs switch registers.
    cards=[ui.load(path) for path in (ui.PAGES/pid/'visuals').glob('*/visual.json')
           if ui.load(path)['visual']['visualType']=='cardVisual']
    targets=[job]+selectors+tables+cards
    visual_ids=[heat['name'],job['name']]+[s['name'] for s in selectors]
    for source in visual_ids:
        for target in targets:
            if source!=target['name']:
                p['visualInteractions'].append({'source':source,'target':target['name'],'type':'DataFilter'})
    for t in tables:
        for target in [heat,job]+selectors:
            p['visualInteractions'].append({'source':t['name'],'target':target['name'],'type':'NoFilter'})
    put(ui.button(pid,'back-calendar','← Load calendar',36,1070,224,36,'PageNavigation',ui.CAL))
    put(ui.button(pid,'back-quality','Quality & Schema →',278,1070,224,36,'PageNavigation',ui.QUALITY))
    put(ui.textbox(pid,'retention-note','History shows retained evidence only. Current-reference tabs stay explicitly separate from job-run snapshots.',532,1077,1110,28,11,ui.MUTED))
    ui.save(ui.PAGES/pid/'page.json',p)
    return {'pageId':pid,'displayName':group['title'],'tables':group['tables'],'calendarId':heat['name'],
            'tableVisuals':[v['name'] for v in tables], 'default':'Latest available discovery per retained table',
            'history':'Selected job IDs from Load Calendar; unlinked tables remain current snapshots',
            'referenceTables':[table for table in group['tables'] if not history_filter(table)]}

def live_job_history():
    """Use the already-authorized monitoring view through the same live source.

    This avoids falsely reporting no jobs for dates newer than the old imported
    job cache. The original job table, relationships and storage modes survive.
    """
    source=(ui.TABLES/'cfg_data_domain.tmdl').read_text(encoding='utf-8-sig')
    endpoint=re.search(r'Sql.Database\(("[^"]+",\s*"[^"]+")\)',source)
    if not endpoint:
        raise ValueError('Cannot resolve the existing monitoring SQL source.')
    specs=[('job_run_id','string'),('pipeline_name','string'),('started_at','dateTime'),
           ('ended_at','dateTime'),('status','string'),('steps_failed','int64'),('Run Date','dateTime')]
    name_='Discovery Job Runs'
    content="table '"+name_+"'\n\tlineageTag: "+str(uuid.uuid5(uuid.NAMESPACE_URL,name_))+'\n\n'
    for col,kind in specs:
        content+="\tcolumn '"+col+"'\n\t\tdataType: "+kind+'\n\t\tsummarizeBy: none\n\t\tsourceColumn: '+col+'\n'
        if kind=='dateTime':
            content+='\t\tformatString: '+('dd MMM yyyy' if col=='Run Date' else 'dd MMM yyyy HH:mm')+'\n'
        content+='\t\tlineageTag: '+str(uuid.uuid5(uuid.NAMESPACE_URL,name_+':'+col))+'\n\n'
    original=', '.join('"'+col+'"' for col,_ in specs if col!='Run Date')
    content+="\tpartition 'Discovery Job Runs' = m\n\t\tmode: directQuery\n\t\tsource =\n"
    content+='\t\t\t\tlet\n\t\t\t\t    Source = Sql.Database('+endpoint.group(1)+'),\n'
    content+='\t\t\t\t    Jobs = Source{[Schema="monitoring", Item="rpt_job_run_summary"]}[Data],\n'
    content+='\t\t\t\t    Columns = Table.SelectColumns(Jobs, {'+original+'}),\n'
    content+='\t\t\t\t    Dates = Table.AddColumn(Columns, "Run Date", each Date.From([started_at]), type date)\n\t\t\t\tin\n\t\t\t\t    Dates\n'
    (ui.TABLES/(name_+'.tmdl')).write_text(content,encoding='utf-8')
    model_path=ui.TABLES.parent/'model.tmdl';model=model_path.read_text(encoding='utf-8-sig')
    if "ref table 'Discovery Job Runs'" not in model:
        model=model.replace('ref cultureInfo',"ref table 'Discovery Job Runs'\n\nref cultureInfo",1)
    match=re.search(r'annotation PBI_QueryOrder = (\[.*?\])',model)
    if match:
        order=json.loads(match.group(1))
        if name_ not in order:
            order.append(name_);model=model[:match.start(1)]+json.dumps(order)+model[match.end(1):]
    model_path.write_text(model,encoding='utf-8')
    measure('Discovery history selected', "IF(ISFILTERED('Load Calendar'[Date]) || ISFILTERED('Discovery Job Runs'[job_run_id]), 1, 0)", '0')
    measure('Discovery calendar jobs', '''COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))), 0)''', '#,0')
    measure('Discovery calendar failures', '''COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
    FILTER('Discovery Job Runs', UPPER('Discovery Job Runs'[status]) IN {"FAILED", "FAILURE", "ERROR"}
        || 'Discovery Job Runs'[steps_failed] > 0)), 0)''', '#,0')
    measure('Discovery calendar other', '''COALESCE(CALCULATE(COUNTROWS('Discovery Job Runs'),
    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date])),
    FILTER('Discovery Job Runs', NOT(UPPER('Discovery Job Runs'[status]) IN {"SUCCESS", "SUCCESSFUL", "SUCCEEDED", "FAILED", "FAILURE", "ERROR"})
        && COALESCE('Discovery Job Runs'[steps_failed], 0) = 0)), 0)''', '#,0')
    measure('Discovery job picker visible', '''IF(CALCULATE(COUNTROWS('Discovery Job Runs'),
    KEEPFILTERS(TREATAS(VALUES('Load Calendar'[Date]), 'Discovery Job Runs'[Run Date]))) > 0, 1, 0)''', '0')

def latest_first_existing_views():
    latest_cohort = '''
VAR LatestJob = CALCULATETABLE(TOPN(1,
    FILTER(rpt_job_run_summary, NOT ISBLANK(rpt_job_run_summary[started_at])),
    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC),
    ALLSELECTED(rpt_job_run_summary))
VAR LatestId = MAXX(LatestJob, rpt_job_run_summary[job_run_id])
'''
    for m, table in [('Day Explorer Job Visible','rpt_job_run_summary'),
                     ('Timeline Job Visible','rpt_job_run_summary'),
                     ('Timeline Step Visible','rpt_job_step_timing'),
                     ('Latest Pipeline Row Visible','cfg_pipeline_run')]:
        guard = "IF(ISFILTERED('Load Calendar'[Date]) && NOT HASONEVALUE('Load Calendar'[Date]), 0, " if m=='Day Explorer Job Visible' else ''
        expression = f'''IF(ISFILTERED('Load Calendar'[Date]), COUNTROWS({table}),
    CALCULATE(COUNTROWS({table}), KEEPFILTERS(TREATAS({{LatestId}}, rpt_job_run_summary[job_run_id]))))'''
        measure(m, latest_cohort+f'VAR n = {expression}\nRETURN '+guard+'IF(n > 0, 1, 0)'+(')' if guard else ''), '0')
    for label, table, original, fmt, vid in [
        ('Runs','_Load Experience','Runs','#,0','43756e2036440b35a2a4'),
        ('Success rate','_Load Experience','Success rate','0.0%','11ee704a4e0dc534c1a0'),
        ('Failures','_Load Experience','Failures','#,0','0428d60a51d577c214ea'),
        ('P95 duration min','_Load Experience','P95 duration min','0.0','8f2d99cd4f4f6e856f82'),
        ('Rows written','_Load Experience','Rows written','#,0','42e369df6e646973e811')]:
        m='Latest or selected '+label
        measure(m,latest_cohort+f'''RETURN IF(ISFILTERED('Load Calendar'[Date]), [{original}],
    CALCULATE([{original}], KEEPFILTERS(TREATAS({{LatestId}}, rpt_job_run_summary[job_run_id]))))''',fmt)
        v=ui.visual(ui.CAL,vid)
        v['visual']['query']={'queryState':{'Data':{'projections':[ui.projection('_MissionControl_Measures',m)]}}}
        ui.put(ui.CAL,v)
    # The new row gate handles latest/default and historical contexts. The old
    # Vega single-day-only condition would incorrectly hide the latest default.
    v=ui.visual(ui.CAL,'3b28a42eb9ca129a560e');pr=ui.props(v['visual']['objects'],'vega')
    spec=json.loads(pr['jsonSpec']['expr']['Literal']['Value'][1:-1].replace("''","'"))
    spec['transform']=[t for t in spec['transform'] if t.get('filter') != "datum['Single calendar day'] == 1"]
    pr['jsonSpec']=ui.string(json.dumps(spec,ensure_ascii=False));ui.put(ui.CAL,v)
    for pid,vid,m in [
        (ui.DETAIL,'a2951e4af3b6ba28e98a','Timeline Job Visible'),
        (ui.DETAIL,'9cad86fc1f811a8887ad','Timeline Step Visible'),
        (ui.DETAIL,'6833f80013eb8175a2f7','Latest Pipeline Row Visible')]:
        v=ui.visual(pid,vid);ui.add_filter(v,m);ui.put(pid,v)
    for pid,vid,text in [
        (ui.CAL,'eccc8b5a690c7caffdfb','Latest load opens by default. Select a calendar day to inspect its jobs, then Open day timelines for the selected context.'),
        (ui.TIMELINES,'2eaeb6eabd759ca05260','Latest load by default; calendar drillthrough carries the selected day and pipeline. Select a job to inspect its steps. Bands: prior P25–P75 · tick: mean · red glow: failure.'),
        ('26a97c060b27eb5c8381','8bc8616412d8abac3aff','Latest load opens by default. Calendar drillthrough carries the selected day and pipeline filters. Select a job to inspect its steps. Bands describe prior successful history; Back returns to the calendar.')]:
        v=ui.visual(pid,vid);ui.texts(v)[0]['value']=text;ui.put(pid,v)
    # Current schema inventory has no historical job lineage.
    DATES['cfg_archived_schema_live']='contract_loaded_at'
    table_measures('cfg_archived_schema_live')
    v=ui.visual(ui.QUALITY,'67b2658ef36a75631c5d');ui.add_filter(v,name('cfg_archived_schema_live','Visible'));ui.put(ui.QUALITY,v)
    # Existing archive selectors still choose a cohort; default displays the
    # newest matching ZIP batch / Gold snapshot instead of all historical rows.
    for table, timestamp, vid in [('cfg_archive_zip_load','started_at','f5abe87bbe2fa0fa43b1'),
                                  ('cfg_month_end_gold_run','started_at','1167d11d499a47936099')]:
        DATES[table]=timestamp;table_measures(table)
        m=name(table,'Latest key')
        measure(m,f'''
VAR Batches = CALCULATETABLE(SUMMARIZE({table}, {table}[run_id], "DiscoveryTime", MAX({table}[{timestamp}])), ALLSELECTED({table}))
VAR LatestBatch = TOPN(1, FILTER(Batches, NOT ISBLANK([DiscoveryTime])), [DiscoveryTime], DESC, {table}[run_id], DESC)
RETURN MAXX(LatestBatch, {table}[run_id])''')
        v=ui.visual('5133b9c7cfcf12cf7f74',vid);ui.add_filter(v,name(table,'Visible'));ui.put('5133b9c7cfcf12cf7f74',v)
    for vid,table,original in [
        ('20ba560db882915a59b7','cfg_archive_zip_load','Archive ZIP Batches'),
        ('5eab460ad81a4a9cc4ae','cfg_archive_zip_load','Archive ZIP Batches Awaiting Reload'),
        ('f1264ff02064c4cc7a5e','cfg_archive_zip_load','Failed Archive ZIP Batches'),
        ('c0e527711d471509b704','cfg_month_end_gold_run','Failed Gold Snapshots')]:
        m='Latest matching '+original
        measure(m,f'CALCULATE([{original}], KEEPFILTERS(TREATAS({{[{name(table,"Latest key")}]}}, {table}[run_id])))','#,0')
        v=ui.visual('5133b9c7cfcf12cf7f74',vid)
        v['visual']['query']={'queryState':{'Data':{'projections':[ui.projection('_MissionControl_Measures',m)]}}}
        ui.put('5133b9c7cfcf12cf7f74',v)

def build():
    missing = [t for group in GROUPS for t in group['tables'] if not (ui.TABLES/(t+'.tmdl')).exists()]
    if missing:
        raise ValueError('Missing monitoring tables: '+', '.join(missing))
    ui.backup()
    live_job_history()
    for group in GROUPS:
        for table in group['tables']:
            table_measures(table)
    records=[create_page(group) for group in GROUPS]
    latest_first_existing_views()
    metadata=ui.load(ui.PAGES/'pages.json')
    added=[r['pageId'] for r in records]
    old=[pid for pid in metadata['pageOrder'] if pid not in added]
    at=old.index(ui.QUALITY)+1
    metadata['pageOrder']=old[:at]+added+old[at:]
    ui.save(ui.PAGES/'pages.json',metadata)
    # A visible entry on the main page, without disturbing its existing links.
    ui.put(ui.CAL,ui.button(ui.CAL,'discovery-hub','Discovery monitoring →',1042,896,300,38,'PageNavigation',added[0]))
    ui.save(ui.ROOT/'Discovery monitoring pages.json',{'pages':records,'newTables':len({t for g in GROUPS for t in g['tables']}),
                'retention':'cfg_data_domain currently replaces per-column profiles; old job runs may have no retained domain results.',
                'dataAccess':'DirectQuery sources require the existing Power BI/Fabric sign-in. External ADOMD data profiling was unavailable (Integrated Security not supported).',
                'sourceMode':'Preserved all user-added DirectQuery tables and original storage modes. Added a live job navigator from the existing monitoring job-summary view. No credentials, existing source imports, relationships or warehouse data changed.'})
    print(f'Built {len(records)} discovery pages for {len({t for g in GROUPS for t in g["tables"]})} newly added monitoring tables.')

if __name__=='__main__':
    build()
