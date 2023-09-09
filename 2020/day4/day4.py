import re


Record = dict[str, str]

# field constants
HEIGHT = re.compile(r"(\d+)(cm|in)")
HAIR = re.compile(r"\#[a-f0-9]{6}")
EYE = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}
# record constants
FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL = {"cid"}


def check_year(value: str):
    return all(letter.isdigit() for letter in value) and len(value) == 4


def check_field(key: str, value:str) -> bool:
    if key == "byr":
        valid_num = check_year(value)
        return valid_num and 1920 <= int(value) <= 2002
    if key == "iyr":
        valid_num = check_year(value)
        return valid_num and 2010 <= int(value) <= 2020
    if key == "eyr":
        valid_num = check_year(value)
        return valid_num and 2020 <= int(value) <= 2030
    if key == "hgt":
        m = HEIGHT.match(value)
        if m is not None:
            number, unit = m.groups()
            number = int(number)
            if unit == "cm":
                return 150 <= number <= 193
            else:
                return 59 <= number <= 76
        return False
    if key == "hcl":
        m = HAIR.match(value)
        return m is not None
    if key == "ecl":
        return value in EYE
    if key == "pid":
        return all(letter.isdigit() for letter in value) and len(value) == 9
    return key in OPTIONAL

def parse_text(text:list[str]) -> list[Record]:
    records: list[Record] = []
    record: Record = {}
    for line in text:
        line = line.strip()
        if not line:
            records.append(record)
            record = {}
            continue
        pairs = line.split()
        for pair in pairs:
            key, value = pair.split(":")
            if check_field(key, value):
                record[key] = value
    else:
        records.append(record)
    return records


if __name__ == "__main__":
    with open("sample.txt") as file:
        text = file.readlines()
    records = parse_text(text) 
    assert 2 == (total := sum(1 for record in records if FIELDS.difference(record.keys()) in [set(), OPTIONAL])), total

    with open("input.txt") as file:
        text = file.readlines()
    records = parse_text(text) 
    print(sum(1 for record in records if FIELDS.difference(record.keys()) in [set(), OPTIONAL]))

