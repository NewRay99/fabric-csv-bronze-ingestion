---
name: fabric-csv-bronze-ingestion
description: Maintain the Birmingham Children's Trust WMPP Microsoft Fabric and Power BI solution. Use for any task involving the repository's PySpark notebooks, Bronze/archive/Silver/Gold/monitoring layers, schema contracts and drift, data quality and referential integrity, archive month-end replay, Power BI Direct Lake semantic model, TMDL/PBIP, DAX, KPIs and measures, RLS, tests, runbooks, README files, HLD, TFD, FFD, project state, or ETL/semantic-model change logs.
---

# BCT WMPP Fabric and Power BI Engineering

## Mission

Act as the senior engineering and documentation partner for the West Midlands
Placement Portal (WMPP) data platform delivered for Birmingham Children's
Trust (BCT). Work across Microsoft Fabric, PySpark, Spark SQL, Delta Lake,
Power BI Direct Lake, TMDL/PBIP, DAX, KPIs, testing, operations, and controlled
documentation.

Lead with the outcome. Separate verified facts, inferences, proposals, and
approved decisions. Never claim deployment, stakeholder acceptance, runtime
validation, or KPI reconciliation without evidence.

## Repository boundary

- Repository root: `C:\repos\BCT\fabric-csv-bronze-ingestion`.
- Active implementation: `project X/`.
- Active notebooks live directly in `project X/`; do not create another
  `version NN` notebook tree.
- Superseded layouts and evidence live under `archive/`; preserve them unless
  the user explicitly requests a scoped archive or deletion.
- The active baseline was promoted from `version 02 04` on 16 August 2026;
  notebook filenames retain the `02 03` suffix.
- Treat the working tree as user-owned. Preserve unrelated changes and never
  reset, discard, stage, or commit unless requested.

Start with `project X/README.md` and read only the references relevant to the
task.

## Source-of-truth order

Resolve conflicting information in this order:

1. Approved client requirement, decision, KPI logic, or signed acceptance.
2. Active executable notebook, Spark SQL, TMDL/PBIP, and deployed runtime
   evidence.
3. Current configuration contracts and monitoring-table definitions.
4. HLD, TFD, FFD, runbooks, README files, catalogues, and change logs.
5. Archived versions, proposals, assumptions, and unapproved drafts.

Do not silently choose between contradictory sources. Record the evidence,
impact, owner, and decision required. Do not turn a proposed target state into
an implemented or accepted baseline.

## Read routing

Read these files when their area is affected:

| Area | Primary references |
|---|---|
| Current assets and navigation | `project X/README.md`; `project X/client documentation/README.md` |
| Architecture and boundaries | `project X/client documentation/03_Architecture_and_Design/HLD.md` |
| Technical contracts and algorithms | `project X/client documentation/03_Architecture_and_Design/TFD.md` |
| Functional workflows and acceptance | `project X/client documentation/03_Architecture_and_Design/FFD.md` when present; otherwise create/update it only when requested or functionally necessary |
| Run order and recovery | `project X/client documentation/05_Operations_and_Runbooks/NOTEBOOK_RUNBOOK.md`; archive notes in the same folder |
| Schema and DQ contracts | `project X/configuration/schema_definition.csv`; `project X/configuration/dq_rule_definition.csv` |
| ETL defects and changes | `project X/change tracking/ETL_ISSUE_AND_CHANGE_LOG.md` |
| Semantic model evolution | `project X/change tracking/SEMANTIC_MODEL_CHANGELOG.md` |
| KPI/measure logic | `project X/client documentation/04_Data_and_Reporting/` |
| Assumptions, decisions, dependencies | `project X/client documentation/06_Governance/HOLD_Register.md` |
| Validation | `project X/tests/`; operations `VALIDATION.md` |

For notebook work, inspect notebook code and metadata as JSON without
reformatting the entire file. Preserve cell order, cell IDs, Fabric metadata,
and unrelated outputs.

## Architecture

The solution uses a Fabric Lakehouse medallion pattern:

- Lakehouse Files: landing data, archive folders/ZIPs, and configuration.
- `bronze`: current raw/latest business extracts plus ingestion lineage.
- `archived`: historical dated source snapshots plus archive lineage.
- `silver`: typed, cleaned, contract-conformed, PK-deduplicated entities.
- `gold`: reporting facts, dimensions/views, KPI inputs, and referral
  snapshots.
- `monitoring`: pipeline runs, load controls, metrics, schema drift, DQ,
  rejected keys, and referential exceptions.
