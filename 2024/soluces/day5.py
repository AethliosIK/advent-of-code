import math

## UTILS


SEPARATOR_SECTION = "\n\n"
SEPARATOR_LINE = "\n"
SEPARATOR_RULE = "|"


def parse_input(input: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    rules: list[tuple[int, int]] = []
    pages_list: list[list[int]] = []
    inputs = input.split(SEPARATOR_SECTION)
    for line in inputs[0].split(SEPARATOR_LINE):
        rule = line.split(SEPARATOR_RULE)
        rules.append((int(rule[0]), int(rule[1])))
    for line in inputs[1].split("\n"):
        pages_list.append([int(e) for e in line.split(",")])
    return (rules, pages_list)


def verify_page_integrity(page: list[int], rules: list[tuple[int, int]]) -> bool:
    for i in range(0, len(page) - 1):
        for left, right in rules:
            if right == page[i]:
                if left in page[i:]:
                    return False
    return True


def compute_middle_page_sum(pages: list[list[int]]) -> int:
    r = 0
    for page in pages:
        assert (len(page) % 2) == 1
        r += page[math.floor(len(page) / 2)]
    return r


def sort_page_with_rules(page: list[int], rules: list[tuple[int, int]]) -> list[int]:
    new_page = page.copy()
    for i in range(0, len(new_page) - 1):
        for j in range(0, len(new_page[i:])):
            for left, right in rules:
                if right == new_page[i] and left == new_page[i + j]:
                    (
                        new_page[i],
                        new_page[i + j],
                    ) = (
                        new_page[i + j],
                        new_page[i],
                    )
                    new_page = new_page[:i] + sort_page_with_rules(new_page[i:], rules)
    return new_page


## SOLUCES


def part1(input: str) -> int:
    (rules, pages) = parse_input(input)
    verified_pages: list[list[int]] = []
    for page in pages:
        if verify_page_integrity(page, rules):
            verified_pages.append(page)
    return compute_middle_page_sum(verified_pages)


def part2(input: str) -> int:
    (rules, pages) = parse_input(input)
    sorted_pages: list[list[int]] = []
    for page in pages:
        if not verify_page_integrity(page, rules):
            sorted_pages.append(sort_page_with_rules(page, rules))
    return compute_middle_page_sum(sorted_pages)


## ASSERTS


def test() -> bool:
    example = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47"""
    soluce_part1 = 143
    soluce_part2 = 123
    return part1(example) == soluce_part1 and part2(example) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day5.txt"
    with open(filename) as f:
        input = f.read()
        print(f"Part 1 : {part1(input)}")
        print(f"Part 2 : {part2(input)}")
