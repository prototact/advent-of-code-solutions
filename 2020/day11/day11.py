from enum import Enum


DIRECTIONS: list[tuple[int, int]] = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]


class Seat(Enum):
    Floor = 0
    Empty = 1
    Occupied = 2

    def __str__(self):
        if self == Seat.Floor:
            return "."
        if self == Seat.Empty:
            return "L"
        return "#"


Grid = list[list[Seat]]


def convert_seat(seat:str) -> Seat:
    if seat == ".":
        return Seat.Floor
    if seat == "L":
        return Seat.Empty
    if seat == "#":
        return Seat.Occupied
    raise ValueError("Seat type does not exist.")


def get_seat(grid: Grid, row: int, col: int) -> tuple[Seat, bool]:
    row_count = len(grid)
    col_count = len(grid[0])
    if row < 0 or col < 0 or row >= row_count or col >= col_count:
        return Seat.Floor, True
    return grid[row][col], False


def count_neighbors(row: int, col: int, grid: Grid, long_vision: bool, directions: list[tuple[int, int]] = DIRECTIONS) -> int:
    count_ = 0
    for drow, dcol in directions:
        cur_row = row + drow
        cur_col = col + dcol
        seat, is_out_of_bounds = get_seat(grid, cur_row, cur_col)
        while long_vision and seat == Seat.Floor and not is_out_of_bounds:
                cur_row += drow
                cur_col += dcol
                seat, is_out_of_bounds = get_seat(grid, cur_row, cur_col)
        if seat == Seat.Occupied:
            count_ += 1
    return count_


def take_turn(grid: Grid, long_vision: bool, tolerance: int) -> Grid:
    copy: Grid = []
    for ridx, row in enumerate(grid):
        new_row: list[Seat] = []
        for cidx, seat in enumerate(row):
            occupied = count_neighbors(ridx, cidx, grid, long_vision)
            if seat == Seat.Empty and occupied == 0:
                seat = Seat.Occupied
            elif seat == Seat.Occupied and occupied >= tolerance:
                seat = Seat.Empty
            new_row.append(seat)
        copy.append(new_row)
    return copy


def until_is_equal(grid: Grid, tolerance: int, long_vision: bool = False) -> Grid:
    new_grid = take_turn(grid, long_vision, tolerance)
    while grid != new_grid:
        new_grid, grid = take_turn(new_grid, long_vision, tolerance), new_grid
    return new_grid


def count_occupied(grid: list[list[Seat]]) -> int:
    return sum(seat == Seat.Occupied for row in grid for seat in row)


if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        grid: Grid = []
        for line in file.readlines():
            grid.append([convert_seat(char) for char in line.strip()])

    new_grid = until_is_equal(grid, 4)
    assert (result := count_occupied(new_grid)) == 37, result

    new_grid = until_is_equal(grid, 5, long_vision=True)
    assert (result := count_occupied(new_grid)) == 26, result

    with open("input.txt", "r") as file:
        grid = []
        for line in file.readlines():
            grid.append([convert_seat(char) for char in line.strip()])

    new_grid = until_is_equal(grid, 4)
    print(count_occupied(new_grid))

    new_grid = until_is_equal(grid, 5, long_vision=True)
    print(count_occupied(new_grid))
