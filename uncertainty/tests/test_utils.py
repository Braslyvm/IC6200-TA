import pytest

from utils import load_data


def test_load_data_parses_people_from_csv(tmp_path):
    csv_file = tmp_path / "family.csv"
    csv_file.write_text(
        "name,mother,father,trait\n"
        "Harry,Lily,James,\n"
        "James,,,1\n"
        "Lily,,,0\n"
        "Molly,,,\n",
        encoding="utf-8",
    )

    assert load_data(str(csv_file)) == {
        "Harry": {
            "name": "Harry",
            "mother": "Lily",
            "father": "James",
            "trait": None,
        },
        "James": {
            "name": "James",
            "mother": None,
            "father": None,
            "trait": True,
        },
        "Lily": {
            "name": "Lily",
            "mother": None,
            "father": None,
            "trait": False,
        },
        "Molly": {
            "name": "Molly",
            "mother": None,
            "father": None,
            "trait": None,
        },
    }


@pytest.mark.parametrize(
    (
        "mother",
        "father",
        "trait",
        "expected_mother",
        "expected_father",
        "expected_trait",
    ),
    [
        ("", "", "1", None, None, True),
        ("", "", "0", None, None, False),
        ("", "", "", None, None, None),
        ("Alice", "Bob", "1", "Alice", "Bob", True),
        ("Alice", "Bob", "0", "Alice", "Bob", False),
        ("Alice", "Bob", "", "Alice", "Bob", None),
    ],
)
def test_load_data_parses_parent_and_trait_combinations(
    tmp_path,
    mother,
    father,
    trait,
    expected_mother,
    expected_father,
    expected_trait,
):
    csv_file = tmp_path / "family.csv"
    csv_file.write_text(
        f"name,mother,father,trait\nPerson,{mother},{father},{trait}\n",
        encoding="utf-8",
    )

    assert load_data(str(csv_file)) == {
        "Person": {
            "name": "Person",
            "mother": expected_mother,
            "father": expected_father,
            "trait": expected_trait,
        }
    }


def test_load_data_handles_parent_rows_before_and_after_children(tmp_path):
    csv_file = tmp_path / "family.csv"
    csv_file.write_text(
        "name,mother,father,trait\n"
        "Lily,,,0\n"
        "James,,,1\n"
        "Harry,Lily,James,\n"
        "Rose,Ron,Hermione,1\n"
        "Ron,,,0\n"
        "Hermione,,,\n",
        encoding="utf-8",
    )

    assert load_data(str(csv_file)) == {
        "Lily": {
            "name": "Lily",
            "mother": None,
            "father": None,
            "trait": False,
        },
        "James": {
            "name": "James",
            "mother": None,
            "father": None,
            "trait": True,
        },
        "Harry": {
            "name": "Harry",
            "mother": "Lily",
            "father": "James",
            "trait": None,
        },
        "Rose": {
            "name": "Rose",
            "mother": "Ron",
            "father": "Hermione",
            "trait": True,
        },
        "Ron": {
            "name": "Ron",
            "mother": None,
            "father": None,
            "trait": False,
        },
        "Hermione": {
            "name": "Hermione",
            "mother": None,
            "father": None,
            "trait": None,
        },
    }


def test_load_data_parses_mixed_family_combinations_in_one_csv(tmp_path):
    csv_file = tmp_path / "family.csv"
    csv_file.write_text(
        "name,mother,father,trait\n"
        "Ada,,,1\n"
        "Grace,,,0\n"
        "Alan,,,\n"
        "ChildTrue,Ada,Alan,1\n"
        "ChildFalse,Ada,Alan,0\n"
        "ChildUnknown,Grace,Alan,\n",
        encoding="utf-8",
    )

    assert load_data(str(csv_file)) == {
        "Ada": {
            "name": "Ada",
            "mother": None,
            "father": None,
            "trait": True,
        },
        "Grace": {
            "name": "Grace",
            "mother": None,
            "father": None,
            "trait": False,
        },
        "Alan": {
            "name": "Alan",
            "mother": None,
            "father": None,
            "trait": None,
        },
        "ChildTrue": {
            "name": "ChildTrue",
            "mother": "Ada",
            "father": "Alan",
            "trait": True,
        },
        "ChildFalse": {
            "name": "ChildFalse",
            "mother": "Ada",
            "father": "Alan",
            "trait": False,
        },
        "ChildUnknown": {
            "name": "ChildUnknown",
            "mother": "Grace",
            "father": "Alan",
            "trait": None,
        },
    }
