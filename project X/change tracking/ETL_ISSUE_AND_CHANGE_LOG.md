# Archive loader issue and regression log

This file records resolved defects in `00_archive_load.ipynb`. Before
publishing future changes, run:

```text
python validate_archive_load.py
```

Fabric runtime behaviour must also be confirmed in a development Lakehouse.

## AR-001 — Only one archive batch processed

- **Symptom:** later dated ZIP/file batches were not attempted after a failure.
- **Cause:** processing could stop at the first batch error.
- **Fix:** `STOP_ON_FIRST_ERROR = False` is the default; failures are collected
  and raised after remaining selected batches are attempted.
- **Regression guard:** validator checks both ZIP and file error paths continue.

## AR-002 — Archive loading coupled to ZIP extraction

- **Symptom:** a file copied directly into the archive folder was absent from
  the load queue when no corresponding ZIP was processed in that run.
- **Cause:** the file queue was derived from the current ZIP batch list.
- **Fix:** ZIP extraction and archive inventory are independent. Every run scans
  `ARCHIVE_FILE_ROOT` and builds a new archive inventory dataframe.
- **Regression guard:** validator rejects any file loop derived from
  `zip_batches`.

## AR-003 — One audit query executed per archive file

- **Symptom:** archive preparation was slow and generated many small Spark jobs.
- **Cause:** `monitoring.cfg_archive_file_load` was queried inside the file loop.
- **Fix:** the complete inventory is filtered with one dataframe `left_anti`
  join against the latest audit state.
- **Regression guard:** validator requires `filter_pending_archive_files()` and
  prohibits `audit_record()` in the archive file loop.

## AR-004 — Export date source was ambiguous

- **Symptom:** manually added files or date-named audit files could receive the
  wrong snapshot date.
- **Cause:** filename/ZIP parsing was mixed with folder-date parsing.
- **Fix:** the containing `YYYY-MM-DD` archive folder is authoritative for
  `export_date`. A date-named audit CSV separately receives `audit_file_date`
  from its filename.
- **Regression guard:** validator requires folder-derived export dates and both
  audit date fields.

## AR-005 — Archive file reruns could duplicate target rows

- **Symptom:** replaying a file could append a second copy of its full export.
- **Cause:** prior target rows were not always removed before append.
- **Fix:** a pending file first deletes rows by `_archive_source_path`; legacy
  targets fall back to deleting the matching `export_date`. All file rows are
  then appended without deduplication or ordering requirements.
- **Regression guard:** validator checks both replacement predicates and the
  full-file append path.

## AR-006 — Legacy archived_audit rejected for missing lineage

- **Symptom:** audit files failed with `archived.archived_audit has neither
  export_date nor source-file lineage`.
- **Cause:** the existing audit table pre-dated loader-managed metadata, while
  delete-before-append required that metadata before the incoming frame could
  add it.
- **Fix:** before replacement, the loader adds any missing nullable columns:
  `audit_file_date`, `export_date`, `_archive_source_path`,
  `_archive_source_zip`, `_archive_run_id`, and `_archive_load_ts`. Historical
  rows remain unchanged with null metadata. New audit rows receive folder and
  filename dates plus source lineage, making subsequent reruns safe.
- **Regression guard:** validator requires the legacy audit schema upgrade to
  execute before Delta replacement logic.

## AR-007 — Archive metric schema mismatch marked loaded files failed

- **Symptom:** after archive rows were written, Delta reported that
  `monitoring.cfg_table_load_metric` contained `null_primary_key_count` while
  the archive writer supplied `rejected_row_count`. The file was then recorded
  as `FAILED` even though its archive rows had already been committed.
- **Cause:** the archive notebook used a private metric schema that differed
  from the shared setup/Silver monitoring contract, and metric logging was
  inside the file-load failure boundary.
- **Fix:** archive metrics now use canonical `null_primary_key_count` and supply
  `None` because archive ingestion does not calculate that measure. Metric
  writes have dedicated error handling; failures are retained as pipeline
  warnings without changing a successfully loaded file audit to `FAILED`.
