# Statement of Work

## WMPP Data Engineering Engagement — Fabric Lakehouse Migration & KPI Implementation

| Field | Value |
|---|---|
| **Document Title** | Statement of Work — WMPP Fabric Lakehouse Migration |
| **Document Reference** | WMPP-DE-SoW-001 |
| **Version** | 1.0 |
| **Date** | 12 July 2026 |
| **Prepared By** | [Consultant Name] |
| **Prepared For** | West Midlands Placement Portal (WMPP) Programme |
| **Status** | Draft for Client Review |

---

## 1. Engagement Overview

### 1.1 Project Background

The West Midlands Placement Portal (WMPP) is a regional child placement platform operating across fourteen (14) West Midlands local authorities. The platform currently relies on a Power BI report (version 13.1) containing 90 measures, sourced directly from CSV files stored on network drives. This architecture presents significant operational, performance, and governance limitations:

- **Data fragility** — CSV files on network drives are susceptible to schema drift, file naming inconsistencies, and uncontrolled edits with no audit trail.
- **Performance constraints** — Power BI import-mode refreshes against flat-file sources are slow, resource-intensive, and bounded by desktop capacity.
- **Scalability limitations** — the current measure set (90 KPIs) cannot be extended without further degrading refresh performance and increasing maintenance overhead.
- **Functional gaps** — seventeen (17) functional gaps have been identified against stakeholder requirements, spanning emergency placements, QA workflows, finance reconciliation, document tracking, messaging, audit, and onboarding.
- **Governance deficit** — no medallion architecture, no lineage, no schema enforcement, no automated validation, and no role-level security for commissioner regional access.

The client has approved an architectural transition to Microsoft Fabric, adopting a bronze-silver-gold medallion pattern with Spark-based transformation notebooks and Power BI Direct Lake connectivity.

### 1.2 Objectives

The engagement will deliver the following primary objectives:

1. **Establish a governed Fabric lakehouse** with bronze, silver, and gold layers following the medallion architecture pattern.
2. **Replace the network-drive CSV pipeline** with automated, validated, and auditable ingestion via ADLS Gen2 shortcuts and Spark notebooks.
3. **Migrate all 90 existing measures** from DAX to gold-layer Spark SQL views, ensuring full reconciliation against current report values.
4. **Implement 27 new measures** across the seven functional gap categories (emergency, QA, finance, document, messaging, audit, onboarding).
5. **Consolidate duplicate measures** and correct identified naming errors.
6. **Connect Power BI via Direct Lake mode** to gold-layer tables, eliminating import-mode refresh bottlenecks.
7. **Implement role-level security (RLS)** for commissioner regional access (functional gap R55).
8. **Deliver user acceptance testing, training, and handover** enabling client self-sufficiency.

### 1.3 Expected Outcomes

Upon successful completion of this engagement, the client will have:

- A production-grade Fabric lakehouse with bronze-silver-gold medallion architecture.
- 117 validated KPIs (90 migrated + 27 new) implemented as gold-layer Spark SQL views.
- A Power BI Direct Lake report with sub-5-second load performance.
- Role-level security enforced for all 14 local authority commissioner regions.
- Automated data validation and reconciliation against source CSV files.
- Decommissioned network-drive CSV pipeline with no data loss.
- Trained client personnel capable of maintaining and extending the solution.

---

## 2. Scope of Work

### 2.1 In-Scope Items

The following items are explicitly included in the scope of this engagement:

#### 2.1.1 Infrastructure & Foundation

- Provisioning and configuration of Microsoft Fabric capacity (F-SKU or trial).
- Creation of Fabric lakehouse with bronze, silver, and gold schemas.
- Configuration of Azure Data Lake Storage Gen2 (ADLS Gen2) storage accounts and Fabric shortcuts to network-drive CSV source locations.
- Establishment of workspace(s), environment configurations, and access control policies within the Fabric tenant.

#### 2.1.2 Bronze Layer — Ingestion

