from itertools import islice


def predict(history: list[int]) -> int:
    current = history
    last = current[-1]
    while any(number != 0 for number in current):
        current = [
            next_ - elem
            for elem, next_ in zip(
                islice(current, len(current) - 1), islice(current, 1, None)
            )
        ]
        last += current[-1]

    return last


def predict_backwards(history: list[int]) -> int:
    current = history[:]
    starts: list[int] = [current[0]]
    while any(number != 0 for number in current):
        current = [
            next_ - elem
            for elem, next_ in zip(
                islice(current, len(current) - 1), islice(current, 1, None)
            )
        ]
        starts.append(current[0])

    prev = 0
    while starts:
        start = starts.pop()
        prev = -prev + start
    return prev


def predict_all(histories: list[list[int]]) -> list[int]:
    return [predict(history) for history in histories]


def predict_backwards_all(histories: list[list[int]]) -> list[int]:
    return [predict_backwards(history) for history in histories]


def parse_histories(lines: list[str]) -> list[list[int]]:
    return [[int(number) for number in line.strip().split()] for line in lines]


if __name__ == "__main__":
    with open("sample.txt") as file:
        histories = parse_histories(file.readlines())
    predictions = predict_all(histories)
    total = sum(predictions)
    assert total == 114, total

    predictions = predict_backwards_all(histories)
    total = sum(predictions)
    assert total == 2, total

    with open("input.txt") as file:
        histories = parse_histories(file.readlines())
    predictions = predict_all(histories)
    total = sum(predictions)
    print(total)

    predictions = predict_backwards_all(histories)
    total = sum(predictions)
    print(total)