- **Regression guard:** validator prohibits `rejected_row_count`, requires the
  canonical metric schema, and requires non-fatal metric exception handling.

### CFG table inspection and migration script

For the reported AR-007 error, the live CFG table already contained the correct
`null_primary_key_count` field. Only the archive notebook writer was wrong, so
the CFG table did not require alteration.

Run this Fabric/PySpark cell when deploying to another environment. It reports
the current position and adds the canonical field only when it is genuinely
missing and no conflicting legacy field exists:

```python
METRIC_TABLE = "monitoring.cfg_table_load_metric"

metric_columns = {
    column.name.lower(): column.dataType.simpleString()
    for column in spark.table(METRIC_TABLE).schema.fields
}
print(f"Current {METRIC_TABLE} columns: {metric_columns}")

has_canonical = "null_primary_key_count" in metric_columns
has_legacy = "rejected_row_count" in metric_columns

if has_canonical and not has_legacy:
    print("CFG metric schema is already canonical; no change required.")
elif not has_canonical and not has_legacy:
    spark.sql(f"""
        ALTER TABLE {METRIC_TABLE}
        ADD COLUMNS (null_primary_key_count BIGINT)
    """)
    print("Added null_primary_key_count BIGINT.")
else:
    print(
        "Legacy rejected_row_count is present. Use the controlled rebuild "
        "below so the table does not retain both competing columns."
    )
```

If an older environment contains `rejected_row_count`, use this controlled
rebuild. It first creates a timestamped backup, then recreates the original
table with the canonical schema. Review the backup before deleting it:

```python
from datetime import datetime
from pyspark.sql import functions as F

METRIC_TABLE = "monitoring.cfg_table_load_metric"
backup_suffix = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
BACKUP_TABLE = (
    f"monitoring.cfg_table_load_metric_backup_{backup_suffix}"
)

source_df = spark.table(METRIC_TABLE)
source_columns = {name.lower() for name in source_df.columns}

if "rejected_row_count" not in source_columns:
    print("No rejected_row_count column exists; controlled rebuild skipped.")
else:
    (
        source_df.write.format("delta")
        .mode("errorifexists")
        .saveAsTable(BACKUP_TABLE)
    )

    canonical_value = (
        F.coalesce(
            F.col("null_primary_key_count").cast("long"),
            F.col("rejected_row_count").cast("long"),
        )
        if "null_primary_key_count" in source_columns
        else F.col("rejected_row_count").cast("long")
    )

    canonical_df = spark.table(BACKUP_TABLE).select(
        "run_id",
        "layer",
        "source_kind",
        "source_object",
        "target_object",
        F.col("rows_read").cast("long").alias("rows_read"),
        F.col("rows_written").cast("long").alias("rows_written"),
        F.col("duplicate_key_count").cast("long").alias(
            "duplicate_key_count"
        ),
        canonical_value.alias("null_primary_key_count"),
        F.col("recorded_at").cast("timestamp").alias("recorded_at"),
    )

    (
        canonical_df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(METRIC_TABLE)
    )
    print(
        f"Rebuilt {METRIC_TABLE} with the canonical schema. "
        f"Backup retained as {BACKUP_TABLE}."
    )
```

Do not solve AR-007 by enabling automatic schema merging. That would preserve
both metric columns and reintroduce inconsistent writers.

## AR-008 — Archive audit files made general archive runs too slow

- **Symptom:** the large number of date-named audit CSV files made the archive
  notebook take too long when the immediate requirement was to load business
  archive tables.
- **Cause:** audit files entered the same monitoring join and full
  read/count/delete/write path as every other archive file.
- **Fix:** the top-level `LOAD_ARCHIVE_AUDIT` control defaults to `False`.
  Archive inventory rows targeting `archived.archived_audit` are removed at the
  inventory seam before CFG filtering or file processing. Set the control to
  `True` for a dedicated audit catch-up run.
- **Audit behaviour:** skipped audit files are not recorded as successful and
  their existing `monitoring.cfg_archive_file_load` state is not changed.
- **Regression guard:** validator checks filename classification, the default
  toggle value, and that filtering happens before the archive audit-state join.

## AR-009 — Delta could not merge legacy export_date types

