import config


def load_data_from_config():
    data = config.data
    validate_data(data)
    return data


def validate_data(data):
    assert len(data) == 81, f"expected 81 chars, got {len(data)}"
    for c in data:
        assert c.isnumeric(), f"Non-numeric character found: {c}"


def create_grid(data):
    grid = {}
    char_count = 0
    for row in range(9):
        for col in range(9):
            c = data[char_count]
            if c == "0":
                grid[f"{row}{col}"] = set()
            else:
                grid[f"{row}{col}"] = set(c)
            char_count += 1

    assert len(grid.keys()) == 81
    return grid


def get_solved_cells():
    global grid
    solved_cells = []
    for k, v in grid.items():
        if len(v) == 1:
            solved_cells.append(k)
    return solved_cells


def get_square(ref):
    """
    Given a cell reference, return which of the nine squares the cell is in
    """
    for k, v in config.square_map.items():
        if ref in v:
            return k


def get_cell_refs_in_house(ref, mode):
    global grid
    row, col = ref[0], ref[1]
    assert mode in "rcs"
    house = []
    if mode == "r":
        # get all cell refs in the same row as the supplied cell ref
        for k in grid:
            if k[0] == row and k != ref:
                house.append(k)

    elif mode == "c":
        # get all cell refs in the same col as the supplied cell ref
        for k in grid:
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


def get_impossibles(ref):
    global grid
    impossibles = set()
    for mode in "rcs":
        interacting_cells = get_cell_refs_in_house(ref, mode)
        for cell in interacting_cells:
            if len(grid[cell]) == 1:
                iterable = list(grid[cell])
                impossibles.add(iterable[0])
    return impossibles


def get_possibles(ref):
    global ALL_NUMBERS
    impossibles = get_impossibles(ref)
    return ALL_NUMBERS.difference(impossibles)


def clarify_all_cells():
    for k, v in grid.items():
        if not len(v) == 1:  # cell is not solved
            possibles = get_possibles(k)
            grid[k] = possibles


ALL_NUMBERS = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

data = load_data_from_config()
grid = create_grid(data)

if __name__ == "__main__":

    while len(get_solved_cells()) < 81:
        clarify_all_cells()
        print(f"solved: {len(get_solved_cells())} cells")

