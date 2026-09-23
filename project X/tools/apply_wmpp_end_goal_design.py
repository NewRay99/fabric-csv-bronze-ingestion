"""Add the three supplied design views and a selectable snapshot month window.

Only generated pages/support tables are written. Existing report pages and the
client connection remain intact. Open definition-local.pbir for local review;
the client semantic model needs the added tables/measures before deployment.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import rebuild_mission_control_dashboard_v16 as ui
from validate_wmpp_v16_enhancements import semantic_fields, field_pairs

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / 'reports/current/RPT WMPP v16/WMPP_DASHBOARD_v16.Report'
PAGES = REPORT / 'definition/pages'
MODEL = ROOT / 'reports/current/SM WMPP v16 updated/SM_WMPP_v16.SemanticModel/definition'
TABLES = MODEL / 'tables'
SUPPORT = '_Design Measures'
NEW = {}


def ident(label):
    return hashlib.sha1(('end-goal-v16:' + label).encode()).hexdigest()[:20]


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def expression(table, prop, kind='Column'):
    return {kind: {'Expression': {'SourceRef': {'Entity': table}}, 'Property': prop}}


def project(table, prop, kind='Column', label=None):
    return {'field': expression(table, prop, kind), 'queryRef': f'{table}.{prop}',
            'nativeQueryRef': label or prop, 'displayName': label or prop}


def measure(name, label=None):
    result = project(SUPPORT if name in NEW else '_Measures', name, 'Measure', label)
    if name in ('Placement Target Hit Rate', 'Offer Acceptance Rate'):
        result['format'] = '0.0%'
    elif name in ('Median Days to IPA', 'Average Offers per Referral'):
        result['format'] = '0.0'
    return result


def add_measure(name, dax, fmt='0', note=''):
    NEW[name] = (dax.strip(), fmt, note)


def support_table(name, rows):
    """Disconnected label/order table; ordinal doubles as numeric parameter."""
    values = ',\n'.join('\t\t\t    { ' + json.dumps(label) + ', ' + str(order) + ' }'
                        for label, order in rows)
    text = f'''table '{name}'
\tcolumn Label
\t\tdataType: string
\t\tsummarizeBy: none
\t\tsourceColumn: [Label]
\t\tsortByColumn: Ordinal

\tcolumn Ordinal
\t\tdataType: int64
\t\tsummarizeBy: none
\t\tsourceColumn: [Ordinal]

\tpartition '{name}' = calculated
\t\tmode: import
\t\tsource =
\t\t\tDATATABLE ( "Label", STRING, "Ordinal", INTEGER, {{
{values}
\t\t\t}} )
'''
    (TABLES / f'{name}.tmdl').write_text(text, encoding='utf-8')
    return name


def model_changes():
    tables = [support_table('Snapshot Window', [('Last 6 months', 6), ('Last 12 months', 12)]),
              support_table('Target Status', [('On Track', 1), ('Due Soon', 2), ('Overdue', 3), ('No target', 4)]),
              support_table('Days to Target', [('0–1 days', 1), ('2–3 days', 2), ('4–7 days', 3), ('8+ days', 4), ('Overdue', 5), ('No target', 6)]),
              support_table('Open Referral Age', [('0–2 days', 1), ('3–7 days', 2), ('8–14 days', 3), ('15–28 days', 4), ('29+ days', 5), ('Unknown', 6)]),
              support_table('Placement Window', [('Within 1 day', 1), ('Within 3 days', 3), ('Within 7 days', 7), ('Within 14 days', 14)]),
              support_table('Offer Journey Stage', [('Offers received', 1), ('Reviewed — unavailable', 2), ('Shortlisted — unavailable', 3), ('Accepted', 4), ('Accepted with IPA', 5)])]
    add_measure('Snapshot Window Months', "SELECTEDVALUE ( 'Snapshot Window'[Ordinal], 12 )")
    add_measure('Snapshot Window Anchor', "CALCULATE ( MAX ( 'fact_referral_snapshot'[snapshot_month_start] ), REMOVEFILTERS ( 'dim_snapshot_month' ) )", 'mmm yyyy')
    add_measure('Snapshot Month In Window', '''VAR anchor = [Snapshot Window Anchor]
VAR axis_month = MAX ( 'dim_snapshot_month'[month_start] )
VAR months = [Snapshot Window Months]
RETURN IF ( NOT ISBLANK ( anchor ) && NOT ISBLANK ( axis_month )
    && axis_month >= EDATE ( anchor, 1 - months ) && axis_month <= anchor, 1, 0 )''')
    add_measure('Current Referral As Of', "MAX ( 'fact_referral'[as_of_date] )", 'dd mmm yyyy')
    add_measure('Critical Overdue Referrals', '''CALCULATE ( [Open Overdue Referrals],
    KEEPFILTERS ( 'fact_referral'[placement_urgency_band] = "Critical" ) )''')
    add_measure('Critical Target Hit Rate', '''CALCULATE ( [Placement Target Hit Rate],
    KEEPFILTERS ( 'fact_referral'[placement_urgency_band] = "Critical" ) )''', '0.0%')
    add_measure('Referrals Due in Reporting Period', '''CALCULATE ( [Total Referrals],
    USERELATIONSHIP ( 'fact_referral'[required_placement_date], 'dim_date'[date] ),
    KEEPFILTERS ( NOT ISBLANK ( 'fact_referral'[required_placement_date] ) ) )''')
    add_measure('Referrals Due This As Of Month', '''VAR asof = [Current Referral As Of]
VAR first_day = DATE ( YEAR ( asof ), MONTH ( asof ), 1 )
RETURN IF ( NOT ISBLANK ( asof ), CALCULATE ( [Total Referrals], REMOVEFILTERS ( 'dim_date' ),
    KEEPFILTERS ( 'fact_referral'[required_placement_date] >= first_day ),
    KEEPFILTERS ( 'fact_referral'[required_placement_date] < EDATE ( first_day, 1 ) ) ) )''')
    add_measure('Open Referrals Due in 3 Days', '''COUNTROWS ( FILTER ( 'fact_referral',
    'fact_referral'[is_open] = TRUE () && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
    && NOT ISBLANK ( 'fact_referral'[as_of_date] )
    && INT ( 'fact_referral'[required_placement_date] ) >= INT ( 'fact_referral'[as_of_date] )
    && INT ( 'fact_referral'[required_placement_date] ) <= INT ( 'fact_referral'[as_of_date] ) + 3 ) )''')
    add_measure('Average Days Early', '''AVERAGEX ( FILTER ( 'fact_referral',
    NOT ISBLANK ( 'fact_referral'[ipa_issued_date] ) && NOT ISBLANK ( 'fact_referral'[required_placement_date] )
    && 'fact_referral'[placed_by_required_date] = TRUE () ),
    DATEDIFF ( 'fact_referral'[ipa_issued_date], 'fact_referral'[required_placement_date], DAY ) )''', '0.0')
    add_measure('Homes Offered', '''CALCULATE ( DISTINCTCOUNT ( 'fact_offer'[home_id] ),
    KEEPFILTERS ( FILTER ( 'fact_offer', NOT ISBLANK ( 'fact_offer'[home_id] ) && 'fact_offer'[home_id] <> "" ) ) )''')
    add_measure('Median Offered Weekly Cost', "MEDIAN ( 'fact_offer'[estimated_weekly_cost] )", '£#,0.00')
    add_measure('Provider Median Days to First Offer', '''VAR per_referral =
    ADDCOLUMNS ( VALUES ( 'fact_offer'[referral_id] ),
        "FirstOffer", CALCULATE ( MIN ( 'fact_offer'[offer_submitted_date] ) ),
        "Created", LOOKUPVALUE ( 'fact_referral'[referral_created_date], 'fact_referral'[referral_id], 'fact_offer'[referral_id] ) )
RETURN MEDIANX ( FILTER ( per_referral, NOT ISBLANK ( [Created] ) && NOT ISBLANK ( [FirstOffer] ) && [FirstOffer] >= [Created] ),
    DIVIDE ( DATEDIFF ( [Created], [FirstOffer], HOUR ), 24.0 ) )''', '0.0')
    add_measure('Open Referrals by Target Status', '''VAR band = SELECTEDVALUE ( 'Target Status'[Ordinal] )
RETURN COUNTROWS ( FILTER ( 'fact_referral',
    VAR target = 'fact_referral'[required_placement_date]
    VAR asof = 'fact_referral'[as_of_date]
    VAR days = INT ( target ) - INT ( asof )
    VAR bucket = SWITCH ( TRUE (), ISBLANK ( target ) || ISBLANK ( asof ), 4, days < 0, 3, days <= 3, 2, 1 )
    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )''')
    add_measure('Open Referrals by Days to Target', '''VAR band = SELECTEDVALUE ( 'Days to Target'[Ordinal] )
RETURN COUNTROWS ( FILTER ( 'fact_referral',
    VAR target = 'fact_referral'[required_placement_date]
    VAR asof = 'fact_referral'[as_of_date]
    VAR days = INT ( target ) - INT ( asof )
    VAR bucket = SWITCH ( TRUE (), ISBLANK ( target ) || ISBLANK ( asof ), 6, days < 0, 5, days <= 1, 1, days <= 3, 2, days <= 7, 3, 4 )
    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )''')
    add_measure('Open Referrals by Age', '''VAR band = SELECTEDVALUE ( 'Open Referral Age'[Ordinal] )
RETURN COUNTROWS ( FILTER ( 'fact_referral',
    VAR days = 'fact_referral'[days_open]
    VAR bucket = SWITCH ( TRUE (), ISBLANK ( days ) || days < 0, 6, days <= 2, 1, days <= 7, 2, days <= 14, 3, days <= 28, 4, 5 )
    RETURN 'fact_referral'[is_open] = TRUE () && ( ISBLANK ( band ) || bucket = band ) ) )''')
    add_measure('Cohort Placement Within Window', '''VAR days = SELECTEDVALUE ( 'Placement Window'[Ordinal] )
VAR eligible = FILTER ( 'fact_referral', NOT ISBLANK ( 'fact_referral'[referral_created_date] )
    && NOT ISBLANK ( 'fact_referral'[as_of_date] )
    && 'fact_referral'[referral_created_date] + days <= 'fact_referral'[as_of_date] )
VAR placed = FILTER ( eligible, NOT ISBLANK ( 'fact_referral'[ipa_issued_date] )
    && 'fact_referral'[ipa_issued_date] >= 'fact_referral'[referral_created_date]
    && 'fact_referral'[ipa_issued_date] <= 'fact_referral'[referral_created_date] + days )
RETURN IF ( NOT ISBLANK ( days ), DIVIDE ( COUNTROWS ( placed ), COUNTROWS ( eligible ) ) )''', '0.0%',
                'Only referrals old enough to complete each observation window enter its denominator.')
    add_measure('Offer Journey Count', '''SWITCH ( SELECTEDVALUE ( 'Offer Journey Stage'[Ordinal] ),
    1, [Offers Submitted], 2, BLANK (), 3, BLANK (), 4, [Accepted Offers], 5, [Accepted Offers With IPA] )''', '0',
                'Reviewed and shortlisted have no reliable event history; missing stages intentionally return BLANK.')
    # Add supporting measures in their own table, preserving canonical measure definitions.
    blocks = [f"table '{SUPPORT}'\n"]
    for name, (dax, fmt, note) in NEW.items():
        if note:
            blocks.append('\t/// ' + note + '\n')
        blocks.append(f"\tmeasure '{name}' = ```\n" + '\n'.join('\t\t\t' + line for line in dax.splitlines()) +
                      f"\n\t\t\t```\n\t\tformatString: {fmt}\n\t\tdisplayFolder: Design KPIs\n\n")
    blocks.append(f"\tpartition '{SUPPORT}' = m\n\t\tmode: import\n\t\tsource = #table ( type table [], {{}} )\n")
    (TABLES / f'{SUPPORT}.tmdl').write_text(''.join(blocks), encoding='utf-8')
    tables.append(SUPPORT)
    model_path = MODEL / 'model.tmdl'
    content = model_path.read_text(encoding='utf-8-sig')
    for table in tables:
        reference = f"ref table '{table}'"
        if reference not in content:
            content = content.rstrip() + '\n' + reference + '\n'
    model_path.write_text(content, encoding='utf-8')


class Page:
    def __init__(self, key, title, subtitle, height=1100):
        self.key, self.id, self.count = key, ident(key), 0
        self.path = PAGES / self.id
        self.data = ui.page_json(self.id, title, height, 1680)
        self.data['objects']['background'][0]['properties']['color'] = {'solid': {'color': ui.literal("'#F7F8FA'")}}
        self.text('title', title.upper(), (26, 18, 1000, 55), 28)
        self.text('subtitle', subtitle, (26, 78, 1628, 40), 13, False)

    def put(self, key, value):
        self.count += 1
        value['name'] = ident(self.key + ':' + key)
        value['position']['z'] = self.count
        value['position']['tabOrder'] = self.count
        save(self.path / 'visuals' / value['name'] / 'visual.json', value)
        return value['name']

    def text(self, key, text, pos, size=14, bold=True):
        return self.put(key, ui.textbox('temp', text, ui.position(*pos, 0), size, bold))

    def visual(self, key, kind, roles, title, pos, objects=None):
        v = ui.visual_shell('temp', kind, ui.position(*pos, 0))
        v['visual']['query'] = {'queryState': {role: {'projections': values} for role, values in roles.items()}}
        v['visual']['visualContainerObjects'] = ui.container_objects(title)
        v['visual']['objects'] = objects or {}
        return self.put(key, v)

    def card(self, key, name, label, pos):
        v = ui.card('temp', name, ui.position(*pos, 0))
        v.pop('filterConfig', None)
        v['visual']['query'] = {'queryState': {'Data': {'projections': [measure(name, label)]}}}
        v['visual']['objects']['value'][0]['properties']['fontColor'] = {'solid': {'color': ui.literal("'#202124'")}}
        v['visual']['objects']['label'][0]['properties']['fontSize'] = ui.literal('12D')
        return self.put(key, v)

    def slicer(self, key, table, prop, label, pos, default=None):
        v = ui.slicer('temp', table, prop, label, ui.position(*pos, 0))
        v['visual']['objects']['data'] = [{'properties': {'mode': ui.literal("'Dropdown'")}}]
        if default is not None:
            v['visual']['objects']['selection'][0]['properties']['singleSelect'] = ui.literal('true')
            v['visual']['objects']['selection'][0]['properties']['selectAllCheckboxEnabled'] = ui.literal('false')
            filt = {'Version': 2, 'From': [{'Name': 's', 'Entity': table, 'Type': 0}],
                    'Where': [{'Condition': {'In': {'Expressions': [{'Column': {'Expression': {'SourceRef': {'Source': 's'}}, 'Property': prop}}],
                                                  'Values': [[{'Literal': {'Value': "'" + default + "'"}}]]}}}]}
            v['visual']['objects']['general'] = [{'properties': {'filter': {'filter': filt}}}]
        return self.put(key, v)

    def chart(self, key, title, table, col, measures, pos, kind='clusteredColumnChart', series=None):
        roles = {'Category': [{**project(table, col), 'active': True}], 'Y': [measure(m) for m in measures]}
        if series:
            roles['Series'] = [project(*series)]
        objects = {'labels': [{'properties': {'show': ui.literal('true')}}],
                   'legend': [{'properties': {'position': ui.literal("'Bottom'")}}],
                   'dataPoint': [{'properties': {'defaultColor': {'solid': {'color': ui.literal("'#FC6547'")}}}}]}
        vid = self.visual(key, kind, roles, title, pos, objects)
        p = self.path / 'visuals' / vid / 'visual.json'
        v = json.loads(p.read_text(encoding='utf-8'))
        v['visual']['query']['sortDefinition'] = {'sort': [{'field': expression(table, col), 'direction': 'Ascending'}], 'isDefaultSort': True}
        save(p, v)
        return vid

    def finish(self):
        save(self.path / 'page.json', self.data)
        return self.id


def controls(page):
    page.slicer('period', 'dim_date', 'year_month', 'Referral created period', (1040, 15, 280, 60))
    page.slicer('urgency', 'fact_referral', 'placement_urgency_band', 'Urgency band', (1335, 15, 320, 60))


def cards(page, entries):
    for i, (name, label) in enumerate(entries):
        pos = (26 + i * 273, 128, 260, 125)
        if name:
            page.card('kpi-' + str(i), name, label, pos)
        else:
            page.text('kpi-' + str(i), label, pos, 17)


PANELS = [(26 + col * 552, 280 + row * 350, 530, 325) for row in range(2) for col in range(3)]


def board():
    p = Page('board', 'Board Dashboard', 'Referral cohort and current outcomes • Required Placement Date is the target • Select the reporting period above')
    controls(p)
    cards(p, [('Total Referrals', 'Referrals created'), ('Open Referrals', 'Open referrals'),
              ('Placement Target Hit Rate', 'Placed by target'), ('Critical Overdue Referrals', 'Critical overdue'),
              ('Median Days to IPA', 'Median days to IPA'), ('Estimated Active Weekly Cost', 'Est. active weekly cost')])
    p.chart('urgency', 'Referrals by urgency band', 'fact_referral', 'placement_urgency_band', ['Total Referrals'], PANELS[0])
    p.chart('hit', 'Target hit rate by urgency', 'fact_referral', 'placement_urgency_band', ['Placement Target Hit Rate'], PANELS[1])
    p.chart('status', 'Open referrals by target status', 'Target Status', 'Label', ['Open Referrals by Target Status'], PANELS[2])
    p.text('region', 'Referrals by region\n\nAwaiting a governed region source.\nCurrent Gold region values are null.', PANELS[3], 19)
    p.chart('outcomes', 'Referral outcome mix — recorded status', 'fact_referral', 'current_status', ['Total Referrals'], PANELS[4], 'donutChart')
    p.chart('provider', 'Provider offers vs accepted', 'dim_provider', 'provider_name', ['Offers Submitted', 'Accepted Offers'], PANELS[5])
    p.text('notes', 'Target rate: referrals with an IPA and a known target. Due soon: 0–3 days from the data as-of date. Cost is weekly liability, not a lifetime estimate.', (26, 985, 1628, 75), 13, False)
    return p.finish()


def supply():
    p = Page('supply', 'Provider & Placement Supply', 'Offers linked to the selected referral-created cohort • Distinct homes and provider performance')
    controls(p)
    cards(p, [('Providers Who Made Offers', 'Providers making offers'), ('Offers Submitted', 'Offers received'),
              ('Offer Acceptance Rate', 'Offer acceptance rate'), ('Average Offers per Referral', 'Avg offers / referral with offer'),
              ('Homes Offered', 'Homes offered'), ('Median Offered Weekly Cost', 'Median offered weekly cost')])
    p.chart('offers', 'Offers by provider', 'dim_provider', 'provider_name', ['Offers Submitted'], PANELS[0])
    p.chart('accepted', 'Accepted offers by provider', 'dim_provider', 'provider_name', ['Accepted Offers'], PANELS[1])
    p.chart('response', 'Median days to first offer by provider', 'dim_provider', 'provider_name', ['Provider Median Days to First Offer'], PANELS[2])
    p.chart('homes', 'Homes offered by county (region unavailable)', 'dim_provider_home', 'county', ['Homes Offered'], PANELS[3], 'clusteredBarChart')
    p.chart('mix', 'Homes offered by placement type', 'dim_placement_type', 'placement_type', ['Homes Offered'], PANELS[4], 'donutChart')
    p.chart('funnel', 'Offer to IPA — evidenced stages', 'Offer Journey Stage', 'Label', ['Offer Journey Count'], PANELS[5], 'funnel')
    p.text('notes', 'Reviewed / shortlisted stages are unavailable: last-modified date is not review evidence. Accepted-with-IPA counts offers linked to an IPA. Acceptance rate uses decided offers.', (26, 985, 1628, 75), 13, False)
    return p.finish()


def target():
    p = Page('target', 'Target & Urgency Performance', 'Open referral triage at the source as-of date • Trend uses required placement month • Cohort window uses days from referral creation')
    # No created-period slicer: it would obscure the target-date trend.
    p.slicer('urgency', 'fact_referral', 'placement_urgency_band', 'Urgency band', (1335, 15, 320, 60))
    cards(p, [('Referrals Due This As Of Month', 'Due this month (data as-of)'), ('Open Referrals Due in 3 Days', 'Due within 3 days'),
              ('Open Overdue Referrals', 'Overdue'), ('Critical Target Hit Rate', 'Critical hit rate'),
              ('Average Days Early', 'Avg days early — successful'), (None, 'Escalated cases\nUnavailable: no escalation history')])
    p.chart('due', 'Required placement date trend', 'dim_date', 'year_month', ['Referrals Due in Reporting Period'], PANELS[0])
    p.chart('hit', 'Created-month cohort hit rate by urgency', 'dim_date', 'year_month', ['Placement Target Hit Rate'], PANELS[1], 'lineChart', ('fact_referral', 'placement_urgency_band'))
    p.chart('days', 'Open referrals by days to target', 'Days to Target', 'Label', ['Open Referrals by Days to Target'], PANELS[2])
    p.visual('matrix', 'pivotTable', {'Rows': [project('fact_referral', 'placement_urgency_band')],
             'Columns': [project('Target Status', 'Label')], 'Values': [measure('Open Referrals by Target Status')]},
             'Urgency / target-status matrix', PANELS[3])
    p.chart('age', 'Ageing of open referrals', 'Open Referral Age', 'Label', ['Open Referrals by Age'], PANELS[4], 'clusteredBarChart')
    p.chart('cohort', 'Cohort placement within observation window', 'Placement Window', 'Label', ['Cohort Placement Within Window'], PANELS[5])
    p.text('notes', 'Urgency from creation-to-required-date: Critical ≤1 day • High ≤3 • Medium ≤7 • Planned >7. Cohort rates exclude referrals too recent to complete each window.', (26, 985, 1628, 75), 13, False)
    return p.finish()


def snapshots():
    p = Page('snapshots', 'Referral Snapshots', 'Monthly retained referral state • Window ends at the latest available snapshot • Missing months remain gaps', 1000)
    window = p.slicer('window', 'Snapshot Window', 'Label', 'X-axis window', (1080, 15, 270, 60), 'Last 12 months')
    p.slicer('placement', 'dim_placement_type', 'placement_type', 'Placement type', (1370, 15, 285, 60))
    p.card('anchor', 'Snapshot Window Anchor', 'Latest snapshot month', (26, 130, 330, 105))
    p.text('help', 'Choose Last 6 months or Last 12 months to change the chart and detail-table month axis. Each point is a month-end state, not a sum of current referrals.', (390, 142, 1260, 80), 15, False)
    trend = p.chart('trend', 'Referral snapshot trend', 'dim_snapshot_month', 'month_start',
                    ['Snapshot Referrals', 'Open Referrals at Snapshot', 'Active Referrals Awaiting Offers at Snapshot',
                     'Active Referrals Under Offer at Snapshot', 'Closed or Cancelled Referrals at Snapshot'],
                    (26, 260, 1628, 400), 'lineChart')
    detail = p.visual('detail', 'tableEx', {'Values': [project('dim_snapshot_month', 'month_start')] +
                       [measure(m) for m in ['Snapshot Referrals', 'Open Referrals at Snapshot',
                        'Referrals with IPA at Snapshot', 'Open Overdue Referrals at Snapshot']]},
                      'Snapshot detail by month', (26, 680, 1628, 280))
    for vid in (trend, detail):
        path = p.path / 'visuals' / vid / 'visual.json'
        v = json.loads(path.read_text(encoding='utf-8'))
        v['filterConfig'] = {'filters': [{'name': ident('window-filter-' + vid),
            'field': expression(SUPPORT, 'Snapshot Month In Window', 'Measure'), 'type': 'Advanced',
            'filter': {'Version': 2, 'From': [{'Name': 'm', 'Entity': SUPPORT, 'Type': 0}],
                'Where': [{'Condition': {'Comparison': {'ComparisonKind': 0,
                    'Left': {'Measure': {'Expression': {'SourceRef': {'Source': 'm'}}, 'Property': 'Snapshot Month In Window'}},
                    'Right': {'Literal': {'Value': '1L'}}}}}]}, 'howCreated': 'User'}]}
        if vid == trend:
            v['visual']['objects']['categoryAxis'] = [{'properties': {'axisType': ui.literal("'Categorical'")}}]
        v['visual']['query']['sortDefinition'] = {'sort': [{'field': expression('dim_snapshot_month', 'month_start'), 'direction': 'Ascending'}], 'isDefaultSort': True}
        save(path, v)
    p.data['visualInteractions'] = [{'source': window, 'target': vid, 'type': 'DataFilter'} for vid in (trend, detail)]
    return p.finish()


def validate(page_ids):
    fields = semantic_fields(TABLES)
    errors = []
    for path in (REPORT / 'definition').rglob('*.json'):
        data = json.loads(path.read_text(encoding='utf-8-sig'))
        for entity, prop in field_pairs(data):
            if entity not in fields or prop not in fields[entity]:
                errors.append(f'{path.name}: {entity}[{prop}]')
    assert not errors, errors
    for pid in page_ids:
        page = json.loads((PAGES / pid / 'page.json').read_text(encoding='utf-8'))
        boxes = []
        for path in (PAGES / pid / 'visuals').glob('*/visual.json'):
            v = json.loads(path.read_text(encoding='utf-8'))
            box = v['position']
            assert 0 <= box['x'] and 0 <= box['y']
            assert box['x'] + box['width'] <= page['width'] and box['y'] + box['height'] <= page['height']
            for other in boxes:
                assert (box['x'] >= other['x'] + other['width'] or other['x'] >= box['x'] + box['width']
                        or box['y'] >= other['y'] + other['height'] or other['y'] >= box['y'] + box['height']), (pid, box, other)
            boxes.append(box)
    print(json.dumps({'status': 'PASS', 'newPages': page_ids, 'supportMeasures': len(NEW), 'unresolvedFields': 0}, indent=2))


def main():
    model_changes()
    if (REPORT / 'StaticResources/RegisteredResources/wmpp-reference-board.svg').exists():
        # The reference-led layout uses deliberate backdrop/content overlays.
        # Do not regenerate the retired boxed layout or its non-overlap check.
        import redesign_wmpp_reference_style
        redesign_wmpp_reference_style.main()
        return
    pages = [board(), supply(), target(), snapshots()]
    meta = json.loads((PAGES / 'pages.json').read_text(encoding='utf-8-sig'))
    meta['pageOrder'] = [pid for pid in meta['pageOrder'] if pid not in pages]
    meta['pageOrder'][1:1] = pages
    meta['activePageName'] = pages[0]
    save(PAGES / 'pages.json', meta)
    validate(pages)


if __name__ == '__main__':
    main()
