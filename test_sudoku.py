import pytest
import deprecated_main, config

d = deprecated_main.load_data_from_config()
g = deprecated_main.create_grid(d)

test_data = {
    "valid_data": "200910568000254100100000300300009600958062004074038010081040026000700800006891003",
    "bad_data_invalid_sudoku": "222910568000254100100000300302222220958062004074038010081040026000700800006891003",
    "bad_data_short": "200910500254100100000300300009600958062004074038010081040026000700800006891003",
    "bad_data_invalid_character": "2X0910568000254100100000300300009600958062004074038010081040026000700800006891003",
    "qqwing_format_data": "....1...5....93.48.2.4.5........1.6..3...4.2....9....4...1.........56.9356.2..41.",
}


def test_create_grid():
    """
    Test that the grid is the correct length and type.
    """
    assert len(g) == 81 and isinstance(g, dict)


def test_grid_keys():
    """
    Test that the correct grid refs are in grid.keys().
    """
    for row in range(9):
        for col in range(9):
            ref = f"{row}{col}"
            assert ref in g.keys()


def test_get_square():
    """
    Test that get_square() returns the correct square for a given cell.
    """
    assert deprecated_main.get_square("44") == "4"


def test_get_cell_refs_in_house_square():
    """
    Test that test_get_cell_refs_in_house() returns the correct cells when the mode is set to "square".
    """
    assert deprecated_main.get_cell_refs_in_house("00", "s") == [
        "01",
        "02",
        "10",
        "11",
        "12",
        "20",
        "21",
        "22",
    ]


def test_get_cell_refs_in_house_row():
    """
    Test that test_get_cell_refs_in_house() returns the correct cells when the mode is set to "row".
    """
    assert deprecated_main.get_cell_refs_in_house("00", "r") == [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
    ]


def test_get_cell_refs_in_house_col():
    """
    Test that test_get_cell_refs_in_house() returns the correct cells when the mode is set to "columns".
    """
    assert deprecated_main.get_cell_refs_in_house("00", "c") == [
        "10",
        "20",
        "30",
        "40",
        "50",
        "60",
        "70",
        "80",
    ]


def test_get_impossibles():
    """
    Test that get_impossibles() correctly returns the impossible values for a cell.
    """
    d = config.test_data["valid_data"]
    g = deprecated_main.create_grid(d)
    assert deprecated_main.get_impossibles("01", test_grid=g) == {
        "1",
        "2",
        "5",
        "6",
        "7",
        "8",
        "9",
    }


def test_get_possibles():
    """
    Test that get_possibles() correctly returns the possible values for a cell.
    """
    d = config.test_data["valid_data"]
    g = deprecated_main.create_grid(d)
    assert deprecated_main.get_possibles("01", test_grid=g) == {"3", "4"}


def test_get_solved_cells():
    """
    Test that get_solved_cells returns the correct number for the test data, and that cell 00 (solved) is returned and cell 01 (not solved) isn't.
    """
    d = config.test_data["valid_data"]
    g = deprecated_main.create_grid(d)
    sc = deprecated_main.get_solved_cells(test_grid=g)
    assert len(sc) == 38 and "00" in sc and not "01" in sc


def test_clarify_all_cells():
    """
    Test that clarify_all_cells() is actually updating the grid.
    """
    solved_before = len(deprecated_main.get_solved_cells())
    deprecated_main.clarify_all_cells()
    solved_after = len(deprecated_main.get_solved_cells())
    assert solved_after > solved_before


def test_validate_data_short():
    """
    Test that validate_data() raises an exception if the supplied data is not 81 chars long.
    """
    with pytest.raises(AssertionError):
        d = config.test_data["bad_data_short"]
        deprecated_main.validate_data(d)


def test_validate_data_non_numeric():
    """
    Test that  validate_data() raises an exception if a non-numeric char is present in the data.
    """
    with pytest.raises(AssertionError):
        d = config.test_data["bad_data_invalid_character"]
        deprecated_main.validate_data(d)


def test_validate_data_valid():
    """
    Test that validate_data() does not raise an exception if the data is valid.
    """
    d = config.test_data["valid_data"]
    deprecated_main.validate_data(d)


def test_convert_qqwing_data_to_standard_format():
    """
    Test that convert_qqwing_to_standard_format() returns a correctly formatted string.
    """
    d = config.test_data["qqwing_format_data"]
    converted_data = deprecated_main.convert_qqwing_to_standard_format(d)
    assert len(converted_data) == 81
    assert "." not in converted_data
