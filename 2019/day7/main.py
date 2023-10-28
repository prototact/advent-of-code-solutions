from dataclasses import dataclass
from typing import Optional
from collections.abc  import Generator


@dataclass(frozen=True)
class Amplifier:
    phase: int

    def run_program(self, inpt: int, prog: list[int]) -> int:
        pointer = 0
        phased = False
        output: Optional[int] = None
        while prog[pointer] != 99:
            digits = str(prog[pointer]).zfill(5)
            if digits.endswith('1'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                prog[prog[pointer + 3]] = left + right
                pointer += 4
            elif digits.endswith('2'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                prog[prog[pointer + 3]] = left * right
                pointer += 4
            elif digits.endswith('3'):
                prog[prog[pointer + 1]] = self.phase if not phased else inpt
                phased = True
                pointer += 2
            elif digits.endswith('4'):
                mode = digits[:-2][::-1]
                output = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                pointer += 2
            elif digits.endswith('5'):
                mode = digits[:-2][::-1]
                bit = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                if bit:
                    pointer = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                else:
                    pointer += 3
            elif digits.endswith('6'):
                mode = digits[:-2][::-1]
                bit = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                if not bit:
                    pointer = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                else:
                    pointer += 3
            elif digits.endswith('7'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                if left < right:
                    prog[prog[pointer + 3]] = 1
                else:
                    prog[prog[pointer + 3]] = 0
                pointer += 4
            elif digits.endswith('8'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                if left == right:
                    prog[prog[pointer + 3]] = 1
                else:
                    prog[prog[pointer + 3]] = 0
                pointer += 4
            else:
                raise ValueError(f"Unknown op code: {prog[pointer]}")
        if output is not None:
            return output
        raise ValueError("Failed to output a value")

@dataclass
class LoopedAmplifier:
    phase: int

    def run_program(self, inpt: int, prog: list[int]) -> Generator[int, int, None]:
        pointer = 0
        phased = False
        output: Optional[int] = None
        while prog[pointer] != 99:
            digits = str(prog[pointer]).zfill(5)
            if digits.endswith('1'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                prog[prog[pointer + 3]] = left + right
                pointer += 4
            elif digits.endswith('2'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                prog[prog[pointer + 3]] = left * right
                pointer += 4
            elif digits.endswith('3'):
                prog[prog[pointer + 1]] = self.phase if not phased else inpt
                phased = True
                pointer += 2
            elif digits.endswith('4'):
                mode = digits[:-2][::-1]
                output = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                pointer += 2
                inpt = yield output
            elif digits.endswith('5'):
                mode = digits[:-2][::-1]
                bit = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                if bit:
                    pointer = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                else:
                    pointer += 3
            elif digits.endswith('6'):
                mode = digits[:-2][::-1]
                bit = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                if not bit:
                    pointer = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                else:
                    pointer += 3
            elif digits.endswith('7'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                if left < right:
                    prog[prog[pointer + 3]] = 1
                else:
                    prog[prog[pointer + 3]] = 0
                pointer += 4
            elif digits.endswith('8'):
                mode = digits[:-2][::-1]
                left = prog[prog[pointer + 1]] if mode[0] == '0' else prog[pointer + 1]
                right = prog[prog[pointer + 2]] if mode[1] == '0' else prog[pointer + 2]
                if left == right:
                    prog[prog[pointer + 3]] = 1
                else:
                    prog[prog[pointer + 3]] = 0
                pointer += 4
            else:
                raise ValueError(f"Unknown op code: {prog[pointer]}")

def chain_amplifiers(phases: list[int], program: list[int]) -> int:
    amplifiers = [Amplifier(phase) for phase in phases]
    input_ = 0
    for amplifier in amplifiers:
        input_ = amplifier.run_program(input_, program[:])
    return input_

def chain_amplifiers_looped(phases: list[int], program: list[int]) -> int:
    amplifiers = [LoopedAmplifier(phase) for phase in phases]
    input_ = 0
    gens: list[Generator[int, int, None]] = []
    for amplifier in amplifiers:
        g = amplifier.run_program(input_, program[:])
        input_ = next(g)
        gens.append(g)
    idx = 0
    finished = 0
    while finished < len(gens):
        g = gens[idx]
        try:
            input_ = g.send(input_)
        except StopIteration:
            finished += 1
        idx = (idx + 1) % len(gens)
    return input_ 


def permutations(values: list[int]) -> Generator[list[int], None, None]:
    if not values:
        yield []
        return
    for idx, value in enumerate(values):
        for sub in permutations(values[:idx] + values[idx + 1:]):
            yield [value, *sub]


def test_combinations(program: list[int]) -> Optional[int]:
    phases = list(range(0, 5))
    return max(chain_amplifiers(perm, program) for perm in permutations(phases))


def test_combinations_looped(program: list[int]) -> Optional[int]:
    phases = list(range(5, 10))
    return max(chain_amplifiers_looped(perm, program) for perm in permutations(phases))


if __name__ == "__main__":
    program = [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]
    assert (res := chain_amplifiers([4,3,2,1,0], program)) == 43210, res
    assert (res := test_combinations(program)) == 43210, res
    
    program = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
    assert (res := test_combinations_looped(program)) == 139629729, res

    with open("input.txt") as file:
        program = [int(num) for num in file.readline().strip().split(',')]
    print(test_combinations(program))
    print(test_combinations_looped(program))