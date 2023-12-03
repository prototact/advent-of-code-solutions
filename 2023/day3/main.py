from collections.abc import Iterator, Callable
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

    def _get_surrounding_numbers(self, idx: int, jdx: int, visited: set[tuple[int, int]]) -> Iterator[int]:
        """Generates the number surrounding the symbol at Coords (idx, jdx). 
        Coords should point to a symbol, not a number or an empty space.

        Side effect:
        Registers the coordinates to the visited ones. This is so that the same number is not returned twice.
        Check the lifetime of the visisted set in your code for correctness.
        """
        for step in DIRECTIONS:  
            dx, dy = step 
            coords = (idx + dx, jdx + dy)
            try:
                char = self[coords]
            except IndexError:
                continue
            if char.isdigit() and coords not in visited:
                number = self._expand_left_and_right(coords, visited)
                yield number
                visited.add(coords)

    def _expand_left_and_right(self, coords: tuple[int, int], visited: set[tuple[int, int]]) -> int:
        """Returns the whole number, starting from a single digit at the coords.

        Side Effect:
        Registers the coords of each digit in the number as visisted, so the number is not returned twice.
        """
        idx, jdx = coords
        total = self[idx, jdx]
        def expand(total: str, dir_: Iterator[int], combine: Callable[[str, str], str]):
            for step in dir_:
                try:
                    char = self[idx, jdx + step]
                except IndexError:
                    break
                if char.isdigit():
                    total = combine(char, total)
                    visited.add((idx, jdx + step))
                else:
                    break
            return total
        total = expand(total, count(-1, -1), lambda x, y: x + y)
        total = expand(total, count(1, 1), lambda x, y: y + x)
        return int(total)


    def scan(self) -> list[int]:
        visited: set[tuple[int, int]] = set()
        return list(
            chain.from_iterable(
                self._get_surrounding_numbers(idx, jdx, visited)
                for idx, row in enumerate(self)
                for jdx, char in enumerate(row)
                if char != '.' and not char.isdigit()
            )
        ) 
 
    @staticmethod
    def _take_product(numbers: list[int]) -> int:
        if len(numbers) < 2:
            return 0
        return prod(numbers)

    def scan_for_gears(self) -> list[int]:
        visited: set[tuple[int, int]] = set()
        return [
            self._take_product(list(self._get_surrounding_numbers(idx, jdx, visited)))
            for idx, row in enumerate(image)
            for jdx, char in enumerate(row)
            if char == '*'
        ]


if __name__ == "__main__":
    with open("sample.txt") as file:
        image = Image([line.strip() for line in file.readlines()])
    numbers = image.scan()
    assert (result := sum(numbers)) == 4361, result
    
    gear_ratios = image.scan_for_gears()
    assert sum(gear_ratios) == 467835

    with open("input.txt") as file:
        image = Image([line.strip() for line in file.readlines()])
    numbers = image.scan()
    print(sum(numbers))

    gear_ratios = image.scan_for_gears()
    print(sum(gear_ratios))
