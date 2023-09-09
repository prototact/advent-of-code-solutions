from collections.abc import Iterator, Generator
from dataclasses import dataclass
from collections import deque
import re

LEAF = re.compile(r"(\d+): \"(\w)\"")
RULE = re.compile(r"(\d+): (.+)")



@dataclass
class Value:
    ...

@dataclass
class Ref(Value):
    seqs: list[list[int]]

@dataclass
class Char(Value):
    value: str

Rules = dict[int, Value]

def parse_rules(itr: Iterator[str]) -> Rules:
    rules: Rules = {}
    for line in itr:
        line = line.strip()
        if not line:
            break
        match_ = LEAF.match(line)
        match2 = RULE.match(line)
        if match_ is not None:
            rule_id, char = match_.groups()
            rules[int(rule_id)] = Char(value=char)
        elif match2 is not None:
            rule_id, raw = match2.groups()
            seqs = [[int(num) for num in seq.strip().split(" ")] for seq in raw.split("|")]
            rules[int(rule_id)] = Ref(seqs=seqs)
        else:
            raise ValueError(f"Rule not parsed {line}")
    return rules


def check_image(image: str, idx: int, rules: Rules, count: int) -> tuple[bool, int]:
    match rules[idx]:
        case Char(value=value):
            try:
                char = image[count]
            except IndexError:
                return False, count
            return char == value, count + 1
        case Ref(seqs=seqs):
            for seq in seqs:
                new_count = count
                to_accept = True
                for rule_id in seq:
                    accept, new_count = check_image(image, rule_id, rules, new_count)
                    to_accept &= accept
                if to_accept:
                    return True, new_count
            return False, count
        case _:
            raise ValueError(f"Unknown entry type {rules[idx]}")

def check_start(image:list[str | int]) -> str:
    actual = ""
    for c in image:
        if isinstance(c, str):
            actual += c
        else:
            return actual
    return actual



# i have to make it eager somehow, so that it produces the string and terminates 
# when the image terminates
def check_image_infinite(image: str, start_idx: int, rules: Rules) -> bool:
    def resolve(images: dict[str, list[deque[int]]]) -> None:
        img = min(images, key=len)
        to_evaluate = images.pop(img)
        while to_evaluate:
            new_to_evaluate: list[deque[int]] = []
            combination = to_evaluate.pop()
            try:
                first = combination.popleft()
            except IndexError:
                continue
            match rules[first]:
                case Char(value=value):
                    new_value = img + value
                    if image.startswith(new_value):
                        images[new_value] = images.get(new_value, []) 
                        images[new_value].append(combination)
                case Ref(seqs=seqs):
                    for seq in seqs:
                        comb = combination.copy()
                        comb.extendleft(seq[::-1])
                        new_to_evaluate.append(comb)
                case _:
                    raise ValueError("Unreachable")
            to_evaluate.extend(new_to_evaluate)
            
    def generate_image() -> Generator[str, None, None]:
        images = {"": [deque([start_idx])]}
        for _ in range(len(image)):
            resolve(images)
            if not images:
                break
        yield from (img for img, seqs in images.items() if any(not seq for seq in seqs))

    for gen_image in generate_image():
        if gen_image == image:
            return True
    return False
    

def check_images(images: list[str], rules: Rules) -> list[str]:
    valid_images: list[str] = []
    for image in images:
        valid, count = check_image(image, 0, rules, 0)
        if valid and count == len(image):
            valid_images.append(image)
    return valid_images

def check_images_infinite(images: list[str], rules: Rules) -> list[str]:
    valid_images: list[str] = []
    for image in images:
        valid = check_image_infinite(image, 0, rules)
        if valid:
            valid_images.append(image)
    return valid_images


if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    itr = iter(lines)
    rules = parse_rules(itr)
    images = list(line.strip() for line in itr)

    valid_images = check_images(images, rules)
    assert valid_images == ["ababbb", "abbbab"]

    with open("sample2.txt") as file:
        lines = file.readlines()
    itr = iter(lines)
    rules = parse_rules(itr)
    images = list(line.strip() for line in itr)

    valid_images = check_images_infinite(images, rules)
    assert len(valid_images) == 12, len(valid_images)
    print("samples work")

    with open("input.txt") as file:
        lines = file.readlines()
    itr = iter(lines)
    rules = parse_rules(itr)
    images = list(line.strip() for line in itr)

    valid_images = check_images(images, rules)
    print(len(valid_images))

    with open("input2.txt") as file:
        lines = file.readlines()
    itr = iter(lines)
    rules = parse_rules(itr)
    images = list(line.strip() for line in itr)

    valid_images = check_images_infinite(images, rules)
    print(len(valid_images))
