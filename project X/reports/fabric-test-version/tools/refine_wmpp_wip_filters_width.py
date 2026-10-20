"""Scoped WIP presentation cleanup; preserve model, cache, navigation and queries."""
from copy import deepcopy
from datetime import datetime
import json
from pathlib import Path
import re
import shutil

PROJECT = Path(__file__).resolve().parents[1] / 'reports/client-deliverables/WMPP v16/SM WMPP v16 updated WIP'
REPORT = PROJECT / 'SM_WMPP_v16.Report'
DEFINITION = REPORT / 'definition'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def literal(s):
    return {'expr': {'Literal': {'Value': s}}}


def value(p):
    return p.get('expr', {}).get('Literal', {}).get('Value', '').strip("'")


def rename(node):
    if isinstance(node, str):
        node = re.sub(r'Referral Single View', 'Referral Explorer', node, flags=re.I)
        return re.sub(r'Provider Single View', 'Provider Explorer', node, flags=re.I)
    if isinstance(node, list):
        return [rename(x) for x in node]
    if isinstance(node, dict):
        return {k: rename(v) for k, v in node.items()}
    return node


def props(objects, key):
    return objects.setdefault(key, [{'properties': {}}])[0].setdefault('properties', {})


def is_navigation(v):
    pos = v['position']
    alt = json.dumps(v.get('visual', {}).get('visualContainerObjects', {}).get('general', []))
    return (pos['y'] < 120 or 'WMPP navigation:' in alt or 'White dropdown surround:' in alt
            or 'Open Filters' in alt or 'Close Filters' in alt)


