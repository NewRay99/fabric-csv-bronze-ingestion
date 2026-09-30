"""Finish native formatting placement and drillthrough affordances in WIP."""
from copy import deepcopy
from build_report_design_delivery import L, field, fill, ident, obj, project, quoted, read, save
from rework_wmpp_wip_storyboard import DEFINITION, PROJECT, DETAIL, SINGLE
import rebuild_mission_control_dashboard_v16 as ui


def main():
    fixed=0
    for path in (DEFINITION/'pages').glob('*/visuals/*/visual.json'):
        v=read(path);old=deepcopy(v);visual=v.get('visual',{})
        containers=visual.get('visualContainerObjects',{})
        # The card's internal padding is distinct from outer visual-container padding.
        for entry in containers.get('padding',[]):
            extra={k:x for k,x in entry['properties'].items() if k not in ('top','bottom','left','right')}
            if not extra:continue
            for k in extra:entry['properties'].pop(k)
            target=visual.setdefault('objects',{}).setdefault('padding',[])
            match=next((e for e in target if e.get('selector')==entry.get('selector')),None)
            if match:match['properties']={**extra,**match['properties']}
            else:target.append({**({'selector':entry['selector']} if 'selector' in entry else {}),'properties':extra})
        if 'padding' in containers:containers['padding']=[e for e in containers['padding'] if e['properties']]
        if v!=old:save(path,v);fixed+=1
    d=DEFINITION/'pages'/DETAIL/'visuals'
    msg=d/ident('wmpp-story:'+DETAIL+':messages')/'visual.json'
    v=read(msg)
    projections=v['visual']['query']['queryState']['Values']['projections']
    if not any(p['queryRef']=='dim_provider.provider_name' for p in projections):
        projections.insert(1,project('dim_provider','provider_name',label='Provider'))
    save(msg,v)
    event=d/ident('wmpp-story:'+DETAIL+':lifecycle')/'visual.json'
    v=read(event);v['visual']['query']['sortDefinition']={'sort':[{'field':field('fact_referral_lifecycle_event','sequence_number'),'direction':'Ascending'}],'isDefaultSort':False}
    save(event,v)
    # Remove the obsolete header-level response slicer from the rebuilt detail page.
    old=d/'131643d00361d0945467'/'visual.json'
    if old.exists():
        v=read(old);v['isHidden']=True;save(old,v)
    back=ui.visual_shell(ident('wmpp-story:'+DETAIL+':back'),'actionButton',ui.position(1380,250,264,72,92000))
    back['visual']['objects']={'text':obj(show=L('true'),text=L("'← Back to results'"),fontSize=L('12D'),bold=L('false')),'fill':obj(show=L('true'),fillColor=fill('#FFFFFF')),'outline':obj(show=L('false'))}
    back['visual']['visualContainerObjects']={'visualLink':obj(show=L('true'),type=L("'Back'")), 'title':obj(show=L('false'))}
    save(d/back['name']/'visual.json',back)
    # Links into the archived Geography/Snapshots pages are hidden rather than deleted.
    # A previous duplicate single-view destination resolves to the active new explorer.
    for bp in (DEFINITION/'bookmarks').glob('*.bookmark.json'):
        b=read(bp)
        if b['displayName'].startswith('Go to ') and b['explorationState'].get('activeSection')=='4be6f15f15a086c98c33':
            b['explorationState']['activeSection']=SINGLE;b['displayName']='Go to Referral Single View'
            save(bp,b)
    print({'padding_corrected':fixed,'back_button_added':True})


if __name__=='__main__':main()
