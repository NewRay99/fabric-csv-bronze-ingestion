"""Verify saved layouts and prove non-phone definitions match the baseline ZIP."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import build_mission_control_mobile as mobile

parser=argparse.ArgumentParser()
parser.add_argument('--project-root',type=Path,required=True)
args=parser.parse_args();root=args.project_root
manifest=mobile.read(root/'Mission Control mobile layout revision.json')
plans={}
for page in manifest['pages']:
    for record in page['records']:
        path=root/'SM WMPP Mission Control.Report/definition/pages'/page['id']/'visuals'/record['id']/'mobile.json'
        value=mobile.read(path)
        assert value['position']==record['position'],('Saved phone position differs',path)
        plans[path]=value
qa=mobile.validate_plan(root,manifest['pages'],plans)
current=mobile.protected(root)
assert current==manifest['protected'],'Non-mobile files differ from the authoring baseline.'
with zipfile.ZipFile(manifest['backup']) as archive:
    for relative,digest in current.items():
        assert hashlib.sha256(archive.read(relative.replace('\\','/'))).hexdigest()==digest,('Non-mobile definition changed',relative)
qa.update(protectedFilesComparedToOriginalBackup=len(current),desktopReportUnchanged=True,semanticModelUnchanged=True,
          nativePhoneRenderVerified=False,nativePreviewCoverage='Native preview screenshots reviewed separately',sourceRefresh='None')
mobile.write(root/'Mission Control mobile layout validation.json',qa)
print(json.dumps(qa))