- **Symptom:** archive files failed with `[DELTA_FAILED_TO_MERGE_FIELDS] Failed
  to merge fields 'export_date' and 'export_date'` after the legacy target slice
  had already been deleted.
- **Cause:** incoming rows correctly used folder-derived Spark `TIMESTAMP`, but
  some existing `archived.*` Delta tables stored the same column as `STRING`,
  `DATE`, or `TIMESTAMP_NTZ`. Delta `mergeSchema` cannot change an existing
  column's datatype.
- **Fix:** before any source-path or export-date deletion, the loader inspects
  the existing target. A noncanonical `export_date` is converted to `TIMESTAMP`
  in a staging Delta table. Conversion values, row count and staged datatype are
  validated before the original target is atomically overwritten. A failed
  migration retains its staging table for investigation and leaves file-level
  replacement unstarted.
- **Contract decision:** folder-derived `export_date` is the sole archive
  contract field. Any CSV field with the same name is overwritten and no
  `_source_export_date` field is retained.
- **Recovery:** affected CFG file rows remain `FAILED` and are selected on the
  next run. The loader migrates their targets, removes any prior source/date
  slice, and reloads the complete source files.
- **Regression guard:** validator requires migration to run before Delta delete,
  requires `TIMESTAMP` staging and invalid-value checks, and prohibits
  `_source_export_date`.

## AR-010 — Migrated target and incoming timestamp variants could still differ

- **Symptom:** `DELTA_FAILED_TO_MERGE_FIELDS` could still be raised after target
  migration, and only after the existing source/date slice had been deleted.
- **Cause:** the target migration validated the target table in isolation but
  did not re-read its exact Spark datatype and align the incoming dataframe to
  it. `TIMESTAMP` and `TIMESTAMP_NTZ`, or duplicate case-insensitive field names,
  can still fail Delta schema merging even when displayed date values match.
- **Fix:** after migration, `align_frame_export_date_to_target()` requires one
  case-insensitive `export_date`, casts it to the target field's exact Spark
  datatype, verifies equality, and returns the aligned dataframe. This safety
  gate runs before `DeltaTable.delete()`.
- **Regression guard:** validator requires alignment and type verification to
  occur before the first file-level Delta deletion.

### Bronze-to-Silver decision

`02_silver_formatter.ipynb` does not require archive-style target
migration. It casts all fields from `schema_definition.csv` and performs an
atomic full overwrite with `overwriteSchema = true`, rather than deleting a
slice and appending. It now calls `validate_silver_export_date()` before the
overwrite to require exactly one non-null `TIMESTAMP` export field. Missing
table contracts continue to be logged and skipped.

## Operational reminders

- New files under `ARCHIVE_FILE_ROOT/YYYY-MM-DD/...` are automatically pending.
- A file already recorded as `SUCCESS` is skipped unless `reload = true`.
- Overwriting a file at the same path therefore requires setting its audit row's
  reload flag.
- Keep `PROCESS_EXPORT_DATE` blank to discover every archive date, or set it to
  the exact folder date being replayed.
- Keep `LOAD_ARCHIVE_AUDIT = False` for normal business archive runs. Set it to
  `True` only when `archived.archived_audit` should be loaded or caught up.

## SI-001 — Internal `ref_*` tables failed latest-to-Silver formatting

- **Symptom:** `02_silver_formatter.ipynb` failed on
  `bronze.ref_KPI_Definition`, `bronze.ref_KPI_RID_linkage`,
  `bronze.ref_RID`, and `bronze.ref_Table_Lineage` because they do not contain
  `export_date`.
- **Cause:** table discovery treated every physical Bronze table as a dated
  source extract before checking whether it was an internal/reference table.
- **Fix:** `common_util.ipynb` now owns the explicit exclusions and the `ref_`
  prefix rule. Latest ingestion, archive ingestion, live/archive schema capture,
  latest Silver, and archive Silver apply the shared predicate at their table or
  file discovery boundaries.
- **Behaviour:** excluded tables are reported once and are not audited as failed,
  loaded to Silver, or reported as source-schema drift.
- **Regression guard:** run `python validate_ref_exclusions.py`.