- Development and deployment of the **bronze loader** Spark notebook.
- Automated ingestion of all identified CSV source files into bronze-layer Delta tables (raw preservation, no transformation).
- Metadata capture: source file path, ingestion timestamp, row count, file hash.
- Idempotency and incremental-load logic (append or overwrite as appropriate per source).

#### 2.1.3 Silver Layer — Schema Enforcement

- Development and deployment of the **silver formatter** Spark notebook.
- Type casting, null handling, column renaming, and schema enforcement for all bronze tables.
- Deduplication logic where applicable.
- Data quality flag columns (is_valid, validation_error).
- Schema documentation and enforcement metadata.

#### 2.1.4 Gold Layer — KPI Views

- Development and deployment of the **gold translator** Spark notebook.
- Migration of all 90 existing DAX measures to gold-layer Spark SQL views.
- Implementation of 27 new measures across the following categories:
  - Emergency placements (e.g., emergency placement count, time-to-placement, emergency placement rate)
  - Quality assurance (e.g., QA review completion rate, QA overdue count, QA pass rate)
  - Finance (e.g., placement cost variance, cost per child per week, monthly spend forecast)
  - Document tracking (e.g., document completeness score, overdue document count)
  - Messaging (e.g., response time averages, unread message count, message volume trends)
  - Audit (e.g., audit trail completeness, change log coverage, access audit metrics)
  - Onboarding (e.g., onboarding completion rate, time-to-onboard, onboarding dropout count)
- Duplicate measure consolidation — identified duplicates will be merged into canonical definitions with stakeholder confirmation.
- Measure name corrections — identified typographical errors will be corrected with a rename mapping documented.

#### 2.1.5 Data Validation & Reconciliation

- Automated reconciliation of gold-layer KPI outputs against current Power BI report values (V13.1).
- Variance reporting with configurable tolerance thresholds.
- Data quality dashboard/report summarising completeness, accuracy, and consistency metrics.

#### 2.1.6 Power BI Integration

- Configuration of Power BI Direct Lake connection to gold-layer Delta tables.
- Migration of existing Power BI report (V13.1) visuals, layouts, and navigation to the Direct Lake-connected dataset.
- Visual reconfiguration where Direct Lake semantic model differences require adjustment.
- Implementation of **role-level security (RLS)** for commissioner regional access (R55), with row-level filters for each of the 14 local authorities.
- Performance optimisation to achieve sub-5-second dashboard load times.

#### 2.1.7 Testing & Quality Assurance

- Unit testing of all bronze, silver, and gold notebook transformations.
- End-to-end reconciliation testing across the full pipeline.
- User Acceptance Testing (UAT) with stakeholder representatives.
- Parallel running of the new Fabric pipeline alongside the existing network-drive CSV pipeline for a defined period.

#### 2.1.8 Training & Handover

- Technical handover sessions for client technical lead and data engineering team.
- End-user training sessions for placement officers, QA analysts, commissioners, and finance users.
- Documentation: pipeline architecture diagrams, notebook usage guides, KPI dictionary, RLS configuration guide, troubleshooting runbook.
- Post-handover hypercare support for a defined period (see Commercial Summary, Section 8).

#### 2.1.9 Decommissioning

- Controlled decommissioning of the network-drive CSV pipeline following successful parallel run and UAT sign-off.
- Migration of any remaining file-based dependencies to Fabric lakehouse storage.
- Archival of legacy CSV pipeline artefacts.

### 2.2 Out-of-Scope Items

The following items are explicitly excluded from this engagement:

