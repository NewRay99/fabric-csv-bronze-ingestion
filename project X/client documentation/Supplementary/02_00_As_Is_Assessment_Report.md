# As-Is Assessment Report

## WMPP Power BI Dashboard — Current State Evaluation

| Field | Value |
|-------|-------|
| **Project** | WMPP — West Midlands Placement Portal |
| **Document Type** | As-Is Assessment Report |
| **Report Under Review** | WMPP PILOT DASHBOARD (V13.1) |
| **Report Author** | Hamant K Jakhu, Senior ICT Manager |
| **KPI Logic Document Date** | 23 June 2026 |
| **Assessment Date** | 12 July 2026 |
| **Prepared By** | Akhtar Miah |
| **Version** | 2.0 |
| **Classification** | Client Confidential |

---

## 0. Functional Requirement vs KPI Comparison Matrix

This table maps every functional requirement (R1–R96) from the WMPP Functional Specification
to the KPIs that address it, drawn from the KPI Reference Guide (`kpi_reference_guide.md`)
and the Measures Comparison Checklist (`measures_comparison_checklist.md`).

**Status legend:** ✅ Implemented · ⚠️ Partial · ❌ Missing · ℹ️ Non-functional / Feature / Security

### 0.1 Referral Volume & Placement Officer Requirements

| Req ID | Requirement | Stakeholder | Priority | KPI(s) | Status | Gap / Notes | Suggested Action |
|--------|-------------|-------------|----------|--------|--------|-------------|------------------|
| R1 | Place children with complex care needs | Placement Officer | High | KPI-01, KPI-08 | ✅ Implemented |  |  |
| R2 | Consider current incumbent solution | All | Low | — | ℹ️ Non-functional | Design constraint, no KPI required |  |
| R3 | Single regional platform (cross-boundary) | All | High | — | ℹ️ Non-functional | Architecture constraint, no direct KPI |  |
| R4 | Open source suitability | All | Low | — | ℹ️ Non-functional |  |  |
| R5 | Agile / MVP / backlog | All | Low | — | ℹ️ Non-functional |  |  |
| R6 | COTS preferred over bespoke | All | Low | — | ℹ️ Non-functional |  |  |
| R7 | APIs across WM IT ecosystem | All | High | — | ℹ️ Non-functional |  |  |
| R8 | Open-source API compliance | All | Low | — | ℹ️ Non-functional |  |  |
| R9 | Form pre-population (referral, OFSTED, auth) | Placement Officer | Medium | — | ℹ️ Feature | Data quality benefit, no dedicated KPI |  |
| R11 | Publish placement requirements to providers | Placement Officer | High | KPI-01, KPI-08 | ✅ Implemented |  |  |
| R12 | GDPR / DPA 2018 compliance for vulnerable-child data | All | High | — | ℹ️ Security | No dedicated KPI; covered by RLS (R55) |  |
| R13 | Filter by specialisms, placement type, placement status | Placement Officer | Medium | KPI-26, KPI-34 | ✅ Implemented |  |  |
| R14 | In-system messaging (auditable, prioritised, urgent) | Placement Officer | Medium | KPI-110, KPI-111, KPI-112 | ❌ Missing | Message table exists (fact_provider_message) but no KPI for volume, response time, or priority handling | Add Messages Sent, Avg Response Time, Priority Messages Unread measures |
| R15 | Digital info & signatures for IPA | Placement Officer | High | KPI-73, KPI-76, KPI-77 | ✅ Implemented |  |  |
| R16 | Priority information flagged in placement requests | Placement Officer | Medium | — | ℹ️ Feature | Visual flag, no dedicated measure |  |
| R17 | Placement info immediately available on accept | Placement Officer | High | KPI-75 | ✅ Implemented |  |  |
| R18 | Emergency placements: same-day, distinct ID, separate reporting & finance | Placement Officer | High | KPI-91, KPI-92, KPI-94 | ❌ Missing | No KPI distinguishes emergency from planned/spot. is_spot ≠ emergency. Statutory compliance risk. | Add Emergency Referrals and Emergency Placement Rate measures. Add is_emergency flag to fact_referral. |
| R19 | Update referrals; auto-notify providers | Placement Officer | Low | KPI-115 | ❌ Missing | No KPI for referral update frequency or notification delivery | Add Referral Updates per Day measure from referral audit trail |
| R20 | Full audit tracking (placements, IPA, signatures, approvals, negotiations) | Commissioner | Medium | KPI-113, KPI-114 | ❌ Missing | No audit trail KPIs exist | Add Audit Events by Type and IPA Signature Completion Rate measures |
| R21 | Auto-notify unsuccessful providers; optional rejection feedback | Placement Officer | Medium | — | ℹ️ Feature | Notification feature, no dedicated KPI |  |
| R22 | Out-of-region placements tagged; finance informed | Placement Officer | High | KPI-90 (partial), KPI-95, KPI-96 | ❌ Missing | Overlap Referrals measure exists but unclear if it tracks external (non-WM) placements | Add Out-of-Region Referrals measure with geographic tagging |
| R24 | Dashboard: status overview, provider updates, task mgmt, quick updates | Placement Officer | High | KPI-01–KPI-89 (85 measures) | ✅ Implemented |  |  |