## SI-002 — Configuration setup was distributed across parent ETL notebooks

- **Symptom:** ETL notebooks could fail when a required `monitoring.cfg_*`
  table had not already been created, and table definitions were duplicated
  between setup, archive ingestion, schema capture, data quality, and Gold.
- **Cause:** `00_setup_cfg.ipynb` created only part of the configuration
  catalogue; several parent notebooks still owned their own config DDL.
- **Fix:** `00_setup_cfg.ipynb` now owns an idempotent registry of all 18
  configuration tables, adds missing columns to older deployments, and seeds
  `gold.cfg_placement_urgency_rule`. Every ETL/control notebook invokes setup
  before its first configuration operation; duplicate child DDL was removed.
- **Validation:** `validate_cfg_setup.py` checks ownership, setup-call
  order, required table coverage, and notebook Python syntax.


## SI-003 — Archive Silver baseline omitted the shared `ref_*` exclusion

- **Symptom:** after promoting the current version 02 04 baseline, archive
  Silver did not import `common_util` and could treat `archived_ref_*` tables as
  dated business extracts.
- **Cause:** the promoted archive notebook imported the shared formatting
  library but not the separate internal-table exclusion utility.
- **Fix:** `02a_archive_silver.ipynb` now imports both shared notebooks,
  filters `ref_*` tables before export-date processing, and reports exclusions.
- **Validation:** the relocated `validate_ref_exclusions.py` checks all
  latest/archive consumers and passes from `project X/tests`.


## RG-001 — Repository structure consolidated around one active baseline

- **Change:** version 02 04 was promoted to `project X` root; prior notebook
  trees, legacy repository documentation, generated simulation outputs, and
  superseded report artefacts were moved to the dated repository archive.
- **Documentation:** client material was organised by lifecycle; HLD, TFD, and
  a two-stream notebook runbook were added; ETL tracking was renamed and moved
  to the separate `change tracking` folder.
- **Recovery:** `archive/2026-08-16-reorganisation/MOVE_MANIFEST.tsv` records
  every move and promoted copy.


## SI-004 — Promoted source copy contained the earlier partial config setup

- **Symptom:** post-promotion validation found that the current source folder's
  setup notebook lacked nine configuration tables, live schema capture did not
  call setup, and Gold still owned local configuration DDL.
- **Cause:** the source folder contained an earlier notebook baseline even
  though its change log and validators described the later centralised design.
- **Fix:** the active repository baseline now restores the 18-table idempotent
  config registry, the missing live setup call, and central Gold-rule seeding.
- **Validation:** `validate_cfg_setup.py` verifies ownership, required
  table coverage, setup-call order, and absence of child config DDL.

## SI-005 — Archive replay had no framework source when the table was absent

- **Symptom:** historical Silver replay could not materialise
  `silver.slv_framework` when archive deliveries did not contain a logical
  `framework` table. Downstream `provider_framework.framework_code`
  referential checks therefore had no parent object.
- **Cause:** `02a_archive_silver.ipynb` discovered only physical archive
  tables. The controlled legacy framework CSV was not registered as an
  archive-replay source.
- **Fix:** archive Silver now uses the archived framework's latest eligible
  snapshot when available. When no framework snapshot exists on or before a
  canonical month—including complete physical-table absence—it reads
  `Files/deprecated_wmpp_files/framework.csv`, validates
  the required columns and non-empty content, stamps each canonical monthly
  snapshot date into `export_date`, and routes the frame through normal PK
  deduplication, conformance, auditing, metrics, and FK dependency ordering.
- **Provenance:** the Silver result records `_archive_fallback = true` and
  `_source_file`. No synthetic `archived.archived_framework` table is created.
- **Contract note:** `framework` is currently absent from
  `schema_definition.csv`, although `provider_framework` references
  `framework.framework_code`. The notebook uses a narrow evidence-based local
  contract for both archived and fallback framework data until the central
  schema contract is formally approved. The missing contract remains visible
  as schema drift rather than being silently approved.
- **Failure behaviour:** a missing file, empty file, or missing required column
  fails the affected canonical month and is retained in the existing audit and
  month-end error controls.