1. **Source system changes** — modifications to upstream systems that generate CSV files (e.g., the WMPP application database, third-party provider systems) are not included.
2. **New data sources** — ingestion of data sources not currently part of the CSV pipeline at the time of scope agreement. Any additional sources will be handled via the change control process (Section 10).
3. **Application development** — no changes to the WMPP application front-end, back-end, or API layer.
4. **Data migration beyond CSV scope** — migration of data stores not related to the current CSV pipeline is excluded.
5. **Network infrastructure changes** — client network, VPN, firewall, or Active Directory configuration changes are the responsibility of the client's IT team.
6. **Licensing procurement** — Fabric capacity licensing, Power BI Premium per-user licensing, and Azure storage costs are the client's responsibility. The consultant will advise on appropriate SKUs but does not procure licences on behalf of the client.
7. **Ongoing operational support beyond hypercare** — post-hypercare, ongoing maintenance, monitoring, and enhancement will be governed by a separate support agreement.
8. **Report redesign** — visual design changes beyond those necessitated by Direct Lake migration are excluded. The consultant will migrate existing visuals; cosmetic redesign is out of scope.
9. **Additional KPIs beyond the agreed 117** — any KPIs identified after scope agreement will be processed via change control.
10. **Mobile/reporting server configuration** — configuration of Power BI Report Server, paginated reports, or mobile report publishing is excluded.

---

## 3. Delivery Approach

The engagement is structured into three sequential phases over a twelve (12) week period. Each phase has defined entry criteria, deliverables, and exit gates. Phases are sequential — a phase cannot commence until the preceding phase's exit criteria are met.

### Phase 1: Foundation & Bronze-Silver Pipeline (Weeks 1–4)

**Objective:** Establish the Fabric lakehouse infrastructure and deploy the bronze and silver data pipeline layers.

**Key Activities:**
- Fabric capacity provisioning, workspace creation, and lakehouse setup.
- ADLS Gen2 storage configuration and Fabric shortcuts to CSV source locations.
- Source file inventory and schema mapping documentation.
- Bronze loader notebook development, testing, and deployment.
- Silver formatter notebook development, testing, and deployment.
- End-to-end bronze → silver pipeline execution and validation.
- Reconciliation of silver-layer data against source CSV files (row counts, checksums).
- Initial data validation report production.

**Entry Criteria:**
- Fabric capacity licensed and accessible.
- Client provides access to network drive CSV source locations.
- Client provides current Power BI report (V13.1) and measure documentation.
- Kick-off meeting completed.

**Exit Criteria:**
- Bronze and silver notebooks deployed and executing successfully.
- Silver-layer data reconciles with source CSV files within agreed tolerance (≤0.01% variance).
- Data validation report produced and accepted by client technical lead.

### Phase 2: Gold Layer & KPI Implementation (Weeks 5–8)

**Objective:** Deploy the gold translator notebook, migrate all 90 existing measures, and implement 27 new measures as Spark SQL views.

**Key Activities:**
- Gold translator notebook development and deployment.
- Migration of 90 existing DAX measures to gold-layer Spark SQL views, with one-to-one reconciliation against current PBI report values.
- Implementation of 27 new measures across seven functional gap categories.
- Duplicate measure consolidation (identification, stakeholder confirmation, merge).
- Measure name corrections with documented rename mapping.
- Unit testing of each KPI view (logic validation, null handling, edge cases).
- Full reconciliation report: gold KPI values vs. PBI report V13.1 values for the 90 migrated measures.
- Stakeholder review of 27 new measures for business logic sign-off.

**Entry Criteria:**
- Phase 1 exit criteria met and signed off.
- Client confirms business logic definitions for 27 new measures.
- Client confirms duplicate consolidation mapping.

**Exit Criteria:**
- All 117 KPIs implemented as gold-layer Spark SQL views.
- 90 migrated KPIs reconcile with current PBI report within agreed tolerance (≤0.1% variance).
- 27 new KPIs signed off by business stakeholders.
- Duplicate measures consolidated; naming corrections applied.
- Unit test results documented and accepted.

### Phase 3: Power BI Integration & Migration (Weeks 9–12)

**Objective:** Connect Power BI via Direct Lake, migrate dashboards, implement RLS, conduct UAT, and hand over.

