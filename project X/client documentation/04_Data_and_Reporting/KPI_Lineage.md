# KPI lineage — active Gold semantic model

## Purpose and status

This is the maintained lineage record for the active referral reporting model.
It replaces the implementation role previously inferred from the initial
assessment documents. It maps functional requirements to the deployed KPI
families, their DAX calculations and the Bronze-to-Gold transformations that
support them.

Read this with [KPI Reference Guide](KPI_Reference_Guide.md), which is the
business definition and Gold-table reference, and [Gold Semantic Model DAX
Build Guide](GOLD_SEMANTIC_MODEL_DAX_BUILD_GUIDE.md), which contains the
copy-ready DAX library.

The current Dashboard Legend catalogue contains 109 publishable measures:
108 **Ready** and one **Gold lifecycle-event proxy**. Its ten `GOLD-GAP-*`
rows are explicitly not publishable KPIs until the required Gold fields or
facts have been added.

## Publishing rule

Every published KPI DAX expression must use fields from an active Gold fact,
dimension or bridge imported into the semantic model. Bronze and Silver are
lineage and transformation layers only; they are never valid KPI DAX sources.
The static regression check `tests/validate_gold_dax_guide.py` enforces this
for the published DAX blocks.

## End-to-end data path

```text
Source extract <logical_table>.csv
  → schema_definition.csv contract and cfg extract configuration
  → Bronze table <logical_table>
  → silver.<logical_table> (type conformance and schema checks)
  → derived Silver enrichment / lifecycle relations where needed
  → gold.fact_* / gold.dim_* / gold.bridge_* materialised tables
  → Power BI semantic model
  → Gold-only DAX measure
```

| Stage | Implementing asset | Control or transformation |
| --- | --- | --- |
| Source contract | `configuration/schema_definition.csv`; configured extract files | Defines logical table, expected fields and types. |
| Bronze capture | `01_bronze_get_latest.ipynb`; archive load/replay notebooks | Stores the source extract with ingestion and export context. |
| Silver conformance | `02_silver_formatter.ipynb`; `02a_archive_silver.ipynb` | Applies the schema contract, data types and replayable Silver tables. |
| Business rules | `03_silver_business_rules.ipynb` | Creates `silver.referral_enrichment` and `silver.referral_lifecycle_event`; applies derived-date and DQ rules. |
| Gold facts | `04_gold_model.ipynb` | Materialises referral, snapshot, offer, IPA, referral-provider and lifecycle facts. |
| Gold dimensions | `05_gold_dimensions.ipynb` | Materialises provider, home, framework, document, date and lookup/bridge tables. |
| Semantic/DAX | Power BI model; DAX build guide | Imports active Gold objects and evaluates the published measures. |

## Source-to-Gold lineage

