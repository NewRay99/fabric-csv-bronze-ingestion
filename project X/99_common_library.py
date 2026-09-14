# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {},
# META   "spark_compute": {
# META     "compute_id": "/trident/default",
# META     "session_options": {
# META       "conf": {
# META         "spark.synapse.nbs.session.timeout": "1200000"
# META       }
# META     }
# META   }
# META }

# MARKDOWN ********************

# # Shared ETL library
#
# One source for ETL exclusions, schema conformance, audit helpers, and Silver formatting utilities.

# CELL ********************

import re
from bisect import bisect_right
import uuid
from collections import defaultdict
from datetime import datetime

from delta.tables import DeltaTable
from pyspark.sql import functions as F
from pyspark.sql.types import (
    BooleanType, IntegerType, LongType, StringType, StructField, StructType,
    TimestampType,
)
from pyspark.sql.window import Window

# Preserve caller parameters when this notebook is loaded with %run, while
# keeping the library executable and lintable on its own.
TIME_PARSER_POLICY = globals().get("TIME_PARSER_POLICY", "CORRECTED")
DATE_FORMATS = globals().get(
    "DATE_FORMATS", ["yyyy-MM-dd", "dd/MM/yyyy", "yyyy-MM-dd'T'HH:mm:ss"]
)
TIMESTAMP_FORMATS = globals().get(
    "TIMESTAMP_FORMATS",
    [
        "yyyy-MM-dd", "yyyy-MM-dd HH:mm:ss.SSSSSS", "yyyy-MM-dd HH:mm:ss.SSS",
        "yyyy-MM-dd HH:mm:ss.S", "yyyy-MM-dd HH:mm:ss",
        "yyyy-MM-dd'T'HH:mm:ss.SSSSSS", "yyyy-MM-dd'T'HH:mm:ss.SSS",
        "yyyy-MM-dd'T'HH:mm:ss.S", "yyyy-MM-dd'T'HH:mm:ss",
        "yyyy-MM-dd'T'HH-mm-ssX",
    ],
)
VERBOSE_DIAGNOSTICS = globals().get("VERBOSE_DIAGNOSTICS", False)
DIAGNOSTIC_KEY_SAMPLE_SIZE = globals().get("DIAGNOSTIC_KEY_SAMPLE_SIZE", 5)
SILVER_SCHEMA = globals().get("SILVER_SCHEMA", "silver")
AUDIT_TABLE = globals().get("AUDIT_TABLE", "monitoring.cfg_silver_export_load")
contracts_by_table = globals().get("contracts_by_table", {})
RUN_ID = globals().get("RUN_ID", str(uuid.uuid4()))
JOB_RUN_ID = globals().get("JOB_RUN_ID", "")
STARTED_AT = globals().get("STARTED_AT", datetime.utcnow())
spark.conf.set("spark.sql.legacy.timeParserPolicy", TIME_PARSER_POLICY)

ETL_EXCLUDED_TABLES = [
    "ref_KPI_Definition",
    "ref_KPI_RID_linkage",
    "ref_RID",
    "ref_Table_Lineage",
]
ETL_EXCLUDED_TABLE_PREFIXES = ["ref_"]
ETL_PHYSICAL_PREFIXES = ()


def etl_logical_table_name(table_name):
    name = str(table_name or "").replace("\\", "/").rsplit("/", 1)[-1]
    name = name.rsplit(".", 1)[0] if name.lower().endswith((".csv", ".parquet")) else name
    name = name.rsplit(".", 1)[-1].lower()
    for prefix in ETL_PHYSICAL_PREFIXES:
        if name.startswith(prefix):
            name = name[len(prefix):]
    return name


_ETL_EXCLUDED_TABLES_LOWER = {name.lower() for name in ETL_EXCLUDED_TABLES}
_ETL_EXCLUDED_PREFIXES_LOWER = tuple(prefix.lower() for prefix in ETL_EXCLUDED_TABLE_PREFIXES)


