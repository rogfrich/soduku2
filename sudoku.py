import copy

import config
from exceptions import UnableToSolveError, NumberNotInPossibleValuesError


class Sudoku:
    def __init__(self, init_data):
        self.init_data = init_data
        self.data = self.clean_data()
        self.grid = self.create_grid()
        self.update_solved_cells()
        self.ALL_NUMBERS = config.ALL_NUMBERS
        self.solved = False

    def __repr__(self):
        return f"sudoku object with {81 - len(self.solved_cells)} cells left to solve"

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

    def get_grid_subset(self, index, mode):
        """
        Return a subset of the grid.
        """
        assert mode in "rcs"

        if mode == "r":
            subset = {k: v for (k, v) in self.grid.items() if k[0] == index}
        elif mode == "c":
            subset = {k: v for (k, v) in self.grid.items() if k[1] == index}
        else:
            subset = {}
            cells_in_square = config.square_map[index]
            for cell in cells_in_square:
                subset[cell] = self.grid[cell]

        return subset

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

    def invert_grid(self, subset):
        """
        Return a an inverted version of the grid subset provided. This means that the returned key will be a combination
        of possible numbers, and the value will be a list of cells which hold those values.
        """
        inverted_subset = dict()
        for k, v in subset.items():
            inverted_subset.setdefault(tuple(v), list()).append(k)

        return inverted_subset

    def find_naked_multiples(self, index, multiple, mode):
        """
        :param index: The row, column or square ID to identify which house we are interested in.
        :param multiple: how many matches - are we looking for naked pairs, triples, etc
        :param mode: [r]ow, [col] or [s]quare.
        :return: matches: a list of 2-item tuples where item[0] is the pair / triple etc and item[1] is a list of cells
        which hold that pair as possibilities, meaning we should remove those possibilities from all the other cells in
        the house.
        """
        subset = self.get_grid_subset(index, mode=mode)
        inverted_subset = self.invert_grid(subset)
        matches = []
        for k, v in inverted_subset.items():
            if len(v) == multiple:
                matches.append((k, v))
        return matches

    def naked_solve(self):
        for i in range(config.ROW_LENGTH):
            for mode in ("r", "c", "s"):
                matches = self.find_naked_multiples(f"{i}", 2, mode=mode)
                if matches:
                    matched_possibles = matches[0][0]
                    matched_cells = matches[0][1]
                    for cell in self.get_grid_subset(f"{i}", mode=mode):
                        if cell not in matched_cells:
                            self.remove_possibles_from_grid(cell, matched_possibles)

    def solve(self):
        while not self.solved:
            start = self.create_snapshot()
            self.clarify_all_cells()

            # If the grid hasn't changed after running self.clarify_all_cells, then raise an exception
            if self.create_snapshot() == start:
                raise UnableToSolveError

    def remove_possibles_from_grid(self, cell, possibles_to_remove):
        """
        Remove possible values from a given cell's list of possibles.
        :param cell: str
        :param possibles_to_remove: list
        :return: None
        """

        for possible in possibles_to_remove:
            if possible in self.grid[cell]:
                self.grid[cell].remove(possible)


if __name__ == "__main__":
    # Use for exploratory testing.
    s = Sudoku(config.test_data["valid_data"])
    s.clarify_all_cells()