def main():
    manifest = PROJECT / 'FILTER_EXPLORER_WIDTH_UPDATE.json'
    if manifest.exists():
        raise SystemExit('Already applied; inspect the existing manifest before any rerun.')
    paths = list(DEFINITION.rglob('*.json')) + [PROJECT/'WMPP_Theme.json', REPORT/'StaticResources/RegisteredResources/WMPP_Theme.json']
    original = {p: read(p) for p in paths}
    docs = {p: rename(d) for p, d in original.items()}
    slicers = 0
    for p, doc in docs.items():
        if p.name == 'WMPP_Theme.json':
            styles = doc['visualStyles']['slicer']
            for style in styles.values():
                for h in style.setdefault('header', [{}]):
                    h['show'] = False
            for t in styles['*'].setdefault('title', [{}]):
                t.update(show=True, bold=False, fontFamily='Segoe UI', fontSize=13)
            continue
        vi = doc.get('visual', {})
        if vi.get('visualType') != 'slicer':
            continue
        slicers += 1
        objects = vi.setdefault('objects', {})
        header = next((e['properties'] for e in objects.get('header', []) if not e.get('selector')), {})
        container = vi.setdefault('visualContainerObjects', {})
        title = props(container, 'title')
        fields = [pr.get('nativeQueryRef', '') for well in vi.get('query', {}).get('queryState', {}).values() for pr in well.get('projections', [])]
        label = value(title.get('text', {})) or value(header.get('text', {}))
        if not label:
            raw = fields[0] if fields else 'Filter'
            label = {'service_type': 'Service type', 'Dashboard Metric Selector': 'Dashboard metric',
                     'referral_id': 'Referral ID', 'Category': 'Framework category', 'date': 'Referral date',
                     'placement_urgency_band': 'Placement urgency band', 'person_search_label': 'Person',
                     'year_month': 'Month', 'Label': 'Period'}.get(raw, raw.replace('_', ' ').capitalize())
        title['text'] = literal("'" + label.replace("'", "''") + "'")
        # Theme owns header visibility and title typography, including on existing slicers.
        for e in objects.get('header', []):
            e.get('properties', {}).pop('show', None)
        for key in ('show', 'fontSize', 'fontFamily', 'bold', 'heading'):
            title.pop(key, None)

    plans = {
        '08ef33dc6a87d1b14392': (35, 1450, 36, 1644),
        '1f33996970651e846183': (26, 1480, 24, 1656),
        '58d36c775c032a42e01b': (36, 1473, 36, 1644),
        'ad5ab4aa6928c9178a35': (26, 1480, 24, 1656),
        'b95eb4c0b53cd8c60710': (36, 1467, 36, 1644),
    }
    moved = []
    for pid, (left, right, target_left, target_right) in plans.items():
        scale = (target_right-target_left)/(right-left)
        vs = {p: d for p, d in docs.items() if p.name == 'visual.json' and p.parents[2].name == pid}
        candidates = {p: d for p, d in vs.items() if not d.get('isHidden') and not d.get('parentGroupName') and not is_navigation(d)}
        large = [deepcopy(d['position']) for d in candidates.values() if d['position']['width'] > 100 and d.get('visual', {}).get('visualType') not in ('image', 'actionButton', 'textbox')]
        for p, d in candidates.items():
            old = deepcopy(d['position']); pos = d['position']
            pos['x'] = round(target_left + (old['x']-left)*scale, 2)
            fixed = old['width'] <= 60 or d.get('visual', {}).get('visualType') in ('image', 'actionButton')
            if fixed:
                parents = [q for q in large if q['x'] <= old['x'] and q['y'] <= old['y'] and q['x']+q['width'] >= old['x']+old['width'] and q['y']+q['height'] >= old['y']+old['height']]
                if parents:
                    q = min(parents, key=lambda q:q['width']*q['height'])
                    gap = q['x']+q['width']-old['x']-old['width']
                    if gap < 70:
                        pos['x'] = round(target_left+(q['x']+q['width']-left)*scale-gap-old['width'], 2)
            else:
                pos['width'] = round(old['width']*scale, 2)
            moved.append({'page': pid, 'visual': d['name'], 'before': old, 'after': deepcopy(pos)})

    # The home guide contains one explanatory block rather than a two-column grid.
    for p, d in docs.items():
        if p.name == 'visual.json' and p.parents[2].name == '09def13cccc062a04aa4' and d.get('visual', {}).get('visualType') == 'textbox' and d['position']['y'] >= 150:
            d['position']['width'] = 1644 - d['position']['x']

    # No query, filter state, ID, visibility or bookmark action changes are permitted.
    for p, before in original.items():
        after = docs[p]
        if p.name == 'visual.json':
            assert before['name'] == after['name']
            for key in ('query', 'filterConfig'):
                assert before.get('visual', {}).get(key) == after.get('visual', {}).get(key), (p, key)
            assert before.get('filterConfig') == after.get('filterConfig')
            assert before.get('isHidden') == after.get('isHidden')
            assert before.get('visual', {}).get('objects', {}).get('general') == after.get('visual', {}).get('objects', {}).get('general') or before.get('visual', {}).get('visualType') == 'textbox'
            if is_navigation(before):
                assert before['position'] == after['position'], p
        if p.name.endswith('.bookmark.json'):
            assert before['explorationState'] == after['explorationState'], p

    changed = {p: d for p, d in docs.items() if d != original[p]}
    backup = PROJECT.parent/'_review'/('filter-explorer-width-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
    for p in changed:
        target = backup/p.relative_to(PROJECT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, target)
    for p, doc in changed.items():
        p.write_text(json.dumps(doc, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    audit = []
    retired = {'4be6f15f15a086c98c33','f028a4be56d03e8404d7','dd3a58c056d723048dbf','7b4c90309550bd42911c'}
    for p, pg in docs.items():
        if p.name != 'page.json':
            continue
        pid = p.parent.name
        body = [d for q, d in docs.items() if q.name == 'visual.json' and q.parents[2].name == pid and not d.get('isHidden') and not d.get('parentGroupName') and not is_navigation(d)]
        end = max((d['position']['x']+d['position']['width'] for d in body), default=0)
        status = 'retired/archive preserved' if pid in retired else 'tooltip size preserved' if pg['width'] < 1000 else 'expanded' if pid in plans or pid == '09def13cccc062a04aa4' else 'already uses canvas width'
        if status not in ('retired/archive preserved','tooltip size preserved'):
            assert end >= pg['width']-60, (pg['displayName'], end)
        audit.append({'page':pg['displayName'], 'width':pg['width'], 'content_right':round(end,2),'result':status})
    result = {'backup':str(backup),'slicers_using_theme_header_visibility':slicers,'changed_files':len(changed), 'layout_changes':moved,'page_width_audit':audit,'desktop_render_verified':False,'semantic_model_modified':False,'cache_modified':False}
    manifest.write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('layout_changes','page_width_audit')},indent=2))
    print('Audited pages:',len(audit),'Repositioned/resized body visuals:',len(moved))


if __name__ == '__main__':
    main()
