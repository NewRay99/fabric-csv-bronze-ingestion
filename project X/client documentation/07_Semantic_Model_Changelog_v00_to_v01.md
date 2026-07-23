# Semantic-Model Changelog — report v00 to v01

## WMPP Power BI Baseline Reconciliation

| Field | Value |
|---|---|
| **Document Reference** | WMPP-DE-CHG-001 |
| **Version** | 1.0 |
| **Date** | 23 July 2026 |
| **Prepared For** | West Midlands Placement Portal (WMPP) Programme |
| **Status** | Draft for Client Validation |
| **Classification** | Commercial in Confidence |

---

## 1. Purpose and Decision Summary

This document records the verified semantic-model changes between the archived `report v00.zip` and `report v01.zip` Power BI projects. It reconciles those changes with the draft [Statement of Work](06_Statement_of_Work.md) and the legacy [Measures Comparison Checklist](../measures_comparison_checklist.md).

The archive comparison establishes that:

- v00 declares **90 measures**, all as `EXTERNALMEASURE(...)` references to the remote model `DirectQuery to AS - NEW WMPP PILOT DASHBOARD (V13)`.
- v01 retains all **90 measure names**, replaces the external references with local DAX definitions, and adds **5 measures**, giving **95 measures** in total.
- No measure is removed or renamed between the two archives.
- Relationships reduce from **54 to 48**: six date-table relationships are removed; three existing one-to-one relationships are recreated with reversed endpoints; nineteen date relationships change to `datePartOnly`; two relationships become bidirectional; and one export-date relationship becomes inactive.
- The Statement of Work still uses a commercial baseline of **90 migrated + 27 new = 117 KPIs**. If v01 is the accepted migration baseline and the 27 gap measures remain additional, the arithmetic becomes **95 + 27 = 122 KPIs**. This is a scope decision, not an editorial correction, and must be resolved through the Statement of Work change-control process before contractual counts are amended.

**Recommended control position:** preserve all 95 v01 measures as the technical parity baseline, keep the 27 gap measures separate unless the client explicitly confirms an overlap, and raise a formal count-baseline decision under Statement of Work Section 10.

---

## 2. Authoritative Sources and Method

### 2.1 Source controls

| Version | Source archive | Semantic-model path inside archive | SHA-256 | Archive members | Table TMDL files |
|---|---|---|---|---:|---:|
| v00 | `project X/report v00.zip` | `Report/WMPP PILOT DASHBOARD (V13.1).SemanticModel/definition/` | `fb0089ac6d16561e34e1140fe830fa93e3a978e91fc6ad1197b068e9dff157b8` | 381 | 50 |
| v01 | `project X/report v01.zip` | `semantic_model __/SM_WMPP.SemanticModel/definition/` | `db3d5df1151e03cf4e07fa682d28b0af3cc194e158630443c3c9568c93dff4be` | 546 | 79 |

Both archived models use compatibility level 1600. The comparison was performed directly against the ZIP members, not against the mutable extracted working tree. Later repository enhancements, including the separately documented `Closed_Date` calculated columns, are therefore outside this v00-to-v01 delta.

### 2.2 Comparison method

1. Parsed every `measure` declaration across `definition/tables/*.tmdl` in both archives.
2. Matched measures by exact name and compared their source expressions and metadata.
3. Parsed every declaration in `definition/relationships.tmdl`.
4. Matched relationships first by directed `fromColumn`/`toColumn` endpoints and then by undirected endpoint pair to identify direction reversals.
5. Normalised omitted TMDL defaults when comparing relationship semantics:
   - `isActive: true`
   - `crossFilteringBehavior: oneDirection`
   - `fromCardinality: many`
   - `toCardinality: one`
   - `joinOnDateBehavior: dateAndTime`

### 2.3 Interpretation constraint

The v00 archive does not contain the remote measures' executable DAX; it contains 90 `EXTERNALMEASURE(...)` declarations. The comparison proves name retention and the transition to local v01 DAX, but it cannot prove that each v01 expression is logically identical to the remote v00 measure. Statement of Work reconciliation criteria must therefore be verified using report outputs and representative filter contexts, not source-text equality alone.

---

## 3. Measure Changelog

### 3.1 Inventory summary

| Metric | v00 | v01 | Delta |
|---|---:|---:|---:|
| Measure declarations | 90 | 95 | +5 |
| Unique measure names | 90 | 95 | +5 |
| Names retained from v00 | 90 | 90 | 0 lost |
| Local DAX definitions | 0 | 95 | +95 |
| `EXTERNALMEASURE(...)` references | 90 | 0 | -90 |
| Removed measures | — | 0 | 0 |
| Renamed measures | — | 0 | 0 |

