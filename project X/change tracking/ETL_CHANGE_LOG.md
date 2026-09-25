# ETL change log

Delivery batches and their verification. Add new issues and dated resolution notes
to the [ETL issue log](ETL_ISSUE_LOG.md). Run relevant portable validators for
each batch; confirm Fabric behaviour separately in a development Lakehouse.

## 2026-09-25 — Move monitoring reports to the end of both ETL pipelines

- Added `06_reports` with the six `monitoring.rpt_*` materialized lake view
  definitions and removed those definitions from `00_setup_cfg`. Setup retains
  the configuration tables and Gold lineage mapping.
- Live and archive runners now call `06_reports` after Gold dimensions. Updated
  the runbooks and ETL validators; **100 Python/ETL tests pass** and direct Ruff
  checks pass.
- Client work: import the new notebook with both runners, verify it in Fabric,
  and configure the materialized lake view refresh after the parent job completes
  to capture final job and reporting-step statuses.

Issue: [CFG-010](ETL_ISSUE_LOG.md#cfg-010--monitoring-reporting-views-ran-during-configuration-setup).

## 2026-09-25 — Category and location ETL batch

- Updated the active Silver and Gold notebooks, setup lineage and both runners
  for category links, spot bridges, the offer home key and generalised location
  enrichment. Updated the reusable report builder's Homes Offered key.
- Updated ETL validators and the Gold SQL simulation fixture. Local verification:
  **99 Python/ETL tests pass**, direct Ruff checks pass, and `git diff --check`
  passes. The pre-commit wrapper's local cache is not writable. Fabric/Delta
  execution and the optional Spark simulation were not run locally.
- Client deployment still needs an approved coordinate reference, location rule
  acceptance, downstream key and relationship updates, and Fabric verification.

Issues: [GLD-019](ETL_ISSUE_LOG.md#gld-019--missing-framework-category-links-in-referral-and-offer-facts),
[GLD-020](ETL_ISSUE_LOG.md#gld-020--rename-the-offer-home-key-to-provider_home_id),
[GLD-021](ETL_ISSUE_LOG.md#gld-021--add-provider-home-and-referral-spot-category-bridges),
and [SLV-001](ETL_ISSUE_LOG.md#slv-001--generalised-referral-location-and-approximate-offer-distance).
See the [implementation guide](../client%20documentation/04_Data_and_Reporting/CATEGORY_AND_LOCATION_ETL_IMPLEMENTATION.md)
for deployment and audit details.

## 2026-09-23 — Removed obsolete Power BI test files from lint scope

- Pytest-only exclusions left semantic/report test files under Ruff's independent
  `tests/(validate_.*|test_.*).py` pre-commit filter. Reproduced the reported two
  E402 errors in `validate_wmpp_end_goal_design.py` with Ruff before changing it.
- Deleted 11 obsolete semantic-model/DAX/report validators, two related helper
  test modules and the now-unneeded pytest exclusion `conftest.py`. Their
  previous contents remain recoverable from Git history/index. No active
  Python/ETL validators or report implementation tools were removed.
- This supersedes the earlier decision to retain those test files for manual
  use. No lint suppressions or broader lint exclusions were introduced.
- Verified: Ruff 0.16.6 passes all remaining files matched by the pre-commit
  test-folder filter; **73 pytest tests pass**. The hook is pinned to 0.16.3;
  the available local binary was used without changing that pin. Existing
  staged content was left untouched; stage the deletions before committing.

## 2026-09-23 — Removed obsolete snapshot dependencies from Python validators

- Reproduced all four remaining failures: each read an older client notebook
  snapshot instead of relying only on the maintained numbered Python sources.
- Removed duplicate snapshot assertions from GLD-017, Gold schema, job lineage
  and Silver-column validators. Retargeted unique provider-spot and export-date
  checks to active notebooks; all four validators remain in routine pytest.
- Fixed a brittle Gold snapshot assertion: it now checks AST select arguments
  for required columns without requiring an obsolete adjacent column order.
- Added four regression cases that run validators in an isolated active-source
  tree without any report/snapshot folder, then prove missing primary inputs
  still fail. New cases failed before the correction and pass afterwards.
- Full Python-only pytest: **73 passed, 0 failed**. No semantic/report tests ran;
  no production notebook or historical snapshot was changed in this follow-up.

## 2026-09-23 — Routine pytest excludes client Power BI projects

- Per user direction, semantic-model, DAX/measure coverage and report-project
  checks are no longer part of routine pytest. Client project names and versions
  are not stable repository test contracts.
- Python validators use an explicit allowlist; model/DAX helper unit tests are
  excluded from directory collection. Existing Power BI scripts remain available
  only for separately requested reviews. No model/report files were changed.
- Verified collection contains 69 Python/notebook tests and no Power BI tests.
  Result: **65 passed, 4 failed**. The four failures are unchanged comparisons
  against the older WMPP Python notebook snapshot, not semantic/report checks.

## 2026-09-23 — Primary Python notebooks reconciled with Notebooks v16.zip

- Compared all 17 ZIP notebook sources with the active numbered Python files.
  Fifteen match after newline normalisation; two retain documented exceptions.
- Imported the completed Gold closure-column rename, qualified IPA referral
  grouping, removal of ad-hoc CSV preview cells, and ZIP runner timeout/DQ
  settings (archive 9,200 seconds; live 7,800 seconds; essential DQ enabled).
- Retained the valid `monitoring.rpt_job_step_timing` dependency rather than
  reintroducing the ZIP's retired `vw_*` reference. Retained opt-in archive
  reset defaults instead of the ZIP's preconfirmed July 2026 reset.
- Added six regression tests, including synthetic-data execution of the closure
  query. Focused source/syntax/regression tests: **30 passed**. Full pytest:
  **79 passed, 9 failed**, versus **73 passed, 9 failed** before the sync.
  Remaining failures concern the older WMPP snapshot and absent Power BI assets;
  no test was skipped or removed. No Fabric runtime execution or deployment.
- [Comparison, hashes, exceptions and outstanding failures](../reports/notebook-v16-sync/README.md).

## 2026-09-20 — SEM-002: reconciled v16 snapshots, provider KPI evidence and dynamic RLS

**20 September 2026 — implemented in repository; Fabric refresh, Desktop
validation, security population and business acceptance pending.**

- Preserved `MWPP Repo 20092026.zip` as the immutable client baseline and
  created `reports/current/SM WMPP v16 updated` as the repository PBIP
  candidate. `tools/reconcile_semantic_model_v16.py` makes the reconciliation
  repeatable.
- Added a dedicated snapshot-month role and physical month/rule fields,
  migrated state Month-on-Month measures to snapshot data, removed the active
  current/snapshot fact path, changed business relationships to single
  direction and removed automatic date tables.
- Added conservative assignment-to-response evidence from offers and recorded
  decline/cancel reasons. Messages remain excluded until authorship is
  governed. Published scoped, unweighted provider KPI components and the
  provider-home/framework-category bridge; no composite score was invented.
- Added deny-by-default security configuration/Gold tables, a dynamic TMDL
  role for current detail, snapshot detail and provider KPI aggregates, and an
  identifier-free global monthly summary for the separately approved partial-
  RLS path.
- Repaired every statically detectable report field binding, including the 23
  legacy referral-closure-reason references, four placement-type references
  and missing measure aliases.
- Validation: 76 repository tests pass. Static TMDL/reference checks cover 37
  model tables, all report JSON bindings, relationship direction, snapshot
  fields and the RLS role. Fabric SQL execution, refresh, DAX result
  reconciliation and real-identity RLS UAT remain required.

## 2026-09-15 — SEM-001: Gold-only v15 report and requirement-aligned measures

**15 September 2026 — implemented in repository; Fabric refresh and business acceptance pending.**

- Migrated the extracted v15 business report to Gold-only business sources and consistent Import mode; embedded KPI/requirement reference metadata from Markdown. Removed legacy Silver staging and unused report views with missing-field dependencies.
- Repaired referral/date relationships, stale calculated columns and 31 report JSON files with retired field bindings. Kept the provider-to-home relationship inactive to avoid two filter paths into offers; home/QA counts transfer provider IDs explicitly.
- Corrected draft, pending-age, active/under-offer, gender, QA and refresh-label measures. Retained the original inclusive 15–30 KPI alongside the non-overlapping 15–29 dashboard band.
- Added per-IPA signature flags to `gold.fact_ipa` and changed IPA counts/rates to meet the original IPA-grain requirements. Open unsigned and closed unsigned IPAs are distinguished. Same-day draft timestamp edits now count as activity.
- Updated both measure libraries, the WIP guide, KPI reference, schema contract and the complete requirement disposition. See [implementation and acceptance details](../client%20documentation/04_Data_and_Reporting/GOLD_REPORT_IMPLEMENTATION_AND_REQUIREMENTS.md).
- Validation: portable model/visual reference and graph checks, SQL signature predicate cases, and Microsoft TMDL deserialization. Live DAX and Fabric refresh have not been executed. Deploy the changed Gold notebook before refreshing the report.

## 2026-09-13 — Silver export_date propagation and Gold semantic-model push-downs

- SI-025: `export_date` now propagates from Bronze into every Silver table via a
  self-healing contract guard (`ensure_export_date_contract`) in
  `99_common_library`, applied by `02_silver_formatter` and
  `02a_archive_silver`; four new DQ rules guard the column.
- SI-025 correction: the deployed WMPP formatter now carries the same
  self-healing contract guard, parses date-only Bronze values such as
  `2026-09-12`, and recognises the legacy archive representation
  `2026-09-12T00-00-00Z`. Archive date discovery, snapshot selection and
  legacy-table migration use the explicit parser before a Silver run.
- GLD-013: mined the 268 measures in `SM WMPP v15 (3).zip` and pushed the
  remaining computable business rules into the pipeline:
  `silver.referral_enrichment` gained `provider_assignment_count`;
  `gold.fact_referral` gained `provider_assignment_count`,
  `is_emergency_placement` and `is_open_overdue` (all three carried into
  `gold.fact_referral_snapshot`); `gold.fact_offer` gained `offer_age_days`,
  `days_since_offer_activity`, `is_draft_no_activity`,
  `is_draft_missing_dates`, `is_awaiting_ipa_creation`, `is_ipa_pending` and
  `is_ipa_completed` (rolled up from `silver.ipa` signature flags).
- Updated `GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md`,
  `GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE WIP.md`,
  `Gold_DAX_Schema_Contract.md`, `GOLD_DAX_FIELD_COVERAGE_AUDIT.md` (rev 4) and
  `KPI_Reference_Guide.md`: 18 DAX measures rewritten as single flag/column
  filters, the IPA-signature funnel rebuilt at offer grain, KPI-77–78, 80–82,
  85–86 moved from blocked/proxy to covered (195 supported measures; legacy
  v15 reconciliation now 62 covered · 68 ported · 15 retired · 8 blocked).
- Validation: all portable validators pass, including new GLD-013 guards in
  `validate_archive_snapshot_and_enrichment.py` and
  `validate_gold_referral_schema.py`, plus a 15-case DuckDB smoke test of the
  new Gold SQL. Fabric execution and import remain separate acceptance checks.

## 2026-09-12 — Gold referral flags aligned to the original business rules

- GLD-009: `is_open` now implements the original business rule in
  `silver.referral_enrichment` (`03_silver_business_rules`) and propagates to
  `gold.fact_referral` and the snapshot, replacing the inline status check.
- GLD-010: `is_spot` restored to `gold.fact_referral` from
  `silver.referral.is_spot` and carried into the snapshot.
- GLD-011: new `is_awaiting_offer` flag in `silver.referral_enrichment`,
  propagated to `gold.fact_referral`; the `Referrals Awaiting Offer` DAX
  measure is now a single flag filter.
- GLD-012: new `is_engaged` flag on `gold.fact_referral_provider`
  (not cancelled, not closed, not excluded).
- Regenerated the `tests/_gold_fact_sql.sql` simulation fixture from the
  updated `04_gold_model` (extractor now locates the fact cell by content)
  and rewrote `tests/_gold_sim_test.py` for the snake_case model: it
  fabricates `silver.referral_enrichment`, `silver.referral_person` and
  `silver.referral_closure_reason_summary`, derives the GLD-009/GLD-011
  flags from fabricated provider/offer/IPA records, and checks the
  propagated `is_open` / `is_awaiting_offer` / `is_spot` values.
- Validation: all 23 portable validators pass against the updated source,
  including new regression guards for the four fixes. Fabric execution and
  import remain separate acceptance checks.

## 2026-09-11 — Primary notebook source converted to Fabric Python

- Converted all 17 root `.ipynb` notebooks to primary `.py` Fabric notebook
  source, preserving business logic, run defaults, cells, parameter tags,
  dependency bindings and original Spark/session metadata. Retained `.ipynb`
  files are migration references; future edits use `.py`.
- Updated portable validators and the Gold SQL extractor to parse `.py` source;
  added format-boundary and per-notebook syntax/round-trip coverage.
- Compared the primary sources against the supplied client WMPP snapshot:
  nine matching code definitions, six with code differences, and two originals
  missing from that snapshot. No client definitions were overwritten.
- Evidence and reproducible diffs: [notebook comparison](../reports/notebook-comparison/README.md).
- Validation: all 22 existing validators pass against the converted source.
  Fabric execution and import remain separate acceptance checks.
