import re

COORDS = re.compile(r"<x=(\-*\d+), y=(\-*\d+), z=(\-*\d+)>")

Coords = tuple[int, int, int]
Pair = tuple[Coords, Coords]


def parse_coords(lines: list[str]) -> list[Coords]:
    planets: list[Coords] = []
    for line in lines:
        match_ = COORDS.match(line.strip())
        if match_ is not None:
            planet = Coords(int(gr) for gr in match_.groups())
            planets.append(planet)
    return planets


def compute_vdiff(left: int, right: int) -> tuple[int, int]:
    if left < right:
        dvleft = 1
        dvright = -1
    elif left > right:
        dvleft = -1
        dvright = 1
    else:
        dvleft = 0
        dvright = 0
    return dvleft, dvright


def compute_gravity(left: Coords, right: Coords) -> Pair:
    """Computes the change in velocities for each planet-pair."""
    xleft, yleft, zleft = left
    xright, yright, zright = right
    dvxleft, dvxright = compute_vdiff(xleft, xright)
    dvyleft, dvyright = compute_vdiff(yleft, yright)
    dvzleft, dvzright = compute_vdiff(zleft, zright)
    dvleft = (dvxleft, dvyleft, dvzleft)
    dvright = (dvxright, dvyright, dvzright)
    return dvleft, dvright


def apply_diff(velocity: Coords, dv: Coords) -> Coords:
    return tuple[int, int, int](veli + dvi for veli, dvi in zip(velocity, dv))


def compute_velocity(planets: list[Coords], velocities: list[Coords]) -> list[Coords]:
    for idx, planet in enumerate(planets):
        for jdx, other in enumerate(planets[idx + 1 :], start=idx + 1):
            dv, dv_other = compute_gravity(planet, other)
            vel = apply_diff(velocities[idx], dv)
            vel_other = apply_diff(velocities[jdx], dv_other)
            velocities[idx] = vel
            velocities[jdx] = vel_other

    return [
        apply_diff(planet, velocity) for planet, velocity in zip(planets, velocities)
    ]


def run(planets: list[Coords], steps: int) -> tuple[list[Coords], list[Coords]]:
    velocities: list[tuple[int, int, int]] = [(0, 0, 0) for _ in planets]
    for _ in range(steps):
        planets = compute_velocity(planets, velocities)
    return planets, velocities


def run_forever(planets: list[Coords]) -> int:
    velocities: list[Coords] = [(0, 0, 0) for _ in planets]
    copy = velocities[:]
    steps = 0
    init_planets = planets[:]
    while True:
        planets = compute_velocity(planets, copy)
        steps += 1
        if planets == init_planets and velocities == copy:
            break
    return steps


def norm_one(planet: Coords) -> int:
    return sum(abs(i) for i in planet)


def compute_energy(planets: list[Coords], velocities: list[Coords]) -> int:
    return sum(
        norm_one(planet) * norm_one(vel) for planet, vel in zip(planets, velocities)
    )


if __name__ == "__main__":
    with open("sample.txt") as file:
        planets = parse_coords(file.readlines())
    planets_after, velocities = run(planets, 100)
    energy = compute_energy(planets_after, velocities)
    assert energy == 1940, energy

    with open("sample0.txt") as file:
        planets = parse_coords(file.readlines())
    timesteps = run_forever(planets)
    assert timesteps == 2772, timesteps

    with open("input.txt") as file:
        planets = parse_coords(file.readlines())
    planets, velocities = run(planets, 1000)
    energy = compute_energy(planets, velocities)
    print(energy)
