import re
from dataclasses import dataclass
from enum import Enum
from itertools import cycle

NODE = re.compile(r"(\w+) = \((\w+), (\w+)\)")


class Move(Enum):
    Left = 1
    Right = 2


@dataclass
class Node:
    name: str
    left: str
    right: str


@dataclass
class Adjacency:
    _start: str
    _end: str
    _vectors: dict[str, Node]

    def _move(self, current: Node, dir_: Move) -> Node:
        match dir_:
            case Move.Left:
                return self._vectors[self._vectors[current.name].left]
            case Move.Right:
                return self._vectors[self._vectors[current.name].right]

    def follow_instructions(self, instructions: list[Move]) -> int:
        steps = 0
        current = self._vectors[self._start]
        for dir_ in cycle(instructions):
            if current.name == self._end:
                break
            current = self._move(current, dir_)
            steps += 1
        return steps

    def follow_ghost_instructions(self, instructions: list[Move]) -> int:
        steps = 0
        currents = [
            value
            for name, value in self._vectors.items()
            if name.endswith(self._start[-1])
        ]
        for dir_ in cycle(instructions):
            if all(current.name.endswith(self._end[-1]) for current in currents):
                break
            currents = [self._move(current, dir_) for current in currents]
            steps += 1
        return steps


def parse_instructions(lines: list[str]) -> tuple[list[Move], Adjacency]:
    itr = iter(lines)
    moves = [Move.Left if c == "L" else Move.Right for c in next(itr, "").strip()]
    vec: dict[str, Node] = {}
    for line in itr:
        m = NODE.match(line.strip())
        if m is not None:
            name, left, right = m.group(1), m.group(2), m.group(3)
            node = Node(name, left, right)
            vec[node.name] = node
    adjacency = Adjacency("AAA", "ZZZ", vec)
    return moves, adjacency


if __name__ == "__main__":
    with open("sample.txt") as file:
        moves, adjacency = parse_instructions(file.readlines())
    steps = adjacency.follow_instructions(moves)
    assert steps == 6, steps

    with open("sample2.txt") as file:
        moves, adjacency = parse_instructions(file.readlines())
    steps = adjacency.follow_ghost_instructions(moves)
    assert steps == 6, steps

    with open("input.txt") as file:
        moves, adjacency = parse_instructions(file.readlines())
    steps = adjacency.follow_instructions(moves)
    print(steps)

    steps = adjacency.follow_ghost_instructions(moves)
    print(steps)
