# HOLD Register

## Assumptions, Constraints, Dependencies & Decisions

| **Field** | **Value** |
|---|---|
| **Project** | WMPP — West Midlands Placement Portal |
| **Document Title** | HOLD Register |
| **Document Reference** | WMPP-DOC-05 |
| **Version** | 1.0 |
| **Date** | 12 July 2026 |
| **Author** | Fabric Data Platform Delivery Team |
| **Status** | Draft for Client Review |
| **Classification** | OFFICIAL — SENSIVE |
| **Distribution** | WMPP Programme Board, LA Data Leads, Technical Architecture Group |

---

## 1. Document Purpose & Scope

### 1.1 Purpose

This HOLD Register constitutes the authoritative record of **Assumptions**, **Constraints**, **Dependencies**, and **Decisions** (collectively "HOLD") identified during the delivery of the West Midlands Placement Portal (WMPP) data platform migration. It serves as a living governance artefact, ensuring that all foundational premises underpinning the solution design are explicitly documented, validated, and tracked throughout the project lifecycle.

The register is maintained under formal change control. Any material change to an assumption, constraint, dependency, or decision recorded herein must be submitted to the WMPP Programme Board for approval before implementation.

### 1.2 Scope

This register encompasses all HOLD items relating to:

- The migration from the current-state Power BI report (V13.1) and CSV-on-network-drive data pipeline to a Microsoft Fabric lakehouse with medallion (bronze-silver-gold) architecture.
- The functional scope defined in the Functional Specification (requirements R1–R87) and the KPI Logic Document (117 KPIs).
- The cross-authority operating model spanning 14 West Midlands local authorities.
- The technical, regulatory, commercial, and operational parameters within which the solution must be delivered.

### 1.3 Document Structure

| **Section** | **Content** |
|---|---|
| Section 2 | Assumptions Register |
| Section 3 | Constraints Register |
| Section 4 | Dependencies Register |
| Section 5 | Decisions Log |
| Section 6 | Open Items Requiring Client Input |
| Section 7 | Change Log |

### 1.4 Related Documents

| **Ref** | **Document** | **Version** |
|---|---|---|
| WMPP-FN-001 | Functional Specification (R1–R87) | 1.0 |
| WMPP-KPI-001 | KPI Logic Document — H. K. Jakhu | 23 June 2026 |
| WMPP-ARC-001 | Target Architecture Design Document | 0.9 (Draft) |
| WMPP-GAP-001 | Functional Gap Analysis (17 gaps) | 1.0 |
| WMPP-PBI-001 | Power BI Report V13.1 — Current State | 13.1 |
| WMPP-CSV-001 | CSV Source File Inventory & Schema Definition | 1.0 |

---

## 2. Assumptions Register

The following assumptions have been made during the planning, design, and delivery phases. Each assumption carries an associated risk if proven invalid. Assumptions marked with status **⚠ VALIDATION REQUIRED** must be confirmed by the client before the relevant workstream can proceed beyond the identified milestone.

