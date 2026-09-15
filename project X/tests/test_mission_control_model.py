"""Check Desktop save compatibility without hiding meaningful model changes."""

import pytest

from validate_mission_control_model import comparable_tmdl, validate_measures_table


TABLE = (
    "table _MissionControl_Measures\n"
    "\n\tmeasure 'Status Label' = ```\n"
    '\n\t\t\tIF ( [Runs] > 0, "In progress", "Not started" )\n'
    "\n\t\t\t```\n"
    "\t\tformatString: 0\n"
    "\t\tdisplayFolder: Control health\n"
    "\n\tpartition _MissionControl_Measures = m\n"
    "\t\tmode: import\n"
    "\t\tsource =\n"
    "\t\t\t\t#table ( type table [], {} )\n"
)


def test_desktop_save_metadata_and_whitespace_are_accepted():
    saved = TABLE.replace(
        "table _MissionControl_Measures\n",
        "table _MissionControl_Measures\n\tlineageTag: table-id\n",
        1,
    ).replace(
        "\t\tformatString: 0\n",
        "\t\tformatString: 0\n\t\tlineageTag: measure-id\n",
    ).replace(
        "\t\tsource =\n\t\t\t\t", "\t\tsource = "
    ).replace("\n\n", "\n\t\t\t\n").replace("\n", "\r\n")
    assert comparable_tmdl(TABLE) == comparable_tmdl(saved)


@pytest.mark.parametrize(
    ("old", "new"),
    [
        ("[Runs] > 0", "[Runs] > 1"),
        ('"In progress"', '"In  progress"'),
        ("measure 'Status Label'", "measure 'Different Label'"),
        ("formatString: 0", "formatString: 0.0%"),
        ("mode: import", "mode: directQuery"),
        ("type table [], {}", "type table [], {{}}"),
    ],
)
def test_meaningful_changes_are_detected(old, new):
    assert comparable_tmdl(TABLE) != comparable_tmdl(TABLE.replace(old, new))


def test_missing_partition_still_fails(tmp_path):
    path = tmp_path / "measures.tmdl"
    path.write_text(TABLE.split("\n\tpartition", 1)[0], encoding="utf-8")
    with pytest.raises(AssertionError, match="one explicit Import partition"):
        validate_measures_table(path)
