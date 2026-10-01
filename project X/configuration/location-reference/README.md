# Offline location reference hydration in Fabric

Prepared 30 September 2026. No geocoding API or external lookup is used. All
matching and coordinate conversion runs inside the attached Fabric Lakehouse.
The loader is prepared, not deployed/executed in the client workspace.

## Reference files to upload

Obtain client-approved **CSV** editions of both products and retain the supplied
licence/attribution, release metadata and original files:

1. **OS Code-Point Open**: postcode representative points for Great Britain.
   Extract its `Data/CSV` data files to
   `Files/cfg_files/location_reference/code_point/Data/CSV`.
2. **OS Open Names**: city/town representative points for Great Britain.
   Extract its data CSV tiles to
   `Files/cfg_files/location_reference/open_names/Data` (subfolders are supported).

Do not upload just the ZIP or mix the documentation/header CSV into those data
folders. The notebook accepts the official headerless data layouts. The source
paths can be changed, but must remain below `Files/cfg_files/location_reference/`
in the default Lakehouse. No HTTP, external storage URI or local computer path
is accepted. Use locally stored files, not shortcuts to unapproved external sources.

Code-Point alone cannot supply named referral-city points. Open Names supplies
representative settlement locations, **not geometric centroids or child addresses**.
Neither product covers Northern Ireland; do not substitute a GB location for an
unmatched postcode/city. An approved local supplementary reference is needed there.

## Run in the Fabric portal

1. Import `project X/00c_load_location_coordinates.py` as a Fabric notebook and
   attach the intended `LH_BCT_WMPP` Lakehouse. Run `00_setup_cfg` first.
2. Ensure `02_silver_formatter` has populated `silver.provider_home`. The loader
   reads only its postcode field locally; it does not read or send addresses or
   referral text. Only postcodes present in that Silver state are converted.
3. Use an approved Fabric environment containing **pyproj** and its local PROJ
   data. The notebook never installs packages or downloads transformation grids.
   If absent, ask the Fabric administrator to supply approved offline packages.
4. Set `CODE_POINT_VERSION` and `OPEN_NAMES_VERSION` to the actual source release
   identifiers. Do not substitute today's execution date for a dataset version.
5. Run with `APPLY_CHANGES=False`. Inspect counts, missing postcode coverage and
   ambiguity counts. The `staged`, `needed_postcodes` and `incoming` dataframes
   are available for in-Fabric inspection; no identifying rows are logged by default.
6. Once satisfied, set `APPLY_CHANGES=True` and rerun. This merges into
   `monitoring.cfg_location_coordinate`; it never deletes rows. Existing nonblank
   approved coordinates are preserved unless `UPDATE_EXISTING=True` is explicitly
   selected. Back up/pin the existing Delta version before any approved refresh.
7. Run `03_silver_business_rules`, `04_gold_model`, `05_gold_dimensions`, and the
   normal reporting step; then refresh the Power BI model. Verify distance status
   counts and several known offers. Loading the lookup alone does not rebuild Gold.

This is a deliberate reference-maintenance notebook, not automatically added to
live/archive runners. Rerun after new provider postcodes appear or an approved
reference release changes. For archive processing, pin the reference version and
hydrate the required historical postcodes before replay; current Silver alone may
not contain them. No historic snapshots are automatically rebuilt.

## Safety and meaning

- British National Grid eastings/northings are converted locally to WGS84. PROJ
  networking is explicitly disabled. Only an installed non-ballpark transformation
  with stated accuracy <=10 metres is accepted; its method/version is recorded.
  Transformation accuracy is not the accuracy of the city or postcode point.
- No random selection among duplicate city/town names: conflicting keys are
  excluded. Use an explicitly reviewed local lookup row to resolve an ambiguity.
- Code-Point quality 60 (postcode-sector point) and 90 (no coordinates) are excluded;
  quality 10–50 are accepted as approximate postcode points. Unknown quality,
  missing coordinates and zero grid placeholders are not treated as real locations.
- Output preserves source/release provenance. Existing reviewed/default referral
  rules remain unchanged; negative or ambiguous preferences still suppress distance.
- Missing locations remain null, not zero distance or a silently substituted town.
- Gold labels Open Names rows `CITY_REPRESENTATIVE_POINT_TO_POSTCODE_STRAIGHT_LINE`;
  it retains the existing centroid basis for other approved references. Label report
  distances as **approximate preferred-city-to-postcode straight-line distance**,
  not actual child-to-home or driving distance. The distance formula is unchanged.

## Verification and sources

Local tests exercise path guards, preview defaults, parameter parsing, invalid
coordinates, axis ordering, offline projection selection and notebook syntax.
They do not execute actual pyproj transformations, Spark/Delta merges or the
client's uploaded files. Complete those checks in development Fabric before use.

- [Code-Point CSV layout](https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-technical-specification/supply-formats-overview)
- [Code-Point positional quality](https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/code-point-open/code-point-open-technical-specification/product-structure)
- [Open Names data/header documentation](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-downloads)
- [pyproj offline network control](https://pyproj4.github.io/pyproj/stable/api/network.html)
