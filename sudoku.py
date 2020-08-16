import copy

import config
from exceptions import UnableToSolveError


class Sudoku:
    def __init__(self, init_data):
        self.init_data = init_data
        self.data = self.clean_data()
        self.grid = self.create_grid()
        self.update_solved_cells()
        self.ALL_NUMBERS = config.ALL_NUMBERS
        self.solved = False

    def __repr__(self):
        return f'sudoku object with {81 - len(self.solved_cells)} cells left to solve'

    def clean_data(self):
        # Length check
        assert (
                len(self.init_data) == config.ROW_LENGTH ** 2
        ), f"expected 81 chars, got {len(self.init_data)}"

        # Character check
        for c in self.init_data:
            if not c.isnumeric():
                if not c == ".":
                    raise ValueError(f"invalid character in sudoku data: {c}")

        # Sudoku sourced from QQwing.com uses "." for an empty cell. This app uses "0" for empty cells.
        if "." in self.init_data:
            converted_data = ""
            for c in self.init_data:
                if c == ".":
                    converted_data += "0"
                else:
                    converted_data += c

            return converted_data
        else:
            return self.init_data

    def create_grid(self):
        grid = {}
        char_count = 0
        for row in range(config.ROW_LENGTH):
            for col in range(config.ROW_LENGTH):
                c = self.data[char_count]
                if c == "0" or c == ".":
                    grid[f"{row}{col}"] = set()
                else:
                    grid[f"{row}{col}"] = set(c)
                char_count += 1

        assert len(grid.keys()) == config.ROW_LENGTH ** 2
        return grid

    def create_snapshot(self):
        """
        Returns a snapshot of the grid, so that it can be used to see if the state of the grid has changed.
        """
        return copy.deepcopy(self.grid)

    def update_solved_cells(self):
        solved = []
        for k, v in self.grid.items():
            # if there's only one possible value, them the cell is solved.
            if len(v) == 1:
                solved.append(k)

        if hasattr(self, "solved_cells"):
            self.solved_cells.extend([x for x in solved if x not in self.solved_cells])
        else:
            self.solved_cells = solved

    def get_square(self, ref):
        """
        Given a cell reference, return which of the nine squares the cell is in
        """
        for k, v in config.square_map.items():
            if ref in v:
                return k

    def get_related_cells(self, ref, mode):
        row, col = ref[0], ref[1]
        assert mode in "rcs"
        house = []  # "house" is a generic term for rows, cols and squares
        if mode == "r":
            # get all cell refs in the same row as the supplied cell ref
            for k in self.grid:
                if k[0] == row and k != ref:
                    house.append(k)

        elif mode == "c":
            # get all cell refs in the same col as the supplied cell ref
            for k in self.grid:
                if k[1] == col and k != ref:
                    house.append(k)
        else:
            # get all cell refs in the same square as the supplied cell ref
            for k, v in config.square_map.items():
                if ref in v:
                    for cell in v:
                        if not cell == ref:
                            house.append(cell)

        assert len(house) == 8
        return house

    def get_impossibles(self, ref):
        impossibles = set()
        related_cells = []
        for mode in "rcs":
            house = self.get_related_cells(ref, mode=mode)
            for cell in house:
                if cell not in related_cells:
                    related_cells.append(cell)

        for cell in related_cells:
            possible_values_for_cell = self.grid[cell]
            if len(possible_values_for_cell) == 1:
                for i in possible_values_for_cell:
                    impossibles.add(i)

        return impossibles

    def get_possibles(self, ref):
        impossibles = self.get_impossibles(ref)

        return self.ALL_NUMBERS.difference(impossibles)

    def clarify_all_cells(self):
        for k, v in self.grid.items():
            if not len(v) == 1:
                possibles = self.get_possibles(k)
                self.grid[k] = possibles

        self.update_solved_cells()
        if hasattr(self, "solved_cells"):
            if len(self.solved_cells) == config.ROW_LENGTH ** 2:
                self.solved = True

    def solve(self):
        while not self.solved:
            start = self.create_snapshot()
            self.clarify_all_cells()

            # If the grid hasn't changed after running self.clarify_all_cells, then raise an exception
            if self.create_snapshot() == start:
                raise UnableToSolveError

if __name__ == '__main__':
    s = Sudoku(config.test_data['valid_data'])
    #s = Sudoku(config.test_data['bad_data_invalid_sudoku'])

    print(s)
    s.solve()
    print(f'Solved: {s.solved}')
