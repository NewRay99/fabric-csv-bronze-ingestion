"""Dry-run by default; consolidate WIP bookmarks while proving saved-state equivalence."""
import argparse
from collections import defaultdict
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import shutil

from build_report_design_delivery import read, save, L
from rework_wmpp_wip_storyboard import PROJECT, DEFINITION
from add_wmpp_table_icons_provider_detail import replace_ids, EXPLORER, DETAIL


def actions(v):
    for entry in v.get('visual',{}).get('visualContainerObjects',{}).get('visualLink',[]):
        properties=entry.get('properties',{})
        target=properties.get('bookmark',{}).get('expr',{}).get('Literal',{}).get('Value','').strip("'")
        if target:yield properties,target


def refs(docs, bookmarks):
    result=defaultdict(int)
    for p,d in docs.items():
        if p.parent.name=='bookmarks' and p.name=='bookmarks.json':continue
        text=json.dumps(d)
        for bid in bookmarks:
            if bid in text:result[bid]+=1
    return result


def applicable_state(b,pages,visuals):
    """Keep every payload for an extant page/visual, including absent display = visible."""
    result=deepcopy(b)
    result.pop('name',None);result.pop('displayName',None)
    result['explorationState']['sections']={pid:sec for pid,sec in result['explorationState'].get('sections',{}).items() if pid in pages}
    opts=result.get('options',{})
    if 'targetVisualNames' in opts:opts['targetVisualNames']=[vid for vid in opts['targetVisualNames'] if vid in visuals]
    return result


