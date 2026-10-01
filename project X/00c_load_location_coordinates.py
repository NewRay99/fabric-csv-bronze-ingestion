# Fabric notebook source
# ruff: noqa: E402 -- Fabric parameter cell intentionally precedes imports.

# METADATA ********************
# META {
# META   "kernel_info": {"name": "synapse_pyspark"},
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "d286fa39-f255-4ba7-a982-32cb69362ef7",
# META       "default_lakehouse_name": "LH_BCT_WMPP",
# META       "default_lakehouse_workspace_id": "fefdb483-d26c-4bd9-9a4f-0c41cc786770",
# META       "known_lakehouses": [{"id": "d286fa39-f255-4ba7-a982-32cb69362ef7"}]
# META     }
# META   }
# META }

# MARKDOWN ********************
# # Local coordinate reference loader — no external lookups
# Upload the two OS CSV ZIP deliveries to the default Lakehouse first. Run setup and
# Silver formatting before this notebook, then Silver business rules and Gold.
# Preview is the default. No API, package install, grid download or address export.
# Requires an approved Fabric environment with pyproj already installed.
# See configuration/location-reference/README.md for formats and coverage limits.

# PARAMETERS CELL ********************
# These inputs accept ZIP deliveries or previously extracted data directories.
CODE_POINT_CSV_PATH = "Files/cfg_files/location_reference/codepo_gb.zip"
OPEN_NAMES_CSV_PATH = "Files/cfg_files/location_reference/opname_csv_gb.zip"
CODE_POINT_VERSION = ""  # Actual release on the uploaded Code-Point Open delivery.
OPEN_NAMES_VERSION = ""  # Actual release on the uploaded OS Open Names delivery.
APPLY_CHANGES = False
UPDATE_EXISTING = False  # Preserve existing approved coordinates unless explicitly enabled.
MAX_CONVERSION_ROWS = 100000  # Relevant postcodes + city/town references; bounds driver memory.

# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}

# CELL ********************
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
import zipfile

from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


def local_reference_path(value):
    """Accept only files under this default Lakehouse's reference directory."""
    value = str(value).strip()
    parts = PurePosixPath(value).parts
    if (
        "\\" in value
        or ":" in value
        or ".." in parts
        or not value.startswith("Files/cfg_files/location_reference/")
    ):
        raise ValueError("Reference inputs must be local Files/cfg_files/location_reference/ paths")
    return value


def parameter_bool(value):
    if isinstance(value, bool):
        return value
    values = {"true": True, "false": False, "1": True, "0": False}
    try:
        return values[str(value).strip().lower()]
    except KeyError as exc:
        raise ValueError("Boolean parameters must be true/false or 1/0") from exc


