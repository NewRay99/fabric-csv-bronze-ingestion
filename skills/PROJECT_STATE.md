# Project State

## 17 October 2026 — KPI Definition reconciled to latest saved WIP

KPI Definition is now reconciled to the latest saved local WIP, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. These local report definitions include changes newer than default `master` (`0a65e96`); they are captured by source hashes and complete calculation snapshots, not represented as committed model changes or deployment evidence.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

Current fixed-metric coverage: 338 business definitions and 184 operational definitions; the 843-measure inventory also includes technical helpers. Original scope/approval decisions remain separate. Next: controlled embedded-reference synchronisation and runtime/role/UAT checks. No source model or ETL mutation.

[Current DAX, Python/Spark SQL and source evidence](../project%20X/client%20documentation/04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

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
- SI-013–SI-016 repaired and consolidated `99_common_library 02 03` and
  introduced guarded `PROCESS_ONLY = "YYYY-MM"` archive replay controls.
- The nonexistent source event-log shell was removed. Silver now materialises
  `slv_referral_lifecycle_event` from available Referral, Offer, Provider
  Message, and IPA timestamps; Gold consumes this derived lifecycle stream.
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