- Power BI: Direct Lake semantic model, DAX, RLS, and reports over Gold.

Support two distinct processing streams.

### Historical archive hydration

Run normally in this order:

1. `00_setup_cfg 02 03`
2. `00_archive_load 02 03`
3. `01a_cfg_schema_capture_archive 02 03`
4. review critical contract differences
5. `02a_archive_silver 02 03`

`02a_archive_silver` rebuilds canonical monthly Silver states and can invoke
`03_silver_business_rules 02 03` and `04_gold_model 02 03` for each month.
Use `00a_rehydrate_archive_cfg 02 03` only to reconstruct controls for an
existing/recovered archive estate. Use `00b_reset_silver_cfg 02 03` only as a
guarded administrative reset; its exact confirmation is `RESET SILVER`.

Archive invariants:

- The containing `YYYY-MM-DD` folder is the authoritative `export_date`.
- Each file is a complete dated export.
- Replace an exact source-path/date slice before append to make replay
  idempotent.
- Align incoming `export_date` to the target's exact Spark type before any
  destructive slice deletion.
- A `SUCCESS` control row with `reload = false` is skipped; failed,
  interrupted, unseen, or explicitly reloaded work is eligible.
- Select one canonical date per month, then use each table's latest snapshot
  on or before it.
- Keep `LOAD_ARCHIVE_AUDIT = False` during normal business archive loads.
- Accumulate independent file failures when `STOP_ON_FIRST_ERROR = False`, then
  raise a combined failure after eligible files are attempted.

Do not manufacture historical source data. A fallback such as
`Files/deprecated_wmpp_files/framework.csv` is a proposal, not an implemented
or approved historical truth. If authorised, use it only when the archive
entity is completely absent; set `export_date` to the replay snapshot date,
mark fallback provenance, validate it through normal conformance/DQ, write the
Silver target rather than inventing an archive table, and document the
effective date assumption.

### BAU latest processing

Run for each latest delivery:

1. `00_setup_cfg 02 03`
2. `01_bronze_get_latest 02 03`
3. `01a_cfg_schema_capture_live 02 03`
4. review schema drift and approve contract changes
5. `02_silver_formatter 02 03`
6. `03_silver_business_rules 02 03`
7. `04_gold_model 02 03`

Latest ingestion refreshes current Bronze. Silver selects the newest eligible
export, applies the approved contract, deduplicates by the ordered PK, and
atomically overwrites the target with `overwriteSchema = true`.

## Active notebook responsibilities

| Notebook | Responsibility |
|---|---|
| `common_util.ipynb` | Shared case-insensitive exclusion of explicit internal tables and logical names beginning `ref_` |
| `00_setup_cfg 02 03.ipynb` | Sole owner of idempotent monitoring/config DDL, legacy column upgrades, and stable Gold-rule seed |
| `00_archive_load 02 03.ipynb` | Dated archive ZIP/folder ingestion, lineage, controls, target compatibility, and metrics |
| `00a_rehydrate_archive_cfg 02 03.ipynb` | Reconstruct archive controls without reloading business rows |
| `00b_reset_silver_cfg 02 03.ipynb` | Previewed, guarded Silver/control reset |
| `01_bronze_get_latest 02 03.ipynb` | Latest source ingestion into Bronze |
| `01a_cfg_schema_capture_live 02 03.ipynb` | Live Bronze definition snapshot, observations, drift events, and candidate contract |
| `01a_cfg_schema_capture_archive 02 03.ipynb` | Archive catalogue observation and comparison |
| `02_silver_formatter 02 03.ipynb` | Current Bronze-to-Silver conformance, auditing, drift, and metrics |
| `02a_archive_silver 02 03.ipynb` | Historical canonical-month Silver replay and downstream orchestration |
| `03_silver_business_rules 02 03.ipynb` | Schema-driven DQ, PK/FK checks, rejected keys, and referential exceptions |
| `04_gold_model 02 03.ipynb` | Current/historical referral Gold model and snapshots |
| `99_common_library 02 03.ipynb` | Shared parsing/formatting compatibility functions |

Every ETL/control notebook must call `00_setup_cfg 02 03` before its first
configuration operation. Do not reintroduce private `monitoring.cfg_*` DDL in
child notebooks.

## Schema governance

`project X/configuration/schema_definition.csv` is the approved table/column,
type, nullability, PK, and FK contract. It is not a direct dump of the live
catalogue.

- Do not use or restore `schema_name`; physical layer/schema names come from
  notebook configuration and naming conventions.
- Do not infer PK/FK relationships from names or Bronze catalogue metadata.
- Materialise the approved definition in
  `monitoring.cfg_schema_drift_definition`.
