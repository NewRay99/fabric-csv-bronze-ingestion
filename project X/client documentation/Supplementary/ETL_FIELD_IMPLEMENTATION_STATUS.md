# ETL field implementation status

## Bronze-to-Silver field mapping

The latest Silver formatter uses the approved schema contract as its mapping
specification. `bronze.referral` is a representative example: its contracted
fields retain their names in `silver.referral`, are cast to their declared
types, and are deduplicated by `referral_id` within the newest `export_date`.
Only approved contract fields are materialised; missing and extra fields are
recorded as schema drift. The formatter then appends Silver lineage columns,
not the Bronze ingestion columns. The detailed rule and field groups are in the
[technical design](../03_Architecture_and_Design/TFD.md#worked-example-bronzereferral-to-silverreferral).

## Implemented from available data

- The Gold referral fact provides referral-created, required-placement, first-action, first-offer, accepted-offer, IPA, last-activity, offer-count and urgency fields.
- The Gold dimensions notebook creates date, provider, holding-company, provider-home, framework, framework-category, placement-type and referral-status dimensions, plus provider-framework and provider-SIC bridges.
- `provider_submission_docs`, `provider_sic_codes`, `referral_person_support_needs`, `mlv_additional_fee` and the Bronze `ref_*` reference tables are now contracted so the Silver formatter materialises them rather than skipping them.

## Not source-backed yet

A true referral closure reason, reopen date, status-change history, and placement end/breakdown fields are not in the available Bronze contract. They must be supplied by the source system before becoming Gold facts or dimensions. The referral lifecycle event table remains a declared derivation from real Referral, Offer and IPA timestamps; it is not an audit log.

## Adding a field safely

1. Confirm the field and type in the Bronze schema-capture/drift output.
2. Add it to `configuration/schema_definition.csv` with its real source name, type and evidence-backed join metadata.
3. Run setup, then the applicable Silver formatter; inspect `monitoring.cfg_schema_drift_event`.
4. Add it to a Gold fact or dimension only after the Silver table and data-quality checks succeed.
5. Update the Gold source preflight, test and reporting documentation whenever the new field is mandatory.
