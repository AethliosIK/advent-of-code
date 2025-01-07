## UTILS


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def parse_input(input: str) -> list[list[str]]:
    r: list[list[str]] = []
    i = 0
    for line in input.split("\n"):
        r.append([])
        for value in line:
            r[i].append(value)
        i += 1
    return r


def compute_perimeter_for_one_cell(matrix: list[list[str]], x: int, y: int) -> int:
    cell = matrix[x][y]
    r = 0
    for direction_x, direction_y in DIRECTIONS:
        new_direction_x, new_direction_y = x + direction_x, y + direction_y
        if (
            new_direction_x >= len(matrix)
            or new_direction_x < 0
            or new_direction_y >= len(matrix[new_direction_x])
            or new_direction_y < 0
            or cell != matrix[new_direction_x][new_direction_y]
        ):
            r += 1
    return r


def has_way_to(
    matrix: list[list[str]],
    result_cells: list[tuple[str, int, int]],
    x: int,
    y: int,
    visited_cells: list[tuple[str, int, int]] | None = None,
) -> tuple[str, int, int] | None:
    cell = matrix[x][y]

    if not visited_cells:
        visited_cells = []
    if (cell, x, y) in visited_cells:
        return None
    if (cell, x, y) in result_cells:
        return (cell, x, y)
    for direction_x, direction_y in DIRECTIONS:
        new_direction_x, new_direction_y = x + direction_x, y + direction_y
        if (
            new_direction_x < len(matrix)
            and new_direction_x >= 0
            and new_direction_y < len(matrix[new_direction_x])
            and new_direction_y >= 0
            and cell == matrix[new_direction_x][new_direction_y]
        ):
            visited_cells.append((cell, x, y))
            r = has_way_to(
                matrix,
                result_cells,
                new_direction_x,
                new_direction_y,
                visited_cells=visited_cells,
            )
            if r:
                return r
    return None


## SOLUCES


def part1(input: str) -> int:
    matrix = parse_input(input)
    result: dict[tuple[str, int, int], tuple[int, int]] = {}
    for i in range(len(matrix)):
        line = matrix[i]
        for j in range(len(line)):
            cell = line[j]
            perimeter_cell = compute_perimeter_for_one_cell(matrix, i, j)
            origin_cell = has_way_to(matrix, list(result.keys()), i, j)
            if origin_cell and origin_cell in result:
                area, perimeter = result[origin_cell]
                result[origin_cell] = (area + 1, perimeter + perimeter_cell)
            else:
                result[(cell, i, j)] = (1, perimeter_cell)
    return sum([result[cell_type][0] * result[cell_type][1] for cell_type in result])


def part2(input: str) -> int:
    pass


## ASSERTS


def test() -> bool:
    example = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""
    soluce_part1 = 1930
    soluce_part2 = 1206
    return part1(example) == soluce_part1  # and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day12.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