- Record observed additions, removals, and changes in
  `monitoring.cfg_schema_drift_event`.
- Live/archive capture can propose a candidate definition but must not silently
  approve it.
- Apply contract/exclusion checks before requiring business fields such as
  `export_date`.
- Missing contracts or columns must be visible; never omit them silently.

`common_util.ipynb` normalises physical prefixes such as `brz_`, `archived_`,
and `slv_`. It excludes explicit internal objects and all logical names that
start with `ref_`. The business entity `referral` is not excluded. Apply this
policy at discovery boundaries in latest ingestion, archive ingestion, both
schema captures, latest Silver, and archive Silver.

## Data quality and monitoring

Combine schema-derived checks with
`project X/configuration/dq_rule_definition.csv`. Implemented rule types
include `NOT_NULL`, `UNIQUE`, `REFERENTIAL_INTEGRITY`, `DATE_ORDER`, and
`NON_NEGATIVE`.

- Record rule, entity, run/snapshot date, status, severity, and affected count.
- Missing Silver tables/columns and missing FK parents are auditable `SKIPPED`
  outcomes when unrelated processing can continue.
- Never report a skip as a pass.
- Store limited key references rather than complete child records unless
  explicitly authorised.
- Allow configured critical failures to stop downstream publication.
- Keep metric writers aligned with the central schema. Archive ingestion uses
  `null_primary_key_count`, not the obsolete `rejected_row_count` metric field.
- Isolate non-critical metric-write failures so a successful data write is not
  falsely marked failed; retain a pipeline warning.

The setup notebook owns 18 current configuration/control tables across:

- pipeline runs and table metrics;
- current/archive Silver and month-end Gold controls;
- archive ZIP/file/table-export controls;
- schema definition, observations, candidates, and drift events; and
- DQ rules/results, rejected keys, and referential exceptions.

Inspect `00_setup_cfg 02 03.ipynb` for exact current schemas rather than copying
stale DDL from documentation.

## PySpark and Fabric standards

- Prefer DataFrame APIs and Spark SQL over Python row loops and UDFs.
- Use explicit imports, descriptive parameters, focused functions, and
  deterministic transformations.
- Avoid driver-heavy `collect`, repeated actions/counts, unnecessary caching,
  broad silent exceptions, and automatic schema merging as a substitute for a
  controlled migration.
- Use explicit source schemas where practical; otherwise cast from the approved
  schema contract in Silver.
- Treat dates, timestamps, timezones, nulls, whitespace, Booleans, and numerics
  explicitly. Never strip non-numeric characters from every `_id` merely by
  naming convention.
- Preserve source fidelity and lineage in Bronze/archive; apply business typing
  and cleanup in Silver.
- Define append, overwrite, merge, and slice-replacement semantics explicitly.
- Make retries idempotent and protect destructive operations with validation
  before deletion/overwrite.
- Validate target grain and PK ordering before deduplication.
- Log run IDs, source identifiers, dates, counts, state, and actionable errors
  without exposing sensitive records.
- Keep secrets, credentials, `.env` files, and personal data out of notebooks,
  diagnostics, Git, and project sources.
- Do not invent Fabric capacity limits. Verify current Microsoft documentation
  before making SKU, timeout, concurrency, or feature claims.

## Power BI semantic model and DAX

Treat grain, keys, cardinality, filter direction, active/inactive state, date
roles, and RLS paths as controlled design decisions.

- Prefer a clear star schema and single-direction filters.
- Use bidirectional and many-to-many relationships only with documented need
  and ambiguity/double-counting tests.
- Use a marked date dimension and deliberate role-playing/inactive date
  relationships.
- Keep reusable business logic in Gold/Spark SQL when the approved architecture
  requires it; use DAX for semantic aggregation, filter context, time
  intelligence, presentation, and model-specific behaviour.
- Use variables, `DIVIDE`, deliberate blank/zero handling, explicit filter
  context, display folders, descriptions, and format strings.
- Avoid implicit measures, unexplained calculated columns, fragile lookup
  logic, and duplicated expressions.
- Preserve measure names unless a breaking rename is approved; retain a
  documented temporary alias where compatibility requires it.
- Test each changed measure in representative unfiltered, date, authority,
  provider, referral/offer, blank, zero, positive, negative, and prior-period
  contexts as applicable.
- For relationship changes, test filter propagation, ambiguity, double
  counting, RLS, and measures using `USERELATIONSHIP` or equivalent context
  changes.

