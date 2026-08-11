"""Regression checks for archive audit CSV and multi-batch processing."""

import ast
import json
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
NOTEBOOK = ROOT / "00_archive_load 02 03.ipynb"
notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))

for index, cell in enumerate(notebook["cells"]):
    code = "".join(cell.get("source", []))
    if cell["cell_type"] == "code" and not code.lstrip().startswith("%%"):
        ast.parse(code, filename=f"archive-load:cell-{index}")
print("PASS notebook JSON and Python syntax")

parameters = "".join(notebook["cells"][1]["source"])
helpers = "".join(notebook["cells"][2]["source"])
zip_loop = "".join(notebook["cells"][4]["source"])
file_loop = "".join(notebook["cells"][5]["source"])
all_source = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])

# Exercise the real filename classification functions without importing Spark.
tree = ast.parse(helpers)
wanted = {
    "parse_export_date",
    "clean_table_name",
    "should_load_archive_file",
    "legacy_audit_columns_to_add",
    "is_archive_audit_file",
}
function_nodes = [
    node for node in tree.body
    if isinstance(node, ast.FunctionDef) and node.name in wanted
]
namespace = {"re": re, "os": os, "datetime": __import__("datetime").datetime,
             "TABLE_PREFIX": "archived_", "ValueError": ValueError}
exec(compile(ast.Module(body=function_nodes, type_ignores=[]), "helpers", "exec"), namespace)
assert namespace["clean_table_name"]("2026-06-29.csv") == "archived_audit"
assert namespace["parse_export_date"]("2026-06-29.csv").strftime("%Y-%m-%d") == "2026-06-29"
print("PASS date-named CSV routes to archived.archived_audit")

should_load = namespace["should_load_archive_file"]
assert should_load(None)
assert not should_load({"status": "SUCCESS", "reload": False})
assert should_load({"status": "SUCCESS", "reload": True})
assert should_load({"status": "FAILED", "reload": False})
assert should_load({"status": "SUCCESS", "reload": False}, True)
print("PASS cfg archive audit status/reload controls the pending queue")

assert 'STOP_ON_FIRST_ERROR = False' in parameters
assert "if STOP_ON_FIRST_ERROR:\n            break" in zip_loop
assert "if STOP_ON_FIRST_ERROR:\n            break" in file_loop
assert "FAIL_ON_FILE_ERROR" not in all_source
print("PASS errors are collected while later ZIP/file batches continue")

assert '"audit_file_date"' in file_loop
assert '"export_date"' in file_loop
assert "parse_export_date(file_name)" in file_loop
print("PASS audit filename date and ZIP export date are both retained")

assert "Discovered dated ZIPs" in zip_loop
assert "Archive inventory root" in file_loop
assert "zip_batches_by_month" in zip_loop
print("PASS batch-discovery diagnostics are present")

assert "RUN_ZIP_EXTRACTION = True" in parameters
assert "ARCHIVE_FILE_ROOT = EXTRACT_ROOT" in parameters
assert "for zip_export_date, relative_zip, _ in zip_batches:" not in file_loop
assert "archive_file_root_posix" in file_loop
assert "extraction folder is missing" in zip_loop
print("PASS archive inventory is independent from ZIP extraction and audit filtered")

# Archive discovery must include files copied directly into the archive folder,
# then perform one dataframe-to-dataframe audit filter (not one SQL lookup/file).
assert "def discover_archive_files_dataframe(" in helpers
assert "def filter_pending_archive_files(" in helpers
assert "archive_files_df = discover_archive_files_dataframe(" in file_loop
assert "pending_files_df = filter_pending_archive_files(" in file_loop
assert 'spark.table("monitoring.cfg_archive_file_load")' in file_loop
assert ".first()" not in file_loop
assert "audit_record(" not in file_loop
assert "left_anti" in helpers
assert "os.walk(archive_root_abs)" in helpers
assert '"DIRECT_ARCHIVE_FOLDER"' in helpers
print("PASS direct archive files use one dataframe inventory and one bulk audit filter")

# Files are full dated exports. Processing order is irrelevant; a pending file
# replaces its source-path/date slice and then appends every source row.
assert "folder_export_date = parse_export_date(folder_relative)" in helpers
assert ".sort(" not in file_loop
assert ".orderBy(" not in file_loop
assert 'F.col("_archive_source_path") == F.lit(relative_path)' in file_loop
assert 'F.to_date("export_date") == F.lit(export_date.date())' in file_loop
assert 'frame.write.format("delta").mode("append")' in file_loop
assert "Loaded all {row_count:,} rows" in file_loop
print("PASS unordered full-file replacement inherits the dated folder export_date")

