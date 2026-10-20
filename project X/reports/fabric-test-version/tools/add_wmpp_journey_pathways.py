"""Add evidence-led native pathways to the WIP. Dry-run unless --apply is supplied.

No warehouse, cache, relationship, security, or bookmark changes. Missing provider
browsing/confirmation evidence is explicitly unavailable, never a fabricated zero.
"""
import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import shutil
import xml.etree.ElementTree as ET

from build_report_design_delivery import read, save, L, field, project, obj, fill, ident, quoted, measures, add_columns
from rework_wmpp_wip_storyboard import PROJECT, REPORT, MODEL, DEFINITION, SINGLE, DETAIL
from refine_wmpp_wip_filters_width import is_navigation
import rebuild_mission_control_dashboard_v16 as ui

PROVIDER='08ef33dc6a87d1b14392'
MT='_Journey Measures'
ACCEPTED=['accepted','approved','selected','offer_successful']
PENDING=['pending','submitted','offered','offer_made','offer_pending','under_review','under review','awaiting','awaiting_decision','awaiting decision']
TERMINAL_OFFER=['declined','rejected','withdrawn','closed','cancelled','canceled','offer_unsuccessful','unsuccessful']
CLOSED=['closed','cancelled','canceled','withdrawn','completed']
REF_LABELS=['Referral created','Provider search','Offers received','Offer accepted','IPA created','IPA signed']
PROVIDER_LABELS=['Message activity only','Offers made','Offer accepted','Provider confirmation','Provider signed']
BRAND=Path(__file__).resolve().parents[1]/'assets/brand-pack/icons'


def dax_set(values):return '{'+', '.join('"'+v+'"' for v in values)+'}'


def column_definitions():
    accepted=dax_set(ACCEPTED);pending=dax_set(PENDING)
    known=dax_set(ACCEPTED+PENDING+TERMINAL_OFFER+['draft'])
    expression=f'''VAR status = LOWER(TRIM(COALESCE('fact_referral'[current_status], "")))
VAR offers = CALCULATETABLE('fact_offer', ALLEXCEPT('fact_referral', 'fact_referral'[referral_id]))
VAR ipas = FILTER(CALCULATETABLE('fact_ipa', ALLEXCEPT('fact_referral', 'fact_referral'[referral_id])), NOT('fact_ipa'[is_placement_closed] == TRUE()))
VAR signed = COUNTROWS(FILTER(ipas, 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0
VAR accepted = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {accepted})) > 0
VAR pending = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {pending})) > 0
VAR unknownOffer = COUNTROWS(FILTER(offers, NOT(LOWER(TRIM(COALESCE('fact_offer'[offer_status], "")))) IN {known})) > 0
RETURN SWITCH(TRUE(),
    status IN {dax_set(CLOSED)}, 7,
    signed, 6,
    COUNTROWS(ipas) > 0, 5,
    accepted, 4,
    pending, 3,
    unknownOffer || status = "", 8,
    COUNTROWS(CALCULATETABLE('fact_referral_provider', ALLEXCEPT('fact_referral', 'fact_referral'[referral_id]))) > 0, 2,
    NOT ISBLANK('fact_referral'[referral_created_date]), 1,
    8)'''
    # Parenthesize the complete IN expression for clarity and DAX parser portability.
    expression=expression.replace('NOT(LOWER(TRIM(COALESCE(\'fact_offer\'[offer_status], "")))) IN '+known,
                                  'NOT(LOWER(TRIM(COALESCE(\'fact_offer\'[offer_status], ""))) IN '+known+')')
    labels='SWITCH(\'fact_referral\'[Journey stage order], '+', '.join(f'{i}, "{label}"' for i,label in enumerate(REF_LABELS+['Closed / cancelled / withdrawn','Needs review'],1))+', "Needs review")'
    return [('Journey stage order','int64',expression,''),('Journey stage','string',labels,"\t\tsortByColumn: 'Journey stage order'\n")]


