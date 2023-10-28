

def parse_image(image: str, dims: tuple[int, int]) -> list[list[list[int]]]:
    layers: list[list[list[int]]] = []
    layer: list[list[int]] = []
    row: list[int] = []
    width, height = dims
    for digit in image:
        row.append(int(digit))
        if len(row) == width:
            layer.append(row)
            row = []
        if len(layer) == height:
            layers.append(layer)
            layer = []    
    return layers


def validate(layers: list[list[list[int]]]) -> int:
    layer = min(layers, key=lambda lar: sum(1 for row in lar for digit in row if digit == 0))
    ones = sum(1 for row in layer for digit in row if digit == 1)
    twos = sum(1 for row in layer for digit in row if digit == 2)
    return ones * twos


def render(layers: list[list[list[int]]], dims: tuple[int, int]) -> list[str]:
    actual: list[list[str]] = []
    width, height = dims
    for jdx in range(height):
        row: list[str] = []
        for idx in range(width):
            for layer in layers:
                color = layer[jdx][idx] 
                if color == 0:
                    row.append('\u25AF')
                    break
                elif color == 1:
                    row.append('\u25AE')
                    break
        actual.append(row)
        assert len(row) == width
    return [''.join(row) for row in actual]


if __name__ == "__main__":
    image = "123456789012"
    dims = (3, 2)
    layers = parse_image(image, dims)
    assert (res := validate(layers)) == 1, res

    with open("input.txt") as file:
        image = file.readline().strip()
    dims = (25, 6)
    layers = parse_image(image, dims)
    print(validate(layers))

    for row in render(layers, dims):
        print(row)