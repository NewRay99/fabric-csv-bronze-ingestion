# ETL change log

## 17 October 2026 — KPI Date Added metadata

Appended the user-requested `Date Added` field as KPI Definition column I. All 117 original KPI rows first appear in the repository on 26 August 2026 (`b372181`); this is a first-recorded date, not business creation or approval. Original A:H column names/order, KPI values and v1 remain unchanged. Dates are native Excel dates (`dd mmm yyyy`). No notebook, ETL contract, job control or runtime behaviour changed.

## 17 October 2026 — Legend v1 compatibility and verified coverage

**LEGEND-001 — reference workbook/documentation only.** Preserved `Dashboard Legend v1.xlsx`, rebuilt the canonical Legend with its exact three original import schemas, and kept expanded evidence on Gold Source Coverage. Active notebooks, schema/DQ contracts, job ordering and monitoring refresh behaviour are unchanged. Static source evidence and workbook compatibility checks do not certify a Fabric run. See [release runbook](../client%20documentation/05_Operations_and_Runbooks/DASHBOARD_LEGEND_RUNBOOK.md).

Delivery batches and their verification. Add new issues and dated resolution notes
to the [ETL issue log](ETL_ISSUE_LOG.md). Run relevant portable validators for
each batch; confirm Fabric behaviour separately in a development Lakehouse.

## 2026-10-16 — Include sibling placement fields in referral facts (GLD-025)

- `04_gold_model.py` now carries `is_sibling_placement` and `sibling_count`
  from the current Silver referral into the referral fact and its snapshots,
  retaining source types and NULLs. Source validation includes both columns.
- Existing retained months gain nullable fields through snapshot schema
  evolution; historical values require the corresponding archive replay.
- Portable SQL checks cover source values, NULLs and latest-record selection;
  the snapshot checks and extracted simulation SQL are aligned. All 422 tests
  and 158 subtests passed. Fabric execution and consuming-model refresh remain
  deployment checks.

## 2026-10-15 — Retained domain versions and load-count trends (CFG-002)

- `99_data_domain` appends complete run snapshots instead of clearing/replacing
  domains. Preserves old values and marks additions/removals; skipped scans never
  masquerade as removals. Adds standalone job lineage and comparison metadata.
- The current Mission Control WIP supports all retained domain versions and value
  changes, plus previous-load count/percentage differences and 12-load sparklines
  for both read and written counts. Existing report/cache and original ZIPs stay
  separate from the prepared source package; source definitions were backed up.
- 416 tests / 158 subtests passed. Read-only cached checks verify 50 load deltas,
  100 SVG trends and legacy-baseline semantics. Deploy setup/library/profiler and
  refresh the updated model before native visual acceptance; no cloud publication.

## 2026-10-15 — Consistent mobile logo and size-9 page titles (MOB-009)

- Copied the user's saved Target & Urgency Performance phone header to the
  other 30 existing mobile pages, including guides, extracts and drill-through
  pages. The logo is 111 × 25 at (0, 9); each page keeps its own title, now
  size 9 in the neighbouring 203 × 25 box at (120, 9).
- Reused existing logo visuals on 15 other pages. Added 15 off-desktop-canvas
  image sources where no matching logo existed; all reference the same embedded
  asset. No image duplication, model/cache change, desktop-visible layout edit,
  content reflow, custom menu restoration, refresh or publication.
- All 75 changed/added definitions pass published compatible schema checks,
  retaining saved schema references. The previously failing saved-header check
  now passes on all 31 pages; 50 portable tests pass. Full non-target byte hashes
  and cache bytes/timestamp are unchanged from the user's latest saved baseline.
  No new overlaps. Native appearance remains a post-reopen acceptance check.
- Recovery: `reports/_review/mobile-logo-headers-before-20261015`.
  Delivery: `MOBILE_LOGO_HEADERS_DELIVERY.json` in the WIP project root.

## 2026-10-15 — Lossless report-folder size reduction (RPT-003)

- Reduced the saved WIP folder from 83,542,375 bytes (79.7 MiB) to 47,717,099
  bytes (45.5 MiB), including the new delivery record: approximately 43% smaller.
  The report's 4,054 JSON definitions shrink from 53,866,491 to 18,039,421 bytes.
  Only insignificant JSON whitespace/escaping changed; all parsed values are
  identical. No visual, field, measure, bookmark or page was removed.
- Preserved the 21,649,003-byte `SM_WMPP_v16.SemanticModel/.pbi/cache.abf`
  byte-for-byte, including its modification timestamp. All semantic-model files,
  local settings, resources/images, project notes and other non-target files
  are byte-identical. The existing ZIP was not rebuilt or overwritten.
