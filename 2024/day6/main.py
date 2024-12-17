from typing import Optional
from enum import Enum
from collections import deque
from itertools import islice


class Direction(Enum):
    Up = (-1, 0)
    Down = (1, 0)
    Left = (0, -1)
    Right = (0, 1)

    def turn_right(self) -> "Direction":
        match self:
            case Direction.Up:
                return Direction.Right
            case Direction.Right:
                return Direction.Down
            case Direction.Down:
                return Direction.Left
            case Direction.Left:
                return Direction.Up
            case _:
                raise ValueError("Impossible, enum has a specific number of values and it is covered here.")
            
    def get_icon(self) -> str:
        match self:
            case Direction.Up:
                return "^"
            case Direction.Right:
                return ">"
            case Direction.Down:
                return "v"
            case Direction.Left:
                return "<"
            case _:
                raise ValueError("Impossible, enum has a specific number of values and it is covered here.")


def print_grid(grid: list[list[bool]], guard_pos: tuple[int, int], dir_: Direction) -> None:
    for idx, row in enumerate(grid):
        row = "".join(dir_.get_icon() if guard_pos == (idx, jdx) else "." if spot else "#" for jdx, spot in enumerate(row))
        print(row)
    print()


def count_guard_path(grid: list[list[bool]], guard_pos: tuple[int, int], trace: bool = False) -> int:
    x_border, y_border = len(grid), len(grid[0])
    def is_outside(x: int, y: int) -> bool:
        return x < 0 or x >= x_border or y < 0 or y >= y_border
    def move_guard(guard_pos: tuple[int, int], dir_: Direction) -> tuple[Optional[tuple[int, int]], Direction]:
        x, y = guard_pos
        dx, dy = dir_.value
        x_new, y_new = x + dx, y + dy
        if is_outside(x_new, y_new):
            return None, dir_
        if grid[x_new][y_new]:
            return (x_new, y_new), dir_
        return guard_pos, dir_.turn_right()
    
    dir_ = Direction.Up
    visited: set[tuple[int, int]] = {guard_pos}
    while guard_pos is not None:
        guard_pos, dir_ = move_guard(guard_pos, dir_)
        if trace:
            print_grid(grid, guard_pos, dir_)
        if guard_pos is not None:
            visited.add(guard_pos)

    return len(visited)



def find_loops(grid: list[list[bool]], init_guard_pos: tuple[int, int]) -> int:
    x_border, y_border = len(grid), len(grid[0])
    def is_outside(x: int, y: int) -> bool:
        return x < 0 or x >= x_border or y < 0 or y >= y_border
    def move_guard(guard_pos: tuple[int, int], dir_: Direction, block: tuple[int, int] = None) -> tuple[Optional[tuple[int, int]], Direction, bool]:
        x, y = guard_pos
        dx, dy = dir_.value
        x_new, y_new = x + dx, y + dy
        if is_outside(x_new, y_new):
            return None, dir_, True
        if grid[x_new][y_new] and (block is None or block != (x_new, y_new)):
            return (x_new, y_new), dir_, True
        return guard_pos, dir_.turn_right(), False

    def is_loop(trajectory: deque[tuple[int, int]]) -> bool:
        loop: list[tuple[int, int]] = []
        for idx, pos in enumerate(trajectory):
            if loop and pos == loop[0] and loop == list(islice(trajectory, idx, idx + len(loop))):
                print(f"The size of the loop was {len(loop)}")
                return True
            loop.append(pos)
            if len(loop) > len(trajectory) - idx:
                return False
        return False

    def is_loop_trick(trajectory: deque[tuple[int, int]]) -> bool:
        seen: list[tuple[int, int]] = []
        idx = 0
        temp: list[tuple[int, int]] = []
        for pos in trajectory:
            if seen and idx == len(seen):
                return True
            if seen and seen[idx] == pos:
                idx += 1
                temp.append(pos)
            elif seen and seen[idx] != pos:
                idx = 0
                seen.extend(temp)
                temp = []
                seen.append(pos)
            else:
                seen.append(pos)
        return False

    def find_loop(guard_pos: tuple[int, int], dir_: Direction, block: tuple[int, int], estimated_size: int) -> bool:
        trajectory = deque([guard_pos])
        total_steps = 0
        while True:
            guard_pos, dir_, step = move_guard(guard_pos, dir_, block) 
            if guard_pos is None:
                return False
            total_steps += step
            if step:
                trajectory.appendleft(guard_pos)
                if not (total_steps % estimated_size) and is_loop_trick(trajectory):
                    return True

    init_dir = Direction.Up
    dir_ = init_dir
    visited: set[tuple[int, int]] = set()
    guard_pos = init_guard_pos
    while guard_pos is not None:
        guard_pos, dir_, _ = move_guard(guard_pos, dir_)
        if guard_pos is not None and guard_pos != init_guard_pos:
            visited.add(guard_pos)
    return sum(find_loop(init_guard_pos, init_dir, block, len(visited)) for block in visited)


def read_map(filename: str) -> tuple[list[list[bool]], tuple[int, int]]:
    grid: list[list[bool]] = []
    guard_pos: Optional[tuple[int, int]] = None
    with open(filename) as file:
        for idx, line in enumerate(map(lambda x: x.strip(), file.readlines())):
            if guard_pos is None and Direction.Up.get_icon() in line:
                guard_pos = (idx, line.index(Direction.Up.get_icon())) 
            grid.append([c in {".", "^"} for c in line])
    if guard_pos is None:
        raise ValueError("Missing guard position on the grid, check input!")
    return grid, guard_pos


if __name__ == "__main__":
    grid, guard_pos = read_map("sample.txt")
    print(count_guard_path(grid, guard_pos))
    print(find_loops(grid, guard_pos))

    grid, guard_pos = read_map("input.txt")
    print(count_guard_path(grid, guard_pos))
    print(find_loops(grid, guard_pos))
