from collections import Counter, deque
import re


FOOD = re.compile(r"((?:\w+\s*)+) \(contains ((?:\w+(?:,\s)*)+)\)")


def parse_ingredients_and_allergies(lines: list[str]) -> list[tuple[list[str], list[str]]]:
    ingredients_and_allergies: list[tuple[list[str], list[str]]] = []
    for line in lines:
        line = line.strip()
        match_ = FOOD.match(line)
        if match_ is not None:
            ingredients, allergies = match_.groups()
            ingr = ingredients.strip().split()
            allg = [alg.strip() for alg in allergies.strip().split(',')]
            ingredients_and_allergies.append((ingr, allg))
    return ingredients_and_allergies


def find_safe(ingredients_and_allergies: list[tuple[list[str], list[str]]]) -> tuple[set[str], dict[str, list[set[str]]]]: 
    possible: dict[str, list[set[str]]] = {}
    all_ingredients: set[str] = set()
    for ingredients, allergies in ingredients_and_allergies:
        for allergy in allergies:
            associated_ingredients = possible.get(allergy, [])
            associated_ingredients.append(set(ingredients))
            possible[allergy] = associated_ingredients
            all_ingredients = all_ingredients.union(ingr for ingredients in associated_ingredients for ingr in ingredients)
    impossible: set[str] = set()
    for ingredient in all_ingredients:
        if all(not all(ingredient in ingredients for ingredients in associated_ingredients)
                   for _, associated_ingredients in possible.items()):
            impossible.add(ingredient)
    return impossible, possible


def count_safe(ingredients_and_allergies: list[tuple[list[str], list[str]]], safe: set[str]) -> int:
    counts = Counter(ingredient for ingredients, _ in ingredients_and_allergies for ingredient in ingredients)
    return sum(count for ingredient, count in counts.items() if ingredient in safe)


def remove_safe(safe: set[str], possible: dict[str, list[set[str]]]) -> dict[str, list[set[str]]]:
    return {allergy: [set(ingredient for ingredient in ingredients if ingredient not in safe) for ingredients in rules]
            for allergy, rules in possible.items()}


def find_unsafe(possible: dict[str, list[set[str]]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    all_allergies = deque(possible)
    while all_allergies:
        allergy = all_allergies.popleft()
        rules = possible[allergy]
        all_ingredients = set[str]().union(ingr for ingredients in rules for ingr in ingredients)
        for ingredient in all_ingredients:
            others = set(all_ingredients)
            others.remove(ingredient)
            if (all(ingredient in ingredients for ingredients in rules) and
                all(not all(other in ingredients for ingredients in rules) for other in others)):
                mapping[allergy] = ingredient
                break
        if allergy not in mapping:
            all_allergies.append(allergy)
        else:
            possible = {allrg: [set(ingr for ingr in ingredients if mapping[allergy] != ingr) 
                                for ingredients in rules] for allrg, rules in possible.items()}

    return mapping


def get_canonical_dangerous_list(mapping: dict[str, str]) -> str:
    return ','.join(ingr for _, ingr in sorted(mapping.items(), key=lambda x: x[0]))


if __name__ == "__main__":
    with open("sample.txt") as file:
        lines = file.readlines()
    ingredients_and_allergies = parse_ingredients_and_allergies(lines)
    safe, possible = find_safe(ingredients_and_allergies)
    total = count_safe(ingredients_and_allergies, safe)
    assert total == 5
    possible = remove_safe(safe, possible)
    mapping = find_unsafe(possible)
    assert get_canonical_dangerous_list(mapping) == "mxmxvkd,sqjhc,fvjkl"

    with open("input.txt") as file:
        lines = file.readlines()
    ingredients_and_allergies = parse_ingredients_and_allergies(lines)
    certainly_safe, possible = find_safe(ingredients_and_allergies)
    total = count_safe(ingredients_and_allergies, certainly_safe)
    print(total)
    possible = remove_safe(safe, possible)
    mapping = find_unsafe(possible)
    print(get_canonical_dangerous_list(mapping))
