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
