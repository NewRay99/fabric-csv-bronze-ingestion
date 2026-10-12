"""Apply the October readability, latest-load and calendar revision to WIP only."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import uuid
import zipfile
from datetime import datetime

ROOT = pathlib.Path(__file__).resolve().parents[1] / 'reports/WIP/SM WMPP Mission Control v16'
REPORT = ROOT / 'SM WMPP Mission Control.Report'
DEF = REPORT / 'definition'
PAGES = DEF / 'pages'
TABLES = ROOT / 'SM WMPP Mission Control.SemanticModel/definition/tables'
CAL = '803165f7d2f5aaccd8ac'
TIMELINES = 'ed27e90d06816c7c1eee'
QUALITY = 'd807778066085fbd96dc'
DETAIL = '112fda69b94ad2ed064c'
TOOLTIP = '2af45662f5a13e0c063b'
DENEB = 'deneb7E15AEF80B9E4D4F8E12924291ECE89A'
BG, PANEL, ALT, TEXT, MUTED, ACCENT = '#101713', '#1B241E', '#242F28', '#F3F7EF', '#A7B6A9', '#CBF576'

def load(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def save(p, v):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(v, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sid(s):
    return hashlib.sha1(('mission-control-october:' + s).encode()).hexdigest()[:20]

def lit(s):
    return {'expr': {'Literal': {'Value': s}}}

def string(s):
    return lit("'" + s.replace("'", "''") + "'")

def color(s):
    return {'solid': {'color': string(s)}}

def field(table, name, kind='Measure'):
    return {kind: {'Expression': {'SourceRef': {'Entity': table}}, 'Property': name}}

def projection(table, name, kind='Measure', label=None):
    v = {'field': field(table, name, kind), 'queryRef': table + '.' + name, 'nativeQueryRef': label or name}
    if label and label != name:
        v['displayName'] = label
    return v

def path(pid, vid):
    return PAGES / pid / 'visuals' / vid / 'visual.json'

def visual(pid, vid):
    return load(path(pid, vid))

def put(pid, v):
    save(path(pid, v['name']), v)

def pos(v, x, y, w, h, z=None):
    v['position'].update(x=x, y=y, width=w, height=h)
    if z is not None:
        v['position'].update(z=z, tabOrder=z)
    return v

def props(objects, key):
    a = objects.setdefault(key, [{'properties': {}}])
    if not a:
        a.append({'properties': {}})
    return a[0].setdefault('properties', {})

def texts(v):
    return [t for g in v['visual'].get('objects', {}).get('general', [])
            for p in g.get('properties', {}).get('paragraphs', []) for t in p.get('textRuns', [])]

TEXT_TEMPLATE = visual(CAL, '8335a1c4e82d9ae351c3')
PANEL_TEMPLATE = visual(CAL, 'fa3abf7e2ce8b2d29b4d')
CARD_TEMPLATE = visual(CAL, '43756e2036440b35a2a4')
BUTTON_TEMPLATE = visual(CAL, '89bfad1ebbda3675c1c3')

def textbox(pid, label, text, x, y, w, h, size=13, ink=TEXT, bold=False, z=60000):
    v = copy.deepcopy(TEXT_TEMPLATE)
    v['name'] = sid(pid + ':' + label)
    v['visual']['objects']['general'] = [{'properties': {'paragraphs': [{'textRuns': [{
        'value': text, 'textStyle': {'fontFamily': 'Segoe UI', 'fontSize': f'{size}px',
                                  'fontWeight': 'bold' if bold else 'normal', 'color': ink}}]}]}}]
    return pos(v, x, y, w, h, z)

def panel(pid, label, x, y, w, h):
    v = copy.deepcopy(PANEL_TEMPLATE)
    v['name'] = sid(pid + ':' + label)
    return pos(v, x, y, w, h, -1000)

def card(pid, label, measure, x, y, w, h, size=29, table='_MissionControl_Measures'):
    v = copy.deepcopy(CARD_TEMPLATE)
    v['name'] = sid(pid + ':' + label)
    v['visual']['query'] = {'queryState': {'Data': {'projections': [projection(table, measure)]}}}
    props(v['visual']['objects'], 'value')['fontSize'] = lit(f'{size}D')
    props(v['visual']['visualContainerObjects'], 'general')['altText'] = string(measure)
    return pos(v, x, y, w, h, 61000)

def hide(v, state=True):
    if state:
        v['isHidden'] = True
    else:
        v.pop('isHidden', None)

def measure_filter(name):
    f = field('_MissionControl_Measures', name)
    expression = field('_MissionControl_Measures', name)
    expression['Measure']['Expression']['SourceRef'] = {'Source': 'm'}
    return {'name': sid('filter:' + name), 'field': f, 'type': 'Advanced',
            'filter': {'Version': 2, 'From': [{'Name': 'm', 'Entity': '_MissionControl_Measures', 'Type': 0}],
                       'Where': [{'Condition': {'Comparison': {'ComparisonKind': 0,
                                    'Left': expression, 'Right': {'Literal': {'Value': '1L'}}}}}]},
            'howCreated': 'User', 'isLockedInViewMode': True}

def add_filter(v, name):
    fs = v.setdefault('filterConfig', {}).setdefault('filters', [])
    fs[:] = [f for f in fs if f.get('name') != sid('filter:' + name)]
    fs.append(measure_filter(name))

def add_measure(name, dax, fmt=None, folder='Latest load report'):
    p = TABLES / '_MissionControl_Measures.tmdl'
    source = p.read_text(encoding='utf-8-sig')
    if "\tmeasure '" + name + "' =" in source:
        return
    block = "\tmeasure '" + name + "' =\n" + '\n'.join('\t\t\t' + s for s in dax.strip().splitlines()) + '\n'
    if fmt:
        block += '\t\tformatString: ' + fmt + '\n'
    block += '\t\tdisplayFolder: ' + folder + '\n\t\tlineageTag: ' + str(uuid.uuid5(uuid.NAMESPACE_URL, name)) + '\n\n'
    idx = source.index('\tpartition ')
    p.write_text(source[:idx] + block + source[idx:], encoding='utf-8')

def recolor(node):
    mapping = {'#F8F5F1': BG, '#FFFFFF': PANEL, '#FFF9FB': ALT, '#FCE8ED': ALT,
               '#2B2427': TEXT, '#756A70': MUTED, '#61575C': MUTED,
               '#EEDCE3': '#34463A', '#E8DCE1': '#34463A', '#B78D98': '#000000'}
    if isinstance(node, dict):
        for k, val in node.items():
            if isinstance(val, (dict, list)):
                recolor(val)
            elif isinstance(val, str):
                for old, new in mapping.items():
                    if val in (old, "'" + old + "'"):
                        node[k] = val.replace(old, new)
    elif isinstance(node, list):
        for child in node:
            recolor(child)

def table_style(v):
    o = v['visual'].setdefault('objects', {})
    for item in o.setdefault('values', [{'properties': {}}]):
        p = item['properties']
        if 'selector' not in item:
            p.pop('fontColor', None)
            p.update(fontColorPrimary=color(TEXT), fontColorSecondary=color(TEXT),
                     backColorPrimary=color(PANEL), backColorSecondary=color(ALT),
                     fontFamily=string('Segoe UI'), fontSize=lit('10D'))
    props(o, 'columnHeaders').update(fontColor=color(MUTED), backColor=color(PANEL), fontFamily=string('Segoe UI Semibold'))
    for key in ['total', 'rowTotal', 'columnTotal']:
        if key in o:
            props(o, key).update(fontColor=color(TEXT), backColor=color(PANEL))
    if v['visual']['visualType'] == 'pivotTable':
        props(o, 'rowHeaders').update(fontColor=color(MUTED), backColor=color(PANEL), fontSize=lit('10D'))
    container = v['visual'].setdefault('visualContainerObjects', {})
    props(container, 'visualHeader').update(background=color(PANEL), foreground=color(TEXT), border=color('#34463A'))

def backup():
    out = ROOT.parent / '_backups' / ('Mission Control before October design fixes ' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.zip')
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob('*'):
            if p.is_file() and '.pbi' not in p.relative_to(ROOT).parts:
                z.write(p, p.relative_to(ROOT))
    print('Backup:', out)

def latest_load():
    add_measure('Latest Load Run ID', '''VAR latest = TOPN(1,
    FILTER(ALL(rpt_job_run_summary), NOT ISBLANK(rpt_job_run_summary[started_at])),
    rpt_job_run_summary[started_at], DESC, rpt_job_run_summary[job_run_id], DESC)
RETURN CALCULATE(MAXX(latest, rpt_job_run_summary[job_run_id]), REMOVEFILTERS())''')
    # REMOVEFILTERS belongs around TOPN too: the selector must be independent of page and row context.
    p = TABLES / '_MissionControl_Measures.tmdl'
    source = p.read_text(encoding='utf-8')
    source = source.replace('FILTER(ALL(rpt_job_run_summary), NOT ISBLANK(rpt_job_run_summary[started_at]))',
                            'FILTER(CALCULATETABLE(rpt_job_run_summary, REMOVEFILTERS()), NOT ISBLANK(rpt_job_run_summary[started_at]))')
    p.write_text(source, encoding='utf-8')
    add_measure('Latest Load Started', '''VAR id = [Latest Load Run ID]
RETURN IF(NOT ISBLANK(id), CALCULATE(MAX(rpt_job_run_summary[started_at]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = id))''', 'dd MMM yyyy HH:mm')
    add_measure('Latest Load Status', '''VAR id = [Latest Load Run ID]
RETURN IF(ISBLANK(id), "No loads", CALCULATE(SELECTEDVALUE(rpt_job_run_summary[status]), REMOVEFILTERS(), rpt_job_run_summary[job_run_id] = id))''')
    add_measure('Latest Load Quality Records', '''VAR id = [Latest Load Run ID]
RETURN IF(NOT ISBLANK(id), COALESCE(CALCULATE(COUNTROWS(cfg_data_quality_result), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = id), 0))''', '#,0')
    for new, base in [('Latest Load Evaluated Checks', 'DQ Evaluated Checks'),
                      ('Latest Load Failed Checks', 'DQ Failed Checks'),
                      ('Latest Load Failed Rows', 'DQ Failed Rows'),
                      ('Latest Load Critical Rules', 'Critical Rules Failing')]:
        add_measure(new, f'''VAR id = [Latest Load Run ID]
RETURN IF([Latest Load Quality Records] > 0,
    COALESCE(CALCULATE([{base}], KEEPFILTERS(TREATAS({{id}}, cfg_data_quality_result[job_run_id]))), 0))''', '#,0')
    add_measure('Show Latest Load Quality', '''VAR id = [Latest Load Run ID]
RETURN IF(NOT ISBLANK(id) && CALCULATE(COUNTROWS(cfg_data_quality_result),
    KEEPFILTERS(TREATAS({id}, cfg_data_quality_result[job_run_id]))) > 0, 1, 0)''', '0')
    add_measure('Latest Load Quality Report', '''VAR id = [Latest Load Run ID]
VAR lastCheck = CALCULATE(MAX(cfg_data_quality_result[checked_at]), REMOVEFILTERS(), cfg_data_quality_result[job_run_id] = id)
RETURN IF(ISBLANK(id), "No load recorded in this model",
    "Load started " & FORMAT([Latest Load Started], "dd MMM yyyy HH:mm") & " | " &
    IF([Latest Load Quality Records] = 0, "No quality report for this load yet",
       "Quality checked " & FORMAT(lastCheck, "dd MMM yyyy HH:mm")))''')
    add_measure('Calendar Day Runs', 'COALESCE([Job Runs], 0)', '#,0')
    add_measure('Calendar Day Failures', 'COALESCE([Failed Job Runs], 0)', '#,0')
    add_measure('Calendar Day Other', 'COALESCE(CALCULATE([Job Runs], KEEPFILTERS(rpt_job_run_summary[Outcome] IN {"Running", "Other"})), 0)', '#,0')
    add_measure('Calendar Day In Window', '''VAR d = SELECTEDVALUE('Load Calendar'[Date])
RETURN IF(NOT ISBLANK(d) && d >= TODAY() - 364 && d <= TODAY(), 1, 0)''', '0')

def quality_page():
    # Latest ID replaces the historical-run selector. The three inspection slicers stay intact.
    v = card(QUALITY, 'latest-id', 'Latest Load Run ID', 53, 168, 349, 35, 13)
    v['name'] = 'ee0a70825c985d8b98e2'
    put(QUALITY, v)
    put(QUALITY, textbox(QUALITY, 'latest-id-label', 'Latest load · run ID', 53, 145, 349, 23, 12, MUTED, True))
    for vid, text in [('0e1b6d9f7e1bb4bb161a', 'The latest load. Quality in focus.'),
                      ('206c4b784806a4203fb3', 'KPIs and quality results follow the newest load in this model. Use severity, table and status to inspect its report.'),
                      ('d75b5467d38a54806787', 'Latest load · quality report'),
                      ('7131cc0a5c953208f1cd', 'Current captured schema · independent inventory; no load-level lineage is recorded.')]:
        v = visual(QUALITY, vid)
        texts(v)[0]['value'] = text
        put(QUALITY, v)
    report = card(QUALITY, 'latest-report-caption', 'Latest Load Quality Report', 58, 448, 976, 34, 11)
    report['name'] = '05d74a83400dafe5c6a1'
    put(QUALITY, report)
    existing = [
        ('80589721178b61fe9e1a','6bb0a2d34ad7a066ab43','6436b26d607517c8e536','d59b7f28a7d9c0317001','Evaluated checks','Latest Load Evaluated Checks','Completed check executions'),
        ('9a4c3824f674ba923d18','4f4624272888f07eac8f','91dbc24e8ec5bf2914fd','64264bd4693e23594b05','Failed checks','Latest Load Failed Checks','In the latest load · filtered'),
        ('cf499cd95492078568e9','88553e82de1fe3ff7c08','6c219e5f5141119a7075','c63f31e30cb676efc136','Failed rows','Latest Load Failed Rows','Rows counted per check'),
        ('13067799b85a00f032df','42e7351ea768791d5ddd','6a14ab4b95d922a1f641','f4e5b108d450e952e9cc','Critical rules failing','Latest Load Critical Rules','Investigate these first')]
    for i, (p, label, value, caption, title, measure, note) in enumerate(existing, 1):
        x = 36 + i * 326
        put(QUALITY, pos(visual(QUALITY,p), x,232,304,146))
        for vid, y, h, text in [(label,248,27,title),(caption,338,30,note)]:
            v = visual(QUALITY,vid);texts(v)[0]['value']=text
            put(QUALITY,pos(v,x+20,y,268,h))
        v = card(QUALITY,measure,measure,x+17,280,268,50)
        v['name'] = value;put(QUALITY,v)
    put(QUALITY, panel(QUALITY,'latest-status-panel',36,232,304,146))
    put(QUALITY, textbox(QUALITY,'latest-status-label','Latest load status',56,248,268,27,13,MUTED,True))
    put(QUALITY, card(QUALITY,'latest-status','Latest Load Status',53,280,268,50,23))
    put(QUALITY, textbox(QUALITY,'latest-status-note','Newest started job · all loads',56,338,268,30,11,MUTED))
    v = visual(QUALITY,'bd4e4e7dd119737ed15d')
    add_filter(v,'Show Latest Load Quality')
    for name in ['job_run_id','run_id','checked_at']:
        ps = v['visual']['query']['queryState']['Values']['projections']
        if not any(x['queryRef']=='cfg_data_quality_result.'+name for x in ps):
            ps.append(projection('cfg_data_quality_result',name,'Column'))
    put(QUALITY,v)

def bookmark(label, targets, showing):
    name = sid(label)
    containers = {}
    for v in targets:
        sv = {'visualType': v['visual']['visualType'], 'objects': {}}
        if v['name'] not in showing:
            sv['display'] = {'mode':'hidden'}
        containers[v['name']] = {'singleVisual':sv}
    b = {'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json',
         'displayName':label,'name':name,'options':{'applyOnlyToTargetVisuals':True,
         'targetVisualNames':[v['name'] for v in targets],'suppressActiveSection':True,'suppressData':True},
         'explorationState':{'version':'1.0','activeSection':CAL,'sections':{CAL:{'visualContainers':containers}}}}
    save(DEF/'bookmarks'/f'{name}.bookmark.json',b)
    meta=load(DEF/'bookmarks/bookmarks.json')
    if not any(x.get('name')==name for x in meta['items']):
        meta['items'].append({'name':name});save(DEF/'bookmarks/bookmarks.json',meta)
    return name

def button(pid,label,title,x,y,w,h,kind,target):
    v=copy.deepcopy(BUTTON_TEMPLATE);v['name']=sid(pid+':'+label)
    v['visual']['objects']={
        'fill':[{'properties':{'show':lit('true')}},{'selector':{'id':'default'},'properties':{'fillColor':color(ALT),'transparency':lit('0D')}}],
        'outline':[{'properties':{'show':lit('false')}}],
        'icon':[{'properties':{'show':lit('false')}}],
        'text':[{'properties':{'show':lit('true')}},{'selector':{'id':'default'},'properties':{
            'text':string(title),'fontColor':color(ACCENT),'fontSize':lit('11D'),'fontFamily':string('Segoe UI'),'bold':lit('true')}}]}
    link={'show':lit('true'),'type':string(kind),'tooltip':string(title)}
    target_property = {'Bookmark': 'bookmark', 'Drillthrough': 'drillthroughSection',
                       'PageNavigation': 'navigationSection'}.get(kind)
    if target_property:
        link[target_property]=string(target)
    v['visual']['visualContainerObjects']['visualLink']=[{'properties':link}]
    return pos(v,x,y,w,h,70000)

def calendar_page():
    # Keep the two-column standard layout. A 53-week graph fits the left panel.
    calp=TABLES/'Load Calendar.tmdl';source=calp.read_text(encoding='utf-8')
    source=source.replace('VAR _firstDate = COALESCE(MIN(rpt_job_run_summary[Run Date]), TODAY())',
                          'VAR _firstDate = MIN(COALESCE(MIN(rpt_job_run_summary[Run Date]), TODAY()), TODAY() - 364)')
    calp.write_text(source,encoding='utf-8')
    month=visual(CAL,'5c55c8df64c46f54fa93')
    for obj in month['visual'].get('objects',{}).get('general',[]):
        obj['properties'].pop('filter',None)
    put(CAL,month)
    monthly=visual(CAL,'52b0db0e9f2a1ebfb85e')
    rows=monthly['visual']['query']['queryState']['Rows']['projections']
    if not any(p['queryRef']=='Load Calendar.Month' for p in rows):
        m=projection('Load Calendar','Month','Column');m['active']=True;rows.insert(0,m)
    table_style(monthly)
    props(monthly['visual']['objects'],'rowHeaders').update(backColor=color(PANEL),fontColor=color(MUTED),fontSize=lit('10D'))
    for w in monthly['visual']['objects'].get('columnWidth',[]):
        if w.get('selector',{}).get('metadata')=='Load Calendar.Week':
            w['properties']['value']=lit('38D')
    pos(monthly,58,525,648,323);hide(monthly)
    put(CAL,monthly)
    heat=copy.deepcopy(visual(CAL,'3b28a42eb9ca129a560e'))
    heat['name']=sid('github-load-calendar');pos(heat,58,568,648,166,62000)
    heat.pop('isHidden',None)
    heat['visual']['query']={'queryState':{'dataset':{'projections':[
        projection('Load Calendar','Date','Column'),projection('Load Calendar','Weekday','Column'),
        *[projection('_MissionControl_Measures',n) for n in ['Calendar Day Runs','Calendar Day Failures','Calendar Day Other']]]}},
        'sortDefinition':{'sort':[{'field':field('Load Calendar','Date','Column'),'direction':'Ascending'}]}}
    spec={'$schema':'https://vega.github.io/schema/vega-lite/v5.json','data':{'name':'dataset'},
        'width':594,'height':96,'padding':{'left':2,'right':2,'top':4,'bottom':4},
        'transform':[
            {'calculate':"toDate(datum.Date)",'as':'Day'},
            {'calculate':"time(datetime(year(datum.Day), month(datum.Day), date(datum.Day) - ((day(datum.Day) + 6) % 7)))",'as':'WeekStart'},
            {'calculate':"datum['Calendar DayFailures']",'as':'unused'}],
        'mark':{'type':'rect','cornerRadius':2,'stroke':BG,'strokeWidth':2,'cursor':'pointer'},
        'encoding':{
            'x':{'field':'WeekStart','type':'ordinal','sort':'ascending','axis':{'title':None,'orient':'top','labelAngle':0,
                'labelExpr':"date(toDate(datum.value)) <= 7 ? timeFormat(toDate(datum.value), '%b') : ''",'labelOverlap':False,'ticks':False,'domain':False,'labelPadding':8}},
            'y':{'field':'Weekday','type':'ordinal','sort':['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],'axis':{'title':None,'domain':False,'ticks':False,
                'labelExpr':"indexof(['Mon','Wed','Fri'], datum.label) >= 0 ? datum.label : ''",'labelPadding':8}},
            'color':{'condition':[
                {'test':"datum['Calendar Day Failures'] > 0",'value':'#D35A66'},
                {'test':"datum['Calendar Day Other'] > 0",'value':'#B58D43'},
                {'test':"datum['Calendar Day Runs'] >= 10",'value':'#CBF576'},
                {'test':"datum['Calendar Day Runs'] >= 5",'value':'#91C977'},
                {'test':"datum['Calendar Day Runs'] >= 2",'value':'#4C854F'},
                {'test':"datum['Calendar Day Runs'] > 0",'value':'#345B3D'}],'value':ALT},
            'opacity':{'condition':{'test':"datum['__selected__'] === 'off'",'value':0.3},'value':1},
            'stroke':{'condition':{'test':"datum['__selected__'] === 'on'",'value':TEXT},'value':BG},
            'tooltip':[{'field':'Date','type':'temporal','title':'Load date','format':'%a %d %b %Y'},
                {'field':'Calendar Day Runs','type':'quantitative','title':'Job runs'},
                {'field':'Calendar Day Failures','type':'quantitative','title':'Failed jobs'},
                {'field':'Calendar Day Other','type':'quantitative','title':'Running or other'}]},
        'config':{'background':PANEL,'view':{'stroke':None},'axis':{'labelColor':MUTED,'labelFont':'Segoe UI','labelFontSize':10,'grid':False}}}
    spec['transform'].pop()  # Only derived positioning fields; keep original datum identity for selection.
    o=heat['visual']['objects'];o['vega'][0]['properties']['jsonSpec']=string(json.dumps(spec,ensure_ascii=False))
    o['stateManagement'][0]['properties'].update(viewportHeight=lit('166D'),viewportWidth=lit('648D'))
    o['stateManagement'][0]['properties'].pop('supportFieldConfiguration',None)
    add_filter(heat,'Calendar Day In Window');put(CAL,heat)
    intro=textbox(CAL,'heatmap-intro','365 days of load activity',58,525,648,30,19,TEXT,True)
    legend=textbox(CAL,'heatmap-legend','Less',58,746,30,28,11,MUTED)
    more=textbox(CAL,'heatmap-more','More',176,746,45,28,11,MUTED)
    outcomes=textbox(CAL,'heatmap-outcomes','! Failed    ~ Running / other',242,746,464,28,11,MUTED)
    helptext=textbox(CAL,'heatmap-help','Select a square to inspect that day. Hover for counts.\nChoose a month above to zoom; clear it to return to the year.',58,784,648,62,12,MUTED)
    for v in [intro,legend,more,outcomes,helptext]:put(CAL,v)
    swatches=[]
    for i,ink in enumerate([ALT,'#345B3D','#4C854F','#91C977',ACCENT]):
        swatch=panel(CAL,'heatmap-legend-swatch'+str(i),91+i*15,751,12,12)
        swatch['position']['z']=63000
        props(swatch['visual']['objects'],'shape')['roundEdge']=lit('2L')
        swatch['visual']['objects']['fill'][1]['properties']['fillColor']=color(ink)
        props(swatch['visual']['objects'],'shadow')['show']=lit('false')
        swatches.append(swatch);put(CAL,swatch)
    targets=[monthly,heat,intro,legend,more,outcomes,helptext,*swatches]
    heatbook=bookmark('Year heatmap',targets,{x['name'] for x in [heat,intro,legend,more,outcomes,helptext,*swatches]})
    monthbook=bookmark('Load activity calendar',targets,{monthly['name']})
    put(CAL,button(CAL,'heatmap-switch','Year heatmap',58,482,151,29,'Bookmark',heatbook))
    put(CAL,button(CAL,'monthly-switch','Load activity',219,482,151,29,'Bookmark',monthbook))
    for vid,text in [('489e984aa0a980a7e8cd','Load calendar'),('6c9ce87f84682062899e','Green intensity = job count · Red = failure · Amber = running / other'),
                    ('eccc8b5a690c7caffdfb','Select a day in either calendar to explore its loads. Switch Year heatmap / Load activity, then Day Gantt / Register.')]:
        v=visual(CAL,vid);texts(v)[0]['value']=text;put(CAL,v)
    p=load(PAGES/CAL/'page.json')
    interactions=p.setdefault('visualInteractions',[])
    for target in ['3b28a42eb9ca129a560e','fe821948e1b3b2425852','43756e2036440b35a2a4','11ee704a4e0dc534c1a0','0428d60a51d577c214ea','8f2d99cd4f4f6e856f82','42e369df6e646973e811']:
        if not any(x['source']==heat['name'] and x['target']==target for x in interactions):
            interactions.append({'source':heat['name'],'target':target,'type':'DataFilter'})
    for source in ['3b28a42eb9ca129a560e','fe821948e1b3b2425852']:
        interactions.append({'source':source,'target':heat['name'],'type':'NoFilter'})
    interactions.extend([{'source':heat['name'],'target':monthly['name'],'type':'NoFilter'},
                         {'source':monthly['name'],'target':heat['name'],'type':'NoFilter'}])
    p['visualInteractions']=list({(i['source'],i['target']):i for i in interactions}.values())
    save(PAGES/CAL/'page.json',p)

def day_explorer_filter():
    # SUMMARIZECOLUMNS can retain unrelated job groups when a nonblank measure
    # (including Single calendar day) survives their empty date-filtered context.
    # Require actual fact rows in that context, not just a calendar selection.
    name = 'Day Explorer Job Visible'
    add_measure(name, """
