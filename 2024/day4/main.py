from typing import Optional
from itertools import permutations


Grid = list[list[str]]


DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1), (1 , 1), (1, -1), (-1, 1), (-1, -1)]


def scan(grid: Grid, word: str) -> int:
    def nested_search(idx: int, jdx: int, word: str, dir_: Optional[tuple[int, int]]) -> int:
        if not word:
            return True
        if dir_ is None:
            chosen_directions = DIRECTIONS
        else:
            chosen_directions = [dir_]
        valid_directions = [(x, y) for x,y in chosen_directions if idx + x >= 0 and idx + x < len(grid) and jdx + y >= 0 and jdx + y < len(grid[0])]
        if not valid_directions:
            return False
        return sum(nested_search(idx + x, jdx + y, word[1:], (x, y)) for x, y in valid_directions if grid[idx + x][jdx + y] == word[0])
    return sum(nested_search(idx, jdx, word[1:], None) for idx, row in enumerate(grid) for jdx, letter in enumerate(row) if letter == word[0])

def scan_cross(grid: Grid, word: str) -> int:
    assert len(word) % 2 == 1
    mid = len(word) // 2
    def local_search(idx: int, jdx: int, front: str, back: str) -> bool:
        def check_x(x: int) -> bool:
            return x + idx >= 0 and x + idx < len(grid)
        def check_y(y: int) -> bool:
            return y + jdx >= 0 and y + jdx < len(grid[0])
        def search_diag(x: int, y: int, left: str, right: str, depth: int = 1) -> bool:
            def check(x: int, y: int) -> bool:
                dirs_exist = check_x(x * depth) and check_x(-x * depth) and check_y(y * depth) and check_y(-y * depth)
                return dirs_exist and left[0] == grid[idx + x * depth][jdx + y * depth] and right[0] == grid[idx - x * depth][jdx - y * depth]
            if not left and not right:
                return True
            return (check(x, y)
                    and search_diag(x, y, left[1:], right[1:], depth + 1)
                    )
        def make_dirs() -> list[tuple[str, str, str, str]]:
            return map(lambda assignment: [(x, dir_) for x, dir_ in zip([1, 1, 1, -1], assignment)],
                ((lupart, rdpart, rupart, ldpart) for lupart, rdpart in permutations([front[::-1], back]) for rupart, ldpart in permutations([back, front[::-1]])
                ))
        return any(search_diag(x, y, lupart, rdpart, 1) and search_diag(z, w, rupart, ldpart) for (x, lupart), (y, rdpart), (z, rupart), (w, ldpart) in make_dirs())
    return sum(local_search(idx, jdx, word[:mid], word[mid + 1:]) for idx, row in enumerate(grid) for jdx, letter in enumerate(row) if letter == word[mid])


def parse_grid(filename: str) -> Grid:
    with open(filename) as file:
        grid = [list(line) for line in map(lambda x: x.strip(), file.readlines())]
    return grid


if __name__ == "__main__":
    grid = parse_grid("sample.txt")
    print(scan(grid, "XMAS"))
    print(scan_cross(grid, "MAS"))

    grid = parse_grid("input.txt")
    print(scan(grid, "XMAS"))
    print(scan_cross(grid, "MAS"))
