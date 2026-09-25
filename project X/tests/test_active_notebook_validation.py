"""Notebook regressions must not depend on optional client report snapshots."""

from pathlib import Path
import shutil
import subprocess
import sys

import pytest


PROJECT = Path(__file__).resolve().parents[1]
VALIDATORS = (
    ("validate_gld015_reject_reason_dimension.py", "05_gold_dimensions.py"),
    ("validate_gold_referral_schema.py", "04_gold_model.py"),
    ("validate_job_run_lineage.py", "90_run_live_pipeline.py"),
    ("validate_silver_required_columns.py", "99_common_library.py"),
)


@pytest.mark.parametrize("validator,required_notebook", VALIDATORS)
def test_validates_active_notebooks_without_client_snapshots(
    tmp_path, validator, required_notebook
):
    project = tmp_path / "project X"
    inputs = list(PROJECT.glob("[0-9]*.py")) + [
        PROJECT / "tests" / validator,
        PROJECT / "tests/notebook_loader.py",
        PROJECT / "tests/_gold_sim_test.py",
        PROJECT / "tests/_gold_fact_sql.sql",
        PROJECT / "tools/fabric_notebooks.py",
        PROJECT / "configuration/schema_definition.csv",
        PROJECT / "change tracking/ETL_ISSUE_LOG.md",
        PROJECT / "change tracking/ETL_CHANGE_LOG.md",
    ]
    for original in inputs:
        destination = project / original.relative_to(PROJECT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(original, destination)
    assert not (project / "reports").exists()

    def run_validator():
        return subprocess.run(
            [sys.executable, str(project / "tests" / validator)],
            cwd=tmp_path, capture_output=True, text=True, check=False,
        )

    result = run_validator()
    assert result.returncode == 0, result.stdout + result.stderr
    # A missing active input must still fail, rather than silently skip checks.
    (project / required_notebook).rename(project / f"{required_notebook}.unavailable")
    result = run_validator()
    assert result.returncode != 0
    assert "FileNotFoundError" in result.stderr
    assert required_notebook in result.stderr
