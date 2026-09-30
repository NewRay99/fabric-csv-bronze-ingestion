"""Repair journey layout and add small, selected-slicer-only stage bookmarks."""
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from add_wmpp_journey_pathways import PROJECT,REPORT,MODEL,DEFINITION,SINGLE,DETAIL,PROVIDER,REF_LABELS,PROVIDER_LABELS
from build_report_design_delivery import read,save,ident,L,obj,fill,field,project,quoted,measures,table
from refine_wmpp_wip_filters_width import is_navigation
import rebuild_mission_control_dashboard_v16 as ui

MT='_Journey Interaction'
PROVIDER_SELECTOR='Journey Provider Selection'
DETAIL_SELECTOR='Journey Detail Selection'
STARTS={SINGLE:480,DETAIL:370,PROVIDER:354}


def plain_card(v,centre=True,size=22):
    vi=v['visual'];objects=vi.setdefault('objects',{})
    def both(**props):return [{'properties':props},{'properties':deepcopy(props),'selector':{'id':'default'}}]
    for group in ['accentBar','outline','fillCustom']:objects[group]=both(show=L('false'))
    objects['layout']=both(alignment=L("'top'"),autoGrid=L('true'),orientation=L('2D'),rowCount=L('1L'),backgroundShow=L('false'),backgroundTransparency=L('100D'),borderWidth=L('0D'),borderTransparency=L('100D'),leftOuterMargin=L('0D'),rightOuterMargin=L('0D'),topOuterMargin=L('0D'),bottomOuterMargin=L('0D'),cellPadding=L('0D'))
    objects['padding']=both(paddingSelection=L("'Custom'"),paddingIndividual=L('true'),leftMargin=L('0D'),rightMargin=L('0D'),topMargin=L('0D'),bottomMargin=L('0D'))
    objects['value']=both(fontSize=L(str(size)+'D'),fontColor=fill('#2B2B2C'),bold=L('false'),horizontalAlignment=L("'center'" if centre else "'left'"),textWrap=L('true'))
    objects['label']=both(show=L('false'))
    vi['visualContainerObjects']={
        'background':obj(show=L('false')),'border':obj(show=L('false')),'dropShadow':obj(show=L('false')),
        'title':obj(show=L('false')),'subTitle':obj(show=L('false')),'visualHeader':obj(show=L('false')),
        'padding':obj(top=L('0D'),bottom=L('0D'),left=L('0D'),right=L('0D'))}


