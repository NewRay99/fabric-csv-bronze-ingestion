"""Add problem/discovery recency lights to the four Watch Tower summaries."""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path

import build_mission_control_watch_tower as tower
import refine_mission_control_wip as ui
from reorient_mission_control_change_calendars import QUALITY_FAILURE

COLORS = {'Latest day': '#FF4D5E', 'Prior 7 days': '#FFC45C', 'History': '#8E9991', 'No record': '#F3F7EF'}

def configure(root):
    ui.ROOT = root
    ui.REPORT = root / 'SM WMPP Mission Control.Report'
    ui.DEF = ui.REPORT / 'definition'
    ui.PAGES = ui.DEF / 'pages'
    ui.TABLES = root / 'SM WMPP Mission Control.SemanticModel/definition/tables'
    ui.CARD_TEMPLATE = ui.visual(ui.CAL, '43756e2036440b35a2a4')

def rows(table, predicate='TRUE()'):
    return f"FILTER(CALCULATETABLE('{table}',REMOVEFILTERS()),({predicate}))"

def sources(scope):
    drift = ('cfg_schema_drift_event', 'COALESCE(cfg_schema_drift_event[last_detected_at],cfg_schema_drift_event[detected_at],cfg_schema_drift_event[first_detected_at])', 'TRUE()')
    if scope == 'problems':
        return {
            'Domains': [],
            'Drift': [drift],
            'Contracts': [drift],
            'Quality': [('rpt_job_data_quality', 'rpt_job_data_quality[checked_at]', QUALITY_FAILURE),
                        ('cfg_rejected_row', 'cfg_rejected_row[rejected_at]', 'TRUE()'),
                        ('cfg_referential_exception', 'cfg_referential_exception[detected_at]', 'TRUE()')],
        }
    return {
        'Domains': [('cfg_data_domain', 'cfg_data_domain[profiled_at]', 'TRUE()')],
        'Drift': [drift, ('cfg_schema_drift_definition', 'cfg_schema_drift_definition[definition_loaded_at]', 'TRUE()')],
        'Contracts': [('cfg_bronze_schema_live', 'cfg_bronze_schema_live[captured_at]', 'TRUE()'),
                      ('cfg_schema_contract_column', 'cfg_schema_contract_column[contract_loaded_at]', 'TRUE()')],
        'Quality': [('rpt_job_data_quality', 'rpt_job_data_quality[checked_at]', 'TRUE()'),
                    ('cfg_rejected_row', 'cfg_rejected_row[rejected_at]', 'TRUE()'),
                    ('cfg_referential_exception', 'cfg_referential_exception[detected_at]', 'TRUE()')],
    }

def classification(count='[RecordCount]', captured='[Captured]', load='[LoadDay]'):
    # Date-based because several retained sources do not expose a common load ID.
    return f'''VAR n={count}
VAR t={captured}
VAR anchor={load}
RETURN SWITCH(TRUE(),n=0,0,ISBLANK(t)||ISBLANK(anchor),1,
    INT(t)=INT(anchor),3,
    INT(t)>=INT(anchor)-7 && INT(t)<INT(anchor),2,1)'''

def specification():
    color = "datum['Flag code'] === 3 ? '#FF4D5E' : datum['Flag code'] === 2 ? '#FFC45C' : datum['Flag code'] === 1 ? '#8E9991' : '#F3F7EF'"
    base = {'x': {'value': 52}, 'y': {'value': 28}, 'color': {'field': 'Glow', 'type': 'nominal', 'scale': None},
            'tooltip': [{'field': 'Flag explanation', 'type': 'nominal', 'title': 'Capture recency'}]}
    layers = []
    for size, opacity in [(2450, .045), (1700, .07), (1100, .10), (650, .16), (340, .32), (190, .98)]:
        layers.append({'mark': {'type': 'circle', 'size': size, 'opacity': opacity}, 'encoding': copy.deepcopy(base)})
    layers[-1]['mark'].update(stroke='#F3F7EF', strokeWidth=.5)
    layers.append({'mark': {'type': 'text', 'font': 'Segoe UI', 'fontSize': 11, 'color': ui.MUTED, 'align': 'center', 'baseline': 'middle'},
                   'encoding': {'x': {'value': 52}, 'y': {'value': 64}, 'text': {'field': 'Flag label', 'type': 'nominal'},
                                'tooltip': [{'field': 'Flag explanation', 'type': 'nominal', 'title': 'Capture recency'}]}})
    return {'$schema': 'https://vega.github.io/schema/vega-lite/v5.json', 'data': {'name': 'dataset'},
            'width': 104, 'height': 70, 'padding': 0, 'autosize': 'none',
            'transform': [{'calculate': color, 'as': 'Glow'}], 'layer': layers,
            'config': {'background': ui.PANEL, 'view': {'stroke': None}}}