VAR SelectedDay = SELECTEDVALUE('Load Calendar'[Date])
VAR MatchingJobs = COUNTROWS(rpt_job_run_summary)
RETURN IF(NOT ISBLANK(SelectedDay) && MatchingJobs > 0, 1, 0)
""", '0', 'Calendar & day explorer')
    for vid in ['3b28a42eb9ca129a560e', 'fe821948e1b3b2425852']:
        v = visual(CAL, vid)
        add_filter(v, name)
        if v['visual']['visualType'] == DENEB:
            dataset = v['visual']['query']['queryState']['dataset']['projections']
            if not any(p['queryRef'] == '_MissionControl_Measures.' + name for p in dataset):
                dataset.append(projection('_MissionControl_Measures', name))
            properties = v['visual']['objects']['vega'][0]['properties']
            raw = properties['jsonSpec']['expr']['Literal']['Value']
            spec = json.loads(raw[1:-1].replace("''", "'"))
            gate = {'filter': "datum['Day Explorer Job Visible'] == 1"}
            transforms = spec.setdefault('transform', [])
            if gate not in transforms:
                transforms.insert(0, gate)
            properties['jsonSpec'] = string(json.dumps(spec, ensure_ascii=False))
        put(CAL, v)
    heat = visual(CAL, sid('github-load-calendar'))
    props(heat['visual']['objects'], 'vega')['selectionMode'] = string('simple')
    put(CAL, heat)
    # Keep existing comparison measures and the display-only bookmarks intact.

def calendar_drillthrough():
    filter_id = sid('calendar-to-timelines-date-filter')
    p = load(PAGES/TIMELINES/'page.json')
    filters = p.setdefault('filterConfig', {}).setdefault('filters', [])
    # A fixed date-window filter would intersect an older drillthrough day and
    # produce an empty destination. Apply the default window in row helpers.
    filters[:] = [f for f in filters if f.get('name') != filter_id
                  and f.get('field', {}).get('Column', {}).get('Property') != 'job_run_window']
    date_field = field('Load Calendar', 'Date', 'Column')
    filters.append({'name': filter_id, 'field': date_field, 'type': 'Categorical',
                    'howCreated': 'Drillthrough', 'isLockedInViewMode': True})
    p['pageBinding'] = {'name': 'MissionControlCalendarTimelines', 'type': 'Drillthrough',
                        'acceptsFilterContext': 'Default', 'parameters': [{
                            'name': 'Param_' + filter_id, 'boundFilter': filter_id,
                            'qnaSingleSelectRequired': True, 'fieldExpr': date_field}]}
    save(PAGES/TIMELINES/'page.json', p)
    # The saved Job ID selection belonged to a different day; start the target
    # slicers at All so they do not contradict incoming drillthrough context.
    for vid in ['515044d4c00f60d3220d', 'b77a5cd658430b5400e7', 'efa568dda0486ce4bfb0']:
        v = visual(TIMELINES, vid)
        for entry in v['visual'].get('objects', {}).get('general', []):
            entry.get('properties', {}).pop('filter', None)
        put(TIMELINES, v)
    for name, table in [('Timeline Job Visible', 'rpt_job_run_summary'),
                        ('Timeline Step Visible', 'rpt_job_step_timing')]:
        add_measure(name, f"""
