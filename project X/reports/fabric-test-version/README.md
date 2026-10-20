# Fabric folder test version

Notebook content comes from the current project X numbered Python files.
The v16 ZIP supplies Fabric folder metadata and schedules where available.
New notebooks receive new logical IDs. Review IDs and schedules before deployment.

Run the Python/ETL checks from this folder:

```powershell
python -m pytest tests --ignore-glob=tests/test_wmpp_*.py
```

Power BI report tests require separate report artifacts and are excluded here.
These local checks do not execute Spark notebooks or certify Fabric deployment.
