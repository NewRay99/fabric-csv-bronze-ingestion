# Client Discovery Questionnaire

**Project:** WMPP (West Midlands Placement Portal)
**Document Type:** Client Discovery Questionnaire
**Date:** 12 July 2026
**Prepared by:** [Consultant Name]
**Classification:** Commercial in Confidence

---

## 1. Purpose

This questionnaire is issued as part of the initial client engagement for the WMPP data engineering programme. Its purpose is to gather essential information about the client's Azure estate, current data architecture, reporting requirements, and security/compliance posture before the proposed solution is finalised.

The responses will be used to:

- Confirm Azure Fabric capacity and licensing readiness
- Validate the proposed bronze-silver-gold lakehouse architecture
- Identify any technical constraints or dependencies
- Inform the migration plan from network-drive-based CSV reporting to a Fabric lakehouse
- Ensure GDPR/DPA 2018 compliance for vulnerable children's data

**Please complete all questions marked as [Must-Have].** Questions marked [Nice-to-Have] can be deferred to the discovery workshop.

---

## Question Priority Legend

| Priority | Meaning |
|----------|---------|
| 🔴 Must-Have | Required before solution design can be finalised |
| 🟡 Nice-to-Have | Valuable context, can be gathered during workshop |

---

## 2. Section A — Organisation & Project Context

### A1. Participating Authorities

| Ref | Question | Priority |
|-----|----------|----------|
| A1.1 | Which of the 14 West Midlands local authorities are confirmed as participating in WMPP? Please list all. | 🔴 |
| A1.2 | Which authority is the lead / accountable body for this programme? | 🔴 |
| A1.3 | Are there any authorities in a "observer" or "pipeline" status? If so, which? | 🟡 |
| A1.4 | Is there a formal partnership agreement or MoU between the participating authorities? | 🟡 |

### A2. Governance & Stakeholders

| Ref | Question | Priority |
|-----|----------|----------|
| A2.1 | Who is the Senior Responsible Owner (SRO) for this programme? | 🔴 |
| A2.2 | Who is the project sponsor / budget holder? | 🔴 |
| A2.3 | Who is the designated product owner for the WMPP dashboard? | 🔴 |
| A2.4 | Who is the client-side technical lead / IT contact? | 🔴 |
| A2.5 | Is there a Change Advisory Board (CAB)? What is the change approval process? | 🟡 |
| A2.6 | Are there existing programme boards, steering groups, or working groups we should be aware of? | 🟡 |

### A3. Timeline & Milestones

| Ref | Question | Priority |
|-----|----------|----------|
| A3.1 | What is the target go-live date for the migrated solution? | 🔴 |
| A3.2 | Are there any hard deadlines or external commitments driving the timeline (e.g., board reports, Ofsted inspections, funding cycles)? | 🔴 |
| A3.3 | What is the acceptable duration for parallel running between the current network-drive report and the new lakehouse solution? | 🟡 |
| A3.4 | Is there a target date for decommissioning the network-drive CSV pipeline? | 🟡 |

### A4. Current Solution Context

| Ref | Question | Priority |
|-----|----------|----------|
| A4.1 | What is the current incumbent solution for placement matching? (The functional spec references a "micro-procurement style portal" — please confirm.) | 🔴 |
| A4.2 | What are the top 3 limitations or pain points with the current Power BI report (V13.1)? | 🔴 |
| A4.3 | Are there any known data quality issues with the current CSV files that we should be aware of? | 🔴 |
| A4.4 | Is the KPI Logic Document (authored by Hamant K Jakhu, 23 June 2026) the authoritative KPI specification? Are there any amendments? | 🔴 |
| A4.5 | Is the functional specification (R1–R87) the definitive requirement set? Are there any additional or superseded requirements? | 🔴 |

---

## 3. Section B — Azure Estate & Fabric Capabilities

### B1. Azure Tenant & Identity