| Functional subject | Source extract / Bronze table | Silver relation and manipulation | Active Gold object / fields | KPI families enabled |
| --- | --- | --- | --- | --- |
| Referral state and dates | `referral.csv` → `bronze.referral` | `silver.referral`; `03_silver_business_rules.ipynb` derives lifecycle dates, open state, offer indicators, ageing, target outcome and cost enrichment | `fact_referral`, `fact_referral_snapshot`; fields including `referral_created_date`, `required_placement_date`, `ipa_issued_date`, `is_open`, `estimated_weekly_cost` | Referral performance, snapshot, time, target and confirmed-cost KPIs |
| Child linkage | `referral_person.csv` → `bronze.referral_person` | `silver.referral_person`; one child identifier selected per referral for the current referral fact | `fact_referral[child_id]` | Referral linkage only; demographic KPIs remain a Gold gap |
| Provider assignment | `referral_provider.csv` → `bronze.referral_provider` | `silver.referral_provider`; joins offers and supports enrichment/provider-observation calculations | `fact_referral_provider`; `fact_offer[referral_id, provider_id]` | Assignment, engagement, decline and provider-performance KPIs |
| Offer activity | `offer.csv` → `bronze.offer` | `silver.offer`; offer dates/statuses contribute to `silver.referral_enrichment`; Gold joins each offer to its provider assignment | `fact_offer` | Offer submission, decision, acceptance, draft/pending ageing, cost and rejection-reason KPIs |
| IPA/placement activity | `ipa.csv` → `bronze.ipa` | `silver.ipa`; IPA dates and costs contribute to referral enrichment | `fct_ipa`; referral IPA fields in `fact_referral` | IPA volume, conversion, placement status, weekly estimated cost and target KPIs |
| Lifecycle/message activity | Referral, offer and IPA change data; `referral_provider_message.csv` where delivered | `silver.referral_lifecycle_event` is a derived roll-up. A provider message adds the `ProviderMessageSent` event only when the message source is available. | `fact_referral_lifecycle_event[event_id, referral_id, event_type, event_timestamp]` | Lifecycle activity and message-volume proxy KPI |
| Provider, home and holding company | `holding_company.csv`, `provider.csv`, `provider_home.csv` | Corresponding Silver tables are conformed without KPI aggregation | `dim_holding_company`, `dim_provider`, `dim_provider_home` | Provider/home register, service-type, QA flag and onboarding KPIs |
| Framework reference and membership | `framework.csv`, `framework_category.csv`, `provider_framework.csv`, `provider_sic_codes.csv` | Corresponding Silver tables are conformed; membership is retained as a bridge | `dim_framework`, `dim_framework_category`, `bridge_provider_framework`, `bridge_provider_sic_code` | Framework coverage and provider framework KPIs |
| Provider documents | `provider_submission_docs.csv` → `bronze.provider_submission_docs` | `silver.provider_submission_docs`; document dates also support due-diligence warnings | `dim_provider_submission_document` | Expiring/expired-document KPIs |

## Requirement-to-KPI lineage

The following is the maintained functional-requirement mapping. A requirement
is shown as **partial** where the current Gold model provides a safe proxy but
does not meet the original detailed requirement.

| Functional requirement | Current Gold KPI / KPI family | Gold source | Status and boundary |
| --- | --- | --- | --- |
| R13 | `Closed Referrals`, `Closed Referrals at Snapshot` | `fact_referral`, `fact_referral_snapshot` | Ready. |
| R14 | `Provider Messages Sent` | `fact_referral_lifecycle_event[event_type]` | Partial: message-volume proxy only; not response-time or unread-message reporting. |
| R18, R57 | Placement target, emergency and planned-referral measures | `fact_referral` | Ready for the current urgency-based referral definition; do not infer an unprovided statutory emergency flag. |
| R20 | `Referral Lifecycle Events` | `fact_referral_lifecycle_event` | Ready for activity count; IPA signature is still a referral-level proxy. |
| R22 | `Referrals With Multiple Provider Assignments` | `fact_referral_provider` | Partial: no referral-level out-of-region field. |
| R24, R26, R36 | Referral status, unattended/awaiting offer, provider assignment and offer measures | `fact_referral`, `fact_referral_provider`, `fact_offer` | Ready. |
| R25–R29 | Offer submitted, decision, accepted/unsuccessful and provider offer measures | `fact_offer`, `fact_referral_provider` | Ready. |
| R35 | IPA issue, conversion, active/closed IPA and time-to-IPA measures | `fct_ipa`, `fact_offer`, `fact_referral` | Ready except detailed IPA-signature KPIs. |
| R41 | `Providers With QA Flags` | `dim_provider`, `dim_provider_home` | Partial: no historical QA flag-type fact. |
| R46, R67 | Framework provider measures | `bridge_provider_framework`, `dim_provider` | Ready. |
| R47, R48 | Document expiry measures | `dim_provider_submission_document` | Ready for expiry; no expected-document set or blocking outcome. |
| R51, R52 | Referral volume, offer, snapshot and current-year measures | `fact_referral`, `fact_referral_snapshot` | Ready. |
| R54 | Provider decline and decline-rate measures | `fact_referral_provider` | Ready for delivered assignment decline flags; referral-level decline reason remains a gap. |
| R59 | Provider onboarding measures | `dim_provider` | Ready for provider-status proxy. |
| R62 | Estimated weekly cost, active cost and confirmed-referral average cost | `fact_referral`, `fct_ipa` | Ready for estimates only; payment/invoice reporting remains a gap. |
| R82 | `Gold Model Last Refreshed` | `fact_referral[gold_modelled_at]` | Ready. |
| R91, R93 | Provider/home-register measures | `dim_provider`, `dim_provider_home` | Ready. |

