from itertools import cycle, takewhile, islice


def find_destination(start: int, min_: int, max_: int, picked_up: list[int]) -> int:
    start -= 1
    if start < min_:
        start = max_
    while start in picked_up:
        start -= 1
        if start < min_:
            start = max_
    return start

def run(cups: list[int], rounds:int) -> list[int]:
    cups = cups[:]
    min_ = min(cups)
    max_ = max(cups)
    for _ in range(rounds):
        circle = cycle(cups)
        start = next(circle)
        leftover = [start] 
        picked_up = list(islice(circle, 3))
        leftover += list(takewhile(lambda x: x != start, circle))
        destination_cup = find_destination(start, min_, max_, picked_up)
        itr = iter(leftover)
        cups = list(takewhile(lambda x: x != destination_cup, itr)) + [destination_cup] + picked_up + list(itr)
        cups = cups[1:] + [cups[0]]
    return cups


def run_faster(cups: list[int], rounds: int) -> list[int]:
    cups = cups[:]
    min_ = min(cups)
    max_ = max(cups)
    for _ in range(rounds):
        start = cups[0]
        picked_up = [cups.pop(1) for _ in range(3)]
        destination_cup = find_destination(start, min_, max_, picked_up)
        idx = cups.index(destination_cup)
        for di, value in enumerate(picked_up, start = 1):
            cups.insert(idx + di, value)
        cups.pop(0)
        cups.append(start)
    return cups


def run_even_faster(cups: list[int], rounds: int) -> list[int]:
    start = cups[0]
    prevs = [cups[-1]] + cups[:-1]
    places = {value: (prev, next_) for prev, value, next_ in zip(prevs, cups[:-1], cups[1:])}
    places[cups[-1]] = (cups[-2], start)
    min_ = min(cups)
    max_ = max(cups)
    for _ in range(rounds):
        picked_up: list[int] = []
        to_start = start
        for _ in range(3):
            _, next_ = places[to_start]
            picked_up.append(next_)
            to_start = next_
        _, to_start = places[to_start]
        prev, _ = places[start]
        places[start] = (prev, to_start)
        _, next_ = places[to_start]
        places[to_start] = (start, next_)
        destination_cup = find_destination(start, min_, max_, picked_up)
        prev, next_ = places[destination_cup]
        places[destination_cup] = (prev, picked_up[0])
        places[picked_up[0]] = (destination_cup, picked_up[1])
        places[picked_up[2]] = (picked_up[1], next_)
        _, next_next = places[next_]
        places[next_] = (picked_up[2], next_next)
        start = to_start
    new_cups: list[int] = []
    for _ in range(len(places)):
        new_cups.append(start)
        _, start = places[start]
    return new_cups

def order(cups: list[int]) -> list[int]:
    circle = cycle(cups)
    list(takewhile(lambda x: x != 1, circle))
    return list(takewhile(lambda x: x != 1, circle))


if __name__ == "__main__":
    cups = [int(i) for i in "389125467"]
    shifted = run_even_faster(cups, 10)
    ordered = order(shifted)
    assert ordered == [int(i) for i in "92658374"], ordered
    shifted = run_even_faster(cups, 100)
    ordered = order(shifted)
    assert ordered == [int(i) for i in "67384529"]
    print("tests okay")

    cups = [int(i) for i in "389125467"] 
    cups.extend(range(10, 1_000_001))
    shifted = run_even_faster(cups, 10_000_000)
    idx = shifted.index(1)
    result = shifted[idx + 1] * shifted[idx + 2] 
    assert result == 149245887792, result

    cups = [int(i) for i in "583976241"]
    shifted = run_faster(cups, 100)
    ordered = order(shifted)
    print(''.join(str(i) for i in ordered))

    cups = [int(i) for i in "583976241"] 
    cups.extend(range(10, 1_000_001))
    shifted = run_even_faster(cups, 10_000_000)
    idx = shifted.index(1)
    result = shifted[idx + 1] * shifted[idx + 2] 
    print(result)

