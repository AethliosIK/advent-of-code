## UTILS


def parse_sorted_lists(input: str) -> tuple[list[int], list[int]]:
    separator_line = "\n"
    separator = "   "
    l1: list[int] = []
    l2: list[int] = []
    for line in input.split(separator_line):
        if len(line):
            items = line.replace("\n", "").split(separator)
            l1.append(int(items[0]))
            l2.append(int(items[1]))
    return sorted(l1), sorted(l2)


## SOLUCES


def part1(l1: list[int], l2: list[int]) -> int:
    return sum([abs(e - e2) for (e, e2) in zip(l1, l2)])


def part2(l1: list[int], l2: list[int]) -> int:
    return sum([e * sum([1 for e2 in l2 if e == e2]) for e in l1])


## ASSERTS


def test() -> bool:
    example = """3   4
4   3
2   5
1   3
3   9
3   3"""
    soluce_part1 = 11
    soluce_part2 = 31
    l1, l2 = parse_sorted_lists(example)
    return part1(l1, l2) == soluce_part1 and part2(l1, l2) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day1.txt"
    with open(filename) as f:
        input = f.read()
        l1, l2 = parse_sorted_lists(input)
        print(f"Part 1 : {part1(l1,l2)}")
        print(f"Part 2 : {part2(l1,l2)}")
