from dataclasses import dataclass
from enum import Enum, IntEnum


class Side(IntEnum):
    North = 1
    East = 2
    South = 3
    West = 4


class Pipe(Enum):
    NorthToSouth = 1
    WestToEast = 2
    NorthToEast = 3
    NorthToWest = 4
    SouthToWest = 5
    SouthToEast = 6
    Start = 7
    Ground = 8

    @staticmethod
    def parse_pipe(elem: str) -> "Pipe":
        match elem:
            case "|":
                return Pipe.NorthToSouth
            case "-":
                return Pipe.WestToEast
            case "L":
                return Pipe.NorthToEast
            case "J":
                return Pipe.NorthToWest
            case "7":
                return Pipe.SouthToWest
            case "F":
                return Pipe.SouthToEast
            case "S":
                return Pipe.Start
            case ".":
                return Pipe.Ground
            case _:
                raise ValueError(f"Bad string {elem}!")


@dataclass
class Tile:
    pipe: Pipe
    side: list[Side]

    @classmethod
    def create_with_sides(cls, pipe: Pipe) -> "Tile":
        match pipe:
            case Pipe.NorthToSouth:
                return cls(pipe, [Side.North, Side.South])
            case Pipe.NorthToEast:
                return cls(pipe, [Side.North, Side.East])
            case Pipe.NorthToWest:
                return cls(pipe, [Side.North, Side.West])
            case Pipe.WestToEast:
                return cls(pipe, [Side.East, Side.West])
            case Pipe.SouthToEast:
                return cls(pipe, [Side.East, Side.South])
            case Pipe.SouthToWest:
                return cls(pipe, [Side.South, Side.West])
            case Pipe.Ground:
                return cls(pipe, [])
            case _:
                raise ValueError(f"Invalid pipe {pipe}")


