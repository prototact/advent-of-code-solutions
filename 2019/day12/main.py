import re
from itertools import combinations, chain
from math import sqrt, ceil

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
    return Coords(veli + dvi for veli, dvi in zip(velocity, dv))


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


def find_contact(left: tuple[int, int, int], right: tuple[int, int, int]) -> int | None:
    x0, v0, g0 = left
    x1, v1, g1 = right
    if x0 == x1:
        return 0
    alpha = (g0 - g1) / 2
    beta = v0 - v1 + alpha
    gamma = x0 - x1
    if alpha == 0 and beta == 0:
        return None
    if alpha == 0:
        tau = -gamma / beta
        return ceil(tau) if tau >= 0 else None
    delta = beta**2 - 4 * alpha * gamma
    if delta < 0:
        return None
    tau1 = (-beta + sqrt(delta)) / (2 * alpha)
    tau2 = (-beta - sqrt(delta)) / (2 * alpha)
    if tau1 >= 0 and tau2 >= 0:
        return ceil(min(tau1, tau2))
    if tau1 >= 0:
        return ceil(tau1)
    if tau2 >= 0:
        return ceil(tau2)


def find_contact_any_dim(
    left: tuple[Coords, Coords, Coords], right: tuple[Coords, Coords, Coords]
) -> int | None:
    loc_left, vel_left, accel_left = left
    loc_right, vel_right, accel_right = right

    x_contact = find_contact(
        (loc_left[0], vel_left[0], accel_left[0]),
        (loc_right[0], vel_right[0], accel_right[0]),
    )
    y_contact = find_contact(
        (loc_left[1], vel_left[1], accel_left[1]),
        (loc_right[1], vel_right[1], accel_right[1]),
    )
    z_contact = find_contact(
        (loc_left[2], vel_left[2], accel_left[2]),
        (loc_right[2], vel_right[2], accel_right[2]),
    )

    if x_contact is not None and y_contact is not None and z_contact is not None:
        if x_contact < y_contact and x_contact < z_contact:
            return x_contact
        if y_contact < z_contact and y_contact < x_contact:
            return y_contact
        if z_contact < x_contact and z_contact < y_contact:
            return z_contact
        if x_contact == y_contact and x_contact < z_contact:
            return x_contact
        if x_contact == z_contact and x_contact < y_contact:
            return x_contact
        if y_contact == z_contact and y_contact < x_contact:
            return y_contact
        return x_contact
    elif x_contact is not None and y_contact is not None:
        if x_contact < y_contact:
            return x_contact
        if y_contact < x_contact:
            return y_contact
        return x_contact
    elif x_contact is not None and z_contact is not None:
        if z_contact < x_contact:
            return z_contact
        if x_contact < z_contact:
            return x_contact
        return x_contact
    elif y_contact is not None and z_contact is not None:
        if z_contact < y_contact:
            return z_contact
        if y_contact < z_contact:
            return y_contact
        return z_contact
    elif x_contact is not None:
        return x_contact
    elif y_contact is not None:
        return y_contact
    elif z_contact is not None:
        return z_contact


def compute_accels(planets: list[Coords]) -> list[Coords]:
    accels: list[Coords] = []
    for idx, planet in enumerate(planets):
        x_left, y_left, z_left = planet
        accel_x, accel_y, accel_z = (0, 0, 0)
        for other in chain(planets[:idx], planets[idx + 1 :]):
            x_right, y_right, z_right = other
            if x_left < x_right:
                accel_x += 1
            elif x_left > x_right:
                accel_x -= 1
            if y_left < y_right:
                accel_y += 1
            elif y_left > y_right:
                accel_y -= 1
            if z_left < z_right:
                accel_z += 1
            elif z_left > z_right:
                accel_z -= 1
        accels.append((accel_x, accel_y, accel_z))
    return accels


def advance_location(
    planet: Coords, velocity: Coords, accel: Coords, timestep: int
) -> Coords:
    return Coords(
        loc + vel * timestep + acc * ((timestep * (timestep + 1)) // 2)
        for loc, vel, acc in zip(planet, velocity, accel)
    )


def advance_velocity(velocity: Coords, accel: Coords, timestep: int) -> Coords:
    return Coords(vel + acc * timestep for vel, acc in zip(velocity, accel))


def advance(
    planets: list[Coords], velocities: list[Coords]
) -> tuple[list[Coords], list[Coords], int]:
    accels = compute_accels(planets)
    min_contact = None
    for (idx, left), (jdx, right) in combinations(enumerate(planets), r=2):
        contact = find_contact_any_dim(
            (left, velocities[idx], accels[idx]), (right, velocities[jdx], accels[jdx])
        )
        if min_contact is not None and contact is not None:
            if min_contact > contact:
                min_contact = contact
        if min_contact is None and contact is not None:
            min_contact = contact
    if min_contact is None:
        raise ValueError("Impossible, planets should meet at some point!")

    if min_contact == 0:
        new_planets = [
            advance_location(planet, velocity, accel, 1)
            for planet, velocity, accel in zip(planets, velocities, accels)
        ]
        new_velocities = [
            advance_velocity(velocity, accel, 1)
            for velocity, accel in zip(velocities, accels)
        ]
    else:
        new_planets = [
            advance_location(planet, velocity, accel, min_contact)
            for planet, velocity, accel in zip(planets, velocities, accels)
        ]
        new_velocities = [
            advance_velocity(velocity, accel, min_contact)
            for velocity, accel in zip(velocities, accels)
        ]
    return new_planets, new_velocities, 1 if min_contact == 0 else min_contact


def run(planets: list[Coords], steps: int) -> tuple[list[Coords], list[Coords]]:
    velocities: list[tuple[int, int, int]] = [(0, 0, 0) for _ in planets]
    for _ in range(steps):
        planets = compute_velocity(planets, velocities)
    return planets, velocities


def meet_step(
    planet: Coords, velocity: Coords, accel: Coords, init_planet: Coords
) -> int | None:
    x_contact = find_contact((planet[0], velocity[0], accel[0]), (init_planet[0], 0, 0))
    y_contact = find_contact((planet[1], velocity[1], accel[1]), (init_planet[1], 0, 0))
    z_contact = find_contact((planet[2], velocity[2], accel[2]), (init_planet[2], 0, 0))
    if x_contact is not None and y_contact is not None and z_contact is not None:
        if x_contact == y_contact == z_contact:
            return x_contact


def check_stop(
    planets: list[Coords],
    init_planets: list[Coords],
    velocities: list[Coords],
    init_velocities: list[Coords],
) -> int | None:
    accels = compute_accels(planets)
    meet_times: list[int | None] = []
    for idx, planet in enumerate(planets):
        meet = meet_step(planet, velocities[idx], accels[idx], init_planets[idx])
        meet_times.append(meet)
    if all(meet is not None for meet in meet_times):
        meet0 = meet_times[0]
        if all(meet0 == meet for meet in meet_times):
            return meet0


def run_forever(planets: list[Coords]) -> int:
    velocities: list[Coords] = [(0, 0, 0) for _ in planets]
    copy = velocities[:]
    steps = 0
    init_planets = planets[:]
    while True:
        new_planets, new_velocities, timesteps = advance(planets, velocities)
        if steps > 0:
            to_stop = check_stop(planets, init_planets, velocities, copy)
            if to_stop is not None:
                steps += to_stop
                break
        steps += timesteps
        planets = new_planets
        velocities = new_velocities
    return steps + 1


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
    planets_after, velocities = run(planets, 1000)
    energy = compute_energy(planets_after, velocities)
    print(energy)

    timesteps = run_forever(planets)
    print(timesteps)
