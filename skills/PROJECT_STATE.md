# Project State

## 27 October 2026 — Current referral creator (GLD-026)

Local `master` source baseline: `0f0bf4797d32372ecbaecfd7419834cbb169cef0`; GitHub default branch verified as `master`. The working tree was clean before this work item. `04_gold_model.py` now requires and publishes the existing Silver `referral_created_by` string in `gold.fact_referral`, preserving the selected current row's value and NULLs. The fixture, validator and synthetic tests are updated. Snapshot projection/history and Power BI definitions are unchanged.

Verification: **171 portable checks passed**, including 15 creator regressions, 105 neighbouring referral tests, 26 notebook-format tests and 25 maintained validators. Used a fresh writable pytest temporary folder after an existing `.pytest_tmp` permission error. `git diff --check` passed; optional Ruff was unavailable. Next: deploy the notebook, verify current Silver schema, rerun Gold, reconcile creator values and referral grain without logging identifiers, check SQL endpoint discovery and refresh/review the consuming model. Spark/Delta simulation, Fabric runtime and client acceptance remain unverified. This change is unstaged and uncommitted.

## 27 October 2026 — Fabric high level solution summary

Replaced Fabric_Data_Solution.docx with a concise two-page architecture summary covering the live and archive flows, governed Silver processing, materialised Gold tables, WMPP_v16 reporting, Mission Control, security and recovery responsibilities. The summary was reconciled with the architecture archive and current notebook/model definitions, contains no links to other documents or sites, and was rendered in Word for visual review. Branding uses `reports/templates/WMPP_Theme.json` and the unchanged logo from `reports/current/WMPP/SM_WMPP.Report`, with matching Word heading and table styles. The previous Word file is retained in the task backup. This is a documentation update; deployment, refreshed results and client acceptance remain separate.

## 19 October 2026 — Client documentation wording and synchronisation

The client-edited Phase 3 documents and project README have been reconciled with the pending WMPP_v16 report updates and copied back to their original documentation locations. Current model references use WMPP_v16; earlier delivery references use v15 or earlier. Per-expression hashes and repetitive audit commentary have been removed, while business calculations, outstanding decisions, client links and Markdown structure are retained. Prose paragraphs use a single source line. This update changes documentation only. The current reporting inventory is 73 tables and 502 measure definitions; the concurrent linked-referral status display update is included in the documentation.

## 18 October 2026 — Provider documents and missing requirement KPI visibility (SEM-004)

Both provider pages now show home-level document metadata, recorded expiry dates and a document-level `expired_docs` flag (1 expired, 0 dated/not expired, blank unknown). Removed the unrelated monthly-performance row filter. Four scoped document summaries extend the provider KPI list; 33 already implemented requirement-linked calculations are now surfaced on Requirement Matrix with explicit proxy labels.

The saved business model now has 73 tables/501 definitions/35 pages; relationships and roles remain 54/two. KPI Definition preserves all preceding 567 records and its column contract, appends GOLD-KPI-327–330 dated 18 October, and contains 571 dictionary records. Mission Control remains 34 tables/351 definitions/17 pages. These counts include helpers and historical dispositions; they do not establish accepted KPI scope.

Saved model and catalogue checks have passed. Refreshed results, report and mobile review, access checks and client acceptance remain pending. The data owner must confirm how documents are assigned to homes; the model link and schema contract currently differ. Document compliance, reminder delivery and referral blocking still require separate rules and evidence.

[Implementation, exact calculations, gaps and acceptance](../project%20X/client%20documentation/04_Data_and_Reporting/REQUIREMENT_DASHBOARD_ADDITIONS.md).

## 17 October 2026 — KPI Definition reconciled to latest saved WMPP_v16

KPI Definition is now reconciled to the latest saved local WMPP_v16, rather than only the September catalogue or repository ZIP. The business source has 72 tables/492 measure definitions/35 pages; current Mission Control has 34 tables/351 definitions/17 pages. The calculation reference records these changes; production refresh and acceptance remain pending.

