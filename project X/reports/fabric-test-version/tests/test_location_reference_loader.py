"""Offline loader guards; no live reference data, Fabric writes or network access."""

import ast
import math
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tempfile
from types import SimpleNamespace
from unittest.mock import Mock, patch
import zipfile

import pytest

from notebook_loader import load_notebook


PATH = Path(__file__).resolve().parents[1] / "00c_load_location_coordinates.py"
NOTEBOOK = load_notebook(PATH)
SOURCE = "\n".join("".join(c["source"]) for c in NOTEBOOK["cells"] if c["cell_type"] == "code")


def helpers():
    functions = [n for n in ast.parse(SOURCE).body if isinstance(n, ast.FunctionDef)]
    scope = {
        "math": math,
        "os": os,
        "re": re,
        "PurePosixPath": PurePosixPath,
        "Path": Path,
        "shutil": shutil,
        "stat": stat,
        "tempfile": tempfile,
        "zipfile": zipfile,
    }
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(PATH), "exec"), scope)
    return scope


@pytest.mark.parametrize(
    "path",
    [
        "https://example.com/postcodes.csv",
        "abfss://external/coordinates.csv",
        "Files/cfg_files/location_reference/../../private.csv",
        "C:/temp/reference.csv",
        "Files/cfg_files/location_reference/..\\private.csv",
    ],
)
def test_external_or_escaping_paths_rejected(path):
    with pytest.raises(ValueError):
        helpers()["local_reference_path"](path)


def test_local_reference_path_and_string_false():
    functions = helpers()
    local = "Files/cfg_files/location_reference/code_point/Data/CSV"
    assert functions["local_reference_path"](local) == local
    assert functions["parameter_bool"]("false") is False
    assert functions["parameter_bool"]("True") is True
    with pytest.raises(ValueError):
        functions["parameter_bool"]("enable")
    assert functions["postcode_key"](" b1  1AA ") == "B11AA"


@pytest.mark.parametrize(
    "coords", [(None, 100), (0, 0), (float("nan"), 100), (400000, float("inf")), (800000, 100000)]
)
def test_bad_grid_points_rejected(coords):
    assert helpers()["valid_grid_point"](*coords) is False


def test_conversion_axis_order_and_range_guards():
    transformer = Mock()
    transformer.transform.return_value = (-1.9, 52.5)
    assert helpers()["convert_grid_point"](transformer, 407000, 287000) == (52.5, -1.9)
    transformer.transform.assert_called_once_with(407000.0, 287000.0, errcheck=True)
    transformer.transform.return_value = (float("inf"), 52.5)
    with pytest.raises(ValueError):
        helpers()["convert_grid_point"](transformer, 407000, 287000)


def test_projection_network_disabled_and_no_ballpark_fallback(monkeypatch):
    monkeypatch.setenv("PROJ_NETWORK", "ON")
    transform = SimpleNamespace(
        accuracy=2, description="local transform", definition="local pipeline"
    )
    group = Mock(return_value=SimpleNamespace(transformers=[transform]))
    network = SimpleNamespace(set_network_enabled=Mock())
    module = SimpleNamespace(network=network, __version__="test", proj_version_str="test")
    with patch.dict(
        "sys.modules",
        {
            "pyproj": module,
            "pyproj.transformer": SimpleNamespace(TransformerGroup=group),
        },
    ):
        chosen, provenance = helpers()["offline_transformer"]()
        assert chosen is transform and "accuracy 2m" in provenance
        assert os.environ["PROJ_NETWORK"] == "OFF"
        network.set_network_enabled.assert_called_once_with(False)
        group.assert_called_once_with(
            "EPSG:27700", "EPSG:4326", always_xy=True, allow_ballpark=False
        )
        group.return_value = SimpleNamespace(transformers=[SimpleNamespace(accuracy=-1)])
        with pytest.raises(RuntimeError, match="No installed"):
            helpers()["offline_transformer"]()