def is_etl_excluded_table(table_name):
    logical_name = etl_logical_table_name(table_name)
    return (
        logical_name in _ETL_EXCLUDED_TABLES_LOWER
        or logical_name.startswith(_ETL_EXCLUDED_PREFIXES_LOWER)
    )


def excluded_etl_tables(table_names):
    return sorted(name for name in table_names if is_etl_excluded_table(name))


_LOG_STEP_STATE = {}


def log_step(label):
    """Print step, elapsed and cumulative time for pipeline monitoring.

    State lives in the shared %run namespace, so timings accumulate across
    the calling notebook's cells. Added for LIVE-ETL-003 observability.
    """
    now = datetime.utcnow()
    start = _LOG_STEP_STATE.setdefault("start", now)
    previous = _LOG_STEP_STATE.setdefault("previous", now)
    elapsed = (now - previous).total_seconds()
    total = (now - start).total_seconds()
    _LOG_STEP_STATE["previous"] = now
    print(f"[{now:%Y-%m-%d %H:%M:%S}] {label} | +{elapsed:,.1f}s step | {total:,.1f}s total")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def qident(value):
    return "`" + str(value).replace("`", "``") + "`"


def normalise(value):
    return re.sub(r"[^a-z0-9]", "", (value or "").lower())


def append_rows(table_name, rows, schema):
    if rows:
        spark.createDataFrame(rows, schema).write.format("delta").mode("append").saveAsTable(table_name)


def merge_monitor_row(table_name, row, schema, condition):
    """Upsert one parent-job or child-step monitoring record."""
    source = spark.createDataFrame([row], schema)
    target = DeltaTable.forName(spark, table_name)
    (target.alias("target").merge(source.alias("source"), condition)
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())


def drift_event_row(source_kind, source_table, target_table, drift_type,
                    column_name=None, expected_type=None, actual_type=None,
                    referenced_table=None, referenced_column=None):
    """Build a consistently keyed Silver schema-drift monitoring row."""
    now = datetime.utcnow()
    identity = "||".join(str(value or "") for value in (
        source_kind, source_table, column_name, drift_type,
        referenced_table, referenced_column,
    ))
    drift_key = str(uuid.uuid5(uuid.NAMESPACE_URL, identity))
    return (
        RUN_ID, source_kind, source_table, target_table, drift_type,
        column_name, expected_type, actual_type, referenced_table,
        referenced_column, drift_key, "ACTIVE", 1, now, now, None, now, JOB_RUN_ID or None,
    )


def map_data_type(pg_type):
    value = (pg_type or "").lower().strip()
    if "[]" in value:
        return "ARRAY<STRING>"
    if any(token in value for token in ("uuid", "json", "text", "character", "varchar")):
        return "STRING"
    if value in {"smallint", "int2", "integer", "int", "int4"}:
        return "INT"
    if value in {"bigint", "int8"}:
        return "BIGINT"
    match = re.search(r"(?:numeric|decimal)\s*\((\d+)\s*,\s*(\d+)\)", value)
    if match:
        precision = min(int(match.group(1)), 38)
        scale = min(int(match.group(2)), precision)
        return f"DECIMAL({precision},{scale})"
    if "numeric" in value or "decimal" in value:
        return "DECIMAL(38,18)"
    if any(token in value for token in ("double", "float", "real")):
        return "DOUBLE"
    if "boolean" in value or value == "bool":
        return "BOOLEAN"
    if value == "date":
        return "DATE"
    if "timestamp" in value:
        return "TIMESTAMP"
    return "STRING"


def first_parsed(column, formats, parser):
    return F.coalesce(*[parser(column, fmt) for fmt in formats])


