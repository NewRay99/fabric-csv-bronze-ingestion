# SKILLS.md — WMPP Fabric Data Platform Navigation

**Project:** West Midlands Placement Portal (WMPP) data platform
**Client:** Birmingham Children's Trust
**Platform:** Microsoft Fabric Lakehouse (medallion: bronze → silver → gold)
**Repo root:** `project X/`
**Companion:** `skills/PROJECT_NAVIGATION.md` (detailed layout and task quick-starts)

---

## 1. What this project does

Ingests WMPP CSV extracts (live drops + archive ZIPs) into a Fabric
Lakehouse, cleanses them through Bronze/Silver, and publishes a Gold
analytical model that feeds the replacement Power BI semantic model and the
Mission Control monitoring report.

- Live pipeline: `90_run_live_pipeline.ipynb`
- Archive replay: `90_run_archive_pipeline.ipynb`
- Monitoring (`monitoring.cfg_*`) DDL is owned solely by `00_setup_cfg.ipynb`;
  table contents are driven by `configuration/schema_definition.csv` and
  `configuration/dq_rule_definition.csv`.

## 2. Where things live

| Area | Path |
|---|---|
| Pipeline notebooks | `project X/*.ipynb` (numbered 00–05, 90, 99) |
| Shared helpers | `99_common_library.ipynb`, `99_data_domain.ipynb`, `99_data_extracts.ipynb` |
| Schema & DQ contracts | `configuration/schema_definition.csv`, `configuration/dq_rule_definition.csv` |
| KPI eligibility tracker | `configuration/Dashboard Legend.xlsx` |
| Requirements / as-is | `client documentation/02_Assessment_and_Requirements/` |
| Architecture (HLD/TFD/contract) | `client documentation/03_Architecture_and_Design/` |
| DAX & KPI docs | `client documentation/04_Data_and_Reporting/` |
| Runbooks | `client documentation/05_Operations_and_Runbooks/` |
| Change log | `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md` |
| Legacy Power BI deliverables | `reports/client-deliverables/` (`SM WMPP v15.zip`, `report v15.zip`, `SM WMPP Mission Control.zip`) |
| Regression validators | `tests/` |

## 3. The reporting contract (read before touching DAX)

1. **Gold-only rule:** published DAX may reference active `gold.*` tables
   only. Never `bronze.*`, `silver.*`, or retired tables (`fact_placement`,
   `fact_referral_offer`, legacy `dim_referral` / `dim_offer_status` /
   `LocalDateTable_*` / `KPI Selector` / `ref_KPI` / `Draft Age Band Table`).
2. **Copy-ready measures:**
   `04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md` —
   185 measures (109 original + 76 ported from legacy v15), including the
   legacy v15 full-library port section with disposition for all 153 legacy
   measures (59 covered · 62 ported · 15 retired · 17 blocked).
3. **Field proof:**
   `04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md` — every measure
   mapped to its Gold column(s); blocked KPIs listed with the source change
   that would unblock them.
4. **Schema contract:**
   `03_Architecture_and_Design/Gold_DAX_Schema_Contract.md` — table
   inventory, column-to-DAX mapping, relationship rules, blocked fields,
   extension rules, verification checklist.
5. **Monitoring model is separate:** Mission Control measures use
   `monitoring.cfg_*` tables and stay in their own semantic model
   (`SM WMPP Mission Control.zip` lineage), not the referral Gold model.

## 4. Common tasks

| I want to… | Steps |
|---|---|
| Run the live pipeline | `90_run_live_pipeline.ipynb` → verify `monitoring.cfg_pipeline_run` |
| Replay an archive month | `90_run_archive_pipeline.ipynb` with `PROCESS_ONLY = "YYYY-MM"` + confirmation phrase |
| Add a source column to Gold | `schema_definition.csv` → `02_silver_formatter` (auto) → `03_silver_business_rules`/`04_gold_model`/`05_gold_dimensions` → build guide → schema contract → change log (`GLD` prefix) |
| Build the Power BI semantic model | Build guide → coverage audit → schema contract relationship rules → reconcile `DISTINCTCOUNT` of `referral_id`, `offer_id`, `ipa_id`, `referral_provider_id` |
| Check whether a KPI is supported | Coverage audit Section 2 (supported) / Section 4 (blocked) |
| Log an issue or change | `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md`, Symptom/Cause/Fix/Validation format; see prefix table below |

## 5. Change-log prefixes

`AR` archive loader · `ARCH-ETL` archive pipeline · `LIVE-ETL` live pipeline ·
`SI`/`SIL` silver · `GLD` gold · `CFG` configuration/monitoring · `RG` repo
reorganisation. Find the next free number per prefix before writing the
entry; add a validator in `tests/` where possible.

## 6. Hard pitfalls

1. `fact_placement` is retired → use `gold.fct_ipa`.
2. `fact_referral_offer` never existed in Gold → use
   `gold.fact_referral_provider`.
3. No active `fact_offer[offer_id]` → `fct_ipa[accepted_offer_id]`
   relationship (ambiguous path) → use `TREATAS`/`USERELATIONSHIP`.
4. NULL Gold fields (`region`, `complexity_band`, actual placement dates,
   `contact_made`) are blocked source gaps — never invent values in DAX.
5. `dim_date` → `fct_ipa[ipa_issued_date]` must stay inactive; use
   `USERELATIONSHIP` in IPA time-intelligence measures.
6. Run portable validators (`tests/`) before committing; confirm Fabric
   runtime behaviour in a dev Lakehouse.

---

*Created 27 August 2026 alongside change-log entry GLD-003. Update when the
notebook set, Gold contract, or documentation layout changes.*
