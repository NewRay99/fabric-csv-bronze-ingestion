"""Run the maintained Python/notebook validators, not client Power BI projects."""

from pathlib import Path
import subprocess
import sys

import pytest


TEST_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = TEST_DIRECTORY.parents[1]
# Explicit opt-in prevents a newly added client/version-specific report or
# semantic-model validator from silently joining the normal Python test suite.
# Obsolete Power BI test files have been removed, not just excluded from pytest.
PYTHON_VALIDATORS = (
    "validate_archive_framework_fallback.py",
    "validate_archive_load.py",
    "validate_archive_snapshot_and_enrichment.py",
    "validate_cfg_setup.py",
    "validate_cfg005_contract_source_rows.py",
    "validate_common_library_lint.py",
    "validate_core_pipeline.py",
    "validate_data_domain.py",
    "validate_gld015_reject_reason_dimension.py",
    "validate_gld016_provider_kpi_offer_keys.py",
    "validate_gold_referral_schema.py",
    "validate_job_run_lineage.py",
    "validate_live_pipeline_monitoring.py",
    "validate_monitoring_views.py",
    "validate_notebook_integration.py",
    "validate_ref_exclusions.py",
    "validate_referral_lifecycle_events.py",
    "validate_referral_provider_rollup.py",
    "validate_schema_drift_dimensions.py",
    "validate_schema_drift.py",
    "validate_si007_materialisations.py",
    "validate_si013_si016.py",
    "validate_si022_source_schema_contract.py",
    "validate_silver_required_columns.py",
    "validate_table_naming_and_archive_runner.py",
)
VALIDATORS = sorted(TEST_DIRECTORY / name for name in PYTHON_VALIDATORS)


@pytest.mark.parametrize("validator", VALIDATORS, ids=lambda path: path.stem)
def test_validator(validator):
    """Each opted-in Python validator must pass from the repository root."""
    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        print(f"PASS: {validator.name}")
        return

    print(f"FAIL: {validator.name}")
    assert result.returncode == 0, (
        f"{validator.name} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