All 90 v00 names are present in v01. Each moves from a thin external-measure declaration to a local DAX definition. This is a materialisation/change-of-ownership change; it is not, by itself, evidence that all 90 business calculations changed.

### 3.2 Measures added in v01

All five additions are stored in `_Measures.tmdl` under the `Referral Offers` display folder.

| Added measure | Archived v01 DAX | Provisional requirements alignment | Validation status |
|---|---|---|---|
| `Open Referral` | `CALCULATE(DISTINCTCOUNT(dim_referral[referral_id]), dim_referral[referral_status] IN {"OPEN", "UNDER_OFFER"})` | R24 — referral-status overview | Technically verified; business mapping to confirm |
| `Open Referral Previous Month` | `CALCULATE([Open Referral], DATEADD(dim_date[Date], -1, MONTH))` | R24 and R52 — status and period comparison | Technically verified; business mapping to confirm |
| `Open Referrals MoM %` | `DIVIDE([Open Referral] - [Open Referral Previous Month], [Open Referral Previous Month])` | R24 and R52 — month-on-month status trend | Technically verified; business mapping to confirm |
| `Closed Referral Previous Month` | `CALCULATE([Closed Referrals (by Reason)], DATEADD(dim_date[Date], -1, MONTH))` | Extends the existing R24/R54 closure measure with period comparison | Technically verified; does not by itself close the R54 decline-reason gap |
| `Closed Referrals MoM %` | `DIVIDE([Closed Referrals (by Reason)] - [Closed Referral Previous Month], [Closed Referral Previous Month])` | R24, R52 and the existing R54 closure analysis | Technically verified; does not by itself close the R54 decline-reason gap |

The requirements links above are a traceability proposal based on the existing checklist. They are not stakeholder acceptance or proof that a functional gap is closed.

### 3.3 Effect on the Measures Comparison Checklist

The checklist header correctly identifies v01 as a **95-measure** model, while Sections 1–9 map the **90 retained legacy names** and the original summary statistics are based on those 90 rows. The five measures above are not classified in that legacy row set.

For controlled use of the checklist:

- treat the checklist's **85 implemented, 2 partial and 3 extra** row classifications as a **legacy 90-measure assessment**;
- treat its duplicate analysis separately from those row classifications: exact-DAX comparison identifies **5 duplicate groups containing 11 measures**, or **6 redundant definitions**;
- treat the five v01 additions as **unclassified pending stakeholder validation**;
- use **95** as the current archived v01 measure count;
- do not reduce the checklist's 17 declared gaps solely because these five status-trend measures exist; and
- retain the R54 gap until referral-level decline reasons are demonstrably covered, because the two closed-referral trend measures depend on the existing `Closed Referrals (by Reason)` logic.

---

## 4. Relationship Changelog

### 4.1 Inventory summary

| Metric | v00 | v01 | Delta |
|---|---:|---:|---:|
| Total relationships | 54 | 48 | -6 |
| Active relationships | 50 | 43 | -7 |
| Inactive relationships | 4 | 5 | +1 |
| Bidirectional relationships | 5 | 7 | +2 |
| `datePartOnly` relationships | 0 | 19 | +19 |

After normalising the three endpoint reversals, v01 introduces no relationship between a wholly new pair of columns. The net reduction of six comes from the six removed auto-date relationships below.

### 4.2 Relationships removed

| From column | To column | v00 state | v01 state |
|---|---|---|---|
| `dim_provider.created_timestamp` | `LocalDateTable_028b54cc-b5ca-4596-92c3-03b7a602d970.Date` | Active, many-to-one | Removed |
| `dim_provider.last_regulating_body_inspection_date` | `LocalDateTable_da8a63b0-82df-48d8-a6fc-361a373f5eb1.Date` | Active, many-to-one | Removed |
| `rpt_provider_fostering.created_timestamp` | `LocalDateTable_35189341-4f41-416e-a7f2-179b0d5d0332.Date` | Active, many-to-one | Removed |
| `rpt_provider_fostering.last_regulating_body_inspection_date` | `LocalDateTable_ea69a351-efb4-4da7-9953-b0cb7b411e7e.Date` | Active, many-to-one | Removed |
| `rpt_provider_registry.'stg_provider.last_regulating_body_inspection_date'` | `LocalDateTable_e1ed68d9-90c8-434e-b7a1-065734bdd0f4.Date` | Active, many-to-one | Removed |
| `rpt_provider_registry.created_timestamp` | `LocalDateTable_0dfd875d-78fe-44d7-be28-3cc950a23cd7.Date` | Active, many-to-one | Removed |

### 4.3 Endpoint direction reversals

These remain active, one-to-one, and bidirectional in both archives. The logical column pair is retained, but the relationship object is recreated with opposite `fromColumn` and `toColumn` endpoints.