def cast_column(frame, definition):
    name = definition["column_name"]
    spark_type = map_data_type(definition["data_type"])
    if name not in frame.columns:
        return F.lit(None).cast(spark_type).alias(name)
    source = F.col(qident(name))
    if spark_type == "BOOLEAN":
        clean = F.lower(F.trim(source.cast("string")))
        return (F.when(clean.isin("true", "t", "1", "yes", "y"), F.lit(True))
            .when(clean.isin("false", "f", "0", "no", "n"), F.lit(False))
            .otherwise(F.lit(None).cast("boolean")).alias(name))
    if spark_type == "DATE":
        return first_parsed(source.cast("string"), DATE_FORMATS, F.to_date).alias(name)
    if spark_type == "TIMESTAMP":
        return first_parsed(source.cast("string"), TIMESTAMP_FORMATS, F.to_timestamp).alias(name)
    if spark_type.startswith("DECIMAL") or spark_type in {"INT", "BIGINT", "DOUBLE"}:
        return F.regexp_replace(source.cast("string"), r"[^0-9eE+\.\-]", "").cast(spark_type).alias(name)
    if spark_type == "ARRAY<STRING>":
        return F.when(source.isNull(), F.lit(None).cast("array<string>"))             .otherwise(F.split(F.regexp_replace(source.cast("string"), r"^[\{\[]|[\}\]]$", ""), r"\s*,\s*")).alias(name)
    return F.trim(source.cast("string")).alias(name)


def resolve_contract(physical_table, prefixes):
    base = physical_table.lower()
    for prefix in prefixes:
        if base.startswith(prefix):
            base = base[len(prefix):]
    matches = contracts_by_table.get(normalise(base), [])
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ValueError(f"Ambiguous table contract for {physical_table}: {matches}")
    return None


def primary_key_columns(schema_cols):
    """Return the ordered business key defined by the schema contract."""
    return [
        column["column_name"] for column in schema_cols
        if (column.get("is_primary_key") or "").upper() == "YES"
    ]


def deduplicate_frame(frame, schema_cols):
    """Keep one row per contracted PK without triggering count jobs here."""
    key_columns = primary_key_columns(schema_cols)
    if not key_columns:
        return frame, key_columns
    if "_archive_load_ts" in frame.columns:
        ordering = F.col("_archive_load_ts").cast("timestamp").desc_nulls_last()
    elif "_ingestion_timestamp" in frame.columns:
        ordering = F.col("_ingestion_timestamp").cast("timestamp").desc_nulls_last()
    else:
        ordering = F.col(qident("export_date")).cast("timestamp").desc_nulls_last()
    window = Window.partitionBy(
        *[F.col(qident(column)) for column in key_columns]
    ).orderBy(ordering)
    ranked = frame.withColumn("_silver_row_number", F.row_number().over(window))
    return ranked.where(F.col("_silver_row_number") == 1).drop("_silver_row_number"), key_columns


def diagnostic_key_sample(frame, key_columns):
    """Collect a small identifier-only sample for operational tracing."""
    if not VERBOSE_DIAGNOSTICS or not key_columns:
        return []
    return [
        row.asDict(recursive=True)
        for row in frame.select(*[F.col(qident(column)) for column in key_columns])
            .limit(DIAGNOSTIC_KEY_SAMPLE_SIZE).collect()
    ]


def print_load_diagnostics(source_table, target_table, snapshot_date, source_date,
                           raw_frame, formatted_frame, key_columns,
                           source_count, written_count, duplicate_count,
                           formatted_export_non_null):
    """Print dates, counts and PK identifiers needed to diagnose a batch."""
    if not VERBOSE_DIAGNOSTICS:
        return
    raw_export_type = next(
        field.dataType.simpleString() for field in raw_frame.schema.fields
        if field.name == "export_date"
    )
    formatted_dates = [
        str(row["export_date"])
        for row in formatted_frame.select(F.to_date("export_date").alias("export_date"))
            .where(F.col("export_date").isNotNull()).distinct().orderBy("export_date").collect()
    ]
    print(f"  Source: {source_table}; selected export={source_date}; raw type={raw_export_type}")
    print(f"  Target: {target_table}; Gold snapshot={snapshot_date}")
    print(f"  Rows: source={source_count:,}; written={written_count:,}; duplicates removed={duplicate_count:,}")
    print(f"  Primary keys: {key_columns or ['<none>']}")
    print(f"  Primary-key sample: {diagnostic_key_sample(formatted_frame, key_columns)}")
    print(
        f"  Silver export_date: non-null={formatted_export_non_null:,}; "
        f"null={written_count - formatted_export_non_null:,}; values={formatted_dates}"
    )


