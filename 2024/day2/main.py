REPORT = list[int]


def is_safe(levels: REPORT) -> bool:
    return (all((left < right and left + 4 > right) for left, right in zip(levels[:-1], levels[1:])) 
            or all((left > right and left < right + 4) for left, right in zip(levels[:-1], levels[1:])))


def is_safe_with_dampener(levels: REPORT) -> bool:
    return is_safe(levels) or any(is_safe(dampened) for dampened in [levels[:index] + levels[index + 1:] for index, _ in enumerate(levels)])


def count_safe_reports(reports: list[REPORT], dampener: bool = False) -> int:
    return sum(1 for report in reports if (is_safe(report) if not dampener else is_safe_with_dampener(report)))


def parse_reports(filename: str) -> list[REPORT]:
    with open(filename) as file:
        return [[int(c) for c in line.strip().split()] for line in file.readlines() if line.strip()]
    

if __name__ == "__main__":
    reports = parse_reports("sample.txt")
    print(count_safe_reports(reports))

    reports = parse_reports("input.txt")
    print(count_safe_reports(reports))

    reports = parse_reports("sample.txt")
    print(count_safe_reports(reports, True))

    reports = parse_reports("input.txt")
    print(count_safe_reports(reports, True))