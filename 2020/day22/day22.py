from collections import deque


def parse_decks(lines: list[str]) -> tuple[deque[int], deque[int]]:
    left, right = deque[int](), deque[int]()
    queue = left
    for line in lines:
        line = line.strip()
        if not line:
            queue = right
        elif not all(d.isdigit() for d in line):
            continue
        else:
            number = int(line)
            queue.append(number)
    return left, right


def take_round(left: deque[int], right: deque[int]) -> tuple[deque[int], deque[int]]:
    lcard = left.popleft()
    rcard = right.popleft()
    if lcard > rcard:
        left.append(lcard)
        left.append(rcard)
    elif rcard > lcard:
        right.append(rcard)
        right.append(lcard)
    else:
        raise ValueError("Cards should be unique!")
    return left, right


def run_game(left: deque[int], right: deque[int]) -> deque[int]:
    while left and right:
        left, right = take_round(left, right)
    if left:
        return left
    return right


def count_score(deck: deque[int]) -> int:
    return sum(value * card for value, card in enumerate(reversed(deck), start=1))


def run_recur_game(left: deque[int], right: deque[int]) -> tuple[bool, deque[int]]:
    seen_before: set[tuple[tuple[int, ...], tuple[int, ...]]] =  set()
    pair = tuple([tuple(left), tuple(right)]) 
    seen_before.add(pair)
    while left and right:
        lcard = left.popleft()
        rcard = right.popleft()
        if lcard <= len(left) and rcard <= len(right):
            winner, _ = run_recur_game(
                deque(list(left)[:lcard]),
                deque(list(right)[:rcard])
            )
            if winner:
                left.append(lcard)
                left.append(rcard)
            else:
                right.append(rcard)
                right.append(lcard)
        elif lcard > rcard:
            left.append(lcard)
            left.append(rcard)
        elif rcard > lcard:
            right.append(rcard)
            right.append(lcard)
        else:
            raise ValueError("Cards should be unique!")
        pair = tuple([tuple(left), tuple(right)])
        if pair in seen_before:
            return True, left
        else:
            seen_before.add(pair)

    if left:
        return True, left
    return False, right


if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    left, right = parse_decks(lines)
    deck = run_game(left.copy(), right.copy())
    score = count_score(deck)
    assert score == 306

    winner, deck = run_recur_game(left.copy(), right.copy())
    score = count_score(deck)
    assert score == 291

    with open("input.txt") as file:
        lines = file.readlines()
    left, right = parse_decks(lines)
    deck = run_game(left.copy(), right.copy())
    score = count_score(deck)
    print(score)

    winner, deck = run_recur_game(left.copy(), right.copy())
    score = count_score(deck)
    print(winner, score)