Measures whose Dashboard Legend requirement ID is `—` are still valid Gold
operational measures, but have not yet been formally linked to a functional
requirement. They must not be counted as requirement coverage until that
mapping is agreed and added to the catalogue.

## Published KPI families

The Dashboard Legend is the detailed measure index; the table below groups
every active Gold KPI by its DAX source and lineage path.

| KPI family | Gold KPI IDs | Gold DAX source | Upstream source path |
| --- | --- | --- | --- |
| Referral performance | `GOLD-KPI-001`–`013` (non-contiguous) | `fact_referral` | `referral` → Silver referral/enrichment → `fact_referral` |
| Offer, provider and IPA | `GOLD-KPI-012`, `014`–`023` | `fact_offer`, `fct_ipa`, `fact_referral`, lifecycle fact | offer/referral-provider/IPA → Silver conformance/enrichment → Gold facts |
| Confirmed-referral cost | `GOLD-KPI-024` | `fact_referral[ipa_issued_date, estimated_weekly_cost]` | referral + linked IPA → Silver enrichment → referral fact |
| Provider engagement | `GOLD-KPI-025`–`027`, `051` | `fact_referral_provider`, `dim_provider` | referral-provider → Silver referral provider → Gold fact/dimension |
| Referral snapshot | `GOLD-KPI-028`–`035` | `fact_referral_snapshot` | Gold referral fact snapshot materialisation |
| Referral/provider trends | `GOLD-KPI-036`–`050` | `fact_referral`, `fact_referral_provider` | referral/referral-provider → Silver enrichment → Gold facts |
| Offer portfolio and ageing | `GOLD-KPI-052`–`075` | `fact_offer`, `dim_provider_home`, `dim_provider` | offer/referral-provider/provider/home → Silver → Gold facts/dimensions |
| Provider, framework and documents | `GOLD-KPI-076`–`094` | provider/home/framework/document dimensions and bridge | provider, home, framework and document extracts → Silver → Gold dimensions/bridge |
| IPA, cost and lifecycle | `GOLD-KPI-095`–`108` | `fct_ipa`, `fact_offer`, `fact_referral`, lifecycle fact | IPA/offer/referral/lifecycle roll-up → Silver → Gold facts |
| Message volume | `GOLD-KPI-109` | `fact_referral_lifecycle_event[event_type]` | provider-message event → Silver lifecycle roll-up → Gold event fact |

## Non-publishable roadmap items

The following Dashboard Legend rows describe genuine model gaps, not DAX work
to be completed against Bronze or Silver: child demographics; IPA-grain
signature detail; referral geography; QA flag history; document compliance and
blocking outcome; referral-level decline reason; framework change history;
payment/invoice facts; detailed message-status facts; and referral category /
support-needs analysis.

See the **Gold Source Coverage** sheet in `configuration/Dashboard Legend.xlsx`
for the required additional source or Gold object for each gap. The rule is
simple: promote and validate the field in Gold first, then publish its DAX.

## Validation and maintenance

When a new KPI is requested:

1. Identify its functional requirement ID and record it in Dashboard Legend.
2. Confirm the data exists in the source contract and specify the source file.
3. Record every Bronze-to-Silver transformation and DQ condition.
4. Materialise the required Gold field/fact/dimension with lower-case
   `snake_case` columns.
5. Add Gold-only DAX to the DAX build guide and the Dashboard Legend catalogue.
6. Update this lineage record, then run `python -m pytest`.

This document records static implementation lineage. It does not prove live
Lakehouse data completeness; use monitoring and data-quality outputs to verify
each deployed run.