| v00 direction | v01 direction |
|---|---|
| `dim_referral.referral_id` → `dim_referral_gender.referral_id` | `dim_referral_gender.referral_id` → `dim_referral.referral_id` |
| `dim_referral.referral_id` → `tmp_referral_person_gender.referral_id` | `tmp_referral_person_gender.referral_id` → `dim_referral.referral_id` |
| `dim_provider_home.provider_home_id` → `rpt_provider_registry.provider_home_id` | `rpt_provider_registry.provider_home_id` → `dim_provider_home.provider_home_id` |

### 4.4 Date-join behaviour changed to `datePartOnly`

The following 19 retained relationships change from the omitted/default `dateAndTime` behaviour in v00 to explicit `datePartOnly` behaviour in v01.

| # | From column | To column |
|---:|---|---|
| 1 | `dim_category.framework_start_date` | `LocalDateTable_1d1f28af-4ee0-445d-932d-406e35e3ffc7.Date` |
| 2 | `dim_date.Date` | `LocalDateTable_bbbcde47-d5df-4426-b044-338ecb6b7c37.Date` |
| 3 | `dim_framework.start_date` | `LocalDateTable_3c610ead-1ead-40e8-a8cd-e61d9fa02e4d.Date` |
| 4 | `dim_person.export_date` | `LocalDateTable_06406ba6-a64f-4dbb-8f63-615e13ea27b3.Date` |
| 5 | `dim_provider.export_date` | `LocalDateTable_890337fe-8ea3-4060-a30b-2e84e230ab08.Date` |
| 6 | `dim_provider_framework.export_date` | `LocalDateTable_efcb9c79-f5af-4d12-b2d3-95377a4b1c64.Date` |
| 7 | `dim_provider_home.export_date` | `LocalDateTable_6d4ae097-14d6-4557-bdd5-62ecae22c3c2.Date` |
| 8 | `dim_provider_home.last_regulating_body_inspection_date` | `LocalDateTable_8f2a60c8-3c88-4eff-b199-beb431e63809.Date` |
| 9 | `dim_referral.'Export Date Clean'` | `LocalDateTable_45fe65dd-0b5c-4a92-892b-18a0d47ecc18.Date` |
| 10 | `dim_referral.'Response Required Date Clean'` | `LocalDateTable_8891e268-a5d2-4afb-b123-d5e7559b73b0.Date` |
| 11 | `dim_referral_provider_message.export_date` | `LocalDateTable_7a31c86c-072f-40cb-ba1c-e823599ebaec.Date` |
| 12 | `fact_ipa.export_date` | `LocalDateTable_5fb970bc-aa2a-4b57-9991-fc2ef569d2b3.Date` |
| 13 | `fact_offer.estimated_start_date` | `LocalDateTable_a7d1d006-5922-4cf6-9273-75b1c3c15f5b.Date` |
| 14 | `fact_offer.export_date` | `LocalDateTable_62f66eb0-ba0f-4926-a158-67ca75f4cea5.Date` |
| 15 | `fact_provider_message.export_date` | `LocalDateTable_cb1f7675-6be0-4d04-b7a5-22ae1fed1cb5.Date` |
| 16 | `fact_referral_category.export_date` | `LocalDateTable_85241257-bd71-4f71-b4ab-c05eb501e49e.Date` |
| 17 | `fact_referral_person.export_date` | `LocalDateTable_9aee7af0-8a2a-46fe-8cbd-b666a98670f9.Date` |
| 18 | `rpt_provider_fostering.export_date` | `LocalDateTable_09a85944-f641-4f4a-a66d-cf7464a2c1a1.Date` |
| 19 | `rpt_provider_registry.last_regulating_body_inspection_date` | `LocalDateTable_3f4b0f03-f3b5-48c7-ae80-c033233778a8.Date` |

### 4.5 Filter-direction and activation changes

| Relationship | v00 | v01 | Test implication |
|---|---|---|---|
| `fact_offer.offer_date_only` → `dim_date.Date` | Active, single-direction | Active, bidirectional | Check date filters, offer status totals, and ambiguity with other referral/date paths |
| `fact_offer.referral_id` → `dim_referral.referral_id` | Active, single-direction | Active, bidirectional | Check referral/offer propagation and double-filtering across `fact_referral_offer` |
| `fact_referral_offer.export_date` → `dim_date.Date` | Active | Inactive | Measures that require export-date context must activate the relationship explicitly or use another date path |

### 4.6 Required relationship regression tests

