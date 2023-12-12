from dataclasses import dataclass
from enum import Enum


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


if __name__ == "__main__":
    with open("sample.txt") as file:
        springrows = [SpringRow.parse_row(line) for line in file.readlines()]
    total = sum(springrow.count_orderings() for springrow in springrows)
    assert total == 21, total

    with open("input.txt") as file:
        springrows = [SpringRow.parse_row(line) for line in file.readlines()]
    total = sum(springrow.count_orderings() for springrow in springrows)
    print(total)
