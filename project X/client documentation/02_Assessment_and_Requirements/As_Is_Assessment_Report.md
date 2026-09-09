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
| **Prepared By** | [Consultant Name] |
| **Version** | 1.0 |
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
> requirements map to 90 existing + 27 new = 117 KPIs itemised in [§4.7 KPI Calculation Inventory](#47-kpi-calculation-inventory-as-is).

---

## Table of Contents

1. [Functional Requirement vs KPI Comparison Matrix](#0-functional-requirement-vs-kpi-comparison-matrix)
2. [Executive Summary](#1-executive-summary)
2. [Current Architecture Overview](#2-current-architecture-overview)
3. [Report Inventory](#3-report-inventory)
4. [Measures Analysis](#4-measures-analysis)
   - 4.7 [KPI Calculation Inventory (As-Is)](#47-kpi-calculation-inventory-as-is)
5. [Functional Coverage Assessment](#5-functional-coverage-assessment)
6. [Key Findings](#6-key-findings)
7. [Risk Assessment](#7-risk-assessment)
8. [Recommendations Summary](#8-recommendations-summary)

---

## 1. Executive Summary

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

## 2. Current Architecture Overview

### 2.1 Data Source Layer

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

### 2.2 Data Extraction and Ingestion

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

### 2.3 Key Architectural Characteristics

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

### 2.4 Architectural Concerns

The reliance on network drives as the intermediary data store introduces multiple points of failure:

- **File availability risk**: Network drive outages, access permission changes, or file locks can prevent refresh.
- **No data validation**: CSV files are consumed directly without schema validation, type checking, or data quality gates.
- **No audit trail**: Changes to CSV files on network drives are not version-controlled or auditable.
- **No incremental loading**: Full file refresh on each cycle — no delta/incremental extraction.
- **No separation of concerns**: Raw, cleansed, and curated data are not differentiated — all logic resides in Power BI DAX measures.

---

## 3. Report Inventory

### 3.1 Report Overview

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

### 3.2 Dashboard Page Inventory

| # | Page Name | Purpose | Target Audience |
|---|-----------|---------|-----------------|
| 1 | **Referrals Overview** | Referral demand and status — volumes, trends, status distribution | Placement Officers, Commissioners |
| 2 | **Offers Overview** | Market response to referrals — offer volumes, acceptance rates, provider response | Placement Officers, Providers |
| 3 | **Pending Offers in Progress** | Ageing of pending offers — time-in-state analysis, bottleneck identification | Placement Officers, QA Officers |
| 4 | **Draft Offers** | Hidden backlog identification — draft offers not yet submitted | Placement Officers, Commissioners |
| 5 | **IPA Overview** | Workflow conversion funnel — referral-to-IPA conversion, stage-by-stage drop-off | Commissioners, Strategic Leads |

### 3.3 PBIP Format Assessment

The report is published in **PBIP (Power BI Project)** format, which is a positive finding:

- ✅ **Source control compatibility**: TMDL files are text-based and can be managed in Git.
- ✅ **ALM enablement**: Supports branch-based development, pull requests, and code review.
- ✅ **Semantic model visibility**: Full TMDL definition allows inspection of tables, columns, measures, relationships, and calculations.
- ✅ **Deployment automation**: PBIP supports CI/CD pipelines for automated publish to Power BI Service.

### 3.4 Semantic Model Structure

The semantic model contains tables sourced from CSV files corresponding to the PostgreSQL schemas. Measures are distributed across these tables and implement the business logic defined in the KPI Logic Document.

---

## 4. Measures Analysis

### 4.1 Summary

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

### 4.2 Implemented Measures (75)

The 75 implemented measures represent the core of the dashboard's analytical capability. These measures correctly implement the DAX logic defined in the KPI Logic Document and map to functional requirements across placement management, offer tracking, provider analytics, and IPA workflow conversion.

### 4.3 Partial Measures (2)

Two measures exist in the semantic model but do not fully satisfy their corresponding functional requirements. These measures require enhancement to close the identified coverage gap.

| Measure | Requirement | Gap Description |
|---------|-------------|-----------------|
| *[To be detailed in Gap Analysis document]* | — | Partial implementation — logic present but incomplete |
| *[To be detailed in Gap Analysis document]* | — | Partial implementation — logic present but incomplete |

### 4.4 Extra Measures (4)

Four measures exist in the Power BI semantic model but have no corresponding functional requirement in the KPI Logic Document. These may represent exploratory additions, legacy measures, or measures added outside the formal specification process.

| Measure | Status | Recommendation |
|---------|--------|----------------|
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |
| *[To be detailed in Gap Analysis document]* | No corresponding requirement | Review for retention or removal |

### 4.5 Duplicate Measures (5)

Five measures have been identified as duplicates — they implement the same underlying DAX logic as another measure but under a different name. All identified duplicates relate to **pending offer age bucket** calculations.

| # | Duplicate Measure Pair | Logic | Issue |
|---|------------------------|-------|-------|
| 1 | *[Pair 1 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 2 | *[Pair 2 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 3 | *[Pair 3 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 4 | *[Pair 4 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |
| 5 | *[Pair 5 — pending offer age bucket]* | Same age-bucket calculation | Redundant definition |

> **Impact**: Duplicate measures create maintenance burden (changes must be applied in multiple places), increase the risk of logic divergence over time, and clutter the semantic model.

### 4.6 Missing Measures (17)

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

> **Detailed requirement-by-requirement analysis** is provided in the Gap Analysis document (03_Gap_Analysis_Report.md). The full 117-KPI calculation inventory — requirement IDs, source tables, calculation logic and PBI measure names — follows in [§4.7](#47-kpi-calculation-inventory-as-is).

### 4.7 KPI Calculation Inventory (As-Is)

The table below is the complete as-is KPI inventory for the V13.1 pilot dashboard: every KPI with its functional requirement IDs (from the WMPP Functional Specification), source tables, calculation logic and Power BI measure name. It is ported from `Supplementary/02_01_As_Is_KPI.md` so that the assessment report is self-contained; the supplementary copy remains the historic original.

#### 4.7.1 Table mapping — Silver-era model to Gold-era objects (as assessed)

| Model table | Source | Schema definition table | Functional area |
|---|---|---|---|
| fact_referral_offer | referral_provider | referral.referral_provider | Referral → Provider mapping |
| fact_offer | offer | offer.offer | Provider offers |
| fact_ipa | ipa | ipa.ipa | Individual Placement Agreements |
| fact_referral | referral | referral.referral | Referral header |
| dim_provider | provider | provider.provider | Provider master |
| dim_provider_home | provider_home | provider.provider_home | Provider homes |
| dim_provider_framework | provider_framework | provider.provider_framework | Provider-framework link |
| fact_referral_person | person | referral.person | Child demographics |
| fact_referral_category | referral_category | referral.referral_category | Referral categories |
| fact_provider_message | referral_provider_message | referral.referral_provider_message | Inter-party messages |
| fact_referral_gender | person | referral.person | Gender aggregation |
| fact_referral_event_log | referral_event_log | referral.referral_event_log | Audit trail |
| dim_s3_file_metadata | s3_file_metadata | document.s3_file_metadata | Document metadata |
| dim_provider_document | provider_document | provider.provider_document | Provider docs |
| dim_submission_documents | submission_documents | provider.submission_documents | Onboarding docs |
| fact_referral_provider_decline_reason | referral_provider_decline_reason | referral.referral_provider_decline_reason | Decline reasons |
| dim_offer_status | offer (derived) | offer.offer | Offer status lookup |

> These are the table names used by the assessed V13.1 model. They are **not** the active notebook-created Gold v02 objects — see `04_Data_and_Reporting/KPI_Reference_Guide.md` for the current mapping.

#### 4.7.2 KPI inventory by report section

##### Section 1 — Referral Volume KPIs

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-01 | [R24,R51] | Total Referrals | R24 dashboard referral status overview; R51 robust data model | gold.dim_referral | COUNT(DISTINCT referral_id) WHERE status IS NOT NULL | Total Referrals |
| KPI-02 | [R24,R36] | Referrals With Offers | R24 referral status; R36 outstanding offers | gold.dim_referral + gold.fact_referral_offer | COUNT DISTINCT referrals with valid offers | Referrals With Offers |
| KPI-03 | [R24,R36] | Referrals Awaiting Offer | R24 referral status; R36 outstanding offers | gold.dim_referral, gold.fact_referral_offer | Open/Under Offer referrals without valid offer | Referrals Awaiting Offer |
| KPI-04 | [R51] | Male Referrals | R51 demographic monitoring | gold.fact_referral_person | Gender='M' | Male Referrals |
| KPI-05 | [R51] | Female Referrals | R51 demographic monitoring | gold.fact_referral_person | Gender='F' | Female Referrals |
| KPI-06 | [R51] | Other Referrals | R51 demographic monitoring | gold.fact_referral_person | Gender not M/F | Other Referrals |
| KPI-07 | [R51] | Total Gendered Referrals | R51 demographic monitoring | gold.fact_referral_person | Sum of gender counts | Total Gendered Referrals |
| KPI-08 | [R24] | Referrals Not Yet Closed (Created in Period) | R24 dashboard | gold.dim_referral | Status not Closed/Cancelled | Referrals Not Yet Closed (Created in Period) |
| KPI-09 | [R24,R51] | Referrals With Offers (Created in Period) | R24 dashboard; R51 reporting | gold.dim_referral + gold.fact_referral_offer | KPI-02 filtered by created period | Referrals With Offers (Created in Period) |
| KPI-10 | [R51] | Total Referrals That Received Offers | R51 referral offer rate | gold.dim_referral + gold.fact_referral_offer | Referrals having valid offer | Total Referrals That Received Offers |

##### Section 2 — Provider Activity

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-11 | [R25,R26] | No. Providers Who Made Offers | R25 review requests; R26 prioritise requests | gold.fact_offer + gold.fact_referral_offer | Distinct providers with offers | No. Providers Who Made Offers |
| KPI-12 | [R25-R29] | Total Offers Made Historically | Provider offer management | gold.fact_offer | Distinct offers excluding Draft | Total Offers Made Historically |
| KPI-13 | [R51] | Avg Offers per Referral (Under Offer) | R51 market intelligence | gold.fact_offer + gold.fact_referral_offer | Offers / Referrals | Avg Offers per Referral Under Offer |
| KPI-14 | [R51] | Avg Offers per Provider (Under Offer) | R51 market intelligence | gold.fact_offer + gold.fact_referral_offer | Offers / Providers | Avg Offers per Provider (Under Offer) |
| KPI-15 | [R28] | Successful Offers (Under Offer Referrals) | R28 accept placements | gold.fact_offer | Accepted offers | Successful Offers (Under Offer Referrals) |
| KPI-16 | [R28] | Unsuccessful Offers (Under Offer Referrals) | R28 reject placements | gold.fact_offer | Declined/Rejected/Withdrawn offers | Unsuccessful Offers (Under Offer Referrals) |
| KPI-17 | [R24] | Offers in Draft (Under Offer Referrals) | R24 dashboard tasks | gold.fact_offer | Draft offers | Offers in Draft (Under Offer Referrals) |
| KPI-18 | [R24] | Pending Offers (Under Offer Referrals) | R24 dashboard tasks | gold.fact_offer | Pending offers | Pending Offers (Under Offer Referrals) |
| KPI-19 | [R24,R26] | Active Referrals With Provider Engagement | Dashboard and prioritisation | gold.dim_referral + gold.fact_referral_offer | Active referrals with offer activity | Active Referrals With Provider Engagement |
| KPI-20 | [R24,R26] | Active Referral Engagement Rate | Dashboard and prioritisation | Same as KPI-19 | KPI-19 / Active referrals | Active Referral Engagement Rate |
| KPI-21 | [R24,R26] | Active Awaiting Offers (Engaged) | Dashboard and prioritisation | dim_referral + referral_offer | Open referrals with engagement | Active Awaiting Offers (Engaged) |
| KPI-22 | [R24,R26] | Active Awaiting Offers (No Engagement) | Dashboard and prioritisation | dim_referral + referral_offer | Open referrals without engagement | Active Awaiting Offers (No Engagement) |

##### Section 3 — Time-based

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-23 | [R24,R52] | Referrals This Month | Dashboard; reporting | gold.dim_referral | Created current month | Referrals This Month |
| KPI-24 | [R52] | Referrals This FY | Reporting | gold.dim_referral | Created current FY | Referrals This FY |

##### Section 4 — Spot vs Framework

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-25 | [R67,R68] | Total Offers Made | Framework management | gold.fact_offer + gold.fact_referral_offer | Non-draft offers | (NEW) Total Offers Made |
| KPI-26 | [R13] | Placement Type Totals (Visual) | Placement type filtering | gold.fact_offer + gold.fact_referral_offer | Spot vs Framework split | Placement Type Totals (Visual) |
| KPI-27 | [R18] | Spot Offers (Under Offer Referrals) | Emergency placement reporting | gold.fact_offer + gold.fact_referral_offer | Spot offers only | Spot Offers (Under Offer Referrals) |

##### Section 5 — Referral Offers

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-28 | [R25-R29] | Offer Count | Provider offer management | gold.fact_offer | Distinct offers | Offer Count |
| KPI-29 | [R24] | Referrals Currently Active | Dashboard | gold.dim_referral | Open or Under Offer | Referrals Currently Active |
| KPI-30 | [R24,R36] | Active Referrals Under Offer | Dashboard; offers | dim_referral + referral_offer | Under-offer referrals with valid offers | Active Referrals Under Offer |
| KPI-31 | [R13] | Referrals Cancelled/Closed | Placement filtering | gold.dim_referral | Closed or Cancelled | Referrals Cancelled/Closed |
| KPI-32 | [R24,R36] | Active Referrals Awaiting Offers | Dashboard and offers | dim_referral + referral_offer | Open referrals without offers | Active Referrals Awaiting Offers |
| KPI-33 | [R24] | Referrals With One or More Offers | Dashboard | dim_referral + referral_offer | Referrals with valid offers | Referrals With One or More Offers |
| KPI-34 | [R54] | Closed Referrals (by Reason) | Declined placement reasons | referral + referral_offer + offer | Group by decline reason | Closed Referrals (by Reason) |
| KPI-35 | [R25-R29] | Total Offers Made (Active Referrals Under Offer) | Provider offer management | gold.fact_offer | Non-draft offers | Total Offers Made (Active Referrals Under Offer) |
| KPI-36 | [R25-R29] | Offer IDs (Under Offer Referrals) | Provider offer management | offer + referral_offer | Distinct offer IDs | Offer IDs (Under Offer Referrals) |
| KPI-37 | [R26] | Offers per Provider (Under Offer Referrals) | Prioritise requests | offer + referral_offer | Offers grouped by provider | Offers per Provider (Under Offer Referrals) |
| KPI-38 | [R67,R68] | Framework Offers (Under Offer Referrals) | Framework management | offer + referral_offer | Non-spot offers | Framework Offers (Under Offer Referrals) |
| KPI-39 | [R28,R35] | Accepted Offers (Scoped Table) | Acceptance and IPA | gold.fact_offer | Accepted offers | Accepted Offers (Scoped Table) |

##### Section 6 — Provider Registry

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-40 | [R91,R93] | Provider Homes Registered | Registration; directory | gold.dim_provider_home | Count homes | Provider Homes Registered |
| KPI-41 | [R91,R93] | Providers Registered | Registration; directory | gold.dim_provider | Count providers | Providers Registered |
| KPI-42 | [R95] | Providers - Fostering | Fostering framework | provider_home + provider | Fostering providers | Providers - Fostering |
| KPI-43 | [R96] | Providers - Residential | Residential Framework 2.0 | provider_home + provider | Residential providers | Providers - Residential |
| KPI-44 | [R91] | Providers - Supported Accommodation | Registration | provider_home + provider | Supported Accommodation providers | Providers - Supported Accommodation |
| KPI-45 | [R67] | Framework Providers | Framework maintenance | gold.dim_provider_framework | Providers by framework | Framework Providers |
| KPI-46 | [R46] | NON Framework Providers | QA non-framework providers | provider_framework | QA flag false | NON Framework Providers |
| KPI-47 | [R46] | Is Non Framework Provider | QA non-framework providers | provider_framework | Boolean flag | Is Non Framework Provider |
| KPI-48 | [R93] | Directory Summary Count | Provider directory | provider + provider_home | Aggregated provider count | Directory Summary Count |
| KPI-49 | [R96] | Residential Homes | Residential framework | provider_home | Residential homes | Residential Homes |
| KPI-50 | [R91] | Supported Accommodation Homes | Registration | provider_home | Supported homes | Supported Accommodation Homes |
| KPI-51 | [R95] | Fostering Providers | Fostering framework | provider + provider_home | Fostering providers | Fostering Providers |
| KPI-52 | [R95] | Fostering Chart Count | Fostering reporting | provider_home | Chart aggregation | Fostering Chart Count |

##### Section 7 — Draft/Pending Offers

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-53 | [R24] | Draft No Activity Since Creation | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date = last_modified_date` | Draft No Activity Since Creation |
| KPI-54 | [R24] | Draft Offers With Activity Since Creation | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND offer_date != last_modified_date` | Draft Offers With Activity Since Creation |
| KPI-55 | [R24] | Draft Offers Missing Dates | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND (offer_date IS NULL OR last_modified_date IS NULL)` | Draft Offers Missing Dates |
| KPI-56 | [R24] | Draft Offers Updated After Creation | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND last_modified_date > offer_date` | Draft Offers Updated After Creation |
| KPI-57 | [R24] | Draft No Activity 7+ Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 7` | Draft No Activity 7+ Days |
| KPI-58 | [R24] | Drafts No Activity 14+ Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT' AND DATEDIFF(current_date(), offer_date) >= 14` | Drafts No Activity 14+ Days |
| KPI-59 | [R24] | Average Days in Draft | R24 (dashboard task management) | `gold.fact_offer` | `AVG(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'` | Average Days in Draft |
| KPI-60 | [R24] | Oldest Draft Age (Days) | R24 (dashboard task management) | `gold.fact_offer` | `MAX(DATEDIFF(current_date(), offer_date)) WHERE offer_status = 'DRAFT'` | Oldest Draft Age (Days) |
| KPI-61 | [R24] | Draft Offer Count | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'DRAFT'` | Draft Offer Count |
| KPI-62 | [R24] | Draft With No Activity Since Creation (%) | R24 (dashboard task management) | `gold.fact_offer` | `KPI-53 / KPI-61 * 100` | Draft With No Activity Since Creation (%) |
| KPI-63 | [R24] | Drafts With No Activity 14+ Days | R24 (dashboard task management) | `gold.fact_offer` | Same as KPI-58 (duplicate measure in PBI) | Drafts With No Activity 14+ Days |
| KPI-64 | [R24] | Pending Offers by Age Bucket | R24 (dashboard task management) | `gold.fact_offer` ⨝ `gold.pending_age_band` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN min_days AND max_days GROUP BY band_label` | Pending Offers by Age Bucket |
| KPI-65 | [R24] | Pending Offers 15–30 Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 15 AND 30` | Pending Offers 15–30 Days |
| KPI-66 | [R24] | Pending Offers 30+ Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30` | Pending Offers 30+ Days |
| KPI-67 | [R24] | Pending Offers 0–7 Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 0 AND 7` | Pending Offers 0–7 Days |
| KPI-68 | [R24] | Pending Offers 8–14 Days | R24 (dashboard task management) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) BETWEEN 8 AND 14` | Pending Offers 8–14 Days |
| KPI-69 | [R24,R26] | Provider with Offers over 30+ Days | R24 (dashboard task management), R26 (prioritise requests) | `gold.fact_offer` ⟕ `gold.fact_referral_offer` | `COUNT(DISTINCT provider_id) WHERE offer_status = 'PENDING' AND DATEDIFF(current_date(), offer_date) >= 30` | Provider with Offers over 30+ Days |
| KPI-70 | [R24] | Offers At Risk (8–14 Days) | R24 (dashboard task management) | `gold.fact_offer` | Same as KPI-68 (duplicate) | Offers At Risk (8–14 Days) |
| KPI-71 | [R24] | Offers Outside Timeframe (15–30 Days) | R24 (dashboard task management) | `gold.fact_offer` | Same as KPI-65 (duplicate) | Offers Outside Timeframe (15–30 Days) |
| KPI-72 | [R24] | Critical Offers (30+ Days) | R24 (dashboard task management) | `gold.fact_offer` | Same as KPI-66 (duplicate) | Critical Offers (30+ Days) |

##### Section 8 — IPA Measures

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-73 | [R35] | IPA Exists | R35 (digitised IPA) | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) > 0` (boolean) | IPA Exists |
| KPI-74 | [R28] | Is In Accepted KPI | R28 (accept placements) | `gold.fact_offer` ⟕ `gold.fact_ipa` | `offer_status = 'ACCEPTED'` flag, base for IPA funnel | Is In Accepted KPI |
| KPI-75 | [R28,R35] | Accepted Offers Base | R28 (accept placements), R35 (digitised IPA) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) WHERE offer_status = 'ACCEPTED'` | Accepted Offers Base |
| KPI-76 | [R35] | IPA Created | R35 (digitised IPA) | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id)` | IPA Created |
| KPI-77 | [R35] | IPA Completed | R35 (digitised IPA) | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) WHERE signed_by_local_authority = true AND signed_by_provider = true` | IPA Completed |
| KPI-78 | [R35] | IPAs Pending Completion | R35 (digitised IPA) | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) WHERE (signed_by_local_authority = false OR signed_by_provider = false) AND closed = false` | IPAs Pending Completion |
| KPI-79 | [R35] | Offers Awaiting IPA Creation | R35 (digitised IPA) | `gold.fact_offer` ⟕ `gold.fact_ipa` | `COUNT(DISTINCT f.offer_id) LEFT JOIN fact_ipa i ON f.offer_id = i.offer_id WHERE f.offer_status = 'ACCEPTED' AND i.ipa_id IS NULL` | Offers Awaiting IPA Creation |
| KPI-80 | [R35] | Is IPA Pending | R35 (digitised IPA) | `gold.fact_ipa` | Boolean flag, IPA exists but not signed | Is IPA Pending |
| KPI-81 | [R35] | Is Awaiting IPA Creation | R35 (digitised IPA) | `gold.fact_offer` ⟕ `gold.fact_ipa` | Boolean flag, accepted offer with no IPA | Is Awaiting IPA Creation |
| KPI-82 | [R35] | Is IPA Completed | R35 (digitised IPA) | `gold.fact_ipa` | Boolean flag, both signatures present | Is IPA Completed |
| KPI-83 | [R35] | Accepted Offer to IPA Conversion % | R35 (digitised IPA) | `gold.fact_offer` ⟕ `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) / COUNT(DISTINCT accepted_offers) * 100` | Accepted Offer to IPA Conversion % |
| KPI-84 | [R35] | Offers Still to Progress to IPA | R35 (digitised IPA) | `gold.fact_offer` ⟕ `gold.fact_ipa` | `100 - KPI-83` | Offers Still to Progress to IPA |
| KPI-85 | [R35] | IPA Created to Completion % | R35 (digitised IPA) | `gold.fact_ipa` | `COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT all_ipa) * 100` | IPA Created to Completion % |
| KPI-86 | [R35] | Successful Offers to IPA Completed % | R35 (digitised IPA) | `gold.fact_offer` ⟕ `gold.fact_ipa` | `COUNT(DISTINCT completed_ipa) / COUNT(DISTINCT accepted_offers) * 100` | Successful Offers to IPA Completed % |

##### Section 9 — Other Measures

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-87 | [R82] | Dashboard Last Refreshed | R82 (reporting and dashboard refresh visibility) | N/A (system timestamp) | `current_timestamp()` | Dashboard Last Refreshed |
| KPI-88 | [R53] | Latest Export per Offer | R53 (export/reporting capability) | `gold.fact_offer` | `MAX(offer_date) GROUP BY offer_id` | Latest Export per Offer |
| KPI-89 | [R24] | Latest Offer Status Count | R24 (dashboard monitoring) | `gold.fact_offer` | `COUNT(DISTINCT offer_id) GROUP BY offer_status ORDER BY count DESC` | Latest Offer Status Count |
| KPI-90 | [R22] | Overlap Referrals | R22 (out-of-region placements — partial) | `gold.fact_referral` ⟕ `gold.fact_referral_offer` | Referrals appearing in multiple provider referral-provider mappings | Overlap Referrals |

##### Section 10 — New Outstanding Measures (functional-gap closure)

| KPI ID | Req IDs | KPI description | Requirement context | Tables | Calculation | PBI measure |
|---|---|---|---|---|---|---|
| KPI-91 | [R18,R57] | Emergency Referrals | R18 emergency placements; R57 emergency vs planned reporting | `gold.fact_referral` | `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN','UNDER_OFFER') AND created_timestamp::date = required_start_date` | Emergency Referrals |
| KPI-92 | [R18,R57] | Emergency Placement Rate | R18 emergency placements; R57 emergency reporting | `gold.fact_referral` | `KPI-91 / KPI-01 * 100` | Emergency Placement Rate |
| KPI-93 | [R57] | Planned Referrals | R57 planned placements separately reportable | `gold.fact_referral` | `COUNT(DISTINCT referral_id) WHERE status IN ('OPEN','UNDER_OFFER') AND created_timestamp::date != required_start_date` | Planned Referrals |
| KPI-94 | [R18,R57] | Emergency vs Planned Split | R18 emergency placements; R57 reporting split | `gold.fact_referral` | `COUNT(DISTINCT referral_id) GROUP BY CASE WHEN created_timestamp::date = required_start_date THEN 'Emergency' ELSE 'Planned' END` | Emergency vs Planned Split |
| KPI-95 | [R22] | Out-of-Region Referrals | R22 out-of-region placements tagged and reported | `gold.fact_referral` ⟕ `gold.fact_referral_offer` ⟕ `gold.dim_provider` | `COUNT(DISTINCT r.referral_id) JOIN fact_referral_offer rpo JOIN dim_provider p WHERE p.country != 'United Kingdom' OR p.county NOT LIKE '%West Midlands%'` | Out-of-Region Referrals |
| KPI-96 | [R22] | Out-of-Region Placement Rate | R22 out-of-region placement reporting | Same as KPI-95 | `KPI-95 / KPI-01 * 100` | Out-of-Region Placement Rate |
| KPI-97 | [R41] | Providers with QA Flags | R41 advisory notices and safeguarding flags | `gold.dim_provider` | `COUNT(DISTINCT provider_id) WHERE qa_flag = true OR qa_flag_fostering_spot = true OR qa_flag_sup_acc = true OR qa_flag_resi = true` | Providers with QA Flags |
| KPI-98 | [R41] | QA Flag Type Breakdown | R41 information notices and safeguarding concerns | `gold.dim_provider` | `UNPIVOT qa_flag columns → COUNT(DISTINCT provider_id) GROUP BY flag_type` | QA Flag Type Breakdown |
| KPI-99 | [R41] | QA Flagged Providers by Home | R41 advisory notices and safeguarding flags | `gold.dim_provider` ⟕ `gold.dim_provider_home` | `COUNT(DISTINCT provider_home_id) WHERE provider/home QA flags exist` | QA Flagged Providers by Home |
| KPI-100 | [R47] | Documents Expiring (30 Days) | R47 documentation expiry monitoring | `gold.dim_s3_file_metadata` | `COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date BETWEEN current_date() AND date_add(current_date(),30)` | Documents Expiring (30 Days) |
| KPI-101 | [R47,R48] | Documents Expired | R47 documentation control; R48 provider eligibility | `gold.dim_s3_file_metadata` | `COUNT(DISTINCT s3_file_metadata_id) WHERE expiry_date < current_date()` | Documents Expired |
| KPI-102 | [R48] | Providers Blocked (Incomplete Docs) | R48 exclude providers with incomplete documentation | `gold.dim_provider` ⟕ `gold.dim_provider_document` ⟕ `gold.dim_s3_file_metadata` | `COUNT(DISTINCT provider_id) WHERE expired documentation exists` | Providers Blocked (Incomplete Docs) |
| KPI-103 | [R48] | Document Compliance Rate | R48 documentation compliance | `gold.dim_provider` ⟕ `gold.dim_s3_file_metadata` | `(Total Providers - KPI-102) / Total Providers * 100` | Document Compliance Rate |
| KPI-104 | [R49] | Provider Due Diligence Status | R49 provider due diligence monitoring | `gold.dim_provider` | `COUNT(DISTINCT provider_id) GROUP BY provider_status` | Provider Due Diligence Status |
| KPI-105 | [R54] | Decline Reasons (Referral Level) | R54 capture reasons for declined placements | `gold.fact_referral_offer` ⟕ `gold.fact_referral_provider_decline_reason` | `COUNT(DISTINCT referral_id) GROUP BY decline_reason_code` | Decline Reasons (Referral Level) |
| KPI-106 | [R58] | Framework Changes During Active Referrals | R58 commissioners alerted to framework changes | `gold.fact_referral_category` ⟕ `gold.fact_referral_offer` ⟕ `gold.fact_referral` | Active referrals where referral category changed during lifecycle | Framework Changes During Active Referrals |
| KPI-107 | [R62] | Total Weekly Fee Liability | R62 finance payment reporting | `gold.fact_ipa` | `SUM(costs_total_weekly_fee) WHERE signed_by_local_authority = true AND signed_by_provider = true AND closed = false` | Total Weekly Fee Liability |
| KPI-108 | [R62] | Payment Method Breakdown | R62 finance payment reporting | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) GROUP BY payment_method WHERE closed = false` | Payment Method Breakdown |
| KPI-109 | [R62] | IPA Payment Status | R62 finance payment reporting | `gold.fact_ipa` | `COUNT(DISTINCT ipa_id) GROUP BY payment lifecycle status` | IPA Payment Status |
| KPI-110 | [R14] | Messages Sent | R14 provider messaging | `gold.fact_provider_message` | `COUNT(DISTINCT message_id)` | Messages Sent |
| KPI-111 | [R14] | Avg Message Response Time (Hours) | R14 auditable messaging and prioritisation | `gold.fact_provider_message` ⟕ `gold.fact_referral_offer` | `AVG(response hours between messages)` | Avg Message Response Time (Hours) |
| KPI-112 | [R14] | Priority Messages Unread | R14 urgent message tracking | `gold.fact_provider_message` ⟕ `gold.fact_provider_message_status` | `COUNT(DISTINCT message_id) WHERE no message status exists` | Priority Messages Unread |
| KPI-113 | [R20] | Audit Events by Type | R20 audit tracking across placement lifecycle | `gold.fact_referral_event_log` | `COUNT(DISTINCT event_id) GROUP BY event_type` | Audit Events by Type |
| KPI-114 | [R20,R35] | IPA Signature Completion Rate | R20 signatures tracked; R35 electronic signatures | `gold.fact_ipa` | Counts and rates for LA signed, provider signed, both signed, total IPA | IPA Signature Completion Rate |
| KPI-115 | [R19] | Referral Updates per Day | R19 referral maintenance and provider notification | `gold.fact_referral` | `COUNT(DISTINCT referral_id) / COUNT(DISTINCT DATE(modified_timestamp))` | Referral Updates per Day |
| KPI-116 | [R59] | Provider Onboarding Pipeline | R59 bulk provider onboarding | `gold.dim_provider` ⟕ `gold.dim_submission_documents` | `COUNT(DISTINCT provider_id) WHERE provider_status = 'Pending'` | Provider Onboarding Pipeline |
| KPI-117 | [R59] | Bulk Onboarding Success Rate | R59 bulk provider onboarding | `gold.dim_provider` | `COUNT(DISTINCT approved providers) / COUNT(DISTINCT providers) * 100` | Bulk Onboarding Success Rate |

#### 4.7.3 Inventory summary

| Category | Existing KPIs | New KPIs | Total |
|---|---:|---:|---:|
| Referral Volume | 10 | 4 (emergency/planned) | 14 |
| Provider Activity | 12 | 0 | 12 |
| Timebased | 2 | 0 | 2 |
| Spot vs Framework | 3 | 0 | 3 |
| Referral Offers | 12 | 1 (decline reasons) | 13 |
| Provider Registry | 13 | 3 (QA flags, due diligence) | 16 |
| Draft/Pending | 20 | 0 | 20 |
| IPA Measures | 14 | 3 (finance, signatures) | 17 |
| Out-of-Region | 1 | 2 (out-of-region, rate) | 3 |
| Document Compliance | 0 | 4 (expiry, blocked, rate) | 4 |
| Messaging | 0 | 3 (response, unread) | 3 |
| Audit Trail | 0 | 2 (events, signatures) | 2 |
| Onboarding | 0 | 2 (pipeline, success) | 2 |
| Finance | 0 | 3 (fees, payment, status) | 3 |
| **Total** | **90** (existing) | **27** (new) | **117** |

---

## 5. Functional Coverage Assessment

### 5.1 Coverage by Stakeholder Role

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

### 5.2 Coverage Analysis

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

## 6. Key Findings

### 6.1 Network Drive Dependency — Critical Data Pipeline Risk

**Finding**: The entire data pipeline relies on CSV files stored on network drives. There is no lakehouse, no medallion architecture, and no structured data ingestion framework.

**Implications**:
- Single point of failure — network drive unavailability breaks all reporting
- No data validation or quality gates between source and semantic model
- No audit trail for data changes
- No incremental loading — full refresh on each cycle
- Limited scalability as data volumes grow
- No disaster recovery or data lineage

### 6.2 Missing KPIs — 17 Functional Gaps

**Finding**: 17 functional requirements defined in the KPI Logic Document have no corresponding Power BI measure.

**Critical missing KPIs include**:
- **Emergency placements (R18)**: No visibility of emergency placement activity — a safeguarding concern
- **Out-of-region placements (R22)**: No tracking of placements made outside the 14 West Midlands authorities
- **QA flags (R41)**: No quality alert mechanism in the dashboard
- **Document expiry (R47/R48)**: No tracking of expiring compliance certificates or insurance documents
- **Finance (R62)**: No payment or fee-related KPIs whatsoever

### 6.3 QA Officer Coverage at 25% — Safeguarding Gap

**Finding**: Only 2 of 8 QA Officer requirements are implemented in the dashboard.

**Implications**:
- Quality assurance and safeguarding teams lack dashboard visibility
- Compliance certificate and insurance expiry are not tracked
- No proactive alerting for QA issues
- Risk of non-compliance with regulatory requirements

### 6.4 Finance Officer Coverage at 0% — Financial Oversight Gap

**Finding**: No measures exist for the Finance Officer role (R62).

**Implications**:
- No visibility of placement costs, fees, or payment status
- Finance team cannot use the dashboard for financial planning or reconciliation
- No cost-per-placement or cost-per-provider analytics
- Gap between operational and financial reporting

### 6.5 Duplicate Measures — Maintenance and Governance Risk

**Finding**: 5 duplicate measures have been identified, all related to pending offer age bucket calculations.

**Implications**:
- Maintenance burden — logic changes must be applied in multiple places
- Risk of logic divergence over time if duplicates are updated independently
- Semantic model clutter — 5 measures serving no unique purpose
- Indicates absence of formal code review or measure governance process

### 6.6 Data Quality Issues — Typographical Errors

**Finding**: A typographical error was identified in a measure name — 'Recieved' (should be 'Received').

**Implications**:
- Unprofessional appearance in the Power BI field list
- Potential confusion for report developers and consumers
- Indicates absence of naming convention enforcement or code review
- Suggests informal development practices

### 6.7 No Medallion Architecture — No Data Separation

**Finding**: There is no bronze-silver-gold data architecture. All transformation logic resides in DAX measures within the Power BI semantic model.

**Implications**:
- No separation of raw, cleansed, and curated data
- Data quality issues in source CSVs propagate directly to the dashboard
- No reusable data assets outside Power BI
- Limits ability to serve other consumers (e.g., Excel, other BI tools, data science)

### 6.8 PBIP Format — Positive Finding

**Finding**: The report is published in PBIP format with TMDL semantic model definition.

**Benefits**:
- Enables source control and version history
- Supports branch-based development and code review
- Facilitates CI/CD deployment automation
- Provides full transparency of semantic model logic

---

## 7. Risk Assessment

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

## 8. Recommendations Summary

The following recommendations provide a high-level direction for addressing the findings of this assessment. Detailed analysis, prioritisation, and implementation guidance are provided in the Gap Analysis document (03_Gap_Analysis_Report.md).

### 8.1 Data Architecture Modernisation

- **Migrate from network drive CSV to Fabric Lakehouse**: Establish a OneLake-based data store with bronze (raw), silver (cleansed), and gold (curated) layers.
- **Implement automated ingestion pipeline**: Replace manual CSV export with automated data pipeline (e.g., Fabric Data Factory, Azure Data Factory) with scheduling and monitoring.
- **Introduce data quality gates**: Validate data at each medallion layer transition — schema checks, null checks, referential integrity.
- **Enable incremental loading**: Move from full refresh to incremental/delta loading for scalability.

### 8.2 Functional Gap Closure

- **Prioritise high-priority missing measures (8)**: Implement emergency placements (R18), out-of-region (R22), QA flags (R41), document expiry (R47/R48), and finance KPIs (R62) as immediate priorities.
- **Address QA Officer coverage (25% → target 90%)**: Close safeguarding and compliance gaps.
- **Address Finance Officer coverage (0% → target 100%)**: Build payment, fee, and cost analytics.
- **Review partial measures (2)**: Enhance to full requirement satisfaction.
- **Review extra measures (4)**: Confirm whether formal requirements should be created or measures removed.

### 8.3 Governance and Quality

- **Eliminate duplicate measures (5)**: Consolidate into single canonical measures; update report visuals to reference canonical names.
- **Fix typographical errors**: Correct 'Recieved' → 'Received' and audit all measure names for spelling/convention compliance.
- **Establish naming conventions**: Define and enforce DAX measure naming conventions (e.g., PascalCase, standard prefixes).
- **Implement code review process**: Leverage PBIP/Git workflow for pull-request-based code review on all semantic model changes.
- **Document data lineage**: Create end-to-end lineage documentation from PostgreSQL schemas through to dashboard visuals.

### 8.4 Monitoring and Operations

- **Implement pipeline monitoring**: Automated alerting on refresh failure, data quality anomalies, and pipeline latency.
- **Establish refresh cadence SLA**: Define and publish expected data freshness.
- **Create operational runbook**: Document troubleshooting steps for common pipeline and dashboard issues.

### 8.5 Recommendation Prioritisation

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
| 4 | Gap Analysis Report (03_Gap_Analysis_Report.md) | [Consultant Name] | July 2026 |

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