**Key Activities:**
- Power BI Direct Lake connection configuration to gold-layer Delta tables.
- Dashboard migration: visuals, layouts, navigation, bookmarks from V13.1 to the new Direct Lake dataset.
- Visual reconfiguration where Direct Lake semantic model differences require adjustment.
- RLS implementation for commissioner regional access (R55) — row-level filters for each of the 14 local authorities.
- RLS testing with test accounts across all authority regions.
- Performance testing and optimisation (target: dashboard load < 5 seconds).
- User Acceptance Testing with stakeholder representatives (placement officers, QA, commissioners, finance).
- Parallel running of Fabric pipeline alongside network-drive CSV pipeline (minimum 2 weeks).
- Decommissioning of network-drive CSV pipeline following parallel run sign-off.
- Training sessions: technical handover (client technical lead), end-user training (placement officers, QA, commissioners, finance).
- Final documentation delivery: architecture diagrams, notebook guides, KPI dictionary, RLS config guide, troubleshooting runbook, training materials.

**Entry Criteria:**
- Phase 2 exit criteria met and signed off.
- Client provides test user accounts for RLS verification across all 14 authorities.
- Client nominates UAT participants from each stakeholder group.

**Exit Criteria:**
- Power BI Direct Lake report deployed and accessible to all stakeholders.
- RLS verified for all 14 local authority commissioner regions.
- Dashboard load performance < 5 seconds (validated via performance testing).
- UAT sign-off obtained from client sponsor.
- Parallel run completed with no data loss or material discrepancies.
- Network-drive CSV pipeline decommissioned.
- Training delivered; documentation accepted.
- Hypercare period commenced.

---

## 4. Deliverables

### 4.1 Phase 1 Deliverables

| Ref | Deliverable | Description | Acceptance Criteria |
|---|---|---|---|
| D1.1 | Fabric Lakehouse | Provisioned lakehouse with bronze, silver, gold schemas, workspaces, and access controls | Lakehouse accessible; schemas created; access policies enforced |
| D1.2 | ADLS Gen2 Configuration | Storage account configuration and Fabric shortcuts to CSV source locations | Shortpoints resolve; CSV files accessible from Fabric notebooks |
| D1.3 | Bronze Loader Notebook | Spark notebook for automated CSV → Delta ingestion | Executes successfully; idempotent; metadata captured |
| D1.4 | Silver Formatter Notebook | Spark notebook for schema enforcement, type casting, data quality flags | Schema enforced; type errors flagged; deduplication operational |
| D1.5 | Data Validation Report | Reconciliation report: silver data vs. source CSV files | Variance ≤ 0.01%; report accepted by client technical lead |
| D1.6 | Pipeline Architecture Diagram | Visual documentation of bronze-silver architecture | Reviewed and accepted by client technical lead |

### 4.2 Phase 2 Deliverables

| Ref | Deliverable | Description | Acceptance Criteria |
|---|---|---|---|
| D2.1 | Gold Translator Notebook | Spark notebook for gold-layer KPI view generation | Executes successfully; all 117 views created |
| D2.2 | 90 Migrated KPI Spark SQL Views | Gold-layer views replicating existing PBI measures | Each view reconciles with PBI V13.1 ≤ 0.1% variance |
| D2.3 | 27 New KPI Spark SQL Views | Gold-layer views for new measures across 7 categories | Each view signed off by business stakeholder |
| D2.4 | Duplicate Consolidation Report | Documentation of merged duplicate measures | Mapping confirmed by client; duplicates resolved |
| D2.5 | Measure Name Correction Log | Documented rename mapping for typographical corrections | Corrections applied; mapping documented; client notified |
| D2.6 | Unit Test Results | Test documentation for all 117 KPI views | All tests pass; edge cases documented; results accepted |
| D2.7 | KPI Dictionary | Business and technical definition for each of 117 KPIs | Reviewed by client; published to documentation repository |

### 4.3 Phase 3 Deliverables

