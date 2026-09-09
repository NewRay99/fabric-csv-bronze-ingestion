"""Parse Supplementary/02_01_As_Is_KPI.md into /tmp/kpi_rows.json.

Output: dict KPI-ID -> list of cells
[kpi, reqs, desc, reqdesc, tables, calc, pbi_measure, section]
Escaped markdown (\\[, \\], \\_) is unescaped. Duplicate KPI-40..52 rows are
deduped, preferring the later (fixed) occurrence on ties.
"""
import json
import re

SRC = "project X/client documentation/Supplementary/02_01_As_Is_KPI.md"

rows = {}
order = []
for line in open(SRC, encoding="utf-8"):
    if not line.startswith("| KPI-"):
        continue
    cells = re.split(r"(?<!\\)\|", line.rstrip("\n"))
    cells = cells[1:-1]  # drop leading/trailing empty from outer pipes
    cells = [c.strip() for c in cells]
    cells = [
        c.replace("\\[", "[").replace("\\]", "]").replace("\\_", "_")
        for c in cells
    ]
    kpi = cells[0]
    filled = len([c for c in cells if c])
    if kpi in rows:
        existing_filled = len([c for c in rows[kpi] if c])
        if existing_filled > filled:
            continue  # keep richer existing row
    rows[kpi] = cells
    if kpi not in order:
        order.append(kpi)

json.dump(rows, open("/tmp/kpi_rows.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

print("unique KPIs:", len(rows))
ids = sorted(int(k.split("-")[1]) for k in rows)
missing = [i for i in range(1, 118) if i not in ids]
print("missing 1..117:", missing)
weird = {k: len(v) for k, v in rows.items() if len(v) != 8}
print("rows without exactly 8 cells:", weird)
