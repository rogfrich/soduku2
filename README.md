# soduku2

## About
A basic sudoku solver. Currently uses the following logic:
1. A cell is considered solved if there is exactly one possible value
1. For each unsolved cell, work out what the possible values are (by looking at the solved cells around it), and update the cell
1. Repeat until all the cells are solved.

Future iterations will implement more advanced solving logic, but this works for the "easy" sudokus I've tested it with.

## Data format
Sudokus are represented as a string, 81 characters long (for the 81 cells in a sudoku). Empty cells are represented as a "0".
The size of the grid is set by the `row_length` constant in `config.py` - although only 9x9 grids are supported at present, there's an intention to support variable-size grids in the future.

## Terminology
I use the following terms in this code:
- `cell`: a single space in the puzzle. It will either have a value of 1 to 9 (i.e. has been answered) or will be empty.
- `ref`: the identifier for a given cell. A string in the format `f"{row}{col}"`.  "05" is row 0, col 5. Rows start counting from the top. Columns start counting from the left. 
- `row`: a horizontal row.
- `col`: a vertical column.
- `square`: one of the nine 3x3 squares in the grid, which will hold the numbers 1-9 (once the puzzle is solved). Squares are numbered 1 to 9 (as strings). Square 0 is top-left, Square 1 is top-middle. Square 8 is bottom-right.
- `house`: A generic term for rows, cols and squares. Don't blame me; I didn't make it up.
- `clarify`: work out what the possible values for a given square are based on the other squares in its houses.

## App lifecycle
This app is mainly a test-bed for concepts and techniques I learn as I study Python. As such, it tends to get completely gutted and rewritten from time to time. Breaking changes are frequent, severe... and completely unapologetic. :-)

For this reason, I deliberately haven't licensed the app - it's not really meant for any sort of use other than my own learning, and I don't really want to be on the hook for supporting it in the wild. In the unlikely circumstance that someone wants to use this code, feel free to raise an issue and we can sort something out (which might just be me biting the bullet and giving it a proper license).

Cheers!