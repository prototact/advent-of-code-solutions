from typing import Optional
from collections.abc import Generator
from collections import deque, Counter
from itertools import product, combinations


Point = tuple[int, int, int]


def flip_axis(axis: int, point: Point) -> Point:
    x, y, z = point
    if axis == 0:
        return -x, y, z
    if axis == 1:
        return x, -y, z
    if axis == 2:
        return x, y, -z
    raise ValueError(f"Bad axis value {axis}, must be between 0 and 2")

# counter-clock-wise
def rotate_axis(axis: int, point: Point) -> Point:
    x, y, z = point
    if axis == 0:
        return x, -z, y
    if axis == 1:
        return -z, y, x
    if axis == 2:
        return y, -x, z
    raise ValueError(f"Bad axis value {axis}, must be between 0 and 2")
    

def rotate_axis_clockwise(axis: int, point: Point) -> Point:
    x, y, z = point
    if axis == 0:
        return x, z, -y
    if axis == 1:
        return z, y, -x
    if axis == 2:
        return -y, x, z
    raise ValueError(f"Bad axis value {axis}, must be between 0 and 2")


def suborientations(cube: set[Point], total: list[set[Point]]) -> Generator[set[Point], None, None]:
    yield cube
    total.append(cube)
    rotated = cube
    for _ in range(3):
        rotated = set(rotate_axis(0, point) for point in rotated)
        yield rotated
        total.append(rotated)
    flipped = set(flip_axis(0, point) for point in cube)
    yield flipped
    total.append(flipped)
    for _ in range(3):
        flipped = set(rotate_axis(0, point) for point in flipped)
        yield flipped
        total.append(flipped)


def orientations(xcube: set[Point]) -> Generator[set[Point], None, None]:
    total: list[set[Point]] = []
    yield from suborientations(xcube, total)

    ycube = set(rotate_axis_clockwise(0, rotate_axis_clockwise(2, point)) for point in xcube)
    yield from suborientations(ycube, total)

    zcube = set(rotate_axis(0, rotate_axis(1, point)) for point in xcube)
    yield from suborientations(zcube, total)
    counter = Counter(frozenset(points) for points in total)
    print(f"unique orientations {len(counter)}, should be 24")


def overlap_cubes(cube: set[Point], other: set[Point]) -> Optional[set[Point]]:
    # it has to be between -2000 and 2000 otherwise no overlap
    # in all three dimensions
    candidates: list[set[Point]]=  []
    for oriented in orientations(other):
        for ref, far in product(cube, oriented):
            dx, dy, dz = [x_ - x for x_, x in zip(far, ref)]
            translated = set((x_ - dx, y_ - dy, z_ - dz) for x_, y_, z_ in oriented)
            intersection = translated & cube
            if len(intersection) >= 12:
                candidates.append(translated)
    if candidates:
        cnt = Counter(frozenset(points) for points in candidates)
        assert len(cnt) == 1
        print(f"the count of candidates is {len(candidates)}")
        return max(candidates, key=lambda cand: len(cube & cand))
        

def parse_scanners(lines: list[str]) -> deque[set[Point]]:
    scanners: deque[set[Point]] = deque()
    scanner: set[Point] = set()
    for line in lines:
        line = line.strip()
        if line.startswith("---"):
            continue
        elif not line:
            scanners.append(scanner)
            scanner = set()
        else:
            x, y, z  = line.split(",")
            point: Point = (int(x), int(y), int(z))
            scanner.add(point)
    else:
        scanners.append(scanner)
    return scanners


def merge_scanners(scanners: deque[set[Point]]) -> Optional[set[Point]]:
    indexed = {str(i): scanner for i, scanner in enumerate(scanners)}
    tried_combs: set[tuple[str, str]] = set()
    while len(indexed) > 1:
        for idx, jdx in combinations(indexed.keys(), r=2):
            if (idx, jdx) in tried_combs:
                if set(combinations(indexed.keys(), r=2)) <= tried_combs:
                    print("Failed to solve the problem")
                    return
                continue
            else:
                tried_combs.add((idx, jdx))
            cube = indexed.pop(idx)
            other = indexed.pop(jdx)
            print(f"trying again {jdx} with {idx}")
            found = overlap_cubes(cube, other)
            if found is not None:
                translated = found
                merged = cube | translated
                indexed[f"{idx}-{jdx}"] = merged
                print(f"merged two scanners, {idx} with {jdx}!")
                break
            else:
                indexed[jdx] = other
                indexed[idx] = cube
                print(f"no overlap found between {idx} and {jdx}")
        
    _, final = indexed.popitem()
    return final


if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines() 
    scanners = parse_scanners(lines)
    assert len(scanners) == 5
    merged = merge_scanners(scanners)
    assert merged is not None
    assert len(merged) == 79, len(merged)

    # with open("input.txt") as file:
    #    lines = file.readlines()
    # scanners = parse_scanners(lines)
    # assert len(scanners) == 34
    # merged = merge_scanners(scanners)
    # print(len(merged))
