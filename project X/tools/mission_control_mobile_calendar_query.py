"""Prepare a read-only DAX query for all seven calendar layouts."""
import json
from pathlib import Path
import sys

root=Path(sys.argv[1])
manifest=json.loads((root/'Change and discovery calendar revision.json').read_text(encoding='utf-8-sig'))
pieces=[]
groups=[('803165f7d2f5aaccd8ac',['Calendar Day Runs','Calendar Day Failures','Calendar Day Other'])]
groups += [(p['pageId'],p['measures']) for p in manifest['pages']]
for pid,names in groups:
    projections=','.join('"v'+str(i)+'",['+name+']' for i,name in enumerate(names))
    grouped="SUMMARIZECOLUMNS('Load Calendar'[Date],'Load Calendar'[Weekday],FILTER(ALL('Load Calendar'[Date]),'Load Calendar'[Date]>=TODAY()-364 && 'Load Calendar'[Date]<=TODAY()),"+projections+')'
    values=['[v0]','[v1]','[v2]','0','0','0'] if pid==groups[0][0] else ['0','0','0','[v0]','[v1]','[v2]']
    aliases=['Jobs','Failures','Other','Changes','Discoveries','Critical']
    pieces.append('SELECTCOLUMNS('+grouped+',"Page","'+pid+'","Date",\'Load Calendar\'[Date],"Weekday",\'Load Calendar\'[Weekday],'+','.join('"'+alias+'",'+value for alias,value in zip(aliases,values))+')')
(root/'Mission Control mobile calendars.dax').write_text('EVALUATE UNION('+','.join(pieces)+')\n',encoding='utf-8')
