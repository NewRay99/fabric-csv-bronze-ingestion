# Functional and Feature Design (FFD)

**Project:** West Midlands Placement Portal data platform
**Client:** Birmingham Children's Trust
**Platform:** Microsoft Fabric Lakehouse and Power BI
**Status:** Initial controlled baseline
**Baseline date:** 16 August 2026

## 1. Purpose

This document defines the business-facing capabilities and expected behaviour
of the WMPP data platform. It complements:

- the HLD, which describes architecture and system boundaries; and
- the TFD, which describes technical components, contracts, controls, and
  implementation behaviour.

The FFD owns personas, workflows, functional rules, KPI behaviour, exceptions,
and acceptance outcomes.

## 2. Users and stakeholders

| Persona | Primary need |
|---|---|
| Data operations | Run and recover archive and BAU loads, identify failures, and avoid duplicate processing |
| Data engineer | Maintain reliable, testable PySpark/Spark SQL pipelines and governed contracts |
| Data quality owner | Review schema drift, DQ failures, skipped checks, and referential exceptions |
| Power BI developer | Maintain a clear semantic model, relationships, RLS, DAX measures, and report metadata |
| Business analyst / KPI owner | Define KPI intent, filters, grain, thresholds, and requirement traceability |
| Commissioner / operational user | Consume timely, accurate, authority-appropriate dashboards and trends |
| Technical lead / client approver | Control architecture, scope, risks, acceptance, and production readiness |

## 3. Functional scope

### 3.1 Historical archive hydration

The platform shall:

1. discover dated archive extracts;
2. load each eligible file into the historical raw layer with source lineage;
3. support retry and controlled reload without duplicate source/date slices;
4. identify a canonical month-end processing date;
5. build each monthly Silver state using the latest eligible table export on or
   before that date;
6. run data-quality and referential checks;
7. publish a dated Gold snapshot; and
8. record auditable status, counts, skips, warnings, and failures.

Fallback data may be used only where explicitly approved. It must record its
source, applicable date range, business assumption, audit marker, and validation
result. Current fallback data must not silently be treated as historically true.

### 3.2 BAU latest processing

The platform shall:

1. ingest the latest eligible business extracts into Bronze;
2. exclude internal and `ref_*` reference objects before dated-extract checks;
3. capture live schema and compare it with the approved definition;
4. format, type, and deduplicate data into Silver;
5. apply data-quality and referential checks; and
6. refresh the current Gold model for reporting.

A completed export shall be skipped on a normal rerun unless reload is
explicitly enabled.

### 3.3 Schema governance

- The approved schema definition shall identify expected tables, columns,
  types, nullability, primary keys, and foreign-key references.
- Live observations shall not automatically become the approved contract.
- Added, removed, and changed tables or columns shall create drift evidence.
- Missing Silver tables/columns and missing FK parents shall be recorded as
  auditable `SKIPPED` outcomes where continuing is safe.
- A critical incompatibility shall prevent the affected object from being
  presented as successfully conformed.

### 3.4 Data quality and exceptions

- Rules shall be traceable to a contract or approved rule definition.
- Results shall identify rule, entity, processing date/run, status, severity,
  and count.
- Exception evidence shall minimise personal data and normally store only key
  references.
- Critical failures may block downstream publication when configured.
- Skips shall never be reported as passes.

### 3.5 Gold model and reporting

- Gold objects shall expose business-ready facts, dimensions, and approved KPI
  inputs at documented grain.
- Historical snapshots shall remain distinguishable from the current state.
- The Power BI semantic model shall expose approved tables, relationships,
  hierarchies, formats, KPIs, measures, and RLS behaviour.
- Commissioners shall see only data allowed by the approved authority/region
  security mapping.
- Report values shall be reconcilable to Gold data and approved KPI logic.

## 4. KPI and measure behaviour

Each KPI requires an approved definition covering:

| Field | Required content |
|---|---|
| Identifier and name | Stable ID, user-facing name, aliases, and lifecycle status |
| Business intent | Question answered and decision supported |
| Requirement mapping | Relevant requirement(s), gap, or acceptance criterion |
| Grain and population | Entity/time grain and eligible population |
| Calculation | Numerator, denominator, exclusions, thresholds, and rounding |
| Time behaviour | As-of date, period, prior period, month end, and incomplete-period handling |
| Blank/zero behaviour | Display and mathematical treatment |
| Direction and presentation | Direction-of-good, variance indicator, colour, and format |
| Data lineage | Gold sources, joins/relationships, and required attributes |
| Security | Expected RLS behaviour and restricted dimensions |
| Implementation | Spark SQL/Gold object and/or DAX measure location |
| Validation | Test cases, reconciliation source, tolerance, owner, and approval evidence |

The accepted KPI baseline is controlled. Historical inventories and proposals
with different counts must not be merged without an approved mapping.

## 5. Semantic-model features

### 5.1 Relationships

- Relationship cardinality and filter direction shall match documented grain.
- Bidirectional and many-to-many relationships require a recorded reason and
  ambiguity/double-counting tests.
- Inactive date relationships shall be activated explicitly by measures that
  need them.
- Relationship changes require measure and report regression testing.

### 5.2 DAX measures

- Measures shall preserve intentional filter context and return documented
  blank/zero behaviour.
- Ratios shall use safe division.
- Prior-period measures shall use the approved calendar and period semantics.
- Indicator and colour measures shall be tested for blank, zero, positive, and
  negative outcomes.
- Duplicate calculations shall be consolidated only after dependency and
  compatibility review.

### 5.3 Security

- RLS shall be tested using representative authority/region users.
- Tests shall prove permitted visibility and prohibited cross-authority access.
- Security mappings, role logic, ownership, and exception handling shall be
  documented and approved before production acceptance.

## 6. Operational outcomes

| Scenario | Expected outcome |
|---|---|
| First eligible load | Process and write control/metric evidence |
| Successful rerun with reload off | Skip without duplicating target data |
| Failed/interrupted prior attempt | Retry safely |
| Reload explicitly enabled | Replace/reprocess the defined scope and clear reload state when successful |
| Missing non-critical entity/dependency | Record an auditable skip and continue safe unrelated work |
| Critical contract or DQ failure | Fail the affected scope and block publication when configured |
| Schema drift | Preserve observation and comparison evidence; do not silently approve it |
| Historical fallback used | Mark provenance and assumption; validate compatibility and applicable period |

## 7. Acceptance criteria

The solution is functionally acceptable when:

1. both archive and BAU streams complete in the documented order;
2. reruns are idempotent and recovery behaviour is demonstrated;
3. source-to-Bronze/archive and Silver/Gold counts reconcile within approved
   rules;
4. PK, FK, drift, DQ, skip, and failure results are auditable;
5. historical month-end dates and snapshot outputs reconcile;
6. accepted KPIs reconcile in representative unfiltered and filtered contexts;
7. relationship and RLS regression tests pass;
8. operational users can identify the failed object and corrective action;
9. README, HLD, TFD, FFD, runbooks, KPI catalogue, state, and change logs are
   current; and
10. outstanding assumptions and client decisions are visible and owned.

## 8. Controlled open decisions

The following must remain visible until formally resolved:

- contractual/current semantic-model baseline and classification of measures
  above the original 90;
- mapping of proposed new KPIs into the target total;
- approval and temporal validity of any fallback source used in historical
  replay;
- production RLS mapping and test identities;
- runtime reconciliation evidence for measures affected by relationship
  changes.
