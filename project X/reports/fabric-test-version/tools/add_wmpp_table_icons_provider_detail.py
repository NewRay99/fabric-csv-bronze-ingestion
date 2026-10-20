"""Add WIP category icon formatting and provider-key drillthrough, with rollback backup."""
from copy import deepcopy
from datetime import datetime
from pathlib import Path
import base64
import hashlib
import json
import re
import shutil
import xml.etree.ElementTree as ET
from wmpp_status_icons import TARGET_COLUMNS, icon_format as status_icon_format, icons as status_icons

from build_report_design_delivery import read, save, L, quoted, field, project, obj, fill, ident, measures, add_columns
from rework_wmpp_wip_storyboard import PROJECT, REPORT, MODEL, DEFINITION
from refine_wmpp_wip_filters_width import is_navigation
import rebuild_mission_control_dashboard_v16 as ui

EXPLORER = '08ef33dc6a87d1b14392'
DETAIL = ident('wmpp-provider-detail-page')
MT = '_Provider Detail Measures'
BRAND = Path(__file__).resolve().parents[1]/'assets/brand-pack/icons'
PALETTE = {'orange':'#EF7911','blue':'#0D35B8','berry':'#E63496','red':'#C0392B','amber':'#E69512','green':'#277455','teal':'#4DAAAB','ink':'#2B2B2C'}


def replace_ids(node, mapping):
    if isinstance(node, str):
        if node in mapping:return mapping[node]
        if node.startswith("'") and node.endswith("'") and node[1:-1] in mapping:
            return "'"+mapping[node[1:-1]]+"'"
        return node
    if isinstance(node, list): return [replace_ids(v, mapping) for v in node]
    if isinstance(node, dict): return {mapping.get(k,k):replace_ids(v,mapping) for k,v in node.items()}
    return node


def parse_columns():
    result={}
    for p in (MODEL/'tables').glob('*.tmdl'):
        text=p.read_text(encoding='utf-8-sig')
        for match in re.finditer(r"(?m)^\tcolumn (?:'((?:[^']|'')+)'|([^\s=]+))[^\n]*\n((?:\t\t[^\n]*\n|\n)*)",text):
            name=(match[1] or match[2]).replace("''", "'")
            dtype=re.search(r'dataType: (\w+)',match[3])
            result[(p.stem,name)]=dtype[1] if dtype else 'string'
    return result


def icons():
    # Reuse the project's licensed Lucide geometry; small primitives are original.
    specs={
        'critical':('triangle-alert-c13f35','red'), 'high':('triangle-alert-c13f35','orange'),
        'medium':('clock-a86612','amber'), 'planned':('calendar-days-d94d2b','teal'),
        'accepted':('file-check-corner-287c73','green'), 'pending':('clock-a86612','amber'),
        'draft':('file-pen-line-d94d2b','blue'), 'closed':('clipboard-check-575756','ink'),
        'assigned':('users-d94d2b','blue'), 'offer':('handshake-d94d2b','orange'),
        'active':('activity-287c73','teal'), 'residential':('house-d94d2b','orange'),
        'fostering':('users-d94d2b','teal'), 'supported':('building-complex-d94d2b','blue'),
        'framework':('network-d94d2b','blue'), 'review':('triangle-alert-c13f35','amber'),
        'location':('map-pin-287c73','teal'), 'event':('route-d94d2b','blue')}
    raw={}
    for key,(asset,color) in specs.items():
        source=BRAND/f'lucide-kpi-{asset}.svg'
        root=ET.fromstring(source.read_text(encoding='utf-8-sig'))
        root.set('viewBox','0 0 24 24');root.set('width','24');root.set('height','24')
        for el in root.iter():
            if el.get('stroke') and el.get('stroke')!='none':el.set('stroke',PALETTE[color])
        root.set('stroke',PALETTE[color])
        raw[key]=ET.tostring(root,encoding='unicode')
    simple={
        'yes':('teal','<path d="m5 12 4 4L19 6"/>'),
        'no':('ink','<path d="M5 12h14"/>'),
        'declined':('berry','<path d="m6 6 12 12M18 6 6 18"/>'),
        'cancelled':('ink','<circle cx="12" cy="12" r="9"/><path d="m6 6 12 12"/>'),
        'unknown':('ink','<circle cx="12" cy="12" r="9"/><path d="M9 9a3 3 0 0 1 6 0c0 2-3 2-3 4M12 17h.01"/>'),
        'category':('ink','<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>')}
    for key,(color,body) in simple.items():
        raw[key]=f'<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{PALETTE[color]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>'
    raw.update(status_icons())
    return raw


