from dataclasses import dataclass
from itertools import combinations

Coord = tuple[int, int]
Pair = tuple[Coord, Coord]


@dataclass
class Galaxies:
    _grid: list[list[bool]]
    _empty_rows: set[int]
    _empty_cols: set[int]
    _expansion_offset: int

    @classmethod
    def parse(cls, lines: list[str], offset: int) -> "Galaxies":
        grid = [[elem == "#" for elem in line.strip()] for line in lines]
        empty_rows = {idx for idx, row in enumerate(grid) if not any(row)}
        empty_cols = {
            idx for idx, _ in enumerate(grid[0]) if not any(row[idx] for row in grid)
        }
        return cls(grid, empty_rows, empty_cols, offset)

    def _find_galaxies(self) -> list[Coord]:
        return [
            (idx, jdx)
            for idx, row in enumerate(self._grid)
            for jdx, elem in enumerate(row)
            if elem
        ]

    def _count_empty_between(self, pair: Pair) -> tuple[int, int]:
        (left_row, left_col), (right_row, right_col) = pair
        if left_row > right_row:
            right_row, left_row = left_row, right_row
        empty_rows = sum(
            1 for row in range(left_row + 1, right_row) if row in self._empty_rows
        )

        if left_col > right_col:
            right_col, left_col = left_col, right_col

        empty_cols = sum(
            1 for col in range(left_col + 1, right_col) if col in self._empty_cols
        )
        return empty_rows, empty_cols

    def _compute_distance(self, pair: Pair) -> int:
        left, right = pair
        empty_rows, empty_cols = self._count_empty_between(pair)
        dx = abs(right[0] - left[0]) + empty_rows * (self._expansion_offset - 1)
        dy = abs(right[1] - left[1]) + empty_cols * (self._expansion_offset - 1)
        return dx + dy

    def compute_shortest_distance_between_all_pairs(self) -> int:
        galaxies = self._find_galaxies()
        return sum(self._compute_distance(pair) for pair in combinations(galaxies, r=2))


if __name__ == "__main__":
    with open("sample.txt") as file:
        galaxies = Galaxies.parse(file.readlines(), 2)
    distance = galaxies.compute_shortest_distance_between_all_pairs()
    assert distance == 374, distance

    with open("sample.txt") as file:
        galaxies = Galaxies.parse(file.readlines(), 10)
    distance = galaxies.compute_shortest_distance_between_all_pairs()
    assert distance == 1030, distance

    with open("sample.txt") as file:
        galaxies = Galaxies.parse(file.readlines(), 100)
    distance = galaxies.compute_shortest_distance_between_all_pairs()
    assert distance == 8410, distance

    with open("input.txt") as file:
        galaxies = Galaxies.parse(file.readlines(), 2)
    distance = galaxies.compute_shortest_distance_between_all_pairs()
    print(distance)

    with open("input.txt") as file:
        galaxies = Galaxies.parse(file.readlines(), 1_000_000)
    distance = galaxies.compute_shortest_distance_between_all_pairs()
    print(distance)
