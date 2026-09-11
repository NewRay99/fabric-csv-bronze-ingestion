"""Pytest bootstrap: keep the temp base inside the repo.

On machines where %TEMP%\\pytest-of-<user> was created by an elevated
process, the directory is unreadable afterwards and every tmp_path
fixture fails with PermissionError (WinError 5). Pointing basetemp at a
repo-local directory keeps the suite runnable everywhere.
.pytest_tmp/ can be deleted at any time; it is git-ignored.
"""

from pathlib import Path


def pytest_configure(config):
    if getattr(config.option, "basetemp", None) is None:
        config.option.basetemp = str(Path(config.rootdir) / ".pytest_tmp")