VAR HasCalendarContext = ISCROSSFILTERED('Load Calendar'[Date])
VAR MatchingRows = IF(HasCalendarContext, COUNTROWS({table}),
    CALCULATE(COUNTROWS({table}),
        KEEPFILTERS(rpt_job_run_summary[job_run_window] = "Last 14 days")))
RETURN IF(MatchingRows > 0, 1, 0)
""", '0', 'Calendar & day explorer')
    for vid, name in [('8137eed10da16ee6c04a', 'Timeline Job Visible'),
                      ('1eba88b43b2625ccf766', 'Timeline Job Visible'),
                      ('515044d4c00f60d3220d', 'Timeline Job Visible'),
                      ('b77a5cd658430b5400e7', 'Timeline Job Visible'),
                      ('efa568dda0486ce4bfb0', 'Timeline Job Visible'),
                      ('32a158a22eb7ccd12103', 'Timeline Step Visible'),
                      ('7c53d6ccb195c7cb1b59', 'Timeline Step Visible')]:
        v = visual(TIMELINES, vid)
        add_filter(v, name)
        if v['visual']['visualType'] == DENEB:
            dataset = v['visual']['query']['queryState']['dataset']['projections']
            if not any(x['queryRef'] == '_MissionControl_Measures.' + name for x in dataset):
                dataset.append(projection('_MissionControl_Measures', name))
            pr = props(v['visual']['objects'], 'vega')
            raw = pr['jsonSpec']['expr']['Literal']['Value']
            spec = json.loads(raw[1:-1].replace("''", "'"))
            gate = {'filter': f"datum['{name}'] == 1"}
            if gate not in spec.setdefault('transform', []):
                spec['transform'].insert(0, gate)
            pr['jsonSpec'] = string(json.dumps(spec, ensure_ascii=False))
        put(TIMELINES, v)
    v = visual(TIMELINES, '2eaeb6eabd759ca05260')
    texts(v)[0]['value'] = 'Selected calendar day and pipeline; otherwise last 14 days. Select a job to inspect its steps. Bands: prior P25–P75 · tick: mean · red glow: failure.'
    put(TIMELINES, v)
    put(TIMELINES, button(TIMELINES, 'calendar-drillthrough-back', '← Back to calendar',
                         1414, 22, 230, 34, 'Back', CAL))
    b = button(CAL, 'calendar-timelines-drillthrough', 'Open day timelines →',
               1303, 436, 320, 36, 'Drillthrough', TIMELINES)
    link = props(b['visual']['visualContainerObjects'], 'visualLink')
    link.update(enabledTooltip=string('Open Job & Step Timelines for the selected day and current filters'),
                disabledTooltip=string('Select one square in the calendar first'))
    b['visual']['objects']['text'].append({'selector': {'id': 'disabled'}, 'properties': {
        'text': string('Select a calendar day'), 'fontColor': color(MUTED),
        'fontSize': lit('11D'), 'fontFamily': string('Segoe UI')}})
    b['visual']['objects']['fill'].append({'selector': {'id': 'disabled'}, 'properties': {
        'fillColor': color(ALT), 'transparency': lit('0D')}})
    put(CAL, b)
    heat = visual(CAL, sid('github-load-calendar'))
    props(heat['visual']['objects'], 'vega')['enableContextMenuSelector'] = lit('true')
    put(CAL, heat)
    p = load(PAGES/CAL/'page.json')
    interactions = p.setdefault('visualInteractions', [])
    for source in [heat['name'], '52b0db0e9f2a1ebfb85e', '3b28a42eb9ca129a560e', 'fe821948e1b3b2425852']:
        interactions[:] = [i for i in interactions if (i['source'], i['target']) != (source, b['name'])]
        interactions.append({'source': source, 'target': b['name'], 'type': 'DataFilter'})
    save(PAGES/CAL/'page.json', p)
    helptext = visual(CAL, sid(CAL + ':heatmap-help'))
    texts(helptext)[0]['value'] = 'Select a square, then Open day timelines to inspect its jobs and steps.\nOr right-click a square → Drillthrough → Job & Step Timelines.'
    put(CAL, helptext)
    for pid, vid, text in [
        ('faff55cdb2ebf5436d8d', 'a7aedc610c28e34762c9',
         'Year heatmap opens with the last 365 days. Load activity switches to the monthly calendar. Select a square, then Open day timelines to carry that day and pipeline into Job & Step Timelines. Use Back to return to the calendar.'),
        ('26a97c060b27eb5c8381', '8bc8616412d8abac3aff',
         'Calendar drillthrough carries the selected load day and current pipeline filters. Direct browsing shows the last 14 days. Select a job to inspect its steps; Back returns to the source. Bands show prior 30-day successful history, with at least five samples.')]:
        v = visual(pid, vid);texts(v)[0]['value'] = text;put(pid, v)

def detail_page():
    p=load(PAGES/DETAIL/'page.json');p.update(width=1680,height=1128)
    p['objects']=copy.deepcopy(load(PAGES/CAL/'page.json')['objects']);save(PAGES/DETAIL/'page.json',p)
    title=visual(DETAIL,'2a07e005f7912e1f0823');texts(title)[0].update(value='One run. Every step.',textStyle={'fontWeight':'bold','fontFamily':'Segoe UI','fontSize':'30px','color':TEXT})
    put(DETAIL,pos(title,36,53,1400,44))
    put(DETAIL,textbox(DETAIL,'overline','OPERATIONS / MISSION CONTROL',36,22,1200,22,12,ACCENT,True))
    put(DETAIL,textbox(DETAIL,'intro','Inspect the selected job, notebook steps and pipeline executions. With no job selected, headline cards show the latest run.',36,102,1580,28,13,MUTED))
    put(DETAIL,button(DETAIL,'back','← Job & step timelines',36,147,260,40,'PageNavigation','ed27e90d06816c7c1eee'))
    ids=[('5fccf90da812e32ebd66','Run ID','Selected or Latest Job Run ID','Confirm the selected job',12),
         ('3c4ad0b631c26a003ddf','Job status','Selected or Latest Job Status','Recorded execution outcome',23),
         ('aa6144922064df4f2107','Duration · min','Selected or Latest Job Duration (min)','Recorded job runtime',29),
         ('8078fd76c6c013cd38b3','Notebook steps','Selected or Latest Job Steps','Steps belonging to this job',29),
         ('14c1c997f46edd75d75a','Failed steps','Selected or Latest Failed Steps','Inspect recorded errors below',29)]
    for i,(vid,label,measure,note,size) in enumerate(ids):
        x=36+i*326;put(DETAIL,panel(DETAIL,'kpi'+str(i),x,232,304,146))
        put(DETAIL,textbox(DETAIL,'label'+str(i),label,x+20,248,268,27,13,MUTED,True))
        v=card(DETAIL,measure,measure,x+17,280,268,50,size);v['name']=vid;put(DETAIL,v)
        put(DETAIL,textbox(DETAIL,'note'+str(i),note,x+20,338,268,30,11,MUTED))
    data=[('a2951e4af3b6ba28e98a','Job summary','The job record, timings, row counts and quality totals.',36,400,1608,220,54,485,1572,115),
          ('9cad86fc1f811a8887ad','Notebook steps','Step order, duration, prior gaps and recorded errors.',36,642,792,363,54,727,758,257),
          ('6833f80013eb8175a2f7','Pipeline executions','Execution status, table outcomes and recorded row counts.',851,642,792,363,867,727,758,257)]
    for vid,label,note,x,y,w,h,tx,ty,tw,th in data:
        put(DETAIL,panel(DETAIL,vid+'panel',x,y,w,h))
        put(DETAIL,textbox(DETAIL,vid+'heading',label,x+22,y+17,w-44,28,18,TEXT,True))
        put(DETAIL,textbox(DETAIL,vid+'subheading',note,x+22,y+48,w-44,34,11,MUTED))
        v=visual(DETAIL,vid);props(v['visual']['visualContainerObjects'],'title')['show']=lit('false')
        table_style(v);put(DETAIL,pos(v,tx,ty,tw,th))
    for vid,x,y in [('4022af979f0d7a71a817',72,1084),('7c823f09d808d9cbc76c',36,1090)]:
        v=visual(DETAIL,vid);v['position'].update(x=x,y=y);put(DETAIL,v)
    for i,(name,target) in enumerate([('Load calendar',CAL),('Quality & schema',QUALITY),('Archive & replay','5133b9c7cfcf12cf7f74')]):
        put(DETAIL,button(DETAIL,'footer-'+name,name+' →',36+i*228,1027,220,38,'PageNavigation',target))

def guides_and_tooltip():
    for p in PAGES.glob('*/page.json'):
        page=load(p);pid=page['name']
        if not page['displayName'].endswith(' - guide'):
            continue
        page['objects']=copy.deepcopy(load(PAGES/CAL/'page.json')['objects']);save(p,page)
        vs=[load(v) for v in (p.parent/'visuals').glob('*/visual.json')]
        heading=next(v for v in vs if v['visual']['visualType']=='textbox' and v['position']['y'] in [24,53])
        intro=next(v for v in vs if v['visual']['visualType']=='textbox' and v['position']['y'] in [78,102])
        put(pid,pos(heading,36,53,1580,44))
        put(pid,pos(intro,36,102,1590,58))
        for t in texts(heading):t['textStyle'].update(fontSize='30px',color=TEXT)
        for t in texts(intro):t['textStyle'].update(color=MUTED,fontSize='13px')
        put(pid,heading);put(pid,intro)
        put(pid,textbox(pid,'guide-overline','MISSION CONTROL / PAGE GUIDE',36,22,1200,22,12,ACCENT,True))
        for i,head in enumerate(sorted([v for v in vs if v['visual']['visualType']=='textbox' and v['position']['height']==30],key=lambda v:(v['position']['y'],v['position']['x']))):
            body=next(v for v in vs if v['visual']['visualType']=='textbox' and v['position']['x']==head['position']['x'] and v['position']['y'] in [head['position']['y']+34,head['position']['y']+37])
            x=36+(i%2)*815;y=185+(i//2)*166
            put(pid,panel(pid,'guide-panel-'+head['name'],x,y,792,154))
            texts(head)[0]['textStyle'].update(color=TEXT,fontSize='17px')
            for t in texts(body):t['textStyle'].update(color=MUTED,fontSize='14px')
            put(pid,pos(head,x+22,y+17,748,30));put(pid,pos(body,x+22,y+54,748,90))
        if pid=='72d11707044e0285ccd2':
            for v in vs:
                for t in texts(v):
                    if v['name']=='4278bb2692af6bd2ceba':
                        t['value']='This page follows the latest started job in the saved model. Run ID and load status identify it. Missing quality results are shown as unavailable, not replaced by an older report.'
                    elif v['name']=='df81e4e4d6f9fc08b734':
                        t['value']='Only checks whose job_run_id matches the latest load are included. Severity, source table and status narrow this report. Run ID, quality run ID and checked time are available in the register.'
                    elif v['name']=='4947f971ad627017b06a':
                        t['value']='Current captured schema inventory is independent of the latest load. This source does not record load-level schema lineage; do not treat it as that job’s historical schema.'
                put(pid,v)
        if pid=='faff55cdb2ebf5436d8d':
            v=visual(pid,'a7aedc610c28e34762c9');texts(v)[0]['value']='Year heatmap opens with the last 365 days. Load activity switches to the monthly calendar. Select a square, then Open day timelines to carry that day and pipeline into Job & Step Timelines. Use Back to return to the calendar.';put(pid,v)
            v=visual(pid,'537a15139e9138a6a727');texts(v)[0]['value']='Green intensity counts job runs: 1, 2–4, 5–9 or 10+. Failure takes red precedence; running or other statuses are amber. Hover for exact counts. The month selector can narrow either calendar.';put(pid,v)
    p=load(PAGES/TOOLTIP/'page.json');p['objects']=copy.deepcopy(load(PAGES/CAL/'page.json')['objects']);save(PAGES/TOOLTIP/'page.json',p)
    put(TOOLTIP,textbox(TOOLTIP,'tooltip-overline','MISSION CONTROL / JOB RUN',15,10,620,23,11,ACCENT,True))
    for i,(vid,label,size) in enumerate([('f79bcf5f508aae1f1669','Run ID',12),('f7edb403743551be9ab4','Job status',23),('98c009f9ec0842f4dcb4','Duration · min',26),('6c5ff7f9a5c89bed10d2','Failed steps',26)]):
        x=15+(i%2)*315;y=42+(i//2)*124
        original=visual(TOOLTIP,vid);measure=original['visual']['query']['queryState']['Data']['projections'][0]['field']['Measure']['Property']
        put(TOOLTIP,panel(TOOLTIP,'tooltip-panel'+str(i),x,y,300,110))
        put(TOOLTIP,textbox(TOOLTIP,'tooltip-label'+str(i),label,x+15,y+10,270,23,12,MUTED,True))
        v=card(TOOLTIP,measure,measure,x+15,y+39,270,57,size);v['name']=vid;put(TOOLTIP,v)

def main():
    backup()
    # Desktop 26.09 upgrades the running model to 1606; external reload cannot downgrade it.
    database = TABLES.parent / 'database.tmdl'
    definition = database.read_text(encoding='utf-8-sig')
    level = re.search(r'compatibilityLevel:\s*(\d+)', definition)
    if not level:
        raise ValueError('Database compatibility level is missing.')
    if int(level.group(1)) < 1606:
        definition = definition[:level.start(1)] + '1606' + definition[level.end(1):]
        database.write_text(definition, encoding='utf-8')
    for p in PAGES.glob('*/page.json'):
        page=load(p);page['objects']=copy.deepcopy(load(PAGES/CAL/'page.json')['objects']);save(p,page)
        for vp in (p.parent/'visuals').glob('*/visual.json'):
            v=load(vp);recolor(v)
            if v['visual']['visualType'] in ['tableEx','pivotTable']:table_style(v)
            save(vp,v)
    latest_load();quality_page();calendar_page();day_explorer_filter();calendar_drillthrough();detail_page();guides_and_tooltip()
    # Report-specific theme now protects future tables too. Keep other WMPP projects untouched.
    p=REPORT/'StaticResources/RegisteredResources/WMPP_Theme.json';theme=load(p)
    for kind in ['tableEx','pivotTable']:
        for style in theme['visualStyles'].get(kind,{}).values():
            recolor(style)
            for values in style.get('values',[]):
                values.update(fontColorPrimary={'solid':{'color':TEXT}},fontColorSecondary={'solid':{'color':TEXT}},
                              backColorPrimary={'solid':{'color':PANEL}},backColorSecondary={'solid':{'color':ALT}})
    save(p,theme)
    print('Updated',ROOT)

if __name__=='__main__':main()