| Ref | Deliverable | Description | Acceptance Criteria |
|---|---|---|---|
| D3.1 | Power BI Direct Lake Report | Migrated report connected to gold tables via Direct Lake | All visuals functional; sub-5s load; no data loss vs V13.1 |
| D3.2 | RLS Configuration | Role-level security for 14 local authority commissioner regions | Verified with test accounts; no cross-region data leakage |
| D3.3 | UAT Sign-Off Document | Formal UAT completion record with stakeholder signatures | All critical UAT defects resolved; sign-off obtained |
| D3.4 | Parallel Run Report | Results of parallel running period | No material discrepancies; report accepted by client sponsor |
| D3.5 | Decommissioning Record | Documentation of network-drive CSV pipeline decommissioning | Pipeline disabled; archival complete; sign-off recorded |
| D3.6 | Training Materials | User guides and training session recordings for all stakeholder groups | Materials delivered; training sessions completed |
| D3.7 | Technical Documentation | Architecture diagrams, notebook guides, RLS config, troubleshooting runbook | Complete documentation set; accepted by client technical lead |

---

## 5. Roles & Responsibilities

The following RACI matrix defines responsibilities across the engagement. R = Responsible, A = Accountable, C = Consulted, I = Informed.

| Activity | Data Engineer (Lead) | Power BI Developer | Client Sponsor | Client Technical Lead | Stakeholder Group |
|---|---|---|---|---|---|
| Fabric capacity & lakehouse setup | R | C | I | A | I |
| ADLS Gen2 & shortcut configuration | R | I | I | A | I |
| Bronze loader notebook | R | I | I | A | I |
| Silver formatter notebook | R | I | I | A | I |
| Data validation & reconciliation | R | C | I | A | C |
| Gold translator notebook | R | C | I | A | I |
| 90 measure migration | R | C | I | A | C |
| 27 new measure implementation | R | C | I | A | C |
| Duplicate consolidation | R | I | I | A | C |
| Measure name corrections | R | I | I | A | C |
| Unit testing | R | C | I | A | I |
| PBI Direct Lake connection | C | R | I | A | I |
| Dashboard migration | C | R | I | A | C |
| RLS implementation | C | R | I | A | C |
| Performance optimisation | C | R | I | A | I |
| UAT coordination | C | R | A | C | R |
| Parallel running | R | C | I | A | C |
| Decommissioning | R | C | A | C | I |
| Training delivery | C | R | I | A | R |
| Documentation | R | R | I | A | I |
| Phase sign-off | C | C | A | C | I |

### 5.1 Role Descriptions

- **Data Engineer (Lead):** Primary technical resource responsible for Fabric lakehouse architecture, Spark notebook development (bronze, silver, gold), data pipeline implementation, and overall technical delivery quality.
- **Power BI Developer:** Responsible for Power BI Direct Lake connection, dashboard migration, visual reconfiguration, RLS implementation, performance optimisation, and end-user training delivery.
- **Client Sponsor:** Senior client representative accountable for engagement outcomes, phase sign-off, budget approval, and escalation resolution.
- **Client Technical Lead:** Client-side technical owner responsible for environment access, technical reviews, acceptance of deliverables, and post-handover operational ownership.
- **Stakeholder Group:** Representatives from placement officers, QA analysts, commissioners, and finance users who participate in requirements confirmation, UAT, and training.

---

## 6. Assumptions & Prerequisites

### 6.1 Assumptions

1. The client has, or will procure, appropriate Microsoft Fabric capacity (F-SKU or equivalent) before Phase 1 commencement.
2. The client holds appropriate Power BI licensing (Premium per-user or Premium per-capacity) for Direct Lake connectivity.
3. The client's IT team will provide network access to CSV source file locations from the Fabric tenant.
4. The current Power BI report (V13.1) and its 90 measures represent the complete and accurate current-state measure set at the time of scope agreement.
5. Business logic definitions for the 27 new measures will be confirmed by the client within Phase 1, no later than end of Week 4.
6. The client will nominate UAT participants from each stakeholder group by the start of Phase 3 (Week 9).
7. The client will provide test user accounts for RLS verification across all 14 local authority regions by the start of Phase 3 (Week 9).
8. No material changes to source CSV file structures or naming conventions will occur during the engagement. Any such changes will be managed via the change control process (Section 10).
9. The consultant will have remote access to the client's Fabric workspace, Power BI service, and source file locations for the duration of the engagement.
10. The client will respond to review and sign-off requests within five (5) working days to maintain the project timeline.

