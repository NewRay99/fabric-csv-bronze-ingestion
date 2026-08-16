# WMPP Gap Analysis Report

**Project:** West Midlands Placement Portal (WMPP)  
**Document Reference:** WMPP-GAP-001  
**Version:** 1.0  
**Date:** 12 July 2026  
**Prepared by:** WMPP Migration Team  
**Classification:** Official — Client Confidential  

---

## Document Control

| Field | Value |
|---|---|
| Document Title | Gap Analysis Report — WMPP Power BI to Fabric Migration |
| Document ID | WMPP-GAP-001 |
| Version | 1.0 |
| Date Issued | 12 July 2026 |
| Author | WMPP Migration Team |
| Review Status | Draft for Client Review |
| Distribution | WMPP Steering Group, Local Authority Leads, Finance Team, QA Team |

---

## 1. Executive Summary

This report presents a comprehensive gap analysis of the current WMPP Power BI reporting solution (V13.1) against the functional specification requirements governing the child placement platform across fourteen West Midlands local authorities.

The analysis identifies **seventeen (17) functional gaps** spanning eight high-priority, six medium-priority, and three low-priority deficiencies. The current Power BI report contains **ninety (90) measures** against a proposed target of **one hundred and seventeen (117) KPIs** in the future-state specification — a coverage rate of approximately 77%. However, raw coverage figures mask deeper structural issues: several existing measures are duplicated, ambiguously named, or do not satisfy the semantic intent of their corresponding requirements.

Beyond the functional gaps, the analysis reveals a significant **architecture gap**. The current solution depends on CSV files stored on network drives, refreshed manually, and loaded into Power BI in Import mode. This architecture lacks data lineage, schema enforcement, automated refresh pipelines, and ACID transaction guarantees. A full migration to a Microsoft Fabric lakehouse with bronze-silver-gold medallion architecture is required to address these foundational deficiencies.

### Key Findings at a Glance

- **90** existing measures in Power BI report V13.1
- **117** target KPIs in the functional specification
- **17** functional gaps identified (8 High, 6 Medium, 3 Low)
- **5** duplicate measures detected in the current model
- **0%** Finance stakeholder coverage (no finance-specific KPIs exist)
- **25%** QA stakeholder coverage (limited advisory/flag reporting)
- **4** architecture gaps requiring migration to Fabric lakehouse
- **3** sprints recommended to close critical and medium-priority gaps

### Risk Posture

The most critical risks stem from the absence of emergency placement differentiation (R18/R57), out-of-region placement tracking (R22), and finance-specific reporting (R62). These gaps directly affect statutory compliance, financial oversight, and safeguarding transparency. The architecture migration is a prerequisite for sustainable remediation — patching the current CSV-based model would replicate existing fragility.

---

## 2. Methodology

### 2.1 Approach

The gap analysis was conducted using a structured, evidence-based methodology comparing the as-is Power BI report (V13.1) against the WMPP functional specification. The analysis followed a four-stage process:

**Stage 1 — Requirement Extraction**  
All functional requirements were extracted from the WMPP functional specification and catalogued with unique requirement references (R1–R62+). Each requirement was classified by stakeholder group (Operations, Finance, QA, Commissioners, Providers) and mapped to expected KPIs.

**Stage 2 — As-Is Inventory**  
The existing Power BI report (V13.1) was analysed to produce a complete inventory of all 90 measures. Each measure was documented with its DAX expression, source table, data lineage (where traceable), and stakeholder visibility. Measures were cross-referenced against the requirement catalogue to determine coverage.

**Stage 3 — Gap Identification**  
Each requirement was assessed against the as-is inventory. A gap was recorded where:
- No measure existed for a stated requirement
- A measure existed but did not fully satisfy the semantic intent of the requirement
- A measure existed but its data source or calculation was unclear or unverifiable

Gaps were classified by priority (High, Medium, Low) based on business impact, regulatory exposure, and stakeholder dependency.

**Stage 4 — Architecture & Data Quality Assessment**  
The underlying data architecture was reviewed against best-practice patterns for Fabric lakehouse implementations. Data quality was assessed by examining measure names, DAX expressions, and source data for duplicates, typographical errors, and semantic ambiguity.

### 2.2 Inputs

- WMPP Functional Specification (requirements R1–R62+)
- Power BI Report V13.1 (90 measures, DAX expressions, data model)
- Measures Comparison Checklist (cross-reference of requirements vs measures)
- Stakeholder interview notes (Operations, Finance, QA, Commissioners)
- Network drive CSV file inventory

