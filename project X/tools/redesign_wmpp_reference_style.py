"""Reference-led WMPP page chrome + live native visuals; never fake KPI data.

Keeps page IDs, field bindings, local/client connections and models. SVG assets
contain only interface decoration, labels and icons, not charts or KPI values.
"""
from copy import deepcopy
import hashlib
import html
import json
from pathlib import Path
import shutil
import sys

import apply_wmpp_end_goal_design as d
import sync_wmpp_report_theme as shared

ROOT = d.ROOT
SOURCE = d.REPORT
LOCAL = ROOT / 'reports/current/SM WMPP v16 updated/SM_WMPP_v16.Report'
ARCHIVE = ROOT / 'reports/retired/2026-09-23-reference-design-revision'
ASSETS = SOURCE / 'StaticResources/RegisteredResources'
PALETTE = ['#FF5D43', '#FF8C42', '#FFB49F', '#FFDAD4', '#222222', '#45AEAF']
CORAL = PALETTE[0]
NEW_PRESET = 'WMPP Reference Clean'
L = d.ui.literal
fill = lambda color: {'solid': {'color': L(repr(color))}}
obj = lambda **props: [{'properties': props}]
read = shared.read
save = shared.save

ICONS = {
    'people': '<circle cx="9" cy="7" r="3"/><path d="M3 21v-4a6 6 0 0 1 12 0v4M17 8a3 3 0 0 1 0 6m1 2a5 5 0 0 1 3 5"/>',
    'document': '<path d="M6 3H3v18h12v-4M7 3h6l4 4v5M13 3v5h4M6 9h4M6 13h3"/><circle cx="15" cy="15" r="4"/><path d="m18 18 4 4"/>',
    'target': '<circle cx="11" cy="13" r="9"/><circle cx="11" cy="13" r="5"/><path d="m11 13 9-9m-1 0V1m1 3h3"/>',
    'alert': '<path d="M10 3a2 2 0 0 1 4 0l9 17H1Z"/><path d="M12 8v6m0 3v1"/>',
    'clock': '<circle cx="12" cy="12" r="10"/><path d="M12 5v8l4 2"/>',
    'pound': '<path d="M18 5C12-1 7 3 8 9l1 9-4 3h15M5 12h11"/>',
    'home': '<path d="m1 11 11-9 11 9M4 9v13h6v-8h4v8h6V9"/>',
    'trend': '<path d="m2 19 7-8 5 4 8-12m-7 0h7v7"/>',
    'calendar': '<rect x="2" y="4" width="20" height="18" rx="2"/><path d="M7 1v6m10-6v6M2 10h20M6 14h2m4 0h2m4 0h1M6 18h2m4 0h2"/>',
    'list': '<path d="M8 6h14M8 12h14M8 18h14M2 6h1M2 12h1M2 18h1"/>',
    'chart': '<path d="M2 22h21M4 20v-7h4v7m3 0V8h4v12m3 0V3h4v17"/>',
    'clipboard': '<rect x="4" y="3" width="16" height="20" rx="2"/><rect x="8" y="1" width="8" height="5" rx="2"/><path d="M8 11h8M8 16h8"/>',
    'pin': '<path d="M12 23S3 14 3 9a9 9 0 0 1 18 0c0 5-9 14-9 14Z"/><circle cx="12" cy="9" r="3"/>',
    'grid': '<rect x="2" y="2" width="7" height="7" rx="1"/><rect x="15" y="2" width="7" height="7" rx="1"/><rect x="2" y="15" width="7" height="7" rx="1"/><rect x="15" y="15" width="7" height="7" rx="1"/>',
}