| **ID** | **Assumption** | **Source** | **Impact if Invalid** | **Owner** |
|---|---|---|---|---|
| A-001 | The client has or will procure Microsoft Fabric capacity at a minimum of F4 SKU (64 Capacity Units). | Target Architecture Design (WMPP-ARC-001) | Insufficient capacity will prevent Direct Lake mode operation, increase query latency, and may require fallback to Import mode with reduced refresh frequency. Cost re-baselining required. | Programme Sponsor (Client) |
| A-002 | CSV file exports from the PostgreSQL source database will continue to be available during the transition period, maintaining the existing export schedule and file format. | Current-state analysis; PBI V13.1 data lineage | Bronze layer ingestion pipeline will fail. Contingency: direct PostgreSQL connector must be developed as a replacement, adding an estimated 3–5 weeks to the delivery timeline. | Data Engineering Lead |
| A-003 | The Functional Specification document (R1–R87) is the authoritative and complete statement of functional requirements. No requirements exist outside this document that have not been captured. | Functional Specification (WMPP-FN-001) | Undocumented requirements may emerge during UAT, triggering change requests and potential rework of silver/gold layer transformations. | Business Analyst |
| A-004 | The KPI Logic Document authored by Hamant K. Jakhu (dated 23 June 2026) is the authoritative source for all 117 KPI definitions, including calculation logic, filtering rules, and granularity. | KPI Logic Document (WMPP-KPI-001) | Incorrect KPI calculations will propagate into the gold layer and semantic model, producing inaccurate management information for 14 LAs. Reconciliation effort estimated at 2–3 weeks per affected KPI batch. | Data Engineering Lead |
| A-005 | All 14 West Midlands local authorities will adopt the solution and complete the onboarding process within the planned migration window. | Programme mandate; R3 (cross-boundary placements) | Reduced adoption will necessitate phased rollout, partial RLS configuration, and revised capacity sizing. Benefits realisation will be deferred for non-participating LAs. | Programme Sponsor (Client) |
| A-006 | Network drives currently hosting CSV files will be decommissioned after lakehouse migration is complete and validated. No ongoing parallel reporting from network drives will be required. | Migration plan; current-state CSV inventory | Dual-running costs will be incurred. Data lineage ambiguity between legacy and target systems. Decommissioning deferment impacts storage cost savings. | Infrastructure Manager (Client) |
| A-007 | The PostgreSQL source database remains the system of record for all placement, referral, and provider data. The Fabric lakehouse is a reporting and analytics platform only — no write-back to source systems. | Architecture decision; R74 (commercially available components) | If write-back is required, additional integration middleware, transaction management, and conflict resolution mechanisms must be designed and built. Estimated 6–8 weeks additional effort. | Solution Architect |
| A-008 | A daily refresh cadence (once per 24-hour period) is acceptable for all reporting requirements. No KPI requires near-real-time or intraday refresh. | KPI Logic Document; Functional Specification | If intraday refresh is required, Direct Lake mode may be insufficient. Streaming pipelines or near-real-time event ingestion must be designed, significantly increasing complexity and cost. | Business Analyst |
| A-009 | The `is_spot` flag in the source data is NOT equivalent to `is_emergency`. These are conceptually distinct attributes and must not be used interchangeably. This is the basis of functional gap R18. | Functional Gap Analysis (WMPP-GAP-001); R18 | If `is_spot` is used as a proxy for `is_emergency`, emergency placement KPIs will be materially overstated or understated. A new `is_emergency` column must be added to `dim_referral` in the silver layer. | Data Engineering Lead |
| A-010 | The existing 90 measures in Power BI report V13.1 are the complete inventory of current-state calculations. No hidden, orphaned, or undocumented measures exist in the PBIX file. | PBI V13.1 audit; measure inventory | Orphaned measures may cause confusion during reconciliation. Duplicate measure consolidation in the gold layer may miss undocumented variants. | Power BI Developer |
| A-011 | Client IT operations will provide network connectivity (ExpressRoute or equivalent) between LA on-premises estates and the Azure/Fabric tenant with sub-50ms latency. | Target Architecture Design (WMPP-ARC-001) | High latency will degrade CSV ingestion performance and may impact Direct Lake query response times. Contingency: batch-optimised ingestion windows outside business hours. | Infrastructure Manager (Client) |
| A-012 | The schema definition file (`schema_definition.csv`) accurately reflects the data types, nullability constraints, and business keys for all source CSV files. | CSV Source File Inventory (WMPP-CSV-001) | Incorrect schema definitions will cause silver-layer type enforcement failures, data quality rejections, and potential data loss during transformation. | Data Engineering Lead |
| A-013 | Entra ID (Azure AD) is the identity provider for all 14 LAs, or federated trust relationships can be established for non-Azure AD authorities. | Architecture decision; R55 (RLS) | LAs without Entra ID integration cannot access the Fabric workspace. Alternative authentication paths (B2B guest accounts) must be configured, adding complexity to RLS implementation. | Security Architect (Client) |

---

## 3. Constraints Register

Constraints are fixed parameters that bound the solution design and delivery. They are non-negotiable unless formally escalated to the Programme Board and approved as a variation.

