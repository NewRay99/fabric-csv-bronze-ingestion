"""Package the prepared source project and matching Fabric notebooks, excluding caches."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import zipfile


PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT / 'reports/WIP/SM WMPP Mission Control'
NOTEBOOKS = ['00_setup_cfg.py', '99_common_library.py', '99_data_domain.py']
INSTRUCTIONS = '''DISCOVERY HISTORY AND LOAD TRENDS

Deployment order
1. Import the updated 00_setup_cfg, 99_common_library and 99_data_domain notebooks
   into the existing Fabric workspace, retaining the configured Lakehouse.
2. Run 00_setup_cfg once. It adds the history columns without deleting existing
   cfg_data_domain rows. The profiler also runs setup itself.
3. Run 99_data_domain. It records a standalone job when no parent JOB_RUN_ID is
   supplied and appends the entire completed discovery in one Delta transaction.
4. Open SM WMPP Mission Control.pbip from the included project folder and refresh
   the semantic model after the new Lakehouse columns are available. Existing
   connection permissions are required. Nothing has been published or refreshed
   against Fabric as part of this delivery.
5. Continue running 99_data_domain on the desired weekly notebook schedule.
   This delivery does not create or alter a schedule.

Domains & Reference
- Latest version remains the default. Select All retained versions to inspect
  the entire retained history; day, linked job, source and column filters apply.
- BASELINE is a first retained observation, not an invented historical change.
- ADDED / UNCHANGED / REMOVED compare each value with the last fully observed
  version of that column. Removed values remain recorded with Present in version
  set to false, while earlier snapshots retain their original values.
- EMPTY means the scan completed and found no eligible values. HIGH_CARDINALITY,
  SOURCE_MISSING and EXCLUDED are retained status records, never proof of value
  removal. Comparisons skip these incomplete/uncollected profiles.
- The existing 40-distinct-value limit and unsuitable-column exclusions remain.
- Old records already overwritten by earlier runs cannot be recovered. Existing
  retained rows serve as the initial comparison baseline.

Load Metrics & Control
- Delta columns compare rows read/written with the preceding retained load of the
  SAME layer, source kind, source object and target object. Live/archive histories
  are kept separate. The comparison also works while viewing a historical day.
- No prior load gives a blank delta. A zero prior count gives a blank percentage.
- The two SVG sparkline columns show up to 12 loads through the selected load.
  Each sparkline uses its own scale. No future loads enter historical trends.

Verification
- 416 Python/notebook tests and 158 subtests passed.
- The prepared load formulas were checked against 6,443 imported metric rows:
  50 independently checked previous-load comparisons and 100 valid sparklines.
- Domain formulas were checked with query-scoped future fields against the 611
  existing records; these remain a baseline with no fabricated additions/removals.
- Model definitions deserialize and report field/layout checks pass.
- Native rendering of the changed pages remains a post-reopen check after the
  new schema has been deployed. The open Desktop model and its cache were not
  changed. This source package omits local caches and machine settings.
'''


def main():
    stamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    target = ROOT.parent / ('SM WMPP Mission Control - history and load trends ' + stamp + '.zip')
    if target.exists():
        raise FileExistsError(target)
    (ROOT / 'DISCOVERY_HISTORY_DEPLOYMENT.txt').write_text(INSTRUCTIONS, encoding='utf-8')
    files = []
    for directory in [ROOT / 'SM WMPP Mission Control.Report',
                      ROOT / 'SM WMPP Mission Control.SemanticModel']:
        for path in directory.rglob('*'):
            if path.is_file() and '.pbi' not in path.relative_to(ROOT).parts:
                files.append((path, Path(ROOT.name) / path.relative_to(ROOT)))
    for path in [ROOT / 'SM WMPP Mission Control.pbip', ROOT / 'DISCOVERY_HISTORY_DEPLOYMENT.txt',
                 ROOT / 'Discovery history revision.json']:
        files.append((path, Path(ROOT.name) / path.name))
    files.extend((PROJECT / name, Path('Notebooks') / name) for name in NOTEBOOKS)
    with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as archive:
        for path, member in files:
            archive.write(path, str(member))
        archive.writestr('START HERE.txt', INSTRUCTIONS)
    result = {'package': str(target), 'files': len(files) + 1,
              'sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
              'includedNotebooks': NOTEBOOKS, 'cacheIncluded': False}
    (ROOT / 'Discovery history package.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