- **Validation:** run
  `python validate_archive_framework_fallback.py`; the full portable
  validator set must also pass.
## SI-006 — Gold referral model used obsolete referral column names

- **Status:** Fixed in the project source; Fabric deployment and April replay are required.
- **Symptom:** archive replay reached `04_gold_model` for 2026-04-30,
  then failed while creating `gold.fact_referral` because
  `modified_timestamp` could not be resolved in `silver.slv_referral`.
- **Cause:** the current flattened referral extract uses `placement_type`,
  `referral_created_date`, `referral_modified_date`, and `referral_status`.
  These fields were visible as `UNCONTRACTED_COLUMN_ADDED` in both schema-drift
  sheets, so Silver removed them. Gold still referred to the older audit-style
  names `placement_type_code`, `created_timestamp`, `modified_timestamp`,
  `status`, and `rev`.
- **Fix:** the referral section of `schema_definition.csv` now includes all six
  captured flattened-extract fields with their observed ordinals. The two date
  fields are conformed to timestamps. `04_gold_model` now uses the
  flattened referral names and orders duplicate candidates by referral modified
  date, referral created date, then export date.
- **Preflight:** Gold now checks all required Silver tables and columns before
  creating views. If a deployment or Silver rerun is missing, it raises one
  actionable `Gold source validation failed` message instead of a sequence of
  unresolved-column errors.
- **Recovery:** deploy the updated notebook and copy the updated contract to
  `Files/cfg_files/schema_definition.csv`; then set the affected month to reload
  and rerun `02a_archive_silver` from 2026-04-30.
- **Validation:** run `python validate_gold_referral_schema.py`; the full
  portable validator set must also pass. The Spark simulation fixture now mirrors
  the flattened referral schema; execute it in a PySpark/Delta-capable environment. The Spark simulation fixture now mirrors
  the flattened referral schema; execute it in a PySpark/Delta-capable environment.

## SI-007 — Reconcile the schema contract with observed source fields

- **Symptom:** The 2026-04-30 replay exposed a stale `silver.slv_referral`
  shape and joins to parents that were not present in the active definition.
- **Evidence:** Both drift sheets recorded 389 matching fields and 247
  contracted fields missing from the observed source. The replay output also
  confirmed the available month-end Silver parents: framework,
  framework_category, holding_company, provider, provider_framework,
  provider_home, provider education provision, and provider-home dimensions.
- **Fix:** `configuration/schema_definition.csv` was rebuilt from available
  observed fields, with the six SI-006 referral fields retained. Definitions
  that were explicitly missing were removed. The `join_class` and
  `join_evidence` columns now distinguish `CONTRACT_FK`, `TRIAL_JOIN`,
  `INVALID_JOIN`, and `NO_JOIN`.
- **Join decision:** Retained source FKs point only to available parent keys.
  High-confidence name/key mappings are marked `TRIAL_JOIN` pending Fabric
  reconciliation; local-authority mappings remain `INVALID_JOIN` because the
  parent definition was not delivered.
- **Validation:** Contract uniqueness, table/column coverage, FK target
  availability, and portable notebook validators must pass before deployment.

## GLD-001 — Gold referral model consumed a stale/untrusted Silver contract

- **Symptom:** Gold failed with unresolved referral fields because the
  deployed contract had removed `placement_type`, `referral_created_date`,
  `referral_modified_date`, and `referral_status` from Silver.
- **Cause:** Gold was run against a Silver snapshot produced from the old
  contract. The previously assumed source event-log table is not delivered.
- **Fix:** Gold now uses the available flattened Silver tables and current
  referral field names. Mandatory sources are preflighted; lifecycle timing
  comes from the explicit derived `silver.slv_referral_lifecycle_event`
  stream rather than a fabricated empty event-log relation.
- **Recovery:** Deploy the rebuilt contract and Gold notebook, mark the
  affected month for reload, rerun archive Silver, then run DQ and Gold.

## SI-008 — Materialise the age-band axis in Silver

The former report-only calculated table is now rebuilt as
`silver.slv_age_band` with `age_band` and `sort_order`.

