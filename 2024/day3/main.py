import re
from collections.abc import Callable


MULTIPLY = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
MUL_DO_DONT = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\)")
OPERATION = tuple[int, int]


def find_all(text: str) -> list[OPERATION]:
    return [(int(x), int(y)) for x, y in MULTIPLY.findall(text)]


def find_and_filter(text: str) -> list[OPERATION]:
    matches: list[OPERATION] = []
    def find(text:str, active: bool, matches: list[OPERATION]) -> list[OPERATION]:
        if text:
            m = MUL_DO_DONT.search(text)
            if m is None:
                return matches
            pos = m.end()
            if m.group(0) == "do()":
                return find(text[pos:], True, matches)
            elif m.group(0) == "don't()":
                return find(text[pos:], False, matches)
            if active:
                x, y = map(int, m.group(1, 2))
                matches.append((x, y))
            return find(text[pos:], active, matches)
        return matches
    return find(text, True, matches)


def read_text(filename: str) -> str:
    with open(filename) as file:
        text = ''.join(file.readlines())
    return text


def compute_and_add(operations: list[OPERATION]) -> int:
    return sum(x * y for x, y in operations)


if __name__ == "__main__":
    text = read_text("sample.txt")
    operations = find_all(text)
    print(compute_and_add(operations))

    text = read_text("sample2.txt")
    operations = find_and_filter(text)
    print(compute_and_add(operations))

    text = read_text("input.txt")
    operations = find_all(text)
    print(compute_and_add(operations))

    operations = find_and_filter(text)
    print(compute_and_add(operations))