### 6.2 Prerequisites (Client Must Provide)

| Ref | Prerequisite | Required By | Owner |
|---|---|---|---|
| P1 | Microsoft Fabric capacity licensed and provisioned | Phase 1 kick-off | Client Sponsor / IT |
| P2 | Power BI Premium licensing (per-user or per-capacity) | Phase 3 commencement | Client Sponsor / IT |
| P3 | Network access to CSV source file locations (SMB/file share or ADLS Gen2 migration) | Phase 1 kick-off | Client IT |
| P4 | Current Power BI report file (V13.1) and dataset | Phase 1 kick-off | Client Technical Lead |
| P5 | Measure documentation / DAX expressions for 90 existing measures | Phase 1, Week 1 | Client Technical Lead |
| P6 | Business logic definitions for 27 new measures | Phase 1, Week 4 | Stakeholder Group |
| P7 | Confirmed duplicate measure consolidation mapping | Phase 2, Week 5 | Client Technical Lead |
| P8 | Test user accounts for RLS (14 local authority regions) | Phase 3, Week 9 | Client IT |
| P9 | Nominated UAT participants (placement officers, QA, commissioners, finance) | Phase 3, Week 9 | Client Sponsor |
| P10 | Fabric workspace admin access for consultant team | Phase 1 kick-off | Client IT |
| P11 | Azure tenant access for ADLS Gen2 configuration | Phase 1 kick-off | Client IT |
| P12 | Source CSV file inventory and data dictionary | Phase 1, Week 1 | Client Technical Lead |

---

## 7. Acceptance Criteria

The following measurable success criteria must be met for engagement completion and final sign-off:

| Ref | Criterion | Measurement | Target |
|---|---|---|---|
| AC1 | KPI Reconciliation — Migrated Measures | Gold KPI values vs. PBI V13.1 values | ≤ 0.1% variance for all 90 migrated measures |
| AC2 | KPI Reconciliation — New Measures | Business stakeholder sign-off | 100% of 27 new measures signed off |
| AC3 | Total KPI Count | Spark SQL views in gold layer | 117 KPIs (90 migrated + 27 new) |
| AC4 | Dashboard Load Performance | Time-to-first-render measured in Power BI Service | < 5 seconds for primary dashboard pages |
| AC5 | Data Loss Prevention | Comparison of row counts and key metrics vs. current report | Zero (0) data loss incidents |
| AC6 | RLS Verification | Testing with test accounts across 14 authorities | 100% of authorities verified; zero cross-region data leakage |
| AC7 | Bronze-Silver Reconciliation | Silver data vs. source CSV files | ≤ 0.01% variance |
| AC8 | Unit Test Pass Rate | Automated unit tests for all notebook transformations | 100% pass rate |
| AC9 | UAT Completion | Formal UAT sign-off document | Signed by client sponsor; all critical defects resolved |
| AC10 | Parallel Run | Fabric pipeline vs. network-drive CSV pipeline (minimum 2 weeks) | No material discrepancies (≤ 0.1% variance on all KPIs) |
| AC11 | Decommissioning | Network-drive CSV pipeline | Formally decommissioned; archival complete; sign-off recorded |
| AC12 | Training Delivery | Training sessions completed for all stakeholder groups | 100% of scheduled sessions delivered; attendance recorded |
| AC13 | Documentation Completeness | Final documentation set delivered | All documents (D3.7) accepted by client technical lead |

---

