# Project State

**Project:** BCT WMPP Fabric and Power BI platform  
**State date:** 18 August 2026  
**Purpose:** Concise handover and continuity record for the ChatGPT Project.

## Current implementation baseline

- Active notebooks are held directly in the `project X` root.
- Two processing streams are supported: historical archive hydration and BAU
  latest processing.
- Configuration-table DDL is centralised in `00_setup_cfg 02 03.ipynb`.
- Schema governance uses an approved definition plus live/archive observations
  and drift events.
- Internal reference objects, including logical names beginning `ref_`, are
  excluded from ordinary dated ETL processing.
- Missing DQ source objects/columns and FK parents can be captured as auditable
  skips.
- Power BI semantic-model history and measure/relationship changes are tracked
  separately from ETL changes.

## Current documentation baseline

- Project README and client documentation index are the entry points.
- HLD and TFD exist under `03_Architecture_and_Design`.
- This pack introduces an FFD so functional behaviour is no longer mixed into
  the TFD alone.
- ETL and semantic-model changes have separate logs.

## Controlled risks and decisions

| Item | Current position | Required action |
|---|---|---|
| KPI/measure baseline | Repository evidence contains several historical/proposed totals | Confirm accepted baseline and classify additions through change control |
| Historical fallback sources | Proposed for entities missing from archives | Approve source, effective date range, provenance, and reconciliation before use |
| RLS | Required for authority/region access | Confirm security mapping, roles, test users, and regression evidence |
| Runtime validation | Some checks are portable; Spark/Delta/DAX validation needs platform access | Record environment-specific test evidence before production acceptance |

## Most recent verified repository work

- Repository structure was reorganised without deleting material.
- Current notebooks were promoted to the `project X` root.
- Client documentation, configuration, tests, reports, and change tracking were
  separated into clear folders.
- Portable notebook validators passed after the reorganisation.
- SI-007 contract rebuilt from observed drift fields: 397 fields across 31
  tables, with explicit `CONTRACT_FK`, `TRIAL_JOIN`, and `INVALID_JOIN`
  classifications.
- GLD-001 Gold mappings use the flattened Silver referral contract and allow
  absent historical event-log enrichment without suppressing mandatory-source
  failures.
- SI-008–SI-012 are idempotent Silver materialisations for axes, closure
  summary, and date dimension.
- Configuration CSVs are now bootstrapped once by setup into
  `monitoring.cfg_schema_contract_column` and
  `monitoring.cfg_data_quality_rule`; child notebooks read the Delta tables.
- Latest and archive Silver no longer trust a prior successful audit when the
  target is missing contract columns; the new Silver-column regression test
  covers the Gold-required referral fields, including `placement_type`.
- SI-013–SI-016 repaired and consolidated `99_common_library 02 03`, added the
  typed optional referral-event-log Silver shell, and introduced guarded
  `PROCESS_ONLY = "YYYY-MM"` archive replay controls.
- Verified with the SI-007 materialisation validator and the full portable
  validator set.

## Next action

- Deploy the current contract and notebooks to Fabric. Use `PROCESS_ONLY` for
  a traceable single-month archive replay, then capture Silver, event-log shell,
  DQ, Gold, and trial-join evidence.

## Update protocol

After every material work item, update:

1. state date;
2. implementation baseline if behaviour changed;
3. documentation baseline if files/roles changed;
4. open risks/decisions;
5. most recent verified change and test evidence; and
6. next actions and owner where known.
