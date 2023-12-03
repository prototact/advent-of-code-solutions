from collections.abc import Generator, Iterator
from itertools import count, chain
from dataclasses import dataclass
from math import prod


DIRECTIONS = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]


@dataclass(frozen=True)
class Image:
    _grid: list[str]

    def __getitem__(self, pair: tuple[int, int]) -> str:
        idx, jdx = pair
        if idx < 0 or jdx < 0:
            raise IndexError(f"Index out of bounds row: {idx}, col: {jdx}")
        try:
            char = self._grid[idx][jdx]
        except IndexError:
            raise IndexError(f"Index out of bounds row: {idx}, col: {jdx}")
        return char

    def __iter__(self) -> Iterator[str]:
        yield from self._grid


def get_surrounding_numbers(idx: int, jdx: int, image: Image, visited: set[tuple[int, int]]) -> Generator[tuple[int, int], None, None]:
    for step in DIRECTIONS:  
        dx, dy = step 
        try:
            char = image[idx + dx, jdx + dy]
        except IndexError:
            continue
        if char.isdigit() and (idx + dx, jdx + dy) not in visited:
            yield (idx + dx, jdx + dy)
            visited.add((idx + dx, jdx + dy))


def expand_left_and_right(coords: tuple[int, int], image: Image, visited: set[tuple[int, int]]) -> int:
    idx, jdx = coords
    total = image[idx, jdx]
    for left in count(-1, -1):
        try:
            char = image[idx, jdx + left]
        except IndexError:
            break
        if char.isdigit():
            total = char + total
            visited.add((idx, jdx + left))
        else:
            break
    for right in count(1, 1):
        try:
            char = image[idx, jdx + right]
        except IndexError:
            break
        if char.isdigit():
            total = total + char
            visited.add((idx, jdx + right))
        else:
            break
    return int(total)


def scan_image(image: Image) -> list[int]:
    visited: set[tuple[int, int]] = set()
    return list(
        chain.from_iterable(
            (   
                expand_left_and_right(coords, image, visited)
                for coords in get_surrounding_numbers(idx, jdx, image, visited)
                if coords not in visited
            )
            for idx, row in enumerate(image)
            for jdx, char in enumerate(row)
            if char != '.' and not char.isdigit()
        )
    )


def take_product(numbers: list[int]) -> int:
    if len(numbers) < 2:
        return 0
    return prod(numbers)


def scan_image_for_gears(image: Image) -> list[int]:
    visited: set[tuple[int, int]] = set()
    return list(
        take_product([expand_left_and_right(coords, image, visited)
             for coords in get_surrounding_numbers(idx, jdx, image, visited)
             if coords not in visited])
        for idx, row in enumerate(image)
        for jdx, char in enumerate(row)
        if char == '*'
    )


if __name__ == "__main__":
    with open("sample.txt") as file:
        image = Image([line.strip() for line in file.readlines()])
    numbers = scan_image(image)
    assert (result := sum(numbers)) == 4361, result
    
    gear_ratios = scan_image_for_gears(image)
    assert sum(gear_ratios) == 467835

    with open("input.txt") as file:
        image = Image([line.strip() for line in file.readlines()])
    numbers = scan_image(image)
    print(sum(numbers))

    gear_ratios = scan_image_for_gears(image)
    print(sum(gear_ratios))