| **ID** | **Constraint** | **Type** | **Rationale** | **Impact** |
|---|---|---|---|---|
| C-001 | Full compliance with UK GDPR and the Data Protection Act 2018 is mandatory. Data subject rights, lawful basis, data minimisation, and retention must be implemented. | Regulatory | The platform processes personal data relating to vulnerable children — one of the most sensitive data categories under Article 9 of UK GDPR. Non-compliance carries regulatory action, reputational damage, and potential criminal liability. | All data flows must include DPIA assessment. Pseudonymisation or anonymisation must be applied where feasible in silver/gold layers. Retention policies must be configurable per LA (see R84). Audit trails must be immutable. |
| C-002 | WCAG 2.0 (minimum) and WCAG 2.1 (target) accessibility compliance is required for all user-facing components. | Regulatory | Statutory obligation under the Equality Act 2010 and Public Sector Bodies (Websites and Mobile Applications) Accessibility Regulations 2018. Requirement R81. | Power BI report design must conform to accessibility patterns: alt text on visuals, keyboard navigation, colour contrast ratios ≥4.5:1, screen reader compatibility. Additional QA effort in UAT phase. |
| C-003 | The solution must use open-source technologies wherever possible, minimising proprietary lock-in. | Commercial | Requirement R4. Public sector value-for-money obligation. Reduces total cost of ownership and supports supplier neutrality. | Fabric lakehouse uses Delta Lake (open source). Spark SQL (open source). Power BI semantic model is proprietary but justified as the existing reporting standard. Any new components must be assessed against this constraint. |
| C-004 | Agile delivery methodology must be used, with iterative sprints, demonstrable increments, and continuous stakeholder feedback. | Operational | Requirement R5. Aligns with UK Government Digital Service (GDS) Service Standard. Supports adaptive planning for a 14-LA stakeholder group with evolving needs. | Delivery plan structured in 2-week sprints. Sprint reviews with LA representatives. Backlog grooming sessions. Documentation produced incrementally alongside code. |
| C-005 | The solution must support cross-boundary placements across all 14 West Midlands LAs, each with potentially different IT estates, data standards, and access policies. | Technical | Requirement R3. Core programme objective — a child placed in Authority A by Authority B must be visible to both. | RLS must accommodate multi-authority data sharing patterns. Data model must support a many-to-many relationship between placement and authority. Entra ID group structure must reflect cross-boundary access needs. |
| C-006 | The existing Power BI report V13.1 must remain fully operational during migration. No "big-bang" cutover is permitted. | Operational | Business continuity — 14 LAs depend on current reports for statutory reporting and operational management. Any reporting outage risks safeguarding delays. | Dual-running period required. CSV-based pipeline and new Fabric pipeline must operate in parallel. Reconciliation between V13.1 and gold-layer outputs must be demonstrated before cutover sign-off. |
| C-007 | Commercially available off-the-shelf components are preferred over bespoke development. | Commercial | Requirements R6 and R74. Reduces maintenance burden, accelerates delivery, and leverages vendor support arrangements. | Fabric-native capabilities (pipelines, dataflows, shortcuts) are used in preference to custom code. Where bespoke DAX or Spark SQL is unavoidable, it must be documented and peer-reviewed. |
| C-008 | The solution must provide high availability, scalability, fault tolerance, and disaster recovery capabilities. | Technical | Requirement R75. The platform supports child safeguarding decisions — unplanned downtime is unacceptable. | Fabric capacity provides inherent HA within a region. DR strategy must include geo-redundant storage for bronze-layer raw data. Gold-layer semantic model must have a documented recovery procedure with RTO ≤ 4 hours and RPO ≤ 24 hours. |
| C-009 | Data retention policies must be configurable per local authority and per data category. | Regulatory | Requirement R84. Different LAs may have different retention obligations based on local safeguarding partnership agreements. Legal advice may vary by authority. | Retention metadata must be stored at the table/partition level. Automated purging or archiving must be configurable. Audit trail of purged records must be maintained. |
| C-010 | Break-glass (emergency) access must be controlled, time-limited, and fully auditable. | Regulatory | Requirement R79. Safeguarding situations may require immediate data access outside normal RLS scope. However, unrestricted access creates significant safeguarding and data protection risks. | Break-glass accounts must use Just-In-Time (JIT) access via Privileged Identity Management (PIM) or equivalent. All break-glass sessions must be logged and reviewed within 48 hours by the Information Governance Lead. |
| C-011 | All data at rest must be encrypted. All data in transit must use TLS 1.2 or above. | Regulatory | UK GDPR Article 32 — security of processing. Azure Platform provides encryption at rest by default. | No additional cost impact. Configuration validation required in deployment scripts. Customer-managed keys (CMK) may be required if client policy mandates. |
| C-012 | The solution must not store or process data outside the UK. | Regulatory | Data residency obligation for public sector children's services data. | Fabric capacity must be provisioned in a UK Azure region. All storage accounts, workspaces, and semantic models must be pinned to UK regions. Shortcuts must not reference cross-region storage. |
| C-013 | The total project budget envelope must not be exceeded without formal change control approval. | Commercial | Public sector financial governance. Funding is committed by the 14 participating LAs under a section 75 agreement. | All design decisions must include cost impact assessment. Fabric capacity sizing must be validated against expected workload before scale-up. |
| C-014 | Changes to the source PostgreSQL database schema are outside the scope of this project. | Technical | The source system is owned and operated by a third-party supplier. Schema changes require a separate change request to the source system vendor. | The silver layer must be resilient to minor source schema drift (column additions). Any source schema changes required (e.g., `is_emergency` column) must be recommended as a formal change request, not implemented directly. |

