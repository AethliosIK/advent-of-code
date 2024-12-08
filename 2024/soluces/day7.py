## UTILS

from typing import Callable

PART1_OPERATORS: list[Callable[[int, int], int]] = [
    lambda x, y: x + y,
    lambda x, y: x * y,
]
PART2_OPERATORS: list[Callable[[int, int], int]] = PART1_OPERATORS + [
    lambda x, y: int(str(x) + str(y)),
]


def parse_input(input: str) -> list[tuple[int, list[int]]]:
    r: list[tuple[int, list[int]]] = []
    for line in input.split("\n"):
        elems = line.split(": ")
        value, subvales = int(elems[0]), [int(e) for e in elems[1].split(" ")]
        r.append((value, subvales))
    return r


def guess_operators(
    final_value: int,
    subvalues: list[int],
    operators: list[Callable[[int, int], int]],
    value: int | None = None,
) -> bool:
    if len(subvalues) == 0:
        return final_value == value
    if not value:
        value = subvalues[0]
        subvalues = subvalues[1:]
    for operator in operators:
        if guess_operators(
            final_value, subvalues[1:], operators, value=operator(value, subvalues[0])
        ):
            return True
    return False


## SOLUCES


def part1(input: str) -> int:
    values = parse_input(input)
    r = 0
    for value, subvalues in values:
        if guess_operators(value, subvalues, PART1_OPERATORS):
            r += value
    return r


def part2(input: str) -> int:
    values = parse_input(input)
    r = 0
    for value, subvalues in values:
        if guess_operators(value, subvalues, PART2_OPERATORS):
            r += value
    return r


## ASSERTS


def test() -> bool:
    example = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20"""
    soluce_part1 = 3749
    soluce_part2 = 11387
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day7.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
