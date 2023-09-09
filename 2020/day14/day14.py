from enum import Enum
import re


class Action(Enum):
    Mask = 0
    Store = 1


MASK = re.compile(r"mask = ((?:X|0|1)+)")
STORE = re.compile(r"mem\[(\d+)\] = (\d+)")


def parse_actions(lines: list[str]) -> list[tuple[Action, tuple[int, int] | list[tuple[int, int]]]]:
    actions: list[tuple[Action, tuple[int, int] | list[tuple[int, int]]]] = []
    for line in lines:
        line = line.strip()
        match = STORE.match(line)
        if match is not None:
            loc, number = match.groups()
            actions.append((Action.Store, (int(loc), int(number))))
        match = MASK.match(line)
        if match is not None:
            mask = match.groups()[0]
            actions.append((Action.Mask, [(idx, int(char)) for idx, char in enumerate(mask[::-1]) if char != "X"]))
        
    return actions


def masked(mask: list[tuple[int, int]], number: int) -> int:
    for power, digit in mask:
        if digit == 0:
            number = (((1 << 37) - 1) ^ (1 << power)) & number
        else:
            number = (1 << power) | number
    return number

def do_actions(mem: dict[int, int], actions: list[tuple[Action, tuple[int, int] | list[tuple[int, int]]]]) -> None:
    mask: list[tuple[int, int]] = []
    for type_, action in actions:
        if type_ == Action.Mask:
            mask = action
        elif type_ == Action.Store:
            loc, number = action
            mem[loc] = masked(mask, number)

# memory space increases exponentially, if i could determine the sum as it
# happens, i only need to decrease/increase the size by the difference times the amount of memory.
# i need to compute differences as well. but these change according to the digits. crap.
def masked_mem(mask: list[tuple[int, int]], number: int) -> list[int]:
    numbers = [number]
    shifts = {key: value for key, value in mask}
    for idx in range(36):
        if idx in shifts:
            digit = shifts[idx]
            if digit == 1:
                for idx2 in range(len(numbers)):
                    numbers[idx2] = (1 << idx) | numbers[idx2]
        else:
            new_nums: list[int] = []
            for num in numbers:
                new_num = (1 << idx) | num
                new_nums.append(new_num)
            numbers.extend(new_nums)
    return numbers


def do_actions_mem(mem: dict[int, int], actions: list[tuple[Action, tuple[int, int] | list[tuple[int, int]]]]) -> None:
    mask: list[tuple[int, int]] = []
    for type_, action in actions:
        if type_ == Action.Mask:
            mask = action
        elif type_ == Action.Store:
            loc, number = action
            for subloc in masked_mem(mask, loc):
                mem[subloc] = number


if __name__ == "__main__":
    with open("sample.txt") as file:
        actions = parse_actions(file.readlines())

    mem: dict[int, int] = {}
    do_actions(mem, actions)
    assert sum(mem.values()) == 165

    mem: dict[int, int] = {}
    do_actions_mem(mem, actions)
    assert sum(mem.values()) == 208

    with open("input.txt") as file:
        actions = parse_actions(file.readlines())

    mem: dict[int, int] = {}
    do_actions(mem, actions)
    print(sum(mem.values()))
