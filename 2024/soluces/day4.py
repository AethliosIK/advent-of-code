## UTILS

WORD_PART1 = "XMAS"
WORD_PART2 = "MAS"


def parse_input(input: str) -> list[list[str]]:
    r: list[list[str]] = []
    i = 0
    for line in input.split("\n"):
        r.append([])
        for character in line:
            r[i].append(character)
        i += 1
    return r


def check_word(
    word: str, matrix: list[list[str]], x: int, y: int, x2: int, y2: int
) -> bool:
    for i in range(0, len(word)):
        new_x = x
        new_y = y
        if x < x2:
            new_x = x + i
        elif x > x2:
            new_x = x - i
        if y < y2:
            new_y = y + i
        elif y > y2:
            new_y = y - i

        if matrix[new_x][new_y] != word[i]:
            return False
    return True


def check_cell_all_direction(
    word: str, matrix: list[list[str]], x: int, y: int, height: int, width: int
) -> int:
    r = 0
    distance = len(word) - 1
    for check in [
        (x - distance) >= 0 and check_word(word, matrix, x, y, (x - distance), y),
        (y - distance) >= 0 and check_word(word, matrix, x, y, x, (y - distance)),
        (x + distance) < height and check_word(word, matrix, x, y, (x + distance), y),
        (y + distance) < width and check_word(word, matrix, x, y, x, (y + distance)),
        (x - distance) >= 0
        and (y - distance) >= 0
        and check_word(word, matrix, x, y, (x - distance), (y - distance)),
        (x + distance) < height
        and (y + distance) < width
        and check_word(word, matrix, x, y, (x + distance), (y + distance)),
        (x - distance) >= 0
        and (y + distance) < width
        and check_word(word, matrix, x, y, (x - distance), (y + distance)),
        (x + distance) < height
        and (y - distance) >= 0
        and check_word(word, matrix, x, y, (x + distance), (y - distance)),
    ]:
        if check:
            r += 1
    return r


def check_cell_with_x(
    word: str, matrix: list[list[str]], x: int, y: int, height: int, width: int
) -> bool:
    assert len(word) // 2 == 1
    distance = int((len(word) - 1) / 2)
    return (
        (
            (x - distance) >= 0
            and (y - distance) >= 0
            and (x + distance) < height
            and (y + distance) < width
        )
        and (
            check_word(
                word,
                matrix,
                (x - distance),
                (y - distance),
                (x + distance),
                (y + distance),
            )
            or check_word(
                word,
                matrix,
                (x + distance),
                (y + distance),
                (x - distance),
                (y - distance),
            )
        )
        and (
            check_word(
                word,
                matrix,
                (x + distance),
                (y - distance),
                (x - distance),
                (y + distance),
            )
            or check_word(
                word,
                matrix,
                (x - distance),
                (y + distance),
                (x + distance),
                (y - distance),
            )
        )
    )


## SOLUCES


def part1(input: str) -> int:
    matrix = parse_input(input)
    (height, width) = (len(matrix), len(matrix[0]))
    r = 0
    for i in range(height):
        for j in range(width):
            r += check_cell_all_direction(WORD_PART1, matrix, i, j, height, width)
    return r


def part2(input: str) -> int:
    matrix = parse_input(input)
    (height, width) = (len(matrix), len(matrix[0]))
    r = 0
    for i in range(height):
        for j in range(width):
            if check_cell_with_x(WORD_PART2, matrix, i, j, height, width):
                r += 1
    return r


## ASSERTS


def test() -> bool:
    example = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"""
    soluce_part1 = 18
    soluce_part2 = 9
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day4.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
