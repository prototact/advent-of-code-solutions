from collections.abc import Sequence


def check_sum(left: int, right: int, sum_: int) -> bool:
    return left + right  == sum_


def find_sum(seq: Sequence[int], sum_: int) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for idx, elem in enumerate(seq):
        if elem > sum_:
            continue
        for elem_ in seq[idx + 1:]:
            if check_sum(elem, elem_, sum_):
                pairs.append((elem, elem_))
    return pairs

def find_sum3(seq: Sequence[int], sum_: int) -> list[tuple[int, int, int]]:
    triplets: list[tuple[int, int, int]] = []
    for idx, elem in enumerate(seq):
        if elem > sum_:
            continue
        for jdx, elem_ in enumerate(seq[idx + 1:], start=idx + 1):
            if elem + elem_ > sum_:
                continue
            for elem__ in seq[jdx + 1:]:
                if elem + elem_ + elem__ == sum_:
                    triplets.append((elem, elem_, elem__))
    return triplets

if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        elems = [int(elem) for elem in file.readlines()]
    pairs = find_sum(elems, 2020)
    assert len(pairs) == 1
    assert pairs[0][0] * pairs[0][1] == 514579
    triplets = find_sum3(elems, 2020)
    assert len(triplets) == 1
    assert triplets[0][0] * triplets[0][1] * triplets[0][2] == 241861950

    with open("input.txt", "r") as file:
        elems = [int(elem) for elem in file.readlines()]
    pairs = find_sum(elems, 2020)
    assert len(pairs) == 1
    print(pairs[0][0] * pairs[0][1])
    triplets = find_sum3(elems, 2020)
    assert len(triplets) == 1
    print(triplets[0][0] * triplets[0][1] * triplets[0][2])
  