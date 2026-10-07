# Provider registry extract

Updated 7 October 2026. GLD-023 now has a COMPLETE provider/home registry from
the Gold notebook through to the saved WIP semantic model and an export table.
The source implementation is ready; Fabric execution, data refresh and Desktop
rendering still require deployment verification. No live contact file has been
generated or published.

## Extract scope

The source population is exactly:

```sql
FROM gold.dim_provider p
LEFT JOIN gold.dim_provider_home h ON p.provider_id = h.provider_id
```

Every dimension provider and its dimension homes are retained, across ALL
placement types, statuses and framework memberships. A provider with no home
has one blank-home row. No membership, offer, IPA, assignment or message is
required. If that unfiltered dimension left join contains 1,002 rows, the Gold
registry must also contain exactly 1,002 rows, with the same provider/home pairs.
The former Fostering-only eligibility and membership INNER JOIN are removed.
This supersedes both earlier provider-only and Fostering-only scopes.

`05_gold_dimensions.py` uses the Gold dimensions for provider/home keys and
basic directory fields. Latest `silver.provider` and `silver.provider_home`
records LEFT enrich contacts, extra home address/status fields and email. A
missing Silver contact row must not hide its Gold dimension provider/home;
a Silver record outside the dimension population must not create a new row.

Frameworks and each separately aggregated metric are LEFT joined. Multiple
frameworks are rolled up first, so they cannot multiply rows. All memberships,
including codes missing a framework lookup, are retained as descriptive data.
A provider without membership has a blank Framework Code/Placement Type and
Framework Count zero. Latest membership ID versions supersede older exports.

Contact enrichment records are ordered by source `export_date`, then `_silver_load_ts`.
Equal timestamps use a stable ordering of all source provider fields, rather
than selecting an arbitrary contact record. NULL contacts remain NULL; an older
email is not substituted for a missing current email. Missing required columns
fail the registry build before its existing table is overwritten.

