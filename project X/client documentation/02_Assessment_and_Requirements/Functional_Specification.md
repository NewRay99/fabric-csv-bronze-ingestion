# AM Functional Specification

## Overview

This document defines the functional and non-functional requirements for a regional child placement and provider matching platform across the West Midlands. The solution will enable local authorities, children's trusts, providers, QA officers, commissioners, finance officers, and other stakeholders to manage placements, provider onboarding, quality assurance, reporting, and contractual workflows through a single regional platform.

---

# 1. High-Level Purpose

## R1
**Requirement:**  
Provide local authorities and children's trusts with the ability to place children with complex care needs with providers across the region who can meet those needs.

**Notes:**
- Must support multiple organisations across the West Midlands region.
- Must operate across different IT estates, systems, and applications.

## R2
**Requirement:**  
Consider the current incumbent solution and associated processes when designing the future-state architecture.

**Notes:**
- Current solution uses a micro-procurement style portal.
- Matching is based on children's needs and provider capabilities.

---

# 2. General Requirements

## R3
The solution must operate as a single regional platform enabling cross-boundary placements.

## R4
All software developed must be suitable for release as open source, including:
- Libraries
- Licences
- Artifacts (except security-restricted items)
- Contribution guidance

## R5
The solution must:
- Use Agile delivery methodologies
- Deliver an MVP (Minimum Viable Product)
- Maintain a product backlog for future enhancements

## R6
Commercially available components should be preferred over bespoke development where practical.

---

# 3. API Requirements

## R7
The solution must utilise APIs to operate seamlessly across the West Midlands IT ecosystem.

## R8
All APIs developed must comply with open-source release requirements.

## R9
The solution must support form pre-population where possible, including:
- Referral forms from social workers
- OFSTED data
- Other authoritative sources

Benefits:
- Reduced dual keying
- Improved efficiency
- Increased data quality

---

# 4. Placement Officer Requirements

## Placement Management

### R11
Placement officers must be able to publish child placement requirements to providers through the platform.

### R12
All vulnerable-child data shared with providers must comply with:
- GDPR
- Data Protection Act 2018

### R13
Placement officers must be able to:
- Apply multiple filters
- Use nested filters
- Filter by:
  - Specialisms
  - Placement type
  - Placement status

Example statuses:
- Offer with social worker
- Closed
- Cancelled
- Placed

### R14
The solution should provide in-system messaging between placement officers and providers.

Messaging should:
- Be auditable
- Support prioritised message types
- Highlight urgent responses

Examples:
- Further information required
- Change of offer

### R15
Placement officers must be able to gather:
- Digital information
- Digital signatures

For completion of the Individual Placement Agreement (IPA).

### R16
Priority information must be clearly flagged within placement requests.

### R17
When a placement is accepted, all necessary placement information must be immediately available.

### R18
Emergency placements must support:
- Same-day placement
- Distinct identification
- Separate reporting and finance categorisation

### R19
Placement officers must be able to update referrals.

Updates must automatically notify providers.

### R20
Full audit tracking is required across:
- Placement activities
- IPA completion
- Signatures
- Approvals
- Negotiations

### R21
The system should provide:
- Automated notifications to unsuccessful providers
- Optional customised rejection feedback

### R22
Placement officers must be able to make placements outside the West Midlands region.

Requirements:
- External placements tagged appropriately
- Finance officers informed

### R24
A dashboard should provide:
- Referral status overview
- Provider updates
- Centralised task management
- Quick referral updates

---

# 5. Provider Requirements

## Placement Requests

### R25
Providers must be able to quickly review detailed placement requests.

### R26
Providers should be able to prioritise requests based on:
- Match suitability
- Home statement of purpose
- Existing placements

### R27
Providers must be able to:
- Request additional information
- Raise queries
- See responses and updates clearly

### R28
Providers must be able to:
- Accept placements
- Reject placements
- Request further information

### R29
The offer process should be highly streamlined and efficient.

### R31
Resolved requests should be automatically removed or hidden from general provider views.

### R32
Matching capabilities should target:
- Relevant providers only
- Based on statement of purpose
- Based on care specialisms

### R33
Providers must be able to:
- Upload supporting documents
- Manage placement documentation efficiently

### R34
Emergency referrals should be:
- Easily identifiable
- Prioritised within provider workflows

### R35
The solution must provide a digitised IPA.

Benefits:
- Reduced paper processes
- Electronic approvals
- Electronic signatures
- Full auditing

### R36
Providers should have a dedicated view showing:
- Referrals with outstanding offers
- Open offers

---

# 6. QA Officer Requirements

### R38
QA officers must record assessment outcomes against provider records.

### R39
QA officers must:
- Conduct desk-based research
- Identify missing documentation

### R41
QA officers must be able to apply advisory notices and flags against providers.

Examples:
- Information notices
- Safeguarding concerns

### R45
SPOT providers must be able to upload registration documentation.