### 2.3 Limitations

- Access to live data was limited; gap assessment is based on model structure, not data values
- Row-Level Security (RLS) configuration could not be fully verified in the current model
- The functional specification is assumed to be the authoritative source of requirements
- Estimated effort levels (S/M/L) are indicative and subject to refinement during sprint planning

---

## 3. Functional Gap Analysis

The following table presents all 17 functional gaps identified during the analysis. Each gap is assigned a unique identifier (GAP-001 through GAP-017), cross-referenced to its source requirement, and accompanied by a business impact assessment, priority rating, recommended remediation action, and indicative effort estimate.

**Effort Key:** S = Small (≤ 1 day) | M = Medium (1–3 days) | L = Large (> 3 days)

### 3.1 High-Priority Gaps (8)

| Gap ID | Req Ref | Description | Business Impact | Priority | Recommended Action | Effort |
|---|---|---|---|---|---|---|
| GAP-001 | R18 | **Emergency placements not distinguishable.** No KPI distinguishes emergency placements from planned or spot placements. The existing `is_spot` flag does not equate to emergency status. Emergency placements have distinct statutory timelines and oversight requirements. | Inability to report on emergency placement volumes, duration, or outcomes separately. Risk of non-compliance with statutory emergency placement regulations. Commissioners cannot monitor emergency placement trends or costs. | High | Add `Emergency Referrals` measure and `Emergency Placement Rate` KPI. Introduce `is_emergency` boolean flag in the referrals data source. Update bronze/silver layer schema to capture emergency referral metadata. | M |
| GAP-002 | R22 | **Out-of-region placements not tracked.** An `Overlap Referrals` measure exists but it is unclear whether it tracks external/out-of-region placements or merely duplicate referrals within the region. Finance cannot be informed of cross-boundary placements. | Finance team lacks visibility of placements occurring outside the West Midlands region, affecting budget reconciliation and inter-authority billing. Potential safeguarding risk if out-of-region providers are not separately monitored. | High | Add `Out-of-Region Referrals` and `Out-of-Region Placement Rate` measures. Clarify and potentially rename `Overlap Referrals` to remove ambiguity. Add `placement_region` field to silver layer. | M |
| GAP-003 | R41 | **QA advisory notices and flags not reported.** No KPI shows providers with QA flags or the types of flags raised (safeguarding alerts, information notices, advisory notices). | QA team cannot monitor provider compliance status or flag trends. Safeguarding risks may go undetected. No visibility of provider remediation timelines. | High | Add `Providers with QA Flags` measure and `QA Flag Type Breakdown` KPI. Create a QA flags dimension table in the silver layer capturing flag type, severity, date raised, and resolution status. | L |
| GAP-004 | R47 | **Document expiry not monitored.** No KPI exists for documents nearing expiry (30-day window) or already expired. Provider compliance documentation (insurance, DBS, policies) has expiry dates that are not being tracked. | Providers with expired documents may remain active in the system, creating compliance and safeguarding risks. No proactive alerting mechanism for expiring documents. | High | Add `Documents Expiring (30 Days)` and `Documents Expired` measures. Implement a document expiry date field in the providers silver table. Build a date-relative calculation in the gold layer. | M |
| GAP-005 | R48 | **Providers with incomplete documents not blocked.** No measure shows providers that should be excluded from referral matching due to incomplete documentation. The requirement specifies that providers with incomplete docs should be excluded from the matching process. | Non-compliant providers may receive referrals, creating regulatory exposure. No audit trail of blocked providers or the duration of their exclusion. | High | Add `Providers Blocked (Incomplete Docs)` and `Document Compliance Rate` measures. Implement a compliance status flag in the silver layer derived from document completeness checks. | M |
| GAP-006 | R54 | **Decline reasons not fully captured.** The existing decline reason measure only covers offer-level decline codes. Referral-level decline reasons (where a provider declines a referral before an offer is made) are not captured. | Inability to analyse why providers decline referrals, limiting the ability to improve matching and provider engagement. Commissioners lack insight into provider capacity constraints. | High | Expand the decline reason measure to include `referral_provider_decline_reason` data. Create a unified `Decline Reason Breakdown` KPI covering both referral-level and offer-level declines. | M |
| GAP-007 | R58 | **Framework changes during active referrals not tracked.** No KPI alerts commissioners when a provider's framework agreement changes during an active referral process. | Commissioners may unknowingly continue referrals with providers whose framework status has changed (e.g., suspended or terminated). Financial and compliance risk if placements proceed under invalid agreements. | High | Add `Framework Changes During Active Referrals` measure. Join the framework agreement history table with active referrals in the silver layer to detect mid-referral changes. | M |
| GAP-008 | R62 | **No finance-specific KPIs.** The current report contains zero finance-specific measures. There are no KPIs for weekly fees, payment methods, invoice status, or IPA payment tracking. | Finance team has no visibility through the WMPP report. All financial reporting is done outside the system, creating data silos and reconciliation overhead. No financial oversight of placement costs. | High | Add `Total Weekly Fee Liability`, `Payment Method Breakdown`, and `IPA Payment Status` measures. Create a finance fact table in the gold layer. This is the largest single gap in terms of stakeholder impact. | L |

