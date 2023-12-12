from dataclasses import dataclass
from enum import Enum
from itertools import repeat, chain
from functools import reduce


class Spring(Enum):
    Okay = 1
    Broken = 2
    Wildcard = 3

    @staticmethod
    def parse_spring(char: str) -> "Spring":
        match char:
            case ".":
                return Spring.Okay
            case "#":
                return Spring.Broken
            case "?":
                return Spring.Wildcard
            case _:
                raise ValueError(f"Bad character {char}")


@dataclass
class SpringRow:
    _springs: list[Spring]
    _broken: list[int]

    @classmethod
    def parse_row(cls, line: str) -> "SpringRow":
        springs, broken = line.strip().split()
        return cls(
            [Spring.parse_spring(char) for char in springs],
            [int(char) for char in broken.split(",")],
        )

    def count_orderings(self) -> int:
        broken = self._broken[:]
        springs = self._springs[::-1]

        def go(springs: list[Spring], broken: list[int], start: bool, end: bool) -> int:
            copy = springs[:]
            try:
                spring = copy.pop()
            except IndexError:
                spring = None
            match (spring, broken, start, end):
                case (Spring.Okay, _, True, False):
                    return 0
                case (Spring.Okay, xs, False, _):
                    return go(copy, xs, False, False)
                case (Spring.Broken, [1, *xs], _, False):
                    return go(copy, xs, False, True)
                case (Spring.Broken, [x, *xs], _, False) if x > 1:
                    return go(copy, [x - 1, *xs], True, False)
                case (Spring.Broken, _, False, True):
                    return 0
                case (Spring.Broken, [], _, _):
                    return 0
                case (Spring.Wildcard, [], False, _):
                    return go(copy, [], False, False)
                case (Spring.Wildcard, [1, *xs], False, False):
                    return go(copy, xs, False, True) + go(copy, [1, *xs], False, False)
                case (Spring.Wildcard, [1, *xs], True, False):
                    return go(copy, xs, False, True)
                case (Spring.Wildcard, [x, *xs], False, False) if x > 1:
                    return go(copy, [x, *xs], False, False) + go(
                        copy, [x - 1, *xs], True, False
                    )
                case (Spring.Wildcard, [x, *xs], False, True):
                    return go(copy, [x, *xs], False, False)
                case (Spring.Wildcard, [x, *xs], True, False) if x > 1:
                    return go(copy, [x - 1, *xs], True, False)
                case (None, [_, *_], _, _):
                    return 0
                case (None, [], False, _):
                    return 1
                case _:
                    raise ValueError(f"Unreachable {spring, broken, start, end}")

        return go(springs, broken, False, False)

    @staticmethod
    def split_on_okay(springs: list[Spring]) -> list[list[Spring]]:
        splitted: list[list[Spring]] = []
        to_split: list[Spring] = []
        for spring in springs:
            if spring != Spring.Okay:
                to_split.append(spring)
            elif spring == Spring.Okay and to_split:
                splitted.append(to_split)
                to_split = []
        if to_split:
            splitted.append(to_split)
        return splitted

    def count_orderings_unfold(self) -> int:
        broken = list(chain.from_iterable(repeat(self._broken[:], 5)))
        rev5 = repeat(self._springs[:], 5)
        springs = reduce(
            lambda agg, x: agg + [Spring.Wildcard] + x,
            rev5,
        )
        groups = self.split_on_okay(springs)

        def go(broken: list[int], groups: list[list[Spring]]) -> int:
            if not broken:
                return (
                    1
                    if all(
                        all(spring != Spring.Broken for spring in group)
                        for group in groups
                    )
                    else 0
                )
            if not groups:
                return 0

            size, *rest = broken
            group, *rest_groups = groups
            if len(group) < size and all(spring == Spring.Wildcard for spring in group):
                return go(broken, rest_groups)
            if len(group) < size:
                return 0
            if len(group) == size and all(
                spring == Spring.Wildcard for spring in group
            ):
                return go(rest, rest_groups) + go(broken, rest_groups)
            if len(group) == size:
                return go(rest, rest_groups)
            if len(group) > size and all(spring == Spring.Broken for spring in group):
                return 0
            if len(group) > size:
                return (
                    sum(
                        go(rest, [group[idx + size + 1 :], *rest_groups])
                        for idx in range(len(group) - size)
                        if group[idx + size] == Spring.Wildcard
                        and all(spring != Spring.Broken for spring in group[:idx])
                    )
                    + (
                        go(rest, rest_groups)
                        if all(
                            spring != Spring.Broken
                            for spring in group[: len(group) - size]
                        )
                        else 0
                    )
                    + (
                        go(broken, rest_groups)
                        if all(spring == Spring.Wildcard for spring in group)
                        else 0
                    )
                )
            raise ValueError(f"Unreachable {broken, groups}")

        return go(broken, groups)


if __name__ == "__main__":
    with open("sample.txt") as file:
        springrows = [SpringRow.parse_row(line) for line in file.readlines()]
    total = sum(springrow.count_orderings() for springrow in springrows)
    assert total == 21, total

    total = sum(springrow.count_orderings_unfold() for springrow in springrows)
    assert total == 525152, total

    with open("input.txt") as file:
        springrows = [SpringRow.parse_row(line) for line in file.readlines()]
    total = sum(springrow.count_orderings() for springrow in springrows)
    print(total)

    total = sum(springrow.count_orderings_unfold() for springrow in springrows)
    print(total)