| Ref | Question | Priority |
|-----|----------|----------|
| B1.1 | Do you have an existing Azure tenant? If yes, what is the tenant ID / Entra ID (Azure AD) tenant name? | 🔴 |
| B1.2 | Is Entra ID (Azure AD) the primary identity provider? Are there any federated or B2B guest user scenarios? | 🔴 |
| B1.3 | Are Multi-Factor Authentication (MFA) and Conditional Access policies enforced? | 🔴 |
| B1.4 | Are managed identities used for service-to-service authentication within Azure? | 🟡 |
| B1.5 | Are there any restrictions on creating new Entra ID service principals or app registrations? | 🟡 |

### B2. Azure Subscriptions

| Ref | Question | Priority |
|-----|----------|----------|
| B2.1 | How many Azure subscriptions do you currently have? | 🔴 |
| B2.2 | Which subscription will host the WMPP data engineering solution? (Please provide subscription ID or name.) | 🔴 |
| B2.3 | Who is the subscription owner / Global Admin? | 🔴 |
| B2.4 | Are there subscription-level policies (Azure Policy) that restrict resource creation? If so, which? | 🟡 |
| B2.5 | What is the budget allocation for Azure resources for this programme? | 🟡 |

### B3. Microsoft Fabric

| Ref | Question | Priority |
|-----|----------|----------|
| B3.1 | Do you currently have Microsoft Fabric capacity? If yes, what SKU? (F2, F4, F8, F16, F32, F64, F128, F256) | 🔴 |
| B3.2 | If no Fabric capacity, are you planning to procure one? What is the expected timeline? | 🔴 |
| B3.3 | What licensing model will be used? (Fabric capacity, Premium Per User, Fabric Trial) | 🔴 |
| B3.4 | Has a Fabric workspace been created for WMPP? If yes, what is the workspace name and capacity assignment? | 🟡 |
| B3.5 | Are there any existing Fabric lakehouses, data pipelines, or dataflows in the tenant? | 🟡 |
| B3.6 | Who will be the Fabric workspace administrator? | 🟡 |
| B3.7 | Do you have Fabric capacities in multiple regions? Which region is preferred for data residency? | 🟡 |

### B4. Azure Data Lake Storage Gen2

| Ref | Question | Priority |
|-----|----------|----------|
| B4.1 | Do you have existing ADLS Gen2 storage accounts? If yes, please provide account name(s) and resource group. | 🔴 |
| B4.2 | What storage tiers are configured? (Hot, Cool, Archive) | 🔴 |
| B4.3 | Is hierarchical namespace enabled on the storage account? (Required for Delta Lake / lakehouse) | 🔴 |
| B4.4 | Is the storage account accessible from the Fabric workspace? (Shortcuts, managed identity, service principal?) | 🔴 |
| B4.5 | What is the approximate data volume currently stored? What is the expected growth rate? | 🟡 |
| B4.6 | Are there lifecycle management policies configured on the storage account? | 🟡 |

### B5. Azure Databricks

| Ref | Question | Priority |
|-----|----------|----------|
| B5.1 | Do you currently use Azure Databricks? If yes, what tier (Standard / Premium)? | 🔴 |
| B5.2 | Is Unity Catalog enabled? If yes, what is the metastore configuration? | 🟡 |
| B5.3 | If no Databricks, are you planning to use Fabric Spark pools instead? (Preferred for cost efficiency.) | 🔴 |
| B5.4 | Are there any existing Databricks notebooks, jobs, or pipelines that interact with the WMPP data? | 🟡 |

### B6. Data Integration & Pipelines

| Ref | Question | Priority |
|-----|----------|----------|
| B6.1 | Do you use Azure Data Factory (ADF)? Or Fabric Data Factory / Data Pipelines? | 🔴 |
| B6.2 | Are there existing pipelines that extract data from the PostgreSQL source database to CSV? | 🔴 |
| B6.3 | What orchestrator is used for scheduled jobs? (ADF triggers, Fabric pipeline schedules, Azure Logic Apps, other?) | 🟡 |
| B6.4 | Is there a desire to replace the CSV extraction with a direct database connection or CDC (Change Data Capture) in future? | 🟡 |