### 0.2 Provider Requirements

| Req ID | Requirement | Stakeholder | Priority | KPI(s) | Status | Gap / Notes | Suggested Action |
|--------|-------------|-------------|----------|--------|--------|-------------|------------------|
| R25 | Quickly review detailed placement requests | Provider | High | KPI-11, KPI-12 | ✅ Implemented |  |  |
| R26 | Prioritise by match suitability, SOP, existing placements | Provider | High | KPI-19, KPI-20, KPI-37 | ✅ Implemented |  |  |
| R27 | Request additional info, raise queries, see responses | Provider | Medium | — | ℹ️ Feature | Communication feature, no dedicated KPI |  |
| R28 | Accept / reject / request further info | Provider | High | KPI-15, KPI-16, KPI-75 | ✅ Implemented |  |  |
| R29 | Streamlined offer process | Provider | Medium | — | ℹ️ Feature | Process efficiency, no dedicated KPI |  |
| R31 | Resolved requests auto-removed from provider views | Provider | Medium | — | ❌ Missing | No measure tracking resolved-but-not-hidden requests | Add Resolved Requests Visible measure for data quality |
| R32 | Matching by SOP and care specialisms | Provider | Medium | — | ℹ️ Feature | Matching algorithm, no dedicated KPI |  |
| R33 | Upload and manage placement documentation | Provider | Medium | — | ℹ️ Feature | Document management, no dedicated KPI |  |
| R34 | Emergency referrals identifiable and prioritised | Provider | High | KPI-91, KPI-94 | ❌ Missing | Same as R18 — emergency not distinguishable | See R18 action |
| R35 | Digitised IPA (review, approvals, signing, audit) | Provider | High | KPI-73–KPI-86 | ✅ Implemented |  |  |
| R36 | Dedicated view: referrals with outstanding offers / open offers | Provider | High | KPI-10, KPI-29 | ✅ Implemented |  |  |

### 0.3 QA Officer Requirements

| Req ID | Requirement | Stakeholder | Priority | KPI(s) | Status | Gap / Notes | Suggested Action |
|--------|-------------|-------------|----------|--------|--------|-------------|------------------|
| R38 | Record QA assessment outcomes against providers | QA Officer | Medium | — | ℹ️ Data entry | Assessment recording, no dedicated KPI |  |
| R39 | Desk-based research; identify missing documentation | QA Officer | Medium | — | ℹ️ Feature | Research workflow, no dedicated KPI |  |
| R41 | Apply advisory notices and flags (information notices, safeguarding) | QA Officer | High | KPI-97, KPI-98, KPI-99 | ❌ Missing | No KPI shows flagged provider counts or flag types | Add Providers with QA Flags, QA Flag Type Breakdown measures |
| R45 | SPOT providers upload registration documentation | QA Officer | Medium | — | ℹ️ Feature | Document upload, no dedicated KPI |  |
| R46 | QA intelligence for non-framework providers shared appropriately | QA Officer | Medium | KPI-46, KPI-47 | ✅ Implemented |  |  |
| R47 | Monitor documentation expiry; send reminders; highlight missing | QA Officer | High | KPI-100, KPI-101 | ❌ Missing | No KPI for documents nearing expiry or already expired | Add Documents Expiring (30 Days) and Documents Expired measures |
| R48 | Providers with incomplete docs excluded from referrals | QA Officer | High | KPI-102, KPI-103 | ❌ Missing | No measure showing providers blocked due to incomplete docs | Add Providers Blocked (Incomplete Docs) and Document Compliance Rate measures |
| R49 | Easily identify provider due diligence status | QA Officer | Medium | KPI-104 | ❌ Missing | No KPI for due diligence status | Add Providers by Due Diligence Status measure |

### 0.4 Commissioner & Finance Requirements

| Req ID | Requirement | Stakeholder | Priority | KPI(s) | Status | Gap / Notes | Suggested Action |
|--------|-------------|-------------|----------|--------|--------|-------------|------------------|
| R51 | Robust data model: placement records, market intelligence, value analysis | Commissioner | High | KPI-01–KPI-10, KPI-13, KPI-14, KPI-20 | ✅ Implemented |  |  |
| R52 | Accurate and customisable reporting | Commissioner | High | KPI-23, KPI-24 | ✅ Implemented |  |  |
| R53 | Data consistent, exportable, supports bespoke analysis | Commissioner | Medium | KPI-88 | ✅ Implemented |  |  |
| R54 | Capture reasons for declined placements | Commissioner | High | KPI-34 (partial), KPI-105 | ⚠️ Partial | Closed Referrals (by Reason) only covers offer-level decline codes, not full referral-level decline reasons | Expand to include referral_provider_decline_reason data |
| R55 | RBAC: commissioners access regional data, market-wide trends | Commissioner | Medium | — | ℹ️ Security | RLS requirement, not a measure. Verify RLS configured | Verify RLS configuration in semantic model |
| R57 | Emergency and planned placements separately reportable | Commissioner | High | KPI-91, KPI-93, KPI-94 | ❌ Missing | Same as R18 — emergency vs planned not splittable | See R18 action |
| R58 | Alert when framework changes during active referrals | Commissioner | High | KPI-106 | ❌ Missing | No KPI for framework change tracking during active referrals | Add Framework Changes During Active Referrals measure |
| R59 | Bulk provider onboarding supported | Commissioner | Low | KPI-116, KPI-117 | ❌ Missing | No KPI for onboarding pipeline | Add Providers in Onboarding Pipeline and Bulk Onboarding Success Rate measures |
| R62 | View completed placements, access IPAs, extract payment info | Finance Officer | High | KPI-107, KPI-108, KPI-109 | ❌ Missing | IPA funnel exists but no finance-specific views (weekly fees, payment methods, invoice details) | Add Total Weekly Fee Liability, Payment Method Breakdown, IPA Payment Status measures |