def definitions():
    defs=[]
    def add(name,dax,fmt=None):defs.append((name,dax,fmt))
    for i,label in enumerate(REF_LABELS+['Closed / cancelled / withdrawn','Needs review'],1):
        add(f'Journey referrals {i}',f"COALESCE(CALCULATE([Matching referrals], KEEPFILTERS('fact_referral'[Journey stage order] = {i})), 0)",'#,0')
    add('Journey referral reconciliation', '[Matching referrals] - ('+' + '.join(f'[Journey referrals {i}]' for i in range(1,9))+')','#,0')
    add('Journey referral exceptions','"Closed / cancelled / withdrawn: " & FORMAT([Journey referrals 7], "#,0") & "     |     Needs review: " & FORMAT([Journey referrals 8], "#,0") & "     |     Matching referrals: " & FORMAT(COALESCE([Matching referrals],0), "#,0")')
    add('Journey selected stage',"IF(HASONEVALUE('fact_referral'[referral_id]), SELECTEDVALUE('fact_referral'[Journey stage order]))",'0')
    add('Journey current position', '''IF(NOT HASONEVALUE('fact_referral'[referral_id]), "Select one referral to see its journey",
"Current position: " & SELECTEDVALUE('fact_referral'[Journey stage]) &
IF(SELECTEDVALUE('fact_referral'[is_open_overdue]) == TRUE(), " | Overdue", ""))''')
    add('Journey next action', '''SWITCH([Journey selected stage],
1,"Next: assign providers and begin the search.",
2,"Next: seek suitable offers; declined or withdrawn offers remain in the activity history.",
3,"Next: review the available offers and record the decision.",
4,"Next: prepare the IPA for the selected offer.",
5,"Next: complete provider and local-authority signatures on the same IPA.",
6,"Next: confirm admission separately. A planned admission date is not proof of placement start.",
7,"Referral closed: retain its recorded reason and milestone evidence; closure does not prove placement.",
8,"Review missing or unrecognised status evidence before assigning a stage.",
"The pathway requires a single referral selection.")''')
    evidence={
      1:"NOT ISBLANK(SELECTEDVALUE('fact_referral'[referral_created_date]))",
      2:"COUNTROWS('fact_referral_provider') > 0",
      3:"COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN "+dax_set(ACCEPTED+PENDING+TERMINAL_OFFER)+")) > 0",
      4:"COUNTROWS(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN "+dax_set(ACCEPTED)+")) > 0",
      5:"COUNTROWS('fact_ipa') > 0",
      6:"COUNTROWS(FILTER('fact_ipa', 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0"}
    dates={1:"SELECTEDVALUE('fact_referral'[referral_created_date])",2:'BLANK()',
      3:"MINX(FILTER('fact_offer', LOWER(TRIM('fact_offer'[offer_status])) IN "+dax_set(ACCEPTED+PENDING+TERMINAL_OFFER)+"), 'fact_offer'[offer_submitted_date])",
      4:"SELECTEDVALUE('fact_referral'[offer_accepted_date])",5:"MIN('fact_ipa'[ipa_issued_date])",6:'BLANK()'}
    for i in range(1,7):
        add(f'Journey detail evidence {i}',f'IF(HASONEVALUE(\'fact_referral\'[referral_id]), IF({evidence[i]}, 1, 0))','0')
        add(f'Journey detail label {i}',f'''VAR stage = [Journey selected stage]
VAR evidence = [Journey detail evidence {i}]
VAR stamp = {dates[i]}
RETURN IF(ISBLANK(stage), "Select one referral",
IF(evidence = 1,
IF(stage = {i}, "Current", "Recorded") & " | " & IF(ISBLANK(stamp), "Date unknown", FORMAT(stamp, "dd MMM yyyy"){' & " (proxy)"' if i==4 else ''}),
"Not evidenced"))''')
        add(f'Journey detail colour {i}',f'IF([Journey selected stage] = {i}, "#FCA356", IF([Journey detail evidence {i}] = 1, "#E4F1E9", "#F0EBE7"))')
    # Explicit offer-ID filter is essential: the IPA fact has no active provider relationship.
    add('Journey provider stage',f'''VAR homeScope = ISCROSSFILTERED('dim_provider_home')
VAR matchingHomes = CALCULATE(COUNTROWS('dim_provider_home'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]), 'dim_provider_home'[provider_id])))
VAR assignments = COUNTROWS('fact_referral_provider')
VAR messages = COUNTROWS('dim_referral_provider_message')
VAR offers = FILTER('fact_offer', NOT ISBLANK('fact_offer'[provider_id]))
VAR offerIDs = SELECTCOLUMNS(offers, "OfferKey", 'fact_offer'[offer_id])
VAR ipas = CALCULATETABLE('fact_ipa', KEEPFILTERS(TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])))
VAR signed = COUNTROWS(FILTER(ipas, 'fact_ipa'[signed_by_provider] == TRUE())) > 0
VAR accepted = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {dax_set(ACCEPTED)})) > 0
VAR submitted = COUNTROWS(FILTER(offers, LOWER(TRIM('fact_offer'[offer_status])) IN {dax_set(ACCEPTED+PENDING+TERMINAL_OFFER)})) > 0
RETURN IF(NOT HASONEVALUE('dim_provider'[provider_id]) || (homeScope && matchingHomes = 0), BLANK(),
SWITCH(TRUE(), signed, 5, accepted, 3, submitted, 2, messages > 0, 1, assignments > 0 || COUNTROWS(offers) > 0, 0, BLANK()))''','0')
    for i in [0,1,2,3,5]:
        add(f'Journey providers {i}',f"COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]), NOT ISBLANK('dim_provider'[provider_id]) && CALCULATE([Journey provider stage]) == {i})), 0)",'#,0')
    add('Journey providers 4','"Not captured"')
    add('Journey provider label', '''VAR stage = [Journey provider stage] RETURN IF(ISBLANK(stage), BLANK(), SWITCH(stage, 0,"Assigned / draft / unclear",1,"Message activity only",2,"Offers made",3,"Offer accepted",5,"Provider signed",BLANK()))''')
    add('Journey providers both signed', '''COALESCE(COUNTROWS(FILTER(VALUES('dim_provider'[provider_id]),
VAR offerIDs = CALCULATETABLE(VALUES('fact_offer'[offer_id]))
VAR signedIPAs = CALCULATETABLE('fact_ipa', KEEPFILTERS(TREATAS(offerIDs, 'fact_ipa'[accepted_offer_id])))
RETURN NOT ISBLANK('dim_provider'[provider_id]) && COUNTROWS(FILTER(signedIPAs, 'fact_ipa'[signed_by_provider] == TRUE() && 'fact_ipa'[signed_by_local_authority] == TRUE())) > 0)),0)''','#,0')
    add('Journey provider coverage','"Assigned / draft / unclear: " & FORMAT([Journey providers 0], "#,0") & "     |     Both parties signed (subset): " & FORMAT([Journey providers both signed], "#,0")')
    return defs