### B7. Networking & Security

| Ref | Question | Priority |
|-----|----------|----------|
| B7.1 | What is the network topology? Are resources in a VNet? | 🔴 |
| B7.2 | Are Private Endpoints / Private Link used for Azure services? | 🔴 |
| B7.3 | Is ExpressRoute or VPN Gateway configured? | 🟡 |
| B7.4 | Are there Network Security Groups (NSGs) or firewall rules that would affect lakehouse or Power BI access? | 🔴 |
| B7.5 | Is there a managed jumpbox / bastion host for secure access to internal resources? | 🟡 |
| B7.6 | What are the DNS resolution requirements? Are custom DNS zones in use? | 🟡 |

### B8. Secrets & Key Management

| Ref | Question | Priority |
|-----|----------|----------|
| B8.1 | Do you have Azure Key Vault configured? If yes, please provide vault name and resource group. | 🔴 |
| B8.2 | Are connection strings, API keys, and secrets currently stored in Key Vault? | 🔴 |
| B8.3 | Who has Key Vault administrator access? | 🟡 |
| B8.4 | Is there a secrets rotation policy? | 🟡 |

---

## 4. Section C — Current Data Architecture (As-Is)

### C1. Network Drive & CSV Files

| Ref | Question | Priority |
|-----|----------|----------|
| C1.1 | Where are the CSV files currently hosted? (On-premise file server, SharePoint document library, Azure Files, other?) | 🔴 |
| C1.2 | If on-premise, what is the server name and share path? Is it accessible from Azure? | 🔴 |
| C1.3 | How frequently are the CSV files generated/updated? (Daily, weekly, ad-hoc, event-driven?) | 🔴 |
| C1.4 | Who is responsible for generating the CSV files? (Manual export, scheduled job, application-generated?) | 🔴 |
| C1.5 | What is the CSV file naming convention? Are there timestamps or versioning in the filenames? | 🟡 |
| C1.6 | How many CSV files are there? What is the total size? | 🔴 |
| C1.7 | What happens when a CSV schema changes? Is there a change notification process? | 🔴 |

### C2. Source Database

| Ref | Question | Priority |
|-----|----------|----------|
| C2.1 | The schema definition shows a PostgreSQL database. Is this the system of record? Please confirm the database engine and version. | 🔴 |
| C2.2 | Where is the PostgreSQL database hosted? (On-premise, Azure Database for PostgreSQL, AWS RDS, other?) | 🔴 |
| C2.3 | Is the database accessible from Azure? If on-premise, what is the connectivity method? (VPN, ExpressRoute, Hybrid Connection Manager?) | 🔴 |
| C2.4 | What is the database size? Number of tables? Row counts for key tables (referral, offer, ipa, provider)? | 🟡 |
| C2.5 | Are there any database views, materialised views, or stored procedures that the CSV export depends on? | 🟡 |
| C2.6 | Is there a read replica available for reporting queries? | 🟡 |

### C3. Data Lineage

| Ref | Question | Priority |
|-----|----------|----------|
| C3.1 | What is the data flow from source to report? Please confirm: PostgreSQL → CSV export → Network drive → Power BI Import? | 🔴 |
| C3.2 | Are there any intermediate transformations between the database and the CSV files? | 🔴 |
| C3.3 | Is the `schema_definition.csv` the definitive schema for all source tables? Are there any tables not captured? | 🔴 |
| C3.4 | Are there any additional data sources that feed into the report that are not in the schema definition? | 🟡 |

---

## 5. Section D — Power BI Report & Reporting Requirements

### D1. Current Report Usage

