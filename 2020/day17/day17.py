from collections.abc import Generator
from itertools import product


Cube = tuple[int, int, int]
Grid = set[Cube]

Hypercube = tuple[int, int, int, int]
Hypergrid = set[Hypercube]


def yield_neighbors(cube: Cube) -> Generator[Cube, None, None]:
    return ((cube[0] + i, cube[1] + j, cube[2] + k) for i, j, k in product(*[[-1, 0, 1]] * 3) if not (i == j == k == 0))


def yield_hyper_neighbors(hcube: Hypercube) -> Generator[Hypercube, None, None]:
    return ((hcube[0] + i, hcube[1] + j, hcube[2] + k, hcube[3] + l) for i, j, k, l in product(*[[-1, 0, 1]] * 4) if not (i == j == k == l == 0))


def run_cycle(cubes: Grid) -> Grid:
    cubes_after: Grid = set()
    candidates: dict[Cube, int] = {}
    inactive: Grid = set()
    for cube in cubes:
        active = 0
        for neighbor in yield_neighbors(cube):
            if neighbor in cubes:
                active += 1
            elif neighbor not in inactive:
                candidates[neighbor] = candidates.get(neighbor, 0) + 1
                if candidates[neighbor] > 3:
                    inactive.add(neighbor)
                    candidates.pop(neighbor)
        if active in {2, 3}:
            cubes_after.add(cube)
    new_active = {cube for cube, count in candidates.items() if count == 3}
    return cubes_after | new_active


def run_hcycle(hcubes: Hypergrid) -> Hypergrid:
    hcubes_after: Hypergrid = set()
    candidates: dict[Hypercube, int] = {}
    inactive: Hypergrid = set()
    for hcube in hcubes:
        active = 0
        for neighbor in yield_hyper_neighbors(hcube):
            if neighbor in hcubes:
                active += 1
            elif neighbor not in inactive:
                candidates[neighbor] = candidates.get(neighbor, 0) + 1
                if candidates[neighbor] > 3:
                    inactive.add(neighbor)
                    candidates.pop(neighbor)
        if active in {2, 3}:
            hcubes_after.add(hcube)
    new_active = {hcube for hcube, count in candidates.items() if count == 3}
    return hcubes_after | new_active


def run_cycles(cubes: Grid, cycles: int) -> Grid:
    for _ in range(cycles):
        cubes = run_cycle(cubes)
    return cubes


def run_hcycles(hcubes: Hypergrid, cycles: int) -> Hypergrid:
    for _ in range(cycles):
        hcubes = run_hcycle(hcubes)
    return hcubes


def parse_active(lines: list[str]) -> Grid:
    grid: Grid = set()
    for y, row in enumerate(lines):
        for x, cube in enumerate(row.strip()):
            if cube == "#":
                grid.add((x, y, 0))
    return grid


def parse_hyper_active(lines: list[str]) -> Hypergrid:
    hgrid: Hypergrid = set()
    for y, row in enumerate(lines):
        for x, hcube in enumerate(row.strip()):
            if hcube == "#":
                hgrid.add((x, y, 0, 0))
    return hgrid


if __name__ == "__main__":
    with open("sample.txt") as file:
        cubes = parse_active(file.readlines())
    
    cubes = run_cycles(cubes, 6)
    assert (result := len(cubes)) == 112, result

    with open("sample.txt") as file:
        hcubes = parse_hyper_active(file.readlines())
    
    hcubes = run_hcycles(hcubes, 6)
    assert (result := len(hcubes)) == 848, result

    with open("input.txt") as file:
        cubes = parse_active(file.readlines())
    
    cubes = run_cycles(cubes, 6)
    print(len(cubes))

    with open("input.txt") as file:
        hcubes = parse_hyper_active(file.readlines())
    
    hcubes = run_hcycles(hcubes, 6)
    print(len(hcubes))
