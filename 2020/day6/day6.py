from typing import Iterable


def parse_groups(text: Iterable[str]) -> list[list[str]]:
    groups: list[list[str]] = []
    group: list[str] = []
    for line in text:
        line = line.strip()
        if not line:
            groups.append(group)
            group = []
        else:
            group.append(line)
    else:
        groups.append(group)
    return groups


def count_group(group: list[str]) -> int:
    common: set[str] = set()
    common = common.union(*group)
    return len(common)


def count_everyone_group(group: list[str]) -> int:
    common = set(group[0]) if group else set[str]()
    common = common.intersection(*group)
    return len(common)


if __name__ == "__main__":
    with open("sample.txt") as file:
        groups = parse_groups(file.readlines())
    total: int = sum(count_group(group) for group in groups)
    assert total == 11, total

    total = sum(count_everyone_group(group) for group in groups)
    assert total == 6, total

    with open("input.txt") as file:
        groups = parse_groups(file.readlines())
    total = sum(count_group(group) for group in groups)
    print(total)

    total = sum(count_everyone_group(group) for group in groups)
    print(total)