## 8. Commercial Summary

### 8.1 Engagement Type

This engagement is delivered on a **fixed-fee basis** for the agreed scope, with a **day-rate provision** for any additional work authorised via the change control process (Section 10).

### 8.2 Fee Structure

| Component | Description | Duration | Rate | Fee |
|---|---|---|---|---|
| Phase 1 | Foundation & Bronze-Silver Pipeline | 4 weeks | [TBC] | [TBC] |
| Phase 2 | Gold Layer & KPI Implementation | 4 weeks | [TBC] | [TBC] |
| Phase 3 | Power BI Integration & Migration | 4 weeks | [TBC] | [TBC] |
| **Total Fixed Fee** | | **12 weeks** | | **[TBC]** |

### 8.3 Additional Cost Items

| Item | Description | Basis | Fee |
|---|---|---|---|
| Hypercare Support | Post-go-live support | 2 weeks (10 working days) | [TBC] |
| Additional Work (Change Control) | Scope additions authorised via change control | Per day | [TBC] / day |
| Additional Resource | Additional consultant engagement beyond agreed team | Per day | [TBC] / day |
| Expenses | Travel, accommodation (if on-site required) | Reimbursement at cost | At cost |

### 8.4 Payment Schedule

| Milestone | Trigger | Payment |
|---|---|---|
| Milestone 1 | Phase 1 sign-off (end of Week 4) | [TBC]% of total fixed fee |
| Milestone 2 | Phase 2 sign-off (end of Week 8) | [TBC]% of total fixed fee |
| Milestone 3 | Phase 3 sign-off & UAT acceptance (end of Week 12) | [TBC]% of total fixed fee |
| Milestone 4 | Hypercare completion (end of Week 14) | [TBC]% of total fixed fee |

### 8.5 Notes

- All fees are exclusive of applicable taxes (VAT at prevailing rate).
- Microsoft Fabric capacity, Power BI licensing, and Azure storage costs are the client's responsibility and are not included in the fees above.
- Day rates for additional work will be agreed at [TBC] and documented in the change control record.
- Hypercare scope: business-hours support (09:00–17:00, Monday–Friday), remote, for priority P1/P2 incidents related to delivered pipeline and report.

---

## 9. Timeline & Milestones

| Phase | Milestone | Duration | Target Date |
|---|---|---|---|
| Phase 1 | Kick-off & Fabric environment setup | Week 1 | 14 July 2026 |
| Phase 1 | ADLS Gen2 & shortcuts configured | Week 2 | 21 July 2026 |
| Phase 1 | Bronze loader notebook deployed | Week 3 | 28 July 2026 |
| Phase 1 | Silver formatter notebook deployed | Week 4 | 04 August 2026 |
| Phase 1 | Data validation report & Phase 1 sign-off | End of Week 4 | 08 August 2026 |
| Phase 2 | Gold translator notebook deployed | Week 5 | 11 August 2026 |
| Phase 2 | 90 measures migrated to gold SQL views | Week 6 | 18 August 2026 |
| Phase 2 | 27 new measures implemented | Week 7 | 25 August 2026 |
| Phase 2 | Duplicate consolidation & name corrections | Week 7 | 25 August 2026 |
| Phase 2 | Unit testing & reconciliation complete | Week 8 | 01 September 2026 |
| Phase 2 | Phase 2 sign-off | End of Week 8 | 05 September 2026 |
| Phase 3 | Direct Lake connection configured | Week 9 | 08 September 2026 |
| Phase 3 | Dashboard migration & visual reconfiguration | Week 9–10 | 15 September 2026 |
| Phase 3 | RLS implementation & testing | Week 10 | 22 September 2026 |
| Phase 3 | Performance optimisation | Week 10 | 22 September 2026 |
| Phase 3 | UAT execution with stakeholders | Week 11 | 29 September 2026 |
| Phase 3 | Parallel running (2 weeks) | Weeks 11–12 | 29 September – 06 October 2026 |
| Phase 3 | Decommissioning of CSV pipeline | Week 12 | 06 October 2026 |
| Phase 3 | Training delivery | Week 12 | 06 October 2026 |
| Phase 3 | Final documentation & Phase 3 sign-off | End of Week 12 | 10 October 2026 |
| Hypercare | Post-go-live support | Weeks 13–14 | 10–24 October 2026 |
| Hypercare | Hypercare completion & engagement closure | End of Week 14 | 24 October 2026 |

