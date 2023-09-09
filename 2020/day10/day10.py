from typing import Union
from operator import ge, le

CompTree = dict[int, Union["CompTree", int]]


def diffs(values: list[int]) -> int:
    all_diffs:list[int] = []
    for elem1, elem2 in zip(values[:-1], values[1:]):
        diff = elem2 - elem1
        all_diffs.append(diff)
    all_diffs.append(3)
    ones = all_diffs.count(1)
    threes = all_diffs.count(3)
    return ones * threes


def find_compatible(value: int, values: list[int]) -> list[int]:
    return [v for v in values if 1 <= value - v <= 3]


def find_orders(values: list[int], lowest: int) -> int:
    highest = values[-1]
    def go(high: int, rest: list[int]) -> int:
        if high == lowest:
            return 1
        if not rest:
            return 0
        compatible = find_compatible(high, rest)
        total = 0
        for comp in compatible:
            copy = rest[:]
            copy.remove(comp)
            total += go(comp, copy)
        return total
    return go(highest, values[:-1])


def create_compatible_map(values: list[int]) -> dict[int, list[int]]:
    compatible: dict[int, list[int]] = {}
    for value in values:
        compatible[value] = find_compatible(value, values)
    return compatible


def update_compatible(compatible: dict[int, list[int]], value: int) -> dict[int, list[int]]:
    copy = {key: values[:] for key, values in compatible.items()}
    for val in range(value - 3, value):
        if val in copy:
            if value in copy[val]:
               copy[val].remove(value)
    return copy


def enumerate_orderings(values: list[int])  -> int:
    highest = values[-1]
    def go(compatible: dict[int, list[int]], previous: int) -> int:
        if previous == 0:
            return 1
        comps = compatible[previous]
        return sum(go(update_compatible(compatible, comp), comp) for comp in comps)
    comps = create_compatible_map(values)
    return go(comps, highest)


def count_orderings(values: list[int]) -> int:
    """Counts the number of ways values can be chosen according to the rules.
    Values is always ordered in ascending order.
    """
    highest = values[-1]
    orderings: list[tuple[list[int], list[int]]] = [([highest], values[:-1][::-1])]
    count = 0
    while orderings:
        ordering, remaining = orderings.pop()
        if ordering[-1] == 0:
            count += 1
            continue
        for value in remaining:
            if value >= ordering[-1] - 3:
                copy = ordering[:]
                copy.append(value)
                rem = [elem for elem in remaining if value > elem]
                orderings.append((copy, rem))
            else:
                break
    return count


def is_sorted(elems: list[int], descending: bool=True) -> bool:
    """Not strict comparison, if two subsequent elements are equal, than it is still sorted.
    """
    comparison = ge if descending else le
    return all(comparison(left, right) for left, right in zip(elems[:-1], elems[1:]))


def count_orderings_memo(values: list[int]) -> int:
    """Counts the number of ways values can be chosen according to the rules.
    Values is always ordered in ascending order. The input to solve should
    be in descending order.
    This depends on each path being chosen only once, so that the key is unique.
    These details are part of the algorithm.
    """
    if not is_sorted(values, descending=False):
        raise ValueError("List of values is not sorted in ascending order.")

    memo: dict[tuple[int, ...], int] = {(0,): 1}
    def solve(values: list[int]) -> int:
        key = tuple(values)
        if key in memo:
            return memo[key]
        highest = values[0]
        rest = values[1:]
        count_ = 0
        # pick any of the viable choices, 
        # rest is always in descending order
        for idx, _ in enumerate(elem for elem in rest if elem >= highest - 3):
            remaining = rest[idx:]
            if remaining:
                count_ += solve(remaining)
        memo[key] = count_
        return count_
    return solve(values[::-1])


if __name__ == "__main__":
    with open("small.txt", "r") as file:
        joltages = [int(line.strip()) for line in file.readlines()]
    sorted_ = sorted([0] + joltages)
    
    assert (result := diffs(sorted_)) == 35, result
    assert (result := count_orderings_memo(sorted_)) == 8, result

    with open("sample.txt", "r") as file:
        joltages = [int(line.strip()) for line in file.readlines()]
    sorted_ = sorted([0] + joltages)
    
    assert (result := diffs(sorted_)) == 220, result
    assert (result := count_orderings_memo(sorted_)) == 19208, result

    with open("input.txt", "r") as file:
        joltages = [int(line.strip()) for line in file.readlines()]
    sorted_ = sorted([0] + joltages)
    assert len(sorted_) == len(set(sorted_))

    print(diffs(sorted_))
    print(count_orderings_memo(sorted_))