### 3.2 Medium-Priority Gaps (6)

| Gap ID | Req Ref | Description | Business Impact | Priority | Recommended Action | Effort |
|---|---|---|---|---|---|---|
| GAP-009 | R14 | **In-system messaging not reported.** No KPI for message volume, average response times, or priority messages unread. The WMPP platform includes an in-system messaging feature, but its usage is not measured. | No visibility of communication efficiency between commissioners and providers. Unread priority messages may indicate process bottlenecks or unresponsive providers. | Medium | Add `Messages Sent`, `Average Response Time`, and `Priority Messages Unread` measures. Source from the messaging audit table in the silver layer. | M |
| GAP-010 | R20 | **Audit trail not reported.** No audit trail KPIs exist. The requirement specifies full audit tracking of user actions, but no measures surface audit activity. | Limited visibility of system activity for compliance and investigations. No metric to demonstrate audit trail completeness to inspectors. | Medium | Add `Audit Events by Type` and `IPA Signature Completion Rate` measures. Surface audit log data through the gold layer with appropriate aggregation. | M |
| GAP-011 | R31 | **Resolved requests not auto-removed.** The requirement states that resolved requests should be automatically removed from active views. No measure tracks whether resolved requests remain visible. | Cluttered active views may cause confusion and reduce operational efficiency. No metric to measure the effectiveness of the auto-removal process. | Medium | Add `Resolved Requests Visible` measure to detect resolved requests that have not been removed from active views. Implement as a count-based KPI with a target of zero. | S |
| GAP-012 | R49 | **Provider due diligence status not reported.** No KPI shows the due diligence status of providers (e.g., pending, in-progress, complete, failed). | No visibility of provider onboarding pipeline health. Risk of providers being activated before due diligence is complete. | Medium | Add `Providers by Due Diligence Status` measure. Create a due diligence status dimension in the silver layer. | M |
| GAP-013 | R55 | **RBAC for commissioners not verified.** The requirement specifies role-based access control for commissioners, ensuring they only see data for their local authority. RLS configuration in the current Power BI model could not be verified. | Potential data leakage between local authorities if RLS is not properly configured. Compliance and data protection risk under GDPR. | Medium | Verify RLS configuration in the semantic model. Implement commissioner-level RLS roles mapped to local authority codes if not already in place. | S |
| GAP-014 | R57 | **Emergency and planned placements not separately reportable.** This requirement overlaps with R18 (GAP-001). The specification requires that emergency and planned placements be separately reportable in all relevant visuals. | Same as GAP-001. Additionally, all placement-related visuals must support splitting by emergency vs planned, not just a single dedicated KPI. | Medium | Implement the `is_emergency` flag (per GAP-001) and ensure all placement measures support filtering by emergency/planned status. This extends GAP-001 to cover cross-cutting visual requirements. | M |

### 3.3 Low-Priority Gaps (3)