**Total engagement duration:** 14 weeks (12 weeks delivery + 2 weeks hypercare).

---

## 10. Change Control Process

### 10.1 Purpose

This change control process governs any modification to the agreed scope, timeline, deliverables, or commercial terms of this Statement of Work. No work outside the agreed scope will commence without an authorised change control record.

### 10.2 Change Request Initiation

Any party (client or consultant) may initiate a change request by submitting a written Change Request (CR) to the designated representatives:
- **Client representative:** [Client Technical Lead name placeholder]
- **Consultant representative:** [Consultant Name placeholder]

The CR must include:
1. Description of the requested change.
2. Rationale / business justification.
3. Impact assessment (scope, timeline, cost, resources, risks).
4. Priority (Critical / High / Medium / Low).

### 10.3 Change Request Evaluation

The designated representatives will evaluate the CR within five (5) working days of submission. The evaluation will determine:
- Whether the change is in-scope (no additional cost) or out-of-scope (additional cost and/or timeline impact).
- The estimated effort, cost, and schedule impact.
- Any dependencies or risks introduced.

### 10.4 Change Request Approval

Changes are approved as follows:
- **In-scope changes (no cost/timeline impact):** Approved jointly by the client technical lead and consultant lead.
- **Out-of-scope changes (cost and/or timeline impact):** Approved by the client sponsor and consultant commercial lead. A formal Change Order will be issued referencing this SoW.

### 10.5 Change Request Register

All CRs will be logged in a Change Request Register maintained by the consultant and shared with the client. The register will track:
- CR reference number
- Date raised
- Requestor
- Description
- Impact assessment
- Decision (approved / rejected / deferred)
- Decision date
- Implementation status

### 10.6 Scope Creep Prevention

The consultant will flag any activity that appears to extend beyond the agreed scope and will seek written authorisation before commencing such work. The client acknowledges that unauthorised scope extensions will not be deliverable within the agreed timeline or fee.

---

## 11. Sign-Off

### 11.1 Statement of Work Acceptance

By signing below, the parties acknowledge that they have read, understood, and agreed to the terms, scope, deliverables, acceptance criteria, commercial summary, and timeline set out in this Statement of Work.

| Party | Name | Role | Signature | Date |
|---|---|---|---|---|
| Client | [Client Sponsor Name] | Client Sponsor | _________________ | __________ |
| Client | [Client Technical Lead Name] | Client Technical Lead | _________________ | __________ |
| Consultant | [Consultant Name] | Engagement Lead | _________________ | __________ |
| Consultant | [Consultancy Commercial Lead] | Commercial Authority | _________________ | __________ |

### 11.2 Phase Sign-Off Records

Phase sign-off will be recorded separately upon completion of each phase's exit criteria. The sign-off records will reference this SoW and the applicable acceptance criteria defined in Section 7.

| Phase | Sign-Off Date | Client Signatory | Consultant Signatory |
|---|---|---|---|
| Phase 1 — Foundation & Bronze-Silver Pipeline | __________ | __________ | __________ |
| Phase 2 — Gold Layer & KPI Implementation | __________ | __________ | __________ |
| Phase 3 — Power BI Integration & Migration | __________ | __________ | __________ |
| Hypercare Completion & Engagement Closure | __________ | __________ | __________ |

### 11.3 Document Control

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 12 July 2026 | [Consultant Name] | Initial draft for client review |

---

*End of Statement of Work — WMPP-DE-SoW-001*
