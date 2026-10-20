"""Position navigation using saved visual identity, not Desktop-renumbered layers."""
from copy import deepcopy
import json
from pathlib import Path
from build_report_design_delivery import L, read, save
from rework_wmpp_wip_storyboard import PROJECT, DEFINITION, SINGLE, DETAIL, BOARD


def literal(v):
    return v.get('expr',{}).get('Literal',{}).get('Value','').strip("'")


def label(v):
    for e in v.get('visual',{}).get('objects',{}).get('text',[]):
        if 'text' in e['properties']:return literal(e['properties']['text']).replace(' ▾','')
    return ''


def main():
    manifest=read(PROJECT/'STORYBOARD_DELIVERY.json')
    oldroot=Path(manifest['backup'])/'SM_WMPP_v16.Report/definition'
    originals={p.relative_to(oldroot):read(p) for p in oldroot.rglob('*.json')}
    docs={p.relative_to(DEFINITION):read(p) for p in DEFINITION.rglob('*.json')}
    order=['Home','Performance','Referrals','Offers','Draft offers','IPAs','Providers','Requirements']
    navids=set();retired=set();count=0;pagecount=0
    for pp,pagedef in list(docs.items()):
        if pp.name!='page.json':continue
        pid=pp.parent.name
        values={p:v for p,v in docs.items() if p.name=='visual.json' and p.parents[2].name==pid}
        mains={}
        for p,v in values.items():
            pos=v['position'];vis=v.get('visual',{})
            link=vis.get('visualContainerObjects',{}).get('visualLink',[{}])[0].get('properties',{})
            if pos['y']==8 and pos['width']==96 and pos['height']==108 and literal(link.get('tooltip',{}))!='Close menu' and label(v) in order:
                mains[label(v)]=(p,v)
        if not mains:continue
        assert len(mains)==8,(pid,list(mains))
        pagecount+=1
        for p,v in values.items():
            pos=v['position'];text=label(v)
            general=json.dumps(v.get('visual',{}).get('visualContainerObjects',{}).get('general',{}))
            isrow=pos['width']==310 and pos['height']==44 and v.get('visual',{}).get('visualType')=='actionButton'
            isbutton=text in order and ((pos['width']==96 and pos['height']==108) or (pos['width']==104 and pos['height']==116))
            issurround='White dropdown surround:' in general
            if isrow or isbutton or issurround:
                navids.add(v['name'])
                if p in originals:
                    v.pop('isHidden',None)
                    if 'isHidden' in originals[p]:v['isHidden']=originals[p]['isHidden']
            if isbutton:
                index=order.index(text);pos['x']=860+100*index-(4 if pos['width']==104 else 0)
                pos['z']=400010 if pos['width']==104 else 400001 if v.get('isHidden') else 400000
                pos['tabOrder']=index*10+(1 if pos['width']==104 else 0)
                count+=1
            if 'Open Filters' in general or 'Close Filters' in general:
                pos['z']=400020 if 'Open Filters' in general else 400021
        for name,(_,button) in mains.items():
            link=button['visual']['visualContainerObjects']['visualLink'][0]['properties']
            bid=literal(link.get('bookmark',{}));bp=Path('bookmarks')/(bid+'.bookmark.json')
            if bp not in originals or not originals[bp]['displayName'].endswith(' menu'):continue
            states=originals[bp]['explorationState']['sections'][pid]['visualContainers']
            active=[(p,v) for p,v in values.items() if v['name'] in states and states[v['name']]['singleVisual'].get('display',{}).get('mode')!='hidden']
            rows=sorted([(p,v) for p,v in active if v['position']['width']==310 and v['position']['height']==44],key=lambda item:item[1]['position']['y'])
            kept=[]
            for p,v in rows:
                if name=='Referrals' and any(word in label(v).lower() for word in ['geography','snapshot','overview','detail']):
                    retired.add(v['name']);v['isHidden']=True
                else:kept.append((p,v))
            px=min(button['position']['x'],1346)-12
            for i,(_,v) in enumerate(kept):
                v['position'].update(x=px+12,y=136+i*44,z=300020+i)
            for p,v in active:
                alt=json.dumps(v.get('visual',{}).get('visualContainerObjects',{}).get('general',{}))
                if 'White dropdown surround:' not in alt:continue
                if '/ panel' in alt:v['position'].update(x=px,y=124,height=24+44*len(kept),z=300005)
                elif '/ neck' in alt:v['position'].update(x=button['position']['x']-4,z=300006)
    # Restore only known navigation states from the original Desktop bookmarks.
    for p,b in docs.items():
        if not p.name.endswith('.bookmark.json'):continue
        original=originals.get(p,{})
        for pid,sec in b.get('explorationState',{}).get('sections',{}).items():
            oldstates=original.get('explorationState',{}).get('sections',{}).get(pid,{}).get('visualContainers',{})
            for vid,state in sec.get('visualContainers',{}).items():
                if vid in navids and vid in oldstates:
                    state['singleVisual'].pop('display',None)
                    if 'display' in oldstates[vid]['singleVisual']:
                        state['singleVisual']['display']=deepcopy(oldstates[vid]['singleVisual']['display'])
                if vid in retired:state['singleVisual']['display']={'mode':'hidden'}
        if b.get('displayName')=='Go to Board Dashboard':b['displayName']='Go to Overall Performance'
    # The detail page is entered through a referral-key drillthrough, not a menu.
    docs[Path('pages')/DETAIL/'page.json']['visibility']='HiddenInViewMode'
    # Hide the superseded original single-view page from every navigation entry.
    for p,v in docs.items():
        if p.name=='visual.json':
            for entry in v.get('visual',{}).get('objects',{}).get('text',[]):
                if literal(entry['properties'].get('text',{}))=='Board Dashboard':
                    entry['properties']['text']=L("'Overall Performance'")
            for entry in v.get('visual',{}).get('objects',{}).get('general',[]):
                for para in entry.get('properties',{}).get('paragraphs',[]):
                    for run in para.get('textRuns',[]):
                        if run.get('value')=='Board Dashboard':run['value']='Overall Performance'
        save(DEFINITION/p,v)
    manifest.update(moved_navigation_visuals=count,navigation_pages=pagecount,retired_menu_entries=len(retired))
    save(PROJECT/'STORYBOARD_DELIVERY.json',manifest)
    print(json.dumps({'navigation_pages':pagecount,'moved_buttons':count,'retired_menu_entries':len(retired)}))


if __name__=='__main__':main()
