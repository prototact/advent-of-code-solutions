import re
from typing import Optional
from enum import Enum


class Command(Enum):
    NOP = 0
    ACC = 1
    JMP = 2


Program = dict[int, tuple[Command, int]]


COMMAND = re.compile(r"^(nop|acc|jmp) ((?:\+|-)\d+)$")


def parse_command(line: str) -> tuple[Command, int]:
    m = COMMAND.match(line.strip())
    if m is not None:
        command_type, number = m.groups()
        sign = number[0]
        value = number[1:]
        actual_number = int(value) if sign == "+" else -int(value)
        match command_type:
            case "nop":
                return Command.NOP, actual_number
            case "acc":
                return Command.ACC, actual_number
            case "jmp":
                return Command.JMP, actual_number
            case _:
                raise ValueError(f"unknown command: {command_type}")
    raise ValueError(f"Line bad format: {line}")


def run_program(program: Program) -> tuple[int, bool]:
    executed_lines: set[int] = set()
    start = 0
    acc = 0
    last = len(program)
    while start not in executed_lines and start < last:
        cmd = program[start]
        executed_lines.add(start)
        match cmd:
            case (Command.NOP, _):
                start += 1
            case (Command.ACC, num):
                acc += num
                start += 1
            case (Command.JMP, step):
                start += step
    return acc, start >= last


def find_terminating_program(program: Program) -> Optional[int]:
    for number, (command_type, step) in program.items():
        if command_type == Command.NOP:
            new_cmd = Command.JMP
        elif command_type == Command.JMP:
            new_cmd = Command.NOP
        else:
            continue
        new_program = {number_: command if number_ != number else (new_cmd, step)
                       for number_, command in program.items()}
        acc, finished = run_program(new_program)
        if finished:
            return acc


if __name__ == "__main__":
    program: Program = {}
    with open("sample.txt", "r") as file:
        for id_, line in enumerate(file.readlines()):
            cmd = parse_command(line)
            program[id_] = cmd
    acc, _ = run_program(program)
    assert acc == 5, acc

    assert (result := find_terminating_program(program)) == 8, result

    program = {}
    with open("input.txt", "r") as file:
        for id_, line in enumerate(file.readlines()):
            cmd = parse_command(line)
            program[id_] = cmd
    acc, _ = run_program(program)
    print(acc)

    print(find_terminating_program(program))

