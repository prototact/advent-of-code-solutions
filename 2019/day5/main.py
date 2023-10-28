
def run_tests(instructions: list[int]) -> None:
    pointer = 0
    while instructions[pointer] != 99:
        operation = instructions[pointer]
        digits = str(operation).zfill(5)
        if digits.endswith('3'):
            location = instructions[pointer + 1]
            instructions[location] = 1
            pointer += 2
        elif digits.endswith('4'):
            modes = digits[:-2][::-1]
            value = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            print(value)
            pointer += 2
        elif digits.endswith('1'):   # 1
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            sum_ = left + right
            instructions[instructions[pointer + 3]] = sum_
            pointer += 4
        elif digits.endswith('2'):   # 2
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            prod_ = left * right
            instructions[instructions[pointer + 3]] = prod_
            pointer += 4
        else:
            raise ValueError(f"Unknown operation code {operation}")


def run_tests_extended(instructions: list[int]) -> None:
    pointer = 0
    while instructions[pointer] != 99:
        operation = instructions[pointer]
        digits = str(operation).zfill(5)
        if digits.endswith('3'):
            location = instructions[pointer + 1]
            instructions[location] = 5
            pointer += 2
        elif digits.endswith('4'):
            modes = digits[:-2][::-1]
            value = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            print(value)
            pointer += 2
        elif digits.endswith('1'):
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            sum_ = left + right
            instructions[instructions[pointer + 3]] = sum_
            pointer += 4
        elif digits.endswith('2'):
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            prod_ = left * right
            instructions[instructions[pointer + 3]] = prod_
            pointer += 4
        elif digits.endswith('5'):
            modes = digits[:-2][::-1]
            first = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            if first != 0:
                pointer = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            else:
                pointer += 3
        elif digits.endswith('6'):
            modes = digits[:-2][::-1]
            first = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            if first == 0:
                pointer = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            else:
                pointer += 3
        elif digits.endswith('7'):
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            if left < right:
                instructions[instructions[pointer + 3]] = 1
            else:
                instructions[instructions[pointer + 3]] = 0
            pointer += 4
        elif digits.endswith('8'):
            modes = digits[:-2][::-1]
            left = instructions[instructions[pointer + 1]] if modes[0] == '0' else instructions[pointer + 1]
            right = instructions[instructions[pointer + 2]] if modes[1] == '0' else instructions[pointer + 2]
            if left == right:
                instructions[instructions[pointer + 3]] = 1
            else:
                instructions[instructions[pointer + 3]] = 0
            pointer += 4
        else:
            raise ValueError(f"Unknown operation code {operation}")


if __name__ == "__main__":
    with open("input.txt") as file:
        instructions = [int(num) for num in file.readline().split(',')]
    run_tests(instructions[:])
    print("running extended tests")
    run_tests_extended(instructions[:])