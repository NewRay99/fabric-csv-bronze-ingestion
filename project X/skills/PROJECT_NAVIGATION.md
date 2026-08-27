# Project Navigation Skill — WMPP Fabric Data Platform

**Project:** West Midlands Placement Portal (WMPP) data platform
**Client:** Birmingham Children's Trust
**Platform:** Microsoft Fabric Lakehouse
**Purpose:** Find your way around the repository, notebooks, documentation, and change tracking.

---

## 1. Quick-start for common tasks

### I want to run the live pipeline
1. Open `project X/90_run_live_pipeline.ipynb`
2. Verify `Files/cfg_files/schema_definition.csv` is current
3. Run the parent notebook — it orchestrates Bronze → Silver → Gold
4. Check `monitoring.cfg_pipeline_run` for status

### I want to run an archive replay
1. Open `project X/90_run_archive_pipeline.ipynb`
2. Set `PROCESS_ONLY = "YYYY-MM"` and confirmation phrase
3. Run — it replays historical archive → Silver → Gold snapshot
4. Verify `gold.fact_referral_snapshot` rows for the canonical month

### I want to add a new source column to Gold
1. Add the column to `project X/configuration/schema_definition.csv`
2. Update `project X/03_silver_business_rules.ipynb` if enrichment logic is needed
3. Update `project X/04_gold_model.ipynb` or `05_gold_dimensions.ipynb`
4. Update `client documentation/03_Architecture_and_Design/Gold_DAX_Schema_Contract.md`
5. Update `client documentation/04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md`
6. Log in `project X/change tracking/ETL_ISSUE_AND_CHANGE_LOG.md`

### I want to build the Power BI semantic model
1. Read `client documentation/04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md`
2. Read `client documentation/04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md`
3. Import only the active Gold tables listed in the build guide
4. Create relationships per `client documentation/03_Architecture_and_Design/Gold_DAX_Schema_Contract.md`
5. Copy DAX measures from the build guide
6. Reconcile counts before rebuilding visuals

### I want to check if a KPI is supported
1. Check `client documentation/04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md` Section 2
2. If listed ✅ — it is supported
3. If listed in Section 4 — it is blocked by a missing source field
4. Never point DAX at Bronze, Silver, or retired tables

---

## 2. Repository layout

```
project X/
│
├── 00_setup_cfg.ipynb                    # Monitoring/config table DDL owner
├── 00_archive_load.ipynb                 # Archive ZIP/file ingestion
├── 00a_rehydrate_archive_cfg.ipynb       # Legacy archive recovery
├── 00b_reset_silver_cfg.ipynb            # Guarded Silver reset
├── 01_bronze_get_latest.ipynb            # Current CSV → Bronze Delta
├── 01a_cfg_schema_capture_live.ipynb     # Live schema drift detection
├── 01a_cfg_schema_capture_archive.ipynb  # Archive schema drift detection
├── 02_silver_formatter.ipynb             # Bronze → Silver (types, dedup)
├── 02a_archive_silver.ipynb              # Archive → canonical monthly Silver
├── 03_silver_business_rules.ipynb        # DQ, enrichment, rejected rows
├── 04_gold_model.ipynb                   # Silver → Gold facts & KPI views
├── 05_gold_dimensions.ipynb              # Silver → Gold dimensions & bridges
├── 90_run_live_pipeline.ipynb            # BAU orchestration runner
├── 90_run_archive_pipeline.ipynb         # Archive orchestration runner
├── 99_common_library.ipynb               # Shared helpers (exclusions, audit)
│
├── client documentation/
│   ├── 01_Project_Management_and_Governance/
│   ├── 02_Assessment_and_Requirements/
│   │   └── As_Is_Assessment_Report.md    # Legacy v15 KPI inventory
│   ├── 03_Architecture_and_Design/
│   │   ├── HLD.md                        # High-level design
│   │   ├── Proposed_Solution_Architecture.md  # v01 proposal (retained)
│   │   ├── TFD.md                        # Technical/functional design
│   │   └── Gold_DAX_Schema_Contract.md   # ← Gold-to-DAX contract (new)
│   ├── 04_Data_and_Reporting/
│   │   ├── GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md   # Copy-ready DAX
│   │   ├── GOLD_DAX_FIELD_COVERAGE_AUDIT.md         # ← Coverage audit (new)
│   │   ├── KPI_Reference_Guide.md        # Active Gold naming rules
│   │   ├── WMPP_Semantic_Model_Measures.md  # v01 legacy archive
│   │   └── ENHANCEMENT_BACKLOG.md        # Suggested improvements
│   └── Supplementary/
│       └── Measures_Comparison_Checklist.md  # v00 vs functional spec
│
├── change tracking/
│   └── ETL_ISSUE_AND_CHANGE_LOG.md       # All resolved & open ETL issues
│
├── configuration/
│   ├── schema_definition.csv             # Central schema contract
│   ├── dq_rule_definition.csv            # Supplementary DQ rules
│   └── Dashboard Legend.xlsx             # KPI eligibility tracker
│
├── reports/
│   └── client-deliverables/
│       ├── SM WMPP v15.zip               # Legacy semantic model
│       └── report v15.zip                # Legacy PBIX report
│
├── tests/                                # Portable validators
│   ├── validate_archive_load.py
│   ├── validate_silver_required_columns.py
│   ├── validate_notebook_integration.py
│   ├── validate_job_run_lineage.py
│   └── validate_cfg005_contract_source_rows.py
│
└── skills/
    ├── SKILLS.md                     # ← Platform navigation index (start here)
    └── PROJECT_NAVIGATION.md         # Detailed repo layout and task quick-starts
```