# SI-025: every Bronze/Archive frame carries a row-level export_date (the
# formatters reject sources without one), so every Silver table must publish
# it. A deployed cfg_schema_contract_column that pre-dates the export_date
# contract rows would otherwise silently drop the column; the bootstrap only
# loads the CSV into an empty table, so the stale contract never self-heals.
# Patch the in-memory contract instead: the Silver write gains export_date,
# the drift check stops reporting it as EXTRA, and target_requires_refresh
# flags existing Silver tables that lack the column for rebuild.
EXPORT_DATE_CONTRACT_COLUMN = {
    "ordinal_position": 999999,
    "column_name": "export_date",
    "data_type": "timestamp without time zone",
    "is_primary_key": "NO",
    "referenced_table": "",
    "referenced_column": "",
}


def ensure_export_date_contract(schema_cols):
    """Append the export_date contract column when the deployed contract lacks it."""
    if any(definition["column_name"].lower() == "export_date" for definition in schema_cols):
        return schema_cols
    return [*schema_cols, dict(EXPORT_DATE_CONTRACT_COLUMN)]


def format_frame(frame, schema_cols, source_kind, source_table):
    expressions = [cast_column(frame, definition) for definition in schema_cols]
    return (frame.select(*expressions)
        .withColumn("_record_source", F.lit(source_kind))
        .withColumn("_source_table", F.lit(source_table))
        .withColumn("_silver_run_id", F.lit(RUN_ID))
        .withColumn("_silver_load_ts", F.current_timestamp()))


AUDIT_SCHEMA = StructType([
    StructField("source_kind", StringType(), False),
    StructField("source_schema", StringType(), False),
    StructField("source_table", StringType(), False),
    StructField("target_table", StringType(), True),
    StructField("export_date", TimestampType(), False),
    StructField("status", StringType(), False),
    StructField("reload", BooleanType(), False),
    StructField("attempt_count", IntegerType(), False),
    StructField("run_id", StringType(), True),
    StructField("rows_read", LongType(), True),
    StructField("rows_written", LongType(), True),
    StructField("duplicate_key_count", LongType(), True),
    StructField("started_at", TimestampType(), True),
    StructField("ended_at", TimestampType(), True),
    StructField("error_message", StringType(), True),
    StructField("last_updated_at", TimestampType(), True),
    StructField("job_run_id", StringType(), True),
])


def audit_record(source_kind, source_schema, source_table, export_date):
    rows = (spark.table(AUDIT_TABLE)
        .where((F.col("source_kind") == source_kind)
            & (F.col("source_schema") == source_schema)
            & (F.col("source_table") == source_table)
            & (F.col("export_date") == F.lit(export_date).cast("timestamp")))
        .limit(1).collect())
    return rows[0].asDict() if rows else None


def should_skip(source_kind, source_schema, source_table, export_date):
    record = audit_record(source_kind, source_schema, source_table, export_date)
    return bool(record and record["status"] == "SUCCESS" and not record["reload"])