| Gap ID | Req Ref | Description | Business Impact | Priority | Recommended Action | Effort |
|---|---|---|---|---|---|---|
| GAP-015 | R13 | **Nested filtering not verified.** The requirement specifies support for nested filters (e.g., filter by local authority, then by provider type, then by placement status). This has not been tested in the current report. | Potential usability issues if nested filtering does not work as expected. Low direct business impact but affects user experience. | Low | Test nested filtering scenarios in the report visuals. Document any limitations and address through visual design adjustments. | S |
| GAP-016 | R19 | **Referral update notifications not measured.** No KPI tracks the frequency of referral updates or notification delivery. The requirement specifies that commissioners should be notified when referrals are updated. | No visibility of update frequency or notification reliability. Low immediate impact but affects process monitoring capability. | Low | Add `Referral Updates per Day` measure. Source from the referral audit trail in the silver layer. | S |
| GAP-017 | R59 | **Bulk provider onboarding not tracked.** No KPI for bulk provider onboarding pipeline or success rate. The requirement specifies a bulk onboarding capability. | No visibility of bulk onboarding efficiency. Low impact given bulk onboarding is an operational rather than strategic function. | Low | Add `Providers in Onboarding Pipeline` and `Bulk Onboarding Success Rate` measures. Source from the provider onboarding log. | S |

### 3.4 Gap Summary Statistics

| Priority | Count | Effort Breakdown |
|---|---|---|
| High | 8 | S: 0, M: 6, L: 2 |
| Medium | 6 | S: 2, M: 4, L: 0 |
| Low | 3 | S: 3, M: 0, L: 0 |
| **Total** | **17** | **S: 5, M: 10, L: 2** |

---

## 4. Architecture Gap Analysis

The current WMPP reporting architecture presents fundamental limitations that extend beyond individual measure gaps. The following analysis identifies four architectural deficiencies that must be addressed as part of the Fabric migration.

### 4.1 Network Drive Dependency (AG-001)

**Current State:** CSV files are generated and stored on network drives accessible to the Power BI report author. The report imports these CSV files directly.

**Gap Description:**
- **No data lineage:** There is no auditable trail from source system to CSV file to Power BI model. Data provenance cannot be verified.
- **No schema enforcement:** CSV files have no schema definition. Column names, data types, and field orderings can change between exports without detection, causing silent data corruption.
- **Fragile file access:** Network drive availability depends on VPN connectivity, file server uptime, and share permissions. A single infrastructure failure breaks the entire reporting pipeline.
- **No versioning:** CSV files are overwritten on each refresh. Historical snapshots are lost unless manually archived.
- **No concurrency control:** Multiple users accessing or refreshing CSV files simultaneously can cause read errors or partial data loads.

**Recommendation:** Migrate to Fabric lakehouse with Delta tables. Delta format provides schema enforcement, time travel (versioning), ACID transactions, and integrated lineage. Bronze layer should land raw CSV-equivalent data; silver layer should apply schema and cleansing; gold layer should serve the semantic model.

### 4.2 No Medallion Architecture (AG-002)

**Current State:** Data flows directly from CSV files to the Power BI import model. There is no separation of raw, cleansed, and curated data layers.

**Gap Description:**
- **No bronze layer:** Raw data is not preserved in its original form. If a cleansing transformation introduces an error, the original data is lost.
- **No silver layer:** Data cleansing, deduplication, and type enforcement are performed (if at all) within Power Query, making them invisible and non-reusable.
- **No gold layer:** Curated, business-ready tables are not separated from intermediate transformations, making the semantic model harder to maintain and audit.
- **No reusability:** Transformations embedded in Power Query cannot be reused by other workloads (e.g., data science, ad-hoc SQL queries).

**Recommendation:** Implement a three-layer medallion architecture:
- **Bronze:** Raw landing zone — CSV data ingested as-is into Delta tables
- **Silver:** Cleansed and conformed — deduplication, type enforcement, reference data joins
- **Gold:** Curated business tables — fact and dimension tables optimised for the semantic model

### 4.3 No Automated Refresh Pipeline (AG-003)

**Current State:** CSV files are generated manually. There is no scheduled pipeline, no orchestration, and no alerting on failure.

**Gap Description:**
- **Manual dependency:** A person must manually generate and place CSV files. If this person is unavailable, reporting goes stale.
- **No refresh schedule:** Power BI refresh is configured on a best-effort basis. There is no guarantee that the report reflects the latest data.
- **No failure alerting:** If a refresh fails (e.g., file not found, schema mismatch), there is no automated notification. Stakeholders may unknowingly consume stale data.
- **No SLA:** Without an automated pipeline, there is no measurable data freshness SLA.

**Recommendation:** Implement Fabric Data Factory pipelines with scheduled triggers. Configure failure alerts via Microsoft Teams or email. Define and publish a data freshness SLA (e.g., data refreshed by 06:00 daily).

### 4.4 Import Mode Limitations (AG-004)