def test_preview_merge_and_source_contract():
    tree = ast.parse(SOURCE)
    values = {
        n.targets[0].id: ast.literal_eval(n.value)
        for n in tree.body
        if isinstance(n, ast.Assign)
        and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id in {"APPLY_CHANGES", "UPDATE_EXISTING"}
    }
    assert values == {"APPLY_CHANGES": False, "UPDATE_EXISTING": False}
    write_gate = next(
        n
        for n in tree.body
        if isinstance(n, ast.If) and isinstance(n.test, ast.Name) and n.test.id == "apply_changes"
    )
    assert "whenNotMatchedInsert" in ast.unparse(write_gate)
    assert "t.latitude IS NULL AND t.longitude IS NULL" in SOURCE
    assert ".isin(10, 20, 30, 40, 50)" in SOURCE
    assert '"City", "Town"' in SOURCE
    assert '"left_anti"' in SOURCE  # Ambiguous place keys are not chosen arbitrarily.
    assert '"silver.provider_home"' in SOURCE
    imported = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    assert not imported.intersection({"requests", "urllib", "httpx", "socket"})
    for forbidden in ("download_grids", "%pip", "address_line_1"):
        assert forbidden not in SOURCE


@pytest.mark.parametrize(
    ("dataset", "filename", "tile"),
    [
        ("code_point", "codepo_gb.zip", "delivery/Data/CSV/b.csv"),
        ("open_names", "opname_csv_gb.zip", "Data/SP00.csv"),
    ],
)
def test_zip_extracts_only_data_and_preserves_source(tmp_path, dataset, filename, tile):
    reference = tmp_path / "Files/cfg_files/location_reference"
    reference.mkdir(parents=True)
    archive_path = reference / filename
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr(tile, "sample,10,400000,300000\n")
        archive.writestr("Doc/OS_Headers.csv", "not,data\n")
        archive.writestr("Data/headers.csv", "not,data\n")
        archive.writestr("Readme.txt", "licence retained in source")
    original = archive_path.read_bytes()
    prepare = helpers()["prepare_reference_input"]
    result = prepare(f"Files/cfg_files/location_reference/{filename}", dataset, tmp_path)
    extracted = tmp_path / result
    tiles = list(extracted.rglob("*.csv"))
    assert len(tiles) == 1
    assert tiles[0].read_text() == "sample,10,400000,300000\n"
    assert archive_path.read_bytes() == original
    assert not list(extracted.rglob("*.txt"))
    second = prepare(f"Files/cfg_files/location_reference/{filename}", dataset, tmp_path)
    assert second != result  # No overwriting a prior run or user-managed data.


@pytest.mark.parametrize(
    "bad_member", ["../escape.csv", "/escape.csv", "Data/../bad.csv", "C:/bad.csv"]
)
def test_unsafe_zip_members_rejected(tmp_path, bad_member):
    reference = tmp_path / "Files/cfg_files/location_reference"
    reference.mkdir(parents=True)
    with zipfile.ZipFile(reference / "bad.zip", "w") as archive:
        archive.writestr("Data/CSV/b.csv", "data")
        archive.writestr(bad_member, "data")
    with pytest.raises(ValueError, match="Unsafe"):
        helpers()["prepare_reference_input"](
            "Files/cfg_files/location_reference/bad.zip", "code_point", tmp_path
        )
    assert not (reference / "_extracted").exists()


def test_zip_missing_data_and_duplicate_tiles_rejected(tmp_path):
    reference = tmp_path / "Files/cfg_files/location_reference"
    reference.mkdir(parents=True)
    prepare = helpers()["prepare_reference_input"]
    for members, message in [
        (["Doc/headers.csv"], "No code_point"),
        (["first/Data/CSV/b.csv", "second/Data/CSV/b.csv"], "Duplicate"),
    ]:
        with zipfile.ZipFile(reference / "bad.zip", "w") as archive:
            for member in members:
                archive.writestr(member, "data")
        with pytest.raises(ValueError, match=message):
            prepare("Files/cfg_files/location_reference/bad.zip", "code_point", tmp_path)


def test_existing_extracted_directory_still_supported():
    value = "Files/cfg_files/location_reference/code_point/Data/CSV"
    assert helpers()["prepare_reference_input"](value, "code_point") == value
