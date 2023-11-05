from math import gcd, sqrt
from typing import Optional


def sign(num: int) -> int:
    return 1 if num > 0 else  -1


def compute_quadrant(horiz_rng: range, vert_rng: range, added: set[tuple[int, int]], reverse: bool) -> list[tuple[int, int]]:
    dirs: list[tuple[int, int]] = []
    for horiz in horiz_rng:
        for vert in vert_rng:
            if horiz == 0 and vert == 0:
                continue
            elif horiz == 0:
                dir_ = (sign(vert), 0)
            elif vert == 0:
                dir_ = (0, sign(horiz))
            else:
                common = gcd(abs(horiz), abs(vert))
                dir_ = (vert // common, horiz // common)
            if dir_ not in added:
                dirs.append(dir_)
                added.add(dir_)
    return sorted(dirs, key=lambda x: x[1]/sqrt(x[1] ** 2 + x[0] ** 2), reverse=reverse)


def compute_directions(loc: tuple[int, int], dims: tuple[int, int]) -> list[tuple[int, int]]:
    height, width = dims
    dirs: list[tuple[int, int]] = []
    added: set[tuple[int, int]] = set()
    left = - loc[1]
    right = width - loc[1]
    up = - loc[0]
    down = height - loc[0]
    # top right quadrant
    dirs.extend(compute_quadrant(range(right + 1), range(up, 1), added, reverse=False))
    # bottom right quadrant
    dirs.extend(compute_quadrant(range(right, -1, -1), range(down + 1), added, reverse=True))
    # bottom left quadrant
    dirs.extend(compute_quadrant(range(0, left - 1, -1), range(down, -1, -1), added, reverse=True))
    # top left quadrant
    dirs.extend(compute_quadrant(range(left, 1), range(0, up - 1, -1), added, reverse=False))

    return dirs

def count_viewable(loc: tuple[int, int], field: list[str]) -> int:
    width = len(field[0])
    height = len(field)
    def search(dir_: tuple[int, int], init_: int) -> int:
        horiz = loc[1] + dir_[1] * init_
        vert = loc[0] + dir_[0] * init_
        if horiz >= width or horiz < 0:
            return 0
        if vert >= height or vert < 0:
            return 0
        if field[vert][horiz] == '#':
            return 1
        return search(dir_, init_ + 1)
    directions = compute_directions(loc, (height, width))
    return sum(search(dir_, 1) for dir_ in directions)


def find_best(field: list[str]) -> Optional[tuple[int, tuple[int, int]]]:
    locs: list[tuple[int, int]] = []
    for idx, row in enumerate(field):
        for jdx, point in enumerate(row):
            if point == "#":
                locs.append((idx, jdx))
    max_ = None
    max_locs = None
    for loc in locs:
        viewable = count_viewable(loc, field)
        if max_ is None:
            max_locs = loc
            max_ = viewable
        elif viewable > max_:
            max_locs = loc
            max_ = viewable
    if max_ is not None and max_locs is not None:
        return max_, max_locs


def find_nth_eliminated(coords: tuple[int, int], n: int, field: list[str]) -> tuple[int, int]:
    # sort directions in from (-1, 0) clock-wise
    dims = len(field), len(field[0])
    height, width = dims
    dirs = compute_directions(coords, dims)
    copy = [[0 if spot == '.' else 1 for spot in row] for row in field]
    def laser(dir_: tuple[int, int], init_: int) -> Optional[tuple[int, int]]:
        horiz = coords[1] + dir_[1] * init_
        vert = coords[0] + dir_[0] * init_
        if horiz >= width or horiz < 0:
            return
        if vert >= height or vert < 0:
            return
        if copy[vert][horiz] == 1:
            copy[vert][horiz] = 0
            return vert, horiz
        return laser(dir_, init_ + 1)
    while True:
        for dir_ in dirs:
            lasered = laser(dir_, 1)
            if lasered is not None:
               n -= 1
            if n == 0 and lasered is not None:
                return lasered


if __name__ == "__main__":
    with open("sample1.txt") as file:
        field = [line.strip() for line in file.readlines()]
    res = find_best(field)
    assert res is not None and res[0] == 8, res

    with open("sample2.txt") as file:
        field = [line.strip() for line in file.readlines()]
    res = find_best(field)
    assert res is not None and res[0] == 33, res

    with open("sample5.txt") as file:
        field = [line.strip() for line in file.readlines()]
    res = find_best(field)
    assert res is not None and res[0] == 210, res
    coords = res[1]
    lasered = find_nth_eliminated(coords, 200, field)
    assert (lasered[1] * 100) + lasered[0] == 802, lasered

    print("finished tests")

    with open("input.txt") as file:
        field = [line.strip() for line in file.readlines()]
    res = find_best(field)
    print(res)
    if res is not None:
       coords = res[1]
       lasered = find_nth_eliminated(coords, 200, field)
       print(lasered[1] * 100 + lasered[0])
