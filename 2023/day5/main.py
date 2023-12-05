import re
from collections.abc import Iterator
from dataclasses import dataclass

SEEDS = re.compile(r"seeds:((?:\s\d+)+)")
ORDER = {
    "seed-to-soil": 1,
    "soil-to-fertilizer": 2,
    "fertilizer-to-water": 3,
    "water-to-light": 4,
    "light-to-temperature": 5,
    "temperature-to-humidity": 6,
    "humidity-to-location": 7,
}


@dataclass
class Subdivision:
    overlap: range | None
    non_overlap: list[range]


@dataclass(frozen=True)
class Map:
    ranges: list[tuple[range, range]]

    @classmethod
    def parse_map(cls, values: list[tuple[int, int, int]]) -> "Map":
        ranges: list[tuple[range, range]] = []
        for value in values:
            dst_start, src_start, size = value
            src_range = range(src_start, src_start + size)
            dst_range = range(dst_start, dst_start + size)
            ranges.append((src_range, dst_range))
        return cls(ranges)

    def __getitem__(self, key: int) -> int:
        for src_range, dst_range in self.ranges:
            if key in src_range:
                dst = dst_range.start + (key - src_range.start)
                break
        else:
            dst = key
        return dst

    @staticmethod
    def subdivide(left: range, right: range) -> Subdivision:
        """Subdivides the left range into overlap with right and non-overlaps.
        It is not symmetric in left and right.
        Instead, only members of left are of interest.
        """
        # right is contained in left
        if left.start <= right.start and right.stop <= left.stop:
            if left.start == right.start and right.stop == left.stop:
                return Subdivision(overlap=right, non_overlap=[])
            if left.start < right.start and right.stop == left.stop:
                lower = range(left.start, right.start)
                return Subdivision(overlap=right, non_overlap=[lower])
            if left.start == right.start and right.stop < left.stop:
                upper = range(right.stop, left.stop)
                return Subdivision(overlap=right, non_overlap=[upper])
            lower = range(left.start, right.start)
            upper = range(right.stop, left.stop)
            return Subdivision(overlap=right, non_overlap=[lower, upper])
        # left is contained in right
        if right.start <= left.start and left.stop <= right.stop:
            return Subdivision(overlap=left, non_overlap=[])
        # left is hanging from below
        if left.start <= right.start <= left.stop <= right.stop:
            if left.start == right.start:
                return Subdivision(overlap=left, non_overlap=[])
            if right.start == left.stop:
                return Subdivision(overlap=None, non_overlap=[left])
            inbetween = range(right.start, left.stop)
            lower = range(left.start, right.start)
            return Subdivision(overlap=inbetween, non_overlap=[lower])
        # left is hanging from above
        if right.start <= left.start <= right.stop <= left.stop:
            if right.stop == left.stop:
                return Subdivision(overlap=left, non_overlap=[])
            if left.start == right.stop:
                return Subdivision(overlap=None, non_overlap=[left])
            inbetween = range(left.start, right.stop)
            upper = range(right.stop, left.stop)
            return Subdivision(overlap=inbetween, non_overlap=[upper])
        # left and right do not overlap
        # if right.stop < left.start or left.stop < right.start:
        return Subdivision(overlap=None, non_overlap=[left])

    def map_range(self, rng: range) -> list[range]:
        to_map = [rng]
        mapped: list[range] = []
        for src_range, dst_range in self.ranges:
            subdivs = [self.subdivide(rng, src_range) for rng in to_map]
            for subdiv in subdivs:
                if subdiv.overlap is not None:
                    start = dst_range.start + (subdiv.overlap.start - src_range.start)
                    stop = dst_range.start + (subdiv.overlap.stop - src_range.start)
                    mapped.append(range(start, stop))
            to_map = [rng for subdiv in subdivs for rng in subdiv.non_overlap]
        mapped.extend(to_map)
        return mapped


def extract_values(itr: Iterator[str]) -> list[tuple[int, int, int]]:
    values: list[tuple[int, int, int]] = []
    line = next(itr, "").strip()
    while line:
        dst_start, src_start, size = (int(num) for num in line.split())
        values.append((dst_start, src_start, size))
        line = next(itr, "").strip()
    return values


def parse_seeds_and_maps(lines: list[str]) -> tuple[list[int], dict[str, Map]]:
    itr = iter(lines)
    m = SEEDS.match(next(itr, "").strip())
    if m is not None:
        seeds = [int(num) for num in m.group(1).strip().split()]
    else:
        raise ValueError("No seeds found.")

    next(itr, "")

    maps: dict[str, Map] = {}
    while True:
        line = next(itr, "").strip()
        match line:
            case "seed-to-soil map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["seed-to-soil"] = map_
            case "soil-to-fertilizer map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["soil-to-fertilizer"] = map_
            case "fertilizer-to-water map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["fertilizer-to-water"] = map_
            case "water-to-light map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["water-to-light"] = map_
            case "light-to-temperature map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["light-to-temperature"] = map_
            case "temperature-to-humidity map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["temperature-to-humidity"] = map_
            case "humidity-to-location map:":
                values = extract_values(itr)
                map_ = Map.parse_map(values)
                maps["humidity-to-location"] = map_
            case _:
                break
    return seeds, maps


def parse_seeds(seeds: list[int]) -> list[range]:
    actual_seeds: list[range] = []
    itr = iter(seeds)
    for seed_start, seed_range in zip(itr, itr):
        rng = range(seed_start, seed_start + seed_range)
        actual_seeds.append(rng)
    return actual_seeds


def map_seed_to_location(seed: int, maps: dict[str, Map]) -> int:
    value = seed
    for _, map_ in sorted(maps.items(), key=lambda x: ORDER[x[0]]):
        value = map_[value]
    return value


def map_seed_to_location_rng(seeds: range, maps: dict[str, Map]) -> list[range]:
    values = [seeds]
    for _, map_ in sorted(maps.items(), key=lambda x: ORDER[x[0]]):
        values = [rng for value in values for rng in map_.map_range(value)]
    return values


if __name__ == "__main__":
    with open("sample.txt") as file:
        seeds, maps = parse_seeds_and_maps(file.readlines())
    min_location = min(map_seed_to_location(seed, maps) for seed in seeds)
    assert min_location == 35, min_location
    actual_seeds = parse_seeds(seeds)
    min_location = min(
        rng.start
        for seeds in actual_seeds
        for rng in map_seed_to_location_rng(seeds, maps)
    )
    assert min_location == 46, min_location

    print("test ok!")

    with open("input.txt") as file:
        seeds, maps = parse_seeds_and_maps(file.readlines())
    min_location = min(map_seed_to_location(seed, maps) for seed in seeds)
    print(min_location)
    # too slow, ranges too big, need to optimize
    actual_seeds = parse_seeds(seeds)
    min_location = min(
        rng.start
        for seeds in actual_seeds
        for rng in map_seed_to_location_rng(seeds, maps)
    )
    print(min_location)
