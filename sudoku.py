import config


class Sudoku:
    def __init__(self, init_data):
        self.init_data = init_data
        self.data = self.clean_data()
        self.grid = self.create_grid()
        self.update_solved_cells()
        self.ALL_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}
        self.solved = False

    def __repr__(self):
        return f'sudoku object with {81 - len(self.solved_cells)} cells left to solve'

    def clean_data(self):
        # Length check
        assert (
                len(self.init_data) == 81
        ), f"expected 81 chars, got {len(self.init_data)}"

        # Character check
        for c in self.init_data:
            if not c.isnumeric():
                if not c == ".":
                    raise ValueError(f"invalid character in sudoku data: {c}")

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
        for row in range(9):
            for col in range(9):
                c = self.data[char_count]
                if c == "0" or c == ".":
                    grid[f"{row}{col}"] = set()
                else:
                    grid[f"{row}{col}"] = set(c)
                char_count += 1

        assert len(grid.keys()) == 81
        return grid

    def update_solved_cells(self):
        solved = []
        for k, v in self.grid.items():
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
            if len(self.solved_cells) == 81:
                self.solved = True

    def solve(self):
        while not self.solved:
            self.clarify_all_cells()


if __name__ == '__main__':
    s = Sudoku(config.test_data['qqwing_format_data'])
    print(s)
    s.solve()