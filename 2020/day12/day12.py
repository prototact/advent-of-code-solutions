from enum import Enum


class Direction(Enum):
    North = 0
    East = 1
    South = 2
    West = 3


Ship = tuple[Direction, int, int]

Point = tuple[int, int]

class Action(Enum):
    North = 0
    East = 1
    South = 2
    West = 3
    Left = 4
    Right = 5
    Forward = 6


def parse_action(line: str) -> tuple[Action, int]:
    letter, size = line[0], int(line[1:])
    if letter == "N":
        action = Action.North
    elif letter == "E":
        action = Action.East
    elif letter == "S":
        action = Action.South
    elif letter == "W":
        action = Action.West
    elif letter == "L":
        action = Action.Left
    elif letter == "R":
        action = Action.Right
    elif letter == "F":
        action = Action.Forward
    else:
        raise ValueError(f"Unknown action: {letter}")
    return (action, size)


def distance(start: Ship, end: Ship) -> int:
    _, init_north, init_east = start
    _, final_north, final_east = end
    return abs(final_north - init_north) + abs(final_east - init_east)


def simple_distance(start: Point, end: Point) -> int:
    init_north, init_east = start
    final_north, final_east = end
    return abs(final_north - init_north) + abs(final_east - init_east)


def change_direction(direction: Direction, size: int) -> Direction:
    if direction == Direction.North:
        if size == 90:
            return Direction.West
        if size == 180:
            return Direction.South
        if size == 270:
            return Direction.East
        if size == -90:
            return Direction.East
        if size == -180:
            return Direction.South
        if size == -270:
            return Direction.West
        raise ValueError(f"Unknown angle {size}")
    if direction == Direction.East:
        if size == 90:
            return Direction.North
        if size == 180:
            return Direction.West
        if size == 270:
            return Direction.South
        if size == -90:
            return Direction.South
        if size == -180:
            return Direction.West
        if size == -270:
            return Direction.North
        raise ValueError(f"Unknown angle {size}")
    if direction == Direction.South:
        if size == 90:
            return Direction.East
        if size == 180:
            return Direction.North
        if size == 270:
            return Direction.West
        if size == -90:
            return Direction.West
        if size == -180:
            return Direction.North
        if size == -270:
            return Direction.East
        raise ValueError(f"Unknown angle {size}")
    if direction == Direction.West:
        if size == 90:
            return Direction.South
        if size == 180:
            return Direction.East
        if size == 270:
            return Direction.North
        if size == -90:
            return Direction.North
        if size == -180:
            return Direction.East
        if size == -270:
            return Direction.South
        raise ValueError(f"Unknown angle {size}")
    raise ValueError(f"Uknown direction {direction}")


def do_actions(start: Ship, actions: list[tuple[Action, int]]) -> Ship:
    direction, north, east = start
    for action in actions:
        match action:
            case (Action.North, size):
                north += size
            case (Action.East, size):
                east += size
            case (Action.South, size):
                north -= size
            case (Action.West, size):
                east -= size
            case (Action.Left, size):
                direction = change_direction(direction, size)
            case (Action.Right, size):
                direction = change_direction(direction, -size)
            case (Action.Forward, size):
                if direction == Direction.North:
                    north +=  size
                elif direction == Direction.East:
                    east += size
                elif direction == Direction.South:
                    north -= size
                elif direction == Direction.West:
                    east -= size

    return (direction, north, east)


def change_direction_waypoint(ship: Point, waypoint: Point, size: int) -> tuple[int, int]:
    north, east = ship
    wnorth, weast = waypoint
    ediff, ndiff = (weast - east, wnorth - north)
    if size == 90 or size == -270:
        ediff, ndiff = -ndiff, ediff
    elif size == 180 or size == -180:
        ndiff = -ndiff
        ediff = -ediff
    elif size == 270 or size == -90:
        ediff, ndiff = ndiff, -ediff
    else:
        raise ValueError(f"Unknown angle {size}")
    return (north + ndiff, east + ediff)


def move_forward(ship: Point, waypoint: Point, size: int) -> tuple[int, int, int, int]:
    north, east = ship
    wnorth, weast = waypoint
    ndiff, ediff = (wnorth - north, weast - east)
    north += ndiff * size
    east += ediff * size
    wnorth += ndiff * size
    weast += ediff * size
    return north, east, wnorth, weast


def do_actions_waypoint(start: Point, waypoint: Point, actions: list[tuple[Action, int]]) -> tuple[Point, Point]:
    north, east = start
    wnorth, weast = waypoint
    for action in actions:
        match action:
            case (Action.North, size):
                wnorth += size
            case (Action.East, size):
                weast += size
            case (Action.South, size):
                wnorth -= size
            case (Action.West, size):
                weast -= size
            case (Action.Left, size):
                wnorth, weast = change_direction_waypoint((north, east), (wnorth, weast), size)
            case (Action.Right, size):
                wnorth, weast = change_direction_waypoint((north, east), (wnorth, weast), -size)
            case (Action.Forward, size):
                north, east, wnorth, weast = move_forward((north, east), (wnorth, weast), size)
    return (north, east), (wnorth, weast)


if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        actions = [parse_action(line.strip()) for line in file.readlines()] 

    start = (Direction.East, 0, 0)
    end = do_actions(start, actions)
    assert distance(start, end) == 25

    start = (0, 0)
    waypoint = (1, 10)
    end, waypoint_end = do_actions_waypoint(start, waypoint, actions)
    assert simple_distance(start, end) == 286

    with open("input.txt", "r") as file:
        actions = [parse_action(line.strip()) for line in file.readlines()] 

    start = (Direction.East, 0, 0)
    end = do_actions(start, actions)
    print(distance(start, end))

    start = (0, 0)
    waypoint = (1, 10)
    end, _ = do_actions_waypoint(start, waypoint, actions)
    print(simple_distance(start, end))
