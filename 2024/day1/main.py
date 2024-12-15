from collections import Counter


def distance(left: list[int], right: list[int]) -> int:
    return sum(abs(litem - ritem) for litem, ritem in zip(sorted(left), sorted(right)))


def similarity(left: list[int], right: list[int]) -> int:
    counter = Counter(right)
    return sum(item * counter.get(item, 0) for item in left)


def read_lists(filename: str) -> tuple[list[int], list[int]]:
    with open(filename) as data:
        left: list[int] = []
        right: list[int] = []
        for litem, ritem in map(lambda x: map(int, x.strip().split()), data.readlines()):
            left.append(litem)
            right.append(ritem)
    return left, right


if __name__ == "__main__":
    left, right = read_lists("input.txt")
    print(distance(left, right))
    print(similarity(left, right))