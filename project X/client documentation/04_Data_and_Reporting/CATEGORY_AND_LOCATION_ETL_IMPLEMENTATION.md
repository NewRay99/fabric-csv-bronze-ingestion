# Category links and approximate location distances

## Offer Locations connection map 5 October 2026

The saved project at `reports/WIP/SM WMPP v16 updated WIP` now has an Azure Maps
connection panel below the existing Offer Locations distance chart and offer
register. The page is taller, not narrower; existing visuals and navigation retain
their positions and sizes. Other pages and bookmarks are unchanged.

Select one referral in the existing search dropdown, or select an offer row in
the register, to show its city-to-home connections. Provider, offer status,
framework, category and distance-band filters also apply. Hover over a marker or
line for the referral, city, postcode, provider, home, offer status, distance and
location quality. Map selection does not filter the register backwards; use the
register or slicers to choose offers.

Orange lines connect teal endpoint markers. They represent approximate
straight-line connections between a city representative point and a postcode
representative point, not driving routes or exact addresses. A default city is
explicitly identified; locations requiring review, incomplete pairs and
out-of-range coordinates do not produce paths. Offers with unavailable locations
remain in the original register and distance chart.

### Coordinate refresh

`04_gold_model.py` now publishes four additional fields in `gold.fact_offer`:
`referral_latitude`, `referral_longitude`, `provider_home_latitude` and
`provider_home_longitude`. The first pair comes from
`silver.referral_location`; the second comes from
`silver.provider_home_location`. These use the approved offline OS lookup and
perform no external geocoding in Fabric. Reviewed referral origins are withheld.

The WIP offer import accepts these fields as nullable numbers. Missing fields in
an older Gold deployment are filled with null, so the map can remain empty
without an import column error. Real lines require the Gold coordinate fields to
be populated and the Power BI model to be refreshed. Cached distances alone
cannot reconstruct the missing coordinates.

If Silver coordinates are already populated, deploy the revised Gold offer SQL
cell, with the notebook's parameter and helper initialization and source checks.
For a map-only deployment, do not run the entire Gold notebook: the earlier
referral journey status change requires the coordinated
[semantic model migration](GOLD_REFERRAL_JOURNEY_STATUS.md). This map addition does
not perform that migration. If coordinates are not yet populated, first follow
the offline lookup hydration steps below and rebuild the Silver location tables.

After the source refresh, reopen the saved WIP and refresh the model. Select a
referral with several geolocated offers, then verify two endpoints per offer and
the displayed distinct-offer coverage. Check provider/status/category filters,
missing/reviewed locations and the dynamic detail RLS role before release. The new
`Offer Location Paths` table uses the active one-way relationship from the
existing secured offer fact; no broader or bidirectional access rule is added.

Azure Maps still uses an online map service and needs existing tenant approval;
offline lookup data does not make the map offline. No tenant settings, Fabric
tables or published reports were changed by this local update. Native rendering
and live RLS/filter checks remain to verify in Desktop after source refresh.
See [Microsoft's path layer guidance](https://learn.microsoft.com/en-us/azure/azure-maps/power-bi-visual-add-path-layer)
and [Azure Maps access guidance](https://learn.microsoft.com/en-us/azure/azure-maps/power-bi-visual-manage-access).

## Offline lookup hydration — updated 1 October 2026

The missing loader is now prepared as `00c_load_location_coordinates.py`. It reads
approved OS Code-Point Open and OS Open Names CSV ZIP deliveries uploaded inside
the default Lakehouse. The defaults are `Files/cfg_files/location_reference/codepo_gb.zip`
and `Files/cfg_files/location_reference/opname_csv_gb.zip`. It extracts only data
CSV tiles into a fresh Lakehouse folder, converts grid coordinates locally and
merges the coordinate lookup. Previously extracted CSV directories remain supported.
No external geocoding/API calls, referral-text export or package/grid downloads are
used. Setup still only creates the table; the new loader is an explicit maintenance
step after Silver formatting and before Silver business rules/Gold rebuild.

See the [upload and execution instructions](../../configuration/location-reference/README.md).
Preview is default; actual reference releases and an approved pyproj environment
are required. Existing approved coordinates are preserved by default. Ambiguous
city/town names and unavailable/sector-level postcode points remain unresolved.
Code-Point/Open Names coverage is Great Britain, not Northern Ireland.

For OS Open Names inputs, Gold now records
`CITY_REPRESENTATIVE_POINT_TO_POSTCODE_STRAIGHT_LINE`: these are representative
settlement points, not geometric centroids. Existing approved centroid references
keep their prior basis. Always display this as approximate preferred-city-to-postcode
straight-line distance, never a child's actual address or driving distance.

Local verification: 130 tests and 158 subtests passed; loader/test lint passed.
No files have been uploaded to Fabric and no client lookup, Silver or Gold tables
have been changed by this local implementation. Spark/Delta and actual projection
verification remain deployment steps. Earlier implementation notes follow.

## Reporting reassessment 30 September 2026

The downstream WIP now imports the referral category bridge and category/location fields, exposes category-aware Explorer measures and includes referral/provider-offer location maps. The older note that no versioned model was changed applies only to the original 25 September ETL batch.

Current membership is not historical membership; many-to-many categories require distinct counts. Approved coordinate data and runtime completeness remain to verify. The preferred-city distance is a centroid-to-postcode straight-line estimate, not a child address, road distance or out-of-region classification. No new coordinate data or Fabric execution is claimed here.

See [current status and release checks](WMPP_CURRENT_STATUS.md). This dated reassessment takes precedence over older reporting status claims below.


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
