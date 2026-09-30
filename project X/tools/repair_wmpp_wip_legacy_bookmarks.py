"""Redirect retained bookmark IDs from an absent old page to current Referrals."""
from copy import deepcopy
from build_report_design_delivery import read, save
from rework_wmpp_wip_storyboard import DEFINITION


def main():
    bookmarks={p:read(p) for p in (DEFINITION/'bookmarks').glob('*.bookmark.json')}
    by_title={b['displayName']:b for b in bookmarks.values()}
    changed=0
    for path,old in bookmarks.items():
        if old.get('explorationState',{}).get('activeSection')!='b8c7c2636c82c10870b2':
            continue
        title=old['displayName'].replace('Referral Overview','Referrals')
        replacement=deepcopy(by_title[title])
        replacement['name']=old['name']
        replacement['displayName']=title+' (legacy link)'
        save(path,replacement)
        changed+=1
    print({'redirected_missing_page_bookmarks':changed})


if __name__=='__main__':main()
