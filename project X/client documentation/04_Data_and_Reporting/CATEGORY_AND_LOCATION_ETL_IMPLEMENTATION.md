# Category links and approximate location distances

Implementation date: 25 September 2026. Scope: active Python ETL notebooks, not
versioned Power BI projects. Local regression tests use synthetic records; they
do not establish that these changes have executed in the client Lakehouse.

## Category contract

| Output | Meaning |
| --- | --- |
| `gold.fact_offer.framework_category_id` | Provider's proposed category, directly from `silver.offer.category`. |
| `gold.fact_offer.provider_home_framework_category_id` | Actual home category from `silver.provider_home_category`, populated only when there is exactly one distinct category. |
| `gold.fact_offer.provider_home_framework_category_count` | Number of distinct home categories; zero for no link, greater than one for multiple memberships. |
| `gold.fact_referral.framework_category_id` | Referral category from `silver.referral_category`, populated only for a single distinct category. |
| `gold.fact_referral.framework_category_count` | Number of distinct referral categories, including multi-category referrals. |
| `gold.fact_offer.provider_home_id` | Renamed from `home_id`; the old alias is removed, not duplicated. |

Never substitute an arbitrary minimum category for a multi-category referral or
home. Full membership is available through
`gold.bridge_referral_framework_category` and the existing
`gold.bridge_provider_home_framework_category`. Their relationship grains are
`referral_id + framework_category_id` and
`provider_home_id + framework_category_id`. Duplicate links with different export
metadata are reduced to the latest link. Use distinct referral/offer counts when
analysing many-to-many categories; do not sum exploded fact rows.

New spot bridges retain the source field names and source IDs:

- `gold.bridge_provider_home_spot_category`: `provider_home_spot_category_id`,
  `provider_home_id`, `spot_category_code`.
- `gold.bridge_referral_spot_category`: `referral_spot_category_id`, `referral_id`,
  `spot_category`.

Both also retain export metadata and job correlation. Spot codes are not assumed
to be framework category IDs. Missing dimension keys are not silently discarded
by the new joins; existing source foreign-key DQ rules still apply.

These are categories in the supplied Silver state, not proof of the category at
initial creation or at the instant an offer was submitted. That claim would need
effective-dated source history. Referral snapshots retain the single category key,
count and location flags for the rebuilt month. Bridges are current-state only;
do not use them to assert historical category membership. Older retained snapshot
months keep nulls for the newly added fields until deliberately rebuilt.

## Location contract and privacy

`03_silver_business_rules` accepts `DEFAULT_LOCATION_CITY = "Birmingham"`.
The live and archive runners forward this parameter. The conformed source
`silver.referral.location_preference_details` is not overwritten.

The new `silver.referral_location` holds one row per referral. Its `location`,
`location_match_status`, `location_is_default` and `location_requires_review`
fields flow to `gold.fact_referral` and its snapshots. Coordinate provenance is
retained in Silver and on offers. The matching uses explicit whole place names,
a small documented-in-code locality list, Birmingham abbreviations, and any
additional city names loaded into the approved reference table. It is deliberately
not a general address parser: districts, unrecognised spellings, rural descriptions
and other text require review rather than being treated as verified addresses.

| Match status | Interpretation |
| --- | --- |
| `CITY_MATCH` | One recognised place name; still a generalised preference, not a verified child address. |
| `DEFAULT_MISSING` | Blank/missing source text; explicit default city, not observed location. |
| `DEFAULT_REVIEW_EXCLUSION` | Negative/exclusion language; default label only, distance suppressed. |
| `DEFAULT_REVIEW_MULTIPLE` | Multiple cities or alternative-location language; distance suppressed. |
| `DEFAULT_REVIEW_UNRECOGNISED` | No reliable match; default label only, distance suppressed. |

Do not interpret a city mentioned in preference text as the child's actual home.
The conservative rules can flag valid text for review. Review the classification
with the client before using it for decisions. No referral text is sent to a web
service or geocoder, or copied into the new derived outputs/logs.

## Approved coordinate reference

`00_setup_cfg` creates but does not populate or replace
`monitoring.cfg_location_coordinate`:

| Column | Required content |
| --- | --- |
| `location_type` | `CITY` or `POSTCODE`. |
| `location_key` | Canonical city/locality name, or provider-home postcode. |
| `latitude`, `longitude` | Approved WGS84 decimal-degree coordinates; both null or both present, within ±90/±180. |
| `reference_source`, `reference_version` | Mandatory nonblank provenance when coordinates are present. |

Load a licensed, client-approved reference locally. City coordinates should be
documented centroids and postcode coordinates documented postcode representative
points. City keys match case-insensitively; postcode keys ignore whitespace and
case. City-only rows with null coordinates can extend the place-name catalogue
without inventing locations. Exact duplicate rows collapse; conflicting normalised
keys, invalid coordinates or missing coordinate provenance fail validation before
joining. The city catalogue is limited to 10,000 names.

The new `silver.provider_home_location` joins each latest provider-home postcode
to that reference. An empty/missing coordinate reference is supported and yields
null coordinates. No coordinates are bundled with this change.

## Offer distance

`gold.fact_offer.referral_to_home_distance_km` uses the haversine formula and mean
Earth radius 6,371.0088 km. This is approximate city-centroid-to-postcode
straight-line distance, **not road distance, travel time or actual child-to-home
distance**. `referral_to_home_distance_basis` explicitly records
`CITY_CENTROID_TO_POSTCODE_STRAIGHT_LINE`.

`referral_to_home_distance_status` distinguishes `APPROXIMATE_PREFERENCE_CITY`,
`APPROXIMATE_DEFAULT_CITY`, `LOCATION_REQUIRES_REVIEW`,
`MISSING_REFERRAL_LOCATION`, `MISSING_CITY_COORDINATES` and
`MISSING_HOME_COORDINATES`. Only the first two can produce a distance. Never
replace missing distances with zero, and show default-derived results separately
from preference-derived results. Source/version fields for both endpoints remain
on the offer for audit. No precise coordinates are added to the referral fact.

## Deployment and outstanding work

1. Import the changed active notebooks, including both runners and Archive Silver.
   Run `00_setup_cfg` to create the reference schema. Load approved coordinates
   if distance values are required; empty data otherwise remains valid.
2. Run the normal conformed Silver load, then `03_silver_business_rules`,
   `04_gold_model`, and `05_gold_dimensions` in that order. Gold now requires the
   two derived location tables. Publish the notebooks together, not Gold alone.
3. In a development Lakehouse, confirm unique referral/offer keys, category
   memberships, row counts, null/review rates and a sample of known distances.
   Native Fabric/Delta execution has not been performed from this workstation.
4. Obtain client approval of the matching/default rules and coordinate licence,
   provenance and version. Pin the reference version for reproducible archive
   replays: the current table is not an effective-dated reference history.
5. Update downstream imports, relationships and measures that still use
   `fact_offer.home_id`; use `provider_home_id` and the appropriate category role.
   The reusable report-builder measure has been updated, but no versioned semantic
   model/report project was edited, refreshed or tested as part of this change.
6. If older months need these fields, plan an explicit archive rebuild after
   approval. No archived data was deleted or rebuilt locally.

The new Gold objects are registered in `monitoring.cfg_gold_lineage_mapping`.
Mission Control may need an approved refresh/object-list update after deployment;
no dashboard change is implied by the ETL update.