### 0.5 General, Non-Functional & Additional Requirements

| Req ID | Requirement | Stakeholder | Priority | KPI(s) | Status | Gap / Notes | Suggested Action |
|--------|-------------|-------------|----------|--------|--------|-------------|------------------|
| R67 | Support adding new frameworks | All | Medium | KPI-25, KPI-38 | ✅ Implemented |  |  |
| R68 | Frameworks configurable: display, hide, isolate by region | All | Medium | KPI-25, KPI-38 | ✅ Implemented |  |  |
| R69 | Robust analytical data model | All | High | — | ℹ️ Non-functional | Architecture constraint, no dedicated KPI |  |
| R70 | Auto-save across workflows | All | Low | — | ℹ️ Feature |  |  |
| R71 | Digitised IPA: review, approvals, signing, full audit | Provider | High | KPI-73–KPI-86 | ✅ Implemented |  |  |
| R72 | Digitise paper processes: workflow, auditable, trackable, lifecycle | All | Medium | — | ℹ️ Feature | Process digitisation, no dedicated KPI |  |
| R73 | Support future enhancements and Agile delivery | All | Low | — | ℹ️ Non-functional |  |  |
| R74 | COTS preferred | All | Low | — | ℹ️ Non-functional |  |  |
| R75 | High availability, scalability, fault tolerance, DR | All | High | — | ℹ️ Non-functional |  |  |
| R76 | Access restricted to authorised users | All | High | — | ℹ️ Security |  |  |
| R77 | Admin: user management, org onboarding, ownership transfer | All | Medium | — | ℹ️ Feature |  |  |
| R78 | RBAC and full auditing mandatory | All | High | — | ℹ️ Security |  |  |
| R79 | Break-glass access: controlled, auditable, emergency | All | Medium | — | ℹ️ Security |  |  |
| R80 | Fast document upload/retrieval, RBAC-protected access | All | Medium | — | ℹ️ Feature |  |  |
| R81 | WCAG 2.0/2.1/2.2 compliance | All | Medium | — | ℹ️ Non-functional |  |  |
| R82 | Fast response times, scalability, performance reporting | All | Medium | KPI-87 | ✅ Implemented |  |  |
| R83 | Migrate placements, purchases, providers, OFSTED, frameworks, active placements | All | High | — | ℹ️ Non-functional | Data migration, no dedicated KPI |  |
| R84 | Data integrity, retention, export, configurable policies | All | High | — | ℹ️ Non-functional |  |  |
| R85 | Deployment: FAQs, user guides, demos, support materials | All | Low | — | ℹ️ Non-functional |  |  |
| R86 | Device agnostic, browser compatible, mobile friendly | All | Medium | — | ℹ️ Non-functional |  |  |
| R87 | Incident management, issue reporting, SLAs | All | Medium | — | ℹ️ Non-functional |  |  |
| R88 | Modular growth, controlled change, product roadmaps | All | Low | — | ℹ️ Non-functional |  |  |
| R89 | Stakeholder demos, UAT, formal sign-off | All | Low | — | ℹ️ Non-functional |  |  |
| R90 | Hosting options, deployment models, cloud strategy | All | Low | — | ℹ️ Non-functional |  |  |
| R91 | Provider registration: company, services, homes, docs | Provider | High | KPI-40, KPI-41 | ✅ Implemented |  |  |
| R92 | LA review and approve/reject registrations | QA Officer | Medium | — | ℹ️ Feature |  |  |
| R93 | Placement officer: provider directory, services, homes, docs | Placement Officer | High | KPI-40–KPI-52 | ✅ Implemented |  |  |
| R94 | QA: search providers, apply/remove flags | QA Officer | Medium | KPI-97, KPI-98 (partial) | ⚠️ Partial | Flag application exists in UI but no KPI for flag counts or types | Add Providers with QA Flags and QA Flag Type Breakdown measures |
| R95 | Reflect Fostering Framework changes (Q3 2024) | All | Medium | KPI-42, KPI-51 | ✅ Implemented |  |  |
| R96 | Reflect Residential Framework 2.0 (Spring 2025) | All | Medium | KPI-43, KPI-49 | ✅ Implemented |  |  |

### 0.6 Summary Statistics