## SI-009 — Materialise the directory summary axis in Silver

The disconnected reporting axis is now rebuilt as
`silver.slv_directory_summary_axis` with `display_type`.

## SI-010 — Materialise the fostering axis in Silver

The fostering-only disconnected axis is now rebuilt as
`silver.slv_fostering_axis` with `display_type`.

## SI-011 — Materialise referral closure-reason summary in Silver

The former DAX summary is now rebuilt as
`silver.slv_referral_closure_reason_summary`, using the available referral
provider and offer Silver tables and producing one bucket per referral.

## SI-012 — Materialise the date dimension in Silver

The date table is now rebuilt as `silver.slv_dim_date`, covering the observed
date range from referral, offer, and IPA Silver data with year, month, quarter,
and day-name attributes.

## SIL-001 — Successful Silver audit could preserve an incomplete target schema

- **Symptom:** `bronze.referral` was reported as already successful, so the
  formatter skipped rebuilding `silver.slv_referral` even though the target
  lacked contract columns such as `placement_type`.
- **Cause:** the skip decision trusted the audit status without checking the
  existing Silver target schema. The configuration Delta table can also retain
  an older populated contract until setup is deliberately reloaded.
- **Fix:** latest and archive Silver now verify target columns before skipping;
  missing contract columns force an idempotent overwrite. Added
  `validate_silver_required_columns.py` to lock down the referral
  contract and both refresh guards.
- **Recovery:** run setup once with `LOAD_FILE_CONFIG = True` after deploying a
  changed contract CSV, then rerun the affected Silver formatter or archive
  month. Return the flag to `False` afterward.

## Deployment status for SI-007 onwards

- **Source changes:** complete in the repository.
- **Portable validation:** required validators pass locally after the final
  contract and notebook changes.
- **Fabric validation still required:** deploy the contract and notebooks,
  reload 2026-04-30, confirm the Silver materialisations and Gold snapshot,
  then reconcile `TRIAL_JOIN` results before promoting them to contract FKs.

## CFG-001 — Child notebooks reread configuration CSVs

- **Symptom:** schema and DQ consumers each depended on direct CSV paths,
  allowing configuration to drift between notebook runs.
- **Fix:** setup now performs the one-off CSV-to-Delta bootstrap into
  `monitoring.cfg_schema_contract_column` and
  `monitoring.cfg_data_quality_rule`. Consumers use those tables only.
- **Operation:** leave `LOAD_FILE_CONFIG = False` for normal runs; set it to
  `True` for an intentional reload of either CSV-backed configuration table.
- **Validation:** the consumer scan reports no direct schema/DQ CSV readers.

## SI-013 — Referral event-log Silver table was absent

- **Decision:** no `referral_event_log` source table is delivered, so setup
  must not fabricate an empty source-shaped Silver table.
- **Fix:** `03_silver_business_rules` materialises
  `silver.slv_referral_lifecycle_event` from real Referral, Offer, and IPA
  timestamps. Gold consumes that explicitly derived lifecycle stream.
- **Scope:** this is not a full source-system audit trail. The referral
  snapshot remains one row per referral/snapshot date and is not an event
  history.

## SI-014 — Archive replay needed a traceable single-month mode

- **Fix:** `02a_archive_silver` accepts `PROCESS_ONLY = "YYYY-MM"`,
  resolves it to the canonical final export in that month, and processes only
  that snapshot.
- **Safe reset:** `RESET_MONTH_MONITORING` and
  `CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY` are optional. Either requires
  `CONFIRM_PROCESS_ONLY_RESET = "RESET YYYY-MM"`; monitoring deletion is
  limited to that canonical snapshot.

## SI-015 — Latest Silver duplicated common conformance helpers

- **Fix:** `02_silver_formatter` now imports the shared library for
  conformance, casting, audit, and target-schema refresh helpers. Its local
  duplicate implementations were removed.

## SI-016 — Consolidate common helpers into one notebook

- **Fix:** `99_common_library` was repaired as a valid notebook and now
  owns the former `common_util` exclusion policy together with shared Silver
  helpers. Project notebooks no longer import `common_util.ipynb`.
