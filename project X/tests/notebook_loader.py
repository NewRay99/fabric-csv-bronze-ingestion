"""Shared Fabric source reader for standalone validators and pytest."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from fabric_notebooks import load_notebook  # noqa: E402, F401
