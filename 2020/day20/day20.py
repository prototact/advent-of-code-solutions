from collections import deque
from collections.abc import Generator
from typing import Optional
from enum import Enum
from math import sqrt
from functools import partial
from operator import and_
import re


class Border(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3


UP = [(Border.Left, (0, -1)), (Border.Right, (0, 1)), (Border.Down, (1, 0))]
RIGHT = [(Border.Left, (0, -1)), (Border.Up, (-1, 0)), (Border.Down, (1, 0))]
DOWN = [(Border.Left, (0, -1)), (Border.Right, (0, 1)), (Border.Up, (-1, 0))]
LEFT = [(Border.Right, (0, 1)), (Border.Up, (-1, 0)), (Border.Down, (1, 0))]

DRAGON = [[partial(and_, True) if elem == "#" else lambda _: True for elem in row] for row in """
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   
""".splitlines()[1:]]

Tile = list[list[bool]]
Arranged = dict[tuple[int, int], tuple[int, Tile]]


NAME = re.compile(r"Tile (\d+)\:")


def parse_tiles(lines: list[str]) -> deque[tuple[int, Tile]]:
    tiles: deque[tuple[int, Tile]] = deque()

    tile_name: Optional[int] = None
    current_tile: Tile = []
    for line in lines:
        line = line.strip()
        if not line and tile_name is not None:
            tiles.append((tile_name, current_tile))
            current_tile = []
            continue
        match_ = NAME.match(line)
        if match_ is not None:
            tile_name = int(match_.groups()[0])
        else:
            current_tile.append([cell == "#" for cell in line])
    else:
        if tile_name is not None:
            tiles.append((tile_name, current_tile))

    return tiles


def take_border_up(tile: Tile) -> Generator[tuple[list[bool], Border], None, None]:
    yield tile[0], Border.Up
    yield [row[len(row) - 1] for row in tile], Border.Right
    yield tile[len(tile) - 1], Border.Down
    yield [row[0] for row in tile], Border.Left


def take_border_down(tile: Tile) -> Generator[tuple[list[bool], Border], None, None]:
    yield tile[len(tile) - 1], Border.Down
    yield [row[0] for row in tile], Border.Left
    yield tile[0], Border.Up
    yield [row[len(tile) - 1] for row in tile], Border.Right


def match_border(tile: Tile, other: Tile) -> Optional[Border]:
    for (left, ldir), (right, _) in zip(take_border_up(tile), take_border_down(other)):
        if left == right:
            return ldir


def match_border_specific(tile: Tile, side: Border, other: Tile) -> bool:
    for (left, border), (right, _) in zip(take_border_up(tile), take_border_down(other)):
        if side == border:
            return left == right
    return False

def flip(tile: Tile) -> Tile:
    return [row[::-1] for row in tile]


def rotate(tile: Tile) -> Generator[Tile, None, None]:
    yield tile
    to_rotate = [deque(row) for row in tile]
    for _ in range(3):
        new_tile: list[deque[bool]] = [deque() for _ in to_rotate]
        for row in to_rotate:
            for elem, row_ in zip(row, new_tile):
                row_.appendleft(elem)
        yield [[elem for elem in row] for row in new_tile]
        to_rotate = new_tile

def orientations(tile: Tile) -> Generator[Tile, None, None]:
    yield from rotate(tile)
    flipped = flip(tile)
    yield from rotate(flipped)

def insert_tile(tile_id: int, tile: Tile, arranged: Arranged) -> tuple[Arranged, bool]:
    if not arranged:
        loc = (0, 0)
        arranged[loc] = (tile_id, tile)
        return arranged, True
    # tile has to be checked against all neighbors, that depends on border matched.
    # what happens if my current arrangment is wrong?
    for loc_, (_, other) in arranged.items():
        for oriented in orientations(tile):
            border = match_border(oriented, other)
            if border is not None:
                matches = True
                if border == Border.Up:
                    loc = loc_[0] + 1, loc_[1]
                    for border_, dir_ in UP:
                        subloc = loc[0] + dir_[0], loc[1] + dir_[1]
                        neighbor = arranged.get(subloc, None)
                        if neighbor is not None:
                            matches &= match_border_specific(oriented, border_, arranged[subloc][1])
                elif border == Border.Right:
                    loc = loc_[0], loc_[1] - 1
                    for border_, dir_ in RIGHT:
                        subloc = loc[0] + dir_[0], loc[1] + dir_[1]
                        neighbor = arranged.get(subloc, None)
                        if neighbor is not None:
                            matches &= match_border_specific(oriented, border_, arranged[subloc][1])
                elif border == Border.Down:
                    loc = loc_[0] - 1, loc_[1]
                    for border_, dir_ in DOWN:
                        subloc = loc[0] + dir_[0], loc[1] + dir_[1]
                        neighbor = arranged.get(subloc, None)
                        if neighbor is not None:
                            matches &= match_border_specific(oriented, border_, arranged[subloc][1])
                elif border == Border.Left:
                    loc = loc_[0], loc_[1] + 1
                    for border_, dir_ in LEFT:
                        subloc = loc[0] + dir_[0], loc[1] + dir_[1]
                        neighbor = arranged.get(subloc, None)
                        if neighbor is not None:
                            matches &= match_border_specific(oriented, border_, arranged[subloc][1])
                else:
                    raise ValueError(f"Unreachable, border = {border}")
                if matches:
                    arranged[loc] = (tile_id, oriented)
                    return arranged, True
    return arranged, False

def arrange_tiles(tiles: deque[tuple[int, Tile]]) -> Arranged:
    arranged: Arranged = {}
    while tiles:
        tile_id, tile = tiles.popleft()
        arranged, inserted = insert_tile(tile_id, tile, arranged)
        if not inserted:
            tiles.append((tile_id, tile))

    return arranged

def get_locs(arranged: Arranged) -> list[list[Optional[int]]]:
    min_vertical = min(arranged, key=lambda x: x[0])[0]
    min_horizontal = min(arranged, key=lambda x: x[1])[1]

    def reposition(loc: tuple[int, int]) -> tuple[int, int]:
        return loc[0] - min_vertical, loc[1] - min_horizontal
    dim = sqrt(len(arranged))
    locations: list[list[Optional[int]]] = [[None for _ in range(int(dim))] for _ in range(int(dim))]
    for loc, (tile_id, _) in arranged.items():
        loc_ = reposition(loc)
        locations[loc_[0]][loc_[1]] = tile_id
    return locations


def remove_border(tile: Tile) -> list[list[bool]]:
    return [row[1:-1] for row in tile[1:-1]]


def get_image(arranged: Arranged) -> list[list[bool]]:
    cleaned: list[list[bool]] = []
    sorted_ = sorted(arranged.items(), key=lambda x: x[0])
    cur_loc, (_, to_clean) = sorted_[0]
    subcleaned = remove_border(to_clean)
    cur_row = cur_loc[0]
    for loc, (_, tile) in sorted_[1:]:
        clean = remove_border(tile)
        if cur_row != loc[0]:
            cleaned.extend(subcleaned)
            subcleaned = clean
            cur_row = loc[0]
        else:
            for row, subrow in zip(subcleaned, clean):
                row.extend(subrow)
    else:
        cleaned.extend(subcleaned)
    return cleaned

def match_dragon(image: Tile, i: int, j: int) -> int:
    win_height = len(DRAGON)
    win_width = len(DRAGON[0])
    subimage = [row[j:j + win_width] for row in image[i:i + win_height]]
    if len(subimage) < win_height or len(subimage[0]) < win_width:
        return 0
    if all(func(elem) for row, drow in zip(subimage, DRAGON) for elem, func in zip(row, drow)):
        return 1
    return 0

def find_dragons(image: list[list[bool]]) -> int:
    total = sum(elem for row in image for elem in row)
    print(total)
    for oriented in orientations(image):
        num_dragons = 0
        for i, row in enumerate(oriented):
            for j, _ in enumerate(row):
                num_dragons += match_dragon(oriented, i, j)
        if num_dragons > 0:
            break
    print(num_dragons)
    return total - num_dragons * sum(not func(False) for row in DRAGON for func in row)

if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    tiles = parse_tiles(lines)
    tile_id, tile = tiles.popleft()
    size = len(tile)
    tiles.appendleft((tile_id, tile))
    arranged = arrange_tiles(tiles)
    locations = get_locs(arranged)
    assert locations[0][0] * locations[0][-1] * locations[-1][0] * locations[-1][-1] == 20899048083289

    with open("input.txt") as file:
        lines = file.readlines()
    tiles = parse_tiles(lines)
    print(len(tiles))
    tile_id, tile = tiles.popleft()
    size = len(tile)
    tiles.appendleft((tile_id, tile))
    arranged = arrange_tiles(tiles)
    print(len(arranged))
    locations = get_locs(arranged)
    for row in locations:
        print(row)
    if all(elem is not None for row in locations for elem in row):
        print(locations[0][0] * locations[0][-1] * locations[-1][0] * locations[-1][-1])

    image = get_image(arranged)
    print(len(image), len(image[0]))
    remaining = find_dragons(image)
    print(remaining)
   