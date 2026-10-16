"""Create dark PBIR phone layouts without changing Desktop or model definitions."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import zipfile
from datetime import datetime

from PIL import ImageFont
import refine_mission_control_wip as ui

SCHEMA = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainerMobileState/2.4.0/schema.json'
WIDTH, MARGIN, GAP = 323, 12, 8
BODY = WIDTH - MARGIN*2
TOOLTIP = '2af45662f5a13e0c063b'
FONT = Path('C:/Windows/Fonts/segoeui.ttf')
FONT_BOLD = Path('C:/Windows/Fonts/segoeuib.ttf')
INTRO = {
    ui.CAL: 'Latest monitoring discoveries. Flags: red = latest load day; amber = prior 7 days; grey = history; white = no recorded problems. Tap a section for details.',
    ui.TIMELINES: 'Latest load by default. Calendar drillthrough carries the chosen day and pipeline. Select a job to inspect its steps.',
    ui.QUALITY: 'Newest cached load. Filter checks by severity, table and status. Schema is an independent inventory.',
    ui.DETAIL: 'Inspect the selected job, steps and pipeline executions. Without a selection, the cards show the latest cached run.',
    '5133b9c7cfcf12cf7f74': 'Latest matching archive batches and Gold snapshots. Their filters and status measures retain separate contexts.',
}

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def protected(root):
    paths = list((root/'SM WMPP Mission Control.Report').rglob('*')) + list((root/'SM WMPP Mission Control.SemanticModel/definition').rglob('*'))
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths
            if p.is_file() and p.name != 'mobile.json' and '.pbi' not in p.relative_to(root).parts}

def kind(v):
    return v.get('visual', {}).get('visualType', 'group')

def text(v):
    return ' '.join(str(r.get('value','')) for o in v.get('visual',{}).get('objects',{}).get('general',[])
                    for p in o.get('properties',{}).get('paragraphs',[]) for r in p.get('textRuns',[]))

def bold_text(v):
    styles=[r.get('textStyle',{}) for o in v.get('visual',{}).get('objects',{}).get('general',[])
            for p in o.get('properties',{}).get('paragraphs',[]) for r in p.get('textRuns',[])]
    return any(str(s.get('fontWeight','')).lower() in ('bold','600','700') or 'bold' in s.get('fontFamily','').lower() for s in styles)

def literal(value):
    return value.get('expr',{}).get('Literal',{}).get('Value','').strip("'").replace("''","'")

def measure(v):
    return ' / '.join(p.get('nativeQueryRef','') for q in v.get('visual',{}).get('query',{}).get('queryState',{}).values()
                    for p in q.get('projections',[]))

def button_label(v):
    return next((literal(e.get('properties',{}).get('text',{})) for e in v.get('visual',{}).get('objects',{}).get('text',[])
                 if literal(e.get('properties',{}).get('text',{}))), '')

def lines(words, width, points=9, bold=False):
    font=ImageFont.truetype(str(FONT_BOLD if bold else FONT), round(points*4/3))
    result=[]
    for para in words.split('\n') or ['']:
        line=''
        for word in para.split():
            candidate=(line+' '+word).strip()
            if line and font.getlength(candidate)>width:
                result.append(line); line=word
            else:
                line=candidate
        result.append(line)
    return result or ['']

def text_height(words, width, points=9, bold=False):
    # The native textbox reserves an inset and scrollbar space even when the
    # source paragraph has no margins. Measure inside that usable width.
    usable_width = max(1, width-12)
    return max(math.ceil(points*4/3+6), len(lines(words,usable_width,points,bold))*math.ceil(points*4/3*1.35)+4)

def set_props(objects, group, properties, selector=None):
    entries=objects.setdefault(group,[])
    entry=next((e for e in entries if e.get('selector') == selector),None)
    if entry is None:
        entry={'properties':{}}
        if selector is not None: entry['selector']=copy.deepcopy(selector)
        entries.append(entry)
    entry.setdefault('properties',{}).update(properties)

def mobile_button(source, label=None):
    objects={}
    src=source['visual'].get('objects',{})
    fallback=button_label(source) or label or 'Open'
    for name in (None,'default','hover','selected','disabled'):
        selector={'id':name} if name else None
        base=next((e.get('properties',{}) for e in src.get('text',[]) if e.get('selector') is None),{})
        state=next((e.get('properties',{}) for e in src.get('text',[]) if e.get('selector') == selector),{})
        props=copy.deepcopy(base); props.update(copy.deepcopy(state))
        state_label=literal(props.get('text',{}))
        props.update(show=ui.lit('true'),text=ui.string(state_label or fallback),fontSize=ui.lit('9D'),
                     fontFamily=ui.string('Segoe UI'),fontColor=ui.color('#CBF576'),
                     horizontalAlignment=ui.string('center'),verticalAlignment=ui.string('middle'),
                     leftMargin=ui.lit('8D'),rightMargin=ui.lit('8D'),topMargin=ui.lit('0D'),bottomMargin=ui.lit('0D'))
        if name == 'disabled' and state.get('fontColor'):
            props['fontColor'] = copy.deepcopy(state['fontColor'])
        set_props(objects,'text',props,selector)
        set_props(objects,'fill',{'show':ui.lit('true'),'fillColor':ui.color(ui.ALT if name != 'hover' else '#34463A'),'transparency':ui.lit('0D')},selector)
        set_props(objects,'icon',{'show':ui.lit('false')},selector)
    set_props(objects,'shape',{'tileShape':ui.string('rectangle'),'roundEdge':ui.lit('6D')})
    return objects

def phone_calendar(original):
    # Preserve every original record and identity. Facet the 53-week year into
    # four 14-week bands instead of shrinking the day squares across one row.
    spec=copy.deepcopy(original)
    transforms=spec.pop('transform',[])
    transforms += [{'joinaggregate':[{'op':'min','field':'WeekStart','as':'Phone first week'}]},
                   {'calculate':"floor(datum.WeekStart / 604800000) - floor(datum['Phone first week'] / 604800000)",'as':'Phone week'},
                   {'calculate':"floor(datum['Phone week'] / 14)",'as':'Phone band'}]
    unit={k:spec[k] for k in ('mark','encoding')}
    unit.update(width=249,height=126)
    for axis_key in ('x','y'):
        axis=unit['encoding'][axis_key].setdefault('axis',{})
        axis.update(labelFontSize=9,labelPadding=3)
    unit['mark'].update(strokeWidth=1,cornerRadius=1)
    return {'$schema':spec['$schema'],'data':{'name':'dataset'},'transform':transforms,'padding':0,
            'facet':{'row':{'field':'Phone band','type':'ordinal','header':{'labels':False,'title':None}}},
            'spec':unit,'spacing':12,'resolve':{'scale':{'x':'independent','y':'shared'}},
            'config':{**spec.get('config',{}),'background':ui.PANEL,'view':{'stroke':None},'facet':{'spacing':12}}}

def phone_deneb(source):
    original=source['visual']['objects']['vega'][0]['properties']['jsonSpec']['expr']['Literal']['Value']
    spec=json.loads(original[1:-1].replace("''","'"))
    refs=measure(source)
    if 'Flag code' in refs:
        spec.update(width=80,height=70)
        for layer in spec['layer']:
            layer['encoding']['x']['value']=40
            if layer['mark']['type']=='text': layer['mark']['fontSize']=9
        return spec,80,70,'recency flag'
    if 'Weekday' in refs and 'Date' in refs:
        return phone_calendar(spec),275,600,'four-band calendar'
    # Timeline labels keep room for the time axis and each row remains legible.
    spec['width']=164
    if isinstance(spec.get('height'),dict): spec['height']={'step':28}
    def axes(node):
        if isinstance(node,dict):
            for key,value in node.items():
                if key=='axis' and isinstance(value,dict):
                    value.update(labelFontSize=9)
                    if 'labelLimit' in value: value['labelLimit']=80
                    if value.get('format')=='%H:%M': value['tickCount']=4
                else: axes(value)
        elif isinstance(node,list):
            for value in node: axes(value)
    axes(spec)
    # Shorten only displayed axis labels. The full unique Run label remains
    # the y grouping key, so repeated notebook names cannot merge job rows.
    if 'notebook_name' in refs:
        spec['encoding']['y']['axis']['labelExpr']="split(datum.label, ' · ')[2] + ' · ' + split(datum.label, ' · ')[1]"
    else:
        spec['encoding']['y']['axis']['labelExpr']="substring(split(datum.label, ' · ')[2], 0, 8) + ' · ' + split(datum.label, ' · ')[0]"
    spec.setdefault('config',{}).setdefault('axis',{}).update(labelFontSize=9,labelColor=ui.MUTED,titleColor=ui.TEXT)
    return spec,275,280,'timeline'

class PhonePage:
    def __init__(self,pid,page,sources):
        self.pid,self.page,self.sources=pid,page,sources
        self.mobile={}; self.records=[]; self.used=set(); self.y=12
        self.button_words={}; self.omit=set()
        self.match_button_labels()
        self.discovery=page['displayName'] in {'Domains & Reference','Schema & Drift','Contracts & Schema','Quality & Exceptions','Load Metrics & Control','Lineage & Step Summary'}
        if pid==ui.CAL:
            # A long single-value card cannot wrap into a readable phone legend.
            # The phone intro and each light's existing label carry the legend.
            self.omit.update(v['name'] for v in sources.values() if measure(v)=='Watch Tower Flag Legend' or
                             (kind(v)=='textbox' and text(v) in ('Less','More','! Failed    ~ Running / other')))

    def match_button_labels(self):
        # Old desktop navigation used a transparent button plus a separate
        # textbox. Place the complete label inside the native phone button.
        for v in self.sources.values():
            if kind(v)!='actionButton': continue
            p=v['position']; chosen=[]
            for t in self.sources.values():
                if kind(t)!='textbox' or not text(t).strip(): continue
                q=t['position']; cx=q['x']+q['width']/2;cy=q['y']+q['height']/2
                if p['x']-2<=cx<=p['x']+p['width']+2 and p['y']-2<=cy<=p['y']+p['height']+2:
                    chosen.append(t)
            if chosen:
                t=min(chosen,key=lambda t:abs(t['position']['y']-p['y']))
                self.button_words[v['name']]=text(t)
                self.omit.add(t['name'])

    def put(self,v,x,y,w,h,role='body',points=None,words=None):
        assert v['name'] not in self.mobile,(self.page['displayName'],v['name'])
        state={'$schema':SCHEMA,'position':{'x':round(x,2),'y':round(y,2),'width':round(w,2),'height':math.ceil(h),
                'z':100 if kind(v)=='shape' else 5000+len(self.records),'tabOrder':len(self.records)*10}}
        objects={}; container={}
        vt=kind(v); shown_words=words if words is not None else text(v)
        if vt=='textbox':
            size=points if points is not None else 9
            paragraphs=copy.deepcopy(v['visual'].get('objects',{}).get('general',[{}])[0].get('properties',{}).get('paragraphs',[]))
            if words is not None:
                style=copy.deepcopy(paragraphs[0]['textRuns'][0].get('textStyle',{})) if paragraphs else {}
                paragraphs=[{'textRuns':[{'value':words,'textStyle':style}]}]
            for paragraph in paragraphs:
                for run in paragraph.get('textRuns',[]):
                    run.setdefault('textStyle',{}).update(fontSize=f'{size:g}pt',fontFamily='Segoe UI')
            set_props(objects,'general',{'paragraphs':paragraphs})
        elif vt=='cardVisual':
            size=points if points is not None else 9
            for entry in v['visual'].get('objects',{}).get('value',[{}]):
                props=copy.deepcopy(entry.get('properties',{})); props['fontSize']=ui.lit(f'{size:g}D')
                set_props(objects,'value',props,entry.get('selector'))
            for group in ('layout','padding'):
                if group in v['visual'].get('objects',{}): objects[group]=copy.deepcopy(v['visual']['objects'][group])
        elif vt=='actionButton':
            objects=mobile_button(v,words or self.button_words.get(v['name']))
            shown_words=button_label(v) or words or self.button_words.get(v['name'],'Open')
        elif vt=='slicer':
            for group in ('header','items'):
                entries=v['visual'].get('objects',{}).get(group,[{}])
                for entry in entries:
                    props=copy.deepcopy(entry.get('properties',{})); props['fontSize']=ui.lit('9D')
                    set_props(objects,group,props,entry.get('selector'))
            # Source selections and semantic fields continue to come from the desktop visual.
        elif vt in ('tableEx','pivotTable'):
            for group in ('values','columnHeaders','rowHeaders'):
                for entry in v['visual'].get('objects',{}).get(group,[]):
                    props=copy.deepcopy(entry.get('properties',{})); props['fontSize']=ui.lit('9D')
                    set_props(objects,group,props,entry.get('selector'))
            set_props(objects,'grid',{'rowPadding':ui.lit('3D')})
            for entry in v['visual'].get('objects',{}).get('columnWidth',[]):
                value=literal(entry.get('properties',{}).get('value',{}))
                if re.fullmatch(r'[\d.]+[DL]?',value):
                    n=float(value.rstrip('DL'))
                    set_props(objects,'columnWidth',{'value':ui.lit(f'{0 if n==0 else max(65,min(n*.8,180)):g}D')},entry.get('selector'))
            if self.pid==ui.CAL and v['name']=='52b0db0e9f2a1ebfb85e':
                # Seven day columns and a slim dark week header fit the phone.
                # Long tile statuses wrap instead of widening the entire matrix.
                for entry in v['visual']['objects'].get('columnWidth',[]):
                    width=26 if entry.get('selector',{}).get('metadata')=='Load Calendar.Week' else 35
                    set_props(objects,'columnWidth',{'value':ui.lit(f'{width}D')},entry.get('selector'))
                for entry in objects.get('values',[]):
                    entry['properties'].update(fontSize=ui.lit('8D'),wordWrap=ui.lit('true'))
                for group in ('columnHeaders','rowHeaders'):
                    for entry in objects.get(group,[]):
                        entry['properties'].update(fontSize=ui.lit('8D'),wordWrap=ui.lit('true'))
        elif vt.startswith('deneb'):
            spec,_,_,chart_role=phone_deneb(v)
            objects={'vega':[{'properties':{'jsonSpec':ui.string(json.dumps(spec,ensure_ascii=False))}}],
                     'stateManagement':[{'properties':{'viewportWidth':ui.lit(f'{w:g}D'),'viewportHeight':ui.lit(f'{h:g}D')}}]}
            role=chart_role
        if vt!='shape':
            set_props(container,'visualHeader',{'show':ui.lit('false')})
            set_props(container,'title',{'fontSize':ui.lit('10D'),'titleWrap':ui.lit('true')})
            set_props(container,'subTitle',{'fontSize':ui.lit('9D')})
        if objects:state['objects']=objects
        if container:state['visualContainerObjects']=container
        self.mobile[v['name']]=state;self.used.add(v['name'])
        self.records.append({'id':v['name'],'type':vt,'role':role,'text':shown_words or measure(v),
                             'hidden':v.get('isHidden',False),'position':copy.deepcopy(state['position'])})
        return h

    def block(self,v,height=None,points=None,words=None,role='body'):
        if height is None: height=self.height(v,BODY,points,words)
        self.put(v,MARGIN,self.y,BODY,height,role,points,words)
        self.y+=height+GAP

    def height(self,v,w,points=None,words=None):
        vt=kind(v)
        if vt=='textbox': return text_height(words if words is not None else text(v),w,points or 9,bold_text(v))
        if vt=='slicer':return 62
        if vt=='actionButton':return max(44,text_height(button_label(v) or self.button_words.get(v['name'],'Open'),w-16,9)+12)
        if vt in ('tableEx','pivotTable'):return 340 if vt=='tableEx' else 620
        if vt.startswith('deneb'):return phone_deneb(v)[2]
        if vt=='cardVisual':return 44 if ' ID' in measure(v) else 34
        return max(28,min(v['position']['height'],48))

    def header(self):
        for y,size in ((22,8),(53,14),(102,9)):
            candidates=[v for v in self.sources.values() if kind(v)=='textbox' and abs(v['position']['y']-y)<2]
            if not candidates:continue
            v=min(candidates,key=lambda v:v['position']['x'])
            words=self.page['displayName'] if y==53 else INTRO.get(self.pid,text(v)) if y==102 else text(v)
            self.block(v,points=size,words=words,role='page title' if y==53 else 'header')
        self.y+=4

    def panel_contents(self,panel):
        p=panel['position'];result=[]
        for v in self.sources.values():
            if v['name']==panel['name'] or v['name'] in self.used|self.omit or kind(v)=='shape':continue
            q=v['position'];cx=q['x']+q['width']/2;cy=q['y']+q['height']/2
            if p['x']<=cx<=p['x']+p['width'] and p['y']<=cy<=p['y']+p['height']:result.append(v)
        return result

    def summary(self,panel,children):
        x,y=MARGIN,self.y; w,h=BODY,204
        self.put(panel,x,y,w,h,'summary background')
        for v in children:
            vt=kind(v);p=v['position'];ref=measure(v)
            if vt=='actionButton':self.put(v,x+w-44,y+8,40,40,'summary link')
            elif vt.startswith('deneb'):self.put(v,x+w-92,y+52,80,70,'recency flag')
            elif vt=='textbox':
                is_heading=p['y']<190
                self.put(v,x+12,y+(12 if is_heading else 92),w-(68 if is_heading else 139),24 if is_heading else 22,
                         'summary heading' if is_heading else 'summary unit',12 if is_heading else 9)
            elif vt=='cardVisual':
                if ref.endswith(' Count'):self.put(v,x+12,y+44,160,42,'summary value',24)
                elif ref.endswith(' Detail'):self.put(v,x+12,y+122,w-24,22,'summary detail',9)
                elif ref.endswith(' Reference'):self.put(v,x+12,y+148,w-24,20,'summary reference',8)
                elif ref.endswith(' Date'):self.put(v,x+12,y+178,w-24,20,'summary date',8)
        self.y+=h+GAP

    def kpi(self,panel,children,x,y,w,h):
        self.put(panel,x,y,w,h,'KPI background')
        labels=sorted([v for v in children if kind(v)=='textbox'],key=lambda v:v['position']['y'])
        cards=[v for v in children if kind(v)=='cardVisual']
        local=y+12
        for v in labels[:1]:
            th=max(24,text_height(text(v),w-24,9,True))
            self.put(v,x+12,local,w-24,th,'KPI label',9);local+=th+4
        for v in cards:
            ref=measure(v)
            size=9 if ' ID' in ref else 12 if 'Status' in ref else 22
            self.put(v,x+12,local,w-24,38,'KPI value',size);local+=42
        for v in labels[1:]:
            th=text_height(text(v),w-24,8)
            self.put(v,x+12,local,w-24,th,'KPI context',8);local+=th+2
        return local-y+10

    def ordinary_panel(self,panel,children):
        start=self.y;local=start+12; width=BODY-24
        grouped=[]
        for v in sorted(children,key=lambda v:(v['position']['y'],v['position']['x'])):
            # Mutually exclusive table/caption and chart alternatives share one slot.
            same=next((r for r in grouped if abs(r[0]['position']['y']-v['position']['y'])<3 and
                       abs(r[0]['position']['x']-v['position']['x'])<3 and (kind(r[0])==kind(v) or
                       (kind(r[0]) in ('tableEx','pivotTable') or kind(r[0]).startswith('deneb')) and
                       (kind(v) in ('tableEx','pivotTable') or kind(v).startswith('deneb')))),None)
            if same is not None and any(t.get('isHidden') for t in same+[v]):same.append(v)
            else:grouped.append([v])
        # The two Watch Tower calendars use different desktop positions, but
        # their existing visibility-only bookmarks swap them in the same area.
        if self.pid==ui.CAL:
            annual=[r for r in grouped if r[0]['name']=='e263e453f96be0512a19']
            monthly=[r for r in grouped if r[0]['name']=='52b0db0e9f2a1ebfb85e']
            if annual and monthly:
                monthly[0].extend(annual[0]);grouped.remove(annual[0])
        panel_record_count=len(self.records)
        index=0
        while index<len(grouped):
            row=grouped[index];v=row[0];vt=kind(v)
            if vt=='actionButton':
                buttons=[v];next_index=index+1
                while next_index<len(grouped) and kind(grouped[next_index][0])=='actionButton' and abs(grouped[next_index][0]['position']['y']-v['position']['y'])<3:
                    buttons.append(grouped[next_index][0]);next_index+=1
                if len(buttons)>1:
                    half=(width-GAP)/2
                    for i,b in enumerate(buttons):
                        self.put(b,MARGIN+12+(i%2)*(half+GAP),local+(i//2)*52,half,44,'view tab')
                    local+=math.ceil(len(buttons)/2)*52;index=next_index;continue
            points=12 if vt=='textbox' and index==0 else 9
            height=max(self.height(item,width,points if kind(item)=='textbox' else None) for item in row)
            if any(kind(item).startswith('deneb') and 'Weekday' in measure(item) for item in row):
                height=max(600,620 if any(kind(item)=='pivotTable' for item in row) else 0)
            for item in row:
                actual_points=points if kind(item)=='textbox' else 9 if kind(item)=='cardVisual' else None
                self.put(item,MARGIN+12,local,width,height,'section content',actual_points)
            local+=height+GAP;index+=1
        panel_height=local-start+4
        self.put(panel,MARGIN,start,BODY,panel_height,'section background')
        self.y=local+16

    def loose(self,items):
        items=sorted(items,key=lambda v:(v['position']['y'],v['position']['x']))
        index=0
        while index<len(items):
            v=items[index];vt=kind(v)
            if v['name'] in self.used|self.omit or vt in ('image','shape','group'):
                index+=1;continue
            if vt=='textbox':
                p=v['position']
                following=next((c for c in items if c['name'] not in self.used and kind(c)=='cardVisual' and
                                abs(c['position']['x']-p['x'])<4 and -3<=c['position']['y']-p['y']-p['height']<=18),None)
                if following is not None:
                    self.block(v,role='context label')
                    self.block(following,role='context value')
                    index+=1;continue
            if vt=='actionButton':
                buttons=[v];j=index+1
                while j<len(items) and kind(items[j])=='actionButton' and abs(items[j]['position']['y']-v['position']['y'])<3:
                    buttons.append(items[j]);j+=1
                if len(buttons)>1:
                    half=(BODY-GAP)/2
                    for i,b in enumerate(buttons):self.put(b,MARGIN+(i%2)*(half+GAP),self.y+(i//2)*52,half,44,'page navigation')
                    self.y+=math.ceil(len(buttons)/2)*52+GAP;index=j;continue
            self.block(v,role='page navigation' if vt=='actionButton' else 'filter' if vt=='slicer' else 'context')
            index+=1

    def plan(self):
        self.header()
        panels=[v for v in self.sources.values() if kind(v)=='shape' and v['position']['width']>=240 and v['position']['height']>=70]
        panels.sort(key=lambda v:(v['position']['y'],v['position']['x']))
        ownership={p['name']:self.panel_contents(p) for p in panels}
        owned={v['name'] for values in ownership.values() for v in values}
        loose=[v for v in self.sources.values() if v['name'] not in owned|self.used|self.omit and kind(v) not in ('shape','image','group')]
        group_nav=[]
        if self.discovery:
            group_nav=[v for v in loose if kind(v)=='actionButton' and abs(v['position']['y']-148)<3]
            loose=[v for v in loose if v not in group_nav]
            def flow_order(panel):
                contents=ownership[panel['name']]
                if any(kind(v)=='slicer' for v in contents):return (0,0)
                if panel['position']['height']<=150:return (1,panel['position']['x'])
                if any(kind(v).startswith('deneb') for v in contents):return (2,0)
                return (3,0)
            panels.sort(key=flow_order)
        index=0
        while index<len(panels):
            panel=panels[index];children=ownership[panel['name']]
            if self.discovery and any(kind(v).startswith('deneb') for v in children):
                self.loose([v for v in loose if kind(v)=='slicer' and v['name'] not in self.used])
            before=[v for v in loose if v['name'] not in self.used and v['position']['y']<panel['position']['y']]
            self.loose(before)
            if not children:index+=1;continue
            if any(kind(v).startswith('deneb') and 'Flag code' in measure(v) for v in children):
                self.summary(panel,children);index+=1;continue
            simple=all(kind(v) in ('textbox','cardVisual') for v in children) and sum(kind(v)=='cardVisual' for v in children)==1 and panel['position']['height']<=150
            if simple:
                batch=[panel];j=index+1
                while j<len(panels) and abs(panels[j]['position']['y']-panel['position']['y'])<3:
                    batch.append(panels[j]);j+=1
                for k in range(0,len(batch),2):
                    pair=batch[k:k+2]
                    if any(' ID' in measure(v) for p in pair for v in ownership[p['name']] if kind(v)=='cardVisual'):
                        for p in pair:
                            h=140; self.kpi(p,ownership[p['name']],MARGIN,self.y,BODY,h);self.y+=h+GAP
                    else:
                        half=(BODY-GAP)/2; h=140
                        for col,p in enumerate(pair):self.kpi(p,ownership[p['name']],MARGIN+col*(half+GAP),self.y,half if len(pair)==2 else BODY,h)
                        self.y+=h+GAP
                index=j;continue
            self.ordinary_panel(panel,children);index+=1
        self.loose(group_nav)
        self.loose([v for v in loose if v['name'] not in self.used])
        # Useful charts/tables must have a phone placement, including hidden alternatives.
        mandatory=[v['name'] for v in self.sources.values() if v['name'] not in self.omit and
                   (kind(v) in ('slicer','tableEx','pivotTable','cardVisual') or kind(v).startswith('deneb'))]
        assert all(vid in self.mobile for vid in mandatory),(self.page['displayName'],set(mandatory)-set(self.mobile))
        return {'id':self.pid,'name':self.page['displayName'],'height':self.y,'mobileVisuals':len(self.mobile),
                'records':self.records,'mandatoryVisuals':mandatory,'omittedDuplicatedLabels':sorted(self.omit)}

def overlap(a,b):
    return min(a['x']+a['width'],b['x']+b['width'])-max(a['x'],b['x'])>.5 and min(a['y']+a['height'],b['y']+b['height'])-max(a['y'],b['y'])>.5

def validate_plan(root,pages,plans):
    default_overlaps=[];bookmark_overlaps=[];state_checks=0
    for page in pages:
        records=page['records'];by_id={r['id']:r for r in records}
        def check(hidden):
            relevant=[r for r in records if r['type'] not in ('shape','image') and not hidden.get(r['id'],r['hidden'])]
            return [(a['id'],b['id']) for i,a in enumerate(relevant) for b in relevant[i+1:] if overlap(a['position'],b['position'])]
        default_overlaps += [(page['name'],a,b) for a,b in check({})]
        for bookmark_path in (root/'SM WMPP Mission Control.Report/definition/bookmarks').glob('*.bookmark.json'):
            bookmark=read(bookmark_path)
            state=bookmark.get('explorationState',{}).get('sections',{}).get(page['id'],{}).get('visualContainers',{})
            if not state:continue
            hidden={vid:value.get('singleVisual',{}).get('display',{}).get('mode')=='hidden' for vid,value in state.items()}
            bookmark_overlaps += [(page['name'],bookmark['name'],a,b) for a,b in check(hidden)]
            state_checks+=1
        for r in records:
            p=r['position']
            assert 0<=p['x'] and p['x']+p['width']<=WIDTH+.1 and p['y']>=0 and p['height']>0,(page['name'],r)
            if r['type']=='actionButton':assert p['height']>=40,(page['name'],r)
        assert page['height']<9600,(page['name'],'Phone canvas too long')
    assert not default_overlaps,default_overlaps[:20]
    assert not bookmark_overlaps,bookmark_overlaps[:20]
    return {'status':'PASS','pages':len(pages),'phoneVisuals':len(plans),'visibleOverlaps':0,
            'bookmarkStatesChecked':state_checks,'bookmarkOverlaps':0,'phoneWidth':WIDTH,
            'minimumButtonHeight':40,'tableFontPoints':9,'bodyFontPoints':9,'protectedDesktopAndModel':True}

def build(root,apply=False,no_backup=False):
    baseline=protected(root)
    folder=root/'SM WMPP Mission Control.Report/definition/pages'
    page_order=read(folder/'pages.json')['pageOrder']
    pages=[];plans={}
    for pid in page_order:
        if pid==TOOLTIP:continue
        page=read(folder/pid/'page.json')
        sources={p.parent.name:read(p) for p in (folder/pid/'visuals').glob('*/visual.json')}
        planner=PhonePage(pid,page,sources)
        pages.append(planner.plan())
        plans.update({folder/pid/'visuals'/vid/'mobile.json':value for vid,value in planner.mobile.items()})
    qa=validate_plan(root,pages,plans)
    manifest={'version':1,'date':'2026-10-14','project':str(root),'canvasWidth':WIDTH,'theme':'Mission Control dark',
              'formatting':'Independent phone formatting with visualContainerMobileState 2.4.0',
              'pages':pages,'protected':baseline,'excludedPages':[{'id':TOOLTIP,'reason':'Desktop hover tooltip; source visual remains unchanged'}],
              'nativePhoneRenderVerified':False,'sourceRefresh':'None'}
    if apply:
        if no_backup:
            assert (root/'Mission Control mobile layout revision.json').exists(),'A baseline backup is required before repairing phone layouts.'
            backup=Path(read(root/'Mission Control mobile layout revision.json')['backup'])
        else:
            backup=root.parent/'_backups'/('Mission Control before phone layouts '+datetime.now().strftime('%Y%m%d-%H%M%S')+'.zip')
            with zipfile.ZipFile(backup,'w',zipfile.ZIP_DEFLATED) as archive:
                for p in root.rglob('*'):
                    if p.is_file() and '.pbi' not in p.relative_to(root).parts:archive.write(p,p.relative_to(root))
        assert protected(root)==baseline,'Desktop/model changed during preparation.'
        for path,value in plans.items():write(path,value)
        # Delete only obsolete phone JSON files, never their visuals or directories.
        for old in folder.rglob('mobile.json'):
            assert old.resolve().is_relative_to(folder.resolve())
            if old not in plans:old.unlink()
        assert protected(root)==baseline,'A non-mobile definition changed.'
        manifest['backup']=str(backup)
        write(root/'Mission Control mobile layout revision.json',manifest)
        write(root/'Mission Control mobile layout validation.json',qa)
        print('Backup:',backup)
    else:
        write(root/'Mission Control mobile layout plan.json',manifest)
    print(json.dumps(qa))
    print(json.dumps([{'page':p['name'],'height':p['height'],'visuals':p['mobileVisuals']} for p in pages]))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--project-root',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--no-backup',action='store_true')
    args=parser.parse_args()
    build(args.project_root,args.apply,args.no_backup)
