

def run_tests_extended(program: list[int], inpt: int = 1) -> None:
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
            print(value)
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


if __name__ == "__main__":
   instructions = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
   run_tests_extended(instructions)

   instructions = [1102,34915192,34915192,7,4,7,99,0]
   run_tests_extended(instructions)

   print("actual tests")
   with open("input.txt") as file:
       instructions = [int(num) for num in file.readline().strip().split(',')]
   run_tests_extended(instructions[:])
   run_tests_extended(instructions[:], inpt=2)