from collections.abc import Generator


def run_program(program: list[int], inpt: int) -> Generator[int, int, None]:
    instructions = {idx: value for idx, value in enumerate(program)}
    pointer = 0
    base = 0
    while instructions.get(pointer, 0) != 99:
        operation = instructions[pointer]
        digits = str(operation).zfill(5)
        if digits.endswith('3'):
            modes = digits[:-2][::-1]
            location = instructions.get(pointer + 1, 0) if modes[0] == '0' else base + instructions.get(pointer + 1, 0)
            instructions[location] = inpt
            pointer += 2
        elif digits.endswith('4'):
            modes = digits[:-2][::-1]
            value = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            inpt = yield value
            pointer += 2
        elif digits.endswith('1'):
            modes = digits[:-2][::-1]
            left = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            right = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            sum_ = left + right
            if modes[2] == '0':
                instructions[instructions.get(pointer + 3, 0)] = sum_
            elif modes[2] == '2':
                instructions[base + instructions.get(pointer + 3, 0)] = sum_
            pointer += 4
        elif digits.endswith('2'):
            modes = digits[:-2][::-1]
            left = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            right = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            prod_ = left * right
            if modes[2] == '0':
                instructions[instructions.get(pointer + 3, 0)] = prod_
            elif modes[2] == '2':
                instructions[base + instructions.get(pointer + 3, 0)] = prod_
            pointer += 4
        elif digits.endswith('5'):
            modes = digits[:-2][::-1]
            first = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            if first != 0:
                pointer = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            else:
                pointer += 3
        elif digits.endswith('6'):
            modes = digits[:-2][::-1]
            first = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            if first == 0:
                pointer = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            else:
                pointer += 3
        elif digits.endswith('7'):
            modes = digits[:-2][::-1]
            left = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            right = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            if left < right:
                if modes[2] == '0':
                    instructions[instructions.get(pointer + 3, 0)] = 1
                elif modes[2] == '2':
                    instructions[base + instructions.get(pointer + 3, 0)] = 1
            else:
                if modes[2] == '0':
                    instructions[instructions.get(pointer + 3, 0)] = 0
                elif modes[2] == '2':
                    instructions[base + instructions.get(pointer + 3, 0)] = 0
            pointer += 4
        elif digits.endswith('8'):
            modes = digits[:-2][::-1]
            left = instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            right = instructions.get(instructions.get(pointer + 2, 0), 0) if modes[1] == '0' else instructions.get(pointer + 2, 0) if modes[1] == '1' else instructions.get(base + instructions.get(pointer + 2, 0), 0)
            if left == right:
                if modes[2] == '0':
                    instructions[instructions.get(pointer + 3, 0)] = 1
                elif modes[2] == '2':
                    instructions[base + instructions.get(pointer + 3, 0)] = 1
            else:
                if modes[2] == '0':
                    instructions[instructions.get(pointer + 3, 0)] = 0
                elif modes[2] == '2':
                    instructions[base + instructions.get(pointer + 3, 0)] = 0
            pointer += 4
        elif digits.endswith('9'):
            modes = digits[:-2][::-1]
            base += instructions.get(instructions.get(pointer + 1, 0), 0) if modes[0] == '0' else instructions.get(pointer + 1, 0) if modes[0] == '1' else instructions.get(base + instructions.get(pointer + 1, 0), 0)
            pointer += 2
        else:
            raise ValueError(f"Unknown operation code {operation}")


def turn_and_move(coords: tuple[int, int], dir_: tuple[int, int], turn: int) -> tuple[tuple[int, int], tuple[int, int]]:
    left = [[0, -1], [1, 0]]
    right = [[0, 1], [-1, 0]]
    if turn == 0:
        dir_ = (left[0][0] * dir_[0] + left[0][1] * dir_[1], left[1][0] * dir_[0] + left[1][1] * dir_[1])
    else:
        dir_ = (right[0][0] * dir_[0] + right[0][1] * dir_[1], right[1][0] * dir_[0] + right[1][1] * dir_[1])
    coords = (coords[0] + dir_[0], coords[1] + dir_[1])

    return coords, dir_


def move_and_count(program: list[int]) -> int:
    coords = (0, 0) # vert, horiz
    dir_ = (1, 0)
    painted: set[tuple[int, int]] = set()
    colors: dict[tuple[int, int], int] = {}

    current = colors.get(coords, 0)
    g = run_program(program, current)
    color = next(g)
    colors[coords] = color
    painted.add(coords)
    turn = g.send(0)
    coords, dir_ = turn_and_move(coords, dir_, turn) 
    while True:
        current = colors.get(coords, 0)
        try:
            color = g.send(current)
        except StopIteration:
            break
        colors[coords] = color
        painted.add(coords)
        turn = g.send(0)
        coords, dir_ = turn_and_move(coords, dir_, turn)
    return len(painted)


def move_and_paint(program: list[int]) -> dict[tuple[int, int], int]:
    coords = (0, 0) # vert, horiz
    dir_ = (-1, 0)
    colors: dict[tuple[int, int], int] = {}

    current = 1  # start
    g = run_program(program, current)
    color = next(g)
    colors[coords] = color
    turn = g.send(0)
    coords, dir_ = turn_and_move(coords, dir_, turn) 
    while True:
        current = colors.get(coords, 0)
        try:
            color = g.send(current)
        except StopIteration:
            break
        colors[coords] = color
        turn = g.send(0)
        coords, dir_ = turn_and_move(coords, dir_, turn)
    return colors


def print_panels(colors: dict[tuple[int, int], int]) -> None:
    bottom_right = max(colors)
    top_left = min(colors)
    panels = [[colors.get((idx, jdx), 0) for jdx in range(top_left[1], bottom_right[1] + 1)] for idx in range(top_left[0], bottom_right[0] + 1)]
    for row in panels:
        print(''.join('#' if color == 1 else '.' for color in row))


if __name__ == "__main__":
    with open("input.txt") as file:
        program = [int(num) for num in file.readline().strip().split(",")]
    painted = move_and_count(program[:])
    print(painted)
    colors = move_and_paint(program[:])
    print_panels(colors)