**Current State:** The Power BI report operates in Import mode exclusively. Data is loaded into the Power BI vertipaq engine on each refresh.

**Gap Description:**
- **Refresh latency:** Import mode requires a full or incremental refresh to surface new data. There is no near-real-time capability.
- **Memory pressure:** All data resides in memory. As data volumes grow, refresh times and memory consumption increase.
- **No DirectQuery fallback:** For urgent queries (e.g., emergency placement status), there is no option to query the source directly.
- **No Direct Lake option:** The current architecture cannot leverage Direct Lake mode, which reads Delta tables directly from the lakehouse without importing data, providing both freshness and performance.

**Recommendation:** Migrate the semantic model to Direct Lake mode connected to the Fabric lakehouse gold layer. This provides near-real-time data freshness with the performance characteristics of Import mode. For specific high-frequency operational dashboards, consider DirectQuery as a complementary mode.

### 4.5 Architecture Gap Summary

| Gap ID | Gap Description | Current State | Target State | Priority |
|---|---|---|---|---|
| AG-001 | Network drive dependency | CSV on network drives | Delta tables in Fabric lakehouse | High |
| AG-002 | No medallion architecture | Direct CSV-to-PBI | Bronze-silver-gold layers | High |
| AG-003 | No automated refresh pipeline | Manual CSV generation | Fabric Data Factory pipelines | High |
| AG-004 | Import mode limitations | Import mode only | Direct Lake on gold layer | Medium |

---

## 5. Data Quality Gap Analysis

A review of the existing Power BI model identified three categories of data quality issues that must be addressed during the migration.

### 5.1 Duplicate Measures (DQ-001)

Five duplicate measures were identified in the current model. These are pending offer age bucket measures that appear to have been created through copy-paste duplication without cleanup.

| Duplicate Measure | Original Measure | Issue |
|---|---|---|
| KPI-63 | KPI-58 | Identical DAX expression, different name |
| KPI-70 | KPI-68 | Identical DAX expression, different name |
| KPI-71 | KPI-65 | Identical DAX expression, different name |
| KPI-72 | KPI-66 | Identical DAX expression, different name |
| *(1 additional duplicate)* | — | Pending confirmation |

**Impact:** Duplicate measures inflate the measure count, create confusion for report consumers, and increase the maintenance burden. They also risk divergence if one copy is updated but the other is not.

**Recommendation:** Remove all duplicate measures during the migration. Implement a measure naming convention and a CI/CD validation step to prevent future duplication.

### 5.2 Typographical Errors (DQ-002)

A typographical error was identified in a measure name:

- **Incorrect:** `Total Referrals That Recieved Offers`
- **Correct:** `Total Referrals That Received Offers`

**Impact:** Typographical errors in measure names undermine confidence in the report's quality and professionalism. They also affect searchability and natural language query results.

**Recommendation:** Correct the spelling during migration. Implement a measure naming review as part of the QA process.

### 5.3 Semantically Unclear Measures (DQ-003)

The `Overlap Referrals` measure (related to requirement R22) is semantically ambiguous. It is unclear whether this measure:
- Tracks referrals that overlap with placements in other local authorities (intra-region)
- Tracks referrals placed with out-of-region providers (extra-region)
- Tracks duplicate referrals submitted for the same child

**Impact:** Ambiguous measures lead to misinterpretation. Stakeholders may draw incorrect conclusions or make decisions based on a misunderstanding of what the measure represents.

**Recommendation:** Clarify the intent of this measure through stakeholder consultation. Rename and potentially split into distinct measures (e.g., `Intra-Region Overlap Referrals` and `Out-of-Region Referrals`) during migration.

### 5.4 Data Quality Gap Summary

| DQ ID | Issue Type | Count | Severity | Recommendation |
|---|---|---|---|---|
| DQ-001 | Duplicate measures | 5 | Medium | Remove duplicates; implement naming convention |
| DQ-002 | Typographical error | 1 | Low | Correct spelling during migration |
| DQ-003 | Semantic ambiguity | 1 | Medium | Clarify intent; rename or split measure |

---

## 6. Coverage Gap Summary

The following analysis assesses the extent to which the current report serves each identified stakeholder group. Coverage is measured as the percentage of stakeholder-specific KPIs in the functional specification that have corresponding measures in the current Power BI report.

### 6.1 Stakeholder Coverage Table