- Recovery copies of the original report JSON and updated provenance records
  are outside WIP under `reports/_review/report-json-format-before-20261015`.
  Compact-layout/native-navigation byte fingerprints record the authorised
  formatting-only update; no report logic or navigation state changed.
- Verification: the actual formatting check fails before and passes after;
  all 46 portable checks pass, as do saved navigation, desktop homepage and
  shared-version checks. Full original/compacted JSON value comparison and
  cache/model/media preservation checks pass. No temporary formatting files
  remain. Native reopening is not yet observed; no refresh/publication occurred.
  This reduces on-disk project size, not model memory. Desktop may re-expand
  JSON formatting on a later save.

## 2026-10-15 — Use native Power BI mobile navigation (MOB-008)

- Removed the custom Menu opener and full drawer from all 31 existing phone
  layouts: 558 navigation-only placement files (18 per page). Keep page headings,
  widening their phone width from 243 to 323 points without moving or restyling
  them. No data content was moved or resized.
- Preserve all 48 remaining filter visuals, filter open/close controls, four
  homepage shortcuts, two Back buttons and two drill-through buttons. Desktop
  navigation/layout, all source visual definitions, queries, bookmarks, model,
  version parameter, hidden-page settings and assets remain unchanged. Dormant
  off-canvas source controls/bookmarks are retained, not placed on phone canvases.
- Every removed placement and replaced heading is recoverable under
  `reports/_review/native-mobile-navigation-before-20261015`. The compact delivery
  inventory now records native navigation and current saved-source provenance;
  existing source edits were preserved rather than reverted to older fingerprints.
- Verification: 40 portable checks and 31 published compatible mobile contracts
  pass. No new geometric collisions across the 31 pages; existing warnings on
  five pages remain unchanged and are recorded separately, not declared fixed.
  Full byte-preservation checks cover non-target mobile objects, desktop/model/
  bookmark definitions and assets. The version checker now tolerates Desktop's
  trailing blank line without ignoring real query/measure changes. Native app
  rendering remains a post-reopen/publish check. No refresh/publication performed.

## 2026-10-15 — Match the desktop Provider Explorer shortcut (RPT-002)

- Corrected the homepage Provider Explorer shortcut, which had inherited the
  compact sidebar pill rather than the desktop hero-button style. It now uses
  the neighbouring shortcut's exact size and per-state icon/label/background
  design, with the existing white building glyph and correct Provider Explorer
  caption in every state. The navigation bookmark remains unchanged.
- Aligned the four desktop shortcuts in one evenly spaced row, with matching
  descriptive columns and a third neutral divider. Existing descriptions retain
  their words and fonts; the new provider description uses the same styling.
  Page size, footer tiles, sidebar and other report pages stay unchanged.
- All phone placement files and effective Provider Explorer phone styling are
  unchanged. Model, report-version parameter, bookmarks and assets are preserved.
  Nine original definitions are recoverable under
  `reports/_review/home-desktop-provider-style-before-20261015`; two desktop-only
  visuals were added (description/divider). No refresh or publication performed.
- Verification: the actual saved-style comparison failed before and passes
  after; all 34 portable desktop/mobile/version tests and 11 published compatible
  visual contracts pass. Existing homepage/mobile badge/link/version checks pass.
  Four-column alignment, all-state styling, icon/label spacing, and separation
  from descriptions/footer tiles are verified statically. Native appearance
  remains a post-reopen check, not established by schema or geometry checks.

## 2026-10-15 — One shared report version parameter (RPT-001)

- Replaced the 14 existing hardcoded `Version: 0.16` footer values in the saved
  WIP with dynamic text-box values bound to one `Report Version Label` measure.
  All original control IDs, geometry, styles and alignment remain unchanged.
- Added the Power Query text parameter `ReportVersion`, initially `0.16`, and
  a local one-row `Report Settings` import table to expose it to DAX. It has no
  relationships or external data source. Version formatting stays text, so
  values such as `0.20` retain their trailing zero. Blank values fail validation.
- Update in Desktop: Home > Transform data > Manage Parameters > ReportVersion;
  edit Current Value, then Close & Apply. The settings row must refresh before
  labels change. Republish the updated report/model for online consumers.
- Verification: 29 portable version/mobile tests, 14 published compatible
  visual-schema checks and native TMDL parsing pass (72 tables, 491 measures,
  two expressions, unchanged 54 relationships and two roles). All unrelated
  definitions, phone placements and assets are byte-preserved. Backup:
  `reports/_review/report-version-parameter-before-20261015`.
- The previous broad Offer Locations mobile overlap check now flags five
  existing collisions; reconstruction from the version backup yields the same
  five before and after. Those unrelated placements were not changed. Referral
  Explorer filter-panel and homepage-shortcut checks still pass. Parameter
  refresh and native text rendering remain post-reopen acceptance checks;
  no running-model update, data refresh or publication was performed.