def build():
    original={p:read(p) for p in DEFINITION.rglob('*.json')};docs=deepcopy(original)
    assets={};new_visuals=[];moved={}
    def put(pid,v):
        path=DEFINITION/'pages'/pid/'visuals'/v['name']/'visual.json'
        assert path not in docs,path
        docs[path]=v;new_visuals.append((pid,v['name']))
        return v
    def text(pid,key,label,x,y,w,h,size=13):
        return put(pid,ui.textbox(ident('journey:'+pid+':'+key),label,ui.position(x,y,w,h,110000),size,False))
    def card(pid,key,measure,x,y,w,h,size=24):
        v=ui.card(ident('journey:'+pid+':'+key),measure,ui.position(x,y,w,h,110005))
        v['visual']['query']['queryState']['Data']['projections']=[project(MT,measure,True)]
        v.pop('filterConfig',None)
        v['visual']['objects']['value'][0]['properties'].update(fontSize=L(str(size)+'D'),fontColor=fill('#2B2B2C'),bold=L('false'),horizontalAlignment=L("'left'"),textWrap=L('true'))
        v['visual']['objects']['label'][0]['properties']['show']=L('false')
        v['visual']['visualContainerObjects']={'background':obj(show=L('false')),'border':obj(show=L('false')),'dropShadow':obj(show=L('false')),'title':obj(show=L('false')),'visualHeader':obj(show=L('false')),'padding':obj(top=L('0D'),bottom=L('0D'),left=L('0D'),right=L('0D'))}
        return put(pid,v)
    def panel(pid,key,x,y,w,h,colour='#FFFFFF',dynamic=None,radius=14):
        v=text(pid,key,'',x,y,w,h)
        v['position']['z']=109005 if radius==24 else 109000
        color={'expr':field(MT,dynamic,True)} if dynamic else L(quoted(colour))
        v['visual']['visualContainerObjects'].update(background=obj(show=L('true'),color={'solid':{'color':color}},transparency=L('0D')),border=obj(show=L('true'),color={'solid':{'color':color}},radius=L(str(radius)+'D')),dropShadow=obj(show=L('false')))
        return v
    icon_specs=['file-plus-d94d2b','users-d94d2b','handshake-d94d2b','file-check-corner-287c73','file-pen-line-d94d2b','file-check-corner-287c73']
    for index,spec in enumerate(icon_specs,1):
        xml=ET.fromstring((BRAND/('lucide-kpi-'+spec+'.svg')).read_text(encoding='utf-8-sig'))
        xml.set('viewBox','0 0 24 24');xml.set('width','24');xml.set('height','24');xml.set('stroke','#2B2B2C')
        for element in xml.iter():
            if element.get('stroke') and element.get('stroke')!='none':element.set('stroke','#2B2B2C')
        assets[f'wmpp-journey-{index}.svg']=ET.tostring(xml,encoding='unicode')
    def icon(pid,key,index,x,y):
        asset=f'wmpp-journey-{index}.svg'
        v=ui.visual_shell(ident('journey:'+pid+':'+key),'image',ui.position(x,y,28,28,110010))
        v['visual']['objects']={'image':obj(sourceFile={'image':{'name':L(quoted(asset)),'url':{'expr':{'ResourcePackageItem':{'PackageName':'RegisteredResources','PackageType':1,'ItemName':asset}}},'scaling':L("'Fit'")}})}
        v['visual']['visualContainerObjects']={'background':obj(show=L('false')),'border':obj(show=L('false')),'dropShadow':obj(show=L('false')),'visualHeader':obj(show=L('false'))}
        put(pid,v)
    # Insert below existing filters, preserving every main-menu/dropdown position.
    starts={SINGLE:480,DETAIL:370,PROVIDER:354};shift=310
    for pid,start in starts.items():
        pagepath=DEFINITION/'pages'/pid/'page.json'
        docs[pagepath]['height']+=shift
        for p,v in docs.items():
            if p.name!='visual.json' or p.parents[2].name!=pid:continue
            if v['position']['y']>=start and not is_navigation(v):
                old=v['position']['y'];v['position']['y']+=shift;moved[v['name']]={'page':pid,'before_y':old,'after_y':v['position']['y']}
    # Bookmarks currently contain display states, not geometry; fail rather than overlook an override.
    for p,b in docs.items():
        if not p.name.endswith('.bookmark.json'):continue
        for sec in b.get('explorationState',{}).get('sections',{}).values():
            for vid,state in sec.get('visualContainers',{}).items():
                if vid in moved:assert 'position' not in json.dumps(state),('Bookmark has saved geometry',p,vid)
    for pid,start in starts.items():
        detail=pid==DETAIL;provider=pid==PROVIDER
        title='Referral journey' if not provider else 'Provider journey'
        text(pid,'title',title,36,start,1608,32,20)
        subtitle=('Recorded milestones; orange = current, green = evidenced, grey = not evidenced.' if detail else
                  'Distinct providers at their furthest evidenced stage in the current selection; not an additive offer count.' if provider else
                  'Distinct referrals by current stage. Each matching referral appears once; closed and unclear records are separate.')
        text(pid,'subtitle',subtitle,36,start+34,1608,34,12)
        labels=PROVIDER_LABELS if provider else REF_LABELS
        width=(1608-(len(labels)-1)*24)/len(labels)
        for i,label in enumerate(labels,1):
            x=36+(width+24)*(i-1);y=start+76
            panel(pid,f'panel-{i}',x,y,width,142)
            panel(pid,f'circle-{i}',x+16,y+13,48,48,'#FCA356',f'Journey detail colour {i}' if detail else None,24)
            icon(pid,f'icon-{i}',([2,3,4,5,6][i-1] if provider else i),x+26,y+23)
            text(pid,f'heading-{i}',label,x+76,y+18,width-88,45,13)
            name=f'Journey detail label {i}' if detail else f'Journey providers {i}' if provider else f'Journey referrals {i}'
            card(pid,f'value-{i}',name,x+16,y+79,width-32,54,14 if detail or (provider and i==4) else 26)
            if i<len(labels):text(pid,f'arrow-{i}','→',x+width+3,y+51,20,26,16)
        if detail:
            card(pid,'current','Journey current position',36,start+230,1608,28,15)
            card(pid,'next','Journey next action',36,start+263,1608,35,12)
        elif provider:
            card(pid,'coverage','Journey provider coverage',36,start+225,1608,30,13)
            text(pid,'limitations','Message activity includes either sender; browsing is not captured. Separate provider confirmation is not captured. Provider signed uses its IPA signature; both-signed is a subset, not an extra stage.',36,start+261,1608,40,12)
        else:
            card(pid,'exceptions','Journey referral exceptions',36,start+230,1608,30,14)
            text(pid,'note','Stage is evaluated from the refreshed referral, offer and IPA records. Drafts and declined/withdrawn offers do not advance the current stage; lifecycle messages remain activity only.',36,start+267,1608,34,12)
    # Make the derived stage inspectable next to each referral, and each provider ID.
    for p,v in docs.items():
        if p.name!='visual.json' or v.get('visual',{}).get('visualType')!='tableEx':continue
        pid=p.parents[2].name
        ps=v['visual'].get('query',{}).get('queryState',{}).get('Values',{}).get('projections',[])
        if pid==SINGLE and any(x.get('queryRef')=='fact_referral.referral_id' for x in ps):
            ps.insert(1,project('fact_referral','Journey stage',label='Journey stage'))
        if pid==PROVIDER and not v.get('isHidden') and any(x.get('queryRef')=='dim_provider.provider_id' for x in ps):
            ps.append(project(MT,'Journey provider label',True,label='Provider journey'))
    package=next(x for x in docs[DEFINITION/'report.json']['resourcePackages'] if x['name']=='RegisteredResources')
    for name in assets:
        assert not any(i['name']==name for i in package['items'])
        package['items'].append({'name':name,'path':name,'type':'Image'})
    for p,old in original.items():
        if p.name.endswith('.bookmark.json'):assert docs[p]==old
        if p.name=='visual.json' and is_navigation(old):assert docs[p]==old,('Navigation changed',p)
    for pid,vid in new_visuals:
        v=docs[DEFINITION/'pages'/pid/'visuals'/vid/'visual.json'];pos=v['position']
        assert pos['x']>=0 and pos['x']+pos['width']<=1680
        assert pos['y']+pos['height']<=docs[DEFINITION/'pages'/pid/'page.json']['height']
    return original,docs,assets,new_visuals,moved


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');args=parser.parse_args()
    marker=PROJECT/'JOURNEY_PATHWAYS.json';assert not marker.exists(),'Already applied; inspect the manifest before rerunning.'
    original,docs,assets,new_visuals,moved=build();defs=definitions();cols=column_definitions()
    result={'pages':[SINGLE,DETAIL,PROVIDER],'new_visuals':len(new_visuals),'shifted_visuals':len(moved),'measures':len(defs),'columns':2,'bookmarks_changed':0,'navigation_unchanged':True,'provider_gaps':['Browsing is not captured','Message authorship is not classified as provider vs council','Separate provider acceptance/confirmation is not captured'],'model_refresh_required':True,'engine_verified':False,'desktop_render_verified':False}
    print(json.dumps(result,indent=2))
    if not args.apply:return
    backup=PROJECT.parent/'_review'/('journey-pathways-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    shutil.copytree(DEFINITION,backup/'SM_WMPP_v16.Report/definition')
    shutil.copytree(MODEL,backup/'SM_WMPP_v16.SemanticModel/definition')
    for source,relative in [(DEFINITION,'SM_WMPP_v16.Report/definition'),(MODEL,'SM_WMPP_v16.SemanticModel/definition')]:
        for f in source.rglob('*'):
            if f.is_file():assert hashlib.sha256(f.read_bytes()).digest()==hashlib.sha256((backup/relative/f.relative_to(source)).read_bytes()).digest()
    add_columns(MODEL,'fact_referral',[(name,dtype,dax.replace('\n','\n\t\t\t'),extra) for name,dtype,dax,extra in cols])
    measures(MODEL,MT,defs)
    for name,svg in assets.items():
        for parent in [Path(__file__).resolve().parents[1]/'assets/brand-pack/icons/journey',REPORT/'StaticResources/RegisteredResources']:
            parent.mkdir(parents=True,exist_ok=True)
            (parent/name).write_text(svg,encoding='utf-8')
    for p,d in docs.items():
        if d!=original.get(p):save(p,d)
    result.update(backup=str(backup),moved_visuals=moved,new_visual_ids=new_visuals,stage_definitions={'referral':REF_LABELS+['Closed / cancelled / withdrawn','Needs review'],'provider':PROVIDER_LABELS},provider_grain='Distinct provider, highest evidenced stage in current filter context; separate confirmation unavailable. Provider signed includes both-signed.',referral_grain='One current stage per referral, calculated at model refresh; closed status overrides milestones.',status_mappings={'accepted':ACCEPTED,'pending':PENDING,'terminal_offer':TERMINAL_OFFER,'closed_referral':CLOSED})
    save(marker,result);print('Saved pathways. Backup:',backup)


if __name__=='__main__':main()
