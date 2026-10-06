# Provider registry extract

Updated 5 October 2026. GLD-023 now has one Fostering provider registry from
the Gold notebook through to the saved WIP semantic model and an export table.
The source implementation is ready; Fabric execution, data refresh and Desktop
rendering still require deployment verification. No live contact file has been
generated or published.

## Extract scope

Both supplied legacy queries are identical and select Fostering providers. Their
replacement is `gold.rpt_provider_registry`, with one current row per
`provider_id`. A provider needs a Fostering framework membership, but does not
need an offer, referral assignment, message or registered home. Other placement
types and providers without a qualifying framework are outside this extract.

`05_gold_dimensions.py` reads current provider fields and contacts from
`silver.provider`, then joins current memberships from
`gold.bridge_provider_framework` to `gold.dim_framework`. Duplicate links do
not multiply provider rows. Where one membership ID appears in several exports,
the latest version wins. Framework placement types are compared without casing
or surrounding-space differences.

Provider records are ordered by source `export_date`, then `_silver_load_ts`.
Equal timestamps use a stable ordering of all output provider fields, rather
than selecting an arbitrary contact record. NULL contacts remain NULL; an older
email is not substituted for a missing current email. Missing required columns
fail the registry build before its existing table is overwritten.

`Framework Code` contains all distinct qualifying codes, sorted and separated
by `; `. This deliberately replaces the old arbitrary choice of one framework
after sorting and deduplication. Power Query does not guarantee which duplicate
`Table.Distinct` retains. [Microsoft Table.Distinct documentation](https://learn.microsoft.com/en-us/powerquery-m/table-distinct)

`Placement Type` and `Service Type` are both `Fostering`. `Home Name` is `N/A`,
as in the legacy queries: this is not a provider-home extract. It is a current
directory, not a historical/as-of registry. `AS_OF_DATE` does not reconstruct
historical provider contacts or memberships.

## Export fields

The table exposes all 16 explicitly named legacy fields plus the provider key,
provider status, county, country and source export date. Provider ID prevents
different providers with the same name from collapsing into one exported row.

| Group | Export headers |
| --- | --- |
| Provider and location | Provider ID; Provider Name; Town/City; Postcode; Provider Status; County; Country |
| Membership and service | Framework Code; Placement Type; Home Name; Service Type |
| Provider contacts | Provider Email; Provider Phone |
| Responsible individual | Responsible Individual Name; Responsible Individual Contact Number; Responsible Individual Email Address |
| Registrant | Registrant Name; Registrant Role; Registrant Email; Registrant Contact Number |
| Data freshness | Source Export Date |

All contact numbers and identifiers are strings. The semantic model also retains
Holding Company ID, QA Flag, Framework Count and the export/run metadata as
hidden columns. Hidden columns are not included in the default export visual;
hiding a field is not an access-control mechanism.

## Deploy and refresh

The edited project is:

`C:\repos\BCT\fabric-csv-bronze-ingestion\project X\reports\WIP\SM WMPP v16 updated WIP`

1. Import the updated `00_setup_cfg.py` and `05_gold_dimensions.py` into the
   development Fabric workspace attached to `LH_BCT_WMPP`. Setup registers
   three registry lineage entries; no new pipeline child notebook is needed.
2. Run the existing setup and Gold-dimensions steps against current Silver data.
   The registry cell is at the end of `05_gold_dimensions`. For a registry-only
   development run, initialise its schema/run variables and `require_columns`,
   then execute that cell after the existing Gold framework dimension and bridge
   are current. No `04_gold_model` or archive replay is required for GLD-023.
3. Check that `gold.rpt_provider_registry` is visible in the Lakehouse SQL
   endpoint before refreshing its semantic-model import. Reconcile the provider
   count with the distinct provider IDs having Fostering framework memberships.
4. Open/reload the updated saved WIP and refresh the registry import. If Desktop
   was already open, preserve any unsaved work separately before reloading; do
   not save a stale session over the revised definitions. The earlier Gold
   journey-status replacement is superseded by separate source-status and
   journey-stage fields, agreed on 6 October 2026. Follow the
   [Gold status and journey deployment sequence](GOLD_REFERRAL_JOURNEY_STATUS.md)
   before a full-model refresh. The provider registry implementation is unchanged.
5. Inspect **Provider Registry Extract** in Desktop edit mode. Its three filters
   are Provider Name, Provider Status and Town/City. Scroll the table horizontally
   to inspect the remaining contacts. Filters on this isolated page control its
   extract; Explorer offer/journey filters do not implicitly restrict it.

The model imports the new Gold table directly through the existing SQL endpoint.
There are no staging-query dependencies, duplicate fostering query, offer-driven
relationships or new bidirectional filters. Existing page visuals, navigation,
bookmarks, relationships and reader-role rules for other tables are unchanged.

The scoped installer is `tools/add_wmpp_provider_registry_extract.py`; preview
is default and `--apply` creates a backup before changing saved definitions.
It refuses to overwrite manually changed registry definitions or an unrecognised
security role. The WIP folder is Git-ignored, so commit the notebook, template,
installer and this guide to retain a reproducible implementation.

## Generate the file

In Desktop edit mode, open **Provider Registry Extract**, choose the filters,
and use the table's **… → Export data** menu. Use **Summarized data** where that
choice is offered. All 21 export fields are columns on this table, so underlying
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

The audience for the new contacts has not yet been approved. The saved WIP adds
`tablePermission rpt_provider_registry = FALSE ()` to **WMPP Dynamic Detail RLS**.
Readers using that role receive no registry rows, while its existing referral
and scoring rules remain unchanged. No new role, membership, UPN approval,
Lakehouse permission, publication or export-policy change has been made.

The export page is hidden in reading view and omitted from the existing sidebar.
Hiding alone does not secure contacts. Workspace Admins, Members and Contributors
can bypass model RLS; the deny rule is not a way to restrict those editors.
Validate the intended Viewer role and review every additional role before a
production release. SQL endpoint/Lakehouse access must be reviewed separately
because semantic-model RLS does not govern direct database access.
[Microsoft RLS documentation](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)

Do not infer permission to see contacts from `allows_global_summary`: this is
an identifiable contact directory, not an identifier-free aggregate. If report
readers also need the extract, agree the audience and provider-scope policy before
replacing the deny rule or adding reader navigation.

## Acceptance checks

- No duplicate Provider IDs; counts match the qualifying membership population.
- A qualifying provider with no offers is present; a Residential-only provider
  and a provider without Fostering membership are absent.
- Multiple framework codes are retained once each in stable order.
- Current contacts match Silver; missing contacts remain blank; phone numbers
  keep leading zeros.
- All 21 headers appear in a small authorized export and filters match the file.
- **View as WMPP Dynamic Detail RLS** returns no registry rows without changing
  the existing report's authorized referral/scoring results.

Local verification passed 248 tests and 158 subtests, including 17 new synthetic
registry and safe-edit checks. Tool/test lint and the Gold notebook contract
validator passed. These do not establish Fabric execution, actual data counts,
Power BI rendering or export permissions.
