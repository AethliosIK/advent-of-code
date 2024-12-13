## UTILS

NB_STEP_PART1 = 25
NB_STEP_PART2 = 75


def remove_useless_zero(value_as_str: str) -> int:
    return int(str(int(value_as_str)))


def evolv(
    value: int, already_used: dict[tuple[int, int], int], deep: int, maxDeep: int
) -> int:
    if deep >= maxDeep:
        return 1

    if (value, deep) in already_used:
        return already_used[(value, deep)]

    value_as_str = str(value)
    result_value: list[int] = []
    if value == 0:
        result_value = [1]
    elif len(value_as_str) % 2 == 0:
        left = remove_useless_zero(value_as_str[: len(value_as_str) // 2])
        right = remove_useless_zero(value_as_str[len(value_as_str) // 2 :])
        result_value = [left, right]
    else:
        result_value = [value * 2024]
    result = sum([evolv(v, already_used, deep + 1, maxDeep) for v in result_value])
    if not (result, deep) in already_used:
        already_used[(value, deep)] = result
    return result


def process(input: str, nb_step: int) -> int:
    r = 0
    for value in input.split(" "):
        r += evolv(int(value), {}, 0, nb_step)
    return r


## SOLUCES


def part1(input: str) -> int:
    return process(input, NB_STEP_PART1)


def part2(input: str) -> int:
    return process(input, NB_STEP_PART2)


## ASSERTS


def test() -> bool:
    example = "125 17"
    soluce_part1 = 55312
    return part1(example) == soluce_part1


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day11.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