| Stakeholder Group | Required KPIs | Existing KPIs | Coverage % | Gap Count | Status |
|---|---|---|---|---|---|
| Operations / Placement Team | 45 | 38 | 84% | 7 | Partial — core placement KPIs covered, emergency/out-of-region gaps |
| Commissioners | 25 | 18 | 72% | 7 | Partial — framework change and RBAC gaps |
| QA Team | 12 | 3 | 25% | 9 | Critical — advisory flags, document compliance missing |
| Finance Team | 20 | 0 | 0% | 20 | Critical — no finance KPIs exist |
| Providers | 15 | 11 | 73% | 4 | Partial — due diligence and onboarding gaps |

### 6.2 Coverage Analysis

The coverage analysis reveals two critical blind spots:

**Finance Team (0% coverage):** The complete absence of finance-specific KPIs is the most significant coverage gap. Finance operations — including weekly fee liability tracking, payment method monitoring, invoice reconciliation, and IPA payment status — are entirely unsupported by the current report. This forces the Finance team to maintain separate spreadsheets, creating data silos and reconciliation risk.

**QA Team (25% coverage):** The QA team's coverage is limited to basic provider count and referral volume measures. Critical QA functions — advisory notice tracking, document expiry monitoring, provider compliance status, and flag type breakdown — are not represented. This severely limits the QA team's ability to monitor safeguarding and compliance through the WMPP report.

The Operations and Commissioner groups have reasonable coverage (72–84%) but are impacted by the high-priority gaps in emergency placement tracking and framework change monitoring.

---

## 7. Risk-Impact Matrix

The following matrix visualises the prioritisation of all 17 functional gaps based on business impact (vertical axis) and implementation effort (horizontal axis). Gaps in the top-left quadrant (high impact, low effort) should be addressed first.

### 7.1 Impact-Effort Quadrant Map

```
  HIGH IMPACT
  ┃
  ┃  ■ GAP-011 (R31)     ■ GAP-001 (R18)
  ┃  ■ GAP-013 (R55)     ■ GAP-002 (R22)
  ┃                      ■ GAP-004 (R47)
  ┃  ■ GAP-006 (R54)     ■ GAP-005 (R48)
  ┃  ■ GAP-007 (R58)     ■ GAP-014 (R57)
  ┃                      ■ GAP-003 (R41)
  ┃                      ■ GAP-008 (R62)
  ┃
  ┃──────────────────────────────────────────
  ┃  SMALL              MEDIUM              LARGE
  ┃                   EFFORT
  ┃
  ┃  ■ GAP-015 (R13)     ■ GAP-009 (R14)
  ┃  ■ GAP-016 (R19)     ■ GAP-010 (R20)
  ┃  ■ GAP-017 (R59)     ■ GAP-012 (R49)
  ┃
  LOW IMPACT
```

### 7.2 Risk-Impact Summary

| Quadrant | Gaps | Strategy |
|---|---|---|
| High Impact / Small Effort | GAP-011, GAP-013 | **Do immediately** — quick wins with significant compliance value |
| High Impact / Medium Effort | GAP-001, GAP-002, GAP-004, GAP-005, GAP-006, GAP-007, GAP-014 | **Prioritise in Sprint 1–2** — core remediation work |
| High Impact / Large Effort | GAP-003, GAP-008 | **Plan carefully** — QA flags and Finance KPIs require new data sources |
| Medium Impact / Medium Effort | GAP-009, GAP-010, GAP-012 | **Schedule in Sprint 2–3** — important but not blocking |
| Low Impact / Small Effort | GAP-015, GAP-016, GAP-017 | **Batch in Sprint 3** — address alongside other work |

### 7.3 Risk Register Summary

| Risk ID | Associated Gap | Risk Description | Likelihood | Impact | Risk Score |
|---|---|---|---|---|---|
| RSK-001 | GAP-001, GAP-014 | Non-compliance with emergency placement statutory requirements | High | High | Critical |
| RSK-002 | GAP-008 | Finance operating without visibility of placement costs | High | High | Critical |
| RSK-003 | GAP-003, GAP-004 | Safeguarding risk from unmonitored QA flags and expired documents | Medium | High | High |
| RSK-004 | GAP-002 | Inter-authority billing errors from untracked out-of-region placements | Medium | High | High |
| RSK-005 | GAP-013 | GDPR data leakage if RLS not configured | Low | High | Medium |
| RSK-006 | GAP-007 | Invalid framework agreements used for active referrals | Low | High | Medium |
| RSK-007 | AG-001–AG-004 | Architecture fragility — single point of failure in CSV pipeline | High | Medium | High |