## 2026-10-14 — Three additional mobile filter panels (MOB-007)

- Reused the Referral Explorer / Offers Overview Filters and Close design on
  Offer Locations (four slicers), Provider Explorer (three) and Provider Registry
  Extract (three). Keep person search, provider search, and both registry
  Provider Name / Home Name searches above the collapsed panel. Existing theme,
  fonts, table columns and desktop geometry stay unchanged.
- Paired phone copies retain exact query, formatting and saved selection
  configuration. Preserve original desktop slicers, adding sync metadata only.
  Copy 25 explicit interaction rules to the new filters so maps and tables keep
  their original filtering behaviour. Open/Close/navigation bookmarks change
  display only; the navigation drawer remains above the filters panel.
- Replaced ten old inline phone placements with grouped copies and moved only
  phone content vertically to close the vacated space. Original desktop visual
  definitions remain. All modified files and removed placements are recoverable
  under `reports/_review/mobile-filter-panels-three-pages-before-20261014`.
- Verification: 23 portable tests and 132 published compatible schema checks
  pass, preserving actual newer saved schema references. Saved-file checks find
  no default-layout or panel-content collisions on the three pages; previous
  Referral Explorer panel and homepage shortcut checks pass. Byte comparisons
  confirm unrelated report pages, model and assets are unchanged. Native
  expanded rendering, selection synchronization and navigation require a
  post-reopen acceptance check; no refresh or publication performed.

## 2026-10-14 — Referral Explorer mobile filter box (MOB-006)

- Added an Offers-style collapsible Filters panel beneath Search / select person.
  All 11 visible user slicers are included; person search stays outside and is
  byte-for-byte unchanged. Hidden journey/metric helper slicers remain untouched.
- Desktop filters retain their exact geometry, queries, formatting and selection
  definitions. Off-canvas phone copies use paired, page-specific sync groups;
  only the originals' sync metadata changes. Opening/closing the panel changes
  display only, not data state. Navigation opening closes the filter panel.
- Replaced 10 old inline phone placement files with grouped phone copies and
  moved the existing journey/data content upward to remove the old filter stack
  and gap. All original filters remain available; only obsolete phone placements
  were removed, with recoverable backup under
  `reports/_review/referral-mobile-filters-before-20261014`.
- Verification: 18 portable tests; field/query/sync pairing; person-search
  exclusion; zero closed-layout and panel-content collisions; and 85 published
  compatible schema checks pass. Actual native rendering and selection-sync
  behaviour remain post-reopen acceptance checks. Model, assets, other report
  pages and existing data/interaction bookmarks are unchanged.

## 2026-10-14 — Homepage Provider Explorer shortcut (MOB-005)

- Added a visible Provider Explorer button beneath Referral Explorer in the
  homepage content, in both Desktop and mobile layouts. Reuse the existing
  orange building badge and the data-preserving Go to Provider Explorer bookmark.
  Existing sidebar/drawer navigation, assets, bookmark definitions and model stay
  unchanged.
- Fit the Desktop button below the unchanged referral paragraph by reducing its
  empty text-box height to 72 points; text/font remain unchanged. Move only the
  two mobile footer cards down 60 points to accommodate the new 52-point button.
  Backup: `reports/_review/home-provider-shortcut-before-20261014`.
- Verification: destination/link checks, 16 portable tests, all four homepage
  badge/spacing checks and 34 homepage bookmark-state checks pass. Five planned
  documents pass published compatible contracts (2.7 visual / 2.4 mobile), while
  preserving Desktop's saved 2.13 / 2.8 schema references, whose public URLs
  returned 404. Native click/render verification remains pending reopening.
- Reconciled validation inventory with four mobile objects already absent from
  the latest saved report; none were restored or changed. A pre-existing
  Referral Detail one-pixel overflow prevents a whole-report mobile pass and is
  recorded in QA without changing that page. No refresh/publication/model changes.

## 2026-10-13 — Homepage mobile image/title spacing (MOB-004)

- Follow-up correction after native feedback exposed detached white symbols:
  the orange circles were separate button-fill images, not part of those icons.
  The same three phone buttons now use the existing combined orange/white
  sidebar SVGs at 32 points, with the independent centred fill-image layer off.
  Title fonts/colours/labels and all row geometry/actions stay unchanged. Backup:
  `reports/_review/mobile-home-badges-20261013`.
- Combined-badge checks fail before and pass after; 15 portable tests and three
  mobile schemas pass. Existing assets/resource registrations, 1,341 other phone
  files and 3,301 non-mobile definitions remain unchanged. Native appearance
  after reopening remains an acceptance check, not established by static checks.

- Changed only the three existing homepage phone buttons to image-left/title-right
  content: 24-point images, 12-point image inset and 52-point title inset in every
  native button state. Keep existing image resources, compact font sizes/colours,
  row geometry, actions, descriptions and navigation unchanged. Backup:
  `reports/_review/mobile-home-button-spacing-20261013`.