def build():
    original={p:read(p) for p in DEFINITION.rglob('*.json')}
    docs=deepcopy(original)
    bp={d['name']:p for p,d in docs.items() if p.name.endswith('.bookmark.json')}
    before={bid:deepcopy(docs[p]) for bid,p in bp.items()}
    pages={p.parent.name for p in docs if p.name=='page.json'}
    visuals={d['name']:(p,d) for p,d in docs.items() if p.name=='visual.json'}
    assert all(b['explorationState']['activeSection'] in pages for b in before.values())

    # Fix only local menu actions; Go to Provider Explorer remains real navigation.
    menu_map={}
    for bid,b in before.items():
        if b['explorationState']['activeSection']!=EXPLORER or ' | ' not in b['displayName']:continue
        suffix=b['displayName'].split(' | ',1)[1]
        matches=[other for other,v in before.items() if v['explorationState']['activeSection']==DETAIL and v['displayName'].endswith(' | '+suffix)]
        assert len(matches)==1,(b['displayName'],matches)
        menu_map[bid]=matches[0]
    fixed=[]
    for vid,(p,v) in visuals.items():
        if p.parents[2].name!=DETAIL:continue
        if any(bid in menu_map for _,bid in actions(v)):
            docs[p]=replace_ids(v,menu_map);fixed.append(vid)

    # Disable dangling actions only if their owner can never be shown by saved bookmarks.
    disabled=[]
    for vid,(p,_) in visuals.items():
        v=docs[p];pid=p.parents[2].name
        dead=[bid for _,bid in actions(v) if bid not in before]
        if not dead:continue
        assert v.get('isHidden') is True,('Visible broken button needs a separate decision',pid,vid)
        for b in before.values():
            state=b['explorationState'].get('sections',{}).get(pid,{}).get('visualContainers',{}).get(vid)
            if state is not None and vid in b.get('options',{}).get('targetVisualNames',[]):
                assert state.get('singleVisual',{}).get('display',{}).get('mode')=='hidden',(vid,b['displayName'])
        v['visual']['visualContainerObjects']['visualLink']=[{'properties':{'show':L('false')}}]
        disabled.append({'page':pid,'visual':vid,'missing_bookmarks':dead})

    # Remove only references to absent objects, never visibility/reset behaviour.
    removed_sections=0;removed_targets=0
    for bid,p in bp.items():
        old=docs[p]
        normalized=applicable_state(old,pages,visuals)
        removed_sections+=len(old['explorationState'].get('sections',{}))-len(normalized['explorationState'].get('sections',{}))
        removed_targets+=len(old.get('options',{}).get('targetVisualNames',[]))-len(normalized.get('options',{}).get('targetVisualNames',[]))
        docs[p]={'$schema':old['$schema'],'displayName':old['displayName'],'name':old['name'],**normalized}

    reference_counts=refs({p:d for p,d in docs.items() if not p.name.endswith('.bookmark.json')},before)
    groups=defaultdict(list)
    for bid,p in bp.items():
        signature=json.dumps({k:v for k,v in docs[p].items() if k not in ('name','displayName')},sort_keys=True)
        groups[signature].append(bid)
    redirects={};merges=[]
    for bids in groups.values():
        if len(bids)<2:continue
        def preference(bid):
            title=before[bid]['displayName']
            return ('legacy' in title.lower(),not title.endswith(' | Close menus'),-reference_counts[bid],bid)
        canonical=min(bids,key=preference)
        titles=[before[bid]['displayName'] for bid in bids]
        if any('Close menus' in n for n in titles) and any('Close filters' in n for n in titles):
            docs[bp[canonical]]['displayName']=before[canonical]['displayName'].split(' | ',1)[0]+' | Close overlays'
        for bid in bids:
            if bid!=canonical:redirects[bid]=canonical
        merges.append({'kept':canonical,'name':docs[bp[canonical]]['displayName'],'merged_ids':[bid for bid in bids if bid!=canonical],'previous_names':titles})
    for p,d in list(docs.items()):
        if p.name.endswith('.bookmark.json') and d['name'] in redirects:del docs[p];continue
        if not p.name.endswith('.bookmark.json'):docs[p]=replace_ids(d,redirects)

    # Collapse duplicate navigator/pane entries after redirecting IDs.
    metadata=docs[DEFINITION/'bookmarks/bookmarks.json'];seen=set()
    def unique_items(items):
        result=[]
        for item in items:
            if 'items' in item:
                item['items']=unique_items(item['items'])
                if item['items']:result.append(item)
            elif item.get('name') not in seen:
                seen.add(item.get('name'));result.append(item)
        return result
    metadata['items']=unique_items(metadata['items'])
    remaining={d['name']:d for p,d in docs.items() if p.name.endswith('.bookmark.json')}
    assert seen==set(remaining),(seen-set(remaining),set(remaining)-seen)

    # Differential checks prove each original control still gets the same live states.
    for bid,old in before.items():
        new=remaining[redirects.get(bid,bid)]
        assert applicable_state(old,pages,visuals)==applicable_state(new,pages,visuals),bid
    for p,old in original.items():
        if p.name!='visual.json':continue
        new=docs[p]
        assert old['position']==new['position'] and old.get('isHidden')==new.get('isHidden'),p
        assert old.get('visual',{}).get('query')==new.get('visual',{}).get('query'),p
        for _,bid in actions(new):
            assert bid in remaining,(p,bid)
            target=remaining[bid]
            if p.parents[2].name==DETAIL and ' | ' in target['displayName']:
                assert target['explorationState']['activeSection']==DETAIL,(p,target['displayName'])
                assert target['options'].get('suppressData') is True
    for bid,b in remaining.items():
        assert b['options'].get('suppressData') is True,bid
        assert b['explorationState']['activeSection'] in pages
    live_refs=refs({p:d for p,d in docs.items() if not p.name.endswith('.bookmark.json')},remaining)
    unreferenced=[b['displayName'] for bid,b in remaining.items() if not live_refs[bid]]
    assert not unreferenced,('Review manually accessible but unreferenced bookmarks',unreferenced)

    def encoded(p,d):
        # Formatting whitespace has no behavioural meaning. Retain all state payloads.
        return (json.dumps(d,ensure_ascii=False,separators=(',',':'))+'\n') if p.parent.name=='bookmarks' else (json.dumps(d,ensure_ascii=False,indent=2)+'\n')
    old_bytes=sum(p.stat().st_size for p in bp.values())
    new_bytes=sum(len(encoded(p,d).encode()) for p,d in docs.items() if p.name.endswith('.bookmark.json'))
    result={'bookmarks_before':len(before),'bookmarks_after':len(remaining),'bytes_before':old_bytes,'bytes_after':new_bytes,'reduction_percent':round(100*(1-new_bytes/old_bytes),1),'largest_bookmark_after_bytes':max(len(encoded(p,d).encode()) for p,d in docs.items() if p.name.endswith('.bookmark.json')),'provider_detail_menu_actions_fixed':len(fixed),'retired_dead_actions_disabled':disabled,'removed_empty_absent_page_sections':removed_sections,'removed_stale_target_ids':removed_targets,'merges':merges,'unreferenced_bookmarks_remaining':unreferenced,'saved_state_equivalence_verified':True,'existing_positions_queries_visibility_preserved':True,'desktop_render_verified':False}
    return original,docs,result,encoded


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--reapply',action='store_true',help='Re-audit restored files and preserve the prior manifest in the new backup.')
    args=parser.parse_args()
    marker=PROJECT/'BOOKMARK_CLEANUP.json'
    assert not marker.exists() or args.reapply,'Already applied; inspect the existing cleanup manifest first, then use --reapply.'
    original,docs,result,encoded=build()
    print(json.dumps({k:v for k,v in result.items() if k not in ('merges','retired_dead_actions_disabled')},indent=2))
    print('Merged duplicate files:',len(original)-len(docs),'Disabled hidden legacy actions:',len(result['retired_dead_actions_disabled']))
    if not args.apply:return
    backup=PROJECT.parent/'_review'/('bookmark-cleanup-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    backup_definition=backup/'SM_WMPP_v16.Report/definition'
    shutil.copytree(DEFINITION,backup_definition)
    if marker.exists():
        shutil.copy2(marker,backup/marker.name)
        assert marker.read_bytes()==(backup/marker.name).read_bytes()
    # Existing source definitions are copied and hash-checked before removing duplicates.
    for p in original:
        assert hashlib.sha256(p.read_bytes()).digest()==hashlib.sha256((backup_definition/p.relative_to(DEFINITION)).read_bytes()).digest(),p
    for p,d in docs.items():
        if p.parent.name=='bookmarks' or d!=original.get(p):p.write_text(encoded(p,d),encoding='utf-8')
    for p in original.keys()-docs.keys():
        resolved=p.resolve()
        assert resolved.parent==(DEFINITION/'bookmarks').resolve() and resolved.name.endswith('.bookmark.json')
        assert (backup_definition/p.relative_to(DEFINITION)).exists()
        p.unlink()  # Exact redundant file only; complete recoverable backup verified above.
    result['backup']=str(backup)
    result['bytes_after']=sum(p.stat().st_size for p in docs if p.name.endswith('.bookmark.json'))
    result['reduction_percent']=round(100*(1-result['bytes_after']/result['bytes_before']),1)
    save(marker,result)
    print('Saved cleanup; recoverable backup:',backup)


if __name__=='__main__':main()
