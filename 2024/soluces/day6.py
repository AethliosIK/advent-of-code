## UTILS

### PART 1

UNVISITED_CELL = "."
OBSTRUCTION_CELL = "#"
VISITED_CELL = "X"
GUARD_N = "^"
GUARD_E = ">"
GUARD_S = "V"
GUARD_W = "<"
GUARD_CELLS = [GUARD_N, GUARD_E, GUARD_S, GUARD_W]
GUARD_CELLS_DIRECTION = {
    GUARD_N: (-1, 0),
    GUARD_E: (0, 1),
    GUARD_S: (1, 0),
    GUARD_W: (0, -1),
}

### PART 2

GUARD_POSITION_CELL = "^"
VISITED_CELL_WITH_DIRECTION_NS = "|"
VISITED_CELL_WITH_DIRECTION_EW = "-"
VISITED_CELLS_WITH_DIRECTION = {
    (-1, 0): VISITED_CELL_WITH_DIRECTION_NS,
    (0, 1): VISITED_CELL_WITH_DIRECTION_EW,
    (1, 0): VISITED_CELL_WITH_DIRECTION_NS,
    (0, -1): VISITED_CELL_WITH_DIRECTION_EW,
}
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
VISITED_CELLS = [VISITED_CELL_WITH_DIRECTION_NS, VISITED_CELL_WITH_DIRECTION_EW]
VISITED_CELL_WITH_DIRECTION_CHANGE = "+"
NEW_OBSTRUCTION_CELL = "O"


def parse_input(input: str) -> tuple[list[list[str]], int, int]:
    r: list[list[str]] = []
    guard_x, guard_y = (-1, -1)
    i = 0
    for line in input.split("\n"):
        r.append([])
        j = 0
        for character in line:
            if character in GUARD_CELLS:
                guard_x, guard_y = (i, j)
            r[i].append(character)
            j += 1
        i += 1
    return r, guard_x, guard_y


def compute_visited_cell(matrix: list[list[str]]) -> int:
    r = 0
    for line in matrix:
        for cell in line:
            if cell == VISITED_CELL:
                r += 1
    return r


def next(
    matrix: list[list[str]], guard_x: int, guard_y: int
) -> tuple[list[list[str]], int, int]:
    assert matrix[guard_x][guard_y] in GUARD_CELLS

    new_matrix = matrix.copy()
    direction_x, direction_y = GUARD_CELLS_DIRECTION[matrix[guard_x][guard_y]]
    next_guard_x, next_guard_y = guard_x + direction_x, guard_y + direction_y
    if next_guard_x >= len(matrix) or next_guard_x < 0:
        new_matrix[guard_x][guard_y] = VISITED_CELL
        next_guard_x = -1
    if next_guard_y >= len(matrix[0]) or next_guard_y < 0:
        new_matrix[guard_x][guard_y] = VISITED_CELL
        next_guard_y = -1
    if matrix[next_guard_x][next_guard_y] in [UNVISITED_CELL, VISITED_CELL]:
        new_matrix[next_guard_x][next_guard_y] = matrix[guard_x][guard_y]
        new_matrix[guard_x][guard_y] = VISITED_CELL
    if matrix[next_guard_x][next_guard_y] == OBSTRUCTION_CELL:
        guard = matrix[guard_x][guard_y]
        new_guard = GUARD_CELLS[(GUARD_CELLS.index(guard) + 1) % len(GUARD_CELLS)]
        new_matrix[guard_x][guard_y] = new_guard
        next_guard_x, next_guard_y = guard_x, guard_y
    return new_matrix, next_guard_x, next_guard_y


def has_infinity_loop(
    matrix: list[list[str]],
    guard: tuple[int, int],
    direction: tuple[int, int],
) -> bool:
    previous_direction_change: list[tuple[tuple[int, int], tuple[int, int]]] = []
    current_x, current_y = guard
    direction_x, direction_y = direction
    next_current_x, next_current_y = current_x + direction_x, current_y + direction_y
    while not (
        next_current_x >= len(matrix)
        or next_current_x < 0
        or next_current_y >= len(matrix[0])
        or next_current_y < 0
    ):
        if (
            matrix[next_current_x][next_current_y] in VISITED_CELLS
            and ((current_x, current_y), (direction_x, direction_y))
            in previous_direction_change[:-1]
        ):
            return True
        if matrix[next_current_x][next_current_y] == UNVISITED_CELL:
            matrix[next_current_x][next_current_y] = VISITED_CELLS_WITH_DIRECTION[
                (direction_x, direction_y)
            ]
        if matrix[next_current_x][next_current_y] in [
            OBSTRUCTION_CELL,
            NEW_OBSTRUCTION_CELL,
        ]:
            matrix[current_x][current_y] = VISITED_CELL_WITH_DIRECTION_CHANGE
            (next_current_x, next_current_y) = (current_x, current_y)
            (direction_x, direction_y) = DIRECTIONS[
                (DIRECTIONS.index((direction_x, direction_y)) + 1) % len(DIRECTIONS)
            ]
            previous_direction_change.append(
                ((current_x, current_y), (direction_x, direction_y))
            )
        current_x, current_y = next_current_x, next_current_y
        next_current_x, next_current_y = (
            current_x + direction_x,
            current_y + direction_y,
        )
    return False


## DEBUG


def print_matrix(matrix: list[list[str]]) -> None:
    for line in matrix:
        for c in line:
            print(c, end="")
        print("")


## SOLUCES


def part1(input: str) -> int:
    matrix, guard_x, guard_y = parse_input(input)
    while not (guard_x == -1 or guard_y == -1):
        matrix, guard_x, guard_y = next(matrix, guard_x, guard_y)
    return compute_visited_cell(matrix)


def part2(input: str) -> int:
    matrix, guard_x, guard_y = parse_input(input)
    (height, width) = (len(matrix), len(matrix[0]))
    r = 0
    for i in range(height):
        for j in range(width):
            if matrix[i][j] == UNVISITED_CELL:
                new_matrix = list([list(l) for l in matrix])  # deep copy
                new_matrix[i][j] = NEW_OBSTRUCTION_CELL
                r += has_infinity_loop(new_matrix, (guard_x, guard_y), DIRECTIONS[0])
    return r


## ASSERTS


def test() -> bool:
    example = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#..."""
    soluce_part1 = 41
    soluce_part2 = 6
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day6.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
