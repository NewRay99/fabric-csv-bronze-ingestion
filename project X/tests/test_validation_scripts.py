"""Expose the existing portable validation scripts to pytest."""

from pathlib import Path
import subprocess
import sys

import pytest


TEST_DIRECTORY = Path(__file__).resolve().parent
REPOSITORY_ROOT = TEST_DIRECTORY.parents[1]
VALIDATORS = sorted(TEST_DIRECTORY.glob("validate_*.py"))


@pytest.mark.parametrize("validator", VALIDATORS, ids=lambda path: path.stem)
def test_validator(validator):
    """Each standalone validation script must pass from the repository root."""
    result = subprocess.run(
        [sys.executable, str(validator)],
        cwd=REPOSITORY_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, (
        f"{validator.name} failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    )
