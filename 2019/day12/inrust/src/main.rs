use std::vec::Vec;
use std::cmp::Ordering;
use std::fmt::Debug;
use std::iter::repeat;
use itertools::Itertools;


#[derive(Debug, PartialEq, Eq, Clone)]
struct Planet {
    x: i32,
    y: i32,
    z: i32
}

#[derive(Debug, PartialEq, Eq, Clone)]
struct Velocity {
    x: i32,
    y: i32,
    z: i32
}

#[derive(Debug)]
struct Accel {
    x: i32,
    y: i32,
    z: i32
}

fn compute_collision(pos: i32, other: i32, vel: i32, vother: i32, accel: i32, aother: i32) -> Option<u32> {
    let alpha = (accel - aother) as f64 / 2.0;
    let beta = (vel - vother) as f64 + (accel - aother) as f64 / 2.0;
    let gamma = (pos - other) as f64;
    let delta = beta * beta - 4.0 * alpha * gamma;  // assume delta is always non-negative
    if delta < 0.0 {
        return None
    }
    // assume that the two are not in the same location. pos /= other
    let tau1 = (-beta + delta.sqrt()) / (2.0 * alpha);
    let tau2 = (-beta - delta.sqrt()) / (2.0 * alpha);
    if tau1 > 0.0 && tau2 > 0.0 && tau1 <= tau2 {
        Some(tau1.ceil() as u32)
    } else if tau1 > 0.0 && tau2 > 0.0 && tau1 > tau2 {
        Some(tau2.ceil() as u32)
    } else if tau1 > 0.0 {
        Some(tau1.ceil() as u32)
    } else if tau2 > 0.0 {
        Some(tau2.ceil() as u32)
    } else {
        None
    }
}

fn check_collisions(planets: &Vec<i32>, velocities: &Vec<i32>, accels: &Vec<i32>) -> Option<(u32, usize, usize)> {
    let mut shortest: Option<(u32, usize, usize)> = None;
    for ((idx, planet), (jdx, other)) in planets.iter().enumerate().combinations(2).map(|v| (v[0],v[1])){
        let collision = compute_collision(*planet, *other, velocities[idx], velocities[jdx], accels[idx], accels[jdx]);
        match (shortest, collision) {
            (None, None) => (),
            (None, Some(t_)) => shortest = Some((t_, idx, jdx)),
            (Some(_), None) => (),
            (Some((t, _, _)), Some(t_)) => if t > t_ {shortest = Some((t_, idx, jdx))} else {()}
        };
    }
    shortest
}

// It should jump to each collision event and advance all locations, velocities and accelerations. Note accelerations should be changed only if there is a collision.
// It is possible that we have multiple collisions in a timestep and we have to update more than one, so it is useful to compute the locations for all.
// The problem is we may jump over the initial conditions, so we will never count the period of the universe.
fn jump() {
    // maybe add a check for each step whether all velocities become zero whithin the jump interval. 
}

fn compute_acceleration(planet: &Planet, planets: &Vec<Planet>) -> Accel {
    let mut accel = Accel {x: 0, y: 0, z: 0};
    for other in planets {
        match planet.x.cmp(&other.x) {
            Ordering::Less => accel.x += 1,
            Ordering::Greater => accel.x -= 1,
            Ordering::Equal => ()
        };
        match planet.y.cmp(&other.y) {
            Ordering::Less => accel.y += 1,
            Ordering::Greater => accel.y -= 1,
            Ordering::Equal => ()
        };
        match planet.z.cmp(&other.z) {
            Ordering::Less => accel.z += 1,
            Ordering::Greater => accel.z -= 1,
            Ordering::Equal => ()
        };
    }
    accel
}

fn compute_velocity(planets: &Vec<Planet>, velocities: &mut Vec<Velocity>) {
    for (planet, velocity) in planets.iter().zip(velocities) {
        let accel = compute_acceleration(planet, planets);
        velocity.x += accel.x;
        velocity.y += accel.y;
        velocity.z += accel.z;
    }
}

fn run_step(planets: &Vec<Planet>, velocities: &mut Vec<Velocity>) -> Vec<Planet> {
    let mut new_planets = Vec::new();
    compute_velocity(planets, velocities);
    for (planet, velocity) in planets.iter().zip(velocities) {
        let new_planet = Planet {
            x: planet.x + velocity.x,
            y: planet.y + velocity.y, 
            z: planet.z + velocity.z 
        };
        new_planets.push(new_planet)
    }
    new_planets
}

fn run(planets_init: &Vec<Planet>) -> u64 {
    let velocities_init: Vec<Velocity> = repeat(Velocity {x: 0, y: 0, z: 0}).take(planets_init.len()).collect();
    let mut steps: u64 = 1;
    let mut planets = planets_init.clone();
    let mut velocities = velocities_init.clone();
    loop {
        planets = run_step(&planets, &mut velocities);
        if (&planets == planets_init) && (velocities == velocities_init) {
            break steps
        }
        else {
            steps += 1;
        }
    }
}

fn main() {
    let planets = Vec::from([
        Planet {x: -1, y: 0, z: 2},
        Planet {x: 2, y: -10, z: -7},
        Planet {x: 4, y: -8, z: 8},
        Planet {x: 3, y: 5, z: -1}
    ]);
    let steps = run(&planets);
    println!("Total steps until repeat of the universe = {steps}");

    let planets = Vec::from([
        Planet {x: 3, y: -6, z: 6},
        Planet {x: 10, y: 7, z: -9},
        Planet {x: -3, y: -7, z: 9},
        Planet {x: -8, y: 0, z: 4}
    ]);
    let steps = run(&planets);
    println!("Total steps until repeat of the universe = {steps}");
}