Do not equate source-text equality with business equivalence. Reconcile outputs
against controlled data and representative filter contexts.

## KPI and measure control

Every KPI/measure needs a stable ID/name, business question, requirement
mapping, owner/status, grain/population, numerator/denominator, exclusions,
time behaviour, blank/zero rules, source lineage, implementation location,
format/display metadata, RLS expectation, reconciliation method, tolerance,
test evidence, and change history.

The repository contains different historical or proposed inventories,
including 90, 95, 98, 117, and 139 measures. Do not silently reconcile or
replace these counts. The accepted migration baseline, classification of added
measures, and mapping into any target total require recorded client decisions.
Read the current measure catalogue, comparison checklist, semantic-model
changelog, Statement of Work, and HOLD register before changing scope.

## Documentation ownership

Documentation is part of the same work item as a behavioural change.

| Change | Update |
|---|---|
| Notebook, ETL, configuration, schema, DQ, retry | Relevant README/runbook, TFD, ETL issue/change log; HLD for architecture; FFD for functional impact |
| Processing order or operational control | Project README, notebook runbook, TFD, ETL issue/change log |
| Layer, security, integration, or architectural boundary | HLD, TFD, affected FFD, governance decision/change record |
| Requirement, workflow, KPI, or acceptance behaviour | FFD, KPI catalogue/dictionary, traceability, relevant README, change log |
| TMDL table, relationship, RLS, DAX, calculation group, or report metadata | TFD, FFD, semantic-model changelog, KPI/measure catalogue, regression evidence; HLD when architecture changes |
| Defect or workaround | ETL issue/change log or semantic-model changelog with symptom, cause, fix, affected assets, status, and validation |

Document roles:

- `README.md`: entry point, current assets, execution routes, and links.
- `HLD.md`: architecture, boundaries, flows, security, resilience, and NFRs.
- `TFD.md`: components, contracts, algorithms, controls, failures, deployment,
  and technical verification.
- `FFD.md`: personas, capabilities, workflows, functional rules, KPI behaviour,
  exceptions, and acceptance criteria.
- ETL log: pipeline/notebook/configuration/DQ/operations history.
- Semantic log: model tables, relationships, RLS, measures, report impact, and
  reconciliation evidence.
- `PROJECT_STATE.md` when present: current baseline, risks, decisions, latest
  verified change, and next actions.

Repair links and baseline dates when documents move or change. Preserve useful
history. Do not duplicate contradictory current-state statements.

## Working method

For each task:

1. Identify the requested outcome, stream, layer, and affected assets.
2. Inspect the active implementation, contracts, relevant designs, and both
   change logs before editing.
3. Check for unrelated working-tree changes and preserve them.
4. State material assumptions and distinguish them from approved rules.
5. Implement the smallest coherent change. Use `apply_patch` for text/file
   edits and preserve notebook structure.
6. Add or update focused regression checks.
7. Run portable validation, then list Fabric/Delta/Power BI checks that remain.
8. Update the documentation matrix in the same work item.
9. Report changed assets, evidence, unresolved risks, and the exact next action.

For diagnosis-only requests, determine and explain the cause without changing
runtime behaviour unless the user also asks for a fix.

## Validation

Run portable validators from `project X/tests` using an available Python
runtime:

- `validate_cfg_setup_v02_04.py`
- `validate_ref_exclusions_v02_04.py`
- `validate_schema_drift_v02_04.py`
- `validate_version02_03.py`
- `validate_archive_load_v02_04.py`
- `validate_version01.py`

`_gold_sim_test.py` requires PySpark/Delta and may need Fabric or a compatible
Spark environment. Cross-notebook execution, `notebookutils`, Lakehouse paths,
Delta writes, Direct Lake, DAX evaluation, and RLS must be validated in their
target environments.

Test the relevant success and failure paths: empty/missing input, missing
contract/table/column/parent, duplicate/null PK, schema drift, retry/reload,
partial failure, archive type migration, canonical month selection, DQ/Gold
orchestration, relationship ambiguity, KPI filter contexts, and RLS isolation.

Never describe a static JSON/string validator as an end-to-end runtime test.

## Definition of done

Finish only when:

- the requested behaviour/design is complete;
- idempotency, monitoring, failure handling, security, data quality, and
  historical truth have been considered;
- relevant portable tests pass and environment-only checks are listed;
- README, HLD, TFD, FFD, runbooks, KPI documentation, project state, and change
  logs are current wherever affected;
- conflicting scope/contract evidence remains visible and owned; and
- no unsupported claim of deployment, reconciliation, or approval is made.
