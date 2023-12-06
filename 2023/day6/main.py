from dataclasses import dataclass
from functools import reduce
from math import ceil, floor, prod, sqrt


@dataclass
class Race:
    time: int
    dist: int

    def _find_min_and_max_time(self) -> tuple[int, int] | None:
        alpha = 1
        beta = -self.time
        gamma = self.dist
        delta = beta**2 - 4 * alpha * gamma
        if delta < 0:
            return None
        tau1 = (-beta - sqrt(delta)) / 2
        tau2 = (-beta + sqrt(delta)) / 2
        if tau1.is_integer():
            tau1 = tau1 + 1
        if tau2.is_integer():
            tau2 = tau2 - 1
        return ceil(tau1), floor(tau2)

    def count_winning_options(self) -> int:
        pair = self._find_min_and_max_time()
        if pair is None:
            return 0
        tau1, tau2 = pair
        return len(range(tau1, tau2 + 1))


def count_all_wins(races: list[Race]) -> int:
    return prod(race.count_winning_options() for race in races)


def parse_races(lines: list[str]) -> list[Race]:
    times = [int(num) for num in lines[0].strip().split()[1:]]
    dists = [int(num) for num in lines[1].strip().split()[1:]]
    return [Race(time, dist) for time, dist in zip(times, dists)]


def parse_races_correct(lines: list[str]) -> Race:
    time = reduce(lambda x, y: x + y, lines[0].strip().split()[1:])
    dist = reduce(lambda x, y: x + y, lines[1].strip().split()[1:])
    return Race(int(time), int(dist))


if __name__ == "__main__":
    with open("sample.txt") as file:
        races = parse_races(file.readlines())
    assert (result := count_all_wins(races)) == 288, result

    with open("sample.txt") as file:
        race = parse_races_correct(file.readlines())
    assert race.count_winning_options() == 71503

    with open("input.txt") as file:
        races = parse_races(file.readlines())
    print(count_all_wins(races))

    with open("input.txt") as file:
        race = parse_races_correct(file.readlines())
    print(race.count_winning_options())