def prepare_reference_input(value, dataset, mount_root="/lakehouse/default"):
    """Extract only official Data CSV tiles into a fresh, Spark-readable Lakehouse folder."""
    value = local_reference_path(value)
    if not value.lower().endswith(".zip"):
        return value
    if dataset not in {"code_point", "open_names"}:
        raise ValueError("Unknown reference dataset")
    root = Path(mount_root).resolve()
    reference_root = (root / "Files/cfg_files/location_reference").resolve()
    archive_path = (root / value).resolve()
    if not reference_root.is_relative_to(root) or not archive_path.is_relative_to(reference_root):
        raise ValueError("ZIP input escapes the Lakehouse reference directory")
    if not archive_path.is_file():
        raise FileNotFoundError(f"Upload the reference ZIP to the attached Lakehouse: {value}")
    with zipfile.ZipFile(archive_path) as archive:
        selected = []
        total_bytes = 0
        for member in archive.infolist():
            name = member.filename
            parts = PurePosixPath(name).parts
            if (
                "\\" in name
                or ":" in name
                or ".." in parts
                or PurePosixPath(name).is_absolute()
                or stat.S_ISLNK(member.external_attr >> 16)
            ):
                raise ValueError("Unsafe path or symbolic link in reference ZIP")
            lower_parts = [part.lower() for part in parts]
            if member.is_dir() or not name.lower().endswith(".csv") or "data" not in lower_parts:
                continue
            data_index = lower_parts.index("data")
            tile_parts = parts[data_index + 1 :]
            if dataset == "code_point":
                if not tile_parts or tile_parts[0].lower() != "csv":
                    continue
                tile_parts = tile_parts[1:]
            if not tile_parts or "header" in tile_parts[-1].lower():
                continue
            total_bytes += member.file_size
            selected.append((member, PurePosixPath(*tile_parts)))
        if not selected:
            raise ValueError(
                f"No {dataset} data CSV tiles found in ZIP; use the official CSV edition"
            )
        if len(selected) > 10000 or total_bytes > 4 * 1024**3:
            raise ValueError("Reference ZIP exceeds extraction limits (10,000 CSVs / 4 GiB)")
        names = [str(relative).casefold() for _, relative in selected]
        if len(set(names)) != len(names):
            raise ValueError("Duplicate CSV destinations in reference ZIP")
        extraction_parent = (reference_root / "_extracted").resolve()
        if not extraction_parent.is_relative_to(reference_root):
            raise ValueError("Extraction folder escapes the reference directory")
        extraction_parent.mkdir(parents=True, exist_ok=True)
        destination = Path(tempfile.mkdtemp(prefix=f"{dataset}_", dir=extraction_parent))
        # Never extractall: documentation, header CSVs and archive paths are not inputs.
        # Retain this run's files for Spark's lazy reads and subsequent dataframe inspection.
        for member, relative in selected:
            target = destination.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(member) as source, target.open("xb") as output:
                shutil.copyfileobj(source, output, length=1024 * 1024)
    spark_path = destination.relative_to(root).as_posix()
    print(f"Extracted {len(selected)} {dataset} data CSVs to {spark_path}; source ZIP retained")
    return spark_path


def postcode_key(value):
    return re.sub(r"\s+", "", str(value or "")).upper()


def valid_grid_point(easting, northing):
    try:
        easting, northing = float(easting), float(northing)
    except (TypeError, ValueError):
        return False
    return (
        math.isfinite(easting)
        and math.isfinite(northing)
        and 0 < easting < 700000
        and 0 < northing < 1300000
    )


def convert_grid_point(transformer, easting, northing):
    if not valid_grid_point(easting, northing):
        raise ValueError("Invalid British National Grid coordinate")
    longitude, latitude = transformer.transform(float(easting), float(northing), errcheck=True)
    if not (
        math.isfinite(latitude)
        and math.isfinite(longitude)
        and 49 <= latitude <= 61.5
        and -9 <= longitude <= 3
    ):
        raise ValueError("Converted coordinate is outside the expected GB bounds")
    return latitude, longitude


def offline_transformer():
    """Use installed PROJ data only; never enable network or download missing grids."""
    os.environ["PROJ_NETWORK"] = "OFF"
    try:
        import pyproj
        from pyproj import network
        from pyproj.transformer import TransformerGroup
    except ImportError as exc:
        raise RuntimeError(
            "pyproj is required in the approved Fabric environment. "
            "Ask the environment administrator to provide it; this notebook installs nothing."
        ) from exc
    network.set_network_enabled(False)
    group = TransformerGroup("EPSG:27700", "EPSG:4326", always_xy=True, allow_ballpark=False)
    choices = [item for item in group.transformers if 0 <= item.accuracy <= 10]
    if not choices:
        raise RuntimeError("No installed non-ballpark GB transformation with <=10m accuracy")
    transformer = choices[0]
    provenance = (
        f"pyproj {pyproj.__version__}; PROJ {pyproj.proj_version_str}; "
        f"{transformer.description}; transform accuracy {transformer.accuracy}m; "
        f"{transformer.definition}"
    )
    return transformer, provenance


