

def take_turns(target_turn: int, spoken: dict[int, tuple[bool, int]], last_number: int) -> int:
    current_turn = len(spoken) + 1
    while current_turn < target_turn + 1:
        first, prev_turn = spoken[last_number]
        spoken[last_number] = (False, current_turn - 1)
        last_number = 0 if first else current_turn - 1 - prev_turn
        if last_number not in spoken:
            spoken[last_number] = (True, current_turn)
        else:
            spoken[last_number] = (False, spoken[last_number][1])
        current_turn += 1
    return last_number


def take_initial_turns(initial: list[int]) -> dict[int, tuple[bool, int]]:
    return {number: (True, turn) for turn, number in enumerate(initial, start = 1)}

if __name__ == "__main__":
    sample1 = [0, 3, 6]
    spoken = take_initial_turns(sample1)
    assert (result := take_turns(2020, spoken, 6)) == 436, result

    sample2 = [1, 3, 2]
    spoken = take_initial_turns(sample2)
    assert (result := take_turns(2020, spoken, 2)) == 1, result

    sample3 = [2, 1, 3]
    spoken = take_initial_turns(sample3)
    assert (result := take_turns(2020, spoken, 3)) == 10, result

    sample4 = [1, 2, 3]
    spoken = take_initial_turns(sample4)
    assert (result := take_turns(2020, spoken, 3)) == 27, result

    sample5 = [2, 3, 1]
    spoken = take_initial_turns(sample5)
    assert (result := take_turns(2020, spoken, 1)) == 78, result

    sample6 = [3, 2, 1]
    spoken = take_initial_turns(sample6)
    assert (result := take_turns(2020, spoken, 1)) == 438, result

    sample7 = [3, 1, 2]
    spoken = take_initial_turns(sample7)
    assert (result := take_turns(2020, spoken, 2)) == 1836, result

    input_ = [18, 11, 9, 0, 5, 1]
    spoken = take_initial_turns(input_)
    print(take_turns(2020, spoken, 1))

    # spoken = take_initial_turns(input_)
    # print(take_turns(30_000_000, spoken, 1))

   