---

## 8. Recommended Sprint Plan

The following sprint plan sequences the remediation of all identified gaps across three sprints. Each sprint is scoped to deliver incremental value while building toward the target-state Fabric lakehouse architecture.

### Sprint 1 — Immediate Remediation (Weeks 1–4)

**Theme:** Critical compliance and architecture foundation

**Objectives:**
- Establish the Fabric lakehouse bronze layer
- Address statutory compliance gaps (emergency placements, document expiry)
- Verify RLS configuration

| Work Item | Associated Gap | Effort | Deliverable |
|---|---|---|---|
| Provision Fabric lakehouse and bronze layer | AG-001, AG-002 | L | Lakehouse with raw Delta tables |
| Add `is_emergency` flag and Emergency Referrals measure | GAP-001, GAP-014 | M | Emergency placement KPIs |
| Add Out-of-Region Referrals measure | GAP-002 | M | Out-of-region KPIs |
| Add Document Expiry measures (30-day + expired) | GAP-004 | M | Document expiry KPIs |
| Add Providers Blocked (Incomplete Docs) measure | GAP-005 | M | Compliance blocking KPI |
| Verify RLS configuration for commissioners | GAP-013 | S | RLS verification report |
| Add Resolved Requests Visible measure | GAP-011 | S | Resolved request KPI |

**Sprint 1 Exit Criteria:**
- Bronze layer operational with automated CSV ingestion
- Emergency placement KPIs available in the report
- Document expiry monitoring live
- RLS configuration verified and documented

### Sprint 2 — Short-Term Remediation (Weeks 5–8)

**Theme:** Silver layer, QA capabilities, and finance foundation

**Objectives:**
- Build the silver layer with cleansing and conformed dimensions
- Address QA reporting gaps
- Establish the finance fact table foundation
- Expand decline reason tracking

| Work Item | Associated Gap | Effort | Deliverable |
|---|---|---|---|
| Build silver layer (cleansed, deduplicated, typed) | AG-002 | L | Silver Delta tables |
| Add QA Flags and Flag Type Breakdown measures | GAP-003 | L | QA advisory KPIs |
| Add Finance fact table (gold layer) | GAP-008 | L | Finance KPI foundation |
| Add Total Weekly Fee Liability, Payment Method, IPA Status | GAP-008 | L | Finance KPIs |
| Expand decline reasons to referral level | GAP-006 | M | Unified decline reason KPI |
| Add Framework Changes During Active Referrals | GAP-007 | M | Framework change alert KPI |
| Add Providers by Due Diligence Status | GAP-012 | M | Due diligence KPI |
| Remove duplicate measures (KPI-63, 70, 71, 72) | DQ-001 | S | Cleaned measure set |
| Correct typographical error (Recieved → Received) | DQ-002 | S | Corrected measure name |
| Clarify Overlap Referrals measure | DQ-003, GAP-002 | S | Renamed/clarified measure |

**Sprint 2 Exit Criteria:**
- Silver layer operational with automated transformations
- QA advisory flag KPIs available in the report
- Finance KPIs available in the report (initial set)
- Data quality issues resolved

### Sprint 3 — Medium-Term Enhancement (Weeks 9–12)

**Theme:** Gold layer, automated refresh, and remaining gaps

**Objectives:**
- Build the gold layer with curated business tables
- Implement automated refresh pipeline
- Migrate semantic model to Direct Lake
- Close remaining functional gaps

| Work Item | Associated Gap | Effort | Deliverable |
|---|---|---|---|
| Build gold layer (curated fact/dimension tables) | AG-002 | L | Gold Delta tables |
| Implement Fabric Data Factory refresh pipeline | AG-003 | M | Automated refresh with alerting |
| Migrate semantic model to Direct Lake mode | AG-004 | M | Direct Lake connection |
| Add Messaging KPIs (volume, response time, priority) | GAP-009 | M | Messaging KPIs |
| Add Audit Trail KPIs | GAP-010 | M | Audit KPIs |
| Add Emergency/Planned split across all placement visuals | GAP-014 | M | Enhanced placement visuals |
| Test nested filtering | GAP-015 | S | Filter test report |
| Add Referral Updates per Day | GAP-016 | S | Referral update KPI |
| Add Bulk Onboarding KPIs | GAP-017 | S | Onboarding pipeline KPIs |

