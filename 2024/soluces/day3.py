import re

## UTILS


OK_PATTERN = "do()"
NOK_PATTERN = "don't()"
MUL_PATTERN = r"mul\((\d{1,3}),(\d{1,3})\)"

def compute_mul(values: tuple[str, str]):
    return int(values[0]) * int(values[1])

## SOLUCES


def part1(input: str) -> int:
    r = 0
    pattern = re.compile(MUL_PATTERN)
    for values in pattern.findall(input):
        r += compute_mul(values)
    return r

def part2(input: str) -> int:
    r = 0
    pattern = re.compile(MUL_PATTERN)
    for l in input.split(OK_PATTERN):
        activate = l.split(NOK_PATTERN)[0]
        for values in pattern.findall(activate):
            r += compute_mul(values)
    return r


## ASSERTS


def test() -> bool:
    example = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    soluce_part1 = 161
    example2 = (
        "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    )
    soluce_part2 = 48
    return part1(example) == soluce_part1 and part2(example2) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day3.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
