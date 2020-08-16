import pytest
from sudoku import Sudoku
from config import test_data

def test_create_grid():
    """
    Test that the grid is the correct length and type.
    """
    s = Sudoku(test_data['valid_data'])
    assert len(s.grid) == 81
    assert isinstance(s.grid, dict)

def test_grid_keys():
    """
    Test that the keys in .grid are correct.
    """
    s = Sudoku(test_data['valid_data'])
    for row in range(9):
        for col in range(9):
            ref = f'{row}{col}'
            assert ref in s.grid.keys()

def test_get_square():
    """
    Test that get_square() returns the correct square for a given cell.
    """
    s = Sudoku(test_data['valid_data'])
    assert s.get_square("44") == "4"

def test_get_cell_refs_in_house_square():
    """
    Test that test_get_cell_refs_in_house() returns the correct cells when the mode is set to "square".
    """
    s = Sudoku(test_data['valid_data'])
    related_cells = []
    for mode in 'rcs':
        house = s.get_related_cells('00', mode=mode)
        for cell in house:
            if cell not in related_cells:
                related_cells.append(cell)

    correct_cells = [
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "10",
        "20",
        "30",
        "40",
        "50",
        "60",
        "70",
        "80",
        "11",
        "12",
        "21",
        "22",
    ]
    for cell in correct_cells:
        assert cell in related_cells


def test_get_impossibles():
    """
    Test that get_impossibles() correctly returns the impossible values for a cell.
    """
    s = Sudoku(test_data['valid_data'])

    assert s.get_impossibles("01") == {
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
    s = Sudoku(test_data['valid_data'])
    assert s.get_possibles("01") == {"3", "4"}

def test_get_solved_cells():
    """
    Test that get_solved_cells returns the correct number for the test data, and that cell 00 (solved) is returned and cell 01 (not solved) isn't.
    """
    s = Sudoku(test_data['valid_data'])
    sc = s.solved_cells
    assert len(sc) == 38 and "00" in sc and "01" not in sc

def test_clarify_all_cells():
    """
    Test that clarify_all_cells() affects a solvable cell
    """
    s = Sudoku(test_data['valid_data'])
    before = len(s.solved_cells)
    s.clarify_all_cells()
    after = len(s.solved_cells)
    assert after > before


def test_solve():
    """
    Test that solve() is actually updating the grid.
    """
    s = Sudoku(test_data['valid_data'])
    solved_before = len(s.solved_cells)
    s.solve()
    solved_after = len(s.solved_cells)
    assert solved_after > solved_before

def test_clean_data_short():
    """
    Test that clean_data() raises an exception if the supplied data is not 81 chars long.
    """
    with pytest.raises(AssertionError):
        s = Sudoku(test_data['bad_data_short'])

def test_clean_data_non_numeric():
    """
    Test that  clean_data() raises an exception if a non-numeric char is present in the data.
    """
    with pytest.raises(ValueError):
        s = Sudoku(test_data['bad_data_invalid_character'])


def test_clean_data_valid():
    """
    Test that clean_data() does not raise an exception if the data is valid.
    """
    s = Sudoku(test_data['valid_data'])

def test_clean_data_qqwing_format():
    """
    Test that convert_qqwing_to_standard_format() returns a correctly formatted string.
    """
    s = Sudoku(test_data['valid_data'])
    assert len(s.data) == 81 and "." not in s.data

def test_create_snapshot():
    """
    Test that create_snapshot() correctly creates a copy of the grid.
    """
    s = Sudoku(test_data['valid_data'])
    start = s.create_snapshot()
    assert start == s.grid

def test_create_snapshot_is_different_to_grid_after_update():
    """
    Test that once the grid is updated, create_snapshot() does not equal self.grid
    """
    s = Sudoku(test_data['valid_data'])
    start = s.create_snapshot()
    s.clarify_all_cells()
    assert start != s.grid

def test_solve_raises_exception_if_grid_does_not_change():
    """
    Test that once the grid is updated, create_snapshot() does not equal self.grid
    """
    import exceptions
    s = Sudoku(test_data['bad_data_invalid_sudoku'])
    with pytest.raises(exceptions.UnableToSolveError):
        s.solve()