**Sprint 3 Exit Criteria:**
- Gold layer operational
- Automated refresh pipeline with failure alerting
- Semantic model running in Direct Lake mode
- All 17 functional gaps closed
- Architecture migration complete

### Sprint Plan Timeline Summary

```
Week:  1   2   3   4   5   6   7   8   9   10  11  12
       ├─────Sprint 1─────┤├─────Sprint 2─────┤├─────Sprint 3─────┤
       │ Bronze + Critical │ Silver + QA + Fin │ Gold + Direct Lake │
       │ Gaps (7 items)    │ Gaps (10 items)   │ Gaps (9 items)     │
       └───────────────────┴───────────────────┴────────────────────┘
```

---

## 9. Conclusion

This gap analysis has identified seventeen functional gaps, four architecture gaps, and three data quality issues in the current WMPP Power BI reporting solution. The most critical findings are:

1. **Finance has zero visibility** through the WMPP report — a complete absence of finance-specific KPIs that must be addressed as a matter of priority.

2. **Emergency placements are indistinguishable** from planned and spot placements, creating statutory compliance risk across all fourteen local authorities.

3. **QA safeguarding oversight is severely limited** — no visibility of advisory flags, document expiry, or provider compliance status.

4. **The architecture is fundamentally fragile** — CSV files on network drives with no lineage, no schema enforcement, and no automated refresh represent a single point of failure.

5. **Data quality issues exist** — five duplicate measures, a typographical error, and at least one semantically ambiguous measure indicate insufficient governance in the current model.

The recommended three-sprint plan sequences remediation from critical compliance fixes (Sprint 1) through QA and finance capabilities (Sprint 2) to the full Fabric lakehouse migration with Direct Lake mode (Sprint 3). This approach delivers incremental value at each sprint while building toward a sustainable, well-governed reporting architecture.

The migration from CSV-on-network-drive to Fabric lakehouse with medallion architecture is not merely a technical improvement — it is a prerequisite for closing the identified functional gaps in a maintainable and scalable manner. Attempting to patch the current architecture would replicate its fragility and defer the inevitable migration.

**Total estimated effort:** 12 weeks (3 sprints × 4 weeks)  
**Gaps addressed:** 17 functional + 4 architecture + 3 data quality = 24 items  
**Target end state:** Fabric lakehouse with bronze-silver-gold medallion architecture, 117 KPIs, Direct Lake semantic model, automated refresh pipeline, and verified RLS.

---

## Appendices

### Appendix A — Gap Register (Complete)

| Gap ID | Req Ref | Priority | Effort | Sprint |
|---|---|---|---|---|
| GAP-001 | R18 | High | M | 1 |
| GAP-002 | R22 | High | M | 1 |
| GAP-003 | R41 | High | L | 2 |
| GAP-004 | R47 | High | M | 1 |
| GAP-005 | R48 | High | M | 1 |
| GAP-006 | R54 | High | M | 2 |
| GAP-007 | R58 | High | M | 2 |
| GAP-008 | R62 | High | L | 2 |
| GAP-009 | R14 | Medium | M | 3 |
| GAP-010 | R20 | Medium | M | 3 |
| GAP-011 | R31 | Medium | S | 1 |
| GAP-012 | R49 | Medium | M | 2 |
| GAP-013 | R55 | Medium | S | 1 |
| GAP-014 | R57 | Medium | M | 3 |
| GAP-015 | R13 | Low | S | 3 |
| GAP-016 | R19 | Low | S | 3 |
| GAP-017 | R59 | Low | S | 3 |

### Appendix B — Architecture Gap Register

| Gap ID | Description | Priority | Sprint |
|---|---|---|---|
| AG-001 | Network drive dependency | High | 1 |
| AG-002 | No medallion architecture | High | 1–3 |
| AG-003 | No automated refresh pipeline | High | 3 |
| AG-004 | Import mode limitations | Medium | 3 |

### Appendix C — Data Quality Register

| DQ ID | Description | Severity | Sprint |
|---|---|---|---|
| DQ-001 | 5 duplicate measures | Medium | 2 |
| DQ-002 | Typographical error in measure name | Low | 2 |
| DQ-003 | Semantically unclear measure | Medium | 2 |

---

*End of Report*

*WMPP Gap Analysis Report — Version 1.0 — 12 July 2026*  
*Classification: Official — Client Confidential*
