from typing import Optional
from math import prod, floor


def parse_and_index_buses(line: str) -> list[tuple[int, int]]:
    return [(idx, int(num)) for idx, num in enumerate(line.split(",")) if num != "x"]


def only_buses(buses: list[tuple[int, int]]) -> list[int]:
    return [num for _, num in buses]


def find_earliest_bus_and_time(earliest_departure: int, buses: list[int]) -> Optional[tuple[int, int]]:
    earliest: Optional[int] = None
    min_bus: Optional[int] = None
    for bus in buses:
        n = floor(earliest_departure / bus)
        time_to_wait = (n + 1) * bus - earliest_departure
        if earliest is None or earliest > time_to_wait:
            earliest = time_to_wait
            min_bus = bus
    if earliest is not None and min_bus is not None:
        return (min_bus, earliest)


def find_earliest_timestamp(indexed_buses: list[tuple[int, int]]) -> int:
    rev_buses = indexed_buses[::-1]
    _, first_bus = rev_buses.pop()
    buses = rev_buses[:]
    factor = 1
    prev_idx = 0
    timestamp = first_bus
    while buses:
        idx, bus = buses.pop()
        timestamp += idx - prev_idx
        if timestamp % bus != 0:
            buses = rev_buses[:]
            factor += 1
            timestamp = factor * first_bus
            prev_idx = 0
        else:
            prev_idx = idx
    return timestamp - prev_idx 


def find_earliest_timestamp_better(indexed_buses: list[tuple[int, int]]) -> int:
    _, first_bus = indexed_buses[0]
    factor = 1
    while not all((factor * first_bus + index) % bus == 0 for index, bus in indexed_buses[1:]):
        factor += 1 # need to find a better lower boundary based on the first number that does not work
    return factor * first_bus


def find_earliest_timestamp_best(indexed_buses: list[tuple[int, int]]) -> int:
    prev: list[int] = []
    def solve(timestamp: int, idx: int, bus: int): 
        rem = (timestamp + idx) % bus
        while rem != 0:
            timestamp += prod(prev)
            rem = (timestamp + idx) % bus
        return timestamp
    
    timestamp = 1
    for idx, bus in indexed_buses:
        timestamp = solve(timestamp, idx, bus)
        prev.append(bus)
    return timestamp


if __name__ == "__main__":
    with open("sample.txt") as file:
        earliest_departure_time = int(file.readline().strip())
        indexed_buses = parse_and_index_buses(file.readline().strip())
        buses = only_buses(indexed_buses)

    earliest = find_earliest_bus_and_time(earliest_departure_time, buses)
    if earliest is not None:
        bus, time = earliest
        assert bus * time == 295
    else:
        raise ValueError(f"Buses list was empty.")
    timestamp = find_earliest_timestamp(indexed_buses)
    assert timestamp == 1068781, timestamp
    timestamp = find_earliest_timestamp_better(indexed_buses)
    assert timestamp == 1068781, timestamp
    timestamp = find_earliest_timestamp_best(indexed_buses)
    assert timestamp == 1068781, timestamp

    with open("input.txt") as file:
        earliest_departure_time = int(file.readline().strip())
        indexed_buses = parse_and_index_buses(file.readline().strip())
        buses = only_buses(indexed_buses)

    earliest = find_earliest_bus_and_time(earliest_departure_time, buses)
    if earliest is not None:
        bus, time = earliest
        print(bus * time)
    else:
        raise ValueError(f"Buses list was empty.")
    timestamp = find_earliest_timestamp_best(indexed_buses)
    print(timestamp)