---

## 4. Dependencies Register

Dependencies are relationships where the completion or availability of one item is contingent upon another. Dependencies marked as **External** require action by the client or a third party and are outside the delivery team's direct control.

| **ID** | **Dependency** | **Dependency Type** | **Dependent On** | **Status** | **Required By** |
|---|---|---|---|---|---|
| D-001 | Azure tenant exists and Fabric capacity (minimum F4) is provisioned in a UK region. | External | Client IT / Azure subscription owner | ⚠ Not Started — awaiting client confirmation | Sprint 1 — Bronze layer build |
| D-002 | Fabric lakehouse created with workspace assigned to Fabric capacity. | Internal | D-001 (Fabric capacity provisioning) | ⚠ Blocked by D-001 | Sprint 1 — Bronze layer build |
| D-003 | ADLS Gen2 storage account provisioned and Fabric shortcuts configured to reference bronze-layer landing zone. | Internal | D-001, D-002 | ⚠ Blocked by D-001 | Sprint 1 — Bronze layer build |
| D-004 | Entra ID user accounts and security groups provisioned for all 14 LAs, mapped to RLS roles. | External | Client Identity & Access Management team | ⚠ Not Started — LA group structure not yet defined | Sprint 3 — RLS configuration (R55) |
| D-005 | Row-Level Security (RLS) configuration in the Power BI semantic model, implementing authority-scoped data access per R55. | Internal | D-004 (Entra ID groups), Gold layer completion | ⚠ Blocked by D-004 | Sprint 4 — Semantic model deployment |
| D-006 | Read access to network drives hosting CSV source files during the transition/dual-running period. | External | Client infrastructure team; LA data custodians | ✅ Confirmed for current V13.1 pipeline; ⚠ Access for new Fabric pipeline pending | Sprint 1 — Bronze layer ingestion |
| D-007 | PostgreSQL database connectivity (network-level access, firewall rules, credentials) for schema validation and potential direct extraction. | External | Client database administration team | ⚠ Not Started — credentials and firewall rules not yet provided | Sprint 2 — Silver layer schema enforcement |
| D-008 | Azure Key Vault provisioned for storage of connection strings, storage account keys, and any secrets used by Fabric pipelines. | External | Client DevOps / Platform team | ⚠ Not Started — awaiting client infrastructure request | Sprint 1 — Pipeline development |
| D-009 | Power BI workspace created and assigned to Fabric capacity (Premium or Fabric capacity). | Internal | D-001 (Fabric capacity), D-002 (lakehouse) | ⚠ Blocked by D-001 | Sprint 4 — Semantic model deployment |
| D-010 | Functional Specification (R1–R87) signed off by all 14 LA business leads. | External | WMPP Programme Board; LA business leads | ⚠ In Review — 9 of 14 LAs have signed off | Sprint 2 — Silver layer business rules |
| D-011 | KPI Logic Document (117 KPIs) validated and baselined by the business. | External | Hamant K. Jakhu (author); WMPP Programme Board | ⚠ In Review — minor revisions requested on 8 KPIs | Sprint 3 — Gold layer KPI views |
| D-012 | `schema_definition.csv` reviewed and approved by the data engineering team and source system SME. | Internal | Source system SME; Data Engineering Lead | ✅ Complete — v1.0 approved | Sprint 2 — Silver layer build |
| D-013 | Data Protection Impact Assessment (DPIA) completed and approved by the client's Data Protection Officer (DPO). | External | Client DPO / Information Governance team | ⚠ In Progress — draft DPIA circulated, feedback expected | Sprint 1 — before any production data ingestion |
| D-014 | Change Advisory Board (CAB) approval for network drive decommissioning post-migration. | External | Client CAB; Infrastructure team | ⚠ Not Started — to be raised after UAT sign-off | Post-UAT — Decommissioning phase |
| D-015 | UAT environment provisioning (separate Fabric workspace for pre-production testing). | Internal | D-001, D-002, D-009 | ⚠ Blocked by D-001 | Sprint 4 — UAT execution |
| D-016 | Backup and disaster recovery runbook approved by client operations team. | External | Client IT Operations; DR team | ⚠ Not Started — runbook draft in preparation | Sprint 5 — Go-live readiness review |

