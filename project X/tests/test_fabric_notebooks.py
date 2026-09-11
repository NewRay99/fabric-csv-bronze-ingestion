"""Exercise the Fabric format boundary, independently of business validators."""

import ast
from pathlib import Path

import pytest

from notebook_loader import load_notebook
from fabric_notebooks import (
    cell_contract,
    fabric_metadata,
    parse_fabric_source,
    semantic_cells,
    to_fabric_source,
)


PROJECT = Path(__file__).resolve().parents[1]


def test_read_fabric_cells_parameters_markdown_and_sql():
    # Handwritten Fabric fixture, not produced by the serializer under test.
    source = '''# Fabric notebook source
# METADATA ********************
# META {"kernel_info": {"name": "synapse_pyspark"}, "dependencies": {}}
# MARKDOWN ********************
# # Heading
#
# Text with # and Unicode: café.
# PARAMETERS CELL ********************
MONTH = ""
# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}
# CELL ********************
%run ./99_common_library
# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}
# CELL ********************
# MAGIC %%sql
# MAGIC SELECT 'a  b' AS value;
# METADATA ********************
# META {"language": "sparksql", "language_group": "synapse_pyspark"}
# CELL ********************
if MONTH:
    print(MONTH)
# METADATA ********************
# META {"language": "python", "language_group": "synapse_pyspark"}
'''
    notebook = parse_fabric_source("\ufeff" + source.replace("\n", "\r\n"))
    assert semantic_cells(notebook, "markdown") == ["# Heading\n\nText with # and Unicode: café."]
    assert semantic_cells(notebook, "code") == [
        'MONTH = ""', "%run ./99_common_library",
        "%%sql\nSELECT 'a  b' AS value;", "if MONTH:\n    print(MONTH)",
    ]
    assert notebook["cells"][1]["metadata"]["tags"] == ["parameters"]
    assert notebook["cells"][3]["metadata"]["microsoft"]["language"] == "sparksql"
    restored = parse_fabric_source(to_fabric_source(notebook))
    assert restored == notebook


def test_conversion_omits_execution_data_but_preserves_configuration():
    notebook = {
        "nbformat": 4,
        "metadata": {
            "kernel_info": {"name": "synapse_pyspark"},
            "dependencies": {"environment": {"environmentId": "test-environment"}},
            "spark_compute": {"session_options": {"conf": {"timeout": "7200000"}}},
            "synapse_widget": {"state": "EXECUTION_DATA_SENTINEL"},
        },
        "cells": [{
            "cell_type": "code", "source": ['VALUE = "café"\n'],
            "metadata": {"tags": ["parameters"], "advisor": "EXECUTION_DATA_SENTINEL"},
            "outputs": [{"text": "EXECUTION_DATA_SENTINEL"}], "execution_count": 99,
        }],
    }
    text = to_fabric_source(notebook)
    assert "EXECUTION_DATA_SENTINEL" not in text
    assert "execution_count" not in text
    assert "# PARAMETERS CELL ********************" in text
    parsed = parse_fabric_source(text)
    assert parsed["metadata"] == fabric_metadata(notebook)
    assert semantic_cells(parsed, "code") == ['VALUE = "café"']


def test_explicit_python_path_never_falls_back_to_original_ipynb(tmp_path):
    (tmp_path / "example.ipynb").write_text('{"nbformat": 4, "cells": []}')
    with pytest.raises(FileNotFoundError):
        load_notebook(tmp_path / "example.py")


@pytest.mark.parametrize("source", ["", "print('ordinary script')", "# Fabric notebook source\n"])
def test_invalid_source_is_rejected(source):
    with pytest.raises(ValueError):
        parse_fabric_source(source)


def test_unsupported_cells_are_rejected():
    with pytest.raises(ValueError, match="Unsupported cell type"):
        to_fabric_source({"nbformat": 4, "cells": [{"cell_type": "raw", "source": "raw"}]})


# Primary sources are numbered .py files in the development repo; in the
# deployed client repo they are notebooks/<name>.Notebook directories.
PRIMARY_NOTEBOOKS = sorted(PROJECT.glob("[0-9]*.py")) or sorted(
    (PROJECT / "notebooks").glob("[0-9]*.Notebook")
)


@pytest.mark.parametrize("path", PRIMARY_NOTEBOOKS, ids=lambda p: p.stem)
def test_primary_notebook_structure_and_python_syntax(path):
    notebook = load_notebook(path)
    assert notebook["cells"], f"No cells in {path.name}"
    assert notebook["metadata"]["kernel_info"]["name"] == "synapse_pyspark"
    restored = parse_fabric_source(to_fabric_source(notebook))
    assert restored["metadata"] == notebook["metadata"]
    assert cell_contract(restored) == cell_contract(notebook)
    for kind in ("code", "markdown"):
        assert semantic_cells(restored, kind) == semantic_cells(notebook, kind)
    for index, cell in enumerate(notebook["cells"]):
        source = "".join(cell["source"])
        if cell["cell_type"] == "code" and not source.lstrip().startswith("%"):
            ast.parse(source, filename=f"{path.name}:cell-{index}")
