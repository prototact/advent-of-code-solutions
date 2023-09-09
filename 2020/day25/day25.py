from typing import Optional


def transform_key(subject_number: int, loop_size: int, start_value: int = 1) -> int:
    value = start_value
    for _ in range(loop_size):
        value = value * subject_number
        value = value % 20201227
    return value


def find_loop_size(subject_number: int, known_key: int) -> Optional[int]:
    memo: dict[int, int] = {0: 1}
    total_loops = 0
    while True:
        key = transform_key(subject_number, 1, memo[total_loops])
        total_loops += 1
        memo[total_loops] = key
        if key == known_key:
            return total_loops


if __name__ == "__main__":
    card_key = 5764801
    door_key = 17807724

    card_loop_size = find_loop_size(7, card_key)
    door_loop_size = find_loop_size(7, door_key)
    assert card_loop_size == 8 and door_loop_size == 11

    encryption_key = transform_key(door_key, card_loop_size)
    encryption_key2 = transform_key(card_key, door_loop_size)

    assert encryption_key == encryption_key2 == 14897079, (encryption_key, encryption_key2)

    print("test okay!")

    card_key = 19774466
    door_key = 7290641

    card_loop_size = find_loop_size(7, card_key)
    door_loop_size = find_loop_size(7, door_key)
    print(card_loop_size, door_loop_size)

    if card_loop_size is not None:
        encryption_key = transform_key(door_key, card_loop_size)
    if door_loop_size is not None:
        encryption_key2 = transform_key(card_key, door_loop_size)

    print(encryption_key, encryption_key2)
