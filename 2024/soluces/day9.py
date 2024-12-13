## UTILS

FREE_CELL = "."


def get_len_space(input: str) -> int:
    return sum([int(e) for e in input])


def get_space(input: str) -> list[str]:
    len_space = get_len_space(input)
    spaces: list[str] = [FREE_CELL] * len_space
    current = 0
    for i in range(len(input)):
        if i % 2 == 1:
            value = int(input[i])
            current = (current + value) % len_space
        if i % 2 == 0:
            value = int(input[i])
            for j in range(0, value):
                spaces[(current + j) % len_space] = str(int(i / 2))
            current = (current + value) % len_space
    return spaces


def next_free(spaces: list[str], previous_index_free: int) -> int:
    for i in range(previous_index_free, len(spaces)):
        if spaces[i] == FREE_CELL:
            return i
    return -1


def reduce_space(spaces: list[str]) -> list[str]:
    index_free = 0
    for index_value in range(len(spaces) - 1, 0, -1):
        index_free = next_free(spaces, index_free)
        if index_value < index_free:
            break
        if spaces[index_value] != FREE_CELL:
            spaces[index_free], spaces[index_value] = (
                spaces[index_value],
                spaces[index_free],
            )
    return spaces


def compute_sum(spaces: list[str]) -> int:
    return sum(
        [i * int(spaces[i]) for i in range(len(spaces)) if spaces[i] != FREE_CELL]
    )


def next_free_with_good_len(spaces: list[str], len_block: int) -> int:
    index_free = next_free(spaces, 0)
    while (
        index_free + len_block < len(spaces)
        and spaces[index_free : index_free + len_block] != [FREE_CELL] * len_block
    ):

        index_free = next_free(spaces, index_free)
        if spaces[index_free : index_free + len_block] != [FREE_CELL] * len_block:
            index_free += 1
    if index_free + len_block >= len(spaces):
        return -1
    return index_free


def get_len_block(spaces: list[str], index_value: int) -> int:
    value = spaces[index_value]
    len_block = 0
    while index_value - len_block > 0 and spaces[index_value - len_block] == value:
        len_block += 1
    return len_block


def reduce_space_with_good_len(spaces: list[str]) -> list[str]:
    index_free = 0
    index_value = len(spaces) - 1
    while index_value > 0:
        if spaces[index_value] != FREE_CELL:
            len_block = get_len_block(spaces, index_value)
            index_free = next_free_with_good_len(spaces, len_block)
            index_value -= len_block
            if index_free != -1 and index_free < index_value:
                (
                    spaces[index_free : index_free + len_block],
                    spaces[index_value + 1 : index_value + len_block + 1],
                ) = (
                    spaces[index_value + 1 : index_value + len_block + 1],
                    spaces[index_free : index_free + len_block],
                )
        else:
            index_value -= 1
    return spaces


## DEBUG


def print_space(spaces: list[str]) -> None:
    print("".join(spaces))


## SOLUCES


def part1(input: str) -> int:
    spaces = get_space(input)
    reduced_spaces = reduce_space(spaces)
    return compute_sum(reduced_spaces)


def part2(input: str) -> int:
    spaces = get_space(input)
    reduced_spaces = reduce_space_with_good_len(spaces)
    return compute_sum(reduced_spaces)


## ASSERTS


def test() -> bool:
    example = "2333133121414131402"
    soluce_part1 = 1928
    soluce_part2 = 2858
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day9.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
