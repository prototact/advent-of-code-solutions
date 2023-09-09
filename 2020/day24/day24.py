from typing import Optional
from collections.abc import Iterator, Generator
from itertools import chain
from functools import reduce


MAPPING: dict[str, tuple[float, float]] = {
    "ne": (1/2, 1/2),
    "se": (1/2, -1/2),
    "w": (-1, 0),
    "e": (1, 0),
    "nw": (-1/2, 1/2),
    "sw": (-1/2, -1/2)
}


def peek(itr: Iterator[str]) -> tuple[Optional[str], Iterator[str]]:
    try:
        elem = next(itr)
    except StopIteration:
        return (None, itr)
    return elem, chain([elem], itr)


def parse_tile(line: str) -> tuple[float, float]:
    itr = iter(line)
    tile: tuple[float, float] = (0., 0.)
    while True:
        elem, itr = peek(itr)
        if elem is None:
            break
        if elem in {'n', 's'}:
            left, right = next(itr), next(itr)
            symbol = left + right
        else:
            symbol = next(itr)
        vec = MAPPING[symbol]
        tile = (tile[0] + vec[0], tile[1] + vec[1])
    return tile


def parse_tiles(lines: list[str]) -> list[tuple[float, float]]:
    tiles: list[tuple[float, float]] = []
    for line in lines:
        line = line.strip()
        tile = parse_tile(line)
        tiles.append(tile)
    return tiles


def flip_tiles(tiles:list[tuple[float, float]]) -> dict[tuple[float, float], bool]:
    flipped: dict[tuple[float, float], bool] = {}
    for tile in tiles:
        flipped[tile] = not flipped.get(tile, False)
    return flipped


def count_black(tiles: dict[tuple[float, float], bool]):
    return sum(color for color in tiles.values())


def get_neighboors(tile: tuple[float, float]) -> Generator[tuple[float, float], None, None]:
    for other in MAPPING.values():
        yield (tile[0] + other[0], tile[1] + other[1])


def run_day(tiles: dict[tuple[float, float], bool]) -> dict[tuple[float, float], bool]:
    expanded: dict[tuple[float, float], bool] = {}
    for tile, color in tiles.items():
        for neighbor in get_neighboors(tile):
            if neighbor not in tiles:
                expanded[neighbor] = False
            expanded[tile] = color

    new_tiles: dict[tuple[float, float], bool] = {}
    for tile, color in expanded.items():
        total = sum(tiles[other] for other in get_neighboors(tile) if other in tiles)
        if color and (total == 0 or total > 2):
            new_tiles[tile] = not color
        elif not color and total == 2:
            new_tiles[tile] = not color
        else:
            new_tiles[tile] = color
    return new_tiles


def run(tiles: dict[tuple[float, float], bool], days: int) -> dict[tuple[float, float], bool]:
    return reduce(lambda agg, _: run_day(agg), range(days), tiles)

if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    tiles = parse_tiles(lines)
    flipped = flip_tiles(tiles)
    black = count_black(flipped)
    assert black == 10, black
    
    flipped = run(flipped, 100)
    black = count_black(flipped)
    assert black == 2208, black
    
    print("tests okay")

    with open("input.txt") as file:
        lines = file.readlines()
    tiles = parse_tiles(lines)
    flipped = flip_tiles(tiles)
    black = count_black(flipped)
    print(black)

    flipped = run(flipped, 100)
    black = count_black(flipped)
    print(black)