def read_os_csv(path, minimum_columns):
    # Official data tiles are headerless. Never include their documentation/header CSV.
    frame = (
        spark.read.option("header", "false")
        .option("inferSchema", "false")
        .option("mode", "FAILFAST")
        .option("recursiveFileLookup", "true")
        .option("pathGlobFilter", "*.csv")
        .csv(local_reference_path(path))
    )
    if len(frame.columns) < minimum_columns:
        raise ValueError(f"Unexpected CSV structure: need at least {minimum_columns} columns")
    return frame


def normalised_reference(frame):
    return frame.withColumn("location_type", F.upper(F.trim("location_type"))).withColumn(
        "_key",
        F.when(
            F.col("location_type") == "POSTCODE",
            F.regexp_replace(F.upper(F.trim("location_key")), r"\s+", ""),
        ).otherwise(F.lower(F.trim("location_key"))),
    )


def unambiguous_grid_rows(frame, label):
    frame = frame.dropDuplicates(["location_type", "_key", "easting", "northing"])
    conflicting = frame.groupBy("location_type", "_key").count().where("count > 1")
    conflict_count = conflicting.count()
    print(f"{label}: {conflict_count} ambiguous keys excluded; resolve locally before use")
    return frame.join(
        conflicting.select("location_type", "_key"), ["location_type", "_key"], "left_anti"
    )


# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}

# CELL ********************
target_table = "monitoring.cfg_location_coordinate"
spark = SparkSession.getActiveSession()
if spark is None:
    raise RuntimeError("Run this notebook in Fabric with the intended default Lakehouse attached")
apply_changes = parameter_bool(APPLY_CHANGES)
update_existing = parameter_bool(UPDATE_EXISTING)
if not str(CODE_POINT_VERSION).strip() or not str(OPEN_NAMES_VERSION).strip():
    raise ValueError("Supply the actual release versions for both uploaded OS reference datasets")
if not spark.catalog.tableExists(target_table):
    raise RuntimeError("Run 00_setup_cfg first to create the coordinate lookup")
if not spark.catalog.tableExists("silver.provider_home"):
    raise RuntimeError("Run Silver formatting first; provider-home postcodes are needed locally")

needed_postcodes = (
    spark.table("silver.provider_home")
    .select(F.regexp_replace(F.upper(F.trim("postcode")), r"\s+", "").alias("_key"))
    .where(F.col("_key").isNotNull() & (F.length("_key") > 0))
    .distinct()
)

# Official Code-Point Open CSV: PC, PQ, EA, NO, CY, RH, LH, CC, DC, WC.
postcode_raw = read_os_csv(prepare_reference_input(CODE_POINT_CSV_PATH, "code_point"), 10)
postcodes = postcode_raw.select(
    F.lit("POSTCODE").alias("location_type"),
    F.col("_c0").alias("location_key"),
    F.expr("try_cast(_c1 as int)").alias("quality"),
    F.expr("try_cast(_c2 as double)").alias("easting"),
    F.expr("try_cast(_c3 as double)").alias("northing"),
)
postcodes = normalised_reference(postcodes).join(needed_postcodes, "_key", "inner")
# PQ60 is sector-level, PQ90 has no coordinates: neither is labelled postcode-level here.
postcodes = postcodes.where(F.col("quality").isin(10, 20, 30, 40, 50))
postcodes = postcodes.withColumn("location_key", F.col("_key"))

