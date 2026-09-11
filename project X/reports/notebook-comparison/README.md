# Notebook conversion and client comparison — 11 September 2026

The 17 root notebooks in `project X` now have primary `.py` versions in Fabric
source format. Their business logic and run defaults are preserved from the
original `.ipynb` files. Those originals remain as migration references; future
edits and portable validation use `.py`. The supplied WMPP client snapshot has
not been modified.

Of the 17 originals, 15 have a corresponding client `notebook-content.py`:
**nine have identical decoded code, six differ, and two are absent**.
All matched Markdown cells are unchanged. See the [complete comparison](comparison.md)
for inventory, cell counts and links to diffs.

## Material differences

The following describes the client snapshot relative to the converted originals.
It does not assume either side should automatically replace the other.

| Notebook | Difference in client snapshot | Implication |
|---|---|---|
| [90_run_archive_pipeline](90_run_archive_pipeline.code.diff) | Timeout 9,200 versus 7,200 seconds; `PROCESS_ONLY = "2026-07"`, monitoring reset enabled, confirmation `RESET 2026-07`. Original defaults select the normal range with reset disabled. | Client defaults select a July replay with monitoring reset; they should be reviewed as run-specific settings. |
| [90_run_live_pipeline](90_run_live_pipeline.code.diff) | Timeout 2,200 versus 1,800 seconds. | Client allows longer child execution. |
| [02a_archive_silver](02a_archive_silver.code.diff) | Lacks the original guarded `RESET ALL` path, monitoring cleanup helpers and Silver/Gold object rebuild logic. | Original supports a full archive rebuild; client supports the single-month reset path. |
| [04_gold_model](04_gold_model.code.diff) | Uses `child_id` instead of `person_id` in the referral fact and snapshot, with different migration renames; retains PascalCase intermediate SQL aliases; contains a saved, nonblank `JOB_RUN_ID`; adds `signed_by_local_authority`, `signed_datetime_for_local_authority`, `signed_by_provider`, `signed_datetime_for_provider` to the IPA fact query. | There are schema and lineage differences as well as SQL alias changes. Reconcile with the consuming semantic model and source schema before merging. |
| [05_gold_dimensions](05_gold_dimensions.code.diff) | Omits provider-home and registered-manager contact numbers, `gold.dim_person` including `gender_clean`, and `gold.dim_offer_status` including labels and lifecycle flags. | Client code lacks these original reporting dimensions and fields. |
| [01a_cfg_schema_capture_archive](01a_cfg_schema_capture_archive.code.diff) | Omits two trailing CSV preview/display cells for the July audit file and provider submission documents. | The schema capture and SQL comparison cells match; the originals have two additional diagnostic reads. |

`00_setup_cfg` and `00_archive_load` are absent from the supplied snapshot,
although the archive runner references both. This establishes a gap in the
local snapshot; it does not establish their absence from the live workspace.

Client-only items are `Notebook 2.Notebook` and
`version 02 03/common_util.Notebook`. The client folder also contains standalone
`04_gold_model.ipynb` and `05_gold_dimensions.ipynb` files; the comparison uses
the corresponding `.Notebook/notebook-content.py` definitions as requested.

## Format and validation

Conversion preserves code, Markdown, cell order, parameters, `%run`, SQL magic
cells and dependency bindings. Execution outputs, widget data and editor/advisor
state are omitted. Original Spark/session configuration is retained in top-level
`# META` comments; all 15 matched client definitions omit `spark_compute`.
Fabric's treatment of these extra configuration keys has not been runtime-tested;
the retained timeout metadata alone is not evidence of an effective session timeout.

All 22 pre-existing portable validators passed before conversion and after being
updated to read `.py` through the shared Fabric parser. Additional tests cover
source parsing, parameter and SQL cells, omission of execution data, missing-source
failures and syntax/round-trip checks across every primary notebook. Spark/Delta
execution and Fabric import/deployment were not run.

Microsoft references: [Notebook source control and deployment](https://learn.microsoft.com/en-us/fabric/data-engineering/notebook-source-control-deployment)
and [Notebook definition](https://learn.microsoft.com/en-us/rest/api/fabric/articles/item-management/definitions/notebook-definition).

## Reproduce

From the repository root:

```powershell
python "project X/tools/fabric_notebooks.py" compare
python -m pytest
```

Diff direction is **minus = converted original; plus = client snapshot**.
The generated report separates raw source differences, decoded code, Markdown
and metadata. It compares local files only and does not contact Azure DevOps.
