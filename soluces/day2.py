## UTILS


def parse_reports(input: str) -> list[list[int]]:
    separator_line = "\n"
    separator = " "
    l: list[list[int]] = []
    for line in input.split(separator_line):
        if len(line):
            levels = [int(level) for level in line.split(separator)]
            l.append(levels)
    return l


def is_all_decreasing(report: list[int]) -> bool:
    return all([report[i] > report[i + 1] for i in range(0, len(report) - 1)])


def is_all_increasing(report: list[int]) -> bool:
    return all([report[i] < report[i + 1] for i in range(0, len(report) - 1)])


def all_distances_are_in_range(report: list[int], min: int, max: int) -> bool:
    return all(
        [
            abs(report[i + 1] - report[i]) >= min
            and abs(report[i + 1] - report[i]) <= max
            for i in range(0, len(report) - 1)
        ]
    )


def is_safe(report: list[int]) -> bool:
    return (
        is_all_decreasing(report) or is_all_increasing(report)
    ) and all_distances_are_in_range(report, 1, 3)


def is_safe_with_one_bad_level(report: list[int]) -> bool:
    return is_safe(report) or any(
        [is_safe(report[:i] + report[i + 1 :]) for i in range(0, len(report))]
    )


## SOLUCES


def part1(reports: list[list[int]]) -> int:
    return len([report for report in reports if is_safe(report)])


def part2(reports: list[list[int]]) -> int:
    return len([report for report in reports if is_safe_with_one_bad_level(report)])


## ASSERTS


def test() -> bool:
    example = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""
    soluce_part1 = 2
    soluce_part2 = 4
    reports = parse_reports(example)
    return part1(reports) == soluce_part1 and part2(reports) == soluce_part2


## EXECUTION

if __name__ == "__main__":
    print(f"Test: {'OK' if test() else 'NOK'}")
    filename = "inputs/day2.txt"
    with open(filename) as f:
        input = f.read()
        reports = parse_reports(input)
        print(f"Part 1 : {part1(reports)}")
        print(f"Part 2 : {part2(reports)}")
