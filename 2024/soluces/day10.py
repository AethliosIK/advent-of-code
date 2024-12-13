## UTILS

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
BEGIN_ROAD = 0
END_ROAD = 9


def parse_input(input: str) -> list[list[int]]:
    r: list[list[int]] = []
    i = 0
    for line in input.split("\n"):
        r.append([])
        for value in line:
            r[i].append(int(value))
        i += 1
    return r


def get_possible_roads(
    matrix: list[list[int]],
    index: tuple[int, int],
    history: list[tuple[int, int]] | None = None,
) -> list[list[tuple[int, int]]]:
    if not history:
        history = [index]
    index_x, index_y = index
    if matrix[index_x][index_y] == END_ROAD:
        return [history]
    possibilities: list[list[tuple[int, int]]] = []
    for x, y in DIRECTIONS:
        if (
            index_x + x >= 0
            and index_y + y >= 0
            and index_x + x < len(matrix)
            and index_y + y < len(matrix[0])
            and matrix[index_x][index_y] + 1 == matrix[index_x + x][index_y + y]
        ):
            possibilities += get_possible_roads(
                matrix,
                (index_x + x, index_y + y),
                history + [(index_x + x, index_y + y)],
            )
    return possibilities


def count_uniq_end_from_roads(roads: list[list[tuple[int, int]]]) -> int:
    return len(list(set([road[-1] for road in roads])))


## SOLUCES


def part1(input: str) -> int:
    matrix = parse_input(input)
    r = 0
    for i in range(len(matrix)):
        line = matrix[i]
        for j in range(len(line)):
            cell = line[j]
            if cell == BEGIN_ROAD:
                roads = get_possible_roads(matrix, (i, j))
                r += count_uniq_end_from_roads(roads)
    return r


def part2(input: str) -> int:
    matrix = parse_input(input)
    r = 0
    for i in range(len(matrix)):
        line = matrix[i]
        for j in range(len(line)):
            cell = line[j]
            if cell == BEGIN_ROAD:
                roads = get_possible_roads(matrix, (i, j))
                r += len(roads)
    return r


## ASSERTS


def test() -> bool:
    example = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""
    soluce_part1 = 36
    soluce_part2 = 81
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day10.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