| Ref | Question | Priority |
|-----|----------|----------|
| D1.1 | Who currently uses the WMPP dashboard? (Placement officers, QA officers, commissioners, finance officers, senior leadership?) | 🔴 |
| D1.2 | How many concurrent users are there? What is the peak usage pattern? | 🔴 |
| D1.3 | Are there any performance complaints? (Slow load times, refresh failures?) | 🔴 |
| D1.4 | Is the report published to a Power BI workspace? Which workspace? What capacity (Premium, Embedded, Fabric)? | 🔴 |
| D1.5 | Is the report in Import mode or DirectQuery? What is the refresh schedule? | 🔴 |
| D1.6 | Who authored the original dashboard? Is there a handover document or knowledge transfer session available? | 🟡 |

### D2. Row-Level Security (RLS)

| Ref | Question | Priority |
|-----|----------|----------|
| D2.1 | Is Row-Level Security (RLS) currently configured in the Power BI report? | 🔴 |
| D2.2 | If yes, what are the security roles? (e.g., per-local-authority, per-stakeholder-role?) | 🔴 |
| D2.3 | Requirement R55 states commissioners must access regional data and market-wide trends. Is this currently implemented? | 🔴 |
| D2.4 | Are there any dynamic RLS requirements based on user attributes (e.g., Entra ID group membership)? | 🟡 |
| D2.5 | How are users provisioned and de-provisioned for report access? | 🟡 |

### D3. Reporting Expectations

| Ref | Question | Priority |
|-----|----------|----------|
| D3.1 | Is the current 5-page dashboard structure sufficient, or are there additional pages/visuals required? | 🟡 |
| D3.2 | Is there a requirement for paginated reports (RDL) for formal export/print? | 🟡 |
| D3.3 | Are there any mobile reporting requirements? (Dashboard viewing on tablets/phones?) | 🟡 |
| D3.4 | Is self-service reporting a requirement? Should business users be able to create their own reports from the gold layer? | 🟡 |
| D3.5 | What is the expected refresh cadence for the new solution? (Daily, hourly, near-real-time?) | 🔴 |

---

## 6. Section E — Security & Compliance

### E1. Data Protection

| Ref | Question | Priority |
|-----|----------|----------|
| E1.1 | Has a Data Protection Impact Assessment (DPIA) been completed for the WMPP programme? If yes, please share. | 🔴 |
| E1.2 | What is the data classification for the placement data? (Official-Sensitive, OFFICIAL, other?) | 🔴 |
| E1.3 | Are there any restrictions on data residency? Must all data be stored within the UK? | 🔴 |
| E1.4 | Is encryption at rest required? (Default in Azure — please confirm acceptance.) | 🔴 |
| E1.5 | Is encryption in transit required? (Default in Azure — please confirm acceptance.) | 🔴 |
| E1.6 | Are there any specific key management requirements? (Customer-managed keys in Key Vault, Bring Your Own Key?) | 🟡 |

### E2. Data Sharing & Governance

