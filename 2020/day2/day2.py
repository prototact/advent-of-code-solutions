from typing import Optional
import re


Rule = tuple[int, int, str, str]


PASSWORD = re.compile(r"^(\d+)\-(\d+) (\w): (\w+)$")


def parse_rule_and_password(line: str) -> Optional[Rule]:
    m = PASSWORD.match(line)
    if m is not None:
        lows, highs, letter, password = m.groups()
        low = int(lows)
        high = int(highs)
        return (low, high, letter, password)
    

def is_valid(rule: Rule) -> bool:
    low, high, letter, password = rule
    cnt = password.count(letter)
    return cnt in range(low, high + 1)


def is_valid2(rule: Rule) -> bool:
    first, second, letter, password = rule
    left = password[first - 1]
    right = password[second - 1]
    return (left == letter) ^ (right == letter)


if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        rules = [parse_rule_and_password(line) for line in file.readlines()]
        assert all(rule is not None for rule in rules)
        total = sum(1 for rule in rules if rule is not None and is_valid(rule))
        assert total == 2
        total = sum(1 for rule in rules if rule is not None and is_valid2(rule))
        assert total == 1

    with open("input.txt", "r") as file:
        rules = [parse_rule_and_password(line) for line in file.readlines()]
        assert all(rule is not None for rule in rules)
        total = sum(1 for rule in rules if rule is not None and is_valid(rule))
        print(total)
        total = sum(1 for rule in rules if rule is not None and is_valid2(rule))
        print(total)