---

## 5. Decisions Log

The Decisions Log records all significant architectural, design, and delivery decisions made on the project. Each decision has been reviewed and approved through the agreed governance mechanism. Decisions may be revisited if the underlying assumptions or constraints change, subject to formal change control.

| **ID** | **Decision** | **Rationale** | **Decision Date** | **Decision Maker** | **Impact** |
|---|---|---|---|---|---|
| DEC-001 | **Medallion architecture (bronze-silver-gold) adopted as the target data lakehouse pattern.** | Industry-standard pattern for progressive data refinement. Provides clear separation between raw ingestion (bronze), conformed/typed data (silver), and business-ready analytics (gold). Supports data quality, lineage, and reprocessing without re-ingestion from source. Aligns with Fabric lakehouse capabilities. | 30 June 2026 | Solution Architect (approved by Programme Board) | All subsequent design, build, and testing activities follow the three-layer model. Storage costs increase due to data replication across layers, offset by query performance and data quality benefits. |
| DEC-002 | **Delta Lake (Parquet-based) format adopted for all lakehouse tables across bronze, silver, and gold layers.** | Delta Lake provides ACID transactions, schema evolution, time travel, and optimised query performance via Z-ordering. It is the native format for Fabric lakehouses and is fully open source (satisfies constraint C-003). Alternative formats (CSV, JSON) lack transactional guarantees. | 30 June 2026 | Data Engineering Lead | All tables are Delta-format. Bronze layer retains original CSV files in a landing zone but converts to Delta on ingestion. Time travel capability available for audit and rollback. |
| DEC-003 | **Direct Lake mode selected as the Power BI connection mode (not Import or DirectQuery).** | Direct Lake provides near-real-time data access without the import refresh overhead and without the query performance degradation of DirectQuery. It queries the Delta tables in the lakehouse directly, leveraging Fabric compute. This is the optimal mode for Fabric-native architectures. Requires Fabric capacity ≥ F4 (validates assumption A-001). | 02 July 2026 | Solution Architect; Power BI Lead | Semantic model is read-only against gold-layer Delta tables. No scheduled refresh required — data is current as of the last lakehouse update. F4 capacity or above is mandatory. Fallback to Import mode documented as contingency. |
| DEC-004 | **Spark SQL views created in the gold layer for all 117 KPIs.** | Centralises KPI logic in the lakehouse rather than in the Power BI semantic model. Enables KPIs to be consumed by multiple downstream channels (Power BI, Excel, other Fabric artefacts). Spark SQL is transparent, reviewable, and version-controllable. DAX is reserved for the semantic model presentation layer only. | 05 July 2026 | Data Engineering Lead | 117 Spark SQL view definitions to be developed and unit-tested. DAX measures in the semantic model are limited to presentation-level formatting and RLS-scoped aggregations. KPI logic changes are made in Spark SQL, not DAX. |
| DEC-005 | **Bronze layer stores all column data as STRING data type (type preservation).** | Preserves raw data exactly as received from source, preventing type-cast failures during ingestion. Enables replay and reprocessing if silver-layer type definitions change. Supports schema drift tolerance. Data quality issues are surfaced and resolved in the silver layer, not silently dropped in bronze. | 05 July 2026 | Data Engineering Lead | Bronze tables have uniform STRING typing. Silver layer performs explicit CAST operations per `schema_definition.csv`. Storage overhead is minimal due to Parquet/Delta compression. |
| DEC-006 | **Silver layer enforces data types strictly per `schema_definition.csv`.** | Ensures data conformance to the agreed schema before any business logic is applied. Rejects or quarantines non-conforming records. Provides a clean, typed, and reliable foundation for gold-layer KPI calculations. | 05 July 2026 | Data Engineering Lead | Records failing type enforcement are routed to a quarantine table for review. Silver-layer pipeline includes data quality checks (null checks, range validation, referential integrity). Schema changes require `schema_definition.csv` update and silver pipeline redeployment. |
| DEC-007 | **Gold layer overwrites on each refresh (idempotent refresh strategy).** | Gold-layer views are deterministic given the same silver-layer input. Overwrite (rather than append or merge) ensures idempotency — running the gold refresh twice produces the same result. Eliminates duplicate-row risk. Simplifies error recovery. | 07 July 2026 | Data Engineering Lead | Gold refresh truncates and reloads all gold tables. Refresh duration is proportional to silver-layer data volume. No incremental/delta logic required in gold layer. Rollback is achieved by re-running the refresh. |
| DEC-008 | **27 new measures added to close functional gaps, bringing the total KPI count to 117 (from 90 in V13.1).** | Functional Gap Analysis identified 17 functional gaps. Resolving these gaps required 27 new KPIs (some gaps require multiple KPIs). New KPIs are defined in the KPI Logic Document and implemented as Spark SQL views in the gold layer. | 07 July 2026 | Business Analyst; Data Engineering Lead (approved by Programme Board) | Gold layer contains 117 KPI views. Semantic model exposes all 117 KPIs. UAT must validate both the 90 existing KPIs (reconciliation against V13.1) and the 27 new KPIs (validation against KPI Logic Document). |
| DEC-009 | **A new `is_emergency` column is recommended for addition to `dim_referral` in the silver layer.** | Functional gap R18 identifies that `is_spot` is not equivalent to `is_emergency`. Currently, no attribute distinguishes emergency referrals from spot placements. A dedicated `is_emergency` flag enables accurate emergency placement KPIs. Source-system change is recommended (per constraint C-014) but in the interim, the flag is derived in silver using business rules. | 09 July 2026 | Data Engineering Lead; Business Analyst | Silver-layer ETL includes a derived `is_emergency` column based on referral attributes (e.g., referral type, urgency code, time-to-placement). Derivation rules are documented and subject to business validation. Formal change request to source system vendor is raised separately. |
| DEC-010 | **Duplicate measures in V13.1 to be consolidated in the gold layer.** | The V13.1 audit identified multiple measures with identical or near-identical logic but different names (e.g., `Placement_Count` and `Count_of_Placements`). Consolidation reduces maintenance burden and eliminates conflicting results. | 09 July 2026 | Data Engineering Lead; Power BI Lead | Gold layer contains one canonical KPI per business concept. A measure mapping document (V13.1 measure → gold KPI) is produced for traceability. Any V13.1 measure not mapped to a gold KPI is retired and documented. |
| DEC-011 | **Measure name typo "Recieved" to be corrected to "Received" in the gold layer.** | The V13.1 report contains a measure named `Referrals_Recieved` (misspelling of "Received"). Correcting this in the gold layer ensures professional presentation and avoids confusion. The legacy name is retained as an alias in the semantic model for backward compatibility during the transition period. | 10 July 2026 | Power BI Lead | Gold-layer KPI uses `referrals_received`. Semantic model measure is `Referrals Received`. Alias `Referrals_Recieved` retained temporarily. Alias removal is a post-cutover activity, subject to LA confirmation that no downstream reports reference the misspelled name. |
| DEC-012 | **Python (PySpark) used for bronze-layer ingestion; Spark SQL used for silver and gold transformations.** | PySpark provides file-system operations and error handling for CSV ingestion (file discovery, validation, metadata capture). Spark SQL is declarative and more accessible to business analysts for silver/gold logic review. Separation of concerns between ingestion (Python) and transformation (SQL). | 10 July 2026 | Data Engineering Lead | Bronze notebooks are Python (.py). Silver and gold notebooks are Spark SQL (.sql). All code is version-controlled in the project repository. Peer review required for all changes. |
| DEC-013 | **A dual-running / reconciliation period of 4 weeks is planned before V13.1 decommissioning.** | Constraint C-006 mandates no big-bang cutover. A 4-week dual-running period allows LAs to validate gold-layer outputs against V13.1 and raise discrepancies. Reconciliation is performed at KPI level for a sample of 10 KPIs per LA. | 11 July 2026 | Programme Manager (approved by Programme Board) | V13.1 and Fabric pipelines run in parallel for 4 weeks post-UAT. Reconciliation reports are produced weekly. Discrepancies > 1% trigger investigation and potential gold-layer fix. V13.1 decommissioning requires CAB approval (dependency D-014). |