### R46
QA intelligence for non-framework providers should be shared appropriately between organisations.

### R47
The system must:
- Monitor documentation expiry
- Send reminders
- Highlight missing documentation

### R48
Providers with incomplete documentation should be excluded from receiving referrals.

### R49
QA officers must easily identify provider due diligence status.

---

# 7. Commissioner Requirements

### R51
The platform must provide a robust data model supporting:
- Placement records
- Market intelligence
- Value analysis

### R52
Commissioners must have access to:
- Accurate reporting
- Customisable reporting

### R53
Data should:
- Be consistent
- Be exportable
- Support bespoke analysis

### R54
The solution should capture reasons for declined placements.

### R55
Role-Based Access Controls (RBAC) must allow commissioners to:
- Access regional data
- Analyse market-wide trends

### R57
Emergency and planned placements must be separately reportable.

### R58
Commissioners should be alerted when framework changes occur during referral activity.

### R59
Bulk provider onboarding must be supported.

---

# 8. Finance Officer Requirements

### R62
Finance officers must be able to:
- View completed placements
- Access current IPAs
- Extract payment-related information

---

# 9. General Functional Requirements

### R67
The solution must support adding new frameworks.

### R68
Frameworks must be configurable to:
- Display
- Hide
- Isolate by region

### R69
The platform must include a robust analytical data model.

### R70
Auto-save functionality must be available:
- Across workflows
- At field level where appropriate

---

# 10. Digitised Documents

## R71 - Digitised IPA

The IPA workflow must:
- Support review
- Support approvals
- Support signing
- Provide full audit tracking

## R72 - Other Digitised Documents

The platform should digitise paper-based processes where possible.

Requirements:
- Workflow driven
- Auditable
- Trackable
- Lifecycle visibility

---

# 11. Non-Functional Requirements

## Design Principles

### R73
Architecture must support future enhancements and Agile delivery.

### R74
Commercial off-the-shelf components should be preferred.

### R75
The solution must provide:
- High availability
- Scalability
- Fault tolerance
- Disaster recovery

---

## Data Security

### R76
Access must be restricted to authorised users only.

---

## System Administration

### R77
Administration functions must support:
- User management
- Organisation onboarding
- Operational ownership transfer

---

## Access Control

### R78
RBAC and full auditing are mandatory.

### R79
Break-glass access must:
- Be controlled
- Be auditable
- Be available for emergencies

---

## Document Management

### R80
The solution must provide:
- Fast document upload
- Fast document retrieval
- RBAC-protected document access

---

## Accessibility

### R81
The platform must comply with:
- WCAG 2.0
- WCAG 2.1
- Consider WCAG 2.2
- Government accessibility requirements

---

## Performance

### R82
The solution must provide:
- Fast response times
- Scalability
- Performance reporting

---

## Data Migration

### R83
The solution must support migration of:
- Placements
- Purchases
- Provider information
- OFSTED data
- Frameworks
- Active placements

Including:
- Cleansing
- Validation
- Rationalisation

---

## Data Integrity & Retention

### R84
The solution must provide:
- Data integrity controls
- Retention management
- Export capability
- Configurable retention policies

---

## Deployment & Training

### R85
Deployment materials must include:
- FAQs
- User guides
- Demonstrations
- User support materials

---

## Flexibility

### R86
The solution must be:

- Device agnostic
- Browser compatible
- Mobile friendly
- Remote-working capable

Supported devices include:
- Desktop PCs
- Laptops
- Tablets
- Android devices
- Apple devices

---

## Maintainability

### R87
The solution must provide:
- Incident management processes
- Issue reporting
- Service-level agreements

---

## Modularity

### R88
The architecture must support:
- Modular growth
- Controlled change management
- Product roadmaps

---

## Verifiability

### R89
Delivery must include:
- Stakeholder demonstrations
- User acceptance testing
- Formal sign-off processes

---

## Hosting & Deployment

### R90
Stakeholders must be informed of:
- Hosting options
- Deployment models
- Cloud strategy
- SaaS / PaaS / IaaS decisions

---

# 12. Additional Functional Requirements

## Provider Registration

### R91
Providers must be able to:
- Submit company details
- Submit services
- Submit homes
- Upload mandatory documentation

Purpose:
- Apply for portal registration

### R92
Local Authorities must:
- Review provider applications
- Approve or reject registrations

### R93
Placement officers must access:
- Provider directory
- Service details
- Home details
- Uploaded documents

---

## QA Management

### R94
QA officers must:
- Search providers
- Apply provider flags
- Remove provider flags

Notes:
- Historical intelligence not stored
- Flags hidden from providers

---

## Framework Updates

### R95
The solution must reflect Fostering Framework changes implemented in Q3 2024.

### R96
The solution must reflect Residential Framework 2.0 changes implemented in Spring 2025.

Notes:
- Category count increases from 5 to 6.
- No change to process flow.