PRIORITY={'Critical':'critical','Emergency':'critical','Urgent':'critical','High':'high','Medium':'medium','Normal':'medium','Low':'planned','Planned':'planned','Unspecified':'unknown','Unknown':'unknown','Must have':'critical','Should have':'high','Could have':'medium'}
STATUS={'Open':'active','Active':'active','First contact':'assigned','Assigned':'assigned','Under_offer':'offer','Under offer':'offer','Offer made':'offer','Offer_made':'offer','Pending':'pending','Awaiting':'pending','Draft':'draft','Accepted':'accepted','Successful':'accepted','Approved':'accepted','Completed':'accepted','Complete':'accepted','Closed':'closed','Cancelled':'cancelled','Canceled':'cancelled','Withdrawn':'cancelled','Excluded':'cancelled','Declined':'declined','Rejected':'declined','Unsuccessful':'declined','Inactive':'closed','On hold':'pending','In progress':'pending','Not started':'draft','On Track':'active','Due Soon':'pending','Overdue':'critical','No target':'unknown','Implemented':'accepted','Delivered':'accepted','Yes':'yes','No':'no','Unknown':'unknown'}
PLACEMENT={'Residential':'residential',"Children's Home":'residential','Residential Care':'residential','PLCM-RESI':'residential','Fostering':'fostering','Foster Care':'fostering','PLCM-FOST':'fostering','Supported Accommodation':'supported','Supported accommodation':'supported','Supported Living':'supported','Semi Independent':'supported','PLCM-SUPA':'supported','Unspecified':'unknown','Unknown':'unknown'}


def category(t,c,types):
    lower=c.lower()
    if types.get((t,c))=='boolean' or lower.startswith(('is_','has_')):return 'boolean'
    if lower in ('priority','placement_urgency_band'):return 'priority'
    if 'status' in lower or t=='Target Status':return 'status'
    if lower in ('placement_type','placement_type_required','service_type'):return 'placement'
    if any(s in lower for s in ('framework','category')) and not lower.endswith(('_id','_count')):return 'framework'
    if c in ('Offer activity band','Location type','event_type') or (c=='Label' and t in ('Offer Journey Stage','Days to Target','Open Referral Age','Placement Window')):return 'category'
    return None


def rules(t,c,kind):
    if kind=='boolean':return [(True,'yes'),(False,'no')], 'unknown'
    if kind=='priority':return list(PRIORITY.items()),'unknown'
    if kind=='status':return list(STATUS.items()),'category'
    if kind=='placement':return list(PLACEMENT.items()),'location'
    if kind=='framework':return [],'framework'
    if c=='Location type':return [('Assigned provider','assigned'),('Offer home','residential')],'location'
    if c=='Offer activity band':return [('0-3 days','active'),('4-7 days','planned'),('8-14 days','medium'),('15+ days','high'),('Review','review'),('Unknown','unknown')],'unknown'
    if c=='event_type':return [],'event'
    return [],'category'


def icon_format(t,c,kind,reference=None):
    if kind == 'status' and c in TARGET_COLUMNS:
        return status_icon_format(reference or field(t,c))
    choices,default=rules(t,c,kind)
    reference=reference or field(t,c)
    cases=[{'Condition':{'In':{'Expressions':[reference],'Values':[[{'Literal':{'Value':'null'}}]]}},'Value':{'Literal':{'Value':"'wmpp-category-unknown'"}}}]
    for label,key in choices:
        literal=str(label).lower() if isinstance(label,bool) else quoted(label)
        cases.append({'Condition':{'Comparison':{'ComparisonKind':0,'Left':reference,'Right':{'Literal':{'Value':literal}}}},'Value':{'Literal':{'Value':quoted('wmpp-category-'+key)}}})
    return {'kind':'Icon','layout':L("'Before'"),'verticalAlignment':L("'Middle'"),'value':{'expr':{'Conditional':{'Cases':cases,'DefaultValue':{'Literal':{'Value':quoted('wmpp-category-'+default)}}}}}}


