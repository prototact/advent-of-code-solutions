
def make_relations(orbits: list[tuple[str, str]]) -> tuple[dict[str, list[str]], str]:
    relations: dict[str, list[str]] = {}
    dsts: set[str] = set()
    planets: set[str] = set()
    for src, dst in orbits:
        orbs = relations.get(src, [])
        orbs.append(dst)
        relations[src] = orbs
        dsts.add(dst)
        planets.add(dst)
        planets.add(src)
    root = (planets - dsts).pop()
    return relations, root

def count_total_orbits(orbits: list[tuple[str, str]]) -> int:
    relations, root = make_relations(orbits)

    def go(root: str) -> tuple[int, int]:
        dsts = relations.get(root, [])
        if not dsts:
            return 0, 1
        count = 0
        total_size = 0
        for dst in dsts:
            acc, size = go(dst)
            total_size += size
            count += acc + size
        return count, total_size + 1

    final, _ = go(root)
    return final


def find_route(orbits: list[tuple[str, str]]) -> int:
    relations, root = make_relations(orbits)
    def go(root: str, dst: str, acc: set[str]) -> set[str]:
        dsts = relations.get(root, [])
        if not dsts:
            return acc if root == dst else set()
        for adst in dsts:
            new_acc = acc.copy()
            new_acc.add(adst)
            route = go(adst, dst, new_acc)
            if route:
                return route
        return set()
    left = go(root, "YOU", set())
    right = go(root, "SAN", set())
    return len(left ^ right) - 2
        


if __name__ == "__main__":
    with open("sample.txt") as file:
        orbits = [((rel := line.strip().split(")"))[0], rel[1]) for line in file.readlines()]
    assert (res := count_total_orbits(orbits)) == 42, res
    
    augmented_orbits = orbits + [("K", "YOU"), ("I", "SAN")]
    assert (res := find_route(augmented_orbits)) == 4, res

    with open("input.txt") as file:
        orbits = [((rel := line.strip().split(")"))[0], rel[1]) for line in file.readlines()]
    print(count_total_orbits(orbits))
    print(find_route(orbits))