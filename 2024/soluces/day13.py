## UTILS

import re

BUTTON_A_PATTERN = r"Button A: X\+(\d+), Y\+(\d+)"
BUTTON_B_PATTERN = r"Button B: X\+(\d+), Y\+(\d+)"
PRIZE_PATTERN = r"Prize: X=(\d+), Y=(\d+)"

BUTTON_A_TOKEN = 3
BUTTON_B_TOKEN = 1
PART2_APPEND_VALUE = 10000000000000


def parse_input(
    input: str,
) -> list[tuple[tuple[int, ...], ...]]:
    r: list[tuple[tuple[int, ...], ...]] = []
    for claw in input.split("\n\n"):
        lines = claw.split("\n")
        button_a = re.match(BUTTON_A_PATTERN, lines[0])
        button_b = re.match(BUTTON_B_PATTERN, lines[1])
        prize = re.match(PRIZE_PATTERN, lines[2])
        if button_a and button_b and prize:
            r.append(
                tuple(
                    tuple(int(elem) for elem in line.groups())
                    for line in (button_a, button_b, prize)
                )
            )
    return r


def cramer_method(
    e1: tuple[int, int, int], e2: tuple[int, int, int]
) -> tuple[int, int] | None:
    d = e1[0] * e2[1] - e1[1] * e2[0]
    if d != 0:
        x = e1[2] * e2[1] - e1[1] * e2[2]
        y = e1[0] * e2[2] - e1[2] * e2[0]
        if x % d == 0 and y % d == 0:
            return int(x / d), int(y / d)


## SOLUCES


def part1(input: str) -> int:
    claws = parse_input(input)
    result = 0
    for button_a, button_b, prize in claws:
        r = cramer_method(
            (button_a[0], button_b[0], prize[0]), (button_a[1], button_b[1], prize[1])
        )
        if r:
            result += r[0] * BUTTON_A_TOKEN + r[1] * BUTTON_B_TOKEN
    return result


def part2(input: str) -> int:
    claws = parse_input(input)
    result = 0
    for button_a, button_b, prize in claws:
        r = cramer_method(
            (button_a[0], button_b[0], prize[0] + PART2_APPEND_VALUE),
            (button_a[1], button_b[1], prize[1] + PART2_APPEND_VALUE),
        )
        if r:
            result += r[0] * BUTTON_A_TOKEN + r[1] * BUTTON_B_TOKEN
    return result


## ASSERTS


def test() -> bool:
    example = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""
    soluce_part1 = 480
    soluce_part2 = 480
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day13.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