def model_definitions():
    defs=[]
    def add(n,d,f=None):defs.append((n,d,f))
    for i in range(1,7):
        add(f'Rail referrals {i}',f"CALCULATE([Journey referrals {i}], REMOVEFILTERS('fact_referral'[Journey stage order]))",'#,0')
        add(f'Rail referral circle {i}',f'''IF(ISFILTERED('fact_referral'[Journey stage order]), IF(SELECTEDVALUE('fact_referral'[Journey stage order]) = {i}, "#EF7911", "#F0EBE7"), "#FCA356")''')
    add('Rail referral summary',"CALCULATE([Journey referral exceptions], REMOVEFILTERS('fact_referral'[Journey stage order]))")
    for i in range(1,6):
        add(f'Rail provider circle {i}',f'''IF({i}=4, "#F0EBE7", IF(ISFILTERED('{PROVIDER_SELECTOR}'[Stage]), IF(SELECTEDVALUE('{PROVIDER_SELECTOR}'[Stage]) = {i}, "#EF7911", "#F0EBE7"), "#FCA356"))''')
    eligible=f'''VAR selectedStage = SELECTEDVALUE('{PROVIDER_SELECTOR}'[Stage], -1)
VAR eligible = CALCULATETABLE(
    FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Journey provider stage]) == selectedStage),
    ALLSELECTED())'''
    add('Rail provider row visible',eligible+'''
VAR matching = CALCULATE(COUNTROWS('dim_provider'), KEEPFILTERS(eligible))
RETURN IF(selectedStage = -1, 1, IF(matching > 0, 1, BLANK()))''','0')
    add('Rail provider cohort label', '''VAR providerKey = SELECTEDVALUE('dim_provider'[provider_id])
RETURN IF(NOT ISBLANK(providerKey), CALCULATE([Journey provider label], ALLSELECTED(), KEEPFILTERS(TREATAS({providerKey},'dim_provider'[provider_id]))))''')
    parameter=(MODEL/'tables/Dashboard Metric Selector.tmdl').read_text(encoding='utf-8-sig')
    entries=re.findall(r'\("([^"\n]+)",\s*NAMEOF\(\'([^\']+)\'\[([^\]]+)\]\),\s*(\d+)\)',parameter)
    assert len(entries)==8,'Inspect metric parameter before changing its chart.'
    switch='SWITCH(metric, '+', '.join(f'{order}, [{measure}]' for _,_,measure,order in entries)+', BLANK())'
    add('Rail provider selected metric',eligible+f'''
VAR metric = IF(NOT ISCROSSFILTERED('Dashboard Metric Selector'), 0, SELECTEDVALUE('Dashboard Metric Selector'[Dashboard Metric Selector Order]))
VAR assignedRefs = CALCULATETABLE(VALUES('fact_referral_provider'[referral_id]), KEEPFILTERS(eligible))
VAR offeredRefs = CALCULATETABLE(VALUES('fact_offer'[referral_id]), KEEPFILTERS(eligible))
VAR referralKeys = DISTINCT(UNION(assignedRefs, offeredRefs))
VAR offerKeys = CALCULATETABLE(VALUES('fact_offer'[offer_id]), KEEPFILTERS(eligible))
RETURN IF(ISBLANK(metric), BLANK(), IF(selectedStage = -1, {switch},
CALCULATE({switch}, KEEPFILTERS(eligible),
KEEPFILTERS(TREATAS(referralKeys,'fact_referral'[referral_id])),
KEEPFILTERS(TREATAS(offerKeys,'fact_ipa'[accepted_offer_id])),
KEEPFILTERS(TREATAS(eligible,'dim_provider_home'[provider_id])))))''','#,0')
    add('Rail activity row visible',f'''VAR stage = SELECTEDVALUE('{DETAIL_SELECTOR}'[Stage], -1)
VAR eventType = SELECTEDVALUE('fact_referral_lifecycle_event'[event_type])
RETURN IF(stage = -1, 1, IF(SWITCH(stage,
1, eventType IN {{"ReferralCreated", "ReferralModified"}},
2, eventType = "ProviderMessageSent",
3, eventType IN {{"OfferSubmitted", "OfferUpdated"}},
4, eventType = "OfferUpdated",
5, eventType IN {{"IPACreated", "IPAUpdated"}},
6, eventType = "IPAUpdated", FALSE()), 1, BLANK()))''','0')
    add('Rail activity caption',f'''VAR stage = SELECTEDVALUE('{DETAIL_SELECTOR}'[Stage], -1)
VAR focus = SWITCH(stage, 1,"Referral activity",2,"Provider-message activity",3,"Offer activity",4,"Offer updates (acceptance is not an explicit event)",5,"IPA activity",6,"IPA updates (signature is not an explicit event)","All recorded activity")
RETURN "Activity focus: " & focus & ". " & [Journey next action]''')
    return defs