def text(x, y, value, size=14, color='#161616', weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-family="Segoe UI,Arial,sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(value)}</text>'


def icon(name, x, y, size=30, color='#161616'):
    return f'<g transform="translate({x},{y}) scale({size/24})" fill="none" stroke="{color}" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'


def clean(label='', preset=True):
    v = {k: obj(show=L('false')) for k in ('background', 'border', 'dropShadow', 'title', 'subTitle', 'visualHeader')}
    v['padding'] = obj(top=L('0D'), bottom=L('0D'), left=L('0D'), right=L('0D'))
    v['general'] = obj(altText=L(repr(label)))
    if preset:
        v['stylePreset'] = obj(name=L(repr(NEW_PRESET)))
    return v


class Page:
    def __init__(self, key, title, score_y, rows, card_entries, panels, note):
        self.key, self.id = key, d.ident(key)
        self.path = SOURCE / 'definition/pages' / self.id
        self.data = read(self.path / 'page.json')
        self.data.update(width=1680, height=945, displayOption='FitToPage')
        self.data['objects'] = {'background': obj(color=fill('#FAFAFA'), transparency=L('0D'))}
        self.count, self.written, self.bookmarks = 1, set(), []
        self.svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1680" height="945" viewBox="0 0 1680 945">',
            '<defs><filter id="shadow" x="-15%" y="-25%" width="130%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#202124" flood-opacity=".10"/></filter></defs>',
            '<rect width="1680" height="945" fill="#FAFAFA"/>', icon('grid',28,29,42),
            text(96,55,'FOSTER PLACEMENT PERFORMANCE',28,weight=700), text(96,88,title,20,CORAL),
            text(96,112,'Data as of',12,'#666666')]
        self.svg.append('<rect x="1040" y="20" width="360" height="86" rx="14" fill="white" filter="url(#shadow)"/>')
        for i,(label,color) in enumerate(zip(['Critical','High','Medium','Planned'],PALETTE)):
            x=1059+i*84
            self.svg += [f'<circle cx="{x}" cy="91" r="5" fill="{color}"/>',text(x+11,95,label,10)]
        if key!='target':
            self.svg.append('<rect x="840" y="20" width="192" height="86" rx="14" fill="white" filter="url(#shadow)"/>')
        self.svg.append(f'<rect x="24" y="{score_y}" width="1632" height="116" rx="16" fill="white" filter="url(#shadow)"/>')
        for i,(measure,label,glyph,caption) in enumerate(card_entries):
            x = 24+i*272
            if i:
                self.svg.append(f'<path d="M{x} {score_y+23}v70" stroke="#D8D8D8"/>')
            self.svg += [f'<circle cx="{x+55}" cy="{score_y+52}" r="28" fill="white" stroke="#333333" stroke-width="1"/>',
                         icon(glyph,x+39,score_y+35,32),text(x+98,score_y+72,label,14,weight=600),
                         text(x+98,score_y+94,caption,11,'#666666')]
            if measure:
                self.card('kpi-'+str(i),measure,(x+98,score_y+16,164,42),24)
            else:
                self.text('kpi-'+str(i),'—',(x+98,score_y+18,164,40),28)
        for i,(dest,glyph) in enumerate([('board','chart'),('supply','people'),('target','clipboard')]):
            x=1428+i*78
            active=dest==key
            self.svg += [f'<circle cx="{x+31}" cy="56" r="31" fill="{CORAL if active else "white"}" filter="url(#shadow)"/>',
                         icon(glyph,x+16,41,30,'white' if active else '#161616')]
            self.button('nav-'+dest,(x,25,62,62),'PageNavigation',d.ident(dest),'Go to '+dest.title())
        self.card('subtitle','Current Referral As Of',(160,96,215,22),10,'dd MMM yyyy')
        if key!='target':
            self.slicer('period','dim_date','year_month','Referral created period',(850,27,172,68))
        self.slicer('urgency','fact_referral','placement_urgency_band','Placement urgency',(1056,26,328,51))
        self.text('notes',note,(36,909,1608,25),11,False,'#555555')
        self.panels=[]
        for i,panel in enumerate(panels):
            x=24+(i%3)*552; y,h=rows[i//3]; w=528
            self.panels.append((x,y,w,h))
            self.svg += [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="white" filter="url(#shadow)"/>',
                text(x+20,y+31,panel[1],18,weight=650),text(x+20,y+53,panel[2],12),
                f'<circle cx="{x+w-116}" cy="{y+25}" r="7" fill="none" stroke="#777777" stroke-width=".8"/>',
                text(x+w-117.7,y+29,'i',11,'#555555'),
                f'<path d="M{x+16} {y+66}h{w-32}" stroke="#CCCCCC" stroke-width="1"/>']
            self.panel(panel,(x+18,y+78,w-36,h-94),(x,y,w,h))
        if key=='target':
            self.svg += ['<rect x="24" y="847" width="1632" height="66" rx="16" fill="#FFF0EC"/>',
                '<circle cx="63" cy="880" r="26" fill="#FF5D43"/>',icon('target',47,864,32,'white'),
                text(106,886,'Required Placement Date is the core target.',18,weight=650)]
            for i,(label,color) in enumerate([('Critical ≤1 day',CORAL),('High ≤3 days','#FF8C42'),('Medium ≤7 days','#FFBB72'),('Planned >7 days','#FFDAD4')]):
                x=911+i*181
                self.svg += [f'<rect x="{x}" y="864" width="165" height="34" rx="6" fill="{color}"/>',text(x+12,887,label,15,'white' if i<2 else '#161616',600)]

    def put(self,key,v):
        name=d.ident(self.key+':'+key)
        v['name']=name; self.count+=1
        v['position'].update(z=self.count,tabOrder=self.count)
        self.written.add(name)
        save(self.path/'visuals'/name/'visual.json',v)
        return name

    def shell(self,kind,pos,label):
        v=d.ui.visual_shell('temporary',kind,d.ui.position(*pos,0))
        v['visual']['visualContainerObjects']=clean(label)
        return v

    def text(self,key,value,pos,size=14,bold=True,color='#161616'):
        v=d.ui.textbox('temporary',value,d.ui.position(*pos,0),size,bold)
        v['visual']['visualContainerObjects']=clean(value)
        v['visual']['objects']['general'][0]['properties']['paragraphs'][0]['textRuns'][0]['textStyle']['color']=color
        return self.put(key,v)

    def card(self,key,measure,pos,size=24,fmt=None):
        v=self.shell('cardVisual',pos,measure)
        projection=d.measure(measure)
        if fmt: projection['format']=fmt
        v['visual']['query']={'queryState':{'Data':{'projections':[projection]}}}
        default=lambda **props:[{'properties':props,'selector':{'id':'default'}}]
        v['visual']['objects']={'value':default(fontColor=fill('#111111'),fontSize=L(str(size)+'D'),
                fontFamily=L("'Segoe UI Semibold'"),bold=L('true'),horizontalAlignment=L("'left'"),textWrap=L('false')),
                'layout':obj(alignment=L("'top'"),autoGrid=L('true'),orientation=L('2D'),rowCount=L('1L'),columnCount=L('1L'),cellPadding=L('0L')),
                'padding':default(paddingUniform=L('0L'),paddingIndividual=L('true'),paddingSelection=L("'Custom'"),
                    leftMargin=L('0D'),rightMargin=L('0D'),topMargin=L('0D'),bottomMargin=L('0D')),
                'spacing':default(verticalSpacing=L('0L'))}
        v['visual']['objects']['layout']+=default(backgroundShow=L('false'),backgroundTransparency=L('100D'),
                borderWidth=L('0D'),borderTransparency=L('100D'),leftOuterMargin=L('0D'),rightOuterMargin=L('0D'),
                topOuterMargin=L('0D'),bottomOuterMargin=L('0D'),cellPadding=L('0D'))
        for group in ('label','fillCustom','outline','shadowCustom','accentBar','divider','image','cardImage','border'):
            v['visual']['objects'][group]=default(show=L('false'))
        return self.put(key,v)

    def slicer(self,key,table,column,title,pos):
        v=d.ui.slicer('temporary',table,column,title,d.ui.position(*pos,0))
        v['visual']['visualContainerObjects']=clean(title)
        v['visual']['objects']['data']=obj(mode=L("'Dropdown'"))
        v['visual']['objects']['header']=obj(show=L('true'),fontColor=fill('#111111'),textSize=L('11D'),fontFamily=L("'Segoe UI Semibold'"))
        v['visual']['objects']['items']=obj(fontColor=fill('#333333'),background=fill('#FFFFFF'),textSize=L('10D'))
        return self.put(key,v)

    def button(self,key,pos,kind,target,label):
        v=self.shell('actionButton',pos,label)
        props={'show':L('true'),'type':L(repr(kind)),'tooltip':L(repr(label))}
        props['bookmark' if kind=='Bookmark' else 'navigationSection']=L(repr(target))
        v['visual']['visualContainerObjects']['visualLink']=obj(**props)
        v['visual']['objects']={k:obj(show=L('false')) for k in ('fill','outline','icon','text','shadow','glow')}
        return self.put(key,v)

    def panel(self,config,pos,box):
        key,title,subtitle,kind,table,column,measures,*tail=config
        if kind=='unavailable':
            x,y,w,h=box
            self.svg += [icon('pin',x+w/2-22,y+112,44,'#B5B5B5'),
                text(x+95,y+189,'Region breakdown not yet available',17,'#666666',600),
                text(x+95,y+217,'A governed region field is needed.',13,'#777777')]
            # Reuse the old region visual ID, but with an accessible explanatory label.
            self.text(key,'No governed region values in the current model.',(x+54,y+h-40,w-108,22),11,False,'#777777')
            return
        x,y,w,h=box
        roles={'Category':[{**d.project(table,column),'active':True}], 'Y':[d.measure(m) for m in measures]}
        if kind=='pivotTable':
            roles={'Rows':[d.project(table,column)],'Columns':[d.project('Target Status','Label')], 'Values':[d.measure(measures[0])]}
        elif kind=='lineChart' and tail:
            roles['Series']=[d.project(*tail[0])]
        v=self.shell(kind,pos,title+' — '+subtitle)
        v['visual']['query']={'queryState':{r:{'projections':p} for r,p in roles.items()}}
        v['visual']['objects']={
            'labels':obj(show=L('true'),color=fill('#161616'),fontSize=L('11D'),labelDisplayUnits=L('0D')),
            'categoryAxis':obj(labelColor=fill('#222222'),fontSize=L('9D'),showAxisTitle=L('false'),gridlineShow=L('false')),
            'valueAxis':obj(labelColor=fill('#444444'),fontSize=L('9D'),showAxisTitle=L('false'),gridlineShow=L('false')),
            'legend':obj(show=L('true' if len(measures)>1 or kind in ('donutChart','lineChart') else 'false'),position=L("'Top'"),fontSize=L('9D'),labelColor=fill('#333333')),
            'dataPoint':obj(defaultColor=fill(CORAL),fillTransparency=L('0D'))}
        if table in ('Target Status','Days to Target','Open Referral Age'):
            colors=['#45AEAF','#FFB51B','#FF5D43','#DADADA'] if table=='Target Status' else ['#39AEA5','#FFB51B','#FF8C42','#FF5D43','#E94D3E','#DADADA']
            categories={'Target Status':['On Track','Due Soon','Overdue','No target'],
              'Days to Target':['0–1 days','2–3 days','4–7 days','8+ days','Overdue','No target'],
              'Open Referral Age':['0–2 days','3–7 days','8–14 days','15–28 days','29+ days','Unknown']}[table]
        elif column=='placement_urgency_band':
            categories=['Critical','High','Medium','Planned']; colors=PALETTE
        else: categories=[]; colors=PALETTE
        if not categories and len(measures)==1 and kind not in ('pivotTable','lineChart'):
            # Dynamic category gradients: works for actual provider/home names and
            # outcomes without inventing sample categories or adding DAX measures.
            low,high=('#FF5D43','#FFDAD4') if key=='response' else ('#FFDAD4','#FF5D43')
            rule={'FillRule':{'Input':d.measure(measures[0])['field'],
                'FillRule':{'linearGradient2':{'min':{'color':{'Literal':{'Value':repr(low)}}},
                 'max':{'color':{'Literal':{'Value':repr(high)}}}}}}}
            v['visual']['objects']['dataPoint'].append({'properties':{'fill':{'solid':{'color':{'expr':rule}}}},
                'selector':{'data':[{'dataViewWildcard':{'matchingOption':1}}]}})
        for cat,color in zip(categories,colors):
            identity={'Comparison':{'ComparisonKind':0,'Left':d.expression(table,column), 'Right':{'Literal':{'Value':repr(cat)}}}}
            v['visual']['objects']['dataPoint'].append({'properties':{'fill':fill(color)},'selector':{'data':[{'scopeId':identity}]}})
        if len(measures)>1:
            for m,color in zip(measures,[CORAL,'#222222','#45AEAF','#FFB51B','#FFDAD4']):
                v['visual']['objects']['dataPoint'].append({'properties':{'fill':fill(color)},'selector':{'metadata':d.measure(m)['queryRef']}})
        if kind=='pivotTable':
            v['visual']['objects']={'columnHeaders':obj(fontColor=fill('#222222'),backColor=fill('#FFFFFF'),fontSize=L('10D')),
                'rowHeaders':obj(fontColor=fill('#222222'),fontSize=L('10D')),
                'values':obj(fontColor=fill('#222222'),backColorPrimary=fill('#F5FAF8'),backColorSecondary=fill('#FFFFFF'),fontSize=L('10D')),
                'grid':obj(gridVertical=L('false'),gridHorizontal=L('true'),gridHorizontalColor=fill('#EEEEEE'),rowPadding=L('8D'))}
        if kind!='pivotTable':
            provider=table=='dim_provider'
            v['visual']['query']['sortDefinition']={'sort':[{'field':d.measure(measures[0])['field'] if provider else d.expression(table,column),
                'direction':'Descending' if provider and key!='response' else 'Ascending'}],'isDefaultSort':False}
        chart=self.put(key,v)
        table_v=self.shell('tableEx',pos,title+' — data table')
        table_v['isHidden']=True
        projections=[d.project(table,column)]+[d.measure(m) for m in measures]
        if kind=='pivotTable': projections.insert(1,d.project('Target Status','Label'))
        table_v['visual']['query']={'queryState':{'Values':{'projections':projections}}}
        table_v['visual']['objects']={'columnHeaders':obj(fontColor=fill('#222222'),backColor=fill('#FFF1EC'),fontSize=L('10D')),
                'values':obj(fontColor=fill('#222222'),backColorPrimary=fill('#FFFFFF'),backColorSecondary=fill('#FFF9F7'),fontSize=L('10D')),
                'grid':obj(gridVertical=L('false'),gridHorizontal=L('true'),rowPadding=L('7D'))}
        tab=self.put(key+'-table',table_v)
        for mode in ('chart','table'):
            bname=d.ident(self.key+':'+key+':'+mode)
            # PBIR has no "visible" mode; normal display is represented by an
            # absent display property, as in Desktop's existing saved bookmarks.
            states={chart:{'singleVisual':{'visualType':kind,'objects':{},**({'display':{'mode':'hidden'}} if mode!='chart' else {})}},
                    tab:{'singleVisual':{'visualType':'tableEx','objects':{},**({'display':{'mode':'hidden'}} if mode!='table' else {})}}}
            bm={'$schema':'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json',
                'name':bname,'displayName':self.key.title()+' / '+title+' / '+mode.title(),
                'options':{'applyOnlyToTargetVisuals':True,'targetVisualNames':[chart,tab],'suppressData':True,'suppressActiveSection':True},
                'explorationState':{'version':'1.3','activeSection':self.id,'sections':{self.id:{'visualContainers':states}}}}
            save(SOURCE/'definition/bookmarks'/f'{bname}.bookmark.json',bm);self.bookmarks.append(bname)
            bx=x+w-80 if mode=='chart' else x+w-38
            self.svg += [f'<circle cx="{bx}" cy="{y+28}" r="16" fill="{"#111111" if mode=="chart" else "#FFFFFF"}" filter="url(#shadow)"/>',
                         icon('chart' if mode=='chart' else 'list',bx-8,y+20,16,'white' if mode=='chart' else '#222222')]
            self.button(key+'-'+mode+'-button',(bx-18,y+10,36,36),'Bookmark',bname,'Show '+mode+' for '+title)

    def finish(self):
        svg=''.join(self.svg)+'</svg>'
        asset='wmpp-reference-'+self.key+'.svg'
        (ASSETS/asset).write_text(svg,encoding='utf-8')
        v=self.shell('image',(0,0,1680,945),'Reference-style page background; live values and charts are separate visuals')
        resource={'image':{'name':L(repr(asset)),'url':{'expr':{'ResourcePackageItem':{'PackageName':'RegisteredResources','PackageType':1,'ItemName':asset}}},'scaling':L("'Fit'")}}
        v['visual']['objects']={'image':obj(sourceFile=resource)}
        name=self.put('title',v)
        v['name']=name;v['position'].update(z=0,tabOrder=0)
        save(self.path/'visuals'/name/'visual.json',v)
        save(self.path/'page.json',self.data)
        existing={p.parent.name for p in (self.path/'visuals').glob('*/visual.json')}
        if existing-self.written:
            raise ValueError(f'Unexpected stale visuals; preserve/review before removal: {existing-self.written}')
        return asset,self.bookmarks


def build():
    d.NEW={name:None for name in d.semantic_fields(d.TABLES)['_Design Measures']}
    pages=[]
    pages.append(Page('board','Board Dashboard',140,[(276,300),(592,306)],[
        ('Total Referrals','Referrals Created','people','Selected referral-created cohort'),
        ('Open Referrals','Open Referrals','document','Current status within selection'),
        ('Placement Target Hit Rate','Placed by Target','target','IPA ≤ required placement date'),
        ('Critical Overdue Referrals','Critical Overdue','alert','Open critical referrals past target'),
        ('Median Days to IPA','Median Days to IPA','clock','Median time from referral creation'),
        ('Estimated Active Weekly Cost','Est. Weekly Cost','pound','Active weekly liability, not total cost')],[
        ('urgency','Referrals by Urgency Band','Number of referrals created by urgency','clusteredColumnChart','fact_referral','placement_urgency_band',['Total Referrals']),
        ('hit','Target Hit Rate by Urgency','% of placements with IPA on or before target','clusteredColumnChart','fact_referral','placement_urgency_band',['Placement Target Hit Rate']),
        ('status','Open Referrals by Target Status','Open referrals against required placement date','clusteredColumnChart','Target Status','Label',['Open Referrals by Target Status']),
        ('region','Referrals by Region','Region view awaits a governed source','unavailable',None,None,[]),
        ('outcomes','Referral Outcome Mix','Distribution of recorded referral status','donutChart','fact_referral','current_status',['Total Referrals']),
        ('provider','Provider Offers vs Accepted','Offers made and accepted by provider','clusteredColumnChart','dim_provider','provider_name',['Offers Submitted','Accepted Offers'])],
        'ⓘ Values reflect the selected cohort. Current state and accepted offers are not a same-month conversion. Missing source fields are never replaced with sample data.'))
    pages.append(Page('supply','Provider & Placement Supply',124,[(260,294),(572,310)],[
        ('Providers Who Made Offers','Providers Making Offers','people','Distinct providers with an offer'),
        ('Offers Submitted','Offers Received','document','Offers linked to selected referrals'),
        ('Offer Acceptance Rate','Offer Acceptance Rate','target','Accepted ÷ decided offers'),
        ('Average Offers per Referral','Avg Offers per Referral','trend','Referrals with at least one offer'),
        ('Homes Offered','Homes Offered','home','Distinct homes in offers'),
        ('Median Offered Weekly Cost','Median Weekly Cost','pound','Median estimated offered cost')],[
        ('offers','Offers by Provider','Total offers received by each provider','clusteredColumnChart','dim_provider','provider_name',['Offers Submitted']),
        ('accepted','Accepted Offers by Provider','Accepted offers for each provider','clusteredColumnChart','dim_provider','provider_name',['Accepted Offers']),
        ('response','Provider Response Time','Median days to first offer by provider','clusteredColumnChart','dim_provider','provider_name',['Provider Median Days to First Offer']),
        ('homes','Homes Offered by County','County distribution; governed regions unavailable','clusteredBarChart','dim_provider_home','county',['Homes Offered']),
        ('mix','Placement Type Mix','Distribution of distinct homes offered','donutChart','dim_placement_type','placement_type',['Homes Offered']),
        ('funnel','Offer to IPA Funnel','Evidenced stages only; review/shortlist unavailable','funnel','Offer Journey Stage','Label',['Offer Journey Count'])],
        'ⓘ Accepted offers and IPAs are shown separately from new referrals. Reviewed and shortlisted history is unavailable, so those stages remain blank.'))
    pages.append(Page('target','Target & Urgency Performance',120,[(256,272),(544,282)],[
        ('Referrals Due This As Of Month','Due This Month','calendar','Month of the source as-of date'),
        ('Open Referrals Due in 3 Days','Due in 3 Days','clock','Open referrals; today to +3 days'),
        ('Open Overdue Referrals','Overdue','alert','Required placement date has passed'),
        ('Critical Target Hit Rate','Critical Hit Rate','target','Critical placements with known target'),
        ('Average Days Early','Avg Days Early','trend','Successful placements only'),
        (None,'Escalated Cases','alert','Unavailable: no escalation history')],[
        ('due','Required Placement Date Trend','Target-due referrals by required month','clusteredColumnChart','dim_date','year_month',['Referrals Due in Reporting Period']),
        ('hit','Hit Rate by Urgency Over Time','Created-month cohort hit rate by urgency','lineChart','dim_date','year_month',['Placement Target Hit Rate'],('fact_referral','placement_urgency_band')),
        ('days','Open Referrals by Days to Target','Open referrals grouped by time to target','clusteredColumnChart','Days to Target','Label',['Open Referrals by Days to Target']),
        ('matrix','Urgency / Target Status Matrix','Open referrals by urgency and target status','pivotTable','fact_referral','placement_urgency_band',['Open Referrals by Target Status']),
        ('age','Ageing of Open Referrals','Distribution of open referrals by age','clusteredBarChart','Open Referral Age','Label',['Open Referrals by Age']),
        ('cohort','Cohort Placement Within Window','% placed within the completed observation window','clusteredColumnChart','Placement Window','Label',['Cohort Placement Within Window'])],
        'Only referrals old enough to complete an observation window enter its denominator. Urgency thresholds follow the implemented model, not unapproved sample targets.'))
    return [p.finish() for p in pages]


def main():
    if not ARCHIVE.exists():
        for label,folder in [('client-report',SOURCE),('local-report',LOCAL)]:
            for name in ('definition','StaticResources'):
                shutil.copytree(folder/name,ARCHIVE/label/name)
        shutil.copytree(ROOT/'reports/templates',ARCHIVE/'templates-before')
    result=build()
    report=read(SOURCE/'definition/report.json')
    package=next(p for p in report['resourcePackages'] if p['name']=='RegisteredResources')
    for asset,_ in result:
        package['items']=[i for i in package['items'] if i['name']!=asset]
        package['items'].append({'name':asset,'path':asset,'type':'Image'})
    # All headings/textboxes are explicitly borderless, independent of old presets.
    for path in (SOURCE/'definition/pages').rglob('visual.json'):
        v=read(path)
        if v.get('visual',{}).get('visualType')=='textbox':
            vco=v['visual'].setdefault('visualContainerObjects',{})
            for group in ('border','dropShadow','background'):
                vco[group]=obj(show=L('false'))
            save(path,v)
    bm=read(SOURCE/'definition/bookmarks/bookmarks.json')
    for _,names in result:
        for name in names:
            if not any(i.get('name')==name for i in bm['items']):bm['items'].append({'name':name})
    save(SOURCE/'definition/bookmarks/bookmarks.json',bm)
    save(SOURCE/'definition/report.json',report)
    metadata=read(SOURCE/'definition/pages/pages.json')
    first=[d.ident(k) for k in ('board','supply','target','snapshots')]
    metadata['pageOrder']=first+[pid for pid in metadata['pageOrder'] if pid not in first]
    metadata['activePageName']=first[0]
    save(SOURCE/'definition/pages/pages.json',metadata)
    theme=read(shared.THEME)
    clean_theme={g:[{'show':False}] for g in ('background','border','dropShadow','title','subTitle','visualHeader')}
    clean_theme['padding']=[{'top':0,'bottom':0,'left':0,'right':0}]
    for kind in ('card','cardVisual','image','textbox','actionButton','slicer','clusteredColumnChart','clusteredBarChart','donutChart','funnel','lineChart','pivotTable','tableEx'):
        theme['visualStyles'].setdefault(kind,{})[NEW_PRESET]=deepcopy(clean_theme)
    # Preserve all existing palette indices, but give new pages their own warm series defaults.
    for kind in ('clusteredColumnChart','clusteredBarChart','donutChart','funnel','lineChart'):
        theme['visualStyles'][kind][NEW_PRESET]['dataPoint']=[{'defaultColor':{'solid':{'color':CORAL}}}]
    card_style=theme['visualStyles']['cardVisual'][NEW_PRESET]
    card_style['layout']=[{'$id':'default','backgroundShow':False,'backgroundTransparency':100,
        'borderWidth':0,'borderTransparency':100,'leftOuterMargin':0,'rightOuterMargin':0,
        'topOuterMargin':0,'bottomOuterMargin':0,'cellPadding':0}]
    card_style['padding']=[{'$id':'default','paddingSelection':'Custom','paddingIndividual':True,
        'leftMargin':0,'rightMargin':0,'topMargin':0,'bottomMargin':0}]
    for group in ('label','fillCustom','outline','shadowCustom','accentBar','divider','image','cardImage'):
        card_style[group]=[{'$id':'default','show':False}]
    save(shared.THEME,theme)
    manifest=read(shared.MANIFEST)
    affected=(str(SOURCE.relative_to(ROOT)).replace('\\','/'),str(LOCAL.relative_to(ROOT)).replace('\\','/'))
    # New reference pages own their clean preset; do not reapply the retired boxed styles.
    for key in ('visuals','originalPresets'):
        manifest[key]={p:v for p,v in manifest[key].items() if not any(p.startswith(a+'/') and
            (any('/'+d.ident(k)+'/' in p for k in ('board','supply','target')) or
             read(ROOT/p).get('visual',{}).get('visualType')=='textbox') for a in affected)}
    # Mirror authored files, not the client's connection, identity or local cache.
    for directory in ('definition','StaticResources'):
        shutil.copytree(SOURCE/directory,LOCAL/directory,dirs_exist_ok=True)
    for p in list(manifest['safetyFingerprints']):
        if any(p.startswith(a+'/') for a in affected): del manifest['safetyFingerprints'][p]
    for folder in (SOURCE,LOCAL):
        for path in (folder/'definition').rglob('*.json'):
            relative=str(path.relative_to(ROOT)).replace('\\','/')
            spec=manifest['styles'].get(manifest['visuals'].get(relative))
            manifest['safetyFingerprints'][relative]=shared.invariant(read(path),spec,path.name=='report.json',manifest['originalPresets'].get(relative))
    note='Reference-led redesign: three pages rebuilt as icon score strips, borderless headers and native chart/table panels. Previous definitions/audit archived.'
    manifest['notes']=list(dict.fromkeys(manifest['notes']+[note]))
    save(shared.MANIFEST,manifest)
    shared.sync()
    print('Built three 1680x945 reference-style dashboards with live KPI cards, SVG interface chrome, 34 display-only bookmarks and local report parity.')


if __name__=='__main__':main()