| Status | Count |
|--------|-------|
| ✅ Implemented | 23 |
| ⚠️ Partial | 2 |
| ❌ Missing | 15 |
| ℹ️ Non-functional | 20 |
| ℹ️ Feature | 14 |
| ℹ️ Security | 5 |
| ℹ️ Data entry | 1 |
| **Total Requirements** | **80** |

> **Note:** Requirements R2–R9, R29, R32–R33, R39, R45, R55, R69–R70, R72–R90 are non-functional,
> feature, or security requirements that do not map to a specific Power BI measure. The remaining
> requirements map to 90 existing + 27 new = 117 KPIs defined in the KPI Reference Guide.

---


## Table of Contents
1. [Functional Requirement vs KPI Comparison Matrix](#0-functional-requirement-vs-kpi-comparison-matrix)
2. [Executive Summary](#1-executive-summary)
3. [Current Architecture Overview](#2-current-architecture-overview)
4. [Report Inventory](#3-report-inventory)
5. [Measures Analysis](#4-measures-analysis)
6. [Functional Coverage Assessment](#5-functional-coverage-assessment)
7. [Key Findings](#6-key-findings)
8. [Risk Assessment](#7-risk-assessment)
9. [Recommendations Summary](#8-recommendations-summary)

---

## 2. Executive Summary

This report presents a comprehensive assessment of the current state of the WMPP Power BI dashboard (V13.1), which serves as the primary reporting and analytics layer for the West Midlands Placement Portal — a regional child placement and provider matching platform operating across 14 West Midlands local authorities.

The assessment evaluates the dashboard against the functional specification (87 requirements, R1–R87) defined in the KPI Logic Document and examines the underlying data architecture, report structure, measure inventory, and functional coverage across all stakeholder roles.

### Headline Findings

- **90 Power BI measures** have been implemented in the current dashboard, published in PBIP (Power BI Project) format with a semantic model defined in TMDL.
- **75 measures (83%)** are correctly implemented and map to defined functional requirements.
- **17 functional gaps** remain — requirements with no corresponding PBI measure — including critical gaps in emergency placements (R18), QA flags (R41), finance (R62), and document expiry tracking (R47/R48).
- **Finance Officer coverage stands at 0%** — no payment or fee KPIs exist in the dashboard.
- **QA Officer coverage stands at 25%** — significant safeguarding and quality assurance gaps.
- **5 duplicate measures** have been identified, indicating redundancy and potential maintenance risk.
- **Data architecture relies on CSV files stored on network drives**, with no lakehouse, no medallion architecture, and no bronze-silver-gold data separation — creating a fragile and non-resilient data pipeline.
- **Data quality issues** include a typographical error in a measure name ('Recieved') and duplicate measure definitions.

### Overall Assessment

The WMPP dashboard represents a substantial and largely functional reporting capability that has been developed iteratively to meet the operational needs of placement officers and providers. However, the current state presents material risks in three domains: **data pipeline resilience** (network drive dependency), **functional completeness** (17 missing requirements, particularly in QA and Finance), and **governance/maintainability** (duplicates, naming inconsistencies, absence of structured data architecture). These findings form the basis for the recommended modernisation roadmap detailed in the Gap Analysis document.

---

## 3. Current Architecture Overview

### 3.1 Data Source Layer

The WMPP dashboard draws its data from a **PostgreSQL database** containing the WMPP application schema. The database is organised across the following schemas:

| Schema | Purpose |
|--------|---------|
| `document` | Document management — compliance certificates, expiry tracking |
| `ipa` | In-Placement Agreement records and workflow |
| `offer` | Offer records — draft, pending, accepted, rejected |
| `provider` | Provider organisation master data |
| `refdata` | Reference/lookup data — categories, statuses, geographies |
| `referral` | Referral records — demand-side placement requests |
| `framework` | Framework agreements and provider-tier definitions |

### 3.2 Data Extraction and Ingestion

Data is extracted from PostgreSQL and exported as **CSV files** to **network drives**. These CSV files serve as the direct data source for the Power BI semantic model. The ingestion path is as follows:

```
PostgreSQL Database
       │
       ▼
  CSV Export (manual/scheduled)
       │
       ▼
  Network Drive (file share)
       │
       ▼
  Power BI Desktop — Import Mode
       │
       ▼
  Power BI Service (PBIP publish)
```

### 3.3 Key Architectural Characteristics

| Characteristic | Current State | Assessment |
|----------------|---------------|------------|
| **Data Storage** | CSV files on network drives | ❌ No lakehouse, no structured data lake |
| **Data Architecture** | Flat — no medallion layers | ❌ No bronze-silver-gold separation |
| **Ingestion Mode** | Power BI Import Mode | ⚠️ Suitable for small datasets; limits scalability |
| **Pipeline Automation** | Manual/semi-automated CSV export | ⚠️ Fragile; dependent on network drive availability |
| **Data Freshness** | Dependent on manual refresh cadence | ⚠️ No real-time or near-real-time capability |
| **Data Lineage** | Not formally documented | ❌ No end-to-end lineage tracking |
| **Version Control** | PBIP format with TMDL definition | ✅ Enables source control and ALM |
| **Monitoring/Alerting** | None | ❌ No data quality monitoring or pipeline alerting |
| **Medallion Architecture** | Not implemented | ❌ No bronze (raw), silver (cleansed), or gold (curated) layers |

### 3.4 Architectural Concerns

The reliance on network drives as the intermediary data store introduces multiple points of failure:

- **File availability risk**: Network drive outages, access permission changes, or file locks can prevent refresh.
- **No data validation**: CSV files are consumed directly without schema validation, type checking, or data quality gates.
- **No audit trail**: Changes to CSV files on network drives are not version-controlled or auditable.
- **No incremental loading**: Full file refresh on each cycle — no delta/incremental extraction.
- **No separation of concerns**: Raw, cleansed, and curated data are not differentiated — all logic resides in Power BI DAX measures.

---

## 4. Report Inventory

### 4.1 Report Overview

| Attribute | Value |
|-----------|-------|
| **Report Name** | WMPP PILOT DASHBOARD |
| **Version** | V13.1 |
| **Format** | PBIP (Power BI Project) |
| **Semantic Model Definition** | TMDL (Tabular Model Definition Language) |
| **Total Dashboard Pages** | 5 |
| **Total Measures** | 90 |
| **Data Connectivity Mode** | Import |
| **Author** | Hamant K Jakhu, Senior ICT Manager |

### 4.2 Dashboard Page Inventory

| # | Page Name | Purpose | Target Audience |
|---|-----------|---------|-----------------|
| 1 | **Referrals Overview** | Referral demand and status — volumes, trends, status distribution | Placement Officers, Commissioners |
| 2 | **Offers Overview** | Market response to referrals — offer volumes, acceptance rates, provider response | Placement Officers, Providers |
| 3 | **Pending Offers in Progress** | Ageing of pending offers — time-in-state analysis, bottleneck identification | Placement Officers, QA Officers |
| 4 | **Draft Offers** | Hidden backlog identification — draft offers not yet submitted | Placement Officers, Commissioners |
| 5 | **IPA Overview** | Workflow conversion funnel — referral-to-IPA conversion, stage-by-stage drop-off | Commissioners, Strategic Leads |

### 4.3 PBIP Format Assessment

My immediate tasks was to convert the report to a PBIP work format.
The report is now published in **PBIP (Power BI Project)** format, which is a positive:

- ✅ **Source control compatibility**: TMDL files are text-based and can be managed in Git.
- ✅ **ALM enablement**: Supports branch-based development, pull requests, and code review.
- ✅ **Semantic model visibility**: Full TMDL definition allows inspection of tables, columns, measures, relationships, and calculations.
- ✅ **Deployment automation**: PBIP supports CI/CD pipelines for automated publish to Power BI Service.

### 4.4 Semantic Model Structure

The semantic model contains tables sourced from CSV files corresponding to the PostgreSQL schemas. Measures are distributed across these tables and implement the business logic defined in the KPI Logic Document.

---

## 5. Measures Analysis

### 5.1 Summary

A total of **90 Power BI measures** were identified in the semantic model and assessed against the 87 functional requirements (R1–R87) defined in the KPI Logic Document. Each measure was classified into one of five categories:

| Category | Definition | Count | % of Total |
|----------|------------|-------|------------|
| **Implemented** | Measure exists and correctly maps to a functional requirement | 75 | 83.3% |
| **Partial** | Measure exists but does not fully satisfy the requirement | 2 | 2.2% |
| **Extra** | Measure exists in PBI but has no corresponding functional requirement | 4 | 4.4% |
| **Duplicate** | Measure duplicates the logic of another measure under a different name | 5 | 5.6% |
| **Missing** | Functional requirement exists but no PBI measure has been implemented | 17 | — |
| **Total PBI Measures** | | **90** | **100%** |

> **Note**: "Missing" measures are counted against requirements, not against the 90 PBI measures. The 17 missing requirements represent gaps where no measure has been built.

### 5.2 Implemented Measures (75)

The 75 implemented measures represent the core of the dashboard's analytical capability. These measures correctly implement the DAX logic defined in the KPI Logic Document and map to functional requirements across placement management, offer tracking, provider analytics, and IPA workflow conversion.

### 5.3 Partial Measures (2)

Two measures exist in the semantic model but do not fully satisfy their corresponding functional requirements. These measures require enhancement to close the identified coverage gap.

| Measure | Requirement | Gap Description |
|---------|-------------|-----------------|
| *[To be detailed in Gap Analysis document]* | — | Partial implementation — logic present but incomplete |
| *[To be detailed in Gap Analysis document]* | — | Partial implementation — logic present but incomplete |

### 5.4 Extra Measures (4)

Four measures exist in the Power BI semantic model but have no corresponding functional requirement in the KPI Logic Document. These may represent exploratory additions, legacy measures, or measures added outside the formal specification process.

| Measure | Status | Recommendation |
|---------|--------|----------------|
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |

### 5.5 Duplicate Measures (5)

Five measures have been identified as duplicates — they implement the same underlying DAX logic as another measure but under a different name. All identified duplicates relate to **pending offer age bucket** calculations.

| # | Duplicate Measure Pair | Logic | Issue |
|---|------------------------|-------|-------|
| 1 | *[Pair 1 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 2 | *[Pair 2 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 3 | *[Pair 3 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 4 | *[Pair 4 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 5 | *[Pair 5 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |

> **Impact**: Duplicate measures create maintenance burden (changes must be applied in multiple places), increase the risk of logic divergence over time, and clutter the semantic model.

### 5.6 Missing Measures (17)

Seventeen functional requirements have no corresponding Power BI measure. These are prioritised by business criticality:

#### High Priority (8)

| # | Requirement | Description | Stakeholder | Impact |
|---|-------------|-------------|-------------|--------|
| 1 | R18 | Emergency placement tracking | Placement Officer | Critical — safeguarding-relevant |
| 2 | R22 | Out-of-region placements | Placement Officer | Critical — cross-boundary visibility |
| 3 | R41 | QA flags / quality alerts | QA Officer | Critical — safeguarding |
| 4 | R47 | Document expiry tracking (certificates) | QA Officer | Critical — compliance |
| 5 | R48 | Document expiry tracking (insurance) | QA Officer | Critical — compliance |
| 6 | R62 | Finance / payment KPIs | Finance Officer | Critical — financial oversight |
| 7 | *[Additional high-priority gap]* | — | — | — |
| 8 | *[Additional high-priority gap]* | — | — | — |

#### Medium Priority (6)

| # | Requirement | Description | Stakeholder | Impact |
|---|-------------|-------------|-------------|--------|
| 9–14 | *[6 medium-priority requirements]* | — | — | Moderate operational impact |

#### Low Priority (3)

| # | Requirement | Description | Stakeholder | Impact |
|---|-------------|-------------|-------------|--------|
| 15–17 | *[3 low-priority requirements]* | — | — | Limited operational impact |

> **Detailed requirement-by-requirement analysis** is provided in the Gap Analysis document (03_Gap_Analysis_Report.md).

---

## 6. Functional Coverage Assessment

### 6.1 Coverage by Stakeholder Role

The 87 functional requirements (R1–R87) are grouped by stakeholder role. The table below shows the number of requirements, implemented measures, and coverage percentage for each role.

| Stakeholder Role | Requirements | Implemented Measures | Coverage % | Assessment |
|-----------------|-------------|---------------------|------------|------------|
| **Placement Officer** (R11–R24) | 14 | 11 | **79%** | ✅ Good — minor gaps |
| **Provider** (R25–R36) | 12 | 10 | **83%** | ✅ Good — minor gaps |
| **QA Officer** (R38–R49) | 8 | 2 | **25%** | 🔴 Critical — safeguarding gaps |
| **Commissioner** (R51–R59) | 9 | 5 | **56%** | ⚠️ Moderate — strategic gaps |
| **Finance Officer** (R62) | 1 | 0 | **0%** | 🔴 Critical — no coverage |
| **General** (R67–R70) | 4 | 3 | **75%** | ✅ Acceptable |
| **Digitised IPA** (R71–R72) | 2 | 2 | **100%** | ✅ Complete |
| **Overall** | **50** | **33** | **66%** | ⚠️ Needs improvement |

### 6.2 Coverage Analysis

#### Strengths

- **Digitised IPA (100%)**: Full coverage of the IPA digitisation workflow — the most recently developed functional area.
- **Provider (83%)**: Strong coverage of provider-related analytics, reflecting the dashboard's operational focus.
- **Placement Officer (79%)**: Good coverage of core placement management functionality, with gaps in emergency and out-of-region placements.

#### Critical Gaps

- **Finance Officer (0%)**: Complete absence of financial KPIs. No measures exist for payment tracking, fee analysis, or cost-per-placement. This is a critical gap given the financial oversight responsibilities of the Finance Officer role.
- **QA Officer (25%)**: Only 2 of 8 QA requirements are implemented. Missing measures include QA flags (R41), document expiry tracking (R47/R48), and other safeguarding-relevant KPIs. This represents a significant risk to quality assurance and compliance monitoring.

#### Moderate Gaps

- **Commissioner (56%)**: Strategic-level analytics are partially covered but lack completeness for full commissioner decision support.

---

## 7. Key Findings

### 7.1 Network Drive Dependency — Critical Data Pipeline Risk

**Finding**: The entire data pipeline relies on CSV files stored on network drives. There is no lakehouse, no medallion architecture, and no structured data ingestion framework.

**Implications**:
- Single point of failure — network drive unavailability breaks all reporting
- No data validation or quality gates between source and semantic model
- No audit trail for data changes
- No incremental loading — full refresh on each cycle
- Limited scalability as data volumes grow
- No disaster recovery or data lineage

### 7.2 Missing KPIs — 17 Functional Gaps

**Finding**: 17 functional requirements defined in the KPI Logic Document have no corresponding Power BI measure.

**Critical missing KPIs include**:
- **Emergency placements (R18)**: No visibility of emergency placement activity — a safeguarding concern
- **Out-of-region placements (R22)**: No tracking of placements made outside the 14 West Midlands authorities
- **QA flags (R41)**: No quality alert mechanism in the dashboard
- **Document expiry (R47/R48)**: No tracking of expiring compliance certificates or insurance documents
- **Finance (R62)**: No payment or fee-related KPIs whatsoever

### 7.3 QA Officer Coverage at 25% — Safeguarding Gap

**Finding**: Only 2 of 8 QA Officer requirements are implemented in the dashboard.

**Implications**:
- Quality assurance and safeguarding teams lack dashboard visibility
- Compliance certificate and insurance expiry are not tracked
- No proactive alerting for QA issues
- Risk of non-compliance with regulatory requirements

### 7.4 Finance Officer Coverage at 0% — Financial Oversight Gap

**Finding**: No measures exist for the Finance Officer role (R62).

**Implications**:
- No visibility of placement costs, fees, or payment status
- Finance team cannot use the dashboard for financial planning or reconciliation
- No cost-per-placement or cost-per-provider analytics
- Gap between operational and financial reporting

### 7.5 Duplicate Measures — Maintenance and Governance Risk

**Finding**: 5 duplicate measures have been identified, all related to pending offer age bucket calculations.

**Implications**:
- Maintenance burden — logic changes must be applied in multiple places
- Risk of logic divergence over time if duplicates are updated independently
- Semantic model clutter — 5 measures serving no unique purpose
- Indicates absence of formal code review or measure governance process

### 7.6 Data Quality Issues — Typographical Errors

**Finding**: A typographical error was identified in a measure name — 'Recieved' (should be 'Received').

**Implications**:
- Unprofessional appearance in the Power BI field list
- Potential confusion for report developers and consumers
- Indicates absence of naming convention enforcement or code review
- Suggests informal development practices

### 7.7 No Medallion Architecture — No Data Separation

**Finding**: There is no bronze-silver-gold data architecture. All transformation logic resides in DAX measures within the Power BI semantic model.

**Implications**:
- No separation of raw, cleansed, and curated data
- Data quality issues in source CSVs propagate directly to the dashboard
- No reusable data assets outside Power BI
- Limits ability to serve other consumers (e.g., Excel, other BI tools, data science)

### 7.8 PBIP Format — Positive Finding

**Finding**: The report is published in PBIP format with TMDL semantic model definition.

**Benefits**:
- Enables source control and version history
- Supports branch-based development and code review
- Facilitates CI/CD deployment automation
- Provides full transparency of semantic model logic

---

## 8. Risk Assessment

The following risk assessment evaluates the key risks identified in the As-Is state. Risks are rated using a standard impact-likelihood matrix.

**Rating Scale**:

- **Impact**: Low (1) / Medium (2) / High (3) / Critical (4)
- **Likelihood**: Rare (1) / Unlikely (2) / Possible (3) / Likely (4)
- **Severity** = Impact × Likelihood (1–16)

| # | Risk | Description | Impact | Likelihood | Severity | Rating |
|---|------|-------------|--------|------------|----------|--------|
| 1 | **Network drive failure** | Network drive unavailability causes complete reporting outage — no fallback or alternative data source | Critical (4) | Likely (4) | **16** | 🔴 Extreme |
| 2 | **No data validation** | CSV files consumed without schema validation or quality checks — data errors propagate to dashboard undetected | High (3) | Likely (4) | **12** | 🔴 High |
| 3 | **Missing emergency placement KPI (R18)** | Emergency placements not tracked in dashboard — safeguarding visibility gap | Critical (4) | Possible (3) | **12** | 🔴 High |
| 4 | **Finance coverage at 0% (R62)** | No financial KPIs — Finance team has no dashboard support | High (3) | Likely (4) | **12** | 🔴 High |
| 5 | **QA coverage at 25% (R38–R49)** | Safeguarding and compliance gaps — QA officers lack dashboard visibility | Critical (4) | Possible (3) | **12** | 🔴 High |
| 6 | **Document expiry not tracked (R47/R48)** | Expiring compliance certificates and insurance not monitored — regulatory non-compliance risk | High (3) | Possible (3) | **9** | ⚠️ Medium |
| 7 | **Out-of-region placements not tracked (R22)** | Cross-boundary placements invisible to commissioners and placement officers | High (3) | Possible (3) | **9** | ⚠️ Medium |
| 8 | **Duplicate measures (5)** | Redundant measures create maintenance burden and logic divergence risk | Medium (2) | Likely (4) | **8** | ⚠️ Medium |
| 9 | **No medallion architecture** | Absence of bronze-silver-gold separation limits scalability, reusability, and data governance | High (3) | Unlikely (2) | **6** | ⚠️ Medium |
| 10 | **Typographical errors in measure names** | 'Recieved' typo — unprofessional, indicates lack of code review | Low (1) | Likely (4) | **4** | ℹ️ Low |
| 11 | **No pipeline monitoring/alerting** | No automated monitoring of data refresh success/failure — issues may go undetected | High (3) | Possible (3) | **9** | ⚠️ Medium |
| 12 | **No incremental loading** | Full refresh on each cycle — performance degradation as data volumes grow | Medium (2) | Possible (3) | **6** | ⚠️ Medium |
| 13 | **Extra measures without requirements (4)** | Measures exist outside the formal specification — uncontrolled scope creep | Low (1) | Possible (3) | **3** | ℹ️ Low |
| 14 | **No data lineage documentation** | End-to-end lineage not documented — difficult to trace data from source to dashboard | Medium (2) | Likely (4) | **8** | ⚠️ Medium |

### Risk Heat Map Summary

| Severity Range | Rating | Count |
|----------------|--------|-------|
| 12–16 | 🔴 Extreme/High | 5 |
| 6–11 | ⚠️ Medium | 7 |
| 1–5 | ℹ️ Low | 2 |

---

## 9. Recommendations Summary

The following recommendations provide a high-level direction for addressing the findings of this assessment. Detailed analysis, prioritisation, and implementation guidance are provided in the Gap Analysis document (03_Gap_Analysis_Report.md).

### 9.1 Data Architecture Modernisation

- **Migrate from network drive CSV to Fabric Lakehouse**: Establish a OneLake-based data store with bronze (raw), silver (cleansed), and gold (curated) layers.
- **Implement automated ingestion pipeline**: Replace manual CSV export with automated data pipeline (e.g., Fabric Data Factory, Azure Data Factory) with scheduling and monitoring.
- **Introduce data quality gates**: Validate data at each medallion layer transition — schema checks, null checks, referential integrity.
- **Enable incremental loading**: Move from full refresh to incremental/delta loading for scalability.

### 9.2 Functional Gap Closure

- **Prioritise high-priority missing measures (8)**: Implement emergency placements (R18), out-of-region (R22), QA flags (R41), document expiry (R47/R48), and finance KPIs (R62) as immediate priorities.
- **Address QA Officer coverage (25% → target 90%)**: Close safeguarding and compliance gaps.
- **Address Finance Officer coverage (0% → target 100%)**: Build payment, fee, and cost analytics.
- **Review partial measures (2)**: Enhance to full requirement satisfaction.
- **Review extra measures (4)**: Confirm whether formal requirements should be created or measures removed.

### 9.3 Governance and Quality

- **Eliminate duplicate measures (5)**: Consolidate into single canonical measures; update report visuals to reference canonical names.
- **Fix typographical errors**: Correct 'Recieved' → 'Received' and audit all measure names for spelling/convention compliance.
- **Establish naming conventions**: Define and enforce DAX measure naming conventions (e.g., PascalCase, standard prefixes).
- **Implement code review process**: Leverage PBIP/Git workflow for pull-request-based code review on all semantic model changes.
- **Document data lineage**: Create end-to-end lineage documentation from PostgreSQL schemas through to dashboard visuals.

### 9.4 Monitoring and Operations

- **Implement pipeline monitoring**: Automated alerting on refresh failure, data quality anomalies, and pipeline latency.
- **Establish refresh cadence SLA**: Define and publish expected data freshness.
- **Create operational runbook**: Document troubleshooting steps for common pipeline and dashboard issues.

### 9.5 Recommendation Prioritisation

| Priority | Recommendation | Timeline |
|----------|----------------|----------|
| **P1 — Immediate** | Migrate data source from network drive to Fabric Lakehouse (bronze layer) | Phase 1 |
| **P1 — Immediate** | Implement high-priority missing measures (emergency, QA, finance, document expiry) | Phase 1 |
| **P2 — Short-term** | Eliminate duplicates, fix typos, establish naming conventions | Phase 2 |
| **P2 — Short-term** | Build silver and gold medallion layers with data quality gates | Phase 2 |
| **P3 — Medium-term** | Implement pipeline monitoring, alerting, and operational runbooks | Phase 3 |
| **P3 — Medium-term** | Close medium and low priority functional gaps | Phase 3 |

---

## Appendix A: Document References

| # | Document | Author | Date |
|---|----------|--------|------|
| 1 | KPI Logic Document | Hamant K Jakhu, Senior ICT Manager | 23 June 2026 |
| 2 | WMPP PILOT DASHBOARD (V13.1) — Power BI Report | Hamant K Jakhu | — |
| 3 | Measures Comparison Checklist | [Assessment Team] | July 2026 |
| 4 | Gap Analysis Report (03_Gap_Analysis_Report.md) | Akhtar Miah | 29 July 2026 |

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| **PBIP** | Power BI Project — file format enabling source control and ALM for Power BI reports |
| **TMDL** | Tabular Model Definition Language — text-based representation of semantic model |
| **Medallion Architecture** | Data design pattern with bronze (raw), silver (cleansed), gold (curated) layers |
| **Lakehouse** | Data architecture combining lake storage with warehouse query capabilities |
| **OneLake** | Microsoft Fabric's unified data lake storage |
| **IPA** | In-Placement Agreement — formal agreement record in the WMPP workflow |
| **WMPP** | West Midlands Placement Portal — regional child placement platform |
| **Import Mode** | Power BI data connectivity mode where data is cached in-memory |

---

*End of Report*

*This document is classified as Client Confidential and is intended solely for the use of authorised project stakeholders. Unauthorised distribution is prohibited.*
