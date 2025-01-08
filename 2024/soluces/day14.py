## UTILS

from functools import reduce
import re
import time

BOT_PATTERN = r"p=(\d+),(\d+) v=([-0-9]+),([-0-9]+)"

MATRIX_HEIGHT = 101
MATRIX_WIDTH = 103

ROUND = 100
DETECTED_LINE_LENGTH = 20


Bot = list[tuple[int, int, int, int]]
Matrix = list[list[int]]


def parse_input(
    input: str,
) -> Bot:
    r: Bot = []
    for bot in input.split("\n"):
        values = re.match(BOT_PATTERN, bot)
        if values:
            r.append(tuple(int(e) for e in values.groups()))  # type: ignore
    return r


def init_matrix(height: int, width: int, bots: Bot) -> Matrix:
    matrix = [[0] * height for _ in range(width)]
    for bot in bots:
        matrix[bot[1] % width][bot[0] % height] += 1
    return matrix


def step(height: int, width: int, bots: Bot) -> Bot:
    return [((x + vx) % height, (y + vy) % width, vx, vy) for x, y, vx, vy in bots]


def get_safety_factor(matrix: Matrix) -> int:
    sectors = [0, 0, 0, 0]
    mid_x = len(matrix) // 2
    mid_y = len(matrix[0]) // 2
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i == mid_x or j == mid_y:
                continue
            if i < mid_x and j < mid_y:
                sectors[0] += matrix[i][j]
            if i < mid_x and j > mid_y:
                sectors[1] += matrix[i][j]
            if i > mid_x and j < mid_y:
                sectors[2] += matrix[i][j]
            if i > mid_x and j > mid_y:
                sectors[3] += matrix[i][j]
    return reduce(lambda x, y: x * y, sectors)


## DETECTION

DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def detect_any_line(matrix: Matrix, limit: int) -> bool:
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if detect_line(matrix, limit, x=i, y=j):
                return True
    return False


def detect_line(
    matrix: Matrix, limit: int, x: int = 0, y: int = 0, deep: int = 0
) -> bool:
    if matrix[x][y] == 0:
        return False
    if deep >= limit:
        return True
    for direction_x, direction_y in DIRECTIONS:
        new_x, new_y = x + direction_x, y + direction_y
        if (
            new_x < len(matrix)
            and new_x >= 0
            and new_y < len(matrix[new_x])
            and new_y >= 0
        ):
            return detect_line(matrix, limit, x=new_x, y=new_y, deep=deep + 1)
    return False


## DEBUG


def print_matrix(matrix: Matrix) -> None:
    for line in matrix:
        for c in line:
            if c == 0:
                print("-", end="")
            else:
                print("#", end="")
        print("")


## SOLUCES


def part1(input: str, height: int = MATRIX_HEIGHT, width: int = MATRIX_WIDTH) -> int:
    bots = parse_input(input)
    for _ in range(ROUND):
        bots = step(height, width, bots)
    matrix = init_matrix(height, width, bots)
    return get_safety_factor(matrix)


def part2(input: str, height: int = MATRIX_HEIGHT, width: int = MATRIX_WIDTH) -> None:
    bots = parse_input(input)
    i = 0
    while True:
        bots = step(height, width, bots)
        i += 1
        matrix = init_matrix(height, width, bots)
        if detect_any_line(matrix, DETECTED_LINE_LENGTH):
            print_matrix(matrix)
            print(i)
            time.sleep(1)


## ASSERTS


def test() -> bool:
    example = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""
    soluce_part1 = 12
    return part1(example, 11, 7) == soluce_part1


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day14.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