---

## 3. Notebook chain and dependencies

```
Latest CSVs ──► 01 Bronze ──► 01a Schema Capture ──► 02 Silver ──► 03 Business Rules ──► 04 Gold ──► 05 Dimensions ──► PBI
                      │                              │                │                    │
                      │                              │                │                    └── dim_date, dim_provider, etc.
                      │                              │                └── referral_enrichment, DQ results
                      │                              └── typed, deduped tables
                      └── raw STRING append

Archive ZIPs ──► 00 Archive ──► 02a Archive Silver ──► 03 Business Rules ──► 04 Gold (snapshot)
```

**Key rule:** `00_setup_cfg.ipynb` is the sole owner of monitoring table DDL. Never create config tables in other notebooks.

---

## 4. Document quick-reference

| Question | Go to |
|---|---|
| What tables exist in Gold? | `03_Architecture_and_Design/Gold_DAX_Schema_Contract.md` Section 2 |
| What DAX measures are copy-ready? | `04_Data_and_Reporting/GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md` |
| Is my KPI supported by Gold? | `04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md` Section 2 |
| Why is my KPI blocked? | `04_Data_and_Reporting/GOLD_DAX_FIELD_COVERAGE_AUDIT.md` Section 4 |
| How do relationships work? | `03_Architecture_and_Design/Gold_DAX_Schema_Contract.md` Section 4 |
| What is the processing flow? | `03_Architecture_and_Design/HLD.md` Section 4 |
| What was the last ETL fix? | `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md` (tail) |
| What validators exist? | `tests/` folder |

---

## 5. Issue and change tracking conventions

All ETL changes are logged in `change tracking/ETL_ISSUE_AND_CHANGE_LOG.md`.

| Prefix | Meaning | Example |
|---|---|---|
| `AR-xxx` | Archive loader/replay issue | `AR-001` |
| `ARCH-ETL-xxx` | Archive pipeline orchestration | `ARCH-ETL-001` |
| `LIVE-ETL-xxx` | Live pipeline orchestration | `LIVE-ETL-001` |
| `SI-xxx` / `SIL-xxx` | Silver layer issue | `SI-024` |
| `GLD-xxx` | Gold layer issue | `GLD-001` |
| `CFG-xxx` | Configuration/monitoring | `CFG-009` |
| `RG-xxx` | Repository reorganisation | `RG-001` |

Before fixing a bug: find the next available number in the log, write the issue using **Symptom / Cause / Fix / Validation** format, and add a regression-guard validator in `tests/` where possible.

---

## 6. Naming conventions

| Layer | Prefix | Example |
|---|---|---|
| Bronze | `bronze.` | `bronze.referral` |
| Archive | `archived.` | `archived.referral` |
| Silver | `silver.` | `silver.referral` |
| Gold fact | `gold.fact_` | `gold.fact_referral` |
| Gold IPA fact | `gold.fct_` | `gold.fct_ipa` |
| Gold dimension | `gold.dim_` | `gold.dim_provider` |
| Gold bridge | `gold.bridge_` | `gold.bridge_provider_framework` |
| Gold view | `gold.vw_` | `gold.vw_kpi_referral_board_summary` |
| Monitoring | `monitoring.cfg_` | `monitoring.cfg_pipeline_run` |

**Column naming:** All active Gold columns are lower-case `snake_case`.

---

## 7. Common pitfalls

1. **Do not import `fact_placement`.** It is retired. Use `gold.fct_ipa`.
2. **Do not import `fact_referral_offer`.** It is a v01 proposal name. The active object is `gold.fact_referral_provider`.
3. **Do not point DAX at Bronze or Silver.** The Gold layer is the only KPI contract.
4. **Do not create an active `fact_offer[offer_id]` → `fct_ipa[accepted_offer_id]` relationship.** It creates an ambiguous path. Use `TREATAS` or `USERELATIONSHIP`.
5. **Do not treat NULL as a business category.** `region`, `complexity_band`, and actual placement dates are null until the source delivers them.
6. **Always run validators before committing.** `python validate_archive_load.py`, `python validate_notebook_integration.py`, etc.
7. **Fabric behaviour must be confirmed in a dev Lakehouse.** Local validators catch logic errors; Fabric catches runtime issues.

---

*Last updated: 27 August 2026. Update this file when the repository structure or notebook set changes.*
