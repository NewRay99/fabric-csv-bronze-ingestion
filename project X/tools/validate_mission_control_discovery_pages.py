"""Check model references, layout, table coverage and retained-history wiring."""
from __future__ import annotations

import json
import re

import build_mission_control_discovery_pages as build
import refine_mission_control_wip as ui

def validate():
    fields={}
    for path in ui.TABLES.glob('*.tmdl'):
        source=path.read_text(encoding='utf-8-sig')
        fields[path.stem]={
            'Column':set(m.group(1).split(' =',1)[0].strip("'") for m in re.finditer(r'^\tcolumn (.+)$',source,re.M)),
            'Measure':set(m.group(1).strip("'") for m in re.finditer(r'^\tmeasure (.+?) =',source,re.M))}
    unresolved=[];bounds=[];count=0
    def walk(node, path):
        if isinstance(node,dict):
            for kind in ('Column','Measure'):
                expr=node.get(kind)
                if isinstance(expr,dict):
                    entity=expr.get('Expression',{}).get('SourceRef',{}).get('Entity')
                    prop=expr.get('Property')
                    if entity and prop and (entity not in fields or prop not in fields[entity][kind]):
                        unresolved.append((str(path),entity,kind,prop))
            for value in node.values():walk(value,path)
        elif isinstance(node,list):
            for value in node:walk(value,path)
    for path in ui.PAGES.glob('*/page.json'):
        page=ui.load(path);walk(page,path)
        for vp in (path.parent/'visuals').glob('*/visual.json'):
            v=ui.load(vp);walk(v,vp);count+=1
            p=v['position']
            if p['x']<0 or p['y']<0 or p['x']+p['width']>page['width'] or p['y']+p['height']>page['height']:
                bounds.append(str(vp))
    assert not unresolved,unresolved
    assert not bounds,bounds
    expected={table for group in build.GROUPS for table in group['tables']}
    covered=set();heatmaps=0;table_tabs=0
    for group in build.GROUPS:
        pid=build.page_id(group)
        for table in group['tables']:
            v=ui.visual(pid,ui.sid(pid+':register:'+table))
            projection_tables={p['field']['Column']['Expression']['SourceRef']['Entity']
                for p in v['visual']['query']['queryState']['Values']['projections']}
            assert projection_tables=={table}
            assert any(f['field'].get('Measure',{}).get('Property')==build.name(table,'Visible')
                for f in v['filterConfig']['filters'])
            covered.add(table)
        heat=ui.visual(pid,ui.sid(pid+':calendar'))
        measures={p['field']['Measure']['Property'] for p in heat['visual']['query']['queryState']['dataset']['projections'] if 'Measure' in p['field']}
        assert measures=={'Discovery calendar jobs','Discovery calendar failures','Discovery calendar other'}
        assert heat['visual']['objects']['vega'][0]['properties']['enableSelection']['expr']['Literal']['Value']=='true'
        page=ui.load(ui.PAGES/pid/'page.json')
        for table in group['tables']:
            assert {'source':heat['name'],'target':ui.sid(pid+':register:'+table),'type':'DataFilter'} in page['visualInteractions']
        for label in group['labels']:
            b=ui.load(ui.DEF/'bookmarks'/(ui.sid(pid+':tab:'+label)+'.bookmark.json'))
            assert b['options']['suppressData'] is True
            assert b['options']['suppressActiveSection'] is True
            table_tabs+=1
        heatmaps+=1
    assert covered==expected
    result={'status':'PASS','pages':len(ui.load(ui.PAGES/'pages.json')['pageOrder']),
            'visuals':count,'newPages':6,'newTablesCovered':len(covered),'liveHistoryCalendars':heatmaps,
            'displayOnlyTableTabs':table_tabs,'unresolvedFields':len(unresolved),'outOfBoundsVisuals':len(bounds),
            'dataValidation':'Native DirectQuery figures and historical interactions still require Power BI report-view verification.'}
    ui.save(ui.ROOT/'Discovery page structural validation.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':validate()
