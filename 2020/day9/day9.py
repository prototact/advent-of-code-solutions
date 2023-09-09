from typing import Optional
from collections.abc import Iterator
from itertools import chain


def get_first_n(n: int, numbers: Iterator[int]) -> list[int]:
    return [number for _, number in zip(range(n), numbers)]


def check_numbers(first: list[int], numbers: Iterator[int]) -> Optional[tuple[int, list[int]]]:
    for number in numbers:
        if check_is_sum(first, number):
            first = first[1:]
            first.append(number)
        else:
            return number, first 


def check_is_sum(first: list[int], number: int) -> bool:
    for idx, num1 in enumerate(first):
        for num2 in chain(first[:idx], first[idx + 1:]):
            if num1 == num2:
                continue
            elif num1 + num2 == number:
                return True
    return False


def find_range(number:int, history: list[int]) -> Optional[list[int]]:
    for idx1, _ in enumerate(history):
        for idx2, _ in enumerate(history[idx1 + 1:]):
            total = sum(history[idx1:idx2 + 1])   
            if total == number:
                return history[idx1:idx2 + 1]


if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        history = [int(line.strip()) for line in file.readlines()]
    numbers = iter(history)
    first = get_first_n(5, numbers)
    result = check_numbers(first, numbers)
    assert result is not None and result[0] == 127, result
    number = result[0]
    rng = find_range(number, history)
    assert rng is not None and min(rng) + max(rng) == 62

    with open("input.txt", "r") as file:
        history = [int(line.strip()) for line in file.readlines()]
    numbers = iter(history)
    first = get_first_n(25, numbers)
    result = check_numbers(first, numbers)
    if result is not None: 
        print(result[0])
        number = result[0]
        rng = find_range(number, history)
        if rng is not None:
            print(min(rng) + max(rng))