def audit_begin(source_kind, source_schema, source_table, target_table, export_date):
    now = datetime.utcnow()
    existing = audit_record(source_kind, source_schema, source_table, export_date)
    attempt_count = int(existing["attempt_count"] or 0) + 1 if existing else 1
    row = [(source_kind, source_schema, source_table, target_table, export_date, "RUNNING",
            bool(existing["reload"]) if existing else False, attempt_count, RUN_ID,
            None, None, None, now, None, None, now, JOB_RUN_ID or None)]
    source = spark.createDataFrame(row, AUDIT_SCHEMA)
    target = DeltaTable.forName(spark, AUDIT_TABLE)
    condition = " AND ".join([
        "t.source_kind = s.source_kind", "t.source_schema = s.source_schema",
        "t.source_table = s.source_table", "t.export_date = s.export_date",
    ])
    (target.alias("t").merge(source.alias("s"), condition)
        .whenMatchedUpdate(set={
            "target_table": "s.target_table", "status": "s.status",
            "attempt_count": "s.attempt_count", "run_id": "s.run_id",
            "started_at": "s.started_at", "ended_at": "s.ended_at",
            "error_message": "s.error_message", "last_updated_at": "s.last_updated_at",
            "job_run_id": "s.job_run_id",
        }).whenNotMatchedInsertAll().execute())


def audit_finish(source_kind, source_schema, source_table, target_table, export_date,
                 status, rows_read=0, rows_written=0, duplicate_count=0, error_message=None):
    now = datetime.utcnow()
    existing = audit_record(source_kind, source_schema, source_table, export_date) or {}
    row = [(source_kind, source_schema, source_table, target_table, export_date, status,
            False if status == "SUCCESS" else bool(existing.get("reload", False)),
            int(existing.get("attempt_count") or 1), RUN_ID, int(rows_read), int(rows_written),
            int(duplicate_count), existing.get("started_at") or now, now,
            error_message[:4000] if error_message else None, now, JOB_RUN_ID or None)]
    source = spark.createDataFrame(row, AUDIT_SCHEMA)
    target = DeltaTable.forName(spark, AUDIT_TABLE)
    condition = " AND ".join([
        "t.source_kind = s.source_kind", "t.source_schema = s.source_schema",
        "t.source_table = s.source_table", "t.export_date = s.export_date",
    ])
    (target.alias("t").merge(source.alias("s"), condition)
        .whenMatchedUpdateAll().whenNotMatchedInsertAll().execute())

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Silver-layer helpers

# CELL ********************

def silver_table(table_name):
    return f"{SILVER_SCHEMA}.{table_name.lower()}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

def deduplicate_with_count(frame, schema_cols):
    """Deduplicate with the common key logic and return the removed-row count."""
    deduplicated, _ = deduplicate_frame(frame, schema_cols)
    return deduplicated, frame.count() - deduplicated.count()


def target_requires_refresh(target_table, schema_cols):
    """Return True if a prior-success target is absent or contract-incomplete."""
    if not spark.catalog.tableExists(target_table):
        return True
    actual_columns = {field.name.lower() for field in spark.table(target_table).schema.fields}
    expected_columns = {definition["column_name"].lower() for definition in schema_cols}
    missing_columns = expected_columns - actual_columns
    if missing_columns:
        print(f"REFRESH {target_table}: missing contract columns {sorted(missing_columns)}")
        return True
    return False

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## Data-domain helpers
#
# Shared helpers for contract-driven, low-cardinality Bronze value domains.

# CELL ********************

DATA_DOMAIN_SCHEMA = StructType([
    StructField("source_schema", StringType(), False),
    StructField("source_table", StringType(), False),
    StructField("column_name", StringType(), False),
    StructField("contract_data_type", StringType(), True),
    StructField("data_domain", StringType(), False),
    StructField("distinct_value_count", LongType(), False),
    StructField("profiled_at", TimestampType(), False),
    StructField("run_id", StringType(), False),
    StructField("job_run_id", StringType(), True),
])


def sql_literal(value):
    return "'" + str(value).replace("'", "''") + "'"


def is_contract_string(data_type):
    """Return whether a PostgreSQL contract type is represented as a Spark string."""
    type_name = (data_type or "").strip().lower()
    return any(marker in type_name for marker in ("character", "varchar", "text", "uuid", "json", "string"))


