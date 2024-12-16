from dataclasses import dataclass


@dataclass
class Number:
    x: int
    rules: set[tuple[int, int]]

    def __lt__(self, other: "Number") -> bool:
        return (self.x, other.x) in self.rules
    
    def __eq__(self, other: "Number") -> bool:
        return self.x == other.x


def validate_update(update: list[int], rules: set[tuple[int, int]]):
    return all((elem, other) in rules for idx, elem in enumerate(update) for other in update[idx + 1:]) 


def sum_valid_updates(updates: list[list[int]], rules: set[tuple[int, int]]) -> int:
    return sum(update[len(update) // 2] for update in updates if validate_update(update, rules))

# NOTE: it is not obvious the rules work with the sorted algorithm but it does work
def correct_update(update: list[int], rules: set[tuple[int, int]]) -> list[int]:
    return sorted(update, key=lambda x: Number(x, rules))


def sum_invalid_updates(updates: list[list[int]], rules: set[tuple[int, int]]) -> int:
    invalid = (update for update in updates if not validate_update(update, rules))
    return sum(update[len(update) // 2] for update in map(lambda x: correct_update(x, rules), invalid)) 


def parse_updates(filename: str) -> tuple[set[tuple[int, int]], list[list[int]]]:
    rules: set[tuple[int, int]] = set()
    with open(filename) as file:
        line = file.readline().strip()
        while line:
           earlier, later = map(int, line.split('|'))
           rules.add((earlier, later))
           line = file.readline().strip()
        
        line = file.readline().strip()
        updates: list[list[int]] = []
        while line:
            update = [int(number) for number in line.split(',')]
            updates.append(update)
            line = file.readline().strip()
    return rules, updates


if __name__ == "__main__":
    rules, updates = parse_updates("sample.txt")
    print(sum_valid_updates(updates, rules))
    print(sum_invalid_updates(updates, rules))

    rules, updates = parse_updates("input.txt")
    print(sum_valid_updates(updates, rules))
    print(sum_invalid_updates(updates, rules))