The sheet retains the original A:H column names/order and Date Added in I. Original KPI IDs, requirement links/descriptions, Section values and original specifications are preserved. Current Tables/Calculation/PBI Measure fields have been refreshed and missing reporting definitions appended. It now has **567 dictionary records**: the preceding 152 plus 231 additional business definitions and 184 operational metrics. This is a dictionary record count including historical aliases/dispositions, not an approved KPI scope total. Display/filter/selection helpers are separately labelled in Gold Source Coverage; all 843 current definitions are documented.

Current fixed-metric coverage: 338 business definitions and 184 operational definitions; the 843-measure inventory also includes technical helpers. Original scope/approval decisions remain separate. Next: controlled embedded-reference synchronisation and runtime/role/UAT checks. No source model or ETL mutation.

[Current DAX, Python/Spark SQL and source evidence](../project%20X/client%20documentation/04_Data_and_Reporting/KPI_LATEST_CALCULATIONS.md).

**Project:** BCT WMPP Fabric and Power BI platform **State date:** 18 August 2026 **Purpose:** Concise handover and continuity record for the ChatGPT Project.

## Current implementation baseline

- Active notebooks are held directly in the `project X` root.
- Two processing streams are supported: historical archive hydration and BAU latest processing.
- Configuration-table DDL is centralised in `00_setup_cfg 02 03.ipynb`.
- Schema governance uses an approved definition plus live/archive observations and drift events.
- Internal reference objects, including logical names beginning `ref_`, are excluded from ordinary dated ETL processing.
- Missing DQ source objects/columns and FK parents can be captured as auditable skips.
- Power BI semantic-model history and measure/relationship changes are tracked separately from ETL changes.

## Current documentation baseline

- Project README and client documentation index are the entry points.
- HLD and TFD exist under `03_Architecture_and_Design`.
- This pack introduces an FFD so functional behaviour is no longer mixed into the TFD alone.
- ETL and semantic-model changes have separate logs.

## Controlled risks and decisions

| Item | Current position | Required action |
|---|---|---|
| KPI/measure baseline | Repository evidence contains several historical/proposed totals | Confirm accepted baseline and classify additions through change control |
| Historical fallback sources | Proposed for entities missing from archives | Approve source, effective date range, provenance, and reconciliation before use |
| RLS | Required for authority/region access | Confirm security mapping, roles, test users, and regression evidence |
| Runtime validation | Some checks are portable; Spark/Delta/DAX validation needs platform access | Record environment-specific test evidence before production acceptance |

## Most recent verified repository work

- Repository structure was reorganised without deleting material.
- Current notebooks were promoted to the `project X` root.
- Client documentation, configuration, tests, reports, and change tracking were separated into clear folders.
- Portable notebook validators passed after the reorganisation.
- SI-007 contract rebuilt from observed drift fields: 397 fields across 31 tables, with explicit `CONTRACT_FK`, `TRIAL_JOIN`, and `INVALID_JOIN` classifications.
- GLD-001 Gold mappings use the flattened Silver referral contract and allow absent historical event-log enrichment without suppressing mandatory-source failures.
- SI-008–SI-012 are idempotent Silver materialisations for axes, closure summary, and date dimension.
- Configuration CSVs are now bootstrapped once by setup into `monitoring.cfg_schema_contract_column` and `monitoring.cfg_data_quality_rule`; child notebooks read the Delta tables.
- Latest and archive Silver no longer trust a prior successful audit when the target is missing contract columns; the new Silver-column regression test covers the Gold-required referral fields, including `placement_type`.
- SI-013–SI-016 repaired and consolidated `99_common_library 02 03` and introduced guarded `PROCESS_ONLY = "YYYY-MM"` archive replay controls.
- The nonexistent source event-log shell was removed. Silver now materialises `slv_referral_lifecycle_event` from available Referral, Offer, Provider Message, and IPA timestamps; Gold consumes this derived lifecycle stream.
- Verified with the SI-007 materialisation validator and the full portable validator set.

## Next action

- Deploy the current contract and notebooks to Fabric. Use `PROCESS_ONLY` for a traceable single-month archive replay, then capture Silver, event-log shell, DQ, Gold, and trial-join evidence.

## Update protocol

After every material work item, update:

1. state date;
2. implementation baseline if behaviour changed;
3. documentation baseline if files/roles changed;
4. open risks/decisions;
5. most recent verified change and test evidence; and
6. next actions and owner where known.
