# High-Level Design (HLD)

## 17 October 2026 — KPI Definition reconciled to latest saved WIP

KPI Definition is now reconciled to the latest saved local WIP, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. These local report definitions include changes newer than default `master` (`0a65e96`); they are captured by source hashes and complete calculation snapshots, not represented as committed model changes or deployment evidence.

The workbook remains a controlled reporting dictionary; it is not an ETL feed or a deployed-model guarantee. Current source provenance supersedes older archive counts below.

No report/model, notebook, relationship, RLS or deployment was changed. Existing requirement dispositions remain evidence-led; new associations without source evidence remain unmapped for owner review. Embedded Power BI reference tables still need controlled synchronisation, refresh/context/role checks and client acceptance.

[Current DAX, Python/Spark SQL and source evidence](../04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

## 17 October 2026 — Legend v1 compatibility and verified coverage

The workbook is a controlled reference/requirements artefact, not an ETL configuration feed. The first three sheets retain the v1 schema; expanded evidence lives on Gold Source Coverage. Business and operational monitoring are separate Import semantic models in the inspected source archives. The inspected source baseline is `master` at `0a65e962ff3ab9681ed87d9a0a54df610774b736`. The saved business archive has **71 tables, 490 measure definitions and 35 pages**. The current Mission Control Im archive has **33 tables, 276 measure definitions and 17 pages (10 visible)**. These counts include local tables, display helpers, selectors and benchmarks; they are not approved business KPI totals. The September 58/366 and 87-measure Mission Control statements below describe earlier baselines.

Mission Control now supplies saved reporting evidence for contracts/schema/drift, domains/reference, DQ/RI/rejected keys, lineage, load metrics, pipeline/job/step timing and archive/replay. It partially supports R53, R69, R75, R82, R83, R84, R85, R87 and R88; R20 receives operational context only, not a business audit trail. A mapped measure/page is not proof of uptime, DR, alert delivery, SLA compliance, export/security policy or client acceptance. See the 80-row reassessment and exact calculation trace.

[Calculation trace and source baselines](../04_Data_and_Reporting/KPI_CALCULATION_TRACEABILITY.md).

## Reporting reassessment 30 September 2026

The report experience is now Overall Performance → Referrals → Referral Explorer → Referral Detail, with Provider Explorer → Provider Detail in parallel. The local WIP has 58 semantic tables including local helpers, and uses Import partitions. Do not describe this saved model as a deployed Direct Lake solution.

Gold includes current demographic, IPA-signature, message/reason and category evidence. Calculated journey stages and selectors live in the semantic layer; they do not add source event history or write back to the portal. The dynamic role and separate global-summary design require identity/disclosure acceptance before client release.

See [current status and release checks](../04_Data_and_Reporting/WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


**Project:** West Midlands Placement Portal data platform
**Client:** Birmingham Children's Trust
**Platform:** Microsoft Fabric Lakehouse
**Status:** Current implementation baseline
**Baseline date:** 16 August 2026

## 1. Purpose

This document defines the high-level architecture for ingesting WMPP current
and historical extracts, conforming them into a governed Silver layer, applying
data-quality controls, and publishing a Gold referral model for reporting.

The solution supports two operational streams:

1. **Historical archive hydration** — builds the archive, replays canonical
   monthly Silver states, and writes historical Gold snapshots.
2. **Business-as-usual latest processing** — loads the latest extracts through
   Bronze, Silver, data quality, and Gold.

## 2. Architecture overview

```mermaid
flowchart LR
    subgraph Sources["WMPP extract sources"]
        Latest["Latest CSV/Parquet extracts"]
        Archive["Dated archive ZIPs/folders"]
    end

    subgraph Fabric["Microsoft Fabric Lakehouse"]
        Bronze["bronze\nCurrent raw extracts"]
        Archived["archived\nHistorical dated extracts"]
        Silver["silver\nTyped, deduplicated entities"]
        Gold["gold\nReferral facts, KPIs, snapshots"]
        Monitoring["monitoring\nRuns, loads, DQ and schema drift"]
    end

    Latest --> Bronze --> Silver --> Gold
    Archive --> Archived --> Silver
    Bronze -. schema capture .-> Monitoring
    Archived -. load controls .-> Monitoring
    Silver -. DQ and load controls .-> Monitoring
    Gold -. month-end controls .-> Monitoring
    Gold --> PowerBI["Power BI / downstream reporting"]
```

## 3. Logical layers

| Layer | Purpose | Key characteristics |
|---|---|---|
| Lakehouse Files | Landing and configuration | Latest shortcut, dated archive folders, `Files/cfg_files` |
| `bronze` | Current raw ingestion | Source fidelity plus ingestion lineage and `export_date` |
| `archived` | Historical raw ingestion | One dated slice per file/export with archive lineage |
| `silver` | Conformed entities | Contract-driven types, PK deduplication, consistent naming |
| `gold` | Reporting model | Referral facts/views and dated snapshot table |
| `monitoring` | Operational control | Idempotency, retries, drift lifecycle, DQ results and metrics |

## 4. Processing streams

### 4.1 Historical archive hydration

```mermaid
flowchart LR
    A["00_setup_cfg"] --> B["00_archive_load"]
    B --> C["00a_rehydrate_archive_cfg\nexisting estates/recovery only"]
    C --> D["01a archive schema capture"]
    D --> E["02a archive Silver replay"]
    E --> F["03 business rules"]
    F --> G["04 Gold model\nhistorical snapshot"]
```

Archive exports are treated as complete table snapshots. The replay selects
the final available export in each calendar month and, for each table, uses its
latest available export on or before that canonical date. DQ and Gold are
orchestrated after a successful monthly Silver state.

### 4.2 BAU latest processing

```mermaid
flowchart LR
    A["00_setup_cfg"] --> B["01 Bronze latest"]
    B --> C["01a live schema capture"]
    C --> D["02 Silver formatter"]
    D --> E["03 business rules"]
    E --> F["04 Gold model"]
```

The latest stream overwrites/refreshed current Bronze entities, captures schema
drift against the approved contract, formats the newest export into Silver,
then runs DQ and Gold.

## 5. Configuration and governance

- `00_setup_cfg.ipynb` is the sole owner of configuration-table DDL and
  non-destructive legacy column upgrades.
- `schema_definition.csv` is the approved schema, PK, and FK contract.
- `dq_rule_definition.csv` contains supplementary DQ rules.
- `ref_*` internal/reference tables are excluded through `common_util.ipynb`;
  they are not dated business extracts.
- Schema changes are recorded in `monitoring.cfg_schema_drift_event`; the
  approved definition is materialised in
  `monitoring.cfg_schema_drift_definition`.
- ETL defects and their resolutions are recorded in
  `change tracking/ETL_ISSUE_LOG.md`; material implementation batches are
  summarised in `change tracking/ETL_CHANGE_LOG.md`.

## 6. Resilience and recoverability

- Archive ZIP/file controls and Silver export controls make runs resumable.
- `SUCCESS` with `reload = false` is skipped; failed, interrupted, unseen, or
  explicitly reloaded work is retried.
- Archive file replacement is idempotent by source path and export date.
- Missing schema contracts and missing DQ source/parent objects are recorded as
  auditable skips rather than causing unrelated tables to fail.
- The guarded Silver reset notebook requires an exact confirmation phrase.

## 7. Security and operational boundaries

- Fabric workspace and Lakehouse access must use Entra ID and least-privilege
  workspace roles.
- Source and Lakehouse permissions are managed outside these notebooks.
- Rejected-row logging stores key references, not full child records.
- Notebook diagnostics should contain identifiers, dates, and counts only.
- Secrets and local `.env` files must never be committed or deployed as
  notebook assets.

## 8. High-level non-functional requirements

| Area | Design response |
|---|---|
| Auditability | Run IDs, table metrics, export controls, DQ results, and drift events |
| Reliability | Idempotent controls, deterministic month selection, retry/reload flags |
| Maintainability | Central setup, shared exclusions, CSV-driven schema/DQ contracts |
| Performance | Bulk archive inventory joins, table-level processing, month-end replay |
| Recoverability | Git history, dated repository archive, guarded reset and rehydration |
| Data protection | Least privilege and key-only exception logging |

## 9. Current boundaries

- End-to-end execution requires Fabric Spark, Delta Lake, `notebookutils`, the
  target Lakehouse, and deployed `Files/cfg_files` configuration.
- Bronze catalogue inspection cannot infer trustworthy PK/FK relationships;
  referential metadata must be approved in `schema_definition.csv`.
- The archive audit-event table is intentionally excluded from standard entity
  replay and requires a dedicated event model if reporting is needed later.
