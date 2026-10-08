# ETL change log

Delivery batches and their verification. Add new issues and dated resolution notes
to the [ETL issue log](ETL_ISSUE_LOG.md). Run relevant portable validators for
each batch; confirm Fabric behaviour separately in a development Lakehouse.

## 2026-10-08 — Nightly raw archive mode and explicit historical replay

- `90_run_archive_pipeline.py` defaults to `ARCHIVE_RUN_MODE="ARCHIVE_ONLY"`:
  setup, archive load, archived-schema capture, then monitoring reports.
  `REPLAY` retains the complete six-step historical Silver/DQ/Gold sequence.
  Neither mode automatically drops raw archive tables or forces a reset.
- Exposed run-mode, job and guarded replay controls in the Fabric parameter
  cell. Validate mode, boolean controls, month and reset confirmation before
  child execution; reject replay controls in archive-only mode.
- Corrected archive capture's source from Bronze to `archived` and designated
  its parameter cell. Derived parent-run checks in archive load/capture and
  full-reset guards in archive Silver now evaluate after Fabric parameter
  overrides instead of using uninjected defaults.
- Verification: 383 tests and 158 subtests pass, including 25 synthetic-child
  checks for routes, forwarding, confirmations, failures and injection ordering.
  Ruff passes for both changed test/validator files. No Spark execution or deletion.
- Updated runbooks with daily scheduling, dated export prerequisites, separate
  full-reset instructions and post-replay live recovery. Existing ZIP/file
  reload protection remains; no copy from `latest/` and no audit-default change.
- Local source changes only. Deploy the four changed notebooks and configure
  the Fabric schedule before nightly retention becomes operational.

## 2026-10-07 — Source-reference identifiers and duplicate review (GLD-024)

- Added `dim_person.source_reference_id` from the existing source field,
  retaining text/leading zeros. `fact_referral` carries the selected person's
  reference plus `has_multiple_referrals`, `source_reference_referral_count`
  and `order_dupe`; no referral is removed and UUID keys remain authoritative.
- Deduplicate person export versions before selection/joining. Preserve the
  existing lowest-person-ID choice on multi-person referrals. Count eligible
  as-of referrals sharing a trimmed, case-insensitive nonblank reference,
  including closed referrals. Sequence oldest creation first, UUID for ties.
  Blank references have flag false/count zero and their own navigation sequence.
- Copy the new fields into newly written snapshots only; old retained months
  remain NULL until historical replay. Annotations are refresh/as-of facts,
  not current-filter or RLS-cohort counts and not automatic deletion rules.
- Updated nine direct import fields, 13 table projections, six identifier
  searches, navigation prose/selection label and compound reference/sequence detail binding
  in the saved WIP. No DAX classifier, relationship rekey, KPI count change,
  security relaxation, visual repositioning or report ZIP rewrite.
- Verification: **358 tests and 158 subtests** pass; 29 new reference/migration
  checks, Gold-schema/dimension validators and idempotent patch preview pass.
  All 27 changed visuals retain positions/sizes; 2,704 unlisted WIP files remain
  hash-identical excluding `.pbi`. Backup contains all 32 touched WIP files:
  `reports/WIP/_review/source-reference-identifiers-20261007-734c16`.
- Root notebook and local definition changes only. Deploy/run `04_gold_model`
  and `05_gold_dimensions` before refreshing/reopening WIP. Native Spark/Delta,
  model refresh and duplicate/blank-reference drillthrough remain acceptance
  checks. No live Fabric execution, permission change or publication.

