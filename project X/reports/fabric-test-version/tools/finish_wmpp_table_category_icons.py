"""Finish aggregated category cells and provider assignment context without rerunning setup."""
from add_wmpp_table_icons_provider_detail import *


def main():
    marker=PROJECT/'TABLE_CATEGORY_ICONS_PROVIDER_DETAIL.json'
    manifest=read(marker)
    types=parse_columns()
    # Add referral priority/status to the new provider assignment details.
    ap=DEFINITION/'pages'/DETAIL/'visuals'/ident('provider-detail:assignments')/'visual.json'
    assignment=read(ap)
    ps=assignment['visual']['query']['queryState']['Values']['projections']
    for c,label in [('priority','Priority'),('current_status','Referral status')]:
        pr=project('fact_referral',c);pr['displayName']=label
        if not any(x['queryRef']==pr['queryRef'] for x in ps):ps.insert(2,pr)
    save(ap,assignment)
    for p in (DEFINITION/'pages').glob('*/visuals/*/visual.json'):
        v=read(p);vi=v.get('visual',{})
        if vi.get('visualType')!='tableEx':continue
        values=vi.setdefault('objects',{}).setdefault('values',[]);changed=False
        for pr in vi.get('query',{}).get('queryState',{}).get('Values',{}).get('projections',[]):
            cf=pr.get('field',{}).get('Column') or pr.get('field',{}).get('Aggregation',{}).get('Expression',{}).get('Column')
            if not cf:continue
            t=cf['Expression']['SourceRef']['Entity'];c=cf['Property'];kind=category(t,c,types)
            if not kind:continue
            existing=next((e for e in values if e.get('selector',{}).get('metadata')==pr['queryRef'] and 'icon' in e.get('properties',{})),None)
            if existing is not None:
                replacement=icon_format(t,c,kind,pr['field'])
                if existing['properties']['icon']!=replacement:
                    existing['properties']['icon']=replacement;changed=True
                continue
            values.append({'properties':{'icon':icon_format(t,c,kind,pr['field'])},'selector':{'data':[{'dataViewWildcard':{'matchingOption':1}}],'metadata':pr['queryRef']}})
            manifest['coverage'].append({'page':p.parents[2].name,'visual':v['name'],'table':t,'column':c,'category':kind,'hidden_visual':bool(v.get('isHidden'))})
            changed=True
        if changed:save(p,v)
    manifest['category_field_instances']=len(manifest['coverage'])
    manifest['tables_formatted']=len({(x['page'],x['visual']) for x in manifest['coverage']})
    save(marker,manifest)
    print('Formatted category cells:',manifest['category_field_instances'],'in',manifest['tables_formatted'],'tables')


if __name__=='__main__':main()
