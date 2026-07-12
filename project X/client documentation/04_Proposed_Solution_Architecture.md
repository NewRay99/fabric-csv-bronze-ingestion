# Proposed Solution & Architecture

**Project:** WMPP — West Midlands Placement Portal
**Document:** Proposed Solution & Architecture
**Version:** 1.0
**Date:** 12 July 2026
**Prepared by:** [Consultant Name]
**Classification:** Official — Sensitive

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Solution Overview](#2-solution-overview)
3. [Target Architecture Diagram](#3-target-architecture-diagram)
4. [Data Pipeline Design](#4-data-pipeline-design)
5. [Gold Layer Analytical Model](#5-gold-layer-analytical-model)
6. [Power BI Integration](#6-power-bi-integration)
7. [Security Architecture](#7-security-architecture)
8. [Data Quality Framework](#8-data-quality-framework)
9. [Migration Strategy](#9-migration-strategy)
10. [Technology Stack Summary](#10-technology-stack-summary)

---

## 1. Executive Summary

The West Midlands Placement Portal (WMPP) is a child placement platform operating across 14 West Midlands local authorities. The platform currently relies on CSV files stored on network drives and a Power BI report (V13.1) containing 90 measures. An analysis of the current estate identified **17 functional gaps** and **87 formal requirements (R1–R87)** spanning Placement Officers, Providers, QA Officers, Commissioners, Finance Officers, and non-functional concerns.

This document proposes a modern data platform built on **Microsoft Fabric** using a **bronze-silver-gold medallion architecture**. The solution migrates CSV-based data into a Fabric Lakehouse, processes it through three pipeline notebooks, and delivers a curated **Gold analytical model** comprising **17 tables** (facts and dimensions) and **117 KPIs** across **14 categories**. The Gold layer connects to Power BI via **Direct Lake mode**, providing near-real-time reporting without import refresh overhead.

Key outcomes:

- **Scalability:** Medallion architecture supports incremental data volume growth and additional local authorities.
- **Data quality:** Automated deduplication, schema enforcement, and measure standardisation eliminate the inconsistencies present in the current V13.1 report.
- **Security:** Entra ID authentication, role-based access control (RBAC), and row-level security (RLS) ensure that commissioners only see data for their respective regions (R55).
- **Performance:** Direct Lake mode eliminates scheduled refresh windows, reducing report latency from hours to minutes.
- **Governance:** All 87 functional requirements are traceable to pipeline components, Gold tables, and KPI definitions.

The recommended approach is a **phased migration**: first, lift-and-shift the existing CSV pipeline into Fabric with parity to the current 90 measures; second, enhance the Gold layer to deliver all 117 KPIs and close the 17 functional gaps.

---

## 2. Solution Overview

### 2.1 Medallion Architecture

The proposed solution adopts the **medallion architecture** (also known as the multi-hop pattern), which organises data into three layers of increasing quality and structure:

| Layer | Purpose | Characteristics | Naming Convention |
|-------|---------|-----------------|-------------------|
| **Bronze** | Raw ingestion | All columns as STRING, append mode, ingestion metadata | `brz_<table>` |
| **Silver** | Typed & cleaned | Correct data types per schema definition, deduplicated, validated | `slv_<table>` |
| **Gold** | Analytical model | Fact/dimension tables, KPIs as Spark SQL views, business-ready | `fact_<name>`, `dim_<name>` |

### 2.2 Design Principles

1. **Schema-on-read at Bronze:** All source columns are ingested as STRING to maximise fidelity and prevent ingestion failures due to type mismatches. Type casting is deferred to Silver.
2. **Idempotent Silver processing:** Silver tables are rebuilt from Bronze on each run, ensuring consistency. Deduplication uses primary key columns defined in `schema_definition.csv`.
3. **Gold as semantic contract:** The Gold layer is the single source of truth for analytics. All 117 KPIs are materialised as Spark SQL views, ensuring that Power BI, ad-hoc queries, and future consumers all reference identical logic.
4. **Direct Lake connectivity:** Power BI connects to Gold Delta tables in Direct Lake mode, bypassing import refresh and providing near-real-time data.
5. **Auditability:** Every Bronze table includes ingestion metadata columns (`_ingestion_timestamp`, `_source_file`, `_ingestion_id`), and the Gold layer includes an event log table (`fact_referral_event_log`) for full audit trail support (R67–R70).

### 2.3 Source Systems

The primary data source is **CSV files on network drives**, which are surfaced to the Fabric Lakehouse via a shortcut (`Files/Latest/*.csv`). The underlying source system is **PostgreSQL** with the following schemas:

- `document` — provider documents and submission documents
- `ipa` — in-placement agreement data
- `offer` — referral offers and offer statuses
- `provider` — provider registry, homes, frameworks, messages
- `refdata` — reference data (genders, decline reasons, etc.)
- `referral` — referrals, referral persons, referral categories, events
- `framework` — framework definitions and associations

CSV exports from PostgreSQL are placed on the network drive and picked up by the Bronze ingestion notebook.

---

## 3. Target Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              WMPP DATA PLATFORM                                  │
│                          Microsoft Fabric Lakehouse                              │
│                                                                                  │
│  ┌───────────┐     ┌──────────────────────────────────────────────────────────┐ │
│  │  Network   │     │                  FABRIC LAKEHOUSE                        │ │
│  │  Drive     │     │                                                        │ │
│  │  (CSV)     │────▶│  ┌────────────────────────────────────────────────┐    │ │
│  └───────────┘     │  │           Files/Latest/*.csv (Shortcut)         │    │ │
│       ▲            │  └──────────────────┬─────────────────────────────┘    │ │
│       │            │                     │                                   │ │
│  ┌────┴──────┐     │                     ▼                                   │ │
│  │ PostgreSQL│     │  ╔═══════════════════════════════════════════════╗   │ │
│  │ (Source)  │     │  ║            NOTEBOOK 1: BRONZE LOADER          ║   │ │
│  │           │     │  ║  CSV → Delta (append), all STRING columns     ║   │ │
│  │ Schemas:  │     │  ║  Creates: brz_<table>                         ║   │ │
│  │ document  │     │  ╚═══════════════════┬═══════════════════════════╝   │ │
│  │ ipa       │     │                      │                               │ │
│  │ offer     │     │                      ▼                               │ │
│  │ provider  │     │  ╔═══════════════════════════════════════════════╗   │ │
│  │ refdata   │     │  ║         NOTEBOOK 2: SILVER FORMATTER          ║   │ │
│  │ referral  │     │  ║  Type casting per schema_definition.csv       ║   │ │
│  │ framework │     │  ║  Deduplication, cleaning, validation          ║   │ │
│  └───────────┘     │  ║  Creates: slv_<table>                         ║   │ │
│                    │  ╚═══════════════════┬═══════════════════════════╝   │ │
│                    │                      │                               │ │
│                    │                      ▼                               │ │
│                    │  ╔═══════════════════════════════════════════════╗   │ │
│                    │  ║         NOTEBOOK 3: GOLD TRANSLATOR           ║   │ │
│                    │  ║  Fact/Dim tables + 117 KPI Spark SQL views   ║   │ │
│                    │  ║  Creates: fact_<name>, dim_<name>             ║   │ │
│                    │  ╚═══════════════════┬═══════════════════════════╝   │ │
│                    │                      │                               │ │
│                    │                      ▼                               │ │
│                    │  ┌────────────────────────────────────────────┐     │ │
│                    │  │           GOLD LAYER (Delta)               │     │ │
│                    │  │  17 tables: facts + dims + 117 KPI views  │     │ │
│                    │  └──────────────────┬─────────────────────────┘     │ │
│                    └──────────────────────┼──────────────────────────────┘ │
│                                           │                                    │
│                                           ▼                                    │
│                    ┌──────────────────────────────────────────────┐        │
│                    │          POWER BI (Direct Lake)               │        │
│                    │  Semantic model, RLS, dashboards              │        │
│                    └──────────────────────────────────────────────┘        │
│                                                                                  │
│  ┌──────────────────────────────────────────────────────────────────┐        │
│  │  SECURITY LAYER: Entra ID | RBAC | RLS (R55) | Encryption       │        │
│  └──────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Data Pipeline Design

The data pipeline consists of three Fabric notebooks, executed sequentially via a Data Pipeline. Each notebook reads from the preceding layer and writes to the next.

### 4.1 Notebook 1 — Bronze Loader

| Attribute | Detail |
|-----------|--------|
| **Name** | `nb_bronze_loader` |
| **Input** | `Files/Latest/*.csv` (lakehouse shortcut to network drive) |
| **Output** | `brz_<table>` Delta tables |
| **Mode** | Append |
| **Column types** | All STRING |
| **Execution** | Scheduled (daily) + on-demand |

**Description:**

The Bronze Loader reads each CSV file from the `Files/Latest/` shortcut and appends its contents to a corresponding Bronze Delta table. All columns are ingested as STRING to ensure maximum fidelity and prevent type-related ingestion failures. Each row receives ingestion metadata:

- `_ingestion_timestamp` — UTC timestamp of ingestion
- `_source_file` — name of the source CSV file
- `_ingestion_id` — unique batch identifier

The notebook iterates over a configured list of source CSV filenames and creates or appends to `brz_<source_name>` Delta tables. No transformations, filtering, or type casting occurs at this stage.

**Key design decisions:**

- Append mode preserves full history, enabling point-in-time reconstruction and audit.
- STRING-only typing defers schema enforcement to Silver, where it can be managed centrally via `schema_definition.csv`.
- The `Files/Latest/` shortcut abstracts the network drive location, allowing the source path to be changed without modifying the notebook.

### 4.2 Notebook 2 — Silver Formatter

| Attribute | Detail |
|-----------|--------|
| **Name** | `nb_silver_formatter` |
| **Input** | `brz_<table>` (Bronze Delta tables) |
| **Output** | `slv_<table>` (Silver Delta tables) |
| **Mode** | Overwrite (full rebuild) |
| **Schema source** | `schema_definition.csv` |
| **Execution** | After Bronze Loader completes |

**Description:**

The Silver Formatter reads each Bronze table and applies type casting according to the centrally managed `schema_definition.csv` file. This configuration file defines, for every source table and column:

- Target data type (INT, BIGINT, DECIMAL, DATE, TIMESTAMP, BOOLEAN, STRING)
- Primary key flag (used for deduplication)
- Nullable flag
- Default value (if applicable)

For each Bronze table, the notebook:

1. Reads the Bronze Delta table.
2. Casts each column to its defined type.
3. Deduplicates rows using the primary key columns (keeping the latest record by `_ingestion_timestamp`).
4. Applies basic cleaning (trimming whitespace, null handling, date normalisation).
5. Writes the result to `slv_<table>` in overwrite mode.

**Deduplication logic:**

Deduplication is performed by partitioning the dataset by primary key columns and selecting the row with the highest `_ingestion_timestamp` within each partition. This ensures that the most recently ingested record for each entity is retained.

### 4.3 Notebook 3 — Gold Translator

| Attribute | Detail |
|-----------|--------|
| **Name** | `nb_gold_translator` |
| **Input** | `slv_<table>` (Silver Delta tables) |
| **Output** | `fact_<name>`, `dim_<name>` (Gold Delta tables) + 117 KPI Spark SQL views |
| **Mode** | Overwrite (full rebuild) |
| **Execution** | After Silver Formatter completes |

**Description:**

The Gold Translator reads Silver tables and constructs the analytical model. It creates:

- **Fact tables:** Normalised transactional tables (e.g., `fact_referral_offer`, `fact_offer`, `fact_ipa`) containing measures and foreign keys to dimensions.
- **Dimension tables:** Descriptive tables (e.g., `dim_referral`, `dim_provider`, `dim_provider_home`) containing attributes for filtering and grouping.
- **KPI views:** 117 Spark SQL views, one per KPI, encapsulating the business logic for each metric. These views serve as the canonical definition of each KPI and are consumed by the Power BI semantic model.

**KPI view structure:**

Each KPI view is named `vw_kpi_<category>_<kpi_name>` and returns a single aggregated value (or a small result set when broken down by dimension). The view SQL is generated from a KPI definition catalogue that specifies:

- KPI name and description
- Category
- Source fact/dimension tables
- Aggregation logic (COUNT, SUM, AVG, etc.)
- Filter conditions
- Group-by dimensions

This approach ensures that KPI logic is version-controlled, testable, and identical across all consumers (Power BI, notebooks, API queries).

---

## 5. Gold Layer Analytical Model

### 5.1 Table Inventory

The Gold layer comprises **17 tables** — a mix of fact and dimension tables designed for star-schema analytics in Power BI.

#### Fact Tables (7)

| # | Table Name | Description |
|---|------------|-------------|
| 1 | `fact_referral_offer` | Core fact table linking referrals to provider offers. Contains measures such as offer count, offer status, and response time. Grain: one row per referral-offer combination. |
| 2 | `fact_offer` | Detailed offer-level facts including offer terms, placement type, and financial attributes. Grain: one row per offer. |
| 3 | `fact_ipa` | In-Placement Agreement facts. Captures IPA execution status, dates, and compliance indicators. Grain: one row per IPA record. |
| 4 | `fact_referral_person` | Person-level referral facts, linking individuals to referrals. Grain: one row per person per referral. |
| 5 | `fact_referral_category` | Categorisation facts for referrals (e.g., placement type, urgency, category codes). Grain: one row per referral-category assignment. |
| 6 | `fact_provider_message` | Provider messaging activity facts. Tracks message volume, response times, and engagement. Grain: one row per message. |
| 7 | `fact_referral_event_log` | Audit trail fact table. Captures all referral lifecycle events (creation, modification, status change, offer, acceptance, rejection). Grain: one row per event. Supports requirements R67–R70. |

#### Dimension Tables (10)

| # | Table Name | Description |
|---|------------|-------------|
| 8 | `dim_referral` | Referral dimension with attributes: referral ID, status, local authority, region, creation date, placement type, urgency level. |
| 9 | `dim_provider` | Provider dimension with attributes: provider ID, name, type, registration status, local authority, region. Supports provider registry KPIs (R25–R36). |
| 10 | `dim_provider_home` | Provider home dimension: home ID, provider ID, address, capacity, registered placements, Ofsted status. |
| 11 | `dim_provider_framework` | Provider framework dimension: framework ID, provider ID, framework name, start/end dates, status. Supports spot vs framework KPIs. |
| 12 | `dim_referral_gender` | Gender reference dimension for referral persons. |
| 13 | `dim_s3_file_metadata` | File metadata dimension: file name, source, upload timestamp, file type, size, checksum. Supports document compliance KPIs. |
| 14 | `dim_provider_document` | Provider document dimension: document ID, provider ID, document type, upload date, expiry date, compliance status. Supports R38–R49. |
| 15 | `dim_submission_documents` | Submission documents dimension: submission ID, referral ID, document list, submission timestamp, submitted by. |
| 16 | `dim_referral_provider_decline_reason` | Decline reason dimension: decline ID, referral ID, provider ID, reason code, reason description, decline timestamp. |
| 17 | `dim_offer_status` | Offer status dimension: status ID, status code, status description, active flag, sort order. |

### 5.2 KPI Summary — 117 KPIs across 14 Categories

| # | Category | KPI Count | Description |
|---|----------|-----------|-------------|
| 1 | Referral Volume | 14 | Total referrals, referrals by local authority, referrals by placement type, referral trends, year-over-year comparisons. |
| 2 | Provider Activity | 12 | Active providers, provider response rates, offer acceptance rates, provider engagement metrics. |
| 3 | Timebased | 2 | Average time from referral to offer, average time from offer to placement. |
| 4 | Spot vs Framework | 3 | Spot placement count, framework placement count, spot-to-framework ratio. |
| 5 | Referral Offers | 13 | Offer volume, offers by status, offer conversion rates, offer decline reasons, offer response times. |
| 6 | Provider Registry | 16 | Registered providers, providers by type, registration trends, compliance status, capacity metrics. Supports R25–R36. |
| 7 | Draft/Pending | 20 | Draft referrals, pending offers, pending IPAs, aged drafts, escalation indicators. |
| 8 | IPA Measures | 17 | IPA execution rate, IPA compliance, IPA cycle time, digitised IPA adoption, IPA exceptions. Supports R71–R72. |
| 9 | Out-of-Region | 3 | Out-of-region placements, out-of-region costs, out-of-region trend. |
| 10 | Document Compliance | 4 | Document completeness, expired documents, missing mandatory documents, compliance rate. Supports R38–R49. |
| 11 | Messaging | 3 | Message volume, average response time, unread message count. |
| 12 | Audit Trail | 2 | Event log completeness, modification tracking rate. Supports R67–R70. |
| 13 | Onboarding | 2 | Provider onboarding cycle time, onboarding completion rate. |
| 14 | Finance | 3 | Placement cost totals, cost per placement, outstanding payments. Supports R62. |
| | **Total** | **117** | |

### 5.3 Star Schema Relationships

The Gold layer follows a star-schema design:

- **`fact_referral_offer`** is the central fact table, with foreign keys to `dim_referral`, `dim_provider`, `dim_provider_home`, `dim_provider_framework`, `dim_offer_status`, and `dim_referral_provider_decline_reason`.
- **`fact_offer`** connects to `dim_provider` and `dim_offer_status`.
- **`fact_ipa`** connects to `dim_referral` and `dim_provider`.
- **`fact_referral_person`** connects to `dim_referral` and `dim_referral_gender`.
- **`fact_referral_event_log`** connects to `dim_referral`.
- **`fact_provider_message`** connects to `dim_provider`.
- **`fact_referral_category`** connects to `dim_referral`.
- **`dim_provider_document`** and **`dim_submission_documents`** connect to `dim_provider` and `dim_referral` respectively.
- **`dim_s3_file_metadata`** is a standalone dimension linked to document-related facts via file name.

---

## 6. Power BI Integration

### 6.1 Direct Lake Mode

The Power BI semantic model connects to Gold Delta tables using **Direct Lake mode**. This mode reads Delta tables directly from the Fabric OneLake storage without importing data into the Power BI model or requiring scheduled refreshes.

**Benefits:**

- **No refresh latency:** Data is read on-demand from Delta tables; updates to Gold are immediately available in reports.
- **Large dataset support:** Direct Lake can handle datasets larger than Power BI Pro import limits.
- **Reduced admin overhead:** No refresh schedule management, no refresh failure monitoring.
- **Automatic schema sync:** When Gold table schemas change, the semantic model can be updated to reflect new columns without full reimport.

**Considerations:**

- Direct Lake requires Power BI Premium or Fabric capacity.
- Complex DAX transformations should be pushed to the Gold layer as Spark SQL views to maintain query performance.
- The semantic model should use relationships defined in the Gold star schema rather than complex DAX cross-table logic.

### 6.2 Semantic Model

The Power BI semantic model is built on top of the Gold Delta tables and includes:

- **Imported tables:** All 17 Gold fact/dimension tables.
- **KPI measures:** 117 DAX measures, each mapped to the corresponding Spark SQL KPI view for validation. The DAX measures provide the user-facing names, formatting, and display folders.
- **Hierarchies:** Date hierarchies (year → quarter → month → date), provider hierarchies (provider → home), and referral hierarchies (local authority → region).
- **Calculation groups:** Time intelligence (YTD, QTD, MTD, prior period) implemented as a calculation group for consistent application across all measures.
- **Row-level security:** RLS roles for commissioner regional access (see Section 7).

### 6.3 Dashboard Pages

The Power BI report will include the following dashboard pages, aligned to functional roles:

| Page | Audience | Content |
|------|----------|---------|
| **Executive Overview** | Commissioners, Senior Leadership | KPI cards for referral volume, offer conversion, IPA compliance, out-of-region placements, finance summary. |
| **Referral Analytics** | Placement Officers (R11–R24) | Referral volume trends, by local authority, by placement type, by urgency. Draft/pending referrals, aged drafts. |
| **Provider Activity** | Placement Officers, Provider Managers (R25–R36) | Provider response rates, offer acceptance, active providers, provider registry, capacity. |
| **Offer Management** | Placement Officers | Offer volume, offers by status, decline reasons, offer response times, spot vs framework. |
| **IPA Compliance** | QA Officers (R38–R49, R71–R72) | IPA execution rate, compliance, cycle time, digitised IPA adoption, exceptions. |
| **Document Compliance** | QA Officers (R38–R49) | Document completeness, expired documents, missing mandatory documents. |
| **Finance Dashboard** | Finance Officers (R62) | Placement cost totals, cost per placement, outstanding payments, cost trends. |
| **Audit Trail** | QA Officers, Auditors (R67–R70) | Event log, modification tracking, data lineage. |
| **Commissioner View** | Commissioners (R51–R59) | Region-filtered view with RLS applied. Regional referral volume, provider performance, out-of-region placements, finance. |
| **Provider Onboarding** | Provider Managers | Onboarding cycle time, completion rate, registration trends. |
| **Messaging** | Placement Officers, Providers | Message volume, response times, unread messages. |

---

## 7. Security Architecture

### 7.1 Authentication — Entra ID (Azure AD)

All access to the Fabric workspace, Lakehouse, and Power BI semantic model is authenticated through **Microsoft Entra ID** (formerly Azure Active Directory). This provides:

- **Single sign-on (SSO):** Users access all platform components with their organisational credentials.
- **Multi-factor authentication (MFA):** Enforced for all users accessing sensitive child placement data.
- **Conditional access:** Policies restricting access to approved devices, IP ranges, and locations.
- **Token-based authentication:** Fabric APIs and notebook execution use Entra ID service principals with managed identities.

### 7.2 Role-Based Access Control (RBAC)

Fabric workspace roles control access to the Lakehouse, notebooks, and pipelines:

| Workspace Role | Assigned To | Permissions |
|----------------|-------------|-------------|
| **Admin** | Data Platform Team | Full control, including workspace settings and member management. |
| **Member** | Data Engineers | Create and manage notebooks, pipelines, and Lakehouse tables. Cannot manage workspace settings. |
| **Contributor** | Report Developers | Create and edit Power BI reports and semantic models. Cannot modify Lakehouse tables or notebooks. |
| **Viewer** | Commissioners, End Users | View Power BI reports. No access to Lakehouse or notebooks. |

### 7.3 Row-Level Security (RLS) — Regional Commissioner Access (R55)

Requirement R55 specifies that commissioners must only see data for their respective local authority or region. This is enforced through **row-level security** in the Power BI semantic model.

**Implementation:**

- **`dim_referral`** includes a `local_authority` column and a `region` column.
- **RLS roles** are defined for each of the 14 West Midlands local authorities (e.g., `RLS_Birmingham`, `RLS_Coventry`, `RLS_Wolverhampton`, etc.).
- Each RLS role applies a DAX filter: `[local_authority] = USERPRINCIPALNAME()` mapped via a security lookup table, or `[region] = "<region_name>"` for region-level roles.
- A **security mapping table** (`dim_security_mapping`) links Entra ID user principal names (UPNs) to their assigned local authority/region. This table is maintained by the platform admin and stored in the Gold layer.
- The RLS DAX expression uses `LOOKUPVALUE` to dynamically resolve the user's region from the mapping table:

```dax
[local_authority] =
LOOKUPVALUE(
    dim_security_mapping[local_authority],
    dim_security_mapping[user_principal_name],
    USERPRINCIPALNAME()
)
```

- RLS is applied at the semantic model level, ensuring that all dashboard pages, including the Commissioner View, are automatically filtered.

### 7.4 Data Encryption

| Layer | Encryption Method |
|-------|-------------------|
| **At rest (OneLake)** | Microsoft-managed AES-256 encryption. Customer-managed keys (CMK) available with Fabric capacity. |
| **In transit** | TLS 1.2+ for all connections (Fabric APIs, Power BI service, notebook execution). |
| **Network drive to Lakehouse** | TLS-secured shortcut connection. CSV files are transferred via the Fabric Files shortcut mechanism. |
| **Power BI service** | Data encrypted at rest in Power BI service. RLS filters applied before data reaches the client. |

### 7.5 Compliance and Data Protection

- **UK GDPR / Data Protection Act 2018:** Child placement data is classified as special category personal data. Access is restricted to authorised personnel with a legitimate need.
- **Audit logging:** All workspace access, notebook executions, and report views are logged in the Fabric activity log.
- **Data retention:** Bronze tables retain full append history for audit purposes. Silver and Gold tables are rebuilt on each run and reflect the current state. Retention policies for Bronze history will be defined in consultation with the data governance team.

---

## 8. Data Quality Framework

### 8.1 Overview

The data quality framework addresses the issues identified in the current V13.1 report, including inconsistent measure names, duplicate records, and schema drift. The framework operates across all three medallion layers.

### 8.2 Deduplication (Silver Layer)

Deduplication is performed in the Silver Formatter notebook using primary key columns defined in `schema_definition.csv`:

- **Method:** Partition by primary key columns, select the row with the maximum `_ingestion_timestamp`.
- **Scope:** Applied to every Silver table.
- **Monitoring:** The notebook logs the number of duplicate rows removed per table to a `dq_deduplication_log` table in the Gold layer.

### 8.3 Measure Name Correction (Gold Layer)

The current V13.1 Power BI report contains 90 measures with inconsistent naming conventions (e.g., `Total Referrals`, `total_referrals`, `[Ref Count]`). The Gold layer standardises all 117 KPIs using a consistent naming convention:

- **KPI view names:** `vw_kpi_<category>_<snake_case_name>`
- **DAX measure names:** `<PascalCase Name>` in display folders by category
- **Mapping:** A `kpi_definition_catalogue` table maps old V13.1 measure names to new standardised names, enabling traceability and validation.

### 8.4 Schema Enforcement (Silver Layer)

Schema enforcement is driven by `schema_definition.csv`, which defines:

- Column names and expected data types
- Primary key columns
- Nullable columns
- Default values

The Silver Formatter validates each Bronze column against the schema definition:

- **Type mismatch:** Records with uncastable values are flagged and logged; the value is set to NULL.
- **Missing columns:** If a Bronze table is missing an expected column, the notebook logs a warning and creates the column with NULL values.
- **Extra columns:** Unexpected columns in Bronze are retained in Silver with a `_extra_` prefix for investigation.

### 8.5 Data Quality Monitoring

A data quality monitoring table (`dq_monitoring`) is maintained in the Gold layer. Each pipeline run records:

| Metric | Description |
|--------|-------------|
| `table_name` | Silver or Gold table name |
| `run_timestamp` | Pipeline execution timestamp |
| `row_count_input` | Rows read from source (Bronze or Silver) |
| `row_count_output` | Rows written to target (Silver or Gold) |
| `duplicate_count` | Number of duplicate rows removed |
| `null_count_by_column` | JSON map of null counts per column |
| `type_cast_errors` | Number of type cast failures |
| `schema_warnings` | List of missing or extra columns |
| `status` | PASS / WARN / FAIL |

This table is exposed as a Power BI dashboard page for the data engineering team, enabling proactive monitoring of data quality trends.

### 8.6 Validation Gates

The pipeline includes validation gates between notebooks:

1. **Bronze → Silver gate:** Verify that all expected Bronze tables exist and have non-zero row counts. Halt pipeline if any expected table is missing.
2. **Silver → Gold gate:** Verify that all Silver tables have been written successfully and that primary key columns contain no NULLs. Halt pipeline if validation fails.
3. **Gold → Power BI gate:** Verify that all 17 Gold tables and 117 KPI views exist. Log warnings for any missing views.

---

## 9. Migration Strategy

### 9.1 Approach

The migration follows a **phased approach**: first achieve functional parity with the current V13.1 report, then enhance to deliver the full 117-KPI Gold model.

### 9.2 Phase 1 — Lift and Shift (Weeks 1–4)

**Objective:** Establish the Fabric Lakehouse pipeline with parity to the current 90-measure V13.1 report.

| Step | Activity | Deliverable |
|------|----------|-------------|
| 1.1 | Create Fabric workspace and Lakehouse | Workspace provisioned, Entra ID groups configured |
| 1.2 | Configure network drive shortcut (`Files/Latest/*.csv`) | Shortcut validated, CSV files accessible from notebooks |
| 1.3 | Deploy and configure `schema_definition.csv` | All source table schemas documented |
| 1.4 | Deploy Notebook 1 (Bronze Loader) | `brz_<table>` Delta tables created from CSV files |
| 1.5 | Deploy Notebook 2 (Silver Formatter) | `slv_<table>` Delta tables with typed columns and deduplication |
| 1.6 | Deploy Notebook 3 (Gold Translator) — V13.1 parity subset | Gold tables with the existing 90 measures |
| 1.7 | Build Power BI semantic model (Direct Lake) | Semantic model connected to Gold tables |
| 1.8 | Recreate V13.1 report pages in new workspace | Report pages matching V13.1 layout |
| 1.9 | User acceptance testing (UAT) | Sign-off from Placement Officers and Commissioners |
| 1.10 | Cutover: V13.1 report decommissioned | New report promoted to production |

### 9.3 Phase 2 — Enhance (Weeks 5–8)

**Objective:** Extend the Gold model to deliver all 117 KPIs and close the 17 functional gaps.

| Step | Activity | Deliverable |
|------|----------|-------------|
| 2.1 | Extend Gold Translator with 27 additional KPIs (117 total) | All 117 KPI Spark SQL views created |
| 2.2 | Add new Gold tables to support functional gaps (e.g., `fact_referral_event_log`, `dim_s3_file_metadata`) | 17 Gold tables fully populated |
| 2.3 | Implement RLS for commissioner regional access (R55) | RLS roles and security mapping table configured |
| 2.4 | Build enhanced dashboard pages (Executive Overview, Audit Trail, Commissioner View, etc.) | All 11 dashboard pages delivered |
| 2.5 | Implement data quality monitoring dashboard | `dq_monitoring` table and dashboard page live |
| 2.6 | Document KPI catalogue and functional requirement traceability | KPI definitions mapped to R1–R87 |
| 2.7 | UAT for enhanced report | Sign-off from all stakeholder groups |
| 2.8 | Production deployment | Enhanced report promoted to production |

### 9.4 Rollback Plan

- **Phase 1 rollback:** If UAT fails, the V13.1 report on the network drive remains operational. The Fabric workspace can be paused without impact.
- **Phase 2 rollback:** If enhanced KPIs fail validation, the Phase 1 Gold model (90 measures) remains available. New KPI views can be deployed individually without disrupting existing reports.
- **Data rollback:** Bronze tables maintain full append history, enabling point-in-time recovery. Silver and Gold tables are rebuilt on each run, so rolling back to a previous state requires re-running the pipeline with a prior Bronze snapshot.

### 9.5 Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Network drive shortcut connectivity issues | Medium | High | Monitor shortcut health; configure alerting on pipeline failure. |
| CSV schema drift (columns added/removed in source) | Medium | Medium | `schema_definition.csv` is centrally managed; Silver logs schema warnings. |
| Direct Lake performance with large fact tables | Low | Medium | Partition Gold Delta tables by date; push complex logic to Spark SQL views. |
| RLS misconfiguration exposes regional data | Low | High | Security review before production; test with non-admin accounts per role. |
| User adoption resistance | Medium | Low | Training sessions and parallel running during Phase 1. |

---

## 10. Technology Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Cloud Platform** | Microsoft Fabric | End-to-end data platform: Lakehouse, notebooks, pipelines, Power BI |
| **Storage** | OneLake (Delta Lake format) | Medallion layer storage (Bronze, Silver, Gold Delta tables) |
| **Data Ingestion** | Fabric Lakehouse Shortcut | Network drive CSV access via `Files/Latest/*.csv` |
| **Data Processing** | Fabric Notebooks (PySpark) | Bronze Loader, Silver Formatter, Gold Translator |
| **Pipeline Orchestration** | Fabric Data Pipeline | Sequential execution of notebooks with validation gates |
| **Schema Management** | `schema_definition.csv` (Lakehouse) | Centralised column type, primary key, and nullable definitions |
| **Analytical Model** | Gold Delta Tables + Spark SQL Views | 17 fact/dimension tables, 117 KPI views |
| **BI / Reporting** | Power BI (Direct Lake mode) | Semantic model, dashboards, RLS |
| **Semantic Modelling** | Power BI Desktop / XMLA endpoint | DAX measures, calculation groups, hierarchies |
| **Authentication** | Microsoft Entra ID (Azure AD) | SSO, MFA, conditional access |
| **Authorisation** | Fabric Workspace RBAC + Power BI RLS | Workspace roles, commissioner regional data filtering (R55) |
| **Encryption (at rest)** | AES-256 (Microsoft-managed / CMK) | OneLake and Power BI service encryption |
| **Encryption (in transit)** | TLS 1.2+ | All API, notebook, and report connections |
| **Source System** | PostgreSQL (7 schemas) | Production WMPP application database |
| **Source Data Format** | CSV (network drive) | Extract files from PostgreSQL, consumed by Bronze Loader |
| **Version Control** | Fabric Git Integration / Azure DevOps | Notebook, pipeline, and semantic model versioning |
| **Monitoring** | Fabric Activity Log + `dq_monitoring` table | Pipeline health, data quality, access auditing |
| **Data Quality** | PySpark (Silver notebook) + DQ monitoring dashboard | Deduplication, schema enforcement, type validation |

---

*End of Document*

**Document Control**

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 12 July 2026 | [Consultant Name] | Initial draft |