def build(root, scope='problems', backup=True):
    configure(root)
    if backup:
        ui.backup()
    expressions = {
        'Watch Tower Flag Latest Load Day': '''VAR t=CALCULATE(MAX('Discovery Job Runs'[started_at]),REMOVEFILTERS())
RETURN IF(NOT ISBLANK(t),INT(t))''',
    }
    noun = 'problems' if scope == 'problems' else 'discoveries'
    explanations = {
        'Domains': 'Domain profiles contain no explicit problem register. Profile captures alone do not create a problem flag.',
        'Drift': 'Recorded schema drift detections are problem evidence; resolution dates do not create a new detection.',
        'Contracts': 'Schema/contract problem evidence uses recorded schema drift. Schema and contract captures alone are not problems.',
        'Quality': 'Failed/error quality findings, rejected rows and referential exceptions are problem evidence. Passing checks alone are not problems.',
    }
    for key, title, unit, table, target in tower.GROUPS:
        specs = sources(scope)[key]
        record_name = f'Watch Tower {key} Flag Records'
        time_name = f'Watch Tower {key} Flag Captured'
        flag_name = f'Watch Tower {key} Flag'
        count = ' + '.join(f'COUNTROWS({rows(t,p)})' for t, date, p in specs) or '0'
        times = ','.join(f'SELECTCOLUMNS({rows(t,p)},"Captured",{date})' for t, date, p in specs)
        expressions[record_name] = f'COALESCE({count},0)'
        expressions[time_name] = f'MAXX({"UNION("+times+")" if len(specs)>1 else times},[Captured])' if specs else 'BLANK()'
        expressions[flag_name] = classification(f'[{record_name}]', f'[{time_name}]', '[Watch Tower Flag Latest Load Day]')
        expressions[f'{flag_name} Label'] = f'''VAR code=[{flag_name}]
VAR captured=[{time_name}]
VAR anchor=[Watch Tower Flag Latest Load Day]
RETURN SWITCH(TRUE(),code=0,"No record",code=3,"Latest day",code=2,"Prior 7 days",
    ISBLANK(captured),"Undated",ISBLANK(anchor),"No load date",INT(captured)>anchor,"Unlinked date","History")'''
        explain = explanations[key] if scope == 'problems' else 'Any retained discovery in this monitoring area is capture evidence.'
        expressions[f'{flag_name} Tooltip'] = f'''VAR t=[{time_name}]
VAR anchor=[Watch Tower Flag Latest Load Day]
RETURN "{title}: " & [{flag_name} Label] & ". " &
    IF([{record_name}]=0,"No retained {noun} recorded. ",IF(ISBLANK(t),"Capture date is not recorded. ","Last captured: " & FORMAT(t,"dd MMM yyyy HH:mm") & ". ")) &
    IF(ISBLANK(anchor),"Latest load date is unavailable. ","Latest cached load day: " & FORMAT(anchor,"dd MMM yyyy") & ". ") &
    "Red means the same load day; amber is the previous seven days; grey is older or undated. Date matching does not prove an exact job link. {explain}"'''
    expressions['Watch Tower Flag Legend'] = '''VAR anchor=[Watch Tower Flag Latest Load Day]
RETURN "''' + noun.capitalize() + ''' recency · latest cached load day " & IF(ISBLANK(anchor),"unavailable",FORMAT(anchor,"dd MMM yyyy")) &
    "   |   RED latest day   ·   AMBER prior 7 days   ·   GREY older / undated   ·   WHITE no recorded ''' + noun + '''"'''
    for name, dax in expressions.items():
        tower.upsert(name, dax, name.endswith('Flag') or name.endswith('Records'))

    flag_visuals = []
    for i, (key, title, unit, table, target) in enumerate(tower.GROUPS):
        v = copy.deepcopy(ui.visual(ui.CAL, 'e263e453f96be0512a19'))
        v['name'] = ui.sid('watch-tower-flag:' + key)
        v.pop('filterConfig', None)
        v.pop('isHidden', None)
        v['visual']['query'] = {'queryState': {'dataset': {'projections': [
            ui.projection('_MissionControl_Measures', f'Watch Tower {key} Flag', label='Flag code'),
            ui.projection('_MissionControl_Measures', f'Watch Tower {key} Flag Label', label='Flag label'),
            ui.projection('_MissionControl_Measures', f'Watch Tower {key} Flag Tooltip', label='Flag explanation'),
        ]}}}
        props = ui.props(v['visual']['objects'], 'vega')
        props.update(jsonSpec=ui.string(json.dumps(specification())), enableSelection=ui.lit('false'), enableContextMenu=ui.lit('false'))
        ui.props(v['visual']['objects'], 'stateManagement').update(viewportWidth=ui.lit('104D'), viewportHeight=ui.lit('70D'))
        ui.props(v['visual']['visualContainerObjects'], 'general')['altText'] = ui.string(title + ' ' + noun + ' recency indicator. Hover for capture date and date-based interpretation.')
        ui.props(v['visual']['visualContainerObjects'], 'visualHeader')['show'] = ui.lit('false')
        ui.put(ui.CAL, ui.pos(v, 36 + i*408 + 267, 203, 104, 70, 63000))
        flag_visuals.append(v['name'])
    legend = tower.make_card('flag-legend', 'Watch Tower Flag Legend', 36, 126, 1608, 19, 9, ui.MUTED)
    ui.put(ui.CAL, legend)
    intro = ui.visual(ui.CAL, 'eccc8b5a690c7caffdfb')
    intro['position']['height'] = 21
    ui.put(ui.CAL, intro)
    page_path = ui.PAGES / ui.CAL / 'page.json'
    page = ui.load(page_path)
    all_visual_ids = [p.parent.name for p in (ui.PAGES / ui.CAL / 'visuals').glob('*/visual.json')]
    targets = flag_visuals + [legend['name']]
    pairs = {(s,t) for s in all_visual_ids for t in targets if s != t} | {(s,t) for s in flag_visuals for t in all_visual_ids if s != t}
    page['visualInteractions'] = [item for item in page['visualInteractions'] if (item['source'],item['target']) not in pairs]
    page['visualInteractions'] += [{'source':s,'target':t,'type':'NoFilter'} for s,t in sorted(pairs)]
    ui.save(page_path, page)
    ui.save(root/'Watch Tower flags revision.json', {'scope':scope, 'writtenMeasures':list(expressions), 'pageId':ui.CAL,
        'flagVisualIds':flag_visuals, 'legendVisualId':legend['name'], 'colors':COLORS,
        'reference':'Latest retained Discovery Job Runs.started_at day, independent of slicers',
        'recency':'Same day / prior 7 calendar days / older or undated / no retained records',
        'exactJobLinkClaimed':False, 'sourceRefresh':'None'})
    define = 'DEFINE\n' + '\n'.join("MEASURE '_MissionControl_Measures'["+name+'] = '+dax for name,dax in expressions.items())
    display_rows = []
    for key,title,unit,table,target in tower.GROUPS:
        flag = f'Watch Tower {key} Flag'
        display_rows.append(f'ROW("Area","{title}","Flag code",[{flag}],"Flag label",[{flag} Label],"Captured",[{flag.replace(" Flag"," Flag Captured")}],"Explanation",[{flag} Tooltip])')
    (root/'Watch Tower flags prepared.dax').write_text(define+'\nEVALUATE UNION('+','.join(display_rows)+')\n',encoding='utf-8')
    (root/'Watch Tower flags loaded.dax').write_text('EVALUATE UNION('+','.join(display_rows)+')\n',encoding='utf-8')
    # Synthetic boundary records exercise the actual classifier expression.
    cases = [("Latest day",1,"DATE(2026,10,13)+TIME(7,15,0)","DATE(2026,10,13)",3),
             ("Previous day",1,"DATE(2026,10,12)","DATE(2026,10,13)",2),
             ("Seven-day boundary",1,"DATE(2026,10,6)","DATE(2026,10,13)",2),
             ("Eight days old",1,"DATE(2026,10,5)","DATE(2026,10,13)",1),
             ("No recorded problems",0,"BLANK()","DATE(2026,10,13)",0),
             ("Undated recorded problem",1,"BLANK()","DATE(2026,10,13)",1),
             ("No load date",1,"DATE(2026,10,13)","BLANK()",1),
             ("Capture after retained load",1,"DATE(2026,10,14)","DATE(2026,10,13)",1)]
    checks=[]
    for label,count,captured,load,expected in cases:
        actual='('+classification(str(count),captured,load)+')'
        checks.append(f'ROW("Case","{label}","Actual",{actual},"Expected",{expected},"Pass",{actual}={expected})')
    for key,title,unit,table,target in tower.GROUPS:
        flag=f'Watch Tower {key} Flag'
        actual=f'CALCULATE([{flag}],TREATAS({{DATE(2026,8,24)}},\'Load Calendar\'[Date]),TREATAS({{"no-job"}},\'Discovery Job Runs\'[job_run_id]))'
        checks.append(f'ROW("Case","{title} ignores historical selection","Actual",{actual},"Expected",[{flag}],"Pass",{actual}=[{flag}])')
    (root/'Watch Tower flags checks.dax').write_text(define+'\nEVALUATE UNION('+','.join(checks)+')\n',encoding='utf-8')
    print(f'Prepared {scope} recency lights: four flags, legend, {len(expressions)} measures, 12 boundary/context checks.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,required=True)
    parser.add_argument('--scope',choices=['problems','discoveries'],default='problems')
    parser.add_argument('--no-backup',action='store_true')
    args=parser.parse_args()
    build(args.project_root,args.scope,not args.no_backup)