- **Validation:** `validate_si013_si016.py` verifies the library JSON,
  the migration, the archive controls, and the event-log shell.

## SI-017 — Bronze drift tables and Gold dimensions were omitted from the active flow

- **Symptom:** Bronze tables such as `provider_submission_docs` existed in the
  drift output but had no `schema_definition.csv` rows, so Silver logged and
  skipped them. The legacy Gold translator also described dimensions based on
  stale source names.
- **Fix:** Added evidence-backed contracts for all eight uncontracted Bronze
  tables, including provider documents, SIC codes, referral-person support
  needs and reference metadata. Added `05_gold_dimensions.ipynb` to create
  Gold dimensions and bridges from real Silver sources, with source/column
  preflight checks.
- **Archive naming:** `00_archive_load.ipynb` now preserves source table names
  in `archived` (for example `archived.referral` and
  `archived.provider_submission_docs`); `archived_` is no longer applied.
  The prior notebook is retained in the version 02 03 archive.
- **Operations:** `90_run_live_pipeline.ipynb` links the standard live
  sequence, and `ARCHIVE_PIPELINE_RUNBOOK.md` records the archive sequence
  and safe single-month recovery controls.

## ARCH-ETL-001 - archive_pipeline
running the 90_run_archive_pipeline notebook at the 02a_archive_silver step notebook i get an error. the error message is captured in the monitoring tables which means the logging tables works

select 
* from monitoring.vw_job_step_summary

heres the error An error occurred while calling o6949.throwExceptionIfHave.
: com.microsoft.spark.notebook.msutils.NotebookExecutionException: Timeout when exe cell - 13 in notebook 02a_archive_silver, code length = 11912 and it costs 1800.0s. You can set timeout parameter to mitigate the issue. Please check the doc https://go.microsoft.com/fwlink/?linkid=2152237#notebook-utilities for details.You can check driver log or snapshot for detailed error info! See how to check logs: https://go.microsoft.com/fwlink/?linkid=2157243 .

please extend the time for the runtime allowance.

## ARCH-ETL-002 - archive_pipeline -multiple current month snapshots
running the 90_run_archive_pipeline notebook at the 02a_archive_silver i noticed it creates a snapshot table for the LATEST current month for example the latest archive extract is 2026-08-20 so a snapshot of the previous current month (if archive load was loaded yesterday) will be 19 august 2026. in this situation the most current snapshot in the target table (2026-08-19) should be overwriting with the latest ready to snapshot 2026-08-20  data... its should do this step each time the archive pipeline is run daily for any reason.  
in summary the latest batch if its mid month should be overwritten with the current data in the archive current batch. example Month-end batches: 5; 2026-04-30, 2026-05-30, 2026-06-30, 2026-07-31, 2026-08-20
should allow overwrite into snapshot for these months... the last batch for the latest data: 2026-08-20 should follow the steps...  delete previous snapshot for that month  2026-08 which might be anything between 2026-08-01 -  2026-08-19 and the insert into the snapshot

## LIVE-ETL-001 - live_pipeline -multiple current month snapshots
i suspect the 90_run_live_pipeline has the same issue as ARCH-ETL-002. could this also be added to the live pipeline.


## SI-018 - missing derived columns
i have asked if you can add the fields to the silver tables to enhance the details, these additional fields arent only restricted to the referrals table but the ipa table, or the referral_provider or offers table.. here are the derived fields in a markdown \project X\client documentation\04_Data_and_Reporting\ENHANCEMENT_BACKLOG.md . 

please asses whether these enhancements should be made in the silver layer or the gold layer.. if decision is made to perform the derivations in the silver then  promote these fields upto the gold layer and and to the snapshot table if these columns are added to the referrals table.. 
could you please add these to the relevant gold tables and have dataquality rules added for them, 

please update the 03_Architecture_and_Design/Proposed_Solution_Architecture.md appropriately with the changes

## SI-019 - new derived columns
also in the fact referral table can we have new enhanced fields such as.. please review these KPI and add or update them to the project X/client documentation/02_Assessment_and_Requirements docs.... 

 - referral.cnt_offer_made (aggregate_fact of offers made for referral)