@dataclass
class TileGrid:
    _grid: list[list[Tile]]
    _start: tuple[int, int]

    @classmethod
    def parse_pipes_with_start(cls, lines: list[str]) -> "TileGrid":
        grid: list[list[Pipe]] = []
        start: tuple[int, int] | None = None
        for y, line in enumerate(lines):
            row: list[Pipe] = []
            for x, elem in enumerate(line.strip()):
                pipe = Pipe.parse_pipe(elem)
                if pipe == Pipe.Start:
                    start = (x, y)
                row.append(pipe)
            grid.append(row)
        if start is not None:
            start_pipe = cls._figure_out_start(grid, start)
            return cls(
                _grid=[
                    [
                        Tile.create_with_sides(
                            pipe if pipe != Pipe.Start else start_pipe
                        )
                        for pipe in row
                    ]
                    for row in grid
                ],
                _start=start,
            )
        raise ValueError(f"Bad input {lines}")

    @staticmethod
    def _figure_out_start(grid: list[list[Pipe]], loc: tuple[int, int]) -> Pipe:
        x, y = loc
        next_tiles: list[Side] = []
        size_y = len(grid)
        size_x = len(grid[0])
        if x - 1 <= 0:
            pipe = grid[y][x - 1]
            if pipe in {Pipe.WestToEast, Pipe.SouthToEast, Pipe.NorthToEast}:
                next_tiles.append(Side.West)
        if x + 1 < size_x:
            pipe = grid[y][x + 1]
            if pipe in {Pipe.WestToEast, Pipe.NorthToWest, Pipe.SouthToWest}:
                next_tiles.append(Side.East)
        if y + 1 < size_y:
            pipe = grid[y + 1][x]
            if pipe in {Pipe.NorthToEast, Pipe.NorthToSouth, Pipe.NorthToWest}:
                next_tiles.append(Side.South)
        if y - 1 >= 0:
            pipe = grid[y - 1][x]
            if pipe in {Pipe.SouthToEast, Pipe.SouthToWest, Pipe.NorthToSouth}:
                next_tiles.append(Side.North)

        match sorted(next_tiles):
            case [Side.North, Side.West]:
                return Pipe.NorthToWest
            case [Side.North, Side.East]:
                return Pipe.NorthToEast
            case [Side.North, Side.South]:
                return Pipe.NorthToSouth
            case [Side.East, Side.South]:
                return Pipe.SouthToEast
            case [Side.East, Side.West]:
                return Pipe.WestToEast
            case [Side.South, Side.West]:
                return Pipe.SouthToWest
            case _:
                raise ValueError(f"Invalid start tile region {grid}")

    def __getitem__(self, loc: tuple[int, int]) -> Tile:
        x, y = loc
        return self._grid[y][x]

    def _get_next(
        self, loc: tuple[int, int], side: Side, tile: Tile
    ) -> tuple[tuple[int, int], Side, Tile]:
        x, y = loc
        match (tile.pipe, side):
            case (Pipe.NorthToEast, Side.North):
                return ((x + 1, y), Side.West, self[x + 1, y])
            case (Pipe.NorthToEast, Side.East):
                return ((x, y - 1), Side.South, self[x, y - 1])
            case (Pipe.NorthToSouth, Side.North):
                return ((x, y + 1), Side.North, self[x, y + 1])
            case (Pipe.NorthToSouth, Side.South):
                return ((x, y - 1), Side.South, self[x, y - 1])
            case (Pipe.NorthToWest, Side.North):
                return ((x - 1, y), Side.East, self[x - 1, y])
            case (Pipe.NorthToWest, Side.West):
                return ((x, y - 1), Side.South, self[x, y - 1])
            case (Pipe.SouthToEast, Side.East):
                return ((x, y + 1), Side.North, self[x, y + 1])
            case (Pipe.SouthToEast, Side.South):
                return ((x + 1, y), Side.West, self[x + 1, y])
            case (Pipe.SouthToWest, Side.South):
                return ((x - 1, y), Side.East, self[x - 1, y])
            case (Pipe.SouthToWest, Side.West):
                return ((x, y + 1), Side.North, self[x, y + 1])
            case (Pipe.WestToEast, Side.East):
                return ((x - 1, y), Side.East, self[x - 1, y])
            case (Pipe.WestToEast, Side.West):
                return ((x + 1, y), Side.West, self[x + 1, y])
            case _:
                raise ValueError(f"Impossible transition {loc, side, tile}")

    def get_loop(self) -> list[tuple[tuple[int, int], Side, Tile]]:
        current = self[self._start]
        loop: list[tuple[tuple[int, int], Side, Tile]] = [
            (self._start, current.side[0], current)
        ]
        while True:
            loc, side, tile = loop[-1]
            loc, side, tile = self._get_next(loc, side, tile)
            if loc == self._start:
                break
            loop.append((loc, side, tile))
        return loop

    def count_inside_area(self) -> int:
        area = 0
        loop = {loc for loc, _, _ in self.get_loop()}
        for y, row in enumerate(self._grid):
            count = False
            parallel: Pipe | None = None
            # somehow account for parallel pipes
            for x, tile in enumerate(row):
                if (x, y) in loop:
                    if tile.pipe == Pipe.SouthToEast:
                        parallel = tile.pipe
                    elif tile.pipe == Pipe.NorthToEast:
                        parallel = tile.pipe
                    elif tile.pipe == Pipe.WestToEast:
                        continue
                    elif tile.pipe == Pipe.SouthToWest and parallel == Pipe.NorthToEast:
                        count = not count
                        parallel = None
                    elif tile.pipe == Pipe.NorthToWest and parallel == Pipe.SouthToEast:
                        count = not count
                        parallel = None
                    elif tile.pipe == Pipe.SouthToWest and parallel == Pipe.SouthToEast:
                        parallel = None
                    elif tile.pipe == Pipe.NorthToWest and parallel == Pipe.NorthToEast:
                        parallel = None
                    else:
                        count = not count
                elif count:
                    area += 1
        return area


if __name__ == "__main__":
    with open("sample.txt") as file:
        tilegrid = TileGrid.parse_pipes_with_start(file.readlines())
    loop = tilegrid.get_loop()
    assert len(loop) // 2 == 8, len(loop)

    with open("sample2.txt") as file:
        tilegrid = TileGrid.parse_pipes_with_start(file.readlines())
    area = tilegrid.count_inside_area()
    assert area == 8, area

    with open("input.txt") as file:
        tilegrid = TileGrid.parse_pipes_with_start(file.readlines())
    loop = tilegrid.get_loop()
    print(len(loop) // 2)

    print(tilegrid.count_inside_area())
