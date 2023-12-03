from typing import Optional


DIGITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}


def find_first_left_and_right(line: str) -> Optional[int]:
    left: Optional[str] = None
    for char in line:
        if char.isdigit():
            left = char
            break
    right: Optional[str] = None
    for char in reversed(line):
        if char.isdigit():
            right = char
            break
    if left is not None and right is not None:
        pair = int(left + right)
        return pair


def find_first_occurence(line: str, reversed: bool = False) -> Optional[tuple[str, bool]]:
    found: Optional[str] = None
    found_index: Optional[int] = None
    for idx, char in enumerate(line):
        if char.isdigit():
            found = char
            found_index = idx
            break

    found_literal : Optional[str] = None
    found_literal_index: Optional[int] = None
    for digit in DIGITS:
        index = line.find(digit if not reversed else digit[::-1])
        if index != -1:
            if found_literal_index is None:
                found_literal_index = index
                found_literal = digit
            elif found_literal_index > index:
                found_literal_index = index
                found_literal = digit

    if found_index is not None and found_literal_index is not None:
        if found_index < found_literal_index:
            return (found, False) if found is not None else None
        return (found_literal, True) if found_literal is not None else None
    elif found_index is not None:
        return (found, False) if found is not None else None
    return (found_literal, True) if found_literal is not None else None


def find_literal_left_and_right(line: str) -> Optional[int]:
    left = find_first_occurence(line)
    right = find_first_occurence(line[::-1], reversed=True)
    if left is not None and right is not None:
        left, is_literal_left = left
        right, is_literal_right = right
        if is_literal_left and is_literal_right:
            return DIGITS[left] * 10 + DIGITS[right]
        elif is_literal_left:
            return DIGITS[left] * 10 + int(right)
        elif is_literal_right:
            return int(left) * 10 + DIGITS[right]
        return int(left + right)


def find_pairs(lines: list[str], literal: bool = False) -> list[int]:
    pairs: list[int] = []
    for line in lines:
        if not literal:
            pair = find_first_left_and_right(line.strip())
        else:
            pair = find_literal_left_and_right(line.strip())
        if pair is not None:
            pairs.append(pair)
    return pairs


if __name__ == "__main__":
    with open("input.txt") as file:
        lines = file.readlines()
    pairs = find_pairs(lines)
    print(sum(pairs))

    actual_pairs = find_pairs(lines, literal=True)
    print(sum(actual_pairs))
