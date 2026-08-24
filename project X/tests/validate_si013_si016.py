"""Regression checks for SI-013 through SI-016 shared-library and replay controls."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECT = ROOT / "project X"
COMMON = PROJECT / "99_common_library.ipynb"
SETUP = PROJECT / "00_setup_cfg.ipynb"
ARCHIVE_REPLAY = PROJECT / "02a_archive_silver.ipynb"
ARCHIVE_RUNNER = PROJECT / "90_run_archive_pipeline.ipynb"
LATEST_SILVER = PROJECT / "02_silver_formatter.ipynb"


def source(path):
    notebook = json.loads(path.read_text(encoding="utf-8"))
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def main():
    common = source(COMMON)
    required_common_symbols = {
        "etl_logical_table_name",
        "is_etl_excluded_table",
        "excluded_etl_tables",
        "qident",
        "normalise",
        "append_rows",
        "map_data_type",
        "cast_column",
        "resolve_contract",
        "format_frame",
    }
    missing_common = sorted(
        symbol for symbol in required_common_symbols
        if f"def {symbol}" not in common
    )
    assert not missing_common, f"Common library is missing: {missing_common}"
    print("PASS common library is valid and owns shared helpers")

    for notebook in PROJECT.glob("*.ipynb"):
        if notebook.name in {COMMON.name, "common_util.ipynb"}:
            continue
        text = source(notebook)
        assert "%run common_util" not in text, f"{notebook.name} still imports common_util"
    print("PASS project notebooks no longer import common_util")

    setup = source(SETUP)
    assert "silver.referral_event_log" not in setup, (
        "Setup must not fabricate a source event-log table"
    )
    print("PASS setup does not fabricate a referral event-log source")

    archive = source(ARCHIVE_REPLAY)
    for token in [
        "PROCESS_ONLY", "RESET_MONTH_MONITORING",
        "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY", "CONFIRM_PROCESS_ONLY_RESET",
        "YYYY-MM", "REFRESH MONTH",
    ]:
        assert token in archive, f"Archive replay lacks SI-014 control: {token}"
    assert 'datetime.strptime(PROCESS_ONLY, "%Y-%m")' in archive
    assert 'expected_confirmation = f"RESET {PROCESS_ONLY}"' in archive
    assert "elif CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY:" in archive, (
        "Clearing Silver targets must flag the archive-month monitoring state "
        "for reload so the replay is not skipped as already successful"
    )
    assert "DELETE FROM monitoring.cfg_month_end_gold_run" in archive
    assert "UPDATE monitoring.cfg_month_end_gold_run" in archive
    assert "UPDATE monitoring.cfg_silver_export_load" in archive
    assert "SET reload = true, last_updated_at = current_timestamp()" in archive
    assert "FLAGGED monitoring state for reload" in archive
    assert "DROP TABLE IF EXISTS {target_table}" in archive
    print("PASS archive replay exposes guarded single-month tracing controls")

    archive_runner = source(ARCHIVE_RUNNER)
    for token in [
        "ARCHIVE_PROCESS_ONLY",
        "CLEAR_SILVER_TABLES_FOR_PROCESS_ONLY",
        "CONFIRM_PROCESS_ONLY_RESET",
        '"PROCESS_ONLY": ARCHIVE_PROCESS_ONLY',
    ]:
        assert token in archive_runner, (
            f"Archive runner does not forward single-month reload control: {token}"
        )
    print("PASS archive runner forwards guarded reload controls to Archive Silver")

    latest = source(LATEST_SILVER)
    for duplicate in ["def qident", "def normalise", "def map_data_type", "def cast_column", "def format_frame"]:
        assert duplicate not in latest, f"Latest Silver still defines common helper {duplicate}"
    assert "%run ./99_common_library" in latest, "Latest Silver does not import the common library"
    print("PASS latest Silver uses common conformance helpers")

    print("VALIDATION PASSED")


if __name__ == "__main__":
    main()