`Framework Code` contains all distinct membership codes, sorted and separated
by `; `. This deliberately replaces the old arbitrary choice of one framework
after sorting and deduplication. Power Query does not guarantee which duplicate
`Table.Distinct` retains. [Microsoft Table.Distinct documentation](https://learn.microsoft.com/en-us/powerquery-m/table-distinct)

`Placement Type` lists all available framework placement types, sorted and
distinct; it is not a Fostering constant or an eligibility test. `Home Name`, `Service Type`,
address, status and contact fields come from the actual home, not a constant
or an inferred value. Providers with mixed services retain their home service
types. Provider Town/City and Postcode remain separate from Home Town/City and
Home Postcode. Before overwrite, the notebook checks BOTH the baseline row count
and provider/home key multiset in both directions; it fails if rows are missing,
extra, substituted or multiplied. It does not silently filter/deduplicate the
baseline. Duplicate natural-key pairs also fail for source-quality review.
It is a current
directory, not a historical/as-of registry. `AS_OF_DATE` does not reconstruct
historical provider contacts or memberships.

## Export fields

The native extract table exposes 72 unaggregated columns: the original 21 plus
51 home, metric and freshness fields. Provider ID and Home ID prevent different
providers or homes with the same name from collapsing into one exported row.

| Group | Export headers |
| --- | --- |
| Provider and location | Provider ID; Provider Name; Town/City; Postcode; Provider Status; County; Country |
| Membership and service | Framework Code; Placement Type; Home Name; Service Type |
| Provider contacts | Provider Email; Provider Phone |
| Responsible individual | Responsible Individual Name; Responsible Individual Contact Number; Responsible Individual Email Address |
| Registrant | Registrant Name; Registrant Role; Registrant Email; Registrant Contact Number |
| Data freshness | Source Export Date |
| Home directory | Home ID; Home Name; Service Type; Home Status; Home Address Line 1/2; Home Town/City; Home County; Home Postcode; Home Country; Home Phone; Home Email; Home Registered Beds; Home Spot; Home Source Export Date |
| Provider/home metrics | Offers; Draft Offers; Accepted Offers; Rejected Offers; Offers With Distance; Average Offer Distance km; IPAs; Active IPAs; Provider Signed IPAs; Completed IPAs; Signature Flag; Both Signed Flag; Estimated Active Weekly Cost; Active IPAs Missing Weekly Cost; Estimated Lifetime Cost To Date; IPAs Missing Lifetime Cost (each prefixed Provider or Home) |
| Provider-only engagement | Provider Assignments; Provider Declined Assignments; Provider Messages; Provider Timed Responses; Provider Average Response Minutes |
| Metric freshness | Metrics As Of Date |

All contact numbers and identifiers are strings. The semantic model also retains
Holding Company ID, QA Flag, Framework Count and the export/run metadata as
hidden columns. Hidden columns are not included in the default export visual;
hiding a field is not an access-control mechanism.

## Metric definitions and safe totals

- **Provider** metrics cover that provider's entire available current Gold
  population, not just one home or one placement type. They repeat on every home
  row. **Do not sum provider-prefixed metrics down the extract.** Take one row
  per Provider ID for provider totals. The model declares all extract fields
  `summarizeBy: none`; no totals row is added to the visual.
- **Home** offer/IPA/cost metrics use both the provider and home key. Provider
  totals include offers without a home or with an unrecognised/mismatched home;
  these cannot be credited to an existing home. Therefore home totals need not
  equal provider totals. A no-home provider row has zero home activity metrics;
  it is not a synthetic home for unattributed offers.
- Offer, IPA, assignment, message and contact enrichments are deduplicated by natural key
  before joins/aggregation, using latest export metadata and deterministic ties.
  The two Gold dimensions are used as-is for the registry baseline, with no
  additional registry eligibility or natural-key filters.
  **Offers includes drafts**. Draft Offers is a subset. Accepted Offers uses
  `OFFER_SUCCESSFUL`, `ACCEPTED`, `APPROVED`, `SELECTED`; Rejected Offers uses
  `OFFER_UNSUCCESSFUL`, `DECLINED`, `REJECTED` (trim/case insensitive). Withdrawn
  offers are not rejection counts. Provider Declined Assignments is the separate
  source assignment `is_declined` count.
- IPAs are attributed through `fact_ipa.accepted_offer_id` to `fact_offer`.
  An IPA without a matching offer cannot be assigned to a provider/home from
  these facts and is excluded, not arbitrarily attached by referral ID. Reconcile
  such exceptions in deployment. Signature Flag means **any IPA signed by the
  provider**; Both Signed Flag means **any completed IPA signed by both parties**.
  These flags include closed IPAs; they are not framework-contract signatures.
- Provider Messages counts distinct message IDs in either direction, including
  messages with an unknown creation date but excluding known dates after the
  metric cut-off. No message text is exported. There is no home message key.
  Average Response Minutes averages non-negative observed assignment response
  minutes from `fact_referral_provider`, not averages of monthly averages. Its
  Timed Responses count is the denominator. Evidence is the first offer or
  recorded decline/cancellation reason, not reading/browsing or all messages.
- Average Offer Distance km is an **offer-weighted straight-line estimate**
  from the referral city reference point to the home postcode. Drafts are
  included, missing/invalid distances excluded. Offers With Distance gives the
  denominator. It is not a driving distance, referrer's office address, or an
  exact child address; repeated offers to the same home each contribute.
- Estimated Active Weekly Cost sums known non-negative weekly fees for
  **non-closed IPAs**, consistent with the existing report liability definition;
  it includes pending/future-start agreements and treats a missing closed flag
  as non-closed. Active IPAs Missing Weekly Cost identifies omitted fees.
- Estimated Lifetime Cost To Date uses each IPA's planned/admission start date
  and current estimated weekly fee: inclusive days through the earlier of
  recorded end date and Metrics As Of Date, divided by seven. Future starts
  contribute zero; closed placements retain their accrued estimate. Missing
  start/fee, a closed IPA without an end date, negative fees or end-before-start
  are excluded and counted in IPAs Missing Lifetime Cost. A total may be partial
  when that count is non-zero. All-missing evidence stays blank, not zero;
  genuinely no eligible IPAs means zero. No invoices, actual start dates or
  historical rate changes are available, so **this is not actual expenditure**.

The fact tables must share one as-of date. The registry checks this before
overwrite and uses that date, not today's date against stale/archive facts.
Current directory contacts and metric as-of dates can differ; inspect both.

## Deploy and refresh

The edited project is:

`C:\repos\BCT\fabric-csv-bronze-ingestion\project X\reports\WIP\SM WMPP v16 updated WIP`

1. Import the updated `00_setup_cfg.py` and `05_gold_dimensions.py` into the
   development Fabric workspace attached to `LH_BCT_WMPP`. Setup registers
   ten registry lineage entries; no new pipeline child notebook is needed.
2. Run setup, the current Silver build, `04_gold_model`, then Gold dimensions.
   The registry cell is at the end of `05_gold_dimensions`. For a registry-only
   development run, initialise its schema/run variables and `require_columns`,
   then execute that cell after Gold provider/home and framework dimensions/bridge, offer,
   IPA and assignment facts are current and have the same as-of date. Home and
   message Silver tables are now required too. The existing live pipeline already
   runs Gold facts before Gold dimensions. No archive replay or database reset
   is required for this expansion.
3. Check that `gold.rpt_provider_registry` is visible in the Lakehouse SQL
   endpoint before refreshing its semantic-model import. Compare the full row
   count and provider/home key pairs with the unfiltered dimension LEFT JOIN
   shown above, not with framework membership. The notebook performs this check
   automatically before overwrite. Check uniqueness of Provider ID / Home ID,
   not Provider ID alone. Reconcile provider/home offer and IPA totals with
   the separate facts, including unattributed records and missing cost evidence.
4. Open/reload the updated saved WIP and refresh the registry import. If Desktop
   was already open, preserve any unsaved work separately before reloading; do
   not save a stale session over the revised definitions. The earlier Gold
   journey-status replacement is superseded by separate source-status and
   journey-stage fields, agreed on 6 October 2026. Follow the
   [Gold status and journey deployment sequence](GOLD_REFERRAL_JOURNEY_STATUS.md)
   before a full-model refresh. The registry import and raw table now include
   the new home and metric columns; other report pages remain unchanged.
5. Inspect **Provider Registry Extract** in Desktop edit mode. Its three filters
   are Provider Name, Provider Status and Town/City. Scroll the table horizontally
   to inspect the remaining contacts. Filters on this isolated page control its
   extract; Explorer offer/journey filters do not implicitly restrict it.

The model imports the new Gold table directly through the existing SQL endpoint.
There are no staging-query dependencies, duplicate legacy extract, offer-driven
relationships or new bidirectional filters. Existing dashboard visuals, sidebar navigation,
bookmarks, relationships and reader-role rules for other tables are unchanged.

The scoped installer is `tools/add_wmpp_provider_registry_extract.py`; preview
is default and `--apply` creates a backup before changing saved definitions.
It refuses to overwrite manually changed registry definitions or an unrecognised
security role. The WIP folder is Git-ignored, so commit the notebook, template,
installer and this guide to retain a reproducible implementation.

For an existing registry, use the separate `--expand-registry` preview. It adds
only missing columns to the existing import and native table plus the known
grain description; it preserves the connection, old lineage tags, positions,
styles, roles, report export settings and other pages. It refuses unsupported
custom selections/aggregated export fields rather than replacing them. The
backed-up expansion touched exactly three WIP files. Backup:
`reports/WIP/_review/registry-home-metrics-20261006-165955`.

## Generate the file

In Desktop edit mode, open **Provider Registry Extract**, choose the filters,
and use the table's **… → Export data** menu. Use **Summarized data** where that
choice is offered. All 72 export fields are columns on this table, so underlying
data export is unnecessary. Current filters carry into the exported rows.

Desktop exports CSV. The Power BI service also offers Excel export where report,
tenant and permission policies permit it. CSV exports have a 30,000-row limit;
Excel exports have a 150,000-row ceiling and may have lower visual/query limits.
If export is disabled or the result exceeds the applicable limit, resolve that
with the report administrator; do not bypass it. [Microsoft export documentation](https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data)

For CSV, import through Excel's Data import and set phone, postcode and identifier
columns to Text. Opening CSV directly can let Excel reinterpret leading zeros.
Verify that the exported row count, filters and headers match the intended
selection, then store and share the contact file only in an approved location.

## Contact access

The user subsequently named **wmpp_report_users** for ordinary dashboard
readers and **wmpp_provider_registry_users** for registry viewers/exporters.
This group-based setup supersedes the earlier two-email approval on 6 October.
The saved WIP no longer hard-codes `akhtar@bham.co.uk` or `hamanat@bham.co.uk`
as contact-access exceptions. Include them in the registry group if they should
retain access. Group membership must be configured and verified in Microsoft
Entra/Fabric; this local change does not create groups or change their members.

| Existing security group | Assign to this model role | Registry data |
| --- | --- | --- |
| `wmpp_report_users` | `WMPP Dynamic Detail RLS` | No registry rows (`FALSE ()`) |
| `wmpp_provider_registry_users` | `WMPP Provider Registry RLS` | Complete provider/home registry rows (`TRUE ()`) |

The registry role copies **every other table predicate** from the ordinary
reader role. Referral, snapshot, identity-scope and provider-scoring rules are
identical, so overlapping group membership does not widen those permissions.
This is not an unrestricted contact-only role. Changing a detail rule in future
requires updating and validating both roles together; the installer refuses
drift rather than silently copying a changed rule over an existing role.

The new registry metrics are precomputed provider/home aggregates across the
available Gold facts, not dynamically limited by the viewer's referral scope
or Explorer filters. The registry audience can therefore see these provider
performance/cost totals even where it cannot see individual referrals. This
is part of the requested extract expansion; review that aggregate audience and
small-cell disclosure before publication. No referral ID, child detail or
message body is added. Existing other-table predicates remain unchanged.

The role's `WMPP_ServiceGroup` annotation is a handover label only. It does not
resolve group membership or grant access. The service role assignments below
are required. Existing user-to-referral-scope mappings are still needed for
secured dashboard detail; joining either group does not populate those mappings.
Use Microsoft Entra **security groups**, not Microsoft 365 groups. Review
external guests with actual service identities before relying on group access.

The registry page is now unhidden, without moving visuals or changing the
existing sidebar. Its page tab is shared navigation, not a per-user security
boundary: an unapproved ordinary reader can reach the page but gets no registry
data. Workspace Admins, Members and Contributors can bypass model RLS, so this
setup does not restrict those editors. Review every additional role and direct
SQL/Lakehouse access separately before production release.
[Microsoft RLS documentation](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)

No live publication, account/group membership, database permissions or tenant
export settings have been changed. The saved report still has
`exportDataMode: None`; exports are deliberately **not enabled yet**. The existing
registry import has user edits and was preserved. The group follow-up changed
only the ordinary role's registry rule/handover annotation, added its scoped
registry-role counterpart and registered that role in `model.tmdl`. Report
visuals, navigation, layout, bookmarks and imports did not change. Backups:
`reports/WIP/_review/registry-groups-20261006-162157`. The earlier page-visibility
and access-note change remains backed up in
`reports/WIP/_review/registry-access-20261006-154319`.

### Simple handover steps

1. Publish the reviewed, refreshed WIP report and semantic model to the intended
   controlled workspace. Publishing has not been performed by this local edit.
2. In Fabric, select the semantic model's **… → Security**. Add
   **wmpp_report_users** to **WMPP Dynamic Detail RLS** and
   **wmpp_provider_registry_users** to **WMPP Provider Registry RLS**.
   Give both groups report/app read access (or workspace **Viewer** if needed),
   not editing roles. Do not assign the ordinary report group to the registry
   role. Review direct registry-role assignments too: role membership, not its
   annotation, controls access. This change has not removed existing service
   memberships or changed the approved referral-scope mappings.
3. Ask the Fabric administrator to review the **Export to Excel** and
   **Export to .csv** tenant settings and restrict the export feature to the
   **wmpp_provider_registry_users** security group, not **wmpp_report_users**.
   "Provider Registry Exporters" was only an earlier suggested name; use the
   actual group above. Verify existing tenant-policy inclusions/exclusions.
   These tenant settings affect other reports, so do not replace the
   organisation's existing export policy without checking the wider impact.
4. Only after the export restriction is effective, allow **summarized data**
   in the report's export settings. The registry table already contains all
   required columns; underlying-data export and extra Build rights are not
   needed for this extract. Report export settings are report-wide, not a
   registry-only permission. If changing the tenant policy would disrupt other
   reports, use a separately restricted extract report instead; that alternative
   has not been created in this change.
5. Test real Viewers in the report group only, registry group only, both groups
   and neither group. Registry-group members must see/export the expected
   filtered registry rows once export controls are enabled; report-only readers
   must see no registry rows. Referral/scoring detail must match the same user's
   approved scope in either role and when both roles apply. An unmapped user
   must not gain referral detail through registry membership. Do not use an
   administrator account as the security test.

Tenant export switches govern export features, not the underlying permission
to read/query data; they are not a substitute for the registry row rule.
[Microsoft export settings](https://learn.microsoft.com/en-us/fabric/admin/service-admin-portal-export-sharing),
[tenant-setting limitations](https://learn.microsoft.com/en-us/fabric/admin/about-tenant-settings).

Do not infer contact permission from `allows_global_summary`: this is an
identifiable contact directory, not an identifier-free aggregate.

For reproducibility, the installer still denies registry rows by default.
An explicit group-access preview for the already installed WIP is:

```powershell
python "project X/tools/add_wmpp_provider_registry_extract.py" --access-only --report-group wmpp_report_users --registry-group wmpp_provider_registry_users
```

Add `--apply` only for an approved, backed-up reapplication. Access-only
group mode edits only the scoped roles and their model reference. Unknown roles,
an unrecognised reader predicate or mismatched existing group-role filters stop
the operation for review. The older `--registry-user` mode intentionally refuses
a project with this second role; do not use it to revert group access silently.
The local WIP remains Git-ignored; preserve it and its backup separately.

## Acceptance checks

- Registry row count and key multiset exactly match unfiltered `dim_provider`
  LEFT `dim_provider_home`; no missing or extra rows. No duplicate Provider ID /
  Home ID combinations unless the baseline itself contains an invalid duplicate,
  which stops the build for source-quality review rather than dropping a row.
- Providers without offers, homes, framework membership or contact evidence
  remain present. Residential-only, inactive/closed and unknown-framework
  providers remain present when they occur in `dim_provider`.
- Multiple framework codes are retained once each in stable order.
- Current contacts match Silver; missing contacts remain blank; phone numbers
  keep leading zeros.
- All 72 headers appear in a small authorized export and filters match the file.
- Provider totals are repeated, not multiplied by the home count; home offer/IPA
  totals reconcile to properly attributed facts. Messages remain provider-only.
  Check signatures, separate offer rejections/assignment declines, response and
  distance denominators, and lifetime estimates on active/closed/future IPAs.
- Cost totals remain blank if evidence is wholly missing; partial estimates
  have non-zero missing-evidence counts. Metrics As Of Date matches the Gold
  fact refresh, including an archive run, rather than blindly using today.
- **WMPP Dynamic Detail RLS** denies registry rows;
  **WMPP Provider Registry RLS** permits registry rows. Both roles, separately
  and together, retain identical authorised referral/scoring results for the
  same mapped identity. Confirm actual group assignments with real service
  Viewers as well as Desktop's **View as**.

Local verification passed 248 tests and 158 subtests, including 17 new synthetic
registry and safe-edit checks. Tool/test lint and the Gold notebook contract
validator passed. These do not establish Fabric execution, actual data counts,
Power BI rendering or export permissions.

The subsequent audience change passes 26 focused synthetic ETL/safe-edit checks,
including explicit-audience validation and preservation of edited imports and
page layout; the full local suite passes **288 tests and 158 subtests**.
Those checks do not execute Power BI's DAX security engine or prove
published role membership, sign-in resolution, native rendering or export.

The subsequent group-based change passes **296 tests and 158 subtests**,
including 34 focused registry ETL/safe-edit checks. The six non-registry table
predicates match in both saved roles. Group preview plans no further edits;
hashes confirm all 2,733 unlisted project files unchanged, excluding `.pbi`.
These are local file/logic checks, not native DAX or live group/export acceptance.

The provider/home expansion passes **306 tests and 158 subtests**, including
44 focused registry checks and the Gold-dimensions/configuration validators.
An expansion preview is idempotent. These checks use synthetic data and saved
definitions; Fabric SQL/Delta execution, native rendering and service exports
still require the deployment checks above. No live data refresh or publication
was performed.

The complete-directory correction on **7 October 2026** passes **313 tests and
158 subtests**, including 51 focused registry checks and both notebook/config
validators. The actual generated SQL retains every row/key in a synthetic
1,002-row dimension left join; the old filter returned only 3 rows. These are
local checks, not observed production counts.

The saved WIP now has 78 registry model columns and all 72 raw export fields.
The expansion preview is idempotent. The source connection, existing lineage,
visual positions/styles and security/export files are preserved; hashes confirm
all 2,732 unlisted project files unchanged, excluding `.pbi`. Recovery backup:
`reports/WIP/_review/registry-complete-baseline-20261007-a681f71c`.

After deploying the updated notebooks, compare unfiltered SQL endpoint counts:

```sql
SELECT COUNT(*) AS expected_registry_rows
FROM gold.dim_provider a
LEFT OUTER JOIN gold.dim_provider_home b ON a.provider_id = b.provider_id;

SELECT COUNT(*) AS actual_registry_rows
FROM gold.rpt_provider_registry;
```

Both counts must be identical. The notebook additionally validates the complete
provider/home key multiset, because equal counts alone could hide different rows.
Then refresh the report's registry import; report filters and existing security
can still legitimately reduce what a viewer sees. No live Fabric run or
publication was performed as part of this correction.