# OS Open Names: ID, NAMES_URI, NAME1, NAME1_LANG, NAME2, NAME2_LANG,
# TYPE, LOCAL_TYPE, GEOMETRY_X, GEOMETRY_Y, ... . No address/free text is queried.
names_raw = read_os_csv(prepare_reference_input(OPEN_NAMES_CSV_PATH, "open_names"), 10)
places = names_raw.where(F.col("_c7").isin("City", "Town")).select(
    F.lit("CITY").alias("location_type"),
    F.trim("_c2").alias("location_key"),
    F.expr("try_cast(_c8 as double)").alias("easting"),
    F.expr("try_cast(_c9 as double)").alias("northing"),
)
places = normalised_reference(places).where(F.length("_key") > 0)
columns = ["location_type", "location_key", "_key", "easting", "northing"]
staged = unambiguous_grid_rows(postcodes.select(*columns), "Postcodes").unionByName(
    unambiguous_grid_rows(places.select(*columns), "Cities/towns")
)
valid_grid = (
    F.col("easting").between(0.000001, 699999.999999)
    & F.col("northing").between(0.000001, 1299999.999999)
    & ~F.isnan("easting")
    & ~F.isnan("northing")
)
staged = staged.where(valid_grid)
grid_rows = staged.limit(int(MAX_CONVERSION_ROWS) + 1).collect()
if len(grid_rows) > int(MAX_CONVERSION_ROWS):
    raise ValueError("Reference conversion exceeds MAX_CONVERSION_ROWS; review input scope")
if not grid_rows or not any(row.location_type == "CITY" for row in grid_rows):
    raise ValueError(
        "No usable city/town coordinates; check the uploaded Open Names CSV data folder"
    )

transformer, transform_source = offline_transformer()
converted = []
for row in grid_rows:
    latitude, longitude = convert_grid_point(transformer, row.easting, row.northing)
    source = (
        "OS Code-Point Open postcode point"
        if row.location_type == "POSTCODE"
        else "OS Open Names representative city/town point (not geometric centroid)"
    )
    version = CODE_POINT_VERSION if row.location_type == "POSTCODE" else OPEN_NAMES_VERSION
    converted.append(
        (
            row.location_type,
            row.location_key,
            latitude,
            longitude,
            f"{source}; {transform_source}",
            str(version).strip(),
        )
    )
incoming = spark.createDataFrame(
    converted,
    "location_type string, location_key string, latitude double, longitude double, "
    "reference_source string, reference_version string",
)
incoming = normalised_reference(incoming)
existing = normalised_reference(spark.table(target_table))
if existing.groupBy("location_type", "_key").count().where("count > 1").limit(1).count():
    raise ValueError("Existing lookup has duplicate normalised keys; resolve before merging")
print(
    f"Prepared {len(converted)} reference rows; apply={apply_changes}; update_existing={update_existing}"
)
incoming.groupBy("location_type").count().show()
matched_postcodes = incoming.where("location_type = 'POSTCODE'").select("_key")
print(
    f"Requested postcodes without an accepted point in this release: {needed_postcodes.join(matched_postcodes, '_key', 'left_anti').count()}"
)

if apply_changes:
    # Merge only; no deletions, overwrite or archive replay. Existing curated values
    # remain unless blank or an operator explicitly requests a reference update.
    target_type = F.upper(F.trim(F.col("t.location_type")))
    target_key = F.when(
        target_type == "POSTCODE",
        F.regexp_replace(F.upper(F.trim(F.col("t.location_key"))), r"\s+", ""),
    )
    target_key = target_key.otherwise(F.lower(F.trim(F.col("t.location_key"))))
    values = {name: f"s.{name}" for name in incoming.columns if name != "_key"}
    merge = (
        DeltaTable.forName(spark, target_table)
        .alias("t")
        .merge(
            incoming.alias("s"),
            (target_type == F.col("s.location_type")) & (target_key == F.col("s._key")),
        )
    )
    merge.whenMatchedUpdate(
        condition="true" if update_existing else "t.latitude IS NULL AND t.longitude IS NULL",
        set=values,
    ).whenNotMatchedInsert(values=values).execute()
    print(
        "Lookup hydrated. Rerun 03_silver_business_rules, 04_gold_model, 05_gold_dimensions; then refresh the report model."
    )
else:
    print(
        "Preview only: lookup unchanged. Review counts, versions and ambiguous keys before setting APPLY_CHANGES=True."
    )

# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}
