from typing import Optional
from collections.abc import Iterable
import re


Bag = str
Rules = dict[Bag, Optional[list[tuple[int, Bag]]]]


RULE = re.compile(r"^(\w+ \w+ \w+) contain((?: \d+ \w+ \w+ \w+\,*){1,}).$")
LEAF = re.compile(r"(\w+ \w+ \w+) contain no other bag.")


def parse_rules(text: Iterable[str]) -> Rules:
    rules: dict[Bag, Optional[list[tuple[int, Bag]]]] = {}
    for line in text:
        line = line.strip()
        m = RULE.match(line)
        if m is not None:
            container, bags = m.groups()
            cleaned: list[tuple[int, Bag]] = []
            items = bags.strip().split(",")
            for item in items:
                item = item.strip()
                count = int(item[0])
                name = item[1:].strip()
                if count == 1:
                    name += "s"
                cleaned.append((count, name))
            rules[container] = cleaned
        else:
            m2 = LEAF.match(line)
            if m2 is not None:
                container = m2.groups()[0]
                rules[container] = None
    return rules


def count_contained(bag: Bag, rules: Rules) -> int:
    stack: list[Bag] = [bag]
    found: set[Bag] = set()
    while stack:
        bag = stack.pop()
        for container, contained in rules.items():
            if contained is not None:
                for _, name in contained:
                    if bag == name:
                        stack.append(container)
                        found.add(container)
    return len(found)


def count_inside(bag: Bag, rules: Rules, root: bool) -> int:
    contained = rules[bag]
    if contained is not None:
        if not root:
            return 1 + sum(size * count_inside(other, rules, False) for size, other in contained)
        else:
            return sum(size * count_inside(other, rules, False) for size, other in contained)
    return 1


if __name__ == "__main__":
    with open("sample.txt", "r") as file:
        rules = parse_rules(file.readlines())
    assert (result := count_contained("shiny gold bags", rules)) == 4, result
    assert (result := count_inside("shiny gold bags", rules, True)) == 32, result

    with open("input.txt", "r") as file:
        rules = parse_rules(file.readlines())
    print(count_contained("shiny gold bags", rules))
    print(count_inside("shiny gold bags", rules, True))