1. Reconcile all 95 v01 measures in default, date-filtered, provider-filtered, and referral-filtered contexts.
2. Test month and day filters against the 19 `datePartOnly` relationships using timestamps with non-midnight values.
3. Validate offer and referral totals with each of the two newly bidirectional paths enabled in combination with existing fact relationships.
4. Confirm measures that use `USERELATIONSHIP` still activate the intended inactive date path.
5. Validate report visuals that previously used the six removed auto-date hierarchies.
6. Check one-to-one gender and provider-registry filters after the three endpoint reversals, even though their bidirectional semantics are retained.

---

## 5. Statement of Work Alignment

### 5.1 Affected clauses

| Statement of Work reference | Current draft baseline | Archive evidence | Required disposition |
|---|---|---|---|
| §1.1 background; §1.2 Objective 3; §2.1.4; Phase 2 objective and activities; D2.2; Assumption 6.1(4); P5; AC1; Phase 2 timeline | 90 current/migrated measures | v01 contains 95; all 90 v00 names are retained and 5 are added | Confirm the accepted current-state baseline and amend through change control if v01 governs delivery |
| §1.3 expected outcomes; Phase 2 exit criteria; D2.1, D2.6 and D2.7; AC3 | 117 total KPIs = 90 migrated + 27 new | 95 + 27 = 122 unless the five v01 additions overlap the 27 | Record an explicit inclusion/exclusion mapping before changing the total |
| §2.1.5; Phase 2 reconciliation; D2.2; AC1 | One-to-one reconciliation with V13.1 | v00 provides external references, not remote DAX source; v01 provides local DAX | Reconcile outputs across representative contexts for every accepted baseline measure |
| §2.1.6; D3.1; AC4 and AC5 | Preserve report behaviour with no data loss | v01 changes relationship activation, direction and date matching | Add the relationship regression tests in §4.6 to the UAT and reconciliation evidence |

### 5.2 Count-baseline options requiring client decision

| Option | Migrated baseline | Remaining/new gap measures | Target total | Consequence |
|---|---:|---:|---:|---|
| A — five v01 additions are part of the agreed 27 | 95 | 22 net additions | 117 | Requires an approved mapping showing which five of the 27 are already delivered; current category descriptions do not establish that overlap |
| B — five v01 additions are additional to the agreed 27 | 95 | 27 | 122 | Preserves v01 parity and the complete gap backlog; requires count, effort, deliverable and acceptance updates |
| C — retain the v00 contractual baseline | 90 | 27 | 117 | Excludes five measures already present in v01; requires an explicit approved exclusion and creates a parity risk |

Until the client chooses an option, the Statement of Work retains its draft commercial figures and this changelog records the technical discrepancy.

---

## 6. Acceptance and Follow-Up Actions

| # | Action | Owner | Evidence required |
|---:|---|---|---|
| 1 | Confirm whether v00 or v01 is the contractual migration baseline | Client Sponsor / Technical Lead | Written baseline decision |
| 2 | Classify the five v01 additions against the agreed 27-measure scope | Product Owner / Technical Lead | Approved measure-to-requirement mapping |
| 3 | Raise a Section 10 change record if counts, timeline, effort or acceptance criteria change | Client Sponsor / Consultant Lead | Approved Change Request / Change Order |
| 4 | Reconcile all accepted baseline measures using outputs, not source-text comparison | Data Engineer / Power BI Developer | Measure-level reconciliation results within AC1 tolerance |
| 5 | Execute the relationship regression tests in §4.6 | Power BI Developer / QA | Test evidence for date, provider, referral and offer filter contexts |
| 6 | Update the checklist classification and future-state KPI dictionary after stakeholder sign-off | Product Owner / Documentation Owner | Approved checklist and KPI dictionary revision |

---

## 7. Verification Record

| Check | Result |
|---|---|
| Source archive hashes captured | Pass |
| Measure declaration counts independently verified | Pass — 90 in v00; 95 in v01 |
| Unique measure names equal declaration counts | Pass |
| Retained/added/removed measure names reconciled | Pass — 90 retained; 5 added; 0 removed |
| External-to-local measure transition verified | Pass — 90 external references in v00; 0 in v01 |
| Relationship declaration counts verified | Pass — 54 in v00; 48 in v01 |
| Relationship removals, reversals and property changes reconciled to totals | Pass |
| Statement of Work count conflict identified without silently changing commercial scope | Pass |
| Checklist row classifications reconciled | Pass — 85 implemented + 2 partial + 3 extra = 90 legacy rows |
| Checklist duplicate analysis reconciled | Pass — 5 exact-DAX groups contain 11 measures (6 redundant definitions); non-exclusive of row classifications |
| Checklist's legacy 90-row analysis separated from the v01 95-measure source count | Pass |

---

*This document is Commercial in Confidence and should not be distributed outside the authorised stakeholder group without written approval.*