See [reference semantics and deployment](../client%20documentation/04_Data_and_Reporting/GOLD_REFERRAL_JOURNEY_STATUS.md#source-person-reference-and-multiple-referrals-7-october-2026).

## 2026-10-07 — Timezone-aware UTC monitoring clocks (LIVE-ETL-005)

- Reproduced Python's `datetime.utcnow()` deprecation directly from the
  notebook clock expressions with deprecation warnings treated as errors.
- Replaced all 43 `utcnow()` calls in the eleven root pipeline/library/helper
  notebooks with `datetime.now(timezone.utc)`, adding explicit timezone imports.
  Silver receives those imports from its existing isolated shared-library
  `%run`. Replaced the archive-rehydration helper's one deprecated
  `utcfromtimestamp()` with `datetime.fromtimestamp(..., timezone.utc)` too.
- Updated both sides of elapsed-time calculations together. UTC run dates,
  job IDs, status transitions, table schemas and source/export-date parsing
  are unchanged; this does not rebuild or clear `monitoring.cfg_job_run`.
  No historical timestamp conversion or Spark session-timezone change.
- Added 16 executable regression checks: real clock expressions warn-free and
  aware UTC, PySpark TimestampType preserves the UTC epoch/microseconds,
  RUNNING/SUCCESS/FAILED child records retain keys/schema, and shared/DQ elapsed
  calculations use compatible objects. Synthetic file metadata only.
- Verification: **329 tests and 158 subtests** pass, plus job-run lineage,
  live monitoring, core pipeline and archive-runner validators. No live Fabric
  execution, notebook deployment, table mutation or report/layout change.
- Deploy the eleven updated root notebooks, including `99_common_library`,
  before rerunning the relevant live/archive runner. Exported notebook copies
  under `reports/` were not rewritten; native Fabric acceptance remains a
  deployment check. Temporary test fixtures removed; no debug logs retained.

See [Python's UTC datetime guidance](https://docs.python.org/3/library/datetime.html#datetime.datetime.utcnow)
and [Spark TimestampType conversion](https://spark.apache.org/docs/3.5.6/api/python/_modules/pyspark/sql/types.html#TimestampType).

## 2026-10-07 — Complete provider/home registry baseline

- Corrected GLD-023's retained Fostering eligibility filter. The authoritative
  population is exactly `gold.dim_provider LEFT JOIN gold.dim_provider_home`
  on provider ID, with no membership, provider-status or activity requirement.
  This supersedes the Fostering-only scope recorded on 6 October below.
- Basic provider/home fields come from the Gold dimensions. Latest Silver
  contacts, all framework memberships and independently aggregated facts are
  LEFT enrichments; missing enrichment cannot remove a directory row. Unknown
  framework lookups retain their codes and providers without membership remain.
- A pre-write count and bidirectional key-multiset comparison catches missing,
  added, multiplied and same-count substituted provider/home rows. Invalid
  duplicate dimension keys stop for source review; they are not silently
  deduplicated. The existing one-row-per-pair check does not mean one provider
  row: a provider with three homes has three registry rows.
- Retained provider/home offers, drafts, accepted/rejected offers, IPA counts,
  signature flags, observed response minutes, message counts, straight-line
  distances and estimated weekly/lifetime costs. Provider-wide values repeat
  across homes; missing-cost and measurement denominators remain explicit.
- Setup now records ten source dependencies, including both Gold dimensions.
  Updated the scoped report expansion and deployment/security guidance.
- Restored the saved WIP's missing home/metric columns: 78 model columns and
  72 direct raw export fields. Changed only that import, its table projections
  and known scope labels. Preserved the source connection, existing lineage,
  all positions/styles, roles, export settings and other project files. Backup:
  `reports/WIP/_review/registry-complete-baseline-20261007-a681f71c`.
- Verification: **313 tests and 158 subtests**, including 51 focused registry
  checks; Gold-dimensions/setup validators and idempotent WIP preview pass.
  The regression reproduced 3 rows from a synthetic 1,002-row dimension
  baseline before the fix; the corrected SQL returns all 1,002 matching keys.
  Hashes confirm all 2,732 unlisted WIP files unchanged, excluding `.pbi`.
- Local checks do not establish actual Lakehouse counts or native Fabric SQL,
  Power BI rendering, service security or Excel exports. No live execution,
  publication, permission change, reset or historical replay was performed.

See [current registry baseline and deployment](../client%20documentation/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md).

## 2026-10-06 — Provider registry home grain and raw metric expansion

The Fostering-only scope in this entry is superseded by the 7 October correction above.

- Supersedes GLD-023's earlier provider-only grain: current Fostering provider
  LEFT current provider_home, unique by provider/home ID. Includes homes without
  offers and one blank-home row for providers without homes. Actual home name,
  service type, status, address, contacts, spot flag and beds replace constants.
- Deduplicate each entity before separate aggregates, avoiding offer/IPA/message
  fan-out. Export provider/home offer, draft, accepted/rejected, IPA, signature,
  completed/active and cost metrics. Messages, assignment declines and response
  times stay provider-only because their source has no home key. Distance is
  offer-weighted city-to-postcode straight-line kilometres, with a denominator.
- Estimated lifetime cost uses inclusive prorated admission/planned days through
  the earlier of recorded end and the common Gold fact as-of date. Known future
  starts contribute zero, missing/invalid evidence is counted, closed costs stay
  included. Current fees, not invoices/rate history: never label actual spend.
  Active weekly liability retains the report's non-closed IPA definition.
- Provider-wide values repeat across homes; label prefixes, `summarizeBy: none`,
  no visual totals and an explicit warning prevent silent additive assumptions.
  Home attribution requires the same provider/home and accepted-offer linkage.
- Updated setup lineage (eight registry dependencies), template, scoped expansion
  tool, synthetic regression checks and deployment/security handover. Facts must
  precede dimensions; existing live/archive runner order already does this.
- Saved WIP changed only registry import additions, raw table projections and
  its grain description. Preserved user connection/lineage, layouts, all roles,
  other pages, relationships/bookmarks and export mode None. Backup:
  `reports/WIP/_review/registry-home-metrics-20261006-165955`.
- Verification: **306 tests and 158 subtests**, including 44 focused registry
  checks; Gold dimensions/config validators and idempotent expansion preview
  pass. Native Fabric/Delta execution, refresh, rendering, service audience and
  export remain deployment checks. Registry aggregates cross referral scopes
  for the registry audience; review small-cell disclosure before publication.
- No live database run/reset, publication, permission change or exported file.

See [updated registry deployment and definitions](../client%20documentation/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md).

## 2026-10-06 — Group-based Provider Registry access

- User named `wmpp_report_users` for ordinary report readers and
  `wmpp_provider_registry_users` for registry viewers/exporters. Supersedes the
  earlier hard-coded email exceptions; group membership becomes authoritative
  after the corresponding service roles are assigned.
- Restored `rpt_provider_registry = FALSE ()` in the ordinary dynamic role.
  Added `WMPP Provider Registry RLS` with registry permission `TRUE ()` and
  **identical predicates on every other table**, preserving referral, snapshot,
  identity and scoped provider-KPI rules even under overlapping membership.
- Registered the new role and added descriptive `WMPP_ServiceGroup` annotations.
  These labels do not create groups or set membership. Consumers remain Viewers;
  do not assign the ordinary group to the registry role.
- Preserved every report page, visual, layout, bookmark, relationship, edited
  import and cache. Backup: `reports/WIP/_review/registry-groups-20261006-162157`.
  Installer group mode accepts only an approved transition from its deny/UPN
  predicate and refuses unknown roles or scoped-role drift.
- Verification: **296 tests and 158 subtests passed**, including 34 focused
  registry ETL/safe-edit checks. All six other saved table predicates match
  between roles, and the group-mode preview is idempotent. Hashes confirm all
  2,733 unlisted project files unchanged (excluding `.pbi` cache). Native DAX,
  real group identity, role membership and export checks remain outstanding.
- No service publication, group creation, account assignments, tenant export
  policy or exported contact file. Report export mode is still **None** until
  IT reviews and enables Excel/CSV exports for the registry group; tenant-wide
  impact and real Viewer acceptance remain deployment checks.

See [group-to-role handover](../client%20documentation/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md#contact-access).

## 2026-10-06 — Earlier two-account access change (superseded)

- User approved `akhtar@bham.co.uk` and `hamanat@bham.co.uk` as the only
  ordinary viewers of the Fostering contact registry. Replaced the registry's
  deny-all expression within the existing `WMPP Dynamic Detail RLS` role with
  an exact sign-in allowlist. Other table permissions and role membership are
  unchanged; no additional model role or referral scope was granted.
- Unhid only the registry page and updated its access note. Page layout,
  dashboard visuals, sidebar, relationships, bookmarks, model imports and
  `.pbi` cache were preserved. The existing edited registry import was not
  overwritten. Backup: `reports/WIP/_review/registry-access-20261006-154319`.
- Added explicit `--registry-user` approval and an `--access-only` mode to the
  reproducible installer. Default setup still denies contacts. Access-only
  mode preserves manually edited imports, visuals and page dimensions.
- Verification: **288 tests and 158 subtests passed**, including 26 focused
  synthetic ETL/safe-edit checks. The access-only
  preview of the saved WIP plans no further changes. Live DAX evaluation,
  service-resolved identities and Viewer/export acceptance are not asserted.
- The saved report's export setting remains **None**. No publication, live
  account/group membership or tenant export policy changed. Fabric handover
  must restrict Excel/CSV exports before enabling summarized report exports;
  review the tenant-wide impact or use a separately restricted extract report.

See [approved audience and simple handover](../client%20documentation/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md#contact-access).

## 2026-10-06 — Separate referral source status and Gold journey stage

- At the user's request, retain `fact_referral.current_status` as the original
  Silver status and add separate `journey_stage` and `journey_stage_order` fields.
  Aggregate offer/IPA evidence at referral grain with the existing journey
  precedence; keep offer/IPA details in their own facts.
- Copy the three fields into new monthly snapshots without relabelling older
  months using current evidence. Source-status outcome rules and summary
  semantics are unchanged.
- Updated only the two referral semantic tables in the saved WIP to import
  Gold stages under the existing journey field names and lineage identifiers.
  Backups: `reports/WIP/_review/source-journey-split-20261006-085714`.
  No report visual, page, bookmark, relationship, security role or ZIP changed.
- Restored the journey SQL checks against the separated fields, retained raw
  status checks and updated the SQL fixture and deployment instructions.
- Verification: **279 tests and 158 subtests passed**, including 85 focused
  source-status/journey SQL checks. Gold notebook validation, Ruff and diff
  checks passed. Import bindings and current journey lineage were checked;
  hashes confirm all 2,536 report-definition files, 74 unrelated model files
  and the user's modified ZIP are unchanged.
  The semantic files are Git-ignored, so retain the saved project and backup
  alongside the notebook changes.
- Deployment: run the revised Gold notebook before reopening/refreshing the updated WIP.
  Fabric deployment, refresh and native interaction checks remain outstanding.

Issue: [GLD-022 revised decision](ETL_ISSUE_LOG.md#gld-022--materialise-referral-journey-status-in-gold).
See [field definitions and deployment steps](../client%20documentation/04_Data_and_Reporting/GOLD_REFERRAL_JOURNEY_STATUS.md).

## 2026-10-06 — Revert Gold referral journey status

Superseded by the separated fields above after the user reconsidered; retained
as local change history. No Fabric deployment occurred between these decisions.

- Reverted GLD-022 at the user's request. `fact_referral.current_status` again
  contains the original Silver referral status. Removed the added Gold
  `referral_status`, stage order/rule version, classifier and evidence joins.
- Restored the original snapshot projection and required-placement-date outcome
  rules. No historic snapshot rows, DAX journey calculations, map coordinates,
  provider extracts, report/semantic files or report ZIP were changed.
- Replaced obsolete Gold journey-classification tests with source-status
  preservation checks and updated the SQL simulation fixture and deployment
  guidance. Fabric execution and semantic refresh remain outstanding.

Issue: [GLD-022 rollback](ETL_ISSUE_LOG.md#gld-022--materialise-referral-journey-status-in-gold).
See [rollback instructions](../client%20documentation/04_Data_and_Reporting/GOLD_REFERRAL_JOURNEY_STATUS.md).

## 2026-10-05 — Provider registry extract

- Consolidated GLD-023's identical Fostering queries into
  `gold.rpt_provider_registry` in `05_gold_dimensions.py`, with setup lineage.
  One current row per provider, all nine contacts and every distinct qualifying
  framework code; no offer/home requirement. No contacts were added to the
  general provider dimension.
- Added the direct import and hidden **Provider Registry Extract** table page
  to `reports/WIP/SM WMPP v16 updated WIP`. The existing reader role denies rows
  on the new contact table pending an audience decision. No service access,
  publication, export settings or existing report layouts were changed.
- Local verification: **248 tests and 158 subtests passed**, including 17 new
  synthetic ETL/safe-edit checks; tool/test Ruff and Gold notebook validation
  passed. Backed-up apply confirmed all unlisted report/model files unchanged.
- Fabric execution, refreshed data, native export and audience approval remain
  outstanding. [Deployment and export guide](../client%20documentation/04_Data_and_Reporting/PROVIDER_REGISTRY_EXTRACT.md).

Issue: [GLD-023](ETL_ISSUE_LOG.md#gld-023---generate-extracts-from-the-report).

## 2026-10-04 — Gold referral journey status

Superseded by the 6 October separated-field decision above; retained as delivery history.

- `04_gold_model.py` now publishes the existing eight referral journey stages
  as `fact_referral.current_status`, with `current_status_order` and an explicit
  rule version. The original source value is retained as `referral_status`.
- Offer/IPA evidence is aggregated before joining to retain one referral row.
  Terminal overrides, same-active-IPA signatures and DAX stage precedence are
  preserved. Source-status outcome rules remain separate from journey stages.
- Retained snapshot/summary status semantics are preserved; new snapshot rows
  have separate journey fields. No historic journey inference, semantic model,
  report layout, report ZIP or deployed Lakehouse was changed.
- Verification: **203 tests and 158 subtests passed**, including 54 new checks
  executing the notebook SQL with a portable relational engine. Fabric/Delta
  execution and the user's semantic-model migration remain to be verified.
- Migration: [Gold referral journey status](../client%20documentation/04_Data_and_Reporting/GOLD_REFERRAL_JOURNEY_STATUS.md).

Issue: [GLD-022](ETL_ISSUE_LOG.md#gld-022--materialise-referral-journey-status-in-gold).

## 2026-10-01 — Uploaded coordinate ZIP support

- `00c_load_location_coordinates.py` now defaults to uploaded `codepo_gb.zip` and
  `opname_csv_gb.zip` in `Files/cfg_files/location_reference/`. Existing CSV folder
  inputs remain supported. No access to local Windows Downloads is required.
- Extracts only official data CSVs into a fresh Lakehouse folder per run, preserving
  source ZIPs and excluding documentation/headers. Rejects unsafe paths, symbolic
  links, duplicate destinations and excessive selected size/count. Extracted files
  remain for lazy Spark reads; old runs are not automatically deleted.
- Lookup preview/merge safeguards and offline projection are unchanged. Preview
  extracts files but does not modify `cfg_location_coordinate`.
- Verification: **130 tests and 158 subtests passed**, including real temporary ZIP
  extraction tests. Loader/test Ruff checks passed. Fabric-mounted extraction,
  actual source deliveries and Spark/Delta execution still require Fabric validation.

## 2026-09-30 — Offline coordinate reference loader

- Added `00c_load_location_coordinates.py` for local, uploaded OS Code-Point Open
  and Open Names CSV data. It uses Silver provider-home postcodes, converts British
  National Grid coordinates locally, and merges into `cfg_location_coordinate`.
- Preview is default; network access for projection is disabled, missing packages
  are not installed, and existing approved coordinates are preserved by default.
  Ambiguous place names and unusable/sector-level postcode points are excluded.
- Gold now distinguishes OS Open Names representative settlement points from its
  existing centroid basis. The haversine formula and suppression rules are unchanged.
- Verification: **122 tests and 158 subtests passed**; direct Ruff checks passed for
  the new loader and tests. Actual pyproj conversion, Spark/Delta merge and Fabric
  execution are still to be verified with approved files/environment. No reference
  datasets were downloaded, customer data exported or deployed tables changed.
- Upload and execution instructions: [offline reference runbook](../configuration/location-reference/README.md).
  This is a deliberate maintenance notebook, not an automatic live/archive step.

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
