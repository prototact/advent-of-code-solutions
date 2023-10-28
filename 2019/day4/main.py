
RANGE = range(264793, 803935 + 1)


def count_passwords(pswd_range: range = RANGE) -> int:
    count = 0
    for psswd in pswd_range:
        digits = str(psswd)
        any_ = False
        all_ = True
        for first, second in zip(digits[:-1], digits[1:]):
            if int(first) > int(second):
                all_ = False
                break
            if first == second:
                any_ = True
        if any_ and all_:
            count += 1
    return count
    

def count_passwords_strict(pswd_range: range = RANGE) -> int:
    count = 0
    for psswd in pswd_range:
        digits = str(psswd)
        any_: dict[str, int] = {}
        all_ = True
        for first, second in zip(digits[:-1], digits[1:]):
            if int(first) > int(second):
                all_ = False
                break
            any_[first] = any_.get(first, 0) + 1
        any_[digits[-1]] = any_.get(digits[-1], 0) + 1
        if any(val == 2 for val in any_.values()) and all_:
            count += 1
    return count


if __name__ == "__main__":
    print(count_passwords())
    print(count_passwords_strict())