| Ref | Question | Priority |
|-----|----------|----------|
| E2.1 | Are there formal data sharing agreements between the 14 participating local authorities? | 🔴 |
| E2.2 | Are there any restrictions on cross-authority data visibility? (e.g., Authority A cannot see Authority B's referrals?) | 🔴 |
| E2.3 | Is there an Information Governance Officer or DPO who should be consulted? | 🟡 |
| E2.4 | Are there audit requirements for data access? (Who accessed what data, when?) | 🔴 |
| E2.5 | What are the data retention requirements for placement records? How long must data be retained? | 🔴 |
| E2.6 | Is there a data deletion / right-to-erasure process that needs to be supported? | 🟡 |

### E3. Access Control

| Ref | Question | Priority |
|-----|----------|----------|
| E3.1 | Is break-glass access required? (R79 — controlled, auditable, emergency access.) | 🔴 |
| E3.2 | Are there privileged access management (PAM) requirements? (Just-in-time access, approval workflows?) | 🟡 |
| E3.3 | Are there any compliance frameworks that must be adhered to beyond GDPR/DPA 2018? (e.g., ISO 27001, Cyber Essentials Plus, NHS DSPT?) | 🟡 |

---

## 7. Section F — Future State & Expectations

### F1. Architecture Preferences

| Ref | Question | Priority |
|-----|----------|----------|
| F1.1 | Is the medallion architecture (Bronze-Silver-Gold) acceptable as the target data pattern? | 🔴 |
| F1.2 | Is Delta Lake format acceptable for all lakehouse tables? | 🔴 |
| F1.3 | Is Power BI Direct Lake mode acceptable as the connection method? (This provides near-real-time data without Import refresh scheduling.) | 🔴 |
| F1.4 | Are there any preferences for Spark vs SQL for data transformations? | 🟡 |
| F1.5 | Is there a preference for notebook-based development vs pipeline-based orchestration? | 🟡 |

### F2. Scalability & Future Needs

| Ref | Question | Priority |
|-----|----------|----------|
| F2.1 | Are there plans to onboard additional local authorities beyond the current 14? If so, which and when? | 🟡 |
| F2.2 | Are there plans to integrate additional data sources in future? (e.g., OFSTED data, finance systems, HR systems?) | 🟡 |
| F2.3 | Is there a requirement for API access to the gold layer for downstream applications? | 🟡 |
| F2.4 | Are there real-time or near-real-time reporting requirements beyond the daily batch refresh? | 🟡 |
| F2.5 | Is there a requirement for data science / ML workloads on the lakehouse data in future? | 🟡 |

### F3. Operational Readiness

| Ref | Question | Priority |
|-----|----------|----------|
| F3.1 | Who will own the operational support for the Fabric lakehouse after go-live? | 🔴 |
| F3.2 | Is there an existing support team familiar with Fabric / Spark / Delta Lake? | 🔴 |
| F3.3 | What are the support hours? Is there an on-call requirement? | 🟡 |
| F3.4 | Is there a monitoring and alerting solution in place? (Azure Monitor, Log Analytics, Fabric monitoring hub?) | 🟡 |
| F3.5 | What is the disaster recovery expectation? (RTO / RPO targets?) | 🔴 |

---

## 8. Response Instructions

Please provide responses in the table format below. Where a question requires a document attachment (e.g., DPIA, data sharing agreement), please reference the document and share separately.

### Response Template

| Ref | Question (summary) | Response | Notes / Attachments |
|-----|--------------------|----------|---------------------|
| A1.1 | Participating authorities | [Enter response] | |
| B3.1 | Fabric capacity SKU | [Enter response] | |
| ... | ... | ... | ... |

---

## 9. Next Steps

1. **Client completes this questionnaire** and returns within [5 business days].
2. **Discovery workshop** scheduled to review responses and discuss open items.
3. **Azure estate assessment** — consultant reviews the client's Azure environment with the client technical lead.
4. **Solution finalisation** — the Proposed Solution & Architecture document is updated based on responses.
5. **Statement of Work** issued for formal approval.

---

## 10. Document Control

| Field | Value |
|-------|-------|
| Document Title | Client Discovery Questionnaire |
| Project | WMPP (West Midlands Placement Portal) |
| Version | 1.0 |
| Date | 12 July 2026 |
| Author | [Consultant Name] |
| Reviewer | [TBD] |
| Approver | [TBD] |
| Classification | Commercial in Confidence |
| Distribution | Client SRO, Client Technical Lead, Consultant Team |

---

*This questionnaire should be read in conjunction with the following documents:*
- *02_As_Is_Assessment_Report.md* — Current state analysis
- *03_Gap_Analysis_Report.md* — Identified functional and architectural gaps
- *04_Proposed_Solution_Architecture.md* — Proposed future state
- *05_HOLD_Register.md* — Assumptions, constraints, dependencies, decisions
- *06_Statement_of_Work.md* — Formal engagement terms