- The internal content-area check fails before and passes after; 14 portable
  tests and three mobile schemas pass. All 1,341 other mobile files and 3,301
  protected non-mobile definitions are unchanged. The previous drawer checks
  and all 823 bookmark/page overlap checks still pass.
- Updated the compact formatter to preserve separated homepage content in future.
  Native rendering after reopening the saved WIP report remains unverified.
  No semantic model, ETL, permissions, refresh or publication changes.

## 2026-10-13 — Mobile drawer native-state text repair (MOB-003)

- The full selected-button screenshot identifies WMPP Homepage and shows an
  empty Default-state Text field. The earlier cropped screenshot did not
  establish that the Target & Urgency pilot was being tested.
- Restored complete text/show settings for Default, Hover, Selected and Disabled
  on all 452 named new mobile controls across 31 pages, without changing compact
  fonts, margins, geometry, colours, actions or main content. Backup:
  `reports/_review/mobile-drawer-text-states-20261013-all`.
- Saved Default-state checks fail before and pass after; 13 portable regression
  tests and 452 mobile schemas pass. All 3,301 non-mobile definitions are
  unchanged. The 823 bookmark/page states still have zero table/tile collisions.
- Updated the original generator and compact formatter to preserve state-specific
  labels in future. Native rendering after reopening the PBIP remains an
  acceptance check; no model, ETL, permissions, refresh or publication changes.

## 2026-10-13 — Earlier mobile drawer label pilot (MOB-003)

- Saved explicit original text/show/family/colour settings alongside the compact
  font/margins for 16 phone buttons on Target & Urgency Performance only.
  Source positions, mobile sizes, layer order, bookmarks and page content stay
  unchanged. Backup: `reports/_review/mobile-drawer-labels-20261013-6ae319c8916a5d63a4ff`.
- Label-contract check fails before and passes after; 16 schemas and all ten
  formatter tests pass. All 3,301 non-mobile definitions are preserved.
- Native Desktop capture failed, so the blank-menu root cause is not confirmed.
  Wider rollout is pending a rendered pilot check. No refresh or publication.

## 2026-10-13 — Compact mobile report layout (MOB-002)

- Compacted all 31 current phone layouts, updating 1,344 mobile state files only.
  Vertical sizes/spacing are approximately 20% smaller; buttons are at least
  36 points high, with up-to-10pt labels. Body/table text is mostly 8-9pt,
  headings up to 14pt and numeric KPI values up to 20pt. Dense tables retain
  all fields and horizontal panning, with 3-point row padding.
- Preserved Desktop/model/bookmark definitions, theme colours, field bindings,
  dynamic titles and current field order. Phone-only filter rows have explicit
  positions; main content has separated rows rather than table/card overlays.
- Verification: nine portable formatter/preservation tests pass; all 1,344
  mobile documents pass Microsoft's published schemas. Zero visible default
  overlaps and zero table/tile collisions in 823 bookmark/page states. Native
  Power BI/phone rendering is not claimed and remains an acceptance check.
- Current pre-change phone files are backed up in the Git-excluded directory
  `reports/_review/mobile-compact-before-20261013`. Reusable tool:
  `tools/compact_wmpp_mobile_layout.py`; delivery and QA manifests are
  `MOBILE_COMPACT_LAYOUT_DELIVERY.json` and `MOBILE_COMPACT_LAYOUT_QA.json`.
  No live model writes, refresh, publication, ETL or security changes.

## 2026-10-13 — Provider Registry Extract column activation (GLD-023)

- Reactivated the 17 inactive fields in the saved WIP registry table. All 21
  configured fields are active; no fields were added, removed or reordered.
- Preserved the table's position, size, styles, filters, mobile layout and
  semantic model. All 4,640 other report/model definition files are unchanged.
- Verification: inactive-field check fails before the repair and passes after
  it. A read-only query against the open Power BI model returns all 21 fields
  with data rows. Actual visual rendering remains a post-reopen acceptance check.
- Original visual backed up under
  `reports/_review/registry-columns-before-20261013-9f1a17c0`, excluded from Git.
  No refresh, publication, permissions or ETL changes were performed.
- Same-day recurrence: the file saved at 18:49:43 contained 13 inactive fields,
  a new field order and six custom column widths. Restored those 13 flags while
  preserving the user's newer order/widths. All 21 fields resolve in the native
  cached model; 4,644 other definitions are unchanged. Second backup:
  `reports/_review/registry-columns-repeat-20261013-736c913f`. Reopen acceptance
  and persistence through a Desktop save remain unverified; no bookmark contains
  this table's state, and the exact reason for the recurrence is not established.

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
