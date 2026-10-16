"""Use retained findings/captures for the six discovery-page calendars.

Only owned measures and visuals are edited. All table storage modes, queries,
cached data, original report pages and visibility-only bookmarks are preserved.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import build_mission_control_discovery_pages as build
import refine_mission_control_wip as ui


def col(table, field):
    return f"'{table}'[{field}]"


def source(table, dates, predicate='TRUE()', key=None, date_expression=None):
    return dict(table=table, dates=dates, predicate=predicate, key=key, dateExpression=date_expression)


DRIFT_DATES = ['first_detected_at', 'detected_at', 'last_detected_at', 'resolved_at']
QUALITY_FAILURE = '''COALESCE(rpt_job_data_quality[failed_row_count],0)>0
    || COALESCE(rpt_job_data_quality[rejected_key_count],0)>0
    || COALESCE(rpt_job_data_quality[referential_exception_count],0)>0
    || UPPER(COALESCE(rpt_job_data_quality[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}'''
EXPORT_ERROR = '''UPPER(COALESCE(cfg_silver_export_load[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
    || LEN(TRIM(COALESCE(cfg_silver_export_load[error_message],"")))>0'''
CONTROL_ERROR = '''UPPER(COALESCE(cfg_silver_load_control[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
    || LEN(TRIM(COALESCE(cfg_silver_load_control[error_message],"")))>0'''
LINEAGE_ERROR = '''UPPER(COALESCE(rpt_job_layer_lineage[lineage_status],""))
    IN {"FAIL","FAILED","FAILURE","ERROR","MISSING","UNMATCHED","BROKEN","NOT_FOUND","STALE"}'''
STEP_ERROR = '''UPPER(COALESCE(rpt_job_step_summary[status],"")) IN {"FAIL","FAILED","FAILURE","ERROR"}
    || COALESCE(rpt_job_step_summary[tables_failed],0)>0
    || LEN(TRIM(COALESCE(rpt_job_step_summary[error_message],"")))>0
    || LEN(TRIM(COALESCE(rpt_job_step_summary[pipeline_error_message],"")))>0'''
EXPORT_TIME = 'COALESCE(cfg_silver_export_load[last_updated_at],COALESCE(cfg_silver_export_load[ended_at],cfg_silver_export_load[started_at]))'
CONTROL_TIME = 'COALESCE(cfg_silver_load_control[ended_at],cfg_silver_load_control[started_at])'
STEP_TIME = 'COALESCE(rpt_job_step_summary[ended_at],rpt_job_step_summary[started_at])'

ACTIVITY = {
    'domains': dict(
        changes=[], critical=[],
        captures=[source('cfg_data_domain',['profiled_at'],key='run_id')],
        note='Captured profiles are discoveries. This current-only source does not retain before/after value changes.'),
    'drift': dict(
        changes=[source('cfg_schema_drift_event',DRIFT_DATES,key='drift_key')],
        critical=[],
        captures=[source('cfg_schema_drift_definition',['definition_loaded_at'])],
        note='Drift dates mark recorded first/latest detections or resolution. Definitions are captured discoveries.'),
    'contracts': dict(
        changes=[source('cfg_schema_drift_event',DRIFT_DATES,key='drift_key')],
        critical=[],
        captures=[source('cfg_bronze_schema_live',['captured_at'],key='run_id'),
                  source('cfg_schema_contract_column',['contract_loaded_at'])],
        note='Schema drift is a recorded change. Schema/contract captures are discoveries; inspect drift on Schema & Drift.'),
    'quality': dict(
        changes=[source('rpt_job_data_quality',['checked_at'],QUALITY_FAILURE),
                 source('cfg_rejected_row',['rejected_at']),
                 source('cfg_referential_exception',['detected_at'])],
        critical=[source('rpt_job_data_quality',['checked_at'],
                         f'({QUALITY_FAILURE}) && UPPER(COALESCE(rpt_job_data_quality[severity],"")) IN {{"CRITICAL","ERROR","FATAL"}}')],
        captures=[],
        note='Only failed quality findings, rejected rows and referential exceptions are highlighted. Passing checks add no activity.'),
    'loads': dict(
        changes=[source('cfg_table_load_metric',['recorded_at'],
                        'COALESCE(cfg_table_load_metric[duplicate_key_count],0)>0 || COALESCE(cfg_table_load_metric[null_primary_key_count],0)>0'),
                 source('cfg_silver_export_load',['last_updated_at','started_at'],
                        f'({EXPORT_ERROR}) || COALESCE(cfg_silver_export_load[duplicate_key_count],0)>0',date_expression=EXPORT_TIME),
                 source('cfg_silver_load_control',['started_at','ended_at'],
                        f'({CONTROL_ERROR}) || COALESCE(cfg_silver_load_control[missing_column_count],0)>0 || COALESCE(cfg_silver_load_control[extra_column_count],0)>0',date_expression=CONTROL_TIME)],
        critical=[source('cfg_table_load_metric',['recorded_at'],'COALESCE(cfg_table_load_metric[null_primary_key_count],0)>0'),
                  source('cfg_silver_export_load',['last_updated_at','started_at'],EXPORT_ERROR,date_expression=EXPORT_TIME),
                  source('cfg_silver_load_control',['started_at','ended_at'],CONTROL_ERROR,date_expression=CONTROL_TIME)],
        captures=[source('cfg_table_load_metric',['recorded_at'],key='run_id'),
                  source('cfg_silver_export_load',['last_updated_at','started_at'],key='run_id',date_expression=EXPORT_TIME),
                  source('cfg_silver_load_control',['started_at','ended_at'],key='run_id',date_expression=CONTROL_TIME)],
        note='Duplicate/null keys, schema mismatches and load errors are findings. Recorded metrics/load batches are captured discoveries.'),
    'lineage': dict(
        changes=[source('rpt_job_layer_lineage',['observed_at'],
                        f'({LINEAGE_ERROR}) || COALESCE(rpt_job_layer_lineage[duplicate_key_count],0)>0'),
                 source('rpt_job_step_summary',['started_at','ended_at'],
                        f'''({STEP_ERROR}) || COALESCE(rpt_job_step_summary[dq_checks_failed],0)>0
                        || COALESCE(rpt_job_step_summary[drift_event_count],0)>0
                        || COALESCE(rpt_job_step_summary[active_drift_count],0)>0
                        || COALESCE(rpt_job_step_summary[duplicate_rows],0)>0
                        || COALESCE(rpt_job_step_summary[null_primary_keys],0)>0''',date_expression=STEP_TIME)],
        critical=[source('rpt_job_layer_lineage',['observed_at'],LINEAGE_ERROR),
                  source('rpt_job_step_summary',['started_at','ended_at'],STEP_ERROR,date_expression=STEP_TIME)],
        captures=[source('rpt_job_layer_lineage',['observed_at'],key='job_run_id')],
        note='Lineage observations are discoveries. Unmatched/error lineage, step errors and recorded drift/quality anomalies are findings.'),
}

RECORD_DATES = {table:[date] for table,date in build.DATES.items()}
RECORD_DATES.update(cfg_schema_drift_event=DRIFT_DATES,
                    rpt_job_schema_drift=['first_detected_at','last_detected_at','resolved_at'],
                    cfg_silver_export_load=['last_updated_at','started_at','ended_at'],
                    cfg_silver_load_control=['started_at','ended_at'],
                    rpt_job_step_summary=['started_at','ended_at'])
RECORD_DATE_EXPRESSIONS={'cfg_silver_export_load':EXPORT_TIME,
                        'cfg_silver_load_control':CONTROL_TIME,
                        'rpt_job_step_summary':STEP_TIME}


def activity_name(group, channel):
    return f'Discovery {group["key"]} calendar {channel}'


def date_test(table, dates, days='Days', expression=None):
    if expression:
        return f'(NOT ISBLANK({expression}) && INT({expression}) IN {days})'
    return '('+' || '.join(f'(NOT ISBLANK({col(table,date)}) && INT({col(table,date)}) IN {days})' for date in dates)+')'


def filtered_activity(spec, job_test=True):
    table=spec['table']
    parts=[date_test(table,spec['dates'],expression=spec.get('dateExpression')), '('+spec['predicate']+')']
    if job_test and 'job_run_id' in build.columns(table):
        parts.append(f'(NOT JobChosen || {col(table,"job_run_id")} IN Jobs)')
    return f'FILTER(ALL(\'{table}\'), '+ ' && '.join(parts)+')'


def activity_dax(specs, capture=False):
    terms=[]
    for spec in specs:
        rows=filtered_activity(spec)
        if spec.get('key'):
            terms.append(f'COUNTROWS(SUMMARIZE({rows},{col(spec["table"],spec["key"])}))')
        elif capture:
            # No batch key exists: distinct retained capture timestamps mark
            # snapshots, not a fabricated job/run identifier.
            dates=','.join(col(spec['table'],d) for d in spec['dates'])
            terms.append(f'COUNTROWS(SUMMARIZE({rows},{dates}))')
        else:
            terms.append(f'COUNTROWS({rows})')
    return '''VAR Days=VALUES('Load Calendar'[Date])
VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
RETURN COALESCE('''+(' + '.join(terms) or '0')+',0)'


def scoped_expression(table, expression):
    fields=build.columns(table)
    latest=build.latest_filter(table)
    default=f'CALCULATE({expression},KEEPFILTERS({latest}))' if latest else expression
    if latest and ('run_id' in fields or 'job_run_id' in fields):
        time_filter=f'TREATAS({{[{build.name(table,"Latest time")}] }},{col(table,build.DATES[table])})'
        default=f'IF(ISBLANK([{build.name(table,"Latest key")}]),CALCULATE({expression},KEEPFILTERS({time_filter})),{default})'
    dates=RECORD_DATES.get(table)
    if not dates:
        return default
    predicates=[f'(NOT DateChosen || {date_test(table,dates,expression=RECORD_DATE_EXPRESSIONS.get(table))})']
    if 'job_run_id' in fields:
        predicates.append(f'(NOT JobChosen || {col(table,"job_run_id")} IN Jobs)')
        history='DateChosen || JobChosen'
    else:
        history='DateChosen'
    return f'''VAR DateChosen=ISFILTERED('Load Calendar'[Date])
VAR JobChosen=ISFILTERED('Discovery Job Runs'[job_run_id])
VAR Days=VALUES('Load Calendar'[Date])
VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
RETURN IF({history},CALCULATE({expression},KEEPFILTERS(FILTER('{table}',{' && '.join(predicates)}))),{default})'''


def record_measures(table):
    build.measure(build.name(table,'Rows'),
                  'COALESCE(('+scoped_expression(table,f'COUNTROWS(\'{table}\')')+'),0)','#,0')
    build.measure(build.name(table,'Visible'),f'IF([{build.name(table,"Rows")}]>0,1,0)','0')
    if table in build.DATES:
        build.measure(build.name(table,'Selected time'),
                      scoped_expression(table,f'MAX({col(table,build.DATES[table])})'),'dd MMM yyyy HH:mm')
    build.measure(build.name(table,'State'),f'''VAR n=[{build.name(table,"Rows")}]
RETURN IF(n=0,IF([Discovery history selected]=1,"No retained records for this activity selection","No discovery records available"),"Retained records: " & FORMAT(n,"#,0"))''')


def text(pid, label, value):
    v=ui.visual(pid,ui.sid(pid+':'+label))
    ui.texts(v)[0]['value']=value
    ui.put(pid,v)


def configure(root):
    ui.ROOT=root
    ui.REPORT=root/'SM WMPP Mission Control.Report'
    ui.DEF=ui.REPORT/'definition'
    ui.PAGES=ui.DEF/'pages'
    ui.TABLES=root/'SM WMPP Mission Control.SemanticModel/definition/tables'


def apply_changes(root, backup=True):
    configure(root)
    if backup:
        ui.backup()
    modes_before={p.name:[m.group(1) for m in build.re.finditer(r'\bmode: (\w+)',p.read_text(encoding='utf-8-sig'))]
                  for p in ui.TABLES.glob('*.tmdl')}
    written=[]
    original_measure=build.measure
    def track(name,dax,fmt=None):
        original_measure(name,dax,fmt)
        if name not in written:
            written.append(name)
    build.measure=track
    panels=0
    pages=[]
    try:
        for group in build.GROUPS:
            pid=build.page_id(group); primary=group['tables'][0]; activity=ACTIVITY[group['key']]
            for table in group['tables']:
                record_measures(table)
            for channel,kind in [('changes','changes'),('discoveries','captures'),('critical','critical')]:
                build.measure(activity_name(group,channel),activity_dax(activity[kind],channel=='discoveries'),'#,0')
            job_measure=activity_name(group,'linked job visible')
            job_terms=[]
            for spec in activity['changes']+activity['captures']:
                table=spec['table']
                if 'job_run_id' not in build.columns(table):
                    continue
                job_terms.append(f'COUNTROWS(FILTER(ALL(\'{table}\'),{date_test(table,spec["dates"],expression=spec.get("dateExpression"))} && ({spec["predicate"]}) && {col(table,"job_run_id")} IN Jobs))')
            build.measure(job_measure,'''VAR Days=VALUES('Load Calendar'[Date])
VAR Jobs=VALUES('Discovery Job Runs'[job_run_id])
RETURN IF('''+(' + '.join(job_terms) or '0')+'>0,1,0)','0')
            context=build.name(primary,'Context')
            build.measure(context,f'''VAR Day=SELECTEDVALUE('Load Calendar'[Date])
VAR Time=[{build.name(primary,'Latest time')}]
RETURN IF([Discovery history selected]=1,"Historical activity" & IF(NOT ISBLANK(Day)," · " & FORMAT(Day,"dd MMM yyyy")," · linked job"),IF(ISBLANK(Time),"No latest discovery available","Latest discovery · " & FORMAT(Time,"dd MMM yyyy HH:mm")))''')
            dims=','.join(col(primary,c) for c in group['metric'][1])
            build.measure(build.name(primary,'Scope count'),'COALESCE(('+scoped_expression(primary,f'COUNTROWS(SUMMARIZE(\'{primary}\',{dims}))')+'),0)','#,0')
            build.measure(build.name(primary,'Distinct objects'),'COALESCE(('+scoped_expression(primary,f'DISTINCTCOUNT({col(primary,group["distinct"][1])})')+'),0)','#,0')
            key='run_id' if 'run_id' in build.columns(primary) else 'job_run_id'
            build.measure(build.name(primary,'Discovery batches'),'COALESCE(('+scoped_expression(primary,f'DISTINCTCOUNT({col(primary,key)})')+'),0)','#,0')

            heat=ui.visual(pid,ui.sid(pid+':calendar'))
            aliases={'changes':'Changes / findings','discoveries':'Captured discoveries','critical':'Critical / error findings'}
            query=heat['visual']['query']['queryState']['dataset']
            query['projections']=[ui.projection('Load Calendar','Date','Column'),ui.projection('Load Calendar','Weekday','Column')]+[
                ui.projection('_MissionControl_Measures',activity_name(group,channel),label=alias)
                for channel,alias in aliases.items()]
            props=ui.props(heat['visual']['objects'],'vega')
            raw=props['jsonSpec']['expr']['Literal']['Value']
            spec=json.loads(raw[1:-1].replace("''","'"))
            spec['encoding']['color']={'condition':[
                {'test':"datum['Critical / error findings'] > 0",'value':'#D35A66'},
                {'test':"datum['Changes / findings'] >= 10",'value':'#CBF576'},
                {'test':"datum['Changes / findings'] >= 5",'value':'#91C977'},
                {'test':"datum['Changes / findings'] >= 2",'value':'#4C854F'},
                {'test':"datum['Changes / findings'] > 0",'value':'#345B3D'},
                {'test':"datum['Captured discoveries'] > 0",'value':'#537E87'}], 'value':ui.ALT}
            spec['encoding']['tooltip']=[{'field':'Date','type':'temporal','title':'Activity date','format':'%a %d %b %Y'}]+[
                {'field':alias,'type':'quantitative','title':alias} for alias in aliases.values()]
            props['jsonSpec']=ui.string(json.dumps(spec,ensure_ascii=False))
            ui.put(pid,heat)
            job=ui.visual(pid,ui.sid(pid+':filter:Job ID · historical selection'))
            job['filterConfig']['filters']=[f for f in job['filterConfig']['filters']
                if f.get('field',{}).get('Measure',{}).get('Property')!='Discovery job picker visible']
            ui.add_filter(job,job_measure)
            ui.props(job['visual']['objects'],'header')['text']=ui.string('Linked job ID · where recorded')
            ui.put(pid,job)
            text(pid,'calendar-heading','Change & discovery history · last 365 days')
            text(pid,'calendar-note','Select an activity day. Linked Job IDs appear where recorded. Clear date and job to return to latest.')
            text(pid,'calendar-legend','Green = changes/findings · Red = critical/errors · Blue = captured discoveries · Empty = no retained activity')
            text(pid,'retention-note','Calendar uses retained detection/capture dates. Current-reference tabs stay separate; job links are shown only where recorded.')
            text(pid,'intro',activity['note'])
            for table in group['tables']:
                dates=RECORD_DATES.get(table)
                note=('Latest retained discovery by default; calendar filters the recorded detection/capture dates. Empty means no retained record for that date.' if dates else
                      'Current reference only; no detection/capture timestamp is recorded. Calendar selection cannot reconstruct prior values.')
                if dates and 'job_run_id' not in build.columns(table):
                    note+=' No job-run link is recorded.'
                if table in {'cfg_schema_drift_event','rpt_job_schema_drift'}:
                    note='Calendar matches retained first/latest detection or resolution dates. The register shows the current event record; intervening occurrences are not reconstructed.'
                text(pid,'table-note:'+table,note)
            # Negative z places these backgrounds behind the canvas in Desktop.
            for path in (ui.PAGES/pid/'visuals').glob('*/visual.json'):
                v=ui.load(path)
                if v['visual']['visualType']=='shape' and v['position']['z']<0:
                    v['position'].update(z=6000,tabOrder=6000)
                    ui.save(path,v);panels+=1
            pages.append({'pageId':pid,'displayName':group['title'],'calendarId':heat['name'],
                          'measures':[activity_name(group,ch) for ch in aliases],
                          'sources':activity,'recordTables':group['tables']})
    finally:
        build.measure=original_measure
    modes_after={p.name:[m.group(1) for m in build.re.finditer(r'\bmode: (\w+)',p.read_text(encoding='utf-8-sig'))]
                 for p in ui.TABLES.glob('*.tmdl')}
    assert modes_before==modes_after,'Storage modes changed unexpectedly'
    manifest={'scope':'Six new monitoring pages only','pages':pages,'writtenMeasures':written,
              'recordDates':RECORD_DATES,'recordDateExpressions':RECORD_DATE_EXPRESSIONS,'restoredPanels':panels,
              'sourceRefresh':'None; existing cached data is preserved',
              'semantics':'Captured discoveries are separate from confirmed findings. Job success is not a calendar activity signal.'}
    ui.save(root/'Change and discovery calendar revision.json',manifest)
    print(json.dumps({'pages':len(pages),'measures':len(written),'restoredPanels':panels,'storageModesPreserved':True},indent=2))
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',required=True,type=Path)
    parser.add_argument('--no-backup',action='store_true')
    args=parser.parse_args()
    apply_changes(args.project_root.resolve(),not args.no_backup)