def main():
    marker=PROJECT/'TABLE_CATEGORY_ICONS_PROVIDER_DETAIL.json'
    assert not marker.exists(),'Already applied; inspect the saved manifest before rerunning.'
    previous=sorted((PROJECT.parent/'_review').glob('table-icons-provider-detail-*'))
    backup=previous[-1] if previous else PROJECT.parent/'_review'/('table-icons-provider-detail-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    if not previous:
        shutil.copytree(PROJECT,backup,ignore=shutil.ignore_patterns('.pbi','.git'))
    cache=PROJECT/'SM_WMPP_v16.SemanticModel/.pbi/cache.abf'
    cache_hash=hashlib.sha256(cache.read_bytes()).hexdigest()
    docs={p:read(p) for p in DEFINITION.rglob('*.json')};original=deepcopy(docs)
    icon_assets=icons()
    icon_dir=BRAND/'category-icons';icon_dir.mkdir(parents=True,exist_ok=True)
    for key,svg in icon_assets.items(): (icon_dir/f'wmpp-category-{key}.svg').write_text(svg,encoding='utf-8')
    shutil.copy2(BRAND/'LUCIDE_LICENSE.txt',icon_dir/'LUCIDE_LICENSE.txt')
    for p in [PROJECT/'WMPP_Theme.json',REPORT/'StaticResources/RegisteredResources/WMPP_Theme.json']:
        theme=read(p)
        for key,svg in icon_assets.items():
            theme.setdefault('icons',{})['wmpp-category-'+key]={'description':'WMPP category: '+key,'url':'data:image/svg+xml;base64,'+base64.b64encode(svg.encode()).decode()}
        save(p,theme)

    # Additive measures only: no relationship changes or role/connection edits.
    selected="COUNTROWS(ALLSELECTED('dim_provider')) = 1"
    home_count="CALCULATE(COUNTROWS('dim_provider_home'), KEEPFILTERS(TREATAS(VALUES('dim_provider'[provider_id]),'dim_provider_home'[provider_id])))"
    defs=[('Provider explorer matching homes',f'VAR n = {home_count} RETURN IF(n > 0,n)', '#,0')]
    for label,expression in [('Provider detail profile rows',"COUNTROWS('dim_provider')"),('Provider detail home rows',home_count),('Provider detail assignment rows',"COUNTROWS('fact_referral_provider')"),('Provider detail offer rows',"COUNTROWS('fact_offer')"),('Provider detail message rows',"COUNTROWS('dim_referral_provider_message')")]:
        defs.append((label,f'VAR n = {expression} RETURN IF({selected} && n > 0,n)', '#,0'))
    measures(MODEL,MT,defs)

    # Clone header/menu visuals and the five display-only menus; retain navigation targets.
    source_visuals={p:v for p,v in docs.items() if p.name=='visual.json' and p.parents[2].name==EXPLORER}
    keep={p:v for p,v in source_visuals.items() if is_navigation(v) or (v['position']['y']<170 and v.get('visual',{}).get('visualType') in ('image','textbox'))}
    bookmarks={p:b for p,b in docs.items() if p.name.endswith('.bookmark.json') and b.get('explorationState',{}).get('activeSection')==EXPLORER and ' | ' in b.get('displayName','')}
    mapping={EXPLORER:DETAIL,**{v['name']:ident('provider-detail:'+v['name']) for v in keep.values()},**{b['name']:ident('provider-detail:'+b['name']) for b in bookmarks.values()}}
    for p,v in keep.items():
        new=replace_ids(deepcopy(v),mapping)
        for e in new.get('visual',{}).get('objects',{}).get('general',[]):
            for paragraph in e.get('properties',{}).get('paragraphs',[]):
                for run in paragraph.get('textRuns',[]):
                    if 'Provider Explorer' in run.get('value',''):run['value']='Provider Detail'
        docs[DEFINITION/'pages'/DETAIL/'visuals'/new['name']/'visual.json']=new
    for p,b in bookmarks.items():
        new=replace_ids(deepcopy(b),mapping);new['displayName']=new['displayName'].replace('Provider Explorer','Provider Detail')
        for sec in new['explorationState'].get('sections',{}).values():
            if 'visualContainers' in sec:sec['visualContainers']={k:v for k,v in sec['visualContainers'].items() if k in mapping.values()}
        if 'targetVisualNames' in new.get('options',{}):new['options']['targetVisualNames']=[n for n in new['options']['targetVisualNames'] if n in mapping.values()]
        docs[DEFINITION/'bookmarks'/f"{new['name']}.bookmark.json"]=new
        docs[DEFINITION/'bookmarks/bookmarks.json']['items'].append({'name':new['name']})
    page=deepcopy(docs[DEFINITION/'pages/4cad3706fca6451c66b8/page.json'])
    page.update(name=DETAIL,displayName='Provider Detail (Drillthrough)',height=2170,width=1680,visibility='HiddenInViewMode')
    filter_id=ident('provider-detail-key-filter')
    page['filterConfig']={'filters':[{'name':filter_id,'field':field('dim_provider','provider_id'),'type':'Categorical','howCreated':'Drillthrough'}]}
    page['pageBinding']={'name':ident('provider-detail-binding'),'type':'Drillthrough','parameters':[{'name':ident('provider-detail-key'),'boundFilter':filter_id,'fieldExpr':field('dim_provider','provider_id')}],'acceptsFilterContext':'None'}
    page['annotations']=[{'name':'wmppPurpose','value':'Selected provider: profile, homes, assignments, offers and messages'}]
    docs[DEFINITION/'pages'/DETAIL/'page.json']=page
    pages=docs[DEFINITION/'pages/pages.json']['pageOrder'];pages.insert(pages.index(EXPLORER)+1,DETAIL)

    def put(v):
        docs[DEFINITION/'pages'/DETAIL/'visuals'/v['name']/'visual.json']=v
        return v
    def text(key,label,x,y,w,h,size=13):
        return put(ui.textbox(ident('provider-detail:'+key),label,ui.position(x,y,w,h,100000),size,False))
    def shell(key,kind,x,y,w,h,title):
        v=ui.visual_shell(ident('provider-detail:'+key),kind,ui.position(x,y,w,h,90000))
        v['visual']['visualContainerObjects']={'title':obj(show=L('true'),text=L(quoted(title)),fontSize=L('13D'),bold=L('false'),fontFamily=L("'Segoe UI'")),'background':obj(show=L('true'),color=fill('#FFFFFF'),transparency=L('0D')),'border':obj(show=L('true'),color=fill('#FFFFFF'),radius=L('14D')),'padding':obj(top=L('16D'),bottom=L('16D'),left=L('16D'),right=L('16D'))}
        return put(v)
    def gate(v,measure):
        mf=field(MT,measure,True)
        filt={'name':ident(v['name']+':scope'),'field':mf,'type':'Advanced','filter':{'Version':2,'From':[{'Name':'m','Entity':MT,'Type':0}],'Where':[{'Condition':{'Comparison':{'ComparisonKind':2,'Left':{'Measure':{'Expression':{'SourceRef':{'Source':'m'}},'Property':measure}},'Right':{'Literal':{'Value':'1L'}}}}}]},'howCreated':'User'}
        v.setdefault('filterConfig',{}).setdefault('filters',[]).append(filt)
    def tab(key,title,cols,y,h,measure):
        v=shell(key,'tableEx',36,y,1608,h,title)
        ps=[]
        for t,c,label in cols:
            pr=project(t,c);pr['displayName']=label;ps.append(pr)
        v['visual']['query']={'queryState':{'Values':{'projections':ps}}}
        v['visual']['objects']={'columnHeaders':obj(fontSize=L('11D'),bold=L('false')),'values':obj(fontSize=L('11D'))}
        gate(v,measure)
        return v

    text('instruction','Provider-specific profile, homes, referral assignments, offers and messages. Use Back to results to return to your previous selection.',36,210,1300,42)
    back=shell('back','actionButton',1380,156,264,48,'')
    back['visual']['visualContainerObjects']['title']=obj(show=L('false'))
    back['visual']['visualContainerObjects']['visualLink']=obj(show=L('true'),type=L("'Back'"),tooltip=L("'Back to Provider Explorer'"))
    back['visual']['objects']={'text':[{'properties':{'show':L('true'),'text':L("'Back to results'"),'fontSize':L('12D'),'bold':L('false')},'selector':{'id':'default'}}]}
    tab('profile','Provider profile',[('dim_provider',c,l) for c,l in [('provider_id','Provider ID'),('provider_name','Provider'),('provider_status','Status'),('town_city','Town / city'),('county','County'),('postcode','Postcode'),('qa_flag','QA flag')]],270,175,'Provider detail profile rows')
    tab('homes','Provider homes',[('dim_provider_home',c,l) for c,l in [('provider_home_id','Home ID'),('home_name','Home'),('service_type','Placement type'),('town_city','Town / city'),('postcode','Postcode'),('registered_beds','Registered beds'),('is_spot','Spot provision'),('qa_flag','QA flag')]],479,300,'Provider detail home rows')
    tab('assignments','Referral assignments and responses',[('fact_referral_provider',c,l) for c,l in [('referral_id','Referral ID'),('referral_provider_id','Assignment ID'),('provider_response_status','Response status'),('assigned_at','Assigned'),('first_qualifying_response_at','First qualifying response'),('response_elapsed_minutes','Response minutes'),('is_engaged','Engaged'),('is_declined','Declined'),('is_closed','Closed')]],813,330,'Provider detail assignment rows')
    tab('offers','Offers and proposed homes',[('fact_offer',c,l) for c,l in [('offer_id','Offer ID'),('referral_id','Referral ID'),('offer_status','Offer status'),('offer_submitted_date','Submitted'),('offer_decision_date','Decision'),('Offer activity band','Activity band'),('estimated_weekly_cost','Weekly cost')]]+[('dim_provider_home','home_name','Proposed home'),('dim_provider_home','service_type','Placement type')],1177,360,'Provider detail offer rows')
    tab('messages','Provider messages',[('fact_referral_provider','referral_id','Referral ID')]+[('dim_referral_provider_message',c,l) for c,l in [('referral_provider_id','Assignment ID'),('created_timestamp','Created'),('created_by','Created by'),('message_text','Message'),('message_read_timestamp','Read')]],1571,440,'Provider detail message rows')
    text('note','Icons supplement the recorded text. A check means Yes, not a positive business outcome. Missing or unrecognised values remain labelled; no status is inferred. Empty tables can mean no matching records or restricted access.',36,2040,1608,90)

    # Provider ID gives an unambiguous drillthrough key even when provider names repeat.
    source_tables=[]
    for p,v in source_visuals.items():
        vi=v.get('visual',{})
        if vi.get('visualType')!='tableEx' or v.get('isHidden'):continue
        ps=vi['query']['queryState']['Values']['projections']
        if any(pr.get('queryRef')=='dim_provider.provider_name' for pr in ps):
            pr=project('dim_provider','provider_id');pr['displayName']='Provider ID'
            if not any(x.get('queryRef')==pr['queryRef'] for x in ps):ps.insert(0,pr)
            source_tables.append(v['name'])
            if any(x.get('queryRef')=='dim_provider_home.home_name' for x in ps):gate(v,'Provider explorer matching homes')
    tip=ui.textbox(ident('provider-explorer:drillthrough-tip'),'Right-click a Provider ID in the tables → Drill through → Provider Detail (Drillthrough).',ui.position(36,1522,1608,65,100000),13,False)
    docs[DEFINITION/'pages'/EXPLORER/'visuals'/tip['name']/'visual.json']=tip

    # Native icon + text formatting retains raw fields, sorting and drillthrough keys.
    types=parse_columns();coverage=[]
    for p,v in list(docs.items()):
        if p.name!='visual.json' or v.get('visual',{}).get('visualType')!='tableEx':continue
        vi=v['visual'];entries=vi.setdefault('objects',{}).setdefault('values',[])
        for pr in vi.get('query',{}).get('queryState',{}).get('Values',{}).get('projections',[]):
            cf=pr.get('field',{}).get('Column') or pr.get('field',{}).get('Aggregation',{}).get('Expression',{}).get('Column')
            if not cf:continue
            t=cf['Expression']['SourceRef']['Entity'];c=cf['Property'];kind=category(t,c,types)
            if not kind:continue
            selector={'data':[{'dataViewWildcard':{'matchingOption':1}}],'metadata':pr['queryRef']}
            existing=next((e for e in entries if e.get('selector')==selector),None)
            if existing is None:existing={'properties':{},'selector':selector};entries.append(existing)
            existing['properties']['icon']=icon_format(t,c,kind,pr['field'])
            coverage.append({'page':p.parents[2].name,'visual':v['name'],'table':t,'column':c,'category':kind,'hidden_visual':bool(v.get('isHidden'))})

    # Matrix headers cannot use value-cell icon formatting. Use compact glyph + text
    # display columns for the existing urgency/target matrix, preserving original fields.
    matrix_fields=[('fact_referral','placement_urgency_band','Urgency icon label',PRIORITY),('Target Status','Label','Target icon label',STATUS)]
    glyph={'critical':'▲','high':'▲','medium':'◷','planned':'◇','unknown':'?','active':'✓','pending':'◷'}
    for t,c,new,mapping_values in matrix_fields:
        cases=', '.join('"'+label+'", "'+glyph.get(k,'•')+' " & raw' for label,k in mapping_values.items())
        dax=f'VAR raw = \'{t}\'[{c}] RETURN IF(ISBLANK(raw), "? Unknown", SWITCH(raw, {cases}, "• " & raw))'
        sort='\t\tsortByColumn: Ordinal\n' if t=='Target Status' else ''
        add_columns(MODEL,t,[(new,'string',dax, '\t\tdisplayFolder: Presentation icons\n'+sort)])
    matrix_changes=0
    for p,v in docs.items():
        if p.name!='visual.json' or v.get('visual',{}).get('visualType')!='pivotTable':continue
        for t,c,new,_ in matrix_fields:
            old=field(t,c);replacement=field(t,new)
            def swap(node):
                if node==old:return deepcopy(replacement)
                if isinstance(node,list):return [swap(x) for x in node]
                if isinstance(node,dict):return {k:swap(x) for k,x in node.items()}
                return node
            for well in v['visual']['query']['queryState'].values():
                for pr in well.get('projections',[]):
                    if pr.get('field')==old:
                        oldref=pr['queryRef'];pr['field']=replacement;pr['queryRef']=t+'.'+new;pr['nativeQueryRef']=new;pr['displayName']='Urgency' if t=='fact_referral' else 'Target status';matrix_changes+=1
                        v['visual']['objects']=replace_ids(v['visual'].get('objects',{}),{oldref:pr['queryRef']})
            if 'sortDefinition' in v['visual']['query']:v['visual']['query']['sortDefinition']=swap(v['visual']['query']['sortDefinition'])

    # Existing bookmarks and navigation coordinates must not change.
    for p,before in original.items():
        if p.name.endswith('.bookmark.json'):assert docs[p]==before,p
        if p.name=='visual.json':
            assert before['position']==docs[p]['position'],p
            assert before.get('isHidden')==docs[p].get('isHidden'),p
    for p,d in docs.items():
        if p not in original or d!=original[p]:save(p,d)
    assert hashlib.sha256(cache.read_bytes()).hexdigest()==cache_hash,'Cache unexpectedly changed.'
    save(icon_dir/'ICON_CATALOG.json',{'icons':[{'name':'wmpp-category-'+k,'file':'wmpp-category-'+k+'.svg'} for k in icon_assets],'palette':PALETTE,'table_rules':{'priority':PRIORITY,'status':STATUS,'placement':PLACEMENT},'boolean_meaning':'Yes/No values only, not good/bad. Missing values use question-mark icon.','licence':'LUCIDE_LICENSE.txt covers adapted existing Lucide geometry; simple check/minus/cross/ban/question/grid primitives are original.','rendering':'Embedded custom theme icons; no external image hosting.'})
    result={'backup':str(backup),'provider_detail_page':DETAIL,'provider_drillthrough_field':'dim_provider.provider_id','source_provider_tables':source_tables,'icons':len(icon_assets),'category_field_instances':len(coverage),'tables_formatted':len({(x['page'],x['visual']) for x in coverage}),'coverage':coverage,'matrix_display_fields':matrix_changes,'new_page_menu_bookmarks':len(bookmarks),'existing_bookmarks_unchanged':True,'existing_positions_unchanged':True,'cache_unchanged':True,'relationships_and_roles_unchanged':True,'desktop_render_verified':False,'model_runtime_verified':False}
    save(marker,result)
    print(json.dumps({k:v for k,v in result.items() if k!='coverage'},indent=2))


if __name__=='__main__':main()
