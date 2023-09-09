from math import prod

Grid = list[str]


def slope(cur: tuple[int, int], move: tuple[int, int], grid: Grid) -> tuple[int, int]:
    horizontal, vertical = cur
    right, down = move
    border_h = len(grid[0])
    new_horizontal = horizontal + right
    if new_horizontal >= border_h:
        new_horizontal = new_horizontal % border_h
    new_vertical = vertical + down
    return new_horizontal, new_vertical    


def finished(cur: tuple[int, int], grid: Grid) -> bool:
    _, vertical = cur
    return vertical >= len(grid)

def is_tree(cur: tuple[int, int], grid: Grid) -> bool:
    horizontal, vertical = cur
    square = grid[vertical][horizontal]
    return square == "#"


if __name__ == "__main__":
    moves = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    with open("sample.txt", "r") as file:
        grid = [line.strip() for line in file.readlines()]
    trees: list[int] = []
    for move in moves:
        cur = (0, 0)
        total = 0
        while not finished(cur, grid):
            total += is_tree(cur, grid)
            cur = slope(cur, move, grid)
        trees.append(total)
    assert trees[1] == 7 and prod(trees) == 336
       
    with open("input.txt", "r") as file:
        grid = [line.strip() for line in file.readlines()]
    trees: list[int] = []
    for move in moves:
        cur = (0, 0)
        total = 0
        while not finished(cur, grid):
            total += is_tree(cur, grid)
            cur = slope(cur, move, grid)
        trees.append(total)
    print(trees[1], prod(trees))
