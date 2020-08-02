import pytest
import main, config

d = main.load_data_from_config()
g = main.create_grid(d)


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
    assert main.get_square("44") == "4"


def test_get_cell_refs_in_house_square():
    """
    Test that test_get_cell_refs_in_house() returns the correct cells when the mode is set to "square".
    """
    assert main.get_cell_refs_in_house("00", "s") == [
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
    assert main.get_cell_refs_in_house("00", "r") == [
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
    assert main.get_cell_refs_in_house("00", "c") == [
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
    assert main.get_impossibles("01") == set(["1", "2", "5", "6", "7", "8", "9"])


def test_get_possibles():
    """
    Test that get_possibles() correctly returns the possible values for a cell.
    """
    assert main.get_possibles("01") == set(["3", "4"])


def test_get_solved_cells():
    """
    Test that get_solved_cells returns the correct number for the test data, and that cell 00 (solved) is returned and cell 01 (not solved) isn't.
    """
    sc = main.get_solved_cells()
    assert len(sc) == 38 and "00" in sc and not "01" in sc


def test_clarify_all_cells():
    """
    Test that clarify_all_cells() is actually updating the grid.
    """
    solved_before = len(main.get_solved_cells())
    main.clarify_all_cells()
    solved_after = len(main.get_solved_cells())
    assert solved_after > solved_before


def test_validate_data_short():
    """
    Test that validate_data() raises an exception if the supplied data is not 81 chars long.
    """
    with pytest.raises(AssertionError):
        d = config.bad_data_short
        main.validate_data(d)


def test_validate_data_non_numeric():
    """
    Test that  validate_data() raises an exception if a non-numeric char is present in the data.
    """
    with pytest.raises(AssertionError):
        d = config.bad_data_invalid_character
        main.validate_data(d)


def test_validate_data_valid():
    """
    Test that validate_data() does not raise an exception if the data is valid.
    """
    d = config.valid_data
    main.validate_data(d)