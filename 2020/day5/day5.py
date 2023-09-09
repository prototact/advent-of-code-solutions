

ROWS = range(128)
COLUMNS = range(8)


def find_seat(code:str) -> tuple[int, int]:
    rows = code[:7]
    cols = code[7:]
    row = ROWS
    for step in rows:
        if step == "F":
            row = bisect(True, row)
        else:
            row = bisect(False, row)

    col = COLUMNS
    for step in cols:
        if step == "L":
            col = bisect(True, col)
        else:
            col = bisect(False, col)
    return row[0], col[0]


def bisect(front:bool, row: range) -> range:
    size = len(row)
    if size == 1:
        return row
    if front:
        return row[:size // 2]
    return row[size // 2:]


def get_id(row: int, column: int) -> int:
    return row * 8 + column


def find_missing(ids: list[int]) -> int:
    first, last = min(ids), max(ids)
    contiguous = range(first, last + 1)
    return set(contiguous).difference(set(ids)).pop()

if __name__ == "__main__":
    with open("sample.txt") as file:
        seats: list[tuple[int, int]] = []
        for line in file.readlines():
            seat = find_seat(line.strip())
            seats.append(seat)
    assert [get_id(*seat) for seat in seats] == [567, 119, 820]

    with open("input.txt") as file:
        seats: list[tuple[int, int]] = []
        for line in file.readlines():
            seat = find_seat(line.strip())
            seats.append(seat)
    print(max(get_id(*seat) for seat in seats))
    print(find_missing([get_id(*seat) for seat in seats]))