def data_domain_exclusion_reason(column_name, data_type):
    """Return why a string column is unsuitable for a reusable value domain.

Domains are intended for stable lookup-like values, not keys, audit users,
personal/contact data, or free text. The policy is name- and contract-based
so unsuitable columns are skipped before their Bronze values are scanned.
"""
    raw_name = str(column_name or "").lower()
    compact_name = normalise(raw_name)
    name_tokens = set(re.findall(r"[a-z0-9]+", raw_name))
    type_name = (data_type or "").strip().lower()

    if any(marker in type_name for marker in ("uuid", "guid", "uniqueidentifier")):
        return "identifier_type"
    if compact_name in {"id", "uid", "uuid", "guid"} or raw_name.endswith(("_id", "_uid", "_uuid", "_guid")):
        return "identifier_column"
    if compact_name.endswith(("uuid", "guid")) or "identifier" in name_tokens:
        return "identifier_column"

    if compact_name in {"createdby", "updatedby", "modifiedby", "lastupdatedby", "deletedby"}:
        return "audit_user"
    if "email" in name_tokens or "email" in compact_name:
        return "email_address"
    if name_tokens.intersection({"phone", "telephone", "mobile", "fax"}) or ("contact" in name_tokens and "number" in name_tokens):
        return "contact_detail"
    if name_tokens.intersection({"address", "postcode", "post"}):
        return "address_detail"
    if name_tokens.intersection({"name", "initials", "username", "user"}):
        return "personal_or_user_name"
    if name_tokens.intersection({"description", "detail", "details", "message", "comment", "note", "notes", "summary", "text", "information", "instruction", "content", "narrative"}):
        return "free_text"
    return None


def is_data_domain_candidate(column_name, data_type):
    """Return True only for a contract string column suitable for value-domain profiling."""
    return is_contract_string(data_type) and data_domain_exclusion_reason(column_name, data_type) is None


def data_domain_predicate(source_schema, source_table, column_name):
    return (
        f"source_schema = {sql_literal(source_schema)} AND "
        f"source_table = {sql_literal(source_table)} AND "
        f"column_name = {sql_literal(column_name)}"
    )


def collect_low_cardinality_domain_values(frame, column_name, max_distinct_values, include_empty_string=False):
    """Return sorted values when the column has at most the threshold, else None.

    The extra value proves that a high-cardinality column is skipped before any
    domain row can be written. Values are kept as stored; whitespace is only
    used when deciding whether a value is empty.
    """
    string_value = F.col(qident(column_name)).cast("string")
    candidates = frame.select(string_value.alias("data_domain")).where(F.col("data_domain").isNotNull())
    if not include_empty_string:
        candidates = candidates.where(F.length(F.trim(F.col("data_domain"))) > 0)
    values = [
        row.data_domain
        for row in candidates.distinct().limit(max_distinct_values + 1).collect()
    ]
    if len(values) > max_distinct_values:
        return None
    return sorted(values)


def clear_data_domain_table(domain_table):
    """Clear all stored domains only when the caller explicitly requests it."""
    DeltaTable.forName(spark, domain_table).delete()


def remove_data_domain(domain_table, source_schema, source_table, column_name):
    """Remove a stale domain for one source column."""
    DeltaTable.forName(spark, domain_table).delete(
        data_domain_predicate(source_schema, source_table, column_name)
    )


def replace_data_domain(domain_table, source_schema, source_table, column_name,
                        contract_data_type, values, profiled_at, run_id, job_run_id):
    """Atomically replace the stored low-cardinality domain for one column."""
    if values is None or not values:
        remove_data_domain(domain_table, source_schema, source_table, column_name)
        return
    predicate = data_domain_predicate(source_schema, source_table, column_name)
    distinct_value_count = len(values)
    rows = [
        (
            source_schema, source_table, column_name, contract_data_type, value,
            distinct_value_count, profiled_at, run_id, job_run_id or None,
        )
        for value in values
    ]
    (
        spark.createDataFrame(rows, DATA_DOMAIN_SCHEMA)
        .write.format("delta")
        .mode("overwrite")
        .option("replaceWhere", predicate)
        .saveAsTable(domain_table)
    )

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