---

## 6. Open Items Requiring Client Input

The following items are unresolved and require explicit client input, decision, or action before they can be closed. Each open item is cross-referenced to the relevant assumption, constraint, dependency, or decision.

| **ID** | **Open Item** | **Related Ref** | **Client Action Required** | **Target Resolution Date** | **Priority** |
|---|---|---|---|---|---|
| OI-001 | Confirm Microsoft Fabric capacity has been procured (minimum F4 SKU) and identify the Azure region for provisioning. | A-001, D-001 | Written confirmation of Fabric capacity SKU, subscription ID, and target region. If not yet procured, provide estimated procurement date. | 19 July 2026 | **CRITICAL** — blocks Sprint 1 |
| OI-002 | Provide Entra ID group structure for 14 LAs, including group names, membership criteria, and cross-boundary access patterns. | D-004, C-005 | Export of current Entra ID group structure or a proposed group taxonomy. Confirmation of which LAs use Entra ID natively vs. federated. | 26 July 2026 | **HIGH** — blocks Sprint 3 |
| OI-003 | Confirm network drive access permissions for the Fabric ingestion service principal (read access to CSV landing folders). | D-006 | Provide service account credentials or managed identity configuration. Confirm firewall/network access rules. | 19 July 2026 | **CRITICAL** — blocks Sprint 1 |
| OI-004 | Provide PostgreSQL database connection details (host, port, database name, read-only credentials) and approve firewall rule for Fabric egress IP. | D-007 | Connection string or individual parameters. Confirmation that a read-only role is available or can be created. | 26 July 2026 | **HIGH** — blocks Sprint 2 |
| OI-005 | Confirm or provide Azure Key Vault instance for secret management. If none exists, confirm whether one should be provisioned as part of this project. | D-008 | Key Vault resource name, resource group, and access policy configuration. Or approval for project team to provision. | 19 July 2026 | **HIGH** — blocks Sprint 1 |
| OI-006 | Complete DPIA review and provide DPO sign-off or list of required amendments. | D-013, C-001 | DPO feedback on draft DPIA. Sign-off or conditional approval with remediation actions. | 02 August 2026 | **CRITICAL** — blocks production data ingestion |
| OI-007 | Obtain functional specification sign-off from the remaining 5 LAs (of 14) that have not yet confirmed. | D-010 | Written confirmation from LA business leads. Escalation to Programme Board if any LA disputes scope. | 26 July 2026 | **HIGH** — blocks Sprint 2 |
| OI-008 | Validate and baseline the revised KPI Logic Document (8 KPIs with pending revisions). | D-011 | Business review of revised KPI definitions. Written confirmation that 117 KPIs are baselined. | 02 August 2026 | **HIGH** — blocks Sprint 3 |
| OI-009 | Confirm data retention policies per LA — minimum and maximum retention periods for each data category (placements, referrals, providers). | C-009 | Retention schedule per LA, or confirmation that a default policy (e.g., 7 years) applies to all. | 09 August 2026 | **MEDIUM** — required before go-live |
| OI-010 | Confirm acceptance of the derived `is_emergency` business rules for the interim period before source system change. | DEC-009, A-009 | Business review of proposed derivation logic. Sign-off that the derived flag is acceptable for reporting until source system is updated. | 02 August 2026 | **HIGH** — blocks Sprint 3 |
| OI-011 | Confirm whether Customer-Managed Keys (CMK) are required for encryption at rest, or if Platform-Managed Keys (PMK) are acceptable. | C-011 | Information governance policy reference or written confirmation. | 26 July 2026 | **MEDIUM** — impacts infrastructure configuration |
| OI-012 | Provide DR requirements: Recovery Time Objective (RTO) and Recovery Point Objective (RPO) for the analytics platform. | C-008, D-016 | Formal RTO/RPO statement from client IT operations or confirmation of proposed defaults (RTO ≤ 4h, RPO ≤ 24h). | 09 August 2026 | **MEDIUM** — required before go-live |
| OI-013 | Confirm break-glass access workflow: who authorises, time limit, and post-access review process. | C-010, R79 | Approval of proposed break-glass procedure or provision of existing organisational policy. | 09 August 2026 | **HIGH** — required before go-live |
| OI-014 | Confirm acceptance of daily refresh cadence for all KPIs, or identify any KPIs requiring intraday refresh. | A-008 | Written confirmation or exception list with required refresh frequency. | 26 July 2026 | **MEDIUM** — impacts pipeline design |

