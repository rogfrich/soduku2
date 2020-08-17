from sudoku import Sudoku
from config import test_data

s = Sudoku(test_data["qqwing_format_data"])
s.solve()
