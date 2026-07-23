# Client Documentation — WMPP Data Engineering Engagement

**Project:** WMPP (West Midlands Placement Portal)
**Prepared:** 12 July 2026
**Classification:** Commercial in Confidence

---

## Document Index

This folder contains the formal client documentation pack for the WMPP data engineering engagement. The documents are numbered in the recommended reading order for the client.

| # | Document | Description | Audience |
|---|----------|-------------|----------|
| 00 | **README** (this file) | Document index and reading guide | All |
| 01 | **Client Discovery Questionnaire** | Structured questions for first contact — Azure estate, current architecture, security, compliance, future state | Client SRO, Technical Lead |
| 02 | **As-Is Assessment Report** | Current state analysis of the v01 PBI report, 95 measures, network-drive architecture, coverage gaps | Client SRO, Project Sponsor, Technical Lead |
| 03 | **Gap Analysis Report** | As-is vs to-be gap analysis — functional gaps, architecture gaps, data quality issues, sprint plan | Client SRO, Product Owner, Technical Lead |
| 04 | **Proposed Solution & Architecture** | Bronze-silver-gold Fabric lakehouse architecture, data pipeline design, proposed KPI expansion, security, migration strategy | Client Technical Lead, Architecture Review |
| 05 | **HOLD Register** | Assumptions, Constraints, Dependencies, Decisions, Open Items | Client SRO, Technical Lead, Consultant Team |
| 06 | **Statement of Work** | Formal engagement document — scope, deliverables, timeline, roles, acceptance criteria, commercial terms | Client SRO, Procurement, Legal |
| 07 | **Semantic-Model Changelog — v00 to v01** | Archive-backed measure and relationship delta, Statement of Work count reconciliation, and required regression tests | Client SRO, Product Owner, Technical Lead, Power BI Developer |

---

## Recommended Reading Order

**For the client SRO / sponsor:**
1. Read `02_As_Is_Assessment_Report.md` for the current state summary
2. Read `03_Gap_Analysis_Report.md` for what's missing and why it matters
3. Read `06_Statement_of_Work.md` for the commercial engagement terms
4. Read `07_Semantic_Model_Changelog_v00_to_v01.md` before approving the measure-count baseline

**For the client technical lead:**
1. Read `01_Client_Discovery_Questionnaire.md` and complete the responses
2. Read `04_Proposed_Solution_Architecture.md` for the technical proposal
3. Read `05_HOLD_Register.md` and confirm/reject each assumption and decision
4. Read `07_Semantic_Model_Changelog_v00_to_v01.md` for the verified v00-to-v01 model delta and test implications

**For the product owner / stakeholders:**
1. Read `02_As_Is_Assessment_Report.md` for the current dashboard inventory
2. Read `03_Gap_Analysis_Report.md` for the functional gaps in the current report
3. Read `04_Proposed_Solution_Architecture.md` Section 5 (Gold Layer Analytical Model) for the proposed 117 KPIs

---

## Key Numbers at a Glance

| Metric | Value |
|--------|-------|
| Current v01 PBI measures | 95 |
| Current v01 model tables | 79 |
| Current v01 model columns | 850 |
| Current v01 relationships | 48 |
| v00 → v01 measure delta | +5 (90 retained; 0 removed) |
| v00 → v01 relationship delta | -6 (54 → 48) |
| Functional requirements (R1–R87) | 87 |
| Measures marked implemented | 85 (legacy row classification — revalidate outputs against v01) |
| Functional gaps identified | 17 (legacy assessment — revalidate against v01) |
| Exact-DAX duplicate groups | 5 (11 measures; 6 redundant definitions in the legacy set) |
| Proposed total KPIs (after enhancement) | 117 (planning target) |
| QA Officer coverage (current) | 25% — lowest |
| Finance Officer coverage (current) | 0% — missing entirely |
| Current data source | Network drive CSV files |
| Proposed data source | Fabric lakehouse (Delta tables) |
| Proposed architecture | Bronze-Silver-Gold (medallion) |
| Proposed PBI connection | Direct Lake mode |
| Estimated delivery timeline | 12 weeks (3 phases) |

For the exact v01 measure inventory and `Closed_Date` logic, see [`../brand pack/WMPP_Semantic_Model_Measures.md`](../brand%20pack/WMPP_Semantic_Model_Measures.md). For the archive-backed v00-to-v01 delta and its Statement of Work implications, see [`07_Semantic_Model_Changelog_v00_to_v01.md`](07_Semantic_Model_Changelog_v00_to_v01.md).

---

## Document Control

| Field | Value |
|-------|-------|
| Pack Version | 1.1 |
| Date Issued | 23 July 2026 |
| Prepared by | [Consultant Name] |
| Review Status | Draft for Client Review |
| Next Review Date | [TBD — after discovery workshop] |

---

*All documents in this folder are Commercial in Confidence and should not be distributed outside the authorised stakeholder group without written approval.*