```select  o.offer_status , count(*)
      from bronze.referral a
      left join bronze.referral_provider b on a.referral_id=b.referral_id
      inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
      group by all
```
  - - result
        OFFER_UNSUCCESSFUL,18
        DRAFT,414
        OFFER_SUCCESSFUL,6
        OFFER_MADE,1095
        OFFER_WITHDRAWN,78
  - referral.first_offer_date:this might be useful in the snapshot tabel to see how responsive the providers are to making an offer
```select  a.referral_id,min(o.offer_date) as first_offer_date 
      from bronze.referral a
      left join bronze.referral_provider b on a.referral_id=b.referral_id
      inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
      group by all
```
  - referral.first_provider_seen_date :referrals without offers and no views by providers: the script below will show referrals that havent been looked at yet
```
with 
cte_view_referral (select  distinct a.referral_id, MIN(created_date) min_seen_date
from bronze.referral a
inner join bronze.referral_provider b on a.referral_id=b.referral_id
)
select  cte_r.referral_id , min_seen_date as first_provider_seen_date
 from bronze.referral a
inner join cte_view_referral cte_r on cte_r.referral_id=a.referral_id
```

  - referral.is_not_seen_by_providers :referrals without offers and no views by providers: the script below will show referrals that havent been looked at yet
```
with 
cte_view_referral (select  distinct a.referral_id
from bronze.referral a
anti join bronze.referral_provider b on a.referral_id=b.referral_id
)
select count(distinct cte_r.referral_id) no_viewed_by_ref
 from bronze.referral a
anti join bronze.ipa c on a.referral_id=c.referral_id
inner join cte_view_referral cte_r on cte_r.referral_id=a.referral_id
```

 - referral.ipa_placement_admission_date :if succesfully assigned to a proivder the child will have an admission date
   
```
select a.referral_id,  c.placement_admission_date as ipa_placement_admission_date
 from bronze.referral a
left join bronze.referral_provider b on a.referral_id=b.referral_id
inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
left join bronze.provider_home ph on o.provider_home_id =ph.provider_home_id
inner join bronze.ipa c on a.referral_id=c.referral_id
```

 - referral.ipa_2_signatures :if succesfully assigned to a proivder the child will have an admission date
   
```
select a.referral_id,  c.status   
 from bronze.referral a
left join bronze.referral_provider b on a.referral_id=b.referral_id
inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
left join bronze.provider_home ph on o.provider_home_id =ph.provider_home_id
inner join bronze.ipa c on a.referral_id=c.referral_id
```
various status are 
SIGNED
READY_FOR_SIGNATURE
DRAFT
SIGNED_BY_PROVIDER
SIGNED_BY_LA

where 'SIGNED' means its signed by at least to bodies

 - referral.ipa_last_signature_date: if successfully assigned to a provider the child will have an admission date
   
```
select a.referral_id,  GREATEST(signed_datetime_for_local_authority, signed_datetime_for_provider,   can_sign_date) as ipa_last_signature_date
 from bronze.referral a
left join bronze.referral_provider b on a.referral_id=b.referral_id
inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
left join bronze.provider_home ph on o.provider_home_id =ph.provider_home_id
inner join bronze.ipa c on a.referral_id=c.referral_id
```

-- ipa.duedilgence_min_review_date
```
select  distinct  a.referral_id, c.status, psd.document_name
,  psd.expiry_date , psd.last_updated, psd.next_review_date
 from bronze.referral a
left join bronze.referral_provider b on a.referral_id=b.referral_id
inner join bronze.offer o on b.referral_provider_id =o.referral_provider_id
left join bronze.provider_home ph on o.provider_home_id =ph.provider_home_id
inner join bronze.ipa c on a.referral_id=c.referral_id and c.offer_id=o.offer_id
inner join bronze.provider_submission_docs psd on psd.home_id =o.provider_home_id
where a.referral_id = '5236db3f-cc23-4109-9c0b-eacfb4a277bb'
```
note that these dates must be greater than the ipa_placement_admission_date and not null as this implies that the provider hasnt got the right paperwork inplace 


      
