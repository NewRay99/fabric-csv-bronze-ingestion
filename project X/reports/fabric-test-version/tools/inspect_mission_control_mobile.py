"""Print a compact page inventory to support phone layout authoring."""
import json
from pathlib import Path
import sys

root=Path(sys.argv[1])/'SM WMPP Mission Control.Report/definition/pages'
for page_id in json.loads((root/'pages.json').read_text(encoding='utf-8-sig'))['pageOrder']:
    page=json.loads((root/page_id/'page.json').read_text(encoding='utf-8-sig'))
    records=[]
    for path in (root/page_id/'visuals').glob('*/visual.json'):
        v=json.loads(path.read_text(encoding='utf-8-sig')); vis=v.get('visual',{}); kind=vis.get('visualType','group')
        words=' '.join(str(t.get('value','')) for o in vis.get('objects',{}).get('general',[]) for p in o.get('properties',{}).get('paragraphs',[]) for t in p.get('textRuns',[]))
        fields=[p.get('nativeQueryRef','') for q in vis.get('query',{}).get('queryState',{}).values() for p in q.get('projections',[])]
        text=[o.get('properties',{}).get('text',{}).get('expr',{}).get('Literal',{}).get('Value','') for o in vis.get('objects',{}).get('text',[])]
        r={'id':v['name'],'kind':kind,'hidden':v.get('isHidden',False),'box':[round(v['position'][k]) for k in ('x','y','width','height')], 'text':(words or ' / '.join(text) or ' / '.join(fields))[:180]}
        if kind.startswith('deneb'):
            raw=vis['objects']['vega'][0]['properties']['jsonSpec']['expr']['Literal']['Value']
            spec=json.loads(raw[1:-1].replace("''","'"))
            r['spec']={k:spec[k] for k in ('$schema','width','height','encoding') if k in spec}
        if kind != 'shape' or v['position']['width']>240:
            records.append(r)
    print(json.dumps({'id':page_id,'name':page['displayName'],'visuals':sorted(records,key=lambda r:(r['box'][1],r['box'][0]))},ensure_ascii=False))
