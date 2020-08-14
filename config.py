# set the maximum range of numbers that a cell could be. For standard sudoku, this will be 9.
ALL_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

# set the length of a row. For now, this app only supports square puzzles, i.e. with the same number of rows and cols.
ROW_LENGTH = 9

# test data is used by tests and also main (pending a mechanism to load ad-hoc data)
test_data = {
    "valid_data": "200910568000254100100000300300009600958062004074038010081040026000700800006891003",
    "bad_data_invalid_sudoku": "222910568000254100100000300302222220958062004074038010081040026000700800006891003",
    "bad_data_short": "200910500254100100000300300009600958062004074038010081040026000700800006891003",
    "bad_data_invalid_character": "2X0910568000254100100000300300009600958062004074038010081040026000700800006891003",
    "qqwing_format_data": "....1...5....93.48.2.4.5........1.6..3...4.2....9....4...1.........56.9356.2..41.",
}

# square_map is used to work out which square a given cell is in, and what the other cells in the square are.
# NOTE - this only works for a 9x9 grid. See https://github.com/rogfrich/soduku2/issues/5
square_map = {
    "0": ("00", "01", "02", "10", "11", "12", "20", "21", "22"),
    "1": ("03", "04", "05", "13", "14", "15", "23", "24", "25"),
    "2": ("06", "07", "08", "16", "17", "18", "26", "27", "28"),
    "3": ("30", "31", "32", "40", "41", "42", "50", "51", "52"),
    "4": ("33", "34", "35", "43", "44", "45", "53", "54", "55"),
    "5": ("36", "37", "38", "46", "47", "48", "56", "57", "58"),
    "6": ("60", "61", "62", "70", "71", "72", "80", "81", "82"),
    "7": ("63", "64", "65", "73", "74", "75", "83", "84", "85"),
    "8": ("66", "67", "68", "76", "77", "78", "86", "87", "88"),
}