def build():
    original={p:read(p) for p in DEFINITION.rglob('*.json')};docs=deepcopy(original)
    new_ids=[];bookmark_ids=[];assets={};hidden=[];slicers={}
    def visual(pid,key):return docs[DEFINITION/'pages'/pid/'visuals'/ident('journey:'+pid+':'+key)/'visual.json']
    def put(pid,v):
        p=DEFINITION/'pages'/pid/'visuals'/v['name']/'visual.json'
        assert p not in docs;p.parent  # Planned write only.
        docs[p]=v;new_ids.append((pid,v['name']));return v
    def text(pid,key,label,x,y,w,h,size=12):
        v=ui.textbox(ident('journey-rail:'+pid+':'+key),label,ui.position(x,y,w,h,110015),size,False)
        v['visual']['visualContainerObjects'].update(title=obj(show=L('false')),subTitle=obj(show=L('false')),border=obj(show=L('false')),dropShadow=obj(show=L('false')))
        return put(pid,v)
    def set_text(v,label,align='left',size=13):
        paragraphs=v['visual']['objects']['general'][0]['properties']['paragraphs']
        paragraphs[:]=[{'horizontalTextAlignment':align,'textRuns':[{'value':label,'textStyle':{'fontFamily':'Segoe UI','fontSize':str(size)+'px','fontWeight':'normal','color':'#2B2B2C'}}]}]
        v['visual']['visualContainerObjects'].update(border=obj(show=L('false')),dropShadow=obj(show=L('false')),title=obj(show=L('false')),subTitle=obj(show=L('false')))
    def pos(v,x,y,w,h,z=None):
        v['position'].update(x=x,y=y,width=w,height=h)
        if z is not None:v['position']['z']=z
    def set_measure(v,name):
        v['visual']['query']['queryState']['Data']['projections']=[project(MT,name,True)]
    def selector(pid,t,c):
        sid=ident('journey-rail:'+pid+':selector')
        v=ui.visual_shell(sid,'slicer',ui.position(36,STARTS[pid]+80,80,60,108000));v['isHidden']=True
        v['visual']['query']={'queryState':{'Values':{'projections':[project(t,c)]}}}
        v['visual']['objects']={'data':obj(mode=L("'Dropdown'")),'selection':obj(singleSelect=L('true'),strictSingleSelect=L('false')),'header':obj(show=L('false'))}
        v['visual']['visualContainerObjects']={'background':obj(show=L('false')),'title':obj(show=L('false')),'border':obj(show=L('false')),'dropShadow':obj(show=L('false'))}
        v['filterConfig']={'filters':[{'name':ident(sid+':field'),'field':field(t,c),'type':'Categorical','howCreated':'User'}]}
        put(pid,v);slicers[pid]=sid
        return sid
    def bookmark(pid,sid,t,c,stage,label):
        bid=ident('journey-rail:'+pid+':stage:'+str(stage))
        f={'Version':2,'From':[{'Name':'s','Entity':t,'Type':0}],'Where':[]}
        if stage is not None:
            f['Where']=[{'Condition':{'In':{'Expressions':[{'Column':{'Expression':{'SourceRef':{'Source':'s'}},'Property':c}}],'Values':[[{'Literal':{'Value':str(stage)+'L'}}]]}}}]
        b={'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json',
           'name':bid,'displayName':label,
           'options':{'applyOnlyToTargetVisuals':True,'targetVisualNames':[sid],'suppressActiveSection':True,'suppressData':False,'suppressDisplay':True},
           'explorationState':{'version':'1.0','activeSection':pid,'sections':{pid:{'visualContainers':{sid:{'singleVisual':{'visualType':'slicer','objects':{'merge':{'general':obj(filter={'filter':f})}},'activeProjections':{'Values':[field(t,c)]}}}}}}}}
        p=DEFINITION/'bookmarks'/f'{bid}.bookmark.json';assert p not in docs
        docs[p]=b;docs[DEFINITION/'bookmarks/bookmarks.json']['items'].append({'name':bid});bookmark_ids.append(bid)
        return bid
    def link(v,bid,label):
        v['visual'].setdefault('visualContainerObjects',{})['visualLink']=obj(show=L('true'),type=L("'Bookmark'"),bookmark=L(quoted(bid)),tooltip=L(quoted(label)))
        v['visual']['visualContainerObjects']['general']=obj(altText=L(quoted(label)))
    for pid,start in STARTS.items():
        provider=pid==PROVIDER;detail=pid==DETAIL;labels=PROVIDER_LABELS if provider else REF_LABELS;n=len(labels)
        title='Provider journey' if provider else 'Referral journey'
        title_v=visual(pid,'title');pos(title_v,60,start+16,1300,34);set_text(title_v,title,size=22)
        subtitle=('Click a milestone to focus recorded activity below; the referral selection stays unchanged.' if detail else
                  'Click a step icon to filter the page. Each provider is counted once at its furthest evidenced stage.' if provider else
                  'Click a step icon to filter the page. Counts show the current cohort; other slicers stay selected.')
        v=visual(pid,'subtitle');pos(v,60,start+53,1520,32);set_text(v,subtitle,size=12)
        main=visual(pid,'panel-1');pos(main,36,start,1608,304,108500)
        main['visual']['visualContainerObjects']['border']=obj(show=L('true'),color=fill('#FFFFFF'),radius=L('18D'))
        for i in range(2,n+1):
            v=visual(pid,f'panel-{i}');v['isHidden']=True;hidden.append(v['name'])
        t,c=('fact_referral','Journey stage order') if pid==SINGLE else (DETAIL_SELECTOR if detail else PROVIDER_SELECTOR,'Stage')
        sid=selector(pid,t,c)
        page_name=docs[DEFINITION/'pages'/pid/'page.json']['displayName']
        reset=bookmark(pid,sid,t,c,None,page_name+' | Clear journey selection')
        reset_label='Clear stage' if not detail else 'All activity'
        reset_v=text(pid,'clear',reset_label,1464,start+20,156,30,12)
        reset_v['visual']['visualType']='actionButton'
        reset_v['visual']['objects']={'shape':obj(tileShape=L("'rectangle'"),roundEdge=L('8D')),'text':[],'icon':[],'fill':[],'outline':[]}
        for state in [None,'default','hover','selected','disabled']:
            for group,props in {
                'text':{'show':L('true'),'text':L(quoted(reset_label)),'fontSize':L('11D'),'bold':L('false'),'fontFamily':L("'Segoe UI'"),'fontColor':fill('#2B2B2C'),'horizontalAlignment':L("'center'"),'verticalAlignment':L("'middle'")},
                'icon':{'show':L('false')},'outline':{'show':L('false')},
                'fill':{'show':L('true' if state=='hover' else 'false'),'fillColor':fill('#F0EBE7'),'transparency':L('0D')}
            }.items():
                entry={'properties':props}
                if state:entry['selector']={'id':state}
                reset_v['visual']['objects'][group].append(entry)
        link(reset_v,reset,'Clear only the journey selection')
        for i,label in enumerate(labels,1):
            center=60+(1560/n)*(i-.5)
            circle=visual(pid,f'circle-{i}');pos(circle,center-32,start+98,64,64,109010)
            circle['visual']['visualContainerObjects']['border'][0]['properties']['radius']=L('32D')
            if not detail:
                expr={'expr':field(MT,f'Rail provider circle {i}' if provider else f'Rail referral circle {i}',True)}
                for group in ['background','border']:
                    circle['visual']['visualContainerObjects'][group][0]['properties']['color']={'solid':{'color':expr}}
            icon=visual(pid,f'icon-{i}');pos(icon,center-32,start+98,64,64,110020)
            old_asset=icon['visual']['objects']['image'][0]['properties']['sourceFile']['image']['url']['expr']['ResourcePackageItem']['ItemName']
            asset=old_asset.replace('.svg','-rail.svg')
            if asset not in assets:
                svg=ET.fromstring((REPORT/'StaticResources/RegisteredResources'/old_asset).read_text(encoding='utf-8-sig'))
                svg.set('viewBox','-14 -14 52 52');svg.set('width','64');svg.set('height','64')
                assets[asset]=ET.tostring(svg,encoding='unicode')
            image=icon['visual']['objects']['image'][0]['properties']['sourceFile']['image']
            image['url']['expr']['ResourcePackageItem']['ItemName']=asset;image['name']=L(quoted(asset))
            if not(provider and i==4):
                bid=bookmark(pid,sid,t,c,i,page_name+' | Journey: '+label)
                link(icon,bid,('Focus activity for ' if detail else 'Filter to ')+label)
            else:
                icon['visual']['visualContainerObjects']['general']=obj(altText=L("'Unavailable: separate provider confirmation is not captured'"))
            v=visual(pid,f'heading-{i}');pos(v,center-116,start+172,232,32);set_text(v,label,'center',14)
            v=visual(pid,f'value-{i}');pos(v,center-118,start+207,236,44)
            plain_card(v,True,13 if detail or (provider and i==4) else 25)
            if pid==SINGLE:set_measure(v,f'Rail referrals {i}')
            if i<n:
                line=visual(pid,f'arrow-{i}');next_center=center+1560/n
                pos(line,center+38,start+129,next_center-center-76,2,109000)
                set_text(line,'')
                line['visual']['visualContainerObjects'].update(background=obj(show=L('true'),color=fill('#E3DADA'),transparency=L('0D')))
        if detail:
            current=visual(pid,'current');pos(current,60,start+246,1536,24);plain_card(current,False,12)
            nxt=visual(pid,'next');pos(nxt,60,start+270,1536,32);plain_card(nxt,False,11);set_measure(nxt,'Rail activity caption')
        else:
            summary=visual(pid,'coverage' if provider else 'exceptions');pos(summary,60,start+260,1536,32);plain_card(summary,False,12)
            if not provider:set_measure(summary,'Rail referral summary')
            note=visual(pid,'limitations' if provider else 'note')
            # Retain the detailed caveat as an accessible tooltip, avoiding clipped footer rows.
            label=('Message activity includes either sender; browsing and separate provider confirmation are not captured. Both-signed is a subset of provider-signed.' if provider else 'Stage uses refreshed records; drafts and declined/withdrawn offers do not advance the current stage.')
            note['isHidden']=True;hidden.append(note['name'])
            subtitle_v=visual(pid,'subtitle');subtitle_v['visual']['visualContainerObjects']['general']=obj(altText=L(quoted(subtitle+' '+label)))
            if provider:
                set_text(subtitle_v,'Click an icon to filter. Message activity can be from either sender; browsing and separate provider confirmation are not captured.',size=12)
    # Provider membership is calculated once for the external cohort, not each offer row.
    def gate(v,name):
        mf=field(MT,name,True)
        v.setdefault('filterConfig',{}).setdefault('filters',[]).append({'name':ident(v['name']+':'+name),'field':mf,'type':'Advanced','howCreated':'User','filter':{'Version':2,'From':[{'Name':'m','Entity':MT,'Type':0}],'Where':[{'Condition':{'Comparison':{'ComparisonKind':2,'Left':{'Measure':{'Expression':{'SourceRef':{'Source':'m'}},'Property':name}},'Right':{'Literal':{'Value':'1L'}}}}}]}})
    for p,v in docs.items():
        if p.name!='visual.json' or v.get('isHidden'):continue
        pid=p.parents[2].name;vi=v.get('visual',{});kind=vi.get('visualType')
        if pid==PROVIDER and kind=='tableEx':
            gate(v,'Rail provider row visible')
            projections=vi['query']['queryState']['Values']['projections']
            for index,pr in enumerate(projections):
                if pr.get('queryRef')=='_Journey Measures.Journey provider label':projections[index]=project(MT,'Rail provider cohort label',True,label='Provider journey')
        if pid==PROVIDER and kind=='donutChart':
            vi['query']['queryState']['Y']={'projections':[project(MT,'Rail provider selected metric',True,label='Selected metric')]}
            vi['query']['sortDefinition']={'sort':[{'field':field(MT,'Rail provider selected metric',True),'direction':'Descending'}]}
            vi.setdefault('visualContainerObjects',{})['title']=obj(show=L('true'),text=L("'Selected metric by placement type'"),fontSize=L('13D'),bold=L('false'))
        if pid==DETAIL and kind=='tableEx' and 'fact_referral_lifecycle_event' in json.dumps(vi.get('query',{})):gate(v,'Rail activity row visible')
    package=next(p for p in docs[DEFINITION/'report.json']['resourcePackages'] if p['name']=='RegisteredResources')
    for name in assets:
        assert not any(x['name']==name for x in package['items'])
        package['items'].append({'name':name,'path':name,'type':'Image'})
    for p,old in original.items():
        if p.name.endswith('.bookmark.json'):assert docs[p]==old
        if p.name=='page.json':assert docs[p]==old
        if p.name=='visual.json' and is_navigation(old):assert docs[p]==old
    return original,docs,assets,{'new_visual_ids':new_ids,'new_bookmark_ids':bookmark_ids,'hidden_redundant_visual_ids':hidden,'selector_ids':slicers}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    marker=PROJECT/'JOURNEY_RAIL_REPAIR.json';assert not marker.exists(),'Already applied; inspect before rerunning.'
    original,docs,assets,result=build()
    print(json.dumps({'changed_files':sum(d!=original.get(p) for p,d in docs.items()),'small_stage_bookmarks':len(result['new_bookmark_ids']),'new_selectors':3,'existing_bookmarks_changed':0,'model_measures':len(model_definitions())},indent=2))
    if not args.apply:return
    backup=PROJECT.parent/'_review'/('journey-rail-repair-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    for src,relative in [(DEFINITION,'SM_WMPP_v16.Report/definition'),(MODEL,'SM_WMPP_v16.SemanticModel/definition')]:
        shutil.copytree(src,backup/relative)
        for f in src.rglob('*'):
            if f.is_file():assert hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((backup/relative/f.relative_to(src)).read_bytes()).digest()
    for name,labels in [(PROVIDER_SELECTOR,PROVIDER_LABELS),(DETAIL_SELECTOR,REF_LABELS)]:
        rows=', '.join('{'+str(i)+', "'+label+'"}' for i,label in enumerate(labels,1) if not(name==PROVIDER_SELECTOR and i==4))
        table(MODEL,name,[('Stage','int64',''),('Label','string','')], '#table(type table [Stage=Int64.Type, Label=text], {'+rows+'})',mode='m',hidden=True)
    measures(MODEL,MT,model_definitions())
    for name,svg in assets.items():
        for folder in [Path(__file__).resolve().parents[1]/'assets/brand-pack/icons/journey',REPORT/'StaticResources/RegisteredResources']:
            folder.mkdir(parents=True,exist_ok=True)
            (folder/name).write_text(svg,encoding='utf-8')
    for p,d in docs.items():
        if d!=original.get(p):
            if p.name.endswith('.bookmark.json'):p.write_text(json.dumps(d,separators=(',',':'),ensure_ascii=False)+'\n',encoding='utf-8')
            else:save(p,d)
    result.update(backup=str(backup),existing_bookmarks_unchanged=True,other_slicers_preserved_by_design=True,desktop_verified=False,engine_verified=False,model_refresh_required=True)
    save(marker,result);print('Saved connected rails and stage actions. Backup:',backup)


if __name__=='__main__':main()