# A pre-existing archived_audit table may contain only the source event fields.
# The loader must add its managed dates/lineage before delete-before-append runs.
assert "def legacy_audit_columns_to_add(" in helpers
assert "def ensure_legacy_audit_lineage(" in helpers
assert "ensure_legacy_audit_lineage(target_object)" in file_loop
assert file_loop.index("ensure_legacy_audit_lineage(target_object)") < file_loop.index(
    'target_delta = DeltaTable.forName(spark, target_object)'
)
assert "audit_file_date DATE" in helpers
assert "export_date TIMESTAMP" in helpers
assert "_archive_source_path STRING" in helpers
legacy_columns = namespace["legacy_audit_columns_to_add"]([])
assert "audit_file_date DATE" in legacy_columns
assert "export_date TIMESTAMP" in legacy_columns
assert "_archive_source_path STRING" in legacy_columns
assert namespace["legacy_audit_columns_to_add"](
    ["audit_file_date", "export_date", "_archive_source_path",
     "_archive_source_zip", "_archive_run_id", "_archive_load_ts"]
) == []
print("PASS legacy archived_audit gains loader dates and lineage before replacement")

# The shared metric contract is owned by setup/Silver and uses
# null_primary_key_count. Telemetry failure must not mark loaded data FAILED.
assert "null_primary_key_count BIGINT" in all_source
assert "null_primary_key_count long,recorded_at timestamp" in file_loop
assert "rejected_row_count" not in all_source
assert "metric_errors = []" in file_loop
assert "except Exception as metric_exc:" in file_loop
assert "WARNING metric write failed" in file_loop
assert file_loop.index("except Exception as metric_exc:") < file_loop.index(
    "except Exception as exc:"
)
print("PASS archive metrics use the canonical schema and remain non-fatal")

# Audit files can be excluded before audit-state joins and file processing.
assert "LOAD_ARCHIVE_AUDIT = False" in parameters
assert "def is_archive_audit_file(" in helpers
assert "def filter_archive_file_types(" in helpers
assert "raw_archive_files_df = discover_archive_files_dataframe(" in file_loop
assert "archive_files_df = filter_archive_file_types(" in file_loop
assert file_loop.index("archive_files_df = filter_archive_file_types(") < file_loop.index(
    'archive_audit_df = spark.table("monitoring.cfg_archive_file_load")'
)
is_audit = namespace["is_archive_audit_file"]
assert is_audit("2026-06-11.csv")
assert is_audit("audit.csv")
assert not is_audit("ipa.csv")
assert "audit_toggle_skipped" in file_loop
print("PASS archive-audit toggle filters audit files at the inventory seam")

# Folder-derived export_date is the sole contract field and must be TIMESTAMP.
# Legacy target conversion must complete before any dated/source rows are deleted.
assert "def ensure_archive_export_date_timestamp(" in helpers
assert "_source_export_date" not in all_source
assert 'F.to_timestamp(F.col("export_date"))' in helpers
assert 'option("overwriteSchema", "true")' in helpers
assert "Invalid legacy export_date values" in helpers
assert "ensure_archive_export_date_timestamp(target_object)" in file_loop
assert file_loop.index(
    "ensure_archive_export_date_timestamp(target_object)"
) < file_loop.index(
    'target_delta = DeltaTable.forName(spark, target_object)'
)
print("PASS legacy archive export_date is migrated to TIMESTAMP before replacement")

# After target migration, incoming export_date must be cast to the exact target
# Spark datatype and verified before any Delta delete occurs.
assert "def align_frame_export_date_to_target(" in helpers
assert "Incoming export_date type mismatch" in helpers
assert "frame = align_frame_export_date_to_target(frame, target_object)" in file_loop
alignment_index = file_loop.index(
    "frame = align_frame_export_date_to_target(frame, target_object)"
)
delete_index = file_loop.index(
    'target_delta = DeltaTable.forName(spark, target_object)'
)
assert alignment_index < delete_index
assert "Incoming export_date aligned" in helpers
print("PASS incoming and target export_date types align before Delta deletion")