---

## 7. Change Log

The Change Log records all amendments to this HOLD Register. Changes are version-controlled and require approval by the Programme Manager or Programme Board, depending on severity.

| **Version** | **Date** | **Author** | **Change Description** | **Approved By** |
|---|---|---|---|---|
| 0.1 | 05 July 2026 | Data Engineering Lead | Initial draft — assumptions A-001 to A-009, constraints C-001 to C-010, dependencies D-001 to D-010, decisions DEC-001 to DEC-005. | — (Draft) |
| 0.2 | 09 July 2026 | Data Engineering Lead | Added assumptions A-010 to A-013. Added constraints C-011 to C-014. Added dependencies D-011 to D-016. Added decisions DEC-006 to DEC-011. Added Open Items section (OI-001 to OI-010). | Programme Manager |
| 0.9 | 11 July 2026 | Solution Architect | Added decisions DEC-012 and DEC-013. Expanded open items OI-011 to OI-014. Added Section 1.4 (Related Documents). Internal review comments incorporated. | Programme Manager |
| 1.0 | 12 July 2026 | Fabric Data Platform Delivery Team | Formalised for client review. All sections reviewed and cross-referenced. Change log retrospectively populated. Document issued to WMPP Programme Board. | Programme Manager (pending Board endorsement) |

---

### Document Control

| **Field** | **Value** |
|---|---|
| **Next Review Date** | 26 July 2026 (post-Sprint 1 completion) |
| **Review Frequency** | End of each sprint or upon material change |
| **Document Owner** | Fabric Data Platform Delivery Team — Solution Architect |
| **Approval Authority** | WMPP Programme Board |
| **Retention** | Retain for project duration + 7 years post-completion (per C-009 default) |

---

*End of Document — WMPP HOLD Register v1.0 — 12 July 2026*
