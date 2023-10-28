from typing import Optional

def find_intersection(left: list[str], right: list[str]) -> Optional[int]:
    lpoints = trace_path(left)
    rpoints = trace_path(right)
    intersections = lpoints & rpoints
    min_ = None
    for intersection in intersections:
        norm = abs(intersection[0]) + abs(intersection[1])
        if min_ is None:
            min_ = norm
        elif min_ >= norm:
            min_ = norm
    return min_


def trace_path(wire: list[str]) -> set[tuple[int, int]]:
    pos: tuple[int, int] =  (0, 0)
    points: set[tuple[int, int]] = set()
    for point in wire:
        match point[0], point[1:]:
            case "R", digits:
                vert, horiz = pos
                dx = int(digits)
                for i in range(1, dx + 1):
                    points.add((vert, horiz + i))
                pos = vert, horiz + dx
            case "L", d:
                vert, horiz = pos
                dx = int(d)
                for i in range(1, dx + 1):
                    points.add((vert, horiz - i))
                pos = vert, horiz - dx
            case "U", d:
                vert, horiz = pos
                dx = int(d)
                for i in range(1, dx + 1):
                    points.add((vert + i, horiz))
                pos = vert + dx, horiz
            case "D", d:
                vert, horiz = pos
                dx = int(d)
                for i in range(1, dx + 1):
                    points.add((vert - i, horiz))
                pos = vert - dx, horiz
            case _:
                raise ValueError(f"Unexpected move {point}")
    return points


def find_min_steps(left: list[str], right: list[str]) -> Optional[int]:
    lpoints = trace_path_with_steps(left)
    rpoints = trace_path_with_steps(right)
    intersection = lpoints.keys() & rpoints.keys()
    min_left, min_right = None, None
    for point in intersection:
            ldist, rdist = min(lpoints[point]), min(rpoints[point])
            if min_left is None and min_right is None:
                min_left, min_right = ldist, rdist
            elif min_left + min_right > ldist + rdist:
                min_left, min_right = ldist, rdist
    if min_left is not None and min_right is not None:
        return min_left + min_right


def trace_path_with_steps(wire: list[str]) -> dict[tuple[int, int], list[int]]:
    pos: tuple[int, int, int] = (0, 0, 0)
    points: dict[tuple[int, int], list[int]] = {}
    for point in wire:
        match point[0], point[1:]:
            case "R", digits:
                vert, horiz, dist = pos
                dx = int(digits)
                for i in range(1, dx + 1):
                    new_point = vert, horiz + i
                    dists = points.get(new_point, [])
                    dists.append(dist + i)
                    points[new_point] = dists
                pos = vert, horiz + dx, dist + dx
            case "L", digits:
                vert, horiz, dist = pos
                dx = int(digits)
                for i in range(1, dx + 1):
                    new_point = vert, horiz - i
                    dists = points.get(new_point, [])
                    dists.append(dist + i)
                    points[new_point] = dists
                pos = vert, horiz - dx, dist + dx
            case "U", digits:
                vert, horiz, dist = pos
                dx = int(digits)
                for i in range(1, dx + 1):
                    new_point = vert + i, horiz
                    dists = points.get(new_point, [])
                    dists.append(dist + i)
                    points[new_point] = dists
                pos = vert + dx, horiz, dist + dx
            case "D", digits:
                vert, horiz, dist = pos
                dx = int(digits)
                for i in range(1, dx + 1):
                    new_point = vert - i, horiz
                    dists = points.get(new_point, [])
                    dists.append(dist + i)
                    points[new_point] = dists
                pos = vert - dx, horiz, dist + dx
            case _:
                raise ValueError(f"Unexpected move {point}")
    return points



if __name__ == "__main__":
    left = ["R8", "U5","L5", "D3"]
    right = ["U7", "R6", "D4", "L4"]

    dist = find_intersection(left, right)
    assert dist == 6, dist

    total_dist = find_min_steps(left, right)
    assert total_dist == 30, total_dist

    print("processing input")
    with open("input.txt") as file:
        left = file.readline().strip().split(',')
        right = file.readline().strip().split(',')
    assert left != right
    dist = find_intersection(left, right)
    print(dist)

    total_dist = find_min_steps(left, right)
    print(total_dist)
